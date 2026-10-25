#!/usr/bin/env python3
"""把首页指纹候选整理成供人工审核的 CSV，不自动写入已确认店铺表。"""
import argparse
import csv
import json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description='生成卡网候选审核表')
    ap.add_argument('--input', default='data/raw/sources/shop-fingerprint-candidates.jsonl')
    ap.add_argument('--relays', default='data/relays/relays.csv')
    ap.add_argument('--out', default='data/shops/candidates.csv')
    ap.add_argument('--browser-review', default='data/raw/sources/shop-browser-review.jsonl')
    args = ap.parse_args()

    browser = {}
    review_path = Path(args.browser_review)
    if review_path.exists():
        for line in review_path.read_text(encoding='utf-8').splitlines():
            if line.strip():
                rec = json.loads(line)
                browser[rec['domain']] = rec

    with open(args.relays, encoding='utf-8', newline='') as fh:
        relay = {r['domain'] for r in csv.DictReader(fh)}
    # aliases.csv 单独读取，避免把有 API 网关记录的镜像误列为全新店。
    alias_path = Path(args.relays).with_name('aliases.csv')
    if alias_path.exists():
        with alias_path.open(encoding='utf-8', newline='') as fh:
            relay.update(r['alias'] for r in csv.DictReader(fh))

    rows = []
    with open(args.input, encoding='utf-8') as fh:
        for line in fh:
            if not line.strip():
                continue
            r = json.loads(line)
            if r.get('likelihood') not in ('high', 'medium'):
                continue
            known = r['domain'] in relay
            rows.append({
                'domain': r['domain'], 'status': r.get('status'),
                'likelihood': r.get('likelihood'), 'title': r.get('title', ''),
                'systems': '/'.join(r.get('systems') or []),
                'common_hits': '/'.join(r.get('common_hits') or []),
                'ai_hits': '/'.join(r.get('ai_hits') or []),
                'relay_overlap': 'yes' if known else 'no',
                'last_checked': r.get('checked', ''),
                'browser_review': (browser.get(r['domain']) or {}).get('review', ''),
                'rendered_title': (browser.get(r['domain']) or {}).get('rendered_title', ''),
                'notes': ('已有中转站记录，需区分 API 网关与商品店' if known else
                          ('浏览器确认首页有商品/卡密相关内容，仍需核对商品与在售状态'
                           if (browser.get(r['domain']) or {}).get('review') == 'rendered_shop'
                           else '待人工确认在售与商品类型')),
            })
    rows.sort(key=lambda r: (0 if r['likelihood'] == 'high' else 1, r['domain']))
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open('w', encoding='utf-8', newline='') as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    print('审核候选：%d；其中不在中转站主表：%d；输出：%s' %
          (len(rows), sum(r['relay_overlap'] == 'no' for r in rows), out))


if __name__ == '__main__':
    main()
