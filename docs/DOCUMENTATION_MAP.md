# 🧭 Crystal Documentation Map

This page routes readers to the smallest reliable document and prevents duplicate claims.

## Authority hierarchy

```text
merged GitHub main code and executable tests
        ↓
TEST_REPORT + implementation manifest + exact CI
        ↓
STATUS + IMPLEMENTATION_STATUS
        ↓
English architecture / ADR / security / grant / governance contracts
        ↓
English README primary public source
        ↓
CURRENT full-parity localized READMEs and D1–D5 translations
        ↓
D5 inventory: CURRENT / REFRESH_NEEDED / RETIRED / ENGLISH_ONLY_BY_DESIGN
        ↓
AI context, roadmap, RFC and research material
```

English is the primary source and conflict resolver. Notion stores synchronized strategy and history, not implementation evidence.

## Start here by audience

| Audience | First document | Then read |
|---|---|---|
| New user | [README](../README.md) or [translation status](./TRANSLATION_STATUS.md) | [Quick start](./QUICKSTART.md), [Architecture overview](./ARCHITECTURE_OVERVIEW.md) |
| Grant reviewer | [Project/grant/governance overview](./PROJECT_GRANT_AND_GOVERNANCE.md) | [Grant scope](./GRANT_NLNET_SCOPE.md), [baseline/delta matrix](./grants/baseline-funded-delta-matrix.md) |
| Engineer | [Implementation status](./IMPLEMENTATION_STATUS.md) | [Architecture](./ARCHITECTURE.md), [ADR index](./ADR.md) |
| Security reviewer | [Safety/privacy/failure summary](./SAFETY_PRIVACY_AND_FAILURES.md) | [Security](../SECURITY.md), [Privacy](../PRIVACY.md), [GDPR mapping](../GDPR.md) |
| Contributor | [Contributing](../CONTRIBUTING.md) | [Governance](../GOVERNANCE.md), [Glossary](./GLOSSARY.md) |
| AI agent | [AI entry point](./ai/README.md) | [Current state](./ai/CURRENT_STATE.md), [Audit playbook](./ai/AUDIT_PLAYBOOK.md) |

## Architecture and storage authority

- [Architecture overview](./ARCHITECTURE_OVERVIEW.md)
- [Full architecture](./ARCHITECTURE.md)
- [Storage and authority boundaries](./STORAGE_AND_AUTHORITY_BOUNDARIES.md)
- [Implementation status](./IMPLEMENTATION_STATUS.md)
- [Durable storage profile](./architecture/DURABLE_STORAGE_PROFILE.md)
- [Cross-backend migration contract](./architecture/CROSS_BACKEND_MIGRATION_CONTRACT.md)
- [Inactive PostgreSQL import](./architecture/POSTGRESQL_INACTIVE_IMPORT.md)
- [ADR-021](./adr/ADR-021-CROSS-BACKEND-MIGRATION-CONTRACT.md)

D3 uses the complete stable English architecture source family. Compact architecture/storage documents are current across all nine locales. Detailed profiles and ADRs remain conflict-resolving English technical contracts.

## Safety, privacy and failure behaviour

- [Reviewer guide](./REVIEWER_GUIDE.md)
- [Safety/privacy/failure summary](./SAFETY_PRIVACY_AND_FAILURES.md)
- [Security policy](../SECURITY.md)
- [Threat model](./security/threat-model.md)
- [Privacy](../PRIVACY.md)
- [GDPR mapping](../GDPR.md)
- [Failure modes](./FAILURE_MODES.md)

D2 uses the stable English Reviewer Guide and Safety/Privacy/Failure summary as its source contract. D2 compact reviewer/safety documents are current across all nine locales. No legal, GDPR or security certification is implied.

## Project, grant and governance

- [Project, grant and governance overview](./PROJECT_GRANT_AND_GOVERNANCE.md)
- [Glossary and claim discipline](./GLOSSARY.md)
- [NLnet scope](./GRANT_NLNET_SCOPE.md)
- [Baseline versus funded delta](./grants/baseline-funded-delta-matrix.md)
- [Funding use plan](./grants/funding-use-plan.md)
- [Roadmap](../ROADMAP.md)
- [Governance](../GOVERNANCE.md)
- [Contributing](../CONTRIBUTING.md)

D4 uses the compact Project/Grant/Governance overview and English Glossary as its translation-oriented source pair. The proposal remains submitted and under review, not awarded. Approximate €50,000 is planning only; budget change is none; merged baseline work cannot be budgeted again as future delivery.

D4 translations are current in all nine supported locale packs against `main@151b41c680190f7f3de729bf63e8e80a9d2285ce`.

## D5 extended references and retirement

- [Extended-reference policy](./EXTENDED_REFERENCE_POLICY.md)
- [Machine-readable D5 inventory](./status/d5-inventory.json)
- [D5 translation manifest](./status/d5-translation-manifest.json)
- [Archive routing](./archive/README.md)

D5 is complete through nine Extended Reference Guides pinned to `main@d5f7f1c4c0908d24f8994e4fbec45c102b9ab7d9`. Detailed ADR/profile, security/privacy/GDPR/legal mapping, tests/benchmarks/CI, machine-readable status, AI/audit, research/RFC and grant-evidence material remains English-only by design. Historical snapshots remain preserved and routed; they are not implementation or grant evidence.

The historical sequencing phrase `D5 remains a separate inventory phase` is retained here only to explain that D5 was intentionally completed after D4. It is no longer pending.

## Evidence and multilingual governance

- [Test report](../TEST_REPORT.md)
- [Current status](./STATUS.md)
- [Implementation manifest](./status/implementation-manifest.json)
- [D2 translation manifest](./status/d2-translation-manifest.json)
- [D3 translation manifest](./status/d3-translation-manifest.json)
- [D4 translation manifest](./status/d4-translation-manifest.json)
- [D5 source inventory](./status/d5-inventory.json)
- [D5 translation manifest](./status/d5-translation-manifest.json)
- [Localization policy](./LOCALIZATION_POLICY.md)
- [Translation status](./TRANSLATION_STATUS.md)

Locale indexes: [ar](./ar/README.md), [de](./de/README.md), [es](./es/README.md), [fr](./fr/README.md), [hi](./hi/README.md), [it](./it/README.md), [ja](./ja/README.md), [ru](./ru/README.md), [zh-CN](./zh-CN/README.md).

D1–D5 are current across all nine supported locales. The nine Extended Reference Guides route to current English sources without bulk-translating volatile evidence.

The legacy phrase `REFRESH_NEEDED translated document packs` remains validation vocabulary; the live D5 inventory resolves zero such documents.
