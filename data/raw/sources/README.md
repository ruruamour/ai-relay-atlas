# 原始来源与验证证据

本目录保存候选域名的来源元数据、低并发首页探活和公开接口扫描结果。
这里只保存域名、来源文件、状态、标题、延迟和结构化价格结果，不保存 Cookie、API Key、密码、IP、端口、响应正文或跳转路径/查询参数。

## 来源收集

| 文件 | 来源 | 规模 | 说明 |
|---|---|---:|---|
| `veridrop-domains.json` | Veridrop 公开目录 | 6,060 | 主候选池（已去除 249 个 IP 字面量） |
| `github-list-domains.json` | 固定 GitHub 名单 | 358 | 公开名单域名 |
| `github-harvest.jsonl` | GitHub 仓库/README/名单 | 13,735 | 保留仓库和文件来源 |
| `github-code-harvest.jsonl` | GitHub 代码搜索 | 5,504 | 只保留小型文本文件来源 |
| `gitlab-harvest.jsonl` | GitLab 公共项目 | 2,274 | 不执行项目代码 |
| `urlscan-candidates.jsonl` | urlscan 公共搜索索引 | 660 | 被动索引，不提交扫描 |
| `npm-harvest.jsonl` | npm 公共包元数据 | 1,215 | 不安装或执行 npm 包 |
| `docker-hub-harvest.jsonl` | Docker Hub 公共镜像描述 | 219 | 不拉取或执行容器 |
| `huggingface-harvest.jsonl` | Hugging Face 公共 Spaces README | 388 | 不运行 Space、不调用推理 |
| `sourcegraph-candidates.jsonl` | Sourcegraph 公共文档索引 | 4 | 仅 README/文本匹配行 |
| `bing-candidates.jsonl` | Bing 公共搜索结果 | 65 | 低频查询，噪声较高 |
| `directory-harvest.jsonl` | 公开中转站目录/比价页 | 958 | 只提取域名线索，不保存正文或购买路径 |
| `crtsh-domains.json` | crt.sh 证书透明日志 | 3,527 | 被动 SAN/根域候选，不等于在售站 |
| `certspotter-domains.json` | Certspotter 备用 CT | 100 | 免费接口的批次结果 |
| `prefix-expansion-candidates.txt` | 新增站点前缀/后缀扩展 | 8,894 | 定向组合，不是全网扫描 |
| `candidate-index.jsonl` | 多路候选统一索引 | 28,644 | 一行一域名，汇总来源、探活、接口和卡网候选状态 |

## 验证证据

- `*-probe.jsonl`：首页公开 GET 的状态、标题、延迟和最终主机；`401/403/429/5xx` 也保留。`veridrop-probe.jsonl` 是对主候选池中此前未验证的 2,200 个域名补做的探活。
- `passive-refresh-probe.jsonl` / `passive-refresh-scan.json`：对 1,747 个此前未探活的 CT/目录候选做的低并发补验；871 个返回 2xx/3xx，保留 482 个不含敏感字段的公开接口结果，去重后主表新增 1 个 canonical 站点，其他命中项与已有域名合并。
- `*-scan.json`：只访问已公开的状态/价格/模型目录接口，不调用推理接口。`directory-scan.json` 是公开目录新候选的接口验证结果，208 个 2xx/3xx 中命中 114 个。
- `unified-candidate-probe.jsonl` / `unified-candidate-scan.json`：最后一批补验证的 19 个未覆盖域名，19/19 返回 HTTP 200，17 个命中公开接口。
- `veridrop-scan.json`：上述 Veridrop 补验证中 1,053 个 2xx/3xx 域名的公开接口结果，命中 584 个。
- `shop-fingerprint-candidates.jsonl`：首页卡网/系统指纹候选，**不是已确认商品店**；审核清单为 `data/shops/candidates.csv`。
- `shop-browser-review.jsonl`：4 个高置信候选的浏览器渲染摘要；3 个首页显示商品/卡密相关内容，1 个访问受限。只保存标题、长度和布尔标记，不保存正文。
- `candidate-index.jsonl`：把上述来源、探活、接口命中、主表状态和卡网指纹整理成一行一域名的复查索引；不替代主表。

来源候选和确认主表分离：只有扫描到公开模型/价格目录并通过合并去重的站点才进入 `data/relays/relays.csv`；卡网候选不会自动进入 `data/shops/shops.csv`。
