# discover/ · 找新站

候选域名的来源。产出都是"域名清单"，再交给 `tools/scan.py` 扫价格。

| 方法 | 脚本 | 说明 |
|---|---|---|
| Veridrop 目录 | 浏览器 | 站点有 Cloudflare，需在已过盾的浏览器页面里执行下面的 JS |
| GitHub 名单仓库 | `github_lists.py` | 需要 `gh auth login`；新仓库加到 `REPOS` |
| 前缀 / 换后缀 | `../gen_candidates.py` | 基于已收录站点生成，自动跳过泛解析父域 |
| 证书透明日志 | `crtsh.py` / `certspotter.py` | 能挖到猜不到的子域；两者免费额度都很低，容易 429 |

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
python3 tools/gen_candidates.py --skip /tmp/old.json.done > /tmp/cands.txt
python3 tools/scan.py /tmp/cands.txt /tmp/new.json
python3 tools/merge.py /tmp/new.json --via scan
python3 tools/probe.py && bash tools/build.sh
```
