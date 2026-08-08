# Crystal Current State

**Status date:** 2026-08-08  
**Verified runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6`  
**Verified tree:** `f57e58a6f4d1954b649ba324996fcde42ac287b8`  
**Validated runtime head:** `d7af7c80722274f9217bc5545d150f92e9363f37`  
**Runtime PR / CI:** #337 / `31256316536`  
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
is an optional extra and is loaded only by explicit operator commands. The default
installation remains pure standard library.

## 3. Authority boundary

```text
physical L3       != strict Canon
migration bundle  != claim evidence
import success    != backend activation
exact equivalence != ordinary runtime availability
```

The target remains `active=false`, is absent from ordinary runtime composition and cannot
serve normal reads or writes. Guardian, TruthGate, restrictions, TrustSnapshot and
CanonicalView remain unchanged.

## 4. PostgreSQL/pgvector position

PostgreSQL/pgvector now has verified inactive migration tooling, not an active storage
profile. No automatic selection, cutover, rollback, dual-write, ANN acceptance, production
pooling, server backup/restore/upgrade lifecycle or distributed fencing is implemented.

Production credentials and credential-bearing connection strings must not enter profiles,
bundles, receipts, application logs, issues or Notion. TLS is required by default; the
plaintext flag exists only for explicit local integration tests.

## 5. Grant and remaining limitations

The project is submitted and under review; no award or budget change is claimed. PR #337 is
merged baseline and must not be counted again as funded delta. Remaining separately
measurable work includes exact-vs-ANN evaluation, explicit cutover/fencing, rollback proof,
server lifecycle, production IdP/multi-tenancy, supply-chain hardening and a dedicated
Reader Core.

## 6. Documentation language and translation state

English is the primary working, source and conflict-resolving documentation language, but
Crystal is not an English-only documentation project.

- `README.md` is the primary full public presentation.
- `README.ru.md` is the first full visual and semantic translation phase.
- The other eight supported root README files remain temporary `ORIENTATION_ONLY` surfaces
  until their dedicated full-parity translation PRs.
- Existing translated Quick Start, Status, Reviewer Guide, Glossary and Grant Overview files
  are `REFRESH_NEEDED` until checked against a recorded English source checkpoint.
- Other stable documents are translated progressively by language or document family, not
  through one all-at-once final pass.

See [`../LOCALIZATION_POLICY.md`](../LOCALIZATION_POLICY.md) and
[`../TRANSLATION_STATUS.md`](../TRANSLATION_STATUS.md). Runtime or architecture PRs update
English first and record localization impact; substantial translation remains a separate
reviewable documentation change.
