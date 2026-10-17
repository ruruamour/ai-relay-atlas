# Gemini 上游全量价格/倍率采集计划

目标：对 Veridrop Gemini 榜上的全部中转站，产出一张可横向对比的表：** Gemini 价格、分组倍率、支持的模型、是否标准价、充值倍率与活动 **，并标注每个数字的来源与可信度。

工作目录：`/home/sui/projects/nuoapi-ops/playbooks/gemini-upstream-prices/`
榜单来源：`https://veridrop.org/leaderboard/gemini`（2026-09-23 快照 427 个唯一域名）。
原则：只读公开页面/公开价格元数据；不登录、不注册、不调用任何站的推理接口；不改生产配置。

---

## 一、已完成的摸底（用于估算工作量）

| 项目 | 数量 | 说明 |
|---|---:|---|
| 榜单唯一域名 | 427 | 认证 Top 35 + 完整榜位置 81–~489；36–80 坑位页面不渲染 |
| 有结构化 JSON 且含 Gemini | 226 | 可直接解析 |
| ↳ `/api/pricing`（New-API） | 206 | 字段最全，含 group_ratio / model_ratio / billing_expr |
| ↳ `/api/ratio_config`（New-API 精简） | 41 | 只有 ratio/expr，缺分组倍率时需补 `/api/pricing` |
| ↳ `/api/v1/model-plaza`（Sub2API） | 10 | 直接给每 token 的 `input_price`/`output_price`，更准 |
| ↳ `/api/public/transit/v1/snapshot`（Sub2API） | 5 | 同上 |
| 无 JSON Gemini | 201 | HTML/SPA/登录墙/死站，需浏览器或人工 |
| 多引擎并存 | 36 | 同一站命中多个端点，要合并去重 |

已产出的第一版（仅 `/api/pricing` 的 186 家）：
`gemini-ranking.md`、`gemini-stations.csv`、`gemini-prices-long.csv`。

---

## 二、统一数据模型

### 站级（一行一站）
`domain, site_name, reachable, engine, veridrop_pos, veridrop_score, veridrop_samples, veridrop_last, pro, badges, pricing_source_url, billing_currency, cny_to_usd_ratio(充值倍率), topup_bonus(赠送), activity_note, gemini_groups(json), n_gemini_models, cheapest_3.8_flash_input, flags, fetched_at, confidence`

### 模型级（一行一站一模型）
`domain, model, platform(gemini/vertex/antigravity/cli), billing_mode(token/per_call), group_used, group_ratio, model_ratio, completion_ratio, cache_ratio, cache_write_ratio, input_usd_m, output_usd_m, cache_read_usd_m, cache_write_usd_m, per_request_usd, billing_expr, is_official_base, discount_vs_official, source_url, raw(原始字段片段), confidence, notes`

**换算规则（必须写进每一行，不允许静默换算）**
- New-API token 计费：`input = model_ratio × group_ratio × $2`，`output = input × completion_ratio`，`cache_read = input × cache_ratio`。
- 若存在 `billing_expr`：原样保留，另用 ratio 值给参考价并标 `expr`。
- 若 `model_price > 0`：判为按次计费，只记 `per_request_usd`，不折算 token 价。
- Sub2API：`input_price/output_price` 已是 USD/token，乘 `rate_multiplier` 后 ×1e6 得 USD/M。
- `confidence` 取值：`explicit`（站方直接给价）> `ratio_calc`（倍率推算）> `unknown`。

---

## 三、执行阶段

### P0 域名与榜单（已完成）
- 抓 18 页，按域名去重，保留 pos/分数/样本/最近日期/PRO/套壳标记/报告链接。

### P1 结构化引擎全量解析（覆盖面 ~226 家）
1. 对每站按优先级请求：`/api/pricing` → `/api/v1/model-plaza` → `/model-plaza/data/plaza.json` → `/api/ratio_config` → `/api/public/transit/v1/snapshot`。
2. 每个响应按 Content-Type + JSON 可解析 + 含 `gemini` 才判定有效，避免 SPA 首页误判。
3. 多引擎并存的 36 家做字段合并：价格以更具体的为准（Sub2API explicit > New-API ratio_calc）。
4. 输出到统一模型，记录 `source_url` 与 `raw` 片段。

### P2 非结构化站（剩余 ~201 家）
1. 先做可达性分级：HTTP 200 / 401(登录墙) / 404(无该路径) / 5xx / 超时。
2. 200 的：抓 `/pricing`、首页，提取 HTML 内嵌 JSON（Vue/Nuxt 的 `__NUXT__`、`window.__INITIAL_STATE__` 等）或表格文本。
3. 仍是纯 JS 的：用 browser-service（127.0.0.1:9333）逐站渲染后取 DOM，限流（同域串行，间隔 ≥2s）。
4. 401/登录墙的：标 `login_required`，不绕过；只保留首页可见的套餐/活动文案。
5. 死站/超时：标 `unreachable`，保留最后一次快照时间。

### P3 充值倍率与活动
- 优先读接口字段：`pricing_cny_rate`、`first_topup_offer(s)`、`subscription_plans`（如 modelflare.dev）。
- 首页/公告文本：正则抓 `充值|首充|赠送|活动|折扣|折|%|送|返利`，人工可复核片段。
- 登录后才可见的充送规则：标 `login_required`，不猜测。
- 明确区分三种口径：**充值汇率**（¥→$）、**赠送比例**、**限时活动**，不合并成一个"倍率"。

### P4 归一化与标注
- 每个价格生成两个标签：
  - `价格口径`：标准1x / 折扣Nx / 加价Nx / 按次$X / billing_expr。
  - `对官方折扣`：能对齐官方模型的，写 `官方价 vs 本站价` 与倍数；对不齐的写 `unknown`，不硬套。
- 同名不同档位（`gemini-3.8-flash` vs `gemini-3.8-flash-high`）分开成行，不合并。
- 折扣异常低（如 0.01x）单独打 `suspicious_low` 旗标，提示可能是福利组/引流组而非默认价。

### P5 输出
1. `gemini-ranking.md` — 人看，按 3.8 Flash 输入价排序，含"便宜+高分"分区。
2. `gemini-stations.csv` — 站级汇总。
3. `gemini-prices-long.csv` — 站×模型长表（含全部模型与原始字段）。
4. `gemini-candidates.md` — 候选清单：价格低于阈值且 Veridrop 分达标，附待验证项。

### P6 小流量实测（可选，需另行批准）
- 对候选做同模型、同请求的小额对照：成功率、429/5xx、TTFT/P95、实际响应模型、实际扣款。
- 只读+只测，不动 net 站生产渠道；任何切流/改价单独批准。

---

## 四、质量与验收

- 每行都必须能回溯到 `source_url`；抓不到的字段写 `unknown`，不用旧值填。
- 抽样复核：随机 20 家，人工打开价格页核对换算是否一致，误差>10% 则回查公式。
- 区分"站方直接报价"与"倍率推算"；最终结论只用 `explicit` 的做硬排名，推算值只做参考并标出。
- 榜单实时重排，位置会漂移；以域名为键，不以来一次的位置为准。

## 五、风险与限制

- 部分站价格/活动是登录后或前端强渲染，公开抓取拿不到，只能标 `login_required`。
- New-API 各站可能改过基准（不一定是 $2/M），倍率推算存在系统性偏差，故必须保留 `raw`。
- 榜单分数是第三方协议检测，不证明真实上游身份或生产稳定性。
- 全量爬取要控制频率，避免被目标站封禁；同域串行、全局并发受限。

## 六、里程碑

| 阶段 | 产出 | 预计 |
|---|---|---|
| P1 | 226 家结构化全量 JSON + 长表 | 1 轮批抓 |
| P2 | 200 家分级 + 可渲染的补齐 | 2–3 轮 |
| P3 | 充值/活动字段覆盖率 | 与 P2 并行 |
| P4/P5 | 最终对比表 + 候选清单 | P1–P3 完成后 |
| P6 | 候选实测（需批准） | 另行 |
