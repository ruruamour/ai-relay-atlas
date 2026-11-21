# Legacy / 早期调查与验证记录

这里收纳原来源注册表里的旧调查说明。内容对应已有平铺文件，也不改变原文件内容。联系人清单的浏览器核实记录日期为 **2026-11-19**，其它日期以各文件字段为准。

## 验证证据

- `*-probe.jsonl`：首页公开 GET 的状态、标题、延迟和最终主机；`401/403/429/5xx` 也保留。`veridrop-probe.jsonl` 是对主候选池中此前未验证的 2,200 个域名补做的探活。
- `passive-refresh-probe.jsonl` / `passive-refresh-scan.json`：对 1,747 个此前未探活的 CT/目录候选做的低并发补验。871 个返回 2xx/3xx，保留 482 个不含敏感字段的公开接口结果，去重后主表新增 1 个统一站点，其他命中项与已有域名合并。
- `*-scan.json`：只访问已公开的状态/价格/模型目录接口，不调用推理接口。`directory-scan.json` 是公开目录新候选的接口验证结果，208 个 2xx/3xx 中命中 114 个。
- `unified-candidate-probe.jsonl` / `unified-candidate-scan.json`：最后一批补验证的 19 个未覆盖域名，19/19 返回 HTTP 200，17 个命中公开接口。
- `veridrop-scan.json`：上述 Veridrop 补验证中 1,053 个 2xx/3xx 域名的公开接口结果，命中 584 个。
- `contact-harvest.jsonl` / `contact-probe.jsonl` / `contact-scan.json`：从一份群发邮件的收件人清单提取的 130 个域名线索；与主表交叉后 44 个已收录（含换后缀/镜像）、17 个与已收录站同品牌不同后缀、20 个候选索引已有、49 个全新。全清单探活 128/130 可达（102 个 2xx/3xx，其余多为 5xx 而非域名失效），剔除已收录后 90 个未收录域名无一不可达；公开接口命中 22 个，合并后新增 14 站、刷新 10 站报价。清单是他人维护的行业联系人表，可达率接近 100% 说明经过整理，取值高于证书日志的随机候选；免费邮箱 local part 里的两条域名线索（`vipapi.online`、`ttchi.online`）也都对应已收录站，说明 local part 是有效线索。
- `contact-hard-scan.json`：对同一清单里首页返回 403/404/502/5xx 的 26 个主机也扫了公开接口（首页非 2xx 不等于不能查价），只有 `crowllm.com` 命中（403 首页、166 个模型）。该站已在主表，按快照整体刷新后报价行 267153 → 267079：站点删掉了 104 个免费/自定义模型、新增 30 个（`pricing_version` 从旧值变为 `a42d372c…`，`agnes-*`、`MiniCPM*` 已从目录消失，属真实下架而非解析失败）。结论：新候选不要只把 2xx/3xx 清单丢给 `scan.py`，403 首页也会藏着在售站。
- `contact-brandscan.json`：对 20 个“与已收录站同品牌、不同后缀”的域名单独扫了一轮，只有 2 个有响应：`toknex.me`（Sub2API 模型广场 30 个模型，并入 `toknex.ai`，报价行 267079 → 267109）和 `nuoapi.com`（`registration_enabled` 与 `model_plaza_enabled` 都是 false，属于同品牌的非公开实例，按 merge 的规则不收录；公开的那个是 `nuoapi.net`）。其余 18 个换后缀域名虽然有首页或邮箱线索，但没有任何公开状态/价格接口，仍留在候选索引。
- 同一批文档里像卡网的 12 个域名（`wokushop.com`、`fuka.win`、`minecrash.top`、`wookit.cn`、`xiass.com`、`pulseneko.com` 等）过了 `shop_fingerprint.py`，12/12 无卡网系统指纹、无卡密/发货关键词：这份清单是中转站与相邻业务（VPS、代充值、域名待售）的厂商名录，不是发卡站目录，因此没有进 `data/shops/candidates.csv`。
- `contact-browser-verify.jsonl`：清单里 130 个域名**逐个用真实浏览器打开**的实核结果（Cloudflare 挑战页、JS 壳、访客闸门这类只看 HTTP 状态码判断不了的情况），只存判定类别、标题、文本字数与关键词布尔命中，不存正文。结果：中转站 70、打不开 25、相邻业务 13、非中转 12、待定 1、账号/订阅代售 5、停放/待售 3、前台已停 1、运营设施 1。其中 4 个被 Cloudflare 挑战页挡住（`crowllm.com`、`ctok.ai`、`vanvibe.com`、`wokushop.com`），改用有头模式重开才拿到真实页面：`crowllm.com` 是中转站（页面写 138 个模型、17 家上游），`ctok.ai` 是 Claude Code 教程站，`vanvibe.com` 跳到 HugeDomains 域名出售页，`wokushop.com` 是越南语数字账号商店——无头模式会把这几类判定成“被盾拦截”，有头模式一次就能分清。
- `contact-browser-adds.jsonl`：上面 130 个域名里实核为“中转站”但主表没有的 23 个（`51kik.com`、`gptproto.com`、`cubence.com`、`oneprovider.dev`、`bazaarlink.ai` 等），按“首页实核”补进主表：`discovered_via=browser`、`n_models=0`、`notes` 写明“浏览器打开确认，无公开价格/状态接口”。这批记录的来源列和备注写明了入库依据。未入主表的条目仍可在 `candidate-index.jsonl` 查看 `page_category`，页面类别与是否收录是两个独立字段。另外 `aeapi.cn`（首页已暂停、`/api/pricing` 仍返回 50 个模型）和 `partokens.com`（Cloudflare 522）已写进 `annotations.csv`。
- `shop-fingerprint-candidates.jsonl`：首页卡网/系统指纹候选，**不是已确认商品店**；审核清单为 `data/shops/candidates.csv`。
- `shop-browser-review.jsonl`：4 个高置信候选的浏览器渲染摘要；3 个首页显示商品/卡密相关内容，1 个访问受限。只保存标题、长度和布尔标记，不保存正文。
- `candidate-index.jsonl`：把上述来源、探活、接口命中、主表状态和卡网指纹整理成一行一域名的复查索引；不替代主表。

## 站点与候选的历史边界

来源线索、探活、公开接口命中和人工页面类别都可以留在候选索引。只有经过公开接口证据或服务方公开说明核对，并与主域、别名及品牌去重后的记录才进入 `data/relays/relays.csv`。卡网候选不会自动进入 `data/shops/shops.csv`。这些规则用于解释历史数据，索引器不执行网络访问或自动收录。
