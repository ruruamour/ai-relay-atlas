#!/usr/bin/env python3
"""把 scan.py 的结果并入主表。已有站点：用新快照整体替换该站的报价；新站点：追加。
别名域名自动映射到主域名。合并后请运行 tools/build.sh（会重新去重）。
用法: python3 tools/merge.py <scan.json> [--via scan|veridrop|github-list]
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa


def rows_from(host_blob):
    seen, out = set(), []
    for key, src in (('pricing', 'newapi:/api/pricing'), ('plaza', 'sub2api:/api/v1/model-plaza')):
        for x in host_blob.get(key) or []:
            m = (x.get('model') or '').strip()
            if not m or m in seen:
                continue
            seen.add(m)
            out.append(dict(model=m, billing=x.get('billing') or 'token', input_usd_m=fmt(x.get('input')),
                            output_usd_m=fmt(x.get('output')), call_usd=fmt(x.get('call')),
                            group=x.get('group') or '', group_ratio=fmt(x.get('group_ratio')),
                            model_ratio=fmt(x.get('model_ratio')), source=src, flag='',
                            last_checked=host_blob.get('checked') or ''))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('scan_json')
    ap.add_argument('--via', default='scan', choices=['scan', 'veridrop', 'github-list'])
    a = ap.parse_args()
    data = json.load(open(a.scan_json))
    relays = read_csv(RELAYS)
    rows = read_csv(MODELS)
    alias_of = {r['alias']: r['canonical'] for r in read_csv(ALIASES)}
    info = {r['domain']: r for r in relays}
    api_of = {r['api_host']: r['domain'] for r in relays if r.get('api_host')}

    # 每个主域名只取一个快照：优先 api_host 的结果，其次模型最多的
    snap = {}
    for host, blob in data.items():
        new = rows_from(blob)
        if not new:
            continue
        can = api_of.get(host) or alias_of.get(host) or host
        pri = (host == (info.get(can) or {}).get('api_host'), host == can, len(new))
        if can not in snap or pri > snap[can][0]:
            snap[can] = (pri, host, new)

    kept = [r for r in rows if r['domain'] not in snap]
    added_sites = 0
    for can, (_, host, new) in snap.items():
        for r in new:
            r['domain'] = can
            r['model_base'] = model_base(r['model'])
        kept.extend(new)
        if can not in info:
            added_sites += 1
            info[can] = dict(domain=can, discovered_via=a.via)
            relays.append(info[can])
        if host != can:
            info[can]['api_host'] = host
    write_csv(MODELS, MODEL_COLS, kept)
    write_csv(RELAYS, RELAY_COLS, relays)
    print('快照替换 %d 站（新增 %d 站），报价行 %d → %d' % (len(snap), added_sites, len(rows), len(kept)))


if __name__ == '__main__':
    main()
