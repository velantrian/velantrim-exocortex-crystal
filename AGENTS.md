# AGENTS.md — mandatory Crystal agent contract

This file applies to AI coding agents, automated auditors and human contributors in the
entire repository.

Crystal is a public, grant-facing, local-first verifiable memory infrastructure. Work
must preserve its evidence, authority, privacy and proof boundaries.

## 1. Required reading before work

Do not begin by scanning the whole repository.

Read in this order:

1. [`README.md`](README.md) — public purpose and capability boundary.
2. [`docs/ai/README.md`](docs/ai/README.md) — compact AI-agent entry point.
3. [`docs/ai/CURRENT_STATE.md`](docs/ai/CURRENT_STATE.md) — current main, verified
   checkpoint, open PRs and non-implemented work.
4. [`docs/STATUS.md`](docs/STATUS.md) and
   [`docs/status/implementation-manifest.json`](docs/status/implementation-manifest.json)
   — exact verified evidence.
5. [`docs/ai/COMPONENT_MAP.md`](docs/ai/COMPONENT_MAP.md) — relevant authority owner,
   files and tests.
6. [`docs/ai/KNOWN_RISKS.md`](docs/ai/KNOWN_RISKS.md) and recent entries in
   [`docs/ai/WORK_LOG.md`](docs/ai/WORK_LOG.md).
7. [`docs/ai/NOTION_HANDOFF.md`](docs/ai/NOTION_HANDOFF.md) when Notion access is
   unavailable or a pending synchronization item exists.
8. [`docs/ai/AUDIT_PLAYBOOK.md`](docs/ai/AUDIT_PLAYBOOK.md) when auditing or reviewing.
9. Relevant architecture, ADR, code, tests, CI and runtime composition.

Use documentation as an orientation map. Verify material claims against current code,
consumers, tests, workflows and configuration.

## 2. What this repository is

Velantrim Exo-Cortex Crystal is a local-first, pure-standard-library-by-default memory,
evidence and decision-boundary runtime for trustworthy AI systems.

It stores typed source-grounded claims, applies explicit epistemic states, admits trusted
knowledge through TruthGate and Guardian boundaries, reconciles strict read views, and
emits TRACE/Receipt proof artifacts.

This is the public Crystal core. It is not automatically Titan, Full Exo-Cortex,
Personal Exo-Cortex, Mentaury, Native Kernel or Research Mode.

## 3. Source-of-truth hierarchy

For implemented behavior, prefer:

```text
merged GitHub main code
  → executable tests and CI
  → runtime composition/configuration
  → TEST_REPORT and implementation manifest
  → STATUS / IMPLEMENTATION_STATUS
  → accepted architecture and ADRs
  → README/reviewer summaries
  → docs/ai orientation pack
  → PRs/issues/roadmaps/research docs
  → Notion rationale and history
```

Notion is strategy, rationale, grant context and synchronized history. It is not runtime
proof.

## 4. Exact status language

Keep these states separate:

- `PROPOSED` — issue, RFC or research only;
- `IMPLEMENTED` — code exists;
- `TESTED` — named tests pass at an exact SHA;
- `WIRED` — composed into the intended runtime path;
- `ENABLED` — active under the relevant configuration;
- `OBSERVED` — demonstrated in a named runtime;
- `VERIFIED_CHECKPOINT` — exact commit with recorded evidence.

A file existing does not prove wiring, enablement, observation or production readiness.

## 5. Non-negotiable trust boundaries

### Physical graph and strict Canon

- Physical L3 is a multi-status graph, not automatically strict Canon.
- Strict read membership is derived through immutable deny-dominant reconciliation.
- Restricted, erased, unverified or contested content must not leak into strict
  grounding.

### Admission

- TruthGate owns epistemic admission policy.
- Guardian owns structural and safety constraints.
- Do not add a second implicit owner or bypass either boundary.
- Model output, retrieval rank, confidence or topic relevance is not independent
  evidence.

### Query/read paths

- Public HTTP, CLI and MCP query/search surfaces remain read-only with respect to
  canonical truth state.
- Flag any query, retrieval, ranking, answering or background read path that creates,
  reinforces, promotes, demotes, restricts or otherwise mutates Canon.

### Contradictions

- Detection does not select a winner.
- Resolution requires the explicit audited `COEXIST`, `CONTEXTUALIZE` or `SUPERSEDE`
  path with scoped authorization.
- Do not introduce silent last-write-wins or last-verified-wins semantics.

### Topic facets

- TopicFacet metadata is advisory navigation only.
- It cannot change evidence, ESM state, contradiction disposition, TruthGate results or
  Canon membership.

### TRACE, Receipt and audit

- Proof artifacts are part of the contract, not optional presentation.
- A failed or rejected mutation must not create a success-looking receipt.
- Preserve replayability, policy/evidence refs and uncertainty/refusal reasons.

## 6. Producer and consumer review

For every contract or enum change, inspect:

- producers and factories;
- downstream consumers and exhaustive mappings;
- serializers/deserializers;
- CLI, HTTP and MCP adapters;
- storage/migration code;
- runtime composition and configuration;
- tests freezing compatibility and failure behavior;
- docs/status/manifest claims.

Do not approve a changed type only because its defining module is correct.

## 7. Storage, concurrency and recovery

For durable mutations or workers, document and test:

- transaction boundary and partial-failure behavior;
- idempotency and retry semantics;
- crash windows and recovery;
- concurrency/CAS/fencing rules;
- erasure and restriction propagation;
- operator observability;
- bounded resource use.

The current curator lease registry is process-local. Do not claim distributed
coordination without an explicit external adapter and proof.

## 8. Long-document reading boundary

Crystal does not currently claim a verified dedicated multi-pass Reader Core.

Any future Semantic Reading Layer must:

- preserve exact source spans and document identity;
- produce source-linked candidate cards, not trusted facts;
- track coverage, exceptions, contradictions and re-read needs;
- remain upstream of ordinary Guardian and TruthGate admission;
- never become a second Canon owner;
- separate extraction confidence, importance and truth confidence.

## 9. Dependency and packaging discipline

- Python >= 3.11.
- Install development extras with `pip install -e '.[dev]'`.
- The default runtime remains pure standard library.
- Do not add mandatory third-party dependencies without an explicit architecture,
  packaging, security and maintenance decision.
- Optional features belong behind extras and documented opt-in boundaries.

## 10. Required validation

Run the relevant subset during development and the repository-prescribed full gates
before merge.

Baseline command:

```bash
pytest tests/ --cov=. --cov-fail-under=100
```

Also inspect the current CI workflow rather than assuming this command covers every gate.
Crystal's verified status includes code quality, Python 3.11/3.12 tests, JSONL integrity,
evaluation, security, Docker, Ring Zero mutation and docs-status jobs.

Do not advance test counts or the verified runtime checkpoint without regenerating the
prescribed evidence and synchronized status surfaces.

## 11. Claims discipline

Avoid unsupported claims about:

- universal truth;
- zero hallucinations;
- legal GDPR/security certification;
- production-ready multi-tenant deployment;
- distributed locking;
- AGI, consciousness or a living digital mind;
- research modules as current runtime;
- grant award or funded delivery without verified status.

Defer exact capability/status claims to code, tests, `TEST_REPORT.md`, the implementation
manifest and CI.

## 12. Documentation synchronization and Notion access

Every change follows
[`docs/DOCUMENTATION_SYNC_PROTOCOL.md`](docs/DOCUMENTATION_SYNC_PROTOCOL.md) and
classifies impact as `NONE`, `GITHUB_ONLY` or `GITHUB_AND_NOTION`.

Use `GITHUB_AND_NOTION` for new modules, technologies, durable decisions, authority or
privacy changes, grant/roadmap changes, cross-project boundaries, deployment changes, or
implementation/rejection of a documented plan.

### GitHub completeness invariant

Not all AI agents have a Notion connector. Therefore:

- GitHub must contain the complete public technical contract, material audit findings,
  known risks, exact evidence and next actions needed to continue the work;
- no implemented behavior, safety boundary, unresolved risk or required engineering
  action may exist only in Notion;
- Notion may contain deeper rationale, alternatives, grant context and historical detail,
  but it must not be a required dependency for understanding or auditing Crystal;
- do not duplicate every sentence across both systems: synchronize the decision-bearing
  facts and evidence needed to prevent drift or loss.

### When Notion is available

- read the related record when the change is `GITHUB_AND_NOTION`;
- update GitHub and Notion in the same work cycle;
- after merge, add the final merge SHA, CI/checkpoint evidence, limitations and next
  actions to Notion.

### When Notion is unavailable

Do not stop a valid analysis merely because the agent lacks a connector.

1. Complete the analysis and public technical documentation in GitHub.
2. Update the relevant `docs/ai/*` surfaces and add a compact entry to `WORK_LOG.md`.
3. For `GITHUB_AND_NOTION`, add a structured item to
   [`docs/ai/NOTION_HANDOFF.md`](docs/ai/NOTION_HANDOFF.md).
4. Set PR metadata to `Notion access: UNAVAILABLE` and
   `Notion synchronization: HANDOFF_REQUIRED`.
5. Do not claim that Notion was updated.
6. Keep a `GITHUB_AND_NOTION` implementation PR draft until a connected human or AI
   completes the required Notion synchronization.

Use `BLOCKED_PRIVACY_OR_PERMISSION` only when the hand-off cannot be completed safely,
the target record cannot be identified, or permissions/privacy prevent synchronization.
A missing connector alone is `HANDOFF_REQUIRED`, not an information dead end.

Never publish private workspace content, private URLs, secrets, personal information or
private datasets in this public repository.

### Active documentation language policy

English is the sole authoritative working language for Crystal engineering and documentation.

- Write and review implementation, architecture, ADR, status, test, security, grant,
  roadmap and `docs/ai/*` material in English first.
- Maintain `README.md` as the authoritative public capability contract.
- Keep localized top-level READMEs as concise non-authoritative orientation summaries,
  not complete mirrors of the documentation corpus.
- Locale indexes may route readers to selected best-effort onboarding snapshots, but must
  warn that current capability, security, grant and runtime truth remains in English.
- Do not update all translations inside ordinary implementation PRs. Merge and verify the
  English baseline first, then use a dedicated docs-only localization PR when public
  summaries materially need reconciliation.
- Record the exact English source checkpoint in each localized README and locale index.
- Preserve stable API identifiers and exact non-claims; never introduce stronger claims in
  translation.
- Follow [`docs/LOCALIZATION_POLICY.md`](docs/LOCALIZATION_POLICY.md). CI must validate the
  selective localization contract without requiring full-corpus translation.

## 13. AI context-pack maintenance

Update the compact pack when material:

- `docs/ai/CURRENT_STATE.md` — current implementation/wiring/status changed;
- `docs/ai/COMPONENT_MAP.md` — ownership, files or tests changed;
- `docs/ai/KNOWN_RISKS.md` — a risk was discovered, changed or closed;
- `docs/ai/WORK_LOG.md` — significant work or hand-off completed;
- `docs/ai/NOTION_HANDOFF.md` — Notion is required but unavailable, or a pending hand-off
  was synchronized;
- `docs/ai/AUDIT_PLAYBOOK.md` — audit procedure changed.

Do not turn `WORK_LOG.md` into a dump of every commit. Record only decisions, evidence,
limitations and next actions.

## 14. PR and stacked-change discipline

- Keep PRs small and independently reviewable.
- Each PR must be green on its own; do not hide a lower-PR defect in a later stacked PR.
- Record exact base/head SHAs and CI evidence.
- Open PRs and issues are non-authoritative until merged.
- Documentation-only does not mean risk-free: check public claims, grant boundaries,
  links, status drift and conflicts with concurrent documentation PRs.

## 15. Primary navigation

- `docs/ai/README.md` — AI entry point.
- `docs/ai/NOTION_HANDOFF.md` — connectorless Notion synchronization queue and procedure.
- `docs/REVIEWER_GUIDE.md` — canonical external reviewer route.
- `docs/DOCUMENTATION_MAP.md` — documentation hierarchy and reader routes.
- `docs/DOCUMENTATION_SYNC_PROTOCOL.md` — GitHub/Notion completion contract.
- `docs/LOCALIZATION_POLICY.md` — English-first selective localization contract.
- `docs/ARCHITECTURE.md` — architecture and memory/backend/privacy boundaries.
- `docs/EVAL.md` — evaluation metrics and gates.
- `TEST_REPORT.md` — exact verification evidence.
- `DEMO.md` and `docs/DEMO.md` — verified command examples.
- `CONTRIBUTING.md` — contributor workflow.
