# Velantrim ExoCortex — Roadmap

This document is the **honest truth** about what's implemented vs designed.

## ✅ Implemented (MVP, ~600 lines in `core/`)

- L0 (in-memory dict) + L1 (SQLite) memory layers
- ESM state machine with 8 states and transition validation
- Ring Zero immutability guard (I6) for `VALUES_CORE` / `RING_ZERO` fact IDs
- BM25-lite retrieval over a hardcoded demo DATABASE (5 facts)
- Guardian (structural check) + TruthGate (confidence threshold)
- Provenance trace builder (`core/trace.py`)
- Tests: ESM transitions, Ring Zero, pipeline smoke (`tests/`)

## ✅ Implemented (metadata tooling, not runtime)

- `audit_metadata.py`, `fix_metadata*.py`, `fill_dependencies.py`, `check_rfc_duplicates.py`
- `velantrim_migrate_v3_1.py` — production migration tool with rollback
- Metadata hardening: Cyrillic → ASCII (39→0), layers 55→1 null, deps 54→27

## 📋 Designed in spec, NOT yet coded

| RFC | Component | Sprint target |
|-----|-----------|---------------|
| RFC0016 | Velum L1.5 synaptic pre-graph, `_degree_cache` | S2 |
| RFC0066 | Concept Emergence, ProtoConcept, Hebbian learning | S3 |
| RFC0065 | Memory Volition, `write_voluntary()`, VolitionWorker | S3 |
| RFC0067 v2.0 | Analogy Graph, Semantic Bridge Engine, Adaptive Decoder | S4 |
| RFC0063 | Knowledge Ingestion Pipeline | S4 |
| RFC0068 | NeuroCore (plastic memory, Phase 0 passive tracker) | S5+ |
| RFC0017 | FSRS power-law decay `R=(1+19/81×t/S)^(-0.5)` | S2 |
| — | Neo4j / KuzuDB integration (currently only SQLite) | S2 |
| — | Redis + fallback queue | S2 |
| — | Async/await throughout (currently sync) | S2 |
| — | Sprint A patches A1–A10 (documented, not wired) | S3 |

## 📊 Invariant enforcement status

- **I6** (RingZeroImmutable): ✅ enforced in `memory.py` + test
- **I1, I2**: 🟡 partial (MVP-level, SQLite only, not Neo4j graph)
- **I50, I50-b, I66, I70, I-K3, I68**: ❌ components not yet coded
- **I38–I65**: ❌ pending Sprint 3+

## Sprint plan

- **S1 (this sprint)**: Honesty — fix README, ESM bugs, add tests/CI/LICENSE
- **S2**: FSRS decay + Neo4j abstraction + async pipeline
- **S3**: RFC0066 ConceptEmergenceDetector + RFC0065 Volition + A6–A10 wiring
- **S4**: RFC0067 Analogy Graph + RFC0063 Ingestion
- **S5+**: RFC0068 NeuroCore (feature-flagged, Phase 0 passive)

## 🌿 NEW: Hybrid Biological Memory Vision (May 2026)

**Added strategic direction**: Transform Velantrim into a true hybrid biological-inspired memory system.

### New RFCs (Hybrid Architecture)

| RFC     | Component                                      | Priority   | Sprint |
|---------|------------------------------------------------|------------|--------|
| RFC0070 | Fractal Memory Layer (recursive anchoring, multi-scale self-similarity) | High       | S3     |
| RFC0071 | Epigenetic Adaptation Module (dynamic behavior switches without retraining) | High       | S3     |
| RFC0072 | Immune / CRISPR Memory Guard (hallucination blocking + fact verification) | Critical   | S4     |
| RFC0073 | Neurogenesis-inspired Dynamic Growth (add new "neurons" on demand) | Medium     | S5     |

### Updated Sprint Plan (Hybrid Focus)

- **S2 (current)**: Complete S2 items + begin RFC0070 Fractal Layer prototype
- **S3**: RFC0070 + RFC0071 (Fractal + Epigenetic) + integrate with existing TruthGate
- **S4**: RFC0072 Immune Guard + RFC0067 Analogy Graph
- **S5+**: RFC0073 Neurogenesis + full hybrid testing

**See also**: `HYBRID_VISION.md` for full architecture details and biological sources (Human, Dolphin, Insect, Plant, Bacteria, Fractal Brain).