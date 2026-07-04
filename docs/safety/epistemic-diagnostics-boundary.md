# Epistemic Diagnostics Safety Boundary 🔒🧠

**Status:** PROPOSED / DOCUMENTATION ONLY  
**Implementation status:** NOT IMPLEMENTED  
**Scope:** Mentaury / External Labs research boundary  
**Crystal runtime impact:** none

This note defines the safety boundary for proposed Mentaury epistemic diagnostics.

It exists to prevent diagnostic telemetry from becoming a hidden truth engine,
self-modification channel, or Canon write path.

---

## 1. Boundary statement

Epistemic diagnostics may observe internal system history and recommend review.
They must not independently alter truth-state.

```text
Diagnostics are telemetry, not authority.
```

---

## 2. Allowed behavior

Diagnostics may:

- annotate events as `needs_review`;
- raise `WATCH`, `STALE`, or `ESCALATED` alert states;
- surface recurring failure patterns;
- surface possible knowledge gaps;
- suggest operator review;
- suggest Research Mode queueing;
- provide console visibility;
- support later replay from mutation history.

---

## 3. Forbidden behavior

Diagnostics must not:

- write to Crystal Canon;
- bypass TruthGate;
- validate claims;
- reject claims as false;
- promote claims to verified status;
- modify permissions, quotas, or configuration;
- silently quarantine broad clusters without operator review;
- apply automatic confidence penalties;
- become a second source of truth.

---

## 4. Key distinctions

| Signal | Must not be treated as |
|---|---|
| `needs_review` | rejection |
| `knowledge_gap` | falsehood |
| `stale_contradiction` | poison |
| `failure_pattern` | proof of future error |
| `alert_state` | truth-state |
| `failure_pattern_stats` | system-truth |

---

## 5. Required diagnostic invariants

### INV-D1 — Advisory only

```text
Diagnostics may annotate, prioritize, or escalate.
Diagnostics may not directly alter claim truth-state,
Canon membership, or write permissions.
```

### INV-D2 — Reproducibility

```text
Every diagnostic output must be reproducible from mutation_log + current graph snapshot.
```

### INV-D3 — Disposable cache

```text
Materialized diagnostic aggregates are disposable.
If deleted, they must be rebuildable from mutation_log.
```

### INV-D4 — No hidden TruthGate

```text
EpistemicSignal is not a TruthGate.
It may recommend review but cannot accept, reject, or validate claims.
```

### INV-D5 — Crystal boundary

```text
Mentaury diagnostics never write to Crystal Canon.
They remain inside External Labs / Mentaury research scope.
```

---

## 6. Anti-overclaim language

Do not describe these diagnostics as:

- consciousness;
- self-awareness;
- a living organism;
- biological self-healing;
- autonomous personality evolution;
- a second mind inside Crystal.

Preferred language:

```text
operator-facing epistemic diagnostics
self-audit projections over mutation history
derived telemetry over internal memory events
advisory review signals
```

---

## 7. Implementation gate

Before implementation, a separate Operator GO must define:

- exact schema changes;
- migration plan;
- benchmarks for query/cached projection cost;
- tests for reproducibility;
- tests proving diagnostics cannot mutate truth-state;
- tests proving no Canon write path exists.

Until then, this remains a safety boundary for a proposed research/spec draft.
