# 📚 Velantrim Documentation Standard v1

`overview != current state != evidence != history`

This standard keeps Crystal documentation readable for humans, navigable for AI, and synchronized with authoritative repository evidence without rewriting history.

## Source-of-truth rule

Before a documentation update, resolve live GitHub state and read the existing authoritative Notion pages relevant to the workstream. A handoff is a checkpoint, not evergreen truth.

For implementation and validation claims, use this order:

```text
merged code / immutable artifacts
        ↓
exact tests + CI evidence
        ↓
CURRENT_STATE.md + machine manifest
        ↓
synchronized Notion/current presentation
        ↓
historical handoffs and archived checkpoints
```

If a lower documentation layer conflicts with stronger current evidence, reconcile the documentation while preserving historical records.

## Human + AI organization

Maintained project hubs should separate conceptual orientation from volatile evidence:

```text
👤 HUMAN LANDING LAYER
        ↓
🤖 AI READ / UPDATE CONTRACT
        ↓
🚦 CURRENT TECHNICAL TRUTH
        ↓
🧾 PR / CI / EVIDENCE
        ↓
🕰️ HISTORICAL CHECKPOINTS
```

The landing layer explains project purpose, boundaries and navigation. Current-state sections carry volatile phase/runtime/authorization truth. Evidence sections carry exact PR/SHA/CI/result provenance. Historical sections retain prior checkpoints.

## Update classes

### `STRUCTURAL_CHANGE`

Use when architecture, subsystem responsibility, authority boundary, runtime capability, project meaning, a core invariant, or a major roadmap direction changes.

Required action:
- inspect the Executive Summary and project portrait;
- inspect Project Tree, Mindmap, architecture flow, boundary tables, commentary, non-goals and documentation map;
- refresh only representations whose meaning became stale;
- update current-state/evidence surfaces as applicable;
- preserve historical checkpoints.

### `STATE_CHANGE`

Use when an important phase, runtime status, authorization, funding state, admission state or similar project-level state changes without necessarily changing architecture.

Required action:
- update current/top state surfaces so they do not imply an obsolete state;
- update machine-readable navigation/status where applicable;
- retain the stable project portrait unless its meaning changed;
- preserve prior evidence as history.

### `EVIDENCE_ONLY`

Use for a PR, SHA, CI run, review status, test count, mechanical fix, or bounded research result that does not change core system meaning or runtime authority.

Required action:
- update current checkpoint/evidence/log surfaces;
- do not mechanically rewrite a still-correct Tree, Mindmap or architecture portrait;
- do not turn evaluation evidence into runtime or epistemic authority.

## Visual roles

- **Project Tree** — what major parts exist.
- **Mindmap** — conceptual relationships and responsibilities.
- **ASCII architecture/flow** — information, control and authority flow.
- **Boundary table** — what a layer may do and what remains outside its scope.
- **Commentary** — architecture rationale and trade-offs.

When an `EVIDENCE_ONLY` change leaves these meanings intact, visual churn is unnecessary.

## Crystal boundaries

Documentation must preserve these distinctions:

```text
retrieval match          != evidence
similarity               != identity
NLI label                != proposition identity
NLI contradiction        != contradiction adjudication
repetition               != corroboration
cross-document candidate != Canon relation
ranking/filtering        != epistemic authority
candidate discovery      != candidate adjudication
evaluation pass          != runtime authorization
grant submission         != grant award
```

Research/evaluation wording must not imply authority to establish truth, admit evidence, prove proposition identity, adjudicate contradictions, mutate Canon, or alter Guardian/TruthGate responsibilities.

## Machine navigation

Start with `docs/ai/project_manifest.yaml`.

Primary repository surfaces:
- human start: `README.md`;
- AI start: `docs/ai/README.md`;
- volatile current state: `docs/ai/CURRENT_STATE.md`;
- machine implementation state: `docs/status/implementation-manifest.json`;
- maintenance contract: `docs/ai/DOCUMENTATION_STANDARD.md`.

Historical machine/runtime checkpoints inside existing manifests and tests remain evidence and should not be deleted merely because a later milestone exists.

## Update discipline

1. Live-verify current `main`, signature, relevant CI, open PRs/issues and relevant Notion pages.
2. Classify the change as `STRUCTURAL_CHANGE`, `STATE_CHANGE`, or `EVIDENCE_ONLY`.
3. Identify which surfaces are actually stale.
4. Update those surfaces without capability overclaiming.
5. Run repository validation and exact-head CI.
6. After merge, synchronize Notion when repository truth or the documentation contract changed.
7. Read back synchronized pages and verify that current/top truth is not stale.

Do not create new Notion pages unless explicitly authorized. Preserve historical checkpoints. Treat draft work, failed experiments, unavailable automated review, grant submissions and evaluation signals according to their actual evidence strength.
