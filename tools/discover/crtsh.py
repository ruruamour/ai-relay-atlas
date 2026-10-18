#!/usr/bin/env python3
"""用 crt.sh 证书透明日志枚举已收录站点的子域（直连 crt.sh 公共 PostgreSQL，比网页接口稳定）。
需要 psql（postgresql-client）。对 crt.sh 是免费公共服务，默认只开 3 个并发，请勿调大。
用法:
  python3 tools/discover/crtsh.py run <out.json> [--batch 25] [--workers 3]   查询（断点续跑）
  python3 tools/discover/crtsh.py candidates <out.json> > /tmp/cands.txt       导出未收录的子域
"""
import argparse
import concurrent.futures as cf
import json
import os
import re
import subprocess
import sys
import threading
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *  # noqa

NAME_RX = re.compile(r'^[a-z0-9.-]+$')
SKIP_ROOT = {'ccwu.cc', 'qzz.io', 'dpdns.org', 'us.kg', 'eu.org', 'pp.ua', 'nyc.mn', 'duckdns.org', 'railway.app',
             'onrender.com', 'herokuapp.com', 'deno.dev', 'zeabur.app', 'hf.space', 'sealos.run', 'xyz.ws'}
MAX_NAMES = 400  # 单个根域证书名过多，多半是共享托管/CDN，结果丢弃


def roots():
    rl, al = read_csv(RELAYS), read_csv(ALIASES)
    doms = {r['domain'] for r in rl} | {r['alias'] for r in al} | {r['api_host'] for r in rl if r.get('api_host')}
    hosts = defaultdict(set)
    for d in doms:
        if d and not IP_RE.match(d):
            hosts[registered(d)].add(base_host(d))
    priced = {registered(r['domain']) for r in rl if int(r['n_models'] or 0) > 0}
    out = [rd for rd, hs in hosts.items()
           if rd not in SKIP_ROOT and len(hs) < 4 and not any(on_paas(h) for h in hs) and NAME_RX.match(rd)]
    return sorted(out, key=lambda rd: (rd not in priced, rd))


_V4 = None


def _v4():
    global _V4
    if _V4 is None:
        import socket
        try:
            _V4 = socket.getaddrinfo('crt.sh', 5432, socket.AF_INET)[0][4][0]
        except Exception:
            _V4 = ''
    return _V4


def query(batch):
    vals = ','.join("('%s')" % d for d in batch)
    sql = ("SET statement_timeout='300s'; WITH doms(d) AS (VALUES %s) "
           "SELECT DISTINCT doms.d, lower(cai.NAME_VALUE) FROM doms, certificate_and_identities cai "
           "WHERE plainto_tsquery('certwatch', doms.d) @@ identities(cai.CERTIFICATE) "
           "AND (lower(cai.NAME_VALUE) = doms.d OR lower(cai.NAME_VALUE) LIKE '%%.' || doms.d);" % vals)
    env = dict(os.environ, PGCONNECT_TIMEOUT='30')
    if _v4():
        env['PGHOSTADDR'] = _v4()  # 只走 IPv4
    p = subprocess.run(['psql', '-h', 'crt.sh', '-p', '5432', '-U', 'guest', '-d', 'certwatch', '-At', '-F', '\t',
                        '-c', sql], capture_output=True, text=True, timeout=420, env=env)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip()[:200])
    res = defaultdict(set)
    for line in p.stdout.splitlines():
        if '\t' not in line:
            continue
        root, name = line.split('\t', 1)
        name = name.strip().lstrip('*.').rstrip('.')
        if NAME_RX.match(name):
            res[root].add(name)
    return res


def cmd_run(a):
    data = json.load(open(a.out)) if os.path.exists(a.out) else {}
    todo = [r for r in roots() if r not in data]
    print('根域 %d，待查 %d' % (len(data) + len(todo), len(todo)), file=sys.stderr, flush=True)
    lock = threading.Lock()
    batches = [todo[i:i + a.batch] for i in range(0, len(todo), a.batch)]

    def work(batch):
        for attempt in range(3):
            try:
                return batch, query(batch), None
            except Exception as e:
                err = str(e)
        return batch, None, err
    done = 0
    with cf.ThreadPoolExecutor(a.workers) as ex:
        for batch, res, err in ex.map(work, batches):
            done += 1
            if res is None:
                print('批次失败（下次重跑会重试）：%s' % err, file=sys.stderr, flush=True)
                continue
            with lock:
                for r in batch:
                    names = res.get(r, set())
                    data[r] = sorted(names) if len(names) <= MAX_NAMES else ['__too_many__']
                json.dump(data, open(a.out, 'w'), indent=0)
            if done % 5 == 0:
                print('进度 %d/%d 批，子域 %d' % (done, len(batches), sum(len(v) for v in data.values())),
                      file=sys.stderr, flush=True)
    print('完成：根域 %d，子域 %d' % (len(data), sum(len(v) for v in data.values())), file=sys.stderr)


def cmd_candidates(a):
    data = json.load(open(a.out))
    rl = read_csv(RELAYS)
    known = {r['domain'] for r in rl} | {r['alias'] for r in read_csv(ALIASES)} | {r['api_host'] for r in rl if r.get('api_host')}
    out = set()
    for root, names in data.items():
        for n in names:
            if n != '__too_many__' and n not in known and (n == root or n.endswith('.' + root)):
                out.add(n)
    for n in sorted(out):
        print(n)
    print('未收录子域 %d' % len(out), file=sys.stderr)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('mode', choices=['run', 'candidates'])
    ap.add_argument('out')
    ap.add_argument('--batch', type=int, default=25)
    ap.add_argument('--workers', type=int, default=3)
    a = ap.parse_args()
    (cmd_run if a.mode == 'run' else cmd_candidates)(a)


if __name__ == '__main__':
    main()
