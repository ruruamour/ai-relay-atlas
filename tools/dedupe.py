#!/usr/bin/env python3
"""去重与清洗（可重复运行）：
  1. 合并同一站的多个域名（同主机去前缀后同价 / 同品牌换后缀且同价）→ 主域名 + aliases.csv
  2. 去掉泛解析产生的垃圾子域（*.example.com 任意前缀都能打开，前缀扫描会误收）
  3. 归一模型名（model_base）、计价方式、来源标签
  4. 标记异常价格（flag: promo / low / high / zero）
  5. 跨品牌同价表 → backend_group（疑似同一后端/白牌）
用法: python3 tools/dedupe.py [--recheck-wildcard]
"""
import argparse
import hashlib
import re
import json
import os
import statistics
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa

SUMMARY = path('data', 'relays', 'summary.json')
SRC_MAP = {
    'scan:plaza': 'sub2api:/api/v1/model-plaza', 'plaza': 'sub2api:/api/v1/model-plaza',
    'scan:pricing': 'newapi:/api/pricing', '/api/pricing': 'newapi:/api/pricing',
    'scan': 'newapi:/api/pricing',
}
RANK = {'veridrop': 0, 'github-list': 1, 'scan': 2}


def nkey(v):
    x = num(v)
    return '' if x is None else '%.6g' % x


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--recheck-wildcard', action='store_true')
    a = ap.parse_args()

    relays = read_csv(RELAYS)
    rows = read_csv(MODELS)
    old_alias = read_csv(ALIASES)
    vd = set(json.load(open(os.path.join(SOURCES, 'veridrop-domains.json'))))
    gh = set(json.load(open(os.path.join(SOURCES, 'github-list-domains.json'))))
    info = {r['domain']: r for r in relays}
    alias_of = {r['alias']: r['canonical'] for r in old_alias}
    alias_via = {r['alias']: r.get('discovered_via') or r.get('known') or '' for r in old_alias}

    def via(d):
        if d in vd:
            return 'veridrop'
        if d in gh:
            return 'github-list'
        v = (info.get(d) or {}).get('discovered_via') or alias_via.get(d)
        return v if v in RANK else 'scan'

    # ---- 行：同站同模型只留最新一条 ----
    by = defaultdict(dict)
    for r in rows:
        d, m = r['domain'], (r['model'] or '').strip()
        if not d or not m or has_secret(m, r.get('group')):
            continue
        r['model'] = m
        prev = by[d].get(m)
        if prev is None or (r.get('last_checked') or '') >= (prev.get('last_checked') or ''):
            by[d][m] = r

    def fp(d):
        items = sorted((m, nkey(r.get('input_usd_m')), nkey(r.get('output_usd_m')), nkey(r.get('call_usd')))
                       for m, r in by[d].items())
        return hashlib.md5(repr(items).encode()).hexdigest()[:16]

    FP = {d: fp(d) for d in by}
    MS = {d: hashlib.md5(repr(sorted(by[d])).encode()).hexdigest()[:16] for d in by}

    # ---- 并查集 ----
    doms = set(info) | set(by) | set(alias_of) | set(alias_of.values())
    par = {d: d for d in doms}

    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x

    split = set()
    sp = path('data', 'relays', 'split.txt')
    if os.path.exists(sp):
        split = {x.split('#')[0].strip() for x in open(sp, encoding='utf-8')} - {''}

    def union(x, y):
        if x in split or y in split:  # 人工标记为独立站点，不与任何域名合并
            return
        rx, ry = find(x), find(y)
        if rx != ry:
            par[ry] = rx

    for al, ca in alias_of.items():
        union(ca, al)

    # ---- 泛解析：扫描生成的 "前缀.父域"，若 "随机.父域" 也能解析，则该前缀没有意义（泛解析产物）----
    def generated(d):
        if via(d) != 'scan' or IP_RE.match(d):
            return False
        lab = d.split('.')
        return lab[0] in GEN_PREFIX and len(lab) > len(registered(d).split('.'))

    def parent(d):
        return d.split('.', 1)[1]

    gen = {d for d in doms if generated(d)}
    wc = wildcard_map({parent(d) for d in gen}, a.recheck_wildcard)
    artifact = {d for d in gen if wc.get(parent(d))}
    # 规则 W：同主机下的泛解析产物都是同一个目标，直接合并
    first_art = {}
    for d in sorted(artifact):
        h = base_host(d)
        if h in first_art:
            union(first_art[h], d)
        else:
            first_art[h] = d
    # 规则 1：同主机（去前缀后）+ 同价表或同模型集合（≥5 个模型）
    host = defaultdict(list)
    for d in doms:
        host[base_host(d)].append(d)
    for h, ds in host.items():
        if len(ds) < 2:
            continue
        seen_fp, seen_ms = {}, {}
        for d in sorted(ds):
            if d not in by:
                continue
            f = FP[d]
            if f in seen_fp:
                union(seen_fp[f], d)
            else:
                seen_fp[f] = d
            if len(by[d]) >= 5:
                ms = MS[d]
                if ms in seen_ms:
                    union(seen_ms[ms], d)
                else:
                    seen_ms[ms] = d
        # 同主机下模型集合高度重合（≥10 个模型、Jaccard≥0.95）：同一站不同时间的快照
        reps = {}
        for d in ds:
            if d in by and len(by[d]) >= 10:
                r = find(d)
                if r not in reps or len(by[d]) > len(by[reps[r]]):
                    reps[r] = d
        rl = list(reps.values())
        if 1 < len(rl) <= 60:
            for i in range(len(rl)):
                for j in range(i + 1, len(rl)):
                    A, B = set(by[rl[i]]), set(by[rl[j]])
                    if len(A & B) / len(A | B) >= 0.95:
                        union(rl[i], rl[j])
        priced = {find(d) for d in ds if d in by}
        if len(priced) == 1:  # 同主机下没报价的域名（www./根域）归到唯一有报价的站
            p = priced.pop()
            for d in ds:
                if d not in by:
                    union(p, d)
    # 规则 3：同可注册域（非共享托管域）+ 完全同价表
    hosts_per_rd = defaultdict(set)
    for d in doms:
        hosts_per_rd[registered(d)].add(base_host(d))
    seen_rd = {}
    for d in sorted(by):
        rd = registered(d)
        if len(hosts_per_rd[rd]) >= 4:  # ccwu.cc / railway.app 这类共享域，不按此规则合并
            continue
        k = (rd, FP[d])
        if k in seen_rd:
            union(seen_rd[k], d)
        else:
            seen_rd[k] = d
    # 规则 2：同品牌（换后缀/换子域）+ 完全同价表（≥5 个模型）
    byfp = defaultdict(list)
    for d in by:
        if len(by[d]) >= 5:
            byfp[FP[d]].append(d)
    for f, ds in byfp.items():
        if len(ds) < 2:
            continue
        first = {}
        for d in sorted(ds):
            b = brand(d)
            if b in first:
                union(first[b], d)
            else:
                first[b] = d

    # 规则 4：同一个自定义站名（来自 /api/status 或网页标题；共享托管域除外）
    #   同可注册域：直接合并；跨可注册域（换后缀）：站名不能只是域名本身（"2API" 之于 2api.xx 不算证据）
    def nn(x):
        return re.sub(r'[\s\-_.]+', '', (x or '').lower())
    first_name = {}
    for d in sorted(info):
        n = nn(info[d].get('name'))
        if len(n) < 3 or is_generic_name(n) or len(hosts_per_rd[registered(d)]) >= 4:
            continue
        for k in ([('rd', registered(d), n)] + ([('brand', brand(d), n)] if n != nn(brand(d)) and len(n) >= 4 else [])):
            if k in first_name:
                union(first_name[k], d)
            else:
                first_name[k] = d

    clusters = defaultdict(list)
    for d in doms:
        clusters[find(d)].append(d)

    def score(d):
        return num((info.get(d) or {}).get('veridrop_score')) or 0

    def ckey(d):
        return (RANK[via(d)], -score(d), d in artifact, 0 if (d in info and d not in alias_of) else 1,
                d.count('.'), len(d), d)


    # ---- 输出 ----
    out_relays, out_alias, out_rows = [], [], []
    junk_total = 0
    for root, ms in clusters.items():
        ms = sorted(ms, key=ckey)
        can = ms[0]
        keep, junk = [], []
        for d in ms[1:]:
            (junk if d in artifact else keep).append(d)
        junk_total += len(junk)
        cands = [d for d in [can] + keep + junk if by.get(d)]
        donor = max(cands, key=lambda d: (max((r.get('last_checked') or '') for r in by[d].values()),
                                          len(by[d]), d == can, -len(d))) if cands else None
        ci = dict(info.get(can) or {})
        if has_secret(ci.get('name'), ci.get('notes')):
            ci['name'], ci['notes'] = '', ''
        for d in ms:
            o = info.get(d) or {}
            if score(d) > (num(ci.get('veridrop_score')) or 0):
                ci['veridrop_score'] = o.get('veridrop_score')
            for k in ('name', 'version', 'topup_cny_per_usd'):
                if not ci.get(k) and o.get(k):
                    ci[k] = o[k]
        drows = list(by[donor].values()) if donor else []
        srcs = set()
        for r in drows:
            s = SRC_MAP.get(r.get('source'), r.get('source') or '')
            r['source'] = s
            srcs.add(s)
        system = ci.get('system') or ci.get('system_name') or ''
        if system not in SYSTEMS + ('One-API', 'Veloera', 'VoAPI', 'Done-Hub', 'OhMyGPT'):
            if system and not ci.get('name'):
                ci['name'] = system  # 旧数据把站名填进了 system 列
            system = ''
        if any(s.startswith('newapi') for s in srcs):
            system = 'New-API'
        elif any(s.startswith('sub2api') for s in srcs):
            system = 'Sub2API'
        api_host = donor if (donor and donor != can) else (ci.get('api_host') or '')
        notes = [x for x in (ci.get('notes') or '').split('；') if x and not x.startswith('泛解析')]
        if junk:
            notes.append('泛解析，已去掉 %d 个扫描生成的子域' % len(junk))
        elif any(x.startswith('泛解析') for x in (ci.get('notes') or '').split('；')):
            notes.append([x for x in ci['notes'].split('；') if x.startswith('泛解析')][0])
        fams = set()
        for r in drows:
            r['domain'] = can
            r['model_base'] = model_base(r['model'])
            r['billing'] = r.get('billing') or 'token'
            fams.add(family(r['model_base']))
            out_rows.append(r)
        out_relays.append(dict(
            domain=can, api_host=api_host, name=ci.get('name', ''), system=system,
            version=ci.get('version', ''), topup_cny_per_usd=ci.get('topup_cny_per_usd', ''),
            discovered_via=min((via(d) for d in ms), key=lambda v: RANK[v]),
            veridrop_score=ci.get('veridrop_score', ''), n_models=len(drows),
            families='/'.join(c for c in FAMILY_ORDER if c in fams), aliases=len(keep), backend_group='',
            http_status=ci.get('http_status', ''), latency_ms=ci.get('latency_ms', ''),
            last_checked=max([r.get('last_checked') or '' for r in drows] + [ci.get('last_checked') or '']),
            notes='；'.join(notes)))
        for d in keep:
            reason = 'same-host' if base_host(d) == base_host(can) else ('mirror' if brand(d) == brand(can) else 'merged')
            out_alias.append(dict(alias=d, canonical=can, reason=reason, discovered_via=via(d)))

    # ---- 价格标记 ----
    # default: model_ratio=37.5 是 New-API 未配置模型时的默认倍率（占位价）
    def is_default(r):
        return r['billing'] == 'token' and num(r.get('model_ratio')) == 37.5
    for r in out_rows:
        r['_promo'] = bool(PROMO_RX.search(r.get('group') or '') or r.get('promo') == 'yes')
    mins = defaultdict(dict)
    for r in out_rows:
        p = num(r.get('input_usd_m'))
        if r['billing'] == 'token' and p and p > 0 and not r['_promo'] and not is_default(r):
            d = r['domain']
            mins[r['model_base']][d] = min(p, mins[r['model_base']].get(d, p))
    med = {b: statistics.median(v.values()) for b, v in mins.items() if len(v) >= 5}
    cmins = defaultdict(dict)
    for r in out_rows:
        p = num(r.get('call_usd'))
        if r['billing'] == 'call' and p and p > 0 and not r['_promo']:
            d = r['domain']
            cmins[r['model_base']][d] = min(p, cmins[r['model_base']].get(d, p))
    cmed = {b: statistics.median(v.values()) for b, v in cmins.items() if len(v) >= 5}
    for r in out_rows:
        fl = ['promo'] if r.pop('_promo') else []
        p = num(r.get('input_usd_m'))
        m = med.get(r['model_base'])
        if r['billing'] == 'token':
            if p is not None and p <= 0:
                fl.append('zero')
            elif is_default(r) and not (m and p and p <= m * 3):
                fl.append('default')
            elif p and m:
                if p < m * 0.05:
                    fl.append('low')
                elif p > m * 20:
                    fl.append('high')
        else:
            c, cm = num(r.get('call_usd')), cmed.get(r['model_base'])
            if c is not None and c <= 0:
                fl.append('zero')
            elif c and cm:
                if c < cm * 0.05:
                    fl.append('low')
                elif c > cm * 20:
                    fl.append('high')
        r['flag'] = '+'.join(fl)
    json.dump({'token_usd_per_1m_input': {b: float('%.6g' % v) for b, v in sorted(med.items())},
               'call_usd_per_request': {b: float('%.6g' % v) for b, v in sorted(cmed.items())}},
              open(path('data', 'relays', 'medians.json'), 'w'), indent=0, ensure_ascii=False)

    # ---- 跨品牌同价表 → backend_group ----
    rel = {r['domain']: r for r in out_relays}
    cfp = defaultdict(list)
    tmp = defaultdict(list)
    for r in out_rows:
        tmp[r['domain']].append((r['model'], nkey(r.get('input_usd_m')), nkey(r.get('output_usd_m'))))
    for d, items in tmp.items():
        if len(items) >= 5:
            cfp[hashlib.md5(repr(sorted(items)).encode()).hexdigest()].append(d)
    groups = sorted([ds for ds in cfp.values() if len({brand(d) for d in ds}) > 1], key=lambda x: (-len(x), min(x)))
    for i, ds in enumerate(groups, 1):
        for d in ds:
            rel[d]['backend_group'] = 'B%03d' % i

    out_relays.sort(key=lambda r: r['domain'])
    out_alias.sort(key=lambda r: (r['canonical'], r['alias']))
    out_rows.sort(key=lambda r: (r['domain'], r['model_base'], r['model']))
    write_csv(RELAYS, RELAY_COLS, out_relays)
    write_csv(ALIASES, ALIAS_COLS, out_alias)
    write_csv(MODELS, MODEL_COLS, out_rows)

    prev = json.load(open(SUMMARY)) if os.path.exists(SUMMARY) else {}
    summ = dict(sites=len(out_relays), aliases=len(out_alias),
                wildcard_removed=prev.get('wildcard_removed', 0) + junk_total,
                backend_groups=len(groups), backend_group_sites=sum(len(g) for g in groups),
                model_rows=len(out_rows), model_bases=len({r['model_base'] for r in out_rows}),
                raw_model_names=len({r['model'] for r in out_rows}))
    json.dump(summ, open(SUMMARY, 'w'), indent=1, ensure_ascii=False)
    print(json.dumps(summ, ensure_ascii=False))


if __name__ == '__main__':
    main()
