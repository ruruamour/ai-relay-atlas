#!/usr/bin/env python3
"""生成待扫描的候选域名：对已知站点的"主机名"加常见前缀、对"品牌.后缀"换常见后缀。
只基于去前缀后的主机名生成（避免 ai.api.x.com 这类嵌套），跳过泛解析父域与已收录/已扫描的域名。
用法: python3 tools/gen_candidates.py > /tmp/cands.txt [--skip 已扫描.done ...]
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa

TLDS = ['com', 'net', 'org', 'io', 'ai', 'cc', 'top', 'xyz', 'vip', 'dev', 'app', 'pro', 'club', 'shop', 'site',
        'online', 'fun', 'icu', 'me', 'so', 'to', 'im', 'ws', 'life', 'live', 'link', 'cloud', 'tech', 'space',
        'store', 'world', 'zone', 'cn', 'hk', 'tw']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--skip', nargs='*', default=[], help='已扫描清单（每行一个域名，如 scan.py 的 .done 文件）')
    a = ap.parse_args()
    known = {r['domain'] for r in read_csv(RELAYS)} | {r['alias'] for r in read_csv(ALIASES)}
    for f in ('veridrop-domains.json', 'github-list-domains.json'):
        p = os.path.join(SOURCES, f)
        if os.path.exists(p):
            known |= set(json.load(open(p)))
    skip = set(known)
    for f in a.skip:
        skip |= {x.strip() for x in open(f) if x.strip()}
    wc = json.load(open(os.path.join(SOURCES, 'wildcard-dns.json'))) if os.path.exists(
        os.path.join(SOURCES, 'wildcard-dns.json')) else {}
    hosts = {base_host(d) for d in known if not IP_RE.match(d)}
    out = set()
    for h in hosts:
        if not wc.get(h):
            for p in sorted(GEN_PREFIX):
                out.add('%s.%s' % (p, h))
        rd = registered(h)
        if h == rd and rd.count('.') == 1:
            b = rd.split('.')[0]
            for t in TLDS:
                out.add('%s.%s' % (b, t))
    for c in sorted(out - skip):
        print(c)


if __name__ == '__main__':
    main()
