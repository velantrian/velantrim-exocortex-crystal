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
- tooling-classification head `3b478b2112bbbfe01ae4a59e2978a6914fa4423a`: CI #1821 triggered; non-Python gates were green at the branch-audit checkpoint while Python 3.11/3.12 were still running.
- CI green is regression evidence only; it is not production or merge authorization.

## Confirmed findings

### P1 — GitHub governance acceptance drift

Issue #432 had been closed even though its own acceptance criteria were not satisfied by the live ruleset read-back. The live ruleset still showed no required-status-check rule and `required_review_thread_resolution=false` at audit time.

Action in this pass: issue #432 was reopened and a fresh 2026-08-29 read-back was recorded in the issue. It must remain open until a fresh authoritative read-back proves the bounded target configuration.

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

After creating this cleanup branch, live enumeration found **302 branches including `main` and the current cleanup branch**. The count was 301 before this pass created the new branch. Repository settings had automatic head-branch deletion disabled at audit time.

Branch deletion must not be based on age or prefix alone. Two independent signals are required:

1. Git ancestry (`ahead_by` / `behind_by` against current `main`);
2. associated PR disposition, because squash merges can leave a branch `ahead_by>0` even when its work was already merged.

Confirmed examples:

| Branch | Ancestry vs `main` | PR evidence | Classification |
|---|---:|---|---|
| `agent/crystal-freeze-closure-2026-08-19` | ahead 0 / behind 66 | fully contained by `main` ancestry | DELETE CANDIDATE |
| `agent/crystal-pre-freeze-remediation-2026-08-18` | ahead 0 / behind 91 | fully contained by `main` ancestry | DELETE CANDIDATE |
| `docs/crystal-v1-closure-20260822` | ahead 0 / behind 51 | fully contained by `main` ancestry | DELETE CANDIDATE |
| `docs/v1-closure-atlas-sync` | ahead 0 / behind 41 | fully contained by `main` ancestry | DELETE CANDIDATE |
| `feat/reader-file-source-v0-1` | ahead 0 / behind 23 | fully contained by `main` ancestry | DELETE CANDIDATE |
| `feat/reader-pdf-source-v0-1` | ahead 0 / behind 10 | fully contained by `main` ancestry | DELETE CANDIDATE |
| `feat/reader-product-bridge-v0-1` | ahead 0 / behind 32 | fully contained by `main` ancestry | DELETE CANDIDATE |
| `noop` | ahead 0 / behind 7 | no unique ancestry | DELETE CANDIDATE |
| `agent/reader-core-rc1-skeleton` | divergent; ahead 12 / behind 188 | PR #358 MERGED 2026-08-10 | DELETE CANDIDATE AFTER MERGE-METADATA CHECK |
| `feat/reader-rc9-lexical-baseline` | divergent; ahead 40 / behind 179 | PR #376 MERGED 2026-08-12 | DELETE CANDIDATE AFTER MERGE-METADATA CHECK |
| `fix/evidence-current-standing-463` | divergent; ahead 3 / behind 2 | PR #464 MERGED 2026-08-27 | DELETE CANDIDATE AFTER MERGE-METADATA CHECK |
| `docs/crystal-truth-hygiene-2026-08-27` | divergent; ahead 5 / behind 1 | PR #465 MERGED 2026-08-27 | DELETE CANDIDATE AFTER MERGE-METADATA CHECK |
| `probe/crystal-ruleset-432` | divergent; ahead 1 / behind 52 | contains `docs/ai/RULESET_ENFORCEMENT_PROBE.md`; #432 unresolved | RETAIN UNTIL #432 RESOLVED |

This proves the branch graveyard is cleanable, but not by blind mass deletion. The safe algorithm is:

```text
if branch == main or branch == active_cleanup_branch:
    keep
elif ahead_by == 0:
    deletion_candidate
elif associated_pr.merged_at is not null:
    deletion_candidate_after_merge_metadata_check
else:
    inspect_unique_commits_and_retain_or_archive
```

No branch is deleted in this pass because the currently exposed connector does not provide a delete-ref operation, and destructive bulk deletion should remain a separately auditable administration action.

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

`pyproject.toml` explicitly limits the installable runtime to `core`, `core.adapters`, and `adaptive_threshold_module`; these utilities are outside the shipping package surface. The same project configuration runs repository-wide coverage (`--cov=.` with a 100% gate), and the exact-head CI checkpoints are green up to the latest completed checkpoint. Therefore the safe conclusion is **maintenance tooling outside runtime**, not unreferenced garbage.

Movement into a `tools/` namespace may improve root organization, but it is a refactor, not a deletion. It should be performed only with import/test/reference updates and a fresh exact-head CI run.

### P2 — PR #466 readiness drift

PR #466 was created as Draft. GitHub records a `ready_for_review` event by the repository owner account at `2026-08-29T10:04:51Z`. The PR head changed again after that event. The current PR has no review submissions, no review comments and no review threads.

Therefore the old Ready transition is not fresh review evidence for the current head. A connector attempt to convert the PR back to Draft failed because the GraphQL wrapper requested a non-existent `Repository.fullDatabaseId` field. This is a tooling failure, not readiness authorization.

Until the Draft flag is restored or a new explicit owner readiness decision is made on the final exact head, treat PR #466 as:

```text
NOT READY
NO MERGE AUTHORIZATION
```

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
