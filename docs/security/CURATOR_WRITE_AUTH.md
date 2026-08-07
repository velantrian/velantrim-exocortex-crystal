# Curator write authentication and authorization boundary

**Status:** implementation draft for issue #316 / ADR-018.  
**Scope:** approve, reject, force-approve and explicit contradiction decisions across HTTP and CLI.

## Security objective

A public caller must not be able to choose the curator identity later recorded in
audit/provenance. Authentication establishes an identity; authorization then proves the
required capability and candidate/target scopes before `core.review` may mutate state.

```text
authenticated identity
→ CuratorPrincipal
→ capability + scopes
→ report freshness + process-local lease
→ canonical review mutation
```

## Bundled HTTP deployment model

The optional FastAPI service supports one bearer token mapped to one curator principal.
Load `VELANTRIM_API_TOKEN` from the host's runtime secret manager; never place a token
value in source files, examples, shell history or committed environment files.

```text
VELANTRIM_CURATOR_ACTOR=alice
VELANTRIM_CURATOR_ROLES=CURATOR
VELANTRIM_CURATOR_SCOPES=fact:new,fact:old
```

The three curator variables are mandatory for write operations whenever a bearer token is
configured. Missing or malformed principal values return HTTP `403`; the system does not
silently promote the token to an administrator. A whitespace-padded or whitespace-only
`VELANTRIM_API_TOKEN` is invalid configuration and fails closed with HTTP `401`; it never
enables unauthenticated-local mode.

This mapping is intentionally narrow. It does not provide:

- multiple token/principal records;
- token issuance, rotation or revocation;
- OIDC, mTLS or enterprise-directory integration;
- tenant isolation or policy administration;
- distributed lease/fencing guarantees.

A production host may replace the mapping with its own authentication dependency as long
as it returns a validated `CuratorPrincipal` and preserves the same authorization order.

## Bundled CLI contract

All write-capable curator commands require the same principal mapping, even though the
main CLI does not use the HTTP bearer token:

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

`--actor` is only an optional exact-match assertion. It never establishes identity. A
missing/malformed principal configuration exits with code `2`; capability, scope or actor
mismatch exits with code `3`; both paths must have zero canonical mutation. Force approval
requires `ADMIN` plus a non-empty reason.

## Threats and controls

| Threat | Control |
|---|---|
| Request body or CLI flag claims `actor=admin` | audit actor is derived from `principal.actor_id`; supplied actor is only an exact-match assertion |
| Bearer token is valid but curator mapping is absent | curator writes fail with `403` |
| CLI principal mapping is absent | write command exits `2` before mutation |
| Reviewer attempts force approval | separate `FORCE_APPROVE` capability; bundled map grants it only to `ADMIN` |
| Reviewer attempts CONTEXTUALIZE/SUPERSEDE | explicit disposition capability denial before mutation |
| Caller submits `REVIEW_REQUIRED` as a decision | excluded from executable HTTP/CLI disposition choices |
| Curator acts outside candidate scope | normalized `fact:<id>` / `fact:*` scope check before mutation |
| SUPERSEDE includes one unauthorized target | every normalized target is checked; whole operation is denied |
| Report changes between display and decision | current report is re-read and its report id is passed to the canonical mutation |
| Two local workers decide the same report | process-local candidate/report lease; one worker receives `CURATOR_DECISION_LEASE_BUSY` |
| Authorization fails after partial mutation | authorization/report/lease checks occur before `core.review`; denial tests require zero mutation |
| Malformed roles/scopes or partial configuration | enum/non-empty/full-set validation fails closed |
| Legacy IDs contain `:` | length-prefixed lease-key encoding prevents candidate/report pair collisions |
| Unknown conflict fact over HTTP | endpoint returns `404`, consistent with other review endpoints |

## Explicit local-development HTTP mode

`VELANTRIM_API_ALLOW_UNAUTH_LOCAL=1` permits an unauthenticated local HTTP process and
maps it to the fixed synthetic broad principal `api-curator`. Curator environment values
are deliberately ignored in this mode because no authentication proves those identities.
This preserves single-user development workflows while keeping the audit actor explicit.
It is not authentication, production IAM, multi-tenancy or evidence of secure remote
deployment.

When a non-empty valid `VELANTRIM_API_TOKEN` is set, the synthetic local principal is
disabled. Local force approval additionally requires an exact `actor=api-curator`
assertion. The main CLI never receives an unauthenticated-local fallback; it always
requires explicit principal configuration for write commands.

## Role and capability matrix

| Role | Capabilities |
|---|---|
| `REVIEWER` | approve, reject, COEXIST |
| `CURATOR` | reviewer capabilities plus CONTEXTUALIZE and SUPERSEDE |
| `ADMIN` | all curator capabilities including force approval |

Role assignment is a host/deployment policy. Authorization does not determine truth,
evidence quality or the correct contradiction winner.

## Multi-instance deployments

`CuratorLeaseRegistry` is process-local. Multiple processes or hosts require an external
lease/fencing adapter with expiry, ownership and stale-writer protection. Report-id
freshness and ESM optimistic concurrency remain mandatory even when an external lease is
present.

Do not claim distributed locking, global exactly-once decisions or production
multi-tenancy from the bundled implementation.

## Operational checklist

- bind remote deployments to TLS through a reviewed reverse proxy or ASGI deployment;
- generate a high-entropy bearer token with no surrounding whitespace and rotate it through an explicit process;
- inject the bearer token from runtime secret management rather than source-controlled configuration;
- define the actor, roles and smallest practical scopes;
- export the same principal variables before CLI curator writes;
- keep unauthenticated local mode disabled remotely;
- monitor authorization denials and curator audit events without logging claim content;
- use an external identity and lease adapter for multi-user/multi-instance deployment;
- test token revocation/rotation and backup recovery in the host environment;
- never copy secrets or private identity configuration into repository documentation.

## Verification required before acceptance

- actor-spoofing denial with zero L1/L3/audit mutation across HTTP and CLI;
- missing-principal denial under bearer authentication and CLI execution;
- capability and candidate/target scope matrix tests;
- principal-derived audit actor tests;
- force approval restricted to the dedicated capability;
- stale report and lease-busy denial;
- fixed synthetic local-mode tests and documentation;
- invalid bearer-token configuration tests;
- complete Python 3.11/3.12 CI, coverage and security checks.
