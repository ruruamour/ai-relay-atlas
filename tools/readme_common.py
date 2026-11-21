#!/usr/bin/env python3
"""Counts for the two homepages. The build generates the relay summary first."""
import json
from pathlib import Path

from common import iter_csv, path


def snapshot():
    data = Path(path('data'))
    relays = data / 'relays'
    counts = json.loads((relays / 'summary.json').read_text(encoding='utf-8'))
    for name in ('shops', 'products', 'candidates'):
        counts[name] = sum(1 for _ in iter_csv(data / 'shops' / f'{name}.csv'))
    counts['model_pages'] = sum(p.name != 'index.md' for p in (relays / 'by-model').glob('*.md'))
    with (data / 'raw/sources/candidate-index.jsonl').open(encoding='utf-8') as index:
        counts['indexed_domains'] = sum(1 for line in index if line.strip())
    return counts
