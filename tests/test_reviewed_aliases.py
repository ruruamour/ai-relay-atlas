import csv
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


TOOLS = Path(__file__).resolve().parents[1] / 'tools'


class ReviewedAliases(unittest.TestCase):
    def test_seed_only_confirmed_sites_and_keep_canonical_on_rebuild(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in ('dedupe.py', 'common.py', 'discover/relay_search.py'):
                target = root / 'tools' / name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(TOOLS / name, target)
            raw = root / 'data/raw/sources'
            raw.mkdir(parents=True)
            # The listed alias has higher discovery priority than the confirmed host.
            (raw / 'veridrop-domains.json').write_text('["old.atlas-fixture.net"]')
            (raw / 'github-list-domains.json').write_text('[]')
            data = root / 'data/relays'
            data.mkdir()
            (data / 'relays.csv').write_text(
                'domain,name,discovered_via\n'
                'main.atlas-fixture.net,Atlas Service,directory\n'
                'other.atlas-fixture.net,Different Service,directory\n')
            (data / 'aliases.csv').write_text(
                'alias,canonical,reason,discovered_via\n'
                'taken.atlas-fixture.net,other.atlas-fixture.net,merged,directory\n')
            (data / 'reviewed-aliases.csv').write_text(
                'alias,canonical,discovered_via,checked\n'
                'old.atlas-fixture.net,main.atlas-fixture.net,directory,2026-11-23\n'
                'unknown.atlas-fixture.net,missing.atlas-fixture.net,directory,2026-11-23\n'
                'other.atlas-fixture.net,main.atlas-fixture.net,directory,2026-11-23\n'
                'taken.atlas-fixture.net,main.atlas-fixture.net,directory,2026-11-23\n'
                'split.atlas-fixture.net,main.atlas-fixture.net,directory,2026-11-23\n')
            (data / 'split.txt').write_text('split.atlas-fixture.net\n')

            for _ in range(2):
                subprocess.run([sys.executable, str(root / 'tools/dedupe.py')], cwd=root,
                               check=True, capture_output=True)
                with (data / 'relays.csv').open() as f:
                    relays = {r['domain']: r for r in csv.DictReader(f)}
                self.assertEqual(set(relays), {'main.atlas-fixture.net', 'other.atlas-fixture.net'})
                self.assertEqual(relays['main.atlas-fixture.net']['name'], 'Atlas Service')
                self.assertEqual(relays['main.atlas-fixture.net']['aliases'], '1')
                with (data / 'aliases.csv').open() as f:
                    aliases = {r['alias']: r['canonical'] for r in csv.DictReader(f)}
                self.assertEqual(aliases, {'old.atlas-fixture.net': 'main.atlas-fixture.net',
                                           'taken.atlas-fixture.net': 'other.atlas-fixture.net'})
