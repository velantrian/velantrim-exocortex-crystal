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
8. localized root/detail docs at their recorded source checkpoints
9. TRANSLATION_STATUS + locale indexes for freshness
10. this AI context pack
11. PRs, issues, roadmaps and research documents
12. Notion strategy/history
```

Translated public text never overrides current implementation evidence when it disagrees.

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
- Reader RC-1 through RC-7 are bounded implemented layers.
- RC-8 is a completed retrieval architecture/research decision.
- RC-9 is the completed deterministic lexical PRE-ADMISSION candidate-discovery implementation baseline.
- PR #378 adds RC-10 reuse/comparison preregistration only; it executes no semantic/hybrid comparator and adds no Reader runtime.
- `dedicated_reader_core=false` remains the full Reader capability boundary.

```text
retrieval match          != evidence
similarity               != identity
repetition               != corroboration
cross-document candidate != Canon relation
ranking                  != epistemic authority
candidate discovery      != candidate adjudication
comparison pass          != runtime authorization
```

## RC-9 evidence orientation

Authoritative result: `eval/reader_rc9_lexical_baseline.json` and
`docs/architecture/READER_RC9_LEXICAL_BASELINE.md`.

K=5 frozen paired benchmark: Recall@5 `0.937500`, Precision@5 `0.187500`, MRR
`0.895833`, paired hard-negative rate@5 `1.000000`, useful hits `15/16`, hard-negative
hits `4/4`. Cross-lingual `rc8-004` is missed. Classification:
`LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`.

Do not restate Recall@5 as “accuracy”, Precision@5 as semantic precision, or the measured gap
as automatic authorization for semantic/vector retrieval.

## Documentation and translation

English is the primary working and source language. English-first means source-first, not
English-only.

The post-RC-9 grant-presentation reconciliation advances the **English** root/grant-facing
source. It intentionally does not perform a broad translation refresh. Localized documents
therefore remain authoritative only to the source checkpoints recorded in
`TRANSLATION_STATUS.md`; they must not be treated as newer than those checkpoints.

The retained Reader-dependent localization position remains: Russian Reader-dependent
D1/D3/D4/D5 detail surfaces are current to the immutable RC-7 English layer; eight other
Reader-dependent locale packs remain `REFRESH_NEEDED` (64 tracked detail documents). D2 and
Quick Start remain current where their source semantics did not change.

A later localization milestone may restore full parity with the new English public README, but
this grant-truth milestone does not do that work.

Follow [`../DOCUMENTATION_SYNC_PROTOCOL.md`](../DOCUMENTATION_SYNC_PROTOCOL.md),
[`../LOCALIZATION_POLICY.md`](../LOCALIZATION_POLICY.md) and
[`../TRANSLATION_STATUS.md`](../TRANSLATION_STATUS.md).
