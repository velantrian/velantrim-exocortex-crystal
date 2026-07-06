# Contradiction Policy

**What Crystal's contradiction layer currently detects, what it does not, and
the safe policy for conflicting `VERIFIED` claims.**

This document describes `core/contradiction.py` (the classifier) and
`core/reconcile.py` (`find_conflicts`, `contradict`, `supersede`) as they
exist today. It is documentation of current behaviour, not a design proposal
— see [Non-goals / future policy](#non-goals--future-policy-ideas) for what
is deliberately out of scope.

## Implemented behaviour

### The classifier (`core/contradiction.py`)

`classify(claim_a, claim_b)` turns a pair of semantically-close claims into
exactly one of:

| Kind | Meaning |
|---|---|
| `CONTRADICTION` | Same subject, opposite assertion (negation / antonym / differing number) |
| `REFINEMENT` | Same subject, same polarity — a duplicate or a more specific form |
| `RELATED` | Topically near but no contradiction signal |

It is **deterministic and dependency-free** (stdlib regex + fixed word lists,
no NLI/LLM model) and **high-precision over high-recall** by design: it only
returns `CONTRADICTION` when both hold:

1. **Same-subject gate** — the two claims share at least 30% of their content
   tokens (Jaccard overlap, stopwords/negation-cues/bare numbers excluded).
   Below this, the verdict is withheld as `RELATED` regardless of any other
   signal.
2. **An explicit polarity signal**, checked in this order:
   - **antonym** — the claims differ by one of ~55 hardcoded antonym pairs
     (hot/cold, rises/falls, legal/illegal, …);
   - **negation** — exactly one claim carries a negation cue (`not`, `no`,
     `never`, `n't`-contractions, and the Russian equivalents `не`/`нет`/`ни`/
     `без`/`никогда`/`нельзя`);
   - **numeric** — same wording but a differing key number (`100°C` vs
     `90°C`).

`is_contradiction(a, b)` is a boolean convenience wrapper around `classify`.

### Conflict candidates (`reconcile.find_conflicts`)

`find_conflicts(claim, fact_id=None)` finds canonical `WORLD_FACT` nodes with
`epistemic_state == "Validated"` that are semantically close to `claim`
(vector similarity ≥ threshold, default from `_CONFLICT_MIN_SIM`), excluding
`fact_id` itself and verbatim repeats, and classifies each candidate. It
returns a list of `{fact_id, claim, similarity, kind, signal}` — **candidates
only**, not verdicts. It is called from the ingest path (`core/ingest.py`),
import path (`core/imports.py`), review diagnosis (`core/review.py`), the
immune layer (`core/immune.py`), the eval harness, and exposed read-only via
the `conflicts` CLI command and the MCP `find_conflicts` tool.

### Truth-maintenance primitives (`reconcile.contradict` / `reconcile.supersede`)

Two functions exist to actually *mutate* state in response to a conflict:

- `contradict(fact_id, by_id)` — transitions `fact_id` from `Validated` to
  `Contradicted` and adds a `CONTRADICTS` edge to `by_id`.
- `supersede(old_id, new_fact)` — ingests `new_fact` through the TruthGate,
  transitions the old fact `Validated → Contradicted → Deprecated`, and adds
  a `SUPERSEDED_BY` edge.

`CONTRADICTS` and `SUPERSEDED_BY` edges carry **zero relevance weight** in
retrieval's graph-walk (`core/pipeline.py`, `_WALK_EDGE_WEIGHTS`): a fact is
never made *more* relevant because it is refuted or replaced.

## Current limitations

This is the part reviewers should read carefully — the safety story here is
**advisory surfacing, not automatic resolution**:

- **`contradict()` and `supersede()` are not called by any automatic runtime
  path.** A repo-wide search confirms they are only referenced from
  `core/reconcile.py` itself, its tests, and one docstring comment in
  `core/compliance.py`. Detecting a conflict (`find_conflicts`) never, by
  itself, changes any fact's epistemic state. There is one narrower,
  separate exception: `core/ingest.py`'s live ingest path, when
  `VELANTRIM_AUTO_CONTRADICT=1`, calls `graph.add_edge()` **directly**
  (not `reconcile.contradict()`) to persist a `CONTRADICTS` edge for a
  high-precision contradiction. This links the two facts (queryable via
  `fact_history()`) but does not flip either side's epistemic state, and it
  is off by default.
- **No curator-facing entry point calls `contradict()`/`supersede()`
  either.** The CLI exposes read-only `conflicts` and `history`; there is no
  `contradict` or `supersede` CLI/API command today. Acting on a detected
  conflict currently requires calling `core.reconcile` directly from Python
  (the `VELANTRIM_AUTO_CONTRADICT` edge-linking above is not the same thing
  — it links, it does not resolve).
- **A `"conflict"` review diagnosis does not block approval.** In
  `core/review.py`, `_diagnose()` returns `verdict="conflict"` (with the
  contradicted `fact_id`s) when a pending `WORLD_FACT` contradicts the canon.
  But `approve()`'s own docstring is explicit: *"a `ready` or `conflict` item
  is promoted... a conflict is a non-destructive advisory."* A normal
  `approve()` call — no `force`, no `reason` required — promotes the new
  fact to `Validated` exactly as if there were no conflict. **The old,
  contradicted fact is not automatically transitioned or flagged** unless a
  human separately calls `reconcile.contradict()`.
- **Net effect today:** two `Validated` `WORLD_FACT`s that directly
  contradict each other *can* coexist in the canon. On the `review.py`
  curator-approval path, the only record of the conflict is the transient
  `_diagnose()` return value shown at approval time — nothing is persisted
  as a "contested" marker unless a human separately calls
  `reconcile.contradict()`. On the live `ingest()` path, a `CONTRADICTS`
  edge *is* persisted automatically (queryable via `fact_history()`) when
  `VELANTRIM_AUTO_CONTRADICT=1` — but that still only links the two facts;
  it does not transition either one's epistemic state or otherwise mark a
  side as resolved.
- **The classifier's coverage is intentionally narrow, in both directions.**
  ~55 hardcoded antonym pairs, ASCII+Cyrillic negation cues, and
  single-number extraction only. Claims that contradict through implication,
  comparison, or domain reasoning it cannot lexically detect are classified
  `RELATED` and never reach a conflict check at all — a false-negative risk
  (see design rationale in the module docstring: high-precision over
  high-recall). But **false positives are also possible, and measured, not
  just theoretical**: the numeric signal flags `CONTRADICTION` whenever two
  claims clear the content-overlap gate and carry different numbers, even
  when the numbers differ for a non-contradictory reason (different years,
  different scopes). The eval harness tracks a nonzero
  `contradiction.false_positive_rate` (`core/eval.py`, baseline `0.25`)
  precisely because of this — treat contradiction hits as high-precision by
  design, not as verified-correct by construction.
- **`find_conflicts` only looks at `WORLD_FACT` + `Validated` canon nodes.**
  Conflicts against `Supported`/`Hypothesized` facts, or against
  non-`WORLD_FACT` claim types, are out of scope for this function by
  design (callers gate on `claim_type == "WORLD_FACT"` before calling it).

## Safe conflict policy (current, and the floor for any future change)

When two `VERIFIED`/`Validated` claims conflict, the system must not
silently choose one:

1. **Do not silently choose one.** No code path today auto-resolves a
   conflict by picking a "winner" — this is true both because `contradict()`
   is unwired (a fact of today's implementation) and as a hard requirement
   for any future automation (`"last verified wins"` or `"most sources
   wins"` as a *default* policy is explicitly rejected — see Non-goals).
2. **Surface both.** `find_conflicts()` / `_diagnose()` return the
   conflicting fact's `fact_id`, not just a boolean — the caller always has
   both sides.
3. **Mark contested.** `review.approve()`'s `"conflict"` verdict is the
   current contested-marking mechanism, visible to a curator before
   promotion. (It does not yet persist a contested marker in L3 after
   promotion — see Current limitations.)
4. **Show trace paths.** `reconcile.fact_history(fact_id)` exposes
   `contradicts` / `contradicted_by` / `supersedes` / `superseded_by` edges
   so the provenance of a conflict is queryable.
5. **Flag curator review unless an explicit supersession rule applies —
   but only on the review-queue path, not on live ingest.** This holds for
   `core/review.py`'s pending-queue flow (facts an operator left/routed as
   `Observed`, e.g. via `core/imports.py`'s import-then-review pattern): a
   `"conflict"` diagnosis is shown before `approve()` is called, and nothing
   reaches canon ahead of that curator decision. **It does not hold for the
   live `ingest()` path**: once `find_conflicts()` runs post-TruthGate, a
   non-strict-mode conflict does not pause for review — the fact is
   transitioned to `Validated` and merged into L3 in the same call, with the
   conflict attached to the result. Only `VELANTRIM_IMMUNE_STRICT` turns a
   detected contradiction into an outright ingest-time block. Either way,
   resolving *which* side stands afterward is a human decision exercised by
   calling `reconcile.contradict()`/`supersede()` directly — not an
   automatic one, and not one exposed through a CLI/API action today.

## Non-goals / future policy ideas

Explicitly **not** implemented, and not to be inferred from this document:

- **`"last verified wins"` as a default conflict-resolution policy.**
- **`"most sources wins"` as a default conflict-resolution policy.**
- **Automatic resolution of a detected conflict** without a human/curator
  action (no auto-`contradict()`, no auto-`supersede()`).
- **A persistent "contested" state or edge type** distinct from
  `Contradicted`/`CONTRADICTS` — today the only signals are the transient
  review-time diagnosis and, opt-in on ingest, a plain (non-state-changing)
  `CONTRADICTS` link. Adding a persistent contested marker, or wiring
  `contradict()`/`supersede()` into a curator-facing CLI/API action, is
  future work and would need its own RFC and tests before implementation.
- **Broader contradiction detection** (semantic/NLI-based, cross-claim-type,
  cross-epistemic-state) — the current classifier's narrow, lexical,
  high-precision design is a deliberate trade-off, not an oversight, but
  expanding it is a legitimate future direction.

None of the above is implemented by this document. This is a description of
current behaviour plus the policy floor any future change must not violate.
