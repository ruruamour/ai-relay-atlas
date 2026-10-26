# Data reference

[中文说明](README.md)

## Relay data

| File | Meaning |
|---|---|
| `relays/relays.csv` | Canonical relay-site table, one row per site |
| `relays/aliases.csv` | Alias or mirror hostname → canonical site |
| `relays/relay-models.csv` | Site × model × public price rows |
| `relays/medians.json` | Model price medians used for comparison |
| `relays/by-model/` | Model coverage pages |
| `relays/suspicious.csv` | Automated price-anomaly candidates; not a final accusation |

Prices are public-page estimates. `discovered_via` records the public discovery source; `status` and `last_checked` describe the latest homepage validation.

## Shop data

| File | Meaning |
|---|---|
| `shops/shops.csv` | Confirmed shop directory; SaaS and self-hosted shops are separate |
| `shops/products.csv` | Shop × product × price records from public sources |
| `shops/candidates.csv` | Homepage-fingerprint candidates for manual review; not confirmed shops |
| `shops/sources.md` | Shop-source coverage and limitations |

## Source evidence

`raw/sources/` contains source metadata, probe results, documented public-interface scans, and candidate indexes. It does not contain credentials, cookies, response bodies, IPs, ports, redirect paths, query parameters, or purchase links.

See [the source manifest](raw/sources/README.md), [the data license](../DATA-LICENSE.en.md), and [the disclaimer](../DISCLAIMER.en.md).
