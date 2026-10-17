# 抓取脚本（手动运行）

这些脚本用于**手动**发现与抓取公开数据，不接 CI。运行前请自行确认目标站条款。

## 中转站
- `scan_argon.py` / `scan_grok.py` — 批量探测站点是否含某模型
- `extract_argon.py` / `extract_grok.py` — 从 `/api/pricing`、`/api/v1/model-plaza` 提取价格
- `scan_prefix.py` — 子域名扩展发现更多站
- `rebuild.py` — 重建域名清单
- `agg.py` — 汇总

## 归一化
- `normalize.py` — 生成 `data/relays/*.csv`
- `normalize_shops.py` — 生成 `data/shops/*.csv`
- `generate_by_model.py` — 生成 `data/relays/by-model/*.md`

## 说明
脚本内的域名清单、路径为一次性抓取时所用；换环境需自行调整。价格为推算值，未对账。
