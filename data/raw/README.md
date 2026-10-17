# Gemini 上游价格数据（nuoapi.net 选型）

抓取日期：2026-09-23/24。来源：Veridrop Gemini 榜（427 域名）+ 各站公开价格接口/页面。

## 覆盖率（全 427 域名）

| 状态 | 数量 | 说明 |
|---|---:|---|
| **有 Gemini 价格** | **250** | 结构化 233 + 自建站 17（去重后） |
| 自建站、无公开 Gemini 价格 | 86 | 首页 200，但价格页/接口不含 Gemini |
| 不可达 | 65 | 超时/连接失败/死站 |
| New-API 关闭注册 | 18 | 无法取登录后价格 |
| New-API 需登录、已尝试但无 Gemini | 8 | 注册成功但 API 无 Gemini 模型 |

逐域名状态见 `coverage.csv`。

## 文件

| 文件 | 内容 |
|---|---|
| `gemini-ranking.md` | 结构化站（New-API/Sub2API，含登录后）按 3.8 Flash 输入价排序，含分组倍率、折扣标签、Veridrop |
| `gemini-stations.csv` | 一站一行的汇总（各 Flash 档位最低价、分组、充值/活动） |
| `gemini-prices-long.csv` | 站×模型长表，保留 `raw`/`billing_expr` 原始字段与价格口径 |
| `custom-rendered.md` / `custom-rendered.csv` | 自建站/SPA：浏览器渲染价格页 + pi 抽取 |
| `PLAN.md` | 全量采集计划与数据模型 |

## 数据来源与可信度

- **结构化（229→232 家）**：New-API `/api/pricing`、Sub2API `/api/v1/model-plaza`、`transit snapshot`、`/api/ratio_config`；部分站需注册登录后取。
  - New-API 价格 = `model_ratio × group_ratio × $2`（推算，标 `ratio`）；
  - Sub2API/transit 给的是显式 `input_price/output_price`（标 `explicit_token`，更可信）；
  - 带 `billing_expr` 的以原公式为准（标 `expr`）。
- **自建站（13 家）**：浏览器渲染公开价格页，pi 抽取。
- 所有值都是公开配置/页面推算，**未用真实账单核对**。最便宜的组多是福利/引流组，不代表默认可用。

## 账号

注册账号（用户名/密码/token）存于仓库外：`~/.codex/gemini-research/accounts.json`。**不要提交进仓库。**

## 已知限制

- Veridrop 榜显示 473 家，页面实际只渲染 ~427 个唯一域名（36–80 名次坑位不渲染）。
- 部分站价格/活动需登录；部分用 Turnstile/Cap 人机验证。
- 榜单实时重排，位置会漂移；已按域名去重。
