<!-- translation-source: docs/IMPLEMENTATION_STATUS.md@a497b7d3cfbe59ca75b11d7449d5a728455b3130 -->
<!-- translation-status: CURRENT -->
<!-- d1-locale: hi -->
<!-- d1-boundary: public-ask-read-only -->
<!-- d1-boundary: postgresql-active=false -->
<!-- d1-nonclaim: import-is-not-activation -->
<!-- d1-nonclaim: nlnet-not-awarded -->
# Implementation स्थिति: Crystal और भविष्य का कार्य

**तारीख:** 2026-08-08  
**Checkpoint:** `bbd816c` / PR #337  
**Evidence:** [TEST_REPORT.md](../../TEST_REPORT.md)  
**Machine-readable status:** [manifest](../status/implementation-manifest.json)

| Component | स्थिति | वर्तमान सीमा |
|---|---|---|
| Guardian / TruthGate / strict read projection | लागू | storage और migration authority bypass नहीं करते |
| HTTP/CLI/MCP query boundary | लागू | ordinary queries Canon mutate नहीं करतीं |
| SQLite backup/verify/inactive restore | लागू व tested | restore inactive, admission नहीं |
| Bounded SQLite logical export | लागू व tested | canonical backend-neutral bundle |
| PostgreSQL optional dependency/preflight | लागू व tested | explicit extra, lazy load |
| Inactive PostgreSQL/pgvector import | लागू व tested | नया inactive schema, सामान्य I/O नहीं |
| Exact target-state equivalence | लागू व tested | independent read-only re-hash |
| Active PostgreSQL runtime adapter | लागू नहीं | normal composition में target नहीं |
| Automatic SQLite/PostgreSQL switching | निषिद्ध | availability/import success चयन नहीं |
| Exact-vs-ANN evaluation | लागू नहीं | अलग बाद की phase |
| Cutover / rollback / dual-write | लागू नहीं | explicit future phases |
| PostgreSQL server lifecycle | लागू नहीं | backup/restore/upgrade/pooling future |
| Reader Core / Semantic Reading Layer | लागू नहीं | admission से पहले candidate layer |

```text
SQLite lifecycle
→ backup / independent verify / inactive restore

logical portability
→ bounded canonical bundle
→ PostgreSQL preflight
→ inactive transactional import
→ independent exact-state equivalence
→ non-secret receipts
```

Issues #331 और #332 PR #335 तथा #337 से लागू हैं। PostgreSQL `active=false` वाला optional
operator path है। Successful equivalence backend activate नहीं कर सकती और Guardian,
TruthGate या strict Canon को नहीं बदलती।

Future work:

```text
exact-vs-ANN retrieval evaluation
→ explicit cutover and source/target fencing
→ rollback proof and expiry policy
→ PostgreSQL backup/restore/upgrade lifecycle
→ multi-process concurrency and production observability
```

Crystal active PostgreSQL backend, automatic migration, production multi-tenancy,
universal truth, zero hallucinations, legal/security certification या consciousness का
दावा नहीं करता।
