# Velantrim Crystal — Current Status

**Status date:** 2026-08-08  
**Version:** `0.3.0`  
**Verified runtime checkpoint:** `f03e24c85922d0bb46d6d9dfee98338972135908`  
**Verified tree:** `abf75283b382697b323ab69cfa7235b47171dace`  
**Validated implementation head:** `17ce10ffe12da93be50434c73d08f05a70a5922b`  
**Runtime PR / CI:** #335 / `31224184351`  
**Resource benchmark CI:** `31224005804`

## Verification

- Python 3.11: **2059 passed / 12 skipped / 0 failed**;
- Python 3.12: **2059 passed / 12 skipped / 0 failed**;
- **9361 statements / 100.00% line coverage**;
- `core/storage_migration.py`: **626/626 statements**;
- **7/7** declared Ring Zero mutants killed;
- **9/9** permanent CI jobs successful;
- **2/2** resource benchmark jobs successful.

Exact evidence: [`TEST_REPORT.md`](../TEST_REPORT.md), the
[machine-readable manifest](./status/implementation-manifest.json), and the
[resource report](./benchmarks/SQLITE_LOGICAL_MIGRATION_RESOURCE_EVIDENCE.md).

## Current verified capability boundary

Crystal retains its prior trust, evidence, query, review, authorization and SQLite lifecycle
capabilities. PR #335 additionally provides bounded-streaming logical export and independent
verification inside the existing local-first envelope:

```text
locked SQLite profile
→ fixed cursor batches
→ incremental canonical JSONL
→ disk-backed canonical edge sort
→ same-descriptor hash-first verification
→ disk-backed referential checks
→ exact completed bundle
```

Issue #331 is implemented. The production verifier no longer retains complete datasets or
global identifier sets. Temporary storage is private, preflighted and cleaned on handled
initialization failure.

## Resource boundary

The active limits remain 1 MiB control/record, 64 MiB source/dataset, 200,000 records per
dataset and 384 MiB aggregate JSONL. Benchmark `31224005804` covers 1,025 and 8,193-record
synthetic corpora; it is local-first evidence, not a production SLO or institution-scale
certification.

## Still absent

- PostgreSQL/pgvector runtime, inactive import and exact target equivalence (#332);
- activation, cutover, rollback, dual-write or automatic backend switching;
- distributed fencing and production IdP/multi-tenancy;
- dedicated verified Reader Core;
- legal/security/GDPR certification.

## Authority boundary

```text
storage profile         = deployment identity
migration bundle        = operation evidence
physical L3             = multi-status storage
strict Canon            = trusted read projection
migration/import        != TruthGate admission
successful verification != backend activation
```

## Grant status

The project is submitted and under review. **No award or budget change** is claimed. The
bounded-streaming work in PR #335 is now merged baseline and cannot be counted again as
future funded delta. Future storage funding begins with #332 and separately reviewed later
cutover/rollback/server-lifecycle phases.
