#!/usr/bin/env python3
import csv,json,os,re
from urllib.parse import urlparse
from collections import defaultdict
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW=os.path.join(ROOT,'data','raw'); DATE='2026-10-16'
def rd(f):
    p=os.path.join(RAW,f)
    if not os.path.exists(p): return []
    with open(p,newline='',encoding='utf-8-sig') as fh: return list(csv.DictReader(fh))
SYSTEM_BY_HOST={'ultra.makelove.cloud':'独角数卡','gpthub.ciyuanapi.ai':'独角数卡','shihuiai.cn':'异次元发卡'}
def classify(host):
    if host in ('pay.ldxp.cn','ldxp.cn'): return ('SaaS','链动小铺','','')
    if host=='wzyp.cn': return ('SaaS','未知SaaS(wzyp.cn)','','')
    if host in SYSTEM_BY_HOST: return ('自建','',SYSTEM_BY_HOST[host],'开源软件')
    return ('自建','','未知','未知')
def cat(t):
    t=(t or '').lower()
    if 'ultra' in t: return 'Gemini Ultra'
    if 'gemini' in t or 'google ai' in t or 'google one' in t: return 'Gemini'
    if 'grok' in t or 'gr0k' in t: return 'Grok'
    if 'claude' in t: return 'Claude'
    if 'cursor' in t: return 'Cursor'
    if 'codex' in t or 'chatgpt' in t or 'gpt' in t: return 'ChatGPT'
    if 'kiro' in t: return 'Kiro'
    if '邮箱' in t or 'gmail' in t: return '邮箱'
    return '其它'
prod=[]
for r in rd('google-card-offers.csv'):
    h=r.get('host') or urlparse(r.get('url','')).netloc
    prod.append(dict(shop=r.get('shop'),host=h,category=cat(r.get('title')),item=r.get('title'),
        price_cny=r.get('price'),status=r.get('status',''),warranty='',stock='',source='OpenPrice',source_url=r.get('url'),last_checked=DATE))
for r in rd('google-ultra-offers.csv'):
    prod.append(dict(shop=r.get('shop'),host=r.get('host'),category='Gemini Ultra',item=r.get('title'),
        price_cny=r.get('price'),status=r.get('status',''),warranty='',stock='',source='OpenPrice',source_url=r.get('url'),last_checked=DATE))
p=os.path.join(RAW,'aihaotan-goods.json')
if os.path.exists(p):
    for x in json.load(open(p,encoding='utf-8')):
        u=x.get('shopUrl') or ''
        prod.append(dict(shop=x.get('shopName'),host=urlparse(u).netloc,category=cat(x.get('title')),item=x.get('title'),
            price_cny=x.get('price'),status='in_stock',warranty='',stock=x.get('stock'),source='AI号探',source_url=u,last_checked=DATE))
p=os.path.join(RAW,'openprice-offers.json')
if os.path.exists(p):
    for x in json.load(open(p,encoding='utf-8')):
        u=x.get('url') or ''
        prod.append(dict(shop=x.get('shopName'),host=urlparse(u).netloc,category=cat(x.get('title')),item=x.get('title'),
            price_cny=x.get('price'),status=x.get('status',''),warranty='',stock='',source='OpenPrice',source_url=u,last_checked=DATE))
# dedupe products by (shop,item,price)
seen=set(); ded=[]
for x in prod:
    k=(x['shop'],x['item'],x['price_cny'])
    if k in seen: continue
    seen.add(k); ded.append(x)
with open(os.path.join(ROOT,'data','shops','products.csv'),'w',newline='',encoding='utf-8') as fh:
    w=csv.DictWriter(fh,fieldnames=['shop','host','hosting','platform','system','category','item','price_cny','status','warranty','stock','source','source_url','last_checked'],extrasaction='ignore'); w.writeheader()
    for x in ded:
        hosting,plat,sysn,stype=classify(x['host'])
        x.update(hosting=hosting,platform=plat,system=sysn,system_type=stype); w.writerow(x)
print('products',len(ded))
# shops aggregate
agg=defaultdict(lambda:dict(cats=set(),prices=[],hosts=set(),sources=set()))
for x in ded:
    a=agg[x['shop']]; a['cats'].add(x['category']); a['hosts'].add(x['host']); a['sources'].add(x['source'])
    try: a['prices'].append(float(x['price_cny']))
    except: pass
rows=[]
for shop,a in agg.items():
    h=next((classify(x) for x in a['hosts']),('','','',''))
    hosting,plat,sysn,stype=h
    rows.append(dict(shop=shop,hosting=hosting,platform=plat,system=sysn,system_type=stype,
        domain=';'.join(sorted(a['hosts'])),categories='/'.join(sorted(a['cats'])),
        price_range=('%g-%g'%(min(a['prices']),max(a['prices']))) if a['prices'] else '',
        source='/'.join(sorted(a['sources'])),last_checked=DATE,notes=''))
rows.sort(key=lambda r:r['shop'] or '')
with open(os.path.join(ROOT,'data','shops','shops.csv'),'w',newline='',encoding='utf-8') as fh:
    w=csv.DictWriter(fh,fieldnames=['shop','hosting','platform','system','system_type','domain','categories','price_range','source','last_checked','notes']); w.writeheader()
    for r in rows: w.writerow(r)
print('shops',len(rows))
