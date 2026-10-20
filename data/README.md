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
| `split.txt` | 人工拆分名单：列出的域名永不合并 |
| `by-model/*.md` | 按基础模型的榜单（≥20 站提供的模型） |

### relays.csv
| 列 | 含义 |
|---|---|
| `domain` | 主域名 |
| `api_host` | 实际取价的主机（与主域名不同时才填） |
| `name` | 站名（网页标题） |
| `system` | `New-API` / `Sub2API`（价格公开）；`New-API/One-API`（有 `/api/status`，价格不公开）；空（自研或接口不可达） |
| `version` | 系统版本（站点公开的） |
| `topup_cny_per_usd` | 充值价：元 / 1 美元额度（站点公开且币种明确的才填，见 [pricing-basics](../docs/pricing-basics.md#实付价人民币)） |
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
| `reason` | `same-host`：同一主机加/去前缀（api./www.）；`mirror`：同品牌换后缀/子域，价格表相同或站名相同 |

合并保护：两边各有价格表（≥10 个模型）且模型集合重合度 <60% 时视为不同部署，不合并。
误合并可把域名写进 `split.txt`（人工拆分名单）后重建。

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

## 标注（annotations.csv）
人工判断写在 `data/relays/annotations.csv`，重建不会丢，会写进 `relays.csv` 的 `tags` / `notes`，
并在 README、模型榜单、监控报告里显示 ⚠️。

| 列 | 说明 |
|---|---|
| `domain` | 站点主域名 |
| `tag` | 标签，如 `掺水`、`疑似假模型`、`不稳定` |
| `note` | 证据（写成可核查的事实，别只写结论） |
| `source` | 来源：`用户反馈` / `实测` / 公开页面 |
| `date` | 标注日期 |

`掺水` 指：挂牌的是高价模型，实际路由到低价模型（表现为挂牌价远低于全网中位价、且同站没有对应渠道说明）。

## monitor/（监控）
| 文件 | 说明 |
|---|---|
| `targets.txt` | 监控名单（域名，一行一个） |
| `history.csv` | 每轮检查的历史：存活、延迟、是否在售、最低价、充值价、实测结果 |
| `report-<label>.md` | 最近一轮报告（含上架/下架/变价对比） |
| `drift.md` | 最近若干天的价格变动与掉线汇总 |
| `keys.txt` | **不入库**。真实可用性测试用的 `域名,sk-xxx` |

## 约定
- 价格单位：中转站 USD/1M token；发卡 ¥。
- `flag` 非空的行不参与榜单排名。
- `last_checked` 为该行最后核验日期。
- 所有价格为公开页推算，**未对账**。
