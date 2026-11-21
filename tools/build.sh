#!/usr/bin/env bash
# 重建公开数据、候选索引与浏览报告，校验发布文件。
set -euo pipefail
cd "$(dirname "$0")/.."
python3 tools/dedupe.py
python3 tools/normalize_shops.py
python3 tools/discover/index_candidates.py
python3 tools/discover/build_shop_review.py
python3 tools/generate_by_model.py
python3 tools/build_stats.py
python3 tools/build_reports.py
python3 tools/build_readme.py
python3 tools/build_readme_en.py
python3 tools/check_links.py
bash tools/check_secrets.sh
