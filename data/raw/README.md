# 原始抓取产物

本目录保留归一化前的原始文件，便于溯源与复现。**不作为对外主表**，主表见 `../relays/`、`../shops/`。

| 文件 | 内容 | 抓取日 |
|---|---|---|
| `coverage.csv` | Veridrop 收录站覆盖情况（427 站） | 2026-09-24 |
| `gemini-stations.csv` | Gemini 站结构化提取（233 站） | 2026-09-24 |
| `gemini-prices-long.csv` | 站×Gemini 模型×价格（9194 行） | 2026-09-24 |
| `gemini-ranking.md` / `ALL-prices.md` / `BY-RATIO.md` | Gemini 排名与比价 | 2026-09-24/25 |
| `custom-rendered.csv/md` | 浏览器渲染解析的自建站 | 2026-09-25 |
| `mimo-family-*` | mimo 家族扫描（439 站） | 2026-10-02 |
| `mimo-both-pro.md` / `mimo-shortlist.md` | 2.5pro+2.6pro 双有站点 / 采购短名单 | 2026-10-05 |
| `grok-4.5-providers.csv/md` | grok-4.5 扫描（1150 站） | 2026-10-08 |
| `gemini-4-argon-providers.csv/md` | Gemini 4 Argon 扫描（551 站） | 2026-10-14 |
| `google-card-offers.csv` | OpenPrice Google/Gemini 商品（669 条） | 2026-10-16 |
| `google-ultra-offers.csv` | Google Ultra 商品（43 条） | 2026-10-16 |
| `google-*-发卡行情.md` / `google-ultra-20x.md` | Google 会员发卡行情整理 | 2026-10-16 |
| `aihaotan-goods.json` | AI号探商品（204 条） | 2026-10-16 |
| `openprice-offers.json` | OpenPrice 全量报价（9820 条） | 2026-10-16 |
| `ultra20x-shops.json` | Ultra 20x 店铺链接映射 | 2026-10-16 |
| `ultra-and-vertex.md` | Ultra + Vertex/Aistudio 渠道 | 2026-10-16 |

> 价格为公开页面推算值，未对账；版权归各来源站，见根目录 `DATA-LICENSE.md`。

## sources/
| 文件 | 说明 |
|---|---|
| `veridrop-domains.json` | Veridrop 目录收录的域名（浏览器翻页抓取，取并集） |
| `github-list-domains.json` | GitHub 公开名单仓库里提取的域名 |
| `wildcard-dns.json` | 泛解析检测缓存：父域 → 随机子域能否解析 |
