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
primary-key order with `LIMIT`; Mock uses sorted ids. Python never materialises more than
the cap on this path and never invokes `all_facts()`.

The window is deliberately degraded: it may miss a relevant fact outside the cap. That
tradeoff is preferable to an unbounded remote cost-amplification path. Responses disclose
the mode, examined count and recommendation to reindex.

## Reindex boundary

`python -m core.reindex_embeddings rebuild` is an explicit maintenance action. It clears
its compatibility marker before work, rebuilds vectors in batches, and writes the active
fingerprint only after complete success. Stored fact payloads and truth state remain
unchanged.

## Consequences

### Positive

- public candidate work has a testable cap;
- legacy reads remain non-mutating;
- unsupported adapters fail with an actionable stable code;
- partial vector rebuilds cannot masquerade as a compatible complete index;
- no new mandatory dependency is introduced.

### Costs and limitations

- bounded lexical prefix windows reduce recall;
- reindex can be a long operator task;
- Ladybug/other backends need separately reviewed reindex/bounded adapters;
- the informational benchmark does not establish a production latency SLO.

## Non-goals

- no automatic ingest, promotion or contradiction decision;
- no silent fingerprint initialisation;
- no truth or source-authority inference from lexical rank;
- no mandatory FTS/cloud search service;
- no shared-runner hard latency gate.
