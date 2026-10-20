#!/usr/bin/env python3
"""中转站监控：定时检查站点存活、延迟、某模型是否在售（分组/价格），历史落盘。
只访问公开接口（/api/status、/api/pricing），不调用任何推理接口。

用法:
  python3 tools/monitor.py add api.openlux.ai ccoo.ai ...     加入监控名单
  python3 tools/monitor.py run [--workers 32] [--model argon]  跑一轮，追加历史
  python3 tools/monitor.py report [--model argon]              生成 Markdown 报告
  python3 tools/monitor.py drift [--days 7]                     价格变动/掉线汇总
  python3 tools/monitor.py run --probe                          额外做真实可用性测试（需 data/monitor/keys.txt）

data/monitor/keys.txt 每行 `域名,sk-xxx`，用于真实可用性测试：会发一次 max_tokens=1 的最小请求，
按该站价格计费（通常远小于 ¥0.001）。该文件已在 .gitignore 中，不会入库。
"""
import argparse
import concurrent.futures as cf
import csv
import datetime
import json
import os
import re
import ssl
import sys
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa

MON = path('data', 'monitor')
TARGETS = os.path.join(MON, 'targets.txt')
HISTORY = os.path.join(MON, 'history.csv')
COLS = ['ts', 'domain', 'http_status', 'latency_ms', 'system', 'status_name', 'topup_cny_per_usd',
        'has_model', 'groups', 'min_usd_m', 'min_call_usd', 'n_models', 'probe', 'note']
KEYS = os.path.join(MON, 'keys.txt')
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) Chrome/124 ai-relay-atlas monitor'}


def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def get(url, timeout=10):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout, context=CTX) as r:
        return r.status, r.read(4_000_000)


def load_keys():
    out = {}
    if os.path.exists(KEYS):
        for line in open(KEYS, encoding='utf-8'):
            line = line.split('#')[0].strip()
            if ',' in line:
                d, k = line.split(',', 1)
                out[d.strip()] = k.strip()
    return out


def probe_real(host, key, pattern, timeout=45):
    """真实可用性：发一次最小请求。返回 (结果, 说明)。"""
    import json as _json
    try:
        st, body = get('https://%s/v1/models' % host)
        ids = [m.get('id') for m in (_json.loads(body).get('data') or [])]
        target = next((i for i in ids if re.search(pattern, str(i), re.I)), None)
    except Exception as e:
        return 'models-fail', type(e).__name__
    if not target:
        return 'not-listed', ''
    payload = _json.dumps({'model': target, 'messages': [{'role': 'user', 'content': 'ping'}],
                           'max_tokens': 1, 'stream': False}).encode()
    req = urllib.request.Request('https://%s/v1/chat/completions' % host, data=payload, method='POST',
                                 headers={**UA, 'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
            j = _json.loads(r.read())
        ok = bool(j.get('choices'))
        return ('ok' if ok else 'empty'), str(j.get('error') or '')[:60]
    except urllib.error.HTTPError as e:
        return 'http-%d' % e.code, e.read(160).decode('utf-8', 'replace')[:80]
    except Exception as e:
        return 'fail', type(e).__name__


def check(host, pattern, key=None):
    """pattern: 用于匹配模型名的正则（默认 argon）。key: 给了就做真实可用性测试。"""
    row = dict(ts=datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), domain=host, http_status='',
               latency_ms='', system='', status_name='', topup_cny_per_usd='', has_model='',
               groups='', min_usd_m='', min_call_usd='', n_models='', probe='', note='')
    t0 = __import__('time').time()
    try:
        st, body = get('https://%s/api/status' % host)
        row['http_status'], row['latency_ms'] = st, int((__import__('time').time() - t0) * 1000)
        d = (json.loads(body).get('data') or {})
        row['status_name'] = str(d.get('system_name') or '')[:40]
        from scan import topup_cny  # 复用币种换算
        v = valid_topup(topup_cny(d))
        row['topup_cny_per_usd'] = fmt(v) if v else ''
        row['system'] = 'New-API'
    except urllib.error.HTTPError as e:
        row['http_status'], row['latency_ms'] = e.code, int((__import__('time').time() - t0) * 1000)
        row['note'] = 'status-%d' % e.code
    except Exception as e:
        row['note'] = 'down:' + type(e).__name__
        return row
    try:
        st, body = get('https://%s/api/pricing' % host)
        j = json.loads(body)
        data = j.get('data') or []
        gr = {k: num(v) for k, v in (j.get('group_ratio') or {}).items()}
        hit = [m for m in data if isinstance(m, dict) and re.search(pattern, str(m.get('model_name') or ''), re.I)]
        row['n_models'] = len(data)
        row['has_model'] = 'Y' if hit else 'N'
        if hit:
            gs, usd, call = set(), [], []
            for m in hit:
                for g in (m.get('enable_groups') or []):
                    gs.add(g)
                r = num(m.get('model_ratio'))
                cand = [gr[g] for g in (m.get('enable_groups') or []) if g in gr and gr[g] > 0]
                ratio = min(cand) if cand else None
                if m.get('quota_type') == 1:
                    mp = num(m.get('model_price'))
                    if mp is not None and ratio is not None:
                        call.append(mp * ratio)
                elif r is not None and ratio is not None:
                    usd.append(r * ratio * 2)
            row['groups'] = '|'.join(sorted(gs))[:200]
            row['min_usd_m'] = fmt(min(usd)) if usd else ''
            row['min_call_usd'] = fmt(min(call)) if call else ''
    except Exception as e:
        row['note'] = (row['note'] + ';' if row['note'] else '') + 'pricing:' + type(e).__name__
    if key and row['has_model'] == 'Y':
        res, msg = probe_real(host, key, pattern)
        row['probe'] = res
        if msg:
            row['note'] = (row['note'] + ';' if row['note'] else '') + msg
    return row


def cmd_add(a):
    os.makedirs(MON, exist_ok=True)
    cur = [x.strip() for x in open(TARGETS)] if os.path.exists(TARGETS) else []
    add = [d for d in a.domains if d not in cur]
    open(TARGETS, 'w').write('\n'.join(cur + add) + '\n')
    print('监控名单 %d → %d（新增 %d）' % (len(cur), len(cur) + len(add), len(add)))


def targets(a):
    if a.domains:
        return a.domains
    if os.path.exists(TARGETS):
        return [x.strip() for x in open(TARGETS) if x.strip()]
    return []


def cmd_run(a):
    os.makedirs(MON, exist_ok=True)
    hosts = targets(a)
    pat = a.pattern
    keys = load_keys() if a.probe else {}
    if a.probe and not keys:
        print('! --probe 需要 data/monitor/keys.txt（每行 域名,sk-xxx）')
    rows = []
    with cf.ThreadPoolExecutor(a.workers) as ex:
        for r in ex.map(lambda h: check(h, pat, keys.get(h)), hosts):
            rows.append(r)
    new = not os.path.exists(HISTORY)
    with open(HISTORY, 'a', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=COLS, extrasaction='ignore')
        if new:
            w.writeheader()
        w.writerows(rows)
    ok = sum(1 for r in rows if r['http_status'] == 200)
    has = sum(1 for r in rows if r['has_model'] == 'Y')
    pr = [r for r in rows if r.get('probe')]
    print('%s 检查 %d 站：存活 %d，在售 %d%s' % (rows[0]['ts'] if rows else '-', len(rows), ok, has,
          ('，实测 %d 站成功 %d' % (len(pr), sum(1 for r in pr if r.get('probe') == 'ok'))) if pr else ''))


def load_history():
    if not os.path.exists(HISTORY):
        return []
    return read_csv(HISTORY)


def cmd_report(a):
    rows = [r for r in load_history() if r['has_model'] in ('Y', 'N')]
    if not rows:
        print('还没有历史数据，先 run')
        return
    last_ts = max(r['ts'] for r in rows)
    latest = {r['domain']: r for r in rows if r['ts'] == last_ts}
    prev_ts = sorted({r['ts'] for r in rows if r['ts'] < last_ts})
    prev = {r['domain']: r for r in rows if prev_ts and r['ts'] == prev_ts[-1]}
    tp = topup_map()
    warns = {d for d, t in ((r['domain'], r.get('tags') or '') for r in read_csv(RELAYS)) if t}
    L = ['# 监控：%s' % a.label, '',
         '> 最近一次检查 %s（共 %d 站）。只访问公开接口，未做推理调用。' % (last_ts, len(latest)), '',
         '| 站点 | 存活 | 延迟 | 在售 | 实测 | 最低标价 $/1M | 实付 ¥/1M | 充值 ¥/$ | 分组 | 变化 |',
         '|---|---|---|---|---|---|---|---|---|---|']
    for d, r in sorted(latest.items(), key=lambda kv: (kv[1]['has_model'] != 'Y', num(kv[1]['min_usd_m']) or 9e9)):
        p = num(r['min_usd_m'])
        real = ('¥%.4g' % (p * tp[d])) if (p and d in tp) else '-'
        chg = ''
        o = prev.get(d)
        if o:
            if o['has_model'] == 'Y' and r['has_model'] == 'N':
                chg = '⚠️ 下架'
            elif o['has_model'] == 'N' and r['has_model'] == 'Y':
                chg = '✅ 上架'
            elif num(o['min_usd_m']) and p:
                if abs(p - num(o['min_usd_m'])) > 1e-9:
                    chg = '%+.3g' % (p - num(o['min_usd_m']))
        L.append('| `%s` | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
            ('⚠️' if d in warns else '') + d, r['http_status'] or r['note'], (r['latency_ms'] + 'ms') if r['latency_ms'] else '-',
            '✅' if r['has_model'] == 'Y' else '❌', (r.get('probe') or '-'),
            fmt(p) or '-', real, r['topup_cny_per_usd'] or '-', (r['groups'] or '-')[:40], chg))
    out = os.path.join(MON, 'report-%s.md' % a.label)
    open(out, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print('写入', out)


def cmd_drift(a):
    rows = load_history()
    if not rows:
        return
    days = sorted({r['ts'][:10] for r in rows})[-a.days:]
    by = {}
    for r in rows:
        if r['ts'][:10] in days:
            by.setdefault(r['domain'], []).append(r)
    L = ['# 价格变动与掉线（最近 %d 天）' % len(days), '']
    for d, rs in sorted(by.items()):
        rs.sort(key=lambda r: r['ts'])
        first, last = rs[0], rs[-1]
        a0, a1 = num(first['min_usd_m']), num(last['min_usd_m'])
        flags = []
        if a0 and a1 and abs(a1 - a0) > 1e-9:
            flags.append('价格 %s → %s（%+.0f%%）' % (fmt(a0), fmt(a1), (a1 / a0 - 1) * 100))
        if first['has_model'] == 'Y' and last['has_model'] == 'N':
            flags.append('下架')
        if first['has_model'] == 'N' and last['has_model'] == 'Y':
            flags.append('上架')
        downs = sum(1 for r in rs if not r['http_status'])
        if downs:
            flags.append('%d/%d 次不可达' % (downs, len(rs)))
        if flags:
            L.append('- `%s`：%s' % (d, '；'.join(flags)))
    open(os.path.join(MON, 'drift.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print('写入', os.path.join(MON, 'drift.md'))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('mode', choices=['add', 'run', 'report', 'drift'])
    ap.add_argument('domains', nargs='*')
    ap.add_argument('--workers', type=int, default=32)
    ap.add_argument('--pattern', default=r'argon', help='模型名匹配正则')
    ap.add_argument('--label', default='argon')
    ap.add_argument('--days', type=int, default=7)
    ap.add_argument('--probe', action='store_true', help='用 keys.txt 里的密钥做一次最小真实请求')
    a = ap.parse_args()
    {'add': cmd_add, 'run': cmd_run, 'report': cmd_report, 'drift': cmd_drift}[a.mode](a)


if __name__ == '__main__':
    main()
