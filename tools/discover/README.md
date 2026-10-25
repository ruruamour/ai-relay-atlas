# discover/ · 找新站

候选域名的来源。产出都是"域名清单"，再交给 `tools/scan.py` 扫价格。

| 方法 | 脚本 | 说明 |
|---|---|---|
| Veridrop 目录 | 浏览器 | 站点有 Cloudflare，需在已过盾的浏览器页面里执行下面的 JS |
| GitHub 名单仓库 | `github_lists.py` | 需要 `gh auth login`；扫描固定的公开名单仓库 |
| GitHub 高召回收集 | `github_harvest.py` + `github_code_harvest.py` + `candidate_probe.py` | 搜索公开仓库/代码，提取带来源的域名，再低并发探活；支持断点，详见 [docs/internet-measurement.md](../../docs/internet-measurement.md) |
| GitLab 公共项目 | `gitlab_harvest.py` | 搜索公开项目并读取小型文本文件，提取带项目/文件来源的域名；不执行代码 |
| npm 公共包索引 | `npm_harvest.py` | 读取公开包描述/README 元数据，提取带包名/版本来源的域名；不安装、不执行包 |
| Docker Hub 公共镜像 | `docker_hub_harvest.py` | 读取公开镜像描述元数据，提取带镜像名来源的域名；不拉取、不执行容器 |
| Hugging Face 公共 Spaces | `huggingface_harvest.py` | 读取公开 Space README，提取带 Space/搜索词来源的域名；不运行 Space、不调用推理 |
| Sourcegraph 公共索引 | `sourcegraph_harvest.py` | 只读取公开 README/文本匹配行，不下载或执行代码 |
| Bing 公共搜索 | `web_search_harvest.py` | 读取搜索结果链接和标题，不自动打开结果；仅作候选来源 |
| 公开目录页面 | `directory_harvest.py` | 读取公开中转站目录/比价页中的域名线索，不保存正文或购买路径 |
| 前缀 / 换后缀 | `../gen_candidates.py` | 基于已收录站点生成，自动跳过泛解析父域 |
| 证书透明日志 | `crtsh.py` | 直连 crt.sh 公共 PostgreSQL（需 `psql`），批量查询、断点续跑、只走 IPv4；默认 3 并发，请勿调大 |
| 证书透明日志（备用） | `certspotter.py` | HTTP 接口，免费额度很低 |
| 测绘引擎（FOFA/ZoomEye/Shodan） | `faka_fofa.py` | 按源码指纹找自建卡网，详见 [docs/find-faka-shops.md](../../docs/find-faka-shops.md) |
| 测绘查询与导出解析 | `relay_search.py` | 生成中转站/卡网查询串，解析 FOFA/Quake/ZoomEye/Shodan/Censys 的公开 JSON/CSV 导出，详见 [docs/internet-measurement.md](../../docs/internet-measurement.md) |
| urlscan 公共索引 | `urlscan_harvest.py` | 按公开页面标题提取被动扫描索引中的域名，不提交扫描、不保存 IP/路径 |
| 首页卡网指纹 | `shop_fingerprint.py` | 只读首页，保存系统/卡网关键词命中，不保存正文或跳转参数；结果进入 `data/raw/sources/shop-fingerprint-candidates.jsonl` |
| 候选统一索引 | `index_candidates.py` | 汇总多路来源、探活、接口命中、主表和卡网审核状态，一行一域名 |
| 卡网审核表 | `build_shop_review.py` | 从首页指纹和可选浏览器复核摘要生成 `data/shops/candidates.csv`，不自动进入已确认店铺表 |

## Veridrop（浏览器控制台）

在 `https://veridrop.org/relays` 页面的开发者工具里运行，结果另存为 `data/raw/sources/veridrop-domains.json`（与旧文件取并集）：

```js
(async () => {
  const out = new Set();
  for (let p = 1; p <= 200; p++) {
    const t = await (await fetch('/relays?page=' + p)).text();
    const m = [...t.matchAll(/data-impression-domain="([^"]+)"/g)].map(x => x[1]);
    if (!m.length) break;
    m.forEach(x => out.add(x));
  }
  copy(JSON.stringify([...out].sort()));   // 已复制到剪贴板
})();
```

## 完整流程

```bash
python3 tools/discover/github_lists.py > /tmp/gh.txt
python3 tools/discover/crtsh.py run /tmp/crt.json && python3 tools/discover/crtsh.py candidates /tmp/crt.json > /tmp/crt.txt
python3 tools/gen_candidates.py --resolve > /tmp/cands.txt
python3 tools/scan.py /tmp/cands.txt /tmp/new.json
python3 tools/merge.py /tmp/new.json --via scan
python3 tools/probe.py && bash tools/build.sh
```
