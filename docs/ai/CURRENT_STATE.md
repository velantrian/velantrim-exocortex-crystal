# Crystal AI Current State

**Status date:** 2026-08-13

GitHub merged `main`, executable tests, exact CI and machine-readable artifacts are authoritative.
Notion is synchronized only after exact post-merge evidence.

## Verified predecessor checkpoint

- signed `main@e824556f304143cdb8403f44a7b020a528e63291`;
- signature `verified=true`, reason `valid`;
- push CI `31670811115`: 9/9 successful;
- issue #382 / PR #383 completed the post-RC-10 reassessment;
- issue #377 is completed RC-10 preregistration bookkeeping.

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

RC-7 remains signed `main@b5541ce504af9002c8d3e2dcfa44ef4c0ead86c1`, post-merge CI `31572918731`.
RC-9 remains the deterministic lexical candidate-discovery implementation baseline for PRE-ADMISSION inspection in `core/reader_lexical_discovery.py`; signed `main@f8b7d7ea36625b6589a4cf02f12b94c5f98fdb61`, post-merge CI `31594027040`.

Historical RC-9 classification remains `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`; K=5 RC-8 evidence remains Recall@5 `0.937500`, Precision@5 `0.187500`, MRR `0.895833`, useful paired hits 15/16 and hard-negative paired hits 4/4.
RC-9 is empirical and intentionally modest: it is a bounded lexical retrieval baseline, not semantic understanding or evidence admission.

## Reader Retrieval Evaluation Surface v2

Issue #384 / PR #385 freezes evaluation evidence only.

```text
24 queries
12 primary strata
6 candidates/query
144 explicit qrels
judgment coverage = 1.0
K = 5
surface sha256 = 753cc550bc5fc47697aa6d7b1cda294bf11abaa08d515816e5e1db59eb526cdd
```

Candidate IDs are opaque, content-derived and qrel-label-independent. The reviewed `v2-q04` refund-scope conflict and `v2-q23` unconditional cache-scope conflict are both useful `POSSIBLE_CONTRADICTION` candidates. The q23 review-class correction changes the frozen qrels/surface identity but does not change the useful/hard/neutral counts or RC-9 retrieval metrics.

Final unchanged RC-9 v2 control:

- useful hits **42 / 48**;
- Useful Recall@5 **0.875000**;
- fixed-slot Precision@5 **0.350000**;
- judged precision over returned **0.355932**;
- MRR **0.857639**;
- hard-negative hits **38 / 48**;
- hard-negative hit rate@5 **0.791667**;
- any-useful-query rate@5 **1.000000**;
- all-useful-query rate@5 **0.750000**.

Classification: `LEXICAL_CONTROL_EXPOSES_MULTI_STRATUM_GAPS`.

## Future comparator boundary

Model-backed comparator execution is **NOT STARTED**. A later comparator requires separate authorization and must pass the unchanged historical RC-10 screen plus the frozen v2 gate.

```text
retrieval match != evidence
similarity != identity
cross-document link != Canon relation
same-topic != same proposition
possible-same-claim != claim identity
similarity signal != identity proof
repetition across sources != corroboration
ranking != epistemic authority
candidate discovery != candidate adjudication
comparison pass != runtime authorization
```

No semantic/hybrid/vector Reader runtime, Reader FTS, ANN/vector DB, storage activation or new model dependency is added by Evaluation Surface v2. PostgreSQL/pgvector remains `active=false`.

## Localization truth

The immutable phased localization source checkpoint `51c205fe048fd69d39fcd47b43e042a50de432bc` remains historical evidence. D2 retains `main@b7e6574dd7aefa2f32783ab79054fac6b3b4109f`.

Russian Reader-dependent public/detail documentation is refreshed. Russian D1/D3/D4/D5 detail pack is current. D2 reviewer/safety translations remain current across all nine supported locales.
The eight other localized root README files and Reader-dependent detail packs remain `REFRESH_NEEDED`; tracked Reader detail debt remains 64 documents.

## Grant and backlog truth

NLnet remains **submitted / under review / not awarded**. Approximate €50,000 remains planning only. Open backlog scopes remain #155, #165 and #214 and are not implemented by this milestone.

## Stop boundary

After exact-head CI, review closure, guarded merge, signed post-merge CI, Notion 3/3 synchronization/read-back and issue #384 completion evidence: **STOP**.
