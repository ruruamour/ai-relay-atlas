# 原始抓取产物

<a id="sources"></a>

源文件记录报价、目录条目和早期专题快照。对外查询使用[中转站主表](../relays/relays.csv)和[店铺主表](../shops/shops.csv)。收录与核实记录见[来源批次索引](sources/README.md)。

## 当前店铺构建输入

| 文件 | 用途 |
|---|---|
| [google-card-offers.csv](google-card-offers.csv)、[google-ultra-offers.csv](google-ultra-offers.csv) | Google 会员报价 |
| [openprice-offers.json](openprice-offers.json)、[aihaotan-goods.json](aihaotan-goods.json) | 聚合站报价 |
| [shuita-shops.json](shuita-shops.json) | 水獭店铺目录 |
| [shop-fingerprints.json](shop-fingerprints.json) | 已有的店铺系统识别结果 |

[归一脚本](../../tools/normalize_shops.py)读取这些文件。更新方式见[数据字典](../README.md)。

## 历史专题与快照

| 文件 | 内容 | 抓取日 |
|---|---|---|
| `coverage.csv` | Veridrop 收录站覆盖情况（427 站） | 2026-09-24 |
| `gemini-stations.csv` | Gemini 站结构化提取（233 站） | 2026-09-24 |
| `gemini-prices-long.csv` | 站×Gemini 模型×价格（9194 行） | 2026-09-24 |
| `gemini-ranking.md` / `ALL-prices.md` / `BY-RATIO.md` | Gemini 排名与比价 | 2026-09-24/25 |
| `custom-rendered.csv/md` | 浏览器渲染解析的自建站 | 2026-09-25 |
| `mimo-family-*` | mimo 家族扫描（439 站） | 2026-10-02 |
| `mimo-both-pro.md` / `mimo-shortlist.md` | 2.5pro+2.6pro 双有站点 / 采购短名单 | 2026-10-05 |
| `grok-4.5-providers.csv/md` | grok-4.5 扫描（1150 站） | 2026-10-08 |
| `gemini-4-argon-providers.csv/md` | Gemini 4 Argon 扫描（551 站） | 2026-10-14 |
| `google-*-发卡行情.md` / `google-ultra-20x.md` | Google 会员发卡行情整理 | 2026-10-16 |
| `ultra20x-shops.json` | Ultra 20x 店铺映射 | 2026-10-16 |
| `ultra-and-vertex.md` | Ultra + Vertex/Aistudio 渠道 | 2026-10-16 |

> 价格为公开页面推算值，未对账。原始数据的授权见[数据许可](../../DATA-LICENSE.md)。历史快照的提取脚本见[旧工具归档](../../tools/legacy/README.md)。
