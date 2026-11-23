# 原始来源与验证证据

[候选域名索引](candidate-index.jsonl)按域名汇总线索，也包含已收录站点。[中转站主表](../../relays/relays.csv)只列核实过的服务。新资料的文件格式见[批次说明](batches/README.md)。

## 核实批次

| 批次 | 抓取清单 | 收录依据 | 变化 |
|---|---|---|---|
| [2026-11-23 中文目录复核](batches/2026-11-23/README.md) | [141 条记录，140 个域名](batches/2026-11-23/directory-listings.jsonl) | [30 条逐域记录](batches/2026-11-23/directory-review.jsonl) | 站点主表 +10，别名 +2，候选索引 +34 个域名 |
| <a id="2026-11-21-公开目录补录"></a>[2026-11-21 公开目录补录](batches/2026-11-21/README.md) | [940 个目录域名](veridrop-directory-2026-11-21.txt) | [15 条逐站核实记录](directory-review-2026-11-21.jsonl) | 站点主表 +15，候选索引 +497 个域名 |

早期调查见[历史核实记录](batches/legacy/README.md)。

<a id="来源收集"></a>
## 来源注册表

| 文件 | 来源 | 规模 | 含义 |
|---|---|---:|---|
| `veridrop-domains.json` | Veridrop 历史目录 | 6,060 | 历史种子清单，也用于重建发现来源 |
| [`veridrop-directory-2026-11-21.txt`](veridrop-directory-2026-11-21.txt) | Veridrop 最近活跃列表 | 940 | 2026-11-21 的去重域名抓取清单 |
| [`directory-review-2026-11-21.jsonl`](directory-review-2026-11-21.jsonl) | 目录与服务方页面交叉核实 | 15 | 每站一条的实核记录 |
| `github-list-domains.json` | 固定 GitHub 名单 | 358 | 公开名单域名 |
| `github-harvest.jsonl` | GitHub 仓库、README、名单 | 13,735 | 保留仓库和文件来源的线索 |
| `github-code-harvest.jsonl` | GitHub 代码搜索 | 5,504 | 小型文本文件中的线索 |
| `gitlab-harvest.jsonl` | GitLab 公共项目 | 2,274 | 公共项目线索，不执行项目代码 |
| `urlscan-candidates.jsonl` | urlscan 公共搜索索引 | 660 | 被动索引线索，不提交扫描 |
| `npm-harvest.jsonl` | npm 公共包元数据 | 1,215 | 包描述和 README 线索，不安装包 |
| `docker-hub-harvest.jsonl` | Docker Hub 公共镜像描述 | 219 | 描述元数据线索，不拉取容器 |
| `huggingface-harvest.jsonl` | Hugging Face 公共 Spaces README | 388 | README 线索，不运行 Space |
| `sourcegraph-candidates.jsonl` | Sourcegraph 公共文档索引 | 4 | README 和文本匹配线 |
| `bing-candidates.jsonl` | Bing 公共搜索结果 | 65 | 低频、噪声较高的候选来源 |
| `directory-harvest.jsonl` | 公开目录和比价页 | 958 | 目录域名线索，不保存正文或购买路径 |
| [2026-11-23 目录清单](batches/2026-11-23/directory-listings.jsonl) | 公益站导航、API中转站 | 141 | 每个条目记录目录、站名、明列域名和详情页，不自动确认 |
| `crtsh-domains.json` | crt.sh 证书透明日志 | 3,527 | 被动 SAN 和根域候选，不等于在售站 |
| `certspotter-domains.json` | Certspotter 备用 CT | 100 | 免费接口的批次结果 |
| `prefix-expansion-candidates.txt` | 定向前缀和后缀扩展 | 8,894 | 组合候选，不是全网扫描 |
| `contact-harvest.jsonl` | 联系人和邮件清单 | 130 | 只保留域名及分类，不保存邮箱地址 |
| [`daily-candidates.jsonl`](daily-candidates.jsonl) | [每日自动拉取](../../../tools/discover/README.md#daily-candidates) | 按新线索累积 | 保留域名、来源、公开证据页和首次发现日期；合入候选不等于确认服务 |
| [`candidate-index.jsonl`](candidate-index.jsonl) | 多路统一索引 | 见[首页快照计数](../../../README.md#stats) | 汇总来源、探活、接口、主表和卡网候选状态 |

<a id="验证证据"></a>
## 如何读证据

`*-probe.jsonl` 是首页访问记录，含状态、标题、延迟和最终主机。`*-scan.json` 保存公开状态、价格和模型目录接口的结构化结果。`contact-browser-verify.jsonl` 和 `directory-review*.jsonl` 保存页面类别及核实摘要。

确认服务需要公开接口或服务方说明，还要核对主域、别名和品牌。卡网首页的指纹线索另列在[店铺候选审核表](../../shops/candidates.csv)，不计入已收录店铺。
