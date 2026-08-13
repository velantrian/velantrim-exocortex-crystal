# Velantrim Crystal — Current Status

**Status date:** 2026-08-13  
**Retained runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6` / PR #337  
**Signed RC-7 Reader baseline:** `b5541ce504af9002c8d3e2dcfa44ef4c0ead86c1` / PR #372  
**Signed RC-9 Reader merge:** `f8b7d7ea36625b6589a4cf02f12b94c5f98fdb61` / PR #376  
**Post-RC-10 reassessment checkpoint:** signed `main@e824556f304143cdb8403f44a7b020a528e63291`, push CI `31670811115` — 9/9 successful  
**Latest bounded evaluation milestone:** issue #384 — Reader Retrieval Evaluation Surface v2

## Current Reader position

RC-0 is normative architecture. RC-1 through RC-7 are bounded implemented Reader/domain layers.
RC-8 is a completed architecture decision. RC-9 is the implemented deterministic lexical
PRE-ADMISSION retrieval baseline. PR #378 / issue #377 is completed preregistration only.
Issue #382 / PR #383 completed the post-RC-10 reassessment. Issue #384 freezes stronger
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

## RC-9 deterministic lexical baseline — historical control

The unchanged RC-9 method is `reader_rc9_bm25_lexical_v1`.

Historical RC-8 K=5 result:

| Metric | Result |
|---|---:|
| Recall@5 | 0.937500 |
| Precision@5 | 0.187500 |
| MRR | 0.895833 |
| Paired hard-negative rate@5 | 1.000000 |
| Useful hits | 15 / 16 |
| Hard-negative hits | 4 / 4 |

Classification: `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`.

These are retrieval measurements, not semantic/adjudication accuracy.

## Evaluation Surface v2 — frozen judged evidence

Issue #384 adds a separate surface rather than rewriting historical fixtures:

```text
24 queries
× 6 candidates per query
= 144 candidate-query judgments
```

Each query has exactly:

- 2 `USEFUL_CANDIDATE`;
- 2 `HARD_NEGATIVE`;
- 2 `NEUTRAL_DECOY`.

There are 12 primary strata with two queries each and judgment coverage is `1.0`.

Unchanged RC-9 on v2 at K=5:

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

The v2 result confirms that the measured problem is broader retrieval quality, not a demonstrated
Reader scale blocker.

## Frozen future gate

The historical RC-10 screen remains unchanged. Evaluation Surface v2 adds a second pre-result
gate for a **future separately authorized** comparator.

The v2 gate requires, among other conditions:

- retain all 43 useful candidates RC-9 already retrieves on v2;
- recover at least 3 of the 5 RC-9 v2 useful misses;
- useful hits >= 46/48 and Recall@5 >= 0.958333;
- MRR >= 0.829861;
- hard-negative hits <= 24/48;
- per-stratum useful Recall@5 >= 0.75;
- per-stratum hard-negative hit rate@5 <= 0.50;
- exact backend/model/dependency identity;
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

## Stop boundary

After issue #384 receives exact-head CI, semantic review, guarded merge, signed exact post-merge
CI, Notion 3/3 synchronization/read-back, completion evidence and final live audit: **STOP**.

Do not automatically execute a model-backed comparator, add semantic/hybrid/vector Reader
runtime, add FTS/ANN, activate PostgreSQL/pgvector, mutate epistemic authority, implement
#155/#165/#214 or perform broad localization.
