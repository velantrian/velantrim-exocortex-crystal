# ADR-018 — Authenticated curator write composition

- **Status:** Proposed implementation draft in issue #316
- **Date:** 2026-08-06
- **Scope:** public approve, reject, force-approve and contradiction-resolution surfaces across HTTP and CLI

## Context

Crystal already contained useful principal, role, capability, fact-scope and
process-local lease primitives. Public HTTP and CLI review writes still accepted
an `actor` string as request input and delegated directly to `core.review`. A
bearer token authenticated access to the API, but did not by itself prove that
the recorded actor, action capability and candidate/target scopes belonged to
the authenticated identity. The main CLI had the same problem without the HTTP
token: `--actor` could select the audit identity.

## Decision

Every bundled public curator write composes this order:

```text
authenticated/configured host identity
→ CuratorPrincipal
→ action capability
→ candidate and target scopes
→ current contradiction report + process-local lease when applicable
→ canonical core.review operation
```

The audit actor is always `principal.actor_id`. A compatibility actor field or
CLI flag may only assert the same identity; it never establishes identity.

The bundled API maps one bearer token to one explicitly configured principal.
The main CLI and conflict CLI use the same principal variables without the HTTP
token:

```text
VELANTRIM_CURATOR_ACTOR
VELANTRIM_CURATOR_ROLES
VELANTRIM_CURATOR_SCOPES
```

Unknown, missing or partial principal configuration fails closed. HTTP curator
writes return `403`; CLI write commands exit `2` for configuration failure and
`3` for capability, scope or actor mismatch. Read endpoints retain their
existing bearer-token contract.

A bearer token that contains leading/trailing whitespace or is whitespace-only
is invalid configuration and fails with HTTP `401`. It cannot be used as a
trivial secret and cannot activate unauthenticated-local mode.

## Capabilities

- `APPROVE`
- `REJECT`
- `FORCE_APPROVE` — admin only in the bundled role map
- `RESOLVE_COEXIST`
- `RESOLVE_CONTEXTUALIZE`
- `RESOLVE_SUPERSEDE`

A reviewer may approve/reject and choose COEXIST. A curator may additionally
contextualize or supersede. Only an admin may force-approve a blocked gate.
`REVIEW_REQUIRED` describes a state, not an executable disposition, and is
excluded from public HTTP/CLI choices.

## Local development

`VELANTRIM_API_ALLOW_UNAUTH_LOCAL=1` is an explicit unauthenticated **HTTP**
local mode. When no bearer token is configured, the bundled API always maps
this mode to the fixed synthetic broad principal `api-curator`. Curator actor,
role and scope environment values are deliberately ignored because no
authentication proves those identities. Local force approval requires an exact
`api-curator` assertion.

This preserves local single-user HTTP workflows but is not authenticated IAM,
multi-tenancy or a production deployment recommendation. When a valid bearer
token is configured, the synthetic local principal is disabled and all three
curator configuration variables are required.

The main CLI has no unauthenticated-local fallback. `review-approve`,
`review-reject` and contradiction-decision commands always require explicit
principal configuration.

## Conflict lease

The public conflict composer normalizes candidate/target IDs, re-reads the
current report, pins its report id, authorizes candidate/target scopes and
acquires the existing process-local lease before calling
`core.review.resolve_conflict`. Lease keys use length-prefixed fields so IDs
containing `:` cannot collide. The lease is released in a `finally` block.
This is not a distributed lock; multi-instance deployments still require an
external fencing adapter.

## Consequences

### Positive

- request text and CLI flags cannot choose the accountable audit actor;
- actor spoof, missing principal, missing capability and scope denial are
  zero-mutation failures;
- force approval has an explicit separate capability;
- SUPERSEDE authorizes every normalized target;
- the bundled conflict route is registered by `core.api` and returns `404` for
  unknown facts;
- all CLI curator decisions require explicit principal configuration;
- explicit unauthenticated HTTP mode has one invariant synthetic identity;
- partial principal configuration and malformed bearer secrets fail closed.

### Limitations

- the bundled API is one-token/one-principal, not a complete IdP;
- token rotation, revocation, tenant policy administration and per-token role
  mapping remain host/deployment work;
- the included lease is process-local only;
- independent current-head review and full CI are required before acceptance.

## Non-goals

- no truth or contradiction winner is selected by authorization;
- no mandatory OIDC/cloud provider;
- no production multi-tenant certification claim;
- no weakening of bearer-token fail-closed defaults;
- no replacement of `core.review` as the canonical mutation contract.
