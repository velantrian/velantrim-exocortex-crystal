# 🔱 Velantrim ExoCortex — Crystal

**Version**: v8.0.2-sprint1 (spec) · MVP (code) · April 2026

> ⚠️ **Honest status**: this repo contains two layers:
> - **📜 Design spec** — `Velantrim_V8_Crystal_Sprint1.jsonl` (63 chunks, 947KB) describing the full system.
> - **🧩 MVP implementation** — `core/` (~600 lines) that implements ~3% of the spec.
>
> Most RFCs are **designed, not yet coded**. See [ROADMAP.md](./ROADMAP.md) for what's real.

---

## What is Velantrim

Velantrim is a long-term memory system for AI agents: a living knowledge graph with a biological memory model, truth gating, and organic concept emergence — *when fully built*. Right now the working code is a minimum viable pipeline demonstrating the core ideas (ESM lifecycle, truth gate, provenance trace).

## Three principles (spec-level)

1. **Graph = Truth** — the L3 graph is the single source of truth; LLMs speak, the graph decides.
2. **Memory = Physiology** — layers L0–L6 with FSRS decay and consolidation.
3. **Dual-Process** — Fast Path (ms) for the user, Slow Path (async) for the system.

## What's actually in this repo

| Path | Status | What it is |
|------|--------|------------|
| `core/memory.py` | ✅ MVP | L0 (in-memory) + L1 (SQLite) + ESM state machine (8 states) |
| `core/pipeline.py` | ✅ MVP | Retrieve → FactsPack → Guardian → TruthGate → Answer |
| `core/trace.py` | ✅ MVP | Provenance chain for each fact |
| `tests/` | ✅ MVP | Unit tests for ESM and pipeline |
| `Velantrim_V8_Crystal_Sprint1.jsonl` | 📜 Spec | Full system design (63 chunks, 947KB) |
| Metadata tooling | ✅ Stable | `audit_metadata.py`, `fix_metadata*.py`, `velantrim_migrate_v3_1.py` for jsonl maintenance |

## What's in the spec but NOT yet in the code

- 🕸️ RFC0016 — Velum L1.5 synaptic pre-graph
- 🌱 RFC0066 — Concept Emergence (ProtoConcept, Hebbian learning)
- 🗳️ RFC0065 — Memory Volition (`memory.write_voluntary()`)
- 🎨 RFC0067 v2.0 — Analogy Graph + Semantic Bridge Engine
- 📚 RFC0063 — Knowledge Ingestion Pipeline
- 🧠 RFC0068 — NeuroCore (plastic memory layer)
- 🧮 FSRS power-law decay `R = (1 + 19/81 × t/S)^(-0.5)`
- 🔒 Ring Zero / VALUES_CORE immutability (I6)
- 🗄️ Neo4j / KuzuDB / Redis integration
- 🔄 Async/await throughout (code is currently sync)
- 📊 Sprint A patches A1–A10 (documented in `SPRINT_A_V2_ADDITIONAL_PATCHES.md` — not yet wired)

Sprint A patch progress in code: **0 / 45**. See [ROADMAP.md](./ROADMAP.md).

## Quick start

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
pip install -r requirements.txt
python -m core.pipeline        # runs 3 demo queries
pytest tests/                  # runs the MVP test suite
```

## ESM — Epistemic State Machine (implemented)

Facts live in one of 8 states:

```
Observed → Hypothesized → Supported → Validated → ImmutableCore
                                   ↘ Contradicted → Deprecated → Collapsed
```

MVP fast-path allows `Observed → Validated` directly for the demo pipeline. The full transition rules from the spec (evidence_count ≥ 2, truth_gate ≥ 0.7, etc.) are a Sprint 2 task.

## Spec documents

- `Velantrim_V8_Crystal_Sprint1.jsonl` — canonical knowledge base (63 chunks)
- `Velantrim_V8_Crystal_Sprint1_toc.md` — human-readable table of contents
- `METADATA_FIX_REPORT.md` — history of the metadata hardening work
- `SPRINT_A_V2_ADDITIONAL_PATCHES.md` — A6–A10 patch designs (not wired to code)
- `MIGRATION_GUIDE_V3_1.md` — how to use the migration tool

## Invariants tracked in the spec (not yet enforced by tests)

| ID | Name | Status |
|----|------|--------|
| I1 | Graph = Truth | 🟡 MVP approximates via TruthGate |
| I2 | TruthGate is the only entry to L3 | 🟡 MVP enforces on SQLite, not Neo4j |
| I6 | RingZeroImmutable | ✅ enforced in `transition_esm()` |
| I50/I50-b/I66/I70/I-K3 | Concept Emergence | ❌ component not yet coded |
| I68 | NeuroCoreIsolation | ❌ component not yet coded |

Enforcement via `tests/test_invariants.py` — Sprint 3+.

## Contributing

1. Read this README first.
2. Check `ROADMAP.md` to see if your idea is already scoped.
3. New architectural ideas → open an issue before editing the spec.

## License

MIT — see [LICENSE](./LICENSE).

---

> Graph = Truth · LLM = Language · Memory = Physiology · Volition = Agency · Emergence = Life
