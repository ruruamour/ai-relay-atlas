#!/usr/bin/env python3
"""Poll fixed public directory feeds; keep new leads, never visit listed sites."""
import argparse
import csv
import datetime as dt
import json
import os
import re
import sys
import tempfile
from http.client import HTTPException
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener
from urllib.robotparser import RobotFileParser

from daily_lists import LIST_SOURCES
from daily_web import WEB_SOURCES
from relay_search import normalize_host
from common import has_secret


SOURCES = {**WEB_SOURCES, **LIST_SOURCES}
# When retiring a feed or moving its URL, keep its old URLs here for evidence
# validation only. They are never fetched by the scheduler.
HISTORICAL_FEED_URLS = {}
DATA = Path(__file__).resolve().parents[2] / 'data'
QUEUE = Path('raw/sources/daily-candidates.jsonl')
UA = 'ai-relay-atlas/1.0 (+https://github.com/ruruamour/ai-relay-atlas)'
MAX_BYTES = 8_000_000


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *args):
        return None


def get_text(url, limit):
    # A directory moving to a new origin requires a reviewed config change.
    req = Request(url, headers={'User-Agent': UA, 'Accept-Encoding': 'identity'})
    with build_opener(NoRedirect()).open(req, timeout=25) as response:
        length = response.headers.get('Content-Length')
        body = response.read(limit + 1)
    if len(body) > limit:
        raise ValueError('response exceeds size limit')
    if length is not None and len(body) != int(length):
        raise ValueError('incomplete source response')
    return body.decode('utf-8-sig')


def fetch(url):
    parts = urlsplit(url)
    if parts.hostname != 'raw.githubusercontent.com':
        try:
            robots = get_text(f'https://{parts.netloc}/robots.txt', 512_000)
        except HTTPError as exc:
            if exc.code not in (404, 410):
                raise
        else:
            rules = RobotFileParser()
            rules.parse(robots.splitlines())
            if not rules.can_fetch(UA, url):
                raise ValueError('blocked by robots.txt')
    return get_text(url, MAX_BYTES)


def comparison_key(host):
    host = host.rstrip('.').lower().removeprefix('www.')
    try:
        return host.encode('idna').decode('ascii')
    except UnicodeError:
        # Historical indexes include labels too large after IDNA conversion.
        return host


def candidate_host(value):
    if not isinstance(value, str) or not value or any(c.isspace() for c in value):
        return ''
    try:
        p = urlsplit(value if '://' in value else '//' + value)
        if p.scheme not in ('', 'http', 'https') or not p.hostname or p.netloc.lower() != p.hostname:
            return ''  # No credentials, ports or IP literals.
        host = p.hostname.rstrip('.').encode('idna').decode('ascii')
    except (ValueError, UnicodeError):
        return ''
    return host if normalize_host(host) == host and not has_secret(host) else ''


def valid_evidence(page, feed):
    if urlsplit(feed).hostname == 'raw.githubusercontent.com':
        return page == feed
    try:
        p = urlsplit(page)
        return (p.scheme == 'https' and p.netloc == urlsplit(feed).netloc and not p.query
                and not p.fragment and page == p.geturl() and p.path.startswith('/')
                and re.fullmatch(r'/[\w./-]*', p.path, re.ASCII) and '//' not in p.path
                and '..' not in p.path and not has_secret(page))
    except ValueError:
        return False


def known_domains(data):
    # Fail closed on missing inputs; a broken checkout is not an empty baseline.
    known = set()
    for filename, columns in [('relays.csv', ('domain', 'api_host')), ('aliases.csv', ('alias', 'canonical'))]:
        with (data / 'relays' / filename).open(encoding='utf-8', newline='') as f:
            for row in csv.DictReader(f):
                known.update(comparison_key(row[c]) for c in columns if row[c])
    with (data / 'raw/sources/candidate-index.jsonl').open(encoding='utf-8') as f:
        known.update(comparison_key(json.loads(line)['domain']) for line in f if line.strip())
    return known


def read_queue(path, evidence_urls):
    rows = []
    with path.open(encoding='utf-8') as f:
        for line in f:
            r = json.loads(line)
            if (not isinstance(r, dict) or set(r) != {'domain', 'source_site', 'listing_page', 'first_seen'}
                    or not all(isinstance(v, str) and v for v in r.values())
                    or r['domain'] != candidate_host(r['domain'])
                    or not any(valid_evidence(r['listing_page'], url) for url in evidence_urls.get(r['source_site'], ()))
                    or dt.date.fromisoformat(r['first_seen']).isoformat() != r['first_seen']):
                raise ValueError(f'invalid queue record in {path.name}')
            rows.append(r)
    return rows


def collect(data, pending, sources, selected, today, fetcher):
    known = known_domains(data)
    rows, spelling = {}, {}

    def keep(r):
        key = comparison_key(r['domain'])
        domain = spelling.setdefault(key, r['domain'])
        rows.setdefault((domain, r['source_site']), dict(r, domain=domain))

    evidence_urls = {source: set(urls) for source, urls in HISTORICAL_FEED_URLS.items()}
    for source, (url, _) in sources.items():
        evidence_urls.setdefault(source, set()).add(url)
    for r in read_queue(data / QUEUE, evidence_urls):
        keep(r)
    if pending is not None:
        for r in read_queue(pending, evidence_urls):
            k = comparison_key(r['domain'])
            if k not in known or k in spelling:
                keep(r)

    successes = 0
    for source in selected:
        url, parse = sources[source]
        try:
            found = {}
            for value, page in parse(fetcher(url)):
                host = candidate_host(value)
                if not host or not valid_evidence(page, url):
                    continue
                found[host] = min(found.get(host, page), page)
            if not found:
                raise ValueError('no usable entries')
        except (ValueError, OSError, HTTPException, csv.Error, KeyError) as exc:
            # Never echo untrusted page text or a redirect target into CI logs.
            detail = f'HTTP {exc.code}' if isinstance(exc, HTTPError) else type(exc).__name__
            print(f'WARNING: {source}: fetch or parse failed ({detail}); previous entries kept', file=sys.stderr)
            continue
        successes += 1
        before = len(rows)
        for host, page in sorted(found.items()):
            key = comparison_key(host)
            if key in known and key not in spelling:
                continue
            keep(dict(domain=host, source_site=source, listing_page=page, first_seen=today))
        print(f'{source}: {len(found)} listed domains, {len(rows) - before} new source records')
    if not successes:
        raise ValueError('all sources failed; queue not written')
    return ''.join(json.dumps(rows[k], ensure_ascii=False, separators=(',', ':')) + '\n' for k in sorted(rows))


def save_if_changed(path, text):
    if path.exists() and path.read_text(encoding='utf-8') == text:
        return False
    with tempfile.NamedTemporaryFile('w', encoding='utf-8', dir=path.parent, delete=False) as temp:
        try:
            temp.write(text)
            temp.close()
            os.replace(temp.name, path)
        finally:
            Path(temp.name).unlink(missing_ok=True)
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--pending', type=Path, help='carry forward the open review PR queue (data only)')
    ap.add_argument('--source', action='append', choices=sorted(SOURCES), help='select a feed; default: all')
    ap.add_argument('--out', type=Path, default=DATA / QUEUE, help='optional local preview output')
    ap.add_argument('--dry-run', action='store_true', help='print counts only; do not write any file')
    args = ap.parse_args()
    try:
        text = collect(DATA, args.pending, SOURCES, sorted(set(args.source or SOURCES)),
                       dt.datetime.now(dt.timezone.utc).date().isoformat(), fetch)
        n = text.count('\n')
        if args.dry_run:
            print(f'Preview: {n} cumulative source records; no files written')
        elif save_if_changed(args.out, text):
            print(f'Queue updated: {n} cumulative source records')
        else:
            print(f'No changes: {n} cumulative source records')
    except (OSError, KeyError, ValueError) as exc:
        ap.exit(1, f'daily candidates: {exc}\n')


if __name__ == '__main__':
    main()
