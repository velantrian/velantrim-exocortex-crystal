# 🧭 Crystal — Audit & Future Work Ledger

**Document role:** authoritative repository ledger for deferred work, open audit questions, research candidates, and explicitly non-authorized future directions.  
**Audience:** AI agents, automated auditors, maintainers, and reviewers.  
**Project:** `velantrian/velantrim-exocortex-crystal`  
**Default branch:** `main`  
**Authority:** orientation / audit / future-work ledger only; it does **not** authorize implementation.  
**Last live reconciliation:** 2026-08-17  
**Audited repository checkpoint:** `main@31e529cf1269619778449f7f5228b83b184caa56`  
**Current-state / implementation owner:** `docs/status/implementation-manifest.json` + current code/tests/runtime composition  
**Notion mirror:** `🤖 Crystal — AI Agent Context & Audit Hand-off`

> **Critical rule:** `future work entry != implementation authorization` and `priority != authorization`.
>
> **DO NOT AUTO-SELECT NEXT MILESTONE.**
>
> Audit order, open Issues, research candidates, successful experiments, empty PR queues, technology availability, and Notion roadmap entries do not select or authorize implementation.

This document exists so a future AI can resume Crystal without reconstructing unfinished questions from old chats, stale PR prose, or historical Notion checkpoints.

---

## 0. How an AI must use this ledger

Before acting on any item:

1. Read [`../../AGENTS.md`](../../AGENTS.md).
2. Read [`README.md`](./README.md), [`CURRENT_STATE.md`](./CURRENT_STATE.md), [`KNOWN_RISKS.md`](./KNOWN_RISKS.md), the machine implementation manifest, and the relevant accepted architecture/status surfaces.
3. Resolve live GitHub: signed `main`, open PRs, open Issues, exact CI, review threads, and live rules/governance when relevant.
4. Resolve implementation truth from current code + tests + exact CI + runtime configuration/composition.
5. Reconcile this ledger against those owners before treating a dated entry as current.
6. Reproduce a suspected defect before selecting a repair when the question is empirical.
7. Select at most one bounded implementation scope only under separate explicit authorization.
8. Treat Notion as synchronized secondary context, not runtime proof.

Required audit classifications may include:

```text
DONE
STILL_OPEN
INVESTIGATE
CANDIDATE
DEFERRED
BLOCKED
NOT_AUTHORIZED
STALE
SUPERSEDED
NEEDS_REPRODUCTION
NEEDS_ARCHITECTURE_DECISION
NEW_FINDING
```

Do not force repository-local vocabulary into a different ecosystem label when the local meaning is more precise.

---

## 1. Fresh live checkpoint — 2026-08-17

Fresh reconciliation established:

```text
live main:                         31e529cf1269619778449f7f5228b83b184caa56
main signature:                    VERIFIED / valid
open PRs:                          0
exact-main CI:                     31971362495 — SUCCESS
RRTIC-v1:                          FROZEN_ARCHITECTURE_CONTRACT
Reader runtime authorization:      false
semantic/hybrid Reader runtime:    false
NLI Reader runtime filter:         false
RRTIC runtime provider:            false
dedicated Reader core:             false
SQLite ordinary local-first:       active
PostgreSQL/pgvector runtime:        inactive / false
```

Live governance remains weaker than the documented guarded-merge protocol:

```text
ruleset: crystal-main-governance / 20602128
state: active
scope: ~DEFAULT_BRANCH
required approvals: 0
required review-thread resolution: false
required status-check rule: absent
bypass actors: none
current user bypass: never
Issue #432: OPEN
```

Therefore FW-001 is fresh and remains `OPEN / STILL_OPEN`.

The bounded Outbox restart-continuity defect is historical closure evidence:

```text
Issue #434: CLOSED / completed
PR #433: MERGED
```

That work remains a precedent for FW-021. It is **not** authorization to redesign other backend registries.

No fresh live evidence in this audit selects a new Reader experiment, PostgreSQL activation, RRTIC runtime provider, recovery daemon, or other implementation milestone.

**Runtime changed by this reconciliation:** NO.  
**Authority changed by this reconciliation:** NO.

### Evidence anchors

- `main@31e529cf1269619778449f7f5228b83b184caa56`
- exact-main CI run `31971362495`
- machine implementation surface `docs/status/implementation-manifest.json`
- live ruleset `20602128`
- live Issue #432
- closed Issue #434 + merged PR #433

### Global revalidation triggers

Re-run relevant ledger audits when any of these change:

- newer `main` touches the owning Reader, storage, queue, migration, Canon/Guardian/TruthGate, runtime, or governance surfaces;
- a listed Issue/PR closes, reopens, or is superseded;
- an accepted architecture contract / ADR changes;
- the implementation manifest changes an authorization/capability field;
- runtime/backend activation changes;
- a new explicit Owner/maintainer authorization selects a bounded scope;
- grant/public status changes where the claim queue is concerned.

---

## 2. Permanent epistemic and authority rules

These are not implementation suggestions:

```text
retrieval != evidence
similarity != identity
NLI label != proposition identity
NLI contradiction != contradiction adjudication
RRTIC suspicion != adjudicated relation
qualifier mismatch != truth decision
research pass != runtime authorization
implementation presence != runtime activation
submitted grant != awarded grant
```

Reader discovery/inspection remains upstream of ordinary evidence admission and Canon authority. RRTIC-v1 is diagnostic/suspicion-only unless a later explicit architecture decision changes that contract.

---

# 3. Concrete open governance work

## FW-001 — Server-side main governance enforcement

**State:** `OPEN / STILL_OPEN`  
**Priority:** `P1`  
**Suggested audit sequence:** 1  
**Implementation authorized:** NO by this ledger; governance-only scope requires separate action  
**Runtime capability change:** NO  
**Authority impact:** repository merge-governance only if later explicitly changed  
**Known Issue / PR:** Issue #432  
**Last verified:** 2026-08-17  
**Evidence anchor:** live ruleset `20602128` + Issue #432 + `main@31e529cf...`  
**Revalidation trigger:** ruleset update; Issue #432 lifecycle; workflow/context rename; branch-governance decision.

### Question
Does GitHub itself enforce Crystal's permanent PR CI gates and review-thread resolution, or is manual guarded merge still stronger than server-side rules?

### Why it matters
A correctly followed manual process can coexist with a weaker server-side merge gate.

### Current evidence
The active default-branch ruleset still requires PR use but has `required_review_thread_resolution=false`, zero required approvals, no required-status-check rule, and no bypass actors. Issue #432 remains open.

### Files / components to inspect
`.github/workflows/ci.yml`, live ruleset payload, branch/rules governance, and any accepted governance documentation.

### Required audit
Verify permanent always-on PR check contexts separately from path-scoped workflows. Do not make a path-scoped workflow an unconditional required context unless its trigger contract is separately changed.

### Required experiment / reproduction
Optional bounded test PR only if needed to prove enforcement behavior.

### Preconditions
Fresh ruleset read-back and current workflow context names.

### Non-goals
No runtime, Reader, storage, Canon, Guardian, TruthGate, grant, or cross-project change; no independent-review policy implied by thread resolution.

### Authority boundaries
Required approval count remains a separate governance decision. `0 unresolved threads != independent review`.

### Falsification / closure condition
`DONE` only if fresh server-side read-back proves the intended permanent checks and review-thread resolution are actually enforced. Otherwise remain open or mark superseded by a newer explicit governance decision.

### Exit criteria
Evidence-bound `DONE / STILL_OPEN / SUPERSEDED` classification.

### Possible outcomes
`DONE`, `STILL_OPEN`, `SUPERSEDED`, `BLOCKED`.

---

# 4. Reader / retrieval research queue

## FW-010 — Proposition-level discrimination after frozen comparator/NLI failures

**State:** `INVESTIGATE`  
**Priority:** `P2`  
**Suggested audit sequence:** 2  
**Implementation authorized:** NO  
**Runtime capability change:** NO  
**Authority impact:** NONE  
**Known Issue / PR:** no new active implementation scope established by the 2026-08-17 live audit  
**Last verified:** 2026-08-17  
**Evidence anchor:** machine manifest + RC-9 / Comparator v1 / NLI neutral-filter v1 / RRTIC-v1 frozen evidence  
**Revalidation trigger:** Reader evaluation contract/result change; new bounded experiment authorization; Reader runtime/architecture change.

### Question
Is there a bounded, falsifiable next experiment that materially improves proposition-level discrimination while preserving Crystal's authority firewall and avoiding another generic similarity-only stage?

### Why it matters
The frozen results demonstrate different trade-offs; they do not prove that a stronger model or another reranker is the next correct mechanism.

### Current evidence
Re-read before proposing work:

- RC-9 deterministic lexical baseline — implemented;
- Comparator v1 — semantic recall recovered while discrimination gate failed;
- NLI neutral-filter v1 — discrimination improved while recall-safety gate failed;
- RRTIC-v1 — frozen typed diagnostic architecture contract;
- runtime authorization remains false.

### Alternative explanations
The missing capability may be data/fixture discrimination, typed inspection, qualifier handling, evaluation design, or no currently justified runtime mechanism at all.

### Files / components to inspect
Frozen evaluation artifacts/preregistrations, Reader architecture contracts, implementation manifest, Reader tests, and exact historical CI.

### Required audit
Ask first: **what capability gap is demonstrated?** Do not start with “which model should be added?”.

### Required experiment / reproduction
Only a separately authorized experiment with a preregistered hypothesis, frozen success/failure gates, authority-violation checks, and non-goals.

### Preconditions
Current Reader implementation/evaluation surfaces must still be the intended evidence basis.

### Non-goals
No semantic/hybrid Reader runtime activation; automatic identity engine; contradiction adjudication; Canon mutation; generic model/reranker addition; FTS/ANN/vector activation without measured need.

### Authority boundaries
Better retrieval/NLI metrics remain non-authoritative regarding evidence, identity, contradiction resolution, or Canon.

### Falsification / closure condition
Close/defer the line if live evidence no longer demonstrates the gap or if no falsifiable mechanism can be justified.

### Exit criteria
`DEFERRED_WITH_REASON`, `CLOSED_NO_ACTION`, or a separately authorized/preregistered experiment identity.

### Possible outcomes
`INVESTIGATE`, `DEFERRED`, `CANDIDATE`, `NOT_AUTHORIZED`, `NEEDS_REPRODUCTION`.

---

## FW-011 — RRTIC-v1 remains diagnostic/suspicion-only

**State:** `DEFERRED`  
**Priority:** `P2`  
**Suggested audit sequence:** 3  
**Implementation authorized:** NO  
**Runtime capability change:** NO  
**Authority impact:** NONE  
**Last verified:** 2026-08-17  
**Evidence anchor:** frozen RRTIC-v1 architecture contract + implementation manifest `rrtic_runtime_provider=false`  
**Revalidation trigger:** explicit RRTIC architecture replacement or separately authorized executable experiment.

### Question
Does any future experiment actually require executable support for RRTIC-v1, or is the frozen diagnostic representation sufficient?

### Current evidence
RRTIC-v1 remains frozen architecture, not a runtime provider.

### Required audit / experiment
A future proposal must cite a measured failure that cannot be tested with existing bounded surfaces.

### Non-goals / authority boundaries
RRTIC must not silently become evidence admission, proposition identity, contradiction resolution, Canon mutation, or automatic RC-5 registration.

### Exit criteria
Remain deferred unless a separately authorized architecture/experiment decision establishes necessity.

---

# 5. Storage and backend questions

## FW-020 — PostgreSQL / pgvector activation remains demand-driven

**State:** `DEFERRED / NOT_AUTHORIZED`  
**Priority:** `P3`  
**Suggested audit sequence:** 4  
**Implementation authorized:** NO  
**Runtime capability change:** NO  
**Authority impact:** NONE  
**Last verified:** 2026-08-17  
**Evidence anchor:** implementation manifest: optional/inactive PostgreSQL import/equivalence exists; active runtime remains SQLite/local-first; pgvector runtime false  
**Revalidation trigger:** measured workload gap; backend/runtime authorization change; migration/recovery contract change.

### Question
Has a measured workload, concurrency, retrieval, deployment, or durability requirement appeared that active local-first SQLite cannot satisfy within Crystal's intended envelope?

### Why it matters
Implementation/import support is not a reason to activate another backend.

### Required evidence before any activation proposal
Measured problem statement; explicit current-backend gap; migration/rollback; crash/recovery; restriction/erasure behavior; operator observability; equivalence; deployment cost; public/grant impact; explicit runtime authorization.

### Non-goals
No technology-preference activation, no pgvector shortcut to semantic Reader authorization, and no remote database becoming Canon authority by deployment accident.

### Exit criteria
Remain deferred unless evidence establishes a bounded need and a separately authorized activation scope.

---

## FW-021 — Backend identity and restart continuity audit family

**State:** `INVESTIGATE`  
**Priority:** `P2`  
**Suggested audit sequence:** 5  
**Implementation authorized:** AUDIT ONLY until an equivalent defect is reproduced  
**Runtime capability change:** NO  
**Authority impact:** NONE  
**Known Issue / PR:** Issue #434 CLOSED/completed · PR #433 MERGED  
**Last verified:** 2026-08-17  
**Evidence anchor:** #434 reproduction/closure + PR #433 bounded repair  
**Revalidation trigger:** changes to another environment-sensitive persistent backend selector; queue profile semantics; restart/recovery behavior.

### Question
For another persistent backend selector, can deployment identity change across restart and silently hide durable state?

### Why it matters
The Outbox defect proved one concrete failure class, but that result does not establish the same defect elsewhere.

### Required method

```text
static suspicion
→ deterministic reproduction
→ violated invariant
→ causal owner
→ bounded issue
→ only then minimal repair
```

### Audit dimensions
Persistent backend identity; availability probing; invisible pending state; migration/fail-closed signal; explicit/test selection separation; marker/profile I/O failure; first-writer races.

### Non-goals
No registry-wide redesign, queue federation, migration framework, dual-write, or distributed coordinator based solely on analogy.

### Exit criteria
For each future target: `NO_EQUIVALENT_DEFECT`, `NEEDS_REPRODUCTION`, or a separately bounded reproduced defect.

---

# 6. Recovery / crash / operator-observability queue

## FW-030 — Re-audit partial-failure and restart windows when persistence paths change

**State:** `INVESTIGATE`  
**Priority:** `P2`  
**Suggested audit sequence:** 6  
**Implementation authorized:** AUDIT-TRIGGERED ONLY  
**Runtime capability change:** NO  
**Authority impact:** NONE  
**Revalidation trigger:** material changes to persistence, secondary synchronization, queues, migrations, or durable state transitions.

For the changed owner verify:

1. transaction boundary;
2. partial failure behavior;
3. idempotency/retry;
4. crash window/restart recovery;
5. concurrency/fencing;
6. restriction/erasure behavior;
7. operator-visible failure signal;
8. bounded resource growth;
9. stale/corrupt durable records;
10. whether failure can leave success-looking Receipt/TRACE state.

**Non-goal:** no generic distributed transaction framework unless a reproduced failure requires it.

---

## FW-031 — Recovery observability proportional to demonstrated operator need

**State:** `CANDIDATE`  
**Priority:** `P3`  
**Suggested audit sequence:** 7  
**Implementation authorized:** NO  
**Runtime capability change:** NO  
**Authority impact:** NONE

### Question
Are there real recovery states that an operator cannot safely distinguish from healthy/idempotent states using current logs/status/inspection surfaces?

### Required evidence
A concrete operational ambiguity or reproduced incident. “More dashboards would be useful” is insufficient.

### Possible audit dimensions
Backend identity/profile state; pending recovery count; repeat failure class; stale recovery records; fail-closed startup; last successful drain/reconciliation.

### Non-goals
No metrics subsystem, daemon, dashboard, or telemetry dependency is authorized here.

---

# 7. Documentation / localization queue

## FW-040 — Localized documentation parity remains maintainer-controlled

**State:** `DEFERRED`  
**Priority:** `P3`  
**Implementation authorized:** separate docs scope only  
**Runtime capability change:** NO

English implementation/current-truth documentation remains the source language. Localized documents are valid only to their recorded checkpoints.

### Required method
Read `docs/LOCALIZATION_POLICY.md` and `docs/TRANSLATION_STATUS.md`; update source meaning first; do not mix broad translation churn into bounded runtime/audit work; do not claim parity until checked.

### Non-goal
No automatic bulk translation sweep.

---

## FW-041 — Keep AI navigation and ledger discoverable

**State:** `OPEN_AS_MAINTENANCE_RULE`  
**Priority:** `P2`  
**Implementation authorized:** docs maintenance only  
**Runtime capability change:** NO

Preserve the project-native route:

```text
README.md
→ docs/ai/README.md
→ CURRENT_STATE / STATUS / implementation manifest
→ docs/ai/AUDIT_AND_FUTURE_WORK.md
→ relevant risks / architecture / evidence
```

If this ledger is renamed/split/superseded, update the AI router in the same docs change.

---

# 8. Grant / public-truth queue

## FW-050 — Periodic grant/public claim reconciliation

**State:** `INVESTIGATE WHEN PUBLIC CLAIMS CHANGE`  
**Priority:** `P2`  
**Implementation authorized:** docs / claim-audit only  
**Runtime capability change:** NO  
**Revalidation trigger:** grant decision; public capability activation/deactivation; research-to-runtime promotion; major architecture/public-positioning change.

Permanent boundaries:

```text
grant submission != grant award
research evidence != runtime capability
planned module != implemented module
implemented code != enabled runtime
retrieval quality != epistemic authority
```

Do not run repetitive cosmetic claim audits after every mechanical PR.

---

# 9. Cross-project boundary

## FW-060 — Cross-project ideas are references, not inheritance

**State:** `PERMANENT_BOUNDARY`  
**Priority:** `P1`  
**Implementation authorized:** NOT_AUTHORIZED BY REFERENCE  
**Runtime capability change:** NO  
**Authority impact:** NONE

```text
cross-project reference != authority transfer
similar concept != shared contract
shared author != shared runtime
research result elsewhere != Crystal implementation permission
```

Do not import Titan, Native Kernel, Mentaury Soul, Mentaury-Kernel, Continuum/IDPS, or another project's architecture, Canon semantics, storage model, identity model, autonomy, governance, or runtime authority without a separate Crystal decision.

---

# 10. Explicitly forbidden auto-work

The following are **not selected** merely because they appear useful or adjacent:

- semantic/hybrid Reader runtime;
- new NLI/CrossEncoder/LLM judge in Reader runtime;
- RRTIC runtime provider;
- automatic proposition identity;
- automatic contradiction adjudication;
- FTS/ANN/vector Reader activation;
- PostgreSQL/pgvector activation;
- Canon/Guardian/TruthGate authority expansion;
- autonomous background Canon mutation;
- queue federation/distributed coordinator;
- new recovery daemon;
- broad dependency expansion;
- cross-project runtime bridge;
- grant capability expansion;
- mass localization refresh;
- independent-review claims without an actual independent reviewer.

Each requires its own current evidence, bounded decision, explicit authorization, validation, and documentation reconciliation.

---

# 11. Suggested future audit order — not implementation order

```text
1. resolve live main + signature + exact CI
2. resolve open PRs/issues + live governance
3. FW-001 server-side governance
4. FW-010 proposition-level discrimination evidence
5. FW-011 RRTIC diagnostic boundary
6. FW-020 backend activation only on measured need
7. FW-021 backend identity/restart audit on trigger
8. FW-030 persistence/recovery windows on trigger
9. FW-031 observability only on demonstrated ambiguity
10. FW-040/FW-050 docs/public truth when triggered
```

Then report:

```text
what is done?
what is still open?
what became stale/superseded?
what requires reproduction?
what remains not authorized?
is there enough evidence to select one bounded milestone?
```

If the last answer is no: **STOP WITH AUDIT REPORT.**

---

# 12. Defect rule

For a suspected defect:

```text
suspicion
→ reproduction
→ prove violated invariant
→ localize causal boundary
→ bound affected owner
→ only then consider repair
```

Never preselect a repair because another backend/component once had a similar failure.

---

# 13. Template for future additions

```markdown
## FW-XYZ — Short title

ID: FW-XYZ
Name: Short title
State: OPEN | INVESTIGATE | CANDIDATE | DEFERRED | BLOCKED | NOT_AUTHORIZED
Priority: P0 | P1 | P2 | P3
Suggested audit sequence: ...
Implementation authorized: NO | bounded explicit value
Runtime capability change: NO | explicit value
Authority impact: NONE | explicit value
Known Issue / PR: ...
Last verified: YYYY-MM-DD
Evidence anchor: main@... / PR / Issue / CI / ADR / manifest / frozen evaluation
Revalidation trigger: ...

### Question
...
### Why it matters
...
### Current evidence
...
### Alternative explanations
...
### Files / components to inspect
...
### Required audit
...
### Required experiment / reproduction
...
### Preconditions
...
### Non-goals
...
### Authority boundaries
...
### Falsification / closure condition
...
### Exit criteria
...
### Possible outcomes
...
```

Do not add vague entries such as “improve AI”, “make retrieval better”, “add scalability”, or “optimize architecture”. Preserve a bounded question and an auditable/falsifiable exit condition.

---

# 14. Maintenance contract

Reconcile this ledger when:

- a listed Issue/PR materially changes;
- a candidate is explicitly selected or rejected;
- a research question receives new evidence;
- a known risk becomes a reproduced defect or is retired;
- an authority/runtime field changes;
- documentation navigation would make the ledger undiscoverable.

Do not churn it for every SHA or mechanical dependency update. Volatile provenance belongs in GitHub/CI/status history unless it is required to explain a durable unresolved question.

When an item is completed, mark `DONE` with immutable evidence or remove it only when history is safely preserved elsewhere and deletion cannot confuse future audits.

---

## Final invariant

A future AI must be able to determine from Crystal's live repository + this ledger:

- what implementation truth exists;
- what owns semantic/architecture truth;
- what is historical versus active;
- what remains research;
- what is forbidden/not authorized;
- where evidence is anchored;
- what makes an entry stale;
- how to continue safely.

**No ledger entry grants automatic authorization for the next milestone.**
