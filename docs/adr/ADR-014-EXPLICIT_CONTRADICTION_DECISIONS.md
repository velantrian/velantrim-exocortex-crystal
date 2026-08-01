# ADR-014: Contradictions require an explicit, report-bound curator decision

- **Status:** Accepted baseline
- **Date:** 2026-08-01
- **Scope:** pending WORLD_FACT review decisions

## Context

The review queue could diagnose a pending item as `conflict`, but normal
`approve()` treated that diagnosis as advisory and promoted the item without an
explicit conflict decision. This preserved both claims but made the semantic
choice indistinguishable from an ordinary clean approval.

Similarity and confidence cannot safely select a winner. Apparent contradiction
may represent different time periods, populations, scopes, definitions or source
quality. Silent automatic resolution would erase this uncertainty.

## Decision

A current contradiction produces a frozen, content-free
`ContradictionReport`. Normal `approve()` fails closed with
`CONFLICT_DECISION_REQUIRED`. A curator must invoke the separate resolution path
with:

- one explicit disposition;
- a non-empty actor;
- a non-empty reason;
- optionally, an expected report id for optimistic concurrency;
- explicit target ids for `SUPERSEDE`.

Supported dispositions:

| Disposition | Effect |
|---|---|
| `REVIEW_REQUIRED` | no mutation; leave the candidate pending |
| `COEXIST` | validate the candidate and preserve explicit `CONTRADICTS` edges |
| `CONTEXTUALIZE` | validate both and add `CONTEXTUALIZES` edges |
| `SUPERSEDE` | validate the candidate; selected current facts become Deprecated and link `SUPERSEDED_BY` |

The report retains identifiers, classifier kind, signal and similarity only. It
does not duplicate claim/source text and declares no automatic winner.

## Runtime topology

```text
pending WORLD_FACT
        ↓
Guardian + TruthGate
        ↓
contradiction detection
        ↓
frozen ContradictionReport
        ↓
normal approve: blocked
        ↓
explicit curator disposition + actor + reason
        ↓
recompute report / optional report-id check
        ↓
accountable state and graph update
```

## Supersede partial-failure rule

L1 and L3 do not share a distributed transaction. The executor preflights all
selected targets. If a target loses a later CAS race after the candidate has
already been validated, the operation returns `partial=true`, retains the old
fact and records the partial target ids in the audit chain.

The safe residual is explicit coexistence. The implementation never silently
deletes or invalidates a target it failed to transition.

## Consequences

- a conflict can no longer pass through ordinary clean approval;
- every resolution is actor/reason attributed;
- report-id checking detects a stale curator view;
- conflict audit detail remains content-free;
- confidence and similarity remain advisory signals;
- contextual coexistence is distinct from factual supersession;
- review history exposes conflict dispositions.

## Non-goals

- no automatic source-quality winner;
- no LLM/NLI authority over the decision;
- no universal semantic contradiction detector;
- no transactional guarantee across separate L1/L3 fabrics;
- no domain-specific temporal/population schema in this first baseline;
- no change to non-conflicting approval or blocked force-override semantics.
