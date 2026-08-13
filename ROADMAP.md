<!-- d4-source-contract: CURRENT -->
<!-- d4-source-scope: project-grant-governance-glossary -->
# 🗺️ Velantrim Exo-Cortex Crystal — Roadmap

> Only merged `main`, executable tests and exact CI are implementation truth.

**Retained runtime baseline:** `main@bbd816c09dd39a02e6de6c1014438490572f40f6`  
**Signed RC-7 Reader baseline:** `main@b5541ce504af9002c8d3e2dcfa44ef4c0ead86c1` — PR #372; post-merge CI `31572918731`  
**Signed RC-9 merge:** `main@f8b7d7ea36625b6589a4cf02f12b94c5f98fdb61` — PR #376; post-merge CI `31594027040`  
**RC-10 preregistration:** PR #378 / issue #377 completed  
**Grant reconciliation:** issue #379 / PR #380 / PR #381 completed  
**Post-RC-10 reassessment:** issue #382 / PR #383 completed at signed `main@e824556f304143cdb8403f44a7b020a528e63291`, CI `31670811115` 9/9  
**Latest bounded evaluation milestone:** issue #384 / PR #385 — Reader Retrieval Evaluation Surface v2  
**Grant status:** submitted / under review / not awarded

## ✅ Delivered Reader baseline

```text
reader_core_rc1_skeleton               = true
reader_core_rc2_structural_map         = true
reader_core_rc3_multi_pass_mechanics   = true
reader_core_rc4_proposition_extraction = true
reader_core_rc5_relation_candidates    = true
reader_core_rc6_long_context_strategy  = true
reader_core_rc7_cross_document_links   = true
dedicated_reader_core                  = false
```

- **RC-5 — relation candidates** — `core/reader_relations.py`; no admission/resolution authority.
- **RC-6 — bounded long context** — deterministic working sets + caller-supplied summaries.
- **RC-7 — bounded cross-document candidate links** — exact two-sided provenance; no automatic identity.
- **RC-9 — deterministic lexical candidate discovery + benchmark** — PRE-ADMISSION BM25 inspection baseline.

RC-1 through RC-7 are bounded implemented Reader layers. RC-8 is a completed retrieval architecture decision. RC-10 is preregistration only and executed no comparator.

Historical RC-9 K=5 RC-8 evidence remains Recall@5 `0.937500`, Precision@5 `0.187500`, MRR `0.895833`, useful hits `15 / 16`, hard-negative hits `4 / 4`; classification `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`.

## 🔒 Retained authority vocabulary

```text
retrieval match != evidence
similarity != identity
repetition != corroboration
cross-document candidate != Canon relation
cross-document link != Canon relation
same-topic != same proposition
possible-same-claim != claim identity
similarity signal != identity proof
repetition across sources != corroboration
ranking != epistemic authority
candidate discovery != candidate adjudication
comparison pass != runtime authorization
```

## ✅ Post-RC-10 reassessment

Issue #382 / PR #383 established:

```text
measured retrieval-quality gap != measured scaling gap
```

SQLite FTS, ANN/vector DB and server infrastructure were not selected as the next Reader mechanism. RC-9 remains the deterministic control/fallback.

## 🧪 Reader Retrieval Evaluation Surface v2 — #384 / #385

Historical RC-8/RC-9/RC-10 artifacts remain immutable. The final v2 surface uses opaque content-derived qrel-label-independent candidate IDs.

```text
24 queries
12 strata × 2 queries
6 candidates/query
2 useful + 2 hard-negative + 2 neutral/query
144/144 explicit qrels
judgment coverage = 1.0
K = 5
surface sha256 = 753cc550bc5fc47697aa6d7b1cda294bf11abaa08d515816e5e1db59eb526cdd
```

Reviewed q04 refund-scope and q23 unconditional cache-scope conflicts are useful `POSSIBLE_CONTRADICTION` candidates. The q23 review-class correction changes qrels/surface identity but not RC-9 ranking metrics.

| Metric | Result |
|---|---:|
| Useful hits | **42 / 48** |
| Useful Recall@5 | **0.875000** |
| Precision@5 — fixed K slots | **0.350000** |
| Judged precision over returned | **0.355932** |
| MRR | **0.857639** |
| Hard-negative hits | **38 / 48** |
| Hard-negative hit rate@5 | **0.791667** |
| Any-useful-query rate@5 | **1.000000** |
| All-useful-query rate@5 | **0.750000** |

Classification: `LEXICAL_CONTROL_EXPOSES_MULTI_STRATUM_GAPS`.

## 🔒 Future comparator remains separate

The unchanged historical RC-10 screen remains mandatory. The pre-result v2 gate requires retaining all 42 RC-9 v2 useful hits, recovering at least 4/6 misses, >=46/48 useful hits, Recall@5 >=0.958333, MRR >=0.857639, hard negatives <=24/48, per-stratum constraints, exact backend/model/dependency/index identity or explicit no-index, privacy review, no `auto`, zero query-time network calls, zero external Reader source-text transmission and zero authority violations.

```text
comparison pass != runtime authorization
```

No model-backed comparator is executed by #384/#385.

## 🗄️ Storage / backlog truth

```text
SQLite ordinary active local-first
PostgreSQL/pgvector inactive active=false
Reader FTS not implemented
Reader ANN/vector DB not implemented
automatic backend switching absent
```

Issues #155, #165 and #214 remain isolated backlog. No broad localization refresh is part of Evaluation Surface v2.

## 🎓 Grant boundary

NLnet remains **submitted / under review / not awarded**. Approximate €50,000 is planning context only. Work merged before an agreement is existing pre-agreement baseline and cannot later be counted as newly funded delivery.

## Related documents

- [Reader RC-9 lexical baseline](./docs/architecture/READER_RC9_LEXICAL_BASELINE.md)
- [Reader RC-10 preregistration](./docs/architecture/READER_RC10_RETRIEVAL_REUSE_PREREGISTRATION.md)
- [Post-RC-10 reassessment](./docs/architecture/READER_POST_RC10_REASSESSMENT.md)
- [Reader Retrieval Evaluation Surface v2](./docs/architecture/READER_RETRIEVAL_EVAL_V2.md)
- [Translation status](./docs/TRANSLATION_STATUS.md)
