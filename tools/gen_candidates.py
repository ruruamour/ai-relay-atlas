#!/usr/bin/env python3
"""生成待扫描的候选域名：对已知站点的"主机名"加常见前缀、对"品牌.后缀"换常见后缀。
只基于去前缀后的主机名生成（避免 ai.api.x.com 这类嵌套），跳过已收录/已扫描的域名。
--resolve：先做 DNS 过滤（只留能解析的），并丢掉父域是泛解析的前缀候选（任何前缀都能解析，无意义）。
用法: python3 tools/gen_candidates.py --resolve > /tmp/cands.txt [--skip 已扫描清单 ...]
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
    ap.add_argument('--skip', nargs='*', default=[], help='已扫描清单（每行一个域名）')
    ap.add_argument('--resolve', action='store_true', help='DNS 过滤 + 去掉泛解析父域下的前缀候选')
    a = ap.parse_args()
    known = {r['domain'] for r in read_csv(RELAYS)} | {r['alias'] for r in read_csv(ALIASES)}
    known |= {r['api_host'] for r in read_csv(RELAYS) if r.get('api_host')}
    for f in ('veridrop-domains.json', 'github-list-domains.json'):
        p = os.path.join(SOURCES, f)
        if os.path.exists(p):
            known |= set(json.load(open(p)))
    skip = set(known)
    for f in a.skip:
        skip |= {x.strip() for x in open(f) if x.strip()}
    hosts = {base_host(d) for d in known if d and not IP_RE.match(d)}
    pref, tld = set(), set()
    for h in hosts:
        for p in sorted(GEN_PREFIX):
            pref.add('%s.%s' % (p, h))
        rd = registered(h)
        if h == rd and rd.count('.') == 1:
            b = rd.split('.')[0]
            for t in TLDS:
                tld.add('%s.%s' % (b, t))
    pref -= skip
    tld -= skip | pref
    print('候选：前缀 %d，换后缀 %d' % (len(pref), len(tld)), file=sys.stderr)
    out = pref | tld
    if a.resolve:
        wc = wildcard_map({c.split('.', 1)[1] for c in pref})
        pref = {c for c in pref if not wc.get(c.split('.', 1)[1])}
        print('去掉泛解析父域后：前缀 %d' % len(pref), file=sys.stderr)
        out = resolve_many(pref | tld)
        print('能解析：%d' % len(out), file=sys.stderr)
    for c in sorted(out):
        print(c)


if __name__ == '__main__':
    main()
