#!/usr/bin/env python3
"""用 crt.sh 证书透明日志枚举已知根域的子域，输出候选清单。"""
import sys,json,csv,re,time,urllib.request,concurrent.futures as cf,os
UA={'User-Agent':'Mozilla/5.0 Chrome/124'}
def get(root,tries=3):
    u='https://crt.sh/?q=%25.'+root+'&output=json'
    for i in range(tries):
        try:
            r=urllib.request.Request(u,headers=UA)
            b=urllib.request.urlopen(r,timeout=45).read()
            d=json.loads(b)
            out=set()
            for x in d:
                for n in (x.get('name_value') or '').split('\n'):
                    n=n.strip().lower().lstrip('*.')
                    if n and n!=root: out.add(n)
            return root,out
        except Exception:
            time.sleep(2+i*3)
    return root,set()
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
    with cf.ThreadPoolExecutor(8) as ex:
        for root,s in ex.map(get,todo):
            n+=1; res[root]=sorted(s)
            if n%100==0:
                json.dump(res,open(outp,'w')); print('progress',n,'subs',sum(len(v) for v in res.values()),flush=True)
    json.dump(res,open(outp,'w'))
    print('done roots',len(res),'subs',sum(len(v) for v in res.values()))
if __name__=='__main__': main()
