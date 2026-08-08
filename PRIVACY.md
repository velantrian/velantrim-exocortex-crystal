<!-- d2-source-contract: CURRENT -->
<!-- d2-source-scope: reviewer-security-privacy-failure -->
# Privacy

Velantrim Crystal is local-first and private by default, but privacy still depends on the
operator's content, configuration, filesystem, backups and optional integrations. This page
states the current technical boundary. For legal mapping, see [`GDPR.md`](./GDPR.md).

This is research-grade infrastructure, **not a legal or GDPR certification**.

## Default behaviour

- No account, telemetry, analytics, crash reporting or phone-home behaviour is required.
- The default installation has no mandatory cloud, LLM or external database dependency.
- Public CLI and read-only MCP surfaces can operate locally with the standard library.
- Data leaves the local trust boundary only when an operator explicitly enables a networked
  adapter/backend, exposes the API, performs a remote migration or copies an export.

## What can be stored

A fact record can contain the claim, source and source status, claim type, epistemic state,
confidence/significance, timestamps and operator-controlled metadata. Other enabled state can
include graph edges, restrictions, erasure tombstones, review decisions, audit events,
receipts, outbox records and migration evidence.

Personal or confidential material placed in claims, metadata, sources or attachments must be
handled as sensitive data by the operator.

## Where data lives

- **L0** — process-local memory; normally disappears when the process exits.
- **L1** — local SQLite operational memory, with path controlled by configuration.
- **L3** — multi-status graph storage selected through the durable storage profile.

The ordinary documented active profile is SQLite. On a first durable `auto` startup,
LadybugDB may be selected only when its optional dependency is installed; otherwise SQLite is
selected. The durable winner and non-secret locator are persisted and reused. Automatic
fallback to ephemeral Mock is rejected. Explicit Mock remains available for development and
CI when no durable profile exists.

A remote Neo4j backend is an explicit operator choice. PostgreSQL/pgvector is currently only
an optional inactive import/equivalence target with `active=false`; it is not registered as
the normal runtime read/write backend.

Local database, profile and data files are git-ignored, but git-ignore is not access control,
backup policy or encryption.

## Encryption at rest

Setting `VELANTRIM_ENCRYPTION_KEY` protects selected L1 personal-data fields such as claim and
metadata. With the optional `cryptography` package the implementation uses Fernet; otherwise a
standard-library authenticated fallback is available. Encryption is off by default.

This field-level control does not cover every L3 backend, graph index, backup, logical bundle,
receipt, audit record, application log or temporary file. Use host disk encryption, protected
backups and reviewed key management where required.

## Optional integrations that expand the boundary

| Integration | Operator action | Privacy consequence |
|---|---|---|
| Anthropic generator | install `llm` extra and configure credentials | selected retrieved context is sent to Anthropic |
| Sentence-transformers | install `embeddings` extra | model weights may download; inference remains local |
| Neo4j | select/configure remote server backend | facts and graph state are stored on that server |
| PostgreSQL migration | install `postgresql` extra and select DSN environment variable | verified logical bundle is sent to the configured inactive target |
| Redis queue | select/configure Redis | queue/outbox-related state uses the configured server |
| Wikidata adapter | install/use network adapter | queries and responses cross the network |
| HTTP API | install `api` extra and bind a service | reachable clients can access permitted memory surfaces |
| Export/backup | operator copies files or bundles | each copy gains its own retention and deletion obligations |

The default extractive generator and hashing embedder are local. Provider terms and external
retention apply when a third-party service is enabled.

## API and review exposure

The optional API documents loopback-only use and token-based access as a baseline. Binding to
a wider interface or placing it behind a proxy expands the trust boundary. Before wider
exposure, require TLS, strong authentication, least privilege, resource controls and
independent review.

The repository does not claim a complete production IdP or multi-tenant authorization model.

## Data-subject operations

Crystal provides engineering mechanisms for:

- **access / portability** — reports, direct local database access and explicit export;
- **rectification** — update and supersession flows;
- **erasure** — removal across active memory layers plus content-free tombstone/audit evidence;
- **restriction** — reversible exclusion from recall and answers;
- **record of processing** — aggregate content-free processing overview.

See [`GDPR.md`](./GDPR.md) for the intended legal mapping and exact command/function names.

## Erasure and copy limits

Erasing active local state does not automatically erase independent copies such as:

- backups and snapshots;
- logical migration bundles;
- databases copied by an operator;
- data already sent to an external provider;
- remote backends outside the current process;
- logs or receipts governed by a separate retention policy.

Operators need a copy inventory, retention schedule and deletion procedure. Migration receipts
and endpoint identity must remain non-secret, but that does not make every surrounding file
non-sensitive.

## Secrets

Passwords, API tokens, encryption keys and credential-bearing connection strings must not be
stored in profiles, migration bundles, receipts, application logs, GitHub issues or Notion.
Production credentials should come from a protected secret mechanism and be rotated according
to deployment policy.

## Contact

Privacy questions: **qarythus@gmail.com**.
