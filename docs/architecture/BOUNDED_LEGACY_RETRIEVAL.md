# Bounded legacy retrieval and explicit embedding reindex

**Status:** implementation draft for issue #317.  
**Boundary:** read-only public query vs explicit operator maintenance.

## Problem

A legacy L3 store may contain nodes and vectors but no embedder fingerprint. The previous
read-only fallback called `all_facts()`, tokenised every claim, sorted every match and only
then applied output `k`. Output was bounded; candidate work was not.

## Public read contract

```text
fingerprint present
  → existing vector/hybrid retrieval

fingerprint absent + Mock/SQLite backend
  → deterministic bounded node window
  → lexical overlap ranking
  → TrustSnapshot / restriction reconciliation
  → CanonicalView / Guardian

fingerprint absent + unsupported backend
  → legacy_store_requires_reindex
```

The candidate window is independent of output `k` and defaults to 256. It can be adjusted
within a hard range of 1–4096 through:

```text
VELANTRIM_LEGACY_QUERY_CANDIDATES=256
```

SQLite reads `ORDER BY fact_id LIMIT ?` over the primary key and materialises only that
window in Python. Mock selects the deterministic smallest-ID window with
`heapq.nsmallest`, avoiding a full `O(N log N)` key sort while still materialising and
scoring at most the configured window. Neither path calls `all_facts()`.

This is a degraded compatibility path. A relevant fact outside the window may not be
found. Responses expose `retrieval.mode=bounded_legacy_lexical`, candidates examined,
the cap and `reindex_recommended=true`.

## Stable reason code

Backends without a reviewed bounded legacy adapter fail closed with:

```text
legacy_store_requires_reindex
```

HTTP/CLI `ask` returns this in `reason_code`. Structured search adapters use
`search_result()`. The compatibility list-only `search()` remains available for callers
that do not consume status metadata.

## Explicit operator reindex

Public query never stamps a fingerprint or rebuilds vectors. An operator performs the
full maintenance pass explicitly:

```bash
python -m core.reindex_embeddings status
python -m core.reindex_embeddings rebuild --batch-size 100
```

Both reviewed adapters recompute vectors from stored claim text, report total/processed/
skipped/backend/embedder, and leave fact JSON, ESM state, truth status, restriction,
edges and audit unchanged. Their crash semantics differ deliberately:

### SQLite backend

1. removes the active fingerprint before rebuilding;
2. clears and recomputes vectors;
3. commits progress in bounded batches;
4. writes the active fingerprint only after complete success.

If SQLite rebuilding fails after a committed batch, the fingerprint remains absent.
Public reads stay on the bounded compatibility path rather than treating partial vectors
as a compatible complete index.

### Mock backend

1. builds a replacement vector map without modifying the currently complete map;
2. preserves the existing vectors and fingerprint if rebuilding fails;
3. atomically swaps in the replacement vectors and new fingerprint only after success.

Mock therefore keeps the previous complete index usable on failure; it does not expose a
partial replacement as compatible.

The reviewed reindex adapters in this draft are `MockL3Graph` and `SqliteL3Graph`.
Other backends require an explicit adapter and otherwise fail with
`ReindexUnsupported`.

## Security and truth boundary

The bounded index/window is navigation only:

```text
lexical overlap ≠ truth
candidate rank ≠ Canon membership
reindex ≠ admission
fingerprint ≠ evidence
```

Every candidate still resolves through the existing L3/L1 trust snapshot. Restricted
content is excluded before public return. Malformed or conflicting trust metadata remains
fail closed. Query performs no L1/L3/audit/outbox/fingerprint mutation.

## Performance evidence

Run the informational benchmark:

```bash
python scripts/bench_legacy_retrieval.py --sizes 1000 10000
python scripts/bench_legacy_retrieval.py --sizes 30000 --json-out legacy-30k.json
```

It reports p50/p95 and maximum candidates examined. Shared/hosted-runner latency is not a
hard SLO; the invariant under test is that candidate materialisation and scoring do not
exceed the configured cap as corpus size grows. Mock's `nsmallest` selection scans keys
but avoids full sorting; SQLite delegates the ordered limit to its primary-key index.

## Limitations

- deterministic prefix windows trade recall for bounded materialisation/scoring;
- Mock key selection remains `O(N log k)` while avoiding `O(N log N)` full sorting;
- reindex is an explicit potentially long maintenance operation;
- no mandatory FTS, external search service or cloud dependency is added;
- no automatic reindex occurs during query;
- controlled-environment capacity/SLO policy remains separate future work.
