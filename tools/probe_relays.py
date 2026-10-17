#!/usr/bin/env python3
"""探活中转站：记录 HTTP 状态与延迟，写回 relays.csv。手动运行。"""
import csv,os,ssl,time,concurrent.futures as cf,urllib.request
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
UA={'User-Agent':'Mozilla/5.0 Chrome/124'}
def probe(d):
    for scheme in ['https','http']:
        t0=time.time()
        try:
            req=urllib.request.Request('%s://%s/'%(scheme,d),headers=UA)
            r=urllib.request.urlopen(req,timeout=6,context=ctx)
            return d,r.status,int((time.time()-t0)*1000)
        except urllib.error.HTTPError as e:
            return d,e.code,int((time.time()-t0)*1000)
        except Exception:
            continue
    return d,'',''
def main():
    p=os.path.join(ROOT,'data','relays','relays.csv')
    rows=list(csv.DictReader(open(p,encoding='utf-8')))
    doms=[r['domain'] for r in rows]
    res={}
    with cf.ThreadPoolExecutor(80) as ex:
        for d,s,ms in ex.map(probe,doms):
            res[d]=(s,ms)
    for r in rows:
        s,ms=res.get(r['domain'],('',''))
        r['http_status']=s; r['latency_ms']=ms; r['last_checked']='2026-10-17'
    cols=list(rows[0].keys())
    for c in ['http_status','latency_ms']:
        if c not in cols: cols.append(c)
    with open(p,'w',newline='',encoding='utf-8') as fh:
        w=csv.DictWriter(fh,fieldnames=cols,extrasaction='ignore'); w.writeheader()
        for r in rows: w.writerow(r)
    ok=sum(1 for s,_ in res.values() if s==200)
    print('probed',len(doms),'200:',ok)
if __name__=='__main__': main()
