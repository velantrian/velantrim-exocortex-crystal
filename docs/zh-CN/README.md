<!-- localization-index-source: main@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- current-localization-source: main@5e6301f0eaee1a6c85d8543be89dc2e606dc05a8 -->
<!-- d1-source: main@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- d1-status: CURRENT -->
<!-- d2-source: main@b7e6574dd7aefa2f32783ab79054fac6b3b4109f -->
<!-- d2-status: CURRENT -->
<!-- d3-source: main@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- d3-status: CURRENT -->
<!-- d4-source: main@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- d4-status: CURRENT -->
<!-- d5-source: main@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- d5-status: CURRENT -->
# 🇨🇳 Crystal 简体中文文档

简体中文的公开 README 与 D1/D3/D4/D5 Reader-dependent 详细文档现已刷新到当前 **post-RC-9 / post-NLI / RRTIC-v1** 架构事实。D2 reviewer/safety 与 Quick Start 的 governing source semantics 未改变，因此保持原文件不动。

## 🧭 文档路线

- Root：[`README.zh-CN.md`](../../README.zh-CN.md) — human-first 项目入口
- D1：[`QUICKSTART.md`](./QUICKSTART.md) — `CURRENT`（未改动） · [`STATUS.md`](./STATUS.md) — `CURRENT` · [`IMPLEMENTATION_STATUS.md`](./IMPLEMENTATION_STATUS.md) — `CURRENT`
- D2：[`REVIEWER_GUIDE.md`](./REVIEWER_GUIDE.md) — `CURRENT`（未改动） · [`SAFETY_PRIVACY_AND_FAILURES.md`](./SAFETY_PRIVACY_AND_FAILURES.md) — `CURRENT`（未改动）
- D3：[`ARCHITECTURE_OVERVIEW.md`](./ARCHITECTURE_OVERVIEW.md) — `CURRENT` · [`STORAGE_AND_AUTHORITY_BOUNDARIES.md`](./STORAGE_AND_AUTHORITY_BOUNDARIES.md) — `CURRENT`
- D4：[`GRANT_OVERVIEW.md`](./GRANT_OVERVIEW.md) — `CURRENT` · [`GLOSSARY.md`](./GLOSSARY.md) — `CURRENT`
- D5：[`EXTENDED_REFERENCE_GUIDE.md`](./EXTENDED_REFERENCE_GUIDE.md) — `CURRENT`

## 📎 Historical localization compatibility

在历史 RC-6 localization checkpoint 中，简体中文 Reader-dependent 文档属于 `REFRESH_NEEDED`。这个 literal 仅作为旧的 executable provenance/compatibility evidence 保留；它**不是当前 freshness state**。当前状态由上方 D1/D3/D4/D5 `CURRENT` markers、machine manifests 与 translation ledger 决定。

## 🧠 当前 Reader 事实

```text
RC-1…RC-7 = bounded implemented Reader layers
RC-9 = deterministic lexical PRE-ADMISSION candidate discovery
Comparator v1 = frozen evaluation · discrimination gate FAIL
NLI neutral-filter v1 = frozen evaluation · recall-safety gate FAIL
RRTIC-v1 = architecture contract only · no runtime authorization
```

```text
Reader candidate != admitted evidence
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
NLI label != proposition identity
RRTIC suspicion != adjudicated relation
physical L3 != strict Canon
```

English 仍是 primary/source language。机器状态与 translation freshness 请以 [Localization policy](../LOCALIZATION_POLICY.md) 和 [Translation status](../TRANSLATION_STATUS.md) 为准；AI/agent 应从 [Special for AI](../ai/README.md) 进入。