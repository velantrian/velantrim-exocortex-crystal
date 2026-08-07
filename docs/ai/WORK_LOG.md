# 🧾 Crystal AI Work Log

This is the compact engineering hand-off log for material work. It is not a changelog of
every commit and not a replacement for `CHANGELOG.md`, issues, PRs or Notion history.

Add new entries at the top. Record only verified facts and distinguish completed work from
remaining work.

## Entry template

```markdown
## YYYY-MM-DD — Title

### Scope
What repository area, issue or PR was inspected or changed?

### Verified baseline
Exact main SHA, PR base/head and relevant runtime checkpoint.

### Findings / decisions
What was learned or decided, and why?

### Changes
Files, contracts and documentation changed.

### Validation
Tests, CI runs, review evidence and runtime observations.

### Remaining
Concrete follow-up and proof required.

### Synchronization
Documentation impact class and Notion record/checkpoint.
```

---

## 2026-08-07 — Durable L3 storage profile and doctor merged

### Scope

Closed the risk that environment-selected `VELANTRIM_L3_BACKEND=auto` could re-probe
available backends in every new process and silently select a different physical L3 or
fall through to ephemeral Mock.

### Verified baseline

- runtime base: `main@9283850e5b28fe0f8c5a632d3a3d107d780145ff`;
- PR #322 validated head: `156e974393586ada30feaac2500eae7003cb2885`;
- PR #322 merged as `0ca66cc6e194edd06b5de2a6eb5126a30613957e`;
- merged tree: `721049b198045e1c8504d57f64a0ab44b72ae403`, identical to the
  validated PR head tree;
- exact-head CI: `31174042124`.

### Findings / decisions

- `auto` is acceptable only for the first durable bootstrap; the selected backend and
  non-secret locator must then be persisted and reused across restarts.
- The storage profile is deployment identity, not epistemic authority. It cannot establish
  truth, strict Canon membership, evidence or admission permission.
- Automatic fallback to ephemeral Mock must fail closed. Explicit Mock remains available
  for tests and deliberate development use.
- The default profile location must not depend on process working directory. Independent
  diff inspection found the first draft's cwd-relative profile path; it was corrected
  before merge to `~/.velantrim/velantrim-storage-profile.json` and pinned by a regression
  test across working directories.
- Backend/locator changes require an explicit verified migration. Editing or deleting the
  profile is not a migration.
- PostgreSQL/pgvector and a dedicated VectorDB were not added. They remain possible future
  institutional profiles only after invariant-equivalence and migration proof are defined.
- The automatic Codex code review was unavailable because the connected account had
  exhausted its code-review quota. That service limitation is preserved in the PR
  timeline and is not counted as approval or independent review evidence.

### Changes

- added `core/backend_profiles.py` with versioned profile validation, locator checksum,
  atomic first-write behavior and conflict detection;
- integrated profile resolution/finalization into the shared `BackendRegistry` for the
  environment-selected L3 singleton while preserving fresh programmatic explicit
  instances;
- added pure-standard-library `core/doctor.py` and the `velantrim-doctor` entry point;
- rejected automatic Mock fallback and ephemeral `auto` locators;
- anchored the default profile in the user's home directory and documented explicit
  service/container overrides;
- added defensive tests for restart locking, backend/locator drift, malformed profiles,
  concurrent initializers, cleanup, cwd changes and read-only diagnostics;
- added `docs/architecture/DURABLE_STORAGE_PROFILE.md`.

### Validation

- Python 3.11: **1987 passed / 12 skipped / 0 failed**;
- Python 3.12: successful with the same strict coverage gate;
- **8231 measured statements / 100.00% line coverage**;
- **9/9 CI jobs successful** in run `31174042124`;
- Ruff, Gitleaks, Bandit, pip-audit, Ring Zero mutation, eval, JSONL integrity,
  docs-status and Docker successful;
- initial isolated profile/registry/doctor validation: **43 passed / 100% line coverage**;
- manual diff review found and corrected the cwd-relative profile-path defect before the
  final exact-head run and merge.

### Remaining

- implement an explicit storage migration workflow with dry-run, counts/hashes,
  evidence/restriction/audit verification, rollback proof and a migration receipt;
- document and test backup/restore and upgrade behavior for locked profiles;
- define operator-assisted stale-lock recovery without unsafe automatic deletion;
- require explicit `VELANTRIM_STORAGE_PROFILE_PATH` for services, containers and multiple
  deployments sharing one user account;
- evaluate PostgreSQL/pgvector only as a separate institutional RFC with preserved
  authority and migration invariants;
- correct any remaining historical wording that equates physical L3 with truth or strict
  Canon.

### Synchronization

- class: `GITHUB_AND_NOTION`;
- runtime record: PR #322 and merge `0ca66cc6e194edd06b5de2a6eb5126a30613957e`;
- GitHub AI context follow-up updates Current State, Component Map, Known Risks and this
  Work Log;
- Notion targets: Crystal Project Hub and Crystal Current Architectural Position;
- only immutable merge, tree, CI and test evidence is promoted as verified runtime truth.

---

## 2026-08-07 — Runtime hardening train #319–#321 verified and merged

### Scope

Completed the material reliability/security/scale findings from the 2026-08-06 deep
audit: crash-consistent curator decisions, authenticated principal-bound writes and
bounded legacy retrieval with explicit reindex.

### Verified baseline

- PR #319 merged as `62879cd2095450de57d11fcf97c13f5f9768ad0b`;
- PR #320 merged as `1414862786aa0c0d4cf4ad152776dd4e55536bf0`;
- PR #321 merged as `1748677a5c84e8a9b3af08fcaed0215efebcdd66`;
- final verified runtime checkpoint: `1748677a5c84e8a9b3af08fcaed0215efebcdd66`;
- final tree: `38c829b37bb61939792c64ee01ad925d6e8afd13`.

### Findings / decisions

- SQLite is the curator-decision transaction boundary; L3 projection is durable,
  idempotent and recoverable rather than falsely described as cross-database ACID.
- Processing restriction is authoritative in L1 and remains deny-dominant during a
  secondary L3 outage.
- Every bundled curator write derives audit identity and authorization from a validated
  principal; actor text is only an exact-match assertion.
- No-fingerprint compatibility retrieval must have a hard work bound or fail closed with
  `legacy_store_requires_reindex`; query paths never initialize fingerprints.
- Retrieval rank, physical L3 membership and bounded lexical score do not establish truth
  or strict Canon membership.

### Changes

- added transactional decision journal/outbox, idempotent projector and recovery/status
  surfaces;
- added principal capability/scope/report/lease composition across bundled HTTP/CLI
  writes and ADMIN-only force approval;
- added bounded Mock/SQLite legacy retrieval, structured query/MCP degraded-mode metadata
  and explicit reindex;
- added ADR-017, ADR-018, ADR-019, operator/security documentation and defensive tests;
- removed literal bearer-token assignment examples and rebuilt affected PR histories
  cleanly on their current bases;
- recorded 1k/10k/30k bounded retrieval benchmark evidence.

### Validation

- PR #319 exact-head CI `31162857843`: 9/9 jobs green, Python 3.11/3.12,
  1881 passed / 12 skipped / 7578 statements / 100% coverage;
- PR #320 exact-head CI `31164585628`: 9/9 jobs green, Python 3.11/3.12,
  1918 passed / 12 skipped / 7754 statements / 100% coverage;
- PR #321 exact-head CI `31166027193`: 9/9 jobs green, Python 3.11/3.12,
  1943 passed / 12 skipped / 7948 statements / 100% coverage;
- security, Ring Zero mutation, eval, JSONL, docs-status, Ruff and Docker gates green;
- benchmark `31165503179`: candidate cap 256 held for 1k, 10k and 30k corpora.

### Remaining

- external distributed lease/fencing adapter;
- production IdP, tenant isolation, token lifecycle and policy administration;
- bounded degraded-retrieval recall tradeoff and operator reindex lifecycle;
- controlled performance SLO policy and broader mutation testing;
- reproducible dependency/tool/action pinning;
- normalized legacy-ID migration and separately reviewed Reader Core RFC.

### Synchronization

- class: `GITHUB_AND_NOTION`;
- GitHub documentation record: PR #318;
- Notion targets: Crystal Project Hub and Crystal Deep Audit — 2026-08-06;
- immutable merge/CI/benchmark evidence is synchronized; transient branch status is not
  duplicated as long-lived project truth.

## 2026-08-05 — Connectorless GitHub → Notion hand-off

### Scope

PR #312 clarifies how material Crystal analysis and implementation work is preserved when
the originating AI agent does not have direct Notion connector access.

### Verified baseline

- base: `main@027c7359c883c458e99bbea77ea3e84b1619c780`;
- branch: `agent/notion-connectorless-handoff`;
- verified runtime checkpoint remains
  `f91299c44a1a1850fa516f3abb96c916326f7a8c` (PR #302);
- this change is documentation/governance only.

### Findings / decisions

- The existing protocol correctly required GitHub to be independently auditable, but
  treated unavailable Notion access mainly as `BLOCKED`.
- Not every AI agent has a Notion connector; losing or postponing the analysis itself is
  therefore unacceptable.
- GitHub must contain complete public technical/audit continuity: implemented contracts,
  material findings, known risks, exact evidence and next actions.
- Notion remains the deeper rationale, alternatives, grant context and synchronized
  project-history layer.
- The systems do not need sentence-for-sentence duplication. They must preserve the same
  decision-bearing facts and evidence.
- Missing connector status is `HANDOFF_REQUIRED`, not a generic information dead end.
- `BLOCKED_PRIVACY_OR_PERMISSION` is reserved for a real permission, privacy or
  unresolved-target problem.

### Changes

- added `docs/ai/NOTION_HANDOFF.md` with access states, connectorless procedure,
  connected-actor completion procedure and a structured queue template;
- updated `AGENTS.md` with the GitHub completeness invariant;
- expanded `docs/DOCUMENTATION_SYNC_PROTOCOL.md` to cover material audits as well as
  implementation work;
- updated `docs/ai/README.md` with separate connected and connectorless paths;
- expanded the PR template with Notion access, synchronization status and hand-off path;
- linked the route from `docs/DOCUMENTATION_MAP.md`.

### Validation

PR #312 is the mutable record for final head, CI and merge state. The branch changes only
Markdown documentation and the PR template. Full Crystal CI is required before merge.

### Remaining

- synchronize the same connectorless rule into the Crystal Notion protocol/history pages;
- run all nine Crystal CI jobs;
- merge only after CI succeeds and Notion synchronization is recorded;
- use the hand-off queue for future agents without a connector.

### Synchronization

- class: `GITHUB_AND_NOTION`;
- GitHub record: PR #312 and `docs/ai/NOTION_HANDOFF.md`;
- target Notion records: `🔄 Crystal — Code ↔ Documentation Sync Protocol` and
  `🤖 Crystal — AI Agent Context & Audit Hand-off`;
- originating actor Notion access: `AVAILABLE`;
- pre-merge status: `PLANNED` until those records are updated.

---

## 2026-08-05 — AI context navigation and audit hand-off

### Scope

PR #311 creates a compact, mandatory orientation layer for AI coding agents and
automated auditors without changing Crystal runtime behavior.

### Verified baseline

- `main` before this work: `8d576e1342f40d9a823885f9dcce4b1ff16d113a`.
- Verified runtime checkpoint remains
  `f91299c44a1a1850fa516f3abb96c916326f7a8c` (PR #302).
- Runtime evidence at that checkpoint: 1853 passed / 12 skipped on Python 3.11 and
  3.12, 100% measured line coverage, 7/7 declared targeted Ring Zero mutants killed,
  nine CI jobs.

### Findings / decisions

- Existing `AGENTS.md`, `docs/REVIEWER_GUIDE.md`, `docs/DOCUMENTATION_MAP.md`, status
  files and manifest already provide strong reviewer material, but there was no compact
  current-state/risk/component/work-log pack optimized for agent context budgets.
- The new pack is an orientation map, not a competing implementation canon.
- Historical issues and open research PRs must not be treated as current runtime.
- Long-document multi-pass semantic reading is not a verified Crystal runtime component;
  future work must remain source-linked and upstream of normal admission.

### Changes

- added `docs/ai/README.md`;
- added `docs/ai/CURRENT_STATE.md`;
- added `docs/ai/COMPONENT_MAP.md`;
- added `docs/ai/AUDIT_PLAYBOOK.dd`;
- added `docs/ai/KNOWN_RISKS.md`;
- added this `docs/ai/WORK_LOG.md`;
- expanded `AGENTS.md`, README navigation, Documentation Map and PR checklist.

### Validation

PR #311 is the authoritative mutable record for the final branch head, CI jobs and merge
state. The synchronized Notion record stores the final checkpoint after merge. This file
intentionally does not duplicate transient queued/running CI status.

Runtime and historical test-count claims remain tied to the existing verified checkpoint
rather than being re-measured or silently advanced by a documentation-only change.

### Remaining

- keep this pack synchronized through future PRs;
- periodically reconcile stale issues with implemented status;
- review a separate long-document Reader Core RFC before implementation;
- do not merge research PRs solely because they are documentation-only.

### Synchronization

- class: `GITHUB_AND_NOTION`;
- GitHub record: PR #311;
- Notion record: `🤖 Crystal — AI Agent Context & Audit Hand-off`;
- after merge, the Notion record receives final merge SHA, CI evidence and remaining
  limitations.

---

## 2026-08-05 — GitHub ↔ Notion documentation sync contract

### Scope

PR #310 formalized documentation synchronization as part of Crystal's definition of
done.

### Verified baseline

- PR head: `11e6f4b5fbb3423ef9428fc27078728a45922cda`;
- CI workflow run: `30993905461`, conclusion `success`;
- merged commit: `8d576e1342f40d9a823885f9dcce4b1ff16d113a`.

### Changes

- added `docs/DOCUMENTATION_SYNC_PROTOCOL.md`;
- expanded `AGENTS.md`;
- expanded `.github/pull_request_template.md`;
- linked governance from `docs/DOCUMENTATION_MAP.md`.

### Decision

Every material PR now declares `NONE`, `GITHUB_ONLY` or `GITHUB_AND_NOTION` impact.
Notion stores deeper rationale/history but never overrides GitHub implementation truth.

### Validation

CI completed successfully. No runtime code, dependency, coverage threshold, grant
budget or verified runtime checkpoint changed.

### Synchronization

Notion page `🔄 Crystal — Code ↔ Documentation Sync Protocol` was updated after merge
with the final SHA and CI evidence.

---

## 2026-08-01 — Verified runtime checkpoint PR #302

### Scope

Advisory topic facets, scoped curator roles/capabilities and process-local decision
leases on top of the conflict-resolution runtime.

### Verified checkpoint

`f91299c44a1a1850fa516f3abb96c916326f7a8c`.

### Important boundaries

- Topic facets are advisory only.
- Curator authorization is scoped and fail-closed.
- Included decision leases coordinate one process only.
- Physical L3 remains different from strict Canon.

### Evidence

See `TEST_REPORT.md`, `docs/STATUS.md` and
`docs/status/implementation-manifest.json`.
