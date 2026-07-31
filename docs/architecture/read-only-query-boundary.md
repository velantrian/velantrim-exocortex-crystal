# Read-Only Query Boundary

**Status:** `IMPLEMENTED · HTTP + CLI + MCP_SEARCH · BASELINE_HARDENING`  
**Initial HTTP implementation:** merged PR #265 (`cd6fd44`)  
**Invariant:** asking a question or searching memory must not become ingestion, promotion, maintenance or research-state mutation.

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
ordinary query.

Crystal therefore exposes one read-only service module for public query surfaces:

```text
core.query_pipeline.query()   → answer / bounded refusal
core.query_pipeline.search()  → ranked existing graph facts
```

## Routed public surfaces

### HTTP

```text
POST /ask or GET /receipt
    → core.aio.arun
    → core.query_pipeline.query
```

### CLI

```text
velantrim ask <query>
velantrim receipt <query>
python -m core.cli ask <query>
python -m core.cli receipt <query>
    → core.cli.main
    → core.query_pipeline.query
```

The read-only route is implemented inside the canonical CLI module itself. All
other established commands retain their existing explicit write/read behaviour.

### MCP search

```text
MCP tools/call: search
    → core.mcp_server._tool_search
    → core.query_pipeline.search
```

The search contract resolves candidates only against facts already present in
L3, reads L1 deny-dominantly for restrictions and terminal state, excludes
processing-restricted rows before returning content, and never stores unknown
retrieval candidates.

## Forbidden durable effects

The read-only query/search service must not:

- create or update L0/L1 fact rows;
- transition ESM state;
- call TruthGate as an admission decision;
- create, update or delete L3 facts, relations, entities or mentions;
- drain, enqueue or clear the L3 outbox;
- attach evidence or add audit events;
- initialize an embedding-space fingerprint merely because a query was made;
- record episodic context;
- trigger NeuroCore, reconsolidation or adaptive/research-state writes.

It may read local storage, compute retrieval/rendering results, increment
content-free in-process query metrics, and create the requested response or
receipt object. An optional configured generator may phrase an answer, but
CanonicalView remains the strict grounding authority for `query()`.

## Retrieval behaviour

When the graph store already has an embedding fingerprint, the service may reuse
the mature hybrid retriever because its compatibility check is then read-only.

For a legacy store containing graph nodes but no fingerprint, the service uses a
bounded lexical scan. It does not stamp metadata as a side effect of reading.
Candidates that do not resolve to an existing L3 fact are discarded and never
written into memory.

The fingerprint is checked before any full-store lexical fallback. On the normal
fingerprinted path, no unnecessary whole-graph materialization is performed.

## Search is not strict Canon

`search()` is an inspection/retrieval surface, not an answer-authority surface.
It returns explicit `truth_status`, `claim_type` and `epistemic_state` metadata
and must not imply that every physical L3 node belongs to strict CanonicalView.
Processing-restricted rows are excluded before claim/source content is returned.

`query()` additionally runs Guardian's structural check and CanonicalView's
strict projection before producing a confident answer.

## Immutable trust reconciliation

L3 supplies stored claim and verdict fields. L1 is consulted deny-dominantly for
a newer terminal ESM state, processing restriction or trust-metadata drift.

The resolver does not assemble those fields by mutating a shared dictionary.
It first creates a frozen, slotted `core.trust_snapshot.TrustSnapshot`, completes
all consistency decisions, and only then emits a fresh compatibility mapping for
Guardian and CanonicalView.

```text
physical L3 node
        +
optional L1 deny state
        +
retrieval score
        ↓
immutable TrustSnapshot
        ↓
fresh fact mapping
        ↓
Guardian + CanonicalView
```

Representation-only differences do not create false trust conflicts:

- confidence uses numeric tolerance;
- missing L3 `claim_type` uses the established `WORLD_FACT` default;
- equivalent normalized values remain equivalent.

Genuine confidence, claim-type, source-status or non-terminal ESM disagreement
sets the snapshot to `STORE_STATE_CONFLICT` and records only content-free
conflict categories. Malformed confidence becomes unknown rather than being
coerced into a trusted `0.0` value. A confirmed restriction on either store wins.

This is a boundary-object baseline, not a repository-wide fact-schema migration.
See [ADR-012](../adr/ADR-012-IMMUTABLE_TRUST_SNAPSHOT.md).

## Stable query response markers

Every result from `core.query_pipeline.query()` contains:

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

Regression tests assert that HTTP, CLI query commands and MCP search leave
unchanged:

- L1 fact contents;
- L3 facts, edges and mentions;
- pending L3 outbox contents;
- embedding fingerprint, including an unset legacy fingerprint;
- adaptive verification state;
- unknown retrieval candidates.

Additional tests assert that:

- restricted search rows and their content are not returned;
- invalid search limits fail explicitly;
- CLI `ask` and `receipt` call the public read-only query service directly;
- MCP search delegates to the public read-only search contract;
- trust snapshots are frozen, scalar-only and independent of input mutation;
- L1 terminal states/restrictions and genuine metadata drift fail closed.

Repository CI remains the authoritative verification evidence for each merged
revision.

## Explicit compatibility residual

`core.pipeline.run()` remains admission-capable for legacy/internal callers that
explicitly choose it. It is no longer used by CLI `ask` or `receipt`. Removing or
renaming that compatibility function requires a separate deprecation cycle.

The legacy admission path still reconciles transient mutable fact dictionaries
through its existing behaviour-pinned functions. Adopting `TrustSnapshot` there
requires a separate migration because that path intentionally performs L1 repair
and L3 admission work, unlike this pure read boundary.

## Grant boundary

This is corrective trust-boundary hardening of the existing Crystal baseline. It
adds no NLnet milestone, budget item, research mechanism, model dependency,
network default or certification claim.

The pre-synchronization architecture note is preserved byte-for-byte at:

`docs/archive/grant-sync/READ_ONLY_QUERY_BOUNDARY_PRE_SYNC_2026-07-30.md`
