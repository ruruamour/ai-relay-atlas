# 证据批次

- [2026-11-23 中文目录复核](2026-11-23/README.md) — 141 条目录记录，24 个未匹配主机逐一核查，另查新站名称。主表新增 10 站，候选索引新增 34 个域名。
- [`2026-11-21-公开目录补录`](2026-11-21/README.md) — 抓取清单 940 个，实核记录 15 个，候选索引新增 497 个。
- [`legacy/README.md`](legacy/README.md) — 早期调查和验证记录。

批次按材料日期放在 `data/raw/sources/batches/YYYY-MM-DD/`。新批次可以把实际的抓取清单和实核记录直接放进自己的日期目录。

## 文件布局

```text
sources/
├── veridrop-directory-YYYY-MM-DD.txt       # 旧的平铺抓取清单
├── directory-review-YYYY-MM-DD.jsonl       # 旧的平铺实核记录
└── batches/
    └── YYYY-MM-DD/
        ├── README.md                       # 批次说明
        ├── veridrop-directory*.txt         # Veridrop 域名清单，可选
        ├── directory-listings.jsonl        # 其它目录明列的域名和出处，可选
        └── directory-review*.jsonl         # 实核记录，可选
```

索引器只读取上面三种直接放在日期目录里的数据文件。Veridrop 清单每行写一个域名。其它目录清单每行记录 `domain`、公开站名 `name`、来源目录 `source_site`、目录条目链接 `listing_page` 及日期 `checked`。同一域名在多个目录出现时分别保留出处，索引按域名合并，来源标为 `directory`。

逐站核实另写入 `directory-review*.jsonl`，至少给出 `domain`、`checked`、`category` 和判断依据。记录一次核查不代表确认营业或已经收录。

## 留下本批核实依据

每次整理新材料时，新建日期目录，保留域名清单或逐站记录，并在 `README.md` 说明来源、采集日期和核实标准。分别记录目录中看到多少个不同域名、实际核实多少站、站点主表净增多少。若候选索引也有变化，另列去重域名增量。可参考 [2026-11-21 批次](2026-11-21/README.md)。

[`index_candidates.py`](../../../../tools/discover/index_candidates.py) 同时读取旧的平铺文件和日期目录，每个域名只输出一行。多次核实以 `checked` 较新的记录为准，缺少日期时使用文件或批次日期。2026-11-21 批次沿用原文件路径，说明页直接链接到清单和核实记录，无需复制。
