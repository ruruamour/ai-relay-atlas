#!/usr/bin/env python3
"""从 Sourcegraph 公共代码索引的文档匹配行提取候选域名。

只读取公开搜索结果中的 README/文本文件匹配行，不下载或执行代码，不保存
匹配正文；结果保留仓库、文件、commit 和搜索词来源。
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
    'context:global count:50 file:README.md "api/pricing"',
    'context:global count:50 file:README.md "model-plaza"',
    'context:global count:50 file:README.md "Sub2API"',
    'context:global count:50 file:README.md "New API"',
    'context:global count:50 file:README.md "new-api"',
    'context:global count:50 file:README.md "AI中转站"',
    'context:global count:50 file:README.md "AI API"',
    'context:global count:50 file:README.md "发卡网"',
    'context:global count:50 file:README.md "dujiaoka"',
    'context:global count:50 file:README.md "Gemini API"',
]
UA = 'ai-relay-atlas-sourcegraph-harvest/0.1'


def search(query, timeout=150):
    url = 'https://sourcegraph.com/search/stream?q=' + urllib.parse.quote(query) + '&v=V3'
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'text/event-stream'})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        text = resp.read().decode('utf-8', 'replace')
    matches = []
    for block in text.split('\n\n'):
        event = ''
        data_lines = []
        for line in block.splitlines():
            if line.startswith('event:'):
                event = line[6:].strip()
            elif line.startswith('data:'):
                data_lines.append(line[5:].lstrip())
        if event != 'matches' or not data_lines:
            continue
        try:
            obj = json.loads('\n'.join(data_lines))
        except ValueError:
            continue
        if isinstance(obj, list):
            matches.extend(obj)
    return matches


def main():
    ap = argparse.ArgumentParser(description='Sourcegraph 公共文档索引收集')
    ap.add_argument('--out', default='/tmp/sourcegraph-candidates.jsonl')
    ap.add_argument('--domains', default='/tmp/sourcegraph-domains.txt')
    ap.add_argument('--checkpoint', default='/tmp/sourcegraph-harvest.checkpoint.json')
    ap.add_argument('--delay', type=float, default=1.0)
    ap.add_argument('--fresh', action='store_true')
    args = ap.parse_args()

    checkpoint = Path(args.checkpoint)
    done_queries, sources = set(), defaultdict(set)
    if checkpoint.exists() and not args.fresh:
        try:
            saved = json.loads(checkpoint.read_text(encoding='utf-8'))
            done_queries = set(saved.get('done_queries') or [])
            for host, vals in (saved.get('sources') or {}).items():
                sources[host].update(vals)
            print('从断点恢复：query %d，候选 %d' %
                  (len(done_queries), len(sources)), file=sys.stderr)
        except Exception as exc:
            print('断点不可读，重新开始：%s' % exc, file=sys.stderr)
            done_queries.clear(); sources.clear()

    queries = [q for q in QUERIES if q not in done_queries]
    for i, query in enumerate(queries, 1):
        try:
            matches = search(query)
            for item in matches:
                # 只处理文档/文本文件，避免把任意代码索引当作名单读取。
                path = item.get('path') or ''
                if Path(path).suffix.lower() not in {'.md', '.markdown', '.txt', '.json', '.yaml', '.yml', '.csv', '.html'}:
                    continue
                repo = item.get('repository') or ''
                commit = item.get('commit') or ''
                source = 'sourcegraph:%s/%s@%s [%s]' % (repo, path, commit, query)
                for line in item.get('lineMatches') or []:
                    for host in hosts_in_text(line.get('line') or ''):
                        sources[host].add(source)
            print('query %d/%d：匹配 %d，候选 %d' %
                  (i, len(queries), len(matches), len(sources)), file=sys.stderr, flush=True)
        except Exception as exc:
            print('Sourcegraph 搜索失败 %r：%s' % (query, exc), file=sys.stderr)
        done_queries.add(query)
        tmp = Path(str(checkpoint) + '.tmp')
        tmp.parent.mkdir(parents=True, exist_ok=True)
        tmp.write_text(json.dumps(dict(done_queries=sorted(done_queries),
                                       sources={k: sorted(v) for k, v in sources.items()}),
                                 ensure_ascii=False), encoding='utf-8')
        os.replace(tmp, checkpoint)
        time.sleep(max(0, args.delay))

    out = Path(args.out); domains = Path(args.domains)
    out.parent.mkdir(parents=True, exist_ok=True); domains.parent.mkdir(parents=True, exist_ok=True)
    with out.open('w', encoding='utf-8') as fh, domains.open('w', encoding='utf-8') as dh:
        for host in sorted(sources):
            fh.write(json.dumps(dict(domain=host, source='sourcegraph', source_files=sorted(sources[host])),
                                ensure_ascii=False) + '\n')
            dh.write(host + '\n')
    print('完成：%d 个候选；JSONL：%s；域名：%s' % (len(sources), out, domains))


if __name__ == '__main__':
    main()
