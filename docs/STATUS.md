# Velantrim ExoCortex — Crystal: Status (Single Entry Point)

This is the **high-level status entry point** for Velantrim ExoCortex — Crystal.
It is intentionally short: it states the readiness posture and the status
vocabulary, then points to the canonical, detailed documents. For the
authoritative per-component breakdown, see
[`IMPLEMENTATION_STATUS.md`](./IMPLEMENTATION_STATUS.md).

> This page makes **no production-ready, zero-hallucination, or AGI/consciousness
> claims**. Readiness figures below are a self-assessment snapshot for orientation,
> not a certification.

## Current status summary

Crystal is the grant/reviewer-facing open-source core: local-first memory, typed
claims, a type-aware **TruthGate**, trace/receipts, tamper-evident audit, and
GDPR-oriented controls. The runtime is **stdlib-only** by default (optional
backends and adapters are opt-in extras). The test suite is the source of truth
for what counts as *implemented*; CI enforces a 100% coverage gate.

## Readiness posture

| Lens | Assessment | Meaning |
|---|---|---|
| **Grant / reviewer readiness** | ~8/10 | The reviewer-facing Crystal core (memory, TruthGate, trace/receipts, audit, GDPR-oriented controls) is implemented and tested. |
| **Production readiness (full public product)** | ~7/10 — **not claimed** | Not hardened for public, multi-tenant, internet-facing deployment without a dedicated auth/security layer and reverse proxy/TLS in front. |

**Crystal ≠ Titan.** "Titan" (the broader console / research surface) is **not**
claimed as a production-ready Crystal deliverable. Research-Mode / cognitive
concepts (Noetic, Presence, BICA, Mode Layer, Imagination/Spark) are **research
or RFC-level**, not Crystal runtime — see
[`IMPLEMENTATION_STATUS.md`](./IMPLEMENTATION_STATUS.md).

## Status taxonomy

Every capability below maps to one of these labels. The detailed table in
[`IMPLEMENTATION_STATUS.md`](./IMPLEMENTATION_STATUS.md) uses an equivalent
vocabulary (Implemented / Partial / RFC-roadmap / Vision / Out-of-scope).

| Label | Meaning |
|---|---|
| `IMPLEMENTED` | Code **and** tests present in this repository. |
| `FEATURE_FLAGGED` | Implemented but gated behind an env var / opt-in extra; default behaviour may differ. |
| `DOCUMENTED_ONLY` | Specified in docs/RFC; **no** runtime feature yet. |
| `RESEARCH` | Research direction / private architecture; **outside** the Crystal grant core. |
| `EXPERIMENTAL` | Prototype or baseline; not hardened, may change. |

## Component status (high level — see the canonical table for detail)

| Area | Label | Pointer |
|---|---|---|
| Local-first storage, TruthGate, Trace/Receipt, Audit | `IMPLEMENTED` | [`IMPLEMENTATION_STATUS.md`](./IMPLEMENTATION_STATUS.md) |
| ESM (epistemic state machine) review/promotion | `IMPLEMENTED` | [`IMPLEMENTATION_STATUS.md`](./IMPLEMENTATION_STATUS.md) |
| GDPR-oriented controls (erasure, restriction, audit, PII redaction) | `IMPLEMENTED` (baseline; "GDPR-oriented", **not** certified) | [`IMPLEMENTATION_STATUS.md`](./IMPLEMENTATION_STATUS.md) |
| Review web UI / browser console | `IMPLEMENTED` (local-demo; **not** public-deployment hardened) | [`DEMO_UI.md`](./DEMO_UI.md), [`SECURITY.md`](../SECURITY.md) |
| L3 graph backend | `FEATURE_FLAGGED` (SQLite default; Ladybug/Neo4j optional) | [`IMPLEMENTATION_STATUS.md`](./IMPLEMENTATION_STATUS.md) (Graph backends) |
| RRF rank fusion | `IMPLEMENTED` (standalone helper; **not** wired into `retrieve()`) | [`IMPLEMENTATION_STATUS.md`](./IMPLEMENTATION_STATUS.md) |
| `kb_graph` autolinker | `EXPERIMENTAL` (prototype; not proven over external source/evidence coverage) | [`KNOWLEDGE_BASE_ROADMAP.md`](./KNOWLEDGE_BASE_ROADMAP.md) |
| Research Mode / Noetic / Presence / BICA / Mode Layer | `RESEARCH` / `DOCUMENTED_ONLY` | [`IMPLEMENTATION_STATUS.md`](./IMPLEMENTATION_STATUS.md) |

The knowledge graph is **not** presented as a verified universal canon: entry
into L3 is gated, and a populated graph is not a claim of verified truth.

## Security & deployment

- Default API host binds to **`127.0.0.1`**; the review endpoints carry an
  **opt-in** bearer-token guard (`VELANTRIM_API_TOKEN`). See
  [`SECURITY.md`](../SECURITY.md). Do not expose to a routable address without
  real auth and TLS in front.
- No `Dockerfile` / `docker-compose.yml` ships in the repo today; a hardened
  containerisation (fail-closed `VELANTRIM_API_TOKEN`, localhost binding,
  non-root user) is tracked as a separate task.

## Audit response tracker

| Item | Status |
|---|---|
| **CRIT-1** — verifiable per-fact provenance integrity | Implemented as per-fact `ProvenanceChain` (Sprint1 P1-5 / I89); satisfies the CRIT-1 acceptance criteria. **In review** (PR #168). |
| **CRIT-2** — secure container defaults | **Not applicable to current repo state** (no compose file exists; env var is `VELANTRIM_API_TOKEN`, not `VELANTRIM_API_KEY`). Tracked for a separate "secure compose from scratch" task. |
| Status drift | This page added as the single high-level entry point. |

## Canonical references

- [`IMPLEMENTATION_STATUS.md`](./IMPLEMENTATION_STATUS.md) — authoritative per-component status
- [`../TEST_REPORT.md`](../TEST_REPORT.md) — audited test/coverage baseline
- [`../SECURITY.md`](../SECURITY.md) — deployment & token-guard posture
- [`ARCHITECTURE.md`](./ARCHITECTURE.md) — architecture & Ring Zero invariants
- [`../ROADMAP.md`](../ROADMAP.md) — forward-looking roadmap (not implementation status)
