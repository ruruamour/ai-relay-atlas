# 数据说明

## relays/（中转站）
| 文件 | 说明 |
|---|---|
| `relays.csv` | 站点主表，**一站一行**（别名已合并） |
| `aliases.csv` | 别名/镜像域名 → 主域名 |
| `relay-models.csv` | 站 × 模型 × 价格（核心长表） |
| `medians.json` | 各基础模型的正常价中位数（USD/1M 输入） |
| `summary.json` | 去重统计（README 用） |
| `relay-systems.csv` | 中转站软件名录（New-API/One-API/Sub2API…） |
| `by-model/*.md` | 按基础模型的榜单（≥20 站提供的模型） |

### relays.csv
| 列 | 含义 |
|---|---|
| `domain` | 主域名 |
| `api_host` | 实际取价的主机（与主域名不同时才填） |
| `name` | 站名（网页标题） |
| `system` | `New-API` / `Sub2API` / 空（自研或无公开价格接口） |
| `discovered_via` | 发现来源：`veridrop` / `github-list` / `scan`（前缀/后缀扩展扫描） |
| `veridrop_score` | Veridrop 实测分（有才填） |
| `n_models` | 模型数 |
| `families` | 覆盖的模型家族，如 `openai/claude/gemini` |
| `aliases` | 合并进来的别名数 |
| `backend_group` | 疑似同后端组（价格表与其他品牌完全相同），如 `B003`；每次重建编号可能变化 |
| `http_status` / `latency_ms` | 首页探活结果 |
| `notes` | 备注（如"泛解析，已去掉 N 个扫描生成的子域"） |

### aliases.csv
| 列 | 含义 |
|---|---|
| `reason` | `same-host`：同一主机加/去前缀（api./www.）；`mirror`：同品牌换后缀或子域且价格表相同 |

### relay-models.csv
| 列 | 含义 |
|---|---|
| `model` / `model_base` | 站上的原始模型名 / 归一后的基础模型名（去渠道标签、思考档位、日期） |
| `billing` | `token` 按量；`call` 按次 |
| `input_usd_m` / `output_usd_m` | 按量模型的推算价，USD / 1M token |
| `call_usd` | 按次模型的推算价，USD / 次 |
| `group` / `group_ratio` / `model_ratio` | 取价分组、分组倍率、模型倍率 |
| `source` | `newapi:/api/pricing`、`sub2api:/api/v1/model-plaza`、`browser-render`、`scan:model-list` |
| `flag` | 见下表，多个用 `+` 连接 |

| flag | 含义 |
|---|---|
| `promo` | 分组名含福利/特价/免费/限时/体验等 |
| `default` | `model_ratio=37.5`，New-API 未配置模型时的默认倍率（占位价，通常不是真实售价） |
| `zero` | 价格为 0 |
| `low` / `high` | 低于该模型中位价 5% / 高于 20 倍 |

## shops/（发卡/卡网）
| 文件 | 说明 |
|---|---|
| `platforms.csv` | **发卡平台**（SaaS，商家入驻）：链动小铺等 |
| `systems.csv` | **发卡系统**（开源软件，自建）：独角数卡/异次元发卡等 |
| `shops.csv` | 店铺主表，`hosting` 区分 SaaS / 自建 |
| `products.csv` | 店 × 商品 × 价格 × 来源 |

## 约定
- 价格单位：中转站 USD/1M token；发卡 ¥。
- `flag` 非空的行不参与榜单排名。
- `last_checked` 为该行最后核验日期。
- 所有价格为公开页推算，**未对账**。
