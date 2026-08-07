# Topic facets and curator IAM

This guide covers advisory topic metadata and the authenticated curator
composition proposed in issue #316 / ADR-018. Deployment threats and controls
are documented in [Curator write authentication](./security/CURATOR_WRITE_AUTH.md).

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
from core.curator_auth import CuratorPrincipal, CuratorRole
from core.curator_runtime import resolve_conflict_as_principal

principal = CuratorPrincipal(
    actor_id="alice",
    roles=frozenset({CuratorRole.CURATOR}),
    scopes=frozenset({"fact:new", "fact:old"}),
)

result = resolve_conflict_as_principal(
    principal,
    "new",
    disposition="SUPERSEDE",
    requested_actor="alice",  # optional exact-match assertion only
    reason="new external evidence",
    target_fact_ids=("old",),
    expected_report_id="sha256:report",
)
```

The public composer performs capability and normalized candidate/target scope
checks, re-reads and pins the current contradiction report, acquires a
process-local lease and then delegates to the canonical
`core.review.resolve_conflict` contract. The audit actor always comes from
`principal.actor_id`.

## Bundled FastAPI mapping

The built-in HTTP service supports one bearer token mapped to one configured
principal. Inject `VELANTRIM_API_TOKEN` from runtime secret management; do not
place a token value in source-controlled examples or environment files.

```text
VELANTRIM_CURATOR_ACTOR=alice
VELANTRIM_CURATOR_ROLES=CURATOR
VELANTRIM_CURATOR_SCOPES=fact:new,fact:old
```

A token without complete curator configuration may still access authorized read
surfaces, but curator writes fail closed with HTTP `403`. Roles, scopes and
actor values are exact enum/configuration values; unknown, empty or partial
values fail closed. Whitespace-padded/whitespace-only bearer token values are
invalid and fail with HTTP `401`.

Write capabilities are explicit:

```text
REVIEWER → APPROVE, REJECT, RESOLVE_COEXIST
CURATOR  → reviewer capabilities + CONTEXTUALIZE + SUPERSEDE
ADMIN    → all capabilities, including FORCE_APPROVE
```

`REVIEW_REQUIRED` is not an executable disposition and is excluded from HTTP
and CLI choices.

Under bearer authentication, a body `actor` is optional. When supplied on
approve, reject or conflict resolution, it must match the authenticated
principal exactly or the operation fails before mutation. It never selects the
audit identity. Force approval requires an explicit reason and the dedicated
capability, but it does not need a duplicate actor when authentication already
established the principal.

Unknown conflict fact IDs return HTTP `404`, matching the other review
endpoints.

## Main CLI mapping

The main CLI uses the same principal variables for every curator write. It does
not use `VELANTRIM_API_TOKEN` and it has no unauthenticated-local fallback:

```bash
export VELANTRIM_CURATOR_ACTOR=alice
export VELANTRIM_CURATOR_ROLES=CURATOR
export VELANTRIM_CURATOR_SCOPES='fact:*'

python -m core.cli review-approve FACT_ID
python -m core.cli review-reject FACT_ID --reason 'not reliable'
python -m core.conflict_surfaces FACT_ID \
  --disposition COEXIST \
  --reason 'independent contexts'
```

CLI `--actor` is only an optional exact-match assertion. Missing/malformed
principal configuration exits `2`; authorization denial exits `3`; both paths
must perform zero canonical mutation. Force approval requires `ADMIN`.

## Explicit local-development HTTP mode

`VELANTRIM_API_ALLOW_UNAUTH_LOCAL=1` remains an explicit unauthenticated local
HTTP mode. When no bearer token is configured, the bundled API always maps it
to the fixed synthetic broad principal `api-curator`; configured curator actor,
role and scope variables are ignored because no authentication proves them.
This is not authenticated IAM and must not be used to claim production security
or multi-tenancy.

In this mode a reject-body actor is ignored because request text cannot create
an authenticated identity. Force approval must explicitly name `api-curator`;
the audit actor remains the synthetic principal.

When a valid bearer token is set, the synthetic local principal is disabled and
all curator configuration variables are required.

## Multi-curator lease

The bundled registry coordinates threads in one process. It protects the current
candidate/report tuple while a conflict decision is applied. Lease keys are
length-prefixed so identifiers containing `:` cannot produce ambiguous pairs.
The registry is not a distributed lock and has no cross-process fencing
guarantee.

Multi-instance production deployments must provide an external lease/fencing
adapter while retaining:

- authenticated/configured principal mapping;
- capability and normalized candidate/target scope checks;
- report-id freshness;
- ESM optimistic concurrency;
- accountable audit identity;
- zero mutation on authorization failure.
