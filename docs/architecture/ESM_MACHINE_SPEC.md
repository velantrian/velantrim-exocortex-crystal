# Epistemic State Machine — Machine Specification

**Status:** implemented read-only contract  
**Runtime source:** `core.memory`  
**Descriptor and validator:** `core.esm_spec`

## Purpose

Crystal already routes state changes through `memory.transition_esm()`. The
machine specification exposes that same runtime table as deterministic JSON and
checks that its structural invariants remain coherent.

It does **not** create a second transition table.

```text
core.memory.ESM_STATES
core.memory.TERMINAL_STATES
core.memory._ALLOWED_TRANSITIONS
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
| `Supported` | evidence-supported but not necessarily strict Canon |
| `Validated` | completed admission/review transition |
| `Contradicted` | explicit invalidation/conflict state |
| `Deprecated` | terminal historical replacement/invalidation |
| `Collapsed` | terminal rejected/pruned state |
| `ImmutableCore` | terminal explicitly created Ring Zero/value state |

`Validated` does not by itself imply strict Canon. CanonicalView independently
requires the exact truth status, allowed ESM state, provenance shape, confidence
shape and processing-restriction state.

## Entry and terminal states

```text
Entry states:    Observed, ImmutableCore
Terminal states: Collapsed, Deprecated, ImmutableCore
```

`ImmutableCore` is an isolated entry: it may be created explicitly, but no normal
ESM transition may enter it.

## Current transition table

```text
Observed      → Hypothesized, Supported, Validated, Contradicted, Collapsed
Hypothesized  → Supported, Validated, Contradicted, Deprecated
Supported     → Validated, Contradicted, Deprecated, Collapsed
Validated     → Supported, Contradicted, Deprecated, Collapsed
Contradicted  → Supported, Deprecated
Collapsed     → ∅
Deprecated    → ∅
ImmutableCore → ∅
```

The `Supported ↔ Validated` pair is intentionally reversible. The state machine
is therefore not required to be acyclic.

## Structural invariants

`validate_esm_spec()` verifies:

- the state universe is non-empty and contains only non-blank strings;
- terminal and entry states belong to the state universe;
- every transition source and target is known;
- transition target collections have the expected set/frozenset shape;
- self-transitions are absent;
- terminal states have no outgoing transitions;
- every state is reachable from a declared entry state;
- `ImmutableCore` cannot be reached by transition.

The validator is read-only and returns all discovered errors rather than mutating
or repairing the runtime table.

## Descriptor

`esm_spec()` returns a fresh JSON-serializable mapping containing:

- schema version;
- sorted states;
- entry and isolated-entry states;
- terminal states;
- sorted transition table;
- SHA-256 over the canonical descriptor;
- validation report and counts.

The digest identifies the transition contract. It is not a signature and does
not prove that a running process is trustworthy.

## Query helpers

- `transition_allowed(source, target)` — fail-closed direct transition query;
- `shortest_transition_path(source, target)` — deterministic breadth-first path;
- `validate_state_records(records)` — read-only validation of fact-like state
  fields without guessing missing defaults.

## Boundaries

This baseline does not:

- change the runtime transition table;
- bypass `memory.transition_esm()` CAS behavior;
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
