# Read-Only Query Boundary

**Status:** `IMPLEMENTED · PR_265_MERGED · HTTP_QUERY_SURFACES_ONLY · BASELINE_HARDENING`  
**Implementation commit:** `cd6fd44ff4ac8c715121cae1996aa484f11ef250`  
**Invariant:** asking a question must not become ingestion, promotion, maintenance or research-state mutation.

## Why this boundary exists

The historical `core.pipeline.run()` combines two responsibilities:

```text
query / retrieval
    +
admission / ESM transition / L3 merge
```

That compatibility path can store retrieved rows in L0/L1, promote a previously
unknown candidate, drain the L3 outbox and optionally add episodic graph links.
Those behaviours belong to explicit admission or maintenance operations—not an
ordinary HTTP question.

PR #265 introduced a separate HTTP query contract:

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
- create, update or delete L3 facts, relations, entities or mentions;
- drain, enqueue or clear the L3 outbox;
- attach evidence or add audit events;
- initialize an embedding-space fingerprint merely because a question was asked;
- record episodic context;
- trigger NeuroCore, reconsolidation or adaptive/research-state writes.

It may read local storage, compute retrieval and rendering results, increment
content-free process metrics, and create the requested response/receipt object. An
optional configured generator may phrase an answer, but CanonicalView remains the
grounding authority.

## Retrieval behaviour

When the canonical store already has an embedding fingerprint, the query path may
reuse the mature hybrid retriever because its compatibility check is then
read-only.

For a legacy store that contains canonical nodes but has no fingerprint, the HTTP
query path performs a bounded lexical scan. It does not stamp metadata as a side
effect of reading. Retrieval candidates that do not resolve to an existing L3
canonical node are discarded and never written into memory.

The normal fingerprinted path checks the fingerprint before considering a
full-store lexical fallback, avoiding unnecessary whole-Canon materialization on
every HTTP request.

## Trust reconciliation

L3 supplies canonical claim and verdict fields. L1 is consulted deny-dominantly
for a newer terminal ESM state or a processing restriction.

Representation-only differences do not create false trust conflicts:

- confidence uses the established numeric tolerance;
- missing `claim_type` uses the same default as the served fact;
- equivalent normalized values remain equivalent.

Genuine confidence, claim-type or source-status disagreement still fails closed.

## Stable response markers

Every result from the implemented HTTP path contains:

```json
{
  "read_only": true,
  "query_policy": "canonical_read_only"
}
```

Expected bounded failures include stable `reason_code` values such as:

- `no_local_retrieval_results`;
- `no_canonical_retrieval_results`;
- `guardian_rejected_canonical_read`;
- `insufficient_strict_canonical_grounding`.

When an `episode` argument is supplied, the response explicitly reports that it
was not recorded.

## Acceptance evidence

Regression tests assert that an HTTP query leaves unchanged:

- L1 fact contents;
- L3 facts, edges and mentions;
- pending L3 outbox contents;
- embedding fingerprint, including an unset legacy fingerprint;
- adaptive verification state;
- unknown retrieval candidates.

They also assert that `core.aio.arun()`—and therefore FastAPI `/ask` and `/receipt`—
delegates to the strict read-only query pipeline.

CI run `30284938992` completed all seven permanent jobs successfully on the
reviewed PR head, including 1713 passed, 12 skipped and 100% coverage on Python
3.11, plus the Python 3.12 matrix job, Ruff, security, Docker, eval and JSONL gates.

## Residual compatibility scope

This implementation does **not** claim that every historical caller is migrated:

- `core.pipeline.run()` remains admission-capable;
- CLI `ask` and `receipt` still call that compatibility path;
- MCP exposes no explicit mutation tools, but MCP search currently calls retrieval
  code that may initialize an unset embedding fingerprint.

MCP is therefore outside the zero-mutation HTTP guarantee until a separate
follow-up removes or explicitly governs that metadata side effect.

## Grant boundary

This is corrective trust-boundary hardening of the existing Crystal baseline. It
adds no NLnet milestone, budget item, research mechanism, model dependency,
network default or certification claim.

The pre-synchronization architecture note is preserved byte-for-byte at:

`docs/archive/grant-sync/READ_ONLY_QUERY_BOUNDARY_PRE_SYNC_2026-07-30.md`
