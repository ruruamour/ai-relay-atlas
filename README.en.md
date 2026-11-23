# ai-relay-atlas · AI Relay and Virtual-Goods Directory

[简体中文](README.md) · **English**

Find AI API relays, compare model prices, and check shops and their listings against the sources. Prices come from public pages and APIs and have not been checked against invoices.

<a id="toc"></a><a id="tasks"></a>
## Start here

| What do you want to do? | Where to look |
|---|---|
| <a id="relays"></a>Find a relay or mirror domain | [Relay table](data/relays/relays.csv) · [Alias lookup](data/relays/aliases.csv) · [Top 100 relay table](reports/relays.md#top-100-sites) |
| <a id="coverage"></a>Compare prices for one model | [Model price index](data/relays/by-model/index.md) · [All quotes (CSV)](data/relays/relay-models.csv) · [Pricing methodology](docs/pricing-basics.md) |
| <a id="shops"></a>Look up a shop or product | [Listed shops](data/shops/shops.csv) · [Products and prices](data/shops/products.csv) · [Shop overview](reports/shops.md) |
| <a id="sources"></a><a id="discovery-and-validation"></a>Check why a site was listed | [Sources and dated reviews](data/raw/sources/README.md) · [Domain evidence index](data/raw/sources/candidate-index.jsonl) |
| <a id="contributing"></a>Suggest a listing or correction | [Contribution guide](CONTRIBUTING.en.md) · [Which files to edit](data/README.en.md) |

## Snapshot

- The relay table lists **5,165 sites**, with 4,328 additional aliases and **271,412 price records**. `n_models=0` means the atlas has no quotes for that site.
- The evidence index covers 29,264 domains, including sites already listed. A third-party directory entry needs verification before it can become a relay listing.
- The shop table lists 430 shops and 17,212 product price records. Another 191 [shop candidates](data/shops/candidates.csv) are in a separate review queue.

## Quick start

Run these commands from the repository root. They read local CSV files and need neither network access nor a build step.

```bash
python3 tools/query.py site api.openlux.ai --n 10
python3 tools/query.py model gemini-4-argon --token --cny --n 10
python3 tools/query.py group cursor --field any --model claude --call --n 10
```

Use `--token` to compare prices per million input tokens or `--call` for per-call prices. `--cny` estimates costs using each site's disclosed top-up rate. See the [offline query guide](tools/README.en.md#offline-price-queries) for more options.

<a id="reports"></a><a id="files"></a><a id="docs"></a><a id="repository-layout"></a><a id="documentation"></a>
## Reports and data

- <a id="backend"></a><a id="shop-platforms"></a>The [report hub](reports/README.md) links to [model-family coverage](reports/relays.md#family-coverage), [possible shared backends](reports/relays.md#suspected-backends), and [shop platforms and software](reports/shops.md#platforms-and-systems).
- [Statistics](data/stats.md) summarize coverage and prices. The [955 model rankings](data/relays/by-model/index.md) show prices by site.
- The [documentation index](docs/README.en.md) separates using the data from maintaining it. After updating inputs, rebuild from the repository root with `bash tools/build.sh`.

<a id="license"></a><a id="safety"></a><a id="license-and-contribution"></a>
## Scope and licensing

Listings are based on public information. Inclusion does not guarantee availability and the atlas does not provide purchase links. See the [disclaimer](DISCLAIMER.en.md), [code license (MIT)](LICENSE), and [curated data license (CC BY-NC 4.0)](DATA-LICENSE.en.md).
