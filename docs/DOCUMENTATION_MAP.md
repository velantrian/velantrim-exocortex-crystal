# 🧭 Crystal Documentation Map

This page routes each reader to the smallest reliable document and prevents duplicate
implementation claims.

## Start here by audience

| Audience | First document | Then read |
|---|---|---|
| New user | [English README](../README.md) or a [tracked translation](./TRANSLATION_STATUS.md) | [Quick start](./QUICKSTART.md), [Architecture](./ARCHITECTURE.md) |
| Grant reviewer | [Reviewer guide](./REVIEWER_GUIDE.md) | [Test report](../TEST_REPORT.md), [Grant scope](./GRANT_NLNET_SCOPE.md) |
| Engineer | [Implementation status](./IMPLEMENTATION_STATUS.md) | [ADR index](./ADR.md), [Failure modes](./FAILURE_MODES.md) |
| Operator | [Quick start](./QUICKSTART.md) | [Conflict-resolution surfaces](./CONFLICT_RESOLUTION_SURFACES.md), [Topic facets and curator IAM](./TOPIC_FACETS_AND_CURATOR_IAM.md) |
| Security reviewer | [Security policy](../SECURITY.md) | [Threat model](./security/threat-model.md), [Privacy](../PRIVACY.md) |
| Researcher | [Implementation status](./IMPLEMENTATION_STATUS.md) | [Roadmap](../ROADMAP.md), RFCs, [Metaphor vs mechanism](./METAPHOR_VS_MECHANISM.md) |
| Ecosystem reviewer | [Velantrim ecosystem map](./VELANTRIM_ECOSYSTEM.md) | [Grant scope](./GRANT_NLNET_SCOPE.md), [Architecture](./ARCHITECTURE.md) |
| Contributor | [Contributing](../CONTRIBUTING.md) | [Documentation sync protocol](./DOCUMENTATION_SYNC_PROTOCOL.md), [Localization policy](./LOCALIZATION_POLICY.md), [Translation status](./TRANSLATION_STATUS.md), [Governance](../GOVERNANCE.md) |
| AI coding agent or automated auditor | [AI agent entry point](./ai/README.md) | [Mandatory agent contract](../AGENTS.md), [Current state](./ai/CURRENT_STATE.md), [Audit playbook](./ai/AUDIT_PLAYBOOK.md) |
| AI without Notion connector | [Connectorless Notion hand-off](./ai/NOTION_HANDOFF.md) | [Work log](./ai/WORK_LOG.md), [Sync protocol](./DOCUMENTATION_SYNC_PROTOCOL.md) |

## Authority hierarchy

```text
merged GitHub main code and executable tests
        ↓
TEST_REPORT.md + implementation-manifest.json + exact CI
        ↓
docs/STATUS.md + docs/IMPLEMENTATION_STATUS.md
        ↓
English architecture / ADR / security / grant contracts
        ↓
English README primary public source
        ↓
CURRENT full-parity localized READMEs
        ↓
ORIENTATION_ONLY / REFRESH_NEEDED translations with explicit status
        ↓
AI context pack, RFCs, roadmap and research documents
```

English is the primary working and conflict-resolving source language. That does not make
Crystal an English-only documentation project. Completed root README translations are full
public presentations of the same project, and the broader document corpus is translated in
separate phases. When a translation disagrees with current code, tests or English evidence,
the current implementation evidence wins until the translation is reconciled.

Notion is the synchronized strategy, rationale and grant-history map. It does not replace
merged code or exact CI as implementation truth.

## Velantrim ecosystem and cross-project boundaries

- [Bilingual Velantrim ecosystem map](./VELANTRIM_ECOSYSTEM.md)
- [Architecture and authority boundaries](./ARCHITECTURE.md)
- [NLnet grant scope](./GRANT_NLNET_SCOPE.md)

Crystal is the independent grant-facing verifiable-memory track. Titan, Native Kernel and
Mentaury Soul are related Velantrim research projects, but they do not receive automatic
write authority over Crystal, do not share one Canon by default, and are not current runtime
dependencies unless a separately reviewed integration is implemented, tested and merged.

The ecosystem map is bilingual in English and Russian. Additional README and documentation
translations follow the same source-first, phased process described below; translation does
not authorize runtime integration.

## AI agent context and hand-off

- [AI agent entry point](./ai/README.md)
- [Current state](./ai/CURRENT_STATE.md)
- [Component map](./ai/COMPONENT_MAP.md)
- [Known risks](./ai/KNOWN_RISKS.md)
- [Audit playbook](./ai/AUDIT_PLAYBOOK.md)
- [Compact work log](./ai/WORK_LOG.md)
- [Connectorless Notion hand-off queue](./ai/NOTION_HANDOFF.md)

The AI pack reduces context pressure and points agents to the right authority owner, files,
consumers, tests and risks. It is an orientation map, not a competing source of implementation
truth.

Not all AI agents have direct Notion access. GitHub therefore contains the complete public
technical and audit context required to continue the work. A connectorless agent records
`HANDOFF_REQUIRED`; a connected human or AI later updates Notion and marks the item `SYNCED`.

## Change and documentation governance

- [Code ↔ Documentation ↔ Notion synchronization protocol](./DOCUMENTATION_SYNC_PROTOCOL.md)
- [Localization and translation policy](./LOCALIZATION_POLICY.md)
- [Translation status and phased rollout](./TRANSLATION_STATUS.md)
- [Connectorless Notion hand-off](./ai/NOTION_HANDOFF.md)
- [Contributing guide](../CONTRIBUTING.md)
- [Governance](../GOVERNANCE.md)
- [ADR index](./ADR.md)

Every PR classifies its documentation impact as `NONE`, `GITHUB_ONLY`, or
`GITHUB_AND_NOTION`. New technologies, functions, durable decisions, authority/privacy
boundaries, grant/roadmap changes and cross-project decisions require a synchronized Notion
record in addition to the public GitHub technical contract.

When the originating agent lacks a Notion connector, it must still complete the GitHub record
and create a structured hand-off. A missing connector is `HANDOFF_REQUIRED`, not a reason to
lose analysis. Essential implementation, risk and audit information must never exist only in
Notion.

## Core architecture and trust

- [Architecture](./ARCHITECTURE.md)
- [Implementation status](./IMPLEMENTATION_STATUS.md)
- [Read-only query boundary](./architecture/read-only-query-boundary.md)
- [Conflict-resolution surfaces](./CONFLICT_RESOLUTION_SURFACES.md)
- [Topic facets and curator IAM](./TOPIC_FACETS_AND_CURATOR_IAM.md)
- [Ring Zero mutation gate](./testing/RING_ZERO_MUTATION_GATE.md)
- [CanonicalView RFC](./CANONICAL_VIEW_RFC.md)
- [ADR index](./ADR.md)

## Evidence, state and performance

- [Test report](../TEST_REPORT.md)
- [Current status](./STATUS.md)
- [Implementation manifest](./status/implementation-manifest.json)
- [Evaluation](./EVAL.md)
- [Failure modes](./FAILURE_MODES.md)
- [L3 retrieval benchmark](./benchmarks/L3_RETRIEVAL_SCALE.md)

The ESM runtime has one machine-readable specification derived from the shared transition
matrix. Performance history uses versioned scheduled/manual artifacts and comparable-run
reporting; shared PR-runner latency is not a hard SLO.

## Grant boundary

- [NLnet scope](./GRANT_NLNET_SCOPE.md)
- [Baseline versus funded delta](./grants/baseline-funded-delta-matrix.md)
- [Funding use plan](./grants/funding-use-plan.md)

The proposal remains submitted and under review, not awarded. Merged baseline work cannot be
promised or budgeted again as future funded delivery.

## Completed hardening workstream

The documentation/read-only/trust hardening sequence through the current verified baseline
includes read-only queries, non-configurable TruthGate policy, immutable snapshots, mutation
testing, contradiction decisions, ESM specification, performance history, public conflict
surfaces, advisory topic facets, scoped curator authorization, process-local decision leases,
SQLite lifecycle/migration proof and optional inactive PostgreSQL exact-equivalence import.

## Independent future roadmap

Future packages include exact-vs-ANN evaluation, explicit cutover and fencing, rollback proof,
PostgreSQL server lifecycle/operational security, an external distributed lease adapter,
production identity-provider and multi-tenant policy integration, broader provenance lifecycle
wiring, controlled performance SLOs, wider mutation coverage, a separately reviewed
long-document semantic reading layer and separate Titan research.

## Translation policy

- [Localization policy](./LOCALIZATION_POLICY.md)
- [Translation status ledger](./TRANSLATION_STATUS.md)
- [Russian documentation index](./ru/README.md)
- [German documentation index](./de/README.md)
- [French documentation index](./fr/README.md)
- [Spanish documentation index](./es/README.md)
- [Italian documentation index](./it/README.md)
- [Simplified Chinese documentation index](./zh-CN/README.md)
- [Japanese documentation index](./ja/README.md)
- [Hindi documentation index](./hi/README.md)
- [Arabic documentation index](./ar/README.md)

English-first means source-first, not English-only. The target for every supported root README
is full visual and semantic parity with `README.md`: purpose, mind maps, ASCII diagrams,
tables, evidence, limitations, quick start and navigation. Other stable documents are
translated progressively by language or document family. No implementation PR is blocked
until all languages are updated, and no temporary `ORIENTATION_ONLY` file is treated as the
final target.

`docs-status` verifies objective invariants: supported files/indexes, the translation ledger,
English/Russian full-presentation markers for the current phase, source checkpoints, current
capability/non-claim boundaries and local links. Human or language-model review is still
required for natural language and semantic fidelity.

## Active storage and migration documents

- [Durable storage profile](./architecture/DURABLE_STORAGE_PROFILE.md)
- [SQLite storage lifecycle](./architecture/SQLITE_STORAGE_LIFECYCLE.md)
- [SQLite logical export and independent verification](./architecture/SQLITE_LOGICAL_EXPORT.md)
- [Cross-backend migration contract](./architecture/CROSS_BACKEND_MIGRATION_CONTRACT.md)
- [Inactive PostgreSQL import](./architecture/POSTGRESQL_INACTIVE_IMPORT.md)
- [PostgreSQL + pgvector institutional profile RFC](./architecture/POSTGRESQL_PGVECTOR_PROFILE_RFC.md)
- [ADR-021: cross-backend storage migration](./adr/ADR-021-cross-backend-storage-migration.md)

SQLite remains the ordinary local-first read/write profile. PostgreSQL/pgvector is an optional,
lazy-loaded inactive import and exact-equivalence target with `active=false`; it is not an
ordinary runtime read/write backend. Import success is not activation, TruthGate admission,
strict Canon membership, ANN acceptance, cutover, rollback or dual-write.
