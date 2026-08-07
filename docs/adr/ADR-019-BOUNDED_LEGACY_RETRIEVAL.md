# ADR-019 — Bounded no-fingerprint retrieval and explicit reindex

- **Status:** Proposed implementation draft in issue #317
- **Date:** 2026-08-06
- **Scope:** strict read-only query/search on legacy L3 stores

## Context

A store without an embedder fingerprint cannot safely use vectors as a declared compatible
index. The prior compatibility fallback loaded every physical graph fact, tokenised every
claim and sorted all matches. A public request could therefore amplify memory and CPU work
with corpus size even when output `k` was small.

## Decision

Public reads must either use a bounded candidate adapter or fail closed with
`legacy_store_requires_reindex`.

- Fingerprinted stores retain the existing vector/hybrid retrieval.
- No-fingerprint SQLite and Mock stores use a deterministic candidate window capped
  independently of output `k`.
- Unsupported backends return a stable reindex-required result.
- Query never writes a fingerprint or rebuilds vectors.
- Full vector regeneration is an explicit operator command.

## Candidate bound

The default cap is 256 and the hard supported range is 1–4096. SQLite uses its fact-id
primary-key order with `LIMIT`; Mock uses `heapq.nsmallest` to select the deterministic
smallest-ID window without a full key sort. Python never materialises or scores more than
the cap on this path and never invokes `all_facts()`.

The window is deliberately degraded: it may miss a relevant fact outside the cap. That
tradeoff is preferable to an unbounded remote cost-amplification path. Responses disclose
the mode, examined count and recommendation to reindex.

## Reindex boundary

`python -m core.reindex_embeddings rebuild` is an explicit maintenance action with
backend-specific crash semantics:

- **SQLite:** clears the active fingerprint before work, rebuilds/commits vectors in
  bounded batches, and restores the fingerprint only after complete success. A failed
  rebuild therefore leaves the fingerprint absent and public reads on bounded legacy
  retrieval.
- **Mock:** builds a replacement vector map separately and atomically swaps it with the
  new fingerprint only after complete success. A failed rebuild preserves the previous
  complete vectors/fingerprint.

Both adapters leave stored fact payloads, ESM state, truth status, restriction, graph
edges and audit unchanged. Neither can expose a partial replacement as a compatible
complete index.

## Consequences

### Positive

- public candidate materialisation/scoring has a testable cap;
- Mock avoids the prior full `O(N log N)` key sort and uses `O(N log k)` selection;
- legacy reads remain non-mutating;
- unsupported adapters fail with an actionable stable code;
- partial vector rebuilds cannot masquerade as a compatible complete index;
- no new mandatory dependency is introduced.

### Costs and limitations

- bounded lexical prefix windows reduce recall;
- Mock still scans keys to select the smallest bounded window;
- reindex can be a long operator task;
- Ladybug/other backends need separately reviewed reindex/bounded adapters;
- the informational benchmark does not establish a production latency SLO.

## Non-goals

- no automatic ingest, promotion or contradiction decision;
- no silent fingerprint initialisation;
- no truth or source-authority inference from lexical rank;
- no mandatory FTS/cloud search service;
- no shared-runner hard latency gate.
