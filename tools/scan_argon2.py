import json,urllib.request,ssl,concurrent.futures as cf,os,re
ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
UA={'User-Agent':'Mozilla/5.0 Chrome/124','Accept':'*/*'}
D='/home/sui/.codex/gemini-research/mimo'
doms=open(D+'/scan_all2.txt').read().split()
out={}
def fetch(u,t=5,lim=3500000):
    r=urllib.request.Request(u,headers=UA); return urllib.request.urlopen(r,timeout=t,context=ctx).read(lim)
def work(d):
    for path in ['/api/pricing','/api/v1/model-plaza']:
        try: b=fetch('https://'+d+path)
        except Exception: continue
        low=b.decode('utf-8','replace')
        names=set(re.findall(r'"([^"]*argon[^"]*)"',low,re.I))
        names={n for n in names if 'argon' in n.lower() and len(n)<80}
        if names: return d,{'path':path,'names':sorted(names)[:20]}
    return None
cnt=0
with cf.ThreadPoolExecutor(120) as ex:
    for r in ex.map(work,doms):
        cnt+=1
        if r: out[r[0]]=r[1]
        if cnt%5000==0:
            json.dump(out,open(D+'/argon_hits2.json','w'),ensure_ascii=False); print('progress',cnt,'hits',len(out),flush=True)
json.dump(out,open(D+'/argon_hits2.json','w'),ensure_ascii=False)
print('scanned',len(doms),'hits',len(out))
