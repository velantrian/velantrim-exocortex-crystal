# ADR-017: Topic facets are advisory read-only projections

- **Status:** Accepted baseline
- **Date:** 2026-08-01
- **Scope:** navigation and corpus organization only

## Context

Crystal classifies claim modality through existing mechanisms such as MOSC, but
modality and subject domain are different axes. A claim can be a hypothesis about
medicine, an opinion about software, or a verified fact about physics.

A domain classifier becomes dangerous if its score is confused with truth,
evidence quality, source authority or epistemic confidence.

## Decision

Crystal adds a dependency-free, bilingual, multi-label topic projection with the
following fixed boundary:

```text
topic relevance
    ≠ truth status
    ≠ epistemic confidence
    ≠ evidence completeness
    ≠ source authority
    ≠ admission permission
```

`core.topic_facets` is pure and read-only. It imports no storage, ESM, TruthGate,
CanonicalView or review module. It returns immutable `TopicFacet` and
`TopicProjection` values and can attach a fresh ephemeral projection to copies of
fact mappings.

Every projection declares:

- `authoritative: false`;
- `writes_memory: false`;
- `score_meaning: topic_relevance_not_truth`;
- classifier and taxonomy versions;
- `status: suggested`.

## Baseline classifier

The first classifier uses a compact English/Russian weighted keyword taxonomy.
It supports multiple labels, deterministic ordering, explicit abstention and a
configurable relevance threshold.

Scores are bounded lexical relevance hints. They are not calibrated
probabilities. A larger score means that more/stronger terms from one topic were
matched under this taxonomy; it does not mean that a larger fraction of a field
is known or that the text is more truthful.

## Consequences

- topic grouping can be added to review dashboards and corpus reports without
  changing Canon;
- modality remains separate from domain;
- taxonomy drift is testable and versioned;
- alternative local classifiers may preserve the same output contract later;
- no BERT, LLM, network or cloud dependency is required by the baseline;
- callers must explicitly persist any future topic metadata through a separately
  reviewed schema/write-path decision.

## Prohibited authority

The topic classifier must never:

- assign `VERIFIED` or another truth status;
- advance or rewrite ESM;
- bypass Guardian, TruthGate or CanonicalView;
- write directly to L3;
- erase, restrict or merge facts;
- resolve contradictions;
- promote a claim because a topic score is high;
- convert topic coverage into a statement such as “the system knows X% of
  medicine”.

## Non-goals

- no ontology induction;
- no autonomous question generation;
- no domain-expert adjudication;
- no persistent topic index in this first slice;
- no mandatory machine-learning model;
- no claim that the compact taxonomy covers all languages or domains.
