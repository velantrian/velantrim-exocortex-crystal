# 🧭 Crystal — Audit & Future Work Ledger

**Document role:** authoritative repository ledger for deferred work, open audit questions, research candidates, and explicitly non-authorized future directions.  
**Audience:** AI agents, automated auditors, maintainers, and reviewers.  
**Project:** `velantrian/velantrim-exocortex-crystal`  
**Authority:** this file is an orientation and future-work ledger. It does **not** authorize implementation by itself.

> **Critical rule:** `future work entry != implementation authorization` and `priority != authorization`.

This document exists so a future agent can resume Crystal without reconstructing unfinished questions from old chats, stale PR prose, or historical Notion checkpoints.

---

## 0. How an AI must use this ledger

Before acting on any item in this file:

1. Read [`../../AGENTS.md`](../../AGENTS.md).
2. Read [`README.md`](./README.md), [`CURRENT_STATE.md`](./CURRENT_STATE.md), [`KNOWN_RISKS.md`](./KNOWN_RISKS.md), and the relevant authoritative architecture/status surfaces.
3. Resolve **live GitHub**:
   - current signed `main`;
   - open PRs;
   - open issues;
   - exact CI on relevant heads;
   - review-thread state;
   - current repository rules/governance when the task is governance-related.
4. Compare this ledger with current code, tests, runtime composition, manifests, and status docs.
5. Reclassify stale entries before implementation.
6. Select **at most one bounded scope** only when there is explicit authorization to proceed.
7. Reproduce a suspected defect before selecting a repair when the question is empirical.
8. Treat Notion as a synchronized secondary surface, not runtime proof.

Required audit output for each relevant entry:

```text
DONE
STILL_OPEN
STALE
BLOCKED
NEW_FINDING
NEEDS_REPRODUCTION
NEEDS_ARCHITECTURE_DECISION
NOT_AUTHORIZED
```

If the ledger conflicts with live merged code/tests/CI, **live repository evidence wins** and this file must be reconciled afterward.

---

## 1. Status vocabulary

Use these states exactly enough to avoid accidental scope expansion:

| State | Meaning | May an AI implement automatically? |
|---|---|---|
| `OPEN` | concrete unresolved work with a live evidence basis | **No** — verify scope and authorization first |
| `INVESTIGATE` | question worth auditing or experimenting on | **No** |
| `CANDIDATE` | possible future direction, not selected | **No** |
| `DEFERRED` | intentionally postponed | **No** |
| `BLOCKED` | cannot proceed until a named dependency/gate changes | **No** |
| `NOT_AUTHORIZED` | explicitly outside current implementation authority | **No** |
| `DONE` | completed evidence/history only | not applicable |
| `STALE` | ledger entry no longer matches live truth | not applicable; reconcile first |

A `P0/P1/P2/P3` priority describes **importance if the scope is selected**. It does not grant permission to start it.

---

## 2. Current stop boundary

This ledger deliberately does **not** choose Crystal's next milestone.

```text
completed bounded work
        ↓
STOP
        ↓
live audit + architecture reassessment
        ↓
explicitly select one bounded scope
        ↓
reproduce / preregister when required
        ↓
implementation only if authorized
```

Never infer the next milestone from:

- an item appearing first in this document;
- an item having a high priority;
- an open GitHub issue;
- zero open PRs;
- a completed previous milestone;
- a successful research result;
- a Notion roadmap entry;
- a model/tool becoming available;
- a grant/public narrative.

---

# 3. Concrete open work

## FW-001 — Server-side main governance enforcement

**State:** `OPEN`  
**Priority:** `P1`  
**Implementation authorization:** `GOVERNANCE-ONLY; VERIFY LIVE FIRST`  
**Known tracking issue:** GitHub `#432` at the 2026-08-16 checkpoint  
**Last ledger verification:** 2026-08-16  
**Runtime capability change:** `NO`

### Question

Does GitHub itself enforce Crystal's permanent PR CI gates and review-thread resolution, or is the repository still relying on a stronger manual guarded-merge protocol than the server-side ruleset?

### Why it matters

A manual process can be followed correctly while still leaving the default branch weaker than the documented governance contract. Server-side enforcement should match the invariant the project already claims to use.

### Live evidence to resolve

Inspect the active default-branch ruleset and verify:

- required status-check contexts for the permanent CI suite;
- `required_review_thread_resolution`;
- required approval count;
- bypass actors;
- default-branch coverage;
- whether path-scoped workflows are being incorrectly treated as unconditional required checks.

### Known bounded target from issue #432

At the recorded checkpoint, the intended governance-only target was:

- require the nine permanent PR CI job contexts;
- require review-thread resolution;
- keep required independent approvals at `0` unless a separate review policy is explicitly adopted;
- preserve no-bypass behavior;
- do not alter runtime, Reader, storage, Canon, Guardian, TruthGate, grant, or cross-project behavior.

### Non-goals

- no runtime code;
- no Reader changes;
- no storage/backend activation;
- no independent-review claim merely because threads are resolved;
- no unconditional requirement for a workflow that does not run on every PR.

### Exit criteria

Classify as one of:

- `DONE` — fresh ruleset read-back proves the target configuration;
- `STILL_OPEN` — live rules remain weaker;
- `STALE` — issue/target was superseded by a newer explicit governance decision.

---

# 4. Reader / retrieval research queue

## FW-010 — Reassess proposition-level discrimination after frozen comparator/NLI failures

**State:** `INVESTIGATE`  
**Priority:** `P2`  
**Implementation authorization:** `NOT_AUTHORIZED`  
**Runtime authorization:** `false`

### Question

Is there a bounded, falsifiable next experiment that materially improves proposition-level discrimination while preserving Crystal's authority firewall and avoiding another generic similarity-only stage?

### Existing evidence to re-read

Before proposing anything new, inspect the frozen evidence for:

- RC-9 deterministic lexical baseline;
- Comparator v1 — semantic recall improvement with discrimination gate failure;
- NLI neutral-filter v1 — discrimination improvement with recall-safety failure;
- RRTIC-v1 — frozen typed inspection architecture contract;
- relevant evaluation surfaces, preregistrations, and exact CI/history.

### Required reasoning boundary

The next question is not automatically:

> "Which stronger model should we add?"

It is:

> "What missing discriminative capability is demonstrated by the frozen evidence, and what is the smallest experiment that can falsify a proposed mechanism?"

### Before any experiment

A future AI must:

1. resolve current Reader implementation and live issues;
2. confirm the old evaluation surfaces are still the intended evidence basis;
3. state a new hypothesis that is not merely post-result threshold tuning;
4. define frozen success/failure gates;
5. define authority-violation checks;
6. define non-goals;
7. obtain explicit authorization for a new bounded experiment identity.

### Forbidden automatic transitions

```text
better retrieval score != proposition identity
better NLI label != adjudication
RRTIC suspicion != truth relation
research pass != runtime authorization
model availability != milestone selection
```

### Non-goals

- no semantic/hybrid Reader runtime activation;
- no automatic identity engine;
- no automatic contradiction adjudication;
- no Canon mutation from retrieval/model output;
- no second model/reranker merely because one exists;
- no FTS/ANN/vector infrastructure without a separately measured need.

### Exit criteria

- `DEFERRED_WITH_REASON`, or
- a separately authorized/preregistered experiment, or
- `CLOSED_NO_ACTION` if live evidence no longer supports this line.

---

## FW-011 — Reassess RRTIC-v1 only as a diagnostic contract

**State:** `DEFERRED`  
**Priority:** `P2`  
**Implementation authorization:** `NOT_AUTHORIZED`

### Question

Does any future experiment need executable support for the frozen RRTIC-v1 typed inspection contract, or is the architecture-only representation sufficient?

### Mandatory invariant

RRTIC-v1 remains diagnostic/suspicion-only unless a new explicit architecture decision says otherwise.

It must not silently become:

- an evidence-admission engine;
- a truth-relation engine;
- a contradiction resolver;
- a Canon mutation authority;
- an automatic RC-5 registration path.

### Evidence required before reconsideration

A future proposal must point to a measured failure that cannot be tested adequately with the existing bounded research/evaluation surfaces.

---

# 5. Storage and backend future questions

## FW-020 — PostgreSQL / pgvector activation remains demand-driven

**State:** `DEFERRED`  
**Priority:** `P3`  
**Implementation authorization:** `NOT_AUTHORIZED`  
**Current conceptual boundary:** import/equivalence target may exist while active runtime remains SQLite/local-first.

### Question

Has a measured workload, concurrency, retrieval, deployment, or durability requirement appeared that the active local-first SQLite path cannot satisfy within Crystal's intended envelope?

### Do not start from technology preference

The existence of PostgreSQL/pgvector support, import tooling, tests, or ecosystem popularity is not evidence that activation is needed.

### Required evidence before any activation proposal

At minimum:

- measured workload/problem statement;
- explicit capability gap in the current active backend;
- migration and rollback semantics;
- crash/recovery boundaries;
- processing restriction / erasure behavior;
- operator observability;
- compatibility/equivalence evidence;
- deployment complexity cost;
- grant/public claim impact;
- explicit runtime authorization.

### Non-goals

- no "turn it on because it is more scalable" change;
- no pgvector activation as a shortcut to semantic Reader authorization;
- no remote database becoming Canon authority by deployment accident.

---

## FW-021 — Backend identity and restart continuity audit family

**State:** `INVESTIGATE`  
**Priority:** `P2`  
**Implementation authorization:** `AUDIT_ONLY UNTIL A DEFECT IS REPRODUCED`

### Context

The Outbox `auto` backend restart-switch defect was reproduced and repaired in the bounded #434 / PR #433 workstream. That closure should be treated as evidence for an **audit family**, not as permission to redesign all backend registries.

### Future audit questions

When touching another environment-sensitive persistent backend selector, ask:

- Is backend identity persistent across restart?
- Can availability probing silently select a different persistence domain?
- Can pending/durable state become invisible after restart?
- Is there a migration path or a fail-closed operator signal?
- Are explicit programmatic/test selections separate from deployment identity?
- Are profile/marker I/O failures fail-closed?
- Are first-writer races bounded and deterministic?

### Required method

```text
static suspicion
    ↓
deterministic reproduction
    ↓
violated invariant
    ↓
bounded issue
    ↓
minimal repair
```

Do not generalize the Outbox repair to unrelated registries without reproducing an equivalent failure.

---

# 6. Recovery, crash, and operator-observability audit queue

## FW-030 — Re-audit partial-failure and restart windows when persistence paths change

**State:** `INVESTIGATE`  
**Priority:** `P2`  
**Implementation authorization:** `AUDIT-TRIGGERED ONLY`

This is not a standing refactor task. It is a checklist to invoke when a future change affects persistence, secondary synchronization, queues, migrations, or durable state transitions.

For the changed boundary, verify:

1. transaction boundary;
2. partial failure behavior;
3. idempotency and retry;
4. crash window and restart recovery;
5. concurrency/fencing/race behavior;
6. restriction and erasure behavior;
7. operator-visible failure signal;
8. bounded resource growth;
9. stale/corrupt durable record behavior;
10. whether a failed operation can leave a success-looking Receipt/TRACE surface.

### Non-goal

Do not invent a generic distributed transaction framework unless a reproduced failure requires it.

---

## FW-031 — Recovery observability should remain proportional to real operator need

**State:** `CANDIDATE`  
**Priority:** `P3`  
**Implementation authorization:** `NOT_AUTHORIZED`

### Question

Are there real recovery states that an operator cannot distinguish safely from healthy/idempotent states using existing logs/status/inspection surfaces?

### Evidence required

A proposal should cite a concrete operational ambiguity or reproduced incident. "More dashboards would be useful" is not enough.

### Possible dimensions to inspect

- backend identity/profile state;
- pending recovery count;
- repeated retry/failure class;
- stale recovery records;
- fail-closed startup condition;
- last successful drain/reconciliation evidence.

No metrics subsystem, daemon, dashboard, or telemetry dependency is authorized by this entry.

---

# 7. Documentation and localization queue

## FW-040 — Localized documentation parity remains maintainer-controlled

**State:** `DEFERRED`  
**Priority:** `P3`  
**Implementation authorization:** `SEPARATE DOCS SCOPE ONLY`

### Boundary

English implementation/current-truth documentation is the source language. Localized documents remain valid only to their recorded translation checkpoints.

### Future audit question

Which localized documents are materially stale relative to current English meaning, and which can safely remain historical until a dedicated parity pass?

### Required method

- read `docs/LOCALIZATION_POLICY.md`;
- read `docs/TRANSLATION_STATUS.md`;
- update source meaning first;
- do not mix broad translation churn into a bounded runtime fix;
- do not claim parity until checked.

### Non-goal

No automatic bulk translation sweep merely because English documentation changed.

---

## FW-041 — Keep AI navigation and future-work surfaces discoverable

**State:** `OPEN_AS_MAINTENANCE_RULE`  
**Priority:** `P2`  
**Implementation authorization:** `DOCS MAINTENANCE`

When the documentation architecture materially changes, preserve a discoverable path:

```text
README.md
   ↓
docs/ai/README.md
   ↓
CURRENT_STATE / STATUS / manifest
   ↓
AUDIT_AND_FUTURE_WORK.md
   ↓
relevant risks / architecture / evidence
```

If this ledger is renamed, split, or superseded, update the AI router in the same change.

---

# 8. Grant and public-truth queue

## FW-050 — Periodic grant/public claim reconciliation

**State:** `INVESTIGATE WHEN PUBLIC CLAIMS CHANGE`  
**Priority:** `P2`  
**Implementation authorization:** `DOCS / CLAIM-AUDIT ONLY`

### Question

Do README, grant roadmap, public status, and Notion public-facing summaries still describe implemented/authorized reality without inflating research evidence or submitted funding into awarded capability?

### Permanent boundaries

```text
grant submission != grant award
research evidence != runtime capability
planned module != implemented module
implemented code != enabled runtime
retrieval quality != epistemic authority
```

### Trigger conditions

Run this audit when:

- a grant decision changes;
- a public capability is enabled/disabled;
- a research result is promoted into runtime;
- a major architecture boundary changes;
- README/public project positioning changes materially.

Do not perform repetitive cosmetic claim audits after every mechanical PR.

---

# 9. Cross-project boundary

## FW-060 — Cross-project ideas are references, not inheritance

**State:** `PERMANENT_BOUNDARY`  
**Priority:** `P1`  
**Implementation authorization:** `NOT_AUTHORIZED BY REFERENCE`

Crystal may inspect other Velantrim projects when explicitly useful, but:

```text
cross-project reference != authority transfer
similar concept != shared contract
shared author != shared runtime
research result elsewhere != Crystal implementation permission
```

Do not import architecture, code, governance, Canon semantics, autonomy, identity, or runtime authority from Titan, Native Kernel, Mentaury Soul, Continuum/IDPS, or another repository without a separate Crystal decision.

---

# 10. Explicitly forbidden auto-work

The following are **not** selected merely because they appear interesting or adjacent:

- semantic/hybrid Reader runtime;
- new NLI/CrossEncoder/LLM judge in the Reader runtime;
- RRTIC runtime provider;
- automatic proposition identity;
- automatic contradiction adjudication;
- FTS/ANN/vector Reader activation;
- PostgreSQL/pgvector activation;
- Canon/Guardian/TruthGate authority expansion;
- autonomous background Canon mutation;
- queue federation or distributed coordinator;
- new recovery daemon;
- broad dependency expansion;
- cross-project runtime bridge;
- grant capability expansion;
- mass localization refresh;
- independent-review claims without an actual independent reviewer.

Any of these requires its own live evidence, bounded decision, explicit authorization, tests/evaluation, and documentation reconciliation.

---

# 11. Recommended audit order for a future AI

This order is for **inspection efficiency**, not implementation priority:

```text
1. live main + signature + CI
2. open PRs and issues
3. AGENTS.md + docs/ai/README.md
4. CURRENT_STATE + STATUS + implementation manifest
5. this future-work ledger
6. KNOWN_RISKS + WORK_LOG
7. relevant code/tests/runtime composition
8. relevant architecture/evaluation evidence
9. Notion synchronized checkpoint
10. classify each ledger entry
```

Then report:

```text
A. What is still open?
B. What was already completed elsewhere?
C. What became stale?
D. What needs reproduction rather than implementation?
E. What remains explicitly not authorized?
F. Is there enough evidence to select one next bounded milestone?
```

If the answer to F is no, **STOP with an audit report**. Do not manufacture a next milestone.

---

# 12. Entry template for future additions

Use this shape for new entries:

```markdown
## FW-XYZ — Short title

**State:** `OPEN | INVESTIGATE | CANDIDATE | DEFERRED | BLOCKED | NOT_AUTHORIZED`  
**Priority:** `P0 | P1 | P2 | P3`  
**Implementation authorization:** `...`  
**Tracking issue:** `#... | none`  
**Last verified:** `YYYY-MM-DD`

### Question
What exactly remains unknown or unfinished?

### Why it matters
What invariant, measured limitation, operational risk, or project goal makes this worth keeping?

### Existing evidence
What code/tests/CI/issues/evaluations already constrain the answer?

### Required before implementation
What must be reproduced, measured, decided, or authorized first?

### Non-goals
What must this scope not silently expand into?

### Exit criteria
How does the future auditor classify this as DONE, DEFERRED, BLOCKED, or separately authorized?
```

Do not add vague entries such as "improve AI", "make retrieval better", "add scalability", or "optimize architecture". Every entry must preserve a bounded question and a falsifiable or auditable exit condition.

---

# 13. Maintenance contract

Update this ledger when one of these happens:

- a listed issue closes or materially changes;
- a candidate is explicitly selected as a milestone;
- a research question is answered;
- a known risk is retired or becomes a reproduced defect;
- a future direction is explicitly rejected;
- a documentation/navigation change would make this ledger undiscoverable.

Do **not** update it for every SHA or mechanical dependency bump. Volatile provenance belongs in GitHub/CI/status history.

When an item is completed, prefer either:

1. mark it `DONE` with a short pointer to immutable evidence, then later compact it during a dedicated ledger-maintenance pass; or
2. remove it only when its historical value is already preserved elsewhere and removal cannot make future audits ambiguous.

---

## Final invariant

```text
This file remembers what may deserve attention.
It does not decide what Crystal is allowed to build next.
```
