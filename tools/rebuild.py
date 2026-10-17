import urllib.request,re,time,csv,json,os
UA={'User-Agent':'Mozilla/5.0 Chrome/124'}
D='/home/sui/.codex/gemini-research/mimo'
def fetch(u,t=25):
    r=urllib.request.Request(u,headers=UA); return urllib.request.urlopen(r,timeout=t).read().decode('utf-8','replace')
doms=set()
for p in range(1,140):
    for a in range(3):
        try: h=fetch('https://veridrop.org/relays?page=%d'%p); break
        except Exception: time.sleep(2); h=None
    if not h: break
    d=set(re.findall(r'data-impression-domain="([^"]+)"',h))
    if not d: print('stop',p); break
    doms|=d
for proto in ['gemini','claude','openai']:
    for p in range(1,20):
        try: h=fetch('https://veridrop.org/relays/%s?page=%d'%(proto,p))
        except Exception: break
        d=set(re.findall(r'data-impression-domain="([^"]+)"',h))
        if not d: break
        doms|=d
base='/home/sui/projects/nuoapi-ops/playbooks/gemini-upstream-prices'
for r in csv.DictReader(open(base+'/coverage.csv')):
    if r.get('domain'): doms.add(r['domain'].strip())
for f in ['mimo-family-providers.csv','mimo-v2.6-providers.csv']:
    try:
        for r in csv.DictReader(open(base+'/'+f)):
            if r.get('domain'): doms.add(r['domain'].strip())
    except Exception: pass
open(D+'/all_doms.txt','w').write('\n'.join(sorted(doms)))
print('total doms',len(doms))
