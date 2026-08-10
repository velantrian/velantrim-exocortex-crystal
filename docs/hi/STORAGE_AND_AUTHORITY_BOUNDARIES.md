<!-- translation-source: docs/STORAGE_AND_AUTHORITY_BOUNDARIES.md@208f1c772ee3a112cb803d2413c120bef23adb05 -->
<!-- translation-status: CURRENT -->
<!-- d3-locale: hi -->
<!-- d3-boundary: physical-l3-not-strict-canon -->
<!-- d3-boundary: public-query-read-only -->
<!-- d3-boundary: postgresql-active=false -->
<!-- d3-nonclaim: import-is-not-activation -->
<!-- d3-nonclaim: reader-core-not-implemented -->
<!-- d3-nonclaim: nlnet-not-awarded -->
# Storage और Authority सीमाएँ

## अलग identities

```text
storage profile = deployment identity
physical L3 = multi-status graph state
strict Canon = trusted read projection
migration bundle = operation-integrity evidence
retrieval score = ranking signal
model output = generated text
```

इनमें से कोई identity दूसरी की authority स्वतः नहीं देती।

## durable profile

SQLite सामान्य active local-first profile है। पहला durable `auto` optional LadybugDB या SQLite चुन सकता है और backend तथा non-secret locator lock करता है। बाद के conflicts fail-closed होते हैं। Mock केवल explicit development/CI state है।

## physical L3 बनाम strict Canon

physical L3 में VERIFIED, USER_CLAIMED, UNVERIFIED, HYPOTHESIS, SUBJECTIVE, contested, superseded या restricted records हो सकते हैं। strict Canon current evidence और policy पर आधारित deny-dominant projection है। Storage, retrieval या high score पर्याप्त नहीं हैं।

## पढ़ना और लिखना

Public queries `core.query_pipeline.query()` से read-only गुजरती हैं। Explicit `ingest` admission-capable write path है; Guardian और TruthGate structural तथा epistemic boundaries लागू करते हैं।

## SQLite lifecycle और migration

Backup, independent verification, inactive restore, bounded deterministic logical export और bundle verification implemented हैं। Approved physical-L3 datasets को नए inactive PostgreSQL schema में import कर exact तुलना की जा सकती है; target `active=false` रहता है।

यह पूरे L1, audit/outbox, encryption metadata, configuration या independent copies की whole-system migration नहीं है। Active PostgreSQL runtime, ANN acceptance, automatic switching, cutover, fencing, rollback और dual-write अनुपस्थित हैं।

## secrets और copies

Passwords, tokens, private keys और credential-bearing DSNs profiles, bundles, receipts, logs, GitHub या Notion में नहीं जाने चाहिए। Backups, exports और migrations अतिरिक्त copies बनाते हैं; active store से deletion उन्हें स्वतः नहीं मिटाता। Selected L1 field encryption universal encryption नहीं है।

## operation evidence

| घटना | क्या सिद्ध करती है | क्या सिद्ध नहीं करती |
|---|---|---|
| L3 record | physical persistence | strict Canon membership |
| retrieval result | candidate relevance | पर्याप्त evidence |
| verified backup | backup integrity | claim truth |
| successful import | import integrity | activation या runtime selection |
| exact equivalence | approved datasets की समानता | production readiness या cutover |

Dedicated Reader Core implemented नहीं है; NLnet submitted / under review / not awarded है।

## विस्तृत अंग्रेज़ी contracts

- [पूर्ण Architecture](../ARCHITECTURE.md)
- [Durable Storage Profile](../architecture/DURABLE_STORAGE_PROFILE.md)
- [Migration Contract](../architecture/CROSS_BACKEND_MIGRATION_CONTRACT.md)
- [Inactive PostgreSQL Import](../architecture/POSTGRESQL_INACTIVE_IMPORT.md)
- [ADR-021](../adr/ADR-021-CROSS-BACKEND-MIGRATION-CONTRACT.md)
