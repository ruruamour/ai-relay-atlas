#!/usr/bin/env python3
"""从 Bing 公共搜索结果提取 AI 中转站/卡网候选域名。

只读取搜索结果页中的公开链接和标题，不自动打开搜索结果，不保存路径、
查询参数或正文；搜索结果仅作候选来源，后续仍需低并发公开验证。
"""
import argparse
import base64
import html
import json
import re
import time
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from relay_search import normalize_host  # noqa: E402

QUERIES = [
    '"AI中转站"',
    '"API中转站" 价格',
    '"AI API中转站" Gemini Claude',
    '"New API" "api/pricing"',
    '"Sub2API" "model-plaza"',
    '"发卡网" ChatGPT Claude',
    '"独角数卡" AI',
    '"异次元发卡" AI',
    '"ChatGPT" "Claude" "Gemini" 充值',
    '"AI订阅充值" API',
    '"AI API gateway" 充值',
    '"Gemini API" "充值"',
]
UA = 'ai-relay-atlas-bing-harvest/0.1'
SKIP = {'bing.com', 'microsoft.com', 'yahoo.com', 'google.com', 'baidu.com'}


def decode_link(href):
    href = html.unescape(href)
    try:
        p = urllib.parse.urlsplit(href)
        q = urllib.parse.parse_qs(p.query)
        encoded = q.get('u', [''])[0]
        if encoded.startswith('a1'):
            raw = encoded[2:]
            raw += '=' * (-len(raw) % 4)
            return base64.urlsafe_b64decode(raw).decode('utf-8', 'replace')
    except Exception:
        pass
    return href


def search(query):
    url = 'https://www.bing.com/search?q=%s&count=10&setlang=en-US&cc=us' % urllib.parse.quote(query)
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    })
    with urllib.request.urlopen(req, timeout=45) as resp:
        text = resp.read().decode('utf-8', 'replace')
    found = defaultdict(set)
    for block in re.findall(r'<li class="b_algo".*?</li>', text, re.I | re.S):
        anchors = re.findall(r'<a[^>]+href=["\']([^"\']+)', block, re.I)
        if not anchors:
            continue
        link = decode_link(anchors[0])
        host = normalize_host(link)
        if not host or host in SKIP:
            continue
        titles = re.findall(r'<h2[^>]*>(.*?)</h2>', block, re.I | re.S)
        title = re.sub(r'<[^>]+>', ' ', html.unescape(titles[0])) if titles else ''
        title = ' '.join(title.split())[:200]
        found[host].add(title)
    return found


def main():
    ap = argparse.ArgumentParser(description='Bing 公共搜索候选收集')
    ap.add_argument('--out', default='/tmp/web-search-candidates.jsonl')
    ap.add_argument('--domains', default='/tmp/web-search-domains.txt')
    ap.add_argument('--delay', type=float, default=2.0)
    args = ap.parse_args()
    all_found = defaultdict(lambda: {'queries': set(), 'titles': set()})
    for i, query in enumerate(QUERIES, 1):
        try:
            found = search(query)
            for host, titles in found.items():
                all_found[host]['queries'].add(query)
                all_found[host]['titles'].update(titles)
            print('query %d/%d：%d hosts，累计 %d' %
                  (i, len(QUERIES), len(found), len(all_found)), file=sys.stderr, flush=True)
        except Exception as exc:
            print('Bing 搜索失败 %r：%s' % (query, exc), file=sys.stderr)
        time.sleep(max(0, args.delay))
    out = Path(args.out); domains = Path(args.domains)
    out.parent.mkdir(parents=True, exist_ok=True); domains.parent.mkdir(parents=True, exist_ok=True)
    with out.open('w', encoding='utf-8') as fh, domains.open('w', encoding='utf-8') as dh:
        for host in sorted(all_found):
            r = all_found[host]
            fh.write(json.dumps(dict(domain=host, source='bing', source_queries=sorted(r['queries']),
                                     titles=sorted(r['titles'])), ensure_ascii=False) + '\n')
            dh.write(host + '\n')
    print('完成：%d 个候选；JSONL：%s；域名：%s' % (len(all_found), out, domains))


if __name__ == '__main__':
    main()
