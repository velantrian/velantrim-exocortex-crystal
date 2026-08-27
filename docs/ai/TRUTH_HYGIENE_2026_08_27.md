# Crystal truth-hygiene reconciliation — 2026-08-27

## Purpose

Record the bounded documentation/governance reconciliation that followed a fresh GitHub + Notion audit after PR #464.

## Findings reconciled

1. `docs/STATUS.md` and `docs/IMPLEMENTATION_STATUS.md` said Issue #432 was closed, while live GitHub had #432 reopened as a post-V1 governance P1.
2. The machine implementation manifest contains deliberately retained architecture/runtime verification checkpoints that are guarded as historical compatibility evidence. Those fields must not be rewritten merely to imitate volatile repository lifecycle state.
3. Agents therefore need a separate bounded machine-readable lifecycle/governance overlay that is explicitly dated and subordinate to live GitHub.
4. Notion synchronization and grant-roadmap owner pages contained stale top-level `CURRENT` labels tied to historical repository SHAs.

## Decision

- Keep Crystal V1 lifecycle truth unchanged: `COMPLETE / 100% / FREEZE-STABILITY`, V1 `P0=0`, V1 `P1=0`, automatic next milestone `NONE`.
- Represent #432 separately as `POST-V1 GOVERNANCE = OPEN / P1`; it does not reopen V1.
- Preserve `docs/status/implementation-manifest.json` historical architecture/runtime checkpoints.
- Add `docs/status/current-lifecycle-overlay.json` for a dated volatile reconciliation of current lifecycle/governance/post-V1 state.
- Route AI agents through live GitHub first, then the lifecycle overlay, then the retained implementation manifest and status surfaces.
- Preserve all authority boundaries: no runtime, Canon, TruthGate, Guardian, WriteGate, storage activation or production authorization change.

## Evidence checkpoint

```text
base main: ad43d9231f567e06bd092c1b1230d8f0bebf773c
PR #464 reviewed head: 9ffe72ef44fe1005b68ddadec90d016cc2b801eb
PR #464 merge/main checkpoint: ad43d9231f567e06bd092c1b1230d8f0bebf773c
PR #464 exact-head CI: 33057472012 — 9/9 SUCCESS
PR #464 post-merge CI: 33065605480 — 9/9 SUCCESS
Issue #432: OPEN / P1 at audit time
ruleset 20602128: active; review-thread resolution false; no required-status-check rule observed
```

## Notion synchronization

The owning Notion surfaces were reconciled in the same wave:

- `💠 Velantrim Exo-Cortex Crystal — Project Hub`
- `🤖 Crystal — AI Agent Context & Audit Hand-off`
- `🔄 Crystal — Code ↔ Documentation Sync Protocol`
- `🎓 Grant-Safe Module Roadmap — Crystal / Funding Track`

Historical checkpoints remain provenance. They must not be read as live repository-head owners.

## Stop boundary

This is documentation/governance truth hygiene only. It does not authorize implementation of #432, a new Reader stage, storage activation, semantic/hybrid retrieval, EPIS/EITI runtime, or any other next milestone.
