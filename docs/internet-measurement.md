# 用互联网测绘找 AI 中转站和卡网

FOFA、Quake、ZoomEye、Shodan、Censys 等平台已经采集了公开的 HTTP、TLS、DNS 和产品指纹。这里使用的是它们的**索引查询和导出功能**，不是对目标做端口扫描或漏洞探测。

## GitHub 高召回种子

GitHub 适合先建立便宜的候选池，再用公开页面验证；它不是当前在线状态的证明。

```bash
python3 tools/discover/github_harvest.py run \
  --out /tmp/github-candidates.jsonl \
  --domains /tmp/github-domains.txt \
  --checkpoint /tmp/github-candidates.checkpoint.json \
  --search-limit 30

python3 tools/discover/candidate_probe.py \
  /tmp/github-candidates.jsonl \
  --out /tmp/github-probe.jsonl \
  --live-out /tmp/github-live.txt \
  --workers 16

# 代码搜索补充：README/名单之外的公开文本证据
python3 tools/discover/github_code_harvest.py \
  --out /tmp/github-code-candidates.jsonl \
  --domains /tmp/github-code-domains.txt \
  --checkpoint /tmp/github-code.checkpoint.json

# urlscan 被动索引
python3 tools/discover/urlscan_harvest.py \
  --out /tmp/urlscan-candidates.jsonl \
  --domains /tmp/urlscan-domains.txt

# GitLab 公共项目补充
python3 tools/discover/gitlab_harvest.py \
  --out /tmp/gitlab-candidates.jsonl \
  --domains /tmp/gitlab-domains.txt \
  --checkpoint /tmp/gitlab.checkpoint.json

# npm 公共包元数据
python3 tools/discover/npm_harvest.py \
  --out /tmp/npm-candidates.jsonl \
  --domains /tmp/npm-domains.txt

# Docker Hub 公共镜像描述
python3 tools/discover/docker_hub_harvest.py \
  --out /tmp/docker-hub-candidates.jsonl \
  --domains /tmp/docker-hub-domains.txt

# Hugging Face 公共 Spaces README
python3 tools/discover/huggingface_harvest.py \
  --out /tmp/huggingface-candidates.jsonl \
  --domains /tmp/huggingface-domains.txt

# Sourcegraph 公共文档索引
python3 tools/discover/sourcegraph_harvest.py \
  --out /tmp/sourcegraph-candidates.jsonl \
  --domains /tmp/sourcegraph-domains.txt \
  --checkpoint /tmp/sourcegraph.checkpoint.json

# Bing 公共搜索结果
python3 tools/discover/web_search_harvest.py \
  --out /tmp/bing-candidates.jsonl \
  --domains /tmp/bing-domains.txt

# 整理为一行一域名的复查索引
python3 tools/discover/index_candidates.py
```

`github_harvest.py` 只读取公开仓库中的 README、名单和小型数据文件，不执行仓库代码；结果保留仓库/文件来源。`candidate_probe.py` 只对首页做低并发 GET。`200` 和 `3xx` 进入后续处理，`401/403/429/5xx` 也保留作人工复查。最近一轮原始结果保存在 `data/raw/sources/github-harvest.jsonl`、`github-code-harvest.jsonl`、`urlscan-candidates.jsonl`、`gitlab-harvest.jsonl`、`npm-harvest.jsonl`、`docker-hub-harvest.jsonl`、`huggingface-harvest.jsonl`、`sourcegraph-candidates.jsonl` 和 `bing-candidates.jsonl`；探活结果使用同目录下对应的 probe 文件。

## 1. 先生成查询串

```bash
python3 tools/discover/relay_search.py queries --platform fofa --kind all
python3 tools/discover/relay_search.py queries --platform shodan --kind relay
```

第一轮建议使用“系统指纹优先”的查询，不要一开始限定 `Gemini`：

- 中转站：`New-API`、`One-API`、`Sub2API`、`模型广场`、`api/pricing`、`model-plaza`
- 卡网：`dujiaoka`、`acg-faka`、`zfaka`、`自动发货`、`卡密`、`寄售`
- 业务词只作为第二轮收窄：`ChatGPT`、`Claude`、`Gemini`、`Grok`、`API Key`、`充值`

不同平台的查询语法不完全相同，以网页输入框的字段提示为准。FOFA/Quake 对国内站通常更有价值；Shodan/Censys 适合补海外站、证书和基础设施关系。

## 2. 网页端搜索和导出

每条查询先查看少量结果，确认命中率后再导出。导出时保留：

- 域名或 host
- 标题
- 协议和端口（仅用于离线核对，不入库）
- 平台名称、查询串、导出时间

第一轮不要加 `country="CN"`。很多站使用香港 CDN、海外服务器或全球 CDN，地理过滤会漏掉它们。

## 3. 解析导出结果

支持 JSON、CSV 和每行一个 URL/域名：

```bash
python3 tools/discover/relay_search.py parse \
  --platform fofa \
  --kind relay \
  --out /tmp/relay-candidates.txt \
  ~/Downloads/fofa-relay.json
```

多个平台可以一次合并：

```bash
python3 tools/discover/relay_search.py parse \
  --kind relay \
  --out /tmp/measurement-candidates.txt \
  ~/Downloads/fofa.json ~/Downloads/quake.csv ~/Downloads/shodan.json
```

解析器会去掉 IP、明显的代码托管/官方文档域名和当前已收录域名；候选证据会另存为同名 `.jsonl`。

## 4. 公开页面验证

候选域名只代表“测绘平台曾经看见过”，不代表现在仍在线。后续用低并发验证公开页面：

```bash
python3 tools/scan.py /tmp/relay-candidates.txt /tmp/relay-scan.json --workers 16
python3 tools/merge.py /tmp/relay-scan.json --via scan
python3 tools/probe.py
bash tools/build.sh
```

`scan.py` 只访问公开状态、价格和模型目录接口，不调用推理接口。验证顺序是：

1. DNS / 首页是否可达
2. 是否有 `/api/status`、`/api/pricing`、`/api/v1/settings/public` 或 `/api/v1/model-plaza`
3. 是否有公开模型目录或价格
4. 是否为 AI 中转站、卡网，还是普通站/演示站

卡网导出也可以用同一解析器去重；不要把卡网候选交给中转站的 `scan.py`/`merge.py`，卡网专用查询串和后续归类仍在 `tools/discover/faka_fofa.py`。

## 5. 提高覆盖率

同一组查询在多个平台分别执行，最后取并集。对已发现站点再做被动扩展。CT 查询支持断点续跑：

```bash
python3 tools/discover/crtsh.py run data/raw/sources/crtsh-domains.json --batch 15 --workers 1
python3 tools/discover/crtsh.py candidates data/raw/sources/crtsh-domains.json > /tmp/ct-candidates.txt
```

证书日志可能包含大量随机主机名；先做 DNS/关键词过滤，再探活和扫描，不要把所有 SAN 直接并入主表。

- CT 日志中的 SAN 子域
- 同证书、同 NS、同 ASN 的站点
- 页面 JS 和 sitemap 中的关联域名
- GitHub/Gitee 公开名单和代码搜索
- urlscan、Common Crawl 等公开索引

这些关系只用于生成候选，不能单凭同 IP 或同证书认定是同一家。域名去重和同后端判断交给现有 `dedupe.py`，原始来源和查询串应保留，便于复查和增量更新。

## 6. 边界

- 只查询测绘平台已收录的公开数据。
- 不登录、不注册、不爆破、不测试漏洞、不提交推理请求。
- 遵守各平台配额和服务条款。
- 仓库只保存域名、公开模型/价格及来源，不保存 API Key、Cookie、购买链接、IP 和端口等敏感或基础设施信息。
