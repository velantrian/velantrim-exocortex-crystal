# Velantrim Crystal — Current Status

**Status date:** 2026-08-14  
**Current signed architecture checkpoint:** `76a9493b8ba64b832472ef9bfc1f1c23ebe6654e`, `verified=true`, reason `valid`  
**Current architecture milestone:** Reader Retrieval Typed Inspection Contract v1 — Issue #391 / PR #392 — complete  
**RRTIC exact-head CI:** `31754798549` — 9/9 SUCCESS  
**RRTIC post-merge CI:** `31771677028` — 9/9 SUCCESS  
**Historical RC-7 merged baseline:** `main@b5541ce504af9002c8d3e2dcfa44ef4c0ead86c1` — PR #372; retained as immutable cross-document Reader provenance.  
**Historical signed RC-9 implementation baseline:** `main@f8b7d7ea36625b6589a4cf02f12b94c5f98fdb61` — PR #376; post-merge CI `31594027040`; retained RC-10 architecture decision #377  
**Historical post-RC-10 reassessment:** Issue #382 selected an **orchestration-only** evaluation path; it authorized no new retrieval runtime and is retained as provenance, not as the current next action.  
**Retained storage-runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6` / PR #337  
**Repository-head rule:** resolve live GitHub before treating any docs-only merge SHA as the current repository HEAD.

## Current Reader position

RC-1 through RC-7 are bounded implemented Reader/domain layers. RC-8 is a completed architecture/research decision. RC-9 is the implemented deterministic lexical PRE-ADMISSION retrieval baseline. Comparator v1 and NLI neutral-filter v1 are completed frozen evaluations with failed admission gates. RRTIC-v1 is the current frozen architecture contract for typed inspection and does not add a runtime stage.

```text
reader_core_rc1_skeleton               = true
reader_core_rc2_structural_map         = true
reader_core_rc3_multi_pass_mechanics   = true
reader_core_rc4_proposition_extraction = true
reader_core_rc5_relation_candidates    = true
reader_core_rc6_long_context_strategy  = true
reader_core_rc7_cross_document_links   = true
reader_rc9_lexical_candidate_discovery = true
dedicated_reader_core                  = false
semantic_hybrid_reader_runtime         = false
rrtic_runtime_authorization            = false
```

RC-5 remains implemented in `core/reader_relations.py`. RC-9 remains implemented in `core/reader_lexical_discovery.py`.

## Reader evidence chain

```text
RC-9 lexical discovery
        ↓
Evaluation Surface v2
        ↓
Comparator v1
  recall recovered
  hard-negative discrimination FAIL
        ↓
NLI neutral-filter v1
  discrimination improved
  useful-recall safety FAIL
        ↓
post-NLI reassessment
  RELATION-CONTRACT MISMATCH
        ↓
RRTIC-v1
  typed inspection contract only
  runtime_authorization=false
```

## RC-9 deterministic lexical baseline — retained control

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

## Reader Retrieval Evaluation Surface v2 — retained frozen evidence

The fully judged v2 surface remains frozen at SHA-256 `753cc550bc5fc47697aa6d7b1cda294bf11abaa08d515816e5e1db59eb526cdd` with 24 queries, 12 primary strata, 6 candidates/query and 144/144 explicit qrels.

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

Classification: `LEXICAL_CONTROL_EXPOSES_MULTI_STRATUM_GAPS`.

## Comparator v1 — completed evaluation / frozen gate fail

Pinned multilingual semantic similarity recovered all useful v2 candidates (`48/48`, Recall@5 `1.0`, MRR `1.0`) but surfaced `41/48` hard negatives.

Classification: `SEMANTIC_RECALL_RECOVERED_DISCRIMINATION_GATE_FAILED`.

Historical RC-10 screen also failed because all `4/4` hard negatives surfaced. This comparator is research evidence only; it is not a Reader backend.

## NLI neutral-filter v1 — completed evaluation / frozen gate fail

The preregistered bidirectional neutral-neutral filter reduced v2 hard negatives from `41/48` to `18/48`, but useful candidates regressed to `46/48`; historical useful hits regressed from `16/16` to `15/16`. The no-recall-loss overlay and frozen gate therefore failed.

Classification: `NLI_NEUTRAL_FILTER_GATE_FAILED`.

```text
NLI label         != proposition identity
NLI contradiction != contradiction adjudication
filtering          != epistemic authority
```

## RRTIC-v1 — current frozen architecture contract

RRTIC-v1 freezes a retrieval-side diagnostic envelope after the post-NLI reassessment classified the missing capability as a relation-contract mismatch.

Six suspicion-only relation families:

```text
EQUIVALENCE_SUSPECT
RELATED_SUSPECT
CONTRADICTION_SUSPECT
QUALIFICATION_SUSPECT
TOPIC_ONLY_SUSPECT
UNKNOWN
```

Ten qualifier dimensions:

```text
entity_binding
predicate_binding
argument_roles
polarity
modality_quantifier
temporal_version
jurisdiction
condition_direction
units_thresholds
attribution_causality
```

Each qualifier is `MATCH | MISMATCH | UNKNOWN | NOT_APPLICABLE`.

RRTIC-v1 has no accept/reject policy, scalar truth/confidence score, reranking, model execution, runtime provider, identity decision, evidence admission, contradiction adjudication or Canon mutation. Existing RC-5 semantics are unchanged.

```text
RRTIC suspicion    != adjudicated relation
RRTIC diagnostic   != RC-5 registered relation
qualifier mismatch != truth decision
comparison pass    != runtime authorization
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
same-topic != same proposition
possible-same-claim != claim identity
similarity signal != identity proof
repetition across sources != corroboration
retrieval match != evidence
similarity != identity
ranking != epistemic authority
candidate discovery != candidate adjudication
comparison pass != runtime authorization
evaluation pass != runtime authorization
```

Guardian, TruthGate, TrustSnapshot and CanonicalView remain unchanged. Public `HTTP /ask`, `CLI ask` and `MCP search` remain admitted-memory read-only query surfaces, not Reader evaluation/inspection authority interfaces.

## Storage truth

```text
SQLite ordinary active local-first
→ backup / verify / inactive restore
→ bounded logical export
→ PostgreSQL 16 + pgvector inactive import/equivalence
→ active=false
```

Reader SQLite FTS is not implemented. No Reader ANN/vector DB is introduced. Automatic backend switching remains absent.

## Current validation baseline

The RRTIC architecture checkpoint push CI `31771677028` completed **9/9 SUCCESS**. Python 3.11 collected 2244 tests and completed **2231 passed / 13 skipped / 0 failed** at **100% measured line coverage**. Later docs-only reconciliation has its own exact-head/post-merge CI and does not redefine the RRTIC architecture checkpoint.

## Backlog boundaries

- #165: exact normalized admitted-fact dedupe/migration only; no semantic matching.
- #155: downstream Epistemic Router / Evidence State RFC.
- #214: fixture/PII/supply-chain hygiene.

These remain separate open scopes and were not started by RRTIC-v1 or this documentation reconciliation.

## Localization truth

Russian Reader-dependent D1/D3/D4/D5 surfaces retain their immutable historical checkpoint. Eight other Reader-dependent locale packs remain `REFRESH_NEEDED`, with 64 tracked detail documents. Post-RC-9 Comparator/NLI/RRTIC English truth is not automatically propagated into localized files.

## Grant status

NLnet remains **submitted / under review / not awarded**. Approximate **€50,000** is planning context only. Budget change: none. RC-1 through RC-9, Comparator v1, NLI v1 and RRTIC-v1 are existing pre-agreement repository/research history if completed before an agreement.

## Stop boundary

RRTIC-v1 is closed. No discriminator/model/runtime implementation is authorized by this contract. Do not automatically add semantic/hybrid/vector Reader runtime, FTS/ANN, activate PostgreSQL/pgvector, mutate epistemic authority, implement #155/#165/#214 or perform broad localization.
