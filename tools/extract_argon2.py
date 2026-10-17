import json,urllib.request,ssl,re,concurrent.futures as cf
ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
UA={'User-Agent':'Mozilla/5.0 Chrome/124','Accept':'*/*'}
D='/home/sui/.codex/gemini-research/mimo'
hits=json.load(open(D+'/argon_hits2.json'))
def get(d,p,t=12):
    r=urllib.request.Request('https://'+d+p,headers=UA); return urllib.request.urlopen(r,timeout=t,context=ctx).read()
def num(v):
    try: return float(v)
    except: return None
def ispromo(g):
    g=(g or '').lower()
    return any(k in g for k in ['福利','特价','免费','free','活动','赠','引流','白菜','折扣','优惠','订阅','零元','一折','超疯狂','国庆','限时'])
def work(d):
    entry={}
    for p in ['/api/pricing','/api/v1/model-plaza']:
        try: j=json.loads(get(d,p))
        except Exception: continue
        if p=='/api/pricing':
            data=j.get('data') or []; groups=j.get('group_ratio') or {}
            for m in data:
                if not isinstance(m,dict): continue
                n=str(m.get('model_name',''))
                if 'argon' not in n.lower(): continue
                ratio=num(m.get('model_ratio')); cr=num(m.get('completion_ratio')); mp=num(m.get('model_price'))
                eg=m.get('enable_groups') or []
                cand=[(g,groups[g]) for g in eg if g in groups]
                pref=[x for x in cand if any(k in x[0].lower() for k in ('gemini','google','gemini','官','vertex'))]
                g,gr=(pref[0] if pref else (min(cand,key=lambda x:x[1]) if cand else (None,None)))
                inp=round(ratio*gr*2,6) if (ratio is not None and gr is not None) else None
                out=round(inp*cr,6) if (inp is not None and cr is not None) else None
                prev=entry.get(n)
                if inp is not None and (not prev or prev['eff'] is None or inp<prev['eff']):
                    entry[n]=dict(eff=inp,out=out,gr=gr,grp=g,ratio=ratio,raw=n,src=p,price=mp)
        else:
            data=j.get('data') or {}
            if not isinstance(data,dict): data={}
            gs=data.get('groups') or []
            if not isinstance(gs,list): gs=[]
            for g in gs:
                if not isinstance(g,dict): continue
                rm=num(g.get('rate_multiplier')) or 1.0
                for m in (g.get('models') or []):
                    if not isinstance(m,dict): continue
                    n=str(m.get('name',''))
                    if 'argon' not in n.lower(): continue
                    pr=m.get('pricing') or {}; i=num(pr.get('input_price')); o=num(pr.get('output_price'))
                    if i is None: continue
                    eff=round(i*rm*1e6,6); out=round(o*rm*1e6,6) if o is not None else None
                    prev=entry.get(n)
                    if not prev or prev['eff'] is None or eff<prev['eff']:
                        entry[n]=dict(eff=eff,out=out,gr=rm,grp=g.get('name'),ratio=None,raw=n,src='plaza',price=None)
    if entry: return d,entry
    return None
res=[]
with cf.ThreadPoolExecutor(60) as ex:
    for r in ex.map(work,list(hits)):
        if r: res.append(r)
json.dump(res,open(D+'/argon_prices2.json','w'),ensure_ascii=False)
print('priced domains',len(res))
