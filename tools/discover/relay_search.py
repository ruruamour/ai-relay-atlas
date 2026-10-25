#!/usr/bin/env python3
"""生成互联网测绘查询串，并解析公开导出结果中的域名。

本脚本只查询/解析 FOFA、Quake、ZoomEye、Shodan、Censys 等平台已经
收录的公开 banner；不调用测绘平台 API，也不主动扫描目标站。

用法：
  python3 tools/discover/relay_search.py queries --platform fofa --kind all
  python3 tools/discover/relay_search.py parse --platform fofa \
      --out /tmp/relay-candidates.txt export.json
  python3 tools/scan.py /tmp/relay-candidates.txt /tmp/relay-scan.json --workers 16
  python3 tools/merge.py /tmp/relay-scan.json --via scan

导出文件可以是 JSON、CSV 或每行一个 URL/域名。解析器只写域名，不把 IP、
端口或证书等基础设施字段写入候选文件。
"""
import argparse
import csv
import io
import ipaddress
import json
import os
import re
import sys
from collections import defaultdict
from urllib.parse import urlsplit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import ALIASES, RELAYS, read_csv  # noqa: E402
try:
    import tldextract
    _TLD_EXTRACT = tldextract.TLDExtract(
        suffix_list_urls=(), cache_dir=None, include_psl_private_domains=True)
except ImportError:  # 仅在独立运行的最小环境中回退到结构校验。
    _TLD_EXTRACT = None


PLATFORMS = ('fofa', 'quake', 'zoomeye', 'shodan', 'censys')
KINDS = ('relay', 'shop')

# 查询串刻意按“系统指纹优先、业务关键词补充”拆开，避免首页不展示模型时漏站。
QUERIES = {
    'relay': {
        'fofa': [
            ('New-API / One-API / Sub2API',
             '(body="New-API" || body="New API" || body="One-API" || body="Sub2API")'),
            ('公开计价接口指纹',
             '(body="api/pricing" || body="api/v1/model-plaza" || body="api/status")'),
            ('模型广场', 'body="模型广场"'),
            ('中转业务词',
             '(body="充值" || body="余额") && (body="API" || body="模型")'),
            ('模型网关 / API Key',
             '(body="API Key" || body="模型列表" || body="倍率") && (body="API" || body="Token")'),
            ('页面标题',
             '(title="New-API" || title="One-API" || title="Sub2API" || title="模型广场")'),
        ],
        'quake': [
            ('New-API / One-API',
             'body:"New-API" OR body:"One-API" OR body:"Sub2API"'),
            ('公开计价接口指纹',
             'body:"api/pricing" OR body:"model-plaza" OR body:"api/status"'),
            ('模型广场', 'body:"模型广场"'),
            ('中转业务词', 'body:"充值" AND (body:"API" OR body:"模型")'),
        ],
        'zoomeye': [
            ('New-API / One-API',
             'app:"New-API" OR app:"One-API" OR body:"Sub2API"'),
            ('模型广场', 'body:"模型广场"'),
            ('公开计价接口指纹',
             'body:"api/pricing" OR body:"model-plaza" OR body:"api/status"'),
            ('中转业务词', 'body:"充值" && (body:"API" || body:"模型")'),
        ],
        'shodan': [
            ('New-API / One-API',
             'http.html:"New-API" OR http.html:"One-API" OR http.html:"Sub2API"'),
            ('公开计价接口指纹',
             'http.html:"api/pricing" OR http.html:"model-plaza" OR http.html:"api/status"'),
            ('模型广场', 'http.html:"模型广场" OR http.title:"模型广场"'),
            ('中转业务词', 'http.html:"充值" http.html:"API"'),
        ],
        'censys': [
            ('New-API / One-API',
             'services.http.response.body: "New-API" OR services.http.response.body: "One-API" OR services.http.response.body: "Sub2API"'),
            ('模型广场', 'services.http.response.body: "模型广场"'),
            ('公开计价接口指纹',
             'services.http.response.body: "api/pricing" OR services.http.response.body: "model-plaza"'),
        ],
    },
    'shop': {
        'fofa': [
            ('独角数卡', 'body="dujiaoka"'),
            ('独角数卡资源路径', 'body="/assets/dujiaoka"'),
            ('异次元发卡', 'body="acg-faka" || body="异次元发卡"'),
            ('ZFAKA', 'body="zfaka"'),
            ('卡网通用词', 'body="自动发货" || body="卡密" || body="寄售"'),
            ('AI 卡网',
             '(body="自动发货" || body="卡密" || body="寄售") && (body="ChatGPT" || body="Claude" || body="Gemini" || body="Grok")'),
            ('发卡标题', 'title="发卡" || title="卡网" || title="发卡网"'),
        ],
        'quake': [
            ('独角数卡', 'body:"dujiaoka"'),
            ('异次元发卡', 'body:"acg-faka" OR body:"异次元发卡"'),
            ('卡网通用词', 'body:"自动发货" OR body:"卡密" OR body:"寄售"'),
            ('AI 卡网', 'body:"自动发货" AND body:"ChatGPT"'),
        ],
        'zoomeye': [
            ('独角数卡', 'app:"dujiaoka" OR body:"dujiaoka"'),
            ('异次元发卡', 'body:"acg-faka" OR body:"异次元发卡"'),
            ('卡网通用词', 'body:"自动发货" OR body:"卡密" OR body:"寄售"'),
            ('AI 卡网', 'body:"自动发货" && body:"ChatGPT"'),
        ],
        'shodan': [
            ('独角数卡', 'http.html:"dujiaoka"'),
            ('异次元发卡', 'http.html:"acg-faka"'),
            ('卡网通用词', 'http.html:"自动发货" OR http.html:"卡密"'),
            ('AI 卡网', 'http.html:"自动发货" http.html:"ChatGPT"'),
            ('发卡标题', 'http.title:"发卡" OR http.title:"卡网"'),
        ],
        'censys': [
            ('独角数卡', 'services.http.response.body: "dujiaoka"'),
            ('异次元发卡', 'services.http.response.body: "acg-faka"'),
            ('卡网通用词', 'services.http.response.body: "自动发货" OR services.http.response.body: "卡密"'),
        ],
    },
}

# 仅排除明显的代码托管、文档和官方站；不要按“看起来不像 AI”过度过滤。
SKIP_RX = re.compile(
    r'(?:^|\.)(?:github|githubusercontent|gitlab|gitee|npmjs|readthedocs|docs|wiki|ibb|imgur|imgbb|'
    r'example|localhost|vercel|netlify|pages\.dev|cloudflare|openai|anthropic|google)\.',
    re.I,
)
SKIP_HOSTS = {
    'github.com', 'githubusercontent.com', 'gitlab.com', 'gitee.com',
    'openai.com', 'anthropic.com', 'ai.google.dev', 'google.com',
    'dujiaoka.com', 'acg-faka.com', 'zfaka.com', 'veridrop.org',
}

# 不同平台的导出字段命名不统一；只从这些字段提取域名。
HOST_KEYS = {
    'host', 'hostname', 'domain', 'domains', 'url', 'uri', 'link', 'web_url',
    'http_host', 'ip_str', 'ip', 'target', 'asset',
}
URL_RX = re.compile(
    r'(?i)(?:(?:https?|wss?)://|//)?'
    r'(?:[a-z0-9\u0080-\uffff](?:[a-z0-9\u0080-\uffff-]{0,61}[a-z0-9\u0080-\uffff])?\.)+'
    r'[a-z\u0080-\uffff]{2,63}(?::\d+)?(?:[/][^\s"\'<>]*)?'
)


def is_ip(host):
    try:
        ipaddress.ip_address(host.strip('[]'))
        return True
    except ValueError:
        return False


def normalize_host(value):
    """从 URL/host 字段取出域名；IP、端口、路径和明显非站点域名丢弃。"""
    if value is None or isinstance(value, (dict, list, tuple)):
        return ''
    s = str(value).strip().strip('"\'<>[]')
    if not s:
        return ''
    s = s.lstrip('*.')
    if not re.match(r'^[a-z][a-z0-9+.-]*://', s, re.I):
        s = '//' + s
    try:
        host = (urlsplit(s).hostname or '').rstrip('.').lower()
    except ValueError:
        return ''
    if not host or is_ip(host) or host in SKIP_HOSTS or SKIP_RX.search(host):
        return ''
    if _TLD_EXTRACT is not None:
        parsed = _TLD_EXTRACT(host)
        if not parsed.domain or not parsed.suffix:
            return ''
    labels = host.split('.')
    if len(labels) < 2 or any(not x or len(x) > 63 for x in labels):
        return ''
    if any(not re.fullmatch(r'[a-z0-9\u0080-\uffff](?:[a-z0-9\u0080-\uffff-]{0,61}[a-z0-9\u0080-\uffff])?', x, re.I)
           for x in labels):
        return ''
    return host


def hosts_in_text(text):
    """从纯文本中提取 URL/域名，适配每行一个域名和简单 CSV。"""
    out = set()
    for match in URL_RX.findall(text or ''):
        host = normalize_host(match)
        if host:
            out.add(host)
    return out


def _extract_value(value):
    out = set()
    if isinstance(value, str):
        # host 字段可能是 host:port，也可能是完整 URL；正则再兜底处理描述字段。
        host = normalize_host(value)
        if host:
            out.add(host)
        out.update(hosts_in_text(value))
    elif isinstance(value, (list, tuple)):
        for x in value:
            out.update(_extract_value(x))
    elif isinstance(value, dict):
        out.update(extract_obj(value))
    return out


def extract_obj(obj):
    out = set()
    if isinstance(obj, dict):
        for key, value in obj.items():
            lk = re.sub(r'[^a-z0-9_]', '_', str(key).lower())
            if lk in HOST_KEYS or any(token in lk for token in ('hostname', 'domain', 'url', 'host')):
                out.update(_extract_value(value))
            elif isinstance(value, (dict, list, tuple)):
                out.update(extract_obj(value))
    elif isinstance(obj, (list, tuple)):
        for value in obj:
            out.update(extract_obj(value) if isinstance(value, (dict, list, tuple)) else _extract_value(value))
    elif isinstance(obj, str):
        out.update(hosts_in_text(obj))
    return out


def parse_json(text):
    try:
        obj = json.loads(text)
    except (TypeError, ValueError):
        return set()
    return extract_obj(obj)


def parse_csv(text):
    out = set()
    rows = list(csv.reader(io.StringIO(text)))
    if not rows:
        return out
    # 优先按有表头的 CSV 解析，平台导出通常至少包含 host/domain/url 之一。
    fieldnames = [x.strip().lower() for x in rows[0]]
    wanted = [i for i, x in enumerate(fieldnames)
              if x in HOST_KEYS or any(t in x for t in ('host', 'domain', 'hostname', 'url'))]
    if wanted:
        for row in rows[1:]:
            for i in wanted:
                if i < len(row):
                    out.update(_extract_value(row[i]))
        return out
    for row in rows:
        for value in row[:2]:
            out.update(hosts_in_text(value))
    return out


def parse_file(filename):
    with open(filename, encoding='utf-8', errors='replace') as fh:
        text = fh.read()
    stripped = text.lstrip()
    if stripped.startswith('{') or stripped.startswith('['):
        hosts = parse_json(text)
    elif ',' in text or '\t' in text:
        hosts = parse_csv(text)
        if not hosts:
            hosts = hosts_in_text(text)
    else:
        hosts = hosts_in_text(text)
    return hosts


def known_hosts():
    known = {r.get('domain', '').lower() for r in read_csv(RELAYS)}
    known |= {r.get('alias', '').lower() for r in read_csv(ALIASES)}
    known.discard('')
    return known


def cmd_queries(args):
    platforms = PLATFORMS if args.platform == 'all' else [args.platform]
    kinds = KINDS if args.kind == 'all' else [args.kind]
    if args.format == 'json':
        out = []
        for kind in kinds:
            for platform in platforms:
                for name, query in QUERIES[kind][platform]:
                    out.append(dict(kind=kind, platform=platform, name=name, query=query))
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return
    for kind in kinds:
        print('# ' + ('AI 中转站' if kind == 'relay' else '发卡/卡网'))
        for platform in platforms:
            print('\n## ' + platform.upper())
            for name, query in QUERIES[kind][platform]:
                print('\n### ' + name + '\n```text\n' + query + '\n```')


def cmd_parse(args):
    found = defaultdict(list)
    for filename in args.files:
        try:
            hosts = parse_file(filename)
        except OSError as exc:
            print('跳过 %s：%s' % (filename, exc), file=sys.stderr)
            continue
        for host in hosts:
            found[host].append(filename)
    known = set() if args.include_known else known_hosts()
    new = sorted(host for host in found if host not in known)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, 'w', encoding='utf-8') as fh:
        for host in new:
            fh.write(host + '\n')
    evidence = args.evidence or os.path.splitext(args.out)[0] + '.jsonl'
    os.makedirs(os.path.dirname(os.path.abspath(evidence)), exist_ok=True)
    with open(evidence, 'w', encoding='utf-8') as fh:
        for host in new:
            rec = dict(domain=host, kind=args.kind, platform=args.platform,
                       source_files=sorted(set(found[host])))
            fh.write(json.dumps(rec, ensure_ascii=False) + '\n')
    print('提取域名 %d，已收录 %d，新增 %d' % (len(found), len(found) - len(new), len(new)))
    print('候选：%s\n证据：%s' % (args.out, evidence))


def main():
    ap = argparse.ArgumentParser(description='生成测绘查询串并解析公开导出结果')
    sub = ap.add_subparsers(dest='command', required=True)

    q = sub.add_parser('queries', help='输出查询串')
    q.add_argument('--platform', choices=list(PLATFORMS) + ['all'], default='all')
    q.add_argument('--kind', choices=list(KINDS) + ['all'], default='all')
    q.add_argument('--format', choices=['text', 'json'], default='text')
    q.set_defaults(func=cmd_queries)

    p = sub.add_parser('parse', help='解析 JSON/CSV/文本导出结果')
    p.add_argument('files', nargs='+')
    p.add_argument('--platform', default='unknown')
    p.add_argument('--kind', choices=list(KINDS), default='relay')
    p.add_argument('--out', default='/tmp/relay-candidates.txt')
    p.add_argument('--evidence', help='证据 JSONL 路径，默认与 --out 同名')
    p.add_argument('--include-known', action='store_true', help='保留当前主表已经收录的域名')
    p.set_defaults(func=cmd_parse)

    args = ap.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
