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
explicit. The audited suite is now **1661 passed / 12 skipped / 100% coverage**
(see `TEST_REPORT.md`; includes the mutation-boundary quick-wins PR #229 on
top of the small correctness-hardening PR #222, the P0 integrity follow-up
PR #216, the audit-hardening PR #206, #201/#204, and the CanonicalView
strict-grounding implementation PR #257 with its corrective trust-boundary
hardening PR #258). Canonical `main` SHA after #258's squash-merge:
`b2ccc5f99dd71a2fab5b63eb9d2bc93e34664f92`.

```text
PR #201 — deterministic response_policy v0            -> IMPLEMENTED (merged)
PR #202 — wire response_policy onto the read path     -> CLOSED (not merged)
PR #204 — Research Mode v0.5 scaffold (prototypes/)   -> RESEARCH (merged, prototype only)
PR #216 — P0 integrity follow-up (post-#206)          -> IMPLEMENTED (merged)
PR #222 — small correctness hardening (post-#216)     -> IMPLEMENTED (merged)
PR #218 — L3 retrieval-scale smoke benchmark          -> BENCHMARK BASELINE / no runtime behaviour change
PR #257 — CanonicalView strict-grounding trust boundary -> IMPLEMENTED (merged, partial RFC slice — see docs/CANONICAL_VIEW_RFC.md)
PR #258 — corrective trust-boundary hardening (post-#257) -> IMPLEMENTED (merged; 0 unresolved review threads on #257 and #258)
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
- **PR #222 — `IMPLEMENTED`.** Small correctness hardening after the audit
  follow-up, merged as `9377d34`: (1) `truth_gate()` treats a missing
  `confidence` as a controlled rejection instead of raising `KeyError`; (2)
  `volition.write_voluntary()` now passes `source_status="USER_REPORTED"`
  explicitly rather than relying on `classify_claim()`'s fallback; (3)
  `erase_fact()` is a true no-op for a `fact_id` that never existed (no
  tombstone/audit/provenance event), while still correctly erasing an
  L3-only orphan (a fact_id present only in the canonical graph, not L1) —
  a Codex-review fix on top of the initial version; (4) the
  `retrieval-config-set` CLI returns a controlled `invalid retrieval
  config: ...` error instead of a raw traceback on malformed numeric input;
  (5) `pii.py`'s PHONE detector no longer false-flags a bare ISO-8601 date
  (validated via `datetime.strptime`, not just the `YYYY-MM-DD` shape — also
  a Codex-review fix, since the shape-only check would have wrongly exempted
  phone-like values such as `5555-12-34`). 8 new regression tests; suite
  total after this PR: 1307 passed / 12 skipped / 100% coverage (see
  `TEST_REPORT.md` for the current baseline).
- **PR #218 — `BENCHMARK BASELINE`.** Adds `scripts/bench_l3_retrieval.py`
  and `docs/benchmarks/L3_RETRIEVAL_SCALE.md`: a dependency-free smoke
  benchmark measuring current `core.l3_graph` SQLite-backend retrieval
  latency at increasing synthetic corpus sizes. Measures existing behaviour
  only — no retrieval algorithm, TruthGate, or L3 schema change; not a
  performance optimization or a CI gate.
- **PR #257 — `IMPLEMENTED` (partial RFC slice).** Implements the
  strict-grounding slice of the CanonicalView RFC (issue #220,
  `docs/CANONICAL_VIEW_RFC.md`): `core/canonical_view.py`
  (`CanonicalReadMode.STRICT`/`CONTEXTUAL`, `is_strict_canonical()`,
  `project_canonical()`), wired into `core/pipeline.py::generate_answer()` as
  the default answer-grounding filter. Physical L3 membership no longer by
  itself implies verified truth for a confident factual answer. `review` and
  `full_graph` read modes from the RFC remain **not implemented** — see
  `docs/CANONICAL_VIEW_RFC.md` section 9 for the itemized breakdown.
- **PR #258 — `IMPLEMENTED`.** A corrective trust-boundary hardening cycle on
  top of #257: dispositions all 9 review threads raised on #257, then closes
  17 further findings from five rounds of independent re-review. Both #257
  and #258 report **0 unresolved review threads**. Implemented behavior
  (see `docs/CANONICAL_VIEW_RFC.md`'s corrective-hardening section for full
  detail):
  - **CanonicalView** (`core/canonical_view.py`): required `fact_id`/
    `source`/`claim` are non-empty strings only; `confidence` must be a real
    `int`/`float` (never `bool`), finite, in `[0.0, 1.0]` — malformed and
    oversized (e.g. `10**1000`) numeric values fail closed rather than
    crashing; `truth_status == VERIFIED` is cross-checked against the same
    write-path policy function (`_truth_status_for`) rather than trusted in
    isolation, so an inconsistent `claim_type`/`source_status` combination
    fails closed; direct `generate_answer()`/`project_canonical()` callers
    that bypass pipeline reconciliation are independently protected, not
    reliant on an upstream sanitizer.
  - **L1/L3 reconciliation** (`core/pipeline.py::_reconcile_recalled_fact`):
    a terminal epistemic state (`Collapsed`/`Contradicted`/`Deprecated`) on
    either the in-flight fact or the physical L3 node blocks grounding; an
    unresolved non-terminal disagreement fails closed via a
    `STORE_STATE_CONFLICT` sentinel; a confirmed restriction on either L1 or
    L3 blocks; a backend's structural absence of a `restricted` column
    (e.g. `LadybugL3Graph`, which has no such column at all) is **not**
    treated as restricted when L1 independently confirms `False` — only a
    *confirmed* restriction (from either side) blocks; a
    confidence/claim_type/source_status disagreement between the in-flight
    fact and the L3 record fails closed; and polluted L1 trust metadata
    (left behind by an earlier pre-reconciliation write) is restored from
    the authoritative L3 values.
  - **Retrieval** (`core/pipeline.py::retrieve`): a fact already terminal in
    L1, or confirmed-restricted in L1, cannot seed or receive graph-walk
    activation; vector-search candidates are fetched with a margin
    (`_VECTOR_SEARCH_FETCH_MARGIN`) and trimmed after deny-dominant
    filtering, so a denied top-ranked candidate cannot starve a valid
    lower-ranked one out of the `k`-sized result window; malformed trust
    metadata (unhashable `claim_type`/`source_status`, oversized confidence
    integers) fails closed instead of crashing.
  - **TRACE**: a refusal never reports a false `Validated` trace state; a
    success trace's reported `epistemic_state` and `source` are synced to
    the facts that actually grounded the answer, not left from a
    pre-reconciliation snapshot.
  - **Episodic behavior — compatibility change**: implicit co-recall
    episodic linking is **removed**. Episodic graph mutations now require an
    explicit `episode` argument, and occur only after a successful
    strict-grounded answer, for the facts actually used in that answer.
    **Residual risk**: episodic graph binding is not fully transactional —
    a partial write remains theoretically possible on a backend failure
    mid-write. Current mitigation is a content-free log entry plus the
    `episode_link.failed` metric; no outbox/transaction wrapper was
    implemented in this cycle.
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

## Reviewer checkpoint

```text
docs/REVIEWER_CHECKPOINT_2026-07.md -> REVIEWER CHECKPOINT / documentation only
```

A single reviewer/grant-facing summary of the PR #206→#225 audit-hardening
cycle (correctness fixes, contradiction/immune docs, the CanonicalView RFC,
and the L3 retrieval benchmark). It is a snapshot, not a new status
source — `TEST_REPORT.md` and this file remain authoritative if it ages.

```text
docs/grants/SOTA_GRANT_SYNTHESIS_2026-07.md -> SOTA / grant synthesis / documentation only
```

A compact map connecting the existing comparison, grant, reviewer and
benchmark documents into one "where Crystal stands now" view. It cross-links
those documents rather than duplicating them and is not a new grant
application.

## Research-only design docs

The following documents are architecture notes only. They do not change runtime
behaviour and must not be cited as implemented Crystal capabilities.

```text
docs/research/dialogue-cultivation-layer.md -> RESEARCH / DOCUMENTED_ONLY
docs/CANONICAL_VIEW_RFC.md                  -> PARTIALLY IMPLEMENTED (strict-grounding slice) — see below
```

- **Presence & Dialogue Cultivation Layer — `RESEARCH / DOCUMENTED_ONLY`.** This RFC
  studies long-term dialogue continuity, anti-sycophancy, open questions, proactive
  reflection and user-state hypothesis boundaries. It explicitly makes no claims of
  sentience, consciousness, emotion, personhood, biological life or implemented
  autonomous companion behaviour. It does not add code, storage, workers, TruthGate
  wiring, Canon writes or runtime integration.
- **CanonicalView / Trusted-Only Read Mode — `PARTIALLY IMPLEMENTED` (issue #220,
  PR #257, hardened by PR #258).** The RFC's strict-grounding slice (section 4's
  inclusion rule) is implemented: `core/canonical_view.py`
  (`CanonicalReadMode.STRICT`/`CONTEXTUAL`, `is_strict_canonical()`,
  `project_canonical()`), wired into `core/pipeline.py::generate_answer()` as the
  default answer-grounding filter, with 132 net new regression tests across
  PR #258's seven commits. `CONTEXTUAL` mode exists as a tested pure function but
  is **not** wired into any default surface. The RFC's `review`/`full_graph` read
  modes, a CLI `--trusted-only` flag, an API `trusted_only` parameter, and the
  conflicting-`VERIFIED`-facts surfacing/abstention policy remain **not
  implemented** — do not cite those as current Crystal behaviour. See
  `docs/CANONICAL_VIEW_RFC.md` section 9 for the itemized acceptance-criteria
  breakdown.

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
| CanonicalView / trusted-only read boundary | PARTIALLY IMPLEMENTED (strict-grounding slice, PR #257, hardened PR #258) | physical L3 membership does not itself imply verified truth for confident answer grounding | `review`/`full_graph` modes, CLI/API `trusted_only` exposure, and conflicting-`VERIFIED`-facts abstention remain unimplemented (RFC section 9) — do not overclaim | Track remaining RFC slices (issue #220) as separate, narrowly-scoped follow-up PRs |

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
