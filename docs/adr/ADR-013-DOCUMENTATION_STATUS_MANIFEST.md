# ADR-013: Make active implementation claims machine-checkable

- **Status:** Accepted baseline
- **Date:** 2026-08-01
- **Scope:** active public documentation and CI only

## Context

Crystal had multiple active surfaces repeating mutable implementation facts:
README files, `docs/STATUS.md`, `TEST_REPORT.md`, reviewer guides and translated
pages. After runtime hardening, several active documents still reported an older
test count, an older commit and already-closed CLI/MCP residuals.

Modification timestamps cannot reliably prove semantic freshness, and natural
language documentation cannot be fully derived from code. However, a small set
of load-bearing public claims can be represented and checked mechanically.

## Decision

Crystal adds:

- `docs/status/implementation-manifest.json` as a compact machine-readable record
  of the verified runtime checkpoint, test metrics, CI topology, Ring Zero
  mutation result, implemented boundaries and grant-award status;
- `scripts/check_docs_status.sh` to validate manifest structure and required
  markers across active authoritative documents;
- a permanent `docs-status` CI job;
- `docs/DOCUMENTATION_MAP.md` to establish audience routes and authority order.

The manifest records a **verified runtime checkpoint**, not necessarily the most
recent documentation-only commit. A documentation change may update explanation
without pretending to be a new runtime implementation.

## Checked surfaces

The first baseline checks:

- `README.md`;
- `README.ru.md`;
- `docs/STATUS.md`;
- `TEST_REPORT.md`;
- `docs/IMPLEMENTATION_STATUS.md`.

It verifies exact checkpoint/test/gate markers and rejects selected stale claims
that previously remained active after implementation changed.

## Consequences

- stale test counts and closed residuals fail CI on active normative surfaces;
- README can stay readable while exact evidence remains centralized;
- the project distinguishes runtime checkpoint from documentation commit;
- translations remain reader surfaces and do not silently override English
  implementation truth;
- the check is intentionally narrow and deterministic.

## Non-goals

- no claim that all natural-language documentation can be formally verified;
- no automatic translation generation;
- no replacement for human architecture review;
- no inference that every unlisted document is current;
- no runtime, database, trust-policy or grant-scope change.

## Future work

The manifest may later expose a stable schema for release tooling and translation
freshness metadata. Such expansion must remain content-light and must not turn
Notion or generated documentation into implementation authority.
