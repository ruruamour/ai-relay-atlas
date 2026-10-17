# ai-relay-atlas · AI 中转站与发卡地图

[![License: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE)
[![Data: CC BY-NC 4.0](https://img.shields.io/badge/data-CC%20BY--NC%204.0-lightgrey.svg)](DATA-LICENSE.md)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

把 **AI API 中转站**（模型、倍率、价格）和 **发卡/卡网店铺**（会员、账号行情）放进同一张"上游地图"。数据来自公开页面与公开接口，**手动抓取、手动维护**。

> ⚠️ 仅收录公开信息，**不提供购买入口、不参与交易、不担保**。价格为推算值、未对账，以原站为准。详见 [DISCLAIMER.md](DISCLAIMER.md)。

## 目录
- [快速开始](#快速开始)
- [数据概览](#数据概览)
- [目录结构](#目录结构)
- [数据来源](#数据来源)
- [字段说明](#字段说明)
- [授权](#授权)

## 快速开始

```bash
git clone https://github.com/ruruamour/ai-relay-atlas.git
cd ai-relay-atlas

# 查某模型的全站最低价
python3 tools/query.py model gemini-4-argon --n 30

# 查某站的全部模型与价格
python3 tools/query.py domain api.openlux.ai
```

- 数据概览：[data/stats.md](data/stats.md)
- 按模型榜单：[data/relays/by-model/index.md](data/relays/by-model/index.md)
- 原始产物与溯源：[data/raw/README.md](data/raw/README.md)

## 数据概览

| 项 | 数量 |
|---|---|
| 中转站（域名） | 1740 |
| 中转站 × 模型 报价 | 12774 |
| 发卡店铺 | 314（SaaS 259 / 自建 55） |
| 发卡商品报价 | 10646 |
| 按模型榜单 | 143 |

代表性模型覆盖：`grok-4.5`（1042 站）、`gemini-4-argon`（509）、`mimo-v2.5-pro`（332）、`mimo-v2.5`（325）、`gemini-3.6/3.7-flash`（185/182）、`gemini-3.8-flash`（176）、`mimo-v2.6-flash`（145）、`mimo-v2.6-pro`（130）。

## 目录结构

```
data/
  relays/
    relays.csv          # 中转站主表（域名/评分/有哪些模型）
    relay-models.csv    # 站 × 模型 × 价格（核心长表）
    relay-systems.csv   # 中转站软件名录（New-API/One-API/Sub2API…）
    by-model/*.md       # 按模型排名的可读榜单（143 个）
  shops/
    platforms.csv       # 发卡平台（SaaS，商家入驻）
    systems.csv         # 发卡系统（开源软件，自建用）
    shops.csv           # 店铺主表（归属：平台 or 自建）
    products.csv        # 店 × 商品 × 价格
  raw/                  # 原始抓取产物 + 溯源说明
  stats.md              # 数据概览
docs/
  pricing-basics.md     # 倍率/价格怎么算
  glossary.md           # 黑话表（质保/首登/RT/反重力/拼车…）
  how-to-choose.md      # 怎么选上游 / 怎么避免踩坑
tools/                  # 抓取与归一化脚本（手动运行，无 CI）
```

## 数据来源

| 来源 | 用途 |
|---|---|
| [OpenPrice](https://www.openprice.cc) | 卡网渠道报价聚合（284 渠道） |
| [水獭比价](https://shuita.xyz) | 126 家店铺 / 4034 商品，含走势 |
| [PriceAI](https://priceai.cc) | 200+ 卡网订阅比价 |
| [AI号探](https://aihaotan.com) | 链动小铺店铺索引 |
| [AiFaKa](https://github.com/AiHaoTan/AiFaKa) | 发卡店铺名单 |
| [Veridrop](https://veridrop.org) | 中转站实测评分 |
| 各中转站公开接口 | `/api/pricing`、`/api/v1/model-plaza` |

原始报价版权归各来源站，详见 [DATA-LICENSE.md](DATA-LICENSE.md)。

## 字段说明

### `data/relays/relay-models.csv`
`domain, model, input_usd_m, output_usd_m, group, group_ratio, model_ratio, protocol, source, promo, last_checked`

- `input_usd_m` / `output_usd_m`：**推算**实际价，美元 / 1M token
- `promo`：是否为福利/特价/免费组
- 换算：`input = model_ratio × group_ratio × 2`，见 [docs/pricing-basics.md](docs/pricing-basics.md)

### `data/shops/shops.csv`
`shop, hosting, platform, system, system_type, domain, categories, price_range, source, last_checked, notes`

- `hosting`：`SaaS`（入驻发卡平台）或 `自建`
- `platform`：SaaS 店所属平台（链动小铺…）
- `system`：自建店所用发卡系统（独角数卡/异次元发卡/ZFAKA…）
- `domain`：**纯文本**，仅作标识，非购买入口

## 授权

- 代码 **MIT** · [LICENSE](LICENSE)
- 编排与整理 **CC BY-NC 4.0** · [DATA-LICENSE.md](DATA-LICENSE.md)
- 原始报价版权归各来源站

## 贡献
见 [CONTRIBUTING.md](CONTRIBUTING.md)。欢迎提 [Issue](../../issues/new/choose) 或 PR。
