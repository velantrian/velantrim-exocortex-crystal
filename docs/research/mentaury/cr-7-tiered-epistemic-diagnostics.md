# CR-7 v3 — Tiered Epistemic Diagnostics 🧠🧾

**Status:** PROPOSED / AWAITING OPERATOR GO  
**Implementation status:** NOT IMPLEMENTED  
**Repository scope:** documentation-only research draft  
**Placement:** External Labs / Mentaury research layer  
**Crystal runtime impact:** none  
**Canon access:** none

> This document is a design candidate. It does not describe implemented runtime
> behaviour in the current Crystal core. It must not be treated as an accepted
> feature, release promise, or production contract.

---

## 1. Core principle

CR-7 v3 replaces earlier ideas about separate diagnostic memory nodes with a
stricter system-truth principle:

```text
External truth = Crystal Canon.
System-truth = mutation_log.
Diagnostics = derived projections, cached aggregates, and alert states.
```

The design goal is to make internal epistemic diagnostics reproducible from the
system's own mutation history instead of storing diagnostics as a second memory.

```text
Mentaury should not create a second memory to remember its errors.
It should learn to read its own mutation history.
```

---

## 2. What this supersedes as a preferred candidate

Earlier research backlog items split the idea into several mechanisms:

- Meta-Memory of Failure / `FAILURE_MOTIF`
- Epistemic Humility / `UNKNOWN_REGION`
- Stale Contradiction TTL
- Memory Health Metrics

CR-7 v3 keeps the intent, but changes the implementation candidate:

| Earlier idea | CR-7 v3 representation |
|---|---|
| Failure memory | `failure_pattern_stats` derived from `mutation_log` |
| Unknown regions / knowledge gaps | `knowledge_gap_view` |
| Stale contradiction TTL | `contradiction.alert_state` + `stale_contradiction_view` |
| Memory health metrics | operator-facing diagnostics and observability metrics |

The earlier backlog remains useful as research history. CR-7 v3 is the refined
preferred candidate because it minimizes new entities and avoids a second source
of truth.

---

## 3. Architecture overview

```text
mutation_log 🧾
   │
   ├─ contradiction.alert_state ⏳
   ├─ failure_pattern_stats 🪞
   ├─ knowledge_gap_view 🌫️
   ├─ stale_contradiction_view ⏳
   │
   └─ compute_epistemic_signal(event) ⚠️
          └─ needs_review / watch / review_recommended
```

Diagnostics are advisory telemetry. They may annotate, prioritize, or recommend
review. They must not directly alter truth-state, write to Canon, or act as a
hidden TruthGate.

---

## 4. Tier 0 — source of system-truth: `mutation_log`

The mutation log is the authoritative record for internal system events:

- claim creation;
- claim state transitions;
- contradiction creation and resolution;
- source/provenance changes;
- operator actions;
- admission attempts;
- quarantine/review events;
- snapshot/fork/reset events.

All diagnostic outputs must be reproducible from `mutation_log` plus the current
graph snapshot.

```text
If a diagnostic cannot be reproduced from mutation_log + current graph snapshot,
it is invalid and must not be treated as system knowledge.
```

---

## 5. Tier 1 — computed properties on existing records

### 5.1 Contradiction alert state

A stale contradiction should not become a new diagnostic memory object. It is an
existing contradiction whose unresolved age requires operator attention.

Candidate data-model addition:

```yaml
contradiction:
  alert_state:
    - NONE
    - WATCH
    - STALE
    - ESCALATED
    - OPERATOR_PENDING
  slow_loop_age: int
```

Default transition policy:

```text
0-2 Slow Loop cycles  → NONE
3-5 Slow Loop cycles  → WATCH
5-10 Slow Loop cycles → STALE
>10 Slow Loop cycles  → ESCALATED
operator opened item  → OPERATOR_PENDING
```

Boundary rule:

```text
STALE ≠ poison.
ESCALATED ≠ false.
alert_state escalates attention only.
```

In P0, `STALE` and `ESCALATED` should surface in the Observation Console and
suggest operator review. They must not automatically delete, reject, quarantine,
or canonize data.

---

## 6. Tier 2 — disposable materialized aggregate

### 6.1 `failure_pattern_stats`

Failure patterns may need fast lookup in a Fast Loop, but they should not become
semantic memory nodes.

Candidate representation:

```yaml
failure_pattern_stats:
  pattern_id: string
  failure_class:
    - LOW_TRUST_OVERCONFIDENCE
    - HYPOTHESIS_AS_FACT
    - UNSUPPORTED_MERGE
    - ROUTING_MISPLACEMENT
    - TEMPORAL_DRIFT
    - FAKE_PROVENANCE_PATTERN
  source_type: string
  claim_type: string
  trigger_count: int
  first_seen: timestamp
  last_seen: timestamp
  active: boolean
  rebuilt_from_mutation_log_at: timestamp
```

This table is not:

- a graph node;
- a claim;
- a semantic memory item;
- a truth object;
- a Canon candidate.

It is a rebuildable statistical aggregate over `mutation_log`.

```text
failure_pattern_stats is not system-truth.
If deleted, it must be rebuildable from mutation_log.
```

No performance claims are made here. Actual lookup and refresh times require
benchmarks before implementation.

---

## 7. Tier 3 — query-based views

### 7.1 `knowledge_gap_view`

A knowledge gap is not a false claim and not merely a low-confidence claim.

```text
low confidence = weak claim exists.
knowledge gap = evidence coverage is insufficient or missing.
```

Candidate view inputs:

- unresolved open loops;
- low evidence coverage;
- persistent unresolved clusters;
- lack of supported or validated claims;
- high salience with weak evidence;
- repeated need for Research Mode.

Candidate scoring model:

```text
knowledge_gap_score =
  unresolved_pressure
+ low_evidence_coverage
+ persistence
+ salience_pressure
```

Candidate fields:

```yaml
knowledge_gap_view:
  cluster_id: string
  cluster_domain: string
  open_loop_count: int
  supported_claim_count: int
  validated_claim_count: int
  avg_confidence: float
  evidence_coverage: float
  cluster_age_cycles: int
  salience_pressure: float
  knowledge_gap_score: float
  suggested_action:
    - RESEARCH_MODE
    - OPERATOR_REVIEW
    - WAIT
    - ARCHIVE_CONTEXT
```

Important correction:

```text
Knowledge gap must not mark claims as false.
It marks an area as insufficiently supported.
```

### 7.2 `stale_contradiction_view`

This view filters existing contradictions by `alert_state` and unresolved age.

Candidate fields:

```yaml
stale_contradiction_view:
  contradiction_id: string
  open_since: timestamp
  slow_loop_age: int
  alert_state: NONE | WATCH | STALE | ESCALATED | OPERATOR_PENDING
  related_claim_ids: list
  source_summary: json
  reason_unresolved: string
  suggested_action:
    - OPERATOR_REVIEW
    - RESEARCH_QUEUE
    - QUARANTINE_CANDIDATE
    - ARCHIVE_WITH_MARKER
```

```text
stale_contradiction_view is a lens, not a judge.
It does not resolve contradictions automatically.
```

---

## 8. Fast Loop addition — `compute_epistemic_signal(event)`

Fast Loop may use diagnostics as soft telemetry. It must not use diagnostics as
a hidden TruthGate.

Candidate signal object:

```yaml
EpistemicSignal:
  review_flag: boolean
  risk_level:
    - LOW
    - MEDIUM
    - HIGH
  matched_failure_patterns: list
  gap_context: list
  contradiction_pressure: float
  recommendation:
    - NONE
    - LOG
    - WATCH
    - REVIEW
    - OPERATOR_ATTENTION
```

Candidate placement:

```text
on_new_event(event):
  1. record raw event
  2. extract candidate claims
  3. embed / relate to graph
  4. compute semantic novelty
  5. compute salience
  5.5. compute_epistemic_signal(event)
       - lookup failure_pattern_stats
       - check source_type / claim_type pattern matches
       - annotate event with review_flag if needed
       - do not change truth-state
  6. continue normal Fast Loop
```

Hard rule:

```text
EpistemicSignal may add needs_review / watch / review_recommended.
It may not apply confidence penalty or change epistemic_state directly.
```

---

## 9. Slow Loop addition — `refresh_epistemic_projections()`

Candidate placement:

```text
slow_loop():
  ...
  8. write consolidation report

  8.5. refresh_epistemic_projections():
       - update contradiction.slow_loop_age
       - update contradiction.alert_state
       - refresh failure_pattern_stats from mutation_log
       - make knowledge_gap_view available for console / research
       - emit diagnostic summary

  9. watchdog check / cleanup / exit
```

A future implementation may use SQL views, materialized views, cached tables, or
in-memory indexes. Cached projections must remain disposable and derivable from
`mutation_log`.

---

## 10. Observation Console

Candidate dashboard:

```text
EPISTEMIC DIAGNOSTICS 👁️

▸ Failure Patterns 🪞
  - repeated error motifs
  - source-type correlations
  - claim-type correlations
  - matched mutation history

▸ Knowledge Gaps 🌫️
  - unresolved clusters
  - low evidence coverage zones
  - persistent open loops
  - research-mode candidates

▸ Stale Contradictions ⏳
  - WATCH / STALE / ESCALATED conflicts
  - open age
  - related claims
  - suggested operator action
```

Operator actions may include inspection, review, queueing research, manual
quarantine candidate creation, or manual contradiction resolution. These actions
are operator-mediated and must not be treated as self-modification.

---

## 11. Metrics

| Metric | Definition | Status |
|---|---|---|
| Failure recurrence rate | Share of failure patterns recurring more than once in a window. | observational |
| Gap persistence ratio | Share of knowledge gaps lasting more than M cycles. | observational |
| Contradiction aging ratio | Share of contradictions in STALE / ESCALATED. | operational |
| Diagnostic reproducibility rate | Share of diagnostic outputs reproducible from mutation_log + snapshot. | critical |
| Review recommendation rate | Share of Fast Loop events marked `needs_review`. | observational |

```text
Metrics are observability signals, not optimization targets by default.
```

---

## 12. Diagnostic invariants

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

## 13. Compliance check

| Constraint | Result |
|---|---|
| No self-modification | Diagnostics do not alter config, rights, or quotas. |
| No Canon write | No Crystal pathway. |
| Auditability | All outputs derived from mutation_log + snapshot. |
| Fast Loop safety | Soft review signal only. |
| Slow Loop safety | Refresh projections, not graph-truth objects. |
| Rollback/fork safety | Projections rebuild from source state. |
| Grant-safe wording | No consciousness, organism, or biological equivalence claim. |

---

## 14. Rejected from this design

| Rejected item | Reason |
|---|---|
| `DIAGNOSTIC` graph nodes in P0/P1 | Creates second memory / synchronization risk. |
| `confidence = 1.0` diagnostic nodes | Confuses log-event truth with interpretation truth. |
| Auto confidence penalty | Bias risk and hidden truth-state mutation. |
| Automatic claim rejection from diagnostics | Diagnostics are advisory only. |
| One giant untested view as mandatory implementation | Hard to test; implementation may use smaller views. |
| Performance claims without benchmarks | Generated estimates are not evidence. |
| “Metacognition” as philosophical claim | Use engineering framing: diagnostics / telemetry. |

---

## 15. Non-goals

CR-7 v3 does not implement:

- runtime code;
- database migrations;
- Canon integration;
- self-modification;
- autonomous repair;
- CDR / Contradiction-Driven Refactoring;
- HTB / Homeostatic Truth Budget;
- ETP / Epistemic Trace Playback beyond mutation-log replay potential.

Those may be future research candidates, but they are out of scope here.
