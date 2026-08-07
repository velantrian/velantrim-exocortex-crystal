# Crystal Current State

**Status date:** 2026-08-07  
**Current documentation branch:** `agent/grant-baseline-sync-333`  
**Verified runtime checkpoint:** `c612c1f7de067b05ed7d01ad82d47a7bc39af23a`  
**Verified tree:** `17d65f52ac1d985fca249e6c9a183168d6116ffb`  
**Validated runtime head:** `e70c31bf517039f0dd3f77f7bc4b6d3f03936736`  
**Runtime PR / CI:** #330 / `31213056560`  
**Version:** `0.3.0`

GitHub `main`, executable tests and completed CI are implementation truth. Notion stores
synchronized rationale, grant context and history; it does not override repository evidence.

## 1. Verified runtime evidence

- Python 3.11: **2047 passed / 12 skipped / 0 failed**;
- Python 3.12: **2047 passed / 12 skipped / 0 failed**;
- **9219 measured statements / 100.00% line coverage**;
- **7/7** declared Ring Zero mutants killed;
- **9/9** permanent CI jobs successful;
- security, Ruff, eval, JSONL integrity, docs-status and Docker green.

## 2. Current storage runtime

The verified sequence is:

```text
locked durable SQLite profile
→ backup / verify / inactive restore
→ deterministic logical export
→ completed canonical JSONL bundle
→ independent fail-closed verification
```

PR #330 adds export/verification for physical L3 nodes, vectors, edges, entities, mentions
and metadata. It preserves source/profile identity, canonical ordering, hashes, counts,
vector dimensions, referential integrity and descriptor-bound TOCTOU protections.

The implementation is explicitly bounded for local-first use:

```text
control JSON          <= 1 MiB
source SQLite         <= 64 MiB
one canonical record <= 1 MiB
records per dataset  <= 200,000
one dataset          <= 64 MiB
aggregate JSONL      <= 384 MiB
```

## 3. Authority boundary

```text
storage profile         = deployment identity
migration bundle        = operation evidence
physical L3             = multi-status storage
strict Canon            = deny-dominant trusted read projection
migration/import        != TruthGate admission
successful verification != backend activation
```

Guardian, TruthGate, restrictions, TrustSnapshot and CanonicalView remain unchanged.

## 4. PostgreSQL/pgvector position

PostgreSQL/pgvector is an optional future institutional profile, not the universal default.

```text
SQLite                = verified local-first/lightweight profile
PostgreSQL + pgvector = proposed server/institutional profile
```

No automatic fallback or capability-based switching is permitted after a durable profile
exists. Issue #331 must first add streaming/incremental verification and disk-backed
referential checks. Issue #332 then governs inactive PostgreSQL import and exact-state
equivalence. Activation, cutover and rollback require later explicit phases.

## 5. Grant baseline

The project is submitted and under review; no award or budget change is claimed.
Issue #333 freezes the current baseline and recalculates M1–M9 so merged work is not counted
again as funded delta.

## 6. Important remaining limitations

- no institution-scale streaming cross-backend migration (#331);
- no PostgreSQL/pgvector runtime or exact target equivalence (#332);
- no cutover/rollback/fencing implementation;
- no distributed curator coordination;
- no complete production IdP/multi-tenancy;
- performance evidence is not a production SLO;
- supply-chain pinning remains incomplete;
- no dedicated verified Reader Core;
- no legal/security/GDPR certification claim.

## 7. Documentation policy

English is the sole authoritative actively maintained GitHub documentation language during
engineering. Existing localized READMEs are frozen snapshots and may lag until a dedicated
final reconciliation pass.
