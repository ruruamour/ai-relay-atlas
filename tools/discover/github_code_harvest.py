#!/usr/bin/env python3
"""从 GitHub 代码搜索结果提取 AI 中转站/卡网候选域名。

代码搜索比仓库搜索噪声更大，因此只读取搜索命中的小型文本文件，
不执行代码、不保存正文；输出保留 query、仓库、文件和 commit 来源。
"""
import argparse
import base64
import concurrent.futures as cf
import json
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from relay_search import hosts_in_text  # noqa: E402

QUERIES = [
    'api/pricing',
    'model-plaza',
    '/api/v1/settings/public',
    'New-API',
    'Sub2API',
    'dujiaoka',
    'acg-faka',
    'AI中转站',
    '发卡网',
    '自动发货',
]
TEXT_EXTS = {'.md', '.markdown', '.txt', '.csv', '.json', '.yaml', '.yml', '.html', '.htm'}
UA = 'ai-relay-atlas-github-code-harvest/0.1'
MAX_BYTES = 1_500_000


def gh(*args, timeout=90):
    p = subprocess.run(['gh', *args], capture_output=True, text=True, timeout=timeout)
    if p.returncode != 0:
        raise RuntimeError((p.stderr or p.stdout).strip()[:300])
    return p.stdout


def search_code(query, limit):
    try:
        raw = gh('search', 'code', query, '--limit', str(limit), '--match', 'file', '--json',
                 'path,repository,sha')
        out = []
        for x in json.loads(raw):
            repo = (x.get('repository') or {}).get('nameWithOwner')
            path = x.get('path') or ''
            sha = x.get('sha') or ''
            if repo and path and sha and Path(path).suffix.lower() in TEXT_EXTS:
                out.append(dict(repo=repo, path=path, sha=sha, query=query))
        return out
    except Exception as exc:
        print('GitHub 代码搜索失败 %r：%s' % (query, exc), file=sys.stderr)
        return []


def fetch(rec):
    # code search 返回的是 blob SHA，不是分支/commit ref；用 GitHub blob API 读取正文。
    try:
        encoded = gh('api', 'repos/%s/git/blobs/%s' % (rec['repo'], rec['sha']),
                     '--jq', '.content', timeout=45)
        body = base64.b64decode(encoded, validate=False)
    except Exception:
        return rec, ''
    if len(body) > MAX_BYTES:
        return rec, ''
    return rec, body.decode('utf-8', 'replace')


def save_checkpoint(path, done_queries, sources):
    tmp = Path(str(path) + '.tmp')
    tmp.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_text(json.dumps(dict(done_queries=sorted(done_queries),
                                   sources={k: sorted(v) for k, v in sources.items()}),
                              ensure_ascii=False), encoding='utf-8')
    os.replace(tmp, path)


def main():
    ap = argparse.ArgumentParser(description='GitHub 代码搜索候选收集')
    ap.add_argument('--out', default='/tmp/github-code-candidates.jsonl')
    ap.add_argument('--domains', default='/tmp/github-code-domains.txt')
    ap.add_argument('--checkpoint', default='/tmp/github-code-harvest.checkpoint.json')
    ap.add_argument('--limit', type=int, default=40, help='每个搜索词最多取多少文件')
    ap.add_argument('--workers', type=int, default=4)
    ap.add_argument('--fresh', action='store_true')
    args = ap.parse_args()

    checkpoint = Path(args.checkpoint)
    done_queries, all_sources = set(), defaultdict(set)
    if checkpoint.exists() and not args.fresh:
        try:
            saved = json.loads(checkpoint.read_text(encoding='utf-8'))
            done_queries = set(saved.get('done_queries') or [])
            for host, srcs in (saved.get('sources') or {}).items():
                all_sources[host].update(srcs)
            print('从断点恢复：query %d，候选 %d' %
                  (len(done_queries), len(all_sources)), file=sys.stderr)
        except Exception as exc:
            print('断点不可读，重新开始：%s' % exc, file=sys.stderr)
            done_queries.clear()
            all_sources.clear()

    queries = [q for q in QUERIES if q not in done_queries]
    for qi, query in enumerate(queries, 1):
        results = search_code(query, args.limit)
        # 同一 query 的文件并发读取；正文只在内存中用于提取 host。
        with cf.ThreadPoolExecutor(max_workers=max(1, min(args.workers, 16))) as ex:
            for rec, text in ex.map(fetch, results):
                if not text:
                    continue
                source = '%s/%s@%s [%s]' % (rec['repo'], rec['path'], rec['sha'], query)
                for host in hosts_in_text(text):
                    all_sources[host].add(source)
        done_queries.add(query)
        save_checkpoint(checkpoint, done_queries, all_sources)
        print('query %d/%d %r：文件 %d，候选 %d' %
              (qi, len(queries), query, len(results), len(all_sources)), file=sys.stderr, flush=True)

    out = Path(args.out)
    domains = Path(args.domains)
    out.parent.mkdir(parents=True, exist_ok=True)
    domains.parent.mkdir(parents=True, exist_ok=True)
    with out.open('w', encoding='utf-8') as fh, domains.open('w', encoding='utf-8') as dh:
        for host in sorted(all_sources):
            fh.write(json.dumps(dict(domain=host, source='github-code',
                                     source_files=sorted(all_sources[host])), ensure_ascii=False) + '\n')
            dh.write(host + '\n')
    print('完成：%d 个候选；JSONL：%s；域名：%s' % (len(all_sources), out, domains))


if __name__ == '__main__':
    main()
