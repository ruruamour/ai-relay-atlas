#!/usr/bin/env python3
"""掺水嫌疑检测：旗舰模型挂牌价远低于全网中位价的站。
只用来出"疑似"清单，人工复核后才写进 annotations.csv。

判据：
  1. 只看按 token 计价的旗舰文本模型（opus / sonnet-5 / gpt-6 / gpt-5.6 / gemini-*-pro / gemini-4-argon /
     kimi-k3 / glm-5 / deepseek-v4-pro / grok-4.5+），语音、图像、嵌入、长尾开源模型一律不比；
  2. 该模型必须有 ≥20 个站在卖，中位价才可信；
  3. 本站在该模型的正常价 < 中位价 10% 记一次"可疑"（排除 promo/default/zero 行）；
  4. 站点有 ≥2 次可疑才上榜，分数 = 次数 + 0.5×（<1% 的次数）。
输出 data/relays/suspicious.csv，不自动写标注。
"""
import os
import re
import statistics
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa

OUT = path('data', 'relays', 'suspicious.csv')
FLAG_STOP = {'promo', 'default', 'zero'}  # low 是信号本身，不排除
HOT = re.compile(r'^(claude-(opus|sonnet-5)|gpt-(6|5\.6)|gemini-(3\.[0-9]+-pro|4-argon)|kimi-k3|glm-5|'
                 r'deepseek-v4-pro|grok-4\.[5-9])')
MIN_SITES = 20
THRESH = 0.10


def main():
    rows = read_csv(MODELS)
    per_model = defaultdict(dict)
    for r in rows:
        if r['billing'] != 'token' or not HOT.match(r['model_base'] or ''):
            continue
        if FLAG_STOP & set((r['flag'] or '').split('+')):
            continue
        p = num(r['input_usd_m'])
        if not p or p <= 0:
            continue
        d, b = r['domain'], r['model_base']
        if d not in per_model[b] or p < per_model[b][d][0]:
            per_model[b][d] = (p, r['group'], r['model'])
    med = {b: statistics.median(v[0] for v in d.values()) for b, d in per_model.items() if len(d) >= MIN_SITES}
    per_site = defaultdict(list)
    for b, d in per_model.items():
        m = med.get(b)
        if not m:
            continue
        for dom, (p, g, raw) in d.items():
            if p / m < THRESH:
                per_site[dom].append((p / m, p, m, b, g, raw))
    out = []
    for dom, items in per_site.items():
        if len(items) < 2:
            continue
        score = len(items) + 0.5 * sum(1 for x in items if x[0] < 0.01)
        ex = sorted(items)[:3]
        out.append(dict(domain=dom, score=round(score, 1), flags=len(items),
                        worst_pct=round(min(x[0] for x in items) * 100, 2),
                        examples=' | '.join('%s $%s vs 中位 $%s（%.2f%%）' % (x[3], fmt(x[1]), fmt(x[2]), x[0] * 100)
                                            for x in ex)))
    out.sort(key=lambda r: (-r['score'], r['worst_pct'], r['domain']))
    write_csv(OUT, ['domain', 'score', 'flags', 'worst_pct', 'examples'], out)
    print('写入 %s：%d 个疑似（比较了 %d 个旗舰模型）' % (OUT, len(out), len(med)))
    print('%-30s %-6s %-5s %-7s %s' % ('站点', '分数', '次数', '最低%', '样例'))
    for r in out[:14]:
        print('%-30s %-6s %-5d %-7s %s' % (r['domain'], r['score'], r['flags'], r['worst_pct'], r['examples'][:74]))


if __name__ == '__main__':
    main()
