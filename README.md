# 🔱 Velantrim ExoCortex — Crystal

**Version**: v8.1.0-hybrid (Enhanced) · April 2026

> ⚠️ **Honest status**: This repository is the foundation for a **hybrid biological-inspired memory system** for AI. It combines truth-first graph memory with nature’s proven mechanisms (human hippocampus, animal episodic memory, insect associative learning, plant epigenetics, bacterial CRISPR immunity, and fractal structures).

---

## Vision: Hybrid Memory Architecture 🧠🌱

Velantrim ExoCortex Crystal is evolving into a **next-generation memory system** that learns from the best biological examples:

- **Human & Dolphins** — Episodic "what-where-when" memory + long-term social recall
- **Birds & Octopuses** — Superior spatial + observational learning
- **Insects (bees, flies)** — Ultra-efficient associative memory (mushroom bodies)
- **Plants & Trees** — Epigenetic inheritance + collective memory via mycorrhizal networks
- **Bacteria** — CRISPR-style immune memory for error protection
- **Fractal principles** — Self-similar, scalable, resilient architecture (inspired by brain and nature)

**Goal**: Create an AI memory that is:
- Long-lasting (lifelong learning without catastrophic forgetting)
- Energy-efficient (like biological systems)
- Self-healing and adaptive (epigenetic switching)
- Protected against hallucinations and errors (immune layer)

## Core Principles (Updated for Hybrid Era)

1. **Graph = Truth** — The knowledge graph remains the single source of truth.
2. **Memory = Physiology** — Multi-layer system (L0–L6) with biological decay, consolidation, and neurogenesis-like growth.
3. **Dual-Process** — Fast Path (real-time) + Slow Path (deep consolidation + epigenetic adaptation).
4. **Fractal Resilience** — Self-similar structures at every scale for scalability and fault tolerance.
5. **Epigenetic Adaptation** — "Gene switches" that change system behavior based on past stress without full retraining.
6. **Immune Memory** — CRISPR-like mechanism to instantly recognize and neutralize contradictions, hallucinations, or attacks.

## Biological Inspiration Table 🐳🐝🌱

| Biological Source       | Mechanism Borrowed                          | Benefit for AI Memory                     |
|-------------------------|---------------------------------------------|-------------------------------------------|
| Human + Dolphins       | Episodic memory + long-term social recall  | Rich "what-where-when" + relationship tracking |
| Birds + Octopuses      | Spatial + observational learning           | Fast adaptation to new environments       |
| Insects (Mushroom Bodies) | Associative + coincidence detection       | Compact, fast pattern recognition         |
| Plants & Trees         | Epigenetics + mycorrhizal networks         | Transgenerational learning + collective resilience |
| Bacteria               | CRISPR immune memory                       | Rapid error/hallucination blocking        |
| Fractal Brain          | Self-similar hierarchical architecture     | Infinite scalability + damage resistance  |

## What's in This Repo (Current State)

| Path                          | Status     | Description                                                                 |
|-------------------------------|------------|-----------------------------------------------------------------------------|
| `core/memory.py`     | ✅ | L0 (in-memory LRU) + L1 (SQLite, WAL) + ESM (8 states) + `update_fact` |
| `core/pipeline.py`   | ✅ | Retrieve (vector + L3 recall) → FactsPack → Guardian → TruthGate → L3 → Answer; episodic linking + `recall_episode`/`recall_by_entity` |
| `core/l3_graph.py`   | ✅ | Swappable L3 canonical graph: `auto`→LadybugDB / `mock` / `neo4j`; nodes, edges, `vector_search` |
| `core/embedding.py`  | ✅ | Swappable embedder: `auto`→sentence-transformers / dependency-free hashing |
| `core/generation.py` | ✅ | Swappable answer generator: extractive (default) / Claude LLM |
| `core/ingest.py`     | ✅ | Utterance → claim_type classification → gate → L3 |
| `core/reconcile.py`  | ✅ | Truth maintenance: reinforce / supersede / contradict / find_conflicts |
| `core/consolidate.py`| ✅ | SleepCycle: significance-weighted confidence decay (FSRS-style) |
| `core/trace.py`      | ✅ | Provenance chain for every fact |
| `core/_registry.py`  | ✅ | Shared swappable-backend singleton factory |
| `tests/`             | ✅ | 230+ tests across memory, pipeline, L3, embedding, generation, ingest, reconcile, consolidate |
| `Velantrim_V8_Crystal_Sprint1.jsonl` | 📜 Spec | Full system design (63 chunks, 947KB) |
| Metadata tools       | ✅ Stable | audit_metadata.py, migration tools |

## What's Planned (Hybrid Roadmap)

- 🌀 **Fractal Memory Layer** (RFC-F1) — Recursive anchoring across time scales
- 🧬 **Epigenetic Module** (RFC-E1) — Dynamic behavior switching
- 🦠 **Immune / CRISPR Layer** (RFC-I1) — ✅ conflict-candidate detection (`find_conflicts`/`contradict`); auto-NLI classification still planned
- 🧠 **Neurogenesis-inspired Growth** — Dynamic addition of new memory nodes
- 🌐 **Mycorrhizal-style Network** — Inter-module communication and collective learning
- Full integration with Eiti ecosystem (Velantrim-Eiti-5, Eiti-Wizard)

**Current status**: full fact lifecycle runs end-to-end — ingest → classify → TruthGate → L3 graph → vector + episodic recall → reinforce / supersede / contradict / decay. Swappable backends (L3: auto→LadybugDB / mock / neo4j; embedder: auto→sbert / hashing; generator: extractive / Claude), zero-dep defaults, 230+ tests. The broader Hybrid vision (Fractal / Epigenetic / Neurogenesis RFCs) is still ahead.

## Quick Start (Unchanged)

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
pip install -r requirements.txt
python -m core.pipeline
pytest tests/
```

## ESM — Epistemic State Machine (Core)

Facts move through 8 states with biological-style transitions:

```
Observed → Hypothesized → Supported → Validated → ImmutableCore
          ↘ Contradicted → Deprecated → Collapsed
```

Future: Add epigenetic "stress response" that accelerates or protects certain states.

## ASCII Architecture Diagram 🔀

```
          🌟 Central Hippocampus-like Core (Episodic + Spatial)
               /               \
     🐝 Associative (Insect Mushroom Bodies)     🌳 Collective Network (Trees + Mycorrhiza)
          |                       |
     🦠 Immune + Epigenetic Layer (Bacteria + Plants)
          \               /
           Fractal Self-Similarity → Lifelong Learning without Forgetting
```

## Key Invariants (Hybrid Era)

| ID     | Name                        | Status                          |
|--------|-----------------------------|---------------------------------|
| I1     | Graph = Truth               | ✅ real L3 graph; single entry via TruthGate |
| I6     | RingZeroImmutable           | ✅ Enforced                     |
| NEW-F1 | Fractal Resilience          | 🔴 Planned                    |
| NEW-E1 | Epigenetic Adaptation       | 🔴 Planned                    |
| NEW-I1 | Immune Memory (CRISPR-style)| 🟡 conflict-candidate detection done; auto-NLI planned |

## Contributing

1. Read this README and the hybrid vision.
2. Check `ROADMAP.md` for current priorities.
3. New biological-inspired ideas → open an issue first.

## License

MIT — see [LICENSE](./LICENSE).

---

> **Graph = Truth** · **Memory = Physiology + Biology** · **Fractal = Resilience** · **Emergence = Life**

*This README was enhanced with hybrid biological memory architecture (human + animals + insects + plants + bacteria + fractal principles).*