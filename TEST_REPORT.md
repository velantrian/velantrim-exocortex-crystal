# Test Report

Honest, reproducible test results for Velantrim ExoCortex — Crystal. No inflated
numbers: run `pytest` yourself and you will get the figures below.

## Summary

| Metric | Value |
|--------|-------|
| **Tests passing** | **501** |
| Tests skipped | 12 |
| Tests failing | 0 |
| **Total coverage** | **~99%** (gate enforced at 95%) |
| Test files | 38 (`tests/test_*.py`) |
| Python | 3.11 (3.10+ supported) |
| Runtime dependencies | standard library only |

The 95% coverage floor is enforced in `pyproject.toml`
(`--cov-fail-under=95`); the suite fails CI if coverage drops below it.
The 12 skipped tests cover optional backends (LadybugDB, sentence-transformers,
Neo4j, Anthropic) that are not installed in the default environment. The Redis
queue backend (`core/queue.py`, 91%) is exercised against an in-memory fake; the
few uncovered lines are the live-server connection path (`redis.from_url` + PING),
which needs a running Redis and is not part of the dependency-free default.

## How to reproduce

```bash
pip install -r requirements.txt
pytest                 # 501 passed, 12 skipped
```

## Coverage by module (core/)

| Module | Stmts | Cover |
|--------|------:|------:|
| `core/_registry.py`    | 18  | 100% |
| `core/adaptation.py`   | 22  | 100% |
| `core/aio.py`          | 10  | 100% |
| `core/audit.py`        | 69  | 100% |
| `core/cli.py`          | 149 | 100% |
| `core/compliance.py`   | 43  | 100% |
| `core/concept.py`      | 93  | 100% |
| `core/consolidate.py`  | 45  | 96%  |
| `core/contradiction.py`| 53  | 100% |
| `core/crypto.py`       | 62  | 100% |
| `core/embedding.py`    | 76  | 100% |
| `core/erasure.py`      | 45  | 100% |
| `core/fractal.py`      | 93  | 99%  |
| `core/generation.py`   | 41  | 100% |
| `core/immune.py`       | 94  | 100% |
| `core/ingest.py`       | 89  | 100% |
| `core/l3_graph.py`     | 259 | 99%  |
| `core/mcp_server.py`   | 104 | 100% |
| `core/memory.py`       | 185 | 100% |
| `core/metrics.py`      | 10  | 100% |
| `core/neurogenesis.py` | 96  | 99%  |
| `core/observe.py`      | 35  | 100% |
| `core/pii.py`          | 56  | 100% |
| `core/pipeline.py`     | 249 | 98%  |
| `core/provenance.py`   | 68  | 100% |
| `core/queue.py`        | 53  | 91%  |
| `core/reconcile.py`    | 80  | 96%  |
| `core/trace.py`        | 26  | 100% |
| `core/velum.py`        | 112 | 99%  |
| `core/volition.py`     | 75  | 99%  |
| **Total (repo-wide)**  | **3154** | **~99%** |

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
| Neurogenesis Dynamic Growth (RFC0073) — plasticity, pattern separation, growth/prune, CLI | `test_neurogenesis.py` |
| L3 canonical graph adapter & backends | `test_l3_graph.py` |
| On-disk SQLite L3 backend (persistence, erase, vectors, entities) | `test_l3_sqlite.py` |
| Packaging contract (entry point, version, package surface) | `test_packaging.py` |
| Embeddings (hashing + optional sbert) | `test_embedding.py` |
| Answer generation (extractive + optional Claude) | `test_generation.py` |
| Ingestion & claim-type classification | `test_ingest.py` |
| Truth maintenance (reinforce/supersede/contradict) | `test_reconcile.py` |
| Contradiction classifier (negation/antonym/numeric, auto-contradict) | `test_contradiction.py` |
| Consolidation / FSRS-style decay | `test_consolidate.py` |
| Provenance trace | `test_trace.py` |
| Verifiable answer receipts (digest, HMAC, replay/drift detection) | `test_provenance.py` |
| GDPR Art. 17 physical erasure, cascade & tombstones | `test_erasure.py` |
| GDPR Art. 18 restriction & Art. 30 record-of-processing | `test_compliance.py` |
| GDPR Art. 32 encryption at rest (round-trip, tamper, at-rest ciphertext) | `test_crypto.py` |
| Tamper-evident audit log (hash chain, tamper detection, HMAC signing) | `test_audit.py` |
| PII detection & redaction (email/phone/card/IPv4/IBAN, Luhn, overlap) | `test_pii.py` |
| Adaptive TruthGate threshold | `test_adaptation.py` |
| Observability & metrics | `test_observe.py`, `test_metrics.py` |
| Migration tooling & rollback | `test_migration.py`, `test_migration_extra.py` |
| Metadata audit scripts | `test_audit_scripts.py`, `test_audit_regressions.py` |
| RFC parsing | `test_rfc_parser.py` |
| Biological-inspiration prototypes | `test_bio_modules.py`, `test_hybrid_biological_memory.py` |

*Figures reflect the suite as of 2026 and are regenerated by running `pytest`.*
