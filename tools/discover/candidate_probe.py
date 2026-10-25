#!/usr/bin/env python3
"""低并发探活候选域名，只访问首页公开 GET。

输入可以是每行一个域名，也可以是 github_harvest.py 生成的 JSONL。
不会登录、提交表单、调用推理接口或猜测 API 路径。

用法：
  python3 tools/discover/candidate_probe.py \
      /tmp/github-domains.txt --out /tmp/github-probe.jsonl --live-out /tmp/github-live.txt
"""
import argparse
import concurrent.futures as cf
import datetime
import html
import ipaddress
import json
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ai-relay-atlas-candidate-probe/0.1',
      'Accept': 'text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8'}
TITLE = re.compile(r'<title[^>]*>(.*?)</title>', re.I | re.S)


def read_candidates(path):
    rows = {}
    with open(path, encoding='utf-8', errors='replace') as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                host = str(obj.get('domain') or '').strip().lower()
                source_files = obj.get('source_files') or []
            except (ValueError, AttributeError):
                host, source_files = line.split()[0].lower(), []
            if host:
                rows.setdefault(host, set()).update(source_files)
    return rows


def safe_host(value):
    host = (value or '').lower()
    try:
        ipaddress.ip_address(host)
    except ValueError:
        return host
    return ''


def probe(host, source_files):
    rec = dict(domain=host, source_files=sorted(source_files), checked=datetime.date.today().isoformat(),
               status=None, final_host='', latency_ms=None, title='', reachable=False, error='')
    for scheme in ('https', 'http'):
        t0 = time.monotonic()
        try:
            req = urllib.request.Request('https://%s/' % host if scheme == 'https' else 'http://%s/' % host,
                                         headers=UA)
            with urllib.request.urlopen(req, timeout=8, context=CTX) as resp:
                body = resp.read(65536).decode('utf-8', 'replace')
                m = TITLE.search(body)
                title = html.unescape(re.sub(r'\s+', ' ', m.group(1)).strip())[:200] if m else ''
                final = urllib.parse.urlsplit(resp.geturl())
                rec.update(status=int(resp.status), final_host=safe_host(final.hostname),
                           latency_ms=round((time.monotonic() - t0) * 1000), title=title,
                           reachable=True, error='')
                return rec
        except urllib.error.HTTPError as exc:
            # 401/403/405/429 也说明主机可达，保留给后续人工判断。
            final = urllib.parse.urlsplit(getattr(exc, 'url', '') or '')
            rec.update(status=int(exc.code), final_host=safe_host(final.hostname),
                       latency_ms=round((time.monotonic() - t0) * 1000), reachable=True,
                       error=str(exc.reason)[:160])
            return rec
        except Exception as exc:
            rec['error'] = (type(exc).__name__ + ': ' + str(exc))[:160]
    return rec


def main():
    ap = argparse.ArgumentParser(description='低并发探活候选域名')
    ap.add_argument('input')
    ap.add_argument('--out', default='/tmp/candidate-probe.jsonl')
    ap.add_argument('--live-out', help='输出 2xx/3xx 域名清单')
    ap.add_argument('--workers', type=int, default=8)
    args = ap.parse_args()
    candidates = read_candidates(args.input)
    result = []
    with cf.ThreadPoolExecutor(max_workers=max(1, min(args.workers, 32))) as ex:
        jobs = [ex.submit(probe, host, source) for host, source in candidates.items()]
        for i, job in enumerate(cf.as_completed(jobs), 1):
            result.append(job.result())
            if i % 100 == 0 or i == len(jobs):
                print('进度 %d/%d' % (i, len(jobs)), file=sys.stderr, flush=True)
    result.sort(key=lambda x: x['domain'])
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open('w', encoding='utf-8') as fh:
        for row in result:
            fh.write(json.dumps(row, ensure_ascii=False) + '\n')
    if args.live_out:
        live = Path(args.live_out)
        live.parent.mkdir(parents=True, exist_ok=True)
        with live.open('w', encoding='utf-8') as fh:
            for row in result:
                if isinstance(row['status'], int) and 200 <= row['status'] < 400:
                    fh.write(row['domain'] + '\n')
    counts = Counter(str(x['status']) if x['status'] is not None else 'error' for x in result)
    print('完成：%d；可达：%d；2xx/3xx：%d；状态：%s' %
          (len(result), sum(x['reachable'] for x in result),
           sum(isinstance(x['status'], int) and 200 <= x['status'] < 400 for x in result),
           ', '.join('%s=%d' % x for x in counts.most_common())))


if __name__ == '__main__':
    main()
