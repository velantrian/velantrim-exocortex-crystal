# Crystal Documentation Map

**Status date:** 2026-08-11

GitHub merged `main` + executable tests + exact CI are implementation truth. Use this page to find the current contract for each surface.

## Reader

- [Reader Core architecture contract](./architecture/READER_CORE_ARCHITECTURE.md) — RC-0 normative authority/fidelity/coverage/privacy contract.
- [Implementation status](./IMPLEMENTATION_STATUS.md) — RC-1 through RC-5 machine-facing capability boundary.
- [Architecture overview](./ARCHITECTURE_OVERVIEW.md) — stable D3 Reader/storage/trust overview.
- [Current status](./STATUS.md) — current public implementation truth and non-claims.

```text
RC-1 exact source/session
→ RC-2 structural map
→ RC-3 explicit passes
→ RC-4 proposition candidates
→ RC-5 relation candidates
→ normal admission remains separate
```

## Reviewer / safety / privacy — D2

D2 uses the stable English Reviewer Guide and safety/privacy/failure source contract. RC-5 changes Reader candidate semantics but does not change D2 reviewer/safety source semantics, so the existing nine-locale D2 translations remain current.

- [Reviewer Guide](./REVIEWER_GUIDE.md)
- [Safety, privacy and failures](./SAFETY_PRIVACY_AND_FAILURES.md)
- [Privacy](../PRIVACY.md)
- [Security](../SECURITY.md)

## Storage / authority

- [Storage and authority boundaries](./STORAGE_AND_AUTHORITY_BOUNDARIES.md)
- [SQLite storage lifecycle](./architecture/SQLITE_STORAGE_LIFECYCLE.md)
- [Inactive PostgreSQL import](./architecture/POSTGRESQL_INACTIVE_IMPORT.md)
- [PostgreSQL/pgvector profile RFC](./architecture/POSTGRESQL_PGVECTOR_PROFILE_RFC.md)

## Grant / governance — D4

Grant truth remains **submitted / under review / not awarded**, budget change none.

- [Project, grant and governance overview](./PROJECT_GRANT_AND_GOVERNANCE.md)
- [Grant scope](./GRANT_NLNET_SCOPE.md)
- [Baseline-funded delta matrix](./grants/baseline-funded-delta-matrix.md)
- [Roadmap](../ROADMAP.md)
- [Glossary](./GLOSSARY.md)

## Localization / reference — D5

- [Localization policy](./LOCALIZATION_POLICY.md)
- [Translation status](./TRANSLATION_STATUS.md)
- [Extended reference policy](./EXTENDED_REFERENCE_POLICY.md)
- [D5 inventory](./status/d5-inventory.json)

Russian is the current Reader secondary surface for the RC-5 source checkpoint. Eight other Reader-dependent locale surfaces remain `REFRESH_NEEDED`; D2 and Quick Start remain current.
