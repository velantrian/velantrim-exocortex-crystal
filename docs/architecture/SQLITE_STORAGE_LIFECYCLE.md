# SQLite Storage Lifecycle

**Status:** implemented by the accompanying change; `TESTED` and
`VERIFIED_CHECKPOINT` remain contingent on exact-head CI and merge evidence.

## Purpose

Crystal's durable L3 profile fixes the physical backend and non-secret locator across
process restarts. This operator layer adds a narrow lifecycle for the dependency-free
SQLite profile:

```text
locked SQLite profile
  → consistent backup bundle
  → independent bundle verification
  → restore to a new inactive database and candidate profile
```

It also exposes guarded recovery for the empty profile-initialization lock that can remain
after a hard crash.

These operations preserve storage continuity only:

```text
backup / restore / lock recovery ≠ truth admission
physical L3 ≠ strict Canon
storage receipt ≠ evidence for a claim
```

TruthGate, Guardian, restrictions and deny-dominant reconciliation continue to own trust
and strict read semantics.

## Operator surface

After installation:

```bash
velantrim-storage status [--profile PATH]
velantrim-storage backup BUNDLE [--profile PATH]
velantrim-storage verify BUNDLE
velantrim-storage restore BUNDLE \
  --target-database NEW_DB \
  --target-profile NEW_PROFILE
velantrim-storage inspect-lock [--profile PATH]
velantrim-storage recover-lock \
  [--profile PATH] \
  --expected-mtime-ns VALUE \
  --expected-sha256 VALUE \
  --min-age-seconds 300 \
  --confirm-no-writer
```

Every command emits one JSON object. Exit `0` means `PASS`, exit `1` means a non-fatal
`WARN`, and exit `2` means fail-closed refusal.

## Backup contract

`backup` accepts only a valid locked SQLite profile and a regular source database. It:

1. creates the destination directory with no-overwrite semantics;
2. uses the SQLite online backup API for a transactionally consistent snapshot;
3. runs `PRAGMA integrity_check` on the snapshot;
4. verifies the required Crystal L3 tables;
5. records table counts, page/freelist counts and `user_version`;
6. records SHA-256 and size for the database plus SHA-256 for the copied profile;
7. verifies the bundle contents;
8. writes `complete.json` last and verifies the completed bundle again.

A completed bundle contains:

```text
storage.sqlite3   consistent SQLite snapshot
profile.json      copied source deployment identity
receipt.json      paths, hashes, counts and SQLite metrics
complete.json     final publication marker bound to receipt.json
```

A missing, malformed or mismatched completion marker causes `verify` to fail closed. A
handled backup failure removes the incomplete output. A hard process or host failure can
leave an incomplete directory without a valid completion marker; it is not accepted as a
backup.

The receipt and hashes provide internal integrity and audit evidence. They are not a
cryptographic signature against a malicious actor who can rewrite the whole bundle.

## Verify contract

`verify` is read-only. It rejects:

- a symlinked bundle or symlinked bundle file;
- missing or malformed files;
- an absent/invalid completion marker;
- receipt/profile schema mismatch;
- profile/receipt locator disagreement;
- database/profile/receipt hash mismatch;
- SQLite integrity failure;
- missing required tables;
- table-count or `user_version` disagreement.

Verification does not open, change or activate the current deployment profile.

## Restore contract

`restore` first performs complete bundle verification, then writes only new targets. It
never overwrites an existing database, profile or restore receipt and rejects final-path
symlinks.

The operation:

1. copies the verified database to a new path with no-overwrite semantics;
2. reruns SQLite integrity/table metrics and compares them with the backup;
3. verifies the copied database hash;
4. writes a restore receipt;
5. writes and validates the candidate profile last.

The current active profile path is explicitly forbidden as a restore target. Therefore a
successful restore is not automatically activated:

```text
restore result = new database + candidate profile + receipt
activation      = separate explicit deployment action
```

This ordering makes the candidate profile the last activation-relevant artifact. A hard
crash can still leave partial new targets; the absence of a valid candidate profile and/or
restore receipt identifies an incomplete restore. The command never deletes or modifies
the source bundle or current storage.

## Multiple deployments

The default storage profile is user-level and assumes one default deployment. Services,
containers and side-by-side instances should each set an explicit profile path:

```bash
export VELANTRIM_STORAGE_PROFILE_PATH=/srv/crystal-a/storage-profile.json
velantrim-storage status
```

The `--profile` option allows inspection, backup and lock recovery for a named profile
without silently changing the process default. A restored candidate becomes active only
when an operator explicitly configures a future process to use it.

## Guarded stale-lock recovery

Profile initialization uses an exclusive empty lock file. A hard crash can leave it after
the writer is gone. Recovery is deliberately two-step:

```text
inspect-lock
  → record path, age, mtime_ns, SHA-256, device and inode
  → independently prove no writer is active
  → recover-lock with the exact recorded identity and explicit confirmation
```

Recovery refuses when:

- the lock is absent, recent, non-regular, unreadable or non-empty;
- the caller does not confirm that no writer is active;
- the supplied mtime or SHA-256 differs;
- device, inode, size, mtime or hash changes during recovery;
- an exclusive recovery guard directory cannot be created.

The mutating phase does not directly unlink the inspected path. It atomically moves the
inspected lock into a private `.recovery/stale.lock` quarantine, then tries to create a
non-empty recovery-owned placeholder at the original lock path with `O_EXCL`:

```text
rename inspected lock → private quarantine
  → create recovery placeholder at original lock path
  → if a new writer won the path: never unlink that writer's lock
  → verify quarantined identity
  → remove quarantined stale lock
  → verify and remove the recovery placeholder last
```

This closes the race where a new initializer could create a lock after the final identity
check but before an ordinary path-based unlink. Lock inspection opens the file without
following a final symlink where the platform supports `O_NOFOLLOW` and compares the opened
file identity with `lstat` before reading. No automatic age-based deletion occurs.

A crash can leave the `.recovery` directory, quarantined stale lock, or non-empty recovery
placeholder. Automatic cleanup of those second-order artifacts is not claimed by this
package; they remain a manual operator investigation boundary.

## Supported and unsupported backends

This package supports only the current dependency-free SQLite lifecycle. It does not claim
online backup or restore for LadybugDB or Neo4j.

The following remain separate future work:

- cross-backend logical migration;
- PostgreSQL/pgvector institutional profile;
- automatic SQLite/PostgreSQL selection after data exists;
- dual-write or live cutover;
- automatic activation or rollback;
- distributed fencing and multi-host coordination.

Any future migration must verify facts, vectors, edges, entities, mentions, metadata,
restrictions, evidence and audit continuity with a separate migration receipt.

## Grant boundary

This is deployment/recovery hardening of the existing local-first SQLite baseline:

- pure Python standard library;
- no mandatory cloud or server;
- no new cognitive architecture;
- no second Canon owner;
- no production certification claim;
- no PostgreSQL, pgvector or dedicated VectorDB dependency.
