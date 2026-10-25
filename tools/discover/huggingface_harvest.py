#!/usr/bin/env python3
"""从 Hugging Face 公共 Space README 提取 AI 中转站候选域名。

只读取公开 Space 搜索结果和 README，不运行 Space、不调用推理接口、不保存
README 正文；结果保留 Space 和搜索词来源。
"""
import argparse
import concurrent.futures as cf
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from relay_search import hosts_in_text  # noqa: E402

QUERIES = [
    'new-api', 'sub2api', 'one-api', 'openai proxy', 'gemini proxy',
    'claude proxy', 'ai gateway', 'api relay', 'llm gateway', 'chatgpt api',
    'AI中转', '发卡网',
]
UA = 'ai-relay-atlas-huggingface-harvest/0.1'
MAX_BYTES = 1_500_000


def get_json(url, timeout=45):
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'application/json'})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())


def search(query, limit):
    url = 'https://huggingface.co/api/spaces?search=%s&limit=%d' % (
        urllib.parse.quote(query), min(limit, 100))
    try:
        return get_json(url)
    except Exception as exc:
        print('Hugging Face 搜索失败 %r：%s' % (query, exc), file=sys.stderr)
        return []


def fetch_readme(space):
    name = space.get('id') or ''
    if not name or '/' not in name:
        return space, ''
    url = 'https://huggingface.co/spaces/%s/raw/main/README.md' % urllib.parse.quote(name, safe='/')
    try:
        req = urllib.request.Request(url, headers={'User-Agent': UA})
        with urllib.request.urlopen(req, timeout=45) as resp:
            body = resp.read(MAX_BYTES + 1)
        if len(body) > MAX_BYTES:
            return space, ''
        return space, body.decode('utf-8', 'replace')
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError):
        return space, ''


def main():
    ap = argparse.ArgumentParser(description='Hugging Face Spaces 公共 README 收集')
    ap.add_argument('--out', default='/tmp/huggingface-candidates.jsonl')
    ap.add_argument('--domains', default='/tmp/huggingface-domains.txt')
    ap.add_argument('--limit', type=int, default=30)
    ap.add_argument('--workers', type=int, default=4)
    ap.add_argument('--delay', type=float, default=0.5)
    args = ap.parse_args()

    spaces = {}
    for query in QUERIES:
        for space in search(query, args.limit):
            if space.get('id'):
                spaces.setdefault(space['id'], set()).add(query)
        time.sleep(max(0, args.delay))
    print('Hugging Face Spaces：%d' % len(spaces), file=sys.stderr)

    sources = defaultdict(set)
    items = list(spaces.items())
    with cf.ThreadPoolExecutor(max_workers=max(1, min(args.workers, 8))) as ex:
        for i, (space, text) in enumerate(ex.map(lambda x: fetch_readme({'id': x[0]}), items), 1):
            if text:
                queries = spaces[space.get('id', '')]
                source = 'hf-space:%s [ %s ]' % (space.get('id'), '|'.join(sorted(queries)))
                for host in hosts_in_text(text):
                    sources[host].add(source)
            if i % 50 == 0:
                print('README %d/%d，候选 %d' % (i, len(items), len(sources)), file=sys.stderr, flush=True)

    out = Path(args.out); domains = Path(args.domains)
    out.parent.mkdir(parents=True, exist_ok=True); domains.parent.mkdir(parents=True, exist_ok=True)
    with out.open('w', encoding='utf-8') as fh, domains.open('w', encoding='utf-8') as dh:
        for host in sorted(sources):
            fh.write(json.dumps(dict(domain=host, source='huggingface', source_files=sorted(sources[host])),
                                ensure_ascii=False) + '\n')
            dh.write(host + '\n')
    print('完成：%d 个候选；JSONL：%s；域名：%s' % (len(sources), out, domains))


if __name__ == '__main__':
    main()
