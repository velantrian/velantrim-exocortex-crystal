# Crystal Repository Hygiene Audit — 2026-08-29

## Scope

Bounded repository/truth-hygiene pass after Crystal V1 closure. This pass does **not** reopen V1, change runtime authority, select a new Reader mechanism, authorize production, or merge any change.

## Live baseline

- audited `main`: `ef8b2204b26d74673182bf734e4ec85e8139e0b9`;
- V1 lifecycle: COMPLETE / FREEZE-STABILITY;
- current cleanup branch: `chore/repository-truth-hygiene-2026-08-29`.

## Confirmed findings

### P1 — GitHub governance acceptance drift

Issue #432 had been closed even though its own acceptance criteria were not satisfied by the live ruleset read-back. The live ruleset still showed no required-status-check rule and `required_review_thread_resolution=false` at audit time.

Action in this pass: issue #432 was reopened. It must remain open until a fresh authoritative read-back proves the bounded target configuration.

### P2 — historical semantic noise in active paths

Several root/architecture documents were correctly labelled historical/superseded but still contained large obsolete planning sections and superseded vocabulary that could be retrieved without the warning header.

Action in this branch: collapse these active surfaces to short history pointers while preserving full historical content in Git history:

- `FUTURE.md`;
- `WORK_SUMMARY.md`;
- `SPRINT_A_V2_ADDITIONAL_PATCHES.md`;
- `docs/architecture/implementation-status.md`.

### P2 — grant taxonomy split

`docs/grant/` and `docs/grants/` represented one conceptual area using singular/plural sibling paths.

Action in this branch: move `CRYSTAL_PRE_FREEZE_EVIDENCE.md` to `docs/grants/evidence/` and remove the obsolete singular path.

### P2 — branch accumulation

Live branch enumeration found roughly 301 branches, including many historical `agent/*`, `claude/*`, `docs/*`, `fix/*`, `feat/*`, probe and no-op branches. Repository settings also had automatic head-branch deletion disabled at audit time.

No branches are deleted in this pass. Branch cleanup requires per-branch reachability/merge review and an explicit repository-administration step.

### P2 — stale authority shorthand in active code comments

Search found the superseded shorthand `Graph = Truth` in active `core/*.py` comments. Current authority vocabulary is `physical L3 != strict Canon` and Canon is a policy-constrained projection.

No runtime behavior changes are authorized by this finding. Comment-only cleanup should be handled as a separately reviewable change or an extension of this PR after exact diff review.

### P2/P3 — prototype and tooling containment

`prototypes/` contains intentionally non-runtime research modules. They may be test-covered without being production-wired. Root metadata/migration utilities are also maintenance tooling rather than runtime modules.

This pass does not delete either class. A later cleanup should classify each item as ACTIVE TOOL / RETAINED RESEARCH / HISTORICAL / SAFE TO REMOVE before movement or deletion.

## Current authority vocabulary

```text
physical L3 != strict Canon
research != runtime
spec != implementation
retrieval != evidence
receipt != truth
claim != belief
evidence != identity
identity != authority
model output != Canon
CI green != production authorization
similarity != identity
```

## Stop boundary

This hygiene pass is intentionally bounded. No runtime semantics, Reader authorization, storage activation, TruthGate/Guardian authority, Canon mutation path, production authorization or V1 completion state changes are introduced.
