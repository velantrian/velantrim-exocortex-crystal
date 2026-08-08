# 🧾 Crystal AI Work Log

This compact log records material decisions, exact evidence, limitations and hand-offs. It
is not a replacement for Git history, issues, pull requests, `CHANGELOG.md` or Notion.
Earlier detailed entries remain available through Git history.

## 2026-08-08 — PR #337 inactive PostgreSQL import/equivalence merged

- Merge: `bbd816c09dd39a02e6de6c1014438490572f40f6`; validated head
  `d7af7c80722274f9217bc5545d150f92e9363f37`.
- Exact-head CI `31256316536`: 9/9; Python 3.11/3.12: 2078 passed / 13 skipped;
  9756 statements / 100.00% coverage.
- Real PostgreSQL/pgvector integration `31256316532`: successful against PostgreSQL 16,
  pgvector 0.8.2 and Psycopg 3.3.4.
- Implemented issue #332 phase 1 only: optional lazy driver, preflight, new inactive schema,
  serializable import, independent exact re-hash and non-secret receipts.
- Independent architecture/security review found no blocking issue; the ephemeral localhost
  `trust` service was explicitly classified as test-only.
- No runtime activation, cutover, rollback, dual-write, automatic switching, ANN acceptance,
  Guardian, TruthGate or strict Canon change.
- Impact classification: `GITHUB_AND_NOTION`.
- Next: separate status-sync PR, then prepend one verified `CURRENT TRUTH` block to the three
  canonical Crystal Notion pages while preserving older checkpoints as audit history.

## 2026-08-08 — PR #335 bounded migration merged

- Merge: `f03e24c85922d0bb46d6d9dfee98338972135908`; validated head
  `17ce10ffe12da93be50434c73d08f05a70a5922b`; CI `31224184351` 9/9.
- Evidence: 2059 passed / 12 skipped, 9361 statements, 100.00% coverage; benchmark
  `31224005804` 2/2.
- Implemented fixed cursor batches, disk-backed canonical edge sorting, same-descriptor
  verification, disk-backed referential checks and failure cleanup.
- Impact classification: `GITHUB_AND_NOTION`.

## 2026-08-07 — Grant/status baseline synchronization (#333 / PR #334)

- Reconciled public README, verification/status files, grant scope, M1–M9 matrix, roadmap,
  security policy and AI context with PR #330.
- The first branch head failed docs-status in CI `31214414769`; stale README/manifest markers
  and incorrect frozen localization blob IDs were corrected before merge.
- Premature Notion merge claims were corrected with top `CURRENT TRUTH` blocks while older
  blocks were retained as audit history.
- PR #334 remains historical grant/status context. Synchronization class:
  `GITHUB_AND_NOTION`.

## 2026-08-07 — Deterministic SQLite logical export merged (#329 / PR #330)

- Merge: `c612c1f7de067b05ed7d01ad82d47a7bc39af23a`; validated head
  `e70c31bf517039f0dd3f77f7bc4b6d3f03936736`; CI `31213056560` 9/9.
- Added canonical JSONL export, independent fail-closed verification and explicit local-first
  resource limits.
- Migration evidence remained operational evidence only and could not activate another
  backend or grant epistemic authority.