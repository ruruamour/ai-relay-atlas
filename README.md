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
| 中转站（域名） | 8074 |
| 中转站 × 模型 报价 | 390523 |
| 模型名（去重） | 5150 |
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

| # | 站点 | 状态 | 延迟 | Veridrop | 模型数 | 覆盖 | 最低价($/1M) |
|---|---|---|---|---|---|---|---|
| 1 | `www.micuapi.ai` | 200 | 2516ms | 100 | 155 | G | $0.0375 |
| 2 | `api.hoxkai.top` | 200 | 1538ms | 100 | 122 | GXA | $0.06375 |
| 3 | `ai.comfly.org` | 200 | 1277ms | 100 | 99 | GXMA | $0.15 |
| 4 | `thousandengine.com` | 200 | 3439ms | 100 | 89 | GXMA | $0.0060662 |
| 5 | `jeniya.cn` | 200 | 3216ms | 100 | 88 | GXM | $0.0055147 |
| 6 | `api.winfull.cloud-ip.cc` | 200 | 3563ms | 100 | 85 | GXM | $0.0375 |
| 7 | `anyaigc.com` | 200 | 2107ms | 100 | 85 | GXM | $0.0375 |
| 8 | `yinli.one` | 200 | 2351ms | 100 | 24 | G | $0.15 |
| 9 | `api.juziai.cc` | 200 | 2239ms | 100 | 18 | GXA | $6 |
| 10 | `api.qfgapi.com` | 200 | 759ms | 100 | 18 | GXA | $0.05 |
| 11 | `api.key77qiqi.com` | 200 | 1890ms | 100 | 17 | G | $0.1 |
| 12 | `tenzen.ai` | 200 | 2623ms | 100 | 16 | G | $0.1 |
| 13 | `gemini30.pro` | 200 | 2881ms | 100 | 16 | G | $0.2625 |
| 14 | `top.taluna.ai` | 200 | 4274ms | 100 | 16 | GX | $0.1 |
| 15 | `code28.ccwu.cc` | 200 | 849ms | 100 | 12 | GXA | $0.375 |
| 16 | `api.humanwill.xyz` | 200 | 2422ms | 100 | 11 | GX | $0.24 |
| 17 | `tian-shu.org` | 200 | 1747ms | 100 | 7 | G | $0.105 |
| 18 | `topapi.io` | 200 | 836ms | 100 | 6 | GX | $0.025 |
| 19 | `aihubmix.com` | 200 | 2536ms | 100 | 3 | G | $0.5 |
| 20 | `doro.lol` | 200 | 3026ms | 100 | 2 | G | $0.45 |
| 21 | `laysoai.com` | 200 | 5669ms | 100 | 2 | G | $0.048 |
| 22 | `www.xcloudtoken.com` | 200 | 2754ms | 100 | 2 | G | $0.03375 |
| 23 | `api.mosshubs.com` | 200 | 4354ms | 100 | 0 | - | - |
| 24 | `meowntor.xyz.hr` | 200 | 1063ms | 100 | 0 | - | - |
| 25 | `www.akucb.com` | 200 | 1535ms | 100 | 0 | - | - |
| 26 | `seesaw2ai.com` | 200 | 1662ms | 100 | 0 | - | - |
| 27 | `kuaiapi.net` | 200 | 2867ms | 100 | 0 | - | - |
| 28 | `kjapi.botsmart.net` | 200 | 468ms | 100 | 0 | - | - |
| 29 | `api-slb.packyapi.com` | 200 | 3936ms | 100 | 0 | - | - |
| 30 | `aigc.x-see.cn` | 200 | 261ms | 100 | 0 | - | - |
| 31 | `wawapi.top` | 200 | 1272ms | 100 | 0 | - | - |
| 32 | `poloai.top` | 200 | 2379ms | 98 | 381 | GXA | $0.016 |
| 33 | `api.apiyi.com` | 200 | 2810ms | 98 | 354 | GXA | $0.01 |
| 34 | `runapi.co` | 200 | 1567ms | 98 | 161 | GXA | $0.008 |
| 35 | `coultra.blueshirtmap.com` | 200 | 4259ms | 98 | 74 | G | $0.065 |
| 36 | `api.vveai.com` | 200 | 1321ms | 98 | 59 | GX | $0.1 |
| 37 | `api.147ai.cn` | 200 | 424ms | 98 | 40 | GXA | $0.4 |
| 38 | `jp-api.tokone.ai` | 200 | 1180ms | 98 | 18 | G | $0.07 |
| 39 | `api.yourapi.cn` | 200 | 858ms | 98 | 16 | GA | $0.35 |
| 40 | `lanxiu.cc` | 200 | 3134ms | 98 | 11 | GX | $0.03 |
| 41 | `api.feiyang.click` | 200 | 1436ms | 98 | 4 | GX | $0.16 |
| 42 | `api.squarefaceicon.org` | 200 | 1445ms | 98 | 2 | G | $0.1875 |
| 43 | `vulcanapi.com` | 200 | 1959ms | 98 | 0 | - | - |
| 44 | `newapi.wuji.us.eu.org` | 200 | 3475ms | 98 | 0 | - | - |
| 45 | `gg.aivvip.cc` | 200 | 1346ms | 97 | 55 | GXA | - |
| 46 | `ac.127api.top` | 200 | 1161ms | 97 | 35 | GA | $75 |
| 47 | `cf-api.o1key.com` | 200 | 1928ms | 97 | 26 | G | $0.1 |
| 48 | `cdn.sta1n.cn` | 200 | 1261ms | 97 | 24 | GMA | $0.125 |
| 49 | `api.gravitex.ai` | 200 | 2364ms | 97 | 18 | GA | $0.1 |
| 50 | `zjapi.com` | 200 | 647ms | 97 | 12 | G | $0.09 |
| 51 | `nikoapi.xyz` | 200 | 1482ms | 97 | 11 | GA | $0.075 |
| 52 | `passion8.cc` | 200 | 678ms | 97 | 8 | GXA | $0.3 |
| 53 | `4sapi.com` | 200 | 1545ms | 96 | 140 | GXA | $0.1 |
| 54 | `iai.iisbo.com` | 200 | 1712ms | 96 | 114 | GXA | $0.5418 |
| 55 | `api.qingyuntop.top` | 200 | 2460ms | 96 | 85 | GXM | $0.0375 |
| 56 | `love.qinyan.icu` | 200 | 1685ms | 96 | 83 | G | $0.065 |
| 57 | `api.rcouyi.com` | 200 | 1872ms | 96 | 71 | GXM | $0.075 |
| 58 | `vsllm.com` | 200 | 1190ms | 96 | 44 | GXM | $0.1 |
| 59 | `console.qqqrouter.ai` | 200 | 1638ms | 96 | 41 | G | $0.1 |
| 60 | `api2.gemai.cc` | 200 | 1457ms | 96 | 35 | GX | $75 |
| 61 | `api.gemai.cc` | 200 | 1562ms | 96 | 35 | GX | $75 |
| 62 | `api3.gemai.cc` | 200 | 1453ms | 96 | 35 | GX | $75 |
| 63 | `api.vectorengine.ai` | 200 | 2244ms | 96 | 32 | GM | $0.1 |
| 64 | `nexaxis.ai` | 200 | 2820ms | 96 | 32 | GA | $0.15 |
| 65 | `tidewhisper-ai.xyz` | 200 | 2352ms | 96 | 27 | GXA | $0.54 |
| 66 | `newapi.youkies.cloud` | 200 | 1918ms | 96 | 25 | GA | $0.012 |
| 67 | `wolfai.top` | 200 | 1897ms | 96 | 23 | GX | $0.25 |
| 68 | `a6api.com` | 200 | 1247ms | 96 | 23 | GXMA | $1 |
| 69 | `api.mcapple.top` | 200 | 1181ms | 96 | 22 | GX | $0.078 |
| 70 | `azemm.cc` | 200 | 2588ms | 96 | 20 | GA | $0.075 |
| 71 | `moyuu.cc` | 200 | 719ms | 96 | 19 | GXMA | $0.0375 |
| 72 | `viper3.ai` | 200 | 1981ms | 96 | 19 | GX | $0.325 |
| 73 | `sparkcode.top` | 200 | 2079ms | 96 | 19 | GXA | $0.15 |
| 74 | `itkk.lol` | 200 | 1228ms | 96 | 18 | GXA | $0.015 |
| 75 | `api.1024token.xyz` | 200 | 1669ms | 96 | 18 | GX | $0.045 |
| 76 | `relayrax.com` | 200 | 1049ms | 96 | 13 | GA | $0.2 |
| 77 | `llm-all.pro` | 200 | 6195ms | 96 | 12 | GXM | $0.06 |
| 78 | `api.clawsocket.com` | 200 | 1077ms | 96 | 11 | GXA | $0.5 |
| 79 | `sapi.zly168.cn` | 200 | 300ms | 96 | 11 | GXMA | $0.97 |
| 80 | `www.wamwuai.com` | 200 | 2584ms | 96 | 11 | G | - |
| 81 | `cf.modelflare.dev` | 200 | 1224ms | 96 | 10 | GX | $0.02 |
| 82 | `qilinapi.nervers.com` | 200 | 2332ms | 96 | 10 | GX | $0.018 |
| 83 | `speed23.toter.me` | 200 | 1684ms | 96 | 9 | GXM | $0.18 |
| 84 | `www.zzshu.cc` | 200 | 2805ms | 96 | 8 | GX | $0.15 |
| 85 | `wawazz.xyz` | 200 | 2347ms | 96 | 8 | GXA | $0.125 |
| 86 | `api.xiaoxuapi.com` | 200 | 813ms | 96 | 8 | G | $0.1925 |
| 87 | `www.weekly-day.top` | 200 | 2168ms | 96 | 8 | GX | $0.09 |
| 88 | `tian-shu.net` | 200 | 1309ms | 96 | 7 | G | $0.105 |
| 89 | `api.maoapi.org` | 200 | 1906ms | 96 | 7 | GXA | $0.24 |
| 90 | `shapi.vip` | 200 | 1642ms | 96 | 5 | G | $0.08 |
| 91 | `dasuapi.com` | 200 | 1715ms | 96 | 4 | GX | $0.22 |
| 92 | `www.hejuapi.com` | 200 | 1120ms | 96 | 4 | GA | $0.1875 |
| 93 | `api.wynb.top` | 200 | 1294ms | 96 | 3 | G | $0.2625 |
| 94 | `zenmux.ai` | 200 | 1317ms | 96 | 0 | - | - |
| 95 | `bbbs.pw` | 200 | 1573ms | 96 | 0 | - | - |
| 96 | `hiflowt.ai` | 200 | 2451ms | 96 | 0 | - | - |
| 97 | `www.ciciapi.com` | 200 | 1582ms | 96 | 0 | - | - |
| 98 | `api.relayrouter.ai` | 200 | 3440ms | 95 | 89 | GXMA | $0.0027574 |
| 99 | `quanzil.com` | 200 | 1779ms | 95 | 89 | GXMA | $0.0055147 |
| 100 | `api.zhongzhuan.chat` | 200 | 2161ms | 95 | 85 | GXM | $0.0375 |

覆盖：G=Gemini · X=Grok · M=MiMo · A=Argon。

完整名单（8074 站）：[relays.csv](data/relays/relays.csv) · 站×模型价：[relay-models.csv](data/relays/relay-models.csv)

[↑ 目录](#toc)

<a id="coverage"></a>
## 中转站 · 模型覆盖

> 家族 → 模型名数 / 覆盖站点数。完整榜单见 [by-model/index.md](data/relays/by-model/index.md)。

| 家族 | 模型名数 | 覆盖站点数 |
|---|---|---|
| Gemini | 1172 | 5133 |
| Grok | 153 | 3672 |
| MiMo | 34 | 1573 |
| Claude | 304 | 5556 |
| OpenAI | 561 | 6201 |
| 其他 | 2926 | 5526 |

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
| `data/relays/relays.csv` | 中转站主表（8074 站） |
| `data/relays/relay-models.csv` | 站 × 模型 × 价格（390523 条） |
| `data/relays/relay-systems.csv` | 中转站软件名录 |
| `data/relays/by-model/` | 按模型榜单（5150 个模型） |
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
