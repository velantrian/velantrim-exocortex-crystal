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
8. [`KNOWN_RISKS.md`](./KNOWN_RISKS.md), [`COMPONENT_MAP.md`](./COMPONENT_MAP.md), [`WORK_LOG.md`](./WORK_LOG.md).
9. [`../../TEST_REPORT.md`](../../TEST_REPORT.md), relevant tests, evaluation artifacts and exact CI.
10. [`../LOCALIZATION_POLICY.md`](../LOCALIZATION_POLICY.md) + [`../TRANSLATION_STATUS.md`](../TRANSLATION_STATUS.md) when public/localized documentation is affected.

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

## 3. Current bounded truth after documentation closure

```yaml
repository_main_at_last_audit: 4628e6fe231103a57c86df8b157b87b8b6b183f2
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
latest_completed_docs_issue: 395
latest_completed_docs_pr: 396
latest_completed_docs_status: CLOSED_COMPLETED
documentation_architecture: HUMAN_AI_MACHINE_EVIDENCE_DOCUMENTATION_ARCHITECTURE_V1
active_milestone: none
next_milestone_selected: false
```

Issue #395 and PR #396 are the latest completed documentation-architecture closure. They must **not** be represented as an active workstream. No residual issue, Reader mechanism, model, backend or runtime milestone becomes active merely because the previous documentation milestone is closed.

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
      ├── 🤖 AI      docs/ai/README.md + AI context pack
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

A lifecycle closure such as `active → closed` is a `STATE_CHANGE` when leaving the old active label in an AI current-state surface would materially misdirect the next agent.

## 9. Localization rules

English is the primary source language. Source-first does not mean English-only.

Localized root/detail documents remain valid only to the checkpoints recorded in `TRANSLATION_STATUS.md`. A visually strong older localized README may be used as a **layout reference**, but its technical claims must not be copied into current English truth without repository verification.

The Human/AI documentation architecture milestone did not perform a broad localization refresh and did not manufacture translation parity.

## 10. Grant and backlog boundaries

```text
NLnet = submitted / under review / not awarded
~€50k = planning context only
```

Residual issues are separate scopes:

```text
#155 Epistemic Router RFC
#165 normalized-id migration / dedupe
#214 PII fixture + supply-chain hygiene
```

Do not auto-start them from documentation closure.

## 11. Current stop boundary

The latest completed documentation workstream is **Issue #395 / PR #396**:

```text
Human / AI / Machine / Evidence Documentation Architecture v1
        ↓
#395 CLOSED / completed
#396 MERGED
        ↓
active_milestone = none
next_milestone_selected = false
        ↓
fresh live verification + architecture reassessment
before any new bounded milestone
```

No model, discriminator, reranker, Reader backend, storage backend activation, authority expansion or residual issue implementation is authorized by the closure of #395/#396.