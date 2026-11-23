# tools/ · 脚本

[项目首页](../README.md) · [数据字典](../data/README.md) · [English](README.en.md)

使用 Python 3.10 或更新版本。完整重建需要 `tldextract`，离线查询使用标准库。

## 离线查价

在仓库根目录运行。`query.py` 读取本地 CSV，无需联网或安装额外依赖。

```bash
python3 tools/query.py model gemini-4-argon --token --cny --n 10
python3 tools/query.py group cursor --field any --model claude --call
```

- `model` 优先精确匹配表中的基础模型名，找不到时才在基础模型名和原始模型名中查找子串。默认展示匹配行数最多的计价方式。
- `group` 在已收录的参考报价中查渠道。默认在分组名和原始模型名中查找关键词。可用 `--field group` 或 `--field model` 限定字段，用 `--model` 按基础模型名或原始模型名进一步筛选。
- 两个命令都可以用 `--token`（每百万输入 token）或 `--call`（每次调用）选定单位，两者互斥。`group` 默认优先显示按量报价，仅匹配到按次报价时显示按次价。
- 默认排除 `promo`、`default`、`low` 和零价，带 `high` 标记的报价仍可参与。`--all` 纳入有标记的报价和零价，沿用当前计价单位。
- 每站保留最低符合条件的报价。`--cny` 仅纳入有有效公开充值价的站点，按名义价 × 充值价排序。`--n` 限制输出条数，默认 30。

查询本身只需标准库。完整回归命令为 `python3 -m unittest discover -s tests`，依赖见下方。

## 日常更新

[每日候选工作流](discover/README.md#daily-candidates)负责读上游、去重和提出审核 PR。它不会更新已确认站点和报价。

在仓库根目录运行下列命令可重建和验证本地快照。

```bash
python3 -m pip install tldextract==5.3.1 beautifulsoup4==4.14.3
bash tools/build.sh
python3 -m unittest discover -s tests
```

`build.sh` 依次清理中转站数据、归一店铺报价、重建候选索引和店铺审核表，再生成模型榜单、统计、独立报告和中英文首页，最后检查文档链接及疑似密钥。

站点或价格有变化时，按[贡献指南](../CONTRIBUTING.md)更新对应输入。公开来源采集已有独立入口，见[发现工具](discover/README.md)和[来源批次](../data/raw/sources/README.md)。

## 脚本

| 用途 | 文件 |
|---|---|
| 查站和查价 | [query.py](query.py) |
| 重建当前快照 | [build.sh](build.sh) |
| 生成读者页面 | [build_reports.py](build_reports.py)、[build_readme.py](build_readme.py)、[build_readme_en.py](build_readme_en.py)、[build_stats.py](build_stats.py)、[generate_by_model.py](generate_by_model.py) |
| 整理中转站 | [merge.py](merge.py) 导入公开报价快照。[dedupe.py](dedupe.py) 合并别名、归一和标记价格 |
| 整理卡网 | [normalize_shops.py](normalize_shops.py) 生成公开店铺表和商品表。[build_shop_review.py](discover/build_shop_review.py) 生成候选审核表 |
| 整理候选证据 | [index_candidates.py](discover/index_candidates.py) 汇总来源、核实结果和入库状态 |
| 检查 | [check_links.py](check_links.py) 验证本地 Markdown 链接。[check_secrets.sh](check_secrets.sh) 检查疑似密钥 |
| 监控和异常分析 | [monitor.py](monitor.py)、[detect_substitution.py](detect_substitution.py) |
| 来源采集 | [discover/](discover/README.md)、[scan.py](scan.py)、[probe.py](probe.py)、[gen_candidates.py](gen_candidates.py) |
| 共用格式和规则 | [common.py](common.py) |
| 历史资料 | [旧工具归档](legacy/README.md)、[早期任务提示词](prompts/) |

## 监控（monitor.py）

```bash
python3 tools/monitor.py add api.openlux.ai ccoo.ai     # 加进名单 data/monitor/targets.txt
python3 tools/monitor.py run                            # 跑一轮，追加 data/monitor/history.csv
python3 tools/monitor.py report --label argon           # 出报告（含上架/下架/变价）
python3 tools/monitor.py drift --days 7                 # 变动汇总
```

只访问 `/api/status` 和 `/api/pricing`，不调用推理接口。`--probe` 会做一次 `max_tokens=1` 的真实请求，
需要 `data/monitor/keys.txt`（每行 `域名,sk-xxx`，已在 `.gitignore`，不会入库）。

## 安全

个别站会把 API Key 误填进模型名或分组名，`merge.py` / `dedupe.py` 入库前会丢弃这类行；`build.sh` 最后跑 `check_secrets.sh` 兜底。**提交前务必看到 ✓。**

## 去重规则（dedupe.py）

| 规则 | 合并条件 |
|---|---|
| 同主机 | 去掉 `api.` `www.` 等通用前缀后主机名相同，且价格表相同（或模型集合相同/Jaccard≥0.95） |
| 同可注册域 | 同一 `example.com` 下的子域价格表完全相同（共享托管域如 `*.ccwu.cc` 除外） |
| 同品牌 | `foo.com` / `foo.ai` 这类换后缀，价格表完全相同且 ≥5 个模型 |
| 同站名 | 同可注册域下站名相同；或换后缀且站名不只是域名本身（`2API` 之于 `2api.xx` 不算证据） |
| 泛解析 | 扫描生成的 `前缀.父域`，若 `随机串.父域` 也能解析，则视为同一目标，只留一个 |

合并保护：别名与同站名两条规则合并前检查价格表，两边都 ≥10 个模型且重合度 <60% → 不同部署，不合并。
人工兜底：`data/relays/split.txt` 里的域名永不合并。

主域名优先级：Veridrop 收录 > GitHub 名单 > 扫描；同级取 Veridrop 分高、非泛解析产物、上次已是主域名、层级少、名字短的。
跨品牌价格表完全相同（≥5 个模型）的站只标 `backend_group`，不合并。
