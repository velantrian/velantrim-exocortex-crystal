# Velantrim Crystal — Current Status

> Date: 2026-07-06
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

## Track 1–3B hardening (completed)

The audit-hardening tracks are merged and implemented:

```text
Track 1  — ProvenanceChain per-fact event chain   -> IMPLEMENTED (#168)
Track 2  — Docker hardening from scratch           -> IMPLEMENTED (#170/#171)
Track 3A — TruthPolicy production default          -> IMPLEMENTED (#172)
Track 3B — Write-path TruthGate audit/tests        -> IMPLEMENTED (#175)
```

Each track was delivered as a separate PR. See `TEST_REPORT.md` and
`docs/IMPLEMENTATION_REALITY_MATRIX.md` for current status.

## Recent PRs — response policy and research mode (status)

These PRs are recorded here so the public implementation boundary stays
explicit. The audited suite is now **1299 passed / 12 skipped / 100% coverage**
(see `TEST_REPORT.md`; includes the P0 integrity follow-up PR #216 on top of
the audit-hardening PR #206, on top of #201/#204).

```text
PR #201 — deterministic response_policy v0            -> IMPLEMENTED (merged)
PR #202 — wire response_policy onto the read path     -> CLOSED (not merged)
PR #204 — Research Mode v0.5 scaffold (prototypes/)   -> RESEARCH (merged, prototype only)
PR #216 — P0 integrity follow-up (post-#206)          -> IMPLEMENTED (merged)
```

- **PR #201 — `IMPLEMENTED`.** Deterministic read-path `response_policy v0`
  (`core/response_policy.py`, `docs/RESPONSE_POLICY_V0.md`, 11 tests). It is a pure
  read-path policy: it does not change write-path admission, does not write to
  Canon/L3, and does not replace the TruthGate.
- **PR #202 — `CLOSED`.** "Expose response_policy on the read path" was **closed
  without merging** — the branch's own `core/pipeline.py` diff was corrupted to a
  placeholder stub, so CI failed and the change was rejected. It is **not
  implementation truth** and was never part of Crystal runtime.
- **PR #216 — `IMPLEMENTED`.** P0 integrity follow-up after the audit-hardening PR
  (#206): (1) `store_fact()` upsert no longer poisons the L0 cache with a reset
  `restricted` flag or a stale `created_at` on a conflict-update; (2)
  `audit.append_event()` / `provenance_chain.append()` serialize their
  read-tail-then-insert sequence (`BEGIN IMMEDIATE` + a bounded write-lock retry)
  instead of racing on a computed `seq`; (3) `knowledge.ingest_claims()` /
  `imports.import_file()` track which facts an import session actually created
  (`new_fact_ids`), so a session that only duplicated a pre-existing claim can no
  longer `erase_session()` / `restrict_session()` a fact it never created. 7 new
  regression tests; current baseline: 1299 passed / 12 skipped / 100% coverage.
- **PR #204 — `RESEARCH` (prototype scaffold only).** The Research Mode v0.5 scaffold
  was merged under `prototypes/research_mode/` (`prototypes/research_mode/essence_card.py`),
  not in `core/`, and `prototypes/` is excluded from the installable package list. It
  is immutable data contracts, a pure transition helper and validators with tests
  only. Explicitly, Research Mode v0.5 is:
  - **not** wired into runtime;
  - **not** wired into TruthGate;
  - **not** storage;
  - **not** an extractor;
  - **not** a worker;
  - **not** a dashboard;
  - **not** current Crystal runtime behaviour.

  Crystal public core remains implementation truth. Research Mode / Personal
  Exo-Cortex / Titan / NoeticCore stay research/prototype directions unless a
  feature is separately merged and listed here (or in `TEST_REPORT.md`) as runtime.

## Research-only design docs

The following documents are architecture notes only. They do not change runtime
behaviour and must not be cited as implemented Crystal capabilities.

```text
docs/research/dialogue-cultivation-layer.md -> RESEARCH / DOCUMENTED_ONLY
```

- **Presence & Dialogue Cultivation Layer — `RESEARCH / DOCUMENTED_ONLY`.** This RFC
  studies long-term dialogue continuity, anti-sycophancy, open questions, proactive
  reflection and user-state hypothesis boundaries. It explicitly makes no claims of
  sentience, consciousness, emotion, personhood, biological life or implemented
  autonomous companion behaviour. It does not add code, storage, workers, TruthGate
  wiring, Canon writes or runtime integration.

## Implementation reality matrix

_High-level summary. The canonical track-by-track audit matrix is [`IMPLEMENTATION_REALITY_MATRIX.md`](./IMPLEMENTATION_REALITY_MATRIX.md)._

_A companion documented evaluation lens (dimensions and criteria only, no status verdicts) lives at [`docs/audits/MEMORY_ARCHITECTURE_AUDIT.md`](./audits/MEMORY_ARCHITECTURE_AUDIT.md); it does not replace this matrix as the source of truth for current implementation status._

| Component / area | Current status | Public claim | Risk / note | Next action |
|---|---|---|---|---|
| Crystal public core | IMPLEMENTED | local-first verifiable memory core | Keep narrow; avoid Titan scope creep | Maintain `TEST_REPORT.md` as source of truth |
| TruthGate / epistemic boundary | IMPLEMENTED | verifies admissibility where wired | Track 3A (#172) set the strict production default; Track 3B (#175) pinned the write-path audit + `gate_reason` (`tests/test_write_path_gate.py`) | Maintain behavioural tests |
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
| Presence & Dialogue Cultivation | RESEARCH / DOCUMENTED_ONLY | future dialogue continuity and anti-sycophancy research | No sentience, consciousness, emotion, personhood, biological life or implemented companion-runtime claim | Keep as research-only RFC unless separately prototyped, tested and audited |

## Crystal hardening sequence (status)

1. Track 1 — per-fact ProvenanceChain and tests — DONE (#168).
2. Track 2 — Dockerfile, docker-compose.yml and .dockerignore with fail-closed `VELANTRIM_API_TOKEN` — DONE (#170/#171).
3. Track 3A — strict TruthPolicy production default — DONE (#172).
4. Track 3B — write-path TruthGate behavioural tests and `gate_reason` audit detail — DONE (#175).
5. Keep this status page and Reality Matrix current after each PR — ongoing.
6. Add knowledge graph status / data-quality verifier rules before claiming verified graph knowledge — pending.

## Relationship to Titan

Titan is valuable as a donor of ideas, UI, research modules and future architecture. Crystal should extract only:

- invariants;
- epistemic contracts;
- evidence/source requirements;
- security lessons;
- minimal dependency-free mechanisms;
- reviewer-safe documentation.

Crystal should not absorb Titan wholesale.
