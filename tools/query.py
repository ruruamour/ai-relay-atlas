#!/usr/bin/env python3
"""从本地 CSV 查询模型报价、渠道、站点与别名。用法见 tools/README.md。"""
import argparse
import math
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (ALIASES, FAMILY_NAME, FAMILY_ORDER, MODELS, RANK_EXCLUDED_FLAGS,
                    RELAYS, family, fmt, iter_csv, num, topup_map)

BILLING = {'token': '按量', 'call': '按次'}


def amount(raw):
    value = num(raw)
    if value is not None and math.isfinite(value) and value >= 0:
        return value
    return None


def price(row):
    if row['billing'] == 'call':
        return amount(row['call_usd'])
    if row['billing'] == 'token':
        return amount(row['input_usd_m'])
    return None


class Quotes:
    """同一计价单位的匹配统计，每站只保留最低的可用报价。"""

    def __init__(self):
        self.count = 0
        self.sites = set()
        self.groups = set()
        self.bases = set()
        self.best = {}

    def add(self, row, args):
        domain = row['domain']
        self.count += 1
        selected = args.billing is None or args.billing == row['billing']
        if args.mode == 'model' or selected:
            self.bases.add(row['model_base'])
        if not selected:
            return
        if args.mode == 'group':
            self.sites.add(domain)
            self.groups.add(row['group'])

        value = price(row)
        if value is None:
            return
        flags = (row.get('flag') or '').split('+')
        if not args.all and (value == 0 or not RANK_EXCLUDED_FLAGS.isdisjoint(flags)):
            return
        if domain not in self.best or value < self.best[domain][0]:
            self.best[domain] = (value, row)


def show_prices(a, matches, mode):
    quotes = matches[mode]
    other = 'call' if mode == 'token' else 'token'
    if other in matches:
        print(f'另有 {matches[other].count} 行{BILLING[other]}报价，可用 --{other} 查看。')
    if not quotes.count:
        print(f'没有匹配的{BILLING[mode]}报价。')
        return
    if not quotes.best:
        hint = '' if a.all else ' 可用 --all 纳入带标记的报价。'
        print(f'没有可用于排名的{BILLING[mode]}报价。{hint}')
        return

    topups = topup_map()
    converted = {}
    for domain, (value, _) in quotes.best.items():
        if domain in topups:
            cny = value * topups[domain]
            if math.isfinite(cny):
                converted[domain] = cny
    if a.cny:
        sites = sorted(converted, key=lambda d: (converted[d], d))
        order = '按实付 ¥ 升序，仅含公开有效充值价的站'
    else:
        sites = sorted(quotes.best, key=lambda d: (quotes.best[d][0], d))
        order = '按名义 $ 升序'
    if not sites:
        print(f'有 {len(quotes.best)} 站提供报价，均缺少可用于排名的实付价。')
        return

    unit = '每次调用' if mode == 'call' else '每百万 token，按输入价排名'
    flags = '含带标记的报价' if a.all else '已排除福利、占位、零价和异常低价'
    print(f'{len(sites)} 个站（{unit}，{order}，推算，{flags}）\n')
    columns = '%-32s %-12s %-11s %-9s %-10s %-12s %-22s %s'
    print(columns % ('站点', '名义$', '输出$', '充值¥/$', '实付¥', '标记', '分组', '原始模型名'))
    for domain in sites[:a.n]:
        value, row = quotes.best[domain]
        nominal = '$' + fmt(value) + ('/次' if mode == 'call' else '')
        output = '-'
        if mode == 'token' and amount(row['output_usd_m']) is not None:
            output = '$' + row['output_usd_m']
        real = '¥' + fmt(converted[domain]) if domain in converted else '-'
        print(columns % (domain, nominal, output, fmt(topups.get(domain)) or '-', real, row['flag'] or '-',
                         (row['group'] or '-')[:22], row['model']))


def cmd_model(a):
    q = a.q.strip().lower()
    matches = defaultdict(Quotes)
    exact = False
    for row in iter_csv(MODELS):
        base = row['model_base'].lower()
        if base == q:
            if not exact:
                # 首次遇到精确匹配，丢弃之前累计的模糊匹配。
                matches.clear()
                exact = True
        elif exact or (q not in base and q not in row['model'].lower()):
            continue
        if row['billing'] in BILLING:
            matches[row['billing']].add(row, a)

    if not matches:
        print(f'没有匹配 {a.q!r} 的模型报价。')
        return
    bases = sorted(set().union(*(quotes.bases for quotes in matches.values())))
    print('匹配 %d 个基础模型（%s%s）' % (len(bases), ', '.join(bases[:8]), ' …' if len(bases) > 8 else ''))
    mode = a.billing or max(matches, key=lambda unit: matches[unit].count)
    show_prices(a, matches, mode)


def cmd_group(a):
    q = a.q.strip().lower()
    model = (a.model or '').strip().lower()
    matches = defaultdict(Quotes)
    for row in iter_csv(MODELS):
        if row['billing'] not in BILLING:
            continue
        in_group = a.field != 'model' and q in (row['group'] or '').lower()
        in_name = a.field != 'group' and q in row['model'].lower()
        if not (in_group or in_name):
            continue
        if model and model not in row['model_base'].lower() and model not in row['model'].lower():
            continue
        matches[row['billing']].add(row, a)

    if not matches:
        print(f'没有符合渠道关键词 {a.q!r} 和筛选条件的报价。')
        return
    mode = a.billing or ('token' if 'token' in matches else 'call')
    quotes = matches[mode]
    print(f'渠道 {a.q!r}（{BILLING[mode]}）匹配 {len(quotes.sites)} 站 · {len(quotes.groups)} 个分组名'
          f' · {len(quotes.bases)} 个模型 · {quotes.count} 行报价')
    show_prices(a, matches, mode)


def cmd_site(a):
    host = a.q.strip().lower().rstrip('.')
    domain = next((r['canonical'] for r in iter_csv(ALIASES) if r['alias'] == host), host)
    if domain != host:
        print(f'{host} 是 {domain} 的别名')
    info = next((r for r in iter_csv(RELAYS) if r['domain'] == domain), None)
    if not info:
        print(f'尚未收录 {host}（可用 find 查找）')
        return
    for k in ('domain', 'api_host', 'name', 'system', 'version', 'topup_cny_per_usd', 'discovered_via', 'veridrop_score', 'n_models', 'families',
              'aliases', 'backend_group', 'http_status', 'latency_ms', 'last_checked', 'tags', 'notes'):
        if info.get(k):
            print('%-15s %s' % (k, info[k]))
    by = defaultdict(list)
    for row in iter_csv(MODELS):
        if row['domain'] == domain:
            by[family(row['model_base'])].append(row)
    for c in FAMILY_ORDER:
        if c not in by:
            continue
        print('\n[%s] %d' % (FAMILY_NAME[c], len(by[c])))
        for r in sorted(by[c], key=lambda r: r['model'])[:a.n]:
            value = price(r)
            unit = '/次' if r['billing'] == 'call' else ''
            nominal = '$' + fmt(value) + unit if value is not None else '-'
            print('  %-40s %-11s %-10s %s' % (r['model'][:40], nominal, r['flag'] or '', r['group'][:30]))
        if len(by[c]) > a.n:
            print('  … 另 %d 个' % (len(by[c]) - a.n))


def cmd_find(a):
    q = a.q.strip().lower()
    for r in iter_csv(RELAYS):
        if q in r['domain'] or q in (r['name'] or '').lower():
            print('站点  %-34s %-8s 模型 %-5s %s' % (r['domain'], r['system'] or '-', r['n_models'], r['name'][:40]))
    for r in iter_csv(ALIASES):
        if q in r['alias']:
            print('别名  %-34s → %s (%s)' % (r['alias'], r['canonical'], r['reason']))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('mode', choices=['model', 'site', 'domain', 'find', 'group'])
    ap.add_argument('q', help='模型名、域名或关键词')
    ap.add_argument('--n', type=int, default=30, help='最多显示的报价数（site 按家族分别计数，默认 30）')
    ap.add_argument('--all', action='store_true', help='model/group 纳入福利、占位、零价和异常低价')
    billing = ap.add_mutually_exclusive_group()
    billing.add_argument('--call', dest='billing', action='store_const', const='call', help='只看按次计价')
    billing.add_argument('--token', dest='billing', action='store_const', const='token', help='只看按量计价')
    ap.add_argument('--cny', action='store_true', help='只看公开充值价的站，按实付 ¥ 排序')
    ap.add_argument('--model', help='group 模式下按模型名进一步筛选')
    ap.add_argument('--field', choices=['any', 'group', 'model'], default='any',
                    help='group 的关键词匹配位置（分组名、原始模型名或两者，默认两者）')
    a = ap.parse_args()
    if a.n < 0:
        ap.error('--n 需要为非负整数')
    {'model': cmd_model, 'site': cmd_site, 'domain': cmd_site, 'find': cmd_find,
     'group': cmd_group}[a.mode](a)


if __name__ == '__main__':
    main()
