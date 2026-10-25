#!/usr/bin/env python3
"""从 Docker Hub 公共镜像搜索和描述提取 AI 中转站候选域名。

只读取公开镜像的描述元数据，不拉取镜像、不执行容器、不保存描述正文；
候选保留镜像名和搜索词来源。
"""
import argparse
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from relay_search import hosts_in_text  # noqa: E402

QUERIES = [
    'new-api', 'sub2api', 'one-api', 'dujiaoka', 'acg-faka',
    'ai api proxy', 'openai proxy', 'gemini proxy', 'claude proxy',
    'ai gateway', 'faka', 'model plaza',
]
UA = 'ai-relay-atlas-dockerhub-harvest/0.1'


def get_json(url, timeout=45):
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'application/json'})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())


def search(query, size):
    url = 'https://hub.docker.com/v2/search/repositories/?query=%s&page_size=%d' % (
        urllib.parse.quote(query), min(size, 100))
    try:
        return get_json(url).get('results') or []
    except Exception as exc:
        print('Docker Hub 搜索失败 %r：%s' % (query, exc), file=sys.stderr)
        return []


def details(repo):
    try:
        return get_json('https://hub.docker.com/v2/repositories/%s/' % repo)
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser(description='Docker Hub 公共镜像元数据收集')
    ap.add_argument('--out', default='/tmp/docker-hub-candidates.jsonl')
    ap.add_argument('--domains', default='/tmp/docker-hub-domains.txt')
    ap.add_argument('--size', type=int, default=25)
    ap.add_argument('--delay', type=float, default=0.35)
    args = ap.parse_args()

    images = {}
    for query in QUERIES:
        for item in search(query, args.size):
            repo = item.get('repo_name')
            if repo:
                images.setdefault(repo, set()).add(query)
        time.sleep(max(0, args.delay))
    print('Docker 镜像：%d' % len(images), file=sys.stderr)

    sources = defaultdict(set)
    for i, (repo, queries) in enumerate(sorted(images.items()), 1):
        obj = details(repo)
        if obj:
            text = '\n'.join(str(x) for x in (
                obj.get('description'), obj.get('full_description'), obj.get('source')) if x)
            source = 'docker:%s [%s]' % (repo, '|'.join(sorted(queries)))
            for host in hosts_in_text(text):
                sources[host].add(source)
        if i % 50 == 0:
            print('元数据 %d/%d，候选 %d' % (i, len(images), len(sources)), file=sys.stderr, flush=True)
        time.sleep(max(0, args.delay / 2))

    out = Path(args.out); domains = Path(args.domains)
    out.parent.mkdir(parents=True, exist_ok=True); domains.parent.mkdir(parents=True, exist_ok=True)
    with out.open('w', encoding='utf-8') as fh, domains.open('w', encoding='utf-8') as dh:
        for host in sorted(sources):
            fh.write(json.dumps(dict(domain=host, source='docker-hub', source_files=sorted(sources[host])),
                                ensure_ascii=False) + '\n')
            dh.write(host + '\n')
    print('完成：%d 个候选；JSONL：%s；域名：%s' % (len(sources), out, domains))


if __name__ == '__main__':
    main()
