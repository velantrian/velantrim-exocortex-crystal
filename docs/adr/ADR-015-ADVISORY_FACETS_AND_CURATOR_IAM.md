# ADR-015: Advisory topic facets and scoped curator IAM

Status: implemented

## Context

Crystal needs better navigation across heterogeneous memories and stronger
production controls around explicit contradiction decisions. Neither concern may
be allowed to redefine truth, evidence, ESM state, Canon membership, or the
contradiction disposition itself.

## Decision

### Advisory topic facets

`core.topic_facets` provides normalized, multi-label metadata with bounded
scores and provenance (`curator`, `rule`, `model`, or `import`). Facets are:

- stored only under the `topic_facets` metadata key;
- deterministic and deduplicated;
- usable for optional filtering;
- never evidence, truth status, an ESM transition, or a Canon admission signal.

A caller must still use the normal authorized persistence path when attaching
facet metadata to a stored fact.

### Scoped curator authorization

`core.curator_auth` separates authenticated identity mapping from Crystal's
review logic. Hosts construct a `CuratorPrincipal` and authorize the requested
disposition before invoking the canonical `core.review.resolve_conflict`
contract.

Roles and capabilities:

| Role | COEXIST | CONTEXTUALIZE | SUPERSEDE |
|---|---:|---:|---:|
| REVIEWER | yes | no | no |
| CURATOR | yes | yes | yes |
| ADMIN | yes | yes | yes |

Every decision additionally requires:

- the payload actor to match the authenticated principal;
- scope over the candidate fact;
- scope over every supersede target;
- an executable disposition rather than `REVIEW_REQUIRED`.

Scopes use exact `fact:<fact_id>` values or the explicit wildcard `fact:*`.
Unknown roles, capabilities, scopes, actors, or dispositions fail closed.

### Multi-curator concurrency

`CuratorLeaseRegistry` supplies a thread-safe in-process lease keyed by candidate
fact and contradiction report. It prevents two curator workers in one process
from deciding the same report concurrently and uses exact owner/token release.
Expired leases may be reacquired.

Distributed deployments must provide an external lease implementation with the
same acquire/release semantics. The existing report-id freshness checks and ESM
CAS remain authoritative safeguards; a lease is an additional coordination
layer, not a substitute for them.

## Consequences

- Topic navigation improves without creating a second truth system.
- Production hosts can map OIDC, mTLS, API-token, or local identities into one
  kernel-neutral authorization contract.
- Low-privilege reviewers cannot supersede canonical facts.
- Parallel curator decisions fail closed at the coordination layer while stale
  report and CAS checks continue to protect the canonical write path.
- Existing deployments are not silently coupled to a specific identity provider
  or distributed lock service.
