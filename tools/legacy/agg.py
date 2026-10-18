import json,re,csv,time
D='/home/sui/.codex/gemini-research/mimo'
base='/home/sui/projects/nuoapi-ops/playbooks/gemini-upstream-prices'
res=json.load(open(D+'/argon_prices2.json'))
old=set(d for d,_ in json.load(open(D+'/argon_prices.json')))
def ispromo(g):
    g=(g or '').lower()
    return any(k in g for k in ['福利','特价','免费','free','活动','赠','引流','白菜','折扣','优惠','订阅','零元','一折','超疯狂','国庆','限时','按次'])
def root(d): return re.sub(r'^(www|api|new|sub|vip|ai|cn|hk|gw|us|2api|api2|relay|cdn)\.','',d)
rows=[]
for d,entry in res:
    for n,x in entry.items():
        if x.get('eff') is None: continue
        rows.append(dict(domain=d,model=n,effective=x['eff'],output=x.get('out'),group_ratio=x.get('gr'),group=x.get('grp'),model_ratio=x.get('ratio'),raw=x.get('raw'),src=x.get('src'),price=x.get('price'),promo='yes' if ispromo(x.get('grp')) else ''))
with open(base+'/gemini-4-argon-providers.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['domain','model','effective','output','group_ratio','group','model_ratio','raw','src','price','promo']); w.writeheader()
    for r in rows: w.writerow(r)
canon=[r for r in rows if re.search(r'argon',r['model'],re.I)]
pay=[r for r in canon if r['promo']!='yes' and r['effective']>0]
pay.sort(key=lambda r:r['effective'])
best={}
for r in pay:
    k=root(r['domain'])
    if k not in best or r['effective']<best[k]['effective']: best[k]=r
ded=sorted(best.values(),key=lambda r:r['effective'])
alldoms=set(r['domain'] for r in rows)
newdom=sorted(alldoms-old)
L=['# Gemini 4 Argon 已上线站点（%s 更新）\n'%time.strftime('%Y-%m-%d %H:%M'),
   '扫描 62383 域名，**%d 家** 出现 argon，精确 argon 常规组去重 **%d 家**。\n'%(len(alldoms),len(ded)),
   '> 多数站标注预览/上游命名/反重力渠道，非官方身份验证。\n',
   '## 本轮新增站点（相对上次）\n','```',*newdom[:150],'```\n',
   '## 常规分组最便宜 Top 60\n','| 站点 | 实际价 入/出 | 倍率 | 分组 | 原始名 |','|---|---|---|---|---|']
for r in ded[:60]:
    L.append('| %s | $%g/%s | %s | %s | %s |'%(r['domain'],r['effective'],('$%g'%r['output']) if r['output'] is not None else '-',r['group_ratio'],r['group'],r['raw']))
open(base+'/gemini-4-argon-providers.md','w').write('\n'.join(L)+'\n')
print('argon domains',len(alldoms),'| 去重常规',len(ded),'| 新增',len(newdom))
print('\n--- 新增 ---'); print('\n'.join(newdom[:80]))
print('\n--- 最便宜 ---')
for r in ded[:35]:
    print('%-30s $%-10g/%s | %s | %s'%(r['domain'],r['effective'],('$%g'%r['output']) if r['output'] is not None else '-',r['group_ratio'],r['group']))
