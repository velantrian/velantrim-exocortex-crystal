# Test Report

Honest, reproducible test results for Velantrim ExoCortex — Crystal. No inflated
numbers: run the commands below and compare the figures.

## Summary

| Metric | Value |
|--------|-------|
| **Tests passing** | **813** |
| Tests skipped | 12 |
| Tests failing | 0 |
| **Total coverage** | **100%** (gate enforced at 100%, repo-wide `--cov=.`) |
| Test files | 46 (`tests/test_*.py`) |
| Python | 3.11 / 3.12 in CI |
| Runtime dependencies | standard library only |

The 100% coverage gate is enforced in `pyproject.toml` (`--cov=. --cov-fail-under=100`)
and in CI with the same flags. The 12 skipped tests cover optional backends
(LadybugDB, sentence-transformers, Neo4j, Anthropic) that are not installed in
the default environment; their backend-specific code paths are excluded via
`pragma: no cover`. Reaching the figures below requires the dev environment from
`requirements-dev.txt` (it installs the optional layers — FastAPI, cryptography,
PyYAML, pypdf, rdflib — that the suite exercises so coverage reflects the whole
codebase; none of them are runtime dependencies).

## How to reproduce

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
| `core/adapters/pdf_adapter.py`  | 22 | 100% |
| `core/adapters/rdf_adapter.py`  | 33 | 100% |
| `core/adapters/yaml_adapter.py` | 30 | 100% |
| `core/aio.py`          | 10  | 100% |
| `core/analogy.py`      | 86  | 100% |
| `core/api.py`          | 56  | 100% |
| `core/audit.py`        | 69  | 100% |
| `core/cli.py`          | 241 | 100% |
| `core/compliance.py`   | 43  | 100% |
| `core/concept.py`      | 96  | 100% |
| `core/consolidate.py`  | 49  | 100% |
| `core/contradiction.py`| 59  | 100% |
| `core/crypto.py`       | 62  | 100% |
| `core/demo_seed.py`    | 1   | 100% |
| `core/embedding.py`    | 76  | 100% |
| `core/erasure.py`      | 45  | 100% |
| `core/eval.py`         | 144 | 100% |
| `core/evidence.py`     | 77  | 100% |
| `core/fractal.py`      | 93  | 100% |
| `core/generation.py`   | 54  | 100% |
| `core/immune.py`       | 94  | 100% |
| `core/imports.py`      | 87  | 100% |
| `core/ingest.py`       | 90  | 100% |
| `core/knowledge.py`    | 132 | 100% |
| `core/l3_graph.py`     | 286 | 100% |
| `core/mcp_server.py`   | 103 | 100% |
| `core/memory.py`       | 196 | 100% |
| `core/metrics.py`      | 10  | 100% |
| `core/neurocore.py`    | 54  | 100% |
| `core/neurogenesis.py` | 96  | 100% |
| `core/observe.py`      | 35  | 100% |
| `core/pii.py`          | 56  | 100% |
| `core/pipeline.py`     | 266 | 100% |
| `core/provenance.py`   | 90  | 100% |
| `core/queue.py`        | 47  | 100% |
| `core/reconcile.py`    | 97  | 100% |
| `core/review.py`       | 81  | 100% |
| `core/trace.py`        | 26  | 100% |
| `core/velum.py`        | 106 | 100% |
| `core/volition.py`     | 75  | 100% |
| root tooling (`audit_metadata`, `check_rfc_duplicates`, `fill_dependencies`, `epigenetic_adaptation_module`, `velantrim_migrate_v3_1`) | 586 | 100% |
| `prototypes/` (4 research prototypes) | 145 | 100% |
| `utils/rfc_parser.py`  | 13  | 100% |
| **Total (repo-wide)**  | **4163** | **100%** |

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
| Optional knowledge adapters (WP4) — YAML, PDF, RDF/Linked Data | `test_adapters.py` |
| Evaluation harness — retrieval/trace/receipt + source-span coverage & contradiction precision/recall, `eval` CLI | `test_eval.py` |
| Import sessions & dry-run review (WP2) — predict-without-write, session restrict/erase, `learn --dry-run` | `test_imports.py` |
| Curator review queue (WP2) — pending/diagnose/approve/reject, audited force override | `test_review.py` |
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

*Figures reflect the suite as of 2026-06-09 and are regenerated by running the
commands above.*
