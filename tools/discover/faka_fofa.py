#!/usr/bin/env python3
"""发卡系统指纹查询串 + 结果解析。

用途：在 FOFA / ZoomEye / Shodan 里搜"自己搭发卡站"的中转/卡网站点，突破聚合站的收录上限。
本脚本**只生成查询串、解析手工导出的结果**，不内置任何平台的 API Key（需要时用环境变量）。

用法:
  python3 tools/discover/faka_fofa.py queries [--platform fofa|shodan|zoomeye]
  python3 tools/discover/faka_fofa.py parse <导出文件>           解析 FOFA/Shodan 导出的 JSON/CSV
  python3 tools/discover/faka_fofa.py api                         有 FOFA_API_KEY 时直接调 API

指纹来源：本仓库对 82 个自建站的实际探测（data/raw/shop-fingerprints.json）+ 各系统的公开特征。
"""
import argparse
import csv
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *  # noqa

OUT = os.path.join(SOURCES, 'fofa-candidates.txt')

# ---- 源码级指纹：命中即基本确定系统 ----
BODY_SIG = {
    '独角数卡': ['dujiaoka', '/assets/dujiaoka', '自动发卡系统', '独角数卡',
                 'name="csrf-token" content', 'card/order', 'dujiaoka.com'],
    '异次元发卡': ['acg-faka', 'acgfaka', '异次元发卡', '/assets/acg', 'acg-faka.com'],
    'ZFAKA': ['zfaka', '/theme/default/', 'zfaka.com'],
    '萌次元': ['萌次元', 'mcy.im'],
    'ACE云寄售': ['aceyun', 'ACE发卡网'],
    '云猫寄售': ['catfk', '云猫寄售'],
}
# ---- 卡网通用特征（系统未知也能捞） ----
COMMON = ['自动发货', '发卡', '卡密', '寄售', '虚拟商品', '自动发卡']

# 这些关键词说明是"卖 AI 账号/会员"的卡网，和后缀组合使用
AI = ['ChatGPT', 'GPT Plus', 'Claude', 'Gemini', 'Grok', '成品种', '成品号', '订阅', '代充']

QUERIES = {
    # FOFA：body 搜索是免费额度也有的基础语法
    'fofa': [
        ('独角数卡', 'body="dujiaoka"'),
        ('独角数卡·备用', 'body="/assets/dujiaoka"'),
        ('异次元发卡', 'body="acg-faka"'),
        ('异次元发卡·备用', 'body="异次元发卡"'),
        ('ZFAKA', 'body="zfaka"'),
        ('萌次元', 'body="萌次元"'),
        ('AI 卡网（独角数卡 + AI 词）', '(body="dujiaoka" || body="acg-faka") && (body="ChatGPT" || body="Claude" || body="Gemini")'),
        ('发卡通用 + AI 词', '(body="自动发货" || body="卡密") && (body="ChatGPT" || body="Claude" || body="Gemini" || body="Grok")'),
        ('寄售平台 + AI 词', '(body="寄售" || body="虚拟商品") && (body="ChatGPT" || body="Claude")'),
        ('标题就是发卡网的', 'title="发卡" || title="卡网" || title="发卡网"'),
        ('无标题单页商城', 'title="购物 -" && (body="ChatGPT" || body="Claude" || body="Gemini")'),
        ('ACE 云寄售', 'body="aceyun"'),
        ('云猫寄售', 'body="catfk"'),
    ],
    'shodan': [
        ('独角数卡', 'http.html:"dujiaoka"'),
        ('异次元发卡', 'http.html:"acg-faka"'),
        ('AI 卡网', 'http.html:"dujiaoka" http.html:"ChatGPT"'),
        ('发卡通用 + AI', 'http.html:"自动发货" http.html:"ChatGPT"'),
        ('标题发卡网', 'http.title:"发卡"'),
    ],
    'zoomeye': [
        ('独角数卡', 'app:"dujiaoka"'),
        ('异次元发卡', 'body:"acg-faka"'),
        ('AI 卡网', 'body:"dujiaoka" && body:"ChatGPT"'),
        ('发卡通用 + AI', 'body:"自动发货" && body:"ChatGPT"'),
    ],
}

# 排除：官方演示站、文档、源码仓库、聚合站自己
SKIP_RX = re.compile(r'(github|gitee|gitlab|npmjs|readthedocs|docs\.|wiki\.|demo\.|test\.|example\.|localhost|'
                     r'dujiaoka\.com|acg-faka\.com|zfaka\.com|mcy\.im|shuita\.xyz|openprice\.cc|priceai\.cc|'
                     r'aihaotan\.com|veridrop)')


def cmd_queries(a):
    print('# %s 查询串（复制到网页版即可，注意配额）\n' % a.platform.upper())
    for name, q in QUERIES[a.platform]:
        print('## %s\n```\n%s\n```\n' % (name, q))


def _host(v):
    v = str(v or '').strip()
    if not v:
        return ''
    v = re.sub(r'^[a-z]+://', '', v, flags=re.I)
    return v.split('/')[0].split(':')[0].lower()


def cmd_parse(a):
    raw = open(a.file, encoding='utf-8', errors='replace').read()
    rows = []
    if raw.lstrip().startswith(('{', '[')):
        d = json.loads(raw)
        for key in ('results', 'data', 'matches'):
            if isinstance(d, dict) and isinstance(d.get(key), list):
                d = d[key]
                break
        for x in d if isinstance(d, list) else []:
            if isinstance(x, (list, tuple)):
                rows.append(_host(x[0]))
            elif isinstance(x, dict):
                rows.append(_host(x.get('host') or x.get('ip_str') or x.get('url') or (x.get('http') or {}).get('host')))
    else:
        rd = csv.reader(raw.splitlines())
        for r in rd:
            if r:
                rows.append(_host(r[0]))
    seen, out = set(), []
    for h in rows:
        if not h or h in seen or SKIP_RX.search(h) or IP_RE.match(h):
            continue
        seen.add(h)
        out.append(h)
    known = {r['domain'] for r in read_csv(RELAYS)} | {r['alias'] for r in read_csv(ALIASES)}
    known |= {r['domain'].split(';')[0] for r in read_csv(path('data', 'shops', 'shops.csv')) if r['domain']}
    new = [h for h in out if h not in known]
    with open(OUT, 'w') as fh:
        fh.write('\n'.join(new) + '\n')
    print('结果 %d，去重后 %d，其中未收录 %d → %s' % (len(rows), len(out), len(new), OUT))
    print('下一步：python3 tools/scan.py %s /tmp/fofa.json  （只关心是否在售某模型的，可用 monitor.py）' % OUT)


def cmd_api(a):
    key = os.environ.get('FOFA_API_KEY', '')
    if not key:
        print('未设置 FOFA_API_KEY。设置后运行：\n  export FOFA_API_KEY=xxx\n'
              '  python3 tools/discover/faka_fofa.py api\n'
              '注意：免费账号每天额度有限，先用 queries 子命令在网页上试。')
        return
    import base64
    import urllib.parse
    import urllib.request
    q = '(body="dujiaoka" || body="acg-faka") && (body="ChatGPT" || body="Claude" || body="Gemini" || body="Grok")'
    b64 = base64.b64encode(q.encode()).decode()
    url = ('https://fofa.info/api/v1/search/all?key=%s&qbase64=%s&size=500&fields=host,title,server'
           % (key, urllib.parse.quote(b64)))
    d = json.loads(urllib.request.urlopen(url, timeout=60).read())
    if d.get('error'):
        print('FOFA 返回错误：', d.get('errmsg'))
        return
    hosts = sorted({_host(x[0]) for x in d.get('results', []) if x})
    known = {r['domain'] for r in read_csv(RELAYS)} | {r['alias'] for r in read_csv(ALIASES)}
    new = [h for h in hosts if h not in known and not SKIP_RX.search(h) and not IP_RE.match(h)]
    with open(OUT, 'w') as fh:
        fh.write('\n'.join(new) + '\n')
    print('FOFA 返回 %d，未收录 %d → %s' % (len(hosts), len(new), OUT))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('mode', choices=['queries', 'parse', 'api'])
    ap.add_argument('file', nargs='?')
    ap.add_argument('--platform', default='fofa', choices=list(QUERIES))
    a = ap.parse_args()
    {'queries': cmd_queries, 'parse': cmd_parse, 'api': cmd_api}[a.mode](a)


if __name__ == '__main__':
    main()
