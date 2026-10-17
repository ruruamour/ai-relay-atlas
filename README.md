# ai-relay-atlas · AI 中转站与发卡地图

把 **AI API 中转站**（模型、倍率、价格）和 **发卡/卡网店铺**（会员、账号行情）放在同一张"上游地图"里。数据来自公开页面与公开接口，手动抓取、手动维护。

> ⚠️ 仅收录公开信息，**不提供购买入口、不参与交易、不担保**。价格未对账，以原站为准。详见 [DISCLAIMER.md](DISCLAIMER.md)。

## 目录结构

```
data/
  relays/
    relays.csv          # 中转站主表（域名/评分/有哪些模型）
    relay-models.csv    # 站 × 模型 × 价格（长表，核心数据）
    by-model/*.md       # 按模型排名的可读榜单
  shops/
    platforms.csv       # 发卡平台（SaaS，商家入驻）
    systems.csv         # 发卡系统（开源软件，自建用）
    shops.csv           # 店铺主表（归属：平台 or 自建）
    products.csv        # 店 × 商品 × 价格
  raw/                  # 原始抓取产物（csv/json/md）
docs/
  pricing-basics.md     # 倍率/价格怎么算
  glossary.md           # 黑话表（质保/首登/RT/反重力/拼车…）
  how-to-choose.md      # 怎么选上游 / 怎么避免踩坑
tools/                  # 抓取与归一化脚本（手动运行，无 CI）
```

## 字段说明

### `data/relays/relay-models.csv`
`domain, model, input_usd_m, output_usd_m, group, group_ratio, model_ratio, protocol, source, promo, last_checked`

- `input_usd_m` / `output_usd_m`：**推算**的实际价，美元 / 1M token。
- 换算方式见 [docs/pricing-basics.md](docs/pricing-basics.md)。
- `promo`：是否为福利/特价/免费组。
- `source`：数据来自哪个接口（`newapi:/api/pricing`、`plaza`、`scan` 等）。

### `data/shops/shops.csv`
`shop, hosting, platform, system, system_type, domain, categories, price_range, source, last_checked, notes`

- `hosting`：`SaaS`（入驻发卡平台）或 `自建`。
- `platform`：SaaS 店所属平台（链动小铺…）。
- `system`：自建店所用发卡系统（独角数卡/异次元发卡/ZFAKA…）。
- `domain`：**纯文本**，仅作标识，非购买入口。

## 数据来源
OpenPrice、水獭比价（shuita.xyz）、PriceAI、AI号探、AiFaKa 名单、Veridrop，以及各中转站公开的 `/api/pricing`、`/api/v1/model-plaza` 等接口。详见 [DATA-LICENSE.md](DATA-LICENSE.md)。

## 授权
- 代码 MIT · [LICENSE](LICENSE)
- 编排与整理 CC BY-NC 4.0 · [DATA-LICENSE.md](DATA-LICENSE.md)
- 原始报价版权归各来源站

## 更新
手动维护，非实时。每行带 `last_checked`。
