import contextlib
import io
import json
import sys
import tempfile
import unittest
from http.client import IncompleteRead
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools/discover'))
import daily_candidates as daily


class DailyCandidates(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.data = Path(tmp.name)
        (self.data / 'relays').mkdir()
        (self.data / 'relays/relays.csv').write_text(
            'domain,api_host\nwww.primary.atlas-fixture.net,prices.atlas-fixture.net\n')
        (self.data / 'relays/aliases.csv').write_text(
            'alias,canonical\nmirror.atlas-fixture.net,www.primary.atlas-fixture.net\n')
        self.queue = self.data / daily.QUEUE
        self.queue.parent.mkdir(parents=True)
        self.queue.touch()
        (self.queue.parent / 'candidate-index.jsonl').write_text('{"domain":"index.atlas-fixture.net"}\n')
        self.sources = {
            'one': ('https://one.atlas-fixture.net/list', json.loads),
            'two': ('https://two.atlas-fixture.net/list', json.loads),
        }

    def collect(self, feed_rows, when='2026-11-23', pending=None):
        def fake_get(url):
            source = {v[0]: k for k, v in self.sources.items()}[url]
            if source not in feed_rows:
                raise TimeoutError
            if isinstance(feed_rows[source], Exception):
                raise feed_rows[source]
            return json.dumps(feed_rows[source])

        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return daily.collect(self.data, pending, self.sources, list(self.sources), when, fake_get)

    def test_net_new_only_multiple_sources_and_repeat_is_byte_stable(self):
        page = 'https://one.atlas-fixture.net/site/one'
        other = 'https://two.atlas-fixture.net/site/one'
        known = ['primary', 'prices', 'www.mirror', 'www.index']
        hit = 'Alpha.atlas-fixture.net'
        feed = {'one': [(h + '.atlas-fixture.net', page) for h in known] +
                       [(hit, page), (hit, page), ('127.0.0.1', page), ('x.atlas-fixture.net', other)],
                'two': [('www.alpha.atlas-fixture.net', other)]}
        first = self.collect(feed)
        rows = list(map(json.loads, first.splitlines()))
        self.assertEqual([r['domain'] for r in rows], ['alpha.atlas-fixture.net'] * 2)
        self.assertEqual([r['source_site'] for r in rows], ['one', 'two'])
        self.assertEqual([r['listing_page'] for r in rows], [page, other])
        self.assertTrue(daily.save_if_changed(self.queue, first))
        self.assertFalse(daily.save_if_changed(self.queue, self.collect(feed, when='2026-11-24')))
        self.assertEqual(self.queue.read_text(), first)

    def test_open_pr_survives_disappearance_or_partial_failure(self):
        pending = self.data / 'pending.jsonl'
        page = 'https://one.atlas-fixture.net/site/a'
        previous = self.collect({'one': [('old.atlas-fixture.net', page)]})
        pending.write_text(previous)
        result = self.collect({'two': [('new.atlas-fixture.net', 'https://two.atlas-fixture.net/item')]},
                              when='2026-11-24', pending=pending)
        seen = {r['domain']: r['first_seen'] for r in map(json.loads, result.splitlines())}
        self.assertEqual(seen, {'old.atlas-fixture.net': '2026-11-23', 'new.atlas-fixture.net': '2026-11-24'})
        # If the base now knows the old host independently, don't re-propose it.
        (self.queue.parent / 'candidate-index.jsonl').write_text('{"domain":"old.atlas-fixture.net"}\n')
        self.assertNotIn('old.atlas-fixture.net', self.collect({'one': [('old.atlas-fixture.net', page)]},
                                                             pending=pending))

    def test_empty_failed_or_malformed_sources_do_not_overwrite_queue(self):
        first = self.collect({'one': [('kept.atlas-fixture.net', 'https://one.atlas-fixture.net/site/a')]})
        self.queue.write_text(first)
        with self.assertRaisesRegex(ValueError, 'all sources failed'):
            self.collect({'one': []})
        self.assertEqual(self.queue.read_text(), first)
        pending = self.data / 'bad.jsonl'
        pending.write_text(first.replace('https://one.atlas-fixture.net', 'https://unrelated.invalid'))
        with self.assertRaisesRegex(ValueError, 'invalid queue'):
            self.collect({'one': []}, pending=pending)

    def test_broken_http_stream_is_a_single_source_failure(self):
        error = IncompleteRead(b'partial source page')
        self.queue.write_text(self.collect({'one': [('old.atlas-fixture.net', 'https://one.atlas-fixture.net/old')]}))
        result = self.collect({'one': error, 'two': [('new.atlas-fixture.net', 'https://two.atlas-fixture.net/new')]})
        self.assertEqual({r['domain'] for r in map(json.loads, result.splitlines())},
                         {'old.atlas-fixture.net', 'new.atlas-fixture.net'})
        with self.assertRaisesRegex(ValueError, 'all sources failed'):
            self.collect({'one': error, 'two': error})

    def test_rejects_short_response_even_when_read_does_not_raise(self):
        body = io.BytesIO(b'partial')
        body.headers = {'Content-Length': str(len(b'complete source page'))}
        with patch.object(daily, 'build_opener') as opener:
            opener.return_value.open.return_value = body
            with self.assertRaisesRegex(ValueError, 'incomplete source response'):
                daily.get_text(self.sources['one'][0], 256)

    def test_retired_source_is_allowed_as_evidence_but_never_fetched(self):
        historical = self.collect({'one': [('old.atlas-fixture.net', 'https://one.atlas-fixture.net/old')]})
        self.queue.write_text(historical)
        retired, _ = self.sources.pop('one')
        with patch.dict(daily.HISTORICAL_FEED_URLS, {'one': (retired,)}):
            result = self.collect({'two': [('new.atlas-fixture.net', 'https://two.atlas-fixture.net/new')]})
        self.assertIn(json.loads(historical), list(map(json.loads, result.splitlines())))

    def test_only_declared_evidence_and_plain_public_hostnames(self):
        for value in ('localhost', '127.0.0.1', 'https://user@site.atlas-fixture.net',
                      'https://site.atlas-fixture.net:443', 'file://site.atlas-fixture.net'):
            self.assertFalse(daily.candidate_host(value), value)
        for bad in ('https://one.atlas-fixture.net/site?a=b', 'https://one.atlas-fixture.net/#token',
                    'https://other.atlas-fixture.net/entry', 'http://one.atlas-fixture.net/site'):
            self.assertFalse(daily.valid_evidence(bad, self.sources['one'][0]), bad)
        raw = 'https://raw.githubusercontent.com/org/list/main/data.csv'
        self.assertTrue(daily.valid_evidence(raw, raw))
        self.assertFalse(daily.valid_evidence(raw + '.other', raw))

    def test_non_encodable_historical_domain_does_not_break_a_run(self):
        invalid = '\u6c49' * 61 + '.net'
        index = self.queue.parent / 'candidate-index.jsonl'
        index.write_text(json.dumps({'domain': invalid}) + '\n')
        self.assertIn(invalid, daily.known_domains(self.data))
        self.assertFalse(daily.candidate_host(invalid))

    def test_network_reads_only_robots_then_fixed_url_and_refuses_redirects(self):
        url = self.sources['one'][0]
        with patch.object(daily, 'get_text', return_value='User-agent: *\nDisallow: /list') as get:
            with self.assertRaisesRegex(ValueError, 'robots'):
                daily.fetch(url)
            self.assertEqual(get.call_count, 1)
        missing = HTTPError(url, 404, 'missing', {}, None)
        with patch.object(daily, 'get_text', side_effect=[missing, 'listing']) as get:
            self.assertEqual(daily.fetch(url), 'listing')
            self.assertEqual([c.args[0] for c in get.call_args_list],
                             ['https://one.atlas-fixture.net/robots.txt', url])
        self.assertIsNone(daily.NoRedirect().redirect_request(None, None, 302, '', {}, 'https://other.invalid/'))
