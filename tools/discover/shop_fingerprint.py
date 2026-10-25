#!/usr/bin/env python3
"""低并发读取首页，判断公开 AI 卡网/发卡系统指纹。

只保存域名、状态、标题和命中词，不保存页面正文、Cookie、跳转路径或查询参数。
这是候选筛选，不等于确认在售；确认后的卡网应走 data/shops/ 的独立流程。
"""
import argparse
import concurrent.futures as cf
import datetime
import html
import ipaddress
import json
import re
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ai-relay-atlas-shop-fingerprint/0.1',
      'Accept': 'text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8'}
TITLE = re.compile(r'<title[^>]*>(.*?)</title>', re.I | re.S)
SYSTEM_SIGS = {
    '独角数卡': ('dujiaoka', '/assets/dujiaoka', '自动发卡系统'),
    '异次元发卡': ('acg-faka', 'acgfaka', '异次元发卡'),
    'ZFAKA': ('zfaka', '/theme/default/'),
    '萌次元': ('萌次元', 'mcy.im'),
    'ACE云寄售': ('aceyun', 'ace云寄售'),
    '云猫寄售': ('catfk', '云猫寄售'),
}
COMMON = ('自动发货', '自动发卡', '发卡网', '发卡', '卡密', '寄售', '虚拟商品',
          '在线购买', '购物车', '商品列表', '卡券', '充值卡')
AI = ('chatgpt', 'gpt plus', 'claude', 'gemini', 'grok', 'cursor', 'codex',
      'openai', 'midjourney', 'api key', '大模型', 'ai模型', '人工智能')


def hosts_from_input(path):
    out = set()
    for line in open(path, encoding='utf-8', errors='replace'):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
            host = str(obj.get('domain') or '').strip().lower()
        except (ValueError, AttributeError):
            host = line.split()[0].lower()
        if host:
            out.add(host)
    return sorted(out)


def text_body(raw):
    # HTML 标签不影响关键词匹配，但压缩长度，避免把响应保存到结果。
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', raw))).lower()[:200000]


def classify(body, title):
    hay = (title + ' ' + body).lower()
    systems = [name for name, words in SYSTEM_SIGS.items() if any(w.lower() in hay for w in words)]
    common = sorted({w for w in COMMON if w.lower() in hay})
    ai = sorted({w for w in AI if w.lower() in hay})
    if systems:
        level = 'high'
    elif len(common) >= 2 and ai:
        level = 'high'
    elif common and ai:
        level = 'medium'
    elif common:
        level = 'low'
    else:
        level = ''
    return systems, common, ai, level


def safe_host(value):
    host = (value or '').lower()
    try:
        ipaddress.ip_address(host)
    except ValueError:
        return host
    return ''


def fetch(host):
    base = dict(domain=host, checked=datetime.date.today().isoformat(), status=None,
                final_host='', latency_ms=None, title='', systems=[], common_hits=[],
                ai_hits=[], likelihood='', reachable=False, error_class='')
    for scheme in ('https', 'http'):
        t0 = time.monotonic()
        try:
            req = urllib.request.Request('%s://%s/' % (scheme, host), headers=UA)
            with urllib.request.urlopen(req, timeout=8, context=CTX) as resp:
                raw = resp.read(128 * 1024).decode('utf-8', 'replace')
                m = TITLE.search(raw)
                title = re.sub(r'\s+', ' ', html.unescape(m.group(1))).strip()[:200] if m else ''
                systems, common, ai, level = classify(text_body(raw), title)
                final = urllib.parse.urlsplit(resp.geturl())
                base.update(status=int(resp.status), final_host=safe_host(final.hostname),
                            latency_ms=round((time.monotonic() - t0) * 1000), title=title,
                            systems=systems, common_hits=common, ai_hits=ai,
                            likelihood=level, reachable=True, error_class='')
                return base
        except urllib.error.HTTPError as exc:
            final = urllib.parse.urlsplit(getattr(exc, 'url', '') or '')
            base.update(status=int(exc.code), final_host=safe_host(final.hostname),
                        latency_ms=round((time.monotonic() - t0) * 1000), reachable=True,
                        error_class='HTTPError')
            return base
        except Exception as exc:
            base['error_class'] = type(exc).__name__
    return base


def main():
    ap = argparse.ArgumentParser(description='首页卡网指纹筛选')
    ap.add_argument('input')
    ap.add_argument('--out', default='/tmp/shop-fingerprint-candidates.jsonl')
    ap.add_argument('--workers', type=int, default=16)
    args = ap.parse_args()
    hosts = hosts_from_input(args.input)
    rows = []
    with cf.ThreadPoolExecutor(max_workers=max(1, min(args.workers, 32))) as ex:
        jobs = [ex.submit(fetch, h) for h in hosts]
        for i, job in enumerate(cf.as_completed(jobs), 1):
            rows.append(job.result())
            if i % 100 == 0 or i == len(jobs):
                print('进度 %d/%d' % (i, len(jobs)), flush=True)
    rows.sort(key=lambda x: x['domain'])
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open('w', encoding='utf-8') as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + '\n')
    print('完成：%d；可达：%d；中高置信：%d；系统指纹：%d；等级：%s' % (
        len(rows), sum(x['reachable'] for x in rows),
        sum(x['likelihood'] in ('medium', 'high') for x in rows),
        sum(bool(x['systems']) for x in rows),
        ', '.join('%s=%d' % x for x in Counter(x['likelihood'] or 'none' for x in rows).most_common())))


if __name__ == '__main__':
    main()
