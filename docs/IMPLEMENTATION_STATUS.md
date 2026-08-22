# Implementation Status: Crystal vs Future Exo-Cortex Work

**Status date:** 2026-08-22  
**V1 lifecycle:** **COMPLETE / 100% / FREEZE-STABILITY**  
**P0/P1 remaining:** `0 / 0`  
**Automatic next implementation milestone:** `NONE`  
**Authoritative closure:** [`docs/status/CRYSTAL_V1_CLOSURE_2026-08-22.md`](./status/CRYSTAL_V1_CLOSURE_2026-08-22.md)

This file describes implementation truth. Historical Reader/evaluation checkpoints remain retained evidence, but they no longer represent an unfinished V1 milestone.

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
| RC-9 lexical candidate discovery | **IMPLEMENTED** | `core/reader_lexical_discovery.py` |
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
dedicated_reader_core                  = false
```

## Research/evaluation evidence is not implementation

The following completed milestones remain immutable evidence but do not authorize runtime expansion:

| Evidence / contract | Result | Runtime meaning |
|---|---|---|
| RC-8 retrieval decision | architecture/research complete | deterministic lexical baseline selected first |
| Reader Retrieval Evaluation Surface v2 | frozen judged surface | no runtime added |
| Comparator v1 | `SEMANTIC_RECALL_RECOVERED_DISCRIMINATION_GATE_FAILED` | semantic comparator rejected as runtime authorization |
| NLI neutral-filter v1 | `NLI_NEUTRAL_FILTER_GATE_FAILED` | filter rejected as Reader retrieval stage |
| RRTIC-v1 | frozen typed inspection contract | no model/filter/reranker/provider added |

Historical RC-9 and evaluation metrics remain available in repository history and their owning evidence records. V1 closure does not reinterpret those results.

## Authority firewall

```text
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
summary != evidence
cross-document link != Canon relation
same-topic != same proposition
similarity signal != identity proof
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

The final governance probe PR #446 exercised the permanent matrix successfully before being closed without merge. Issue #432 is closed. These are V1 closure evidence, not generic production authorization.

## Localization / grant

Localization parity and historical provenance are owned by [`docs/TRANSLATION_STATUS.md`](./TRANSLATION_STATUS.md). The 2026-08-22 V1 lifecycle closure is an overlay across supported locales and does not rewrite older architecture checkpoints.

NLnet remains **submitted / under review / not awarded**. Approximate €50,000 remains planning context only.

## Future work boundary

No P0/P1 implementation work remains in the V1 completion program. P2/P3, research, deferred and frozen items are non-blocking backlog only.

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
P0 = 0
P1 = 0
PHASE = FREEZE / STABILITY
AUTOMATIC NEXT MILESTONE = NONE
```
