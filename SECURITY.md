# Security Policy

Velantrim is verifiable memory infrastructure for AI systems. Because it stores
facts that downstream systems treat as *true*, the integrity and provenance of
that store is itself a security property. This document describes the threat
model, the security properties the codebase enforces today, and how to report
vulnerabilities.

## Supported versions

**Current Crystal line** (grant-facing open core):

| Version | Supported |
|---------|-----------|
| `0.2.x` | ✅ active — receives security updates |

**Legacy / historical lines** (separate research archives, not the grant-facing Crystal core):

| Version | Supported |
|---------|-----------|
| `8.x`   | ⚠️ historical / separate research line — not the main grant-facing support target |
| `< 8.0` | ❌ |

Only the latest minor Crystal line (`0.2.x`) receives active security updates unless otherwise stated. Do not rely on `8.x` archive lines for production or grant-facing deployments.

## Reporting a vulnerability

Please report security issues **privately** rather than opening a public issue.

- Email: **qarythus@gmail.com** with subject `SECURITY: Velantrim`.
- Include: affected version/commit, reproduction steps, and impact.
- We aim to acknowledge within **5 working days** and to agree a disclosure
  timeline (typically up to 90 days) with you.

Please do not run automated scanners against infrastructure you do not own, and
do not include third parties' personal data in reports.

## Threat model

Velantrim runs **locally by default** (see [PRIVACY.md](./PRIVACY.md)); the
default deployment has no network listener and no outbound calls. The primary
assets and threats:

| Asset | Threat | Mitigation in code |
|-------|--------|--------------------|
| Canonical graph (L3) | Unverified data written directly, bypassing review | **Single entry point**: writes go through the TruthGate (`core/pipeline.py`); `store_fact` writes L0/L1 only, never L3. |
| Fact integrity | Subjective/LLM output laundered into world-facts | `claim_type` / `source_status` axis (`core/memory.py`); type-aware gate keeps `EMOTION`/`OPINION` from becoming `WORLD_FACT`. |
| Immutable core | Tampering with foundational values (`VALUES_CORE`, `RING_ZERO`) | Invariant **I6**: `transition_esm` raises `ImmutableStateError` for Ring Zero IDs. |
| Provenance | Loss of "where did this come from" | Every fact records `source` + `source_status`; trace chain in `core/trace.py`. |
| State machine | Illegal epistemic transitions (e.g. Collapsed → Validated) | `ESM_TRANSITIONS` matrix validated in `transition_esm`. |
| Consistency | L3 write fails after L1 commit → orphaned fact | Persistent **outbox** (`l3_outbox`) drains idempotently on next access. |

### Optional HTTP service layer and the review token guard

The optional FastAPI service (`pip install ".[api]"`, `velantrim-api`) binds to
**127.0.0.1 by default** and is intended to stay there: it is a localhost-trust
surface, not an internet-facing service. Do not change `VELANTRIM_API_HOST`
to a routable address without putting real authentication and TLS in front.

The curator review endpoints (`/review/*`) read and mutate pre-canonical
claims, sources, confidence and curator decisions, so they carry an opt-in
token guard: when **`VELANTRIM_API_TOKEN`** is set, every `/review/*` JSON
endpoint — **GET and POST alike** — requires `Authorization: Bearer <token>`
(compared with `hmac.compare_digest`, constant-time). `GET /review/ui` stays
public because it is a static, data-free shell (enforced by test): all data it
shows is fetched client-side through the guarded JSON endpoints. Set the token
whenever anything beyond the local user can reach the port.

### Out of scope (current)

- **Authentication / multi-tenant access control** — beyond the opt-in
  review token guard above, Velantrim is a single-user, local library; there
  is no user/role layer. Do not expose it as a network service without
  adding one.
- **Encryption at rest** — *available* as an opt-in: when
  `VELANTRIM_ENCRYPTION_KEY` is set, the personal-data fields (claim, metadata)
  of the L1 SQLite store are encrypted (`core/crypto.py`). On-disk L3 backends
  (the `sqlite` L3 canon, LadybugDB) store claims in plaintext and are **not yet**
  covered by field-level encryption — use full-disk/filesystem encryption on the
  host for those, or erase via the Art. 17 path (`erase_fact` purges the L3 node).
- **Untrusted optional backends** — enabling the optional Claude generator or a
  remote Neo4j backend extends the trust boundary to those services (see
  [PRIVACY.md](./PRIVACY.md)).

## Security properties enforced today

- No outbound network calls in the default configuration.
- No secrets, credentials, `.env`, databases, or logs are committed to the
  repository (enforced by `.gitignore`; verified clean).
- All untrusted input flows through validation (`store_fact` rejects unknown
  ESM states, claim types, and source statuses).
- **Tamper-evident audit log (GDPR Art. 5(2)/24/30)** — `core/audit.py` keeps an
  append-only hash chain of compliance events (erase / restrict / unrestrict).
  Editing, deleting or reordering any past entry breaks the chain and is caught
  by `verify_audit_log()` (CLI `audit-verify`). Optional per-entry HMAC signing
  (`VELANTRIM_AUDIT_KEY`) adds forgery resistance.
- **Encryption at rest (opt-in, GDPR Art. 32)** — `core/crypto.py` provides
  authenticated, field-level encryption of the personal-data columns. With
  `cryptography` installed it uses Fernet (AES-128-CBC + HMAC); otherwise a
  dependency-free HMAC-SHA256 keystream (CTR) with encrypt-then-MAC. Tokens are
  tamper-evident — a wrong key or modified ciphertext fails authentication.
  Disabled by default (identity), so the default runtime stays stdlib-only.
- The full test suite at 100% coverage guards the invariants above (current
  audited baseline in [TEST_REPORT.md](./TEST_REPORT.md)).

## Dependencies

The default runtime uses the Python standard library only. `requirements.txt` is
kept as a compatibility marker and intentionally contains no mandatory runtime
packages. Development and CI tooling lives in `requirements-dev.txt`; optional
backends are installed through `pyproject.toml` extras. Keep optional backends
pinned and reviewed before enabling them.
