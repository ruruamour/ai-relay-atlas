import json,urllib.request,ssl,concurrent.futures as cf,os,re
ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
UA={'User-Agent':'Mozilla/5.0 Chrome/124','Accept':'*/*'}
D='/home/sui/.codex/gemini-research/mimo'
doms=open(D+'/all_doms.txt').read().split()
done={}
if os.path.exists(D+'/grok_hits.json'):
    try: done=json.load(open(D+'/grok_hits.json'))
    except: pass
def fetch(u,t=6,lim=3500000):
    r=urllib.request.Request(u,headers=UA); return urllib.request.urlopen(r,timeout=t,context=ctx).read(lim)
def work(d):
    if d in done: return None
    for path in ['/api/pricing','/api/v1/model-plaza']:
        try: b=fetch('https://'+d+path)
        except Exception: continue
        low=b.decode('utf-8','replace')
        names=set(re.findall(r'"([^"]*grok[^"]*4[._\-]?5[^"]*)"',low,re.I))
        if names: return d,{'path':path,'names':sorted(names)[:12]}
    return None
cnt=0
with cf.ThreadPoolExecutor(80) as ex:
    for r in ex.map(work,doms):
        cnt+=1
        if r: done[r[0]]=r[1]; print('HIT',r[0],'|',','.join(r[1]['names'][:5]),flush=True)
        if cnt%1500==0:
            json.dump(done,open(D+'/grok_hits.json','w'),ensure_ascii=False); print('progress',cnt,'hits',len(done),flush=True)
json.dump(done,open(D+'/grok_hits.json','w'),ensure_ascii=False)
print('scanned',len(doms),'hits',len(done))
