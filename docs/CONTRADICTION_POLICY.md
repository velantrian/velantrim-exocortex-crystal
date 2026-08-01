# Contradiction Policy

**Status:** implemented baseline for pending `WORLD_FACT` review  
**Decision record:** [ADR-014](./adr/ADR-014-EXPLICIT_CONTRADICTION_DECISIONS.md)

This document defines what Crystal detects as a contradiction, how review handles
it, and what remains deliberately outside the current runtime.

## Core rule

```text
contradiction detection ≠ contradiction resolution
similarity/confidence   ≠ epistemic winner
normal approve          ≠ permission to ignore a conflict
```

Crystal never chooses a winner solely because a claim is newer, more similar,
more frequent or carries a higher confidence value.

## Detection

### Classifier

`core.contradiction.classify(claim_a, claim_b)` returns one of:

| Kind | Meaning |
|---|---|
| `CONTRADICTION` | same-subject claims with an explicit opposite signal |
| `REFINEMENT` | same-subject, same-polarity duplicate or refinement |
| `RELATED` | topically near without a supported contradiction signal |

The classifier is deterministic and dependency-free. It uses a same-subject
content-overlap gate plus narrow lexical signals:

- antonym pairs;
- asymmetric negation;
- differing key numbers.

It is intentionally high-precision rather than complete. It cannot establish
that every detected conflict is semantically genuine, and it will miss conflicts
requiring implication, causal reasoning or specialist domain knowledge.

### Candidate lookup

`core.reconcile.find_conflicts(claim, fact_id=None)` searches validated physical
L3 `WORLD_FACT` nodes and returns candidates containing identifiers, claim text,
similarity, classifier kind and signal.

Candidate lookup is advisory. Calling it never changes ESM state, truth status or
graph authority.

## Immutable review report

For a pending conflicting `WORLD_FACT`, `core.review` creates a frozen
`ContradictionReport` containing only:

- deterministic `report_id`;
- pending candidate `fact_id`;
- conflicting fact identifiers;
- classifier kind and signal;
- similarity as advisory retrieval metadata;
- disposition, initially `REVIEW_REQUIRED`;
- `automatic_winner: null` in the public mapping.

The report does not duplicate claim or source text. Duplicate retrieval hits are
deduplicated deterministically, so input ordering cannot change its identity.

```text
pending fact
    + current conflict candidates
        ↓
content-free immutable ContradictionReport
```

## Normal approval is fail-closed

A current contradiction is no longer treated like an ordinary clean review item.

```text
review.approve(conflicting_fact)
        ↓
approved = false
reason = CONFLICT_DECISION_REQUIRED
candidate remains Observed
```

`force=True` does not bypass this boundary. Force approval remains a separate,
audited exception for a blocked gate diagnosis, not a generic contradiction
resolver.

## Explicit dispositions

`core.review.resolve_conflict()` recomputes the current report immediately before
writing. The curator must provide a non-empty actor and reason and may provide
`expected_report_id` for optimistic concurrency.

| Disposition | Required input | State/graph effect |
|---|---|---|
| `REVIEW_REQUIRED` | none | no mutation; candidate stays pending |
| `COEXIST` | actor + reason | candidate becomes Validated; explicit `CONTRADICTS` edges preserve both sides |
| `CONTEXTUALIZE` | actor + reason | candidate becomes Validated; `CONTEXTUALIZES` edges record scope/context coexistence |
| `SUPERSEDE` | actor + reason + explicit report-member target ids | candidate becomes Validated; selected targets become Contradicted then Deprecated; `SUPERSEDED_BY` edges are added |

Targets for `SUPERSEDE` must:

- belong to the freshly computed report;
- exist at decision time;
- not be processing-restricted;
- still be `Validated`.

Similarity and confidence never choose the disposition or targets.

## Stale-view protection

A curator interface may pass the report id it displayed:

```text
expected_report_id == current report_id
        → decision may proceed

expected_report_id != current report_id
        → CONFLICT_REPORT_CHANGED
        → no mutation
```

This prevents a decision based on a conflict set that changed after inspection.

## Partial supersession

L1 and L3 do not share one distributed transaction. The executor preflights all
selected targets, validates the candidate, and then applies target transitions.

If a target loses a later compare-and-swap race:

- the target is not silently removed or invalidated;
- the candidate remains explicitly Validated;
- the result reports `partial=true` and the affected target ids;
- an explicit `CONTRADICTS` edge records the safe residual coexistence;
- the audit chain records the partial target ids.

This is not full transactional conflict resolution. It is a fail-visible baseline
whose safe residual preserves information rather than erasing it.

## Accountability

Every applied decision records content-free audit metadata:

- actor;
- reason;
- report id;
- disposition;
- conflict ids;
- selected target ids;
- partial target ids, when present;
- whether candidate decision metadata was persisted.

Review history exposes dedicated decisions:

- `conflict_coexist`;
- `conflict_contextualized`;
- `conflict_superseded`.

The candidate's L1 metadata also records report/disposition identifiers through a
CAS-retry update. Failure to save that auxiliary metadata is returned and audited;
it is not hidden.

## Existing lower-level primitives

`core.reconcile` still exposes:

- `contradict(fact_id, by_id)`;
- `supersede(old_id, new_fact)`;
- `fact_history(fact_id)`.

They remain lower-level maintenance primitives. The accountable review path uses
the explicit report-bound decision contract rather than selecting these
operations automatically.

`CONTRADICTS` and `SUPERSEDED_BY` retain zero graph-walk relevance weight. A fact
never becomes more relevant because it is contradicted or replaced.

## Live ingest boundary

This baseline changes pending review decisions. It does not silently convert all
live ingest conflicts into review-queue objects.

The live ingest path still follows its documented Immune behavior:

- non-strict mode may admit both facts and surface/link a conflict;
- strict mode may block the new contradiction;
- `VELANTRIM_AUTO_CONTRADICT=1` may add an edge but does not select an epistemic
  winner.

Unifying live ingest with resumable contradiction review requires a separate
migration and behavior-pinned PR.

## Known limitations

- lexical contradiction detection has false negatives and false positives;
- numeric differences can represent time/scope variation rather than opposition;
- no domain-specific temporal, population or jurisdiction schema exists yet;
- no database transaction spans separate L1 and L3 fabrics;
- no dedicated CLI/API resolution command is part of the core-only baseline;
- no LLM/NLI model has decision authority;
- non-`WORLD_FACT` claim types are outside this contradiction-report path.

## Non-goals

The following are not implemented and must not be inferred:

- `last verified wins`;
- `highest confidence wins`;
- `most sources wins`;
- autonomous source-quality ranking as a final verdict;
- automatic destructive conflict resolution;
- universal semantic contradiction detection;
- causal or legal/medical domain adjudication;
- Titan cognitive contradiction reasoning inside Crystal Core.

## Test contract

The behavior suite pins:

- immutable and deterministic reports;
- content minimization and no automatic winner;
- ordinary approval failing closed;
- actor/reason/report-id/target validation;
- `COEXIST`, `CONTEXTUALIZE` and `SUPERSEDE` state/edge effects;
- restricted/stale/missing targets;
- candidate and target CAS races;
- explicit partial-supersede coexistence;
- content-free audit history;
- auxiliary metadata retry/failure reporting.
