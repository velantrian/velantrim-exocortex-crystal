<!-- d4-source-contract: CURRENT -->
<!-- d4-source-scope: project-grant-governance-glossary -->
# 🗺️ Velantrim Exo-Cortex Crystal — Roadmap

> Only merged `main`, executable tests and exact CI are implementation truth.

**Retained runtime baseline:** `main@bbd816c09dd39a02e6de6c1014438490572f40f6`  
**Signed RC-7 Reader baseline:** `main@b5541ce504af9002c8d3e2dcfa44ef4c0ead86c1` — PR #372; post-merge CI `31572918731`  
**Signed RC-8 merge:** `main@bd85479e014c26ddebd0f4ae06385ce6625f5ab6` — PR #374  
**Signed RC-9 merge:** `main@f8b7d7ea36625b6589a4cf02f12b94c5f98fdb61` — PR #376; post-merge CI `31594027040`  
**RC-10 preregistration:** PR #378 / issue #377 completed  
**Grant reconciliation:** issue #379 / PR #380 / PR #381 completed  
**Post-RC-10 reassessment:** issue #382 / PR #383 completed at signed `main@e824556f304143cdb8403f44a7b020a528e63291`, CI `31670811115` 9/9  
**Latest bounded evaluation milestone:** issue #384 / PR #385 — Reader Retrieval Evaluation Surface v2  
**Grant status:** submitted / under review / not awarded  
**Budget change:** none

## ✅ Delivered Reader implementation baseline

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

- **RC-1** — source/version identity, locators, sessions, fidelity and coverage.
- **RC-2** — caller-supplied Structural Document Map.
- **RC-3** — deterministic multi-pass reading ledger.
- **RC-4** — source-linked `EXTRACTED_PROPOSITION` candidates.
- **RC-5 — relation candidates** — `core/reader_relations.py`; no admission/resolution authority.
- **RC-6 — bounded long context** — deterministic working sets + caller-supplied summaries.
- **RC-7 — bounded cross-document candidate links** — exact two-sided provenance; no automatic identity.
- **RC-8 — retrieval architecture decision** — architecture/research complete.
- **RC-9 — deterministic lexical candidate discovery + benchmark** — PRE-ADMISSION BM25 inspection baseline.
- **RC-10** — reuse/comparison preregistration only; no comparator execution.

## ✅ RC-9 historical control

Frozen RC-8 K=5 result: Recall@5 `0.937500`; Precision@5 `0.187500`; MRR `0.895833`;
paired hard-negative rate@5 `1.000000`; useful paired hits `15 / 16`; hard negatives `4 / 4`.

Classification: `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`.

```text
retrieval match          != evidence
similarity               != identity
repetition               != corroboration
cross-document candidate != Canon relation
ranking                  != epistemic authority
candidate discovery      != candidate adjudication
comparison pass          != runtime authorization
```

## ✅ Post-RC-10 reassessment

Issue #382 / PR #383 established:

```text
measured retrieval-quality gap != measured scaling gap
```

SQLite FTS, ANN/vector DB and server infrastructure were not selected as the next Reader mechanism.
RC-9 remains the deterministic control/fallback.

## 🧪 Reader Retrieval Evaluation Surface v2 — #384 / #385

Historical RC-8/RC-9/RC-10 artifacts remain immutable. The final v2 freeze uses opaque,
content-derived, **qrel-label-independent candidate IDs** and corrects the reviewed refund-scope
conflict to `POSSIBLE_CONTRADICTION`.

Frozen design:

```text
24 queries
12 strata × 2 queries
6 candidates/query
2 useful + 2 hard-negative + 2 neutral/query
144/144 explicit qrels
judgment coverage = 1.0
K = 5
surface sha256 = 7af2b1247e1c1c2590b6b2c830dd605da646989856b6c29cee18aac3e1f785e8
```

Unchanged RC-9 control on final v2:

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

The fixed-slot Precision@5 denominator prevents a comparator from improving precision merely by
returning fewer than K candidates; the fully judged precision-over-returned diagnostic is reported
separately.

## 🔒 Future comparator remains separate

The unchanged historical RC-10 screen remains mandatory. The new pre-result v2 gate requires,
among other conditions, retaining all 42 RC-9 v2 useful hits, recovering at least 4/6 misses,
>=46/48 useful hits, Recall@5 >=0.958333, MRR >=0.857639, hard negatives <=24/48,
per-stratum constraints, exact backend/model/dependency/index identity or explicit no-index,
privacy review, no `auto`, zero query-time network calls, zero external Reader source-text
transmission and zero authority violations.

```text
comparison pass != runtime authorization
```

No model-backed comparator is executed by #384/#385.

## 🗄️ Storage truth

```text
SQLite ordinary active local-first
PostgreSQL/pgvector inactive active=false
Reader FTS not implemented
Reader ANN/vector DB not implemented
automatic backend switching absent
```

## 🧩 Backlog remains isolated

- #155 — Epistemic Router / Evidence State RFC.
- #165 — exact normalized admitted-fact migration/dedupe; no semantic matching.
- #214 — PII fixture / reproducible supply-chain hygiene.

## 🌍 Localization

Historical Reader localization checkpoints remain immutable. Russian Reader-dependent pack remains
current to its recorded source; eight other Reader-dependent locale packs remain
`REFRESH_NEEDED` — 64 tracked detail documents. Evaluation Surface v2 performs no broad refresh.

## 🎓 Grant boundary

NLnet remains **submitted / under review / not awarded**. Approximate €50,000 is planning context
only. Work merged before an agreement is existing pre-agreement baseline and cannot later be
counted again as newly funded delivery.

## Related documents

- [Reader RC-9 lexical baseline](./docs/architecture/READER_RC9_LEXICAL_BASELINE.md)
- [Reader RC-10 preregistration](./docs/architecture/READER_RC10_RETRIEVAL_REUSE_PREREGISTRATION.md)
- [Post-RC-10 reassessment](./docs/architecture/READER_POST_RC10_REASSESSMENT.md)
- [Reader Retrieval Evaluation Surface v2](./docs/architecture/READER_RETRIEVAL_EVAL_V2.md)
- [Translation status](./docs/TRANSLATION_STATUS.md)
