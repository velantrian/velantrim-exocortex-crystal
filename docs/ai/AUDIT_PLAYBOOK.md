# 🔍 Crystal AI Audit Playbook

This procedure helps agents perform a deep audit without filling the context window with
unstructured repository content.

## Phase 1 — establish the exact target

Record:

- repository and default branch;
- exact `main` SHA;
- PR number, base SHA and head SHA when applicable;
- whether the task concerns runtime, docs, research, grant claims or Notion sync;
- the concrete claim being tested.

Never mix `main`, an open PR and a research issue into one implementation claim.

## Phase 2 — read the compact context

Read, in order:

1. `AGENTS.md`;
2. `docs/ai/README.md`;
3. `docs/ai/CURRENT_STATE.md`;
4. `docs/STATUS.md` and the implementation manifest;
5. the relevant section of `docs/ai/COMPONENT_MAP.md`;
6. `docs/ai/KNOWN_RISKS.md` and recent `WORK_LOG.md` entries.

Only then open component code.

## Phase 3 — classify the claimed reality

For every capability, fill this matrix:

| Question | Evidence |
|---|---|
| Proposed? | issue/RFC/research document |
| Implemented? | file and exact commit |
| Tested? | test names and passing CI run |
| Wired? | concrete runtime caller/composition |
| Enabled? | configuration/profile/default |
| Observed? | named runtime/environment evidence |

A missing row is a limitation, not permission to infer the answer.

## Phase 4 — find the authority owner

Determine which component is allowed to make the decision:

- claim admission → TruthGate;
- structural/safety validation → Guardian;
- strict read membership → CanonicalView/TrustSnapshot;
- contradiction disposition → explicit curator resolution path;
- actor permission → curator authorization;
- proof → TRACE/Receipt/audit contract;
- navigation labels → TopicFacet only;
- strategy/history → Notion, without runtime authority.

Flag any second, implicit or bypassing owner.

## Phase 5 — inspect producers, consumers and side effects

Do not audit only the changed file.

For every changed contract, search for:

- constructors and factories;
- enum/value exhaustive maps;
- serializers/deserializers;
- CLI/HTTP/MCP adapters;
- storage schemas and migrations;
- background workers or lifecycle hooks;
- tests that freeze old behavior;
- docs and manifests that repeat the claim.

Ask:

```text
Who produces this value?
Who consumes it?
Who persists it?
Who authorizes it?
Who can replay or reverse it?
What happens after interruption?
```

## Phase 6 — verify trust boundaries adversarially

Attempt to disprove the expected behavior.

### Admission

- Can model output or retrieval relevance become independent evidence?
- Can a public query mutate canonical state?
- Can an internal helper bypass TruthGate or Guardian?
- Can a failed/rejected transition leave partial audit state?

### Read grounding

- Can restricted, erased, unverified or contested records enter strict results?
- Is physical L3 accidentally treated as strict Canon?
- Does a missing dependency fail open?

### Contradictions

- Does detection silently select a winner?
- Can authorization, scope or lease checks be skipped?
- Can two workers commit conflicting dispositions?

### Proof

- Are TRACE/Receipt identifiers stable and replayable?
- Are uncertainty and refusal reasons preserved?
- Does a crash create a success-looking receipt for a failed mutation?

## Phase 7 — inspect tests and CI as evidence, not decoration

Record:

- exact CI run and conclusion;
- jobs executed and skipped;
- Python/runtime matrix;
- coverage scope and threshold;
- mutation gate scope;
- security/dependency checks;
- docs/status drift checks;
- benchmark environment and comparability.

Do not quote historical test counts as current unless tied to the stated verified
checkpoint.

## Phase 8 — inspect runtime wiring

A class or function existing in `core/` is not proof of active behavior.

Trace:

```text
entry point
  → configuration
  → construction
  → call site
  → authority checks
  → storage/proof effects
  → health/metrics/operator visibility
```

For workers or schedules, verify:

- owner and lifecycle;
- startup/shutdown behavior;
- bounded batches and resource limits;
- idempotency/retry/recovery;
- backlog and failure observability;
- feature-gate/default state.

## Phase 9 — reconcile documents

Compare implementation evidence with:

- README and localized READMEs;
- `TEST_REPORT.md`;
- `docs/STATUS.md`;
- `docs/IMPLEMENTATION_STATUS.md`;
- implementation manifest;
- architecture/RFC/ADR documents;
- grant and roadmap material;
- Notion records when required.

Older issues or RFCs may be stale after later implementation. Do not mechanically copy
them into the current-state report.

## Phase 10 — write the finding

Each finding should contain:

1. severity and confidence;
2. exact affected SHA/PR;
3. claim being tested;
4. code and consumer evidence;
5. test/CI/runtime evidence;
6. impact;
7. minimal safe remediation;
8. proof required to close;
9. documentation/Notion updates required.

Prefer concrete failure paths over abstract warnings.

## Context-budget strategy

```text
compact orientation: 5–15k tokens
  → focused component slice
  → consumers and tests
  → CI/runtime evidence
  → only then broader repository search
```

Do not ingest every historical audit, translation or research document by default.

## Completion checklist

- [ ] Exact baseline and PR refs recorded.
- [ ] Main vs PR vs research separated.
- [ ] Authority owner identified.
- [ ] Producers and downstream consumers checked.
- [ ] Tests and CI inspected.
- [ ] Runtime wiring/configuration checked.
- [ ] Failure/recovery paths considered.
- [ ] Claims reconciled with status/manifest/docs.
- [ ] Documentation impact classified.
- [ ] Notion synchronized when required.
- [ ] `CURRENT_STATE`, `KNOWN_RISKS` or `WORK_LOG` updated when material.
