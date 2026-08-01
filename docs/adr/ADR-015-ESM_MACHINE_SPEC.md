# ADR-015: Expose one machine-readable ESM specification from the runtime table

- **Status:** Accepted baseline
- **Date:** 2026-08-01
- **Scope:** read-only ESM description and validation

## Context

Crystal already defines its state universe and allowed transitions in
`core.memory`, and write paths call `memory.transition_esm()`. Documentation and
review discussions still had to restate that table manually, creating a risk of
state/transition drift.

Creating another independently editable ESM table would make the problem worse.

## Decision

`core.esm_spec` imports the active constants from `core.memory` and exposes:

- a deterministic JSON-serializable descriptor;
- a SHA-256 contract identifier;
- structural/reachability validation;
- fail-closed transition queries;
- deterministic shortest-path lookup;
- read-only validation of fact-like state records.

`core.memory` remains the runtime transition authority. The new module is a read
model and invariant checker, not another write path.

## Invariants

- terminal and entry states belong to the state universe;
- transition sources and targets are known;
- no self-transition exists;
- terminal states have no outgoing transitions;
- all states are reachable from declared entries;
- `ImmutableCore` is created explicitly and cannot be reached by transition;
- malformed query/record inputs fail closed rather than raising or receiving a
  guessed default.

## Consequences

- documentation and tooling can consume one deterministic state descriptor;
- transition drift becomes directly testable;
- ESM state remains separate from truth status and CanonicalView authority;
- the runtime table and CAS transition function remain unchanged;
- no additional dependency or persistent schema is introduced.

## Non-goals

- no new ESM state or transition;
- no automatic record repair;
- no migration mechanism;
- no contradiction decision logic;
- no write API;
- no claim that `Validated` alone means strict Canon.
