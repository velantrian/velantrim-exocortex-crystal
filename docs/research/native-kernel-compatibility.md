# Crystal Research Boundary: Velantrim Native Kernel Compatibility

**Status:** `RESEARCH` / `DOCUMENTED_ONLY` / `NOT_IMPLEMENTED`  
**Scope:** optional future compatibility; not Crystal runtime  
**Repository boundary:** documentation only  
**Created:** 2026-07-22  
**Audience:** maintainers, reviewers, grant readers, and future RFC authors

---

## 1. Purpose

This document records a strict boundary between the current public Crystal core and the separate **Velantrim Native Kernel** research direction.

Crystal remains an independent, local-first, verifiable AI memory infrastructure. The Native Kernel is an internal Titan / Full Exo-Cortex research track that explores a more fundamental event-sourced memory substrate.

This document does **not** add runtime behaviour. It does not modify Crystal storage, TruthGate, Guardian, TRACE, Receipt, retrieval, Canon, CLI, API, or any write path.

Safe short formula:

```text
Crystal = deliverable trust product.
Native Kernel = optional internal research substrate.
Compatibility = selective, evidence-driven, and reversible.
```

---

## 2. Current separation

```text
Titan / Full Exo-Cortex research
└── full Native Kernel architecture, experiments, and prototypes

Crystal public repository
└── boundary documentation and separately reviewed trust primitives only

Crystal runtime
└── current code in main, tests, TEST_REPORT.md, and implementation-status docs
```

The following rules are mandatory:

- Crystal works without the Native Kernel.
- Crystal grant deliverables do not depend on the Native Kernel.
- The Native Kernel is not a second Crystal source of truth.
- No Native Kernel event log may write directly to Crystal Canon.
- No live dual-write or storage replacement is proposed here.
- Failure, redesign, or abandonment of the Native Kernel must not invalidate Crystal.

---

## 3. Research architecture being evaluated

The Native Kernel research direction studies the following model:

```text
Claim
→ immutable Event Log
→ deterministic Epistemic State projection
→ rebuildable read models and indexes
→ task-specific PULL selection
→ auditable Receipt
```

Candidate architectural ideas include:

- claim identity and lineage;
- append-only mutation history;
- deterministic state reconstruction;
- explicit `valid_from` / `valid_to` semantics;
- candidate versus canonical contradiction layers;
- idempotent outcome or command handling;
- rebuildable graph, vector, FTS, and SQLite projections;
- task-specific evidence selection;
- receipts that expose selection and conflict state;
- stronger event-envelope integrity.

These are research candidates, not current Crystal capabilities.

---

## 4. Potentially compatible Crystal primitives

Crystal may later evaluate narrowly scoped mechanisms derived from this research.

### 4.1. Claim lineage and version lifecycle

Potential value:

- explicit predecessor and successor relationships;
- traceable supersession;
- historical reconstruction;
- clearer separation of current and expired claims.

Boundary:

```text
Claim lineage may explain history.
It may not bypass TruthGate or create a parallel Canon.
```

### 4.2. Append-only mutation history

Potential value:

- stronger replayability;
- clearer audit semantics;
- deterministic reconstruction after failure;
- separation of accepted facts from the history of how they changed.

Boundary:

- an append-only log is not automatically trustworthy;
- event ordering, actor identity, idempotency, and envelope integrity require separate design;
- a prototype hash chain is not a production integrity guarantee.

### 4.3. Deterministic projection rebuild

Potential value:

- rebuilding read models from authoritative history;
- detecting projection drift;
- treating graph, vector, and FTS indexes as derived infrastructure rather than independent truth authorities.

Boundary:

```text
A projection derives state.
A projection does not self-canonize.
```

### 4.4. Explicit validity intervals

Potential value:

- separating historical truth from current truth;
- avoiding accidental recall of expired states;
- making temporal selection auditable.

Any future Crystal adaptation must define:

- event time versus knowledge time;
- open and closed validity intervals;
- supersession semantics;
- query-time behaviour;
- migration and rollback rules.

### 4.5. Contradiction lifecycle

Potential value:

- separating contradiction candidates from admitted conflicts;
- exposing unresolved conflict state in receipts;
- preventing lexical similarity from becoming an automatic truth mutation.

Boundary:

```text
Candidate contradiction ≠ established contradiction.
Conflict detection ≠ conflict resolution.
```

### 4.6. Receipt and TRACE strengthening

Potential value:

- explicit open and candidate conflicts;
- reproducible selection reasons;
- clearer engine and policy versioning;
- stronger links between claims, evidence, events, and conclusions.

Boundary:

A receipt may prove what the system selected and how it processed it. It does not prove that a weak selection heuristic is sufficient for the user's real task.

### 4.7. Full event-envelope integrity

Potential future fields may include:

```text
event_id
global_seq
timestamp
schema_version
actor
idempotency_key
payload_hash
previous_hash
```

This requires a separate reliability and threat-model RFC. It is not implied by the current Crystal provenance or audit implementation, and it is not introduced by this document.

---

## 5. Explicit non-goals

This document does not propose:

```text
No Native Kernel runtime in Crystal core.
No replacement of current Crystal storage.
No direct Native Event Log → Crystal Canon path.
No live dual-write.
No automatic Canon promotion.
No new autonomous-agent authority.
No consciousness, artificial mind, or living-memory claim.
No production-readiness claim based on a research prototype.
No claim that lexical selection is genuine task sufficiency.
```

The Native Kernel must not be described as:

- Crystal's current source of truth;
- a production operating system for cognition;
- a verified human-like memory model;
- an autonomous truth engine;
- a completed replacement for Crystal architecture.

---

## 6. Grant-safe position

Allowed reviewer-facing wording:

```text
Crystal is an independent, local-first verifiable memory infrastructure.
In a separate Titan research track, Velantrim is exploring an event-sourced
Native Kernel based on immutable claims, provenance, deterministic projections,
and auditable receipts. Crystal does not depend on this experimental kernel.
Future work may selectively adapt validated mechanisms through separate RFCs,
tests, security review, and pull requests.
```

Disallowed wording:

```text
Crystal already runs on the Velantrim Native Kernel.
Native Kernel is Crystal's production source of truth.
Crystal has a new cognitive operating system.
The kernel provides consciousness or autonomous truth.
Prototype benchmarks prove Crystal production scalability.
```

The Native Kernel may appear in strict grant material only as:

```text
optional future R&D direction
separate Titan research track
source of narrowly scoped candidate mechanisms
```

It is not a current grant deliverable.

---

## 7. Evidence and validation requirements

No mechanism may move from this research boundary into Crystal because it is architecturally elegant or because several language models agree with it.

A future proposal must provide:

1. a concrete Crystal failure or limitation;
2. evidence that the current Crystal mechanism is insufficient;
3. a narrow candidate mechanism;
4. measurable expected improvement;
5. invariants and a threat model;
6. failure and rollback behaviour;
7. deterministic tests;
8. compatibility with TruthGate, Guardian, TRACE, and current Canon rules;
9. an independently reviewable benchmark where performance is claimed;
10. a separate maintainer decision and pull request.

Research prototype measurements remain external evidence until reproduced in a reviewable repository artifact with documented methodology.

---

## 8. Promotion path

```text
Titan Native Kernel research
→ reproducible specification and tests
→ offline shadow evaluation on recorded queries
→ evidence that one mechanism solves a Crystal problem
→ Crystal boundary RFC
→ schema, invariants, and threat model
→ bounded prototype outside core/
→ tests and rollback path
→ security and privacy review
→ separate GitHub pull request
→ merge to main
→ implementation-status update
→ only then a claimable Crystal capability
```

No package transfer of the full Native Kernel is permitted.

---

## 9. Decision gates

A mechanism may be considered for Crystal only when all of the following are true:

- a specific Crystal problem has been demonstrated;
- the mechanism is smaller than the research architecture it came from;
- it does not create a second truth authority;
- it does not weaken source, evidence, or admission requirements;
- it does not bypass TruthGate, Guardian, TRACE, or review;
- write idempotency and crash behaviour are defined where relevant;
- projection rebuild and rollback are defined where relevant;
- performance claims use reproducible workloads;
- privacy and deletion consequences are documented;
- the maintainer gives explicit approval for a separate implementation PR.

---

## 10. Relationship to existing Crystal concepts

| Crystal concept | Native Kernel relationship | Boundary |
|---|---|---|
| Canon | possible target of separately admitted facts only | no direct event-log write |
| TruthGate | remains the admission authority | cannot be replaced by replay logic |
| Guardian | remains a structural and policy boundary | cannot be bypassed |
| TRACE / Receipt | may adopt narrowly validated receipt ideas | no automatic compatibility claim |
| ProvenanceChain | conceptually related to event history | not equivalent to a full Native event envelope |
| CanonicalView | conceptually related to deterministic projections | no replacement or duplicate current-state truth |
| Review queue | possible human resolution point for conflicts | no automatic contradiction resolution |
| GDPR erasure / restriction | must remain enforceable | append-only research cannot nullify legal controls |

---

## 11. Reading rule

```text
Research may explore the full substrate.
Crystal may adopt only bounded, tested, auditable primitives.
GitHub main remains implementation truth.
Grant language remains narrower than research language.
```

Final boundary formula:

```text
Research value ≠ current product capability.
Event history ≠ admitted truth.
Projection ≠ Canon.
Compatibility requires evidence, review, and reversibility.
```