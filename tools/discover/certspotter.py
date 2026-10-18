#!/usr/bin/env python3
"""certspotter 证书日志枚举子域（crt.sh 限流时的替代）。"""
import sys,json,time,urllib.request,urllib.error,concurrent.futures as cf,os,threading
UA={'User-Agent':'Mozilla/5.0 Chrome/124'}
lock=threading.Lock()
def get(root,tries=4):
    u='https://api.certspotter.com/v1/issuances?domain='+root+'&include_subdomains=true&expand=dns_names'
    for i in range(tries):
        try:
            r=urllib.request.Request(u,headers=UA)
            d=json.loads(urllib.request.urlopen(r,timeout=30).read())
            out=set()
            for x in d:
                for n in (x.get('dns_names') or []):
                    n=n.strip().lower().lstrip('*.')
                    if n and n!=root: out.add(n)
            time.sleep(1.0)
            return root,sorted(out)
        except urllib.error.HTTPError as e:
            if e.code==429: time.sleep(20+i*20); continue
            time.sleep(3); continue
        except Exception:
            time.sleep(3)
    return root,[]
def main():
    src,outp=sys.argv[1],sys.argv[2]
    roots=[x.strip() for x in open(src) if x.strip()]
    res={}
    if os.path.exists(outp):
        try: res=json.load(open(outp))
        except: pass
    todo=[r for r in roots if r not in res]
    print('todo',len(todo),flush=True)
    n=0
    with cf.ThreadPoolExecutor(3) as ex:
        for root,s in ex.map(get,todo):
            n+=1; res[root]=s
            if n%100==0:
                json.dump(res,open(outp,'w')); print('progress',n,'subs',sum(len(v) for v in res.values()),flush=True)
    json.dump(res,open(outp,'w'))
    print('done roots',len(res),'subs',sum(len(v) for v in res.values()))
if __name__=='__main__': main()
