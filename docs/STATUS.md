# Velantrim Crystal — Current Status

**Status date:** 2026-08-08  
**Verified runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6`  
**Verified tree:** `f57e58a6f4d1954b649ba324996fcde42ac287b8`  
**Validated implementation head:** `d7af7c80722274f9217bc5545d150f92e9363f37`  
**Runtime PR / CI:** #337 / `31256316536`  
**PostgreSQL integration CI:** `31256316532`

## Verification

- Python 3.11: **2078 passed / 13 skipped / 0 failed**;
- Python 3.12: **2078 passed / 13 skipped / 0 failed**;
- **9756 statements / 100.00% line coverage**;
- `core/postgresql_migration.py`: **44/44 statements**;
- `core/postgresql_migration_impl.py`: **336/336 statements**;
- **7/7** declared Ring Zero mutants killed;
- **9/9** permanent CI jobs successful;
- **1/1** real PostgreSQL/pgvector integration job successful.

Exact evidence: [`TEST_REPORT.md`](../TEST_REPORT.md) and the
[machine-readable manifest](./status/implementation-manifest.json).

## Current verified capability boundary

Crystal retains the local-first SQLite baseline and now implements issue #332 phase 1:

```text
verified completed logical bundle
→ PostgreSQL 16 / pgvector 0.8.2 preflight
→ new inactive target schema
→ serializable import
→ independent read-only canonical target re-hash
→ exact count / byte / SHA-256 equivalence
→ non-secret receipts
```

The PostgreSQL driver is an optional extra and is lazy-loaded only by explicit operator
commands. The default installation remains pure standard library. The imported target is
not registered in ordinary runtime composition, remains `active=false`, and cannot serve
normal reads or writes.

## Authority boundary

```text
storage profile         = deployment identity
migration bundle        = operation evidence
physical L3             = multi-status storage
strict Canon            = trusted read projection
migration/import        != TruthGate admission
successful equivalence  != backend activation
```

Guardian, TruthGate, restrictions, TrustSnapshot and CanonicalView are unchanged.

## Still absent

- active PostgreSQL read/write runtime selection;
- exact-vs-ANN retrieval evaluation and accepted ANN thresholds;
- activation, cutover, source/target fencing, rollback or dual-write;
- PostgreSQL backup/restore/upgrade lifecycle, production pooling and distributed fencing;
- production IdP/multi-tenancy and legal/security/GDPR certification;
- dedicated verified Reader Core.

## Grant status

The project is submitted and under review. **No award or budget change** is claimed. PR #337
and issue #332 are now merged baseline and cannot be counted again as future funded delta.
Future storage funding must begin with separately reviewed work beyond inactive import and
exact equivalence.