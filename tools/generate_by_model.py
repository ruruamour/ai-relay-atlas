#!/usr/bin/env python3
"""生成 data/relays/by-model/：每个基础模型一页 + index.md。
排名只用正常价格（排除 promo/zero/default/low），被排除的站点数写在页尾。"""
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
        unit = '$/次' if call else '$/1M 输入'
        L = ['# %s' % base, '',
             '> %d 站提供 · 正常价 %d 站 · 中位价 **$%s**（%s）· 推算，未对账' % (len(sites), len(good), fmt(med), unit), '',
             '[← 返回索引](index.md)', '']
        if call:
            L += ['| # | 站点 | 每次 | 分组 | 倍率 | 原始模型名 |', '|---|---|---|---|---|---|']
        else:
            L += ['| # | 站点 | 输入 | 输出 | 分组 | 倍率 | 原始模型名 |', '|---|---|---|---|---|---|---|']
        for i, (d, (p, r)) in enumerate(it[:TOP], 1):
            if call:
                L.append('| %d | `%s` | $%s | %s | %s | %s |' % (i, d, fmt(p), esc(r['group']) or '-', r['group_ratio'] or '-', esc(r['model'])))
            else:
                o = num(r['output_usd_m'])
                L.append('| %d | `%s` | $%s | %s | %s | %s | %s |' % (i, d, fmt(p), ('$' + fmt(o)) if o is not None else '-',
                                                                     esc(r['group']) or '-', r['group_ratio'] or '-', esc(r['model'])))
        tail = []
        if len(it) > TOP:
            tail.append('另有 %d 站未列出' % (len(it) - TOP))
        if bad:
            tail.append('%d 站只有福利/占位/异常价，未参与排名' % bad)
        if tail:
            L += ['', '> ' + '；'.join(tail) + '。完整数据见 `relay-models.csv`。']
        open(os.path.join(OUT, fname(base) + '.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
        index[family(base)].append((base, len(sites), med, unit))
    total = sum(len(v) for v in index.values())
    L = ['# 按模型榜单', '', '> 共 %d 个模型（≥%d 站提供）。中位价只统计正常价格，推算，未对账。' % (total, MIN_SITES), '']
    toc = [('[%s](#%s)' % (FAMILY_NAME[c], c)) for c in FAMILY_ORDER if index.get(c)]
    L += [' · '.join(toc), '']
    for c in FAMILY_ORDER:
        if not index.get(c):
            continue
        L += ['<a id="%s"></a>' % c, '## %s（%d）' % (FAMILY_NAME[c], len(index[c])), '',
              '| 模型 | 站点数 | 中位价 |', '|---|---|---|']
        for base, n, med, unit in sorted(index[c], key=lambda x: -x[1]):
            L.append('| [%s](%s.md) | %d | $%s%s |' % (base, fname(base), n, fmt(med), '/次' if unit == '$/次' else ''))
        L.append('')
    open(os.path.join(OUT, 'index.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print('by-model pages', total)


if __name__ == '__main__':
    main()
