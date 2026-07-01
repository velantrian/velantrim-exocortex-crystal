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
(e.g. `WORLD_FACT`, `USER_EXPERIENCE`, `EMOTION`, `LLM_OUTPUT`) so that
subjective or generated content cannot silently pass as verified fact.

- Anchor: `core/memory.py` (`claim_type` column and defaults),
  `docs/core/CLAIM_TYPE_AND_ORIGIN.md`.

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
transitions constrained by `ESM_TRANSITIONS`.

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
decision — only the promotion/review path defined in `core/pipeline.py` /
`core/review.py` (behind TruthGate) can move a fact toward Canon.

- Anchor: `core/pipeline.py`, `core/review.py`,
  `docs/architecture/STAGED_WORKING_MEMORY_ADMISSION.md`.

### Retention / Erasure Axis

Two distinct questions must not be collapsed into one:

1. **Soft-decay / retention weighting** — how relevance or recency might
   deprioritize a fact in retrieval, without deleting it.
2. **Hard-erasure / restriction paths** — where a fact must actually be
   removed or restricted (e.g. a GDPR erasure request), recorded as an
   append-only, hash-chained lifecycle event.

**Soft-decay does not replace hard-erasure requirements.** A relevance or
recency weighting mechanism is not a substitute for an explicit erasure path
where one is legally or contractually required.

- Anchor: `core/erasure.py`, `core/provenance_chain.py` (erase-path events),
  `docs/core/PROVENANCE_CHAIN_CONTRACT.md`.

### Response Permission Axis

Given a claim's type, source status, and epistemic state, what is the answer
allowed to say about it — assert plainly, hedge, require a citation, or
refuse? Crystal's read-path `decide_response_policy` decides this from
`claim_type` + `source_status` + `epistemic_state`, never from TruthGate
itself and never by writing to L3.

**Response permission is not based on confidence alone.** A high confidence
score does not by itself grant assertive response permission; the decision
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
cannot be bypassed, Canon cannot be overwritten outside the review path, TRACE
cannot be altered) that every stage above must already respect.

## 5. Testability Gate

An axis claim is usable in reviewer- or grant-facing material only if it is
backed by a test referenced in `TEST_REPORT.md` or a behaviour-pinning test
file (e.g. `tests/test_esm.py`, `tests/test_response_policy.py`,
`tests/test_write_path_gate.py`). This mirrors the existing "honesty
invariant" already required by `CONTRIBUTING.md` and `AGENTS.md`: a doc
claim without a corresponding test is a documentation claim, not a verified
one.

## 6. Source Attribution Discipline

Every axis above ultimately depends on `source_status` being traceable to an
actual evidence span at ingest time (e.g. the PDF adapter's span-preservation
fix, #182, `core/adapters/pdf_adapter.py`) rather than to an unattributed
paraphrase. An audit against this framework should ask, per claim type,
whether the evidence span survives from ingestion through to the answer.

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
- **Memory State** — Does every `epistemic_state` transition go through
  `ESM_TRANSITIONS`, with no path that mutates state outside it?
- **Consolidation** — Does every L2→L3 promotion pass through TruthGate, with
  no compression/merge step that promotes on its own?
- **Retention / Erasure** — Is there a hard-erasure path for every case that
  requires one, independent of any soft-decay/relevance weighting?
- **Response Permission** — Does `decide_response_policy` fully determine
  response framing, with no path that grants assertive permission from
  confidence alone?

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
- claim that Crystal implements, matches, or is architecturally equivalent to
  any external memory-research system;
- describe Research Mode, Titan, or Personal Exo-Cortex capability;
- change TruthGate, Guardian-boundary, or L3 behaviour in any way;
- constitute grant, legal, or compliance certification language.

## 11. Future test candidates

Non-binding ideas for tests that could, in a future and separate PR, let an
axis move from "criteria defined here" to "evaluated in
`IMPLEMENTATION_REALITY_MATRIX.md`":

- A regression test asserting that no code path sets `epistemic_state` to a
  promoted value without going through `ESM_TRANSITIONS`.
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
