#!/usr/bin/env python3
"""把原始抓取产物归一化成 ai-relay-atlas 的标准表。手动运行。"""
import csv,json,os,re
from collections import defaultdict
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW=os.path.join(ROOT,'data','raw')
DATE='2026-10-16'
def rd(f):
    p=os.path.join(RAW,f)
    if not os.path.exists(p): return []
    with open(p,newline='',encoding='utf-8-sig') as fh: return list(csv.DictReader(fh))
def wr(path,cols,rows):
    with open(path,'w',newline='',encoding='utf-8') as fh:
        w=csv.DictWriter(fh,fieldnames=cols,extrasaction='ignore'); w.writeheader()
        for r in rows: w.writerow(r)
    print('wrote',path,len(rows))

# ---------- relay-models ----------
rm=[]
for r in rd('gemini-prices-long.csv'):
    rm.append(dict(domain=r['domain'],model=r['model'],input_usd_m=r.get('input_usd_m'),
        output_usd_m=r.get('output_usd_m'),group=r.get('group'),group_ratio=r.get('group_ratio'),
        model_ratio=r.get('model_ratio'),protocol=r.get('platform') or 'openai',
        source='newapi:/api/pricing',promo='',last_checked='2026-09-24'))
for r in rd('mimo-family-providers.csv'):
    rm.append(dict(domain=r['domain'],model=r['model'],input_usd_m=r.get('effective_input_usd_m'),
        output_usd_m='',group=r.get('group'),group_ratio=r.get('group_ratio'),model_ratio=r.get('model_ratio'),
        protocol='openai',source='scan:model-list',promo='',last_checked='2026-10-02'))
for r in rd('grok-4.5-providers.csv'):
    rm.append(dict(domain=r['domain'],model=r.get('raw') or 'grok-4.5',input_usd_m=r.get('effective'),
        output_usd_m=r.get('output'),group=r.get('group'),group_ratio=r.get('group_ratio'),model_ratio=r.get('model_ratio'),
        protocol='openai',source=r.get('src') or 'scan',promo=r.get('promo',''),last_checked='2026-10-08'))
for r in rd('gemini-4-argon-providers.csv'):
    rm.append(dict(domain=r['domain'],model=r.get('raw') or r['model'],input_usd_m=r.get('effective'),
        output_usd_m=r.get('output'),group=r.get('group'),group_ratio=r.get('group_ratio'),model_ratio=r.get('model_ratio'),
        protocol='openai',source=r.get('src') or 'scan',promo=r.get('promo',''),last_checked='2026-10-14'))
for r in rd('custom-rendered.csv'):
    rm.append(dict(domain=r['domain'],model=r['model'],input_usd_m=r.get('input_usd_m'),
        output_usd_m=r.get('output_usd_m'),group='',group_ratio=r.get('group_ratio'),model_ratio='',
        protocol='openai',source='browser-render',promo='',last_checked='2026-09-25'))
wr(os.path.join(ROOT,'data','relays','relay-models.csv'),
   ['domain','model','input_usd_m','output_usd_m','group','group_ratio','model_ratio','protocol','source','promo','last_checked'],rm)

# ---------- relays (domain level) ----------
cov={r['domain']:r for r in rd('coverage.csv')}
gst={r['domain']:r for r in rd('gemini-stations.csv')}
by=defaultdict(set)
for r in rm:
    m=(r['model'] or '').lower()
    if 'gemini' in m: by[r['domain']].add('gemini')
    if 'mimo' in m: by[r['domain']].add('mimo')
    if 'grok' in m: by[r['domain']].add('grok')
    if 'argon' in m: by[r['domain']].add('argon')
doms=sorted(set(list(cov)+list(gst)+[r['domain'] for r in rm]))
rr=[]
for d in doms:
    c=cov.get(d,{}); g=gst.get(d,{})
    rr.append(dict(domain=d,name=(g.get('title') or '').strip(),system_name=c.get('system_name',''),
        veridrop_score=c.get('vd_score') or g.get('vd_score',''),category=c.get('category',''),
        source=c.get('source',''),status=c.get('home_status',''),n_models=g.get('n_models',''),
        has_gemini='Y' if 'gemini' in by.get(d,()) else '',has_mimo='Y' if 'mimo' in by.get(d,()) else '',
        has_grok='Y' if 'grok' in by.get(d,()) else '',has_argon='Y' if 'argon' in by.get(d,()) else '',
        last_checked=DATE,notes=''))
wr(os.path.join(ROOT,'data','relays','relays.csv'),
   ['domain','name','system_name','veridrop_score','category','source','status','n_models','has_gemini','has_mimo','has_grok','has_argon','last_checked','notes'],rr)
print('relays:',len(rr),'relay-models:',len(rm))
