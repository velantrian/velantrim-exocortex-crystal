# 🔄 Connectorless Notion Hand-off

This file is the GitHub-native transfer queue for material Crystal work produced by an
AI agent or contributor that cannot read or write the Notion workspace.

## Core invariant

```text
GitHub must contain the complete public technical and audit context required to
understand, review, test and continue the work without Notion access.

Notion may contain deeper rationale, alternatives, grant context and synchronized
history, but it must never be the only place where an implemented contract, known risk,
audit finding or required next action is recorded.
```

Do not duplicate every sentence across both systems. Duplicate the **decision-bearing
facts** needed to avoid information loss and preserve continuity.

## Access modes

| Mode | Meaning | Required action |
|---|---|---|
| `NOTION_AVAILABLE` | The current actor can read and update the relevant Notion record | Update GitHub and Notion in the same work cycle |
| `HANDOFF_REQUIRED` | The current actor cannot access Notion, but the change is `GITHUB_AND_NOTION` | Complete the GitHub record and add a hand-off item below |
| `SYNCED` | A connected actor copied the required rationale/history into Notion and recorded the final evidence | Link the safe Notion title/reference and close the item |
| `NOT_REQUIRED` | The work is `NONE` or `GITHUB_ONLY` | No Notion action is required |
| `BLOCKED_PRIVACY_OR_PERMISSION` | Required synchronization cannot be completed safely because of permissions, privacy or an unresolved target | Keep the PR draft and escalate explicitly |

`HANDOFF_REQUIRED` is not permission to omit documentation. It means the connectorless
actor must leave a complete, structured GitHub package for a connected actor.

## Connectorless agent procedure

When an AI agent performs a material audit, analysis or implementation without Notion
access:

1. Continue the analysis using the GitHub repository, code, tests, CI, PRs and issues.
2. Record material findings in the appropriate GitHub surfaces:
   - `docs/ai/CURRENT_STATE.md` for reality/status changes;
   - `docs/ai/COMPONENT_MAP.md` for ownership, files or tests;
   - `docs/ai/KNOWN_RISKS.md` for discovered, changed or closed risks;
   - `docs/ai/WORK_LOG.md` for the compact engineering hand-off;
   - an ADR/RFC/status/security/grant document when its contract changes.
3. Add a pending item to this file when the work class is `GITHUB_AND_NOTION`.
4. Set the PR fields to:
   - `Notion access: UNAVAILABLE`;
   - `Notion synchronization: HANDOFF_REQUIRED`;
   - `GitHub hand-off: docs/ai/NOTION_HANDOFF.md#...`.
5. Do not claim that Notion was updated.
6. Keep a `GITHUB_AND_NOTION` implementation PR draft until a connected actor completes
   the required Notion synchronization. Analysis-only work may remain recorded here
   without blocking unrelated engineering, but its hand-off must remain visible.

## Connected actor procedure

A human or AI agent with Notion access must:

1. Read the complete GitHub hand-off and verify the cited PR, SHA, tests and current
   repository state.
2. Create or update the relevant Notion page with the required rationale, alternatives,
   boundaries, evidence, limitations and next actions.
3. Add the safe Notion page title/reference to the GitHub PR or hand-off item.
4. Change the item status from `HANDOFF_REQUIRED` to `SYNCED`.
5. After merge, add the final merge SHA and CI/checkpoint evidence to Notion.
6. Never copy private Notion content, secrets, personal information or private datasets
   into this public repository.

## Required hand-off item

```markdown
## HOFF-YYYYMMDD-NN — Short title

- Status: `HANDOFF_REQUIRED` / `SYNCED` / `BLOCKED_PRIVACY_OR_PERMISSION`
- Created: YYYY-MM-DD
- GitHub PR/issue:
- Exact base/head SHA:
- Intended Notion record title:
- Notion access for originating actor: `UNAVAILABLE`

### Problem / opportunity

### Material findings

### Decision and rationale

### Alternatives rejected or deferred

### Truth / Canon / evidence / privacy / authority boundaries

### Files and public documentation updated

### Tests / CI / runtime evidence

### Known limitations and next actions

### Synchronization completion
- Connected actor:
- Safe Notion title/reference:
- Synchronization date:
- Final merge SHA / CI evidence:
```

## Pending hand-offs

## HOFF-20261020-01 — NLnet final decision reconciliation

- Status: `SYNCED`
- Created: 2026-10-20
- GitHub PR: [#496](https://github.com/velantrian/velantrim-exocortex-crystal/pull/496), merged on 2026-10-20 from `f3871e33948e44639ece52dfee50ec91d439e393`.
- Exact base SHA: `6660210b65ff99362a16a7290d03b3f769b08cf0`.
- Intended Notion record title: Crystal — NLnet grant status and decision history.
- Notion access for originating actor: `UNAVAILABLE`.

### Problem / opportunity

Current grant surfaces still said the proposal was under review after the user-provided final decision of 2026-10-09.

### Material findings

The machine manifest exposes submission/review/award booleans consumed by docs-status and pytest; D4/D5 checkers also enforce prose. Current locale packs use historical translation checkpoints that must not be rewritten as if they established the final outcome.

### Decision and rationale

Preserve `submitted=true`, set `under_review=false`, preserve `awarded=false` and `budget_changed=false`; add `decision=NOT_SELECTED`, `award_status=NOT_AWARDED`, `decision_date=2026-10-09`. Align current English and nine-locale grant assertions while explicitly retaining their technical translation checkpoints.

### Alternatives rejected or deferred

Do not rewrite historical review records, falsify prior translation provenance, publish a refusal reason, change the requested budget, alter runtime/architecture, or implement another backlog item. No future funding is assumed.

### Truth / Canon / evidence / privacy / authority boundaries

No runtime, evidence admission, Canon, TruthGate, Guardian, security or provenance authority changes. No private correspondence, decision rationale or personal information is included. The decision/date are user-provided facts, not independently retrieved correspondence.

### Files and public documentation updated

Current English README/governance/roadmap/status/grant/AI surfaces; affected root and D1–D5 grant assertions in nine locales; implementation manifest; existing grant checkers and regression tests. The Draft PR diff is the exhaustive changed-file inventory. Frozen archives, evidence, preregistration, original application and source/control SHAs are unchanged.

### Tests / CI / runtime evidence

Run docs-status, D1–D5 source/translation gates, relevant pytest and the existing full CI, including Python 3.11/3.12. The Draft PR records exact commands/results and head-linked CI; no historical runtime checkpoint or test-count record is advanced by this grant-only change.

### Known limitations and next actions

PR #496 has merged. A connected follow-up checked the existing dated decision
record, synchronized the public outcome and exact post-merge evidence into the
Crystal Project Hub and decision page, and read both pages back successfully.
The Hub's October 1 checkpoint is explicitly historical. No private refusal
details were copied into GitHub; no project-specific rejection cause is inferred.
The originating actor's source/access limitations above remain part of its history.

### Synchronization completion

- Connected actor: Codex, with Notion access during the follow-up.
- Safe Notion title/reference: Velantrim Exo-Cortex Crystal — Project Hub;
  NLnet NGI0 Commons Fund — Decision · 2026-10-09.
- Synchronization date: 2026-10-20; both records verified by read-back.
- Final merge SHA: `6fab6a10bf4cead9118ed11e49f6bcc9fd2a36ed`.
- Post-merge CI: [39418258927](https://github.com/velantrian/velantrim-exocortex-crystal/actions/runs/39418258927), 9/9 jobs SUCCESS on that merge SHA.


## Completed hand-offs

Move completed items here or mark them `SYNCED`; preserve their GitHub evidence and safe
Notion reference so later agents can reconstruct the history without private workspace
access.
