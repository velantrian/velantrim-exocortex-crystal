# Crystal Current State

**Status date:** 2026-08-07
**Current documentation base:** `main@5cd0754614327c2ffc14902d5d411e347edf9ae9`
**Verified runtime checkpoint:** `b0df17a06d552ad2543b6d6e5efe8cd99877cfc0`
**Validated runtime head/tree:** `aa822c49c095039de90b92fbe4fe451c7b8f13b7` / `6143d7237222935182db86a166541d0ad07887be`
**Runtime PR / CI:** #325 / `31182471502`
**Version:** `0.3.0`

GitHub `main`, executable tests and completed CI are implementation truth. Notion stores
synchronized rationale and history; it does not override repository evidence.

## 1. Verified runtime evidence

- Python 3.11: **2019 passed / 12 skipped / 0 failed**;
- Python 3.12: successful under the same strict gate;
- **8726 measured statements / 100.00% line coverage**;
- **7/7** declared Ring Zero mutants killed;
- **9/9** permanent CI jobs successful;
- security, Ruff, eval, JSONL integrity, docs-status and Docker green.

The automatic Codex review was unavailable because of quota. That is recorded as absent
review, not approval. Manual diff review found and fixed the stale-lock recovery race before
the final exact-head CI.

## 2. Storage runtime now implemented

PR #322 locked the environment-selected durable L3 backend and non-secret locator across
restarts and added read-only diagnostics.

PR #325 added the pure-standard-library SQLite lifecycle:

```text
status
backup
verify
restore to new inactive database/profile
inspect-lock
explicit guarded recover-lock
```

Backup uses SQLite's online backup API. Verification checks completion, hashes, integrity,
required tables, counts and profile identity. Restore is no-clobber and does not activate
the candidate. Lock recovery uses quarantine plus a recovery-owned placeholder and never
unlinks a lock won by a new initializer.

## 3. Authority boundary

```text
storage profile = deployment identity
backup/restore receipt = operation evidence
physical L3 = multi-status storage
strict Canon = deny-dominant trusted read projection
migration/import != TruthGate admission
```

Storage, migration, retrieval rank and vector indexes cannot establish claim truth.

## 4. Current architecture decision — issue #327

Issue #327 defines a phased cross-backend migration contract and a proposed
PostgreSQL/pgvector institutional profile.

```text
preflight
→ read-only logical export
→ completed verified bundle
→ inactive import
→ exact state equivalence
→ retrieval-quality evaluation
→ explicit cutover
→ optional rollback
```

Architecture acceptance does not mean runtime implementation.

## 5. Approved next runtime slice

The first implementation slice is intentionally narrow:

```text
locked SQLite profile
→ deterministic read-only logical export
→ backend-neutral completed bundle
→ independent fail-closed verification
```

Excluded: target import, activation, rollback, PostgreSQL, pgvector, dual-write, live
cutover and automatic switching.

## 6. Documentation policy

English is the sole authoritative actively maintained GitHub documentation language during
engineering. Existing localized READMEs are frozen snapshots and may lag until a dedicated
final localization pass. Ordinary engineering PRs must not update them.

## 7. Important remaining limitations

- no cross-backend importer or exact-equivalence engine;
- no cutover/rollback/fencing implementation;
- no PostgreSQL/pgvector runtime;
- no distributed curator coordination;
- no complete production IdP/multi-tenancy;
- bounded degraded retrieval can trade recall for work limits;
- performance evidence is not a production SLO;
- supply-chain pinning remains incomplete;
- no dedicated verified Reader Core;
- no legal/security certification claim.

## 8. Synchronization

This issue/PR is `GITHUB_AND_NOTION`. The Project Hub and Current Architectural Position
must record the same status distinction: accepted contract versus absent runtime. Final
merge SHA and CI evidence must be added to Notion after merge.
