# Advisory Topic Facets

**Status:** implemented pure/read-only baseline  
**Module:** `core.topic_facets`  
**Decision:** [ADR-017](../adr/ADR-017-ADVISORY_TOPIC_FACETS.md)

## Purpose

Topic facets answer a narrow navigation question:

> What subjects does this text appear to discuss under the current taxonomy?

They do not determine whether the text is true, well sourced or eligible for
strict Canon.

```text
claim modality (MOSC / explicit claim_type)
        ⟂
topic/domain facets (this module)
        ⟂
truth_status / ESM / source authority
```

The axes are orthogonal. For example:

```text
claim_type: HYPOTHESIS
topic facet: health/medicine
truth_status: UNVERIFIED
```

No field is inferred from another.

## Output contract

A facet contains:

```json
{
  "topic_id": "health/medicine",
  "score": 0.72,
  "matched_terms": ["disease", "treatment"],
  "assigned_by": "keyword-facet-v1",
  "taxonomy_version": "2026-08-v1",
  "status": "suggested"
}
```

The enclosing projection always contains:

```json
{
  "authoritative": false,
  "writes_memory": false,
  "score_meaning": "topic_relevance_not_truth"
}
```

The score is a deterministic lexical relevance hint. It is not:

- a probability that the classification is correct;
- epistemic confidence;
- source reliability;
- evidence coverage;
- knowledge completeness;
- permission to write or promote memory.

## Baseline behavior

- English and Russian keyword/phrase terms;
- multiple labels per text;
- deterministic ordering by score then topic id;
- explicit maximum-facet and minimum-score controls;
- abstention when nothing satisfies the threshold;
- immutable facet/projection objects;
- fresh copies when projecting fact mappings;
- standard-library only;
- no storage or network access.

Initial broad topics include:

- artificial intelligence;
- software engineering;
- security/privacy;
- physics;
- biology;
- medicine;
- climate/water/environment;
- law/governance;
- finance/business/economics.

This compact taxonomy is a baseline, not a complete ontology.

## Usage

```python
from core.topic_facets import classify_topics, project_fact_topics

projection = classify_topics(
    "AI software must preserve security and privacy",
    max_facets=3,
)

facts_with_ephemeral_topics = project_fact_topics(existing_facts)
```

`project_fact_topics()` returns new dictionaries. It does not modify the input
mappings and does not persist the projection.

## Integration boundary

Safe uses:

- grouping a read-only review list;
- filtering a local dashboard;
- corpus-composition reports;
- navigation and search refinement;
- selecting domain-specific review instructions.

Unsafe uses:

- using a topic score as confidence;
- increasing evidence weight;
- choosing a contradiction winner;
- writing directly to physical L3;
- promoting ESM or truth status;
- estimating “percentage of a domain known”.

Any future persistent topic index requires a separate schema, migration,
rebuildability and restriction/erasure review. The current projection creates no
such persistent state.

## Optional future adapters

A future local classifier may implement the same output contract, including an
optional ML/embedding adapter. It must remain opt-in and non-authoritative. The
pure-stdlib keyword classifier remains the dependency-free fallback.
