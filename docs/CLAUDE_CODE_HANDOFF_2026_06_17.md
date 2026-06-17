# Claude Code Handoff — 2026-06-17

> Scope: work that requires code inspection, tests or controlled runtime changes.
> Status: handoff only. ChatGPT added docs; Claude Code should handle code with tests.

## Context

ChatGPT performed the safe docs-only extraction from the Titan/Crystal audits. Runtime code was not intentionally changed.

Docs added:

```text
docs/STATUS.md
docs/security/DEPLOYMENT_SECURITY.md
docs/security/AUDIT_RESPONSE_2026_06_17.md
docs/data/KNOWLEDGE_GRAPH_STATUS.md
docs/core/CLAIM_TYPE_AND_ORIGIN.md
docs/core/INGEST_SCHEMA.md
docs/core/DEDUP_AND_SCALE.md
docs/core/PROVENANCE_CHAIN_CONTRACT.md
docs/core/ANSWER_CONTRACT.md
docs/architecture/ARCHITECTURE_RECONCILIATION.md
docs/architecture/BACKENDS.md
```

## Do not do

- Do not import Titan wholesale into Crystal.
- Do not add Noetic/Attention/Research PWA as current runtime.
- Do not weaken TruthGate, Guardian, TRACE or Receipt semantics.
- Do not promote unverified graph data to verified canon.
- Do not make Graphiti/Neo4j/OpenAI mandatory for the public core.

## P0 tasks

### 1. Provenance chain verification

Inspect current Crystal code for any provenance-chain implementation.

If actor/reason are part of the hash contract:

- ensure `_compute_hash` accepts them;
- ensure append and verify use the same fields;
- add tests for append -> verify;
- add tamper tests for payload, actor and reason;
- ensure empty chain is not reported as equivalent to verified non-empty chain.

### 2. Deployment defaults

Inspect `docker-compose.yml`, `Dockerfile` and `.dockerignore`.

Target direction:

```yaml
VELANTRIM_API_KEY=${VELANTRIM_API_KEY:?Set VELANTRIM_API_KEY}
ports:
  - "127.0.0.1:8000:8000"
```

Also verify:

- non-root container user where practical;
- no `.env`, `.git`, cache or local DB in images;
- production image does not install dev/research extras unnecessarily.

## P1 tasks

### 3. TruthPolicy production profile

If Crystal has claim-type/origin-type or truth-policy mechanisms, verify default behaviour.

Target:

```text
production profile = strict epistemic enforcement
legacy behaviour = explicit dev/test only
```

### 4. Knowledge graph verifier

If this repository contains data import/graph tooling, add a verifier only after confirming schema.

Verifier should check:

- allowed type vocabulary;
- source field is meaningful;
- evidence_ref where required by policy;
- self-contained claims;
- no heuristic edge promoted as verified truth.

### 5. Canonical write path

Verify that single write, batch write and async write paths share validation, dedup, source/evidence handling and index-sync rules.

## P2 tasks

- Link `docs/STATUS.md` from README if appropriate.
- Add CI/doc checks if useful.
- Mark superseded docs or old baseline numbers where found.

## Expected output

Open small PRs, not one large PR:

1. provenance-chain tests/fix;
2. deployment hardening;
3. TruthPolicy/profile decision;
4. data verifier;
5. README/status link and doc sync.
