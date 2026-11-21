#!/usr/bin/env python3
"""Build the reader-facing reports that are too detailed for the root READMEs."""
import os
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_stats import compute  # noqa: E402
from common import (FAMILY_NAME, FAMILY_ORDER, fmt, num, path, read_csv,
                    valid_topup)  # noqa: E402
from generate_by_model import MIN_SITES, fname  # noqa: E402


OUT = path('reports')


def esc(value):
    return str(value if value is not None else '').replace('|', '\\|')


def report_readme(s):
    return f"""# 报告中心

[返回中文首页](../README.md) · [English README](../README.en.md)

想找某一站，可在中转站报告浏览名单；要比较某个模型在各站的价格，直接从模型索引进入榜单。

## 导航

- [中转站报告](relays.md) — 前 100 站、模型家族覆盖和疑似同后端分组
- [店铺报告](shops.md) — 前 120 家店、SaaS 平台和自建系统
- [数据统计](../data/stats.md) — 来源、系统、充值价区间、计价与标记分布
- [模型索引](../data/relays/by-model/index.md) — {s['pages']} 个模型各有一页，可按站查看名义价和人民币估算价

## 复查入口

- [中转站主表](../data/relays/relays.csv) · [别名表](../data/relays/aliases.csv) · [站 × 模型报价](../data/relays/relay-models.csv)
- [已确认店铺](../data/shops/shops.csv) · [商品报价](../data/shops/products.csv) · [卡网候选审核表](../data/shops/candidates.csv)
- [字段与口径](../data/README.md) · [来源注册表](../data/raw/sources/README.md)
- [最近 Argon 监控报告](../data/monitor/report-argon.md) · [价格漂移摘要](../data/monitor/drift.md) · [监控历史 CSV](../data/monitor/history.csv)
- [原始资料索引](../data/raw/README.md) · [工具与更新流程](../tools/README.md)

## 当前口径

参考价来自公开页面或接口，未与账单核对。站点充值价以每 1 美元额度所需的人民币计，乘以模型的名义美元价格可估算人民币费用。店铺标价本身就是人民币。

模型榜单要求至少 {MIN_SITES} 站提供该基础模型且有可排名的报价，默认排除 `promo`、`zero`、`default`、`low` 和缺价。仅带 `high` 标记的报价仍可参与。
"""


def render_relays(s):
    m, relays = s['summ'], s['rl']
    lines = [
        '# 中转站报告',
        '',
        '[返回报告中心](README.md) · [中文首页](../README.md) · [English README](../README.en.md)',
        '',
        '> ⚠️ 这是公开信息目录，不是推荐榜或购买入口。站点状态、模型目录和价格会变化；价格为推算值，未对账。',
        '',
        f"当前主表有 **{m['sites']}** 个去重中转站（首页 HTTP 200：{s['up']}），{m['aliases']} 个别名/镜像，{m['model_rows']} 条站 × 模型报价。完整字段见 [relays.csv](../data/relays/relays.csv)、[aliases.csv](../data/relays/aliases.csv) 和 [relay-models.csv](../data/relays/relay-models.csv)。",
        '',
        '<a id="top-100-sites"></a>',
        '## 综合名单 · 前 100 站',
        '',
        '先列最近一次首页返回 HTTP 200 的站点，再按库中报价行数、Veridrop 分数从高到低排序，取前 100 站。`⚠️` 表示主表有人工标注。',
        '',
        '| # | 站点 | 站名 | 系统 | 模型数 | 覆盖 | 充值 ¥/$ | Veridrop | 状态 | 延迟 |',
        '|---|---|---|---|---|---|---|---|---|---|',
    ]

    def site_key(row):
        return (row['http_status'] == '200', int(row['n_models'] or 0), num(row['veridrop_score']) or 0)

    letter = [('openai', 'O'), ('claude', 'C'), ('gemini', 'G'), ('grok', 'X'), ('mimo', 'M'), ('deepseek', 'D')]
    for i, row in enumerate(sorted(relays, key=site_key, reverse=True)[:100], 1):
        families = set((row['families'] or '').split('/'))
        coverage = ''.join(label for code, label in letter if code in families) or '-'
        name = (row['name'] or '').strip()
        if len(name) > 18:
            name = name[:18] + '…'
        warning = '⚠️ ' if row.get('tags') else ''
        latency = row['latency_ms'] + 'ms' if row['latency_ms'] else '-'
        lines.append('| %d | `%s` | %s | %s | %s | %s | %s | %s | %s | %s |' % (
            i, warning + esc(row['domain']), esc(name) or '-', esc(row['system']) or '-',
            row['n_models'] or 0, coverage, fmt(valid_topup(row['topup_cny_per_usd'])) or '-',
            esc(row['veridrop_score']) or '-', esc(row['http_status']) or '-', latency))
    lines += [
        '',
        '覆盖缩写为 O=OpenAI、C=Claude、G=Gemini、X=Grok、M=MiMo、D=DeepSeek。充值 ¥/$ 是站点公开的“多少元买 1 美元额度”；实付价约为名义价 × 充值价。',
        f"带标注站点共 {sum(1 for row in relays if row.get('tags'))} 个，说明见 [annotations.csv](../data/relays/annotations.csv) 与 [数据说明](../data/README.md#标注annotationscsv)。完整主表仍以 [relays.csv](../data/relays/relays.csv) 为准。",
        '',
        '<a id="family-coverage"></a>',
        '## 模型覆盖 · 家族与榜单链接',
        '',
        f"家族覆盖统计来自 `relay-models.csv`。榜单只为至少 {MIN_SITES} 个站提供的基础模型生成；名义价单位为 USD/1M 输入或 USD/次，默认排名排除福利、零价、占位价、异常低价和缺价。",
        '',
        '| 家族 | 基础模型数 | 覆盖站点 | 覆盖最广的模型 |',
        '|---|---|---|---|',
    ]
    sites_of = defaultdict(set)
    for row in s['rm']:
        sites_of[row['model_base']].add(row['domain'])
    for code in FAMILY_ORDER:
        bases = s['fam_models'].get(code)
        if not bases:
            continue
        top = sorted(bases, key=lambda base: (-len(sites_of[base]), base))[:3]
        links = ' · '.join(
            '[%s](../data/relays/by-model/%s.md)' % (base, fname(base))
            if len(sites_of[base]) >= MIN_SITES else base
            for base in top
        )
        lines.append('| %s | %d | %d | %s |' % (
            FAMILY_NAME[code], len(bases), len(s['fam_sites'][code]), links))
    lines += [
        '',
        f"全部 {s['pages']} 个榜单的入口是 [data/relays/by-model/index.md](../data/relays/by-model/index.md)。榜单中的中位价只用于比较，不代表结算价。",
        '',
        '<a id="suspected-backends"></a>',
        '## 疑似同后端 · 价格表分组',
        '',
        f"共有 {m['backend_groups']} 组、{m['backend_group_sites']} 站被标为疑似同后端。不同品牌至少有 5 条报价、模型名及按量输入输出价全部相同时就会标记。分组不比较按次价格，也不证明站点属于同一运营方。下表按站数列出前 15 组。",
        '',
        '| 组 | 站数 | 站点 |',
        '|---|---|---|',
    ]
    for group, domains in sorted(s['groups'].items(), key=lambda item: (-len(item[1]), item[0]))[:15]:
        shown = ' · '.join('`%s`' % domain for domain in sorted(domains)[:6])
        if len(domains) > 6:
            shown += ' …'
        lines.append('| %s | %d | %s |' % (group, len(domains), shown))
    lines += [
        '',
        '同后端编号每次重建可能变化。更多统计见 [data/stats.md](../data/stats.md)，发现和验证过程见 [来源注册表](../data/raw/sources/README.md)。',
        '',
        '[↑ 回到报告中心](README.md)',
    ]
    return '\n'.join(lines) + '\n'


def render_shops(s):
    shops, products = s['sh'], s['pr']
    lines = [
        '# 店铺报告',
        '',
        '[返回报告中心](README.md) · [中文首页](../README.md) · [English README](../README.en.md)',
        '',
        '> ⚠️ 这是公开页面整理，不提供购买入口，不担保商品、店铺或账号权益。价格可能已变动，购买前应核对原站及服务条款。',
        '',
        f"已确认店铺 {len(shops)} 家（SaaS {sum(1 for row in shops if row['hosting'] == 'SaaS')} / 自建 {sum(1 for row in shops if row['hosting'] == '自建')}），商品报价 {len(products)} 行。完整主表见 [shops.csv](../data/shops/shops.csv) 和 [products.csv](../data/shops/products.csv)。",
        f"另有 {len(s['shop_candidates'])} 条首页指纹候选，单独保存在 [candidates.csv](../data/shops/candidates.csv)，不计入上面的已确认店铺，也不会自动晋级。候选审核证据见 [来源注册表](../data/raw/sources/README.md)。",
        '',
        '<a id="top-120-shops"></a>',
        '## 店铺名单 · 按商品数前 120',
        '',
        '表中价位为公开商品的人民币价格范围，商品可能包含账号、会员、卡密、教程或其它虚拟商品；同一店铺的来源列可能有多个来源。排序保留主表顺序中的并列项。',
        '',
        '| # | 店铺 | 归属 | 卖什么 | 价位(¥) | 来源 |',
        '|---|---|---|---|---|---|',
    ]
    count = Counter(row['shop'] for row in products)
    short = {'Gemini Ultra': 'Ultra', 'ChatGPT': 'GPT'}
    for i, row in enumerate(sorted(shops, key=lambda item: -count.get(item['shop'], 0))[:120], 1):
        owner = row['platform'] or ('自建/' + (row['system'] or '未知'))
        categories = '/'.join(short.get(category, category) for category in (row['categories'] or '').split('/')
                              if category and category != '其它') or '其它'
        lines.append('| %d | %s | %s | %s | %s | %s |' % (
            i, esc(row['shop']), esc(owner), esc(categories), esc(row['price_range']), esc(row['source'])))
    lines += [
        '',
        f"当前共 {len(shops)} 家已确认店铺，上表列出最多 120 家。完整字段、域名和核验日期见 [shops.csv](../data/shops/shops.csv)；逐商品记录见 [products.csv](../data/shops/products.csv)。",
        '',
        '<a id="platforms-and-systems"></a>',
        '## 发卡平台与系统',
        '',
        '**发卡平台（SaaS，商家入驻）**',
        '',
        '| 平台 | 域名 | 说明 |',
        '|---|---|---|',
    ]
    for row in read_csv(path('data', 'shops', 'platforms.csv')):
        lines.append('| %s | `%s` | %s |' % (esc(row['platform']), esc(row['domain']), esc(row['note'])))
    lines += [
        '',
        '**发卡系统（开源软件，自建用）**',
        '',
        '| 系统 | 仓库 | 说明 |',
        '|---|---|---|',
    ]
    for row in read_csv(path('data', 'shops', 'systems.csv')):
        lines.append('| %s | %s | %s |' % (esc(row['system']), esc(row['repo']) or '-', esc(row['note'])))
    lines += [
        '',
        '平台是商家入驻的托管服务，系统是商家自行部署的软件；二者不要与具体店铺数混为一谈。平台和系统的原始说明见 [platforms.csv](../data/shops/platforms.csv) 与 [systems.csv](../data/shops/systems.csv)。',
        '',
        '[↑ 回到报告中心](README.md)',
    ]
    return '\n'.join(lines) + '\n'


def main():
    s = compute()
    os.makedirs(OUT, exist_ok=True)
    s['shop_candidates'] = read_csv(path('data', 'shops', 'candidates.csv'))
    with open(os.path.join(OUT, 'README.md'), 'w', encoding='utf-8') as fh:
        fh.write(report_readme(s))
    with open(os.path.join(OUT, 'relays.md'), 'w', encoding='utf-8') as fh:
        fh.write(render_relays(s))
    with open(os.path.join(OUT, 'shops.md'), 'w', encoding='utf-8') as fh:
        fh.write(render_shops(s))
    print('reports written', OUT)
    print('relay rows', len(s['rl']), 'shop rows', len(s['sh']), 'product rows', len(s['pr']))


if __name__ == '__main__':
    main()
