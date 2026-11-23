#!/usr/bin/env python3
"""把多路候选、探活、接口和卡网指纹证据整理成一个可复查索引。

索引只保留域名、来源标签、状态、标题和布尔命中标记，不保留正文、IP、
端口、Cookie、Key 或 URL 路径。它是整理产物，不会自动把候选加入主表。

除历史的 sources/ 根目录文件外，离线读取器只认识：
  sources/batches/YYYY-MM-DD/veridrop-directory*.txt
  sources/batches/YYYY-MM-DD/directory-listings.jsonl
  sources/batches/YYYY-MM-DD/directory-review*.jsonl
批次里的 README 或其它文件不会被递归猜测或读取。
"""
import argparse
import csv
import ipaddress
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from relay_search import normalize_host  # noqa: E402

SOURCE_FILES = {
    'veridrop': ['veridrop-domains.json', 'veridrop-directory-*.txt'],
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
    'daily-feed': ['daily-candidates.jsonl'],
    'directory-review': ['directory-review-*.jsonl'],
    'contact': ['contact-harvest.jsonl'],
    'contact-verify': ['contact-browser-verify.jsonl'],
}
# These are deliberately narrow: a batch manifest may sit beside them, but is
# not a source payload and must not be picked up by a broad recursive glob.
BATCH_SOURCE_FILES = {
    'veridrop': ['veridrop-directory*.txt'],
    'directory': ['directory-listings.jsonl'],
    'directory-review': ['directory-review*.jsonl'],
}
BATCH_DATE = re.compile(r'^\d{4}-\d{2}-\d{2}$')
DATE_IN_PATH = re.compile(r'(?<!\d)(\d{4}-\d{2}-\d{2})(?!\d)')
PROBE_FILES = [
    'veridrop-probe.jsonl', 'crtsh-probe.jsonl', 'certspotter-probe.jsonl', 'prefix-expansion-probe.jsonl',
    'github-harvest-probe.jsonl', 'github-code-probe.jsonl', 'gitlab-probe.jsonl',
    'urlscan-probe.jsonl', 'npm-probe.jsonl', 'docker-hub-probe.jsonl',
    'huggingface-probe.jsonl', 'bing-probe.jsonl', 'directory-probe.jsonl', 'unified-candidate-probe.jsonl',
    'passive-refresh-probe.jsonl', 'contact-probe.jsonl',
]
SCAN_FILES = [
    'veridrop-scan.json', 'crtsh-scan.json', 'certspotter-scan.json', 'prefix-expansion-scan.json',
    'github-code-scan.json', 'gitlab-scan.json', 'urlscan-scan.json',
    'npm-scan.json', 'docker-hub-scan.json', 'huggingface-scan.json',
    'bing-scan.json', 'directory-scan.json', 'unified-candidate-scan.json', 'passive-refresh-scan.json', 'contact-scan.json',
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


def source_paths(root, source):
    """Allowlisted flat files and their equivalents directly inside dated batches."""
    for pattern in SOURCE_FILES[source]:
        for path in sorted(root.glob(pattern)):
            if not path.is_symlink() and path.is_file():
                yield path

    batches = root / 'batches'
    if batches.is_symlink():
        return
    for pattern in BATCH_SOURCE_FILES.get(source, ()):
        for path in sorted(batches.glob(f'*/{pattern}')):
            if (BATCH_DATE.fullmatch(path.parent.name) and not path.parent.is_symlink()
                    and not path.is_symlink() and path.is_file()):
                yield path


def _path_date(path):
    """Use a batch-directory or filename date only as missing-record fallback."""
    match = DATE_IN_PATH.search(path.name)
    if match:
        return match[1]
    return path.parent.name if BATCH_DATE.fullmatch(path.parent.name) else ''


def _record_key(record, path, line_number):
    """Stable newest-first key for browser review records.

    Review records normally carry ``checked``.  The dated path is a fallback
    for a minimal new-batch record, and the path/line tie-breakers make equal
    dates deterministic without changing the one-row-per-domain index shape.
    """
    date = _path_date(path)
    return (str(record.get('checked') or date), date, str(path), line_number)


def _read_source_file(index, path, source):
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


def _read_reviews(root):
    """Return the newest review record per domain from legacy and batch paths."""
    verified = {}
    review_paths = [*source_paths(root, 'contact-verify'), *source_paths(root, 'directory-review')]
    for verify_path in review_paths:
        for line_number, line in enumerate(verify_path.read_text(encoding='utf-8').splitlines()):
            if not line.strip():
                continue
            rec = json.loads(line)
            host = normalize_host(rec.get('domain'))
            if not host:
                continue
            key = _record_key(rec, verify_path, line_number)
            if host not in verified or key >= verified[host][0]:
                verified[host] = (key, rec)
    return {host: value[1] for host, value in verified.items()}


def main():
    ap = argparse.ArgumentParser(description='整理候选域名与验证证据（仅离线读取）')
    ap.add_argument('--sources-dir', default='data/raw/sources')
    ap.add_argument('--out', default='data/raw/sources/candidate-index.jsonl')
    args = ap.parse_args()
    root = Path(args.sources_dir)
    index = defaultdict(set)

    for source in SOURCE_FILES:
        for path in source_paths(root, source):
            _read_source_file(index, path, source)

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

    # 浏览器逐站实核：只取判定类别与是否打开成功，不含正文。
    # A review is evidence, not a promotion to validated/in_relays.
    verified = _read_reviews(root)

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
                'page_category': (verified.get(host) or {}).get('category', ''),
            }
            fh.write(json.dumps(row, ensure_ascii=False) + '\n')
    print('候选索引：%d；已探活：%d；接口命中：%d；主表已有：%d；浏览器实核：%d' %
          (len(index), sum(x in probes for x in index), sum(x in scans for x in index),
           sum(x in relay_info for x in index), sum(x in verified for x in index)))


if __name__ == '__main__':
    main()
