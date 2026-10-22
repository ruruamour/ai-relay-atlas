# discover/ · 找新站

候选域名的来源。产出都是"域名清单"，再交给 `tools/scan.py` 扫价格。

| 方法 | 脚本 | 说明 |
|---|---|---|
| Veridrop 目录 | 浏览器 | 站点有 Cloudflare，需在已过盾的浏览器页面里执行下面的 JS |
| GitHub 名单仓库 | `github_lists.py` | 需要 `gh auth login`；新仓库加到 `REPOS` |
| 前缀 / 换后缀 | `../gen_candidates.py` | 基于已收录站点生成，自动跳过泛解析父域 |
| 证书透明日志 | `crtsh.py` | 直连 crt.sh 公共 PostgreSQL（需 `psql`），批量查询、断点续跑、只走 IPv4；默认 3 并发，请勿调大 |
| 证书透明日志（备用） | `certspotter.py` | HTTP 接口，免费额度很低 |
| 测绘引擎（FOFA/ZoomEye/Shodan） | `faka_fofa.py` | 按源码指纹全网搜自建卡网，**唯一能突破聚合站上限的路**，详见 [docs/find-faka-shops.md](../../docs/find-faka-shops.md) |

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
