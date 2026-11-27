# ai-relay-atlas · AI 中转站与发卡地图

**简体中文** · [English](README.en.md)

在这里查 AI API 中转站、比较模型报价，或核对发卡店铺的商品与来源。价格来自公开页面或接口，未与账单核对。

<a id="toc"></a><a id="tasks"></a><a id="目录"></a>
## 从这里开始

| 我想做什么 | 从哪里查 |
|---|---|
| <a id="relays"></a><a id="中转站--综合名单"></a>查一个站点或镜像 | [中转站主表](data/relays/relays.csv) · [别名对照表](data/relays/aliases.csv) · [综合名单前 100 站](reports/relays.md#top-100-sites) |
| <a id="coverage"></a><a id="中转站--模型覆盖"></a>比较同一模型的价格 | [按模型查价](data/relays/by-model/index.md) · [全部报价 CSV](data/relays/relay-models.csv) · [计价和换算](docs/pricing-basics.md) |
| <a id="shops"></a><a id="卡网--店铺名单"></a>查店铺和商品 | [已收录店铺](data/shops/shops.csv) · [商品与标价](data/shops/products.csv) · [店铺概览](reports/shops.md) |
| <a id="sources"></a><a id="数据来源"></a>核对收录依据 | [来源与批次](data/raw/sources/README.md) · [候选域名索引](data/raw/sources/candidate-index.jsonl) |
| <a id="contributing"></a><a id="贡献"></a>提交新站或纠错 | [贡献指南](CONTRIBUTING.md) · [哪些文件可以改](data/README.md) |

<a id="stats"></a>
## 数据概览

- 中转站主表有 **5,165 站**，另有 4,328 个别名。共收集 **271,412 条报价**。`n_models=0` 表示仓库暂无该站报价。
- 候选索引涉及 29,272 个域名，其中包含已收录站点。第三方目录中的条目要经核实才会进入主表。
- 店铺表收录 430 家，含 17,212 条商品报价。另有 191 条[店铺待审线索](data/shops/candidates.csv)。

<a id="quickstart"></a>
## 快速开始

在仓库根目录运行。查询只读本地 CSV，无需联网或先运行构建。

```bash
python3 tools/query.py site api.openlux.ai --n 10
python3 tools/query.py model gemini-4-argon --token --cny --n 10
python3 tools/query.py group cursor --field any --model claude --call --n 10
```

`--token` 按每百万输入 token 比价，`--call` 按次比价。`--cny` 使用站点公开的充值价估算人民币费用。更多选项见[离线查询说明](tools/README.md#离线查价)。

<a id="reports"></a><a id="files"></a><a id="docs"></a><a id="数据文件"></a><a id="文档"></a>
## 报告与数据说明

- <a id="backend"></a><a id="shop-platforms"></a><a id="中转站--疑似同后端"></a><a id="卡网--平台与系统"></a>[报告总览](reports/README.md)收录[模型家族覆盖](reports/relays.md#family-coverage)、[疑似同后端分组](reports/relays.md#suspected-backends)及[店铺平台与系统](reports/shops.md#platforms-and-systems)。
- [数据统计](data/stats.md)汇总覆盖和价格分布。[955 个模型榜单](data/relays/by-model/index.md)保留各站明细。
- [文档索引](docs/README.md)分为使用和维护两部分。更新数据后，在仓库根目录运行 `bash tools/build.sh`。

<a id="license"></a><a id="safety"></a><a id="授权"></a>
## 安全与范围

收录仅依据公开信息，不提供购买入口，也不担保站点当前可用。见[免责声明](DISCLAIMER.md)、[代码许可（MIT）](LICENSE)和[整理数据许可（CC BY-NC 4.0）](DATA-LICENSE.md)。
