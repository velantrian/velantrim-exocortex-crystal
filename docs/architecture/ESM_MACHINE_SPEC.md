# Epistemic State Machine — Machine Specification

**Status:** implemented read-only contract  
**Runtime source:** `core.memory.ESM_STATES` and `core.memory.ESM_TRANSITIONS`  
**Descriptor and validator:** `core.esm_spec`

## Purpose

Crystal already routes state changes through `memory.transition_esm()`. The
machine specification exposes that same runtime matrix as deterministic JSON and
checks that its structural invariants remain coherent.

It does **not** create a second transition table.

```text
core.memory.ESM_STATES
core.memory.ESM_TRANSITIONS
core.memory.IMMUTABLE_FACT_IDS
        ↓
core.esm_spec
        ↓
validated deterministic descriptor + sha256
```

## Current states

| State | Role |
|---|---|
| `Observed` | newly stored operational observation |
| `Hypothesized` | candidate hypothesis |
| `Supported` | evidence-supported intermediate state |
| `Validated` | completed admission/review transition |
| `Contradicted` | explicit invalidation/conflict state |
| `Deprecated` | obsolete historical state that may still collapse |
| `Collapsed` | terminal logical removal state |
| `ImmutableCore` | terminal Ring Zero/value state |

`Validated` does not by itself imply strict Canon. CanonicalView independently
requires the exact truth status, allowed ESM state, provenance shape, confidence
shape and processing-restriction state.

## Default entry and terminal states

```text
Default entry state: Observed
Derived terminal states: Collapsed, ImmutableCore
Protected fact ids: VALUES_CORE, RING_ZERO
```

`store_fact()` validates all supplied states, but ordinary ingestion uses
`Observed` as the lifecycle entry. Terminal states are derived from the active
matrix as states with no outgoing transitions.

Protected fact identifiers are a separate write-time rule in
`memory.transition_esm()`. The matrix query alone does not override that guard.

## Current runtime transition table

```text
Observed      → Hypothesized, Supported, Validated, Collapsed
Hypothesized  → Supported, Validated, Collapsed
Supported     → Validated, Collapsed
Validated     → Contradicted, ImmutableCore, Collapsed
Contradicted  → Deprecated, Collapsed
Deprecated    → Collapsed
Collapsed     → ∅
ImmutableCore → ∅
```

There are currently **8 states and 15 directed transitions**.

## Structural invariants

`validate_esm_spec()` verifies:

- the state universe is non-empty and contains only non-blank strings;
- the default entry belongs to the state universe;
- every state has an explicit transition-table row;
- every transition source and target is known;
- transition target collections have the expected set/frozenset shape;
- self-transitions are absent;
- every state is reachable from the declared default entry through the matrix;
- protected fact identifiers are non-blank strings.

The validator is read-only and returns all discovered errors rather than mutating
or repairing the runtime table.

## Descriptor

`esm_spec()` returns a fresh JSON-serializable mapping containing:

- schema version;
- sorted states;
- default entry states;
- terminal states derived from the matrix;
- protected fact identifiers;
- sorted transition table;
- SHA-256 over the canonical descriptor;
- validation report and counts.

The digest identifies the transition contract. It is not a signature and does
not prove that a running process is trustworthy.

## Query helpers

- `transition_allowed(source, target)` — fail-closed matrix-membership query;
- `shortest_transition_path(source, target)` — deterministic breadth-first path;
- `validate_state_records(records)` — read-only validation of fact-like state
  fields without guessing missing defaults.

A positive `transition_allowed()` result means only that the pair exists in the
matrix. The actual write may still fail because the fact is missing, its current
state changed concurrently, or its fact identifier is Ring Zero protected.

## Boundaries

This baseline does not:

- change the runtime transition table;
- bypass `memory.transition_esm()` locking or policy checks;
- determine truth status;
- decide contradictions;
- repair malformed facts automatically;
- expose a write API;
- claim that ESM state alone makes a fact strict Canon.

## Future hardening

A later package may expose the descriptor through operator tooling and add a
repository scan ensuring no production module performs unreviewed direct ESM
field updates. Such a scan must account for legitimate storage initialization and
migration code rather than using a naive string search.
