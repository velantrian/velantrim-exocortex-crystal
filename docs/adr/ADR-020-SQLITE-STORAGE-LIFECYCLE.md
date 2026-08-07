# ADR-020: Fail-closed SQLite storage lifecycle

- **Status:** Accepted by the accompanying implementation, pending merge evidence
- **Date:** 2026-08-07
- **Scope:** existing durable SQLite L3 deployment profile

## Context

ADR/implementation work for the durable L3 profile prevents backend and locator drift, but
it does not provide a verified operator path for backup, restore or recovery of an empty
initialization lock left by a hard crash. Ad-hoc file copying is unsafe with SQLite WAL,
and deleting/editing a storage profile or lock is not a migration or recovery proof.

## Decision

Add a pure-standard-library `velantrim-storage` operator command with six actions:

```text
status
backup
verify
restore to new inactive targets
inspect-lock
explicit guarded recover-lock
```

SQLite backup uses the native backup API, not direct copying of the active database. A
bundle is accepted only when hashes, profile/receipt consistency, SQLite integrity,
required table counts and a completion marker all verify. Restore never overwrites or
activates the current profile; it produces a new database, candidate profile and receipt.
The candidate profile is written last.

Lock recovery requires exact identity values from a prior inspection plus explicit
operator confirmation that no writer is active. It never deletes locks automatically.
The inspected lock is moved into a private recovery quarantine before mutation. A
recovery-owned non-empty placeholder is then created at the original path with `O_EXCL`;
if a new writer wins that path, recovery does not unlink the writer's lock. The stale
quarantine and placeholder are removed only after identity verification.

## Authority boundary

```text
storage lifecycle = deployment continuity
TruthGate          = epistemic admission
Guardian           = structural/safety constraints
TrustSnapshot      = deny-dominant strict read projection
```

No backup, restore receipt, lock age, hash or database presence establishes truth or strict
Canon membership.

## Consequences

### Positive

- consistent backup of WAL-mode SQLite without stopping normal readers/writers;
- machine-readable and independently verifiable bundles;
- no-clobber restore with explicit inactive candidate profile;
- bounded, explicit stale-lock recovery rather than manual blind deletion;
- named profile support for multiple deployments;
- no new runtime dependency.

### Limitations

- SQLite only;
- no cross-backend migration or automatic cutover;
- no malicious-tamper signature for a fully rewritable bundle;
- hard crashes can leave an incomplete output directory or partial restore targets;
- a stale `.recovery` directory, quarantine, or recovery placeholder still requires
  manual investigation;
- no distributed writer fencing or production backup scheduler.

## Rejected alternatives

### Copy the live SQLite file directly

Rejected because WAL/checkpoint state can make a raw file copy inconsistent.

### Restore over the current database/profile

Rejected because partial failure or operator error could destroy the last known-good
instance and silently change deployment identity.

### Automatically delete locks older than a threshold

Rejected because age alone cannot prove that a slow or paused writer is dead.

### Add PostgreSQL/pgvector now

Rejected for this package. A server profile requires a separate architecture, migration,
security, operations and invariant-equivalence decision.
