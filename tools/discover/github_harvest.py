#!/usr/bin/env python3
"""从 GitHub 公开仓库收集 AI 中转站/卡网候选域名。

只读取公开仓库中的文本型名单、README 和数据文件，不执行仓库代码，
也不把原始文件内容写入结果。每个域名保留仓库和文件来源，便于复查。

用法：
  python3 tools/discover/github_harvest.py run \
      --out /tmp/github-candidates.jsonl \
      --domains /tmp/github-domains.txt \
      --checkpoint /tmp/github-candidates.checkpoint.json

需要已登录的 gh CLI。搜索结果和仓库结构走 GitHub API；文件正文通过
raw.githubusercontent.com 读取，默认只读小型文本文件并跳过历史快照。
"""
import argparse
import concurrent.futures as cf
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from relay_search import hosts_in_text  # noqa: E402


SEED_REPOS = [
    'zzsting88/relayAPI',
    'Folkbench/folkbench',
    'panxunying/ai-coding-welfare',
    'peter123023/awesome-claude-api',
    'deverzh/ai-api-proxy-list',
    'hanzohanzhe/Grandet',
    'howardpen9/awesome-ai-api-proxy',
]
SEARCHES = [
    'AI API proxy',
    'AI API relay',
    'AI API gateway',
    'API relay list',
    'OpenAI proxy list',
    'Claude API proxy',
    'Gemini API proxy',
    'ChatGPT API aggregator',
    'New-API',
    'Sub2API',
    'model plaza AI',
    'AI中转站',
    'AI API中转',
    'AI API list',
    'dujiaoka',
    '自助发卡',
    '独角数卡 AI',
    'AI卡网',
    '发卡网 AI',
]
EXTS = {'.md', '.markdown', '.txt', '.csv', '.json', '.yaml', '.yml'}
SKIP_PATH = re.compile(
    r'(^|/)(?:node_modules|vendor|dist|build|coverage|\.git|assets|images|'
    r'snapshots?|history|archives?)(/|$)', re.I
)
SKIP_NAME = re.compile(
    r'(?:package-lock|pnpm-lock|yarn\.lock|prices\.history|\.min\.|\.map$)', re.I
)
UA = 'ai-relay-atlas-github-harvest/0.1'
MAX_FILE_BYTES = 2_000_000


def gh(*args, timeout=60):
    p = subprocess.run(['gh', *args], capture_output=True, text=True, timeout=timeout)
    if p.returncode != 0:
        raise RuntimeError((p.stderr or p.stdout).strip()[:300])
    return p.stdout


def search_repos(query, limit):
    try:
        raw = gh('search', 'repos', query, '--match', 'name,description,readme',
                 '--include-forks=false', '--limit', str(limit), '--json',
                 'fullName,defaultBranch,isArchived,isFork,updatedAt,stargazersCount')
        return json.loads(raw)
    except Exception as exc:
        print('GitHub 仓库搜索失败 %r：%s' % (query, exc), file=sys.stderr)
        return []


def default_branch(repo):
    try:
        return gh('api', 'repos/%s' % repo, '--jq', '.default_branch').strip() or 'main'
    except Exception:
        return 'main'


def collect_repos(search_limit):
    out = {x: dict(fullName=x, defaultBranch=default_branch(x), isArchived=False, isFork=False)
           for x in SEED_REPOS}
    for query in SEARCHES:
        for rec in search_repos(query, search_limit):
            name = rec.get('fullName')
            if name and not rec.get('isArchived'):
                out.setdefault(name, rec)
    return out


def tree(repo, branch):
    raw = gh('api', 'repos/%s/git/trees/%s?recursive=1' %
             (repo, urllib.parse.quote(branch or 'main', safe='')), timeout=90)
    obj = json.loads(raw)
    if obj.get('truncated'):
        print('! %s tree 被 GitHub 截断' % repo, file=sys.stderr)
    return [x.get('path', '') for x in obj.get('tree', [])
            if x.get('type') == 'blob' and x.get('path')]


def score_file(path):
    p = path.lower()
    ext = Path(p).suffix
    if ext not in EXTS or SKIP_PATH.search(p) or SKIP_NAME.search(p):
        return -1
    score = 0
    if p in ('readme.md', 'readme.zh-cn.md', 'readme.zh-tw.md'):
        score += 100
    if any(k in p for k in ('provider', 'relay', 'proxy', 'list', 'link', 'site', 'domain',
                            'price', 'shop', 'faka', 'channel')):
        score += 30
    if '/data/' in p or p.startswith('data/'):
        score += 20
    # 避免把任意项目的大量文档全部拿来扫 URL。
    score -= p.count('/')
    return score


def choose_files(paths, limit):
    ranked = sorted(((score_file(p), p) for p in paths), reverse=True)
    return [p for score, p in ranked if score >= 0][:limit]


def fetch_raw(repo, branch, path):
    url = 'https://raw.githubusercontent.com/%s/%s/%s' % (
        repo, urllib.parse.quote(branch or 'main', safe=''), urllib.parse.quote(path, safe='/'))
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read(MAX_FILE_BYTES + 1)
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError):
        return ''
    if len(body) > MAX_FILE_BYTES:
        return ''
    return body.decode('utf-8', 'replace')


def harvest_repo(rec, max_files):
    repo = rec['fullName']
    branch = rec.get('defaultBranch') or 'main'
    try:
        paths = choose_files(tree(repo, branch), max_files)
    except Exception as exc:
        print('跳过 %s：%s' % (repo, exc), file=sys.stderr)
        return repo, {}, len(paths) if 'paths' in locals() else 0, False
    found = defaultdict(set)
    for path in paths:
        text = fetch_raw(repo, branch, path)
        if not text:
            continue
        for host in hosts_in_text(text):
            found[host].add(path)
    return repo, found, len(paths), True


def save_checkpoint(path, done_repos, all_sources):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = Path(str(path) + '.tmp')
    obj = dict(done_repos=sorted(done_repos),
               sources={h: sorted(v) for h, v in all_sources.items()})
    tmp.write_text(json.dumps(obj, ensure_ascii=False), encoding='utf-8')
    os.replace(tmp, path)


def write_outputs(args, all_sources):
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    domains = Path(args.domains)
    domains.parent.mkdir(parents=True, exist_ok=True)
    with out.open('w', encoding='utf-8') as fh, domains.open('w', encoding='utf-8') as dh:
        for host in sorted(all_sources):
            rec = dict(domain=host, source='github', source_files=sorted(all_sources[host]))
            fh.write(json.dumps(rec, ensure_ascii=False) + '\n')
            dh.write(host + '\n')


def cmd_run(args):
    repos = collect_repos(args.search_limit)
    checkpoint = Path(args.checkpoint or (str(args.out) + '.checkpoint.json'))
    all_sources = defaultdict(set)
    done_repos = set()
    if checkpoint.exists() and not args.fresh:
        try:
            saved = json.loads(checkpoint.read_text(encoding='utf-8'))
            done_repos = set(saved.get('done_repos') or [])
            for host, paths in (saved.get('sources') or {}).items():
                all_sources[host].update(paths)
            print('从断点恢复：仓库 %d，候选 %d' %
                  (len(done_repos), len(all_sources)), file=sys.stderr)
        except Exception as exc:
            print('断点文件不可读，将重新开始：%s' % exc, file=sys.stderr)
            done_repos.clear()
            all_sources.clear()
    pending = [rec for name, rec in repos.items() if name not in done_repos]
    print('仓库 %d（固定 %d + 搜索新增），本轮待查 %d' %
          (len(repos), len(SEED_REPOS), len(pending)), file=sys.stderr)
    scanned_files = 0
    done = 0
    # GitHub API/Raw 都有速率限制，仓库级并发保持较低；每个完成的仓库写断点。
    with cf.ThreadPoolExecutor(max_workers=args.workers) as ex:
        futures = [ex.submit(harvest_repo, rec, args.max_files) for rec in pending]
        for fut in cf.as_completed(futures):
            repo, found, nfiles, ok = fut.result()
            scanned_files += nfiles
            done += 1
            for host, paths in found.items():
                for path in paths:
                    all_sources[host].add(repo + '/' + path)
            if ok:
                done_repos.add(repo)
                save_checkpoint(checkpoint, done_repos, all_sources)
            if done % 10 == 0 or done == len(futures):
                print('进度 %d/%d，候选 %d，文件 %d' %
                      (done, len(futures), len(all_sources), scanned_files), file=sys.stderr)

    write_outputs(args, all_sources)
    print('完成：%d 个候选，%d 个文件；\nJSONL：%s\n域名：%s\n断点：%s' %
          (len(all_sources), scanned_files, args.out, args.domains, checkpoint))


def main():
    ap = argparse.ArgumentParser(description='从 GitHub 公开仓库收集候选域名')
    sub = ap.add_subparsers(dest='command', required=True)
    r = sub.add_parser('run')
    r.add_argument('--out', default='/tmp/github-candidates.jsonl')
    r.add_argument('--domains', default='/tmp/github-domains.txt')
    r.add_argument('--search-limit', type=int, default=20,
                   help='每个 GitHub 关键词最多取多少仓库')
    r.add_argument('--max-files', type=int, default=30,
                   help='每个仓库最多读取多少个小型文本文件')
    r.add_argument('--workers', type=int, default=4)
    r.add_argument('--checkpoint', help='断点 JSON；默认是 <out>.checkpoint.json')
    r.add_argument('--fresh', action='store_true', help='忽略已有断点，从头扫描')
    r.set_defaults(func=cmd_run)
    args = ap.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
