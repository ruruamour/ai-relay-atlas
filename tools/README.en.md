# Tools and update flow

[Project home](../README.en.md) · [Data dictionary](../data/README.en.md) · [简体中文](README.md)

Use Python 3.10 or newer. A complete build requires `tldextract`. Offline queries use the standard library.

## Offline price queries

Run `query.py` from the repository root. It reads local CSV files and requires no network access or extra dependencies.

```bash
python3 tools/query.py model gemini-4-argon --token --cny --n 10
python3 tools/query.py group cursor --field any --model claude --call
```

- `model` first looks for an exact match in the stored base-model names, then checks the base and raw names for a substring. It defaults to the billing unit with the most matching rows.
- `group` searches the stored reference quotes for a channel. By default it matches a substring in the group or raw model name. Use `--field group` or `--field model` to select one field. Use `--model` to filter the matches by base or raw model name.
- Both commands rank one billing unit at a time. Choose `--token` for prices per million input tokens or `--call` for prices per call. `group` defaults to token billing if any token rows match and call billing when only call rows match.
- By default, rankings exclude `promo`, `default`, `low`, and zero prices. Quotes flagged `high` remain eligible. `--all` includes flagged and zero prices within the selected billing unit.
- Each site contributes its lowest eligible quote. `--cny` keeps only sites with a valid disclosed top-up rate and ranks by nominal price × rate. `--n` limits the output to 30 rows by default.

Run `python3 -m unittest discover -s tests` for local regression checks with the Python standard library.

<a id="normal-relay-update"></a>

## Rebuild the snapshot

Run these commands from the repository root.

```bash
python3 -m pip install tldextract
bash tools/build.sh
python3 -m unittest discover -s tests
```

The build normalizes relay and shop data, refreshes the candidate index and shop review table, renders rankings, reports, and both homepages, then checks Markdown links and potential secrets.

For new listings and data corrections, see the [contribution guide](../CONTRIBUTING.en.md) and [source batches](../data/raw/sources/README.md).

<a id="discovery-tools"></a>

## Tool index

| Task | Tools |
|---|---|
| Query sites and prices | [query.py](query.py) |
| Rebuild and check the snapshot | [build.sh](build.sh), [check_links.py](check_links.py), [check_secrets.sh](check_secrets.sh) |
| Generate reports and homepages | [build_reports.py](build_reports.py), [build_readme.py](build_readme.py), [build_readme_en.py](build_readme_en.py) |
| Normalize site and shop data | [merge.py](merge.py), [dedupe.py](dedupe.py), [normalize_shops.py](normalize_shops.py) |
| Rebuild candidate views | [index_candidates.py](discover/index_candidates.py), [build_shop_review.py](discover/build_shop_review.py) |
| Monitor and report possible pricing anomalies | [monitor.py](monitor.py), [detect_substitution.py](detect_substitution.py) |
| Collect public-source evidence | [Discovery tools](discover/README.md) |
| Trace historical snapshots | [Archived tools](legacy/README.md) |

## Safety boundary

- Read public pages and documented public status/pricing/model-directory endpoints only.
- Do not log in, register, submit forms, test keys, call inference, brute-force, scan ports, or test vulnerabilities.
- Do not commit API keys, cookies, passwords, IP addresses, ports, response bodies, redirect paths, query parameters, or purchase links.
- Keep relay confirmation and shop candidates separate.
