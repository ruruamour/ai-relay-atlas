#!/usr/bin/env python3
"""扫描站点公开接口，断点续跑。
  New-API 系：/api/status（站名、版本、充值价）+ /api/pricing（价格）
  Sub2API   ：/api/v1/settings/public（站名、版本）+ /api/v1/model-plaza（价格）
用法: python3 tools/scan.py <域名清单.txt> <输出.json> [--workers 64]
每个模型取"可用分组里最便宜的非免费分组"作为参考价；按次计费模型单独记 call_usd。
连不上的主机只试一次，不再请求其余接口。
"""
import argparse
import concurrent.futures as cf
import datetime
import json
import os
import ssl
import urllib.error
import urllib.request

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) Chrome/124 ai-relay-atlas', 'Accept': 'application/json'}


def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


class Down(Exception):
    """连接层失败（DNS/拒绝/超时/TLS），该主机其余接口不用再试。"""


def fetch_json(url, timeout=8):
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
            body = r.read(8_000_000)
    except urllib.error.HTTPError:
        return None
    except Exception as e:
        raise Down(str(e))
    try:
        return json.loads(body)
    except ValueError:
        return None


def parse_status(j):
    """New-API / One-API 的 /api/status：只取站名、版本、充值价、是否自用/演示。"""
    d = (j or {}).get('data') if isinstance(j, dict) else None
    if not isinstance(d, dict) or not any(k in d for k in ('system_name', 'quota_per_unit', 'version')):
        return None
    return dict(name=str(d.get('system_name') or '')[:80], version=str(d.get('version') or '')[:40],
                topup=num(d.get('price')), topup_cny=topup_cny(d),
                self_use=bool(d.get('self_use_mode_enabled')), demo=bool(d.get('demo_site_enabled')))


def topup_cny(d):
    """充值价换算成"元 / 1 美元额度"。经典 New-API 的 price 就是元；部分分支用美元收款
    （payment_currency_symbol='$'），要乘站点自己的 usd_exchange_rate；币种不明（CUSTOM 等）返回 None。"""
    price = num(d.get('price'))
    if not price or price <= 0 or d.get('enable_online_topup') is False:
        return None
    sym = str(d.get('payment_currency_symbol') or '').strip()
    cur = str(d.get('currency_type') or '').upper()
    if sym in ('$', 'US$', 'USD') or (cur == 'USD' and sym in ('$', '')):
        if not sym and cur == 'USD':
            return None  # 只有 currency_type=USD、没有收款符号：可能只是额度显示单位，不确定
        rate = num(d.get('usd_exchange_rate'))
        return price * rate if rate and 3 <= rate <= 10 else None
    if cur == 'CUSTOM' or (sym and sym not in ('¥', '￥', 'CNY', 'RMB')):
        return None
    return price


def parse_settings(j):
    """Sub2API 的 /api/v1/settings/public：只取站名、版本、是否开放注册/模型广场。不取任何联系方式。"""
    d = (j or {}).get('data') if isinstance(j, dict) else None
    if not isinstance(d, dict) or 'site_name' not in d:
        return None
    return dict(name=str(d.get('site_name') or '')[:80], version=str(d.get('version') or '')[:40],
                registration=bool(d.get('registration_enabled')), plaza=bool(d.get('model_plaza_enabled')))


def r6(x):
    return None if x is None else float('%.6g' % x)


def parse_newapi(j):
    if not isinstance(j, dict) or not isinstance(j.get('data'), list):
        return None
    gr = {k: num(v) for k, v in (j.get('group_ratio') or {}).items() if num(v) is not None}
    usable = set((j.get('usable_group') or {}).keys()) if isinstance(j.get('usable_group'), dict) else set()
    out = []
    for m in j['data']:
        if not isinstance(m, dict) or not m.get('model_name'):
            continue
        eg = m.get('enable_groups') or (['default'] if 'default' in gr else [])
        cand = [(g, gr[g]) for g in eg if g in gr and (not usable or g in usable)] or \
               [(g, gr[g]) for g in eg if g in gr]
        paid = [x for x in cand if x[1] > 0]
        if paid:
            g, ratio = min(paid, key=lambda x: x[1])
        elif cand:
            g, ratio = cand[0]
        else:
            g, ratio = '', None
        rec = dict(model=m['model_name'], group=g, group_ratio=ratio, model_ratio=num(m.get('model_ratio')),
                   input=None, output=None, call=None, billing='token')
        if m.get('quota_type') == 1:
            rec['billing'] = 'call'
            mp = num(m.get('model_price'))
            rec['call'] = r6(mp * ratio) if (mp is not None and ratio is not None) else None
        else:
            mr, cr = num(m.get('model_ratio')), num(m.get('completion_ratio'))
            if mr is not None and ratio is not None:
                rec['input'] = r6(mr * ratio * 2)
                rec['output'] = r6(mr * ratio * 2 * cr) if cr is not None else None
        out.append(rec)
    return out or None


def parse_sub2api(j):
    data = (j or {}).get('data') if isinstance(j, dict) else None
    if not isinstance(data, dict) or not isinstance(data.get('groups'), list):
        return None
    best = {}
    for g in data['groups']:
        if not isinstance(g, dict):
            continue
        rm = num(g.get('rate_multiplier'))
        rm = 1.0 if rm is None else rm
        excl = bool(g.get('is_exclusive'))
        for m in g.get('models') or []:
            if not isinstance(m, dict) or not m.get('name'):
                continue
            p = m.get('pricing') or {}
            rec = dict(model=m['name'], group=g.get('name') or '', group_ratio=rm, model_ratio=None,
                       input=None, output=None, call=None, billing='token')
            prq = num(p.get('per_request_price'))
            if (p.get('billing_mode') not in (None, 'token')) and prq is not None:
                rec['billing'] = 'call'
                rec['call'] = r6(prq * rm)
                key = rec['call']
            else:
                i, o = num(p.get('input_price')), num(p.get('output_price'))
                if i is None:
                    continue
                rec['input'] = r6(i * rm * 1e6)
                rec['output'] = r6(o * rm * 1e6) if o is not None else None
                key = rec['input']
            score = (excl, rm <= 0, key if key is not None else 1e18)
            if m['name'] not in best or score < best[m['name']][0]:
                best[m['name']] = (score, rec)
    return [v[1] for v in best.values()] or None


ONLY = None


def work(host):
    res = {}
    try:
        st = parse_status(fetch_json('https://%s/api/status' % host))
        if ONLY == 'status':
            if st:
                res['status'] = st
            else:
                se = parse_settings(fetch_json('https://%s/api/v1/settings/public' % host))
                if se:
                    res['settings'] = se
            raise Down('status-only')
        if st:
            res['status'] = st
            p = parse_newapi(fetch_json('https://%s/api/pricing' % host))
            if p:
                res['pricing'] = p
        else:
            se = parse_settings(fetch_json('https://%s/api/v1/settings/public' % host))
            if se:
                res['settings'] = se
            p = parse_sub2api(fetch_json('https://%s/api/v1/model-plaza' % host))
            if p:
                res['plaza'] = p
            if not se and not p:  # 没有 status 也不是 Sub2API：仍试一次 pricing（部分魔改站关了 status）
                p = parse_newapi(fetch_json('https://%s/api/pricing' % host))
                if p:
                    res['pricing'] = p
    except Down:
        pass
    if res:
        res['checked'] = datetime.date.today().isoformat()
    return host, (res or None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('src')
    ap.add_argument('out')
    ap.add_argument('--workers', type=int, default=64)
    ap.add_argument('--only', choices=['status'], help='只刷新站点信息（站名/版本/充值价），不取价格')
    a = ap.parse_args()
    global ONLY
    ONLY = a.only
    hosts = [x.strip() for x in open(a.src) if x.strip()]
    res = json.load(open(a.out)) if os.path.exists(a.out) else {}
    done_p = a.out + '.done'
    done = {x.strip() for x in open(done_p)} if os.path.exists(done_p) else set()
    todo = [h for h in hosts if h not in done]
    print('todo', len(todo), 'of', len(hosts), flush=True)
    n = 0
    with open(done_p, 'a') as dfh, cf.ThreadPoolExecutor(a.workers) as ex:
        for h, r in ex.map(work, todo):
            n += 1
            dfh.write(h + '\n')
            if r:
                res[h] = r
            if n % 500 == 0:
                dfh.flush()
                json.dump(res, open(a.out, 'w'), ensure_ascii=False)
                print('progress', n, 'hits', len(res), flush=True)
    json.dump(res, open(a.out, 'w'), ensure_ascii=False)
    print('done', n, 'hits', len(res))


if __name__ == '__main__':
    main()
