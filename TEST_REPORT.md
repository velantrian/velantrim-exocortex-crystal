# Test Report

Honest, reproducible test results for Velantrim ExoCortex — Crystal. No inflated
numbers: run the commands below and compare the figures.

**Current audited baseline after v0.2.0 + TRACE Visualization v0 + CI coverage fixes + Crystal Invariant Checker + Refusal Reasons Taxonomy v0.1 + PR #137 safe repo hygiene/toolchain hardening + PRs #142–#144 Codex P2 hardening + PR #152 reviewer tooling, then the v0.3.0 reviewer-preview audit-hardening
milestone (RRF helper #163, exact-dedup #164, per-fact ProvenanceChain #168,
Docker hardening #170/#171, strict TruthPolicy default #172, write-path
TruthGate audit #175), then the post-tag PDF span fix #182: 1210 passed /
12 skipped.** This file and the README badge are the only places that carry
the exact count; all other documents reference this report so the number
cannot silently drift.

> **PR #137 note.** The safe repo hygiene / toolchain hardening pass added 11
> tests (1130 → 1141) and grew the measured surface by 28 statements
> (5130 → 5158) while preserving the 100% coverage gate.

> **PRs #142–#144 note.** The Codex P2 review hardening passes (adapter
> parsing robustness, runtime bug fixes, eval_track completeness) added 17
> tests (1141 → 1158) and grew the measured surface by 134 statements
> (5158 → 5292) while preserving the 100% coverage gate.

> **PR #152 note.** PR #152 added read-only reviewer tooling for `velantrim trace`
> and `velantrim health`, adding 10 tests (1158 → 1168) and growing the measured
> surface by 42 statements (5292 → 5334) while preserving the 100% coverage gate.

> **v0.3.0 reviewer-preview note.** The audit-hardening milestone — RRF helper
> (#163), exact-duplicate ingest dedup (#164), per-fact ProvenanceChain (#168),
> Docker hardening (#170/#171), strict TruthPolicy production default (#172) and
> the write-path TruthGate audit (#175) — took the suite 1168 → 1209 tests and
> the measured surface 5334 → 5461 statements while preserving the 100% coverage
> gate. After this milestone the runtime is frozen (reviewer-facing packaging
> only).

> **PR #182 note.** A post-tag span fix for repeated identical PDF paragraphs
> (#182, `core/adapters/pdf_adapter.py`) added 1 test in `tests/test_wp1_spans.py`,
> taking the suite 1209 → 1210 while preserving the 100% coverage gate. PR #183
> was docs-only (epistemic dogfooding cases log) and did not change the count.

## Summary

| Metric | Value |
|--------|-------|
| **Tests passing** | **1210** |
| Tests skipped | 12 |
| Tests failing | 0 |
| **Total coverage** | **100%** (gate enforced at 100%, repo-wide `--cov=.`) |
| Test files | 67 (`tests/test_*.py`) |
| Python | 3.11 / 3.12 in CI |
| Runtime dependencies | standard library only |

The 100% coverage gate is enforced in `pyproject.toml` (`--cov=. --cov-fail-under=100`)
and in CI with the same flags. The 12 skipped tests cover optional backends
(LadybugDB, sentence-transformers, Neo4j, Anthropic) that are not installed in
the default environment; their backend-specific code paths are excluded via
`pragma: no cover`. Reaching the figures below requires the dev environment from
`requirements-dev.txt` (it installs the optional layers — FastAPI, cryptography,
PyYAML, pypdf, rdflib, ebooklib, requests — that the suite exercises so coverage
reflects the whole codebase; none of them are runtime dependencies).

## How to reproduce

```bash
# Recommended: single-step editable install (aligns with the [dev] extra)
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
```

The `requirements-dev.txt` file is the equivalent CI path and stays aligned with
the `[dev]` extra; either installs the same environment. On CI:

```bash
pip install -r requirements-dev.txt
pip install -e .
pytest tests/ --cov=. --cov-fail-under=100
```

## Coverage by module

| Module | Stmts | Cover |
|--------|------:|------:|
| `core/_registry.py`    | 24  | 100% |
| `core/adaptation.py`   | 22  | 100% |
| `core/adapters/bibtex_adapter.py`   | 85 | 100% |
| `core/adapters/epub_adapter.py`     | 83 | 100% |
| `core/adapters/pdf_adapter.py`      | 43 | 100% |
| `core/adapters/rdf_adapter.py`      | 33 | 100% |
| `core/adapters/wikidata_adapter.py` | 66 | 100% |
| `core/adapters/yaml_adapter.py`     | 30 | 100% |
| `core/aio.py`          | 10  | 100% |
| `core/analogy.py`      | 86  | 100% |
| `core/api.py`          | 114 | 100% |
| `core/audit.py`        | 69  | 100% |
| `core/cli.py`          | 322 | 100% |
| `core/compliance.py`   | 43  | 100% |
| `core/concept.py`      | 96  | 100% |
| `core/consolidate.py`  | 49  | 100% |
| `core/contradiction.py`| 59  | 100% |
| `core/crypto.py`       | 62  | 100% |
| `core/demo_seed.py`    | 1   | 100% |
| `core/embedding.py`    | 104 | 100% |
| `core/erasure.py`      | 47  | 100% |
| `core/eval.py`         | 207 | 100% |
| `core/evidence.py`     | 77  | 100% |
| `core/fractal.py`      | 93  | 100% |
| `core/generation.py`   | 54  | 100% |
| `core/health.py`       | 14  | 100% |
| `core/immune.py`       | 94  | 100% |
| `core/imports.py`      | 87  | 100% |
| `core/ingest.py`       | 120 | 100% |
| `core/invariant_check.py`   | 64  | 100% |
| `core/kb_ingest.py`    | 49  | 100% |
| `core/knowledge.py`    | 140 | 100% |
| `core/l3_graph.py`     | 286 | 100% |
| `core/mcp_server.py`   | 103 | 100% |
| `core/memory.py`       | 222 | 100% |
| `core/metrics.py`      | 10  | 100% |
| `core/mosc.py`         | 93  | 100% |
| `core/neurocore.py`    | 54  | 100% |
| `core/neurogenesis.py` | 96  | 100% |
| `core/observe.py`      | 35  | 100% |
| `core/pii.py`          | 56  | 100% |
| `core/pipeline.py`     | 252 | 100% |
| `core/provenance.py`   | 90  | 100% |
| `core/provenance_chain.py`  | 46  | 100% |
| `core/queue.py`        | 47  | 100% |
| `core/reconcile.py`    | 117 | 100% |
| `core/refusal_reasons.py`   | 26  | 100% |
| `core/retrieval_config.py`  | 69  | 100% |
| `core/review.py`       | 163 | 100% |
| `core/rrf.py`          | 37  | 100% |
| `core/salience.py`     | 19  | 100% |
| `core/span_extract.py` | 22  | 100% |
| `core/trace.py`             | 26  | 100% |
| `core/trace_visualize.py`   | 73  | 100% |
| `core/truth_gate.py`        | 24  | 100% |
| `core/velum.py`             | 106 | 100% |
| `core/volition.py`          | 75  | 100% |
| `scripts/eval_track.py`     | 72  | 100% |
| `scripts/trace_visualize.py`| 22  | 100% |
| root tooling (`audit_metadata` 109, `check_rfc_duplicates` 44, `fill_dependencies` 43, `epigenetic_adaptation_module` 29, `velantrim_migrate_v3_1` 393) | 618 | 100% |
| `prototypes/` (4 research prototypes) | 142 | 100% |
| `utils/rfc_parser.py`       | 13  | 100% |
| **Total (repo-wide)**       | **5461** | **100%** |

## What the tests cover

| Area | Test file |
|------|-----------|
| Memory layers (L0/L1), ESM transitions, Ring Zero (I6) | `test_memory.py`, `test_esm.py` |
| End-to-end pipeline (retrieve → gate → L3 → answer) | `test_pipeline.py` |
| Pluggable re-merge queue (SQLite/Redis backends, fallback) & async entry points | `test_queue.py` |
| Immune / CRISPR Memory Guard (RFC0072) — threat memory, screening, strict/learn, CLI | `test_immune.py` |
| Fractal Memory Layer (RFC0070) — anchor strength, reanchor/spill, decay protection, CLI | `test_fractal.py` |
| Concept Emergence (RFC0066) — Hebbian weights, union-find clustering, emerge/lookup, CLI | `test_concept.py` |
| Memory Volition (RFC0065) — salience, voluntary writes through the gates, rehearsal, CLI | `test_volition.py` |
| L1.5 Velum (RFC0016) — synaptic edges, signals, session decay, GC, degree cache, CLI | `test_velum.py` |
| Analogy Graph / Bridges / CREATIVE (RFC0067) — edges, structural similarity, bridges, temperature, CLI | `test_analogy.py` |
| Neurogenesis Dynamic Growth (RFC0073) — plasticity, pattern separation, growth/prune, CLI | `test_neurogenesis.py` |
| NeuroCore Phase 0 (RFC0068) — passive plasticity tracker, threshold, I68 isolation, CLI | `test_neurocore.py` |
| External knowledge ingestion (RFC0063) — txt/md/json/jsonl/csv parsers, TruthGate routing, `learn` CLI | `test_knowledge.py` |
| Optional knowledge adapters (WP4) — YAML, PDF, RDF/Linked Data, EPUB, BibTeX, Wikidata | `test_adapters.py` |
| Source span offsets (WP1) — `locate_claim`, `extract_section`, `snippet_around` pure utilities | `test_span_extract.py` |
| Source span offsets (WP1) integration — `ingest_text` / `ingest_claims` span recording, adapter-supplied spans, PDF page chunks | `test_wp1_spans.py` |
| Evaluation harness — retrieval/trace/receipt + source-span coverage & contradiction precision/recall, `eval` CLI | `test_eval.py` |
| Per-release eval tracking (WP3) — trend logging, Markdown trend report, `eval_track` CLI | `test_eval_track.py` |
| TRACE Visualization v0 — read-only receipt formatter (Markdown + DOT), per-citation verify status, trace-array input, CLI | `test_trace_visualize.py` |
| Crystal Invariant Checker — read-only at-rest invariant scan, 3 implemented checks + 2 SKIPPED_UNSUPPORTED, exit codes, reason_code integration | `test_invariant_check.py` |
| Refusal Reasons Taxonomy v0.1 — 13 reason codes, severity levels, API (get/list/is_valid/format), module constants | `test_refusal_reasons.py` |
| Reviewer tooling (PR #152) — `velantrim trace` read-only receipt/trace pretty-printer (file/stdin, `--json`, unrecognized→exit 1) and `velantrim health` diagnostic memory-health score | `test_cli.py`, `test_health.py` |
| Import sessions & dry-run review (WP2) — predict-without-write, session restrict/erase, `learn --dry-run` | `test_imports.py` |
| Curator review queue (WP2) — pending/diagnose/approve/reject, audited force override | `test_review.py` |
| Resumable review sessions (WP2) — create/resume/record/complete, stable-order batch, no-write invariant | `test_review_resumable.py` |
| Force override audit pinning (WP2) — RuntimeWarning, content-free, audit event, metric, rejection guards | `test_force_override_audit.py` |
| KB dry-run batch manifest (WP2/WP4) — JSONL/JSON/NDJSON manifest, accept/block/conflict verdicts, no-write, CLI | `test_kb_dryrun.py` |
| Optional FastAPI service layer — endpoint parity with the CLI, no gate bypass | `test_api.py` |
| Read-only MCP server (JSON-RPC over stdio) | `test_mcp_server.py` |
| L3 canonical graph adapter & backends | `test_l3_graph.py` |
| On-disk SQLite L3 backend (persistence, erase, vectors, entities) | `test_l3_sqlite.py` |
| Packaging contract (entry point, version, package surface) | `test_packaging.py` |
| Embeddings (hashing + optional sbert) | `test_embedding.py` |
| Answer generation (extractive + optional Claude) + A9 LLM call safety (bounded retry/backoff) | `test_generation.py` |
| Ingestion & claim-type classification | `test_ingest.py` |
| Truth maintenance (reinforce/supersede/contradict) | `test_reconcile.py` |
| Contradiction classifier (negation/antonym/numeric, auto-contradict) | `test_contradiction.py` |
| Consolidation / FSRS-style decay | `test_consolidate.py` |
| Provenance trace | `test_trace.py` |
| Verifiable answer receipts (digest, HMAC, replay/drift detection) | `test_provenance.py` |
| Evidence span store + Receipt v2 (source-span provenance, replay, `evidence` CLI) | `test_evidence.py` |
| GDPR Art. 17 physical erasure, cascade & tombstones | `test_erasure.py` |
| GDPR Art. 18 restriction & Art. 30 record-of-processing | `test_compliance.py` |
| GDPR Art. 32 encryption at rest (round-trip, tamper, at-rest ciphertext) | `test_crypto.py` |
| Tamper-evident audit log (hash chain, tamper detection, HMAC signing) | `test_audit.py` |
| PII detection & redaction (email/phone/card/IPv4/IBAN, Luhn, overlap) | `test_pii.py` |
| Adaptive TruthGate threshold | `test_adaptation.py` |
| Observability & metrics | `test_observe.py`, `test_metrics.py` |
| Migration tooling & rollback | `test_migration.py`, `test_migration_extra.py` |
| Metadata audit scripts | `test_audit_scripts.py`, `test_audit_regressions.py` |
| P0 cross-audit hardening (`VELANTRIM_DB` isolation, `_sync_l3` outbox recovery, consolidate None guard) | `test_p0_hardening.py` |
| RFC parsing | `test_rfc_parser.py` |
| Biological-inspiration prototypes | `test_bio_modules.py`, `test_hybrid_biological_memory.py` |

*The per-module table below was regenerated on 2026-06-17 for the v0.3.0 reviewer
preview (audit-hardening milestone: RRF #163, exact-dedup #164, ProvenanceChain
#168, Docker hardening #170/#171, strict TruthPolicy default #172, write-path
TruthGate audit #175) from a live `--cov=.` run at 1209 passed / 12 skipped /
100%. The post-tag PDF span fix #182 then added one test in
`tests/test_wp1_spans.py`; the current total is 1210 passed / 12 skipped / 100%
(confirmed by CI). The per-module rows predate #182 and will be regenerated at the
next full audit. All figures are reproduced by running the commands above.*
