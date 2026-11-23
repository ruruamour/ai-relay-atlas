# 2026-11-23：两个中文目录与新站区复核

从两个目录明确展示的域名里筛出 24 个未匹配主机。逐一核对站方公开页面后，新增 6 家服务；另按「最全 API」的新站名称独立核实 4 家。没有调用模型、核验上游身份或采集报价。

## 目录给出了多少域名

| 来源 | 实际读取 | 匹配已有主域、取价主机或别名 | 仅匹配候选索引 | 未匹配、逐站核查 | 新增服务 |
|---|---:|---:|---:|---:|---:|
| [公益站导航](https://gongyizhan.com/) | 66 个域名 | 35 | 17 | 14 | 3 |
| [API中转站](https://www.apizhongzhuanzhan.com/providers) | 75 个中转域名 | 38 | 27 | 10 | 3 |

「API中转站」表中共 90 行：9 行标为官方，81 行标为中转，后者有 75 行给出官网。两份清单共 141 条，`dawclaudecode.com` 在两个目录都出现，所以只涉及 **140 个不同主机名**。[目录快照](directory-listings.jsonl)保留逐条出处，不是入库名单。

上表与批次前的仓库比对，忽略大小写和 `www.`。候选索引的键则保留完整主机名；两个目录的快照单独贡献 28 个新键，即上述 24 个未匹配域名，加上已有对应记录的 `free.v36.cm`、`serve.yiyongai.cn`、`www.monking.ai`、`www.weelinking.com`。

## 哪些站进了主表

| 线索 | 已核实主域 | 站方给出的依据 |
|---|---|---|
| 公益站导航 | `api.bluesminds.com`（Bluesminds） | 统一网关及公开模型目录列出 OpenAI、Anthropic 和 DeepSeek |
| 公益站导航 | `api.fuka.win`（芙卡卡の小食堂） | 站方说明提供第三方 API 聚合与转发，列出 OpenAI、Claude、Gemini |
| 公益站导航 | `blazeapi.org`（BlazeAPI） | 目录入口 `blazeai.boxu.dev` 跳转到同名官网，接入文档说明如何使用 Claude、GPT、Gemini |
| API中转站 | `nonelinear.com.cn`（非线智能API） | 目录域名 `nonelinear.com` 和该域的站方首页展示相同服务，均指定 `.com.cn` 为规范域名 |
| API中转站 | `teapotrouter.com`（Teapot Router） | 站方教程分别说明通过同一网关接入 Anthropic Claude 和 OpenAI GPT |
| API中转站 | `www.codexhot.com`（热核算力） | 站方开发者指南说明通过本站密钥使用 GPT、Claude 和 Grok |
| 最全 API 名称，另行检索 | `www.latticehub.cc`（LatticeHub） | 官网介绍兼容 OpenAI 的统一接口，模型广场列出了 OpenAI、xAI 和 DeepSeek |
| 最全 API 名称，另行检索 | `midalo.ai`（Midalo） | 官网列出 OpenAI、Anthropic 和 Gemini 的接入方式；[OkkMax 同名条目](https://www.okkmax.com/station/midalo)给出该域名 |
| 最全 API 名称，另行检索 | `www.lumdatech.com`（Lumda AI） | [禾维 AI 同名条目](https://www.hvoyai.com/sites/lumdatechcom/)给出官网，站方示例说明 Claude、ChatGPT 和 DeepSeek 共用网关 |
| 最全 API 名称，另行检索 | `www.olmai.cc`（Olm.ai） | 公开模型目录列出 Anthropic 和 OpenAI，接入教程给出本站 API 主机 |

[逐域核查记录](directory-review.jsonl)同时保存收录和未收录的依据、来源页和日期。`decision=add` 只在已核实主域上记录；`alias` 表示有证据映射到另一主域。上表两个别名另列为[审核过的映射](../../../../relays/reviewed-aliases.csv)，不会算作两个新站。

**原 24 个主机中其余 18 个没有形成新服务**：14 个仍待核（访问失败、说明不足或与已收录品牌重名），2 个只显示域名落地页或图片工具，1 个只公开说明 Claude 接入，1 个跳转到已收录 `ai-api.cc` 的注册页。注册跳转、相同页面模板、相同规范链接或目录对运营方的猜测，单独都不作为别名依据。证书错误或访问拦截不等于停运。

## 最全 API 的新站区

[新站上榜](https://www.zuiquanapi.com/#new)展示了 10 张卡片，卡片只给出名称和站内跳转，没有直接展示官网域名。这里记录读到的卡片 ID，未跟随推广跳转，未确认跳转目的地。按名称另行查到的站方页面与目录直接列出域名是两种来源，前者在主表记为 `browser`。

| 卡片 ID | 名称 | 核对结果 |
|---|---|---|
| 4733 | T7 API | 已收录的 `api.tronzen.tech` 和另一站 `t7api.com` 都使用 T7 名称，不指定卡片域名 |
| 4732 | latticehub | 独立核实同名 LatticeHub 官网及其模型目录 |
| 4731 | Midalo | 通过 OkkMax 交叉核对同名官网及站方说明 |
| 4730 | JetAPI | [`api.jetapi.icu` 的站方说明](https://api.jetapi.icu/about)将 `jetapi.org` 列为独立运营的同名服务；卡片归属待核 |
| 4729 | BigModel | 库内已有多个相近名字，未指定域名 |
| 4728 | ? | 名称不足以核对 |
| 4727 | Lumda AI | 通过禾维 AI 和站方接入说明确认同名服务 |
| 4726 | OlmAI | 由 Olm.ai 的模型目录和官方教程确认同名服务 |
| 4725 | llm2token | 未取得可归属该名称的站方资料 |
| 4724 | 鱼跃云充 | 同名站 `yy9.ai` 展示订阅充值，未见多厂商 API 说明 |

## 本批次的净变化

| 表 | 批次前 | 批次后 | 净增 |
|---|---:|---:|---:|
| [中转站主表](../../../../relays/relays.csv) | 5,155 | 5,165 | 10 家服务 |
| [别名表](../../../../relays/aliases.csv) | 4,326 | 4,328 | 2 个别名 |
| [候选索引](../../candidate-index.jsonl) | 29,215 | 29,249 | 34 个完整主机名 |
| [报价表](../../../../relays/relay-models.csv) | 271,412 | 271,412 | 0 条报价 |

逐域核查文件共 30 条：原 24 个主机、两个站方规范主域和按名称另行核实的 4 个服务主域。后 6 个主域不在两份目录快照中，故索引净增是 **28 + 6 = 34**，不是服务数。`n_models=0` 表示仓库没有该站的报价行。
