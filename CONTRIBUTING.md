# 贡献指南

[English](CONTRIBUTING.en.md) · [数据说明](data/README.md) · [报告中心](reports/README.md)

提交 Issue 或 PR 均可。请给出域名或店铺名、公开来源链接、核验日期（`YYYY-MM-DD`）和可复核的事实摘要。

## 提交中转站

先核对 [relays.csv](data/relays/relays.csv) 的 `domain` 和 `api_host`、[aliases.csv](data/relays/aliases.csv) 里的别名以及同品牌站点。[候选索引](data/raw/sources/candidate-index.jsonl)和第三方目录可提供线索。确认服务请引用服务方的公开说明或已公开的接口，仅能打开首页不等于确认它是中转站。

### 有公开报价

注明公开报价页或接口、原始模型名、分组、输入和输出价或按次价，以及单位。充值价只在币种和数值都明确时记录。报价是公开资料推算，不代表实付或对账结果。

对于脚本支持的接口，可用现有 `scan.py` 格式快照合入。例子使用已有的 `/tmp/scan.json` 和实际来源 `scan`。

```bash
python3 tools/merge.py /tmp/scan.json --via scan
```

有可合并报价时，合并会整站替换已有报价，不要拿局部报价当完整快照。之后构建中的 `dedupe.py` 会统一主域、别名、模型名和价格标记。目录复核 JSONL 和候选索引是证据，`merge.py` 不导入这些文件。只有报价页或不确定格式时，在 Issue 或 PR 里提供证据即可。

<a id="metadata-only"></a>
### 已核实但未采集报价

提交能说明站点确实提供中转服务的公开页面或文档，附发现来源、核验日期和简短事实。可参考 [2026-11-21 目录复核批次](data/raw/sources/batches/2026-11-21/README.md)及[来源注册表](data/raw/sources/README.md)。审核通过后，维护者可直接在 `relays.csv` 加一行按现有表头填写的站点元数据，然后构建。这条路径不需要先扫描或合并。

| 字段 | 填写方式 |
|---|---|
| `domain`、`name` | 核实过的主域名和公开站名 |
| `discovered_via`、`last_checked`、`notes` | 实际发现来源（如 `directory` 或 `browser`）、核验日期、服务摘要和「本次未采集报价」 |
| `n_models`、`aliases` | 独立新站均填 `0`，不在 `relay-models.csv` 新增报价行 |
| 其余字段 | 已核实才填 `api_host`、`system`、`version`、`topup_cny_per_usd` 或 `veridrop_score`。`http_status` 和 `latency_ms` 只填实测值，其余留空 |

`n_models=0` 指仓库暂无该站报价行。以后取得公开报价，再按报价流程补入。

<a id="提交发卡店铺"></a>
## 提交发卡店铺或商品

请提供店铺名、宿主域名和公开店铺或聚合页。提交具体商品时，附商品名称、类别、公开价格及币种和已知的在售状态。SaaS 平台或自建系统有依据再填。商品缺价时留空，不填 `0`。首页的系统或关键词命中还需对照商品和在售情况复核。

请指出[店铺归一支持的原始来源](data/README.md#shop-inputs)，或在 Issue 提交新来源供维护者评估。修正原始来源或归一规则后，`normalize_shops.py` 会重建 `data/shops/shops.csv` 和 `data/shops/products.csv`，不要直接改这两张表。`build.sh` 另用 `build_shop_review.py` 重建 `data/shops/candidates.csv`，审核通过的条目仍需通过受支持的来源入库。补充平台或软件名录可编辑 `platforms.csv` 或 `systems.csv`，不用于新增具体店铺。

## 纠错

写明受影响的表和站点、模型或商品，以及当前值、期望值和依据。

- 报价或倍率错误请更新有来源的快照或解析规则，再合并重建；店铺或商品错误请更新原始来源或归一规则。
- 人工标签和事实说明改 [annotations.csv](data/relays/annotations.csv)。误合并请写明两个域名，把需要独立的域名和原因加到 [split.txt](data/relays/split.txt) 后重建。漏合并请提交两个域名的对应证据供复核。
- 监控数据请注明观测时间和依据，保留旧记录。

<a id="不接受"></a>

提交只使用公开页面及已公开接口的只读信息。不附响应正文、账号凭据、Cookie、令牌、IP、端口、查询参数、个人联系方式、推广链接或购买支付链接。

<a id="关于-readme"></a>
## 构建与检查

从仓库根目录运行。构建环境见[工具说明](tools/README.md)。

```bash
bash tools/build.sh
python3 -m unittest discover -s tests
```

`build.sh` 重建规范化表、候选索引、店铺审核表、模型榜单、统计、报告和首页，检查本地链接与疑似密钥。核对生成差异是否符合预期。纯文档修订可单独运行 `python3 tools/check_links.py`。
