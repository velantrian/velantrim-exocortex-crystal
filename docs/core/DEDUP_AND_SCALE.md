# Deduplication and Scale Contract

> Date: 2026-06-17
> Scope: deduplication and data-growth principles for Crystal
> Status: docs-only unless tied to tested runtime code.

## Principle

Duplicate frequency is not independent evidence.

Crystal must distinguish:

| Case | Treatment |
|---|---|
| same meaning + same source | duplicate / idempotent discard |
| same meaning + different independent source | corroboration candidate |
| opposite meaning | contradiction candidate |
| similar but new aspect | separate claim |

## Exact dedup

Exact or normalized-text dedup should happen before expensive semantic comparison.

Recommended field:

```text
claim_dedup_key = normalized_claim_hash
```

The dedup key should not replace provenance. It only prevents accidental duplicate storage.

## Semantic dedup

Semantic dedup should be treated as a candidate decision, not as verified equivalence.

Recommended safeguards:

- domain blocking;
- threshold calibration;
- human or rule-based review for merges;
- no automatic evidence promotion;
- no automatic truth promotion.

## Scale direction

Crystal should avoid unbounded O(N^2) scans as the corpus grows.

Recommended progression:

1. exact key index;
2. stable ordering for retrieval and export;
3. FTS/BM25 retrieval for lexical lookup;
4. optional ANN/vector layer for candidate generation;
5. graph-neighbour limits for relation traversal;
6. batch import with explicit review and index-sync semantics.

## Index integrity

A fact store and its retrieval indexes must not drift silently.

Batch writes should either:

- update retrieval indexes in the same operation; or
- mark the index dirty and require a rebuild before confident retrieval.

## Public wording

Safe:

```text
Crystal includes a deduplication and scale plan that separates duplicates, corroboration and contradictions.
```

Avoid unless implemented:

```text
Crystal has validated a million-fact verified graph.
```

## Claude Code follow-up

Claude Code should verify current dedup paths before changing them. In particular, check that single write, batch write and any async write path share the same normalization, validation, dedup and index-sync contract.
