# Implementation Status: Crystal vs Future Exo-Cortex Work

**Status date:** 2026-08-13  
**Signed RC-7 Reader baseline:** `main@b5541ce504af9002c8d3e2dcfa44ef4c0ead86c1` / PR #372; post-merge CI `31572918731`  
**Signed RC-9 Reader baseline:** `main@f8b7d7ea36625b6589a4cf02f12b94c5f98fdb61` / PR #376; post-merge CI `31594027040`  
**RC-10 preregistration:** issue #377 / PR #378 completed; no comparator execution  
**Post-RC-10 reassessment:** issue #382 / PR #383 completed at signed `main@e824556f304143cdb8403f44a7b020a528e63291`; CI `31670811115` — 9/9  
**Current bounded evaluation:** issue #384 / PR #385 — Reader Retrieval Evaluation Surface v2

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
dedicated_reader_core=false
```

RC-5 relation candidates remain implemented in `core/reader_relations.py`.
Reader RC-9 lexical candidate discovery remains implemented in `core/reader_lexical_discovery.py`.
Historical RC-9 K=5 evidence remains Recall@5 `0.937500`, Precision@5 `0.187500`, MRR `0.895833`, paired hard-negative rate@5 `1.000000`; classification `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`.

## Reader Retrieval Evaluation Surface v2

Final frozen v2 surface: 24 queries, 12 primary strata ×2, 6 candidates/query, 144/144 explicit qrels, judgment coverage `1.0`, K=5, composite SHA-256 `753cc550bc5fc47697aa6d7b1cda294bf11abaa08d515816e5e1db59eb526cdd`.

Final unchanged RC-9 v2 control:

- useful hits **42 / 48**;
- Recall@5 **0.875000**;
- fixed-slot Precision@5 **0.350000**;
- judged precision-over-returned **0.355932**;
- MRR **0.857639**;
- hard-negative hits **38 / 48**;
- hard-negative rate@5 **0.791667**;
- any-useful-query **1.000000**;
- all-useful-query **0.750000**.

Classification: `LEXICAL_CONTROL_EXPOSES_MULTI_STRATUM_GAPS`.
Reviewed q04 refund-scope and q23 cache-scope conflicts are useful `POSSIBLE_CONTRADICTION` candidates. Candidate IDs are content-derived and qrel-label-independent.

## Retained Reader authority firewall

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

The historical RC-10 screen remains required. The v2 gate is frozen before any model-backed result. Passing remains `ELIGIBLE_FOR_ARCHITECTURE_REVIEW_ONLY`; comparison pass is not runtime authorization.

Model-backed comparator execution is NOT STARTED. Semantic/hybrid/vector Reader runtime, Reader FTS and ANN/vector DB remain absent. PostgreSQL/pgvector remains `active=false`.

Historical RC-8 corpus, RC-9 baseline and RC-10 preregistration remain byte-pinned. Russian D1/D3/D4/D5 Reader documentation retains its historical localization checkpoint; eight other locale detail packs remain `REFRESH_NEEDED` — 64 documents. NLnet remains **submitted / under review / not awarded**. Approximate €50,000 remains planning only. Issues #155, #165 and #214 remain separate scopes.

After issue #384 completion: **STOP before model-backed comparator execution**.
