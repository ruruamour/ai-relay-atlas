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
index=['# 按模型榜单\n','> 价格为推算实际价（USD/1M 输入），未对账；已排除 0 价与免费组。\n']
for key in targets:
    items=by.get(key)
    if not items: continue
    it=sorted(items.items(),key=lambda kv:kv[1][0])
    safe=key.replace('/','_').replace('*','star')
    path=os.path.join(OUT,safe+'.md')
    L=['# %s\n'%key,'共 %d 家。价为推算实际价 USD/1M 输入。\n'%len(it),
       '| # | 站点 | 输入 | 输出 | 倍率 | 分组 |','|---|---|---|---|---|---|']
    for i,(d,v) in enumerate(it[:60],1):
        L.append('| %d | %s | $%g | %s | %s | %s |'%(i,d,v[0],('$%g'%float(v[1])) if v[1] not in ('',None) else '-',v[3],v[2]))
    open(path,'w',encoding='utf-8').write('\n'.join(L)+'\n')
    index.append('- [%s](%s.md) — %d 家，最低 $%g（%s）'%(key,safe,len(it),it[0][1][0],it[0][0]))
    print('wrote',key,len(it))
open(os.path.join(OUT,'index.md'),'w',encoding='utf-8').write('\n'.join(index)+'\n')
