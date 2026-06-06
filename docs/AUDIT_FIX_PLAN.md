# Audit Fix Plan

Runtime changes must preserve the core invariant:

```text
Graph = Truth.
No canonical L3 write without Guardian + TruthGate + Trace.
```

## P0

- Source-aware truth status: a user-reported world claim is `USER_CLAIMED`, not `VERIFIED`.
- `reconcile.supersede()` must validate the new fact before L3 promotion.

## P1

- Verify receipts against L3 and L1, not L1 alone.
- Add L3 outbox handling to `ingest()`.
- Make the default embedder strictly local/offline.
- Report `VELANTRIM_GENERATOR=anthropic` as an external transfer.
- Split trace confidence from retrieval score.

## P2

- Add graph integrity reporting.
- Align package/version documentation.
- Add a maturity statement for grant reviewers.
