# Provenance Chain Contract

> Date: 2026-06-17
> Scope: per-fact provenance-chain expectations for Crystal
> Status: implemented contract. Track 1 (#168) implemented and tested this
> behaviour in `core/provenance_chain.py` (append-only, hash-chained), wired into
> the GDPR erase path. Broader lifecycle wiring (other state transitions) remains
> follow-up.

## Correction after Claude Code plan

The Titan audit reported a concrete `_compute_hash(actor/reason)` regression in Titan. Crystal should not describe that as a confirmed Crystal runtime bug unless reproduced in this repository.

For Crystal, Claude Code identified this as a planned/absent feature:

```text
core/audit.py       = global audit chain
core/provenance.py  = per-answer receipt provenance
core/provenance_chain.py = per-fact event chain (implemented, Track 1 #168)
```

Track 1 (#168) implemented the per-fact event chain from Sprint1 P1-5 / I89.

## Purpose

A provenance chain is only useful if it records per-fact events and detects tampering.

Crystal should not claim per-fact hash-chain provenance until append and verify paths are implemented and tested.

## Minimum event fields

A provenance event should include:

```text
prev_hash
event_type
fact_id
from_state
to_state
payload_str
created_at
actor
reason
seq
```

If `actor` and `reason` are part of the integrity claim, they must be included consistently in both:

1. hash computation;
2. verification replay.

## Required interface

```python
_GENESIS = "0" * 64


def _compute_hash(
    prev_hash,
    event_type,
    fact_id,
    from_state,
    to_state,
    payload_str,
    created_at,
    actor: str = "system",
    reason: str = "",
) -> str:
    ...
```

`ProvenanceChain.append(...) -> bool` should return `False` on exception and should not propagate errors into erasure.

`ProvenanceChain.verify(fact_id) -> dict` should return:

```python
{"status": "empty_chain", "ok": False, "length": 0}
```

for empty chains, and:

```python
{"status": "ok" | "tampered", "ok": bool, "broken_at": seq | None}
```

for non-empty chains.

## Required tests

Claude Code should add tests for:

1. `append()` returns success for a normal event;
2. a non-empty chain verifies successfully;
3. tampering with `payload_str` breaks verification;
4. tampering with `actor` breaks verification;
5. tampering with `reason` breaks verification;
6. deletion / erasure workflows write an `erase` provenance event where applicable;
7. empty chains are reported as `empty_chain`, not as equivalent to verified non-empty provenance.

## Failure semantics

A provenance append failure should not be silently treated as proof.

Recommended behaviour:

```text
append failure -> explicit false/degraded audit status
verify empty chain -> empty_chain / no_events, not verified_nonempty_chain
```

## Public wording

Safe:

```text
Crystal plans/implements per-fact provenance-chain verification where tests prove the append and replay contract.
```

Now satisfied for the erase path (Track 1, #168). Still avoid the unqualified
universal claim until lifecycle wiring covers every state transition:

```text
Every memory mutation is protected by a per-fact hash-chain audit trail.
```
