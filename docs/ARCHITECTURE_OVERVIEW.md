<!-- d3-source-contract: CURRENT -->
<!-- d3-source-scope: architecture-storage-authority -->
# Crystal Architecture Overview

**Status date:** 2026-08-10  
**Purpose:** stable, translation-oriented architecture entry point.  
**Authority:** merged code, exact CI and the implementation manifest remain runtime truth.

## Core model

```text
source/document identity + exact version/hash
        ↓
RC-1 evidence-linked Reader artifacts
        ↓
RC-2 caller-supplied Structural Document Map
        ↓
normal ingest/review/evidence path
        ↓
Guardian policy checks
        ↓
TruthGate admission decision
        ↓
L1 operational state + multi-status physical L3
        ↓
deny-dominant strict Canon read projection
        ↓
read-only retrieval / answer / bounded refusal
```

Reader artifacts and structural metadata remain upstream candidates/observations. They do not
own truth, admission, contradiction resolution or planner authority.

Crystal does not treat every stored node, retrieved result or model output as truth. Physical
L3 stores multiple statuses. Strict Canon is the trusted read projection produced by current
policy and evidence constraints.

## Memory and review layers

| Layer | Role | Authority boundary |
|---|---|---|
| Reader RC-1 | source/version/session artifacts, fidelity and coverage | source-linked observation/candidate, not truth |
| Reader RC-2 | version-bound structural hierarchy/order | structure and prominence are metadata, not confidence |
| L0 | process-local working state | ephemeral, not durable truth |
| L1 | SQLite operational memory | durable facts, ESM, evidence, audit, receipts, import/review and outbox state |
| L2 | pending/review staging | candidate or quarantined claims before final admission |
| L3 | graph-oriented multi-status storage | physical storage, not identical to strict Canon |
| Strict read view | TrustSnapshot / CanonicalView | deny-dominant grounding surface |

## Read and write separation

```text
ask / receipt / MCP inspection → core.query_pipeline.query() → read-only
explicit ingest                → Guardian / TruthGate → admission-capable write
Reader RC-1 / RC-2             → source-linked artifacts only → no admission side effects
```

A public query must not mutate facts, ESM, L3, outbox, episode links, embedding identity or
unknown candidates. If strict grounding is insufficient, a bounded refusal is expected.

## Storage profiles

SQLite is the ordinary active local-first profile. A first durable `auto` selection may use
optional LadybugDB when installed, otherwise SQLite, and then persists the selected backend
and non-secret locator identity. Later backend or locator conflicts fail closed. Silent
fallback to ephemeral Mock is forbidden; explicit Mock remains development/test state.

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

## Source-grounded Reader foundation

Source spans and import-session evidence are implemented baseline. RC-1 now provides the bounded
evidence-linked source/session skeleton: exact source-version identity, locators, SegmentCards,
source-fidelity classes, coverage states, bookmarks/open loops, stale handling and fail-visible
failure/privacy semantics.

RC-2 adds a caller-supplied Structural Document Map anchored to the same exact SourceVersion and
SourceLocator semantics. It models hierarchy/order and explicit `RECOVERED`, `AMBIGUOUS` and
`UNSUPPORTED` structure without claiming automatic parsing.

The dedicated multi-pass Reader / Semantic Reading runtime remains future work. There is no
automatic parser/semantic chunker, LLM/provider Reader orchestration, embeddings/ANN/vector DB,
cross-document reasoning engine or automatic belief update. `coverage != comprehension proof`.

## Safety and privacy

The default installation has no mandatory cloud, LLM, telemetry or analytics dependency.
Optional remote adapters, wider API exposure and migration targets require explicit operator
configuration. Selected L1 field encryption is not universal encryption. Active-store
erasure is not global erasure of backups, exports, remote systems or provider copies.

Reader RC-1/RC-2 retain no source body and derived Reader artifacts inherit source restriction and
sensitivity metadata. Reader structure/order/prominence cannot weaken privacy or epistemic policy.

## Current non-claims

Crystal does not claim:

- AGI, consciousness, universal truth or zero hallucinations;
- active PostgreSQL runtime or automatic backend switching;
- cutover, rollback, dual-write or accepted ANN production profile;
- production multi-tenancy or distributed exactly-once coordination;
- a completed dedicated multi-pass Reader Core or automatic document comprehension;
- security, legal or GDPR certification;
- awarded NLnet funding.

## Detailed English contracts

- [Full architecture](./ARCHITECTURE.md)
- [Reader Core architecture contract](./architecture/READER_CORE_ARCHITECTURE.md)
- [Storage and authority boundaries](./STORAGE_AND_AUTHORITY_BOUNDARIES.md)
- [Implementation status](./IMPLEMENTATION_STATUS.md)
- [Security/privacy/failure summary](./SAFETY_PRIVACY_AND_FAILURES.md)
