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
- [中转站 · 疑似同后端](#backend)
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
| 中转站（去重后） | 4801（首页可访问 4603） |
| 合并的别名/镜像域名 | 3908 |
| 已剔除的泛解析子域 | 5457 |
| 站 × 模型 报价 | 227541 |
| 基础模型数（不同模型，非站数） | 11654 |
| 公开充值价的站 | 2391（≤¥1.5/$ 的 1343 站，≥¥6/$ 的 1013 站） |
| 发卡店铺 | 430（SaaS 348 / 自建 82） |
| 发卡商品报价 | 17212 |

更多分布见 [data/stats.md](data/stats.md)。

<a id="quickstart"></a>
## 快速开始

```bash
git clone https://github.com/ruruamour/ai-relay-atlas.git && cd ai-relay-atlas
python3 tools/query.py model gemini-4-argon      # 某模型哪些站有、什么价
python3 tools/query.py site api.openlux.ai       # 某站的全部模型（别名会自动换成主域名）
bash tools/build.sh                              # 改数据后重建：去重 → 榜单 → 统计 → README
```

<a id="relays"></a>
## 中转站 · 综合名单

| # | 站点 | 站名 | 系统 | 模型数 | 覆盖 | 充值 ¥/$ | Veridrop | 状态 | 延迟 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `subrouter.ai` | SubRouter | New-API | 1490 | OCGXMD | 6.8 | - | 200 | 3775ms |
| 2 | `kfcv50.link` | KFC V50 API | New-API | 1398 | OCGXMD | 1 | - | 200 | 1759ms |
| 3 | `api2.aigcbest.top` | 钱多多 API | New-API | 1311 | OCGXMD | 3.5 | - | 200 | 1685ms |
| 4 | `ai.comfly.org` | comfly | New-API | 1131 | OCGXMD | - | 100 | 200 | 2060ms |
| 5 | `ai.t8star.org` | Zhenzhen's WorkSho… | New-API | 1131 | OCGXMD | 1.35 | - | 200 | 7910ms |
| 6 | `api.bltcy.ai` | 柏拉图AI | New-API | 1131 | OCGXMD | 1 | - | 200 | 4024ms |
| 7 | `openai.sharkmagic.top` | 鲨鱼魔法 | New-API | 1089 | OCGXMD | - | - | 200 | 3133ms |
| 8 | `newapi.hebin123.com` | Hebin-API | New-API | 1037 | OCGXMD | 7.3 | - | 200 | 117ms |
| 9 | `ai.soruxgpt.com` | SoruxGPT | New-API | 969 | OCGXMD | 1 | - | 200 | 2345ms |
| 10 | `open.selart.cc` | 赛艺API | New-API | 858 | OCGXD | 1 | - | 200 | 1393ms |
| 11 | `ai2.qiqiai.top` | AI2 | New-API | 727 | OCGXMD | 7.3 | - | 200 | 1739ms |
| 12 | `api.qhhengxin.top` | api.qhhengxin.top | New-API | 717 | OCGXD | - | - | 200 | 2303ms |
| 13 | `www.hohoapi.com` | HoHoApi | New-API | 703 | OCGXD | 3 | - | 200 | 1636ms |
| 14 | `api.holdai.top` | 毫秒API | New-API | 701 | OCGXD | 1.2 | - | 200 | 1898ms |
| 15 | `api.tu-zi.com` | 兔子API | New-API | 662 | OCGXD | 0.7 | - | 200 | 888ms |
| 16 | `api.zyai.online` | Yun API | New-API | 651 | OCGXD | 1 | 71 | 200 | 1553ms |
| 17 | `api.aliyunfuwu.top` | Top API | New-API | 649 | OCGXD | 1 | - | 200 | 2936ms |
| 18 | `newapi.link` | - | New-API | 643 | OCGXMD | 1 | - | 200 | 1488ms |
| 19 | `daoxe.com` | DaoXE | New-API | 621 | OCGXMD | 1.03 | - | 200 | 1273ms |
| 20 | `api.ocoolai.com` | ocoolAI | New-API | 616 | OCGXD | 1 | - | 200 | 2968ms |
| 21 | `ocool.cn` | ocoolAI | New-API | 616 | OCGXD | 1 | - | 200 | 1380ms |
| 22 | `api.wukong.support` | 悟空API | New-API | 613 | OCGXD | 1 | 68 | 200 | 2470ms |
| 23 | `api.qinzhiai.com` | ClaudeHub | New-API | 591 | OCGXMD | 1 | - | 200 | 1027ms |
| 24 | `botcf.com` | Bot Compute Fabric | New-API | 585 | OCGXMD | 1 | 95 | 200 | 2288ms |
| 25 | `www.ggwk1.online` | ggwk1 API | New-API | 582 | OCGXMD | 1 | - | 200 | 2740ms |
| 26 | `kubernetes-test-api.apiqik.online` | - | New-API | 572 | OCGXD | 7.3 | - | 200 | 1176ms |
| 27 | `api.camel-hub.com` | CaMeL AI | New-API | 556 | OCGXMD | 0.8 | - | 200 | 4471ms |
| 28 | `api.34ku.com` | 速通Api | New-API | 552 | OCGXMD | 1 | - | 200 | 2943ms |
| 29 | `wrduai.com` | WrduAI | New-API | 552 | OCGXD | 7.3 | - | 200 | 107ms |
| 30 | `hk.chenmoai.cn` | 沉默API | New-API | 543 | OCGXD | 1 | - | 200 | 395ms |
| 31 | `keypool.space` | 云创算力 | New-API | 539 | OCGXMD | 1 | - | 200 | 2394ms |
| 32 | `suanliai.top` | 算力AI | New-API | 537 | OCGXD | 1 | - | 200 | 2026ms |
| 33 | `api.hopeai.cc` | HopeAPI | New-API | 522 | OCGXD | 1 | - | 200 | 1221ms |
| 34 | `api.qiqiai.top` | 星AI | New-API | 517 | OCGXMD | 2 | - | 200 | 1316ms |
| 35 | `n.lconai.com` | 智创聚合API | New-API | 504 | OCGXD | 1 | - | 200 | 1365ms |
| 36 | `cn.gptapi.asia` | YutoAPI | New-API | 502 | OCGXMD | 1 | 58 | 200 | 1990ms |
| 37 | `yutoapi.com` | YutoAPI | New-API | 502 | OCGXMD | 1 | - | 200 | 3199ms |
| 38 | `api.tacklekey.com` | TackleKey | New-API | 500 | OCGXMD | 7.3 | - | 200 | 1993ms |
| 39 | `xiaoqie.xyz` | 小企鹅.xyz | New-API | 497 | OCGXMD | - | - | 200 | 1908ms |
| 40 | `api.openai365.top` | OpenAi API | New-API | 493 | OCGXD | - | - | 200 | 216ms |
| 41 | `poloai.top` | PoloAPI | New-API | 490 | OCGXD | 1 | 98 | 200 | 2009ms |
| 42 | `poloapi.top` | PoloAPI | New-API | 490 | OCGXD | - | 88 | 200 | 2301ms |
| 43 | `llm.kagu.one` | KaguAPI | New-API | 490 | OCGXMD | 7.3 | - | 200 | 3519ms |
| 44 | `test.yibuapi.com` | 一步API | New-API | 482 | OCGMD | 1.5 | - | 200 | 2379ms |
| 45 | `api.routeeasy.ai` | RouteEasy | New-API | 480 | OCGXD | 1 | 86 | 200 | 1497ms |
| 46 | `go.sbgpt.site` | 中转货源API | New-API | 477 | OCGXD | 1 | - | 200 | 927ms |
| 47 | `api.vectorengine.ai` | 向量引擎 | New-API | 469 | OCGXMD | - | 96 | 200 | 2502ms |
| 48 | `www.xiaoruiera.top` | 极速链API | New-API | 469 | OCGXMD | - | 84 | 200 | 1549ms |
| 49 | `ai.kalehui.cn` | 中转API | New-API | 469 | OCGXMD | - | - | 200 | 985ms |
| 50 | `aiopus.top` | AIOPUS | New-API | 469 | OCGXMD | - | - | 200 | 2248ms |
| 51 | `api.anthropicricardo.club` | 江南💗赫尔佐格 | New-API | 469 | OCGXMD | - | - | 200 | 2104ms |
| 52 | `api.gpt666claude.top` | 朔风api(找客服0.6一刀) | New-API | 469 | OCGXMD | - | - | 200 | 2134ms |
| 53 | `api.token173.net` | Token173 | New-API | 469 | OCGXMD | - | - | 200 | 1823ms |
| 54 | `api.zhongzhuan.vip` | 向量引擎 | New-API | 469 | OCGXMD | - | - | 200 | 1994ms |
| 55 | `apistudio.vip` | 灵境 API | New-API | 469 | OCGXMD | - | - | 200 | 2173ms |
| 56 | `juhe.34ku.com` | 速通-API | New-API | 469 | OCGXMD | - | - | 200 | 2683ms |
| 57 | `one.chatshare.one` | ChatShare API | New-API | 469 | OCGXMD | - | - | 200 | 1202ms |
| 58 | `tiantoken.cn` | 时迈风 | New-API | 469 | OCGXMD | - | - | 200 | 904ms |
| 59 | `token.kkdmx.com` | KK大模型 | New-API | 469 | OCGXMD | - | - | 200 | 2708ms |
| 60 | `vortexapi.cn` | 芒果API | New-API | 469 | OCGXMD | - | - | 200 | 1922ms |
| 61 | `yuli.host` | 玉玉API_接口 | New-API | 469 | OCGXMD | - | - | 200 | 5796ms |
| 62 | `dawnnode.com` | 黎明智汇 | New-API | 468 | OCGXMD | - | - | 200 | 1991ms |
| 63 | `ruishiglobal.com` | SuperAI公园 | New-API | 467 | OCGXMD | - | - | 200 | 1820ms |
| 64 | `api.uiuihao.com` | UiUiAPI聚合平台 | New-API | 465 | OCGXD | 3.19 | - | 200 | 6243ms |
| 65 | `api.wapq.cn` | LivenHub | New-API | 465 | OCGXMD | 7.3 | - | 200 | 369ms |
| 66 | `api.zhiyikeji.cn` | 千枢词元 | New-API | 465 | OCGXMD | - | - | 200 | 1045ms |
| 67 | `sg.uiuiapi.com` | UiUiAPI聚合平台 | New-API | 465 | OCGXD | 3.19 | - | 200 | 1756ms |
| 68 | `top.qingyuntop.top` | 青云TOP API国际站 | New-API | 444 | OCGXMD | 1 | - | 200 | 188ms |
| 69 | `aws.baby` | 企业级 AI 网关 | New-API | 427 | OCGMD | 1 | - | 200 | 1734ms |
| 70 | `api.luoqianyi.qzz.io` | 迁忆 | New-API | 423 | OCGXMD | - | - | 200 | 3134ms |
| 71 | `magic666.top` | 即刻AI - 即刻拥抱最新AI技术 | New-API | 418 | OCGXD | 1 | 80 | 200 | 2453ms |
| 72 | `api.bianxie.ai` | 便携AI聚合API | New-API | 414 | OCGXMD | 7.3 | - | 200 | 2379ms |
| 73 | `or.mux.la` | - | New-API | 414 | OCGXMD | - | - | 200 | 1685ms |
| 74 | `claudecn.ai` | ClaudeCN | New-API | 413 | OCMD | 1 | - | 200 | 3567ms |
| 75 | `max.openai365.top` | 美团团 API | New-API | 411 | OCGXMD | 7.3 | 77 | 200 | 314ms |
| 76 | `yibuapi.com` | 一步API | New-API | 408 | OCGXMD | 1.5 | - | 200 | 3153ms |
| 77 | `new.yihubang.top` | 小护 | New-API | 398 | OCXMD | 1 | - | 200 | 1788ms |
| 78 | `api1.uiuiapi.com` | UiUi API聚合 | New-API | 393 | OCGX | 3.37 | - | 200 | 1079ms |
| 79 | `hk.moleapi.com` | MoleAPI | New-API | 392 | OCGXMD | 6.8 | - | 200 | 4183ms |
| 80 | `webapi.xjai.cc` | - | New-API | 390 | OCGXD | 3 | - | 200 | 872ms |
| 81 | `azapi.com.cn` | AZ | New-API | 387 | OCGXD | - | - | 200 | 1826ms |
| 82 | `rockapi.ai` | Rock API | New-API | 386 | OCGXMD | 1 | - | 200 | 3139ms |
| 83 | `wish.sillydream.top` | SillyDream | New-API | 382 | OCGXD | - | - | 200 | 2250ms |
| 84 | `www.9915654.ggff.net` | 后羿AI中转站 | New-API | 379 | OCGXMD | 7.3 | - | 200 | 1521ms |
| 85 | `anyaigc.com` | AnyAIGC - API中转站 | New-API | 378 | OCGXMD | - | 100 | 200 | 1514ms |
| 86 | `api.winfull.cloud-ip.cc` | 伝富AI | New-API | 378 | OCGXMD | - | 100 | 200 | 4528ms |
| 87 | `api.qingyuntop.top` | 青云聚合API | New-API | 378 | OCGXMD | - | 96 | 200 | 2611ms |
| 88 | `api.zhongzhuan.chat` | 云雾 API | New-API | 378 | OCGXMD | - | 95 | 200 | 1566ms |
| 89 | `vipapi.online` | 流星API | New-API | 378 | OCGXMD | - | 95 | 200 | 3459ms |
| 90 | `yunwu.ai` | 云雾 API | New-API | 378 | OCGXMD | - | 90 | 200 | 3068ms |
| 91 | `aiapihub.cloud` | 智联API | New-API | 378 | OCGXMD | - | - | 200 | 1575ms |
| 92 | `aiyiwei.vip` | 聚合api | New-API | 378 | OCGXMD | - | - | 200 | 3969ms |
| 93 | `api-hub.vip` | 云柏 API | New-API | 378 | OCGXMD | - | - | 200 | 2796ms |
| 94 | `api.aibh.site` | 空氧API-可以继续使用 | New-API | 378 | OCGXMD | - | - | 200 | 1725ms |
| 95 | `api.aicso.top` | 灵汐API | New-API | 378 | OCGXMD | - | - | 200 | 2545ms |
| 96 | `api.antmoo.com` | AntMoo API | New-API | 378 | OCGXMD | - | - | 200 | 1602ms |
| 97 | `api.apiplus.org` | 云雾 API | New-API | 378 | OCGXMD | - | - | 200 | 1973ms |
| 98 | `api.bitidea.cn` | 小小思路API | New-API | 378 | OCGXMD | - | - | 200 | 1959ms |
| 99 | `api.clai.click` | CLAI API | New-API | 378 | OCGXMD | - | - | 200 | 2771ms |
| 100 | `api.cloudmist.cloud` | 云岚API | New-API | 378 | OCGXMD | - | - | 200 | 4363ms |

⚠️ 标记的站点见 [aliases/标注说明](data/README.md#标注annotationscsv)；目前 1 个。

覆盖：O=OpenAI · C=Claude · G=Gemini · X=Grok · M=MiMo · D=DeepSeek。充值 ¥/$：站点公开的"多少元买 1 美元额度"，实付价 = 名义价 × 充值价。

完整名单（4801 站）：[relays.csv](data/relays/relays.csv) · 别名：[aliases.csv](data/relays/aliases.csv) · 报价：[relay-models.csv](data/relays/relay-models.csv)

[↑ 目录](#toc)

<a id="coverage"></a>
## 中转站 · 模型覆盖

| 家族 | 基础模型数 | 覆盖站点 | 覆盖最广的模型 |
|---|---|---|---|
| OpenAI | 1369 | 2326 | [gpt-5.6-sol](data/relays/by-model/gpt-5.6-sol.md) · [gpt-5.6-terra](data/relays/by-model/gpt-5.6-terra.md) · [gpt-6-astra](data/relays/by-model/gpt-6-astra.md) |
| Claude | 1018 | 2104 | [claude-opus-4-8](data/relays/by-model/claude-opus-4-8.md) · [claude-opus-4-6](data/relays/by-model/claude-opus-4-6.md) · [claude-opus-4-7](data/relays/by-model/claude-opus-4-7.md) |
| Gemini | 1465 | 1688 | [gemini-3.8-flash](data/relays/by-model/gemini-3.8-flash.md) · [gemini-3.1-pro-preview](data/relays/by-model/gemini-3.1-pro-preview.md) · [gemini-3.6-flash](data/relays/by-model/gemini-3.6-flash.md) |
| Grok | 335 | 1563 | [grok-4.5](data/relays/by-model/grok-4.5.md) · [grok-4.6](data/relays/by-model/grok-4.6.md) · [grok-4.7](data/relays/by-model/grok-4.7.md) |
| MiMo | 44 | 562 | [mimo-v2.5-pro](data/relays/by-model/mimo-v2.5-pro.md) · [mimo-v2.5](data/relays/by-model/mimo-v2.5.md) · [mimo-v2.6-flash](data/relays/by-model/mimo-v2.6-flash.md) |
| DeepSeek | 298 | 1672 | [deepseek-v4-pro](data/relays/by-model/deepseek-v4-pro.md) · [deepseek-v4-flash](data/relays/by-model/deepseek-v4-flash.md) · [deepseek-v4.1-flash](data/relays/by-model/deepseek-v4.1-flash.md) |
| Qwen | 618 | 1021 | [qwen3.8-max](data/relays/by-model/qwen3.8-max.md) · [qwen3.7-max](data/relays/by-model/qwen3.7-max.md) · [qwen3.8-flash](data/relays/by-model/qwen3.8-flash.md) |
| GLM | 228 | 1464 | [glm-5.3](data/relays/by-model/glm-5.3.md) · [glm-5.2](data/relays/by-model/glm-5.2.md) · [glm-5.3-flash](data/relays/by-model/glm-5.3-flash.md) |
| Kimi | 101 | 1334 | [kimi-k3](data/relays/by-model/kimi-k3.md) · [kimi-k2.6](data/relays/by-model/kimi-k2.6.md) · [kimi-k2.7-code](data/relays/by-model/kimi-k2.7-code.md) |
| 豆包 | 715 | 664 | [doubao-seedream-5-0](data/relays/by-model/doubao-seedream-5-0.md) · [doubao-seed-2-1-pro](data/relays/by-model/doubao-seed-2-1-pro.md) · [doubao-seed-2-0-pro](data/relays/by-model/doubao-seed-2-0-pro.md) |
| MiniMax | 295 | 944 | [minimax-m3](data/relays/by-model/minimax-m3.md) · [minimax-m2.7](data/relays/by-model/minimax-m2.7.md) · [minimax-m2.5](data/relays/by-model/minimax-m2.5.md) |
| 混元 | 52 | 376 | [hy3](data/relays/by-model/hy3.md) · [hy4-preview](data/relays/by-model/hy4-preview.md) · [hy4](data/relays/by-model/hy4.md) |
| Llama | 113 | 212 | [llama-3.2-11b-vision-instruct](data/relays/by-model/llama-3.2-11b-vision-instruct.md) · [llama-3.2-90b-vision-instruct](data/relays/by-model/llama-3.2-90b-vision-instruct.md) · [llama-3.2-1b-instruct](data/relays/by-model/llama-3.2-1b-instruct.md) |
| 图像/视频/音频 | 922 | 410 | [z-image-turbo](data/relays/by-model/z-image-turbo.md) · [happyhorse-1.1-t2v](data/relays/by-model/happyhorse-1.1-t2v.md) · [happyhorse-1.1-r2v](data/relays/by-model/happyhorse-1.1-r2v.md) |
| 其他 | 4081 | 1005 | [bge-reranker-v2-m3](data/relays/by-model/bge-reranker-v2-m3.md) · [sparkdesk-v3.1](data/relays/by-model/sparkdesk-v3.1.md) · [sparkdesk-v1.1](data/relays/by-model/sparkdesk-v1.1.md) |

全部 829 个模型榜单：[by-model/index.md](data/relays/by-model/index.md)

[↑ 目录](#toc)

<a id="backend"></a>
## 中转站 · 疑似同后端

价格表完全相同的跨品牌站点，共 109 组 / 296 站。前 15 组：

| 组 | 站数 | 站点 |
|---|---|---|
| B001 | 46 | `aiapihub.cloud` · `aiyiwei.vip` · `anyaigc.com` · `api-hub.vip` · `api.aibh.site` · `api.aicso.top` … |
| B002 | 15 | `ai.kalehui.cn` · `aiopus.top` · `api.anthropicricardo.club` · `api.gpt666claude.top` · `api.token173.net` · `api.vectorengine.ai` … |
| B003 | 11 | `aiwuje.com` · `api.echoflowai.cc` · `api.n1n.ai` · `api.quickrouter.ai` · `jeniya.cn` · `linoapi.com` … |
| B004 | 4 | `api.88api.chat` · `api.videocaptioner.cn` · `new.aigc2d.com` · `oyy-ai.xyz` |
| B005 | 4 | `api.chatshare.one` · `api.tiantoken.com` · `tidewhisper-ai.xyz` · `token.34ku.com` |
| B006 | 3 | `88.api456.me` · `api.supxh.xin` · `speed23.toter.me` |
| B007 | 3 | `api.buzzgw.com` · `buzzai.cc` · `claude.buzz7.top` |
| B008 | 3 | `api.dawclaudecode.com` · `dawcode.com` · `dawvip.com` |
| B009 | 3 | `api.tidewhisper-ai.xyz` · `gzxbykj.com` · `yunwu.org` |
| B010 | 3 | `cdn.juaiapi.com` · `www.juapi.net` · `www.tokenrouter.tech` |
| B011 | 3 | `ciyuan.today` · `gptapi.top` · `makerend.com` |
| B012 | 3 | `comeu.ai` · `keuapi.com` · `keutoken.com` |
| B013 | 3 | `niuniutoken.com` · `purecall.cc` · `tokendawang.com` |
| B014 | 2 | `1024token.cc` · `aitokenyes.com` |
| B015 | 2 | `107.167.18.218` · `api.zhengmi.org` |

[↑ 目录](#toc)

<a id="shops"></a>
## 卡网 · 店铺名单

| # | 店铺 | 归属 | 卖什么 | 价位(¥) | 来源 |
|---|---|---|---|---|---|
| 1 | GGbond ai | 链动小铺 | GPT/Claude/Cursor/Gemini/Ultra/Grok/Kiro/邮箱 | 0.12-11433 | OpenPrice |
| 2 | 🐓PT-Plus | 链动小铺 | GPT/Claude/Cursor/Gemini/Ultra/Grok/邮箱 | 0.04-10300 | AI号探/OpenPrice |
| 3 | AI OPC | 链动小铺 | GPT/Claude/Cursor/Gemini/Ultra/Grok/Kiro/邮箱 | 0.01-4802.38 | OpenPrice |
| 4 | AI大集市 | 链动小铺 | GPT/Claude/Cursor/Gemini/Ultra/Grok/邮箱 | 0.01-25605.8 | OpenPrice |
| 5 | 小🐏阳AI精选店 | 链动小铺 | GPT/Claude/Cursor/Gemini/Ultra/Grok/邮箱 | 0.09-3818 | AI号探/OpenPrice |
| 6 | 爪爪AI专卖(对接实力号商) | 链动小铺 | GPT/Claude/Cursor/Gemini/Ultra/Grok/Kiro/邮箱 | 0.05-6004.9 | OpenPrice |
| 7 | 哪都通临时工 | 链动小铺 | GPT/Claude/Cursor/Gemini/Ultra/Grok/邮箱 | 0.02-10300 | AI号探/OpenPrice |
| 8 | 梦泽 | 链动小铺 | GPT/Claude/Cursor/Gemini/Ultra/Grok/Kiro/邮箱 | 0.01-3285.7 | AI号探/OpenPrice |
| 9 | Alexander | 链动小铺 | GPT/Claude/Cursor/Gemini/Ultra/Grok/Kiro/邮箱 | 0-3419.6 | AI号探/OpenPrice |
| 10 |  👑XAI店铺（全品类✨超市）🔥 | 16688 | GPT/Claude/Cursor/Gemini/Ultra/Grok/Kiro/邮箱 | 0.02-5505.82 | OpenPrice |
| 11 | harvey | 链动小铺 | GPT/Claude/Cursor/Gemini/Ultra/Grok/Kiro/邮箱 | 0.08-3171.27 | OpenPrice |
| 12 | 派大星 | 链动小铺 | GPT/Claude/Cursor/Gemini/Ultra/Grok/Kiro/邮箱 | 0.08-3171.27 | OpenPrice |
| 13 | 鹰鹰小铺 | 链动小铺 | GPT/Claude/Gemini/Ultra/Grok/Kiro/邮箱 | 0-2090.64 | OpenPrice |
| 14 | chiyu | 链动小铺 | GPT/Claude/Cursor/Gemini/Ultra/Grok/Kiro/邮箱 | 0.04-3399 | AI号探/OpenPrice |
| 15 | 🛍 壹号铺 | 链动小铺 | GPT/Claude/Cursor/Gemini/Ultra/Grok/Kiro/邮箱 | 0.04-5665 | OpenPrice |
| 16 | AccHarbor | 自建/异次元发卡 | 邮箱 | 0.9-1070.62 | OpenPrice |
| 17 | 晨风Ai｜源头直供 | 链动小铺 | GPT/Claude/Cursor/Gemini/Ultra/Grok/邮箱 | 0.05-14214 | OpenPrice |
| 18 | 陆柒科技 | 链动小铺 | GPT/Claude/Cursor/Gemini/邮箱 | 0.32-2884 | AI号探/OpenPrice |
| 19 | 比特拈花 | 链动小铺 | GPT/Claude/Cursor/Gemini/Ultra/Grok/Kiro/邮箱 | 0-3625.6 | AI号探/OpenPrice |
| 20 | team最后的余晖 | 链动小铺 | GPT/Claude/Gemini/Ultra/Grok/邮箱 | 0.07-10300 | AI号探/OpenPrice |
| 21 | 自行车 Ai 店铺 | 链动小铺 | GPT/Claude/Gemini/Grok/Kiro/邮箱 | 0.04-3499.94 | AI号探/OpenPrice |
| 22 | Xm API | 链动小铺 | GPT/Claude/Cursor/Gemini/Ultra/Grok/邮箱 | 0.07-102999 | OpenPrice |
| 23 | 奥特曼严选 | 链动小铺 | GPT/Gemini/Ultra/Grok/Kiro/邮箱 | 0.21-1102.1 | AI号探/OpenPrice |
| 24 | RenWin | 链动小铺 | GPT/Claude/Cursor/Gemini/Kiro/邮箱 | 0-3306.3 | OpenPrice |
| 25 | （彩虹马）筱博的小店 | 链动小铺 | GPT/Claude/Cursor/Gemini/Ultra/Grok/邮箱 | 1.99-3296 | OpenPrice |
| 26 | 橙子AI源头(全网最低源头) | 链动小铺 | GPT/Claude/Gemini/Grok/邮箱 | 0.01-1699.5 | OpenPrice |
| 27 | recardai | 链动小铺 | GPT/Claude/Cursor/Gemini/Ultra/Grok/邮箱 | 0.1-1895.2 | OpenPrice |
| 28 | 源头AI - Bot | 链动小铺 | GPT/Claude/Gemini/Ultra/Grok/邮箱 | 0.26-3656.5 | OpenPrice |
| 29 | ai教父 | 链动小铺 | GPT/Claude/Gemini/Ultra/Grok/邮箱 | 0.1-3512.3 | AI号探/OpenPrice |
| 30 | YaHo🐯GPT全网低价 | 链动小铺 | GPT/Claude/Gemini/Grok/Kiro/邮箱 | 0-3285.7 | OpenPrice |
| 31 | 稳中求胜 | 链动小铺 | GPT/Claude/Cursor/Gemini/Ultra/Grok/邮箱 | 0.14-3244.5 | OpenPrice |
| 32 | 商家8719 | 链动小铺 | GPT/Claude/Gemini/Ultra/Grok/Kiro/邮箱 | 0.21-5665 | OpenPrice |
| 33 | 一梦低价货源 | 链动小铺 | GPT/Claude/Cursor/Gemini/Ultra/邮箱 | 0.07-3288.79 | OpenPrice |
| 34 | 小柴AI | 链动小铺 | GPT/Claude/Cursor/Gemini/Grok/Kiro/邮箱 | 0.12-2935.5 | OpenPrice |
| 35 | 亚米的整合服务供应商 | 链动小铺 | GPT/Claude/Gemini/Ultra/Kiro/邮箱 | 0-3953.14 | OpenPrice |
| 36 | Tora-雪诺AI源头分销小铺 | 链动小铺 | GPT/Claude/Cursor/Gemini/Ultra/Grok/邮箱 | 0-3397.97 | AI号探/OpenPrice |
| 37 | 52XUEAI | 链动小铺 | GPT/Claude/Cursor/Gemini/Ultra/Kiro/邮箱 | 0.6-3502 | OpenPrice |
| 38 | 大娃 | 链动小铺 | GPT/Claude/Gemini/Kiro/邮箱 | 1.97-1433.76 | OpenPrice |
| 39 | YUJI | 链动小铺 | GPT/Claude/Gemini/Grok/邮箱 | 0.04-3384.58 | OpenPrice |
| 40 | 梦幻小铺 | 链动小铺 | GPT/Claude/邮箱 | 0.52-3500.97 | OpenPrice |
| 41 | 海海星星AI | 链动小铺 | GPT/Claude/Cursor/Gemini/Ultra/Grok/Kiro/邮箱 | 0.06-3378.4 | OpenPrice |
| 42 | 源头AI专售 | 链动小铺 | GPT/Claude/Gemini/Kiro/邮箱 | 1.97-1493.5 | OpenPrice |
| 43 | 自我放飞 | 链动小铺 | GPT/Grok/邮箱 | 0.67-4789.5 | OpenPrice |
| 44 | 东北23333--承接理工科毕设 | 链动小铺 | GPT/Claude/Cursor/Gemini/Ultra/Grok/Kiro/邮箱 | 0.06-3811 | OpenPrice |
| 45 | 棉被的ai小铺 | 链动小铺 | GPT/Claude/Gemini/Grok/邮箱 | 1.91-3213.6 | OpenPrice |
| 46 | 金幺の小店 | 链动小铺 | GPT/Claude/Cursor/Gemini/Grok/Kiro/邮箱 | 0.08-3594.7 | OpenPrice |
| 47 | 东北23333【商品都可开票】 | 链动小铺 | GPT/Claude/Cursor/Gemini/Ultra/Grok/Kiro/邮箱 | 0.06-3811 | OpenPrice |
| 48 | 幻境MirageAI | 链动小铺 | GPT/Claude/Cursor/Gemini/Grok/邮箱 | 0.09-2152.7 | AI号探/OpenPrice |
| 49 | 极速Ai | 链动小铺 | GPT/Claude/Cursor/Gemini/Grok/邮箱 | 0.23-10300 | OpenPrice |
| 50 | 直连AI | 链动小铺 | GPT/Claude/Cursor/Gemini/Ultra/Grok/Kiro/邮箱 | 0.16-3924.3 | OpenPrice |
| 51 | GPT \| Cluade \| Gemini \| Grok 集合铺 | 云猫寄售 | GPT/Claude/Cursor/Gemini/Grok/邮箱 | 0.05-1336.01 | OpenPrice |
| 52 | GPT-源头供货-招代理 | 链动小铺 | GPT/Claude/Gemini/Ultra/邮箱 | 0.72-3399 | OpenPrice |
| 53 | 一筒小铺 | 链动小铺 | GPT/Claude/Cursor/Gemini/邮箱 | 0.49-784.86 | OpenPrice |
| 54 | 启航AI | 链动小铺 | GPT/Claude/Gemini/Kiro/邮箱 | 0.87-3352.65 | OpenPrice |
| 55 | 一梦AI货源 | 16688 | GPT/Claude/Cursor/Gemini/Ultra/Kiro/邮箱 | 0.02-3198.11 | OpenPrice |
| 56 | NiuGe AI 加钟站 | 链动小铺 | GPT/Claude/Gemini/Ultra/Grok/Kiro/邮箱 | 0.09-10300 | OpenPrice |
| 57 | 元宇宙土拨鼠 | 链动小铺 | GPT/Claude/Cursor/Gemini/Ultra/邮箱 | 0.12-3656.5 | OpenPrice |
| 58 | AI猫猫社 | 链动小铺 | GPT/邮箱 | 0-3551.96 | OpenPrice |
| 59 | CodexTool | 16688 | GPT/Claude/Ultra/邮箱 | 0.1-5006.36 | OpenPrice |
| 60 | NianHuaStore | 自建/独角数卡 | GPT/Claude/Gemini/Ultra/Grok/邮箱 | 9-7999 | OpenPrice/水獭比价 |
| 61 | 阿库娅ai源头 | 链动小铺 | GPT/Claude/Gemini/Ultra/Kiro | 3.08-3593.67 | OpenPrice |
| 62 | AI集合铺 | 16688 | GPT/Claude/Ultra/邮箱 | 0.03-1742.46 | OpenPrice |
| 63 | FranklyBuilds的AI小店 | 链动小铺 | GPT/Claude/Gemini/Kiro/邮箱 | 0.03-248.75 | AI号探/OpenPrice |
| 64 | 老马AI（源头直供，招代理） | 链动小铺 | GPT/Claude/Cursor/Gemini/Ultra/Grok/邮箱 | 0.52-3397.97 | OpenPrice |
| 65 | 9号小铺 | 链动小铺 | GPT/Claude/Gemini/Ultra/Grok/邮箱 | 0.09-1616.48 | OpenPrice |
| 66 | 大米AI会员店 | 链动小铺 | GPT/Claude/Gemini/Grok/邮箱 | 0.98-4448.21 | OpenPrice |
| 67 | LeoLab | 链动小铺 | GPT/Claude/Gemini/邮箱 | 0.1-1277.2 | OpenPrice |
| 68 | 吾爱API | 链动小铺 | GPT/邮箱 | 17.46-1236 | OpenPrice |
| 69 | ai跑起来 | 16688 | GPT/Claude/Gemini/Ultra/邮箱 | 0.02-3495.2 | OpenPrice |
| 70 | AI贝贝 | 链动小铺 | GPT/Gemini/邮箱 | 0.03-3502 | OpenPrice |
| 71 | 【AI源头直供】AICA | 链动小铺 | GPT/Claude/Gemini/Kiro/邮箱 | 1.17-1903.44 | OpenPrice |
| 72 | 小智Ai｜聚合站 | 链动小铺 | GPT/Claude/Gemini/Grok/邮箱 | 0.08-1184.5 | OpenPrice |
| 73 | 曼波小铺 | 链动小铺 | GPT/Claude/Gemini/Kiro/邮箱 | 0.38-3424.75 | OpenPrice |
| 74 | open_store | 链动小铺 | GPT/Claude/Gemini/邮箱 | 1.75-1086.65 | OpenPrice |
| 75 | AI小铺 | 链动小铺 | GPT/Gemini/邮箱 | 0-1658.3 | OpenPrice |
| 76 | 柴柴AI | 链动小铺 | GPT/Claude/Gemini/邮箱 | 0-1697.44 | OpenPrice |
| 77 | AI源头批发旗舰店 | 链动小铺 | GPT/Claude/Cursor/Gemini/Ultra/Grok/邮箱 | 3.86-3254.8 | OpenPrice |
| 78 | ai直售 | 链动小铺 | Claude/Cursor/邮箱 | 0.03-1416.25 | OpenPrice |
| 79 | gpt_plus_批发 | 链动小铺 | GPT/Claude/邮箱 | 0.04-259.46 | OpenPrice |
| 80 | 智铺 AI | 链动小铺 | GPT/Claude/Cursor/Ultra/邮箱 | 1.83-1278.86 | OpenPrice |
| 81 | 诚心优选 | 链动小铺 | GPT/Claude/Gemini/Ultra/邮箱 | 0-10299 | OpenPrice |
| 82 | Epoch | 链动小铺 | GPT/Claude/Gemini/Grok/邮箱 | 0.19-816.79 | OpenPrice |
| 83 | 花生AI | 链动小铺 | GPT/Claude/Cursor/Ultra/邮箱 | 0.37-3625.6 | OpenPrice |
| 84 | 马了个马 | 链动小铺 | GPT/Claude/Cursor/Gemini/邮箱 | 0.24-684.95 | OpenPrice |
| 85 | 橙子AI批发站 | 链动小铺 | GPT/Gemini/Ultra/邮箱 | 0.26-3182.7 | AI号探/OpenPrice |
| 86 | ai源头高品质供应商 | 链动小铺 | GPT/Claude/Gemini/邮箱 | 1.03-3930.48 | OpenPrice |
| 87 | 商家1430 | 链动小铺 | GPT/邮箱 | 0.07-1287.5 | OpenPrice |
| 88 | 无事小神仙的ai小店 | 链动小铺 | GPT/Claude/Gemini/Ultra/Grok/邮箱 | 0.01-3306.3 | OpenPrice |
| 89 |  AKMOZ.com魔卡AI（销量20k+）只做精品Ai 直接源头掌握核心科技 | 链动小铺 | GPT/Claude/Gemini/Grok/邮箱 | 0.22-3378.4 | OpenPrice |
| 90 | 007的小铺 | 链动小铺 | GPT/Gemini/邮箱 | 7.36-275.32 | AI号探/OpenPrice |
| 91 | AI猪的店铺 | 自建/未知 | GPT/Claude/Gemini/Grok/邮箱 | 6-3280 | OpenPrice |
| 92 | Tcc谷歌邮箱批发 | 16688 | GPT/Claude/Cursor/Gemini/邮箱 | 0.02-1100.99 | OpenPrice |
| 93 | TxyxT小店 | 自建/未知 | GPT/Claude/Gemini/Grok | 2.5-3600 | OpenPrice |
| 94 | AI gogo渠道 （招代理） | 链动小铺 | GPT/Claude/Gemini/Ultra/邮箱 | 0.01-3316.6 | OpenPrice |
| 95 | AI供应 | 链动小铺 | GPT/Claude/Gemini/Grok/邮箱 | 0.14-3347.5 | OpenPrice |
| 96 | Esa的Ai小铺 | 链动小铺 | GPT/Claude/Gemini/邮箱 | 1.85-1182.44 | OpenPrice |
| 97 | 猫王AI高品质源头 · 官方自营小铺 | 链动小铺 | GPT/Claude/Gemini/邮箱 | 1.03-3930.48 | OpenPrice |
| 98 | 第8号铺 | 链动小铺 | GPT/Claude/Gemini/邮箱 | 0.12-10300 | OpenPrice |
| 99 | 幽羊 AI | 链动小铺 | GPT/邮箱 | 0.04-101.97 | OpenPrice |
| 100 | ai旗舰店 | 链动小铺 | GPT/Claude/Gemini/Ultra/邮箱 | 2.14-3399 | OpenPrice |
| 101 | 卷子ai ( Lucky ) | 链动小铺 | GPT/Claude/Gemini/Ultra/Grok/邮箱 | 0.23-3347.5 | OpenPrice |
| 102 | 还没想好 | 链动小铺 | GPT/Gemini/邮箱 | 0.02-3397.97 | OpenPrice |
| 103 | AI五条悟 | 链动小铺 | GPT/Claude/Gemini/Ultra/Grok | 1.03-3563.8 | OpenPrice |
| 104 | AI杂货铺 | 自建/购物模板（同源） | GPT/Claude/Gemini/Ultra/Grok/邮箱 | 5.75-3215 | OpenPrice |
| 105 | yuyu的G小店 | 链动小铺 | GPT/Gemini/邮箱 | 0.09-1359.6 | OpenPrice |
| 106 | 一站式 AI 杂货铺 | 自建/异次元发卡 | GPT/Claude/Gemini/Ultra/邮箱 | 8-3456 | OpenPrice/水獭比价 |
| 107 | DT的AI小铺 | 链动小铺 | GPT/Claude/Gemini/Ultra/邮箱 | 0.57-1926.1 | OpenPrice |
| 108 | ai补给站 | 链动小铺 | GPT/Grok/邮箱 | 0-3409.3 | OpenPrice |
| 109 | 商家2333 | 链动小铺 | GPT/Gemini/邮箱 | 0.19-1133 | OpenPrice |
| 110 | 稳问AI  --AI 大玩家（AI真源头，招代理） | 链动小铺 | GPT/Claude/Gemini/邮箱 | 2.06-2008.5 | OpenPrice |
| 111 | 海神- GPT-大玩家（招代理） | 链动小铺 | GPT/Claude/Ultra/邮箱 | 3.19-3584.4 | OpenPrice |
| 112 | Aisou智充 | 自建/异次元发卡 | GPT/Claude/Gemini/Ultra/Grok | 5-66666 | OpenPrice |
| 113 | Ai稳定供应（Grok/G.pt/Gemini源头直供） | 链动小铺 | GPT/Claude/Gemini/Ultra/邮箱 | 1.83-3316.6 | OpenPrice |
| 114 | LaniCC AI | 链动小铺 | GPT/Claude/Gemini | 3.61-3450.5 | OpenPrice |
| 115 | YUJAN宇见Ai-Plus Pro-源头直供 | 链动小铺 | GPT/Claude/Gemini/邮箱 | 16.48-3469.04 | OpenPrice |
| 116 | lulu-Ai | 链动小铺 | GPT/Claude/Ultra/邮箱 | 0.08-695.25 | OpenPrice |
| 117 | 52AI店铺 | 链动小铺 | GPT/Claude/Gemini/邮箱 | 0.52-3244.5 | OpenPrice |
| 118 | Esfine科技小店 | 自建/未知 | GPT/邮箱 | 0.5-1150 | OpenPrice |
| 119 | 猫猫豆 | 链动小铺 | Gemini/Grok | 0.09-216.3 | OpenPrice |
| 120 | LLID.ME｜老霖出海账号商城 | 自建/未知 | GPT/邮箱 | 1.9-49.99 | OpenPrice |

共 430 家，上表按商品数取前 120。完整：[shops.csv](data/shops/shops.csv) · [products.csv](data/shops/products.csv)

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
| 16688 | `www.16688.com.cn` | 寄售制，AI 卡密占比高 |
| ACE云寄售 | `aceyun.cn` | ACE 发卡网 |

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
| `data/relays/relays.csv` | 中转站主表（4801 站，一站一行） |
| `data/relays/aliases.csv` | 别名/镜像域名 → 主域名（3908） |
| `data/relays/relay-models.csv` | 站 × 模型 × 价格（227541） |
| `data/relays/by-model/` | 模型榜单（829 页） |
| `data/relays/medians.json` | 各模型正常价中位数 |
| `data/relays/relay-systems.csv` | 中转站软件名录 |
| `data/shops/` | 发卡平台、系统、店铺、商品 |
| `data/raw/` | 原始产物、发现来源、泛解析缓存 |
| `data/stats.md` | 统计分布 |

字段说明见 [data/README.md](data/README.md)。

[↑ 目录](#toc)

<a id="docs"></a>
## 文档

| 文档 | 内容 |
|---|---|
| [pricing-basics.md](docs/pricing-basics.md) | 倍率/价格怎么算、标记含义 |
| [glossary.md](docs/glossary.md) | 黑话表 |
| [how-to-choose.md](docs/how-to-choose.md) | 怎么选上游 / 避坑 |
| [tools/README.md](tools/README.md) | 脚本与更新流程 |

[↑ 目录](#toc)

<a id="sources"></a>
## 数据来源

- 中转站：Veridrop 目录、GitHub 公开名单、证书透明日志（crt.sh）、对已知域名的子域/后缀扩展扫描；站点信息与价格取自各站公开的 `/api/status`、`/api/pricing`、Sub2API `/api/v1/settings/public`、`/api/v1/model-plaza`
- 卡网：OpenPrice、水獭比价(shuita.xyz)、PriceAI、AI号探、AiFaKa
- 原始报价版权归各来源站，见 [DATA-LICENSE.md](DATA-LICENSE.md)

<a id="license"></a>
## 授权

- 代码 **MIT** · [LICENSE](LICENSE)
- 编排与整理 **CC BY-NC 4.0** · [DATA-LICENSE.md](DATA-LICENSE.md)
- 原始报价版权归各来源站

<a id="contributing"></a>
## 贡献

见 [CONTRIBUTING.md](CONTRIBUTING.md)。

[↑ 回到目录](#toc)
