#!/usr/bin/env python3
import csv,os,re
from collections import defaultdict
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT=os.path.join(ROOT,'data','relays','by-model'); os.makedirs(OUT,exist_ok=True)
rows=list(csv.DictReader(open(os.path.join(ROOT,'data','relays','relay-models.csv'),encoding='utf-8')))
def norm(m):
    s=m.lower()
    s=re.sub(r'^[\[\(][^\]\)]*[\]\)]','',s); s=re.sub(r'^[a-z0-9_\-]+/','',s)
    s=re.sub(r'[-_]?(free|thinking|opencode.*|cline.*|high|low|medium)$','',s)
    return s.strip('-')
by=defaultdict(dict)
for r in rows:
    key=norm(r['model']); d=r['domain']
    try: p=float(r['input_usd_m'])
    except: continue
    if p<=0: continue
    prev=by[key].get(d)
    if prev is None or p<prev[0]: by[key][d]=(p,r['output_usd_m'],r['group'],r['group_ratio'],r['model'],r['promo'])
targets=sorted([k for k,v in by.items() if len(v)>=8], key=lambda k:-len(by[k]))
def fam(k):
    if k.startswith('gemini'): return 'Gemini 系列'
    if k.startswith('grok'): return 'Grok'
    if k.startswith('mimo'): return 'MiMo'
    if k.startswith('claude'): return 'Claude'
    if k.startswith('gpt'): return 'OpenAI / GPT'
    return '其他'
entries=[]
for key in targets:
    it=sorted(by[key].items(),key=lambda kv:kv[1][0])
    entries.append((key,len(it),it[0][1][0],it[0][0]))
from collections import defaultdict as dd
g=dd(list)
for e in entries: g[fam(e[0])].append(e)
L=['# 按模型榜单','','> 价格为推算实际价（USD/1M 输入），未对账；已排除 0 价与免费组。共 %d 个模型。'%len(entries),'']
for fname in ['Gemini 系列','Grok','MiMo','Claude','OpenAI / GPT','其他']:
    if not g.get(fname): continue
    L.append('## %s'%fname); L.append('')
    L.append('| 模型 | 家数 | 最低价 | 最低站 |'); L.append('|---|---|---|---|')
    for key,n,p,d in sorted(g[fname],key=lambda x:-x[1]):
        L.append('| [%s](%s.md) | %d | $%g | `%s` |'%(key,key.replace('/','_').replace('*','star'),n,p,d))
    L.append('')
open(os.path.join(OUT,'index.md'),'w',encoding='utf-8').write('\n'.join(L)+'\n')
