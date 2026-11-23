# discover/ · 找新站

本目录记录候选域名的来源和核实方法。索引器只读取本地清单和证据摘要，是否收录由人工复核。

<a id="daily-candidates"></a>
## 每日自动拉取

[GitHub Actions 工作流](../../.github/workflows/daily-candidates.yml)每天 UTC 01:17（北京时间 09:17）读取固定的公开目录和结构化名单，也可在仓库 **Actions → Daily candidates → Run workflow** 手动运行。定时任务从默认分支运行，GitHub 繁忙时可能延后。

1. 把工作流和配套脚本合入默认分支，并启用仓库的 Actions。在 **Settings → Actions → General → Workflow permissions** 允许 **Allow GitHub Actions to create and approve pull requests**。组织策略须允许工作流取得 `contents: write` 和 `pull-requests: write`；不用配置个人令牌。工作流只创建或更新 PR，不审批、不自动合并。
2. 拉取器只请求配置好的来源，**不访问候选主机**。与主域、取价主机、别名和既有候选比对时忽略大小写及 `www.`。新域名以首次见到的写法保存。每个域名与来源只保留一条，`first_seen` 是首次记录该来源的 UTC 日期。
3. 有新域名，或已在每日队列中的域名又得到新来源时，机器人更新同一个 `automation/daily-candidates` 待审 PR。没有增量不产生新提交。条目从上游消失不会删除已有证据；个别源失败会记录告警并继续，全部失败则不更新。拒绝某一批后，若上游仍展示同样的候选，后续可能再次提出。
4. 合并 PR 只更新[每日候选队列](../../data/raw/sources/daily-candidates.jsonl)、候选索引和双语首页计数。确认服务和报价仍按[贡献指南](../../CONTRIBUTING.md)另行处理。

若首次建 PR 被权限设置拦下，保留 `automation/daily-candidates` 分支，授权后从该分支向默认分支打开 PR 即可继续。若直接在待审分支提交修改，机器人会暂停，让维护者先处理该 PR，不会覆盖人工提交。已关闭 PR 且决定丢弃该批候选时，可删除对应的机器人分支。

采集作业只有读权限。发布作业使用干净的运行环境，只接收候选队列、索引和两份首页；不安装采集依赖，也不运行待审分支中的代码。

| 每天读取的源 | 采哪些条目 |
|---|---|
| [HowToken](https://howtok.net/) | 首页已渲染的普通卡片，须有可见域名和站内详情页。跳过赞助区，不跟随 `/go/`，不声称覆盖全站。 |
| [公益站导航](https://gongyizhan.com/) | 站点列表卡片明确展示的域名及对应详情页。 |
| [API中转站](https://www.apizhongzhuanzhan.com/providers) | 平台表中标为「中转」且填了官网的行，不采官方厂商。 |
| [1sh1ro 的结构化名单](https://github.com/1sh1ro/ai-api-zhongzhuan/blob/main/data/sites.json) | 明确标注 relay 或 gateway 的记录，只读官网字段，忽略注册链接。 |

Veridrop 在此次普通 HTTPS 测试中返回 403，仍走人工批次。`bubblevv/ai-api-gongyi-nav` 只有注册字段，没有独立官网字段，未加入每日任务。添加来源须有公开、可直接读取的入口和稳定字段，并补充离线解析测试。

移除来源或迁移 URL 前，将旧来源 ID 和 URL 记入[拉取脚本](daily_candidates.py)的 `HISTORICAL_FEED_URLS`（每个来源 ID 对应一个 URL 列表）。这些地址只用于校验旧队列的出处，不再请求。

本地预览和 CI 使用同一[拉取入口](daily_candidates.py)。`--dry-run` 不写入；`--out` 可把结果写到仓库外；`--source` 可重复指定，具体支持的来源见 `--help`。

```bash
python3 -m pip install tldextract==5.3.1 beautifulsoup4==4.14.3
python3 tools/discover/daily_candidates.py --dry-run
python3 tools/discover/daily_candidates.py --out /tmp/atlas-daily-candidates.jsonl
```

## 其它发现工具

| 方法 | 脚本 | 说明 |
|---|---|---|
| Veridrop 目录 | 浏览器 | 读取公开目录的普通站点卡片，分批保留域名快照 |
| GitHub 名单仓库 | `github_lists.py` | 需要 `gh auth login`；扫描固定的公开名单仓库 |
| GitHub 高召回收集 | `github_harvest.py` + `github_code_harvest.py` + `candidate_probe.py` | 搜索公开仓库/代码，提取带来源的域名，再低并发探活；支持断点，详见 [docs/internet-measurement.md](../../docs/internet-measurement.md) |
| GitLab 公共项目 | `gitlab_harvest.py` | 搜索公开项目并读取小型文本文件，提取带项目/文件来源的域名；不执行代码 |
| npm 公共包索引 | `npm_harvest.py` | 读取公开包描述/README 元数据，提取带包名/版本来源的域名；不安装、不执行包 |
| Docker Hub 公共镜像 | `docker_hub_harvest.py` | 读取公开镜像描述元数据，提取带镜像名来源的域名；不拉取、不执行容器 |
| Hugging Face 公共 Spaces | `huggingface_harvest.py` | 读取公开 Space README，提取带 Space/搜索词来源的域名；不运行 Space、不调用推理 |
| Sourcegraph 公共索引 | `sourcegraph_harvest.py` | 只读取公开 README/文本匹配行，不下载或执行代码 |
| Bing 公共搜索 | `web_search_harvest.py` | 读取搜索结果链接和标题，不自动打开结果；仅作候选来源 |
| 公开目录页面 | `directory_harvest.py` | 读取公开中转站目录/比价页中的域名线索，不保存正文或购买路径 |
| 联系人/邮件清单 | `contact_harvest.py` | 从收件人清单等邮箱文本里提取域名线索；只留域名，不存邮箱地址 |
| 前缀 / 换后缀 | `../gen_candidates.py` | 基于已收录站点生成，自动跳过泛解析父域 |
| 证书透明日志 | `crtsh.py` | 直连 crt.sh 公共 PostgreSQL（需 `psql`），批量查询、断点续跑、只走 IPv4；默认 3 并发，请勿调大 |
| 证书透明日志（备用） | `certspotter.py` | HTTP 接口，免费额度很低 |
| 测绘引擎（FOFA/ZoomEye/Shodan） | `faka_fofa.py` | 按源码指纹找自建卡网，详见 [docs/find-faka-shops.md](../../docs/find-faka-shops.md) |
| 测绘查询与导出解析 | `relay_search.py` | 生成中转站/卡网查询串，解析公开 JSON/CSV 导出，详见 [docs/internet-measurement.md](../../docs/internet-measurement.md) |
| urlscan 公共索引 | `urlscan_harvest.py` | 按公开页面标题提取被动扫描索引中的域名，不提交扫描、不保存 IP/路径 |
| 首页卡网指纹 | `shop_fingerprint.py` | 只读首页，保存系统/卡网关键词命中，不保存正文或跳转参数 |
| 候选统一索引 | `index_candidates.py` | **离线**汇总来源、探活、接口命中、主表和卡网审核状态，一行一域名；不自动确认 |
| 卡网审核表 | `build_shop_review.py` | 从首页指纹和可选浏览器复核摘要生成审核表，不自动进入已确认店铺表 |

## 公开目录批次

- [批次说明](../../data/raw/sources/batches/README.md) — 新批次的文件位置和维护方式。
- [2026-11-21-公开目录补录](../../data/raw/sources/batches/2026-11-21/README.md) — 抓取清单 940 个，实核记录 15 个，候选索引新增 497 个。
- [Veridrop 抓取清单](../../data/raw/sources/veridrop-directory-2026-11-21.txt) 和 [目录实核记录](../../data/raw/sources/directory-review-2026-11-21.jsonl) — 2026-11-21 批次使用的两个文件。
- [两份新目录的逐条来源](../../data/raw/sources/batches/2026-11-23/directory-listings.jsonl)。「API中转站」取标为「中转」的行及其官网字段，公益站导航取卡片明确展示的域名。两者都保留指向目录条目本身的公开链接。

新批次把域名清单和逐站记录放在日期目录，旧批次保留原路径。文件名和统计口径见[批次说明](../../data/raw/sources/batches/README.md)。只想核对索引时，可写入临时文件与现有索引比较。

```bash
python3 tools/discover/index_candidates.py \
  --sources-dir data/raw/sources \
  --out /tmp/candidate-index.jsonl
```

`validated` 表示有探活记录或该域名已在主表中，`in_relays` 才表示主表已收录。页面核实类别另记在 `page_category`。

<a id="veridrop浏览器控制台"></a>
## 既有目录读取口径

若要取得新的公开目录快照，只保留普通站点卡片（`data-impression-surface="relays_list"`），跳过广告；遇到访问限制或没有下一页时停止。将去重后的有效域名按行写入上述受支持的 `veridrop-directory*.txt`。站点是否进入 review 仍需另有公开目录/第一方说明证据，并由人工核对主域、`api_host`、别名和品牌；仅出现在第三方目录不构成确认。

<a id="完整流程"></a>
## 完整流程（历史工具说明）

```bash
python3 tools/discover/github_lists.py > /tmp/gh.txt
python3 tools/discover/crtsh.py run /tmp/crt.json && python3 tools/discover/crtsh.py candidates /tmp/crt.json > /tmp/crt.txt
python3 tools/gen_candidates.py --resolve > /tmp/cands.txt
python3 tools/scan.py /tmp/cands.txt /tmp/new.json
python3 tools/merge.py /tmp/new.json --via scan
python3 tools/probe.py && bash tools/build.sh
```

已有数据的重建只需执行 `bash tools/build.sh`，无需重新采集。
