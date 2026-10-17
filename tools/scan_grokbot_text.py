import json,urllib.request,ssl,concurrent.futures as cf,os,re
ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
UA={'User-Agent':'Mozilla/5.0 Chrome/124','Accept':'text/html,*/*'}
D='/home/sui/.codex/gemini-research/mimo'
doms=open(D+'/all_doms.txt').read().split()
done={}
if os.path.exists(D+'/grokbot_text.json'):
    try: done=json.load(open(D+'/grokbot_text.json'))
    except: pass
pat=re.compile(r'grok[\s\-_]?bot',re.I)
def fetch(u,t=6,lim=1500000):
    r=urllib.request.Request(u,headers=UA); return urllib.request.urlopen(r,timeout=t,context=ctx).read(lim)
def work(d):
    if d in done: return None
    for path in ['/','/about','/notice']:
        try: b=fetch('https://'+d+path)
        except Exception: continue
        t=b.decode('utf-8','replace')
        m=pat.findall(t)
        if m: 
            i=pat.search(t).start()
            return d,re.sub(r'\s+',' ',t[max(0,i-60):i+120])
    return None
cnt=0
with cf.ThreadPoolExecutor(100) as ex:
    for r in ex.map(work,doms):
        cnt+=1
        if r: done[r[0]]=r[1]; print('HIT',r[0],'|',r[1][:120],flush=True)
        if cnt%2000==0:
            json.dump(done,open(D+'/grokbot_text.json','w'),ensure_ascii=False); print('progress',cnt,'hits',len(done),flush=True)
json.dump(done,open(D+'/grokbot_text.json','w'),ensure_ascii=False)
print('scanned',len(doms),'hits',len(done))
