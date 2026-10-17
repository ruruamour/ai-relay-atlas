#!/usr/bin/env python3
"""子域候选扫描：只探 /api/pricing，命中再抓 /api/v1/model-plaza。"""
import sys,json,ssl,urllib.request,concurrent.futures as cf,os
ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
UA={'User-Agent':'Mozilla/5.0 Chrome/124'}
def num(v):
    try: return float(v)
    except: return None
def fetch(u,t=5,lim=4000000):
    r=urllib.request.Request(u,headers=UA); return urllib.request.urlopen(r,timeout=t,context=ctx).read(lim)
def parse_pricing(j):
    data=j.get('data')
    if not isinstance(data,list): return None
    groups=j.get('group_ratio') or {}
    out=[]
    for m in data:
        if not isinstance(m,dict): continue
        n=m.get('model_name')
        if not n: continue
        ratio=num(m.get('model_ratio')); cr=num(m.get('completion_ratio'))
        eg=m.get('enable_groups') or []
        cand=[(g,groups[g]) for g in eg if g in groups]
        pref=[x for x in cand if any(k in x[0].lower() for k in ('gemini','mimo','xiaomi','小米','国模','国产','grok'))]
        g,gr=(pref[0] if pref else (min(cand,key=lambda x:x[1]) if cand else (None,None)))
        inp=round(ratio*gr*2,6) if (ratio is not None and gr is not None) else None
        outp=round(inp*cr,6) if (inp is not None and cr is not None) else None
        out.append(dict(model=n,input=inp,output=outp,group=g,gr=gr,ratio=ratio))
    return out or None
def work(d):
    try: j=json.loads(fetch('https://'+d+'/api/pricing'))
    except Exception: return d,None
    ms=parse_pricing(j)
    if not ms: return d,None
    res={'pricing':ms}
    try:
        j2=json.loads(fetch('https://'+d+'/api/v1/model-plaza'))
        data=j2.get('data') or {}
        gs=data.get('groups') if isinstance(data,dict) else None
        if gs:
            pl=[]
            for g in gs:
                if not isinstance(g,dict): continue
                rm=num(g.get('rate_multiplier')) or 1.0
                for m in (g.get('models') or []):
                    if not isinstance(m,dict): continue
                    n=m.get('name'); pr=m.get('pricing') or {}
                    i=num(pr.get('input_price')); o=num(pr.get('output_price'))
                    if not n or i is None: continue
                    pl.append(dict(model=n,input=round(i*rm*1e6,6),output=round(o*rm*1e6,6) if o is not None else None,group=g.get('name'),gr=rm,ratio=None))
            if pl: res['plaza']=pl
    except Exception: pass
    return d,res
def main():
    src,outp=sys.argv[1],sys.argv[2]
    doms=[x.strip() for x in open(src) if x.strip()]
    res={}
    if os.path.exists(outp):
        try: res=json.load(open(outp))
        except: pass
    done=set(res)
    todo=[d for d in doms if d not in done]
    print('todo',len(todo),flush=True)
    cnt=0
    with cf.ThreadPoolExecutor(100) as ex:
        for d,r in ex.map(work,todo):
            cnt+=1
            if r: res[d]=r
            if cnt%1000==0:
                json.dump(res,open(outp,'w'),ensure_ascii=False); print('progress',cnt,'hits',len(res),flush=True)
    json.dump(res,open(outp,'w'),ensure_ascii=False)
    print('done hits',len(res))
if __name__=='__main__': main()
