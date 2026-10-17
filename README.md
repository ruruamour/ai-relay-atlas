# ai-relay-atlas · AI 中转站与发卡地图

[![License: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE) [![Data: CC BY-NC 4.0](https://img.shields.io/badge/data-CC%20BY--NC%204.0-lightgrey.svg)](DATA-LICENSE.md) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

把 **AI API 中转站**和 **发卡/卡网店铺**放进同一张"上游地图"。**本阶段以收全名单为主**，细节后续补充。

> ⚠️ 仅收录公开信息，不提供购买入口、不参与交易、不担保。价格为推算值、未对账，以原站为准。见 [DISCLAIMER.md](DISCLAIMER.md)。

<a id="toc"></a>
## 目录

- [数据概览](#stats)
- [快速开始](#quickstart)
- [中转站 · 综合名单](#relays)
- [中转站 · 模型覆盖](#coverage)
- [卡网 · 店铺名单](#shops)
- [卡网 · 平台与系统](#shop-platforms)
- [数据文件](#files)
- [文档](#docs)
- [数据来源](#sources)
- [授权](#license)
- [贡献](#contributing)

<a id="stats"></a>
## 数据概览

| 项 | 数量 |
|---|---|
| 中转站（域名） | 1740 |
| 中转站 × 模型 报价 | 12774 |
| 模型名（去重） | 1353 |
| 发卡店铺 | 314（SaaS 273 / 自建 41） |
| 发卡商品报价 | 10646 |

> 说明：**"模型名"是去重后的模型标识数量**（同一模型在多家站只算 1 个），不等于站数。

<a id="quickstart"></a>
## 快速开始

```bash
git clone https://github.com/ruruamour/ai-relay-atlas.git && cd ai-relay-atlas
python3 tools/query.py model gemini-4-argon --n 30   # 查某模型
python3 tools/query.py domain api.openlux.ai        # 查某站
```

重生成本页：`python3 tools/normalize.py && python3 tools/normalize_shops.py && python3 tools/generate_by_model.py && python3 tools/build_readme.py`

<a id="relays"></a>
## 中转站 · 综合名单

> **不按最低价排序**：低价多为福利/免费组，可用性低。这里按 **Veridrop 实测分 → 模型覆盖数** 排序，仅作线索。

| # | 站点 | Veridrop | 模型数 | Gemini | Grok | MiMo | Argon | 最低价($/1M) | 状态 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `www.micuapi.ai` | 100 | 155 | ✓ |  |  |  | $0.0375 | 200 |
| 2 | `api.hoxkai.top` | 100 | 122 | ✓ | ✓ |  | ✓ | $0.06375 | 200 |
| 3 | `ai.comfly.org` | 100 | 99 | ✓ | ✓ | ✓ | ✓ | $0.15 | 200 |
| 4 | `thousandengine.com` | 100 | 89 | ✓ | ✓ | ✓ | ✓ | $0.0060662 | 200 |
| 5 | `jeniya.cn` | 100 | 88 | ✓ | ✓ | ✓ |  | $0.0055147 | 200 |
| 6 | `anyaigc.com` | 100 | 85 | ✓ | ✓ | ✓ |  | $0.0375 | 200 |
| 7 | `api.winfull.cloud-ip.cc` | 100 | 85 | ✓ | ✓ | ✓ |  | $0.0375 | 200 |
| 8 | `yinli.one` | 100 | 24 | ✓ |  |  |  | $0.15 | 200 |
| 9 | `api.juziai.cc` | 100 | 18 | ✓ | ✓ |  | ✓ | $6 | 200 |
| 10 | `api.qfgapi.com` | 100 | 18 | ✓ | ✓ |  | ✓ | $0.05 | 200 |
| 11 | `api.key77qiqi.com` | 100 | 17 | ✓ |  |  |  | $0.1 | 200 |
| 12 | `top.taluna.ai` | 100 | 16 | ✓ | ✓ |  |  | $0.1 | 200 |
| 13 | `gemini30.pro` | 100 | 16 | ✓ |  |  |  | $0.2625 | 200 |
| 14 | `tenzen.ai` | 100 | 16 | ✓ |  |  |  | $0.1 | 200 |
| 15 | `code28.ccwu.cc` | 100 | 12 | ✓ | ✓ |  | ✓ | $0.375 | 200 |
| 16 | `api.humanwill.xyz` | 100 | 11 | ✓ | ✓ |  |  | $0.24 | 200 |
| 17 | `tian-shu.org` | 100 | 7 | ✓ |  |  |  | $0.105 | 200 |
| 18 | `topapi.io` | 100 | 6 | ✓ | ✓ |  |  | $0.025 | 200 |
| 19 | `aihubmix.com` | 100 | 3 | ✓ |  |  |  | $0.5 | 200 |
| 20 | `laysoai.com` | 100 | 2 | ✓ |  |  |  | $0.048 | 200 |
| 21 | `www.xcloudtoken.com` | 100 | 2 | ✓ |  |  |  | $0.03375 | 200 |
| 22 | `doro.lol` | 100 | 2 | ✓ |  |  |  | $0.45 | 200 |
| 23 | `kjapi.botsmart.net` | 100 | 0 |  |  |  |  | - | 200 |
| 24 | `www.akucb.com` | 100 | 0 |  |  |  |  | - | 200 |
| 25 | `runy-test.yitd.cn` | 100 | 0 |  |  |  |  | - |  |
| 26 | `aigc.x-see.cn` | 100 | 0 |  |  |  |  | - | 200 |
| 27 | `kuaiapi.net` | 100 | 0 |  |  |  |  | - | 200 |
| 28 | `seesaw2ai.com` | 100 | 0 |  |  |  |  | - | 200 |
| 29 | `api.mosshubs.com` | 100 | 0 |  |  |  |  | - | 200 |
| 30 | `wawapi.top` | 100 | 0 |  |  |  |  | - | 200 |
| 31 | `meowntor.xyz.hr` | 100 | 0 |  |  |  |  | - |  |
| 32 | `api-slb.packyapi.com` | 100 | 0 |  |  |  |  | - | 200 |
| 33 | `generativelanguage.googleapis.com` | 99 | 0 |  |  |  |  | - |  |
| 34 | `api.apiyi.com` | 98 | 136 | ✓ | ✓ |  | ✓ | $0.0375 | 200 |
| 35 | `coultra.blueshirtmap.com` | 98 | 74 | ✓ |  |  |  | $0.065 | 200 |
| 36 | `poloai.top` | 98 | 72 | ✓ | ✓ |  | ✓ | $0.1 | 200 |
| 37 | `api.vveai.com` | 98 | 59 | ✓ | ✓ |  |  | $0.1 | 200 |
| 38 | `api.147ai.cn` | 98 | 40 | ✓ | ✓ |  | ✓ | $0.4 | 200 |
| 39 | `runapi.co` | 98 | 19 | ✓ | ✓ |  | ✓ | $0.0215 | 200 |
| 40 | `jp-api.tokone.ai` | 98 | 18 | ✓ |  |  |  | $0.07 | 200 |
| 41 | `api.yourapi.cn` | 98 | 16 | ✓ |  |  | ✓ | $0.35 | 200 |
| 42 | `lanxiu.cc` | 98 | 11 | ✓ | ✓ |  |  | $0.03 | 200 |
| 43 | `api.feiyang.click` | 98 | 4 | ✓ | ✓ |  |  | $0.16 | 200 |
| 44 | `api.squarefaceicon.org` | 98 | 2 | ✓ |  |  |  | $0.1875 | 200 |
| 45 | `vulcanapi.com` | 98 | 0 |  |  |  |  | - | 200 |
| 46 | `newapi.wuji.us.eu.org` | 98 | 0 |  |  |  |  | - | 200 |
| 47 | `vip.xiaweiliang.cn` | 98 | 0 |  |  |  |  | - |  |
| 48 | `api.theclawbay.com` | 98 | 0 |  |  |  |  | - |  |
| 49 | `gg.aivvip.cc` | 97 | 55 | ✓ | ✓ |  | ✓ | - | 200 |
| 50 | `ac.127api.top` | 97 | 35 | ✓ |  |  | ✓ | $75 | 200 |
| 51 | `cf-api.o1key.com` | 97 | 26 | ✓ |  |  |  | $0.1 | 200 |
| 52 | `cdn.sta1n.cn` | 97 | 24 | ✓ |  | ✓ | ✓ | $0.125 | 200 |
| 53 | `api.gravitex.ai` | 97 | 18 | ✓ |  |  | ✓ | $0.1 | 200 |
| 54 | `zjapi.com` | 97 | 12 | ✓ |  |  |  | $0.09 | 200 |
| 55 | `nikoapi.xyz` | 97 | 11 | ✓ |  |  | ✓ | $0.075 | 200 |
| 56 | `routemux.com` | 97 | 9 | ✓ |  |  |  | $0.075 | 200 |
| 57 | `passion8.cc` | 97 | 8 | ✓ | ✓ |  | ✓ | $0.3 | 200 |
| 58 | `nextrouterfree.duckdns.org` | 97 | 0 |  |  |  |  | - |  |
| 59 | `api.xkiro.com` | 97 | 0 |  |  |  |  | - |  |
| 60 | `iai.iisbo.com` | 96 | 114 | ✓ | ✓ |  | ✓ | $0.5418 | 200 |
| 61 | `api.qingyuntop.top` | 96 | 85 | ✓ | ✓ | ✓ |  | $0.0375 | 200 |
| 62 | `love.qinyan.icu` | 96 | 83 | ✓ |  |  |  | $0.065 | 200 |
| 63 | `api.rcouyi.com` | 96 | 71 | ✓ | ✓ | ✓ |  | $0.075 | 200 |
| 64 | `4sapi.com` | 96 | 47 | ✓ | ✓ |  | ✓ | $0.25 | 200 |
| 65 | `vsllm.com` | 96 | 44 | ✓ | ✓ | ✓ |  | $0.1 | 200 |
| 66 | `console.qqqrouter.ai` | 96 | 41 | ✓ |  |  |  | $0.1 | 200 |
| 67 | `2api.powerapi.cc` | 96 | 40 | ✓ | ✓ |  | ✓ | $0.03 |  |
| 68 | `api3.gemai.cc` | 96 | 35 | ✓ | ✓ |  |  | $75 | 200 |
| 69 | `api.gemai.cc` | 96 | 35 | ✓ | ✓ |  |  | $75 | 200 |
| 70 | `api2.gemai.cc` | 96 | 35 | ✓ | ✓ |  |  | $75 | 200 |
| 71 | `nexaxis.ai` | 96 | 32 | ✓ |  |  | ✓ | $0.15 | 200 |
| 72 | `api.vectorengine.ai` | 96 | 32 | ✓ |  | ✓ |  | $0.1 | 200 |
| 73 | `tidewhisper-ai.xyz` | 96 | 27 | ✓ | ✓ |  | ✓ | $0.54 | 200 |
| 74 | `newapi.youkies.cloud` | 96 | 25 | ✓ |  |  | ✓ | $0.012 | 200 |
| 75 | `wolfai.top` | 96 | 23 | ✓ | ✓ |  |  | $0.25 | 200 |
| 76 | `a6api.com` | 96 | 23 | ✓ | ✓ | ✓ | ✓ | $1 | 200 |
| 77 | `api.mcapple.top` | 96 | 22 | ✓ | ✓ |  |  | $0.078 | 200 |
| 78 | `azemm.cc` | 96 | 20 | ✓ |  |  | ✓ | $0.075 | 200 |
| 79 | `moyuu.cc` | 96 | 19 | ✓ | ✓ | ✓ | ✓ | $0.0375 | 200 |
| 80 | `viper3.ai` | 96 | 19 | ✓ | ✓ |  |  | $0.325 | 200 |
| 81 | `sparkcode.top` | 96 | 19 | ✓ | ✓ |  | ✓ | $0.15 | 200 |
| 82 | `api.1024token.xyz` | 96 | 18 | ✓ | ✓ |  |  | $0.045 | 200 |
| 83 | `itkk.lol` | 96 | 18 | ✓ | ✓ |  | ✓ | $0.015 | 200 |
| 84 | `relayrax.com` | 96 | 13 | ✓ |  |  | ✓ | $0.2 | 200 |
| 85 | `llm-all.pro` | 96 | 12 | ✓ | ✓ | ✓ |  | $0.06 | 200 |
| 86 | `sapi.zly168.cn` | 96 | 11 | ✓ | ✓ | ✓ | ✓ | $0.97 | 200 |
| 87 | `www.wamwuai.com` | 96 | 11 | ✓ |  |  |  | - | 200 |
| 88 | `api.clawsocket.com` | 96 | 11 | ✓ | ✓ |  | ✓ | $0.5 | 200 |
| 89 | `cf.modelflare.dev` | 96 | 10 | ✓ | ✓ |  |  | $0.02 | 200 |
| 90 | `qilinapi.nervers.com` | 96 | 10 | ✓ | ✓ |  |  | $0.018 | 200 |
| 91 | `speed23.toter.me` | 96 | 9 | ✓ | ✓ | ✓ |  | $0.18 | 200 |
| 92 | `www.zzshu.cc` | 96 | 8 | ✓ | ✓ |  |  | $0.15 | 200 |
| 93 | `api.xiaoxuapi.com` | 96 | 8 | ✓ |  |  |  | $0.1925 | 200 |
| 94 | `www.weekly-day.top` | 96 | 8 | ✓ | ✓ |  |  | $0.09 | 200 |
| 95 | `wawazz.xyz` | 96 | 8 | ✓ | ✓ |  | ✓ | $0.125 | 200 |
| 96 | `api.maoapi.org` | 96 | 7 | ✓ | ✓ |  | ✓ | $0.24 | 200 |
| 97 | `tian-shu.net` | 96 | 7 | ✓ |  |  |  | $0.105 | 200 |
| 98 | `shapi.vip` | 96 | 5 | ✓ |  |  |  | $0.08 | 200 |
| 99 | `dasuapi.com` | 96 | 4 | ✓ | ✓ |  |  | $0.22 | 200 |
| 100 | `www.hejuapi.com` | 96 | 4 | ✓ |  |  | ✓ | $0.1875 | 200 |

完整名单（1740 站）：[relays.csv](data/relays/relays.csv) · 站×模型价：[relay-models.csv](data/relays/relay-models.csv)

[↑ 目录](#toc)

<a id="coverage"></a>
## 中转站 · 模型覆盖

> 家族 → 模型名数 / 覆盖站点数。完整榜单见 [by-model/index.md](data/relays/by-model/index.md)。

| 家族 | 模型名数 | 覆盖站点数 |
|---|---|---|
| Gemini | 1027 | 697 |
| Grok | 15 | 1140 |
| MiMo | 32 | 436 |
| 其他 | 279 | 64 |

[↑ 目录](#toc)

<a id="shops"></a>
## 卡网 · 店铺名单

> 按店铺列，粗记"卖什么"。**不提供购买入口**，`域名` 仅为标识。完整表：[shops.csv](data/shops/shops.csv) / [products.csv](data/shops/products.csv)。

| # | 店铺 | 归属 | 卖什么 | 价位(¥) | 来源 |
|---|---|---|---|---|---|
| 1 | GGbond ai | 链动小铺 | GPT/Claude/Cursor/Gemini/Ultra/Grok/Kiro/邮箱 | 0.12-11433 | OpenPrice |
| 2 | 梦泽 | 链动小铺 | GPT/Claude/Cursor/Gemini/Ultra/Grok/Kiro/邮箱 | 0.01-3325.87 | AI号探/OpenPrice |
| 3 | Alexander | 链动小铺 | GPT/Claude/Cursor/Gemini/Ultra/Grok/Kiro/邮箱 | 0-3419.6 | AI号探/OpenPrice |
| 4 | harvey | 链动小铺 | GPT/Claude/Cursor/Gemini/Ultra/Grok/Kiro/邮箱 | 0.06-2263.73 | OpenPrice |
| 5 | 派大星 | 链动小铺 | GPT/Claude/Cursor/Gemini/Ultra/Grok/Kiro/邮箱 | 0.06-2263.73 | OpenPrice |
| 6 | chiyu | 链动小铺 | GPT/Claude/Cursor/Gemini/Ultra/Grok/Kiro/邮箱 | 0.04-3440.2 | AI号探/OpenPrice |
| 7 | 🛍 壹号铺 | 链动小铺 | GPT/Claude/Cursor/Gemini/Ultra/Grok/Kiro/邮箱 | 0.04-5665 | OpenPrice |
| 8 | AccHarbor | 自建/异次元发卡 | 邮箱 | 0.9-1073.04 | OpenPrice |
| 9 | 陆柒科技 | 链动小铺 | GPT/Claude/Cursor/Gemini/邮箱 | 0.32-2884 | AI号探/OpenPrice |
| 10 | team最后的余晖 | 链动小铺 | GPT/Claude/Gemini/Ultra/Grok/邮箱 | 0.07-10300 | AI号探/OpenPrice |
| 11 | 比特拈花 | 链动小铺 | GPT/Claude/Cursor/Gemini/Ultra/Grok/Kiro/邮箱 | 0-3625.6 | AI号探/OpenPrice |
| 12 | 自行车 Ai 店铺 | 链动小铺 | GPT/Claude/Gemini/Grok/Kiro/邮箱 | 0.04-3499.94 | AI号探/OpenPrice |
| 13 | Xm API | 链动小铺 | GPT/Claude/Cursor/Gemini/Ultra/邮箱 | 0.07-102999 | OpenPrice |
| 14 | RenWin | 链动小铺 | GPT/Claude/Cursor/Gemini/Kiro/邮箱 | 0-3347.5 | OpenPrice |
| 15 | （彩虹马）筱博的小店 | 链动小铺 | GPT/Claude/Cursor/Gemini/Ultra/Grok/邮箱 | 1.99-3296 | OpenPrice |
| 16 | 橙子AI源头(全网最低源头) | 链动小铺 | GPT/Claude/Gemini/Grok/邮箱 | 0.01-1812.8 | OpenPrice |
| 17 | 奥特曼严选 | 链动小铺 | GPT/Cursor/Gemini/Ultra/Grok/Kiro/邮箱 | 0.21-1122.7 | AI号探/OpenPrice |
| 18 | YaHo🐯GPT全网低价 | 链动小铺 | GPT/Claude/Gemini/Kiro/邮箱 | 0-3285.7 | OpenPrice |
| 19 | recardai | 链动小铺 | GPT/Claude/Gemini/邮箱 | 0.1-1895.2 | OpenPrice |
| 20 | ai小头 | 链动小铺 | GPT/Claude/Gemini/Ultra/Grok/邮箱 | 1.13-1461.57 | AI号探/OpenPrice |
| 21 | ai教父 | 链动小铺 | GPT/Claude/Cursor/Gemini/Ultra/Grok/邮箱 | 0.1-3512.3 | AI号探/OpenPrice |
| 22 | 源头AI - Bot | 链动小铺 | GPT/Claude/Cursor/Gemini/Ultra/Grok/邮箱 | 0.26-3656.5 | OpenPrice |
| 23 | 小柴AI | 链动小铺 | GPT/Claude/Cursor/Gemini/Grok/Kiro/邮箱 | 0.12-2935.5 | OpenPrice |
| 24 | 大娃 | 链动小铺 | GPT/Claude/Gemini/Kiro/邮箱 | 1.84-1433.76 | OpenPrice |
| 25 | YUJI | 链动小铺 | GPT/Claude/Gemini/Grok/邮箱 | 0.04-3439.17 | OpenPrice |
| 26 | Tora-雪诺AI源头分销小铺 | 链动小铺 | GPT/Claude/Cursor/Gemini/Ultra/Grok/邮箱 | 0-3397.97 | AI号探/OpenPrice |
| 27 | 商家8719 | 链动小铺 | GPT/Claude/Gemini/Ultra/Grok/Kiro/邮箱 | 0.21-5665 | OpenPrice |
| 28 | 稳中求胜 | 链动小铺 | GPT/Claude/Cursor/Gemini/Ultra/邮箱 | 0.14-6180 | OpenPrice |
| 29 | 52XUEAI | 链动小铺 | GPT/Claude/Cursor/Gemini/Ultra/Kiro/邮箱 | 0.6-2781 | OpenPrice |
| 30 | 一梦低价货源 | 链动小铺 | GPT/Claude/Cursor/Gemini/Ultra/邮箱 | 0.07-1902.36 | OpenPrice |
| 31 | 亚米的整合服务供应商 | 链动小铺 | GPT/Claude/Gemini/Ultra/Kiro/邮箱 | 0-3953.14 | OpenPrice |
| 32 | 商家9027 | 链动小铺 | GPT/Claude/Gemini/Ultra/Kiro/邮箱 | 0.13-2018.8 | OpenPrice |
| 33 | GPT-源头供货-招代理 | 链动小铺 | GPT/Claude/Cursor/Gemini/Ultra/Grok/邮箱 | 0.72-3399 | OpenPrice |
| 34 | 直连AI | 链动小铺 | GPT/Claude/Cursor/Gemini/Ultra/Grok/Kiro/邮箱 | 0.16-3924.3 | OpenPrice |
| 35 | 极速Ai | 链动小铺 | GPT/Claude/Cursor/Gemini/Grok/邮箱 | 0.23-10300 | OpenPrice |
| 36 | 海海星星AI | 链动小铺 | GPT/Claude/Cursor/Gemini/Ultra/Grok/Kiro/邮箱 | 0.05-3378.4 | OpenPrice |
| 37 | 幻境MirageAI | 链动小铺 | GPT/Claude/Cursor/Gemini/Grok/邮箱 | 0.09-2152.7 | AI号探/OpenPrice |
| 38 | 金幺の小店 | 链动小铺 | GPT/Claude/Cursor/Gemini/Grok/Kiro/邮箱 | 0.08-3594.7 | OpenPrice |
| 39 | GPT \| Cluade \| Gemini \| Grok 集合铺 | 云猫寄售 | GPT/Claude/Cursor/Gemini/Grok/邮箱 | 0.05-1336.01 | OpenPrice |
| 40 | 棉被的ai小铺 | 链动小铺 | GPT/Claude/Gemini/Grok/邮箱 | 1.73-3213.6 | OpenPrice |
| 41 | Antipro（请看店铺公告） | 云猫寄售 | GPT/Claude/Gemini/Grok | 0-10299 | OpenPrice |
| 42 | 元宇宙土拨鼠 | 链动小铺 | GPT/Claude/Cursor/Gemini/Ultra/邮箱 | 0.12-3656.5 | OpenPrice |
| 43 | 启航AI | 链动小铺 | GPT/Claude/Gemini/Kiro/邮箱 | 0.87-3406.73 | OpenPrice |
| 44 | 东北23333--承接理工科毕设 | 链动小铺 | GPT/Claude/Cursor/Gemini/Ultra/Kiro/邮箱 | 0.05-3633.84 | OpenPrice |
| 45 | AI猫猫社 | 链动小铺 | GPT/邮箱 | 0-3551.96 | OpenPrice |
| 46 | NiuGe AI 加钟站 | 链动小铺 | GPT/Claude/Gemini/Ultra/Grok/Kiro/邮箱 | 0.09-10300 | OpenPrice |
| 47 | AI OPC | 链动小铺 | GPT/Claude/Cursor/Gemini/Grok | 2.06-3474.86 | OpenPrice |
| 48 | NianHuaStore | 自建/独角数卡 | GPT/Claude/Ultra/Grok/邮箱 | 9-7999 | OpenPrice |
| 49 | 曼波小铺 | 链动小铺 | GPT/Claude/Gemini/Ultra/Grok/Kiro/邮箱 | 0.38-3424.75 | OpenPrice |
| 50 | LeoLab | 链动小铺 | GPT/Claude/Gemini/邮箱 | 0.1-1277.2 | OpenPrice |
| 51 | 自我放飞 | 链动小铺 | GPT/邮箱 | 0.62-3347.5 | OpenPrice |
| 52 | ai直售 | 链动小铺 | GPT/Claude/Cursor/邮箱 | 0.03-1416.25 | OpenPrice |
| 53 | 老马AI（源头直供，招代理） | 链动小铺 | GPT/Claude/Cursor/Gemini/Ultra/Grok/邮箱 | 0.52-3397.97 | OpenPrice |
| 54 | FranklyBuilds的AI小店 | 链动小铺 | GPT/Claude/Gemini/Kiro/邮箱 | 0.03-243.34 | AI号探/OpenPrice |
| 55 | gpt_plus_批发 | 链动小铺 | GPT/Claude/邮箱 | 0.04-192.61 | OpenPrice |
| 56 | 柴柴AI | 链动小铺 | GPT/Claude/Gemini/邮箱 | 0-1903.44 | OpenPrice |
| 57 | 【AI源头直供】AICA | 链动小铺 | GPT/Claude/Gemini/Kiro/邮箱 | 1.17-1984.19 | OpenPrice |
| 58 | 诚心优选 | 链动小铺 | GPT/Claude/Gemini/Ultra/邮箱 | 0-10299 | OpenPrice |
| 59 | 智铺 AI | 链动小铺 | GPT/Claude/Cursor/Ultra/邮箱 | 1.83-1291.28 | OpenPrice |
| 60 | 9号小铺 | 链动小铺 | GPT/Claude/Gemini/Ultra/Grok/邮箱 | 0.09-11845 | OpenPrice |
| 61 | AI源头批发旗舰店 | 链动小铺 | GPT/Claude/Cursor/Gemini/Ultra/Grok/邮箱 | 3.86-3254.8 | OpenPrice |
| 62 | 007的小铺 | 链动小铺 | GPT/Gemini/邮箱 | 8.19-275.32 | AI号探/OpenPrice |
| 63 | AI小铺 | 链动小铺 | GPT/Gemini/邮箱 | 0-1658.3 | OpenPrice |
| 64 | ai源头高品质供应商 | 链动小铺 | GPT/Claude/Gemini/邮箱 | 1.03-3930.48 | OpenPrice |
| 65 | 商家1430 | 链动小铺 | GPT/邮箱 | 0.07-1287.5 | OpenPrice |
| 66 | 无事小神仙的ai小店 | 链动小铺 | GPT/Claude/Gemini/Ultra/Grok/邮箱 | 0.01-3306.3 | OpenPrice |
| 67 | Esa的Ai小铺 | 链动小铺 | GPT/Claude/Gemini/邮箱 | 1.85-1182.44 | OpenPrice |
| 68 | 幽羊 AI | 链动小铺 | GPT/邮箱 | 0.04-107.64 | OpenPrice |
| 69 | 马了个马 | 链动小铺 | GPT/Claude/Cursor/Gemini/邮箱 | 0.24-684.95 | OpenPrice |
| 70 | AI供应 | 链动小铺 | GPT/Claude/Gemini/Grok/邮箱 | 0.14-3347.5 | OpenPrice |
| 71 | 卷子ai ( Lucky ) | 链动小铺 | GPT/Claude/Gemini/Ultra/Grok/邮箱 | 0.23-3347.5 | OpenPrice |
| 72 | 第8号铺 | 链动小铺 | GPT/Claude/Gemini/邮箱 | 0.12-10300 | OpenPrice |
| 73 | TxyxT小店 | 自建/未知 | GPT/Claude/Gemini/Ultra/Grok | 2.5-3600 | OpenPrice |
| 74 | 全网最低批发ai账号 | 自建/未知 | GPT/Claude/Gemini/Ultra/Grok/邮箱 | 6-3300 | OpenPrice |
| 75 | open_store | 链动小铺 | GPT/邮箱 | 1.85-1081.5 | OpenPrice |
| 76 | AI gogo渠道 （招代理） | 链动小铺 | GPT/Claude/Cursor/Gemini/邮箱 | 0.01-3347.5 | OpenPrice |
| 77 | AI贝贝 | 链动小铺 | GPT/Gemini/邮箱 | 0.03-3502 | OpenPrice |
| 78 | yuyu的G小店 | 链动小铺 | GPT/Gemini/邮箱 | 0.09-1359.6 | OpenPrice |
| 79 | 橙子AI批发站 | 链动小铺 | GPT/Gemini/邮箱 | 0.26-3283.64 | AI号探/OpenPrice |
| 80 | DT的AI小铺 | 链动小铺 | GPT/Claude/Gemini/Ultra/邮箱 | 0.57-1926.1 | OpenPrice |
| 81 | 一站式 AI 杂货铺 | 自建/异次元发卡 | GPT/Claude/Gemini/Ultra/Grok/邮箱 | 8-3456 | OpenPrice |
| 82 | 稳问AI  --AI 大玩家（AI真源头，招代理） | 链动小铺 | GPT/Claude/Gemini/邮箱 | 2.06-2008.5 | OpenPrice |
| 83 | 52AI店铺 | 链动小铺 | GPT/Claude/Gemini/邮箱 | 0.52-3244.5 | OpenPrice |
| 84 | Epoch | 链动小铺 | GPT/Claude/Gemini/Grok/邮箱 | 0.19-764.78 | OpenPrice |
| 85 | 海神- GPT-大玩家（招代理） | 链动小铺 | GPT/Claude/Ultra/邮箱 | 3.19-3584.4 | OpenPrice |
| 86 | 猫猫豆 | 链动小铺 | Gemini/Grok | 0.09-216.3 | OpenPrice |
| 87 | Esfine科技小店 | 自建/未知 | GPT | 0.5-1150 | OpenPrice |
| 88 | YUJAN宇见Ai-Plus Pro-源头直供 | 链动小铺 | GPT/Claude/Gemini/邮箱 | 16.48-3499.94 | OpenPrice |
| 89 | LaniCC AI | 链动小铺 | GPT/Claude/Cursor/Gemini | 9.5-3450.5 | OpenPrice |
| 90 | AI-MEMBER发卡网 | 自建/异次元发卡 | GPT/Claude/Gemini/Grok/邮箱 | 0.39-3300 | OpenPrice |
| 91 | AI甄选 | 链动小铺 | GPT/Claude/Gemini/Ultra | 5.05-1863.17 | OpenPrice |
| 92 | 布布 AI | 链动小铺 | GPT/Claude/Gemini/邮箱 | 2.58-288.4 | OpenPrice |
| 93 | Aisou智充 | 自建/异次元发卡 | GPT/Claude/Gemini/Grok | 6.8-66666 | OpenPrice |
| 94 | Nature-Ai账号 | 自建/异次元发卡 | GPT/Claude/Gemini/Grok | 3.6-3488 | OpenPrice |
| 95 | 各类低价对接汇总 | 链动小铺 | GPT/Gemini/Ultra/邮箱 | 0.33-360 | AI号探 |
| 96 | 小JIANG的商店 | 链动小铺 | GPT/Claude/邮箱 | 0.52-2004.16 | OpenPrice |
| 97 | 海王AI-源头直供 | 链动小铺 | GPT/Claude | 4.74-3466.98 | OpenPrice |
| 98 | IKUN货源 | 链动小铺 | Gemini/邮箱 | 4.53-199.73 | OpenPrice |
| 99 | Tim的AI便利店 | 链动小铺 | GPT/Claude/Gemini/Ultra/邮箱 | 1.02-1543.97 | OpenPrice |
| 100 | lulu-Ai | 链动小铺 | GPT/Claude/Grok/邮箱 | 0.08-1122.7 | OpenPrice |
| 101 | 迷途小铺 | 链动小铺 | GPT/Claude/Gemini/邮箱 | 1.55-3489.64 | AI号探/OpenPrice |
| 102 | iKun AI源头小铺 | 链动小铺 | GPT/Gemini/邮箱 | 0.07-1050.6 | OpenPrice |
| 103 | 泡泡Ai | 链动小铺 | GPT/Claude/邮箱 | 1.15-1280.29 | OpenPrice |
| 104 | 王哈哈AI 源头工作室 | 自建/未知 | GPT/Claude/Grok | 34-666666 | OpenPrice |
| 105 | ai源头批发 | 链动小铺 | Gemini/Ultra/Grok | 2.05-968.1 | OpenPrice |
| 106 | dandan的AI小铺 | 链动小铺 | GPT/Claude/Gemini | 0.79-1563.54 | OpenPrice |
| 107 | ton | 链动小铺 | GPT/邮箱 | 0.5-1153.6 | AI号探/OpenPrice |
| 108 | 以太 AI服务订阅充值 | 自建/异次元发卡 | GPT/Gemini/Ultra/Grok/邮箱 | 4-3250 | OpenPrice |
| 109 | 吾爱API | 链动小铺 | 邮箱 | 25.74-710.7 | OpenPrice |
| 110 | 小白源头AI | 链动小铺 | Claude/Gemini/邮箱 | 0-102999 | OpenPrice |
| 111 | 抢抢的AI小铺 | 链动小铺 | GPT/邮箱 | 0.08-1236 | OpenPrice |
| 112 | 还没想好 | 链动小铺 | GPT/Gemini/邮箱 | 1.59-1155.66 | OpenPrice |
| 113 | AI五条悟 | 链动小铺 | GPT/Claude/Gemini | 3.17-3563.8 | OpenPrice |
| 114 | AI奥特曼【源头招代理】对接码：99999 | 云猫寄售 | GPT/Claude | 8.76-3605 | OpenPrice |
| 115 | AI海外账号 | 链动小铺 | GPT/Claude/Ultra/邮箱 | 9.71-2060 | OpenPrice |
| 116 | FlyAI源头 | 自建/未知 | GPT/Claude/Grok | 49-3640 | OpenPrice |
| 117 | GOGO 商店 | 自建/未知 | GPT/Claude | 2.5-1460 | OpenPrice |
| 118 | Gemini源头供货商 | 链动小铺 | Gemini/邮箱 | 1.03-22.66 | AI号探/OpenPrice |
| 119 | HZ-API | 链动小铺 | GPT | 0.89-3244.5 | OpenPrice |
| 120 | YCYAPI | 链动小铺 | GPT/Gemini/邮箱 | 0.34-1030 | OpenPrice |

共 314 家店，上表按商品数取前 120。

[↑ 目录](#toc)

<a id="shop-platforms"></a>
## 卡网 · 平台与系统

**发卡平台（SaaS，商家入驻）**

| 平台 | 域名 | 说明 |
|---|---|---|
| 链动小铺 | `pay.ldxp.cn;wzyp.cn` | 国内最大，AI账号/CDK多在此 |
| 数卡5188 | `5188.faka.com.cn` | 寄售/卡密 |
| 云发卡 | `yunfakaw.com` | 数字商品自动发卡 |
| 酷发卡 | `kufaka.com` | 虚拟商品自动发货 |
| 易发卡 | `efaka.top` | AI账号与虚拟商品 |
| 卡付 | `onecdk.com` | AI会员兑换 |
| 萌次元商城 | `mcy.im` | 多商户，也有自建系统版 |
| 云猫寄售 | `catfk.com` | 服务费率 1.8%，寄售平台 |
| 数卡寄售 | `shuka.cc` | 数卡/卡密寄售 |

**发卡系统（开源软件，自建用）**

| 系统 | 仓库 | 说明 |
|---|---|---|
| 独角数卡 | https://github.com/assimon/dujiaoka | PHP/Laravel，自建最主流 |
| 异次元发卡 | https://github.com/lizhipay/acg-faka | PHP，二次元风，多商户 |
| ZFAKA | - | PHP，2025 年更新到 1.4.6 |
| Orion Key | https://github.com/RivenLau/orion-key | React+Next.js+Spring Boot |
| 萌次元商城系统 | https://wiki.mcy.im | 分站/插件体系 |

[↑ 目录](#toc)

<a id="files"></a>
## 数据文件

| 路径 | 内容 |
|---|---|
| `data/relays/relays.csv` | 中转站主表（1740 站） |
| `data/relays/relay-models.csv` | 站 × 模型 × 价格（12774 条） |
| `data/relays/relay-systems.csv` | 中转站软件名录 |
| `data/relays/by-model/` | 按模型榜单（1353 个模型） |
| `data/shops/platforms.csv` / `systems.csv` | 发卡平台 / 系统 |
| `data/shops/shops.csv` | 店铺主表（314） |
| `data/shops/products.csv` | 商品报价（10646） |
| `data/raw/` | 原始产物与溯源 |
| `data/stats.md` | 数据概览 |

[↑ 目录](#toc)

<a id="docs"></a>
## 文档

| 文档 | 内容 |
|---|---|
| [pricing-basics.md](docs/pricing-basics.md) | 倍率/价格怎么算 |
| [glossary.md](docs/glossary.md) | 黑话表 |
| [how-to-choose.md](docs/how-to-choose.md) | 怎么选上游 / 避坑 |
| [CONTRIBUTING.md](CONTRIBUTING.md) | 贡献格式 |

[↑ 目录](#toc)

<a id="sources"></a>
## 数据来源

OpenPrice、水獭比价(shuita.xyz)、PriceAI、AI号探、AiFaKa、Veridrop，以及各中转站公开的 `/api/pricing`、`/api/v1/model-plaza`。原始报价版权归各来源站，见 [DATA-LICENSE.md](DATA-LICENSE.md)。

<a id="license"></a>
## 授权

- 代码 **MIT** · [LICENSE](LICENSE)
- 编排与整理 **CC BY-NC 4.0** · [DATA-LICENSE.md](DATA-LICENSE.md)
- 原始报价版权归各来源站

<a id="contributing"></a>
## 贡献

见 [CONTRIBUTING.md](CONTRIBUTING.md)。

[↑ 回到目录](#toc)
