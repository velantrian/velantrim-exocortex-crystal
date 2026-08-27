# Implementation Status: Crystal vs Future Exo-Cortex Work

**Status date:** 2026-08-27  
**V1 lifecycle:** **COMPLETE / 100% / FREEZE-STABILITY**  
**V1 P0/P1 remaining:** `0 / 0`  
**Post-V1 governance:** Issue `#432` is **OPEN / P1**; this does **not** reopen V1.  
**Automatic next implementation milestone:** `NONE`  
**Authoritative closure:** [`docs/status/CRYSTAL_V1_CLOSURE_2026-08-22.md`](./status/CRYSTAL_V1_CLOSURE_2026-08-22.md)

This file describes implementation truth. Historical Reader/evaluation checkpoints remain retained evidence, but they no longer represent an unfinished V1 milestone. Resolve live GitHub before treating issue, PR, CI, governance or repository-head state as current.

## Implemented V1 capability truth

Crystal V1 is a local-first evidence/memory kernel and bounded decision boundary. Implemented V1 responsibilities include evidence admission, provenance/lineage, bounded canonical writes, Guardian and fixed TruthGate boundaries, traces, sealed receipts/replay, local persistence/recovery and the bounded Reader components listed below.

| Capability | Status | Primary implementation |
|---|---|---|
| RC-1 source/session skeleton | **IMPLEMENTED** | `core/reader_core.py` |
| RC-2 structural map | **IMPLEMENTED** | `core/reader_structure.py` |
| RC-3 multi-pass mechanics | **IMPLEMENTED** | `core/reader_passes.py` |
| RC-4 proposition extraction contract/runtime | **IMPLEMENTED** | `core/reader_extraction.py` |
| RC-5 relation candidates | **IMPLEMENTED** | `core/reader_relations.py` |
| RC-6 bounded long-context strategy | **IMPLEMENTED** | `core/reader_long_context.py` |
| RC-7 explicit cross-document candidate links | **IMPLEMENTED** | `core/reader_cross_document.py` |
| Reader RC-9 lexical candidate discovery | **IMPLEMENTED** | `core/reader_lexical_discovery.py` |
| Reader Product Bridge v0.1 | **IMPLEMENTED / POST-V1 / NOT PRODUCTION-AUTHORIZED** | `core/reader_product_bridge.py` |
| Local file Reader source v0.1 | **IMPLEMENTED / POST-V1 / PRE-ADMISSION** | `core/reader_file_source.py` |
| Local PDF Reader source v0.1 | **IMPLEMENTED / POST-V1 / PRE-ADMISSION** | `core/reader_pdf_source.py` |
| Public current-evidence standing / exact resolved-claim binding | **IMPLEMENTED** | `core/query_pipeline.py`, `core/evidence.py` |
| Dedicated/full autonomous Reader | **NOT IMPLEMENTED** | `dedicated_reader_core=false` |
| Semantic/hybrid Reader runtime | **NOT AUTHORIZED / NOT IMPLEMENTED** | — |
| Reader FTS / ANN / vector DB | **NOT AUTHORIZED / NOT IMPLEMENTED** | — |
| NLI runtime filter / CrossEncoder reranker | **NOT AUTHORIZED / NOT IMPLEMENTED** | — |
| RRTIC runtime provider | **NOT AUTHORIZED / NOT IMPLEMENTED** | — |
| PostgreSQL/pgvector active runtime | **NOT AUTHORIZED / INACTIVE** | `active=false` |

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
```

## Current public evidence-standing boundary

PR #464 / Issue #463 hardened the public read-only answer path. A resolved `VERIFIED` fact may ground a factual public answer only while qualifying replayable evidence remains, and the evidence must bind to the exact TrustSnapshot-resolved claim being used for grounding.

```text
same fact_id != same claim
evidence(C1) != evidence(C2)
historical VERIFIED != current evidence-backed standing
support loss != falsity
receipt authenticity != current standing
```

This is a read-authority hardening only: no historical ESM or receipt rewrite, no Canon authority expansion, no TruthGate/Guardian/WriteGate weakening, and no production authorization.

## Immutable Reader provenance retained under V1 closure

The lifecycle overlay does not replace the historical Reader evidence chain:

- RC-7 merged baseline: `main@b5541ce504af9002c8d3e2dcfa44ef4c0ead86c1` / PR #372 / post-merge CI `31572918731`;
- RC-9 implementation baseline: `main@f8b7d7ea36625b6589a4cf02f12b94c5f98fdb61` / PR #376 / post-merge CI `31594027040`;
- retained RC-10 architecture decision: #377;
- post-RC-10 reassessment: #382, which selected **Evaluation Surface v2** as an orchestration/evaluation-only path before later comparator work;
- signed RRTIC architecture checkpoint: `76a9493b8ba64b832472ef9bfc1f1c23ebe6654e` / PR #392 / post-merge CI `31771677028`.

These identifiers are immutable provenance. They do not make any historical milestone current again and do not authorize a new runtime.

## Research/evaluation evidence is not implementation

The following completed milestones remain immutable evidence but do not authorize runtime expansion:

| Evidence / contract | Result | Runtime meaning |
|---|---|---|
| RC-8 retrieval decision | architecture/research complete | deterministic lexical baseline selected first |
| Reader Retrieval Evaluation Surface v2 | frozen judged surface | no runtime added |
| Comparator v1 | `SEMANTIC_RECALL_RECOVERED_DISCRIMINATION_GATE_FAILED` | semantic comparator rejected as runtime authorization |
| NLI neutral-filter v1 | `NLI_NEUTRAL_FILTER_GATE_FAILED` | filter rejected as Reader retrieval stage |
| RRTIC-v1 | frozen typed inspection contract | no model/filter/reranker/provider added |

## RC-9 retained implementation evidence

Historical RC-9 K=5 evidence remains immutable provenance:

- Recall@5 `0.937500`;
- Precision@5 `0.187500`;
- MRR `0.895833`;
- paired hard-negative rate@5 `1.000000`;
- useful hits `15/16`;
- hard-negative hits `4/4`;
- classification `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`.

These are retrieval measurements, not semantic/adjudication accuracy. V1 closure does not reinterpret those results.

## Reader Retrieval Evaluation Surface v2 — retained frozen surface

Final frozen v2 surface: 24 queries, 12 primary strata ×2, 6 candidates/query, 144/144 explicit qrels, judgment coverage `1.0`, K=5, composite SHA-256 `753cc550bc5fc47697aa6d7b1cda294bf11abaa08d515816e5e1db59eb526cdd`.

Final unchanged RC-9 v2 control:

- useful hits **42 / 48**;
- Recall@5 **0.875000**;
- fixed-slot Precision@5 **0.350000**;
- judged precision-over-returned **0.355932**;
- MRR **0.857639**;
- hard-negative hits **38 / 48**;
- hard-negative rate@5 **0.791667**.

Classification: `LEXICAL_CONTROL_EXPOSES_MULTI_STRATUM_GAPS`.

## Authority firewall

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
NLI label != proposition identity
RRTIC suspicion != adjudicated relation
qualifier mismatch != truth decision
ranking != epistemic authority
candidate discovery != candidate adjudication
comparison pass != runtime authorization
evaluation pass != runtime authorization
research != runtime
spec != implementation
receipt != truth
model output != Canon
CI green != production
```

TruthGate default remains deterministic and versioned:

```text
DEFAULT_MIN_CONFIDENCE = 0.05
TRUTH_GATE_POLICY_VERSION = "truth-gate-v1-fixed-0.05"
```

Process-local adaptation may remain telemetry/research but does not change default admission authority.

## Persistence and recovery

SQLite remains the ordinary active local-first storage profile. V1 includes restart continuity, backup/verify/inactive restore, bounded logical export and explicit outbox recovery for post-gate merge failure.

```text
SQLite ordinary active local-first
→ backup / verify / inactive restore
→ bounded logical export
→ PostgreSQL 16 + pgvector inactive import/equivalence
→ active=false
```

PostgreSQL/pgvector activation, queue federation, distributed exactly-once behavior and distributed sync are outside V1 authority.

## Validation / governance

The permanent V1 PR matrix consists of nine checks: `code-quality`, `Ring Zero mutation gate`, `docs-status`, `test (3.11)`, `test (3.12)`, `jsonl-integrity`, `eval-gate`, `security`, and `docker-build`.

PR #446 exercised the matrix successfully before being closed without merge. That is V1 closure evidence, not proof of server-side enforcement.

Issue #432 is **OPEN / P1** as a separate post-V1 governance enforcement/read-back issue. At the 2026-08-27 audit checkpoint, the active ruleset still had `required_review_thread_resolution=false` and no required-status-check rule. This governance P1 does not reopen V1 and changes no runtime/epistemic authority.

## Localization / grant

Localization parity and historical provenance are owned by [`docs/TRANSLATION_STATUS.md`](./TRANSLATION_STATUS.md). The 2026-08-22 V1 lifecycle closure is an overlay across supported locales and does not rewrite older architecture checkpoints.

NLnet remains **submitted / under review / not awarded**. Approximate €50,000 remains planning context only.

## Future work boundary

No P0/P1 implementation work remains in the **V1 completion program**. Post-V1 governance #432 remains separate. P2/P3, research, deferred and frozen items are non-blocking backlog only.

V1 completion does **not** authorize:

- V1.x or V2;
- semantic/hybrid/vector Reader runtime;
- GraphRAG or advanced RAG runtime;
- PostgreSQL/pgvector activation;
- EPIS/EITI runtime integration;
- distributed sync or queue federation;
- central authority routing;
- automatic transfer of Titan research into Crystal.

Any future implementation phase requires a separate explicit owner decision, bounded scope and fresh validation design.

## Stop boundary

```text
CRYSTAL V1 = COMPLETE
DONE = 100%
REMAINING = 0%
V1 P0 = 0
V1 P1 = 0
POST-V1 GOVERNANCE #432 = OPEN / P1
PHASE = FREEZE / STABILITY
AUTOMATIC NEXT MILESTONE = NONE
```
