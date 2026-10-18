#!/usr/bin/env python3
"""从 data/ 生成 README.md（勿手改 README）。"""
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa
from build_stats import compute
from generate_by_model import fname, MIN_SITES

LETTER = [('openai', 'O'), ('claude', 'C'), ('gemini', 'G'), ('grok', 'X'), ('mimo', 'M'), ('deepseek', 'D')]


def esc(x):
    return str(x if x is not None else '').replace('|', '\\|')


def main():
    s = compute()
    m, rl, sh, pr = s['summ'], s['rl'], s['sh'], s['pr']
    L = []
    A = L.append
    A('# ai-relay-atlas · AI 中转站与发卡地图')
    A('')
    A('[![License: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE) '
      '[![Data: CC BY-NC 4.0](https://img.shields.io/badge/data-CC%20BY--NC%204.0-lightgrey.svg)](DATA-LICENSE.md) '
      '[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)')
    A('')
    A('把 **AI API 中转站**和 **发卡/卡网店铺**放进同一张"上游地图"。**本阶段以收全名单为主**，细节后续补充。')
    A('')
    A('> ⚠️ 仅收录公开信息，不提供购买入口、不参与交易、不担保。价格为推算值、未对账，以原站为准。见 [DISCLAIMER.md](DISCLAIMER.md)。')
    A('')
    A('<a id="toc"></a>')
    A('## 目录')
    A('')
    for t, a in [('数据概览', 'stats'), ('快速开始', 'quickstart'), ('中转站 · 综合名单', 'relays'),
                 ('中转站 · 模型覆盖', 'coverage'), ('中转站 · 疑似同后端', 'backend'), ('卡网 · 店铺名单', 'shops'),
                 ('卡网 · 平台与系统', 'shop-platforms'), ('数据文件', 'files'), ('文档', 'docs'),
                 ('数据来源', 'sources'), ('授权', 'license'), ('贡献', 'contributing')]:
        A('- [%s](#%s)' % (t, a))
    A('')

    A('<a id="stats"></a>')
    A('## 数据概览')
    A('')
    A('| 项 | 数量 |')
    A('|---|---|')
    A('| 中转站（去重后） | %d（首页可访问 %d） |' % (m['sites'], s['up']))
    A('| 合并的别名/镜像域名 | %d |' % m['aliases'])
    A('| 已剔除的泛解析子域 | %d |' % m['wildcard_removed'])
    A('| 站 × 模型 报价 | %d |' % m['model_rows'])
    A('| 基础模型数（不同模型，非站数） | %d |' % m['model_bases'])
    A('| 发卡店铺 | %d（SaaS %d / 自建 %d） |' % (len(sh), sum(1 for x in sh if x['hosting'] == 'SaaS'),
                                            sum(1 for x in sh if x['hosting'] == '自建')))
    A('| 发卡商品报价 | %d |' % len(pr))
    A('')
    A('更多分布见 [data/stats.md](data/stats.md)。')
    A('')

    A('<a id="quickstart"></a>')
    A('## 快速开始')
    A('')
    A('```bash')
    A('git clone https://github.com/ruruamour/ai-relay-atlas.git && cd ai-relay-atlas')
    A('python3 tools/query.py model gemini-4-argon      # 某模型哪些站有、什么价')
    A('python3 tools/query.py site api.openlux.ai       # 某站的全部模型（别名会自动换成主域名）')
    A('bash tools/build.sh                              # 改数据后重建：去重 → 榜单 → 统计 → README')
    A('```')
    A('')

    A('<a id="relays"></a>')
    A('## 中转站 · 综合名单')
    A('')
    A('| # | 站点 | 系统 | 模型数 | 覆盖 | 别名 | Veridrop | 状态 | 延迟 |')
    A('|---|---|---|---|---|---|---|---|---|')

    def key(r):
        return (r['http_status'] == '200', int(r['n_models'] or 0), num(r['veridrop_score']) or 0)
    for i, r in enumerate(sorted(rl, key=key, reverse=True)[:100], 1):
        fams = set((r['families'] or '').split('/'))
        cov = ''.join(l for c, l in LETTER if c in fams) or '-'
        A('| %d | `%s` | %s | %s | %s | %s | %s | %s | %s |' % (
            i, esc(r['domain']), esc(r['system']) or '-', r['n_models'] or 0, cov, r['aliases'] or 0,
            esc(r['veridrop_score']) or '-', esc(r['http_status']) or '-',
            (r['latency_ms'] + 'ms') if r['latency_ms'] else '-'))
    A('')
    A('覆盖：O=OpenAI · C=Claude · G=Gemini · X=Grok · M=MiMo · D=DeepSeek')
    A('')
    A('完整名单（%d 站）：[relays.csv](data/relays/relays.csv) · 别名：[aliases.csv](data/relays/aliases.csv) · '
      '报价：[relay-models.csv](data/relays/relay-models.csv)' % m['sites'])
    A('')
    A('[↑ 目录](#toc)')
    A('')

    A('<a id="coverage"></a>')
    A('## 中转站 · 模型覆盖')
    A('')
    A('| 家族 | 基础模型数 | 覆盖站点 | 覆盖最广的模型 |')
    A('|---|---|---|---|')
    sites_of = defaultdict(set)
    for r in s['rm']:
        sites_of[r['model_base']].add(r['domain'])
    for c in FAMILY_ORDER:
        bases = s['fam_models'].get(c)
        if not bases:
            continue
        top = sorted(bases, key=lambda b: -len(sites_of[b]))[:3]
        links = ' · '.join(('[%s](data/relays/by-model/%s.md)' % (b, fname(b))) if len(sites_of[b]) >= MIN_SITES else b
                           for b in top)
        A('| %s | %d | %d | %s |' % (FAMILY_NAME[c], len(bases), len(s['fam_sites'][c]), links))
    A('')
    A('全部 %d 个模型榜单：[by-model/index.md](data/relays/by-model/index.md)' % s['pages'])
    A('')
    A('[↑ 目录](#toc)')
    A('')

    A('<a id="backend"></a>')
    A('## 中转站 · 疑似同后端')
    A('')
    A('价格表完全相同的跨品牌站点，共 %d 组 / %d 站。前 15 组：' % (m['backend_groups'], m['backend_group_sites']))
    A('')
    A('| 组 | 站数 | 站点 |')
    A('|---|---|---|')
    for g, ds in sorted(s['groups'].items(), key=lambda kv: (-len(kv[1]), kv[0]))[:15]:
        A('| %s | %d | %s |' % (g, len(ds), ' · '.join('`%s`' % d for d in sorted(ds)[:6]) + (' …' if len(ds) > 6 else '')))
    A('')
    A('[↑ 目录](#toc)')
    A('')

    A('<a id="shops"></a>')
    A('## 卡网 · 店铺名单')
    A('')
    A('| # | 店铺 | 归属 | 卖什么 | 价位(¥) | 来源 |')
    A('|---|---|---|---|---|---|')
    cnt = defaultdict(int)
    for x in pr:
        cnt[x['shop']] += 1
    short = {'Gemini Ultra': 'Ultra', 'ChatGPT': 'GPT'}
    for i, r in enumerate(sorted(sh, key=lambda r: -cnt.get(r['shop'], 0))[:120], 1):
        own = r['platform'] or ('自建/' + (r['system'] or '未知'))
        cats = '/'.join(short.get(c, c) for c in (r['categories'] or '').split('/') if c and c != '其它') or '其它'
        A('| %d | %s | %s | %s | %s | %s |' % (i, esc(r['shop']), esc(own), esc(cats), esc(r['price_range']), esc(r['source'])))
    A('')
    A('共 %d 家，上表按商品数取前 120。完整：[shops.csv](data/shops/shops.csv) · [products.csv](data/shops/products.csv)' % len(sh))
    A('')
    A('[↑ 目录](#toc)')
    A('')

    A('<a id="shop-platforms"></a>')
    A('## 卡网 · 平台与系统')
    A('')
    A('**发卡平台（SaaS，商家入驻）**')
    A('')
    A('| 平台 | 域名 | 说明 |')
    A('|---|---|---|')
    for r in read_csv(path('data', 'shops', 'platforms.csv')):
        A('| %s | `%s` | %s |' % (esc(r['platform']), esc(r['domain']), esc(r['note'])))
    A('')
    A('**发卡系统（开源软件，自建用）**')
    A('')
    A('| 系统 | 仓库 | 说明 |')
    A('|---|---|---|')
    for r in read_csv(path('data', 'shops', 'systems.csv')):
        A('| %s | %s | %s |' % (esc(r['system']), esc(r['repo']) or '-', esc(r['note'])))
    A('')
    A('[↑ 目录](#toc)')
    A('')

    A('<a id="files"></a>')
    A('## 数据文件')
    A('')
    A('| 路径 | 内容 |')
    A('|---|---|')
    A('| `data/relays/relays.csv` | 中转站主表（%d 站，一站一行） |' % m['sites'])
    A('| `data/relays/aliases.csv` | 别名/镜像域名 → 主域名（%d） |' % m['aliases'])
    A('| `data/relays/relay-models.csv` | 站 × 模型 × 价格（%d） |' % m['model_rows'])
    A('| `data/relays/by-model/` | 模型榜单（%d 页） |' % s['pages'])
    A('| `data/relays/medians.json` | 各模型正常价中位数 |')
    A('| `data/relays/relay-systems.csv` | 中转站软件名录 |')
    A('| `data/shops/` | 发卡平台、系统、店铺、商品 |')
    A('| `data/raw/` | 原始产物、发现来源、泛解析缓存 |')
    A('| `data/stats.md` | 统计分布 |')
    A('')
    A('字段说明见 [data/README.md](data/README.md)。')
    A('')
    A('[↑ 目录](#toc)')
    A('')

    A('<a id="docs"></a>')
    A('## 文档')
    A('')
    A('| 文档 | 内容 |')
    A('|---|---|')
    A('| [pricing-basics.md](docs/pricing-basics.md) | 倍率/价格怎么算、标记含义 |')
    A('| [glossary.md](docs/glossary.md) | 黑话表 |')
    A('| [how-to-choose.md](docs/how-to-choose.md) | 怎么选上游 / 避坑 |')
    A('| [tools/README.md](tools/README.md) | 脚本与更新流程 |')
    A('')
    A('[↑ 目录](#toc)')
    A('')

    A('<a id="sources"></a>')
    A('## 数据来源')
    A('')
    A('- 中转站：Veridrop 目录、GitHub 公开名单、对已知域名的子域/后缀扩展扫描；价格取自各站公开的 `/api/pricing`、`/api/v1/model-plaza`')
    A('- 卡网：OpenPrice、水獭比价(shuita.xyz)、PriceAI、AI号探、AiFaKa')
    A('- 原始报价版权归各来源站，见 [DATA-LICENSE.md](DATA-LICENSE.md)')
    A('')
    A('<a id="license"></a>')
    A('## 授权')
    A('')
    A('- 代码 **MIT** · [LICENSE](LICENSE)')
    A('- 编排与整理 **CC BY-NC 4.0** · [DATA-LICENSE.md](DATA-LICENSE.md)')
    A('- 原始报价版权归各来源站')
    A('')
    A('<a id="contributing"></a>')
    A('## 贡献')
    A('')
    A('见 [CONTRIBUTING.md](CONTRIBUTING.md)。')
    A('')
    A('[↑ 回到目录](#toc)')
    open(path('README.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print('README lines', len(L))


if __name__ == '__main__':
    main()
