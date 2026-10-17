#!/usr/bin/env python3
"""从 data/ 生成 README.md。名单优先：中转站按综合信号排序，卡网按店铺粗列。"""
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
def norm(m):
    s=m.lower(); s=re.sub(r'^[\[\(][^\]\)]*[\]\)]','',s); s=re.sub(r'^[a-z0-9_\-]+/','',s)
    s=re.sub(r'[-_]?(free|thinking|opencode.*|cline.*|high|low|medium)$','',s); return s.strip('-')
def fam(k):
    if k.startswith('gemini'): return 'gemini'
    if k.startswith('grok'): return 'grok'
    if k.startswith('mimo'): return 'mimo'
    if k.startswith('claude'): return 'claude'
    if k.startswith('gpt') or k.startswith('o1') or k.startswith('o3') or k.startswith('o4'): return 'gpt'
    return 'other'
FAMNAME={'gemini':'Gemini','grok':'Grok','mimo':'MiMo','claude':'Claude','gpt':'OpenAI','other':'其他'}

rm=rd('data/relays/relay-models.csv'); rl=rd('data/relays/relays.csv')
sh=rd('data/shops/shops.csv'); pr=rd('data/shops/products.csv')

# 站点聚合
st=defaultdict(lambda:dict(models=set(),fams=set(),minp=None,rows=0,argon=False))
for r in rm:
    d=r['domain']; m=r['model'] or ''
    st[d]['rows']+=1; st[d]['models'].add(norm(m)); st[d]['fams'].add(fam(norm(m)))
    if 'argon' in m.lower(): st[d]['argon']=True
    p=f(r['input_usd_m'])
    if p is not None and p>0 and (st[d]['minp'] is None or p<st[d]['minp']): st[d]['minp']=p
vd={r['domain']:f(r['veridrop_score']) for r in rl if r.get('veridrop_score')}
name={r['domain']:r.get('name') for r in rl}
status={r['domain']:r.get('status') for r in rl}
alldoms=set(r['domain'] for r in rl)|set(st)
def score(d):
    v=vd.get(d) or 0
    n=len(st[d]['models']) if d in st else 0
    return (1 if v>0 else 0, v, n)
ranked=sorted(alldoms,key=lambda d:score(d),reverse=True)

L=[];A=L.append
A('# ai-relay-atlas · AI 中转站与发卡地图'); A('')
A('[![License: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE) [![Data: CC BY-NC 4.0](https://img.shields.io/badge/data-CC%20BY--NC%204.0-lightgrey.svg)](DATA-LICENSE.md) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)'); A('')
A('把 **AI API 中转站**和 **发卡/卡网店铺**放进同一张"上游地图"。**本阶段以收全名单为主**，细节后续补充。'); A('')
A('> ⚠️ 仅收录公开信息，不提供购买入口、不参与交易、不担保。价格为推算值、未对账，以原站为准。见 [DISCLAIMER.md](DISCLAIMER.md)。'); A('')
A('<a id="toc"></a>'); A('## 目录'); A('')
for t,a in [('数据概览','#stats'),('快速开始','#quickstart'),('中转站 · 综合名单','#relays'),('中转站 · 模型覆盖','#coverage'),
            ('卡网 · 店铺名单','#shops'),('卡网 · 平台与系统','#shop-platforms'),('数据文件','#files'),('文档','#docs'),
            ('数据来源','#sources'),('授权','#license'),('贡献','#contributing')]:
    A('- [%s](%s)'%(t,a))
A('')
A('<a id="stats"></a>'); A('## 数据概览'); A('')
A('| 项 | 数量 |'); A('|---|---|')
A('| 中转站（域名） | %d |'%len(alldoms))
A('| 中转站 × 模型 报价 | %d |'%len(rm))
A('| 模型名（去重） | %d |'%len(set(norm(r['model'] or '') for r in rm)))
A('| 发卡店铺 | %d（SaaS %d / 自建 %d） |'%(len(sh),sum(1 for x in sh if x['hosting']=='SaaS'),sum(1 for x in sh if x['hosting']=='自建')))
A('| 发卡商品报价 | %d |'%len(pr))
A('')
A('> 说明：**"模型名"是去重后的模型标识数量**（同一模型在多家站只算 1 个），不等于站数。'); A('')
A('<a id="quickstart"></a>'); A('## 快速开始'); A('')
A('```bash')
A('git clone https://github.com/ruruamour/ai-relay-atlas.git && cd ai-relay-atlas')
A('python3 tools/query.py model gemini-4-argon --n 30   # 查某模型')
A('python3 tools/query.py domain api.openlux.ai        # 查某站')
A('```'); A('')
A('重生成本页：`python3 tools/normalize.py && python3 tools/normalize_shops.py && python3 tools/generate_by_model.py && python3 tools/build_readme.py`'); A('')
# 综合名单
A('<a id="relays"></a>'); A('## 中转站 · 综合名单'); A('')
A('> **不按最低价排序**：低价多为福利/免费组，可用性低。这里按 **Veridrop 实测分 → 模型覆盖数** 排序，仅作线索。'); A('')
A('| # | 站点 | Veridrop | 模型数 | Gemini | Grok | MiMo | Argon | 最低价($/1M) | 状态 |')
A('|---|---|---|---|---|---|---|---|---|---|')
def mark(d,k): return '✓' if k in st[d]['fams'] else ''
for i,d in enumerate(ranked[:100],1):
    s=st[d]; v=vd.get(d)
    A('| %d | `%s` | %s | %d | %s | %s | %s | %s | %s | %s |'%(
        i,esc(d),('%g'%v) if v else '-',len(s['models']),mark(d,'gemini'),mark(d,'grok'),mark(d,'mimo'),('✓' if s['argon'] else ''),
        ('$%g'%s['minp']) if s['minp'] else '-',esc(status.get(d,''))))
A('')
A('完整名单（%d 站）：[relays.csv](data/relays/relays.csv) · 站×模型价：[relay-models.csv](data/relays/relay-models.csv)'%len(alldoms)); A('')
A('[↑ 目录](#toc)'); A('')
# 覆盖
A('<a id="coverage"></a>'); A('## 中转站 · 模型覆盖'); A('')
A('> 家族 → 模型名数 / 覆盖站点数。完整榜单见 [by-model/index.md](data/relays/by-model/index.md)。'); A('')
A('| 家族 | 模型名数 | 覆盖站点数 |'); A('|---|---|---|')
fammodels=defaultdict(set); famdoms=defaultdict(set)
for r in rm:
    k=norm(r['model'] or ''); fammodels[fam(k)].add(k); famdoms[fam(k)].add(r['domain'])
for code in ['gemini','grok','mimo','claude','gpt','other']:
    if fammodels.get(code):
        A('| %s | %d | %d |'%(FAMNAME[code],len(fammodels[code]),len(famdoms[code])))
A('')
A('[↑ 目录](#toc)'); A('')
# 卡网店铺
A('<a id="shops"></a>'); A('## 卡网 · 店铺名单'); A('')
A('> 按店铺列，粗记"卖什么"。**不提供购买入口**，`域名` 仅为标识。完整表：[shops.csv](data/shops/shops.csv) / [products.csv](data/shops/products.csv)。'); A('')
A('| # | 店铺 | 归属 | 卖什么 | 价位(¥) | 来源 |')
A('|---|---|---|---|---|---|')
cnt=defaultdict(int)
for x in pr: cnt[x['shop']]+=1
for i,r in enumerate(sorted(sh,key=lambda r:-cnt.get(r['shop'],0))[:120],1):
    own=r['platform'] or ('自建/'+(r['system'] or '未知'))
    raw=[c for c in (r['categories'] or '').split('/') if c and c!='其它']
    short={'Gemini Ultra':'Ultra','Gemini':'Gemini','ChatGPT':'GPT','Claude':'Claude','Grok':'Grok','Cursor':'Cursor','Kiro':'Kiro','邮箱':'邮箱'}
    cats='/'.join([short.get(c,c) for c in raw]) or '其它'
    A('| %d | %s | %s | %s | %s | %s |'%(i,esc(r['shop']),esc(own),esc(cats),esc(r['price_range']),esc(r['source'])))
A('')
A('共 %d 家店，上表按商品数取前 120。'%len(sh)); A('')
A('[↑ 目录](#toc)'); A('')
# 平台系统
A('<a id="shop-platforms"></a>'); A('## 卡网 · 平台与系统'); A('')
A('**发卡平台（SaaS，商家入驻）**'); A('')
A('| 平台 | 域名 | 说明 |'); A('|---|---|---|')
for r in rd('data/shops/platforms.csv'): A('| %s | `%s` | %s |'%(esc(r['platform']),esc(r['domain']),esc(r['note'])))
A(''); A('**发卡系统（开源软件，自建用）**'); A('')
A('| 系统 | 仓库 | 说明 |'); A('|---|---|---|')
for r in rd('data/shops/systems.csv'): A('| %s | %s | %s |'%(esc(r['system']),esc(r['repo']) or '-',esc(r['note'])))
A('')
A('[↑ 目录](#toc)'); A('')
A('<a id="files"></a>'); A('## 数据文件'); A('')
A('| 路径 | 内容 |'); A('|---|---|')
A('| `data/relays/relays.csv` | 中转站主表（%d 站） |'%len(alldoms))
A('| `data/relays/relay-models.csv` | 站 × 模型 × 价格（%d 条） |'%len(rm))
A('| `data/relays/relay-systems.csv` | 中转站软件名录 |')
A('| `data/relays/by-model/` | 按模型榜单（%d 个模型） |'%len(fammodels and set().union(*fammodels.values()) if fammodels else []))
A('| `data/shops/platforms.csv` / `systems.csv` | 发卡平台 / 系统 |')
A('| `data/shops/shops.csv` | 店铺主表（%d） |'%len(sh))
A('| `data/shops/products.csv` | 商品报价（%d） |'%len(pr))
A('| `data/raw/` | 原始产物与溯源 |')
A('| `data/stats.md` | 数据概览 |')
A('')
A('[↑ 目录](#toc)'); A('')
A('<a id="docs"></a>'); A('## 文档'); A('')
A('| 文档 | 内容 |'); A('|---|---|')
A('| [pricing-basics.md](docs/pricing-basics.md) | 倍率/价格怎么算 |')
A('| [glossary.md](docs/glossary.md) | 黑话表 |')
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
print('README lines',len(L))
