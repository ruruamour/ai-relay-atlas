/home/sui/projects/nuoapi-ops/playbooks/gemini-upstream-prices/# 自建站/SPA 价格（浏览器渲染 + 接口抓取 + pi 抽取）


| 站点 | Gemini 模型 | 类型 | 输入 USD/M | 输出 USD/M | 缓存读 | 官方输入 | 官方输出 | 折扣/备注 |
|---|---|---|---|---|---|---|---|---|
| ai.12zx.net | gemini-2.5-flash | token | 0.75 | 4.5 | 0.075 |  |  | 性价比混池 |
| ai.12zx.net | gemini-3-flash | token | 0.75 | 4.5 | 0.075 |  |  | 性价比混池 |
| ai.12zx.net | gemini-3-flash-preview | token | 0.75 | 4.5 | 0.075 |  |  | 性价比混池 |
| ai.12zx.net | gemini-3-pro-image | per_call |  |  |  |  |  | 直连/官方 |
| ai.12zx.net | gemini-3.1-flash-image | per_call |  |  |  |  |  | 性价比混池 |
| ai.12zx.net | gemini-3.1-flash-image-4k | per_call |  |  |  |  |  | 性价比混池 |
| ai.12zx.net | gemini-3.1-flash-lite | token | 0.75 | 4.5 | 0.075 |  |  | 性价比混池 |
| ai.12zx.net | gemini-3.1-flash-lite-preview | token | 0.75 | 4.5 | 0.075 |  |  | 性价比混池 |
| ai.12zx.net | gemini-3.1-pro | token | 2.0 | 12.0 | 0.2 |  |  | 直连/官方 |
| ai.12zx.net | gemini-3.1-pro-high | token | 2.0 | 12.0 | 0.2 |  |  | 直连/官方 |
| ai.12zx.net | gemini-3.1-pro-low | token | 2.0 | 12.0 | 0.2 |  |  | 直连/官方 |
| ai.12zx.net | gemini-3.1-pro-preview | token | 2.0 | 12.0 | 0.2 |  |  | 直连/官方 |
| ai.12zx.net | gemini-3.1-pro-preview-think | token | 2.0 | 12.0 | 2.0 |  |  | 直连/官方 |
| ai.12zx.net | gemini-3.5-flash | token | 2.0 | 12.0 | 0.2 |  |  | 性价比混池 |
| ai.12zx.net | gemini-3.5-flash-low | token | 2.0 | 12.0 | 0.2 |  |  | 性价比混池 |
| ai.12zx.net | gemini-3.6-flash | token | 1.5 | 7.5 | 1.5 |  |  | 性价比混池 |
| ai.12zx.net | gemini-3.6-flash-high | token | 1.5 | 7.5 | 1.5 |  |  | 性价比混池 |
| ai.12zx.net | gemini-3.6-flash-low | token | 1.5 | 7.5 | 1.5 |  |  | 性价比混池 |
| ai.12zx.net | gemini-3.6-flash-tiered | token | 1.5 | 7.5 | 1.5 |  |  | 性价比混池 |
| ai.12zx.net | gemini-3.7-flash | token | 1.5 | 7.5 | 1.5 |  |  | 性价比混池 |
| ai.12zx.net | gemini-3.7-flash-high | token | 1.5 | 7.5 | 1.5 |  |  | 性价比混池 |
| ai.12zx.net | gemini-3.7-flash-low | token | 1.5 | 7.5 | 1.5 |  |  | 性价比混池 |
| ai.12zx.net | gemini-3.8-flash | token | 1.5 | 7.5 | 1.5 |  |  | 性价比混池 |
| ai.12zx.net | gemini-3.8-flash-high | token | 1.5 | 7.5 | 1.5 |  |  | 性价比混池 |
| ai.12zx.net | gemini-3.8-flash-low | token | 1.5 | 7.5 | 1.5 |  |  | 性价比混池 |
| ai.12zx.net | gemini-image | per_call |  |  |  |  |  | 性价比混池 |
| ai.12zx.net | gemini-image-pro | per_call |  |  |  |  |  | 直连/官方 |
| ai.12zx.net | gemini-music | per_call |  |  |  |  |  | 性价比混池 |
| ai.furry.vg | anti/gemini-3-flash | per_call |  |  |  |  |  | 分组 Gemini，端点 gemini, openai |
| ai.furry.vg | anti/gemini-3.1-flash-lite | per_call |  |  |  |  |  | 分组 Gemini，端点 gemini, openai |
| ai.furry.vg | anti/gemini-3.1-pro-preview | per_call |  |  |  |  |  | 分组 Gemini，端点 gemini, openai |
| ai.furry.vg | anti/gemini-3.5-flash | per_call |  |  |  |  |  | 分组 Gemini，端点 gemini, openai |
| ai.furry.vg | anti/gemini-3.6-flash | per_call |  |  |  |  |  | 分组 Gemini，端点 gemini, openai |
| ai.furry.vg | anti/gemini-3.7-flash | per_call |  |  |  |  |  | 分组 Gemini，端点 gemini, openai |
| ai.furry.vg | anti/gemini-3.8-flash | per_call |  |  |  |  |  | 分组 Gemini，端点 gemini, openai |
| ai.furry.vg | anti/gemini-pro-agent | per_call |  |  |  |  |  | 分组 Gemini，端点 gemini, openai |
| ai.furry.vg | autoroute/gemini-3.7-flash | per_call |  |  |  |  |  | 分组 Gemini，端点 gemini, openai |
| ai.furry.vg | gemini-2.5-flash-image | per_call |  |  |  |  |  | 分组 default，端点 gemini, openai |
| ai.furry.vg | gemini-3-pro-image | per_call |  |  |  |  |  | 分组 default，端点 gemini, openai |
| ai.furry.vg | gemini-3.1-flash-image | per_call |  |  |  |  |  | 分组 default，端点 gemini, openai |
| aihubmix.com | Gemini 3.8 Flash | token | 0.75 | 3.75 |  |  |  | Web Search $0.014/request；Cache Storage $0.5/h/M tokens；Input Audio $1/M tokens；Input Video $1/M tokens |
| aihubmix.com | Gemini 3.8 Flash Lite Tts | token | 1.0 | 1.0 |  |  |  | TTS 模型 |
| aihubmix.com | Gemini 3.8 Flash Tts | token | 0.5 | 9.0 |  |  |  | TTS 模型 |
| api.bblabu.ai | nano-banana-2 | per_call |  |  |  |  |  | Gemini分组倍率×2，按请求计费 |
| api.bblabu.ai | nano-banana-pro | per_call |  |  |  |  |  | Gemini分组倍率×2，按请求计费 |
| api.beara.top | gemini-3-flash | token | 0.4 | 2.4 | 0.04 | 0.5 | 3.0 | -20% Gemini 原生 CPA·Claude/Gemini 原生计费，用户结算价¥0.4/¥2.4/¥0.04 每M，结算倍率×0.8 |
| api.beara.top | gemini-3-flash-agent | token | 0.4 | 2.4 | 0.04 | 0.5 | 3.0 | -20% Gemini 原生 CPA·Claude/Gemini 原生计费，用户结算价¥0.4/¥2.4/¥0.04 每M，结算倍率×0.8 |
| api.beara.top | gemini-3.1-flash-image | token | 0.4 | 2.4 |  | 0.5 | 3.0 | -20% Gemini 原生 CPA·Claude/Gemini 原生计费，用户结算价¥0.4/¥2.4 每M，结算倍率×0.8 |
| api.beara.top | gemini-3.1-flash-lite | token | 0.2 | 1.2 | 0.02 | 0.25 | 1.5 | -20% Gemini 原生 CPA·Claude/Gemini 原生计费，用户结算价¥0.2/¥1.2/¥0.02 每M，结算倍率×0.8 |
| api.beara.top | gemini-3.1-pro | token | 1.6 | 9.6 | 0.16 | 2.0 | 12.0 | -20% Gemini 原生 CPA·Claude/Gemini 原生计费，用户结算价¥1.6/¥9.6/¥0.16 每M，缓存写¥1.6每M，结算倍率×0.8 |
| api.beara.top | gemini-3.1-pro-low | token | 1.6 | 9.6 | 0.16 | 2.0 | 12.0 | -20% Gemini 原生 CPA·Claude/Gemini 原生计费，用户结算价¥1.6/¥9.6/¥0.16 每M，结算倍率×0.8 |
| api.beara.top | gemini-3.5-flash | token | 1.2 | 7.2 | 0.12 | 1.5 | 9.0 | -20% Gemini 原生 CPA·Claude/Gemini 原生计费，用户结算价¥1.2/¥7.2/¥0.12 每M，结算倍率×0.8 |
| api.beara.top | gemini-3.5-flash-extra-low | token | 1.2 | 7.2 | 0.12 | 1.5 | 9.0 | -20% Gemini 原生 CPA·Claude/Gemini 原生计费，用户结算价¥1.2/¥7.2/¥0.12 每M，结算倍率×0.8 |
| api.coderplan.ai | Gemini 3.8 Flash | token | 0.68 | 3.38 | 0.07 | 0.76 | 3.76 | 约1.29折 倍率0.9x；实际扣费=模型美元定价×0.9；对比官方已叠加1元=1美元额度充值换算 |
| api.teamorouter.cn | Gemini 3.1 Pro Preview | token | 0.516 | 3.1 | 0.0516 | 2.0 | 12.0 | 75% OFF 2.5折；上下文2M；Google/Vertex，SLA 100.00% |
| api.teamorouter.cn | Gemini 3.6 Flash | token | 0.18 | 0.9 | 0.018 | 0.75 | 3.75 | 76% OFF 2.4折；Google/Vertex，SLA 99.89% |
| api.teamorouter.cn | Gemini 3.7 Flash | token | 0.342 | 1.71 | 0.0342 | 0.75 | 3.75 | 55% OFF 4.5折；Google/Vertex，SLA 99.90% |
| api.teamorouter.cn | Gemini 3.8 Flash | token | 0.251 | 1.26 | 0.0251 | 0.75 | 3.75 | 67% OFF 3.3折；Google/Vertex，SLA 99.71% |
| api.x5m5x.com | gemini-3.1-pro-preview | token | 0.5 | 3.0 | 0.05 | 2.0 | 12.0 | 75% OFF 按量计费元/百万Token；到手价按官网参考×0.25倍率，官网参考$2/$12 |
| api.x5m5x.com | gemini-3.5-flash | token | 0.375 | 2.25 | 0.0375 | 1.5 | 9.0 | 75% OFF 按量计费元/百万Token；到手价按官网参考×0.25倍率，官网参考$1.5/$9 |
| api.x5m5x.com | gemini-3.6-flash | token | 0.375 | 1.875 | 0.0375 | 1.5 | 7.5 | 75% OFF 按量计费元/百万Token；到手价按官网参考×0.25倍率，官网参考$1.5/$7.5 |
| api.x5m5x.com | gemini-3.7-flash | token | 0.1875 | 0.9375 | 0.0187 | 0.75 | 3.75 | 75% OFF 按量计费元/百万Token；到手价按官网参考×0.25倍率，官网参考$0.75/$3.75 |
| api.x5m5x.com | gemini-3.8-flash | token | 0.1875 | 0.9375 | 0.0187 | 0.75 | 3.75 | 75% OFF 按量计费元/百万Token；到手价按官网参考×0.25倍率，官网参考$0.75/$3.75 |
| fapi.leileihog.top | gemini-3.1-flash-image | per_call |  |  |  |  |  | 生图分组，动态计费，每次调用 $1/请求 |
| fapi.leileihog.top | gemini-3.1-pro | per_call |  |  |  |  |  | 分组 default +1，按次计费 $0.19/请求 |
| fapi.leileihog.top | gemini-3.1-pro-preview | per_call |  |  |  |  |  | 分组 svip +1，按次计费 $0.075/请求 |
| fapi.leileihog.top | gemini-3.5-flash | per_call |  |  |  |  |  | 分组 default +1，按次计费 $0.075/请求 |
| fapi.leileihog.top | gemini-3.6-flash | per_call |  |  |  |  |  | 分组 default，按次计费 $0.15/请求 |
| fapi.leileihog.top | gemini-3.7-flash | per_call |  |  |  |  |  | 分组 default +1，按次计费 $0.075/请求 |
| fapi.leileihog.top | gemini-3.8-flash | per_call |  |  |  |  |  | 分组 default +1，按次计费 $0.075/请求 |
| fishai.yanyumeta.cn | gemini-3.1-pro-preview | token | 0.08 | 0.84 |  | 0.55 | 3.3 | Gemini 3.1 Pro Preview（Google）；积分价 0.08/0.84 积分/Tokens；成本 3.96/23.76 元/1M Tokens |
| fishai.yanyumeta.cn | gemini-3.5-flash | token | 0.05 | 0.46 |  | 0.3028 | 1.8194 | Gemini 3.5 Flash（Google）；积分价 0.05/0.46 积分/Tokens；成本 2.18/13.10 元/1M Tokens |
| fishai.yanyumeta.cn | gemini-3.5-flash-lite | token | 0.04 | 0.3 |  | 0.1417 | 1.1778 | Gemini 3.5 Flash Lite（Google）；积分价 0.04/0.30 积分/Tokens；成本 1.02/8.48 元/1M Tokens |
| fishai.yanyumeta.cn | gemini-3.6-flash | token | 0.08 | 0.39 |  | 0.3 | 1.5 | Gemini 3.6 Flash（Google）；积分价 0.08/0.39 积分/Tokens；成本 2.16/10.80 元/1M Tokens |
| fishai.yanyumeta.cn | gemini-3.7-flash | token | 0.04 | 0.17 |  | 0.1708 | 0.8556 | Gemini 3.7 Flash（Google）；积分价 0.04/0.17 积分/Tokens；成本 1.23/6.16 元/1M Tokens |
| fishai.yanyumeta.cn | gemini-3.8-flash | token | 0.044 | 0.187 |  | 0.1708 | 0.8556 | Gemini 3.8 Flash（Google）；积分价 0.044/0.187 积分/Tokens；成本 1.23/6.16 元/1M Tokens |
| laysoai.com | gemini-2.5-flash | token | 0.048 | 0.4 | 0.012 | 0.3 | 2.5 | -84% Token-based；实际按官方$1收费$0.16，即0.16倍率 |
| laysoai.com | gemini-3.1-pro-preview | token | 0.32 | 1.92 | 0.032 | 2.0 | 12.0 | -84% Token-based；实际按官方$1收费$0.16，即0.16倍率 |
| omniakey.com | Gemini 2.5 Flash | token | 0.255 | 2.125 | 0.0255 | 0.3 | 2.5 | 15% OFF |
| omniakey.com | Gemini 2.5 Flash-Lite | token | 0.085 | 0.34 | 0.0085 | 0.1 | 0.4 | 15% OFF |
| omniakey.com | Gemini 2.5 Pro | token | 0.5 | 4.0 | 0.05 | 1.25 | 10.0 | 60% OFF <=200K tier; 200K-1M tier: input $1, cached $0.1, output $6 (official $2.5/$0.25/$15) |
| omniakey.com | Gemini 3.1 Pro Preview | token | 0.8 | 4.8 | 0.08 | 2.0 | 12.0 | 60% OFF <=200K tier; 200K-1M tier: input $1.6, cached $0.16, output $7.2 (official $4/$0.4/$18) |
| omniakey.com | Gemini 3.5 Flash-Lite | token | 0.255 | 2.125 | 0.0255 | 0.3 | 2.5 | 15% OFF |
| omniakey.com | Gemini 3.6 Flash | token | 0.45 | 2.25 | 0.045 | 0.75 | 3.75 | 40% OFF |
| omniakey.com | Gemini 3.7 Flash | token | 0.45 | 2.25 | 0.045 | 0.75 | 3.75 | 40% OFF |
| omniakey.com | Gemini 3.8 Flash | token | 0.45 | 2.25 | 0.045 | 0.75 | 3.75 | 40% OFF |
| onehop.ai | Gemini 2.5 Flash Image (Nano Banana) | per_call |  |  |  |  |  | 50% OFF 打5折；≈¥0.13158/张；¥102/百万 tokens |
| onehop.ai | Gemini 2.5 Pro | token | 0.625 | 5.0 |  | 1.25 | 10.0 | 50% OFF 打5折；Standard >200K ¥8.5/¥51；上下文1M |
| onehop.ai | Gemini 3 Flash Preview | token | 0.25 | 1.5 |  | 0.5 | 3.0 | 50% OFF 打5折；上下文1M |
| onehop.ai | Gemini 3 Pro Image (Nano Banana Pro) | per_call |  |  |  |  |  | ¥0.45696/张；4K ¥0.816 · 2K ¥0.45696；无折扣 |
| onehop.ai | Gemini 3.1 Flash Image (Nano Banana 2) | per_call |  |  |  |  |  | 50% OFF 打5折；≈¥0.26316/张；¥204/百万 tokens |
| onehop.ai | Gemini 3.1 Flash Lite | token | 0.125 | 0.75 |  | 0.25 | 1.5 | 50% OFF 打5折；上下文1M |
| onehop.ai | Gemini 3.1 Flash Lite Image (Nano Banana 2 Lite) | per_call |  |  |  |  |  | 50% OFF 打5折；≈¥0.11424/张；¥102/百万 tokens |
| onehop.ai | Gemini 3.1 Pro | token | 1.0 | 6.0 |  | 2.0 | 12.0 | 50% OFF 打5折；Standard >200K ¥13.6/¥61.2；上下文1M |
| onehop.ai | Gemini 3.5 Flash | token | 0.75 | 4.5 |  | 1.5 | 9.0 | 50% OFF 打5折，按固定汇率6.8折算；上下文1M |
| openox.tech | gemini-3-pro-image-preview | per_call |  |  |  |  |  | 按张计费；1k/2k $0.66，4k $1.182 |
| openox.tech | gemini-3.1-flash-image-preview | per_call |  |  |  |  |  | 按张计费；512 $0.222，1k/2k $0.332，4k $0.592 |
| openox.tech | gemini-3.1-pro-preview | token | 2.0 | 12.0 | 0.2 |  |  | ≤200k tokens 输入$2/输出$12，>200k 输入$4/输出$18；官方来源 Google AI Gemini API pricing |
| openox.tech | gemini-3.5-flash | token | 1.5 | 9.0 | 0.15 |  |  | 官方来源 Google AI Gemini API pricing |
| openox.tech | gemini-3.8-flash | token | 0.75 | 3.75 | 0.075 |  |  |  |
| routemux.com | Gemini 2.5 Pro | token | 0.375 | 3.0 | 0.0375 | 1.25 | 10.0 | 70% OFF Google Official · 1M context · STANDARD · Input ≤ 200K TOKEN |
| routemux.com | Gemini 2.5 Pro | token | 0.75 | 4.5 | 0.075 | 2.5 | 15.0 | 70% OFF Google Official · 1M context · STANDARD · Input > 200K TOKEN |
| routemux.com | Gemini 3 Flash Preview | token | 0.15 | 0.9 | 0.015 | 0.5 | 3.0 | 70% OFF Google Official · 1M context · STANDARD |
| routemux.com | Gemini 3.1 Flash Lite | token | 0.075 | 0.45 | 0.0075 | 0.25 | 1.5 | 70% OFF Google Official · 1M context · STANDARD |
| routemux.com | Gemini 3.1 Pro | token | 0.6 | 3.6 | 0.06 | 2.0 | 12.0 | 70% OFF Google google · 1M context · STANDARD · Input ≤ 200K TOKEN |
| routemux.com | Gemini 3.1 Pro | token | 0.6 | 3.6 | 0.06 | 2.0 | 12.0 | 70% OFF Google google · 1M context · STANDARD (未标注区间,重复档) |
| routemux.com | Gemini 3.1 Pro | token | 1.2 | 5.4 | 0.12 | 4.0 | 18.0 | 70% OFF Google google · 1M context · STANDARD · Input > 200K TOKEN |
| routemux.com | Gemini 3.5 Flash | token | 0.45 | 2.7 | 0.045 | 1.5 | 9.0 | 70% OFF Google Official · 1M context · STANDARD |
| routemux.com | Gemini 3.5 Flash-Lite | token | 0.09 | 0.75 | 0.009 | 0.3 | 2.5 | 70% OFF Google Official · 2026-07-21 · 1M context · STANDARD |
| routemux.com | Gemini 3.6 Flash | token | 0.225 | 1.125 | 0.0225 | 0.75 | 3.75 | 70% OFF Google Official · 2026-07-21 · 1M context · STANDARD |
| routemux.com | Gemini 3.7 Flash | token | 0.225 | 1.125 | 0.0225 | 0.75 | 3.75 | 70% OFF Google Official · 2026-08-13 · 1M context · STANDARD |
| routemux.com | Gemini 3.8 Flash | token | 0.225 | 1.125 | 0.0225 | 0.75 | 3.75 | 70% OFF Google Official · 2026-09-02 · 1M context · STANDARD |
| theforestproxy.pages.dev | ix/gemini-3.1-pro | token | 0.0 | 0.0 | 0.0 |  |  |  |
| theforestproxy.pages.dev | ix/gemini-3.7-flash | token | 0.0 | 0.0 | 0.0 |  |  |  |
| theforestproxy.pages.dev | od/free-gemini-2.5-pro | token | 0.0 | 0.0 | 0.0 |  |  |  |
| theforestproxy.pages.dev | sha/free/gemini-3.1-pro | token | 0.0 | 0.0 | 0.0 |  |  |  |
| theforestproxy.pages.dev | sha/free/gemini-3.8-flash | token | 0.0 | 0.0 | 0.0 |  |  |  |
| theforestproxy.pages.dev | sin/gemini-3.6-flash:free | token | 0.0 | 0.0 | 0.0 |  |  |  |
| theforestproxy.pages.dev | sy/gemini-3.1-pro | token | 0.0 | 0.0 | 0.0 |  |  |  |
| theforestproxy.pages.dev | sy/gemini-3.1-pro-low | token | 0.0 | 0.0 | 0.0 |  |  |  |
| theforestproxy.pages.dev | sy/gemini-3.1-pro-preview | token | 0.0 | 0.0 | 0.0 |  |  |  |
| theforestproxy.pages.dev | sy/gemini-3.1-pro-preview-high | token | 0.0 | 0.0 | 0.0 |  |  |  |
| theforestproxy.pages.dev | sy/gemini-3.1-pro-preview-low | token | 0.0 | 0.0 | 0.0 |  |  |  |
| theforestproxy.pages.dev | yl/gemini-3.1-pro | token | 0.0 | 0.0 | 0.0 |  |  |  |
| theforestproxy.pages.dev | yl/gemini-3.7-flash | token | 0.0 | 0.0 | 0.0 |  |  |  |
| theforestproxy.pages.dev | yl/gemini-3.8-flash | token | 0.0 | 0.0 | 0.0 |  |  |  |
| zivv.pro | gemini-3-flash | token | 0.2 | 1.2 | 0.02 | 0.5 | 3.0 | Gemini Anti · Google Antigravity 渠道 · 1M+ 上下文 |
| zivv.pro | gemini-3.1-flash-image | per_call | 0.5 | 60.0 |  | 0.5 | 60.0 | Gemini 图片 · Google Antigravity 渠道 · 固定价(1K/2K/4K 图片另计 0.055/0.06/0.07) |
| zivv.pro | gemini-3.1-pro-high | token | 0.8 | 4.8 | 0.08 | 2.0 | 12.0 | Gemini Anti · Google Antigravity 渠道 · 1M+ 上下文 |
| zivv.pro | gemini-3.1-pro-low | token | 0.64 | 3.84 | 0.064 | 1.6 | 9.6 | Gemini Anti · Google Antigravity 渠道 · 1M+ 上下文 |
| zivv.pro | gemini-3.5-flash-high | token | 0.6 | 3.6 | 0.06 | 1.5 | 9.0 | Gemini Anti · Google Antigravity 渠道 · 1M+ 上下文 |
| zivv.pro | gemini-3.5-flash-low | token | 0.6 | 3.6 | 0.06 | 1.5 | 9.0 | Gemini Anti · Google Antigravity 渠道 · 1M+ 上下文 |
| zivv.pro | gemini-3.6-flash-high | token | 0.6 | 3.0 | 0.06 | 1.5 | 7.5 | Gemini Anti · Google Antigravity 渠道 · 1M+ 上下文 |
| zivv.pro | gemini-3.6-flash-low | token | 0.6 | 3.0 | 0.06 | 1.5 | 7.5 | Gemini Anti · Google Antigravity 渠道 · 1M+ 上下文 |
| zivv.pro | gemini-3.6-flash-medium | token | 0.6 | 3.0 | 0.06 | 1.5 | 7.5 | Gemini Anti · Google Antigravity 渠道 · 1M+ 上下文 |
| zivv.pro | gemini-3.7-flash-tiered | token | 0.3 | 1.5 | 0.06 | 0.75 | 3.75 | Gemini Anti · Google Antigravity 渠道 · 1M+ 上下文 |
| zivv.pro | gemini-3.8-flash-tiered | token | 0.3 | 1.5 | 0.06 | 0.75 | 3.75 | Gemini Anti · Google Antigravity 渠道 · 1M+ 上下文 |