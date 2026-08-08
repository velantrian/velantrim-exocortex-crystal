# 🧭 Crystal Documentation Map

This page routes each reader to the smallest authoritative document and prevents duplicate or
translated implementation claims.

## Start here by audience

| Audience | First document | Then read |
|---|---|---|
| New user | [README](../README.md) | [Quick start](./QUICKSTART.md), [Architecture](./ARCHITECTURE.md) |
| Grant reviewer | [Reviewer guide](./REVIEWER_GUIDE.md) | [Test report](../TEST_REPORT.md), [Grant scope](./GRANT_NLNET_SCOPE.md) |
| Engineer | [Implementation status](./IMPLEMENTATION_STATUS.md) | [ADR index](./ADR.md), [Failure modes](./FAILURE_MODES.md) |
| Operator | [Quick start](./QUICKSTART.md) | [Conflict-resolution surfaces](./CONFLICT_RESOLUTION_SURFACES.md) |
| Security reviewer | [Security policy](../SECURITY.md) | [Threat model](./security/threat-model.md), [Privacy](../PRIVACY.md) |
| Researcher | [Implementation status](./IMPLEMENTATION_STATUS.md) | [Roadmap](../ROADMAP.md), RFCs |
| Contributor | [Contributing](../CONTRIBUTING.md) | [Sync protocol](./DOCUMENTATION_SYNC_PROTOCOL.md), [Localization policy](./LOCALIZATION_POLICY.md) |
| AI agent | [AI entry point](./ai/README.md) | [Agent contract](../AGENTS.md), [Current state](./ai/CURRENT_STATE.md) |

## Authority hierarchy

```text
merged GitHub main code and tests
        ↓
TEST_REPORT.md + implementation-manifest.json
        ↓
docs/STATUS.md + docs/IMPLEMENTATION_STATUS.md
        ↓
English architecture / ADR / security / grant contracts
        ↓
English README public capability summary
        ↓
localized README orientation summaries
        ↓
locale indexes and optional best-effort snapshots
```

Localized text is never implementation truth. Notion is synchronized strategy, rationale,
grant context and history; it does not replace merged GitHub evidence.

## English-first documentation governance

- [Localization policy](./LOCALIZATION_POLICY.md)
- [Code ↔ Documentation ↔ Notion synchronization protocol](./DOCUMENTATION_SYNC_PROTOCOL.md)
- [Connectorless Notion hand-off](./ai/NOTION_HANDOFF.md)
- [Mandatory agent contract](../AGENTS.md)

English is the sole authoritative working language. Architecture, ADRs, status, tests,
security, grant documents, roadmaps and `docs/ai/*` are maintained in English. The project
does not translate the entire corpus.

The nine `README.<locale>.md` files are concise non-authoritative summaries. Their associated
`docs/<locale>/README.md` files explain the locale route and identify older translated files as
best-effort snapshots that may lag. `docs-status` verifies source checkpoints, capability
boundaries, size limits and local links.

## Core architecture and trust

- [Architecture](./ARCHITECTURE.md)
- [Implementation status](./IMPLEMENTATION_STATUS.md)
- [Read-only query boundary](./architecture/read-only-query-boundary.md)
- [Conflict-resolution surfaces](./CONFLICT_RESOLUTION_SURFACES.md)
- [Topic facets and curator IAM](./TOPIC_FACETS_AND_CURATOR_IAM.md)
- [Ring Zero mutation gate](./testing/RING_ZERO_MUTATION_GATE.md)
- [CanonicalView RFC](./CANONICAL_VIEW_RFC.md)
- [ADR index](./ADR.md)

## Evidence and current state

- [Test report](../TEST_REPORT.md)
- [Current status](./STATUS.md)
- [Implementation manifest](./status/implementation-manifest.json)
- [Evaluation](./EVAL.md)
- [Failure modes](./FAILURE_MODES.md)
- [Current AI context](./ai/CURRENT_STATE.md)
- [Known risks](./ai/KNOWN_RISKS.md)

## Storage and migration

- [Durable storage profile](./architecture/DURABLE_STORAGE_PROFILE.md)
- [SQLite storage lifecycle](./architecture/SQLITE_STORAGE_LIFECYCLE.md)
- [SQLite logical export](./architecture/SQLITE_LOGICAL_EXPORT.md)
- [Cross-backend migration contract](./architecture/CROSS_BACKEND_MIGRATION_CONTRACT.md)
- [Inactive PostgreSQL import contract](./architecture/POSTGRESQL_INACTIVE_IMPORT.md)
- [PostgreSQL + pgvector profile RFC](./architecture/POSTGRESQL_PGVECTOR_PROFILE_RFC.md)
- [ADR-021](./adr/ADR-021-CROSS-BACKEND-MIGRATION-CONTRACT.md)

SQLite remains the ordinary local-first profile. PostgreSQL/pgvector is currently an optional,
lazy-loaded inactive import and exact-equivalence target; it is not an active read/write backend.

## Grant boundary

- [NLnet scope](./GRANT_NLNET_SCOPE.md)
- [Baseline versus funded delta](./grants/baseline-funded-delta-matrix.md)
- [Funding use plan](./grants/funding-use-plan.md)

The proposal remains submitted and under review. No award or budget change is claimed.
