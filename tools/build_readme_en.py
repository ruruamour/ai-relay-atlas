#!/usr/bin/env python3
"""Generate the concise English README from the same data used by README.md."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_stats import compute  # noqa: E402


def main():
    s = compute()
    m, relays, shops, products = s['summ'], s['rl'], s['sh'], s['pr']
    lines = [
        '# ai-relay-atlas · AI Relay and Virtual-Goods Directory',
        '',
        '[简体中文](README.md) · **English**',
        '',
        '[![License: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE) '
        '[![Data: CC BY-NC 4.0](https://img.shields.io/badge/data-CC%20BY--NC%204.0-lightgrey.svg)](DATA-LICENSE.md)',
        '',
        'A public-information map of AI API relay services, model prices, and AI-related virtual-goods shops.',
        'The project is optimized for broad discovery first; prices are public-page estimates and are not audited.',
        '',
        '> **Safety and scope:** read-only public GET requests only. No login, registration, credential testing, inference requests, brute force, vulnerability testing, API keys, cookies, IPs, ports, response bodies, or purchase links are stored.',
        '',
        '## Snapshot',
        '',
        '| Metric | Count |',
        '|---|---:|',
        f'| Relay sites | {m["sites"]} ({s["up"]} homepage HTTP 200) |',
        f'| Relay aliases / mirrors | {m["aliases"]} |',
        f'| Site × model price rows | {m["model_rows"]} |',
        f'| Normalized model bases | {m["model_bases"]} |',
        f'| Virtual-goods shops | {len(shops)} |',
        f'| Shop product quotes | {len(products)} |',
        '',
        'See the generated [distribution report](data/stats.md) and the [candidate review table](data/shops/candidates.csv).',
        '',
        '## Quick start',
        '',
        '```bash',
        'git clone https://github.com/ruruamour/ai-relay-atlas.git',
        'cd ai-relay-atlas',
        'python3 tools/query.py model gemini-4-argon',
        'python3 tools/query.py site api.openlux.ai',
        'bash tools/build.sh',
        '```',
        '',
        '`README.md` and generated reports are built from `data/`; do not edit generated files directly.',
        '',
        '## Repository layout',
        '',
        '| Path | Purpose |',
        '|---|---|',
        '| `data/relays/relays.csv` | One row per canonical relay site |',
        '| `data/relays/relay-models.csv` | Site × model × public price data |',
        '| `data/relays/by-model/` | Model coverage pages |',
        '| `data/shops/shops.csv` | Confirmed shop directory |',
        '| `data/shops/candidates.csv` | Separate shop-candidate review list |',
        '| `data/raw/sources/` | Source, probe, and scan evidence |',
        '| `tools/discover/` | Public-source discovery and validation tools |',
        '',
        '## Discovery and validation',
        '',
        'Sources include Veridrop, GitHub, GitLab, certificate transparency logs, urlscan, npm, Docker Hub, Hugging Face, Sourcegraph, public search, and public relay directories.',
        'Candidates are kept separate from confirmed relays and shops. Homepage probes retain status/title/latency; interface scans only use publicly documented status, pricing, and model-directory endpoints.',
        '',
        'The source manifest is [data/raw/sources/README.md](data/raw/sources/README.md).',
        '',
        '## Documentation',
        '',
        '- [Documentation index](docs/README.en.md)',
        '- [Chinese documentation index](docs/README.md)',
        '- [Internet measurement and discovery](docs/internet-measurement.md)',
        '- [Finding self-hosted shops](docs/find-faka-shops.md)',
        '- [Pricing basics](docs/pricing-basics.md)',
        '- [Glossary](docs/glossary.md)',
        '- [Tools and update flow](tools/README.en.md)',
        '',
        '## License and contribution',
        '',
        '- Code: [MIT](LICENSE)',
        '- Curation and derived data: [CC BY-NC 4.0](DATA-LICENSE.md)',
        '- [English contribution guide](CONTRIBUTING.en.md) · [中文贡献指南](CONTRIBUTING.md)',
        '- [Disclaimer](DISCLAIMER.en.md)',
        '',
        'Original price and product data remain subject to the terms and rights of their respective sources.',
    ]
    with open('README.en.md', 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(lines) + '\n')
    print('README.en lines', len(lines))


if __name__ == '__main__':
    main()
