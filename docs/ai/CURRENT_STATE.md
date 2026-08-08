# Crystal Current State

**Status date:** 2026-08-08  
**Verified runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6`  
**Validated runtime head / CI:** `d7af7c80722274f9217bc5545d150f92e9363f37` / `31256316536`  
**PostgreSQL integration:** `31256316532`  
**Version:** `0.3.0`

GitHub `main`, executable tests and completed CI are implementation truth. Notion stores
synchronized rationale and audit history; it does not override repository evidence.

## 1. Verified evidence

- Python 3.11 and 3.12: **2078 passed / 13 skipped / 0 failed**;
- **9756 statements / 100.00% coverage**;
- PostgreSQL migration modules: **44/44 + 336/336 statements**;
- **7/7** Ring Zero mutants killed;
- **9/9** permanent CI jobs successful;
- **1/1** real PostgreSQL/pgvector integration job successful.

## 2. Current storage and migration capability

```text
locked durable SQLite profile
→ backup / verify / inactive restore
→ bounded deterministic logical export
→ completed canonical bundle
→ PostgreSQL 16 / pgvector 0.8.2 preflight
→ new inactive transactional target
→ independent read-only canonical re-hash
→ exact state equivalence
→ non-secret receipts
```

Issue #332 is implemented by PR #337 for inactive import and exact equivalence only. Psycopg
is optional and loaded only by explicit operator commands. The default installation remains
pure standard library.

The target remains `active=false`, is absent from ordinary runtime composition and cannot
serve normal reads or writes. Import or equivalence does not establish activation, automatic
selection, cutover, rollback, dual-write, ANN acceptance, TruthGate admission or strict Canon
membership.

## 3. Grant and remaining limitations

The project is submitted and under review; no award or budget change is claimed. PR #337 is
merged baseline and cannot be counted again as funded delta. Remaining independent work
includes exact-vs-ANN evaluation, explicit cutover/fencing, rollback proof, PostgreSQL server
lifecycle, production IdP/multi-tenancy, supply-chain hardening and a dedicated Reader Core.

## 4. Documentation language and translation state

English is the primary working, source and conflict-resolving language, not the only intended
documentation language.

PR #340 restores full visual and semantic root README coverage for all nine supported
locales: Arabic, German, Spanish, French, Hindi, Italian, Japanese, Russian and Simplified
Chinese.

Issue #341 tracks progressive translation of the broader corpus. The first D1 tranche now
reconciles the Russian locale index, Quick Start, Status and Implementation Status against
exact English source checkpoint `main@16d71e731ee658b1faa65c9ea45c0d8cca290f7c`. These Russian D1 documents are
`CURRENT` after merge and protected by `docs-status`.

The corresponding D1 files for Arabic, German, Spanish, French, Hindi, Italian, Japanese and
Simplified Chinese remain `REFRESH_NEEDED`. Reviewer/safety documents remain D2;
architecture D3; grant/project context D4; extended references D5.

See [`../TRANSLATION_STATUS.md`](../TRANSLATION_STATUS.md) and
[`../LOCALIZATION_POLICY.md`](../LOCALIZATION_POLICY.md).
