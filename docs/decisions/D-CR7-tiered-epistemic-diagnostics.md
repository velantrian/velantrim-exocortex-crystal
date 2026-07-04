# Decision Draft — CR-7 Tiered Epistemic Diagnostics 🧠🧾

**Status:** PROPOSED / AWAITING OPERATOR GO  
**Implementation status:** NOT IMPLEMENTED  
**Scope:** External Labs / Mentaury research documentation  
**Crystal runtime impact:** none  

This decision draft records why CR-7 v3 prefers derived diagnostics over
materialized diagnostic graph nodes.

---

## Context

The research discussion around Mentaury considered several mechanisms:

- failure memory;
- explicit unknown / knowledge-gap tracking;
- stale contradiction escalation;
- memory health metrics;
- epistemic feedback loops.

An early design represented these as separate diagnostic graph nodes, such as
`FAILURE_MOTIF`, `UNKNOWN_REGION`, and `STALE_CONTRADICTION`.

That design is understandable, but it creates a second memory of facts derived
from existing state. This increases synchronization risk.

---

## Decision candidate

Prefer CR-7 v3:

```text
Tiered Epistemic Diagnostics
Subtitle: Self-Audit Projections over Mutation Log
```

Core rule:

```text
External truth = Crystal Canon.
System-truth = mutation_log.
Diagnostics = derived projections, cached aggregates, and alert states.
```

---

## Accepted as preferred research direction

| Component | Decision |
|---|---|
| `mutation_log` as system-truth | Preferred |
| `contradiction.alert_state` | Preferred for stale contradiction tracking |
| `failure_pattern_stats` | Preferred as disposable aggregate, not graph node |
| `knowledge_gap_view` | Preferred as query-based view |
| `stale_contradiction_view` | Preferred as query-based view |
| `compute_epistemic_signal(event)` | Preferred as soft advisory signal only |
| `refresh_epistemic_projections()` | Preferred Slow Loop hook |

---

## Rejected or deferred alternatives

| Alternative | Decision | Reason |
|---|---|---|
| `DIAGNOSTIC` graph nodes | Rejected for P0/P1 | Creates second memory and synchronization risk. |
| `FAILURE_MOTIF` graph nodes | Rejected for P0/P1 | Better represented as aggregate over mutation history. |
| `UNKNOWN_REGION` graph nodes | Deferred | Knowledge gaps are view-first; may become tracked research objects later if workflow requires it. |
| `STALE_CONTRADICTION` graph nodes | Rejected | Staleness is a property of existing contradiction records. |
| Automatic confidence penalty | Rejected | Diagnostics must not mutate truth-state or create hidden bias. |
| Automatic rejection from diagnostics | Rejected | Unknown, stale, or risky does not mean false. |
| Self-modification | Rejected | Violates the project boundary. |
| Canon write access | Rejected | Mentaury diagnostics remain outside Crystal Canon. |

---

## Rationale

### 1. One source of system-truth

The mutation log already records the internal history needed for diagnostics.
Creating diagnostic memory nodes would duplicate derived facts.

### 2. Better rollback and fork behavior

If diagnostics are views and disposable aggregates, snapshot/fork/reset behavior is simpler. Projections can be rebuilt from the source state.

### 3. Lower architectural surface area

A table, views, and alert state require less conceptual machinery than new graph node types, new payload variants, and synchronization rules.

### 4. Safer truth discipline

Diagnostics become telemetry, not judgment. They may recommend review but cannot accept, reject, validate, or canonize claims.

---

## Decision invariants

```text
INV-D1: Diagnostics are advisory only.
INV-D2: Every diagnostic output must be reproducible from mutation_log + current graph snapshot.
INV-D3: Materialized diagnostic aggregates are disposable and rebuildable.
INV-D4: EpistemicSignal is not a hidden TruthGate.
INV-D5: Mentaury diagnostics never write to Crystal Canon.
```

---

## Consequences

### Positive

- avoids a second diagnostic memory;
- reduces synchronization bugs;
- keeps Crystal boundary clean;
- supports operator-facing observability;
- preserves grant-safe engineering language;
- keeps implementation reversible.

### Costs / open questions

- view performance must be benchmarked before implementation;
- knowledge gap scoring needs calibration;
- the boundary between view-first gaps and tracked research objects remains open;
- future CDR / HTB / ETP integrations require separate decisions.

---

## Current outcome

This is a documentation-only decision draft.

```text
No code.
No migration.
No Canon integration.
No accepted runtime feature.
```

A future Operator GO is required before converting this into implementation tasks.
