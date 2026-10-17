#!/usr/bin/env python3
"""从 data/ 生成 README.md。结构：锚点 + 分层目录 + 摘要榜单；全量数据留在 data/。"""
import csv,os,re
from collections import defaultdict
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def rd(p):
    p=os.path.join(ROOT,p)
    return list(csv.DictReader(open(p,encoding='utf-8'))) if os.path.exists(p) else []
def f(v):
    try: return float(v)
    except: return None
def esc(x): return (str(x) if x is not None else '').replace('|','\\|')
rm=rd('data/relays/relay-models.csv'); rl=rd('data/relays/relays.csv')
sh=rd('data/shops/shops.csv'); pr=rd('data/shops/products.csv')
def norm(m):
    s=m.lower(); s=re.sub(r'^[\[\(][^\]\)]*[\]\)]','',s); s=re.sub(r'^[a-z0-9_\-]+/','',s)
    s=re.sub(r'[-_]?(free|thinking|opencode.*|cline.*|high|low|medium)$','',s); return s.strip('-')
by=defaultdict(dict)
for r in rm:
    p=f(r['input_usd_m'])
    if p is None or p<=0: continue
    k=norm(r['model']); d=r['domain']
    if d not in by[k] or p<by[k][d][0]: by[k][d]=(p,r)
MODELS=[('gemini-4-argon','Gemini 4 Argon'),('mimo-v2.6-pro','MiMo v2.6 Pro'),('mimo-v2.6-flash','MiMo v2.6 Flash'),
        ('mimo-v2.5-pro','MiMo v2.5 Pro'),('mimo-v2.5','MiMo v2.5'),('grok-4.5','Grok 4.5'),
        ('gemini-3.8-flash','Gemini 3.8 Flash'),('gemini-3.7-flash','Gemini 3.7 Flash'),('gemini-2.5-flash','Gemini 2.5 Flash')]
nmodel=sum(1 for k,v in by.items() if len(v)>=8)
L=[]
A=L.append
A('# ai-relay-atlas · AI 中转站与发卡地图'); A('')
A('[![License: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE) [![Data: CC BY-NC 4.0](https://img.shields.io/badge/data-CC%20BY--NC%204.0-lightgrey.svg)](DATA-LICENSE.md) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)'); A('')
A('把 **AI API 中转站**和 **发卡/卡网店铺**放进同一张"上游地图"。本页是摘要与榜单，全量数据在 [`data/`](data/README.md)。'); A('')
A('> ⚠️ 仅收录公开信息，不提供购买入口、不参与交易、不担保。价格为推算值、未对账，以原站为准。见 [DISCLAIMER.md](DISCLAIMER.md)。'); A('')
A('<a id="toc"></a>'); A('## 目录'); A('')
A('- [数据概览](#stats)')
A('- [快速开始](#quickstart)')
A('- [中转站 · 各模型最低价](#relays)')
for k,t in MODELS:
    if by.get(k): A('  - [%s](#model-%s)'%(t,k.replace('.','-')))
A('- [发卡](#shops)')
A('  - [平台与系统](#shop-platforms)')
A('  - [Gemini Pro 低价](#shop-gemini-pro)')
A('  - [Google AI Ultra 20x](#shop-ultra-20x)')
A('  - [店铺速览](#shop-list)')
A('- [数据文件](#files)')
A('- [文档](#docs)')
A('- [数据来源](#sources)')
A('- [授权](#license)')
A('- [贡献](#contributing)')
A('')
A('<a id="stats"></a>'); A('## 数据概览'); A('')
A('| 项 | 数量 |'); A('|---|---|')
A('| 中转站（域名） | %d |'%len(rl))
A('| 中转站 × 模型 报价 | %d |'%len(rm))
A('| 发卡店铺 | %d（SaaS %d / 自建 %d） |'%(len(sh),sum(1 for x in sh if x['hosting']=='SaaS'),sum(1 for x in sh if x['hosting']=='自建')))
A('| 发卡商品报价 | %d |'%len(pr))
A('| 按模型榜单（≥8 家） | %d |'%nmodel)
A('')
A('<a id="quickstart"></a>'); A('## 快速开始'); A('')
A('```bash')
A('git clone https://github.com/ruruamour/ai-relay-atlas.git && cd ai-relay-atlas')
A('python3 tools/query.py model gemini-4-argon --n 30')
A('python3 tools/query.py domain api.openlux.ai')
A('```'); A('')
A('更新数据后重生成本页：')
A('```bash')
A('python3 tools/normalize.py && python3 tools/normalize_shops.py \\')
A('  && python3 tools/generate_by_model.py && python3 tools/build_readme.py')
A('```'); A('')
A('<a id="relays"></a>'); A('## 中转站 · 各模型最低价 Top 15'); A('')
A('> 实际价 = `model_ratio × group_ratio × 2`，USD / 1M 输入，已排除 0 价与免费组。完整榜单见 [by-model/index.md](data/relays/by-model/index.md)。'); A('')
for key,title in MODELS:
    items=by.get(key)
    if not items: continue
    it=sorted(items.items(),key=lambda kv:kv[1][0])[:15]
    A('<a id="model-%s"></a>'%key.replace('.','-'))
    A('### %s（%d 家）'%(title,len(items))); A('')
    A('| # | 站点 | 输入 | 输出 | 倍率 | 分组 |'); A('|---|---|---|---|---|---|')
    for i,(d,v) in enumerate(it,1):
        r=v[1]; out=f(r['output_usd_m'])
        A('| %d | `%s` | $%g | %s | %s | %s |'%(i,esc(d),v[0],('$%g'%out) if out is not None else '-',esc(r['group_ratio']),esc(r['group'])))
    A(''); A('[↑ 目录](#toc)'); A('')
A('<a id="shops"></a>'); A('## 发卡'); A('')
A('<a id="shop-platforms"></a>'); A('### 平台与系统'); A('')
A('**发卡平台（SaaS，商家入驻）**'); A('')
A('| 平台 | 域名 | 说明 |'); A('|---|---|---|')
for r in rd('data/shops/platforms.csv'): A('| %s | `%s` | %s |'%(esc(r['platform']),esc(r['domain']),esc(r['note'])))
A(''); A('**发卡系统（开源软件，自建用）**'); A('')
A('| 系统 | 仓库 | 说明 |'); A('|---|---|---|')
for r in rd('data/shops/systems.csv'): A('| %s | %s | %s |'%(esc(r['system']),esc(r['repo']) or '-',esc(r['note'])))
A(''); A('[↑ 目录](#toc)'); A('')
def cat(name): return [x for x in pr if x['category']==name and f(x['price_cny'])]
def dedup(rows):
    seen=set(); out=[]
    for x in rows:
        k=(x['shop'],x['item'],x['price_cny'])
        if k in seen: continue
        seen.add(k); out.append(x)
    return out
gp=sorted(dedup([x for x in cat('Gemini') if 'pro' in (x['item'] or '').lower() and '教程' not in (x['item'] or '') and '人机验证号' not in (x['item'] or '')]),key=lambda x:f(x['price_cny']))
A('<a id="shop-gemini-pro"></a>'); A('### Gemini Pro 低价 Top 15'); A('')
A('| 商品 | 价格(¥) | 店铺 | 归属 | 来源 |'); A('|---|---|---|---|---|')
for x in gp[:15]:
    own=x['platform'] or ('自建/'+(x['system'] or '未知'))
    A('| %s | ¥%s | %s | %s | %s |'%(esc((x['item'] or '')[:46]),esc(x['price_cny']),esc(x['shop']),esc(own),esc(x['source'])))
A(''); A('[↑ 目录](#toc)'); A('')
gu=sorted(dedup([x for x in cat('Gemini Ultra') if '20x' in (x['item'] or '').lower() and '教程' not in (x['item'] or '')]),key=lambda x:f(x['price_cny']))
A('<a id="shop-ultra-20x"></a>'); A('### Google AI Ultra 20x Top 15'); A('')
A('| 商品 | 价格(¥) | 店铺 | 归属 | 来源 |'); A('|---|---|---|---|---|')
for x in gu[:15]:
    own=x['platform'] or ('自建/'+(x['system'] or '未知'))
    A('| %s | ¥%s | %s | %s | %s |'%(esc((x['item'] or '')[:46]),esc(x['price_cny']),esc(x['shop']),esc(own),esc(x['source'])))
A(''); A('[↑ 目录](#toc)'); A('')
cnt=defaultdict(int)
for x in pr: cnt[x['shop']]+=1
A('<a id="shop-list"></a>'); A('### 店铺速览（按商品数 Top 20）'); A('')
A('| 店铺 | 归属 | 品类 | 价位(¥) | 来源 |'); A('|---|---|---|---|---|')
for r in sorted(sh,key=lambda r:-cnt.get(r['shop'],0))[:20]:
    own=r['platform'] or ('自建/'+(r['system'] or '未知'))
    A('| %s | %s | %s | %s | %s |'%(esc(r['shop']),esc(own),esc(r['categories']),esc(r['price_range']),esc(r['source'])))
A(''); A('完整店铺与商品：[shops.csv](data/shops/shops.csv) · [products.csv](data/shops/products.csv)'); A('')
A('[↑ 目录](#toc)'); A('')
A('<a id="files"></a>'); A('## 数据文件'); A('')
A('| 路径 | 内容 |'); A('|---|---|')
A('| `data/relays/relays.csv` | 中转站主表（域名/评分/模型） |')
A('| `data/relays/relay-models.csv` | 站 × 模型 × 价格（%d 条） |'%len(rm))
A('| `data/relays/relay-systems.csv` | 中转站软件名录 |')
A('| `data/relays/by-model/` | %d 个模型榜单 + index |'%nmodel)
A('| `data/shops/platforms.csv` | 发卡平台 |')
A('| `data/shops/systems.csv` | 发卡系统 |')
A('| `data/shops/shops.csv` | 店铺主表 |')
A('| `data/shops/products.csv` | 商品报价（%d 条） |'%len(pr))
A('| `data/raw/` | 原始产物与溯源 |')
A('| `data/stats.md` | 数据概览 |')
A('')
A('[↑ 目录](#toc)'); A('')
A('<a id="docs"></a>'); A('## 文档'); A('')
A('| 文档 | 内容 |'); A('|---|---|')
A('| [pricing-basics.md](docs/pricing-basics.md) | 倍率/价格怎么算 |')
A('| [glossary.md](docs/glossary.md) | 黑话表（质保/首登/RT/反重力/拼车…） |')
A('| [how-to-choose.md](docs/how-to-choose.md) | 怎么选上游 / 避坑 |')
A('| [CONTRIBUTING.md](CONTRIBUTING.md) | 贡献格式 |')
A('')
A('[↑ 目录](#toc)'); A('')
A('<a id="sources"></a>'); A('## 数据来源'); A('')
A('OpenPrice、水獭比价(shuita.xyz)、PriceAI、AI号探、AiFaKa、Veridrop，以及各中转站公开的 `/api/pricing`、`/api/v1/model-plaza`。原始报价版权归各来源站，见 [DATA-LICENSE.md](DATA-LICENSE.md)。'); A('')
A('<a id="license"></a>'); A('## 授权'); A('')
A('- 代码 **MIT** · [LICENSE](LICENSE)')
A('- 编排与整理 **CC BY-NC 4.0** · [DATA-LICENSE.md](DATA-LICENSE.md)')
A('- 原始报价版权归各来源站'); A('')
A('<a id="contributing"></a>'); A('## 贡献'); A('')
A('见 [CONTRIBUTING.md](CONTRIBUTING.md)。'); A('')
A('[↑ 回到目录](#toc)')
open(os.path.join(ROOT,'README.md'),'w',encoding='utf-8').write('\n'.join(L)+'\n')
print('README lines',len(L),'| models',nmodel)
