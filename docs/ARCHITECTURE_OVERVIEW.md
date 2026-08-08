<!-- d3-source-contract: CURRENT -->
<!-- d3-source-scope: architecture-storage-authority -->
# Crystal Architecture Overview

**Status date:** 2026-08-08  
**Purpose:** stable, translation-oriented architecture entry point.  
**Authority:** merged code, exact CI and the implementation manifest remain runtime truth.

## Core model

```text
sources and explicit ingest
        ↓
provenance + normalization
        ↓
Guardian policy checks
        ↓
TruthGate admission decision
        ↓
L1 operational state + multi-status L3 graph
        ↓
strict Canon read projection
        ↓
read-only retrieval / answer / bounded refusal
```

Crystal does not treat every stored node, retrieved result or model output as truth.
Physical L3 stores multiple statuses. Strict Canon is the deny-dominant trusted read
projection produced by policy and evidence constraints.

## Memory layers

| Layer | Role | Authority boundary |
|---|---|---|
| L0 | process-local working state | ephemeral, not durable truth |
| L1 | SQLite operational memory | durable facts, state, audit, receipts and outbox |
| L2 | semantic retrieval support | ranking aid, not evidence or admission |
| L3 | graph-oriented multi-status storage | physical storage, not identical to strict Canon |

## Read and write separation

```text
ask / receipt / MCP inspection → core.query_pipeline.query() → read-only
explicit ingest                → Guardian / TruthGate → admission-capable write
```

A public query must not mutate facts, ESM, L3, outbox, episode links, embedding identity or
unknown candidates. If strict grounding is insufficient, a bounded refusal is expected.

## Storage profiles

SQLite is the ordinary active local-first profile. A first durable `auto` selection may use
optional LadybugDB when installed, otherwise SQLite, and then persists the selected backend,
schema version and non-secret locator digest. Later conflicts fail closed. Silent fallback
to ephemeral Mock is forbidden; explicit Mock remains development/test state.

Remote Neo4j is an explicit operator choice and expands the trust boundary.

## Portability and PostgreSQL

The verified portability chain is:

```text
SQLite backup / verify / inactive restore
→ bounded deterministic logical export
→ PostgreSQL 16 + pgvector 0.8.2 preflight
→ new inactive target schema
→ serializable import
→ independent read-only target re-hash
→ exact equivalence receipt
→ target remains active=false
```

The PostgreSQL target is absent from ordinary runtime composition. Successful import or
exact equivalence is operation evidence, not activation, backend selection, TruthGate
admission, strict Canon membership, cutover, rollback, dual-write or production readiness.

## Source-grounded ingestion

Source provenance, text spans, document records and import sessions are implemented baseline.
A dedicated Reader Core for multi-pass document structure, coverage maps, contradiction-aware
rereading and document-level synthesis is still future work upstream of admission.

## Safety and privacy

The default installation has no mandatory cloud, LLM, telemetry or analytics dependency.
Optional remote adapters, wider API exposure and migration targets require explicit operator
configuration. Selected L1 field encryption is not universal encryption. Active-store
erasure is not global erasure of backups, exports, remote systems or provider copies.

## Current non-claims

Crystal does not claim:

- AGI, consciousness, universal truth or zero hallucinations;
- active PostgreSQL runtime or automatic backend switching;
- cutover, rollback, dual-write or accepted ANN production profile;
- production multi-tenancy or distributed exactly-once coordination;
- security, legal or GDPR certification;
- awarded NLnet funding.

## Detailed English contracts

- [Full architecture](./ARCHITECTURE.md)
- [Storage and authority boundaries](./STORAGE_AND_AUTHORITY_BOUNDARIES.md)
- [Implementation status](./IMPLEMENTATION_STATUS.md)
- [Security/privacy/failure summary](./SAFETY_PRIVACY_AND_FAILURES.md)
