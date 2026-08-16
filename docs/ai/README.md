# 🤖 Crystal — Special for AI / Agent Entry Point

**Document role:** machine/agent router, not a human landing page.  
**Project:** `velantrian/velantrim-exocortex-crystal`  
**Rule:** re-resolve live GitHub before treating any dated SHA or issue state in documentation as current.

Human-oriented explanation lives in [`../../README.md`](../../README.md) and [`../OVERVIEW.md`](../OVERVIEW.md). Do **not** infer implementation truth from narrative readability, diagrams or competitor comparisons.

## 1. Required read order

Read in this order before making architecture/runtime/status claims:

1. [`../../AGENTS.md`](../../AGENTS.md) — repository operating instructions.
2. [`../status/implementation-manifest.json`](../status/implementation-manifest.json) — machine-readable capability and authorization fields.
3. [`../STATUS.md`](../STATUS.md) — current implementation/evidence summary.
4. [`../IMPLEMENTATION_STATUS.md`](../IMPLEMENTATION_STATUS.md) — capability matrix and explicit non-implementation.
5. [`CURRENT_STATE.md`](./CURRENT_STATE.md) — detailed Reader/evaluation/architecture evidence snapshot.
6. [`../ARCHITECTURE_OVERVIEW.md`](../ARCHITECTURE_OVERVIEW.md) — technical architecture map.
7. [`../ARCHITECTURE.md`](../ARCHITECTURE.md) and relevant `docs/architecture/**` contracts.
8. [`AUDIT_AND_FUTURE_WORK.md`](./AUDIT_AND_FUTURE_WORK.md) — open/deferred audit questions, future-work candidates, and explicit non-authorization boundaries. Treat it as a ledger, **not** as permission to implement the next item.
9. [`KNOWN_RISKS.md`](./KNOWN_RISKS.md), [`COMPONENT_MAP.md`](./COMPONENT_MAP.md), [`WORK_LOG.md`](./WORK_LOG.md).
10. [`../../TEST_REPORT.md`](../../TEST_REPORT.md), relevant tests, evaluation artifacts and exact CI.
11. [`../LOCALIZATION_POLICY.md`](../LOCALIZATION_POLICY.md) + [`../TRANSLATION_STATUS.md`](../TRANSLATION_STATUS.md) when public/localized documentation is affected.

Do not bulk-load the repository before completing this orientation pass.

## 2. Source-of-truth hierarchy

```yaml
authority_order:
  - live_merged_github_main
  - executable_tests_and_exact_ci
  - runtime_configuration_and_composition
  - machine_implementation_manifest
  - status_and_implementation_status
  - accepted_architecture_contracts_and_adrs
  - test_report_and_frozen_evaluation_artifacts
  - english_human_documentation
  - localized_docs_at_recorded_source_checkpoint
  - ai_context_pack
  - issues_prs_roadmaps_research
  - notion_strategy_and_history
```

Notion is synchronized documentation, not a substitute for repository evidence. Localized text never overrides current implementation evidence.

## 3. Durable truth + live provenance resolution

This static router intentionally does **not** freeze volatile repository lifecycle facts such as the current `main` SHA, latest CI run, latest completed docs PR/issue, or active milestone. Those values become stale as soon as a later merge lands.

```yaml
repository_head: RESOLVE_LIVE_GITHUB
repository_ci: RESOLVE_LIVE_GITHUB
documentation_lifecycle: RESOLVE_LIVE_GITHUB
active_milestone: RESOLVE_LIVE_GITHUB
next_milestone: RESOLVE_LIVE_GITHUB
current_architecture_checkpoint: 76a9493b8ba64b832472ef9bfc1f1c23ebe6654e
architecture_contract: RRTIC-v1
architecture_contract_status: FROZEN_ARCHITECTURE_CONTRACT
reader_runtime_authorization: false
dedicated_reader_core: false
semantic_hybrid_reader_runtime: false
nli_reader_runtime_filter: false
rrtic_runtime_provider: false
sqlite_ordinary_local_first: active
postgresql_pgvector_reader: inactive
postgresql_pgvector_active: false
grant_status: submitted_under_review_not_awarded
```

Resolution rule:

```text
current repository/lifecycle claim
        ↓
resolve live GitHub main + PRs/issues + exact CI
        ↓
compare machine/status surfaces
        ↓
read AUDIT_AND_FUTURE_WORK for unresolved/deferred questions
        ↓
use synchronized Notion only as secondary checkpoint/history
```

Do not add a new hard-coded “latest completed docs issue/PR” or “repository main at last audit” field to this router. Immutable historical evidence belongs in the relevant PR/issue, CI/checkpoint record, status/evaluation history, synchronized Notion checkpoint, or the future-work ledger when it is needed to explain an unresolved question.

## 4. Reader capability map

```text
RC-1  source/session foundation                  IMPLEMENTED
RC-2  structural document map                    IMPLEMENTED
RC-3  explicit multi-pass mechanics              IMPLEMENTED
RC-4  proposition candidates                     IMPLEMENTED
RC-5  same-document relation candidates          IMPLEMENTED
RC-6  bounded long-context strategy              IMPLEMENTED
RC-7  explicit cross-document candidate links    IMPLEMENTED
RC-8  retrieval architecture decision            ARCHITECTURE / RESEARCH
RC-9  deterministic lexical discovery            IMPLEMENTED
Comparator v1                                    FROZEN EVALUATION / GATE FAIL
NLI neutral-filter v1                            FROZEN EVALUATION / GATE FAIL
RRTIC-v1                                         FROZEN ARCHITECTURE CONTRACT
Dedicated/full Reader                            NOT IMPLEMENTED
Semantic/hybrid Reader runtime                   NOT AUTHORIZED
```

RRTIC-v1 is model-free and diagnostic-only. It freezes six suspicion-only relation families and ten structural qualifier dimensions. It does not filter, rerank, infer identity, admit evidence, adjudicate contradictions, mutate Canon or auto-register RC-5 relations.

## 5. Permanent authority invariants

These strings express architectural boundaries and must not be weakened by documentation edits:

```text
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
working-set coverage != comprehension proof
summary != evidence
cross-document link != Canon relation
same-topic != same proposition
possible-same-claim != claim identity
similarity signal != identity proof
repetition across sources != corroboration
retrieval match != evidence
similarity != identity
NLI label != proposition identity
NLI contradiction != contradiction adjudication
RRTIC suspicion != adjudicated relation
qualifier mismatch != truth decision
ranking != epistemic authority
candidate discovery != candidate adjudication
comparison pass != runtime authorization
evaluation pass != runtime authorization
```

RC-7 retains **no automatic semantic matching**. Reader discovery/inspection does not establish evidence, identity, contradiction resolution or Canon authority.

## 6. Forbidden inferences

```yaml
never_infer:
  historical_sha_is_live_head: true
  static_ai_snapshot_is_live_repository_provenance: true
  architecture_contract_is_runtime_provider: true
  retrieval_match_is_evidence: true
  similarity_is_identity: true
  nli_label_is_adjudication: true
  rrtic_suspicion_is_truth_relation: true
  failed_evaluation_is_runtime_capability: true
  comparison_success_would_equal_runtime_authorization: true
  physical_l3_is_strict_canon: true
  postgresql_import_is_backend_activation: true
  localized_current_marker_means_latest_english_parity: true
  grant_submission_is_grant_award: true
  zero_review_threads_is_independent_approval: true
  closed_milestone_is_active_work: true
  residual_issue_is_auto_selected: true
  future_work_priority_is_authorization: true
  future_work_entry_is_milestone_selection: true
```

## 7. Machine flags vs explanatory prose

When prose and machine fields appear inconsistent:

```text
live code/tests/CI
      ↓
implementation-manifest.json
      ↓
STATUS / IMPLEMENTATION_STATUS
      ↓
architecture contracts
      ↓
human overview / README
```

Do not “repair” a machine field based solely on prettier or newer prose.

## 8. Documentation interface architecture

One project truth is exposed through four interfaces:

```text
ONE PROJECT TRUTH
      │
      ├── 👤 HUMAN   README.md + docs/OVERVIEW.md
      ├── 🤖 AI      docs/ai/README.md + AI context pack + future-work ledger
      ├── ⚙ MACHINE docs/status/implementation-manifest.json + schemas
      └── 🧾 EVIDENCE STATUS + TEST_REPORT + tests + CI + eval + history
```

The interfaces may use different presentation styles. They must not disagree about implementation or authority.

### Change classification

```yaml
STRUCTURAL_CHANGE:
  meaning: architecture, subsystem responsibility, authority, runtime capability, core invariant
  required: refresh affected human + AI + machine/evidence representations

STATE_CHANGE:
  meaning: phase, gate, enabled/disabled, funding/admission/current status changes
  required: remove stale current-state claims from affected top surfaces

EVIDENCE_ONLY:
  meaning: SHA, PR, CI, review, test count, docs-only reconciliation
  required: update evidence/checkpoints; do not mechanically rewrite still-correct conceptual visuals
```

A lifecycle closure such as `active → closed` is a `STATE_CHANGE` when leaving an old active label in an AI current-state surface would materially misdirect the next agent. Volatile lifecycle evidence itself must be resolved live rather than encoded as an indefinitely-current static field.

## 9. Localization rules

English is the primary source language. Source-first does not mean English-only.

Localized root/detail documents remain valid only to the checkpoints recorded in `TRANSLATION_STATUS.md`. A visually strong older localized README may be used as a **layout reference**, but its technical claims must not be copied into current English truth without repository verification.

The Human/AI documentation architecture milestone did not perform a broad localization refresh and did not manufacture translation parity.

## 10. Grant and backlog boundaries

```text
NLnet = submitted / under review / not awarded
~€50k = planning context only
```

The future-work ledger is the place to preserve unresolved questions and deferred candidates. It is not a backlog executor. Any issue number or candidate listed there must be re-resolved live before use.

Do not auto-start a residual issue from documentation closure, an old roadmap, or the existence of a future-work entry.

## 11. Future-work ledger contract

[`AUDIT_AND_FUTURE_WORK.md`](./AUDIT_AND_FUTURE_WORK.md) exists to prevent loss of unfinished reasoning across chats and agents.

Use it to answer:

```text
what is genuinely still open?
what is only worth investigating?
what is deliberately deferred?
what is explicitly not authorized?
what evidence must exist before implementation?
```

Its states such as `OPEN`, `INVESTIGATE`, `DEFERRED`, `BLOCKED`, and `NOT_AUTHORIZED` are **not** implementation commands.

A future audit should reconcile every relevant entry against live GitHub and report `DONE / STILL_OPEN / STALE / NEW_FINDING / NEEDS_REPRODUCTION / NOT_AUTHORIZED` before selecting work.

## 12. Current stop boundary

This static AI router does not select or persist the current workstream. Before any new bounded work:

```text
resolve live GitHub main + exact CI
        ↓
resolve open PRs/issues and lifecycle state
        ↓
read and reconcile AUDIT_AND_FUTURE_WORK
        ↓
compare authorized Notion checkpoints
        ↓
fresh architecture reassessment
        ↓
select exactly one bounded scope
```

No model, discriminator, reranker, Reader backend, storage backend activation, authority expansion or residual issue implementation is authorized by this document or by the future-work ledger. A historical closure, a stale snapshot, the absence of open PRs, or a high-priority future-work item is not authorization to start the next backlog item.
