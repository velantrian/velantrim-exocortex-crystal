<!-- d4-source-contract: CURRENT -->
<!-- d4-source-scope: project-grant-governance-glossary -->
# 🗺️ Velantrim Exo-Cortex Crystal — Roadmap

> Only merged `main`, executable tests and exact CI are implementation truth.

**Retained runtime baseline:** `main@bbd816c09dd39a02e6de6c1014438490572f40f6`  
**Signed RC-7 Reader baseline:** `main@b5541ce504af9002c8d3e2dcfa44ef4c0ead86c1` — PR #372  
**Signed RC-8 merge:** `main@bd85479e014c26ddebd0f4ae06385ce6625f5ab6` — PR #374  
**Signed RC-9 merge:** `main@f8b7d7ea36625b6589a4cf02f12b94c5f98fdb61` — PR #376  
**RC-10 preregistration:** PR #378 / issue #377 completed  
**Grant reconciliation:** issue #379 / PR #380 / PR #381 completed  
**Post-RC-10 reassessment:** issue #382 / PR #383 completed at signed `main@e824556f304143cdb8403f44a7b020a528e63291`, CI `31670811115` 9/9  
**Latest bounded evaluation milestone:** issue #384 — Reader Retrieval Evaluation Surface v2  
**Grant status:** submitted / under review / not awarded  
**Budget change:** none

## ✅ Delivered bounded Reader chain

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
- **RC-5 — relation candidates** — `POSSIBLE_CONTRADICTION`, `TENSION`, `EXCEPTION`, `QUALIFICATION`; no admission/resolution authority.
- **RC-6 — bounded long context** — working sets + caller-supplied summary with direct leaf provenance.
- **RC-7 — bounded cross-document candidate links** — explicit two-sided provenance; no automatic semantic identity.
- **RC-8** — retrieval architecture decision.
- **RC-9 — deterministic lexical candidate discovery + benchmark** — PRE-ADMISSION BM25 inspection baseline.
- **RC-10** — reuse/comparison preregistration only; no comparator execution.

## ✅ RC-9 frozen historical baseline

At K=5 on the historical RC-8 fixture:

| Metric | Result |
|---|---:|
| Recall@5 | 0.937500 |
| Precision@5 | 0.187500 |
| MRR | 0.895833 |
| Paired hard-negative rate@5 | 1.000000 |
| Useful paired hits | 15 / 16 |
| Hard-negative paired hits | 4 / 4 |

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

SQLite FTS, ANN/vector DB and server infrastructure were therefore not selected as the next
Reader mechanism. RC-9 remains the deterministic control/fallback; RRF remains ordering only;
hashing/trigram signals remain comparison controls.

## 🧪 Reader Retrieval Evaluation Surface v2 — issue #384

The v2 surface is a separate fully judged evaluation layer; historical RC-8/RC-9/RC-10 artifacts
remain immutable.

Frozen design:

- 24 queries;
- 12 primary strata × 2 queries;
- 6 candidates per query;
- 2 useful + 2 hard-negative + 2 neutral-decoy judgments per query;
- 144/144 explicit qrels; judgment coverage `1.0`;
- K=5;
- multiple cross-lingual, low-overlap, negation, modality, quantifier, temporal/version,
  jurisdiction, attribution, units/threshold, homonym, boilerplate and conditional traps.

Unchanged RC-9 control on v2:

| Metric | Result |
|---|---:|
| Useful hits | 43 / 48 |
| Useful Recall@5 | **0.895833** |
| Fully judged Precision@5 | **0.364407** |
| MRR | **0.829861** |
| Hard-negative hits | 38 / 48 |
| Hard-negative hit rate@5 | **0.791667** |
| Any-useful-query rate@5 | **1.000000** |
| All-useful-query rate@5 | **0.791667** |

Classification: `LEXICAL_CONTROL_EXPOSES_MULTI_STRATUM_GAPS`.

Durable evidence:

- `docs/architecture/READER_RETRIEVAL_EVAL_V2.md`;
- `eval/reader_retrieval_eval_v2_manifest.json`;
- `eval/reader_retrieval_eval_v2_rc9_control.json`;
- `eval/reader_retrieval_eval_v2_future_comparator_gate.json`.

This milestone adds evaluation evidence only. It does **not** add semantic/hybrid/vector Reader
runtime, a model, FTS, ANN, PostgreSQL/pgvector activation or epistemic authority.

## ⏭️ Future comparator is still separate

A future comparator requires a new authorization. It must pass both:

1. the unchanged historical RC-10 screen; and
2. the pre-result v2 gate.

Even a pass is only architecture-review eligibility.

No model-backed comparator is executed by issue #384.

## 🗄️ Storage

```text
SQLite ordinary active local-first
→ PostgreSQL/pgvector inactive import/equivalence target
→ active=false
```

Reader FTS is not implemented. Automatic backend switching is absent.

## 🧩 Isolated backlog

- #155 — Epistemic Router / Evidence State RFC.
- #165 — exact normalized admitted-fact migration/dedupe; no semantic matching.
- #214 — PII fixture / reproducible supply-chain hygiene.

## 🌍 Localization

Historical RC-7 localization checkpoint remains immutable. Russian Reader-dependent pack remains
the current localized Reader pack; eight other Reader-dependent locale packs remain
`REFRESH_NEEDED` (64 tracked detail documents). Evaluation Surface v2 does not perform a broad
localization refresh.

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

## 🔒 Retained Reader compatibility / authority markers

Historical Reader truth remains visible after Evaluation Surface v2:

- **Delivered Reader implementation baseline** includes RC-1 through RC-7; `reader_core_rc7_cross_document_links = true` and `dedicated_reader_core = false`.
- **RC-8 — retrieval architecture decision** remains completed architecture/research.
- **RC-9 — deterministic lexical candidate discovery + benchmark** remains the implemented control at `main@f8b7d7ea36625b6589a4cf02f12b94c5f98fdb61`; post-merge CI `31594027040`; RC-10 tracking `#377` is completed preregistration bookkeeping only.
- RC-7 signed history remains `main@b5541ce504af9002c8d3e2dcfa44ef4c0ead86c1`, post-merge CI `31572918731`.
- RC-7 authority vocabulary remains: `cross-document link != Canon relation`; `same-topic != same proposition`; `possible-same-claim != claim identity`; `similarity signal != identity proof`; `repetition across sources != corroboration`.
- There is **no automatic semantic matching**. `embeddings/ANN/vector` Reader runtime is not implemented; **semantic/hybrid retrieval may be compared later** only under separate authorization.
- PostgreSQL/pgvector remains `active=false`; NLnet remains submitted / under review / not awarded.
- Issue `#382` selected Evaluation Surface v2; `comparison pass != runtime authorization`.
