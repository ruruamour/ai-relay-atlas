# discover/ · 找新站

本目录记录候选域名的来源和核实方法。索引器只读取本地清单和证据摘要，是否收录由人工复核。

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
- [Veridrop 抓取清单](../../data/raw/sources/veridrop-directory-2026-11-21.txt) 和 [目录实核记录](../../data/raw/sources/directory-review-2026-11-21.jsonl) — 当前批次实际使用的两个文件。

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
