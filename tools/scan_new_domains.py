#!/usr/bin/env python3
"""扫描域名清单，识别 New-API/Sub2API 并抓模型与价格。用法: scan_new_domains.py <file> <out.json>"""
import sys,json,ssl,urllib.request,concurrent.futures as cf,os
ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
UA={'User-Agent':'Mozilla/5.0 Chrome/124','Accept':'*/*'}
def num(v):
    try: return float(v)
    except: return None
def fetch(u,t=6,lim=4000000):
    r=urllib.request.Request(u,headers=UA); return urllib.request.urlopen(r,timeout=t,context=ctx).read(lim)
def work(d):
    out={}
    for path in ['/api/pricing','/api/v1/model-plaza']:
        try: b=fetch('https://'+d+path)
        except Exception: continue
        try: j=json.loads(b)
        except Exception: continue
        if path=='/api/pricing':
            data=j.get('data')
            if not isinstance(data,list): continue
            groups=j.get('group_ratio') or {}
            models=[]
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
                models.append(dict(model=n,input=inp,output=outp,group=g,gr=gr,ratio=ratio))
            if models: out['pricing']=models
        else:
            data=j.get('data') or {}
            if not isinstance(data,dict): continue
            gs=data.get('groups') or []
            models=[]
            for g in gs:
                if not isinstance(g,dict): continue
                rm=num(g.get('rate_multiplier')) or 1.0
                for m in (g.get('models') or []):
                    if not isinstance(m,dict): continue
                    n=m.get('name'); pr=m.get('pricing') or {}
                    i=num(pr.get('input_price')); o=num(pr.get('output_price'))
                    if not n or i is None: continue
                    models.append(dict(model=n,input=round(i*rm*1e6,6),output=round(o*rm*1e6,6) if o is not None else None,group=g.get('name'),gr=rm,ratio=None))
            if models: out['plaza']=models
    return (d,out) if out else (d,None)
def main():
    src,outp=sys.argv[1],sys.argv[2]
    doms=[x.strip() for x in open(src) if x.strip()]
    res={}
    if os.path.exists(outp):
        try: res=json.load(open(outp))
        except: pass
    cnt=0
    with cf.ThreadPoolExecutor(80) as ex:
        for d,r in ex.map(work,doms):
            cnt+=1
            if r: res[d]=r
            if cnt%500==0:
                json.dump(res,open(outp,'w'),ensure_ascii=False); print('progress',cnt,'hits',len(res),flush=True)
    json.dump(res,open(outp,'w'),ensure_ascii=False)
    print('scanned',len(doms),'hits',len(res))
if __name__=='__main__': main()
