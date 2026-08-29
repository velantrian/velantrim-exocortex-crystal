# Crystal Repository Hygiene Audit — 2026-08-29

## Scope

Bounded repository/truth-hygiene pass after Crystal V1 closure. This pass does **not** reopen V1, change runtime authority, select a new Reader mechanism, authorize production, or merge any change.

## Live baseline

- audited `main`: `ef8b2204b26d74673182bf734e4ec85e8139e0b9`;
- V1 lifecycle: COMPLETE / FREEZE-STABILITY;
- current cleanup branch: `chore/repository-truth-hygiene-2026-08-29`.

## Validation checkpoints

- PR cleanup head `b249eb962b787043ec8f48f576d064591dec0088`: CI #1819 — 9/9 jobs SUCCESS.
- prototype-status correction head `fe6fe37333f7b5fbf27def03f2d0e28970cfa8ab`: CI #1820 — SUCCESS.
- CI green is regression evidence only; it is not production or merge authorization.

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

The superseded shorthand `Graph = Truth` remains in some active `core/*.py` comments. Current authority vocabulary is `physical L3 != strict Canon` and Canon is a policy-constrained projection.

No runtime behavior change is justified by this finding. Because the available GitHub contents mutation replaces whole files, comment-only cleanup of very large runtime modules is deliberately deferred to a separately reviewable patch rather than accepting unnecessary whole-file replacement risk in this PR.

### P2 — prototype containment

`prototypes/` contains intentionally non-runtime research modules. They are retained research evidence, not shipping runtime and not an automatic roadmap.

Action in this branch: `prototypes/README.md` now classifies the modules as `RETAINED RESEARCH`, removes a stale anchor into the previous full `FUTURE.md`, and points readers to current lifecycle/implementation truth.

Presence or test coverage does not promote a prototype into runtime, Canon, or production authority.

### P3 — root maintenance tooling classification

The root metadata/corpus utilities are **not runtime package surface**, but they also should not be called dead code without evidence.

Current classification:

| File | Classification | Reason |
|---|---|---|
| `audit_metadata.py` | ACTIVE/RETAINED MAINTENANCE TOOL | Audits the archived Sprint1 JSONL corpus for structural/RFC metadata issues. |
| `fill_dependencies.py` | ACTIVE/RETAINED MAINTENANCE TOOL | Deterministically derives bounded RFC dependency metadata; supports dry-run and guarded writes. |
| `check_rfc_duplicates.py` | ACTIVE/RETAINED MAINTENANCE TOOL | Specialized historical-corpus duplicate inspection. |
| `velantrim_migrate_v3_1.py` | ACTIVE/RETAINED MIGRATION TOOL | Corpus migration/validation utility with streaming, diff and dependency validation logic. |

`pyproject.toml` explicitly limits the installable runtime to `core`, `core.adapters`, and `adaptive_threshold_module`; these utilities are outside the shipping package surface. The same project configuration runs repository-wide coverage (`--cov=.` with a 100% gate), and the exact-head CI checkpoint is green. Therefore the safe conclusion is **maintenance tooling outside runtime**, not unreferenced garbage.

Movement into a `tools/` namespace may improve root organization, but it is a refactor, not a deletion. It should be performed only with import/test/reference updates and a fresh exact-head CI run.

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
