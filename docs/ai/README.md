# 🤖 Crystal AI Agent Entry Point

This directory is the compact orientation and hand-off layer for AI coding agents,
automated auditors and human reviewers.

## Required reading order

1. [`AGENTS.md`](../../AGENTS.md)
2. [`CURRENT_STATE.md`](./CURRENT_STATE.md)
3. [`../STATUS.md`](../STATUS.md) and [`../status/implementation-manifest.json`](../status/implementation-manifest.json)
4. [`COMPONENT_MAP.md`](./COMPONENT_MAP.md)
5. [`KNOWN_RISKS.md`](./KNOWN_RISKS.md)
6. [`WORK_LOG.md`](./WORK_LOG.md)
7. [`NOTION_HANDOFF.md`](./NOTION_HANDOFF.md)
8. [`AUDIT_PLAYBOOK.md`](./AUDIT_PLAYBOOK.md)
9. [`../LOCALIZATION_POLICY.md`](../LOCALIZATION_POLICY.md) and [`../TRANSLATION_STATUS.md`](../TRANSLATION_STATUS.md) when public documentation or translations are affected
10. Relevant architecture, ADR, code, tests, CI and runtime configuration

Do not load the whole repository before completing this orientation pass.

## Source-of-truth hierarchy

```text
1. merged code on GitHub main
2. executable tests and exact CI
3. runtime configuration and composition
4. TEST_REPORT.md + implementation manifest
5. STATUS + IMPLEMENTATION_STATUS
6. architecture documents and accepted ADRs
7. English README primary public source
8. CURRENT full-parity localized root READMEs
9. TRANSLATION_STATUS + locale indexes for detail-pack freshness
10. this AI context pack
11. PRs, issues, roadmaps and research documents
12. Notion strategy/history
```

Translated public text never overrides current implementation evidence when they disagree.

## GitHub-first continuity

GitHub must be sufficient for a connectorless agent to understand current implementation,
authority boundaries, risks, consumers, tests, exact SHAs and next actions. No implemented
contract, known risk, material audit finding or required engineering action may exist only in
Notion.

## Status vocabulary

| Status | Meaning |
|---|---|
| `PROPOSED` | design, RFC, issue or research only |
| `IMPLEMENTED` | code exists |
| `TESTED` | named tests pass at an exact commit |
| `WIRED` | composed into the intended runtime path |
| `ENABLED` | active under relevant configuration |
| `OBSERVED` | demonstrated in a named environment |
| `VERIFIED_CHECKPOINT` | exact commit with recorded evidence |

## Crystal-specific boundaries

- Physical L3 is not automatically strict Canon.
- TruthGate and Guardian must not be bypassed.
- Public query surfaces remain read-only with respect to canonical truth state.
- Retrieval score, topic relevance, confidence and model fluency do not grant truth.
- Contradiction detection does not choose a winner without an audited decision.
- TRACE and Receipt are proof surfaces.
- The default runtime remains pure standard library.
- Reader RC-1 and RC-2 are bounded implemented foundations; `dedicated_reader_core=false` remains the full Reader boundary.

## Documentation and translation

English is the primary working and source language. English-first means source-first, not
English-only.

PR #340 restored full visual and semantic root README presentations in all nine supported
languages. The current Reader reconciliation keeps all nine localized root READMEs `CURRENT`.

The Russian D1/D3/D4/D5 detail pack is fully refreshed for Reader RC-1/RC-2. D2 and Quick Start remain `CURRENT` in all nine locale packs because Reader milestones did not alter those source semantics. The eight other locale detail packs retain their rich previous translations, but Reader-dependent D1/D3/D4/D5 documents are `REFRESH_NEEDED` until full semantic refresh. Do not replace those rich translations with compressed summaries merely to regain a `CURRENT` marker.

Broad translation work belongs in a dedicated docs-only PR. A translation may never strengthen
English capability, security, grant or authority claims.

Follow [`../DOCUMENTATION_SYNC_PROTOCOL.md`](../DOCUMENTATION_SYNC_PROTOCOL.md),
[`../LOCALIZATION_POLICY.md`](../LOCALIZATION_POLICY.md) and
[`../TRANSLATION_STATUS.md`](../TRANSLATION_STATUS.md).
