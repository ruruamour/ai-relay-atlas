#!/usr/bin/env python3
"""从 npm 公共包索引的描述/README 提取 AI 中转站候选域名。

只读取 npm 的公开搜索和包元数据，不安装包、不执行代码、不保存 README
正文；结果保留包名、版本和搜索词来源。
"""
import argparse
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
    'keywords:sub2api', '"sub2api"', 'keywords:ai-relay',
    'keywords:api-relay', 'keywords:openai-proxy', 'keywords:gemini-proxy',
    'keywords:claude-proxy', 'keywords:one-api', 'keywords:new-api',
    'keywords:ai-api', 'keywords:dujiaoka',
]
UA = 'ai-relay-atlas-npm-harvest/0.1'


def get_json(url, timeout=45):
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'application/json'})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())


def search(query, size):
    url = 'https://registry.npmjs.org/-/v1/search?text=%s&size=%d' % (
        urllib.parse.quote(query), min(size, 250))
    try:
        return get_json(url).get('objects') or []
    except Exception as exc:
        print('npm 搜索失败 %r：%s' % (query, exc), file=sys.stderr)
        return []


def package_metadata(name):
    # npm 包名中的 @ 和 / 是路径的一部分，其他字符按 URL 编码。
    url = 'https://registry.npmjs.org/' + urllib.parse.quote(name, safe='@/')
    try:
        return get_json(url, timeout=45)
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser(description='npm 公共包索引候选收集')
    ap.add_argument('--out', default='/tmp/npm-candidates.jsonl')
    ap.add_argument('--domains', default='/tmp/npm-domains.txt')
    ap.add_argument('--size', type=int, default=50)
    ap.add_argument('--delay', type=float, default=0.3)
    args = ap.parse_args()

    packages = {}
    for query in QUERIES:
        for obj in search(query, args.size):
            p = obj.get('package') or {}
            name = p.get('name')
            if name:
                packages.setdefault(name, set()).add(query)
        time.sleep(max(0, args.delay))
    print('npm 包：%d' % len(packages), file=sys.stderr)

    sources = defaultdict(set)
    for i, (name, queries) in enumerate(sorted(packages.items()), 1):
        meta = package_metadata(name)
        if not meta:
            continue
        latest = (meta.get('dist-tags') or {}).get('latest', '')
        fields = [meta.get('description'), meta.get('readme'), meta.get('homepage')]
        repo = meta.get('repository')
        if isinstance(repo, dict):
            fields.extend([repo.get('url'), repo.get('directory')])
        elif repo:
            fields.append(repo)
        bugs = meta.get('bugs')
        if isinstance(bugs, dict):
            fields.append(bugs.get('url'))
        text = '\n'.join(str(x) for x in fields if x)
        source = 'npm:%s@%s [%s]' % (name, latest, '|'.join(sorted(queries)))
        for host in hosts_in_text(text):
            sources[host].add(source)
        if i % 50 == 0:
            print('元数据 %d/%d，候选 %d' % (i, len(packages), len(sources)), file=sys.stderr, flush=True)
        time.sleep(max(0, args.delay / 2))

    out = Path(args.out); domains = Path(args.domains)
    out.parent.mkdir(parents=True, exist_ok=True); domains.parent.mkdir(parents=True, exist_ok=True)
    with out.open('w', encoding='utf-8') as fh, domains.open('w', encoding='utf-8') as dh:
        for host in sorted(sources):
            fh.write(json.dumps(dict(domain=host, source='npm', source_files=sorted(sources[host])),
                                ensure_ascii=False) + '\n')
            dh.write(host + '\n')
    print('完成：%d 个候选；JSONL：%s；域名：%s' % (len(sources), out, domains))


if __name__ == '__main__':
    main()
