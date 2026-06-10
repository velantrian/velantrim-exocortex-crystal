# 📋 Changelog

All notable changes to Velantrim ExoCortex — Crystal are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

> **Versioning note.** `0.1.0` is the **first public release** of the open core.
> The architecture descends from the internal "v8" Crystal design line (tracked in
> `ROADMAP.md`); the published package version in `pyproject.toml` is the single
> source of truth for releases.

## [Unreleased]

### Changed
- **P1 cross-audit hardening** (follow-up to the P0 round):
  - the evaluation harness now replays receipts with `strict_provenance=True`,
    so a VERIFIED citation without source-span evidence fails
    `receipt_replay_survival` (and the CI eval gate), not just the
    `unsupported_provenance` count;
  - `velantrim verify-receipt` gains `--strict-provenance` (parity with the
    HTTP API's `strict_provenance` option);
  - README adds two deployment-honesty notes: the sector table now carries an
    explicit caveat (local single-user library — no auth/multi-tenant, on-disk
    L3 not field-encrypted yet) and the FastAPI section a "localhost-only,
    no auth" warning;
  - `core/l3_graph.py` comments no longer assert the unverified
    "successor to Kuzu / Apple acquisition" claims (now: "Kuzu lineage;
    upstream repository archived Oct. 2025") and the stale "default — mock"
    header comment matches the real `auto` chain;
  - removed the duplicated `docs/COMPARISON.md` row in the README
    documentation table.

### Fixed
- **P0 cross-audit hardening** (Claude / ChatGPT / Grok review):
  - `VELANTRIM_DB` is now actually read by `core/memory.py`, so
    `scripts/eval_gate.py` and the `docs/DEMO.md` instructions truly isolate the
    L1 SQLite store (previously the variable was set but ignored and L1 always
    wrote to `./data/velantrim_memory.db`).
  - `reconcile._sync_l3()` now mirrors the pipeline's self-heal path: on an L3
    merge failure the fact is queued in the L3 outbox for `drain_l3_outbox()`
    instead of silently losing the sync.
  - `core/consolidate.py` no longer calls `merge_fact(None)` when an L1 record
    was erased while its L3 node lingers (defensive `_remerge` guard).
  - `PRIVACY.md` now describes the real default L3 backend chain
    (`auto` → LadybugDB → **on-disk SQLite** → in-memory mock) instead of
    claiming the in-memory mock is the default.
  - TruthGate invariant wording made precise across README / ARCHITECTURE /
    implementation-status: TruthGate is the only **automatic** entry into L3;
    the sole exception is the explicit, audited curator override in the review
    queue (`core/review.py`).
  - Documentation figures re-synced to the verified suite (**717 passing tests,
    12 skipped optional-backend tests, 100% coverage**) and the coverage gate
    unified at **100%** across `pyproject.toml`, CI and contributor docs
    (previously CI enforced 95% while `pyproject.toml` required 100%).

### Added
- **FastAPI service layer** (`core/api.py`, optional `pip install '.[api]'`,
  console script `velantrim-api`): HTTP endpoints `/health`, `/ingest`, `/ask`,
  `/receipt`, `/verify-receipt`, `/evidence/{fact_id}` — thin async wrappers over
  `core/aio.py` that mirror the CLI and add no TruthGate-bypassing write path.
  FastAPI/uvicorn stay an optional extra; the default runtime is standard-library
  only.
- **RFC0063 — External knowledge ingestion** (`core/knowledge.py`): bulk-import
  `.txt` / `.md` / `.json` / `.jsonl` / `.csv` knowledge files through the same
  Guardian → TruthGate path as user utterances; imported facts carry
  `source_status = EXTERNAL` with the source file as provenance. CLI `learn`.
- **RFC0068 — NeuroCore Phase 0** (`core/neurocore.py`): a passive plasticity
  tracker that logs the norm of the would-be weight delta (ΔW) when surprise > θ.
  Now wired into `pipeline.run()` — when enabled (`VELANTRIM_NEUROCORE`) every
  query records a surprise tick (surprise ≈ 1 − top retrieval relevance, incl.
  zero-hit cold-start queries). Off by default; never touches the model and never
  writes the L3 graph (invariant I68). CLI `neurocore-report`.
- **Sprint-A A9 — LLM call safety** (`core/generation.py`): bounded retry with
  exponential backoff on transient API failures, no retry for non-transient
  errors, output ceiling, graceful degradation to the extractive generator.
- **Evaluation quality gate** (`scripts/eval_gate.py`, `velantrim eval --gate`,
  grant WP3 baseline): the harness now runs over a curated, multi-domain fixture
  corpus bundled with the package (`core/_eval_fixtures/` — 16 retrieval cases
  with ranking distractors, 12 labelled contradiction pairs incl. hard
  negatives), emits per-case `metrics.jsonl` + `eval_report.md`, and is enforced
  by a dedicated `eval-gate` CI job with regression thresholds so retrieval /
  grounding / contradiction quality cannot silently drop. `velantrim eval` gains
  `--detail`, `--md` and `--gate`.
- **Hands-on demo walkthrough** (`docs/DEMO.md`, grant WP5 baseline): a
  reproducible CLI tour with real captured output — ingest → ask → provenance
  receipt + replay → contradiction detection → knowledge import + source-span
  evidence → GDPR erase + tamper-evident audit → NeuroCore telemetry → eval
  harness → optional HTTP. Linked from the README and the NLnet scope.
- Community & governance docs: `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`,
  `GOVERNANCE.md`, this `CHANGELOG.md`, `.github/FUNDING.yml`, and
  `docs/SPRINT_A_STATUS.md` (honest A1–A10 triage).
- README: a "Data sovereignty & offline autonomy" section (local-only storage,
  accurate answers without an LLM / offline, durable interconnections, EU data
  sovereignty).

### Changed
- README headline version aligned to the published package version (`0.1.0`).
- Audit cleanup (#73): `BackendRegistry.reset()` now closes a cached L3 instance
  exposing `close()` (no SQLite connection leak across resets); `get_l3_graph`
  `auto` docstring corrected; `concept.hebbian_weights()` folds directed edge
  counts robustly; assorted LOW smells (`verify-receipt` file handle, decimal
  handling in `contradiction._content`).
- Documentation figures synced to the suite as it stood at the time (**633
  tests, ~99% coverage**) across README, ROADMAP, GDPR, and TEST_REPORT —
  superseded by the 717 / 100% re-sync recorded under *Fixed* above.

### Removed
- Dead research scaffolding: velum's unused observation window
  (`VELANTRIM_VELUM_WINDOW` env knob — recorded but never read by co-occurrence
  counting) and the decorative, unenforced `_Tool.capability` field on the
  read-only MCP server.

## [0.1.0] — first public release

Initial public release of the verifiable, local-first memory core:

- **Foundation:** L0/L1 memory layers, the 8-state Epistemic State Machine, the
  swappable L3 canonical graph (`auto`→LadybugDB / on-disk SQLite / mock / Neo4j),
  vector + graph retrieval, swappable embedder and answerer, utterance ingestion,
  and `pip`-installable packaging with the `velantrim` CLI.
- **Trust & truth:** Guardian + TruthGate, provenance trace, replayable answer
  receipts, contradiction detection, FSRS-style consolidation, and the Immune /
  CRISPR memory guard (RFC0072).
- **Privacy & GDPR:** Art. 17 erasure (+ cascade & tombstones), Art. 18
  restriction, Art. 30 record-of-processing, Art. 32 encryption at rest, a
  tamper-evident audit log, and PII redaction.
- **Living memory (biologically-inspired):** Fractal Memory (RFC0070), Epigenetic
  Adaptation (RFC0071), Neurogenesis (RFC0073), Concept Emergence (RFC0066),
  Memory Volition (RFC0065), Velum L1.5 (RFC0016), and the Analogy Graph +
  Semantic Bridges + CREATIVE mode (RFC0067 v2.0).
- **Ops & integration:** pluggable Redis/SQLite re-merge queue, async entry
  points, a dependency-free read-only MCP server, observability, and the CLI.

[Unreleased]: https://github.com/velantrian/velantrim-exocortex-crystal/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/velantrian/velantrim-exocortex-crystal/releases/tag/v0.1.0
