# Read-Only Query Boundary

**Status:** first runtime P0 slice · HTTP query surfaces · draft PR · no grant-scope change  
**Invariant:** asking a question must not become ingestion, promotion, maintenance, or research-state mutation.

## Why this boundary exists

The historical `core.pipeline.run()` combines two responsibilities:

```text
query / retrieval
    +
admission / ESM transition / L3 merge
```

That compatibility path can store retrieved rows in L0/L1, promote a previously
unknown candidate, drain the L3 outbox, and optionally add episodic graph links.
Those behaviours are valid only in explicit ingestion or maintenance operations.
They are not valid side effects of an ordinary question.

This slice introduces a separate query contract:

```text
HTTP /ask or /receipt
    → core.aio.arun
    → core.query_pipeline.query
    → read existing L3 Canon
    → resolve deny-dominant L1 restrictions/state
    → Guardian structural check
    → CanonicalView strict projection
    → bounded answer or insufficient-evidence result
```

## Forbidden durable effects

`core.query_pipeline.query()` must not:

- create or update L0/L1 fact rows;
- transition ESM state;
- call TruthGate as an admission decision;
- create, update, or delete L3 facts, relations, entities, or mentions;
- drain, enqueue, or clear the L3 outbox;
- attach evidence, create receipts, or add audit events;
- initialise an embedding-space fingerprint merely because a question was asked;
- record episodic context;
- trigger NeuroCore, reconsolidation, or other adaptive/research-state writes.

It may read local storage, compute retrieval and rendering results, and increment
content-free process metrics. An optional configured generator may phrase the answer,
but CanonicalView remains the grounding authority.

## Retrieval behaviour

When the canonical store already has an embedding fingerprint, the query path may
reuse the mature hybrid retriever because its compatibility check is then read-only.

For a legacy store that contains canonical nodes but has no fingerprint, the query
path performs a bounded lexical scan. It does not stamp metadata as a side effect of
reading. Retrieval candidates that do not resolve to an existing L3 canonical node
are discarded and never written into memory.

## Stable response markers

Every result from the new path contains:

```json
{
  "read_only": true,
  "query_policy": "canonical_read_only"
}
```

Expected bounded failures also include a stable `reason_code`, such as:

- `no_local_retrieval_results`;
- `no_canonical_retrieval_results`;
- `guardian_rejected_canonical_read`;
- `insufficient_strict_canonical_grounding`.

If an `episode` argument is supplied, the response explicitly reports that it was not
recorded.

## Acceptance evidence

Regression tests assert that a query leaves unchanged:

- L1 fact contents;
- L3 facts, edges, and mentions;
- L3 outbox contents;
- embedding fingerprint;
- unknown retrieval candidates.

They also assert that `core.aio.arun()`—and therefore the FastAPI `/ask` and `/receipt`
surfaces—delegates to the strict read-only pipeline.

## Residual compatibility scope

This first slice deliberately does **not** claim that every historical caller is already
migrated. `core.pipeline.run()` remains an admission-capable compatibility path, and the
CLI `ask` / `receipt` commands still call it. They must be migrated or explicitly renamed
in a follow-up after downstream compatibility tests are updated.

MCP search already calls the pure retrieval function and does not expose mutation tools.

## Grant boundary

This is corrective trust-boundary hardening of the existing Crystal baseline. It adds no
new NLnet milestone, budget item, research mechanism, model dependency, network default,
or certification claim.
