# Implementation Status: Crystal vs Future Exo-Cortex Work

**Status date:** 2026-08-13  
**Retained runtime checkpoint:** `bbd816c` / PR #337  
**Signed RC-7 Reader baseline:** `main@b5541ce504af9002c8d3e2dcfa44ef4c0ead86c1` / PR #372; post-merge CI `31572918731`  
**Signed RC-9 Reader baseline:** `main@f8b7d7ea36625b6589a4cf02f12b94c5f98fdb61` / PR #376; post-merge CI `31594027040`  
**Post-RC-10 reassessment checkpoint:** signed `main@e824556f304143cdb8403f44a7b020a528e63291`, CI `31670811115` — 9/9  
**Latest bounded evaluation milestone:** issue #384 / PR #385 — Reader Retrieval Evaluation Surface v2  
**Machine-readable runtime status:** [status/implementation-manifest.json](./status/implementation-manifest.json)

| Component | Status | Current boundary |
|---|---|---|
| Guardian / TruthGate / strict read projection | Implemented | retrieval/evaluation cannot bypass authority |
| Read-only HTTP/CLI/MCP query boundary | Implemented | ordinary queries do not mutate Canon |
| SQLite ordinary local-first storage | Implemented | active ordinary profile |
| PostgreSQL/pgvector target | Inactive | `active=false`; import/equivalence only |
| Automatic SQLite/PostgreSQL switching | Forbidden | absent |
| Reader Core RC-0 | Documented | normative contract |
| Reader Core RC-1 skeleton | Implemented/merged | `core/reader_core.py` |
| Reader Core RC-2 structural map | Implemented/merged | `core/reader_structure.py` |
| Reader Core RC-3 multi-pass mechanics | Implemented/merged | `core/reader_passes.py` |
| Reader Core RC-4 proposition extraction | Implemented/merged | `core/reader_extraction.py` |
| Reader Core RC-5 relation candidates | Implemented/merged | `core/reader_relations.py` |
| Reader Core RC-6 long-context strategy | Implemented/merged | bounded working sets |
| Reader Core RC-7 cross-document links | Implemented/merged | exact two-sided provenance |
| Reader RC-8 retrieval decision | Completed | architecture/research only |
| Reader RC-9 lexical candidate discovery | Implemented/measured | deterministic PRE-ADMISSION BM25 |
| RC-10 reuse/comparison preregistration | Completed | no comparator execution |
| Post-RC-10 reassessment | Completed | issue #382 / PR #383 |
| Reader Retrieval Evaluation Surface v2 | Frozen evaluation evidence | issue #384 / PR #385; RC-9 control reproduced |
| Model-backed comparator | **Not executed** | future separately authorized milestone |
| Reader semantic/hybrid/vector retrieval | Not implemented | separate future evidence/authorization |
| Reader SQLite FTS | Not implemented | scaling option only after measured scale need |
| Dedicated/full Reader | Not implemented | `dedicated_reader_core=false` |

## Reader implementation chain

```text
SourceVersion + SourceLocator
→ RC-1 ReaderSession
→ RC-2 DocumentStructuralMap
→ RC-3 explicit reading passes
→ RC-4 EXTRACTED_PROPOSITION candidates
   ├─ RC-5 relation candidates (`core/reader_relations.py`)
   ├─ RC-6 bounded working sets
   ├─ RC-7 explicit cross-document links
   └─ Reader RC-9 lexical candidate discovery → inspection only
→ RC-10 frozen comparison preregistration
→ post-RC-10 reassessment
→ Evaluation Surface v2 → fully judged evidence only
→ future separately authorized comparator, if any
→ separate downstream review/evidence/admission
→ Guardian → TruthGate → strict Canon projection
```

## RC-9 historical baseline

Historical K=5 RC-8 benchmark: Recall@5 `0.937500`, Precision@5 `0.187500`, MRR `0.895833`,
paired hard-negative rate@5 `1.000000`. Classification:
`LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`.

```text
candidate discovery != candidate adjudication
```

## Evaluation Surface v2

The final v2 surface is additive and fully judged:

- 24 queries;
- 12 primary strata × 2;
- 6 candidates per query;
- 48 useful qrels;
- 48 hard-negative qrels;
- 48 neutral-decoy qrels;
- 144 explicit qrels total;
- judgment coverage = 1.0;
- K=5;
- composite surface SHA-256 `7af2b1247e1c1c2590b6b2c830dd605da646989856b6c29cee18aac3e1f785e8`;
- opaque content-derived candidate IDs independent of qrel labels/order.

RC-9 is reproduced unchanged through `core.reader_lexical_discovery.ReaderLexicalIndex`.

Frozen final v2 RC-9 control:

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

The surface is evaluation/research evidence, not a Reader runtime feature.

## Future comparator preregistration

The machine gate is frozen before any model-backed result. The historical RC-10 screen remains
independently required and unchanged.

A future v2 comparator must retain all 42 current useful hits, recover at least 4/6 misses,
reach >=46/48 useful hits / Recall@5 >=0.958333, keep MRR >=0.857639, reduce hard-negative hits
to <=24/48, satisfy per-stratum floors/ceilings, declare exact backend/model/dependency identity,
declare exact index identity when indexed or explicit no-index, record privacy review, use no
`auto`, make zero query-time network calls and transmit no Reader source text externally.

Passing both gates means only:

```text
ELIGIBLE_FOR_ARCHITECTURE_REVIEW_ONLY
comparison pass != runtime authorization
```

## Authority boundaries

```text
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
cross-document link != Canon relation
retrieval match != evidence
similarity != identity
repetition != corroboration
ranking != epistemic authority
candidate discovery != candidate adjudication
comparison pass != runtime authorization
```

No evidence/Canon/ESM mutation, contradiction winner, confidence promotion, Guardian bypass or
TruthGate bypass is introduced.

## Storage and dependency truth

```text
SQLite ordinary active local-first
PostgreSQL/pgvector inactive active=false
Reader FTS absent
Reader ANN/vector DB absent
semantic/hybrid/vector Reader runtime absent
automatic backend switching absent
```

No model download and no new runtime dependency is part of Evaluation Surface v2.

## Historical artifact preservation

Regression tests pin:

- RC-8 corpus Git blob `4be317549d7a8eae9d69f9fa208d07d8855779a4`;
- RC-9 result Git blob `7ffbc86d713b7be89d393fe56c2d160b9dee98dc`;
- RC-10 preregistration Git blob `70758595c220820d456a2ea4db68589289995294`.

## Explicit non-features

No automatic semantic identity/entity resolution, semantic/hybrid/vector Reader runtime,
embeddings model execution, ANN/FAISS/HNSW, Reader FTS, active PostgreSQL/pgvector Reader path,
automatic contradiction adjudication, evidence admission, Canon mutation, public Reader service,
or dedicated/full autonomous Reader exists.

## Localization

Russian Reader-dependent D1/D3/D4/D5 remains tied to its immutable historical Reader checkpoint;
eight other Reader-dependent locale packs remain `REFRESH_NEEDED` — 64 detail documents.
Evaluation Surface v2 performs no broad translation.

## Grant truth

NLnet remains **submitted / under review / not awarded**. Approximate €50,000 remains planning
only; budget change none. Existing pre-agreement work cannot later be represented as newly funded
runtime delivery.

## Backlog isolation

- #155 remains Epistemic Router / Evidence State RFC.
- #165 remains exact normalized admitted-fact migration/dedupe.
- #214 remains fixture/PII/supply-chain hygiene.

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
candidate discovery != candidate adjudication
comparison pass != runtime authorization
```

RC-7 remains `main@b5541ce504af9002c8d3e2dcfa44ef4c0ead86c1`, post-merge CI `31572918731`.
RC-9 remains `main@f8b7d7ea36625b6589a4cf02f12b94c5f98fdb61`,
`core/reader_lexical_discovery.py`, post-merge CI `31594027040`; issue `#377` is completed
RC-10 preregistration bookkeeping.

There is no automatic semantic matching; `embeddings/ANN/vector` Reader runtime remains absent,
semantic/hybrid retrieval may be compared later only with separate authorization,
PostgreSQL/pgvector remains `active=false`, and NLnet remains submitted / under review / not awarded.

After issue #384 completion, STOP before model-backed comparator execution.
