#!/usr/bin/env python3
"""探活：访问每个主域名首页，记录 http_status / latency_ms，缺名称时用网页标题补。
用法: python3 tools/probe.py [--workers 80]
"""
import argparse
import concurrent.futures as cf
import datetime
import html
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE
UA = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) Chrome/124 ai-relay-atlas'}
TITLE = re.compile(r'<title[^>]*>([^<]{1,200})</title>', re.I)
GENERIC = {'new api', 'one api', 'sub2api', 'loading...', 'vite + react', 'react app', ''}


def probe(d):
    for scheme in ('https', 'http'):
        t0 = time.time()
        try:
            with urllib.request.urlopen(urllib.request.Request('%s://%s/' % (scheme, d), headers=UA),
                                        timeout=8, context=CTX) as r:
                body = r.read(65536).decode('utf-8', 'replace')
                m = TITLE.search(body)
                return d, r.status, int((time.time() - t0) * 1000), html.unescape(m.group(1)).strip() if m else ''
        except urllib.error.HTTPError as e:
            return d, e.code, int((time.time() - t0) * 1000), ''
        except Exception:
            continue
    return d, '', '', ''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--workers', type=int, default=80)
    a = ap.parse_args()
    rows = read_csv(RELAYS)
    today = datetime.date.today().isoformat()
    res = {}
    with cf.ThreadPoolExecutor(a.workers) as ex:
        for d, st, ms, title in ex.map(probe, [r['domain'] for r in rows]):
            res[d] = (st, ms, title)
    for r in rows:
        st, ms, title = res[r['domain']]
        r['http_status'], r['latency_ms'] = st, ms
        if title and not r.get('name') and title.lower() not in GENERIC:
            r['name'] = title[:80]
        r['last_checked'] = max(r.get('last_checked') or '', today)
    write_csv(RELAYS, RELAY_COLS, rows)
    print('probed', len(rows), '200:', sum(1 for v in res.values() if v[0] == 200))


if __name__ == '__main__':
    main()
