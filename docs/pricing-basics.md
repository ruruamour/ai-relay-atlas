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
- 有 `model_price` 的模型按次计费。

## Sub2API 体系
`/api/v1/model-plaza` 直接给 `input_price`（美元/token），乘分组 `rate_multiplier × 1e6` 得 USD/1M。

## 两种口径
| 口径 | 含义 |
|---|---|
| 基准价 | `model_ratio × 2`，倍率=1 时的价 |
| 实际价 | 基准价 × 分组倍率，该分组到手价 |

本仓库 `relay-models.csv` 默认给**实际价**，并在 `group_ratio` 标出倍率。

## 常见坑
- 低倍率常来自**福利/特价/免费/拼车**组，不是默认价。
- 同一模型在不同站 `model_ratio` 基数不同，**只比倍率会被带偏**，要比实际价。
- 所有价格为**推算/公开页**，未对账。
