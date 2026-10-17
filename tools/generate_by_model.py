#!/usr/bin/env python3
"""生成 data/relays/by-model/*.md 与 index.md（按模型榜单）。"""
import csv,os,re,glob
from collections import defaultdict
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT=os.path.join(ROOT,'data','relays','by-model'); os.makedirs(OUT,exist_ok=True)
MIN=8
TOP=200
rows=list(csv.DictReader(open(os.path.join(ROOT,'data','relays','relay-models.csv'),encoding='utf-8')))
def norm(m):
    s=(m or '').lower()
    s=re.sub(r'^[\[\(][^\]\)]*[\]\)]','',s); s=re.sub(r'^[a-z0-9_\-]+/','',s)
    s=re.sub(r'[-_]?(free|thinking|opencode.*|cline.*|high|low|medium)$','',s)
    return s.strip('-')
def fname(k): return k.replace('/','_').replace('*','star')
def fam(k):
    if k.startswith('gemini'): return 'Gemini 系列'
    if k.startswith('grok'): return 'Grok'
    if k.startswith('mimo'): return 'MiMo'
    if k.startswith('claude'): return 'Claude'
    if k.startswith('gpt') or re.match(r'o[134]',k): return 'OpenAI / GPT'
    return '其他'
by=defaultdict(dict)
for r in rows:
    key=norm(r['model']); d=r['domain']
    try: p=float(r['input_usd_m'])
    except: continue
    if p<=0: continue
    prev=by[key].get(d)
    if prev is None or p<prev[0]: by[key][d]=(p,r['output_usd_m'],r['group'],r['group_ratio'],r['model'],r['promo'])
targets=sorted([k for k,v in by.items() if len(v)>=MIN], key=lambda k:-len(by[k]))
# clean stale
for old in glob.glob(os.path.join(OUT,'*.md')):
    os.remove(old)
entries=[]
for key in targets:
    it=sorted(by[key].items(),key=lambda kv:kv[1][0])
    L=['# %s'%key,'','> %d 家 · 最低 **$%g** @ `%s` · 推算价（USD/1M 输入），未对账%s'%(len(it),it[0][1][0],it[0][0],('（仅列前 %d）'%TOP if len(it)>TOP else '')),'',
       '| # | 站点 | 输入 | 输出 | 分组 | 倍率 | 原始模型名 |','|---|---|---|---|---|---|---|']
    for i,(d,v) in enumerate(it[:TOP],1):
        p,out,grp,gr,raw,promo=v
        L.append('| %d | `%s` | $%g | %s | %s | %s | %s |'%(i,d,p,('$'+str(out)) if out not in ('',None) else '-',(grp or '-').replace('|','\\|'),gr or '-',raw))
    L+=['','[← 返回索引](index.md)']
    open(os.path.join(OUT,fname(key)+'.md'),'w',encoding='utf-8').write('\n'.join(L)+'\n')
    entries.append((key,len(it),it[0][1][0],it[0][0]))
g=defaultdict(list)
for e in entries: g[fam(e[0])].append(e)
L=['# 按模型榜单','','> 推算价（USD/1M 输入），未对账；已排除 0 价。仅列 ≥%d 家的模型，共 %d 个。'%(MIN,len(entries)),'']
for f in ['Gemini 系列','Grok','MiMo','Claude','OpenAI / GPT','其他']:
    if not g.get(f): continue
    L+=['## %s'%f,'','| 模型 | 家数 | 最低价 | 最低站 |','|---|---|---|---|']
    for key,n,p,d in sorted(g[f],key=lambda x:-x[1]):
        L.append('| [%s](%s.md) | %d | $%g | `%s` |'%(key,fname(key),n,p,d))
    L.append('')
open(os.path.join(OUT,'index.md'),'w',encoding='utf-8').write('\n'.join(L)+'\n')
print('models written',len(entries))
