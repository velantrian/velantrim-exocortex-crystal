# Velantrim Crystal — Current Status

**Status date:** 2026-08-13  
**Retained runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6` / PR #337  
**Signed RC-7 Reader baseline:** `b5541ce504af9002c8d3e2dcfa44ef4c0ead86c1` / PR #372; post-merge CI `31572918731`  
**Signed RC-9 Reader merge:** `f8b7d7ea36625b6589a4cf02f12b94c5f98fdb61` / PR #376; post-merge CI `31594027040`  
**Post-RC-10 reassessment checkpoint:** signed `main@e824556f304143cdb8403f44a7b020a528e63291`, push CI `31670811115` — 9/9  
**Latest bounded evaluation milestone:** issue #384 / PR #385 — Reader Retrieval Evaluation Surface v2

## Current Reader position

RC-0 is normative architecture. RC-1 through RC-7 are bounded implemented Reader/domain layers.
RC-8 is a completed architecture/research decision. RC-9 is the implemented deterministic lexical
PRE-ADMISSION retrieval baseline. PR #378 / issue #377 is completed preregistration only.
Issue #382 / PR #383 completed the post-RC-10 reassessment. Issue #384 / PR #385 freezes stronger
evaluation evidence without adding Reader runtime.

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

RC-5 remains implemented in `core/reader_relations.py`.
RC-9 remains implemented in `core/reader_lexical_discovery.py`.

## RC-9 deterministic lexical baseline — historical control

Historical RC-8 K=5 evidence remains:

| Metric | Result |
|---|---:|
| Recall@5 | 0.937500 |
| Precision@5 | 0.187500 |
| MRR | 0.895833 |
| Paired hard-negative rate@5 | 1.000000 |
| Useful hits | 15 / 16 |
| Hard-negative hits | 4 / 4 |

Classification: `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`.

## Evaluation Surface v2 — final frozen judged evidence

Issue #384 adds a separate fully judged surface rather than rewriting historical fixtures:

```text
24 queries
12 primary strata × 2
6 candidates/query
48 useful qrels
48 hard-negative qrels
48 neutral-decoy qrels
144/144 explicit qrels
judgment coverage = 1.0
K = 5
surface sha256 = 753cc550bc5fc47697aa6d7b1cda294bf11abaa08d515816e5e1db59eb526cdd
```

Candidate IDs are opaque, content-derived and qrel-label-independent; their order cannot encode
useful/hard/neutral position. The reviewed refund-scope and unconditional cache-scope conflicts are
both useful `POSSIBLE_CONTRADICTION` candidates. These review-class corrections preserve the
2 useful / 2 hard-negative / 2 neutral design and do not change RC-9 retrieval metrics.

Unchanged RC-9 on v2:

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

The fixed-slot Precision@5 denominator is `24 × 5`; a method cannot improve it by abstaining.
The precision-over-returned diagnostic is fully judged but reported separately.

## Frozen future gate

The unchanged historical RC-10 screen remains independently mandatory. The v2 gate is frozen
before any model-backed result and requires, among other conditions:

- retain all 42 useful candidates RC-9 already retrieves on v2;
- recover at least 4 of 6 v2 useful misses;
- useful hits >= 46/48 and Recall@5 >= 0.958333;
- MRR >= 0.857639;
- hard-negative hits <= 24/48;
- per-stratum useful Recall@5 >= 0.75;
- per-stratum hard-negative hit rate@5 <= 0.50;
- exact backend/model/dependency identity;
- exact index identity when indexed, or explicit no-index declaration;
- privacy review;
- no `auto` backend;
- zero query-time network calls;
- zero external Reader source-text transmission;
- zero authority violations.

No model-backed comparator is executed by issue #384.

```text
comparison pass != runtime authorization
```

## Reader authority boundaries

```text
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
working-set coverage != comprehension proof
summary != source text
summary != evidence
summary != verified fact
summary != Canon admission
cross-document link != Canon relation
cross-document support != admitted evidence
cross-document contradiction candidate != confirmed contradiction
same-topic != same proposition
possible-same-claim != claim identity
similarity signal != identity proof
repetition across sources != corroboration
retrieval match != evidence
similarity != identity
ranking != epistemic authority
candidate discovery != candidate adjudication
comparison pass != runtime authorization
```

Guardian, TruthGate, TrustSnapshot and CanonicalView remain unchanged. Public `HTTP /ask`,
`CLI ask` and `MCP search` remain admitted-memory read-only query surfaces, not Reader v2
evaluation interfaces.

## Storage truth

```text
SQLite ordinary active local-first
→ backup / verify / inactive restore
→ bounded logical export
→ PostgreSQL 16 + pgvector inactive import/equivalence
→ active=false
```

Reader SQLite FTS is not implemented. No ANN/vector DB is introduced. Automatic backend
switching remains absent.

## Evaluation artifacts

- `docs/architecture/READER_RETRIEVAL_EVAL_V2.md`
- `eval/reader_retrieval_eval_v2_queries.jsonl`
- `eval/reader_retrieval_eval_v2_candidates.jsonl`
- `eval/reader_retrieval_eval_v2_qrels.jsonl`
- `eval/reader_retrieval_eval_v2_manifest.json`
- `eval/reader_retrieval_eval_v2_rc9_control.json`
- `eval/reader_retrieval_eval_v2_future_comparator_gate.json`
- `scripts/bench_reader_eval_v2_lexical.py`

Historical RC-8, RC-9 and RC-10 evidence remains byte-identical.

## Backlog boundaries

- #165: exact normalized admitted-fact dedupe/migration only; no semantic matching.
- #155: downstream Epistemic Router / Evidence State RFC.
- #214: fixture/PII/supply-chain hygiene.

## Localization truth

Russian Reader-dependent D1/D3/D4/D5 surfaces retain their immutable historical checkpoint.
Eight other Reader-dependent locale packs remain `REFRESH_NEEDED`, 64 tracked detail documents.
Evaluation Surface v2 is English evaluation/research truth only; no broad localization is run.

## Grant status

NLnet remains **submitted / under review / not awarded**. Approximate **€50,000** is planning
context only. Budget change: none. RC-1 through RC-9, PR #378, the post-RC-10 reassessment and
Evaluation Surface v2 are existing pre-agreement repository work if merged before an agreement.

## Retained historical Reader truth markers

```text
reader_core_rc6_long_context_strategy  = true
reader_core_rc7_cross_document_links   = true
dedicated_reader_core                  = false
working-set coverage != comprehension proof
summary != evidence
cross-document link != Canon relation
same-topic != same proposition
possible-same-claim != claim identity
similarity signal != identity proof
repetition across sources != corroboration
candidate discovery != candidate adjudication
comparison pass != runtime authorization
```

RC-7 remains signed `main@b5541ce504af9002c8d3e2dcfa44ef4c0ead86c1`, exact post-merge CI
`31572918731`. RC-9 remains signed `main@f8b7d7ea36625b6589a4cf02f12b94c5f98fdb61`,
runtime module `core/reader_lexical_discovery.py`, exact post-merge CI `31594027040`; RC-10 issue
`#377` is completed preregistration bookkeeping only. Historical RC-9 classification remains
`LEXICAL_BASELINE_EXPOSES_MEASURED_GAP` with Recall@5 `0.937500` and paired hard-negative
rate@5 `1.000000`.

Issue `#382` completed the reassessment and selected Evaluation Surface v2. There is no automatic
semantic matching; `embeddings/ANN/vector` Reader runtime is absent and semantic/hybrid retrieval
may be compared later only after separate authorization. PostgreSQL/pgvector remains
`active=false`; NLnet remains submitted / under review / not awarded.

## Stop boundary

After issue #384 receives exact-head CI, semantic review, guarded merge, signed exact post-merge
CI, Notion 3/3 synchronization/read-back, completion evidence and final live audit: **STOP**.

Do not automatically execute a model-backed comparator, add semantic/hybrid/vector Reader runtime,
add FTS/ANN, activate PostgreSQL/pgvector, mutate epistemic authority, implement #155/#165/#214
or perform broad localization.
