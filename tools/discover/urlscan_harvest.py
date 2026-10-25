#!/usr/bin/env python3
"""从 urlscan.io 公共搜索索引提取 AI 中转站/卡网域名。

只读取公开搜索结果，不提交扫描、不访问目标站、不保存 IP/端口/原始 URL
路径。urlscan 结果只是被动索引证据，后续仍需本项目的低并发公开页面验证。
"""
import argparse
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
    'page.title:"New API"',
    'page.title:"New-API"',
    'page.title:"One API"',
    'page.title:"One-API"',
    'page.title:"Sub2API"',
    'page.title:"AI API Gateway"',
    'page.title:"AI Gateway"',
    'page.title:"AI API"',
    'page.title:"OpenAI API"',
    'page.title:"Gemini API"',
    'page.title:"Claude API"',
    'page.title:"模型广场"',
    'page.title:"模型API"',
    'page.title:"API中转"',
    'page.title:"AI中转"',
    'page.title:"发卡网"',
    'page.title:"自动发货"',
    'page.title:"卡密"',
    'page.title:"AI订阅"',
    'page.title:"ChatGPT" AND page.title:API',
    'page.title:"Claude" AND page.title:API',
]
UA = 'ai-relay-atlas-urlscan-harvest/0.1'


def search(query):
    url = 'https://urlscan.io/api/v1/search/?q=' + urllib.parse.quote(query)
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'application/json'})
    with urllib.request.urlopen(req, timeout=45) as resp:
        return json.loads(resp.read())


def extract(query, data):
    found = defaultdict(lambda: {'queries': set(), 'titles': set(), 'statuses': set(), 'last_seen': ''})
    for item in data.get('results') or []:
        page = item.get('page') or {}
        task = item.get('task') or {}
        host = normalize_host(page.get('domain') or task.get('domain') or '')
        if not host:
            continue
        rec = found[host]
        rec['queries'].add(query)
        if page.get('title'):
            rec['titles'].add(str(page['title'])[:200])
        if page.get('status') is not None:
            rec['statuses'].add(str(page['status']))
        if task.get('time') and task['time'] > rec['last_seen']:
            rec['last_seen'] = task['time']
    return found


def main():
    ap = argparse.ArgumentParser(description='urlscan.io 公共搜索索引收集')
    ap.add_argument('--out', default='/tmp/urlscan-candidates.jsonl')
    ap.add_argument('--domains', default='/tmp/urlscan-domains.txt')
    ap.add_argument('--delay', type=float, default=1.0)
    args = ap.parse_args()
    all_found = defaultdict(lambda: {'queries': set(), 'titles': set(), 'statuses': set(), 'last_seen': ''})
    for i, query in enumerate(QUERIES, 1):
        try:
            data = search(query)
            found = extract(query, data)
            for host, rec in found.items():
                all_found[host]['queries'].update(rec['queries'])
                all_found[host]['titles'].update(rec['titles'])
                all_found[host]['statuses'].update(rec['statuses'])
                all_found[host]['last_seen'] = max(all_found[host]['last_seen'], rec['last_seen'])
            print('query %d/%d: %d results, %d hosts, total %d' %
                  (i, len(QUERIES), len(data.get('results') or []), len(found), len(all_found)),
                  file=sys.stderr, flush=True)
        except Exception as exc:
            print('query failed %r: %s' % (query, exc), file=sys.stderr)
        time.sleep(max(0, args.delay))
    out = Path(args.out); domains = Path(args.domains)
    out.parent.mkdir(parents=True, exist_ok=True); domains.parent.mkdir(parents=True, exist_ok=True)
    with out.open('w', encoding='utf-8') as fh, domains.open('w', encoding='utf-8') as dh:
        for host in sorted(all_found):
            r = all_found[host]
            row = dict(domain=host, source='urlscan', source_queries=sorted(r['queries']),
                       titles=sorted(r['titles']), statuses=sorted(r['statuses']), last_seen=r['last_seen'])
            fh.write(json.dumps(row, ensure_ascii=False) + '\n')
            dh.write(host + '\n')
    print('完成：%d 个候选；JSONL：%s；域名：%s' % (len(all_found), out, domains))


if __name__ == '__main__':
    main()
