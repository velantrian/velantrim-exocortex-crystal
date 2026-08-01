# Topic facets and curator IAM

This guide covers the two optional production-facing helpers added after the
final implementation checkpoint.

## Advisory topic facets

```python
from core.topic_facets import TopicFacet, attach_facets, filter_records

record = attach_facets(
    {"fact_id": "f1", "metadata": {}},
    [
        TopicFacet("machine-learning", 0.92, "model"),
        TopicFacet("safety", 1.0, "curator"),
    ],
)

results = filter_records([record], all_of=["safety"], min_score=0.8)
```

Facets are navigation metadata only. They must not be used to promote a fact,
change evidence, choose a contradiction winner, or claim that a record belongs
to strict Canon.

## Scoped curator authorization

```python
from core.curator_auth import (
    CuratorPrincipal,
    CuratorRole,
    authorize_conflict_decision,
)

principal = CuratorPrincipal(
    actor_id="alice",
    roles=frozenset({CuratorRole.CURATOR}),
    scopes=frozenset({"fact:new", "fact:old"}),
)

decision = authorize_conflict_decision(
    principal,
    actor="alice",
    disposition="SUPERSEDE",
    candidate_fact_id="new",
    target_fact_ids=("old",),
)
if not decision.allowed:
    raise PermissionError(decision.reason)
```

Only after authorization succeeds should the host call the canonical
`core.review.resolve_conflict` contract. Authentication remains a host concern:
OIDC, mTLS, API keys, Unix identities, or another mechanism may be used to
construct the principal.

## Multi-curator lease

```python
from core.curator_auth import CuratorLeaseRegistry

leases = CuratorLeaseRegistry()
lease = leases.acquire(
    candidate_fact_id="new",
    report_id="sha256:report",
    owner="alice",
    ttl_seconds=30,
)
if lease is None:
    raise RuntimeError("another curator is deciding this report")
try:
    # Re-read the current report, authorize, then resolve through core.review.
    ...
finally:
    leases.release(lease)
```

The bundled registry coordinates threads in one process. Multi-instance
production deployments should replace it with a database or distributed-lock
adapter while retaining report-id freshness and ESM CAS checks.
