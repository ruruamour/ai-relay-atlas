# Contributing

[中文贡献指南](CONTRIBUTING.md) · [Data reference](data/README.en.md) · [Report hub](reports/README.md)

Open an issue or PR with the hostname or shop name, stable public source links, the check date (`YYYY-MM-DD`), and a short factual summary. The [data reference](data/README.en.md) lists schemas and update paths.

<a id="relay-submissions"></a>
## Submit a relay

Check `domain` and `api_host` in [relays.csv](data/relays/relays.csv), [aliases.csv](data/relays/aliases.csv), and same-brand entries first. The [candidate index](data/raw/sources/candidate-index.jsonl) and third-party directories provide leads. To confirm the service, cite a public provider page or a documented public interface. A reachable homepage alone is not confirmation.

### Public quotes

Include the public pricing page or endpoint, raw model name, group, input and output prices or per-call price, and the units. Include a top-up rate only when the currency and amount are clear. Treat the quote as an estimate, not an audited charge.

For supported interfaces, merge an existing `scan.py` snapshot. This example uses `/tmp/scan.json` and the `scan` discovery label.

```bash
python3 tools/merge.py /tmp/scan.json --via scan
```

A nonempty quote snapshot replaces that site's stored rows, so don't merge a partial list as a full snapshot. The build then uses `dedupe.py` to normalize canonical domains, aliases, model names, and flags. `merge.py` does not import directory-review JSONL or the candidate index. For a public pricing page without a supported snapshot, submit the evidence in an issue or PR for review.

<a id="metadata-only"></a>
### Reviewed relays without collected quotes

Submit a public first-party page or document showing that the site provides relay service, with the discovery source, check date, and a short factual summary. See the [2026-11-21 directory review](data/raw/sources/batches/2026-11-21/README.md) and the [source registry](data/raw/sources/README.md). Once the evidence is accepted, maintainers can add one metadata row to `relays.csv` using the existing header and rebuild. This route does not require a scan or merge.

| Fields | What to enter |
|---|---|
| `domain`, `name` | Verified canonical hostname and public site name |
| `discovered_via`, `last_checked`, `notes` | Actual discovery route (for example `directory` or `browser`), check date, and a short summary that says no quote was collected |
| `n_models`, `aliases` | Both are `0` for a new standalone site. Add no quote row to `relay-models.csv` |
| Other fields | Fill `api_host`, `system`, `version`, `topup_cny_per_usd`, or `veridrop_score` if verified. Fill `http_status` and `latency_ms` only if observed. Leave the rest blank |

`n_models=0` means the atlas has no quote rows for that site. Add public quotes later through the quote workflow.

<a id="shop-submissions"></a>
## Submit a shop or product

Include the shop name, hostname, and a public shop or aggregator page. For an individual product, include the title, category, published price and currency, and known availability. Include the SaaS platform or self-hosted system when verified. Leave an unknown price blank rather than using `0`. Check homepage fingerprint leads against actual product listings and availability.

Identify the [supported raw source](data/README.en.md#shop-inputs), or open an issue for maintainers to review a new source. Update the raw source or the normalization rule. `normalize_shops.py` rebuilds `data/shops/shops.csv` and `data/shops/products.csv`, so do not edit those tables directly. `build.sh` also runs `build_shop_review.py` to refresh `data/shops/candidates.csv`. Reviewed candidates enter shop data through a supported source. Edit `platforms.csv` or `systems.csv` for reference catalog changes, not to add an individual shop.

## Report a correction

Name the affected table and site, model, or product. Give the current value, the expected value, and the evidence.

- For incorrect quotes or multipliers, update the supporting snapshot or parser and rebuild after merging. For incorrect shop or product data, update the raw source or the normalization rule.
- Put manual tags and factual notes in [annotations.csv](data/relays/annotations.csv). For an incorrect merge, name both hosts and add the hostname that must stay separate, with a reason, to [split.txt](data/relays/split.txt) before rebuilding. For a missed merge, submit evidence linking both hostnames.
- For monitoring corrections, report the observation timestamp and evidence. Retain the original history.

<a id="data-and-safety-rules"></a>

Use read-only information from public pages and documented public interfaces. Leave out response bodies, credentials, cookies, tokens, IPs, ports, query parameters, personal contact details, referral links, and checkout or payment links.

<a id="generated-files"></a>
## Build and check

Run from the repository root. Build prerequisites are in the [tools guide](tools/README.en.md).

```bash
bash tools/build.sh
python3 -m unittest discover -s tests
```

The build refreshes normalized tables, the candidate index and shop review CSV, model pages, statistics, reports, and root READMEs. It checks local links and potential secrets. Review the generated diff for unexpected changes. For a docs-only change, `python3 tools/check_links.py` can check links on its own.
