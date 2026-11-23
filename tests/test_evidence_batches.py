import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


INDEXER = Path(__file__).resolve().parents[1] / "tools" / "discover" / "index_candidates.py"


class EvidenceBatchTests(unittest.TestCase):
    def test_nested_and_legacy_batches_merge_and_keep_latest_review(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            sources = root / "data" / "raw" / "sources"
            sources.mkdir(parents=True)

            (sources / "veridrop-domains.json").write_text(
                json.dumps(["legacy.atlas-fixture.net", "duplicate.atlas-fixture.net"]),
                encoding="utf-8",
            )
            (sources / "veridrop-directory-2026-11-19.txt").write_text(
                "flat.atlas-fixture.net\nduplicate.atlas-fixture.net\n", encoding="utf-8"
            )
            self.write_reviews(
                sources / "directory-review-2026-11-19.jsonl",
                {
                    "domain": "duplicate.atlas-fixture.net",
                    "category": "旧记录",
                    "checked": "2026-11-19",
                },
                {
                    "domain": "flat-review.atlas-fixture.net",
                    "category": "旧记录",
                    "checked": "2026-11-19",
                },
            )
            self.write_reviews(sources / "daily-candidates.jsonl",
                               {"domain": "daily.atlas-fixture.net", "source_site": "fixture"})

            first = sources / "batches" / "2026-11-20"
            second = sources / "batches" / "2026-11-21"
            first.mkdir(parents=True)
            second.mkdir(parents=True)
            (first / "veridrop-directory-2026-11-20.txt").write_text(
                "nested.atlas-fixture.net\nduplicate.atlas-fixture.net\n",
                encoding="utf-8",
            )
            self.write_reviews(
                first / "directory-review-2026-11-20.jsonl",
                {
                    "domain": "duplicate.atlas-fixture.net",
                    "category": "中间记录",
                    "checked": "2026-11-20",
                },
            )
            (second / "veridrop-directory-2026-11-21.txt").write_text(
                "nested.atlas-fixture.net\nnew.atlas-fixture.net\n", encoding="utf-8"
            )
            self.write_reviews(
                second / "directory-review-2026-11-21.jsonl",
                {
                    "domain": "duplicate.atlas-fixture.net",
                    "category": "最新记录",
                    "checked": "2026-11-21",
                },
                {
                    "domain": "review-only.atlas-fixture.net",
                    "category": "中转站",
                    "checked": "2026-11-21",
                },
            )

            # The newer batch date is a fallback only when checked is absent.
            self.write_reviews(
                second / "directory-review-extra.jsonl",
                {"domain": "duplicate.atlas-fixture.net", "category": "旧资料", "checked": "2026-10-01"},
                {"domain": "flat-review.atlas-fixture.net", "category": "使用批次日期"},
            )
            # Only the documented names directly inside date-named folders are read.
            self.write_reviews(
                second / "directory-listings.jsonl",
                {"domain": "new.atlas-fixture.net", "source_site": "one.directory"},
                {"domain": "listing-only.atlas-fixture.net", "source_site": "one.directory"},
                {"domain": "listing-only.atlas-fixture.net", "source_site": "two.directory"},
            )
            self.write_reviews(second / "directory-listings-backup.jsonl", {"domain": "backup.atlas-fixture.net"})
            archive = second.parent / "archive"
            archive.mkdir()
            (archive / "veridrop-directory.txt").write_text("archive.atlas-fixture.net\n", encoding="utf-8")
            (second / "not-a-directory-file.txt").write_text(
                "ignored.atlas-fixture.net\n", encoding="utf-8"
            )
            ignored_dir = second / "subdir"
            ignored_dir.mkdir()
            self.write_reviews(
                ignored_dir / "directory-review-2026-11-22.jsonl",
                {
                    "domain": "deep.atlas-fixture.net",
                    "category": "不应读取",
                    "checked": "2026-11-22",
                },
            )

            output = root / "candidate-index.jsonl"
            result = subprocess.run(
                [
                    sys.executable,
                    str(INDEXER),
                    "--sources-dir",
                    str(sources),
                    "--out",
                    str(output),
                ],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            rows = [json.loads(line) for line in output.read_text(encoding="utf-8").splitlines()]
            by_domain = {row["domain"]: row for row in rows}

            self.assertEqual(
                set(by_domain),
                {
                    "legacy.atlas-fixture.net",
                    "duplicate.atlas-fixture.net",
                    "flat.atlas-fixture.net",
                    "nested.atlas-fixture.net",
                    "new.atlas-fixture.net",
                    "flat-review.atlas-fixture.net",
                    "review-only.atlas-fixture.net",
                    "listing-only.atlas-fixture.net",
                    "daily.atlas-fixture.net",
                },
            )
            self.assertEqual(len(rows), len(by_domain))
            daily = by_domain['daily.atlas-fixture.net']
            self.assertEqual(daily['sources'], ['daily-feed'])
            self.assertFalse(daily['validated'] or daily['in_relays'] or daily['page_category'])
            self.assertEqual(by_domain["new.atlas-fixture.net"]["sources"], ["directory", "veridrop"])
            listed = by_domain["listing-only.atlas-fixture.net"]
            self.assertEqual(listed["sources"], ["directory"])
            self.assertEqual(listed["page_category"], "")
            self.assertFalse(listed["validated"] or listed["in_relays"])
            self.assertEqual(by_domain["flat-review.atlas-fixture.net"]["page_category"], "使用批次日期")
            self.assertEqual(
                by_domain["duplicate.atlas-fixture.net"]["page_category"], "最新记录"
            )
            self.assertEqual(
                by_domain["duplicate.atlas-fixture.net"]["sources"],
                ["directory-review", "veridrop"],
            )
            self.assertEqual(
                by_domain["nested.atlas-fixture.net"]["sources"], ["veridrop"]
            )
            self.assertEqual(
                by_domain["review-only.atlas-fixture.net"]["sources"],
                ["directory-review"],
            )
            self.assertFalse(by_domain["review-only.atlas-fixture.net"]["validated"])
            self.assertFalse(by_domain["review-only.atlas-fixture.net"]["in_relays"])
            self.assertNotIn("ignored.atlas-fixture.net", by_domain)
            self.assertNotIn("deep.atlas-fixture.net", by_domain)

    @staticmethod
    def write_reviews(path, *records):
        path.write_text(
            "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records),
            encoding="utf-8",
        )


if __name__ == "__main__":
    unittest.main()
