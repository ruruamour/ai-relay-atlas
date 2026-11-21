# 数据说明

[English](README.en.md) · [贡献指南](../CONTRIBUTING.md) · [报告中心](../reports/README.md)

## 数据文件与更新入口

| 文件 | 用途和来源 | 怎么更新 | 手改 |
|---|---|---|---|
| [relays.csv](relays/relays.csv) | 一站一行的中转站主表，同时是构建输入和输出 | `merge.py` 合入公开接口快照，维护者也可加入[已核实的无报价记录](../CONTRIBUTING.md#metadata-only)。`dedupe.py` 统一主域和统计，`probe.py` 可更新首页状态 | 仅限审核过的元数据 |
| [aliases.csv](relays/aliases.csv) | 别名或镜像域名到主域名的映射 | `dedupe.py` 综合现有映射、站名、域名、报价和拆分规则重建 | 否 |
| [relay-models.csv](relays/relay-models.csv) | 按站点和原始模型保存的参考报价 | `merge.py` 用完整报价快照替换该站报价，`dedupe.py` 归一模型名、计价和标记 | 否 |
| [annotations.csv](relays/annotations.csv) · [split.txt](relays/split.txt) | 人工标注和拆分规则 | 补充事实或拆分原因后重建，`dedupe.py` 读取两者 | 是 |
| [relay-systems.csv](relays/relay-systems.csv) | 中转软件参考目录 | 按项目公开资料维护，不参与站点识别 | 是 |
| [platforms.csv](shops/platforms.csv) · [systems.csv](shops/systems.csv) | SaaS 发卡平台和自建软件的参考目录 | 按平台或软件项目的公开资料维护，供 `build_reports.py` 展示 | 是 |
| [shops.csv](shops/shops.csv) · [products.csv](shops/products.csv) | 已收录店铺和商品，来自已支持的公开来源快照 | 更新[原始来源或归一规则](#shop-inputs)，由 `normalize_shops.py` 重建 | 否 |
| [candidates.csv](shops/candidates.csv) | 首页指纹候选的审核表 | `build.sh` 调用 `discover/build_shop_review.py` 汇总[首页指纹](raw/sources/shop-fingerprint-candidates.jsonl)、[浏览器复核摘要](raw/sources/shop-browser-review.jsonl)和中转站主域、别名 | 否 |
| [来源快照](raw/README.md) · [来源注册表](raw/sources/README.md) | 目录、探活、公开接口快照、人工复核摘要和历史产物 | 按原有来源流程保留日期和出处。各生成器只读取其支持的文件 | 按来源流程 |
| [candidate-index.jsonl](raw/sources/candidate-index.jsonl) | 一行一域名的来源和核验索引 | `build.sh` 调用 `discover/index_candidates.py` 汇总已有来源、探活、接口命中、主表和卡网指纹 | 否 |
| [wildcard-dns.json](raw/sources/wildcard-dns.json) · [summary.json](relays/summary.json) · [medians.json](relays/medians.json) | 泛解析缓存、去重摘要（含累计清理数）和价格中位数 | `dedupe.py` 使用已有缓存和旧摘要，缺缓存时会查询 DNS，并写出新摘要及中位数 | 否 |
| [suspicious.csv](relays/suspicious.csv) | 价格异常复核线索 | `detect_substitution.py` 单独生成，不会自动写入人工标注 | 否 |
| [targets.txt](monitor/targets.txt) · [history.csv](monitor/history.csv) | 监控名单和历轮观测 | 人工维护名单，`monitor.py run` 追加历史 | 仅改名单 |
| [报告中心](../reports/README.md) · [stats.md](stats.md) · [模型榜单](relays/by-model/index.md) | 供阅读的汇总和榜单 | `build_reports.py`、`build_stats.py`、`generate_by_model.py` 分别生成。首页中英文 README 也由构建生成 | 否 |
| [监控报告](monitor/report-argon.md) · [价格漂移](monitor/drift.md) | 最近一轮及历史变化摘要 | `monitor.py report` / `drift` 读取监控历史，独立于常规构建 | 否 |

<a id="relays中转站"></a>
## 中转站字段

### relays.csv

| 列 | 含义 |
|---|---|
| `domain` / `api_host` | 主域名和实际取价主机。取价主机不同且已核实时才填 `api_host` |
| `name` / `system` / `version` | 公开站名、可识别的系统和公开版本。常见系统为 `New-API`、`Sub2API`、`New-API/One-API`，无法确认则留空 |
| `topup_cny_per_usd` | 每 1 美元站内额度所需的人民币。币种或数值不明时留空，见[实付价](../docs/pricing-basics.md#实付价人民币) |
| `discovered_via` / `veridrop_score` | 发现来源和可用的 Veridrop 分数。`dedupe.py` 的 `RANK` 决定 `veridrop`、`github-list`、`scan`、`directory`、`browser` 等来源的优先级 |
| `n_models` / `families` | 仓库保留的报价行数和由报价归类出的模型家族。`n_models=0` 表示仓库没有该站的报价行，不表示站点不提供模型 |
| `aliases` / `backend_group` | 合并的别名数和疑似同后端组。组号来自跨品牌相同的模型名及输入、输出价，可能随构建变化，不意味着合并或同一运营方 |
| `http_status` / `latency_ms` | 首页访问的 HTTP 状态和耗时（毫秒），未测则留空 |
| `last_checked` | 最近一次入库核验或已记录观察的日期。具体报价日期看报价行 |
| `tags` / `notes` | 来自人工标注的标签，以及站点核验、标注或泛解析清理的备注 |

### aliases.csv

`alias` 是别名，`canonical` 是主域名，`discovered_via` 是别名的发现来源。`reason` 记录合并后的关系，`same-host` 指去掉通用前缀后同主机，`mirror` 指同品牌域名，`merged` 指其他合并。对已有别名、同名等带保护的合并规则，当两边各有至少 10 个模型且模型集合重合度低于 60%（Jaccard）时不合并。误合并请改 [split.txt](relays/split.txt) 并重建，每行一个应独立的域名，可用 `#` 写原因。

### relay-models.csv

| 列 | 含义 |
|---|---|
| `domain` | 对应主表的 `domain` |
| `model` / `model_base` | 原始模型名和归一后的基础模型名。归一会去掉部分渠道标签、思考档位和日期等后缀 |
| `billing` | `token` 按量，`call` 按次 |
| `input_usd_m` / `output_usd_m` / `call_usd` | 按量的输入、输出价（USD / 百万 token）或按次价（USD / 次）。不适用或缺失的价格留空 |
| `group` / `group_ratio` / `model_ratio` | 取价分组及分组倍率、模型倍率 |
| `source` | 常见为 `newapi:/api/pricing` 和 `sub2api:/api/v1/model-plaza`。现有数据也保留 `browser-render` 和 `scan:model-list` |
| `flag` / `last_checked` | 报价标记和快照日期。多个标记用 `+` 连接 |

| 标记 | 含义 |
|---|---|
| `promo` | 福利、特惠、体验等分组 |
| `default` | New-API 按量模型的 `model_ratio=37.5` 被判为占位价 |
| `zero` | 用于排名的价格为零或负数 |
| `low` / `high` | 用于排名的价格低于该模型对应计价中位数的 5%，或高于 20 倍 |

<a id="标注annotationscsv"></a>
### 标注（annotations.csv）

`domain,tag,note,source,date` 分别是主域名、标签、事实摘要、来源和日期（`YYYY-MM-DD`）。`dedupe.py` 将标签和备注合入主表，报告和榜单用警示符号提示。`掺水` 指挂牌模型被替换为更低价的模型。异常低价仅是线索，证据不足时注明是反馈或待复核。

<a id="shops发卡卡网"></a>
## 发卡店铺字段

`platforms.csv` 使用 `platform,type,domain,note`，多个平台宿主以分号分隔。`systems.csv` 和中转软件目录 `relay-systems.csv` 使用 `system,type,repo,note`。

| 文件 | 表头 |
|---|---|
| [shops.csv](shops/shops.csv) | `shop,hosting,platform,system,system_type,domain,categories,price_range,source,last_checked,notes` |
| [products.csv](shops/products.csv) | `shop,host,hosting,platform,system,category,item,price_cny,status,warranty,stock,source,source_url,last_checked` |
| [candidates.csv](shops/candidates.csv) | `domain,status,likelihood,title,systems,common_hits,ai_hits,relay_overlap,last_checked,browser_review,rendered_title,notes` |

`hosting` 分 `SaaS` 和 `自建`。店铺的 `domain` 可含多个宿主，`price_range` 汇总已知商品的人民币标价。商品的 `source_url` 来自上游记录，新增证据请用公开资料页。`last_checked` 目前是归一脚本的批次日期。候选表的 `likelihood` 是首页指纹置信度，`relay_overlap` 表示命中中转站主域或别名。`browser_review` 即使确认首页有商品内容，也还要核对品类和在售状态。

<a id="shop-inputs"></a>
### 店铺归一输入

`normalize_shops.py` 读取 `data/raw/` 下的 `google-card-offers.csv`、`google-ultra-offers.csv`、`openprice-offers.json`、`aihaotan-goods.json` 和 `shuita-shops.json`。平台和系统归属由脚本的宿主映射以及 `shop-fingerprints.json` 判定。参考目录和候选审核表都不参与归一。已人工复核的候选还需来自受支持的来源，才会出现在店铺和商品表中。更多来源信息见[店铺来源说明](shops/sources.md)。

<a id="evidence"></a>
## 来源证据

[来源注册表](raw/sources/README.md) 和 [2026-11-21 目录复核批次](raw/sources/batches/2026-11-21/README.md) 链接到原始域名清单和逐站记录。目录复核记录保存域名、核验日期、公开目录和服务方说明页、事实摘要，以及实际测得的首页状态码（如有）。`merge.py` 读取命令行指定的 `scan.py` 格式 JSON，目录复核记录供人工审核。候选索引的 `validated` 表示有探活记录或该域名在主表中，收录情况看 `in_relays`，页面判定看 `page_category`。

<a id="monitor监控"></a>
## 监控数据

监控名单每行一个域名。历史中的 `ts` 是观测时间，`http_status` 和 `latency_ms` 来自公开状态接口。`has_model` 表示目标模型是否出现在当轮公开价格记录中，`groups`、`min_usd_m` 和 `min_call_usd` 记录相关分组和最低报价。纠错请注明轮次及依据，不覆盖旧观测。`monitor/keys.txt` 仅限本地且已被 Git 忽略。

## 约定

- 价格是公开资料推算，未对账。实付估算为名义价乘以站点公开的充值价。缺价留空，不用 `0` 代替。
- 默认价格排名排除 `promo`、`zero`、`default`、`low` 和缺价。仅带 `high` 的报价仍可参与排名。模型榜单要求至少 20 个站有该模型记录，且有可排名的报价。
- `query.py` 只读本地 CSV。查询选项见[离线查价](../tools/README.md#离线查价)。

[数据许可](../DATA-LICENSE.md) · [免责声明](../DISCLAIMER.md)
