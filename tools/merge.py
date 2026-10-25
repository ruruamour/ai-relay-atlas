#!/usr/bin/env python3
"""把 scan.py 的结果并入主表。
- 有价格：已有站点用新快照整体替换该站报价；新站点追加。
- 只有站点信息（/api/status 或 Sub2API 设置）没有公开价格：已有站点只更新站名/版本/充值价；
  新站点仅在"已知目录收录"或"有自定义站名且非自用/演示"时收录（避免把私人部署当中转站）。
别名域名的报价单独保存，是否同一站由 dedupe 判断（价格表差异大的不会合并）。合并后请运行 tools/build.sh。
用法: python3 tools/merge.py <scan.json> [--via scan|crtsh|urlscan|gitlab|npm|huggingface|bing|veridrop|github-list]
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa


def rows_from(blob):
    seen, out = set(), []
    for key, src in (('pricing', 'newapi:/api/pricing'), ('plaza', 'sub2api:/api/v1/model-plaza')):
        for x in blob.get(key) or []:
            m = (x.get('model') or '').strip()
            if not m or m in seen or has_secret(m, x.get('group')):
                continue
            seen.add(m)
            out.append(dict(model=m, billing=x.get('billing') or 'token', input_usd_m=fmt(x.get('input')),
                            output_usd_m=fmt(x.get('output')), call_usd=fmt(x.get('call')),
                            group=x.get('group') or '', group_ratio=fmt(x.get('group_ratio')),
                            model_ratio=fmt(x.get('model_ratio')), source=src, flag='',
                            last_checked=blob.get('checked') or ''))
    return out


def meta_from(blob):
    st, se = blob.get('status') or {}, blob.get('settings') or {}
    m = st or se
    if not m:
        return None
    return dict(name=m.get('name') or '', version=m.get('version') or '',
                topup=st.get('topup_cny'), topup_known='topup_cny' in st,
                system='Sub2API' if se else 'New-API/One-API',
                public=not (st.get('self_use') or st.get('demo')) and (not se or se.get('registration') or se.get('plaza')))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('scan_json')
    ap.add_argument('--via', default='scan', choices=['scan', 'crtsh', 'urlscan', 'gitlab', 'npm', 'huggingface', 'bing', 'veridrop', 'github-list'])
    a = ap.parse_args()
    data = json.load(open(a.scan_json))
    relays = read_csv(RELAYS)
    rows = read_csv(MODELS)
    info = {r['domain']: r for r in relays}
    api_of = {r['api_host']: r['domain'] for r in relays if r.get('api_host')}
    known = set()
    for f in ('veridrop-domains.json', 'github-list-domains.json'):
        p = os.path.join(SOURCES, f)
        if os.path.exists(p):
            known |= set(json.load(open(p)))

    snap, metas = {}, {}
    for host, blob in data.items():
        can = api_of.get(host) or host
        new = rows_from(blob)
        if new:
            pri = (host == (info.get(can) or {}).get('api_host'), host == can, len(new))
            if can not in snap or pri > snap[can][0]:
                snap[can] = (pri, host, new)
        mt = meta_from(blob)
        if mt and (can not in metas or host == can):
            metas[can] = mt

    kept = [r for r in rows if r['domain'] not in snap]
    added = updated_meta = 0
    for can, (_, host, new) in snap.items():
        for r in new:
            r['domain'] = can
            r['model_base'] = model_base(r['model'])
        kept.extend(new)
        if can not in info:
            added += 1
            info[can] = dict(domain=can, discovered_via=a.via)
            relays.append(info[can])
        if host != can:
            info[can]['api_host'] = host
    for can, mt in metas.items():
        if can not in info:
            ok = mt['public'] and (can in known or not is_generic_name(mt['name']))
            if not ok:
                continue
            added += 1
            info[can] = dict(domain=can, discovered_via=a.via)
            relays.append(info[can])
        r = info[can]
        if mt['name'] and not is_generic_name(mt['name']) and not has_secret(mt['name']):
            r['name'] = mt['name']
        r['version'] = mt['version'] or r.get('version', '')
        if mt['topup_known']:  # 旧格式扫描结果没有币种信息，不覆盖
            r['topup_cny_per_usd'] = fmt(valid_topup(mt['topup'])) if valid_topup(mt['topup']) else ''
        if r.get('system') not in ('New-API', 'Sub2API'):
            r['system'] = mt['system']
        updated_meta += 1
    write_csv(MODELS, MODEL_COLS, kept)
    write_csv(RELAYS, RELAY_COLS, relays)
    print('价格快照 %d 站，站点信息 %d 站，新增 %d 站；报价行 %d → %d' % (len(snap), updated_meta, added, len(rows), len(kept)))


if __name__ == '__main__':
    main()
