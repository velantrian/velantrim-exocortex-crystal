# Provenance Chain Contract

> Date: 2026-06-17
> Scope: provenance-chain expectations for Crystal
> Status: docs-only contract. Code must be verified by tests.

## Purpose

A provenance chain is only useful if it records events and detects tampering.

Crystal should not claim hash-chain provenance unless append and verify paths are tested.

## Minimum event fields

A provenance event should include:

```text
prev_hash
event_type
fact_id
from_state
to_state
payload_hash or payload_str
created_at
actor
reason
```

If `actor` and `reason` are part of the integrity claim, they must be included consistently in both:

1. hash computation;
2. verification replay.

## Required tests

Claude Code should add or verify tests for:

1. `append()` returns success for a normal event;
2. a non-empty chain verifies successfully;
3. tampering with payload breaks verification;
4. tampering with `actor` breaks verification if actor is hashed;
5. tampering with `reason` breaks verification if reason is hashed;
6. deletion / erasure workflows write provenance events where applicable;
7. empty chains are not reported as equivalent to a verified non-empty chain.

## Failure semantics

A provenance append failure should not be silently treated as success.

Recommended behaviour:

```text
append failure -> explicit error / degraded audit status
verify empty chain -> empty_chain / no_events, not verified_nonempty_chain
```

## Public wording

Safe:

```text
Crystal provides provenance and receipt mechanisms where implemented and tested.
```

Avoid unless tests prove it:

```text
Every memory mutation is protected by a blockchain-like audit trail.
```

## Relationship to Claude audit

A recent external code audit reported a possible regression in a Titan provenance implementation where `actor` and `reason` were used in hash computation but not accepted by the function signature. Crystal should treat this as a verification task, not as a confirmed Crystal bug unless reproduced in this repository.
