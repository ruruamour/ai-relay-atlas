import csv
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


TOOLS = Path(__file__).resolve().parents[1] / "tools"
BASE = "gpt-4.1"
CHANNEL = "channel"
PRICE_QUERIES = (("group", CHANNEL), ("model", BASE))
CSV_FIELDS = {
    "relay-models.csv": (
        "domain", "model", "model_base", "billing", "input_usd_m",
        "output_usd_m", "call_usd", "group", "flag",
    ),
    "relays.csv": ("domain", "name", "topup_cny_per_usd"),
    "aliases.csv": ("alias", "canonical", "reason"),
}


def quote(domain, price, *, model=None, model_base=BASE, group=CHANNEL,
          billing="token", flag=""):
    return {
        "domain": domain,
        "model": model if model is not None else model_base,
        "model_base": model_base,
        "billing": billing,
        "input_usd_m" if billing == "token" else "call_usd": price,
        "group": group,
        "flag": flag,
    }


class QueryTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.data = self.root / "data" / "relays"
        self.data.mkdir(parents=True)
        tools = self.root / "tools"
        tools.mkdir()
        for name in ("query.py", "common.py"):
            shutil.copyfile(TOOLS / name, tools / name)
        for name in CSV_FIELDS:
            self.write_rows(name)

    def write_rows(self, name, *rows):
        with (self.data / name).open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, CSV_FIELDS[name])
            writer.writeheader()
            writer.writerows(rows)

    def run_query(self, *args):
        return subprocess.run(
            [sys.executable, "-X", "utf8", "tools/query.py", *args],
            cwd=self.root, capture_output=True, encoding="utf-8", timeout=10,
        )

    def query_output(self, *args):
        result = self.run_query(*args)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def ranked_domains(self, *args):
        fields = (line.split(maxsplit=1) for line in self.query_output(*args).splitlines())
        return [row[0] for row in fields if row and row[0].endswith(".invalid")]

    def test_group_matches_group_or_raw_model_case_insensitively(self):
        self.write_rows(
            "relay-models.csv",
            quote("group-match.invalid", 1, group="Plus CuRsOr Pool"),
            quote("raw-match.invalid", 2, model="[CURSOR] gpt-4.1"),
            quote("unrelated.invalid", 3),
        )
        both = ["group-match.invalid", "raw-match.invalid"]
        for options, expected in (
            ((), both),
            (("--field", "any"), both),
            (("--field", "group"), ["group-match.invalid"]),
            (("--field", "model"), ["raw-match.invalid"]),
        ):
            with self.subTest(options=options):
                self.assertCountEqual(self.ranked_domains("group", "cURsor", *options), expected)

    def test_group_model_filter_matches_base_or_raw_model(self):
        self.write_rows(
            "relay-models.csv",
            quote("base-match.invalid", 1, model="gpt_4.1"),
            quote("raw-match.invalid", 2, model="qwen3 [gPt-4 Preview]", model_base="qwen3"),
            quote("wrong-model.invalid", 3, model_base="qwen3"),
            quote("wrong-group.invalid", 4, group="retail"),
        )
        self.assertCountEqual(
            self.ranked_domains("group", CHANNEL, "--model", "GPT-4"),
            ["base-match.invalid", "raw-match.invalid"],
        )

    def test_billing_flags_are_strict(self):
        self.write_rows(
            "relay-models.csv",
            quote("flat.invalid", 1, model=f"[flat] {BASE}", billing="call"),
            quote("metered.invalid", 2, model=f"[metered] {BASE}"),
        )
        for mode, term in PRICE_QUERIES:
            for option, matching, other in (
                ("--call", "flat", "metered"),
                ("--token", "metered", "flat"),
            ):
                with self.subTest(mode=mode, option=option):
                    self.assertEqual(self.ranked_domains(mode, term, option), [f"{matching}.invalid"])
                    self.assertEqual(self.ranked_domains(mode, other, option), [])

    def test_billing_flags_are_mutually_exclusive(self):
        self.write_rows(
            "relay-models.csv",
            quote("flat.invalid", 1, billing="call"),
            quote("metered.invalid", 2),
        )
        for mode, term in PRICE_QUERIES:
            with self.subTest(mode=mode):
                result = self.run_query(mode, term, "--call", "--token")
                self.assertNotEqual(result.returncode, 0, result.stdout)
                self.assertNotIn("Traceback", result.stderr)

    def test_automatic_billing_uses_row_count_for_model_and_token_preference_for_group(self):
        self.write_rows(
            "relay-models.csv",
            quote("metered.invalid", 2),
            quote("flat.invalid", 1, group=f"{CHANNEL} flat", billing="call"),
            quote("flat.invalid", 0.5, group=f"{CHANNEL} flat", billing="call"),
        )
        self.assertEqual(self.ranked_domains("model", BASE), ["flat.invalid"])
        self.assertEqual(self.ranked_domains("group", CHANNEL), ["metered.invalid"])
        self.assertEqual(self.ranked_domains("group", "flat"), ["flat.invalid"])

    def test_group_all_prefers_token_in_mixed_billing(self):
        self.write_rows(
            "relay-models.csv",
            quote("flat.invalid", 0.1, billing="call"),
            quote("pay-per-use.invalid", 0.2, billing="call"),
            quote("shared.invalid", 0.3, billing="call"),
            quote("shared.invalid", 3),
            quote("metered.invalid", 2),
        )
        # Using the shared site's call price would move it ahead of the metered site.
        self.assertEqual(
            self.ranked_domains("group", CHANNEL, "--all"),
            ["metered.invalid", "shared.invalid"],
        )

    def test_all_keeps_flagged_and_zero_prices_but_not_invalid_prices(self):
        offers = (
            ("regular.invalid", 3, ""),
            ("high.invalid", 99, "high"),
            ("flagged.invalid", 2, "promo+low"),
            ("zero.invalid", 0, ""),
            ("empty.invalid", "", ""),
            ("nan.invalid", "nan", ""),
            ("infinite.invalid", "inf", ""),
            ("neg-infinite.invalid", "-inf", ""),
            ("negative.invalid", -1, ""),
        )
        for billing in ("token", "call"):
            self.write_rows("relay-models.csv", *(
                quote(domain, price, billing=billing, flag=flag)
                for domain, price, flag in offers
            ))
            for mode, term in PRICE_QUERIES:
                for options, expected in (
                    ((), ["regular.invalid", "high.invalid"]),
                    (("--all",), ["zero.invalid", "flagged.invalid", "regular.invalid", "high.invalid"]),
                ):
                    with self.subTest(billing=billing, mode=mode, options=options):
                        self.assertEqual(
                            self.ranked_domains(mode, term, f"--{billing}", *options), expected,
                        )

    def test_model_prefers_exact_base_over_earlier_fuzzy_matches(self):
        self.write_rows(
            "relay-models.csv",
            quote("fuzzy-base.invalid", 1, model="gpt_4.1-mini", model_base="gpt-4.1-mini"),
            quote("fuzzy-raw.invalid", 2, model="qwen3 [GPT-4.1]", model_base="qwen3"),
            quote("exact-base.invalid", 3, model="[Preferred] GPT_4.1-20250101"),
        )
        self.assertEqual(self.ranked_domains("model", "GPT-4.1"), ["exact-base.invalid"])

    def test_unpriced_exact_base_does_not_rank_a_different_model(self):
        self.write_rows(
            "relay-models.csv",
            quote("priced-variant.invalid", 2, model_base=f"{BASE}-mini"),
            quote("unpriced.invalid", "", billing=""),
        )
        self.assertEqual(self.ranked_domains("model", BASE), [])

    def test_model_falls_back_to_raw_substring(self):
        self.write_rows(
            "relay-models.csv",
            quote("raw-match.invalid", 2, model="[NiGhTlY] gpt-4.1"),
            quote("group-only.invalid", 1, group="nightly"),
        )
        self.assertEqual(self.ranked_domains("model", "nIgHtLy"), ["raw-match.invalid"])

    def test_model_ranks_each_site_by_its_cheapest_quote(self):
        self.write_rows(
            "relay-models.csv",
            quote("middle.invalid", 2),
            quote("later-cheapest.invalid", 5, group="premium"),
            quote("earlier-cheapest.invalid", 1.5),
            quote("later-cheapest.invalid", 1),
            quote("earlier-cheapest.invalid", 8, group="premium"),
        )
        self.assertEqual(
            self.ranked_domains("model", BASE),
            ["later-cheapest.invalid", "earlier-cheapest.invalid", "middle.invalid"],
        )

    def test_invalid_output_price_preserves_valid_input_price(self):
        self.write_rows("relay-models.csv", dict(quote("input-only.invalid", 1), output_usd_m="nan"))
        output = self.query_output("model", BASE)
        self.assertIn("input-only.invalid", output)
        self.assertNotIn("$nan", output.lower())

    def test_cny_ranks_by_price_times_valid_topup(self):
        offers = (
            ("cheap-nominal.invalid", 1, 10),
            ("cheap-topup.invalid", 12, 0.5),
            ("cheap-converted.invalid", 2, 2),
            ("missing-topup.invalid", 0.1, ""),
            ("bad-topup.invalid", 0.1, "unknown"),
            ("out-of-range.invalid", 0.1, 100),
            ("conversion-overflow.invalid", "1e308", 2),
        )
        self.write_rows("relay-models.csv", *(quote(domain, price) for domain, price, _ in offers))
        self.write_rows("relays.csv", *(
            dict(domain=domain, topup_cny_per_usd=topup) for domain, _, topup in offers
        ))
        for mode, term in PRICE_QUERIES:
            with self.subTest(mode=mode):
                self.assertEqual(
                    self.ranked_domains(mode, term, "--cny"),
                    ["cheap-converted.invalid", "cheap-topup.invalid", "cheap-nominal.invalid"],
                )

    def test_site_and_domain_look_up_canonical_relay_by_alias(self):
        canonical, alias = "canonical.invalid", "mirror.invalid"
        model = "gpt-4.1-20250101"
        self.write_rows("relay-models.csv", quote(canonical, 1, model=model))
        self.write_rows("relays.csv", dict(domain=canonical, name="Canonical Relay"))
        self.write_rows("aliases.csv", dict(alias=alias, canonical=canonical, reason="mirror"))
        for mode in ("site", "domain"):
            with self.subTest(mode=mode):
                output = self.query_output(mode, alias.upper() + ".")
                self.assertIn(canonical, output)
                self.assertIn("Canonical Relay", output)
                self.assertIn(model, output)


if __name__ == "__main__":
    unittest.main()
