# CanonicalView / Trusted-Only Read Mode — RFC

```text
Status:         PARTIALLY IMPLEMENTED (strict grounding slice)
Implementation: core/canonical_view.py — STRICT mode wired into
                core/pipeline.py::generate_answer() (the answer-grounding
                path). CONTEXTUAL mode exists as a pure, tested function but
                is NOT wired into any default surface. review / full_graph
                modes below remain PROPOSED, not implemented.
Scope:          read-path contract only
```

This document originally defined a **proposed** read-path contract. A PR
has since implemented the smallest production-safe runtime slice of it:
section 4's inclusion rule (`truth_status == VERIFIED`, non-restricted,
non-Contradicted/Deprecated/Collapsed, identity-complete) as
`core.canonical_view.is_strict_canonical()` / `project_canonical()`, wired
as the default grounding filter for confident factual answers. **Not**
implemented: the `review` / `full_graph` read modes (section 6), trace
replayability as an inclusion condition, and the conflicting-`VERIFIED`-facts
surfacing/abstention policy (section 5) — those remain proposed only. See
[Non-goals](#7-non-goals) and [Reviewer-safe wording](#10-reviewer-safe-wording)
below, both still accurate for the unimplemented remainder.

## 1. Status

```text
Status: PARTIALLY IMPLEMENTED — see the header above and section 9 below for
        exactly which acceptance criteria are met and which remain open.
Scope:  read-path contract only
```

The strict-grounding slice of this RFC is implemented: `core/canonical_view.py`
(`CanonicalReadMode`, `is_strict_canonical()`, `project_canonical()`), wired
into `core/pipeline.py::generate_answer()` as the default answer-grounding
filter. It does not implement every mode or acceptance criterion this RFC
describes — see section 9 for the itemized breakdown. This RFC remains the
authoritative contract for the unimplemented remainder (tracked as issue
#220); do not cite this document as evidence that the whole RFC landed.

## 2. Problem statement

Velantrim Crystal's architecture already distinguishes two things that are
easy to conflate ([`docs/ARCHITECTURE.md`](./ARCHITECTURE.md)):

```text
Physical graph = structured memory space (typed, source-tracked, multi-status).
Canon          = the VERIFIED + trace-valid subgraph of it.
```

The physical L3 graph may legitimately contain nodes with `truth_status` in
`VERIFIED`, `USER_CLAIMED`, `UNVERIFIED`, `HYPOTHESIS`, or `SUBJECTIVE` — the
gate is type-aware and admits a subjective claim *as* a subjective claim,
not as a rejected one. Some read paths may expose working-memory material
outside the strict canon boundary unless the caller explicitly applies a
trusted-only projection.

The ambiguity this RFC targets:

```text
L3 physical graph ≠ trusted-only canon view
```

Today, a caller that queries the graph and expects "the canon" can silently
receive pending, hypothetical, subjective, restricted, or contradicted
material mixed in with `VERIFIED` facts, because no single read-time
concept currently separates "everything the graph knows" from "what an
external-facing, high-confidence answer may cite." This RFC proposes that
concept.

## 3. Definitions

- **Physical L3 graph** — all stored graph nodes, edges, and mentions,
  regardless of `truth_status` or `epistemic_state`. Includes
  `Observed`/`Hypothesized`/`Supported` pending material, `Contradicted`/
  `Deprecated` superseded material, and restricted (GDPR Art. 18) nodes.
- **Strict canon** — the `VERIFIED` + trace-valid subgraph of the physical
  graph, as already defined in `docs/ARCHITECTURE.md`.
- **CanonicalView** — a proposed *read projection* over the physical graph.
  It does not move, copy, or duplicate data; it is a filter applied at read
  time. It has no write authority and does not participate in TruthGate
  admission.
- **Trusted-only mode** — the proposed default `CanonicalView` read mode,
  intended for high-confidence, external-facing answers.
- **Full graph / research view** — a proposed explicit, opt-in mode for
  inspection, debugging, research, and curator review — never the default
  evidence source for a confident factual answer.

## 4. Default inclusion rules (proposed)

A `CanonicalView` in `trusted_only` mode would include a fact only if **all**
of the following hold. This is a proposed contract, not a description of
current enforced behavior:

```text
truth_status == VERIFIED
trace is present and replayable / trace-valid
fact is not erased (no tombstone)
fact is not restricted for the current read purpose (GDPR Art. 18)
source metadata is present
```

Note: several of these conditions are already checked in *other* parts of
the system today for *other* purposes — e.g. `retrieve()`
(`core/pipeline.py`) already skips `restricted` nodes and
`generate_answer()` already requires `Validated`/`Supported`
`epistemic_state` before using a fact as grounding. `CanonicalView` does not
yet exist as a named, reusable read-time contract that combines these
checks; this RFC proposes making that combination explicit, named, and
independently testable rather than re-deriving it ad hoc.

## 5. Exclusion / marking rules (proposed)

A `CanonicalView` should exclude, or explicitly mark, the following rather
than admit them silently:

- `UNVERIFIED` facts;
- `USER_CLAIMED` facts;
- `HYPOTHESIS` facts;
- `SUBJECTIVE` facts, unless explicitly requested by the caller;
- restricted facts (GDPR Art. 18);
- erased facts / tombstoned `fact_id`s;
- superseded facts, where the graph already carries explicit
  `SUPERSEDED_BY` metadata (`core/reconcile.py`);
- contradicted facts (`CONTRADICTS` edges, `core/reconcile.py`), unless the
  read is specifically about the conflict itself.

### Conflicting `VERIFIED` facts

This RFC does not propose "latest wins" or "majority wins" as a resolution
policy — that would silently manufacture a winner between two claims the
system itself has not adjudicated. This mirrors the safe conflict policy
already specified in
[`docs/CONTRADICTION_POLICY.md`](./CONTRADICTION_POLICY.md):

```text
If verified facts conflict, CanonicalView must not silently pick a winner.
It should surface conflict metadata or abstain, depending on read policy.
```

Concretely: if two `VERIFIED` facts reachable by a `trusted_only` read
contradict each other (per the classifier in `core/contradiction.py`), a
`CanonicalView` implementation would need to either (a) surface both with
conflict metadata attached, or (b) abstain from citing either as
uncontested — never silently return one as if the other did not exist.
Which of (a)/(b) applies is a read-policy choice this RFC leaves open (see
[Open questions](#open-questions)); it does not resolve it.

## 6. Read modes (proposed)

| Mode | Proposed semantics |
|---|---|
| `trusted_only` | Only strict canon material (section 4). The intended default for confident, external-facing answers. |
| `review` | Includes pending / `USER_CLAIMED` / `HYPOTHESIS` material, explicitly labelled as such — for a curator deciding what to promote or reject. |
| `full_graph` | Diagnostic / admin / research view of the entire physical graph. Never the default evidence source for a confident factual answer, regardless of caller. |

None of these three modes exist as a runtime parameter, CLI flag, or API
field today. Naming them here is scope-setting for a future implementation,
not a claim that they are selectable now.

## 7. Non-goals

This RFC explicitly does **not** propose, and a future implementation must
not smuggle in under this name:

- a new graph backend;
- a new TruthGate, or any change to the existing one;
- a write path of any kind — `CanonicalView` is read-only by definition;
- a contradiction resolver (see section 5 — conflicts are surfaced or
  abstained, never resolved by this layer);
- a replacement for `core/provenance.py` / `core/provenance_chain.py`;
- a benchmark or performance work (tracked separately, issue #218);
- a UI implementation;
- a guarantee of legal compliance (GDPR or otherwise) — see
  `SECURITY.md`'s existing scope disclaimers, which apply unchanged here;
- an AGI, cognitive-architecture, or personality/companion layer of any
  kind.

## 8. Relationship to existing docs

- [`docs/ARCHITECTURE.md`](./ARCHITECTURE.md) — source of the physical
  graph vs. strict canon distinction this RFC operationalizes into a named
  read projection.
- [`docs/CONTRADICTION_POLICY.md`](./CONTRADICTION_POLICY.md) — this RFC's
  conflict-handling stance (section 5) is the same "surface, don't silently
  resolve" policy already specified there for contradiction detection in
  general; `CanonicalView` would consume that policy at read time rather
  than redefine it.
- [`docs/IMMUNE_LAYER.md`](./IMMUNE_LAYER.md) — read-path safety framing
  (advisory vs. strict, never a silent auto-decision) is consistent with
  how this RFC treats conflicting `VERIFIED` facts.
- [`TEST_REPORT.md`](../TEST_REPORT.md) — see that file for the current
  audited test-suite baseline. This RFC adds no tests and does not change
  that baseline; a future implementation PR would need to grow it per the
  acceptance criteria below.

## 9. Acceptance criteria for future implementation

Status per criterion, after the strict-grounding-slice PR:

- ✅ add read-path filter helpers implementing section 4's inclusion rules
  (except trace-replayability — see below): `core/canonical_view.py`.
- ✅ add tests for every inclusion/exclusion rule actually implemented
  (`tests/test_canonical_view.py`, plus integration tests in
  `tests/test_pipeline.py`).
- ✅ prove restricted facts cannot appear in a strict read.
- ✅ prove `USER_CLAIMED` / `HYPOTHESIS` / `SUBJECTIVE` material is excluded
  from strict grounding unless the caller explicitly requests `CONTEXTUAL`
  mode (this PR's two-mode `CanonicalReadMode`, not the RFC's original
  three-mode `trusted_only`/`review`/`full_graph` naming — `review` and
  `full_graph` are not implemented).
- ⬜ **not implemented**: trace-present-and-replayable as an inclusion
  condition (section 4) — strict grounding checks `truth_status`,
  `epistemic_state`, `restricted`, and identity/provenance fields, but does
  not independently re-verify trace replayability per fact.
- ⬜ **not implemented**: erased/tombstoned `fact_id`s are excluded
  *structurally* (erasure physically removes the record — see
  `is_strict_canonical()`'s docstring) rather than via an explicit check in
  this module; no dedicated regression test was added here beyond that
  structural argument.
- ⬜ **not implemented**: the conflicting-`VERIFIED`-facts surfacing/
  abstention policy (section 5) — this PR does not detect or handle
  contradicting `VERIFIED` facts reaching a strict read together; that
  remains open, tracked here, not silently resolved either way.
- ✅ preserve existing TruthGate and L3 write-path semantics unchanged —
  the implementation touches only `core/pipeline.py::generate_answer()`
  (read path) and `build_facts_pack()`'s `restricted` sync (still read-side:
  it copies an already-persisted field onto the in-flight fact dict, no new
  write). No TruthGate, ESM, or L3 write-path code was modified.

## 10. Reviewer-safe wording

Accurate language, after the strict-grounding-slice PR:

> Strict CanonicalView grounding is implemented for answer generation
> (`core/canonical_view.py`, wired into `core/pipeline.py::generate_answer()`).
> Physical L3 membership does not itself imply verified truth. `USER_CLAIMED`
> remains available as labelled contextual memory (`CanonicalReadMode.
> CONTEXTUAL`) but is excluded from strict factual grounding.

Not language like:

> The CanonicalView RFC is fully implemented.
> Every read surface now enforces trusted-only mode.
> All L3 data is Canon.
> This achieves zero hallucination.

The `review` / `full_graph` modes, trace-replayability as an inclusion
condition, and the conflicting-`VERIFIED`-facts policy remain unimplemented
(section 9) — do not claim otherwise.

## Open questions

- When `VERIFIED` facts conflict, should the default `trusted_only`
  behavior be "surface both with conflict metadata" or "abstain," and is
  that a global default or a per-caller read-policy parameter?
- Should `trusted_only` be the unconditional default for every read path
  (CLI, API, MCP), or only for the ones that currently claim to serve
  confident factual answers?
- What is the smallest useful shape for "conflict metadata" surfaced to a
  caller — a list of contradicting `fact_id`s, or something richer?
- Should `review` mode's pending-material labelling reuse
  `response_policy`'s existing `claim_type`/`source_status`/
  `epistemic_state` vocabulary (`docs/RESPONSE_POLICY_V0.md`), or define
  its own?

## Current recommendation

The strict-grounding slice (section 4's inclusion rule, as the default
answer-grounding filter) is implemented — see the status header and section
9. The open questions above are still genuinely open and block the
remainder: `review`/`full_graph` modes, the conflicting-`VERIFIED`-facts
policy, and trace-replayability as an inclusion condition should each be
their own, separately reviewed, narrowly-scoped follow-up PR, not bundled
together or with unrelated work — the same discipline that produced this
slice.
