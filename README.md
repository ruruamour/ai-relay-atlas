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
| 中转站（去重后） | 3857（首页可访问 3247） |
| 合并的别名/镜像域名 | 871 |
| 已剔除的泛解析子域 | 5251 |
| 站 × 模型 报价 | 179347 |
| 基础模型数（不同模型，非站数） | 10361 |
| 公开充值价的站 | 1874（≤¥1.5/$ 的 1154 站，≥¥6/$ 的 697 站） |
| 发卡店铺 | 314（SaaS 273 / 自建 41） |
| 发卡商品报价 | 10646 |

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
| 1 | `subrouter.ai` | SubRouter | New-API | 1491 | OCGXMD | 6.8 | - | 200 | 1741ms |
| 2 | `kfcv50.link` | KFC V50 API | New-API | 1394 | OCGXMD | 1 | - | 200 | 7683ms |
| 3 | `api2.aigcbest.top` | 钱多多 API | New-API | 1311 | OCGXMD | 3.5 | - | 200 | 14168ms |
| 4 | `ai.comfly.org` | comfly | New-API | 1131 | OCGXMD | 1.2 | 100 | 200 | 16748ms |
| 5 | `ai.t8star.org` | Zhenzhen's WorkSho… | New-API | 1131 | OCGXMD | 1.35 | - | 200 | 3345ms |
| 6 | `api.bltcy.ai` | 柏拉图AI | New-API | 1131 | OCGXMD | 1 | - | 200 | 1793ms |
| 7 | `openai.sharkmagic.top` | 鲨鱼魔法 | New-API | 1089 | OCGXMD | - | - | 200 | 3152ms |
| 8 | `ai.soruxgpt.com` | SoruxGPT | New-API | 969 | OCGXMD | 1 | - | 200 | 3915ms |
| 9 | `open.selart.cc` | 赛艺API | New-API | 858 | OCGXD | 1 | - | 200 | 3057ms |
| 10 | `ai2.qiqiai.top` | AI2 | New-API | 727 | OCGXMD | 7.3 | - | 200 | 9795ms |
| 11 | `www.hohoapi.com` | HoHoApi | New-API | 703 | OCGXD | 3 | - | 200 | 2440ms |
| 12 | `api.holdai.top` | 毫秒API | New-API | 701 | OCGXD | 1.2 | - | 200 | 3140ms |
| 13 | `api.tu-zi.com` | 兔子API | New-API | 662 | OCGXD | 0.7 | - | 200 | 2993ms |
| 14 | `api.zyai.online` | Yun API | New-API | 651 | OCGXD | 1 | 71 | 200 | 3764ms |
| 15 | `api.aliyunfuwu.top` | Top API | New-API | 649 | OCGXD | 1 | - | 200 | 3395ms |
| 16 | `newapi.link` | - | New-API | 643 | OCGXMD | 1 | - | 200 | 3205ms |
| 17 | `api.ocoolai.com` | ocoolAI | New-API | 616 | OCGXD | 1 | - | 200 | 7030ms |
| 18 | `api.wukong.support` | 悟空API | New-API | 613 | OCGXD | 1 | 68 | 200 | 2331ms |
| 19 | `botcf.com` | Bot Compute Fabric | New-API | 585 | OCGXMD | 1 | 95 | 200 | 831ms |
| 20 | `www.ggwk1.online` | ggwk1 API | New-API | 582 | OCGXMD | 1 | - | 200 | 1692ms |
| 21 | `api.camel-hub.cn` | CaMeL AI | New-API | 556 | OCGXMD | 0.8 | - | 200 | 1966ms |
| 22 | `api.34ku.com` | 速通Api | New-API | 552 | OCGXMD | 1 | - | 200 | 4013ms |
| 23 | `wrduai.com` | WrduAI | New-API | 552 | OCGXD | 7.3 | - | 200 | 203ms |
| 24 | `hk.chenmoai.cn` | 沉默API | New-API | 543 | OCGXD | 1 | - | 200 | 488ms |
| 25 | `keypool.space` | 云创算力 | New-API | 539 | OCGXMD | 1 | - | 200 | 1496ms |
| 26 | `suanliai.top` | 算力AI | New-API | 537 | OCGXD | 1 | - | 200 | 7056ms |
| 27 | `n.lconai.com` | 智创聚合API | New-API | 504 | OCGXD | 1 | - | 200 | 5285ms |
| 28 | `yutoapi.com` | YutoAPI | New-API | 502 | OCGXMD | 1 | - | 200 | 1854ms |
| 29 | `xiaoqie.xyz` | 小企鹅.xyz | New-API | 497 | OCGXMD | 7.3 | - | 200 | 3584ms |
| 30 | `poloai.top` | PoloAPI | New-API | 490 | OCGXD | 1 | 98 | 200 | 2881ms |
| 31 | `poloapi.top` | PoloAPI | New-API | 490 | OCGXD | 1 | 88 | 200 | 2806ms |
| 32 | `llm.kagu.one` | - | New-API | 490 | OCGXMD | 7.3 | - | 200 | 2101ms |
| 33 | `go.sbgpt.site` | 中转货源API | New-API | 477 | OCGXD | 1 | - | 200 | 9382ms |
| 34 | `api.vectorengine.ai` | 向量引擎 | New-API | 469 | OCGXMD | 0.5 | 96 | 200 | 12667ms |
| 35 | `www.xiaoruiera.top` | 极速链API | New-API | 469 | OCGXMD | 0.8 | 84 | 200 | 4328ms |
| 36 | `api.anthropicricardo.club` | 江南💗赫尔佐格 | New-API | 469 | OCGXMD | 1 | - | 200 | 2569ms |
| 37 | `api.zhongzhuan.vip` | 向量引擎 | New-API | 469 | OCGXMD | 0.5 | - | 200 | 3584ms |
| 38 | `apistudio.vip` | 灵境 API | New-API | 469 | OCGXMD | 0.6 | - | 200 | 3679ms |
| 39 | `one.chatshare.one` | ChatShare API | New-API | 469 | OCGXMD | 0.6 | - | 200 | 2620ms |
| 40 | `yuli.host` | 玉玉API_接口 | New-API | 469 | OCGXMD | 0.58 | - | 200 | 6262ms |
| 41 | `dawnnode.com` | 黎明智汇 | New-API | 468 | OCGXMD | 1 | - | 200 | 2455ms |
| 42 | `ruishiglobal.com` | SuperAI公园 | New-API | 467 | OCGXMD | 1.08 | - | 200 | 2630ms |
| 43 | `api.uiuihao.com` | UiUiAPI聚合平台 | New-API | 465 | OCGXD | 3.19 | - | 200 | 4560ms |
| 44 | `api.wapq.cn` | LivenHub | New-API | 465 | OCGXMD | 7.3 | - | 200 | 793ms |
| 45 | `api.zhiyikeji.cn` | 千枢词元 | New-API | 465 | OCGXMD | 0.6 | - | 200 | 1019ms |
| 46 | `sg.uiuiapi.com` | UiUiAPI聚合平台 | New-API | 465 | OCGXD | 3.19 | - | 200 | 5110ms |
| 47 | `aws.baby` | 企业级 AI 网关 | New-API | 427 | OCGMD | 1 | - | 200 | 1705ms |
| 48 | `api.luoqianyi.qzz.io` | 迁忆 | New-API | 423 | OCGXMD | 0.5 | - | 200 | 1902ms |
| 49 | `magic666.top` | 即刻AI - 即刻拥抱最新AI技术 | New-API | 415 | OCGXD | 1 | 80 | 200 | 4840ms |
| 50 | `api.bianxie.ai` | 便携AI聚合API | New-API | 414 | OCGXMD | 7.3 | - | 200 | 2357ms |
| 51 | `max.openai365.top` | 美团团 API | New-API | 411 | OCGXMD | 7.3 | 77 | 200 | 403ms |
| 52 | `yibuapi.com` | 一步API | New-API | 408 | OCGXMD | 1.5 | - | 200 | 2281ms |
| 53 | `new.yihubang.top` | 小护 | New-API | 398 | OCXMD | 1 | - | 200 | 3062ms |
| 54 | `api1.uiuiapi.com` | UiUi API聚合 | New-API | 393 | OCGX | 3.37 | - | 200 | 5580ms |
| 55 | `wish.sillydream.top` | SillyDream | New-API | 389 | OCGXD | - | - | 200 | 2108ms |
| 56 | `rockapi.ai` | Rock API | New-API | 386 | OCGXMD | 1 | - | 200 | 8069ms |
| 57 | `www.9915654.ggff.net` | 后羿AI中转站 | New-API | 379 | OCGXMD | 7.3 | - | 200 | 2418ms |
| 58 | `anyaigc.com` | AnyAIGC - API中转站 | New-API | 378 | OCGXMD | 0.66 | 100 | 200 | 1229ms |
| 59 | `api.winfull.cloud-ip.cc` | 伝富AI | New-API | 378 | OCGXMD | 0.55 | 100 | 200 | 2648ms |
| 60 | `api.zhongzhuan.chat` | 云雾 API | New-API | 378 | OCGXMD | 0.5 | 95 | 200 | 3933ms |
| 61 | `vipapi.online` | 流星API | New-API | 378 | OCGXMD | 1 | 95 | 200 | 2771ms |
| 62 | `v2.cloudmist.cloud` | 云岚API | New-API | 378 | OCGXMD | 1 | 94 | 200 | 4015ms |
| 63 | `yunwu.ai` | 云雾 API | New-API | 378 | OCGXMD | 0.5 | 90 | 200 | 2790ms |
| 64 | `aiapihub.cloud` | 智联API | New-API | 378 | OCGXMD | 1.1 | - | 200 | 2923ms |
| 65 | `aiyiwei.vip` | 聚合api | New-API | 378 | OCGXMD | 0.63 | - | 200 | 4797ms |
| 66 | `api-hub.vip` | 云柏 API | New-API | 378 | OCGXMD | 1 | - | 200 | 2851ms |
| 67 | `api.aibh.site` | 空氧API-可以继续使用 | New-API | 378 | OCGXMD | 1 | - | 200 | 4634ms |
| 68 | `api.aicso.top` | 灵汐API | New-API | 378 | OCGXMD | 0.55 | - | 200 | 4211ms |
| 69 | `api.antmoo.com` | AntMoo API | New-API | 378 | OCGXMD | 0.8 | - | 200 | 3115ms |
| 70 | `api.apiplus.org` | 云雾 API | New-API | 378 | OCGXMD | 0.5 | - | 200 | 6792ms |
| 71 | `api.bitidea.cn` | 小小思路API | New-API | 378 | OCGXMD | 1 | - | 200 | 2185ms |
| 72 | `api.clai.click` | CLAI API | New-API | 378 | OCGXMD | 0.55 | - | 200 | 3543ms |
| 73 | `api.mumuverse.space` | MuMuのAPI | New-API | 378 | OCGXMD | 0.75 | - | 200 | 5750ms |
| 74 | `api.wlai.vip` | 云雾 API | New-API | 378 | OCGXMD | 0.5 | - | 200 | 4528ms |
| 75 | `api.xueai.me` | XUEAI | New-API | 378 | OCGXMD | 1 | - | 200 | 3940ms |
| 76 | `api123.eu.cc` | 123 API | New-API | 378 | OCGXMD | 0.55 | - | 200 | 126ms |
| 77 | `apipro.maynor1024.live` | momoAPIPro | New-API | 378 | OCGXMD | 1.25 | - | 200 | 3709ms |
| 78 | `apixin.cn` | 芯数智API | New-API | 378 | OCGXMD | 1 | - | 200 | 1359ms |
| 79 | `code.yansd666.com` | 烟神殿AI | New-API | 378 | OCGXMD | 1 | - | 200 | 5123ms |
| 80 | `fluxapi.top` | 流光API | New-API | 378 | OCGXMD | 0.7 | - | 200 | 5350ms |
| 81 | `linxingran.top` | 星然API | New-API | 378 | OCGXMD | 0.78 | - | 200 | 2298ms |
| 82 | `minitoken.top` | 云算 API | New-API | 378 | OCGXMD | 0.8 | - | 200 | 4995ms |
| 83 | `next.aigc2d.com` | AIGC2D | New-API | 378 | OCGXMD | 1 | - | 200 | 3048ms |
| 84 | `qianfufu.com` | 芙芙API | New-API | 378 | OCGXMD | 0.8 | - | 200 | 9083ms |
| 85 | `sparkapi.cn` | 灵光 API | New-API | 378 | OCGXMD | 1 | - | 200 | 3117ms |
| 86 | `startapi.top` | StartAPI | New-API | 378 | OCGXMD | 1 | - | 200 | 5577ms |
| 87 | `uouo.fun` | UOUO API | New-API | 378 | OCGXMD | 1 | - | 200 | 5341ms |
| 88 | `www.aifast.club` | AI快站 | New-API | 378 | OCGXMD | 0.75 | - | 200 | 1675ms |
| 89 | `www.aigeek.life` | AI 极客 | New-API | 378 | OCGXMD | 1 | - | 200 | 2780ms |
| 90 | `xiaohumini.site` | XIAOHUMINI-API | New-API | 378 | OCGXMD | 0.8 | - | 200 | 3827ms |
| 91 | `xinyuanai666.com` | 鑫源API | New-API | 378 | OCGXMD | 0.8 | - | 200 | 7476ms |
| 92 | `yunai.chat` | 凌云  API | New-API | 378 | OCGXMD | 0.8 | - | 200 | 7654ms |
| 93 | `yunshu.hk` | 云雾 | New-API | 378 | OCGXMD | 1 | - | 200 | 3107ms |
| 94 | `api.xhuoai.com` | 星火API官 | New-API | 372 | OCGXD | 1.5 | - | 200 | 111ms |
| 95 | `na.wanxiaot.com` | 鈉 API \| ナトリウム API | New-API | 368 | OCGXMD | 1 | - | 200 | 2873ms |
| 96 | `naapi.cc` | 鈉 API \| ナトリウム API | New-API | 368 | OCGXMD | 1 | - | 200 | 2346ms |
| 97 | `newapi.prorisehub.com` | Pro API | New-API | 363 | OCGXMD | 1 | 86 | 200 | 2210ms |
| 98 | `i.v1api.cc` | - | New-API | 358 | OCGXMD | 1 | - | 200 | 6811ms |
| 99 | `freegpt.tech` | FreeGPT-免费GPT网站在线体… | New-API | 357 | OCGMD | 1 | - | 200 | 3292ms |
| 100 | `iai.iisbo.com` | 小波 API | New-API | 349 | OCGXD | 10 | 96 | 200 | 6414ms |

覆盖：O=OpenAI · C=Claude · G=Gemini · X=Grok · M=MiMo · D=DeepSeek。充值 ¥/$：站点公开的"多少元买 1 美元额度"，实付价 = 名义价 × 充值价。

完整名单（3857 站）：[relays.csv](data/relays/relays.csv) · 别名：[aliases.csv](data/relays/aliases.csv) · 报价：[relay-models.csv](data/relays/relay-models.csv)

[↑ 目录](#toc)

<a id="coverage"></a>
## 中转站 · 模型覆盖

| 家族 | 基础模型数 | 覆盖站点 | 覆盖最广的模型 |
|---|---|---|---|
| OpenAI | 1246 | 1850 | [gpt-5.6-sol](data/relays/by-model/gpt-5.6-sol.md) · [gpt-5.6-terra](data/relays/by-model/gpt-5.6-terra.md) · [gpt-6-astra](data/relays/by-model/gpt-6-astra.md) |
| Claude | 950 | 1701 | [claude-opus-4-8](data/relays/by-model/claude-opus-4-8.md) · [claude-opus-4-6](data/relays/by-model/claude-opus-4-6.md) · [claude-opus-5](data/relays/by-model/claude-opus-5.md) |
| Gemini | 1369 | 1354 | [gemini-3.8-flash](data/relays/by-model/gemini-3.8-flash.md) · [gemini-3.1-pro-preview](data/relays/by-model/gemini-3.1-pro-preview.md) · [gemini-3.7-flash](data/relays/by-model/gemini-3.7-flash.md) |
| Grok | 309 | 1311 | [grok-4.5](data/relays/by-model/grok-4.5.md) · [grok-4.6](data/relays/by-model/grok-4.6.md) · [grok-4.7](data/relays/by-model/grok-4.7.md) |
| MiMo | 40 | 458 | [mimo-v2.5-pro](data/relays/by-model/mimo-v2.5-pro.md) · [mimo-v2.5](data/relays/by-model/mimo-v2.5.md) · [mimo-v2.6-flash](data/relays/by-model/mimo-v2.6-flash.md) |
| DeepSeek | 257 | 1349 | [deepseek-v4-pro](data/relays/by-model/deepseek-v4-pro.md) · [deepseek-v4-flash](data/relays/by-model/deepseek-v4-flash.md) · [deepseek-v4.1-flash](data/relays/by-model/deepseek-v4.1-flash.md) |
| Qwen | 600 | 813 | [qwen3.8-max](data/relays/by-model/qwen3.8-max.md) · [qwen3.7-max](data/relays/by-model/qwen3.7-max.md) · [qwen3.8-flash](data/relays/by-model/qwen3.8-flash.md) |
| GLM | 208 | 1201 | [glm-5.3](data/relays/by-model/glm-5.3.md) · [glm-5.2](data/relays/by-model/glm-5.2.md) · [glm-5.3-flash](data/relays/by-model/glm-5.3-flash.md) |
| Kimi | 96 | 1101 | [kimi-k3](data/relays/by-model/kimi-k3.md) · [kimi-k2.6](data/relays/by-model/kimi-k2.6.md) · [kimi-k2.7-code](data/relays/by-model/kimi-k2.7-code.md) |
| 豆包 | 580 | 496 | [doubao-seed-2-1-pro](data/relays/by-model/doubao-seed-2-1-pro.md) · [doubao-seedream-5-0](data/relays/by-model/doubao-seedream-5-0.md) · [doubao-seed-2-0-pro](data/relays/by-model/doubao-seed-2-0-pro.md) |
| MiniMax | 272 | 741 | [minimax-m3](data/relays/by-model/minimax-m3.md) · [minimax-m2.7](data/relays/by-model/minimax-m2.7.md) · [minimax-m2.5](data/relays/by-model/minimax-m2.5.md) |
| 混元 | 51 | 314 | [hy3](data/relays/by-model/hy3.md) · [hy4-preview](data/relays/by-model/hy4-preview.md) · [hy4](data/relays/by-model/hy4.md) |
| Llama | 106 | 166 | [llama-3.2-11b-vision-instruct](data/relays/by-model/llama-3.2-11b-vision-instruct.md) · [llama-3.2-90b-vision-instruct](data/relays/by-model/llama-3.2-90b-vision-instruct.md) · [llama-3.2-1b-instruct](data/relays/by-model/llama-3.2-1b-instruct.md) |
| 图像/视频/音频 | 889 | 301 | [z-image-turbo](data/relays/by-model/z-image-turbo.md) · [viduq3-turbo](data/relays/by-model/viduq3-turbo.md) · [happyhorse-1.1-t2v](data/relays/by-model/happyhorse-1.1-t2v.md) |
| 其他 | 3388 | 775 | [bge-reranker-v2-m3](data/relays/by-model/bge-reranker-v2-m3.md) · [bce-reranker-base-v1](data/relays/by-model/bce-reranker-base-v1.md) · [sparkdesk-v1.1](data/relays/by-model/sparkdesk-v1.1.md) |

全部 722 个模型榜单：[by-model/index.md](data/relays/by-model/index.md)

[↑ 目录](#toc)

<a id="backend"></a>
## 中转站 · 疑似同后端

价格表完全相同的跨品牌站点，共 99 组 / 261 站。前 15 组：

| 组 | 站数 | 站点 |
|---|---|---|
| B001 | 38 | `aiapihub.cloud` · `aiyiwei.vip` · `anyaigc.com` · `api-hub.vip` · `api.aibh.site` · `api.aicso.top` … |
| B002 | 11 | `aiwuje.com` · `api.echoflowai.cc` · `api.n1n.ai` · `api.quickrouter.ai` · `jeniya.cn` · `linoapi.com` … |
| B003 | 7 | `api.anthropicricardo.club` · `api.vectorengine.ai` · `api.zhongzhuan.vip` · `apistudio.vip` · `one.chatshare.one` · `www.xiaoruiera.top` … |
| B004 | 3 | `ai-one.vip` · `aizzz.vip` · `kuaipao.ai` |
| B005 | 3 | `ai.orbitlink.me` · `subrouter.ai` · `usawest.up.railway.app` |
| B006 | 3 | `api.buzzgw.com` · `buzzai.cc` · `claude.buzz7.top` |
| B007 | 3 | `api.dawclaudecode.com` · `dawcode.com` · `dawvip.com` |
| B008 | 3 | `api.kbq.de5.net` · `hk.xn--0xv303ar5c.com` · `xn--vduyey89e.com` |
| B009 | 3 | `cdn.juaiapi.com` · `www.juapi.net` · `www.tokenrouter.tech` |
| B010 | 3 | `ciyuan.today` · `gptapi.top` · `makerend.com` |
| B011 | 3 | `cn.jbbt.cc` · `jbbtoken.cn` · `jbbtoken.pages.dev` |
| B012 | 3 | `code.ddsst.online` · `code.ppchat.vip` · `code.pumpkinai.vip` |
| B013 | 3 | `codeworksta.com` · `codex101.cf-cdn.site` · `new-cdn.dg8.site` |
| B014 | 3 | `comeu.ai` · `keuapi.com` · `keutoken.com` |
| B015 | 3 | `grok101.site` · `llm-all.pro` · `u-ai.me` |

[↑ 目录](#toc)

<a id="shops"></a>
## 卡网 · 店铺名单

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

共 314 家，上表按商品数取前 120。完整：[shops.csv](data/shops/shops.csv) · [products.csv](data/shops/products.csv)

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
| `data/relays/relays.csv` | 中转站主表（3857 站，一站一行） |
| `data/relays/aliases.csv` | 别名/镜像域名 → 主域名（871） |
| `data/relays/relay-models.csv` | 站 × 模型 × 价格（179347） |
| `data/relays/by-model/` | 模型榜单（722 页） |
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

- 中转站：Veridrop 目录、GitHub 公开名单、对已知域名的子域/后缀扩展扫描；价格取自各站公开的 `/api/pricing`、`/api/v1/model-plaza`
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
