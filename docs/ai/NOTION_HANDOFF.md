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

No pending hand-offs at the time this protocol was created.

## Completed hand-offs

Move completed items here or mark them `SYNCED`; preserve their GitHub evidence and safe
Notion reference so later agents can reconstruct the history without private workspace
access.
