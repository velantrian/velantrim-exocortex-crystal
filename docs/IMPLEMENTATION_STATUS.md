# Implementation Status: Crystal vs Future Exo-Cortex Work

**Status date:** 2026-08-13  
**Retained runtime checkpoint:** `bbd816c` / PR #337  
**Signed RC-7 Reader baseline:** `main@b5541ce504af9002c8d3e2dcfa44ef4c0ead86c1` / PR #372; post-merge CI `31572918731`  
**Signed RC-9 Reader baseline:** `main@f8b7d7ea36625b6589a4cf02f12b94c5f98fdb61` / PR #376; post-merge CI `31594027040`  
**Post-RC-10 reassessment checkpoint:** signed `main@e824556f304143cdb8403f44a7b020a528e63291`, CI `31670811115` — 9/9  
**Latest bounded evaluation milestone:** issue #384 / PR #385 — Reader Retrieval Evaluation Surface v2

| Component | Status | Current boundary |
|---|---|---|
| Guardian / TruthGate / strict read projection | Implemented | retrieval/evaluation cannot bypass authority |
| SQLite ordinary local-first storage | Implemented | active ordinary profile |
| PostgreSQL/pgvector target | Inactive | `active=false`; import/equivalence only |
| Reader Core RC-1..RC-7 | Implemented/merged | bounded Reader layers |
| Reader RC-8 retrieval decision | Completed | architecture/research only |
| Reader RC-9 lexical candidate discovery | Implemented/measured | deterministic PRE-ADMISSION BM25 |
| RC-10 reuse/comparison preregistration | Completed | no comparator execution |
| Post-RC-10 reassessment | Completed | issue #382 / PR #383 |
| Reader Retrieval Evaluation Surface v2 | Frozen evaluation evidence | issue #384 / PR #385; RC-9 control reproduced |
| Model-backed comparator | **Not executed** | future separately authorized milestone |
| Reader semantic/hybrid/vector retrieval | Not implemented | separate future evidence/authorization |
| Reader SQLite FTS | Not implemented | deferred pending measured scale need |
| Dedicated/full Reader | Not implemented | `dedicated_reader_core=false` |

## Reader implementation chain

```text
RC-1 source/session identity
→ RC-2 structural map
→ RC-3 reading passes
→ RC-4 extracted propositions
→ RC-5 relation candidates
→ RC-6 bounded working sets
→ RC-7 cross-document candidates
→ Reader RC-9 lexical candidate discovery
→ RC-10 frozen comparison preregistration
→ post-RC-10 reassessment
→ Evaluation Surface v2 — fully judged evidence only
→ future separately authorized comparator, if any
```

RC-5 remains implemented in `core/reader_relations.py`.
RC-9 remains implemented in `core/reader_lexical_discovery.py`.
Historical RC-9 K=5 RC-8 benchmark remains Recall@5 `0.937500`, Precision@5 `0.187500`, MRR `0.895833`, paired hard-negative rate@5 `1.000000`; classification `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`.

## Evaluation Surface v2

Final frozen surface:

- 24 queries;
- 12 primary strata × 2;
- 6 candidates/query;
- 48 useful, 48 hard-negative and 48 neutral-decoy qrels;
- 144/144 explicit qrels, judgment coverage `1.0`;
- K=5;
- composite SHA-256 `753cc550bc5fc47697aa6d7b1cda294bf11abaa08d515816e5e1db59eb526cdd`;
- opaque content-derived candidate IDs independent of qrel labels/order.

The reviewed q04 refund-scope and q23 unconditional cache-scope conflicts are useful `POSSIBLE_CONTRADICTION` candidates. Their final review semantics do not change RC-9 ranking metrics.

Frozen unchanged RC-9 v2 control:

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

## Future comparator preregistration

The historical RC-10 screen remains independently required. The v2 gate is frozen before any model-backed result. A future comparator must retain all 42 current useful hits, recover at least 4/6 misses, reach >=46/48 useful hits / Recall@5 >=0.958333, keep MRR >=0.857639, reduce hard-negative hits to <=24/48, satisfy per-stratum constraints, declare exact backend/model/dependency/index identity or explicit no-index, record privacy review, use no `auto`, make zero query-time network calls and transmit no Reader source text externally.

```text
ELIGIBLE_FOR_ARCHITECTURE_REVIEW_ONLY
comparison pass != runtime authorization
```

## Retained Reader machine truth and authority firewall

```text
reader_core_rc1_skeleton               = true
reader_core_rc2_structural_map         = true
reader_core_rc3_multi_pass_mechanics   = true
reader_core_rc4_proposition_extraction = true
reader_core_rc5_relation_candidates    = true
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
retrieval match != evidence
similarity != identity
ranking != epistemic authority
candidate discovery != candidate adjudication
comparison pass != runtime authorization
```

No semantic/hybrid/vector Reader runtime, embeddings model execution, ANN/FAISS/HNSW, Reader FTS, active PostgreSQL/pgvector Reader path, automatic evidence admission or dedicated autonomous Reader is introduced. PostgreSQL/pgvector remains `active=false`.

Historical RC-8 corpus, RC-9 baseline and RC-10 preregistration remain byte-pinned by their existing Git blob identities.

Russian D1/D3/D4/D5 Reader documentation retains its historical localization checkpoint; eight other locale detail packs remain `REFRESH_NEEDED` — 64 detail documents. No broad localization is performed.

NLnet remains **submitted / under review / not awarded**. Approximate €50,000 remains planning only. Issues #155, #165 and #214 remain separate scopes.

After issue #384 completion, **STOP before model-backed comparator execution**.
