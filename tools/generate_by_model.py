#!/usr/bin/env python3
"""生成 data/relays/by-model/：每个基础模型一页 + index.md。
排名只用正常价格（排除 promo/zero/default/low），被排除的站点数写在页尾。
实付价 = 名义价 × 该站充值价（元/1 美元额度）；公开了充值价的站按实付价单独排一张表。"""
import glob
import os
import statistics
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa

OUT = path('data', 'relays', 'by-model')
MIN_SITES = 20
TOP = 50
BAD = {'promo', 'zero', 'default', 'low'}


def fname(b):
    return re.sub(r'[^a-z0-9.\-]+', '_', b).strip('_') or 'model'


def esc(x):
    return str(x or '').replace('|', '\\|')


def main():
    rows = read_csv(MODELS)
    tp = topup_map()
    warn = {r['domain'] for r in read_csv(RELAYS) if (r.get('tags') or '')}
    by = defaultdict(lambda: defaultdict(list))
    for r in rows:
        by[r['model_base']][r['domain']].append(r)
    os.makedirs(OUT, exist_ok=True)
    for f in glob.glob(os.path.join(OUT, '*.md')):
        os.remove(f)
    index = defaultdict(list)
    for base, sites in by.items():
        if len(sites) < MIN_SITES:
            continue
        good, bad = {}, 0
        call = sum(1 for rs in sites.values() if any(r['billing'] == 'call' for r in rs)) > len(sites) / 2
        for d, rs in sites.items():
            cand = []
            for r in rs:
                if BAD & set((r['flag'] or '').split('+')):
                    continue
                p = num(r['call_usd'] if call else r['input_usd_m'])
                if p is not None and p > 0 and (r['billing'] == 'call') == call:
                    cand.append((p, r))
            if cand:
                good[d] = min(cand, key=lambda x: x[0])
            else:
                bad += 1
        if not good:
            continue
        it = sorted(good.items(), key=lambda kv: kv[1][0])
        med = statistics.median(p for p, _ in good.values())
        real = sorted(((d, p, r, p * tp[d]) for d, (p, r) in good.items() if d in tp), key=lambda x: x[3])
        nom = [(d, p, r) for d, (p, r) in it if d not in tp]
        rmed = statistics.median(x[3] for x in real) if real else None
        u = '次' if call else '1M 输入'
        unit = '$/次' if call else '$/1M 输入'
        L = ['# %s' % base, '',
             '> %d 站提供 · 正常价 %d 站 · 名义中位价 **$%s**/%s%s · 推算，未对账' % (
                 len(sites), len(good), fmt(med), u,
                 (' · 实付中位价 **¥%.4g**/%s（%d 站公开充值价）' % (rmed, u, len(real))) if real else ''), '',
             '[← 返回索引](index.md)', '']

        def price_cell(r, p):
            if call:
                return '$' + fmt(p)
            o = num(r['output_usd_m'])
            return '$%s / %s' % (fmt(p), ('$' + fmt(o)) if o is not None else '-')
        if real:
            L += ['## 实付价（按 ¥ 排序）', '', '实付 = 名义价 × 充值价（元 / 1 美元额度）。', '',
                  '| # | 站点 | 实付 ¥ | 名义 $%s | 充值 ¥/$ | 分组 | 原始模型名 |' % ('' if call else ' 输入/输出'),
                  '|---|---|---|---|---|---|---|']
            for i, (d, p, r, rp) in enumerate(real[:TOP], 1):
                L.append('| %d | `%s` | ¥%s | %s | %s | %s | %s |' % (i, ('⚠️' if d in warn else '') + d, '%.4g' % rp, price_cell(r, p), fmt(tp[d]),
                                                                    esc(r['group']) or '-', esc(r['model'])))
            if len(real) > TOP:
                L.append('')
                L.append('> 另有 %d 站未列出。' % (len(real) - TOP))
            L.append('')
        if nom:
            L += ['## 名义价（未公开充值价，按 $ 排序）' if real else '## 名义价（按 $ 排序）', '',
                  '| # | 站点 | 名义 $%s | 分组 | 倍率 | 原始模型名 |' % ('' if call else ' 输入/输出'),
                  '|---|---|---|---|---|---|']
            for i, (d, p, r) in enumerate(nom[:TOP], 1):
                L.append('| %d | `%s` | %s | %s | %s | %s |' % (i, ('⚠️' if d in warn else '') + d, price_cell(r, p), esc(r['group']) or '-',
                                                              r['group_ratio'] or '-', esc(r['model'])))
            if len(nom) > TOP:
                L.append('')
                L.append('> 另有 %d 站未列出。' % (len(nom) - TOP))
            L.append('')
        if bad:
            L += ['> %d 站只有福利/占位/异常价，未参与排名。完整数据见 `relay-models.csv`。' % bad]
        open(os.path.join(OUT, fname(base) + '.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
        index[family(base)].append((base, len(sites), med, unit, rmed))
    total = sum(len(v) for v in index.values())
    L = ['# 按模型榜单', '', '> 共 %d 个模型（≥%d 站提供）。中位价只统计正常价格；名义价单位 USD/1M 输入，实付价 = 名义价 × 站点充值价（元/1 美元额度）。推算，未对账。' % (total, MIN_SITES), '']
    toc = [('[%s](#%s)' % (FAMILY_NAME[c], c)) for c in FAMILY_ORDER if index.get(c)]
    L += [' · '.join(toc), '']
    for c in FAMILY_ORDER:
        if not index.get(c):
            continue
        L += ['<a id="%s"></a>' % c, '## %s（%d）' % (FAMILY_NAME[c], len(index[c])), '',
              '| 模型 | 站点数 | 名义中位价 | 实付中位价 |', '|---|---|---|---|']
        for base, n, med, unit, rmed in sorted(index[c], key=lambda x: -x[1]):
            per = '/次' if unit == '$/次' else ''
            L.append('| [%s](%s.md) | %d | $%s%s | %s |' % (base, fname(base), n, fmt(med), per,
                                                           ('¥%.4g%s' % (rmed, per)) if rmed else '-'))
        L.append('')
    open(os.path.join(OUT, 'index.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print('by-model pages', total)


if __name__ == '__main__':
    main()
