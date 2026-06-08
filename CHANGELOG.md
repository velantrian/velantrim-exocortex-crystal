# 📋 Changelog

All notable changes to Velantrim ExoCortex — Crystal are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

> **Versioning note.** `0.1.0` is the **first public release** of the open core.
> The architecture descends from the internal "v8" Crystal design line (tracked in
> `ROADMAP.md`); the published package version in `pyproject.toml` is the single
> source of truth for releases.

## [Unreleased]

### Added
- **RFC0063 — External knowledge ingestion** (`core/knowledge.py`): bulk-import
  `.txt` / `.md` / `.json` / `.jsonl` / `.csv` knowledge files through the same
  Guardian → TruthGate path as user utterances; imported facts carry
  `source_status = EXTERNAL` with the source file as provenance. CLI `learn`.
- **RFC0068 — NeuroCore Phase 0** (`core/neurocore.py`): a passive plasticity
  tracker that logs the norm of the would-be weight delta (ΔW) when surprise > θ.
  Off by default (`VELANTRIM_NEUROCORE`); never touches the model and never writes
  the L3 graph (invariant I68). CLI `neurocore-report`.
- **Sprint-A A9 — LLM call safety** (`core/generation.py`): bounded retry with
  exponential backoff on transient API failures, no retry for non-transient
  errors, output ceiling, graceful degradation to the extractive generator.
- Community & governance docs: `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`,
  `GOVERNANCE.md`, this `CHANGELOG.md`, `.github/FUNDING.yml`, and
  `docs/SPRINT_A_STATUS.md` (honest A1–A10 triage).
- README: a "Data sovereignty & offline autonomy" section (local-only storage,
  accurate answers without an LLM / offline, durable interconnections, EU data
  sovereignty).

### Changed
- README headline version aligned to the published package version (`0.1.0`).
- Documentation figures synced to the current suite (**605 tests, ~99% coverage**)
  across README, ROADMAP, GDPR, and TEST_REPORT.

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
