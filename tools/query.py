#!/usr/bin/env python3
"""查询。
  python3 tools/query.py model gemini-4-argon [--n 30] [--all] [--cny]   某模型的站点与价格（默认排除福利/占位/异常价；--cny 按实付 ¥ 排）
  python3 tools/query.py site api.openlux.ai                     某站的全部模型（别名自动换成主域名）
  python3 tools/query.py find openlux                            按关键词找站点/别名
"""
import argparse
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa

BAD = {'promo', 'zero', 'default', 'low'}


def p(r):
    return num(r['call_usd']) if r['billing'] == 'call' else num(r['input_usd_m'])


def cmd_model(a):
    rows = read_csv(MODELS)
    q = a.q.lower()
    hit = [r for r in rows if r['model_base'] == q] or [r for r in rows if q in r['model_base'] or q in r['model'].lower()]
    from collections import Counter
    bc = Counter(r['billing'] for r in hit)
    mode = 'call' if a.call else ('token' if a.token else (bc.most_common(1)[0][0] if bc else 'token'))
    best = {}
    for r in hit:
        if r['billing'] != mode:
            continue
        if not a.all and BAD & set(r['flag'].split('+')):
            continue
        v = p(r)
        if v is None or v <= 0:
            continue
        if r['domain'] not in best or v < p(best[r['domain']]):
            best[r['domain']] = r
    bases = sorted({r['model_base'] for r in hit})
    print('匹配基础模型 %d 个：%s%s' % (len(bases), ', '.join(bases[:8]), ' …' if len(bases) > 8 else ''))
    other = sum(v for k, v in bc.items() if k != mode)
    print('%d 个站（%s，按价格升序，推算%s）%s\n' % (len(best), '按次' if mode == 'call' else '按量 $/1M 输入',
          '' if a.all else '，已排除福利/占位/异常价，--all 显示全部',
          ('；另有 %d 行%s计价，用 --%s 查看' % (other, '按量' if mode == 'call' else '按次', 'token' if mode == 'call' else 'call')) if other else ''))
    tp = topup_map()
    key = (lambda kv: (0, p(kv[1]) * tp[kv[0]])) if a.cny else (lambda kv: (0, p(kv[1])))
    rows_ = sorted(((d, r) for d, r in best.items() if (not a.cny or d in tp)), key=key)
    if a.cny:
        print('只看公开了充值价的站，按实付 ¥ 排序\n')
    print('%-32s %-12s %-11s %-9s %-10s %-12s %-22s %s' % ('站点', '名义$', '输出$', '充值¥/$', '实付¥', '标记', '分组', '原始模型名'))
    for d, r in rows_[:a.n]:
        unit = '/次' if r['billing'] == 'call' else ''
        real = ('¥' + fmt(p(r) * tp[d])) if d in tp else '-'
        print('%-32s %-12s %-11s %-9s %-10s %-12s %-22s %s' % (d, '$' + fmt(p(r)) + unit,
              ('$' + r['output_usd_m']) if r['output_usd_m'] else '-', fmt(tp.get(d)) or '-', real,
              r['flag'] or '-', (r['group'] or '-')[:22], r['model']))


def cmd_site(a):
    alias = {r['alias']: r['canonical'] for r in read_csv(ALIASES)}
    d = alias.get(a.q, a.q)
    if d != a.q:
        print('%s 是 %s 的别名' % (a.q, d))
    info = {r['domain']: r for r in read_csv(RELAYS)}.get(d)
    if not info:
        print('未收录：%s（试试 find）' % a.q)
        return
    for k in ('domain', 'api_host', 'name', 'system', 'version', 'topup_cny_per_usd', 'discovered_via', 'veridrop_score', 'n_models', 'families',
              'aliases', 'backend_group', 'http_status', 'latency_ms', 'last_checked', 'notes'):
        if info.get(k):
            print('%-15s %s' % (k, info[k]))
    rows = [r for r in read_csv(MODELS) if r['domain'] == d]
    by = defaultdict(list)
    for r in rows:
        by[family(r['model_base'])].append(r)
    for c in FAMILY_ORDER:
        if not by.get(c):
            continue
        print('\n[%s] %d' % (FAMILY_NAME[c], len(by[c])))
        for r in sorted(by[c], key=lambda r: r['model'])[:a.n]:
            unit = '/次' if r['billing'] == 'call' else ''
            print('  %-40s $%-10s %-10s %s' % (r['model'][:40], fmt(p(r)) + unit, r['flag'] or '', r['group'][:30]))
        if len(by[c]) > a.n:
            print('  … 另 %d 个' % (len(by[c]) - a.n))


def cmd_find(a):
    q = a.q.lower()
    for r in read_csv(RELAYS):
        if q in r['domain'] or q in (r['name'] or '').lower():
            print('站点  %-34s %-8s 模型 %-5s %s' % (r['domain'], r['system'] or '-', r['n_models'], r['name'][:40]))
    for r in read_csv(ALIASES):
        if q in r['alias']:
            print('别名  %-34s → %s (%s)' % (r['alias'], r['canonical'], r['reason']))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('mode', choices=['model', 'site', 'domain', 'find'])
    ap.add_argument('q')
    ap.add_argument('--n', type=int, default=30)
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--call', action='store_true', help='只看按次计价')
    ap.add_argument('--cny', action='store_true', help='只看公开充值价的站，按实付 ¥ 排序')
    ap.add_argument('--token', action='store_true', help='只看按量计价')
    a = ap.parse_args()
    {'model': cmd_model, 'site': cmd_site, 'domain': cmd_site, 'find': cmd_find}[a.mode](a)


if __name__ == '__main__':
    main()
