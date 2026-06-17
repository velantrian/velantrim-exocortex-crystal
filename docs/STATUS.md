# Velantrim Crystal — Current Status

> Date: 2026-06-17
> Scope: public Crystal repository status note
> Status: docs-only integrity map; does not change runtime behaviour

## Reading rule

Crystal is the public, minimal, verifiable memory core. Titan / Full Exo-Cortex is the broader private research laboratory.

```text
GitHub Crystal = implementation truth for the public core.
Notion Crystal = grant and strategy map.
Titan / Full = research laboratory and future architecture.
```

Do not treat Titan, V9, V10, Noetic, Research PWA, BICA, or private Full Exo-Cortex notes as current Crystal runtime unless a feature is implemented, tested, and listed here or in `TEST_REPORT.md`.

## Status vocabulary

| Status | Meaning |
|---|---|
| `IMPLEMENTED` | Present in the Crystal runtime and covered by tests or reviewer tooling. |
| `FEATURE_FLAGGED` | Code exists but is off by default or requires explicit configuration. |
| `DOCUMENTED_ONLY` | Architecture/specification only; no runtime claim. |
| `PLANNED` | Accepted implementation plan, not yet current runtime. |
| `RESEARCH` | Private or future research direction; not a public Crystal deliverable. |
| `LEGACY` | Historical material retained for context. |
| `SUPERSEDED` | Old statement replaced by newer repository status. |

## Current public claim boundary

Crystal may safely claim:

- local-first verifiable AI memory infrastructure;
- source-grounded / provenance-oriented memory boundaries where implemented;
- TruthGate / Guardian / TRACE / Receipt-oriented design where implemented;
- explicit separation of memory, evidence, retrieval, truth, reasoning, and speech;
- LLM output is not treated as truth by default where the relevant gates are active;
- research directions are separated from current runtime claims.

Crystal must not claim:

- AGI, consciousness, autonomous mind, or biological brain implementation;
- zero hallucinations as a guarantee;
- production-ready Titan console;
- NoeticCore / AttentionRouter / Research PWA as current Crystal runtime;
- Graphiti, Neo4j, OpenAI, or cloud LLMs as mandatory Crystal dependencies;
- verified World Knowledge Core unless source/evidence requirements are met.

## Current Track 1–3B plan

The current implementation plan is:

```text
Track 1  — ProvenanceChain per-fact event chain
Track 2  — Docker hardening from scratch
Track 3A — TruthPolicy production default
Track 3B — Write-path TruthGate audit/tests
```

Each track must be a separate branch and PR.

## Implementation reality matrix

| Component / area | Current status | Public claim | Risk / note | Next action |
|---|---|---|---|---|
| Crystal public core | IMPLEMENTED | local-first verifiable memory core | Keep narrow; avoid Titan scope creep | Maintain `TEST_REPORT.md` as source of truth |
| TruthGate / epistemic boundary | IMPLEMENTED / evolving | verifies admissibility where wired | Track 3A defines strict production default; Track 3B pins write-path behaviour | Separate PRs for 3A and 3B |
| TRACE / Receipt | IMPLEMENTED | replayable proof path where generated | Keep receipt semantics stable | Document threat model and replay assumptions |
| Per-fact ProvenanceChain | IMPLEMENTED | per-fact, append-only, hash-chained provenance log | Implemented in current merged scope via #168 (`core/provenance_chain.py`, table in `core/memory.py`, wired into the erase path); broader lifecycle wiring (other state transitions) remains follow-up | Broader lifecycle wiring is follow-up |
| Claim type / origin type | CANDIDATE / FEATURE DESIGN | separates fact, opinion, experience, LLM output | Do not imply all Crystal paths already enforce it unless verified | Track 3A/3B plus future tests |
| Ingest schema | DOCUMENTED / CANDIDATE | source-first ingestion contract | No source must mean no confident answer | Keep docs, add verifier later |
| Dedup / scale design | DOCUMENTED / CANDIDATE | exact/semantic dedup roadmap | Frequency is not independent evidence | Future separate work |
| Docker deployment | IMPLEMENTED | secure local-first deployment defaults | #170 + #171: `Dockerfile`, `docker-compose.yml`, `.dockerignore`; non-root `velantrim` user; named-volume default; `VELANTRIM_API_TOKEN` fail-fast; safe image default host `127.0.0.1`; compose loopback exposure `127.0.0.1:8000:8000` | Maintain alongside `SECURITY.md` |
| Titan console | RESEARCH / TITAN ONLY | demo/research UI | Not production Crystal UI | Keep outside Crystal runtime claim |
| Noetic Orchestration | RESEARCH | future external attention / cognitive routing | Not wired into `/query` as Crystal runtime | Keep as RFC only |
| BICA Alignment | RESEARCH / GRANT LANGUAGE | BICA-informed mapping only | Not a BICA implementation | Use only as cautious framing |
| Graphiti / Neo4j | OPTIONAL / RESEARCH | optional advanced backend inspiration | Not Crystal truth authority | Keep stdlib/local-first Crystal core |
| Knowledge graph / WSC data | RESEARCH / UNVERIFIED unless sourced | draft graph / autolinker prototype if no evidence | Do not call verified canon without real sources/evidence_refs | Data verifier after schema confirmation |

## Immediate Crystal hardening sequence

1. Track 1: implement per-fact ProvenanceChain and tests.
2. Track 2: create Dockerfile, docker-compose.yml and .dockerignore with fail-closed `VELANTRIM_API_TOKEN`.
3. Track 3A: define strict TruthPolicy production default.
4. Track 3B: add write-path TruthGate behavioural tests and `gate_reason` audit detail.
5. Keep this status page and Reality Matrix current after each PR.
6. Add knowledge graph status / data-quality verifier rules before claiming verified graph knowledge.

## Relationship to Titan

Titan is valuable as a donor of ideas, UI, research modules and future architecture. Crystal should extract only:

- invariants;
- epistemic contracts;
- evidence/source requirements;
- security lessons;
- minimal dependency-free mechanisms;
- reviewer-safe documentation.

Crystal should not absorb Titan wholesale.
