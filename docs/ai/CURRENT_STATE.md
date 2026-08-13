# Crystal AI Current State

**Status date:** 2026-08-13

GitHub merged `main`, executable tests, exact CI and machine-readable artifacts are authoritative.
Notion is synchronized strategy/history only after exact post-merge evidence.

## Latest verified checkpoint before Evaluation Surface v2

- signed `main`: `e824556f304143cdb8403f44a7b020a528e63291`;
- signature: `verified=true`, reason `valid`;
- exact push CI `31670811115`: 9/9 successful;
- issue #382 / PR #383: post-RC-10 reassessment completed;
- issue #377: closed completed bookkeeping for preregistration-only PR #378;
- issue #379: completed grant-presentation reconciliation.

Evaluation Surface v2 is tracked by issue #384 / PR #385 and is evaluation/research work only.

## Reader implementation truth

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

RC-9 remains the implemented deterministic lexical PRE-ADMISSION candidate-discovery runtime.
Evaluation Surface v2 adds no new Reader runtime layer.

Historical RC-9 classification remains `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`.
Historical K=5 RC-8 evidence remains Recall@5 `0.937500`, Precision@5 `0.187500`, MRR
`0.895833`, useful paired hits 15/16 and hard-negative paired hits 4/4.

## Evaluation Surface v2 — final pre-result freeze

```text
24 queries
12 primary strata
6 candidates/query
144 explicit candidate-query qrels
judgment coverage = 1.0
K = 5
surface sha256 = 7af2b1247e1c1c2590b6b2c830dd605da646989856b6c29cee18aac3e1f785e8
```

Each query has 2 useful, 2 hard-negative and 2 neutral-decoy candidates. Final candidate IDs are
opaque, content-derived and qrel-label-independent; deterministic ordering no longer encodes
judgment class. The reviewed `v2-q04` refund-scope conflict is a useful
`POSSIBLE_CONTRADICTION`.

Unchanged RC-9 on final v2:

- useful hits: **42 / 48**;
- Useful Recall@5: **0.875000**;
- Precision@5 with fixed K slots: **0.350000**;
- judged precision over returned: **0.355932**;
- MRR: **0.857639**;
- hard-negative hits: **38 / 48**;
- hard-negative hit rate@5: **0.791667**;
- any-useful-query rate@5: **1.000000**;
- all-useful-query rate@5: **0.750000**.

Classification: `LEXICAL_CONTROL_EXPOSES_MULTI_STRATUM_GAPS`.

These are candidate-retrieval metrics, not truth, proposition identity, corroboration,
contradiction resolution or evidence-admission metrics.

## Future comparator remains NOT STARTED

The v2 future-comparator gate is frozen **before any model-backed result**. A later comparator
requires separate authorization and must pass both the unchanged historical RC-10 screen and
the v2 gate. Exact backend/model/dependency/index identity, privacy review, no `auto`, zero
query-time network and zero external Reader source-text transmission are mandatory.

```text
comparison pass != runtime authorization
```

No SentenceTransformer or other model is executed or downloaded in issue #384 / PR #385.

## Authority invariants

```text
coverage != comprehension proof
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
comparison pass != runtime authorization
```

No Reader evaluation result may mutate `truth_status`/ESM, strict Canon, Guardian, TruthGate,
confidence, evidence sufficiency or contradiction winners.

## Runtime / storage truth

- SQLite ordinary active local-first;
- PostgreSQL/pgvector inactive `active=false`;
- Reader FTS absent;
- Reader ANN/vector DB absent;
- semantic/hybrid/vector Reader runtime absent;
- no model dependency added by Evaluation Surface v2;
- existing admitted-memory retrieval remains a separate authority/data lifecycle.

## Historical evaluation preservation

The historical RC-8 corpus, RC-9 result and RC-10 preregistration are byte-pinned by Git blob
identity and remain unchanged.

## Localization truth

The immutable phased localization source checkpoint
`51c205fe048fd69d39fcd47b43e042a50de432bc` remains historical evidence. D2 retains its own
translation checkpoint `main@b7e6574dd7aefa2f32783ab79054fac6b3b4109f`.

Russian Reader-dependent public/detail documentation is refreshed. Russian D1/D3/D4/D5 detail
pack is current. D2 reviewer/safety translations remain current across all nine supported locales.
The **eight other localized root README files** and Reader-dependent detail packs remain
`REFRESH_NEEDED`; eight other locale detail packs require Reader refresh. Tracked Reader detail
debt remains 64 documents. Evaluation Surface v2 performs no broad localization refresh.

## Open backlog boundaries

- #155 — Epistemic Router / Evidence State RFC;
- #165 — exact normalized admitted-fact migration/dedupe, no semantic matching;
- #214 — PII fixture / supply-chain hygiene.

## Grant truth

NLnet remains **submitted / under review / not awarded**. Approximate €50,000 remains planning
only. RC-1 through RC-9, PR #378, post-RC-10 reassessment and Evaluation Surface v2 are existing
pre-agreement work if completed before any funding agreement.

## Retained historical Reader compatibility markers

RC-1 through RC-7 are merged bounded Reader layers. RC-7 remains signed
`main@b5541ce504af9002c8d3e2dcfa44ef4c0ead86c1`, post-merge CI `31572918731`, with
`reader_core_rc7_cross_document_links = true`.

**RC-9 — deterministic lexical candidate discovery: COMPLETE.** The implementation baseline
remains signed `main@f8b7d7ea36625b6589a4cf02f12b94c5f98fdb61`, post-merge CI `31594027040`;
issue `#377` is completed preregistration bookkeeping only.

Issue `#382` completed the post-RC-10 reassessment and selected Evaluation Surface v2. There is no
automatic semantic matching; `embeddings/ANN/vector` Reader runtime is absent, semantic/hybrid
retrieval may be compared later only after separate authorization, PostgreSQL/pgvector remains
`active=false`, and NLnet remains submitted / under review / not awarded.

## Stop boundary

Issue #384 completes only after exact-head CI, semantic review, guarded merge, signed post-merge
CI, Notion 3/3 synchronization/read-back, completion evidence and final live audit.

Then STOP. Do not execute a model-backed comparator, add semantic/hybrid/vector runtime, FTS/ANN,
activate PostgreSQL/pgvector, implement #155/#165/#214 or perform broad localization.
