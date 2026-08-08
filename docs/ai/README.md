# 🤖 Crystal AI Agent Entry Point

This directory is the compact orientation and hand-off layer for AI coding agents,
automated auditors and human reviewers working on Velantrim Exo-Cortex Crystal.

It exists to prevent a common failure mode: reading hundreds of files without first
understanding Crystal's authority boundaries, current verified checkpoint, open work and
document hierarchy.

## Required reading order

Before auditing or changing Crystal, read:

1. [`AGENTS.md`](../../AGENTS.md) — mandatory repository-wide agent contract.
2. [`CURRENT_STATE.md`](./CURRENT_STATE.md) — what is in `main`, what is only proposed,
   and what is not implemented.
3. [`../STATUS.md`](../STATUS.md) and
   [`../status/implementation-manifest.json`](../status/implementation-manifest.json) —
   verified runtime checkpoint and machine-readable evidence.
4. [`COMPONENT_MAP.md`](./COMPONENT_MAP.md) — decision owners, first files, first tests
   and authority boundaries.
5. [`KNOWN_RISKS.md`](./KNOWN_RISKS.md) — unresolved engineering, operational,
   governance and research risks.
6. [`WORK_LOG.md`](./WORK_LOG.md) — compact history of material work and hand-offs.
7. [`NOTION_HANDOFF.md`](./NOTION_HANDOFF.md) — connectorless synchronization queue and
   procedure.
8. [`AUDIT_PLAYBOOK.md`](./AUDIT_PLAYBOOK.md) — context-efficient audit procedure.
9. [`../LOCALIZATION_POLICY.md`](../LOCALIZATION_POLICY.md) and
   [`../TRANSLATION_STATUS.md`](../TRANSLATION_STATUS.md) when README, public meaning or
   translations are affected.
10. The relevant architecture, ADR, code, tests, CI and runtime configuration.

Do not load the whole repository before completing this orientation pass.

## Source-of-truth hierarchy

For implemented behavior, prefer evidence in this order:

```text
1. merged code on GitHub main
2. executable tests and CI evidence
3. runtime configuration and composition
4. TEST_REPORT.md + implementation manifest
5. docs/STATUS.md + docs/IMPLEMENTATION_STATUS.md
6. architecture documents and accepted ADRs
7. English README primary public source
8. CURRENT full-parity translations
9. this AI context pack
10. PR descriptions, issues, roadmaps and research documents
11. Notion strategy/history records
```

`ORIENTATION_ONLY` and `REFRESH_NEEDED` translations help navigation but do not override
current implementation or English evidence. Lower levels provide orientation and rationale;
they do not override executable reality.

## GitHub-first continuity

Not every AI agent has a Notion connector. The repository must therefore remain sufficient
for a connectorless agent to:

- understand current implementation and authority boundaries;
- perform a material audit;
- identify risks and downstream consumers;
- continue an unfinished engineering task;
- verify tests, CI and exact SHAs;
- prepare a complete hand-off for later Notion synchronization.

No implemented contract, known risk, material audit finding or required engineering next
action may exist only in Notion.

Notion remains valuable for deeper rationale, rejected alternatives, grant context and
project history. The goal is not sentence-for-sentence duplication; it is synchronized
preservation of the decision-bearing facts.

## Notion access modes

### Agent with Notion access

1. Read the relevant Project Hub record for `GITHUB_AND_NOTION` work.
2. Update the GitHub technical/audit surfaces.
3. Update Notion with the deeper rationale and history.
4. Record the safe Notion title/reference in the PR.
5. After merge, add final SHA, CI evidence, limitations and next actions.

### Agent without Notion access

1. Continue the analysis from GitHub; do not abandon it because the connector is absent.
2. Update the relevant GitHub files in this directory and any affected ADR/status/RFC.
3. Add a structured item to [`NOTION_HANDOFF.md`](./NOTION_HANDOFF.md) for
   `GITHUB_AND_NOTION` work.
4. Use `Notion synchronization: HANDOFF_REQUIRED`, never `DONE`.
5. Keep a `GITHUB_AND_NOTION` implementation PR draft until a connected actor completes
   the Notion update.
6. Use `BLOCKED_PRIVACY_OR_PERMISSION` only for a real permission, privacy or unresolved
   target problem — not merely because the current agent lacks a connector.

## Status vocabulary

Use these words precisely:

| Status | Meaning |
|---|---|
| `PROPOSED` | design, RFC, issue or research idea only |
| `IMPLEMENTED` | code exists in a branch or `main` |
| `TESTED` | relevant tests pass for a stated commit |
| `WIRED` | composed into the intended runtime path |
| `ENABLED` | active under the relevant configuration/profile |
| `OBSERVED` | demonstrated in a named running environment |
| `VERIFIED_CHECKPOINT` | exact commit with recorded test/status evidence |

Never collapse these into one claim.

## Crystal-specific non-negotiable boundaries

- Physical L3 is not automatically strict Canon.
- TruthGate and Guardian boundaries must not be bypassed.
- Public query surfaces remain read-only with respect to canonical truth state.
- Retrieval score, topic relevance, confidence or model fluency do not grant truth.
- Contradiction detection does not choose a winner without an explicit audited decision.
- TRACE and Receipt are proof surfaces, not decoration.
- Research Mode, Titan, Native Kernel, Mentaury, Personal Exo-Cortex and future cognitive
  modules are separate tracks unless independently implemented, tested, reviewed and
  merged into Crystal.
- The default runtime remains pure standard library; mandatory dependencies require an
  explicit architectural and packaging decision.

## Documentation synchronization

Every material change follows
[`../DOCUMENTATION_SYNC_PROTOCOL.md`](../DOCUMENTATION_SYNC_PROTOCOL.md).

For `GITHUB_AND_NOTION` work, update the relevant Notion record directly when access exists.
Without access, create a complete GitHub-native package and a visible hand-off in
`NOTION_HANDOFF.md`; a connected actor then synchronizes the deeper record. Never copy
private workspace content into this public repository.

## How to use this pack

Use these files to form a hypothesis about where to inspect. Then verify that hypothesis
against current code, consumers, tests, workflows and runtime composition.

```text
orientation map
  → exact claim
  → authority owner
  → relevant files and consumers
  → tests and CI
  → runtime wiring
  → documented GitHub finding
  → direct Notion sync or connectorless hand-off
```

## Active documentation language and translation policy

English is the primary working and source language. English-first means source-first, not
English-only.

- Completed root localized READMEs must preserve full visual and semantic coverage of the
  English README, including meaningful diagrams, tables, quick start, limitations and
  navigation.
- The Russian README is the first full-parity translation phase.
- Other supported root READMEs remain temporary `ORIENTATION_ONLY` surfaces until their
  dedicated translation PRs.
- Existing translated document packs are `REFRESH_NEEDED` unless their locale index and
  translation ledger record a reviewed source checkpoint.
- Other documents are translated progressively by language or document family; there is no
  single mandatory final pass for the whole corpus.
- Implementation PRs update English first and record whether translated public meaning
  changed. Substantial translation work belongs in a separate docs-only PR.
- A translation may not strengthen capability, security, grant or authority claims.

Agents must read [`../LOCALIZATION_POLICY.md`](../LOCALIZATION_POLICY.md) and update
[`../TRANSLATION_STATUS.md`](../TRANSLATION_STATUS.md) when a language phase changes.
