#!/usr/bin/env python3
"""从 data/ 生成 README.md（内嵌榜单，全量数据仍在 CSV）。"""
import csv,os,re
from collections import defaultdict
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def rd(p):
    p=os.path.join(ROOT,p)
    return list(csv.DictReader(open(p,encoding='utf-8'))) if os.path.exists(p) else []
def esc(x): return (str(x) if x is not None else '').replace('|','\\|')
def f(v):
    try: return float(v)
    except: return None
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
        ('mimo-v2.5-pro','MiMo v2.5 Pro'),('grok-4.5','Grok 4.5'),('gemini-3.8-flash','Gemini 3.8 Flash')]
L=[]
L+=['# ai-relay-atlas · AI 中转站与发卡地图','',
'[![License: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE) [![Data: CC BY-NC 4.0](https://img.shields.io/badge/data-CC%20BY--NC%204.0-lightgrey.svg)](DATA-LICENSE.md) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)','',
'把 **AI API 中转站**和 **发卡/卡网店铺**放进同一张"上游地图"。README 直接给榜单，全量数据在 `data/`。','',
'> ⚠️ 仅收录公开信息，不提供购买入口、不参与交易、不担保。价格为推算值、未对账，以原站为准。见 [DISCLAIMER.md](DISCLAIMER.md)。','',
'## 数据概览','','| 项 | 数量 |','|---|---|',
'| 中转站（域名） | %d |'%len(rl),'| 中转站 × 模型 报价 | %d |'%len(rm),
'| 发卡店铺 | %d（SaaS %d / 自建 %d） |'%(len(sh),sum(1 for x in sh if x['hosting']=='SaaS'),sum(1 for x in sh if x['hosting']=='自建')),
'| 发卡商品报价 | %d |'%len(pr),'| 按模型榜单 | %d（≥8 家） |'%sum(1 for k,v in by.items() if len(v)>=8),'',
'```bash\npython3 tools/query.py model gemini-4-argon --n 30\npython3 tools/query.py domain api.openlux.ai\n```','',
'## 中转站 · 各模型最低价 Top 15','',
'> 实际价 = `model_ratio × group_ratio × 2`，USD / 1M 输入，已排除 0 价与免费组。完整榜单见 [by-model/](data/relays/by-model/index.md)。','']
for key,title in MODELS:
    items=by.get(key)
    if not items: continue
    it=sorted(items.items(),key=lambda kv:kv[1][0])[:15]
    L+=['### %s（%d 家）'%(title,len(items)),'','| # | 站点 | 输入 | 输出 | 倍率 | 分组 |','|---|---|---|---|---|---|']
    for i,(d,v) in enumerate(it,1):
        r=v[1]; out=f(r['output_usd_m'])
        L.append('| %d | `%s` | $%g | %s | %s | %s |'%(i,esc(d),v[0],('$%g'%out) if out is not None else '-',esc(r['group_ratio']),esc(r['group'])))
    L.append('')
# shops
L+=['## 发卡 · 平台与系统','','**发卡平台（SaaS，商家入驻）**','','| 平台 | 域名 | 说明 |','|---|---|---|']
for r in rd('data/shops/platforms.csv'): L.append('| %s | `%s` | %s |'%(r['platform'],r['domain'],r['note']))
L+=['','**发卡系统（开源软件，自建用）**','','| 系统 | 仓库 | 说明 |','|---|---|---|']
for r in rd('data/shops/systems.csv'): L.append('| %s | %s | %s |'%(r['system'],r['repo'] or '-',r['note']))
# gemini pro
def cat(name): return [x for x in pr if x['category']==name and f(x['price_cny'])]
def dedup(rows):
    seen=set(); out=[]
    for x in rows:
        k=(x['shop'],x['item'],x['price_cny'])
        if k in seen: continue
        seen.add(k); out.append(x)
    return out
gp=sorted(dedup([x for x in cat('Gemini') if 'pro' in (x['item'] or '').lower() and '教程' not in (x['item'] or '') and '人机验证号' not in (x['item'] or '')]),key=lambda x:f(x['price_cny']))
L+=['','## 发卡 · Gemini Pro 低价 Top 15','','| 商品 | 价格(¥) | 店铺 | 归属 | 来源 |','|---|---|---|---|---|']
for x in gp[:15]:
    own=x['platform'] or ('自建/'+(x['system'] or '未知'))
    L.append('| %s | ¥%s | %s | %s | %s |'%(esc((x['item'] or '')[:46]),esc(x['price_cny']),esc(x['shop']),esc(own),esc(x['source'])))
gu=sorted(dedup([x for x in cat('Gemini Ultra') if '20x' in (x['item'] or '').lower() and '教程' not in (x['item'] or '')]),key=lambda x:f(x['price_cny']))
L+=['','## 发卡 · Google AI Ultra 20x Top 15','','| 商品 | 价格(¥) | 店铺 | 归属 | 来源 |','|---|---|---|---|---|']
for x in gu[:15]:
    own=x['platform'] or ('自建/'+(x['system'] or '未知'))
    L.append('| %s | ¥%s | %s | %s | %s |'%(esc((x['item'] or '')[:46]),esc(x['price_cny']),esc(x['shop']),esc(own),esc(x['source'])))
# top shops
L+=['','## 发卡 · 店铺速览（按商品数 Top 20）','','| 店铺 | 归属 | 品类 | 价位(¥) | 来源 |','|---|---|---|---|---|']
cnt=defaultdict(int)
for x in pr: cnt[x['shop']]+=1
top=sorted(sh,key=lambda r:-cnt.get(r['shop'],0))[:20]
for r in top:
    own=r['platform'] or ('自建/'+(r['system'] or '未知'))
    L.append('| %s | %s | %s | %s | %s |'%(esc(r['shop']),esc(own),esc(r['categories']),esc(r['price_range']),esc(r['source'])))
L+=['','## 目录','','```','data/relays/relays.csv          中转站主表','data/relays/relay-models.csv    站×模型×价格（12774 条）',
'data/relays/relay-systems.csv   中转站软件名录','data/relays/by-model/*.md       143 个模型榜单',
'data/shops/platforms.csv        发卡平台','data/shops/systems.csv          发卡系统','data/shops/shops.csv            店铺主表',
'data/shops/products.csv         商品报价（10646 条）','data/raw/                       原始产物与溯源','docs/                           价格原理/黑话表/选购指南','tools/                          抓取、归一化、查询','```','',
'## 数据来源','','OpenPrice、水獭比价(shuita.xyz)、PriceAI、AI号探、AiFaKa、Veridrop，以及各中转站公开的 `/api/pricing`、`/api/v1/model-plaza`。原始报价版权归各来源站，见 [DATA-LICENSE.md](DATA-LICENSE.md)。','',
'## 授权','','- 代码 **MIT** · [LICENSE](LICENSE)','- 编排与整理 **CC BY-NC 4.0** · [DATA-LICENSE.md](DATA-LICENSE.md)','- 原始报价版权归各来源站','',
'## 贡献','','见 [CONTRIBUTING.md](CONTRIBUTING.md)。']
open(os.path.join(ROOT,'README.md'),'w',encoding='utf-8').write('\n'.join(L)+'\n')
print('README lines',len(L))
