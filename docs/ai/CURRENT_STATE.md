# Crystal Current State

**Status date:** 2026-08-09  
**Verified runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6`  
**Validated runtime head / CI:** `d7af7c80722274f9217bc5545d150f92e9363f37` / `31256316536`  
**Version:** `0.3.0`

GitHub `main`, executable tests and completed CI are implementation truth. Notion stores synchronized rationale and history; it does not override repository evidence.

## 1. Verified runtime evidence

- Python 3.11 and 3.12: **2078 passed / 13 skipped / 0 failed**;
- **9756 statements / 100.00% coverage**;
- PostgreSQL migration modules: **44/44 + 336/336 statements**;
- **7/7** Ring Zero mutants killed;
- **9/9** permanent CI jobs successful;
- **1/1** real PostgreSQL/pgvector integration job successful.

## 2. Current storage and migration capability

SQLite remains the ordinary active local-first profile. PostgreSQL remains `active=false`, absent from ordinary runtime composition and unable to serve normal reads or writes. Import/equivalence does not establish activation, automatic selection, cutover, rollback, dual-write, TruthGate admission or strict Canon membership.

## 3. Grant and remaining limitations

The NLnet proposal is submitted / under review / not awarded. Approximate €50,000 is planning only, not an approved budget or payment commitment. Budget change is none. Work merged before an agreement is existing baseline and cannot be counted again as funded delta. Reader Core is not implemented. No legal, GDPR, security or native-speaker editorial certification is claimed.

## 4. Documentation language and D1–D3

English is the primary working, source and conflict-resolving language. Translations create no independent implementation, security, grant, TruthGate or Canon authority.

Issue #341 D1 is complete for all nine supported locales. Russian D1 is tied to `main@16d71e731ee658b1faa65c9ea45c0d8cca290f7c`; the other eight locales are tied to `main@a497b7d3cfbe59ca75b11d7449d5a728455b3130`.

D1 is current across all nine supported locale packs. D2 reviewer/safety translations are current against `main@b7e6574dd7aefa2f32783ab79054fac6b3b4109f`. The D2 English source family is reconciled.

**D3 English source checkpoint:** `main@208f1c772ee3a112cb803d2413c120bef23adb05`. The complete D3 source validator covers the stable architecture/storage authority family. D3 is current across all nine supported locale packs. The D3 validator covers **18 architecture/storage documents plus nine indexes**.

## 5. D4 state

The D4 English source family is reconciled at `main@151b41c680190f7f3de729bf63e8e80a9d2285ce` across `docs/PROJECT_GRANT_AND_GOVERNANCE.md`, `docs/GLOSSARY.md`, `docs/GRANT_NLNET_SCOPE.md`, `ROADMAP.md`, `GOVERNANCE.md`, `CONTRIBUTING.md` and grant evidence routing.

D4 is current across all nine supported locale packs. The D4 validator covers **18 project/grant/glossary documents plus nine indexes**, exact source checkpoint, local links and all mandatory capability, authority, grant and certification non-claims.

D1–D4 remain current multilingual public surfaces while D5 adds the extended-reference routing layer.

## 6. D5 completed state

D5 source inventory/policy is anchored to signed `main@d5f7f1c4c0908d24f8994e4fbec45c102b9ab7d9`. D5 is current across all nine supported locale packs through **nine Extended Reference Guides** and nine synchronized indexes.

The D5 source validator classifies the live corpus as `CURRENT`, `REFRESH_NEEDED`, `RETIRED` or `ENGLISH_ONLY_BY_DESIGN`; the final localized phase adds the guides as current and leaves zero unresolved `REFRESH_NEEDED` documents. Detailed ADR/profile contracts, security/privacy/GDPR/legal mapping, tests/benchmarks/CI, machine-readable status, AI/audit/archive context, research/RFC and grant evidence are not bulk translated. Historical snapshots remain preserved with retirement routing.

D1–D5 are current multilingual public surfaces for all nine supported locales.

See [`../TRANSLATION_STATUS.md`](../TRANSLATION_STATUS.md), [`../LOCALIZATION_POLICY.md`](../LOCALIZATION_POLICY.md), [`../EXTENDED_REFERENCE_POLICY.md`](../EXTENDED_REFERENCE_POLICY.md), [`../status/d4-translation-manifest.json`](../status/d4-translation-manifest.json), [`../status/d5-inventory.json`](../status/d5-inventory.json) and [`../status/d5-translation-manifest.json`](../status/d5-translation-manifest.json).
