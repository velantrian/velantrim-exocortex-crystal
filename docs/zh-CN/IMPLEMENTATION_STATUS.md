<!-- translation-source: docs/IMPLEMENTATION_STATUS.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- historical-translation-source: docs/IMPLEMENTATION_STATUS.md@a497b7d3cfbe59ca75b11d7449d5a728455b3130 -->
<!-- current-translation-source: docs/IMPLEMENTATION_STATUS.md@5e6301f0eaee1a6c85d8543be89dc2e606dc05a8 -->
<!-- d1-locale: zh-CN -->
<!-- d1-boundary: public-ask-read-only -->
<!-- d1-boundary: postgresql-active=false -->
<!-- d1-nonclaim: import-is-not-activation -->
<!-- d1-nonclaim: nlnet-not-awarded -->
# 🇨🇳 实现状态：Crystal 当前能力与明确未实现项

## ✅ Reader implementation boundary

```text
reader_core_rc1_skeleton = true
reader_core_rc2_structural_map = true
reader_core_rc3_multi_pass_mechanics = true
reader_core_rc4_proposition_extraction = true
reader_core_rc5_relation_candidates = true
reader_core_rc6_long_context_strategy = true
reader_core_rc7_cross_document_links = true
reader_rc9_lexical_candidate_discovery = true
dedicated_reader_core = false
semantic_hybrid_reader_runtime = false
rrtic_runtime_authorization = false
nli_reader_runtime_filter = false
```

| Component | 状态 | 当前边界 |
|---|---|---|
| Reader RC-1…RC-7 | ✅ Implemented | bounded Reader layers，不产生自动 epistemic authority |
| Reader RC-9 | ✅ Implemented | deterministic lexical PRE-ADMISSION candidate discovery |
| Comparator v1 | 🧊 Frozen evaluation | semantic recall recovered；discrimination gate FAIL |
| NLI neutral-filter v1 | 🧊 Frozen evaluation | discrimination improved；recall-safety gate FAIL |
| RRTIC-v1 | 📐 Frozen architecture contract | typed suspicion/qualifiers；没有 runtime provider |
| Guardian / TruthGate | ✅ Implemented | authority boundary，不是 retrieval component |
| TrustSnapshot / CanonicalView | ✅ Implemented | deny-dominant reconciliation / strict trusted projection |
| SQLite ordinary runtime | ✅ Active | local-first ordinary path |
| PostgreSQL/pgvector import target | ⛔ Inactive | `active=false`，不进入 normal runtime composition |
| semantic/hybrid Reader runtime | ❌ Not authorized | 无 Reader FTS/ANN/vector backend |
| RRTIC runtime provider | ❌ NOT AUTHORIZED / NOT IMPLEMENTED | architecture contract only |
| NLI Reader runtime filter | ❌ NOT AUTHORIZED / NOT IMPLEMENTED | frozen failed evaluation only |
| dedicated/full autonomous Reader | ❌ Not implemented | bounded layers ≠ autonomous Reader core |

## 🛡 Authority invariants

```text
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
cross-document link != Canon relation
retrieval match != evidence
similarity != identity
ranking != epistemic authority
candidate discovery != candidate adjudication
NLI label != proposition identity
RRTIC suspicion != adjudicated relation
evaluation pass != runtime authorization
physical L3 != strict Canon
```

RC-1…RC-7 与 RC-9 的实现不能绕过 Guardian / TruthGate，也不能因为 retrieval、ranking、NLI label 或 typed suspicion 而自动创建 strict Canon authority。

## 🧬 RRTIC-v1 implementation status

RRTIC-v1 只冻结 relation suspicion 与 structural qualifier vocabulary。它没有 model execution、hard filter、reranking、identity claim、evidence admission、adjudication、truth score、accept/reject policy 或 Canon writer。

因此：

```text
RRTIC contract implemented as architecture documentation = yes
RRTIC runtime provider = NOT AUTHORIZED / NOT IMPLEMENTED
rrtic_runtime_authorization = false
```

## 💾 Storage

```text
SQLite ordinary local-first = ACTIVE
PostgreSQL/pgvector = INACTIVE
active=false
successful import != backend activation
physical L3 != strict Canon
```

可选 PostgreSQL/pgvector surface 只覆盖 inactive import/equivalence path。没有 automatic switching、cutover、rollback、dual-write 或 Reader backend activation。

## 💶 Grant truth

```text
programme: NLnet NGI0 Commons Fund
proposal: submitted
review: in progress
award: not awarded
budget change: none
```

约 €50,000 只是 planning/transparency context，不是 approved budget 或 committed funding。

## 📎 Historical evidence

`bbd816c09dd39a02e6de6c1014438490572f40f6`、`2078 passed / 13 skipped / 0 failed` 与 `9756 statements / 100.00% line coverage` 保留为 historical compatibility evidence；它们不是当前 repository test count。

精确 live implementation 与 CI 状态必须从 GitHub、[`docs/STATUS.md`](../STATUS.md)、[`TEST_REPORT.md`](../../TEST_REPORT.md) 与 [machine-readable manifest](../status/implementation-manifest.json) 解析。