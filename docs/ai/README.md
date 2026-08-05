# 🤖 Crystal AI Agent Entry Point

This directory is the compact orientation and hand-off layer for AI coding agents,
automated auditors, and human reviewers working on Velantrim Exo-Cortex Crystal.

It exists to prevent a common failure mode: reading hundreds of files without first
understanding Crystal's authority boundaries, current verified checkpoint, open work,
and document hierarchy.

## Required reading order

Before auditing or changing Crystal, read:

1. [`AGENTS.md`](../../AGENTS.md) — mandatory repository-wide agent contract.
2. [`CURRENT_STATE.md`](./CURRENT_STATE.md) — what is in `main`, what is only proposed,
   and what is not implemented.
3. [`../STATUS.md`](../STATUS.md) and
   [`../status/implementation-manifest.json`](../status/implementation-manifest.json) —
   verified runtime checkpoint and machine-readable evidence.
4. [`COMPONENT_MAP.md`](./COMPONENT_MAP.md) — decision owners, first files, first tests,
   and authority boundaries.
5. [`KNOWN_RISKS.md`](./KNOWN_RISKS.md) — unresolved engineering, operational,
   governance, and research risks.
6. [`WORK_LOG.md`](./WORK_LOG.md) — compact history of material work and hand-offs.
7. [`AUDIT_PLAYBOOK.md`](./AUDIT_PLAYBOOK.md) — context-efficient audit procedure.
8. The relevant architecture, ADR, code, tests, CI and runtime configuration.

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
7. README and reviewer-facing summaries
8. this AI context pack
9. PR descriptions, issues, roadmaps and research documents
10. Notion strategy/history records
```

The lower levels provide orientation and rationale. They do not override executable
reality.

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
- Retrieval score, topic relevance, confidence, or model fluency do not grant truth.
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

For `GITHUB_AND_NOTION` work, update the relevant Notion record before review and add the
final merge SHA, CI evidence, limitations, and remaining work after merge. Never copy
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
  → documented finding
  → synchronized hand-off
```
