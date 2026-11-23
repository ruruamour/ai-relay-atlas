import json
import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools" / "discover"))
import daily_lists  # noqa: E402


class DailyListParserTests(unittest.TestCase):
    def make_document(self, *rows):
        return json.dumps({"schemaVersion": 1, "sites": list(rows)})

    def test_registered_source_uses_verified_raw_file_for_both_fields(self):
        self.assertEqual(
            set(daily_lists.LIST_SOURCES), {"1sh1ro/ai-api-zhongzhuan"}
        )
        source_url, parser = daily_lists.LIST_SOURCES["1sh1ro/ai-api-zhongzhuan"]
        self.assertEqual(source_url, daily_lists.ZHONGZHUAN_RAW_URL)
        rows = parser(
            self.make_document(
                {
                    "homepage": "https://Relay-One.AI/",
                    "registrationUrl": "https://Relay-One.AI/register?aff=ignored",
                    "tags": ["gpt", "api-relay"],
                }
            )
        )
        self.assertEqual(rows, [("relay-one.ai", daily_lists.ZHONGZHUAN_RAW_URL)])
        self.assertTrue(source_url.startswith("https://raw.githubusercontent.com/"))
        self.assertNotIn("?", source_url)

    def test_accepts_explicit_gateway_and_relay_rows_in_source_order(self):
        rows = daily_lists.parse_zhongzhuan_sites(
            self.make_document(
                {
                    "id": "gateway",
                    "homepage": "https://gateway-service.dev/",
                    "tags": ["api-gateway", "gpt"],
                },
                {
                    "id": "new-api",
                    "homepage": "https://new-api-relay.cn/zh",
                    "tags": ["public-benefit", "new-api", "api-relay"],
                },
            )
        )
        self.assertEqual(
            rows,
            [
                ("gateway-service.dev", daily_lists.ZHONGZHUAN_RAW_URL),
                ("new-api-relay.cn", daily_lists.ZHONGZHUAN_RAW_URL),
            ],
        )

    def test_uses_homepage_only_and_rejects_nonrelay_or_non_direct_rows(self):
        rows = daily_lists.parse_zhongzhuan_sites(
            self.make_document(
                {
                    "homepage": "https://homepage-only.ai/",
                    "registrationUrl": "https://wrong-site.ai/register?aff=tracking",
                    "sources": [{"type": "official-website", "url": "https://source.ai/"}],
                    "tags": ["api-relay"],
                },
                {
                    "homepage": "https://vendor.ai/",
                    "tags": ["api-relay", "vendor"],
                },
                {
                    "homepage": "https://community.ai/",
                    "tags": ["api-relay", "community"],
                },
                {
                    "homepage": "https://model-directory.ai/",
                    "tags": ["gpt", "claude"],
                },
                {
                    "homepage": "https://tracked.ai/?aff=redirect",
                    "tags": ["api-relay"],
                },
                {
                    "registrationUrl": "https://registration-only.ai/",
                    "tags": ["api-relay"],
                },
            )
        )
        self.assertEqual(
            rows,
            [("homepage-only.ai", daily_lists.ZHONGZHUAN_RAW_URL)],
        )

    def test_rejects_http_ip_placeholder_markdown_and_invalid_hosts(self):
        rows = daily_lists.parse_zhongzhuan_sites(
            self.make_document(
                {"homepage": "http://plain-http.ai/", "tags": ["api-relay"]},
                {"homepage": "https://192.0.2.10/", "tags": ["api-relay"]},
                {"homepage": "https://example.com/", "tags": ["api-relay"]},
                {
                    "homepage": "![relay](https://markdown.ai/logo.png)",
                    "tags": ["api-relay"],
                },
                {"homepage": "https://bad_host.ai/", "tags": ["api-relay"]},
                {"homepage": "https://user:pass@private.ai/", "tags": ["api-relay"]},
                {"homepage": "https://promo.ai/invite/123", "tags": ["api-relay"]},
                {"homepage": "https://software.ai/", "tags": ["new-api"]},
            )
        )
        self.assertEqual(rows, [])

    def test_malformed_and_drifted_documents_fail_closed(self):
        fixtures = (
            "",
            "{",
            "[]",
            json.dumps({"sites": {"homepage": "https://wrong.ai/"}}),
            self.make_document({"homepage": "https://wrong.ai/", "tags": "api-relay"}),
            self.make_document("not a row", None),
        )
        for fixture in fixtures:
            with self.subTest(fixture=fixture):
                self.assertEqual(daily_lists.parse_zhongzhuan_sites(fixture), [])

    def test_affiliate_registration_feed_is_explicitly_omitted(self):
        source = "bubblevv/ai-api-gongyi-nav"
        self.assertNotIn(source, daily_lists.LIST_SOURCES)
        raw_url, reason = daily_lists.OMITTED_SOURCES[source]
        self.assertEqual(raw_url, daily_lists.GONGYI_RAW_URL)
        self.assertIn("registration links", reason)
        self.assertIn("affiliate", reason)
        self.assertTrue(raw_url.startswith("https://raw.githubusercontent.com/"))
        self.assertNotIn("?", raw_url)


if __name__ == "__main__":
    unittest.main()
