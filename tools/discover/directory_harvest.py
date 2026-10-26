#!/usr/bin/env python3
"""从公开 AI 中转站目录/比价页提取候选域名。

只读取公开目录页面，在内存中提取域名；不保存页面正文、商品购买链接、
路径或查询参数。目录站只是来源线索，候选仍需本项目公开首页/接口验证。
"""
import argparse
import json
import time
import urllib.request
from collections import defaultdict
from pathlib import Path

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from relay_search import hosts_in_text  # noqa: E402

PAGES = [
    ('howtok.net', 'https://howtok.net/'),
    ('howtok.net', 'https://howtok.net/models'),
    ('apiznz.com', 'https://www.apiznz.com/compare'),
    ('apiznz.com', 'https://www.apiznz.com/model/lists'),
    ('computeunion.net', 'https://www.computeunion.net/zh/api-pricing/cn-relay'),
    ('computeunion.net', 'https://www.computeunion.net/zh/platform/runapi'),
    ('computeunion.net', 'https://www.computeunion.net/zh/platform/proaiapi'),
    ('zhongzhuanzhanrank.github.io', 'https://zhongzhuanzhanrank.github.io/gpt-zhongzhuanzhan/'),
    ('aizhongzhuanzhan.github.io', 'https://aizhongzhuanzhan.github.io/'),
    ('aizhongzhuanzhan.github.io', 'https://aizhongzhuanzhan.github.io/page/2/'),
    ('aizhongzhuanzhan.github.io', 'https://aizhongzhuanzhan.github.io/page/3/'),
    ('aizhongzhuanzhan.github.io', 'https://aizhongzhuanzhan.github.io/page/4/'),
    ('helpaio.com', 'https://www.helpaio.com/transit'),
    ('helpaio.com', 'https://www.helpaio.com/transit/compare'),
    ('helpaio.com', 'https://www.helpaio.com/transit/availability'),
    ('helpaio.com', 'https://www.helpaio.com/transit/table'),
    ('helpaio.com', 'https://www.helpaio.com/transit/recommend'),
    ('helpaio.com', 'https://www.helpaio.com/transit/starter'),
    ('hvoyai.com', 'https://www.hvoyai.com/'),
]
DIRECTORY_HOSTS = {x[0] for x in PAGES} | {'github.io'}
UA = 'ai-relay-atlas-public-directory-harvest/0.1'
MAX_BYTES = 8_000_000


def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'text/html,*/*;q=0.8'})
    with urllib.request.urlopen(req, timeout=60) as resp:
        body = resp.read(MAX_BYTES + 1)
    if len(body) > MAX_BYTES:
        return ''
    return body.decode('utf-8', 'replace')


def main():
    ap = argparse.ArgumentParser(description='公开目录候选收集')
    ap.add_argument('--out', default='/tmp/directory-candidates.jsonl')
    ap.add_argument('--domains', default='/tmp/directory-domains.txt')
    ap.add_argument('--delay', type=float, default=1.0)
    args = ap.parse_args()
    found = defaultdict(set)
    for label, url in PAGES:
        try:
            text = fetch(url)
            for host in hosts_in_text(text):
                if host in DIRECTORY_HOSTS or any(host.endswith('.' + x) for x in DIRECTORY_HOSTS):
                    continue
                found[host].add(label)
            print(label, 'candidates', len(found), file=sys.stderr, flush=True)
        except Exception as exc:
            print(label, 'failed:', exc, file=sys.stderr)
        time.sleep(max(0, args.delay))
    out = Path(args.out); domains = Path(args.domains)
    out.parent.mkdir(parents=True, exist_ok=True); domains.parent.mkdir(parents=True, exist_ok=True)
    with out.open('w', encoding='utf-8') as fh, domains.open('w', encoding='utf-8') as dh:
        for host in sorted(found):
            fh.write(json.dumps(dict(domain=host, source='public-directory', source_sites=sorted(found[host])), ensure_ascii=False) + '\n')
            dh.write(host + '\n')
    print('完成：%d 个候选；JSONL：%s；域名：%s' % (len(found), out, domains))


if __name__ == '__main__':
    main()
