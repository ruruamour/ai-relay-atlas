#!/usr/bin/env python3
"""从 GitHub 上公开的中转站名单仓库提取域名（需要已登录的 gh CLI）。
用法: python3 tools/discover/github_lists.py > /tmp/gh.txt
新仓库可加到 REPOS；数据文件（json/yaml/csv）也会扫。
"""
import base64
import json
import re
import subprocess
import sys

REPOS = ['zzsting88/relayAPI', 'Folkbench/folkbench', 'panxunying/ai-coding-welfare',
         'peter123023/awesome-claude-api', 'deverzh/ai-api-proxy-list', 'hanzohanzhe/Grandet']
DATA_EXT = ('.md', '.json', '.yaml', '.yml', '.csv', '.txt')
BAD = ('github', 'githubusercontent', 'shields.io', 'google.com', 'python.org', 'npmjs', 'example.com', 'codecov',
       'pre-commit', 'jsdelivr', 'badgen', 'travis', 'gitlab', 't.me', 'discord', 'openai.com', 'anthropic.com',
       'cloudflare', 'vercel.com', 'twitter.com', 'x.com', 'youtube', 'bilibili', 'zhihu', 'linux.do')
URL = re.compile(r'https?://([a-z0-9][a-z0-9.-]*\.[a-z]{2,})', re.I)


def gh(*args):
    return subprocess.run(['gh', 'api', *args], capture_output=True, text=True, timeout=60).stdout


def main():
    out = set()
    for repo in REPOS:
        tree = gh('repos/%s/git/trees/HEAD?recursive=1' % repo, '--jq', '.tree[]|select(.type=="blob")|.path')
        files = [f for f in tree.split('\n') if f.endswith(DATA_EXT) and not f.startswith('.')][:40]
        n = 0
        for f in files:
            raw = gh('repos/%s/contents/%s' % (repo, f), '--jq', '.content').strip()
            if not raw:
                continue
            text = base64.b64decode(raw).decode('utf-8', 'replace')
            for d in URL.findall(text):
                d = d.lower()
                if not any(b in d for b in BAD):
                    out.add(d)
                    n += 1
        print('%-36s %d 文件, %d 域名' % (repo, len(files), n), file=sys.stderr)
    for d in sorted(out):
        print(d)


if __name__ == '__main__':
    main()
