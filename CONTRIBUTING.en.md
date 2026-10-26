# Contributing

Thank you for improving the public AI relay and virtual-goods directory.

## Relay submissions

Add a row to `data/relays/relays.csv` and model prices to `data/relays/relay-models.csv` only when the evidence is public and reproducible. Record the public endpoint in `source` and mark estimated or unaudited values in `notes`.

```text
domain,name,system_name,veridrop_score,category,source,status,n_models,has_gemini,has_mimo,has_grok,has_argon,last_checked,notes
```

## Shop submissions

Keep shops separate from relays. Add confirmed shops through the raw-source normalization flow; do not promote a homepage candidate automatically. Do not add purchase or payment URLs.

```text
shop,hosting,platform,system,system_type,domain,categories,price_range,source,last_checked,notes
```

Product-level data should cite an aggregator or public source page, not a direct checkout URL.

## Data and safety rules

- Use public information only.
- Keep requests low-concurrency and read-only.
- Do not log in, register, submit forms, call inference endpoints, brute-force, scan ports, or test vulnerabilities.
- Never commit API keys, cookies, passwords, IP addresses, ports, response bodies, redirect paths, query parameters, or purchase links.
- Preserve source provenance and distinguish candidates from confirmed records.

## Generated files

`README.md`, `README.en.md`, `data/stats.md`, `data/relays/by-model/`, and normalized shop tables are generated. After changing source data, run:

```bash
bash tools/build.sh
python3 tools/check_secrets.sh
```

中文说明见 [CONTRIBUTING.md](CONTRIBUTING.md)。
