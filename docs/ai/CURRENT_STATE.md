# Crystal Current State

**Status date:** 2026-08-08  
**Verified runtime checkpoint:** `f03e24c85922d0bb46d6d9dfee98338972135908`  
**Verified tree:** `abf75283b382697b323ab69cfa7235b47171dace`  
**Validated runtime head:** `17ce10ffe12da93be50434c73d08f05a70a5922b`  
**Runtime PR / CI:** #335 / `31224184351`  
**Resource benchmark:** `31224005804`  
**Version:** `0.3.0`

GitHub `main`, executable tests and completed CI are implementation truth. Notion stores
synchronized rationale and history; it does not override repository evidence.

## 1. Verified evidence

- Python 3.11 and 3.12: **2059 passed / 12 skipped / 0 failed**;
- **9361 statements / 100.00% coverage**;
- storage migration module: **626/626 statements**;
- **7/7** Ring Zero mutants killed;
- **9/9** permanent CI jobs and **2/2** benchmark jobs successful.

## 2. Current storage runtime

```text
locked durable SQLite profile
→ backup / verify / inactive restore
→ fixed-batch deterministic logical export
→ private disk-backed edge ordering
→ completed canonical JSONL bundle
→ same-descriptor independent verification
→ private disk-backed referential checks
```

Issue #331 is implemented by PR #335. The production path is bounded-memory inside the
existing local-first size envelope. Benchmark results for 1,025 and 8,193 synthetic corpora
are recorded in `docs/benchmarks/SQLITE_LOGICAL_MIGRATION_RESOURCE_EVIDENCE.md`; they are not
a production SLO or institution-scale certification.

## 3. Authority boundary

```text
physical L3      != strict Canon
migration bundle != claim evidence
verification     != backend activation
benchmark        != deployment certification
```

Guardian, TruthGate, restrictions, TrustSnapshot and CanonicalView remain unchanged.

## 4. PostgreSQL/pgvector position

SQLite remains the verified local-first profile. PostgreSQL/pgvector is proposed future
work under #332. No driver, importer, target schema, activation, cutover, rollback,
dual-write or automatic fallback is implemented.

## 5. Grant and remaining limitations

The project is submitted and under review; no award or budget change is claimed. PR #335
is merged baseline and must not be counted again as funded delta. Remaining work includes
#332, later cutover/rollback/server lifecycle, distributed coordination, production IdP,
supply-chain hardening and a dedicated Reader Core.

English is the sole authoritative actively maintained GitHub documentation language during
engineering. Localized READMEs remain frozen snapshots.
