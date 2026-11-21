# 证据批次

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
        ├── veridrop-directory*.txt         # 抓取清单，可选
        └── directory-review*.jsonl         # 实核记录，可选
```

索引器只读取日期目录的直接子文件，并且只认 `veridrop-directory*.txt` 和 `directory-review*.jsonl`。其它文件、README 和更深的子目录都会忽略。`.txt` 每行写一个归一化域名，`.jsonl` 每行写一条至少带有 `domain` 的 JSON 实核记录，建议同时保留 `checked`、页面类别和公开说明链接。

## 留下本批核实依据

每次整理新材料时，新建日期目录，保留域名清单或逐站记录，并在 `README.md` 说明来源、采集日期和核实标准。分别记录目录中看到多少个不同域名、实际核实多少站、站点主表净增多少。若候选索引也有变化，另列去重域名增量。可参考 [2026-11-21 批次](2026-11-21/README.md)。

[`index_candidates.py`](../../../../tools/discover/index_candidates.py) 同时读取旧的平铺文件和日期目录，每个域名只输出一行。多次核实以 `checked` 较新的记录为准，缺少日期时使用文件或批次日期。2026-11-21 批次沿用原文件路径，说明页直接链接到清单和核实记录，无需复制。
