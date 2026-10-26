# Tools and update flow

The tools are intentionally manual and conservative. They use low-concurrency public GET requests and do not call model inference endpoints.

## Normal relay update

```bash
python3 tools/gen_candidates.py --resolve > /tmp/candidates.txt
python3 tools/scan.py /tmp/candidates.txt /tmp/scan.json
python3 tools/merge.py /tmp/scan.json --via scan
python3 tools/probe.py
bash tools/build.sh
```

Run `bash tools/check_secrets.sh` before every commit. Generated files include `README.md`, `data/stats.md`, `data/relays/by-model/`, and normalized shop tables.

## Discovery tools

| Tool | Purpose |
|---|---|
| `discover/github_harvest.py` | Public GitHub repository/README/list harvesting with checkpoints |
| `discover/github_code_harvest.py` | Public GitHub code-search text harvesting |
| `discover/gitlab_harvest.py` | Public GitLab project text harvesting |
| `discover/urlscan_harvest.py` | Passive urlscan public-index harvesting |
| `discover/directory_harvest.py` | Public relay-directory and comparison-page harvesting |
| `discover/crtsh.py` / `certspotter.py` | Passive certificate-transparency expansion |
| `discover/candidate_probe.py` | Homepage status/title/latency checks |
| `discover/shop_fingerprint.py` | Homepage-only shop/system candidate fingerprinting |
| `discover/index_candidates.py` | One-row-per-domain evidence index |
| `discover/build_shop_review.py` | Human-review CSV for shop candidates |

See [the Chinese discovery guide](discover/README.md) for the full source list and examples.

## Safety boundary

- Read public pages and documented public status/pricing/model-directory endpoints only.
- Do not log in, register, submit forms, test keys, call inference, brute-force, scan ports, or test vulnerabilities.
- Do not commit API keys, cookies, passwords, IP addresses, ports, response bodies, redirect paths, query parameters, or purchase links.
- Keep relay confirmation and shop candidates separate.
