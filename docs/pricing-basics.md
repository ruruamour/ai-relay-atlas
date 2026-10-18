# 倍率与价格怎么算

## New-API / One-API 体系
模型列表接口 `/api/pricing` 返回：
- `model_ratio`：模型基准倍率
- `completion_ratio`：输出相对输入的倍率
- 全局 `group_ratio`：分组倍率
- 模型的 `enable_groups`：可用分组

**推算输入价（USD / 1M）**：
```
input_usd_m  = model_ratio × group_ratio × 2
output_usd_m = input_usd_m × completion_ratio
```
`× 2` 是 New-API 的美元基准（$2 = 1 倍率）。

**注意**：
- `model_ratio × 2` 是**基准价**（倍率=1）；乘上分组倍率才是该组的**实际价**。
- 部分站的倍率含分组折扣，不严格等价于美元价。
- 有 `billing_expr` 的站按表达式计费，上面的公式不适用。
- `quota_type=1` 的模型**按次计费**：`call_usd = model_price × group_ratio`（本仓库记在 `call_usd` 列）。
- `model_ratio=37.5` 是 New-API 未配置倍率时的默认值，多半是占位价，本仓库标记为 `default`。

## Sub2API 体系
`/api/v1/model-plaza` 直接给 `input_price`（美元/token），乘分组 `rate_multiplier × 1e6` 得 USD/1M。
`billing_mode` 非 token 时按 `per_request_price × rate_multiplier` 计次。专属分组（`is_exclusive`）不参与取价。

## 两种口径
| 口径 | 含义 |
|---|---|
| 基准价 | `model_ratio × 2`，倍率=1 时的价 |
| 实际价 | 基准价 × 分组倍率，该分组到手价 |

本仓库 `relay-models.csv` 默认给**实际价**，并在 `group_ratio` 标出倍率。

## 本仓库怎么取参考价
一个模型通常开放给多个分组。取价规则：
1. 只看匿名可见的分组（`usable_group`），没有则看全部；
2. 排除倍率为 0 的免费组；
3. 取剩下最便宜的分组。

所以参考价 ≈ "该站公开的最低付费价"，不代表默认分组价。

## 实付价（人民币）
名义价只是"额度"的价格。各站卖 1 美元额度要多少钱差很多（¥1 到 ¥7 以上都有），所以**名义价不能跨站直接比**：

```
实付 ¥ / 1M = 名义 $ / 1M × 充值价（元 / 1 美元额度）
```

充值价取自站点公开的 `/api/status`：
- 经典 New-API：`price` 就是"元 / 1 美元额度"；
- 部分分支用美元收款（`payment_currency_symbol='$'`）：`price × usd_exchange_rate` 才是元；
- 币种不明（`CUSTOM` 等）或数值不在 ¥0.3–15 之间：视为未公开，不算实付价。

没算进去的：充值满减/阶梯折扣、卡密/兑换码渠道、订阅制套餐（Sub2API 多为订阅制，通常不公开充值价）。

## 常见坑
- 低倍率常来自**福利/特价/免费/拼车**组，不是默认价。
- 同一模型在不同站 `model_ratio` 基数不同，**只比倍率会被带偏**，要比实际价。
- 所有价格为**推算/公开页**，未对账。
