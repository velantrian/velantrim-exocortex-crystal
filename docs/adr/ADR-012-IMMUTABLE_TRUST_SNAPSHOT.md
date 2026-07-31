# ADR-012: Reconcile trust metadata through an immutable read snapshot

- **Status:** Accepted baseline
- **Date:** 2026-08-01
- **Scope:** read-only query resolution only

## Context

Crystal stores and transports fact-shaped data through several representations:
L1 rows, physical L3 nodes, retrieval hits, FactsPack entries, CanonicalView
inputs, TRACE elements and Receipt citations.

The read-only query path must combine L3 content with deny-dominant L1 state.
Doing that directly in a mutable dictionary creates a hybrid-record risk: one
field can be replaced before all disagreements have been detected, and later
code cannot distinguish an authoritative value from an intermediate mutation.

## Decision

The query resolver first builds a frozen, slotted `TrustSnapshot` from:

- one resolved physical L3 node;
- an optional L1 row for deny-dominant state/restriction checks;
- ranking-only retrieval score metadata.

The snapshot:

- is immutable after construction;
- retains only scalar immutable fields;
- takes claim/source/verdict metadata from L3;
- allows L1 only to make the result more restrictive;
- represents missing or malformed trust metadata as unknown (`None`) rather
  than coercing it into a trusted default;
- records disagreement categories in a content-free immutable tuple;
- sets `epistemic_state=STORE_STATE_CONFLICT` when trust representations
  genuinely disagree or when a required L3 trust field is malformed;
- emits a fresh compatibility dictionary only after reconciliation is complete.

`CanonicalView`, Guardian and existing answer/receipt code continue consuming a
mapping in this first slice. The snapshot is therefore a boundary object, not a
repository-wide schema migration.

## Trust rules

```text
L3 content/verdict
        +
L1 terminal state or restriction
        +
explicit metadata consistency checks
        ↓
frozen TrustSnapshot
        ↓
fresh compatibility mapping
        ↓
Guardian + CanonicalView
```

Important details:

- terminal L1 states (`Collapsed`, `Contradicted`, `Deprecated`) win;
- a confirmed restriction on either side wins;
- a confirmed L1 `restricted=False` may fill a backend's missing L3 bit;
- non-terminal ESM drift fails closed;
- confidence comparisons use numeric tolerance;
- missing L3 `claim_type` uses the established `WORLD_FACT` default;
- malformed or missing L3 confidence remains unknown (`None`) inside the typed
  snapshot, adds the content-free `confidence` conflict category and forces
  `STORE_STATE_CONFLICT` even when no L1 row exists;
- the temporary compatibility mapping preserves the historical safe `0.0`
  confidence sentinel for existing mapping consumers. That sentinel is not the
  snapshot's internal truth and cannot erase the recorded conflict;
- retrieval score remains ranking metadata and never changes trust state.

## Consequences

- reconciliation decisions cannot be changed by accidental in-place mutation;
- store disagreement and malformed required metadata become explicit and
  content-free;
- unknown/corrupt confidence is distinguishable from a genuine numeric zero
  inside the typed boundary;
- public search/answer mapping shapes remain compatible during the narrow
  migration;
- the legacy admission-capable pipeline remains unchanged in this PR;
- future work may adopt the same boundary object in other paths only through
  separate behaviour-pinned migrations;
- removal of the outward `0.0` compatibility sentinel is deferred until
  downstream mapping consumers accept optional typed confidence directly.

## Non-goals

- no new ESM state machine;
- no TruthGate or CanonicalView policy change;
- no database/schema change;
- no automatic contradiction resolution;
- no repository-wide replacement of all fact dictionaries;
- no serialization format commitment for the internal snapshot class.

## Verification

`tests/test_trust_snapshot.py` pins immutability, strict scalar normalization,
L1 deny dominance, restriction handling, metadata drift, content-free conflict
categories, internal `None` versus outward `0.0` compatibility behaviour and
fresh compatibility mappings. Existing query-boundary tests pin end-to-end
behaviour.