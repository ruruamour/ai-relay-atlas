#!/usr/bin/env python3
"""把多路候选、探活、接口和卡网指纹证据整理成一个可复查索引。

索引只保留域名、来源标签、状态、标题和布尔命中标记，不保留正文、IP、
端口、Cookie、Key 或 URL 路径。它是整理产物，不会自动把候选加入主表。
"""
import argparse
import csv
import ipaddress
import json
import os
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from relay_search import normalize_host  # noqa: E402

SOURCE_FILES = {
    'veridrop': ['veridrop-domains.json'],
    'github-list': ['github-list-domains.json'],
    'crtsh': ['crtsh-domains.json'],
    'certspotter': ['certspotter-domains.json'],
    'prefix': ['prefix-expansion-candidates.txt'],
    'github': ['github-harvest.jsonl'],
    'github-code': ['github-code-harvest.jsonl'],
    'gitlab': ['gitlab-harvest.jsonl'],
    'urlscan': ['urlscan-candidates.jsonl'],
    'npm': ['npm-harvest.jsonl'],
    'docker-hub': ['docker-hub-harvest.jsonl'],
    'huggingface': ['huggingface-harvest.jsonl'],
    'sourcegraph': ['sourcegraph-candidates.jsonl'],
    'bing': ['bing-candidates.jsonl'],
    'directory': ['directory-harvest.jsonl'],
}
PROBE_FILES = [
    'veridrop-probe.jsonl', 'crtsh-probe.jsonl', 'certspotter-probe.jsonl', 'prefix-expansion-probe.jsonl',
    'github-harvest-probe.jsonl', 'github-code-probe.jsonl', 'gitlab-probe.jsonl',
    'urlscan-probe.jsonl', 'npm-probe.jsonl', 'docker-hub-probe.jsonl',
    'huggingface-probe.jsonl', 'bing-probe.jsonl', 'directory-probe.jsonl', 'unified-candidate-probe.jsonl',
    'passive-refresh-probe.jsonl',
]
SCAN_FILES = [
    'veridrop-scan.json', 'crtsh-scan.json', 'certspotter-scan.json', 'prefix-expansion-scan.json',
    'github-code-scan.json', 'gitlab-scan.json', 'urlscan-scan.json',
    'npm-scan.json', 'docker-hub-scan.json', 'huggingface-scan.json',
    'bing-scan.json', 'directory-scan.json', 'unified-candidate-scan.json', 'passive-refresh-scan.json',
]


def is_ip(value):
    try:
        ipaddress.ip_address(str(value))
        return True
    except ValueError:
        return False


def add_source(index, host, source):
    host = normalize_host(host)
    if host and not is_ip(host):
        index[host].add(source)


def main():
    ap = argparse.ArgumentParser(description='整理候选域名与验证证据')
    ap.add_argument('--sources-dir', default='data/raw/sources')
    ap.add_argument('--out', default='data/raw/sources/candidate-index.jsonl')
    args = ap.parse_args()
    root = Path(args.sources_dir)
    index = defaultdict(set)

    for source, names in SOURCE_FILES.items():
        for name in names:
            path = root / name
            if not path.exists():
                continue
            if path.suffix == '.jsonl':
                for line in path.read_text(encoding='utf-8').splitlines():
                    if line.strip():
                        add_source(index, json.loads(line).get('domain'), source)
            elif path.suffix == '.json':
                obj = json.loads(path.read_text(encoding='utf-8'))
                values = obj.keys() if isinstance(obj, dict) else obj
                for host in values:
                    add_source(index, host, source)
            else:
                for host in path.read_text(encoding='utf-8').splitlines():
                    add_source(index, host.strip(), source)

    probes = {}
    for name in PROBE_FILES:
        path = root / name
        if not path.exists():
            continue
        for line in path.read_text(encoding='utf-8').splitlines():
            if not line.strip():
                continue
            rec = json.loads(line)
            host = normalize_host(rec.get('domain'))
            if not host or is_ip(host):
                continue
            old = probes.get(host)
            if old is None or (rec.get('checked') or '') >= (old.get('checked') or ''):
                probes[host] = rec

    scans = set()
    for name in SCAN_FILES:
        path = root / name
        if not path.exists():
            continue
        obj = json.loads(path.read_text(encoding='utf-8'))
        if isinstance(obj, dict):
            for host in obj:
                host = normalize_host(host)
                if host and not is_ip(host):
                    scans.add(host)

    relay_info = {}
    relay_path = Path('data/relays/relays.csv')
    if relay_path.exists():
        relay_info = {normalize_host(r['domain']): r for r in csv.DictReader(relay_path.open(encoding='utf-8'))}

    shops = {}
    shop_path = root / 'shop-fingerprint-candidates.jsonl'
    if shop_path.exists():
        for line in shop_path.read_text(encoding='utf-8').splitlines():
            if line.strip():
                rec = json.loads(line)
                host = normalize_host(rec.get('domain'))
                if host:
                    shops[host] = rec

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open('w', encoding='utf-8') as fh:
        for host in sorted(index):
            probe = probes.get(host) or {}
            shop = shops.get(host) or {}
            row = {
                'domain': host,
                'sources': sorted(index[host]),
                'validated': host in probes or host in relay_info,
                'status': probe.get('status') if probe else (relay_info.get(host) or {}).get('http_status'),
                'title': probe.get('title', '') if probe else (relay_info.get(host) or {}).get('name', ''),
                'checked': probe.get('checked', '') if probe else (relay_info.get(host) or {}).get('last_checked', ''),
                'scan_hit': host in scans,
                'in_relays': host in relay_info,
                'shop_likelihood': shop.get('likelihood', ''),
                'shop_systems': shop.get('systems') or [],
            }
            fh.write(json.dumps(row, ensure_ascii=False) + '\n')
    print('候选索引：%d；已探活：%d；接口命中：%d；主表已有：%d' %
          (len(index), sum(x in probes for x in index), sum(x in scans for x in index),
           sum(x in relay_info for x in index)))


if __name__ == '__main__':
    main()
