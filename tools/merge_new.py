#!/usr/bin/env python3
import csv,json,os,sys,re
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src=sys.argv[1]
data=json.load(open(src))
def norm(m):
    s=(m or '').lower(); s=re.sub(r'^[\[\(][^\]\)]*[\]\)]','',s); s=re.sub(r'^[a-z0-9_\-]+/','',s)
    s=re.sub(r'[-_]?(free|thinking|opencode.*|cline.*|high|low|medium)$','',s); return s.strip('-')
def fam(m):
    m=m.lower()
    if 'gemini' in m: return 'gemini'
    if 'mimo' in m: return 'mimo'
    if 'grok' in m: return 'grok'
    if 'claude' in m: return 'claude'
    if 'gpt' in m or re.match(r'o[134]',m): return 'gpt'
    return 'other'
# existing
rp=os.path.join(ROOT,'data','relays','relays.csv')
mp=os.path.join(ROOT,'data','relays','relay-models.csv')
rrows=list(csv.DictReader(open(rp,encoding='utf-8')))
mrows=list(csv.DictReader(open(mp,encoding='utf-8')))
rdom=set(r['domain'] for r in rrows)
mkey=set((r['domain'],r['model']) for r in mrows)
added_d=0; added_m=0
for d,blob in data.items():
    ms=[]
    for k in ('pricing','plaza'):
        ms+=blob.get(k,[])
    if not ms: continue
    fams=set(); n=0
    for x in ms:
        model=x.get('model'); inp=x.get('input')
        if not model or inp is None or inp<=0: continue
        n+=1; fams.add(fam(norm(model)))
        if (d,model) in mkey: continue
        mkey.add((d,model)); added_m+=1
        mrows.append(dict(domain=d,model=model,input_usd_m=inp,output_usd_m=x.get('output') if x.get('output') is not None else '',
            group=x.get('group') or '',group_ratio=x.get('gr') if x.get('gr') is not None else '',model_ratio=x.get('ratio') if x.get('ratio') is not None else '',
            protocol='openai',source='scan:'+k,promo='',last_checked='2026-10-17'))
    if d in rdom: 
        # update n_models
        for r in rrows:
            if r['domain']==d: r['n_models']=str(max(int(r['n_models'] or 0),n))
        continue
    rdom.add(d); added_d+=1
    rrows.append(dict(domain=d,name='',system_name='',veridrop_score='',category='new',source='scan',status='200',n_models=n,
        has_gemini='Y' if 'gemini' in fams else '',has_mimo='Y' if 'mimo' in fams else '',has_grok='Y' if 'grok' in fams else '',
        has_argon='Y' if any('argon' in (x.get('model') or '').lower() for x in ms) else '',last_checked='2026-10-17',notes='',http_status='200',latency_ms=''))
cols=list(rrows[0].keys())
with open(rp,'w',newline='',encoding='utf-8') as fh:
    w=csv.DictWriter(fh,fieldnames=cols,extrasaction='ignore'); w.writeheader()
    for r in rrows: w.writerow(r)
mcols=['domain','model','input_usd_m','output_usd_m','group','group_ratio','model_ratio','protocol','source','promo','last_checked']
with open(mp,'w',newline='',encoding='utf-8') as fh:
    w=csv.DictWriter(fh,fieldnames=mcols,extrasaction='ignore'); w.writeheader()
    for r in mrows: w.writerow(r)
print('new domains',added_d,'new model rows',added_m,'total domains',len(rrows),'total model rows',len(mrows))
