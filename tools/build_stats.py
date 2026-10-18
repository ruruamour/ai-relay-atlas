#!/usr/bin/env python3
"""统计：compute() 供 build_readme.py 复用；直接运行则写 data/stats.md。"""
import glob
import json
import os
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa


def compute():
    rl, rm, al = read_csv(RELAYS), read_csv(MODELS), read_csv(ALIASES)
    sh, pr = read_csv(path('data', 'shops', 'shops.csv')), read_csv(path('data', 'shops', 'products.csv'))
    summ = json.load(open(path('data', 'relays', 'summary.json')))
    fam_models, fam_sites = defaultdict(set), defaultdict(set)
    for r in rm:
        f = family(r['model_base'])
        fam_models[f].add(r['model_base'])
        fam_sites[f].add(r['domain'])
    flags = Counter()
    for r in rm:
        for f in (r['flag'] or '').split('+'):
            if f:
                flags[f] += 1
    groups = defaultdict(list)
    for r in rl:
        if r['backend_group']:
            groups[r['backend_group']].append(r['domain'])
    return dict(
        rl=rl, rm=rm, al=al, sh=sh, pr=pr, summ=summ,
        up=sum(1 for r in rl if r['http_status'] == '200'),
        pages=len(glob.glob(path('data', 'relays', 'by-model', '*.md'))) - 1,
        via=Counter(r['discovered_via'] for r in rl),
        system=Counter(r['system'] or '未知' for r in rl),
        fam_models=fam_models, fam_sites=fam_sites, flags=flags,
        billing=Counter(r['billing'] for r in rm),
        groups=groups,
        hosting=Counter((x['hosting'], x['platform'] or x['system']) for x in sh),
        category=Counter(x['category'] for x in pr),
    )


def main():
    s = compute()
    m = s['summ']
    L = ['# 数据概览', '', '## 中转站', '', '| 项 | 数量 |', '|---|---|',
         '| 中转站（去重后） | %d |' % m['sites'],
         '| 其中首页可访问 | %d |' % s['up'],
         '| 合并的别名/镜像域名 | %d |' % m['aliases'],
         '| 已剔除的泛解析子域 | %d |' % m['wildcard_removed'],
         '| 疑似同后端（同价表跨品牌） | %d 组 / %d 站 |' % (m['backend_groups'], m['backend_group_sites']),
         '| 站 × 模型 报价 | %d |' % m['model_rows'],
         '| 基础模型数（不同模型，非站数） | %d |' % m['model_bases'],
         '| 模型榜单页（≥20 站） | %d |' % s['pages'], '',
         '## 发现来源', '', '| 来源 | 站点 |', '|---|---|']
    L += ['| %s | %d |' % (k, v) for k, v in s['via'].most_common()]
    L += ['', '## 系统', '', '| 系统 | 站点 |', '|---|---|']
    L += ['| %s | %d |' % (k, v) for k, v in s['system'].most_common()]
    tps = [valid_topup(r['topup_cny_per_usd']) for r in s['rl'] if valid_topup(r['topup_cny_per_usd'])]
    if tps:
        L += ['', '## 充值价（元 / 1 美元额度）', '', '公开了充值价的站：%d。' % len(tps), '',
              '| 区间 | 站点 |', '|---|---|']
        for lo, hi, lab in [(0, 1.5, '≤1.5（约 1:1）'), (1.5, 3.5, '1.5–3.5'), (3.5, 6, '3.5–6'), (6, 99, '≥6（接近汇率）')]:
            L.append('| %s | %d |' % (lab, sum(1 for x in tps if lo < x <= hi or (lo == 0 and x <= hi))))
    L += ['', '## 模型家族', '', '| 家族 | 基础模型数 | 覆盖站点 |', '|---|---|---|']
    L += ['| %s | %d | %d |' % (FAMILY_NAME[c], len(s['fam_models'][c]), len(s['fam_sites'][c]))
          for c in FAMILY_ORDER if s['fam_models'].get(c)]
    L += ['', '## 计价与标记', '', '| 项 | 报价行 |', '|---|---|']
    L += ['| 按 token 计价 | %d |' % s['billing'].get('token', 0), '| 按次计价 | %d |' % s['billing'].get('call', 0)]
    names = {'promo': '福利/特价分组', 'default': '占位价（未配置倍率）', 'zero': '0 价', 'low': '异常低价', 'high': '异常高价'}
    L += ['| 标记：%s | %d |' % (names.get(k, k), v) for k, v in s['flags'].most_common()]
    L += ['', '## 发卡店铺', '', '| 项 | 数量 |', '|---|---|', '| 店铺 | %d |' % len(s['sh']), '| 商品报价 | %d |' % len(s['pr']),
          '', '| 归属 | 店铺 |', '|---|---|']
    L += ['| %s / %s | %d |' % (k[0], k[1], v) for k, v in s['hosting'].most_common()]
    L += ['', '| 品类 | 商品 |', '|---|---|']
    L += ['| %s | %d |' % (k, v) for k, v in s['category'].most_common()]
    open(path('data', 'stats.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print('stats.md written')


if __name__ == '__main__':
    main()
