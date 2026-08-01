# ADR-015: Expose one machine-readable ESM specification from the runtime table

- **Status:** Accepted baseline
- **Date:** 2026-08-01
- **Scope:** read-only ESM description and validation

## Context

Crystal already defines its state universe and allowed transitions in
`core.memory.ESM_STATES` and `core.memory.ESM_TRANSITIONS`, and write paths call
`memory.transition_esm()`. Documentation and review discussions still had to
restate that table manually, creating a risk of state/transition drift.

Creating another independently editable ESM table would make the problem worse.

## Decision

`core.esm_spec` imports the active constants from `core.memory` and exposes:

- a deterministic JSON-serializable descriptor;
- terminal states derived from rows with no outgoing transitions;
- protected Ring Zero fact identifiers as a separate write-time constraint;
- a SHA-256 contract identifier;
- structural/reachability validation;
- fail-closed transition queries;
- deterministic shortest-path lookup;
- read-only validation of fact-like state records.

`core.memory` remains the runtime transition authority. The new module is a read
model and invariant checker, not another write path.

## Invariants

- the default `Observed` entry belongs to the state universe;
- every state has an explicit transition-table row;
- transition sources and targets are known;
- target collections are sets/frozensets;
- no self-transition exists;
- all states are reachable from the default entry through the runtime matrix;
- protected fact identifiers are non-blank strings;
- malformed query/record inputs fail closed rather than raising or receiving a
  guessed default.

The active baseline contains 8 states, 15 directed transitions and two derived
terminal states: `Collapsed` and `ImmutableCore`. `Deprecated → Collapsed` and
`Validated → ImmutableCore` are current runtime transitions and are represented
without reinterpretation.

## Consequences

- documentation and tooling can consume one deterministic state descriptor;
- transition drift becomes directly testable;
- matrix membership is explicitly separated from additional write-time guards;
- ESM state remains separate from truth status and CanonicalView authority;
- the runtime table and transition locking/policy behavior remain unchanged;
- no additional dependency or persistent schema is introduced.

## Non-goals

- no new ESM state or transition;
- no automatic record repair;
- no migration mechanism;
- no contradiction decision logic;
- no write API;
- no claim that `Validated` alone means strict Canon;
- no claim that a positive matrix query guarantees a successful write for a
  missing, concurrently changed or protected fact.
