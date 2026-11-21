import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from check_links import check


class LocalLinks(unittest.TestCase):
    def test_links_and_anchors_without_contacting_external_sites(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'docs').mkdir()
            target = root / 'docs' / '数据.md'
            target.write_text('## 价格\n\n## 价格\n\n<a id="old-id"></a>\n', encoding='utf-8')
            (root / 'README.md').write_text(
                '[heading](docs/%E6%95%B0%E6%8D%AE.md#%E4%BB%B7%E6%A0%BC)\n'
                '[duplicate](docs/数据.md#价格-1) · [alias](docs/数据.md#old-id)\n'
                '[external](https://example.invalid/) · `[example](missing.md)`\n'
                '~~~markdown\n[example](other.md)\n~~~\n', encoding='utf-8')
            self.assertEqual(check(root), (2, []))
            target.write_text('## 价格\n\n## 价格\n', encoding='utf-8')
            self.assertEqual(check(root), (2, ['README.md:2: 找不到锚点 docs/数据.md#old-id']))

    def test_broken_targets_annotated_with_source_location(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'README.md').write_text(
                '# Home\n[missing](absent.csv)\n[outside](../README.md)\n', encoding='utf-8')
            self.assertEqual(check(root), (1, [
                'README.md:2: 找不到路径 absent.csv', 'README.md:3: 找不到路径 ../README.md']))
