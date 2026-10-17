# 数据说明

## relays/（中转站）
| 文件 | 说明 |
|---|---|
| `relays.csv` | 站级主表：域名、Veridrop 评分、是否有 gemini/mimo/grok/argon、`http_status`、`latency_ms` |
| `relay-models.csv` | 站 × 模型 × 价格（核心），价格为**推算实际价** USD/1M |
| `relay-systems.csv` | 中转站软件名录（New-API/One-API/Sub2API…） |
| `by-model/*.md` | 按模型的可读榜单（143 个模型） |

## shops/（发卡/卡网）
| 文件 | 说明 |
|---|---|
| `platforms.csv` | **发卡平台**（SaaS，商家入驻）：链动小铺等 |
| `systems.csv` | **发卡系统**（开源软件，自建）：独角数卡/异次元发卡等 |
| `shops.csv` | 店铺主表，`hosting` 区分 SaaS / 自建 |
| `products.csv` | 店 × 商品 × 价格 × 来源 |

## 约定
- 价格单位：中转站 USD/1M token；发卡 ¥。
- `promo=yes` 表示福利/特价/免费组，不是默认价。
- `last_checked` 为该行最后核验日期。
- 所有价格为公开页推算，**未对账**。
