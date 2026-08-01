# Implementation Status: Crystal vs Full Exo-Cortex

This page separates implemented Crystal behavior from RFC, roadmap, Titan and
broader Exo-Cortex concepts.

**Status date:** 2026-08-01  
**Verified runtime checkpoint:** `b10a744`  
**Exact test evidence:** [TEST_REPORT.md](../TEST_REPORT.md)  
**Machine-readable status:** [status/implementation-manifest.json](./status/implementation-manifest.json)

## Status vocabulary

- **Implemented** — code and behavior-pinning tests are merged.
- **Implemented baseline** — usable slice exists; broader integration may remain.
- **Partial** — only part of the complete contract exists.
- **RFC / roadmap** — design only; not a runtime claim.
- **Research / out of scope** — outside the current Crystal core.

## Current implementation table

| Component | Status | Current boundary |
|---|---|---|
| Local-first L0/L1 storage | Implemented | in-process cache plus SQLite/WAL operational state |
| Pluggable L3 graph storage | Implemented baseline | dependency-free SQLite baseline plus optional adapters |
| TruthGate | Implemented | admission policy, not an objective-truth oracle |
| Non-configurable LLM-origin rule | Implemented | `LLM_OUTPUT + WORLD_FACT` cannot automatically become `VERIFIED` |
| Guardian and CanonicalView | Implemented | structural contract and strict read projection; physical L3 is not strict Canon |
| Unified public read-only query boundary | Implemented | HTTP `/ask`/`receipt`, CLI `ask`/`receipt` and MCP search |
| Immutable TrustSnapshot | Implemented | frozen deny-dominant L3/L1 read reconciliation |
| TRACE, Receipt and replay | Implemented | grounding trace, tamper evidence and citation replay |
| Evidence spans and import sessions | Implemented baseline | accountable source/import metadata |
| Review queue and resumable sessions | Implemented | explicit review lifecycle |
| Typed contradiction report | Implemented | immutable, content-free and deterministic report identity |
| Explicit contradiction decisions | Implemented | `COEXIST`, `CONTEXTUALIZE`, `SUPERSEDE`; no automatic winner |
| Conflict-resolution CLI | Implemented | validated public adapter over `review.resolve_conflict` |
| Conflict-resolution HTTP route | Implemented | host-authenticated FastAPI route; unguarded mode is explicit local-only opt-in |
| Machine-readable ESM specification | Implemented | derived from the runtime transition matrix; 8 states, 15 transitions, 2 terminal states |
| Deterministic eval gate | Implemented | retrieval, grounding, contradiction and refusal controls |
| Ring Zero mutation gate | Implemented | 7/7 declared semantic mutants must be killed |
| Documentation manifest and link check | Implemented | 9th CI job prevents active-surface drift |
| L3 performance history | Implemented baseline | scheduled/manual versioned artifacts and comparable-run reporting; no brittle shared-runner SLO |
| GDPR-relevant controls | Partial | erasure, restriction, audit, redaction and opt-in encryption; not certification |
| Roles and multi-curator authorization | Partial | token boundary is not production multi-tenant IAM |
| Fractal Memory anchoring | Implemented baseline | memory anchoring only; not Fractal Attention cognition |

## Current trust and decision topology

```text
explicit ingest → Guardian → TruthGate → L3 multi-status graph
public query → read-only retrieval → TrustSnapshot → CanonicalView STRICT
unresolved contradiction → ContradictionReport → explicit curator disposition
```

## Completed workstream

The previously identified packages are complete:

- detailed README and documentation routing;
- read-only public query surfaces;
- removal of the TruthPolicy bypass;
- immutable trust snapshots;
- targeted mutation testing;
- typed contradiction decision contract;
- machine-readable ESM specification;
- scheduled performance history;
- public CLI/API conflict-resolution surfaces;
- exact status and Notion synchronization.

## Independent future roadmap

These are future improvements, not unfinished parts of the completed workstream:

- advisory multi-label topic facets that cannot influence truth;
- scoped roles, identities and concurrent multi-curator authorization;
- broader provenance-chain lifecycle integration;
- controlled-runner performance thresholds;
- wider mutation-testing coverage;
- temporal and bi-temporal claim semantics;
- distributed replication;
- Titan cognitive integration as a separate research track.

## Non-claims

Crystal is not Titan, an autonomous cognitive OS, a consciousness simulation, a
universal truth detector, a zero-hallucination guarantee, legal GDPR
certification, security certification or a production multi-tenant platform.

## Documentation routes

- [README](../README.md)
- [Documentation map](./DOCUMENTATION_MAP.md)
- [Current status](./STATUS.md)
- [Conflict-resolution surfaces](./CONFLICT_RESOLUTION_SURFACES.md)
- [Architecture](./ARCHITECTURE.md)
- [ADR index](./ADR.md)
- [Test report](../TEST_REPORT.md)
- [Failure modes](./FAILURE_MODES.md)
- [Evaluation](./EVAL.md)
- [Grant scope](./GRANT_NLNET_SCOPE.md)
