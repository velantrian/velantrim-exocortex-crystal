# Memory Architecture Audit Framework

> Date: 2026-07-01
> Scope: documented evaluation lens for memory-quality review — methodology only
> Status: DOCUMENTED_ONLY · RESEARCH_COMPARISON · NOT_RUNTIME_CLAIM

## 1. Purpose

This document defines a reviewer- and grant-safe **lens** for evaluating the
quality of Crystal's memory architecture: how claims are typed, how much
verification effort backs them, what epistemic state they hold, how they get
consolidated toward Canon, how they are retained or erased, and what
permission a response has to speak from them.

It is an **evaluation methodology**, not a new module. It introduces no
runtime behaviour, no new class, no new endpoint, and no new dependency. It
does not itself assert that any axis below is "done" — it only defines what
"done" would mean and where the real answer already lives.

## 2. Scope boundary

This lens applies only to mechanisms that already exist in the Crystal
runtime (`core/`) and its accompanying `docs/`. It does not describe, expand,
or evaluate Research Mode, Titan, Personal Exo-Cortex, or any other
private/prototype track — those remain out of scope for any Crystal-facing
audit per `docs/STATUS.md`'s reading rule.

**External research vocabulary.** Terms from external memory-architecture
research (e.g. MAGMA, GAM, D-MEM, LiCoMemory) are not implementation targets
for Crystal and are not otherwise used in this document. If a future revision
of this file cites any external system or paper for comparison, it must be
labelled explicitly as *research comparison only / not an implementation
claim*, and marked `VERIFIED_SOURCE` or `UNVERIFIED_SOURCE` per the
vocabulary in §7. No such citation is added here; nothing above should be
read as claiming Crystal implements, matches, or is architecturally
equivalent to any external system.

## 3. Six-Axis Memory Audit Lens

Each axis names what to check and points to the real mechanism it evaluates.
None of the axes below carries a status verdict — see §9.

### Object Type Axis

What kind of claim is this? Crystal already separates `claim_type` values
(e.g. `WORLD_FACT`, `USER_EXPERIENCE`, `EMOTION`, `OPINION`) so that
subjective or generated content cannot silently pass as verified fact. Note:
`LLM_OUTPUT` is a `source_status` value (`core/memory.py`'s
`SOURCE_STATUSES`), not a `claim_type` — the two axes are distinct and must
not be conflated.

- Anchor: `core/memory.py` (`claim_type` column, `CLAIM_TYPES`, and
  defaults), `docs/core/CLAIM_TYPE_AND_ORIGIN.md`.

### Verification Effort Axis

How much evidence backs this claim, and does more repetition change that?
Crystal ties admissibility to `source_status` and `confidence`, evaluated at
the TruthGate boundary — not to how often a claim has been seen.

**Repetition is not truth.** Seeing the same unsourced claim many times does
not raise its verification effort; frequency is not independent evidence.

- Anchor: `core/truth_gate.py`, `docs/core/INGEST_SCHEMA.md`.

### Memory State Axis

What epistemic state does this fact currently hold, and can that state be
trusted as final? Crystal's ESM (`epistemic_state`) tracks states such as
`Observed`, `Validated`, `Supported`, `Contradicted`, and `Collapsed`, with
*subsequent* transitions constrained by `ESM_TRANSITIONS`. This axis must
distinguish that from *initial* state assignment: `core/memory.py`'s
`store_fact()` persists a caller-supplied initial `epistemic_state` for a new
row after only an enum-membership check, not a transition — a freshly
imported or seeded fact can legitimately start in a later state than
`Observed`.

**`promotion_candidate` is not truth.** A fact sitting in an early,
not-yet-admitted state (e.g. `Observed`) is a candidate for promotion, not an
admitted claim — the two must never be described interchangeably in
reviewer- or grant-facing material.

- Anchor: `core/memory.py` (`ESM_TRANSITIONS`, `transition_esm`),
  `tests/test_esm.py`.

### Consolidation Axis

How does a fact move from pending candidate toward Canon, and what does *not*
count as consolidation? Crystal routes this through the L2→L3 promotion path
in `core/pipeline.py` and the curator review path in `core/review.py`.

**Compression does not promote to Canon by itself.** Summarizing, merging, or
otherwise compressing memory content is not, on its own, an admission
decision. This axis evaluates the admission/promotion path defined in
`core/pipeline.py` / `core/review.py` (behind TruthGate) — it does not claim
that path is the *only* code that ever touches L3. Other runtime paths call
`merge_fact()` directly for sync/reconcile/compliance purposes outside
promotion (e.g. `core/reconcile.py`, `core/compliance.py`, `core/volition.py`,
`core/consolidate.py`, `core/fractal.py`); those must be audited separately
for state preservation and no TruthGate bypass. This framework must not
overstate a single canonical write path.

- Anchor: `core/pipeline.py`, `core/review.py`,
  `docs/architecture/STAGED_WORKING_MEMORY_ADMISSION.md` (admission path);
  `core/reconcile.py`, `core/compliance.py`, `core/volition.py`,
  `core/consolidate.py`, `core/fractal.py` (other `merge_fact()` callers, out
  of scope for this axis but noted so the lens is not read as exhaustive).

### Retention / Erasure Axis

Two distinct questions must not be collapsed into one:

1. **Soft-decay / retention weighting** — how relevance or recency might
   deprioritize a fact in retrieval, without deleting it.
2. **Hard-erasure / restriction paths** — where a fact must actually be
   removed or restricted (e.g. a GDPR erasure or Art. 18 restriction
   request).

**Soft-decay does not replace hard-erasure requirements.** A relevance or
recency weighting mechanism is not a substitute for an explicit erasure path
where one is legally or contractually required.

Point 2 itself covers two currently different mechanisms, and this axis must
not treat them as one uniform lifecycle log:

- **Erase path** — recorded as an append-only, hash-chained, per-fact
  `core/provenance_chain.py` event, where implemented.
- **Restriction / unrestriction** (Art. 18) — `core/compliance.py`'s
  `restrict_processing()` / `unrestrict_processing()` currently record to the
  **global** audit log (`core/audit.py`), not the per-fact ProvenanceChain.
  Broader per-fact lifecycle chain coverage (including restriction events) is
  a documented follow-up in `docs/core/PROVENANCE_CHAIN_CONTRACT.md`, not a
  current claim.

- Anchor: `core/erasure.py`, `core/provenance_chain.py` (erase-path events),
  `core/compliance.py` (restriction, global audit log),
  `docs/core/PROVENANCE_CHAIN_CONTRACT.md`.

### Response Permission Axis

Given a claim's type, source status, and epistemic state, what *would* an
answer be allowed to say about it — assert plainly, hedge, require a
citation, or refuse? `core/response_policy.py`'s `decide_response_policy` is
implemented and tested as a pure policy module that computes this decision
from `claim_type` + `source_status` + `epistemic_state`, never from TruthGate
itself and never by writing to L3.

This module is **not currently wired into `generate_answer()`** or any other
current read-path runtime call; `decide_response_policy` is referenced only
from its own module, its docs, and its tests as of this writing, and the
read-path wiring work is tracked separately (PR #202, open/unmerged). The
Response Permission Axis therefore evaluates the policy contract and its
planned future read-path wiring, not a current end-to-end runtime
answer-control claim.

**Response permission is not based on confidence alone.** A high confidence
score does not by itself grant assertive response permission; the contract
draws on claim type, source status, and epistemic state together. (Note:
"ResponseGate" is a Notion-only conceptual term — there is no such module in
`core/`. This axis refers strictly to `core/response_policy.py`.)

- Anchor: `core/response_policy.py` (`decide_response_policy`),
  `docs/RESPONSE_POLICY_V0.md`.

## 4. Guardian as invariant shell

Some existing docs (`docs/ADR.md` ADR-005, `docs/security/threat-model.md`
residual-risk table) refer to "Guardian" as the boundary that constrains what
any optimizer, promotion path, or future automation is allowed to do to
TruthGate, Canon, or TRACE. There is no `class Guardian` or standalone
Guardian module in `core/` — the concept is documented, not implemented as a
discrete component.

**Guardian is an invariant shell, not a seventh pipeline step.** It is not
another stage a fact passes through; it is the set of invariants (TruthGate
cannot be bypassed, Canon cannot be overwritten outside the review path, and
sealed/emitted TRACE receipts must remain tamper-evident and not silently
rewritten) that every stage above must already respect.

This does not forbid the normal, approved lifecycle update of pre-seal trace
elements: `core/trace.py`'s `promote_trace()` intentionally mutates trace
elements in place after TruthGate approval, and
`tests/test_trace.py::test_promote_trace_mutates_in_place` pins that
behaviour. The invariant is about tamper resistance for sealed/emitted
receipts, not a blanket ban on that approved in-place update during
promotion.

## 5. Testability Gate

An axis claim is usable in reviewer- or grant-facing material only if it is
backed by a test referenced in `TEST_REPORT.md` or a behaviour-pinning test
file (e.g. `tests/test_esm.py`, `tests/test_response_policy.py`,
`tests/test_write_path_gate.py`). This mirrors the existing "honesty
invariant" already required by `CONTRIBUTING.md` and `AGENTS.md`: a doc
claim without a corresponding test is a documentation claim, not a verified
one.

## 6. Source Attribution Discipline

Source attribution should be evaluated as *appropriate to the claim's source
type*, not as one blanket evidence-span requirement for every claim:

- **Adapter-ingested factual claims** (e.g. the PDF adapter's
  span-preservation fix, #182, `core/adapters/pdf_adapter.py`) should
  preserve evidence spans.
- **User-reported / subjective claims** (`source_status = USER_REPORTED`) may
  legitimately have no adapter evidence span —
  `core/knowledge.py`'s `attach_evidence` parameter is optional there — but
  should preserve actor / source-turn attribution and an audit trace instead.
- **Generated content** (`source_status = LLM_OUTPUT`) must not be treated as
  external evidence for another claim.

An audit against this framework should ask, per claim type and source
status, whether the *appropriate* form of attribution for that source type
survives from ingestion through to the answer — not whether every claim
carries an evidence span.

## 7. Source Verification Status

Any reference used by a future revision of this document — internal or
external — must be tagged with one of:

- `VERIFIED_SOURCE` — confirmed against the cited file/test/commit at review
  time.
- `UNVERIFIED_SOURCE` — cited for context only, not independently confirmed;
  must not be used to support an implementation claim.

This document currently cites only internal repository files, all of which
are `VERIFIED_SOURCE` by direct file-path reference. No external paper or
system is cited here (see §2); none is being artificially added to satisfy a
citation requirement.

## 8. Evaluation Criteria

A future worked audit against this lens (kept in a separate document — see
§9) would ask, per axis:

- **Object Type** — Is every claim's `claim_type` set at ingest, not
  inferred later?
- **Verification Effort** — Can the `source_status` + `confidence` pair be
  traced to a specific evidence span, independent of how many times the claim
  recurs?
- **Memory State** — Is a fact's *initial* `epistemic_state` enum-valid and
  justified by its ingest/import context (`core/memory.py`'s `store_fact()`
  persists a caller-supplied initial state for new rows after only enum
  validation — that is initialization, not a transition), and does every
  *subsequent* state change go through `transition_esm()` /
  `ESM_TRANSITIONS`?
- **Consolidation** — Does every admission/promotion decision pass through
  TruthGate, with no compression/merge step that promotes on its own? (Other
  `merge_fact()` call sites outside the promotion path are a separate audit
  question — see §3 Consolidation Axis.)
- **Retention / Erasure** — Is there a hard-erasure path for every case that
  requires one, independent of any soft-decay/relevance weighting, and is the
  erase-path vs. restriction-path distinction in §3 respected?
- **Response Permission** — Once wired onto the read path, would
  `decide_response_policy`'s contract determine response framing without any
  path that grants assertive permission from confidence alone? (A
  contract-level question — current read-path wiring status is tracked
  outside this document; see §3 Response Permission Axis.)

## 9. Current-status source of truth

This framework defines what to look for. It does not say what Crystal
currently satisfies. That determination belongs exclusively to:

- [`docs/IMPLEMENTATION_REALITY_MATRIX.md`](../IMPLEMENTATION_REALITY_MATRIX.md)
- [`docs/STATUS.md`](../STATUS.md)
- `TEST_REPORT.md`

This file must never carry its own competing `IMPLEMENTED` / `PARTIAL` /
`NEEDS_VERIFICATION` table. Any future per-axis status assessment belongs in
the matrix above, not here.

## 10. Non-claims

This document does **not**:

- assert that Crystal currently satisfies any axis in full;
- assign `IMPLEMENTED`, `PARTIAL`, or `NEEDS_VERIFICATION` verdicts per axis
  (those live only in `docs/IMPLEMENTATION_REALITY_MATRIX.md`);
- claim Guardian is a discrete, implemented module;
- claim that "ResponseGate" exists in Crystal's code;
- claim that `decide_response_policy` is currently wired into
  `generate_answer()` or any other live read-path call (read-path wiring is
  tracked separately in PR #202, open/unmerged);
- claim that `core/pipeline.py` / `core/review.py` are the only code paths
  that ever call `merge_fact()` (other sync/reconcile/compliance paths exist
  and are out of scope for the Consolidation Axis as defined here);
- claim that Crystal implements, matches, or is architecturally equivalent to
  any external memory-research system;
- describe Research Mode, Titan, or Personal Exo-Cortex capability;
- change TruthGate, Guardian-boundary, or L3 behaviour in any way;
- constitute grant, legal, or compliance certification language.

## 11. Future test candidates

Non-binding ideas for tests that could, in a future and separate PR, let an
axis move from "criteria defined here" to "evaluated in
`IMPLEMENTATION_REALITY_MATRIX.md`":

- A regression test asserting that no code path *transitions* an existing
  fact's `epistemic_state` without going through `ESM_TRANSITIONS` (distinct
  from initial state assignment on a new row, which is a separate,
  documented case — see §3 Memory State Axis).
- A test asserting that `decide_response_policy` output does not vary with
  `confidence` alone when `claim_type`/`source_status`/`epistemic_state` are
  held constant.
- A test asserting every `core/provenance_chain.py` erase event has a
  corresponding `core/erasure.py` caller (no orphaned soft-decay path that
  substitutes for it).

These are candidate ideas, not commitments, and not part of this PR.

## 12. Promotion path

Like any other architecture concept in this project, an idea introduced here
does not become a Crystal capability claim until it passes:

```text
idea → RFC → invariants → tests → implementation → audit → GitHub main
```

This framework itself follows that discipline: it is `DOCUMENTED_ONLY` today,
and stays that way until a future, separate PR adds the tests in §11 and
updates `docs/IMPLEMENTATION_REALITY_MATRIX.md` accordingly.
