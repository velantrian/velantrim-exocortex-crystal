# Velantrim Crystal — Current Status

**Status date:** 2026-08-07  
**Version:** `0.3.0`  
**Verified runtime checkpoint:** `c612c1f7de067b05ed7d01ad82d47a7bc39af23a`  
**Verified tree:** `17d65f52ac1d985fca249e6c9a183168d6116ffb`  
**Validated implementation head:** `e70c31bf517039f0dd3f77f7bc4b6d3f03936736`  
**Runtime PR / CI:** #330 / `31213056560`

## Verification

- Python 3.11: **2047 passed / 12 skipped / 0 failed**;
- Python 3.12: **2047 passed / 12 skipped / 0 failed**;
- **9219 statements / 100.00% line coverage**;
- **7/7** declared Ring Zero mutants killed;
- **9/9** permanent CI jobs successful.

Exact evidence: [`TEST_REPORT.md`](../TEST_REPORT.md) and the
[machine-readable manifest](./status/implementation-manifest.json).

## Current verified capability boundary

Crystal currently provides:

- local-first L0/L1 memory and pluggable physical L3 storage;
- explicit Guardian and TruthGate admission boundaries;
- physical L3 multi-status storage separated from strict Canon;
- immutable deny-dominant `TrustSnapshot` / `CanonicalView` reads;
- read-only public HTTP, CLI and MCP query paths;
- TRACE, receipts, provenance and replay controls;
- explicit contradiction reports and authorized `COEXIST`, `CONTEXTUALIZE` and
  `SUPERSEDE` decisions;
- scoped curator roles/capabilities and process-local decision leases;
- bounded legacy retrieval and explicit reindex refusal;
- durable L3 profile locking;
- SQLite backup, independent verification, inactive restore and guarded stale-lock
  recovery;
- deterministic SQLite logical export and independent bundle verification under a fixed
  local-first resource contract.

## Storage and migration status

```text
SQLite local-first profile
→ backup / verify / inactive restore
→ deterministic logical export
→ independent bundle verification
```

Current logical-export limits:

| Resource | Limit |
|---|---:|
| control JSON | 1 MiB |
| source SQLite file | 64 MiB |
| record | 1 MiB |
| records per dataset | 200,000 |
| dataset | 64 MiB |
| aggregate JSONL | 384 MiB |

This is a finite local-first envelope, not an institution-scale streaming engine.

Still absent:

- cursor-batched/incremental cross-backend migration (#331);
- PostgreSQL/pgvector runtime, inactive import and exact target equivalence (#332);
- cutover, rollback, dual-write or automatic backend switching;
- distributed fencing and production IdP/multi-tenancy;
- dedicated verified Reader Core;
- production SLO or legal/security certification.

## Authority boundary

```text
storage profile         = deployment identity
migration bundle        = operation evidence
physical L3             = multi-status storage
strict Canon            = trusted read projection
migration/import        != TruthGate admission
successful verification != backend activation
```

No storage adapter, migration result, retrieval score, topic facet or model output may
establish claim truth or bypass Guardian/TruthGate.

## Grant status

The project is submitted and under review. No award or budget change is claimed.
Merged baseline work must not be counted again as funded delta. Issue #333 governs the
current baseline freeze and M1–M9 recalculation.

## Documentation policy

English is the authoritative actively maintained GitHub documentation language. Existing
localized README files are frozen snapshots until a dedicated final reconciliation pass.
GitHub main, tests and CI are implementation truth; Notion stores synchronized rationale,
planning and history.
