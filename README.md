# ai-relay-atlas · AI 中转站与发卡地图

[![License: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE) [![Data: CC BY-NC 4.0](https://img.shields.io/badge/data-CC%20BY--NC%204.0-lightgrey.svg)](DATA-LICENSE.md) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

把 **AI API 中转站**和 **发卡/卡网店铺**放进同一张"上游地图"。README 直接给榜单，全量数据在 `data/`。

> ⚠️ 仅收录公开信息，不提供购买入口、不参与交易、不担保。价格为推算值、未对账，以原站为准。见 [DISCLAIMER.md](DISCLAIMER.md)。

## 数据概览

| 项 | 数量 |
|---|---|
| 中转站（域名） | 1740 |
| 中转站 × 模型 报价 | 12774 |
| 发卡店铺 | 314（SaaS 261 / 自建 53） |
| 发卡商品报价 | 10646 |
| 按模型榜单 | 142（≥8 家） |

```bash
python3 tools/query.py model gemini-4-argon --n 30
python3 tools/query.py domain api.openlux.ai
```

## 中转站 · 各模型最低价 Top 15

> 实际价 = `model_ratio × group_ratio × 2`，USD / 1M 输入，已排除 0 价与免费组。完整榜单见 [by-model/](data/relays/by-model/index.md)。

### Gemini 4 Argon（509 家）

| # | 站点 | 输入 | 输出 | 倍率 | 分组 |
|---|---|---|---|---|---|
| 1 | `codelypixverse.com` | $0.069231 | $0.115385 | 1 | default |
| 2 | `ccoo.ai` | $0.2 | $1 | 0.1 | Google 特惠 |
| 3 | `www.ccoo.ai` | $0.2 | $1 | 0.1 | Google 特惠 |
| 4 | `catapi.catcard.uk` | $0.3 | $1.5 | 0.15 | 【自营按量】Gemini |
| 5 | `moyuu.cc` | $0.3 | $1.5 | 0.15 | gemini |
| 6 | `www.lingzhan.top` | $0.3 | $1.5 | 0.15 | Gemini(Antigravity反代自有号池) |
| 7 | `www.moyuu.cc` | $0.3 | $1.5 | 0.15 | gemini |
| 8 | `newapi.youkies.cloud` | $0.32 | $1.6 | 0.16 | a/gemini |
| 9 | `api.fluxapi.vip` | $0.36 | $1.8 | 0.18 | Gemini满血反重力 |
| 10 | `api.luciferai.cc` | $0.36 | $2.16 | 0.18 | gemini |
| 11 | `fluxapi.vip` | $0.36 | $1.8 | 0.18 | Gemini满血反重力 |
| 12 | `sub2api.luciferai.cc` | $0.36 | $2.16 | 0.18 | gemini |
| 13 | `www.fluxapi.vip` | $0.36 | $1.8 | 0.18 | Gemini满血反重力 |
| 14 | `api.lt4net.org` | $0.4 | $2 | 0.1 | gemini |
| 15 | `api.toapis.com` | $0.4 | $2 | 1 | default |

### MiMo v2.6 Pro（130 家）

| # | 站点 | 输入 | 输出 | 倍率 | 分组 |
|---|---|---|---|---|---|
| 1 | `sub2api.xybbz.xyz` | $0.0015 | - | 0.06 | Kimi-k3 |
| 2 | `ai.gigimed.cn` | $0.06525 | - | 0.15 | a6api |
| 3 | `api.wuhen-ai.com` | $0.075 | - | 0.3 | 小米-（cc客户端可接） |
| 4 | `apiv3.52codeflow.top` | $0.087 | - | 0.2 | 世界第一模型 |
| 5 | `aiapibank.com` | $0.15 | - | 0.05 | GPT超疯狂分组（国庆特惠） |
| 6 | `keylinkclub.com` | $0.1827 | - | 0.42 | guochan |
| 7 | `api.bingyun.vip` | $0.24 | - | 0.08 | 国模福利-008倍率 |
| 8 | `api.asdfas.party` | $0.248 | - | 0.08 | 英伟达 |
| 9 | `api.openlux.ai` | $0.32625 | - | 0.75 | Xiaomi-1 |
| 10 | `api.relayrouter.ai` | $0.32625 | - | 0.75 | Xiaomi-1 |
| 11 | `gzxbykj.com` | $0.358875 | - | 0.8250000000000001 | Xiaomi-1 |
| 12 | `worldcodes.online` | $0.36 | - | 1.0 | 国模低价分组【实际倍率0.12】 |
| 13 | `v2.cloudmist.cloud` | $0.375187 | - | 0.8624999999999999 | Xiaomi-1 |
| 14 | `makerend.com` | $0.407813 | - | 0.9375 | Xiaomi-1 |
| 15 | `hetune.top` | $0.42 | - | 1 | 国模统一分组 |

### MiMo v2.6 Flash（145 家）

| # | 站点 | 输入 | 输出 | 倍率 | 分组 |
|---|---|---|---|---|---|
| 1 | `ai.gigimed.cn` | $0.021 | - | 0.15 | a6api |
| 2 | `apiv3.52codeflow.top` | $0.028 | - | 0.2 | 世界第一模型 |
| 3 | `keylinkclub.com` | $0.042 | - | 0.3 | guochan_便宜 |
| 4 | `aiapibank.com` | $0.05 | - | 0.05 | GPT超疯狂分组（国庆特惠） |
| 5 | `api.hud.im` | $0.05 | - | 0.05 | 【国模】deepseek-特价 |
| 6 | `api.asdfas.party` | $0.08 | - | 0.08 | 英伟达 |
| 7 | `api.bingyun.vip` | $0.08 | - | 0.08 | 国模福利-008倍率 |
| 8 | `api.openlux.ai` | $0.105 | - | 0.75 | Xiaomi-1 |
| 9 | `api.relayrouter.ai` | $0.105 | - | 0.75 | Xiaomi-1 |
| 10 | `gptzzz.ai` | $0.109 | - | 0.64 | MiMo 小米官key |
| 11 | `gzxbykj.com` | $0.1155 | - | 0.8250000000000001 | Xiaomi-1 |
| 12 | `ai.lfree.org` | $0.12 | - | 1 | claude |
| 13 | `worldcodes.online` | $0.12 | - | 1.0 | 国模低价分组【实际倍率0.12】 |
| 14 | `www.lingzhan.top` | $0.12 | - | 0.12 | 普通国模 |
| 15 | `v2.cloudmist.cloud` | $0.12075 | - | 0.8624999999999999 | Xiaomi-1 |

### MiMo v2.5 Pro（332 家）

| # | 站点 | 输入 | 输出 | 倍率 | 分组 |
|---|---|---|---|---|---|
| 1 | `api.khaix.net` | $0.0099 | - | 0.045 | 🇨🇳国模池-按次计费（chat接口） |
| 2 | `aeapi.cn` | $0.01 | - | 1 | default |
| 3 | `pianyitoken.gay` | $0.032877 | - | 0.08 | 国模0.08x |
| 4 | `api.deepsb.com` | $0.0435 | - | 0.1 | 一折国模大杂烩 |
| 5 | `ai.gigimed.cn` | $0.06 | - | 0.15 | a6api |
| 6 | `api.inktandwkx.top` | $0.068055 | - | 0.065 | 限时福利 |
| 7 | `api.wuhen-ai.com` | $0.075 | - | 0.3 | 小米-gpt可接 |
| 8 | `apiv3.52codeflow.top` | $0.08 | - | 0.2 | 世界第一模型 |
| 9 | `ikun.love` | $0.08 | - | 0.2 | 国模 |
| 10 | `openoneapi.com` | $0.12 | - | 0.3 | 国模 |
| 11 | `kimera.cc` | $0.1305 | - | 0.3 | 国产模型聚合 超低价 |
| 12 | `api.moleapi.com` | $0.135 | - | 0.3 | relay |
| 13 | `hk.moleapi.com` | $0.135 | - | 0.3 | relay |
| 14 | `hetune.top` | $0.14 | - | 1 | 国模统一分组 |
| 15 | `api.yjs.im` | $0.15 | - | 0.15 | OpenModels |

### Grok 4.5（1042 家）

| # | 站点 | 输入 | 输出 | 倍率 | 分组 |
|---|---|---|---|---|---|
| 1 | `api-hub.asia` | $0.002 | $0.006 | 0.001 | Grok |
| 2 | `tmdapis.com` | $0.015 | $0.0375 | 0.25 | grok |
| 3 | `790053500.com` | $0.02 | $0.06 | 0.01 | Grok-4.6《free号池》 |
| 4 | `api.khala.online` | $0.02 | $0.06 | 0.01 | grok-free |
| 5 | `api.wuhen-ai.com` | $0.02 | $0.06 | 0.01 | grok(标准messages) |
| 6 | `cf.modelflare.dev` | $0.02 | $0.06 | 0.01 | grok-award |
| 7 | `llm-api.aigw2.cn` | $0.02 | $0.06 | 0.01 | Grok Free |
| 8 | `modelflare.dev` | $0.02 | $0.06 | 0.01 | grok-award |
| 9 | `o-ai.me` | $0.02 | $0.06 | 0.01 | grok-001 |
| 10 | `origin.modelflare.dev` | $0.02 | $0.06 | 0.01 | grok-award |
| 11 | `weilai.chat` | $0.02 | $0.06 | 0.01 | grok free |
| 12 | `xinyue.mom` | $0.02 | $0.06 | 0.01 | Gork【未开质量守护】 |
| 13 | `api3.kscsnkli.site` | $0.021 | $0.061 | 0.01 | 低价国模 |
| 14 | `pianyitoken.gay` | $0.027397 | $0.082191 | 0.1 | grok heavy |
| 15 | `aggretoken.com` | $0.03 | $0.09 | 1 | Standard |

### Gemini 3.8 Flash（176 家）

| # | 站点 | 输入 | 输出 | 倍率 | 分组 |
|---|---|---|---|---|---|
| 1 | `apiroute.top` | $0.0075 | $0.0375 | 0.01 | gemini-anti-特惠 |
| 2 | `www.nexotoken.net` | $0.0128983 | $0.0644914 | 0.09273 | Gemini·CLI特价版 |
| 3 | `fishai.yanyumeta.cn` | $0.044 | $0.187 |  |  |
| 4 | `modelsell.com` | $0.05 | $0.3 | 0.1 | Gemini Cli |
| 5 | `api.openlux.ai` | $0.0551475 | $0.275738 | 0.07353 | Anti-Gemini-1 |
| 6 | `api.relayrouter.ai` | $0.0551475 | $0.275738 | 0.07353 | Anti-Gemini-1 |
| 7 | `v2.cloudmist.cloud` | $0.0634196 | $0.317098 | 0.0845595 | Anti-Gemini-1 |
| 8 | `crowllm.com` | $0.065 | $0.34 | 0.5 | pro |
| 9 | `api-top.com` | $0.075 | $0.375 | 0.1 | Gemini满血 |
| 10 | `topapi.io` | $0.075 | $0.375 | 0.1 | Gemini满血 |
| 11 | `newapi.youkies.cloud` | $0.09 | $0.45 | 0.12 | a/gemini |
| 12 | `api.liangrekui.com` | $0.10875 | $0.54375 | 0.145 | JA gemini自制 |
| 13 | `quanzil.com` | $0.110295 | $0.551475 | 0.14706 | Anti-Gemini-1 |
| 14 | `tryallapi.com` | $0.110295 | $0.551475 | 0.14706 | Anti-Gemini-1 |
| 15 | `jeniya.cn` | $0.110295 | $0.551475 | 0.14706 | Anti-Gemini-1 |

## 发卡 · 平台与系统

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

**发卡系统（开源软件，自建用）**

| 系统 | 仓库 | 说明 |
|---|---|---|
| 独角数卡 | https://github.com/assimon/dujiaoka | PHP/Laravel，自建最主流 |
| 异次元发卡 | https://github.com/lizhipay/acg-faka | PHP，二次元风，多商户 |
| ZFAKA | - | PHP，2025 年更新到 1.4.6 |
| Orion Key | https://github.com/RivenLau/orion-key | React+Next.js+Spring Boot |
| 萌次元商城系统 | https://wiki.mcy.im | 分站/插件体系 |

## 发卡 · Gemini Pro 低价 Top 15

| 商品 | 价格(¥) | 店铺 | 归属 | 来源 |
|---|---|---|---|---|
| Google AI Pro会员 学生会员一年续期【要有学生资格认证的号】 | ¥0.01 | RenWin | 未知SaaS(wzyp.cn) | OpenPrice |
| Gemini3个月Pro激活链接\|需要绑卡\|可使用反重力\| | ¥2.58 | GPT-源头供货-招代理 | 未知SaaS(wzyp.cn) | OpenPrice |
| Gemini3个月Pro激活链接\|需要绑卡\|可使用反重力\| | ¥3.61 | 梦泽 | 未知SaaS(wzyp.cn) | OpenPrice |
| Gemini Pro 18个月 Google One 5TB（兑换链接,不需要绑卡 | ¥3.91 | RenWin | 未知SaaS(wzyp.cn) | OpenPrice |
| Gemini 3.5pro家庭组（月卡） | ¥3.98 | Ai俱乐部 | 链动小铺 | AI号探 |
| Gemini Pro  3个月链接 | ¥4 | 以太 AI服务订阅充值 | 自建/未知 | OpenPrice |
| Gemini3个月Pro激活链接\|需要绑卡\|可使用反重力\| | ¥4.02 | YaHo🐯GPT全网低价 | 未知SaaS(wzyp.cn) | OpenPrice |
| （1个起）Google ai pro三个月领取优惠链接（couresa渠道） | ¥4.5 | AI 能量小店 | 自建/未知 | OpenPrice |
| JIO Gemini pro 18个月 兑换链接 \| 考虑售后请提前录屏 | ¥4.53 | IKUN货源 | 未知SaaS(wzyp.cn) | OpenPrice |
| 【绝版】Gemini Pro 18个月 Google One 5TB（兑换链接 | ¥4.64 | 双子星AI | 未知SaaS(wzyp.cn) | OpenPrice |
| JIO Gemini pro 18个月 兑换链接 \| 考虑售后请提前录屏 | ¥4.86 | GGbond ai | 未知SaaS(wzyp.cn) | OpenPrice |
| Gemini AI Pro 18个月权益【官方链接直接领取】无质保~ | ¥5.1 | RenWin | 未知SaaS(wzyp.cn) | OpenPrice |
| Gemini 18个月 pro 特价出一批 群友特供  不是成品看清楚（活动10月25日结束 | ¥5.15 | gemini源头直供 | 未知SaaS(wzyp.cn) | OpenPrice |
| Gemini AI Pro 18个月权益【官方链接直接领取】无质保~ | ¥5.47 | GGbond ai | 未知SaaS(wzyp.cn) | OpenPrice |
| Gemini18个月Pro激活链接\|无需绑卡\|可使用反重力\|直接激活\| | ¥5.83 | GGbond ai | 未知SaaS(wzyp.cn) | OpenPrice |

## 发卡 · Google AI Ultra 20x Top 15

| 商品 | 价格(¥) | 店铺 | 归属 | 来源 |
|---|---|---|---|---|
| Google AI Ultra 20x【质保订阅】支持Antigravity反重力｜家庭组邀 | ¥203.0 | 懂你AI的小铺 | 链动小铺 | AI号探 |
| Google AI Ultra 20x【质保订阅】支持Antigravity反重力｜家庭组邀 | ¥203.04 | 如鱼得水(玩转ai) | 链动小铺 | AI号探 |
| 【全程质保30天】Gemini Ultra 20x 家庭组席位\|随机Flow积分 | ¥204.85 | Tim的AI便利店 | 未知SaaS(wzyp.cn) | OpenPrice |
| Google AI Ultra 20x【质保订阅】支持Antigravity反重力｜家庭组邀 | ¥206.8 | 各类低价对接汇总 | 链动小铺 | AI号探 |
| Google AI Ultra 20x【质保订阅】支持Antigravity反重力｜家庭组邀 | ¥206.8 | 牟利ai | 链动小铺 | AI号探 |
| Veo3.1-无积分的Ultra20x企业版【不可以用反重力】 | ¥210 | 全网最低批发ai账号 | 自建/未知 | OpenPrice |
| Google AI Ultra 20x【质保订阅】支持Antigravity反重力｜家庭组邀 | ¥218.0 | 奥特曼严选 | 链动小铺 | AI号探 |
| Google AI Ultra 20x【质保订阅】支持Antigravity反重力｜家庭组邀 | ¥224.54 | 奥特曼严选 | 未知SaaS(wzyp.cn) | OpenPrice |
| Google AI Ultra 20x【质保订阅】支持Antigravity反重力｜家庭组邀 | ¥225.6 | 比特拈花 | 链动小铺 | AI号探 |
| Google AI Ultra 20x【质保订阅】支持Antigravity反重力｜家庭组邀 | ¥225.6 | ai小头 | 链动小铺 | AI号探 |
| Google AI Ultra 20x【质保订阅】支持Antigravity反重力｜家庭组邀 | ¥232.37 | 比特拈花 | 未知SaaS(wzyp.cn) | OpenPrice |
| Google AI Ultra 20x【质保订阅】支持Antigravity反重力｜家庭组邀 | ¥236.88 | 小🐏阳AI精选店 | 链动小铺 | AI号探 |
| Google AI Ultra 20x【质保订阅】支持Antigravity反重力｜家庭组邀 | ¥238.0 | 胡小阳的AI店铺（招代理） | 链动小铺 | AI号探 |
| Google AI Ultra 20x【质保订阅】支持Antigravity反重力｜家庭组邀 | ¥245.14 | （彩虹马）筱博的小店 | 未知SaaS(wzyp.cn) | OpenPrice |
| Google AI Ultra 20x【质保订阅】支持Antigravity反重力｜家庭组邀 | ¥263.2 | 🐓PT-Plus | 链动小铺 | AI号探 |

## 发卡 · 店铺速览（按商品数 Top 20）

| 店铺 | 归属 | 品类 | 价位(¥) | 来源 |
|---|---|---|---|---|
| GGbond ai | 未知SaaS(wzyp.cn) | ChatGPT/Claude/Cursor/Gemini/Gemini Ultra/Grok/Kiro/其它/邮箱 | 0.12-11433 | OpenPrice |
| 梦泽 | 未知SaaS(wzyp.cn) | ChatGPT/Claude/Cursor/Gemini/Gemini Ultra/Grok/Kiro/其它/邮箱 | 0.01-3325.87 | AI号探/OpenPrice |
| Alexander | 未知SaaS(wzyp.cn) | ChatGPT/Claude/Cursor/Gemini/Gemini Ultra/Grok/Kiro/其它/邮箱 | 0-3419.6 | AI号探/OpenPrice |
| harvey | 未知SaaS(wzyp.cn) | ChatGPT/Claude/Cursor/Gemini/Gemini Ultra/Grok/Kiro/其它/邮箱 | 0.06-2263.73 | OpenPrice |
| 派大星 | 未知SaaS(wzyp.cn) | ChatGPT/Claude/Cursor/Gemini/Gemini Ultra/Grok/Kiro/其它/邮箱 | 0.06-2263.73 | OpenPrice |
| chiyu | 未知SaaS(wzyp.cn) | ChatGPT/Claude/Cursor/Gemini/Gemini Ultra/Grok/Kiro/其它/邮箱 | 0.04-3440.2 | AI号探/OpenPrice |
| 🛍 壹号铺 | 未知SaaS(wzyp.cn) | ChatGPT/Claude/Cursor/Gemini/Gemini Ultra/Grok/Kiro/其它/邮箱 | 0.04-5665 | OpenPrice |
| AccHarbor | 自建/未知 | 其它/邮箱 | 0.9-1073.04 | OpenPrice |
| 陆柒科技 | 未知SaaS(wzyp.cn) | ChatGPT/Claude/Cursor/Gemini/其它/邮箱 | 0.32-2884 | AI号探/OpenPrice |
| team最后的余晖 | 未知SaaS(wzyp.cn) | ChatGPT/Claude/Gemini/Gemini Ultra/Grok/其它/邮箱 | 0.07-10300 | AI号探/OpenPrice |
| 比特拈花 | 未知SaaS(wzyp.cn) | ChatGPT/Claude/Cursor/Gemini/Gemini Ultra/Grok/Kiro/其它/邮箱 | 0-3625.6 | AI号探/OpenPrice |
| 自行车 Ai 店铺 | 未知SaaS(wzyp.cn) | ChatGPT/Claude/Gemini/Grok/Kiro/其它/邮箱 | 0.04-3499.94 | AI号探/OpenPrice |
| Xm API | 未知SaaS(wzyp.cn) | ChatGPT/Claude/Cursor/Gemini/Gemini Ultra/其它/邮箱 | 0.07-102999 | OpenPrice |
| RenWin | 未知SaaS(wzyp.cn) | ChatGPT/Claude/Cursor/Gemini/Kiro/其它/邮箱 | 0-3347.5 | OpenPrice |
| （彩虹马）筱博的小店 | 未知SaaS(wzyp.cn) | ChatGPT/Claude/Cursor/Gemini/Gemini Ultra/Grok/其它/邮箱 | 1.99-3296 | OpenPrice |
| 橙子AI源头(全网最低源头) | 未知SaaS(wzyp.cn) | ChatGPT/Claude/Gemini/Grok/其它/邮箱 | 0.01-1812.8 | OpenPrice |
| 奥特曼严选 | 未知SaaS(wzyp.cn) | ChatGPT/Cursor/Gemini/Gemini Ultra/Grok/Kiro/其它/邮箱 | 0.21-1122.7 | AI号探/OpenPrice |
| YaHo🐯GPT全网低价 | 未知SaaS(wzyp.cn) | ChatGPT/Claude/Gemini/Kiro/其它/邮箱 | 0-3285.7 | OpenPrice |
| recardai | 未知SaaS(wzyp.cn) | ChatGPT/Claude/Gemini/其它/邮箱 | 0.1-1895.2 | OpenPrice |
| ai小头 | 未知SaaS(wzyp.cn) | ChatGPT/Claude/Gemini/Gemini Ultra/Grok/其它/邮箱 | 1.13-1461.57 | AI号探/OpenPrice |

## 目录

```
data/relays/relays.csv          中转站主表
data/relays/relay-models.csv    站×模型×价格（12774 条）
data/relays/relay-systems.csv   中转站软件名录
data/relays/by-model/*.md       143 个模型榜单
data/shops/platforms.csv        发卡平台
data/shops/systems.csv          发卡系统
data/shops/shops.csv            店铺主表
data/shops/products.csv         商品报价（10646 条）
data/raw/                       原始产物与溯源
docs/                           价格原理/黑话表/选购指南
tools/                          抓取、归一化、查询
```

## 数据来源

OpenPrice、水獭比价(shuita.xyz)、PriceAI、AI号探、AiFaKa、Veridrop，以及各中转站公开的 `/api/pricing`、`/api/v1/model-plaza`。原始报价版权归各来源站，见 [DATA-LICENSE.md](DATA-LICENSE.md)。

## 授权

- 代码 **MIT** · [LICENSE](LICENSE)
- 编排与整理 **CC BY-NC 4.0** · [DATA-LICENSE.md](DATA-LICENSE.md)
- 原始报价版权归各来源站

## 贡献

见 [CONTRIBUTING.md](CONTRIBUTING.md)。
