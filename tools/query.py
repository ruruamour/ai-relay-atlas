#!/usr/bin/env python3
"""按模型或域名查询。用法：
  python3 tools/query.py model gemini-4-argon [--n 30]
  python3 tools/query.py domain api.openlux.ai
"""
import csv,os,sys,argparse
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def load():
    p=os.path.join(ROOT,'data','relays','relay-models.csv')
    return list(csv.DictReader(open(p,encoding='utf-8')))
def f(v):
    try: return float(v)
    except: return None
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('mode',choices=['model','domain']); ap.add_argument('q'); ap.add_argument('--n',type=int,default=30)
    a=ap.parse_args(); rows=load()
    if a.mode=='model':
        hit=[r for r in rows if a.q.lower() in (r['model'] or '').lower()]
        best={}
        for r in hit:
            p=f(r['input_usd_m'])
            if p is None or p<=0: continue
            d=r['domain']
            if d not in best or p<best[d][0]: best[d]=(p,r)
        print('模型匹配 %d 条，%d 个站（按输入价升序，USD/1M，推算）\n'%(len(hit),len(best)))
        print('%-32s %-10s %-10s %-8s %s'%('domain','input','output','ratio','group'))
        for d,(p,r) in sorted(best.items(),key=lambda kv:kv[1][0])[:a.n]:
            print('%-32s $%-9g %-10s %-8s %s'%(d,p,('$%g'%f(r['output_usd_m'])) if f(r['output_usd_m']) is not None else '-',r['group_ratio'],r['group']))
    else:
        hit=[r for r in rows if a.q.lower() in (r['domain'] or '').lower()]
        hit.sort(key=lambda r:(r['model'] or ''))
        print('域名匹配 %d 条\n'%len(hit))
        print('%-34s %-10s %-10s %-8s %s'%('model','input','output','ratio','group'))
        for r in hit[:a.n]:
            print('%-34s $%-9s %-10s %-8s %s'%(r['model'],r['input_usd_m'],r['output_usd_m'],r['group_ratio'],r['group']))
if __name__=='__main__': main()
