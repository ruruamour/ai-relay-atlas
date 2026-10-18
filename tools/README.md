# tools/ · 脚本

全部手动运行，无 CI。Python 3.10+；`dedupe.py` 需要 `pip install tldextract`。

## 日常更新

```bash
# 1. 找候选（任选，见 discover/README.md）
python3 tools/gen_candidates.py --resolve > /tmp/cands.txt

# 2. 扫价格（断点续跑，可中断）
python3 tools/scan.py /tmp/cands.txt /tmp/new.json

# 3. 并入主表（已有站点整体替换报价，新站点追加）
python3 tools/merge.py /tmp/new.json --via scan

# 4. 探活 + 重建
python3 tools/probe.py
bash tools/build.sh
```

刷新已收录站点的价格：把 `relays.csv` 的 `domain`（或 `api_host`）导出成清单，走 2–4 步。

## 脚本

| 脚本 | 作用 |
|---|---|
| `build.sh` | 一键重建：dedupe → 店铺归一 → 模型榜单 → 统计 → README → 密钥检查 |
| `check_secrets.sh` | 检查仓库里有没有疑似 API Key/Token（有则报错，禁止提交） |
| `scan.py` | 扫站点信息（`/api/status`、Sub2API `/api/v1/settings/public`）与价格（`/api/pricing`、`/api/v1/model-plaza`）；取最低付费分组价，区分按量/按次；`--only status` 只刷新站名/版本/充值价 |
| `merge.py` | 扫描结果并入 `relays.csv` / `relay-models.csv`；价格不公开的站按"目录收录或自定义站名"收录 |
| `dedupe.py` | 合并别名与镜像、剔除泛解析子域、归一模型名、打价格标记、识别疑似同后端 |
| `probe.py` | 首页探活（状态码、延迟、网页标题） |
| `gen_candidates.py` | 前缀/换后缀生成候选，跳过已收录、已扫描；`--resolve` 先做 DNS 过滤并去掉泛解析父域 |
| `generate_by_model.py` | 生成 `data/relays/by-model/` |
| `build_stats.py` | 生成 `data/stats.md` |
| `build_readme.py` | 生成 `README.md` |
| `query.py` | 命令行查询：`model` / `site` / `find` |
| `normalize_shops.py` | 卡网数据归一（`data/raw/` → `data/shops/`） |
| `common.py` | 共享：CSV、模型名归一、模型家族、域名归一 |
| `discover/` | 找新站的方法（Veridrop、GitHub 名单、证书日志） |
| `legacy/` | 早期一次性脚本，已停用 |
| `prompts/` | 让 AI 代理执行扫描任务的提示词 |

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
