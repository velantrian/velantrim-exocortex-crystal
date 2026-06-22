# Claim Metadata Glossary

> Date: 2026-06-20
> Scope: as-built terminology reference for Crystal's claim / verification / origin vocabulary.
> Status: docs-only. Describes already-implemented runtime fields and discipline; changes nothing.

## Purpose

Crystal uses several **orthogonal** metadata axes, and a few have overlapping
everyday words (e.g. `epistemic_state="Validated"` vs the derived
`truth_status="VERIFIED"`). This glossary is the single **as-built** reference so
a reviewer never has to guess which term means what. It exists for
**reviewer-facing clarity** only.

Ground truth is the code (`core/memory.py`, `core/pipeline.py`,
`core/truth_gate.py`) plus the audited baseline in `TEST_REPORT.md`. Where this
glossary and any forward-looking contract doc disagree, **the code wins**.

```
memory ≠ knowledge
experience ≠ world fact
importance ≠ confidence
LLM output ≠ evidence
signal ≠ decision
```

## The axes (as implemented)

| Axis | Field | Question it answers | Implemented values / source |
|---|---|---|---|
| Modality | `claim_type` | What kind of statement is it? | `core/memory.py` `CLAIM_TYPES` |
| Origin | `source_status` | Where did the claim come from? | `core/memory.py` `SOURCE_STATUSES` |
| Verification (internal) | `epistemic_state` (ESM) | How verified is it, as a persisted lifecycle state? | `core/memory.py` `ESM_STATES` / `ESM_TRANSITIONS` |
| Verification (outward) | `truth_status` | A derived, outward-facing label | `core/pipeline.py` `_truth_status_for` (not stored) |
| Reliability | `confidence` | How reliable is the support? | `facts.confidence`; `core/reconcile.py` `reinforce()` |
| Retrieval priority | `significance` / salience | How important for attention/retrieval? | `facts.significance`; `core/salience.py` |

## 1. `claim_type` — what kind of claim this is

Implemented runtime values (`core/memory.py` `CLAIM_TYPES`):

- `WORLD_FACT` — a claim about the external world (requires evidence)
- `USER_EXPERIENCE` — an event as the user experienced it
- `EMOTION` — an internal state / feeling
- `INTERPRETATION` — an inference / explanation (hypothesis)
- `OPINION` — the user's opinion
- `GOAL` — a goal
- `PREFERENCE` — a preference

`WORLD_FACT` is deliberately **not** a synonym for "verified". Subjective types
(`USER_EXPERIENCE`, `EMOTION`, `OPINION`, `PREFERENCE`, `GOAL`) are valid records
but are **not** admissible as facts about the world.

## 2. `source_status` — where the claim came from

Implemented runtime values (`core/memory.py` `SOURCE_STATUSES`):

- `USER_REPORTED` — reported by the user
- `OBSERVED` — observed by the system
- `DERIVED` — derived from other facts
- `EXTERNAL` — external source / retrieval / import
- `LLM_OUTPUT` — the model's own text — by itself NOT evidence
- `UNKNOWN` — origin not established (default)

Source monitoring guards against "saw / imagined / heard / inferred" confusion.

## 3. ESM / `epistemic_state` — internal persisted state machine

`epistemic_state` is the **persisted** lifecycle column. States
(`core/memory.py`): `Observed → Hypothesized → Supported → Validated`, plus
`Contradicted`, `Deprecated`, `Collapsed`, `ImmutableCore`. Transitions are
constrained by `ESM_TRANSITIONS`; the only legal path to change it is
`transition_esm()` — a direct write to the column is an architectural bug.

This is the **internal** verification axis, distinct from the outward-facing
`truth_status` below.

## 4. `truth_status` — derived, outward-facing overlay

`truth_status` is **derived** at read time by `core/pipeline.py`
`_truth_status_for(claim_type, source_status)` and overlaid onto a fact; it is
**not a stored database column** and **not** the source of truth. Indicative
values: `VERIFIED`, `USER_CLAIMED`, `UNVERIFIED`.

- `epistemic_state="Validated"` (persisted) and `truth_status="VERIFIED"`
  (derived) are **related but distinct** — do not treat them as one field.
- This glossary does **not** add a new `epistemic_status` enum; the persisted
  axis stays `epistemic_state`.

## 5. `confidence` — reliability / support score

A numeric reliability score (`facts.confidence`), adjusted only by an explicit
`reinforce()` decision (decaying Laplace update in `core/reconcile.py`).

Confidence is **not** significance, **not** frequency, and **not** retrieval
priority. Repeating the same claim is a frequency signal, not added confidence.

## 6. `significance` / salience — retrieval / attention priority

`significance` (`facts.significance`) and the salience signal
(`core/salience.py`) express how important a memory is for **retrieval /
attention ordering**. They are **ranking-only**: they never set or change
`truth_status`, `confidence`, or `epistemic_state`. Importance is not truth.

## 7. Receipt / TRACE / provenance — auditability & replayable evidence

- **Receipt** (`core/provenance.py`, Receipt v2): a content-sealed, **replayable
  evidence path** for an answer; verifiable offline.
- **TRACE** (`core/trace.py`): the recorded grounding/reasoning path.
- **Per-fact provenance chain** (`core/provenance_chain.py`): an append-only,
  hash-chained lifecycle log scoped to a single fact.
- **Audit ledger** (`core/audit.py`): an append-only, hash-chained record of
  governance events (erase / restrict / review decisions …).
- **Evidence spans** (`core/evidence.py`): source-span records linking a fact to
  where it came from.

Together these provide **auditability** and source-grounded, replayable proof —
not a correctness guarantee.

## 8. TruthGate — admissibility boundary

`core/truth_gate.py` is the **admissibility boundary**, not a metaphysical truth
engine. It returns a decision `(passed, reason)`; the **caller** performs any
write. By default it enforces unsupported-claim prevention — e.g. `LLM_OUTPUT`
cannot become a `WORLD_FACT` without an independent source — while letting
subjective claims pass as subjective. It decides what is **admissible**, not what
is ultimately true.

## 9. Guardian — invariant / safety / scope boundary

Guardian is the companion safety/permission/invariant check on the write path.
It enforces scope and protection invariants (e.g. immutable Ring Zero) alongside
the TruthGate before anything reaches the canonical graph.

## Discipline — what these axes do NOT permit

- **`LLM_OUTPUT` cannot prove itself** — it is never a `WORLD_FACT` without an
  independent source.
- **`USER_REPORTED` is not automatically a world fact** — it is a sourced claim,
  not verified canon.
- **Subjective material** (`EMOTION` / `OPINION` / `INTERPRETATION` /
  `USER_EXPERIENCE` / `GOAL` / `PREFERENCE`) must **not** be promoted to
  `WORLD_FACT` without evidence.
- **Frequency / occurrence must not become truth confidence** — occurrence
  tracking updates frequency metadata only.
- **Signal ≠ decision** — conflict/contradiction detection surfaces *candidates*;
  supersede / contradict stay explicit.
- **Canon writes remain controlled** — the TruthGate is the only entry; there is
  **no automatic `ADMIT` / `SUPERSEDE`**.

## Relationship to other docs

- `docs/core/CLAIM_TYPE_AND_ORIGIN.md` is a **contract / forward-looking** doc.
  Its `origin_type` axis and `SYSTEM_OBSERVED` / `SYSTEM_GENERATED` /
  `SYSTEM_NOTE` names are **proposed**, **not** the implemented runtime
  vocabulary. The implemented origin axis is `source_status` with the six values
  listed above. This glossary is the **as-built** reference.
- `docs/METAPHOR_VS_MECHANISM.md` — implemented-vs-research naming discipline.
- `docs/STATUS.md` / `docs/IMPLEMENTATION_REALITY_MATRIX.md` — component status;
  `TEST_REPORT.md` + the README badge carry the exact test baseline.

## Non-goals

This document is descriptive only. It does **not**:

- introduce ClaimVersion nodes;
- introduce a new `epistemic_status` enum;
- change TruthGate behaviour;
- change schemas;
- change runtime behaviour;
- add bitemporal fields (`valid_time` / `transaction_time`);
- add event sourcing;
- add cache / snapshot systems;
- permit automatic Canon writes;
- lower test or coverage gates.
