# 🧭 Crystal Documentation Map

This page routes each reader to the smallest reliable document and prevents duplicate
implementation claims.

## Start here by audience

| Audience | First document | Then read |
|---|---|---|
| New user | [README](../README.md) or a [full translation](./TRANSLATION_STATUS.md) | [Quick start](./QUICKSTART.md), [Architecture overview](./ARCHITECTURE_OVERVIEW.md) |
| Grant reviewer | [Reviewer guide](./REVIEWER_GUIDE.md) | [Test report](../TEST_REPORT.md), [Grant scope](./GRANT_NLNET_SCOPE.md) |
| Engineer | [Implementation status](./IMPLEMENTATION_STATUS.md) | [Full architecture](./ARCHITECTURE.md), [ADR index](./ADR.md), [Failure modes](./FAILURE_MODES.md) |
| Operator | [Quick start](./QUICKSTART.md) | [Storage and authority boundaries](./STORAGE_AND_AUTHORITY_BOUNDARIES.md), [Durable storage profile](./architecture/DURABLE_STORAGE_PROFILE.md) |
| Security reviewer | [Safety/privacy/failure summary](./SAFETY_PRIVACY_AND_FAILURES.md) | [Security policy](../SECURITY.md), [Threat model](./security/threat-model.md), [Privacy](../PRIVACY.md) |
| Contributor | [Contributing](../CONTRIBUTING.md) | [Sync protocol](./DOCUMENTATION_SYNC_PROTOCOL.md), [Localization policy](./LOCALIZATION_POLICY.md), [Translation status](./TRANSLATION_STATUS.md) |
| AI agent | [AI entry point](./ai/README.md) | [Agent contract](../AGENTS.md), [Current state](./ai/CURRENT_STATE.md), [Audit playbook](./ai/AUDIT_PLAYBOOK.md) |

## Authority hierarchy

```text
merged GitHub main code and executable tests
        ↓
TEST_REPORT.md + implementation manifest + exact CI
        ↓
STATUS + IMPLEMENTATION_STATUS
        ↓
English architecture / ADR / security / grant contracts
        ↓
English README primary public source
        ↓
CURRENT full-parity localized READMEs and checkpointed D1/D2/D3 translations
        ↓
REFRESH_NEEDED translated document packs for D4–D5
        ↓
AI context pack, roadmap, RFC and research documents
```

English is the primary source and conflict resolver, but Crystal is not English-only. Root
READMEs, D1 entry/use, D2 reviewer/safety and D3 architecture/storage-authority surfaces are
current for all nine supported locales. Notion stores synchronized strategy and history, not
runtime proof.

## Core architecture and trust

- [Architecture overview](./ARCHITECTURE_OVERVIEW.md)
- [Full architecture](./ARCHITECTURE.md)
- [Storage and authority boundaries](./STORAGE_AND_AUTHORITY_BOUNDARIES.md)
- [Implementation status](./IMPLEMENTATION_STATUS.md)
- [Read-only query boundary](./architecture/read-only-query-boundary.md)
- [Conflict-resolution surfaces](./CONFLICT_RESOLUTION_SURFACES.md)
- [Topic facets and curator IAM](./TOPIC_FACETS_AND_CURATOR_IAM.md)
- [Ring Zero mutation gate](./testing/RING_ZERO_MUTATION_GATE.md)
- [CanonicalView RFC](./CANONICAL_VIEW_RFC.md)
- [ADR index](./ADR.md)

D3 uses the complete stable English architecture source family. The compact Architecture
Overview and Storage/Authority Boundaries are current in all nine locales; detailed profiles,
migration contracts and ADRs remain conflict-resolving English technical contracts.

## Safety, privacy and failure behaviour

- [Reviewer guide](./REVIEWER_GUIDE.md)
- [Safety/privacy/failure summary](./SAFETY_PRIVACY_AND_FAILURES.md)
- [Security policy](../SECURITY.md)
- [Threat model](./security/threat-model.md)
- [Privacy](../PRIVACY.md)
- [GDPR mapping](../GDPR.md)
- [Failure modes](./FAILURE_MODES.md)

D2 uses the stable English Reviewer Guide and Safety/Privacy/Failure summary as its source
contract. Current D2 translations exist for all nine supported locales and link to the
detailed English Security, Privacy, GDPR and Failure Modes contracts.

## Evidence and performance

- [Test report](../TEST_REPORT.md)
- [Current status](./STATUS.md)
- [Implementation manifest](./status/implementation-manifest.json)
- [D2 translation manifest](./status/d2-translation-manifest.json)
- [D3 translation manifest](./status/d3-translation-manifest.json)
- [Evaluation](./EVAL.md)
- [L3 retrieval benchmark](./benchmarks/L3_RETRIEVAL_SCALE.md)

## Grant boundary

- [NLnet scope](./GRANT_NLNET_SCOPE.md)
- [Baseline versus funded delta](./grants/baseline-funded-delta-matrix.md)
- [Funding use plan](./grants/funding-use-plan.md)

The proposal remains submitted and under review, not awarded. Merged baseline work cannot be
budgeted again as future delivery.

## Translation program

- [Localization policy](./LOCALIZATION_POLICY.md)
- [Translation status ledger](./TRANSLATION_STATUS.md)
- locale indexes: [ar](./ar/README.md), [de](./de/README.md), [es](./es/README.md), [fr](./fr/README.md), [hi](./hi/README.md), [it](./it/README.md), [ja](./ja/README.md), [ru](./ru/README.md), [zh-CN](./zh-CN/README.md)

Root READMEs, D1, D2 and D3 are current. D4–D5 remain separate phases with
`REFRESH_NEEDED translated document packs` until independently reconciled.

## Active storage and migration documents

- [Durable storage profile](./architecture/DURABLE_STORAGE_PROFILE.md)
- [SQLite storage lifecycle](./architecture/SQLITE_STORAGE_LIFECYCLE.md)
- [SQLite logical export](./architecture/SQLITE_LOGICAL_EXPORT.md)
- [Cross-backend migration contract](./architecture/CROSS_BACKEND_MIGRATION_CONTRACT.md)
- [Inactive PostgreSQL import](./architecture/POSTGRESQL_INACTIVE_IMPORT.md)
- [PostgreSQL/pgvector profile RFC](./architecture/POSTGRESQL_PGVECTOR_PROFILE_RFC.md)
- [ADR-021](./adr/ADR-021-CROSS-BACKEND-MIGRATION-CONTRACT.md)

SQLite remains the ordinary local-first read/write profile. PostgreSQL/pgvector remains an
optional inactive exact-equivalence target with `active=false`, not an ordinary runtime
backend. Successful import is not activation, Canon admission, cutover, rollback or dual-write.
