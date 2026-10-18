#!/usr/bin/env bash
# 重建所有派生文件：去重 → 店铺归一 → 模型榜单 → 统计 → README
set -euo pipefail
cd "$(dirname "$0")/.."
python3 tools/dedupe.py
python3 tools/normalize_shops.py
python3 tools/generate_by_model.py
python3 tools/build_stats.py
python3 tools/build_readme.py
