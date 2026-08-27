# Velantrim Crystal — Current Status

**Status date:** 2026-08-27  
**Lifecycle:** **V1 COMPLETE / 100% / FREEZE-STABILITY**  
**V1 P0:** `0`  
**V1 P1:** `0`  
**Post-V1 governance:** Issue `#432` is **OPEN / P1**; it does **not** reopen Crystal V1.  
**Automatic next milestone:** `NONE`  
**Authoritative closure record:** [`docs/status/CRYSTAL_V1_CLOSURE_2026-08-22.md`](./status/CRYSTAL_V1_CLOSURE_2026-08-22.md)  
**Repository-head rule:** resolve live GitHub before treating any documentation checkpoint, issue state, PR state, CI state, or governance snapshot as current.

## Current product position

Crystal V1 is complete. The bounded V1 completion program is closed; remaining P2/P3, research, deferred and frozen records are non-blocking backlog and do not create an automatic V1.x, V2 or research implementation phase.

Crystal remains a local-first evidence/memory kernel and bounded decision boundary. Its trusted responsibilities are evidence admission, provenance/lineage, bounded canonical writes, fixed TruthGate semantics, Guardian constraints, traces, receipts, local persistence and auditable replay.

The current repository also contains post-V1 bounded Reader bridges and the public-query evidence-standing hardening merged through PR #464. Those changes do not reopen V1 and do not create production/runtime authorization.

```text
CRYSTAL V1 = COMPLETE
PROJECT COMPLETION = 100%
REMAINING = 0%
PHASE = FREEZE / STABILITY
V1 P0 = 0
V1 P1 = 0
POST-V1 GOVERNANCE #432 = OPEN / P1
AUTOMATIC NEXT MILESTONE = NONE
```

## Implemented Reader position

RC-1 through RC-7 remain bounded implemented Reader/domain layers. RC-5 remains implemented in `core/reader_relations.py`. RC-9 remains the deterministic lexical PRE-ADMISSION retrieval baseline implemented in `core/reader_lexical_discovery.py`. Comparator v1 and NLI neutral-filter v1 remain completed frozen evaluations whose admission gates failed. **Reader Retrieval Typed Inspection Contract v1 (RRTIC-v1)** remains a frozen typed-inspection architecture contract and adds no runtime authority.

Post-V1 bounded Reader surfaces now in `main` include Reader Product Bridge v0.1, local UTF-8 file source v0.1 and local PDF source v0.1. They remain read-side/pre-admission and do not authorize evidence admission, Canon writes, semantic/model execution or production runtime.

```text
reader_core_rc1_skeleton               = true
reader_core_rc2_structural_map         = true
reader_core_rc3_multi_pass_mechanics   = true
reader_core_rc4_proposition_extraction = true
reader_core_rc5_relation_candidates    = true
reader_core_rc6_long_context_strategy  = true
reader_core_rc7_cross_document_links   = true
reader_rc9_lexical_candidate_discovery = true
bounded_reader_product_bridge_v0_1     = true
reader_file_source_v0_1                = true
reader_pdf_source_v0_1                 = true
dedicated_reader_core                  = false
semantic_hybrid_reader_runtime         = false
rrtic_runtime_authorization            = false
```

Historical Reader checkpoints and evaluation measurements remain immutable provenance; they are not the current lifecycle milestone.

## Public evidence-standing hardening

PR #464 / Issue #463 closed a real public-read standing gap. A `VERIFIED` fact may ground the public read-only answer path only while it retains qualifying replayable evidence, and evidence must bind to the exact TrustSnapshot-resolved claim used for current public grounding. Divergent L1/L3 claim content under the same `fact_id` cannot inherit stale evidence authority.

```text
same fact_id != same claim
evidence(C1) != evidence(C2)
historical VERIFIED != current evidence-backed standing
support loss != falsity
receipt authenticity != current standing
```

This hardening does not rewrite historical ESM/receipt state, expand Canon authority, change TruthGate/Guardian/WriteGate ownership, or authorize production.

## Authority boundaries

```text
research != runtime
spec != implementation
retrieval != evidence
receipt != truth
claim != belief
evidence != identity
identity != authority
model output != Canon
CI green != production
similarity != identity
ranking != epistemic authority
```

Guardian, TrustSnapshot and CanonicalView retain their existing authority roles. TruthGate's default WORLD_FACT confidence policy remains fixed and versioned:

```text
DEFAULT_MIN_CONFIDENCE = 0.05
TRUTH_GATE_POLICY_VERSION = "truth-gate-v1-fixed-0.05"
```

Process-local adaptation remains telemetry/research and cannot silently change default admission authority.

## Storage truth

```text
SQLite ordinary active local-first
→ backup / verify / inactive restore
→ bounded logical export
→ PostgreSQL 16 + pgvector inactive import/equivalence
→ active=false
```

PostgreSQL/pgvector activation, Reader FTS/ANN/vector runtime, distributed sync and queue federation are not authorized by V1 closure.

## Validation and governance

The permanent PR matrix remains nine checks:

1. `code-quality`
2. `Ring Zero mutation gate`
3. `docs-status`
4. `test (3.11)`
5. `test (3.12)`
6. `jsonl-integrity`
7. `eval-gate`
8. `security`
9. `docker-build`

The final V1 governance probe PR #446 exercised the permanent matrix successfully and was closed without merge. That evidence supports the bounded V1 closure, but it does **not** prove that GitHub server-side governance enforces the matrix.

Issue #432 is currently **OPEN / P1** as a post-V1 governance enforcement/read-back issue. The current ruleset snapshot must be resolved live before use; at the 2026-08-27 audit checkpoint, required review-thread resolution was still false and no required-status-check rule was present. This does not reopen V1 and does not change runtime or epistemic authority.

## Localization truth

Localization freshness is owned by [`docs/TRANSLATION_STATUS.md`](./TRANSLATION_STATUS.md). All nine supported locale packs retain their previously verified stable architecture translations. The V1 closure is represented as a lifecycle overlay rather than by rewriting historical architecture provenance.

`CURRENT` localization markers never override current English implementation truth or live GitHub.

## Backlog boundary

There is no open P0/P1 work in the **V1 completion program**. Post-V1 governance Issue #432 remains separately open. Existing P2/P3, research, future and frozen records remain optional backlog/evidence only.

The following are explicitly **not** implied next steps:

- V1.x or V2;
- semantic/hybrid/vector Reader runtime;
- GraphRAG or advanced RAG runtime;
- PostgreSQL/pgvector activation;
- EPIS/EITI runtime integration;
- distributed synchronization;
- central authority routing;
- automatic promotion of Titan research into Crystal.

Any such phase requires a separate explicit owner decision and fresh validation scope.

## Grant status

NLnet remains **submitted / under review / not awarded**. Approximate **€50,000** remains planning context only; no award or budget change is implied by V1 completion.

---

## Immutable Reader evidence chain — retained historical provenance

This section preserves the previously verified Reader checkpoints, measurements and authority-firewall language as immutable evidence. It is **not** the current lifecycle milestone and does not supersede the V1 closure above.

**Signed Reader Retrieval Typed Inspection Contract v1 architecture checkpoint:** `76a9493b8ba64b832472ef9bfc1f1c23ebe6654e`, `verified=true`, reason `valid`  
**RRTIC exact-head CI:** `31754798549` — 9/9 SUCCESS  
**RRTIC post-merge CI:** `31771677028` — 9/9 SUCCESS  
**Historical RC-7 merged baseline:** `main@b5541ce504af9002c8d3e2dcfa44ef4c0ead86c1` — PR #372; post-merge CI `31572918731`.  
**Historical signed RC-9 implementation baseline:** `main@f8b7d7ea36625b6589a4cf02f12b94c5f98fdb61` — PR #376; post-merge CI `31594027040`; retained RC-10 architecture decision #377.  
**Historical post-RC-10 reassessment:** Issue #382 selected an **orchestration-only** Evaluation Surface v2 path; it authorized no new retrieval runtime.  
**Retained storage-runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6` / PR #337.

### Reader evidence chain

```text
RC-9 lexical discovery
        ↓
Reader Retrieval Evaluation Surface v2
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

### RC-9 deterministic lexical baseline — retained control

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

### Reader Retrieval Evaluation Surface v2 — retained frozen evidence

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

### Comparator v1 — completed evaluation / frozen gate fail

Pinned multilingual semantic similarity recovered all useful v2 candidates (`48/48`, Recall@5 `1.0`, MRR `1.0`) but surfaced `41/48` hard negatives.

Classification: `SEMANTIC_RECALL_RECOVERED_DISCRIMINATION_GATE_FAILED`.

Historical RC-10 screen also failed because all `4/4` hard negatives surfaced. This comparator is research evidence only; it is not a Reader backend.

### NLI neutral-filter v1 — completed evaluation / frozen gate fail

The preregistered bidirectional neutral-neutral filter reduced v2 hard negatives from `41/48` to `18/48`, but useful candidates regressed to `46/48`; historical useful hits regressed from `16/16` to `15/16`. The no-recall-loss overlay and frozen gate therefore failed.

Classification: `NLI_NEUTRAL_FILTER_GATE_FAILED`.

```text
NLI label         != proposition identity
NLI contradiction != contradiction adjudication
filtering          != epistemic authority
```

### RRTIC-v1 — retained frozen architecture contract

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

### Reader authority firewall — retained contract

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

Guardian, TrustSnapshot and CanonicalView retain their existing authority roles. Public `HTTP /ask`, `CLI ask` and `MCP search` remain admitted-memory read-only query surfaces, not Reader evaluation/inspection authority interfaces.

### Retained validation provenance

The RRTIC architecture checkpoint push CI `31771677028` completed **9/9 SUCCESS**. Python 3.11 collected 2244 tests and completed **2231 passed / 13 skipped / 0 failed** at **100% measured line coverage**. Later bounded fixes/docs reconciliations have their own exact-head/post-merge CI and do not redefine the RRTIC architecture checkpoint.

## Stop boundary

```text
💠 VELANTRIM EXO-CORTEX CRYSTAL
PROJECT V1 — DONE
DONE 100%
REMAINING 0%
██████████ 100%
V1 P0 0
V1 P1 0
POST-V1 GOVERNANCE #432 OPEN / P1
V1.x / V2 / RESEARCH = BACKLOG ONLY
CURRENT PROJECT PHASE = FREEZE / STABILITY
AUTOMATIC NEXT MILESTONE = NONE
STOP
```
