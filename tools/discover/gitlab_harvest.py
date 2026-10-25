#!/usr/bin/env python3
"""从 GitLab 公共项目收集 AI 中转站/卡网候选域名。

只读取公开项目的文本文件，不执行仓库代码、不保存正文；结果保留项目、
文件、分支和搜索词来源。GitLab 公共 API 可能对中文搜索返回 500，单个
查询失败会跳过并保留其他结果。
"""
import argparse
import base64
import concurrent.futures as cf
import json
import os
import re
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
    'new-api', 'newapi', 'one-api', 'sub2api', 'dujiaoka', 'acg-faka',
    'AI API proxy', 'AI API relay', 'AI API gateway', 'OpenAI proxy',
    'Gemini proxy', 'Claude proxy', 'AI relay', 'AI gateway',
]
TEXT_EXTS = {'.md', '.markdown', '.txt', '.csv', '.json', '.yaml', '.yml'}
SKIP_PATH = re.compile(r'(^|/)(?:node_modules|vendor|dist|build|coverage|\.git|assets|images|snapshots?|history|archives?)(/|$)', re.I)
SKIP_NAME = re.compile(r'(?:package-lock|pnpm-lock|yarn\.lock|\.min\.|\.map$)', re.I)
UA = 'ai-relay-atlas-gitlab-harvest/0.1'
MAX_FILE_BYTES = 2_000_000


def request_json(path, params=None, timeout=45):
    url = 'https://gitlab.com/api/v4/' + path
    if params:
        url += '?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'application/json'})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())


def search_projects(query, limit):
    try:
        return request_json('projects', {
            'search': query, 'simple': 'true', 'per_page': min(limit, 100),
            'order_by': 'last_activity_at', 'sort': 'desc',
        })
    except Exception as exc:
        print('GitLab 项目搜索失败 %r：%s' % (query, exc), file=sys.stderr)
        return []


def score_file(path):
    p = path.lower()
    if Path(p).suffix not in TEXT_EXTS or SKIP_PATH.search(p) or SKIP_NAME.search(p):
        return -1
    score = 0
    name = Path(p).name
    if name.lower() in ('readme.md', 'readme.zh-cn.md', 'readme.zh-tw.md'):
        score += 100
    if any(x in p for x in ('relay', 'proxy', 'list', 'link', 'site', 'domain', 'price', 'shop', 'faka', 'channel')):
        score += 30
    score -= p.count('/')
    return score


def fetch_project(rec, max_files):
    project = str(rec['id'])
    branch = rec.get('default_branch') or 'main'
    try:
        tree = request_json('projects/%s/repository/tree' % project, {
            'recursive': 'true', 'per_page': 100, 'ref': branch,
        }, timeout=60)
    except Exception as exc:
        print('跳过 GitLab %s：%s' % (rec.get('path_with_namespace'), exc), file=sys.stderr)
        return rec, {}
    paths = sorted((x.get('path', '') for x in tree if x.get('type') == 'blob'),
                   key=lambda p: (-score_file(p), p))
    paths = [p for p in paths if score_file(p) >= 0][:max_files]
    found = defaultdict(set)
    for path in paths:
        try:
            obj = request_json('projects/%s/repository/files/%s' %
                               (project, urllib.parse.quote(path, safe='')), {
                                   'ref': branch,
                               }, timeout=45)
            if obj.get('encoding') != 'base64':
                continue
            body = base64.b64decode(obj.get('content', ''), validate=False)
            if len(body) > MAX_FILE_BYTES:
                continue
            text = body.decode('utf-8', 'replace')
        except Exception:
            continue
        source = '%s/%s@%s' % (rec.get('path_with_namespace'), path, branch)
        for host in hosts_in_text(text):
            found[host].add(source)
    return rec, found


def save_checkpoint(path, done_queries, sources):
    tmp = Path(str(path) + '.tmp')
    tmp.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_text(json.dumps(dict(done_queries=sorted(done_queries),
                                   sources={k: sorted(v) for k, v in sources.items()}),
                              ensure_ascii=False), encoding='utf-8')
    os.replace(tmp, path)


def main():
    ap = argparse.ArgumentParser(description='GitLab 公共项目候选收集')
    ap.add_argument('--out', default='/tmp/gitlab-candidates.jsonl')
    ap.add_argument('--domains', default='/tmp/gitlab-domains.txt')
    ap.add_argument('--checkpoint', default='/tmp/gitlab-harvest.checkpoint.json')
    ap.add_argument('--limit', type=int, default=25, help='每个关键词最多读取多少项目')
    ap.add_argument('--max-files', type=int, default=8, help='每个项目最多读取多少文本文件')
    ap.add_argument('--workers', type=int, default=3)
    ap.add_argument('--delay', type=float, default=0.5)
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
        projects = search_projects(query, args.limit)
        # 同一个项目可能被多个词命中；每个 query 内去重。
        unique = {x.get('id'): x for x in projects if x.get('id')}
        with cf.ThreadPoolExecutor(max_workers=max(1, min(args.workers, 8))) as ex:
            for rec, found in ex.map(lambda x: fetch_project(x, args.max_files), unique.values()):
                for host, vals in found.items():
                    sources[host].update('%s [%s]' % (v, query) for v in vals)
        done_queries.add(query)
        save_checkpoint(checkpoint, done_queries, sources)
        print('query %d/%d %r：项目 %d，候选 %d' %
              (i, len(queries), query, len(unique), len(sources)), file=sys.stderr, flush=True)
        time.sleep(max(0, args.delay))

    out = Path(args.out); domains = Path(args.domains)
    out.parent.mkdir(parents=True, exist_ok=True); domains.parent.mkdir(parents=True, exist_ok=True)
    with out.open('w', encoding='utf-8') as fh, domains.open('w', encoding='utf-8') as dh:
        for host in sorted(sources):
            fh.write(json.dumps(dict(domain=host, source='gitlab', source_files=sorted(sources[host])),
                                ensure_ascii=False) + '\n')
            dh.write(host + '\n')
    print('完成：%d 个候选；JSONL：%s；域名：%s' % (len(sources), out, domains))


if __name__ == '__main__':
    main()
