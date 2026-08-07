# ADR-017 — Crash-consistent curator decisions and idempotent L3 projection

- **Status:** Proposed implementation draft in issue #315
- **Date:** 2026-08-06
- **Scope:** curator approve, force approve, reject and explicit contradiction decisions

## Context

Crystal stores authoritative operational state and the tamper-evident audit chain in
SQLite, while physical L3 may use a separate graph backend. These fabrics do not share a
transaction. The previous review flow performed effects sequentially:

```text
transition L1
→ merge physical L3
→ persist decision metadata / graph edges
→ append audit event
```

A process or backend failure between steps could leave a `Validated` fact without the
corresponding L3 projection or decision audit proof. Attempting to call this a distributed
ACID transaction would be inaccurate.

## Decision

SQLite is the authoritative decision boundary. One SQLite transaction now records:

1. current candidate and target preconditions;
2. candidate/target ESM transitions and decision metadata;
3. the ordinary tamper-evident curator audit entry;
4. a content-light `review_decisions` command with a stable idempotency key;
5. an idempotent L3 projection intent.

After commit, a synchronous projector attempts the physical L3 node/edge changes. Failure
is stored as `failed` or `blocked`; the command remains retryable after restart. Operator
status exposes decision ids, fact ids, event type, attempt count and bounded error text,
never claim/source text.

```text
SQLite transaction
  ├── persisted state/revision/restriction re-check
  ├── ESM + decision metadata
  ├── audit chain entry + checkpoint
  └── durable projection command
          ↓
idempotent L3 projector
  ├── participant restriction/erasure/state preflight
  ├── MERGE candidate/targets
  ├── deterministic edges
  └── completed / failed / blocked status
```

## Idempotency and recovery

- decision ids are SHA-256 keys over the decision snapshot and accountability inputs;
- L3 node updates use existing idempotent `merge_fact()` semantics;
- edge timestamps/properties are stored in the command, not regenerated during retry;
- a completed command is a no-op on replay;
- pending, failed and blocked commands can be drained in deterministic order;
- projection outcome changes append content-light audit events.

## Erasure and restriction

Projection preflights every participant before writing L3. A tombstoned, missing or
restricted participant blocks the command. Retry therefore cannot recreate erased content
or process restricted content. The durable decision record remains content-light for
accountability.

## Partial SUPERSEDE

A target that loses an optimistic revision/state race remains unchanged. The transaction
records its id in `partial_target_ids`; projection adds the explicit residual
`CONTRADICTS` relation instead of silently deleting or selecting a winner. Missing or
restricted targets fail the entire decision precondition rather than becoming a partial
success.

## Consequences

### Positive

- no untracked L1/audit/L3 crash window for new curator decisions;
- backend outages become observable durable work rather than lost projection;
- restart recovery and replay are deterministic;
- force-override metadata and audit proof share the state transaction;
- reject state and audit proof are atomic even though no L3 projection is required.

### Costs and limitations

- this is transactional-outbox consistency, not cross-database ACID;
- L3 may temporarily lag a recorded decision and must expose that status;
- process-local projector execution is not distributed exactly-once delivery;
- multi-process scheduling/fencing remains a separate concern;
- a complete CI run and independent review are required before this draft becomes
  accepted runtime baseline.

## Non-goals

- no second Canon owner;
- no automatic contradiction winner;
- no TruthGate or Guardian weakening;
- no hidden chain-of-thought persistence;
- no new cloud, broker or graph dependency;
- no production distributed-lock claim.

## Verification required before acceptance

- L3 failure after decision commit;
- audit failure before commit;
- restart recovery;
- repeated node/edge replay;
- restriction and erasure before retry;
- partial target CAS race;
- content-light operator status;
- Python 3.11/3.12 full suite, 100% coverage gate and all permanent CI jobs.
