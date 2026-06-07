# 🔱 Velantrim ExoCortex — Crystal

### *Verifiable, local-first, open-source memory infrastructure for trustworthy AI*

`v8.1.0` · 🧪 **513 tests** · 🎯 **99% coverage** · 🐍 **pure-stdlib runtime** · ⚖️ **AGPL-3.0** · 🔒 **local-first**

> Velantrim is **not another chatbot**. It is a **verifiable memory layer** that AI
> systems write to and read from, where **every stored fact carries its
> provenance, its epistemic state, and its source** — and where **nothing enters
> the canonical graph except through a single audited gate** (the *TruthGate*).
> It runs **locally by default**: no cloud, no telemetry, no external calls unless
> you explicitly opt in.

> 📦 **Scope of this repository.** This repo is the **verified, dependency-free open
> core**: the memory engine, provenance, GDPR machinery and biologically-inspired
> memory layers you can run *today*. It is one tier of the broader Velantrim
> ExoCortex system; some parts (a browser PWA demo, deeper research builds) live
> elsewhere. **Honesty rule:** this README documents only what is *implemented and
> tested in this repository*.

---

## 📑 Contents

- [🧭 What is this, in one minute](#-what-is-this-in-one-minute)
- [🎯 What you can build with it](#-what-you-can-build-with-it)
- [🚀 Quick start](#-quick-start)
- [🧠 Why it's different](#-why-its-different)
- [🏛️ How it works](#-how-it-works)
- [🧩 What's inside — the systems](#-whats-inside--the-systems)
- [🔬 Deep dives](#-deep-dives)
- [🔌 Integrations (MCP, async, scaling)](#-integrations)
- [🗺️ Roadmap](#-roadmap)
- [📚 Documentation & license](#-documentation)

---

## 🧭 What is this, in one minute

Modern AI is **confidently wrong**. It blends what the user *said*, what was
*observed*, what was *inferred*, and what the model *hallucinated* into one
undifferentiated stream — with no way to ask *"where did this come from, and how
sure are we?"*

**Velantrim Crystal is the layer you put underneath an AI system so its memory can
be trusted.** Instead of an opaque vector blob, memory is a **graph of verifiable
facts**: every fact knows its source, its confidence, and its epistemic state;
nothing becomes "truth" without passing an audited gate; the system can forget
gracefully, defend itself against hallucinations, and answer with a **receipt you
can replay**. All of it runs on your machine with **zero mandatory dependencies**.

> 🔑 In one line: **a memory engine for AI that you — and a regulator — can audit.**

---

## 🎯 What you can build with it

| | Use case | What Velantrim gives you |
|---|---|---|
| 🤖 | **Trustworthy agent memory** | Long-term memory an agent can't quietly hallucinate into — every fact gated, sourced, and epistemically typed |
| 🔎 | **Verifiable RAG / receipts** | Answers sealed into tamper-evident **receipts** that replay back to their exact sources (detects later edits/erasure/contradiction) |
| ⚖️ | **GDPR-ready AI memory** | Physical erasure + tombstones, processing restriction, Art. 30 record-of-processing, encryption at rest, audit log, PII redaction |
| 🔐 | **Local-first knowledge base** | An on-disk canon that survives restarts with **no cloud and no telemetry** — your data never leaves the device |
| 🔌 | **Drop-in MCP memory server** | A pure-stdlib **Model Context Protocol** server for Claude Desktop, Cursor, any MCP client |
| 🧬 | **Biological-memory research** | A working, tested platform for immune defence, fractal anchoring, neurogenesis, concept emergence, volition & analogy |

**Where it runs:** a laptop, a Raspberry Pi, a server, or CI — it's pure Python
standard library by default. Heavier backends (LadybugDB graph, Redis queue,
neural embeddings, an LLM answerer) are **optional add-ons**, never requirements.

---

## 🚀 Quick start

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
pip install .                          # stdlib-only runtime; installs the `velantrim` CLI
python -m core.pipeline                # runs the end-to-end demo, fully local
pytest                                 # 513 passing, 99% coverage  (pip install -e '.[dev]')
```

After install the `velantrim` CLI is on your PATH:

```bash
velantrim ingest "Water boils at 100C at sea level"
velantrim ask    "how does water behave"
# Dependency-free, on-disk canon that survives restarts:
VELANTRIM_L3_BACKEND=sqlite VELANTRIM_L3_PATH=./data/canon.db velantrim ask "..."
```

🔒 No data leaves your machine. See **[DEMO.md](./DEMO.md)** for a full walkthrough
of the *ingest → evidence → trace → answer* chain.

---

## 🧠 Why it's different

Four principles, enforced in code (not just documented):

- **📊 Graph = Truth** — one canonical knowledge graph is the single source of
  truth, and the **only** way in is through the TruthGate.
- **🔗 Provenance for every fact** — each fact records its `source`, its
  `source_status` (user-reported / observed / derived / external / LLM-output),
  and a full trace chain.
- **🎓 Epistemic honesty** — facts move through an **8-state machine**
  (Observed → … → Validated → ImmutableCore, or → Contradicted → Collapsed), so
  the system distinguishes *"verified"* from *"someone claimed this"*. A feeling
  is real *as a feeling* but never becomes a fact about the world.
- **🏠 Local-first & private by design** — stdlib-only defaults, everything on your
  machine. See **[PRIVACY.md](./PRIVACY.md)** and **[GDPR.md](./GDPR.md)**.

> 🇪🇺 **Public-benefit framing.** Crystal is built as **open European
> infrastructure for accountable AI**: privacy-respecting, auditable, and operable
> without sending personal data to third-party clouds — directly supporting GDPR
> data minimisation, purpose limitation, rectification and erasure.

---

## 🏛️ How it works

Every query flows through one auditable path — **trace first, validate, then
answer; never the other way around:**

```
Query ─▶ Retrieve (vector + graph recall) ─▶ FactsPack ─▶ Trace
      ─▶ 🛡️ Guardian (structure) ─▶ ✅ TruthGate (verification)
      ─▶ L3 canon (MERGE) ─▶ Answer (+ replayable receipt)
```

Facts live in an **Epistemic State Machine** — transitions only via
`transition_esm()`, never a raw write:

```
Observed → Hypothesized → Supported → Validated → ImmutableCore
                                    ↘ Contradicted → Deprecated → Collapsed
```

`claim_type` (world-fact / experience / emotion / opinion / …) is an **orthogonal
axis** to the ESM: this is how Velantrim refuses to launder subjective input into
objective truth.

---

## 🧩 What's inside — the systems

Crystal is a set of **small, focused modules**, all dependency-free by default and
individually tested. Grouped by what they do:

#### 🏗️ Foundation — store, retrieve, answer
| Module | Role |
|---|---|
| `core/memory.py` | L0 (in-RAM LRU) + L1 (SQLite/WAL) + the 8-state ESM |
| `core/l3_graph.py` | Swappable canonical graph: `auto`→LadybugDB / **on-disk SQLite (dependency-free)** / mock / Neo4j |
| `core/pipeline.py` | Retrieve → FactsPack → Guardian → TruthGate → L3 → Answer; episodic recall |
| `core/embedding.py` | Swappable embedder: `auto`→sentence-transformers / dependency-free hashing |
| `core/generation.py` | Swappable answerer: extractive (local default) / Claude (opt-in) |
| `core/ingest.py` | Utterance → claim-type classification → gate → L3 |

#### 🛡️ Trust & truth
| Module | Role |
|---|---|
| `core/trace.py` · `core/provenance.py` | Provenance chain + tamper-evident **replayable answer receipts** |
| `core/reconcile.py` | Truth maintenance: reinforce / supersede / contradict / find-conflicts |
| `core/contradiction.py` | Deterministic contradiction classifier (negation / antonym / numeric) |
| `core/immune.py` | 🦠 **Immune / CRISPR Guard** — blocks known hallucination/harmful patterns |
| `core/consolidate.py` · `core/adaptation.py` | FSRS-style decay + adaptive TruthGate threshold |

#### ⚖️ Privacy & GDPR
| Module | Role |
|---|---|
| `core/erasure.py` | Art. 17 physical erasure across L0/L1/L3 + content-free tombstone |
| `core/compliance.py` | Art. 18 processing restriction + Art. 30 record-of-processing |
| `core/crypto.py` | Art. 32 opt-in encryption at rest (Fernet/AES or stdlib HMAC) |
| `core/audit.py` | Tamper-evident hash-chained audit log (optional HMAC signing) |
| `core/pii.py` | PII detection & redaction at ingest (email/phone/card/IPv4/IBAN) |

#### 🧬 Living memory (biologically-inspired, all implemented & tested)
| Module | Role |
|---|---|
| `core/fractal.py` | 🪟 **Fractal Memory** — multi-scale anchoring; CORE anchors resist forgetting |
| `core/neurogenesis.py` | 🌱 **Neurogenesis** — plasticity, pattern separation, lifelong capacity |
| `core/concept.py` | 💡 **Concept Emergence** — ProtoConcepts from Hebbian co-activation |
| `core/volition.py` | ✍️ **Memory Volition** — the system writes & rehearses its own memory |
| `core/velum.py` | 🕸️ **Velum L1.5** — synaptic pre-graph of entity co-occurrence |
| `core/analogy.py` | 🎨 **Analogy Graph + CREATIVE mode** — metaphors & semantic bridges |

#### 🔌 Ops & integration
| Module | Role |
|---|---|
| `core/queue.py` | Self-healing L3 re-merge outbox: `auto`→Redis (shared) / SQLite (default) |
| `core/aio.py` | Async entry points for asyncio / FastAPI / MCP |
| `core/mcp_server.py` | Dependency-free read-only **MCP** server |
| `core/observe.py` · `core/metrics.py` | Memory observability report + in-process counters |
| `core/cli.py` | The full `velantrim` command-line surface |

> ✅ **Current status:** the full fact lifecycle runs end-to-end — ingest →
> classify → TruthGate → L3 graph → vector + episodic recall → reinforce /
> supersede / contradict / decay — with swappable backends and zero-dependency
> defaults. **513 passing tests, 99% coverage** ([TEST_REPORT.md](./TEST_REPORT.md)).

---

## 🔬 Deep dives

### 🦠 Immune / CRISPR Memory Guard (RFC0072)

Inspired by bacterial CRISPR immunity, the guard keeps a **persistent, adaptive
record of known threat patterns** (hallucination signatures, harmful or
previously-refuted claims) and screens every incoming claim *before* it can reach
the canon. **Truth-first and non-destructive by default**: a claim that merely
contradicts the canon is flagged (`QUARANTINE`) and linked, not silently
overwritten — only an explicitly recorded threat is blocked.

```bash
velantrim immune-block "the earth is flat" --type hallucination
velantrim immune-check "as everyone knows, the earth is flat"   # → {"verdict": "BLOCK"}
velantrim ingest      "as everyone knows, the earth is flat"    # → blocked (Immune)
velantrim immune-report
```
Opt-in escalations: `VELANTRIM_IMMUNE_STRICT=1` blocks any contradiction;
`VELANTRIM_IMMUNE_LEARN=1` records each blocked claim as a new spacer. Every
record/forget is written to the tamper-evident audit log.

### 🪟 Fractal Memory Layer (RFC0070)

Lifelong learning **without catastrophic forgetting**. Facts are anchored across
self-similar scales — `SHORT → MEDIUM → LONG → CORE` — with fractal capacities
(`base, base/2, base/4, base/8`), so the deep scales are scarce and hold only the
strongest knowledge. SleepCycle lengthens the decay half-life by scale, and
**CORE anchors are exempt from decay entirely** — important memory stops drifting.

```bash
velantrim fractal-reanchor    # recompute scales over the canon
velantrim fractal-report
velantrim fractal-anchors --scale CORE
```
A fact's scale is *earned*: significance plus repeated reinforcement graduate it
toward CORE. The layer is inert until `reanchor()` runs.

### 🌱 Neurogenesis Dynamic Growth (RFC0073)

Modelled on adult hippocampal neurogenesis. Every fact has a **plasticity** that
is high when young and matures to a stable floor.
- **Pattern separation** — a new fact that is vectorally close but *not* a
  contradiction is kept distinct via a `SEPARATED_FROM` edge (opt-in,
  `VELANTRIM_NEURO_SEPARATION=1`).
- **Growth & capacity** — `neuro-report` shows young/mature counts, plasticity,
  and capacity headroom; `neuro-prune-candidates` lists reclaimable facts
  (advisory; CORE anchors are never candidates).

### 💡 Concept Emergence (RFC0066)

*"Cells that fire together, wire together."* Facts recalled together get
`CO_OCCURRED` edges — the Hebbian substrate. Concept emergence clusters them
(deterministic union-find) into **ProtoConcepts**, materialised as `CONCEPT`
nodes with `MEMBER_OF` links. Computed from the live graph, idempotent, **0 tokens
/ no LLM**, and never touches fact truth.

```bash
velantrim concepts            # concepts emerging now (read-only)
velantrim concepts-emerge     # materialise them as CONCEPT nodes
velantrim concepts-for <fact_id>
```

### ✍️ Memory Volition (RFC0065)

*Memory = Agency.* The canon can act on its own memory — without bypassing truth:
- **Voluntary writes** — `write_voluntary()` authors a fact through the **same
  Guardian → TruthGate path** (it earns its place or is blocked), tagged
  `metadata.volition`.
- **Rehearsal** — the system ranks the canon by salience and **rehearses** its
  most salient memories (refreshing their decay clock) *without* fabricating
  evidence (confidence untouched).

```bash
velantrim volition-write "A self-authored claim"
velantrim volition-focus
velantrim volition-cycle
```

### 🕸️ L1.5 Velum — the synaptic pre-graph (RFC0016)

Between the episode buffer and the canon sits **Velum**, a lightweight in-memory
layer that notices *which entities keep appearing together* and strengthens a
synaptic edge between them (the analogue of LTP). It emits a hint when a pair
co-occurs enough; weak edges decay; a `_degree_cache` gives O(1) connectivity.
**Strictly a hint layer — never a source of facts.**

```bash
velantrim velum-report
velantrim velum-neighbors <entity> --min-weight 0.3
```

### 🎨 Creative intelligence — Analogy Graph & Semantic Bridges (RFC0067)

Velantrim can map **metaphors and analogies** and build **semantic bridges**
between distant ideas — dependency-free and deterministic (no LLM, no Redis):
- **Analogy Graph** — explicit `METAPHOR_OF` (directional) / `ANALOGOUS_TO`
  (symmetric) edges. *Associations, never facts* — so Graph = Truth is untouched.
- **Semantic Bridge Engine** — `find_bridges(a, b)` explains how two nodes connect
  (shared neighbour / shared concept / explicit edge); `analogy-suggest` proposes
  structurally-similar candidates.
- **CREATIVE mode** — an advisory `creative_temperature()` (0.6→0.85) for an LLM
  decoder, while the answer's facts stay **Validated-only**: creativity in framing,
  accuracy in substance.

```bash
velantrim analogy-link atom solar-system --kind ANALOGOUS_TO --weight 0.8
velantrim analogy-bridges atom solar-system
velantrim analogy-suggest atom
```

---

## 🔌 Integrations

### 🤝 MCP server (read-only)

A **dependency-free MCP server** (pure stdlib, no SDK) lets agents — Claude
Desktop, Cursor, any MCP client — query the verifiable memory over stdio:

```bash
python -m core.mcp_server          # JSON-RPC 2.0 over stdio
```
```json
{ "mcpServers": { "velantrim": { "command": "python", "args": ["-m", "core.mcp_server"] } } }
```

It exposes **read-only** tools only — `search`, `memory_report`, `get_fact`,
`fact_history`, `find_conflicts`, `verify_receipt` — so an agent can read and
*verify* memory but cannot mutate the canon. Capability-gated write access behind
the TruthGate is on the roadmap.

### ⚡ Async embedding

```python
from core.aio import aingest, arun
await aingest("Water boils at 100C at sea level")
result = await arun("how does water behave")
```

### 📈 Scaling the re-merge queue

The self-healing L3 outbox runs on a persistent, dependency-free SQLite queue by
default. To share one queue across several workers, point it at Redis:

```bash
pip install '.[redis]'
VELANTRIM_QUEUE_BACKEND=redis VELANTRIM_REDIS_URL=redis://localhost:6379/0 velantrim ask "..."
# default 'auto' uses Redis when a server answers PING, else the SQLite outbox
```

---

## 🛡️ Key invariants

| ID | Name | Status |
|---|---|---|
| I1 | Graph = Truth | ✅ real L3 graph; single entry via TruthGate |
| I6 | Ring Zero Immutable | ✅ enforced (`VALUES_CORE` / `RING_ZERO` cannot transition) |
| E1 | Epigenetic Adaptation | ✅ wired into adaptive TruthGate (`core/adaptation.py`) |
| I1-prov | Provenance preserved | ✅ every fact has source + source_status + trace |

---

## 🗺️ Roadmap

Velantrim ships as **fundable, verifiable deliverables**. See
**[ROADMAP.md](./ROADMAP.md)** for the full implemented-vs-designed split.

**✅ Delivered (running & tested today)**
- Verifiable provenance & **replayable answer receipts** (`trace`, `provenance`)
- Full **GDPR data-subject operations** (`erasure`, `compliance`, `crypto`, `audit`, `pii`)
- **Local-first persistence & packaging** (dependency-free SQLite L3 backend)
- **Conflict / hallucination detection** (`contradiction` + Immune Guard)
- The complete **biological-memory suite** — fractal, neurogenesis, concept
  emergence, volition, Velum, analogy/creative mode
- **Ops**: pluggable Redis/SQLite queue, async entry points, read-only MCP server

**⬜ Next**
- 🌾 **RFC0063** — external knowledge ingestion (PDF / JSON / RDF → TruthGate)
- 🧠 **RFC0068** — NeuroCore plastic memory (feature-flagged, Phase 0 passive)
- 🩹 **Sprint-A hardening patches** (A1–A10)

---

## 📚 Documentation

- **[PRIVACY.md](./PRIVACY.md)** — what is stored, where, and what never leaves the device
- **[GDPR.md](./GDPR.md)** — article-by-article mapping of the design to GDPR
- **[docs/PERSISTENT_MEMORY.md](./docs/PERSISTENT_MEMORY.md)** — persistent vs canonical vs immutable memory
- **[SECURITY.md](./SECURITY.md)** — threat model & responsible disclosure
- **[TEST_REPORT.md](./TEST_REPORT.md)** — current, un-inflated test results
- **[ROADMAP.md](./ROADMAP.md)** — implemented vs designed, sprint by sprint
- **[HYBRID_VISION.md](./HYBRID_VISION.md)** · **[FUTURE.md](./FUTURE.md)** — the longer research arc

## 🌿 Research inspiration

The living-memory layers draw on biological memory systems — hippocampal episodic
memory & neurogenesis, insect associative learning, plant epigenetic adaptation,
and CRISPR-style immune recognition of contradictions. In Crystal these are **no
longer just metaphors: they are implemented, dependency-free, tested runtime
modules** (see the **🧬 Living memory** group and deep dives above). The deeper,
still-exploratory arc lives in
[HYBRID_VISION.md](./HYBRID_VISION.md) and [FUTURE.md](./FUTURE.md).

## 🤝 Contributing

1. Read this README and **[ROADMAP.md](./ROADMAP.md)**.
2. Open an issue before large changes.
3. Keep the **honesty invariant**: `ROADMAP.md` distinguishes *implemented* from
   *designed* — please preserve that distinction.

## ⚖️ License

**AGPL-3.0** — see **[LICENSE](./LICENSE)**. The copyleft open core keeps community
work open (no closed-source cloud re-hosting); integrations may be released under
permissive terms (Apache-2.0) where noted.

---

> **📊 Graph = Truth** · **🔗 Provenance = Trust** · **🏠 Local-first = Privacy**
