# Implementation Status: Crystal vs Full Exo-Cortex

This page exists so a reviewer never has to guess which statements describe
**implemented, tested repository behaviour** and which describe **RFC-level
architecture or long-term vision**. Statuses below are derived from the code
and test suite actually present in this repository (audited baseline in
[TEST_REPORT.md](../TEST_REPORT.md)) — not from roadmap ambition.

## The three documentation surfaces

Velantrim has three distinct surfaces, and reviewer-facing Crystal documents
must not mix them without explicit status labels:

1. **Crystal Core** — the grant/reviewer-facing open-source core in this
   repository: local-first memory, typed claims, TruthGate, trace/receipts,
   auditability and GDPR-oriented controls.
2. **Full Velantrim Exo-Cortex** — the broader architecture vision: Mode
   Layer, Observer action policies, procedural memory, temporal reasoning and
   future cognitive extensions. RFC/roadmap material unless explicitly present
   in code and tests.
3. **Velantrim Culture** — symbols, myths, language, rituals and creative
   artifacts. Intentionally **outside** the Crystal grant core.

## Status table

Statuses: **Implemented** (code + tests in this repo), **Partial** (baseline
exists; hardening or formal docs pending), **RFC / roadmap** (design idea, no
runtime feature), **Vision** (research direction), **Out of scope** (not part
of Crystal).

| Component | Status | In Crystal current core? | Notes |
|---|---|---|---|
| Local-first storage | Implemented | Yes | SQLite/WAL L1; dependency-free SQLite default for L3 canon, evidence, receipts, audit and operational state |
| TruthGate | Implemented | Yes | `core/truth_gate.py` (extracted, behaviour-pinned); type-aware; the only automatic entry into L3 |
| Trace / Receipt | Implemented | Yes | `core/trace.py`, `core/provenance.py`; sealed, replayable receipts with strict-provenance replay |
| Guardian | Partial | Baseline | Boundary function in `core/pipeline.py` runs before the gate; a formal detect → flag/block/pass contract document is future work |
| FactsPack | Partial | Baseline | Grounding pack used by the answer path; explicit conflict/contestation policy is a future RFC |
| Review queue + web UI | Implemented | Yes | `core/review.py`, token-guarded HTTP API, static Kanban UI; roles/multi-curator workflows are grant-scope hardening |
| GDPR-oriented controls | Partial | Baseline | Erasure, restriction, record-of-processing, tamper-evident audit, PII redaction, opt-in field encryption; "GDPR-oriented", **not** a certification claim |
| Eval gate | Implemented | Yes | English corpus CI-gated; Russian corpus report-only; expansion planned |
| Memory observability | Implemented | Yes | `core/observe.py` — read-only `memory_report` over L3 (states, statuses, contradictions) |
| Fractal Memory (multi-scale anchoring) | Implemented (baseline) | Yes | `core/fractal.py` (RFC0070): SHORT→MEDIUM→LONG→CORE anchoring, CORE exempt from decay; `fractal-*` CLI |
| Observer **action policy** (flag → action routing) | RFC / roadmap | No | Observability exists (read-only); a policy that routes flags to receivers/actions does not |
| Mode Layer | RFC / roadmap | No runtime feature | Policy-boundary concept only; nothing in code or tests |
| Imagination Mode | RFC / roadmap | No runtime feature | Creative-sandbox concept only; see boundary note below |
| Mode Router | RFC / roadmap | No runtime feature | Future explicit/rule-based design |
| Temporal reasoning / bi-temporal claims | RFC / roadmap | No | Future RFC; no schema fields today |
| Provenance grades (BRONZE/SILVER/GOLD) | RFC / roadmap | No | Future RFC; no schema fields today |
| Essence Engine | Vision | No | Meaning-oriented future layer |
| Umwelt / Lens Layer | Vision | No | Multi-view knowledge-graph concept |
| Velantrim Culture | Out of scope | No | Separate culture/vision layer, intentionally outside the grant core |

If a component is not in this table, assume it is **not** an implemented
Crystal feature unless `core/` and `tests/` demonstrably contain it.

## Reviewer Package

For external reviewers and grant/university evaluation:

- [Reviewer Overview](REVIEWER_OVERVIEW.md)
- [Architecture Decision Records](ADR.md)
- [Failure Modes and Mitigations](FAILURE_MODES.md)
- [Evaluation Metrics](EVALUATION_METRICS.md)

Research inspirations are tracked separately as non-normative context and must
not be treated as implementation status (ADR-006).

## Imagination Mode boundary (RFC-level, stated early on purpose)

Mode Layer and Imagination Mode are documented here as **RFC-level architecture
boundaries**, not Crystal runtime features. When they are designed, one rule is
fixed in advance: Imagination output (creative drafts, cultural artifacts,
myths, language variants, design fiction) stays **sandboxed** — it cannot
become `VERIFIED`, `WORLD_FACT` or L3 canon without explicit human review and a
Guardian/TruthGate-compatible promotion. This is the same Ring Zero invariant
that already governs `LLM_OUTPUT` today (see
[ARCHITECTURE.md](./ARCHITECTURE.md), "Ring Zero").

## Graph backends (role summary)

| Component | Role |
|---|---|
| SQLite | dependency-free default: local canon, metadata, evidence, receipts, audit |
| LadybugDB | active embedded graph backend candidate (Kuzu lineage) |
| KuzuDB | legacy/archived predecessor (upstream archived Oct. 2025) — compatibility reference, **not** the primary future dependency |
| Neo4j | optional inspector/demo/audit tooling — never required runtime |

## Future RFC backlog (documentation backlog only — nothing here is implemented)

| RFC | Purpose | Status |
|---|---|---|
| GUARDIAN_CONTRACT | Formal detect → flag/block/pass behaviour of Guardian | Future |
| TRUTHGATE_BEHAVIOR | Hard blocks, thresholds, conflict handling in one document | Future |
| FACTSPACK_POLICY | Evidence requirements + explicit contradiction/contested-answer policy | Future |
| WRITE_POLICY | Allowed write targets per mode | Future |
| OBSERVER_ACTION_POLICY | Observer flag → receiver/action routing | Future |
| STATE_MACHINE | Complete ESM ↔ truth_status transition map | Future |
| MEMORY_MAPPING | L0–L7 ↔ fractal anchoring ↔ storage mapping | Future |
| RFC_MODE_LAYER | Modes, fallback, explicit triggers | Future |
| RFC_PROVENANCE_GRADES | BRONZE/SILVER/GOLD evidence tiers | Future |
| RFC_TEMPORAL_LAYER | Bi-temporal claim fields and temporal reasoning | Future |
| [RFC_HARNESS_REPLAY_OPTIMIZATION](./RFC_HARNESS_REPLAY_OPTIMIZATION.md) | Trajectory record/replay + human-approved harness optimization | Proposed (drafted, RFC-only) |
| [EPISTEMIC_INFRASTRUCTURE_UPGRADE](./EPISTEMIC_INFRASTRUCTURE_UPGRADE.md) | Temporal Layer, Context/Scope, Conflict Resolution, Negative Knowledge, Known Unknowns, Plausibility Pre-Filter, Confidence Calibration, Epistemic Debt | Future RFC / v0.3.0+ research roadmap / no runtime feature / no schema fields today |
