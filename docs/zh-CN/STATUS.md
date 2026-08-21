<!-- translation-source: docs/STATUS.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- historical-translation-source: docs/STATUS.md@a497b7d3cfbe59ca75b11d7449d5a728455b3130 -->
<!-- current-translation-source: docs/STATUS.md@5e6301f0eaee1a6c85d8543be89dc2e606dc05a8 -->
<!-- truthgate-v1-source: docs/STATUS.md@b4be6831a8b9f87cea815b6a0ef2c497a2d5059a -->
<!-- truthgate-v1-status: CURRENT -->
<!-- d1-locale: zh-CN -->
<!-- d1-boundary: public-ask-read-only -->
<!-- d1-boundary: postgresql-active=false -->
<!-- d1-nonclaim: import-is-not-activation -->
<!-- d1-nonclaim: nlnet-not-awarded -->
# 🇨🇳 Crystal — 当前状态

**状态日期：** 2026-08-15  
**冻结的 Reader architecture checkpoint：** `76a9493b8ba64b832472ef9bfc1f1c23ebe6654e` — Reader Retrieval Typed Inspection Contract v1 / PR #392  
**RRTIC exact-head CI：** `31754798549` — 9/9 SUCCESS  
**RRTIC post-merge CI：** `31771677028` — 9/9 SUCCESS  
**简体中文 parity audit base：** `main@5e6301f0eaee1a6c85d8543be89dc2e606dc05a8`。

## TruthGate v1 — PR #440 后重新核对

本 D1 页面已针对 `main@b4be6831a8b9f87cea815b6a0ef2c497a2d5059a` 中英文政策的实质性变化重新核对。`WORLD_FACT` 的默认 TruthGate policy 现在固定且版本化：`DEFAULT_MIN_CONFIDENCE = 0.05`，`TRUTH_GATE_POLICY_VERSION = "truth-gate-v1-fixed-0.05"`。process-local adaptation 仍仅属于 telemetry/research，不会静默改变默认 admission authority。此澄清不会启用 Reader/RAG/retrieval runtime 或 PostgreSQL/pgvector，不扩展 Canon，也不会向 Titan 转移 authority。此前的 source markers 保留为 historical provenance。

> 📎 下列 runtime 数字仅作为 retained historical compatibility evidence，不是当前 repository 的 test count。

```text
bbd816c09dd39a02e6de6c1014438490572f40f6
2078 passed / 13 skipped / 0 failed
9756 statements / 100.00% line coverage
```

## 📖 当前 Reader position

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

RC-1…RC-7 是已实现的 bounded Reader layers。RC-9 是已实现的 deterministic lexical **PRE-ADMISSION** candidate discovery。Comparator v1 与 NLI neutral-filter v1 是冻结的 evaluation evidence，两个 gate 都失败。RRTIC-v1 是冻结的 typed-inspection architecture contract，没有 runtime provider。

## 🔬 Evidence chain

```text
RC-9 lexical discovery
        ↓
Evaluation Surface v2
        ↓
Comparator v1
recall recovered · discrimination FAIL
        ↓
NLI neutral-filter v1
discrimination improved · recall-safety FAIL
        ↓
post-NLI reassessment
relation-contract mismatch
        ↓
RRTIC-v1
architecture contract only
```

保留的 RC-9 control K=5：Recall@5 `0.937500`、Precision@5 `0.187500`、MRR `0.895833`、useful hits `15/16`、hard-negative hits `4/4`；classification `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`。

Comparator classification：`SEMANTIC_RECALL_RECOVERED_DISCRIMINATION_GATE_FAILED`。  
NLI classification：`NLI_NEUTRAL_FILTER_GATE_FAILED`。

## 🧬 RRTIC-v1

RRTIC-v1 使用 suspicion-only relation families：`EQUIVALENCE_SUSPECT`、`RELATED_SUSPECT`、`CONTRADICTION_SUSPECT`、`QUALIFICATION_SUSPECT`、`TOPIC_ONLY_SUSPECT`、`UNKNOWN`，qualifier state 为 `MATCH | MISMATCH | UNKNOWN | NOT_APPLICABLE`。

它不执行 model execution、filtering、reranking、identity decision、evidence admission、contradiction adjudication 或 Canon mutation。

## 🛡 Authority boundaries

```text
coverage != comprehension proof
pass completion != comprehension proof
working-set coverage != comprehension proof
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
summary != evidence
cross-document link != Canon relation
same-topic != same proposition
possible-same-claim != claim identity
similarity signal != identity proof
repetition across sources != corroboration
retrieval match != evidence
similarity != identity
ranking != epistemic authority
candidate discovery != candidate adjudication
NLI label != proposition identity
RRTIC suspicion != adjudicated relation
evaluation pass != runtime authorization
```

Guardian、TruthGate、TrustSnapshot 与 CanonicalView 保持彼此独立的 authority/read roles。Public `HTTP /ask`、`CLI ask`、`MCP search` 保持 read-only。

## 💾 Storage / grant / localization

SQLite 是 ordinary active local-first path。PostgreSQL/pgvector 仍是 inactive target，`active=false`；不存在 automatic backend switching。`physical L3 != strict Canon`，successful import 也不是 backend activation。

NLnet 仍为 **submitted / under review / not awarded**；约 €50,000 只是 planning context，budget change none。

当前简体中文 parity 以 `main@5e6301f0eaee1a6c85d8543be89dc2e606dc05a8` 为 audit base。旧 source marker `a497b7d3cfbe59ca75b11d7449d5a728455b3130` 仅保留为历史 provenance；实时 repository lifecycle state 必须从 GitHub live 解析。