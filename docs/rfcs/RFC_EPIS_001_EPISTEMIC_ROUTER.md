# EPIS-001 — Epistemic Router / Evidence State Layer

```text
Status:                FROZEN_ARCHITECTURE_CONTRACT
Runtime implementation: NOT IMPLEMENTED
Runtime authorization:  false
Tracking issue:         #155
Scope:                  read-only evidence-state observability contract
```

## 1. Purpose

Crystal already separates retrieval, provenance, admission, strict grounding, and answer generation. The remaining gap is observability: a caller can receive a `FactsPack`, `Trace`, Guardian result, and strict CanonicalView grounding without one explicit, bounded representation of **how much answer-relevant evidence is actually available**.

EPIS-001 freezes that representation. It does **not** implement it.

The router is a future pure/read-only projection that may classify answer-grounding sufficiency as:

```text
KNOWN | PARTIAL | UNKNOWN
```

These labels are response/observability metadata only. They are not truth verdicts and have no write or promotion authority.

## 2. Live architecture being preserved

The current repository already has distinct authority boundaries:

```text
ADMISSION / WRITE PATH
FactsPack
   ↓
Guardian              structural integrity only
   ↓
TruthGate             admission decision only
   ↓
caller-owned ESM/L3 transition when admitted

READ / ANSWER PATH
already-admitted local memory
   ↓
FactsPack + Trace
   ↓
Guardian              structural integrity only
   ↓
CanonicalView         strict read-time grounding projection
   ↓
generation / refusal
```

EPIS-001 does not reorder or replace these boundaries.

The original issue sketch placed an EpistemicRouter before TruthGate and Guardian. Fresh inspection of the live code shows that this ordering is no longer architecture-safe: Guardian is explicitly the structural gate before TruthGate on admission paths, TruthGate is the L3 admission boundary, and CanonicalView is the strict read-time grounding boundary. This RFC therefore binds the router to **observability after existing authority decisions**, not to authority itself.

## 3. Core invariant

```text
evidence_state
  != truth_status
  != epistemic_state
  != CanonicalReadMode
  != Guardian verdict
  != TruthGate verdict
  != evidence admission
  != Canon authority
```

No `KNOWN`, `PARTIAL`, or `UNKNOWN` result may:

- create or update L0/L1/L3 data;
- mutate `truth_status`;
- transition ESM state;
- promote confidence;
- admit evidence;
- resolve a contradiction;
- select a canonical winner;
- bypass Guardian;
- bypass or replace TruthGate;
- bypass or replace CanonicalView;
- turn retrieval similarity/ranking into epistemic authority.

## 4. Evidence-state vocabulary

### `KNOWN`

`KNOWN` means **complete strict-grounding coverage has been demonstrated for the explicitly declared answer requirements**.

A future implementation may emit `KNOWN` only when all of the following are true:

1. an explicit coverage contract declares the answer requirements/units;
2. every required unit is linked to at least one fact that passes the existing strict CanonicalView projection;
3. the Trace structurally covers the referenced facts;
4. no required unit is marked as unresolved-conflict/ambiguous by an authoritative upstream conflict surface;
5. no required unit depends only on restricted, contextual, `USER_CLAIMED`, hypothetical, unverified, malformed, or otherwise non-strict material.

A non-empty FactsPack, high confidence, retrieval rank, physical L3 membership, or `Validated` ESM state alone is **never sufficient** for `KNOWN`.

### `PARTIAL`

`PARTIAL` means there is at least one usable strict-canonical grounding path for the declared answer scope, but complete coverage has not been demonstrated.

Examples:

- only some required units have strict grounding;
- strict grounding exists but an explicit coverage proof is incomplete;
- one requirement has an unresolved conflict while other requirements remain uncontested;
- a caller did not supply enough bounded coverage information to justify `KNOWN`, but strict grounding is present for part of the response.

`PARTIAL` is not permission to fill missing content from model priors.

### `UNKNOWN`

`UNKNOWN` means the router cannot establish usable strict grounding for the requested answer scope.

It is also the fail-closed state for malformed/ambiguous router inputs when a safer, narrower diagnosis cannot be made.

Examples:

- no strict-canonical grounding facts;
- all candidate support is restricted or non-canonical;
- no declared requirement has usable support;
- all potentially supporting requirements are unresolved conflicts;
- the coverage contract is malformed in a way that prevents trustworthy classification.

## 5. Coverage contract

EPIS-001 deliberately does **not** invent a semantic query decomposer.

A future runtime implementation must receive an explicit, bounded coverage contract from its caller, for example conceptually:

```json
{
  "requirements": [
    {"id": "r1", "supporting_fact_ids": ["fact-a"]},
    {"id": "r2", "supporting_fact_ids": ["fact-b", "fact-c"]}
  ]
}
```

This mapping is a claim about **answer scope**, not about truth. The router must independently re-check referenced facts against CanonicalView rather than trusting a caller-supplied `strict=true` bit.

No LLM-generated requirement decomposition is authorized by this RFC. If a later milestone proposes one, it requires its own contract and validation.

## 6. Future input contract

A future pure router is expected to consume only already-available read-side material:

```text
FactsPack
Trace
explicit coverage requirements
optional existing conflict metadata / reason codes
```

The router may use the existing pure CanonicalView predicate/projection to determine which referenced facts are eligible for strict grounding.

It must not call a write API, invoke TruthGate as a substitute classifier, or derive truth from confidence/rank.

## 7. Future output schema sketch

Illustrative only; no runtime schema exists in this milestone:

```json
{
  "contract": "EPIS-001-v1",
  "evidence_state": "PARTIAL",
  "authority": "DIAGNOSTIC_ONLY",
  "requirements_total": 3,
  "requirements_strictly_grounded": 2,
  "strict_grounding_fact_ids": ["fact-a", "fact-b"],
  "reason_codes": ["PARTIAL_REQUIREMENT_COVERAGE"],
  "runtime_authorization": false,
  "mutation_performed": false
}
```

Default output should minimize data duplication. Raw claim text is not required merely to report evidence state. TRACE/Receipt integration, if later implemented, should bind identifiers/reason codes without converting the diagnostic label into proof.

## 8. Reason-code families

A future implementation should use stable machine-readable reasons. The frozen families are:

```text
COMPLETE_REQUIREMENT_COVERAGE
PARTIAL_REQUIREMENT_COVERAGE
NO_STRICT_GROUNDING
COVERAGE_CONTRACT_MISSING
COVERAGE_CONTRACT_MALFORMED
TRACE_INCOMPLETE
NONCANONICAL_SUPPORT_EXCLUDED
RESTRICTED_SUPPORT_EXCLUDED
UNRESOLVED_CONFLICT
```

These reason codes describe why the diagnostic state was produced. They do not adjudicate the underlying claims.

## 9. Relationship to Guardian

Guardian remains the structural integrity gate. EPIS-001 does not duplicate Guardian's checks or weaken them.

A future read-path integration must not use `KNOWN` to override a Guardian block. If Guardian blocks, no router result can make the answer path admissible.

## 10. Relationship to TruthGate

TruthGate remains the L3 admission boundary.

EPIS-001:

- does not replace TruthGate;
- does not call `truth_gate()` to infer an answer state;
- does not turn `KNOWN` into admission permission;
- does not transition ESM after a diagnostic result;
- does not write to Canon/L3.

Admission semantics remain exactly where they are today.

## 11. Relationship to CanonicalView

CanonicalView is the existing strict read-time authority for answer grounding. EPIS-001 is downstream/observational relative to that authority.

A future router may summarize **coverage of facts that CanonicalView already accepts**. It may not create a second definition of strict canon.

This is especially important because:

```text
physical L3 membership != strict canon
Validated ESM state      != VERIFIED truth by itself
high confidence          != verification
```

## 12. Relationship to TRACE / Receipt

TRACE is provenance metadata. A future Receipt may record an EPIS-001 diagnostic for auditability.

But:

```text
recorded diagnostic != proof of truth
receipt presence     != evidence admission
trace presence       != complete answer coverage
```

A receipt should preserve the exact state/reason codes and identifiers used for the response without silently upgrading them.

## 13. Failure modes and fail-closed behavior

The future implementation must fail closed against at least:

- malformed FactsPack/Trace structures;
- requirement references to missing facts;
- caller-supplied support IDs that fail CanonicalView;
- restricted support;
- unverified/contextual-only support;
- incomplete Trace binding;
- unresolved conflict on a required unit;
- fabricated `KNOWN`/`strict` caller flags;
- unknown evidence-state or reason-code values;
- any attempt to mutate memory or authority state from classification.

A malformed condition must never be normalized into `KNOWN` merely because some facts exist.

## 14. Runtime non-goals

This milestone does **not** add:

- `core/epistemic_router.py`;
- pipeline wiring;
- a new API/CLI/MCP surface;
- a new storage schema;
- any L3 write;
- any ESM transition;
- a new TruthGate/Guardian/CanonicalView implementation;
- semantic/vector retrieval;
- an NLI/CrossEncoder/LLM judge;
- external dependencies;
- a new model/provider;
- contradiction adjudication;
- answer generation changes;
- a grant-deliverable or funding-status change.

## 15. Future implementation test plan

Runtime implementation is separately authorized work. Before it can be considered complete, a future milestone must test at least:

1. `KNOWN` requires explicit complete requirement coverage.
2. A non-empty FactsPack alone cannot yield `KNOWN`.
3. Retrieval score/confidence alone cannot yield `KNOWN`.
4. Every referenced support fact is independently checked through CanonicalView.
5. `PARTIAL` is emitted for incomplete but non-zero strict coverage.
6. `UNKNOWN` is emitted when no strict grounding exists.
7. Malformed coverage input fails closed and never becomes `KNOWN`.
8. Restricted/contextual/unverified support is excluded.
9. Unresolved conflict prevents complete `KNOWN` coverage.
10. Guardian block cannot be overridden by router output.
11. Router execution performs zero L0/L1/L3 writes and zero ESM transitions.
12. Router execution performs zero `truth_status`/confidence mutation.
13. Trace/Receipt serialization preserves the diagnostic label without promoting authority.
14. Direct callers cannot fabricate strict support through a boolean flag.
15. Existing query/read-only and CanonicalView behavior remains unchanged unless a separate wiring milestone explicitly changes it.

Any runtime proposal must include an explicit diff plan and identify its exact call site before code changes are authorized.

## 16. Reviewer-safe wording

Accurate after this RFC milestone:

> EPIS-001 freezes a read-only evidence-state observability contract for `KNOWN | PARTIAL | UNKNOWN`. It is not implemented at runtime and has no truth, evidence-admission, Canon, or pipeline authority.

Not accurate:

> Crystal now has an Epistemic Router runtime.
> `KNOWN` means the system proved a claim true.
> The router replaces TruthGate or CanonicalView.
> The router eliminates hallucinations.

## 17. Acceptance for this architecture milestone

This milestone is complete only when:

- this RFC is merged;
- machine status records `runtime_implemented=false` and `runtime_authorization=false`;
- AI-facing context records the same authority boundaries;
- regression tests protect the architecture-only status and state-separation invariants;
- full exact-head CI passes;
- review gate is recorded without inventing independent approval;
- guarded merge, signed main, post-merge CI, authorized Notion sync/read-back, completion evidence, issue closure, and final live audit complete.

After closure: **STOP**. A runtime EpistemicRouter requires a separate explicitly selected milestone.