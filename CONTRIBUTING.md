# 贡献指南

欢迎提交新站、纠错、补充文档。请遵循以下格式。

## 提交中转站
在 `data/relays/relays.csv` 增加一行，并在 `data/relays/relay-models.csv` 补充模型价格：

```
domain,name,system_name,veridrop_score,category,source,status,n_models,has_gemini,has_mimo,has_grok,has_argon,last_checked,notes
```

价格请注明来源接口（`newapi:/api/pricing`、`plaza`、`scan` 等），并在 `notes` 写"推算/未对账"。

## 提交发卡店铺
在 `data/shops/shops.csv` 增加一行：

```
shop,hosting,platform,system,system_type,domain,categories,price_range,source,last_checked,notes
```

- `hosting`：`SaaS` 或 `自建`
- SaaS 店填 `platform`（链动小铺/数卡5188/…），自建店填 `system`（独角数卡/异次元发卡/ZFAKA/…）
- `domain` 用**纯文本**，不要放购买/支付直达链接
- `source` 写数据来源站（OpenPrice/水獭/AI号探/自测）

商品级数据加到 `data/shops/products.csv`，`source_url` 指向聚合站页面，不指向店主购买页。

## 纠错
请附：原始页面链接、截图或接口返回、期望值。

## 不接受
- 购买/支付直达链接
- 店铺联系方式、推广码、返佣链接
- 未公开的私有数据或账号凭据
