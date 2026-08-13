# Crystal AI Current State

**Status date:** 2026-08-13

GitHub merged `main`, executable tests, exact CI and machine-readable artifacts are authoritative.
Notion is synchronized strategy/history after exact post-merge evidence.

## Latest verified checkpoint before Evaluation Surface v2

- signed `main`: `e824556f304143cdb8403f44a7b020a528e63291`;
- signature: `verified=true`, reason `valid`;
- exact push CI `31670811115`: 9/9 successful;
- issue #382 / PR #383: post-RC-10 reassessment completed;
- issue #377: closed completed bookkeeping for preregistration-only PR #378;
- issue #379: completed grant-presentation reconciliation.

Evaluation Surface v2 is tracked by issue #384 and is evaluation/research work only.

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
Evaluation Surface v2 does not add a new Reader runtime layer.

Historical RC-9 classification remains:

```text
LEXICAL_BASELINE_EXPOSES_MEASURED_GAP
```

Historical K=5 RC-8 evidence remains Recall@5 `0.937500`, Precision@5 `0.187500`, MRR
`0.895833`, useful paired hits 15/16 and hard-negative paired hits 4/4.

## Evaluation Surface v2

The stronger pre-frozen surface contains:

```text
24 queries
12 primary strata
6 candidates/query
144 explicit candidate-query qrels
judgment coverage = 1.0
K = 5
```

Each query has 2 useful, 2 hard-negative and 2 neutral-decoy candidates. The surface covers
cross-lingual and low-overlap paraphrase plus repeated polarity, modality, quantifier,
temporal/version, jurisdiction, attribution, units/threshold, homonym, boilerplate and
conditional/exception traps.

Unchanged RC-9 on v2 measures:

- useful hits: **43/48**;
- Useful Recall@5: **0.895833**;
- fully judged Precision@5: **0.364407**;
- MRR: **0.829861**;
- hard-negative hits: **38/48**;
- hard-negative hit rate@5: **0.791667**;
- any-useful-query rate@5: **1.000000**;
- all-useful-query rate@5: **0.791667**.

Classification:

```text
LEXICAL_CONTROL_EXPOSES_MULTI_STRATUM_GAPS
```

These results measure candidate retrieval only. They do not measure truth, proposition identity,
corroboration, contradiction resolution or evidence admission.

## Future comparator remains NOT STARTED

A second future-comparator gate is frozen in
`eval/reader_retrieval_eval_v2_future_comparator_gate.json` **before any model result**.

A later comparator requires separate authorization and must pass both the unchanged historical
RC-10 screen and the v2 gate. A pass remains architecture-review eligibility only.

```text
comparison pass != runtime authorization
```

No SentenceTransformer or other model is executed or downloaded in issue #384.

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
- semantic/hybrid Reader runtime absent;
- no model dependency added by Evaluation Surface v2;
- existing admitted-memory retrieval remains a separate authority/data lifecycle.

## Historical evaluation preservation

The historical RC-8 corpus, RC-9 result and RC-10 preregistration are byte-pinned by Git blob
identity and remain unchanged.

## Localization truth

The immutable phased localization source checkpoint
`51c205fe048fd69d39fcd47b43e042a50de432bc` remains historical evidence. D2 retains its own
translation checkpoint `main@b7e6574dd7aefa2f32783ab79054fac6b3b4109f`.

Russian Reader-dependent public/detail documentation is refreshed. Russian D1/D3/D4/D5 detail pack is current.
D2 reviewer/safety translations remain current across all nine supported locales. The eight other localized root README files and Reader-dependent detail packs remain `REFRESH_NEEDED`; in other words, eight other locale detail packs require Reader refresh. Tracked Reader detail debt remains 64 documents. Evaluation Surface v2 performs no broad localization refresh.

## Open backlog boundaries

- #155 — Epistemic Router / Evidence State RFC;
- #165 — exact normalized admitted-fact migration/dedupe, no semantic matching;
- #214 — PII fixture / supply-chain hygiene.

## Grant truth

NLnet remains **submitted / under review / not awarded**. Approximate €50,000 remains planning
only. RC-1 through RC-9, PR #378, post-RC-10 reassessment and Evaluation Surface v2 are existing
pre-agreement work if completed before any funding agreement.

## Stop boundary

Issue #384 completes only after exact-head CI, semantic review, guarded merge, signed
post-merge CI, Notion 3/3 synchronization/read-back, completion evidence and final live audit.

Then STOP. Do not execute a model-backed comparator, add semantic/hybrid/vector runtime, FTS/ANN,
activate PostgreSQL/pgvector, implement #155/#165/#214 or perform broad localization.
