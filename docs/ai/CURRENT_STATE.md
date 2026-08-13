# Crystal AI Current State

**Status date:** 2026-08-13

GitHub merged `main`, executable tests and exact CI are authoritative.

## Verified predecessor

- signed `main@e824556f304143cdb8403f44a7b020a528e63291`
- signature `verified=true`, reason `valid`
- post-merge CI `31670811115` — 9/9

## Reader machine truth

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

RC-1 through RC-7 are merged bounded Reader layers.
RC-7 remains signed `main@b5541ce504af9002c8d3e2dcfa44ef4c0ead86c1`, post-merge CI `31572918731`.
RC-9 remains the deterministic lexical candidate-discovery implementation baseline in `core/reader_lexical_discovery.py`; signed `main@f8b7d7ea36625b6589a4cf02f12b94c5f98fdb61`, post-merge CI `31594027040`.
Historical classification: `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`.
RC-9 is empirical and intentionally modest.

## Retained authority markers

```text
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
working-set coverage != comprehension proof
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

## Reader Retrieval Evaluation Surface v2

Issue #384 / PR #385. Evaluation/research only.

```text
24 queries
12 primary strata
6 candidates/query
144/144 explicit qrels
judgment coverage = 1.0
K = 5
surface sha256 = 753cc550bc5fc47697aa6d7b1cda294bf11abaa08d515816e5e1db59eb526cdd
```

Final RC-9 v2 control: useful hits `42 / 48`; Recall@5 `0.875000`; fixed-slot Precision@5 `0.350000`; judged precision-over-returned `0.355932`; MRR `0.857639`; hard-negative hits `38 / 48`; hard-negative rate@5 `0.791667`; any-useful-query `1.000000`; all-useful-query `0.750000`.

Reviewed q04 refund-scope and q23 unconditional cache-scope pairs are useful `POSSIBLE_CONTRADICTION` candidates. Candidate IDs are content-derived and qrel-label-independent.

Model-backed comparator execution is NOT STARTED. Semantic/hybrid/vector Reader runtime is absent. Reader FTS and ANN/vector DB are absent. PostgreSQL/pgvector remains `active=false`.

## Localization truth

Immutable phased localization source checkpoint: `51c205fe048fd69d39fcd47b43e042a50de432bc`.
D2 checkpoint: `main@b7e6574dd7aefa2f32783ab79054fac6b3b4109f`.
Russian Reader-dependent public/detail documentation is refreshed. Russian D1/D3/D4/D5 detail pack is current. D2 reviewer/safety translations remain current across all nine supported locales.
The eight other localized root README files and Reader-dependent detail packs remain `REFRESH_NEEDED`; eight other locale detail packs require Reader refresh.
Tracked Reader detail debt remains 64 documents.

## Grant / backlog truth

NLnet remains submitted / under review / not awarded.
Approximate €50,000 remains planning only.
Issues #155, #165 and #214 remain separate scopes.

## Stop boundary

After exact-head CI, review closure, guarded merge, signed post-merge CI, Notion 3/3 read-back and issue #384 completion evidence: **STOP**.
