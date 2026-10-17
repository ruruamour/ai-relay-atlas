import json,urllib.request,ssl,re,os
ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
UA={'User-Agent':'Mozilla/5.0 Chrome/124','Accept':'*/*'}
D='/home/sui/.codex/gemini-research/mimo'
hits=json.load(open(D+'/prefix_hits.json'))
def get(d,p,t=12):
    r=urllib.request.Request('https://'+d+p,headers=UA); return urllib.request.urlopen(r,timeout=t,context=ctx).read()
def num(v):
    try: return float(v)
    except: return None
def ispromo(g):
    g=(g or '').lower()
    return any(k in g for k in ['福利','特价','免费','free','活动','赠','引流','白菜','折扣','优惠','订阅','零元','一折','超疯狂','国庆','限时'])
out=[]
for d in hits:
    entry={}
    for p in ['/api/pricing','/api/v1/model-plaza']:
        try: j=json.loads(get(d,p))
        except Exception: continue
        if p=='/api/pricing':
            data=j.get('data') or []; groups=j.get('group_ratio') or {}
            for m in data:
                if not isinstance(m,dict): continue
                n=str(m.get('model_name','')).lower()
                if 'mimo-v2.5-pro' not in n and 'mimo-v2.6-pro' not in n: continue
                key='mimo-v2.5-pro' if 'mimo-v2.5-pro' in n else 'mimo-v2.6-pro'
                ratio=num(m.get('model_ratio')); cr=num(m.get('completion_ratio'))
                eg=m.get('enable_groups') or []
                cand=[(g,groups[g]) for g in eg if g in groups]
                pref=[x for x in cand if any(k in x[0].lower() for k in ('mimo','xiaomi','小米','国模','国产','openweight'))]
                g,gr=(pref[0] if pref else (min(cand,key=lambda x:x[1]) if cand else (None,None)))
                inp=round(ratio*gr*2,6) if (ratio is not None and gr is not None) else None
                prev=entry.get(key)
                if inp is not None and (not prev or prev['eff'] is None or inp<prev['eff']):
                    entry[key]=dict(eff=inp,gr=gr,grp=g,raw=m.get('model_name'))
        else:
            data=j.get('data') or {}; gs=data.get('groups') or []
            for g in gs:
                if not isinstance(g,dict): continue
                rm=num(g.get('rate_multiplier')) or 1.0
                for m in (g.get('models') or []):
                    if not isinstance(m,dict): continue
                    n=str(m.get('name','')).lower()
                    if 'mimo-v2.5-pro' not in n and 'mimo-v2.6-pro' not in n: continue
                    key='mimo-v2.5-pro' if 'mimo-v2.5-pro' in n else 'mimo-v2.6-pro'
                    pr=m.get('pricing') or {}; i=num(pr.get('input_price'))
                    if i is None: continue
                    eff=round(i*rm*1e6,6)
                    prev=entry.get(key)
                    if not prev or prev['eff'] is None or eff<prev['eff']:
                        entry[key]=dict(eff=eff,gr=rm,grp=g.get('name'),raw=m.get('name'))
    if 'mimo-v2.5-pro' in entry and 'mimo-v2.6-pro' in entry:
        out.append(dict(domain=d,p25=entry['mimo-v2.5-pro'],p26=entry['mimo-v2.6-pro']))
json.dump(out,open(D+'/prefix_both.json','w'),ensure_ascii=False,indent=1)
print('prefix hits with BOTH:',len(out))
for r in sorted(out,key=lambda r:r['p26']['eff'] or 9e9):
    print('  %-32s 2.5pro $%-10g 2.6pro $%-10g | %s'%(r['domain'],r['p25']['eff'] or 0,r['p26']['eff'] or 0,r['p26']['grp']))
