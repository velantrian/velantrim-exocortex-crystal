# Crystal Current State

**Status date:** 2026-08-09  
**Verified runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6`  
**Validated runtime head / CI:** `d7af7c80722274f9217bc5545d150f92e9363f37` / `31256316536`  
**PostgreSQL integration:** `31256316532`  
**Version:** `0.3.0`

GitHub `main`, executable tests and completed CI are implementation truth. Notion stores
synchronized rationale and history; it does not override repository evidence.

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

Issue #332 is implemented by PR #337 for inactive import and exact equivalence only. The
target remains `active=false`, is absent from ordinary runtime composition and cannot serve
normal reads or writes. Import/equivalence does not establish activation, automatic selection,
cutover, rollback, dual-write, ANN acceptance, TruthGate admission or strict Canon membership.

## 3. Grant and remaining limitations

The project is submitted and under review; no award or budget change is claimed. PR #337 is
merged baseline and cannot be counted again as funded delta. Remaining independent work
includes exact-vs-ANN evaluation, cutover/fencing, rollback proof, PostgreSQL server lifecycle,
production IdP/multi-tenancy, supply-chain hardening and a dedicated Reader Core.

## 4. Documentation language and translation state

English is the primary working, source and conflict-resolving language. Translations are
maintained public product surfaces but create no independent implementation, security,
grant, TruthGate or Canon authority.

Issue #341 D1 is complete for Arabic, German, Spanish, French, Hindi, Italian, Japanese,
Russian and Simplified Chinese. Russian D1 is tied to
`main@16d71e731ee658b1faa65c9ea45c0d8cca290f7c`; the other eight locales are tied to
`main@a497b7d3cfbe59ca75b11d7449d5a728455b3130`.

D1 is current across all nine supported locale packs. D2 reviewer/safety translations are
also current across all nine supported locale packs against
`main@b7e6574dd7aefa2f32783ab79054fac6b3b4109f`.

The D1 validator checks 36 entry/use documents. The D2 validator checks 18 reviewer/safety
documents plus nine indexes, exact checkpoint, local links, read-only query, PostgreSQL
`active=false`, non-global erasure, security/legal/GDPR non-certification and NLnet-not-awarded
boundaries.

Architecture remains D3. PR #346 added compact English D3 summaries but changed only three
files and did not wire its validator into CI. The corrective D3 source reconciliation must
update the detailed architecture, durable profile, migration contracts and ADR-021, then run
the D3 validator in `docs-status` before any localized D3 document is marked `CURRENT`.

D3 translations remain `REFRESH_NEEDED` until that corrective English checkpoint is merged
and used as their exact source. Grant/project context remains D4; extended references D5.

See [`../TRANSLATION_STATUS.md`](../TRANSLATION_STATUS.md),
[`../LOCALIZATION_POLICY.md`](../LOCALIZATION_POLICY.md) and
[`../status/d2-translation-manifest.json`](../status/d2-translation-manifest.json).
