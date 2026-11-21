# 报告中心

[返回中文首页](../README.md) · [English README](../README.en.md)

想找某一站，可在中转站报告浏览名单；要比较某个模型在各站的价格，直接从模型索引进入榜单。

## 导航

- [中转站报告](relays.md) — 前 100 站、模型家族覆盖和疑似同后端分组
- [店铺报告](shops.md) — 前 120 家店、SaaS 平台和自建系统
- [数据统计](../data/stats.md) — 来源、系统、充值价区间、计价与标记分布
- [模型索引](../data/relays/by-model/index.md) — 955 个模型各有一页，可按站查看名义价和人民币估算价

## 复查入口

- [中转站主表](../data/relays/relays.csv) · [别名表](../data/relays/aliases.csv) · [站 × 模型报价](../data/relays/relay-models.csv)
- [已确认店铺](../data/shops/shops.csv) · [商品报价](../data/shops/products.csv) · [卡网候选审核表](../data/shops/candidates.csv)
- [字段与口径](../data/README.md) · [来源注册表](../data/raw/sources/README.md)
- [最近 Argon 监控报告](../data/monitor/report-argon.md) · [价格漂移摘要](../data/monitor/drift.md) · [监控历史 CSV](../data/monitor/history.csv)
- [原始资料索引](../data/raw/README.md) · [工具与更新流程](../tools/README.md)

## 当前口径

参考价来自公开页面或接口，未与账单核对。站点充值价以每 1 美元额度所需的人民币计，乘以模型的名义美元价格可估算人民币费用。店铺标价本身就是人民币。

模型榜单要求至少 20 站提供该基础模型且有可排名的报价，默认排除 `promo`、`zero`、`default`、`low` 和缺价。仅带 `high` 标记的报价仍可参与。
