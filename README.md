# 🔱 Velantrim ExoCortex — Crystal

**Verifiable, local-first, open-source memory infrastructure for trustworthy AI systems.**

**Version**: v8.1.0 · 2026

> Velantrim is not another chatbot. It is a **verifiable memory layer** that AI
> systems can write to and read from, where **every stored fact carries its
> provenance, its epistemic state, and its source** — and where nothing enters
> the canonical graph except through a single audited gate (the *TruthGate*).
> It runs **locally by default**: no cloud, no telemetry, no external calls
> unless you explicitly opt in.

> **Scope of this repository.** This repo is the **verified, dependency-free open
> core** (v8.1.0 — 384 passing tests, 99% coverage): the memory layer, provenance,
> and GDPR machinery you can run today. It is one component of the broader
> Velantrim ExoCortex system; extended parts (a browser PWA demo, MCP integration,
> and further research modules) are in active development and described in the
> project roadmap. In keeping with the honesty principle below, this README
> documents only what is implemented and tested **in this repository**.

---

## Why this exists

LLM-based systems are confidently wrong. They blend what a user *said*, what was
*observed*, what was *inferred*, and what the model *hallucinated* into a single
undifferentiated stream — and there is no way to ask *"where did this come from,
and how sure are we?"*

Velantrim addresses this at the infrastructure level. It treats memory as a
**graph of verifiable facts** rather than an opaque vector blob:

- **Graph = Truth** — one canonical knowledge graph is the single source of
  truth; the only way in is through the TruthGate.
- **Provenance for every fact** — each fact records its `source`,
  `source_status` (user-reported / observed / derived / external / LLM-output),
  and a full trace chain (`core/trace.py`).
- **Epistemic honesty** — facts move through an 8-state machine
  (Observed → … → Validated → ImmutableCore, or → Contradicted → Collapsed),
  so the system can distinguish *"verified"* from *"someone claimed this"*.
- **Local-first & private by design** — default backends are stdlib-only and
  run entirely on your machine. See [PRIVACY.md](./PRIVACY.md) and
  [GDPR.md](./GDPR.md).

## European public benefit

Velantrim is built as **open European infrastructure** for AI that has to be
*accountable*: privacy-respecting, auditable, and operable without sending
personal data to third-party clouds. The design directly supports
GDPR principles — data minimisation, purpose limitation, the right to
rectification (via fact supersession) and erasure (physical `erase_fact` with a
content-free audit tombstone), and full auditability of provenance. See
[GDPR.md](./GDPR.md) for the article-by-article mapping.

## What's in this repo (current, honest state)

| Path                  | Status | Description                                                                 |
|-----------------------|--------|-----------------------------------------------------------------------------|
| `core/memory.py`      | ✅ | L0 (in-memory LRU) + L1 (SQLite, WAL) + ESM (8 states) + `update_fact`      |
| `core/pipeline.py`    | ✅ | Retrieve (vector + L3 recall) → FactsPack → Guardian → TruthGate → L3 → Answer; episodic linking + `recall_episode`/`recall_by_entity` |
| `core/l3_graph.py`    | ✅ | Swappable L3 canonical graph: `auto`→LadybugDB / **`sqlite` (on-disk, dependency-free)** / `mock` / `neo4j`; nodes, edges, `vector_search`, persistence |
| `core/embedding.py`   | ✅ | Swappable embedder: `auto`→sentence-transformers / dependency-free hashing  |
| `core/generation.py`  | ✅ | Swappable answer generator: extractive (default, local) / Claude LLM (opt-in) |
| `core/ingest.py`      | ✅ | Utterance → claim_type classification → gate → L3                           |
| `core/reconcile.py`   | ✅ | Truth maintenance: reinforce / supersede / contradict / find_conflicts      |
| `core/contradiction.py`| ✅ | Deterministic contradiction classifier (negation / antonym / numeric); high-precision immune signal |
| `core/consolidate.py` | ✅ | SleepCycle: significance-weighted confidence decay (FSRS-style)             |
| `core/trace.py`       | ✅ | Provenance chain for every fact                                             |
| `core/provenance.py`  | ✅ | Tamper-evident, replayable answer receipts — re-verify any answer against the canon (detects later erase/restrict/modify/contradict) |
| `core/erasure.py`     | ✅ | GDPR Art. 17 physical erasure across L0/L1/L3 + content-free tombstone; cascade to derived facts |
| `core/compliance.py`  | ✅ | GDPR Art. 18 processing restriction + Art. 30 record-of-processing export |
| `core/crypto.py`      | ✅ | GDPR Art. 32 opt-in encryption at rest for claim/metadata (Fernet/AES or stdlib HMAC) |
| `core/audit.py`       | ✅ | Tamper-evident, hash-chained audit log of erase/restrict events (optional HMAC signing) |
| `core/pii.py`         | ✅ | PII detection & redaction at ingest — email/phone/card(Luhn)/IPv4/IBAN (GDPR Art. 5) |
| `core/adaptation.py`  | ✅ | Adaptive TruthGate threshold (RFC0071): stress ↑ → stricter; healthy → relaxes |
| `core/observe.py`     | ✅ | Memory observability report over the L3 canonical graph                     |
| `core/metrics.py`     | ✅ | Lightweight in-process counters (query / ingest / gate)                     |
| `core/cli.py`         | ✅ | CLI: `ingest`/`ask`/`history`/`report`/`erase`/`erasures`/`restrict`/`unrestrict`/`ropa`/`audit`/`audit-verify`/`redact`/`receipt`/`verify-receipt`/`conflicts` |
| `tests/`              | ✅ | **384 passing**, 12 skipped, **99% coverage** (gate: 95%) — see [TEST_REPORT.md](./TEST_REPORT.md) |
| `docs/Velantrim_V8_Crystal_Sprint1.jsonl` | 📜 Spec | Full system design (63 chunks) |

**Current status**: the full fact lifecycle runs end-to-end — ingest → classify
→ TruthGate → L3 graph → vector + episodic recall → reinforce / supersede /
contradict / decay. Swappable backends, zero-dependency defaults.

## Quick start

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
pip install .                          # stdlib-only runtime; installs the `velantrim` CLI
python -m core.pipeline                # runs the end-to-end demo, fully local
pytest                                 # 384 passing, 99% coverage  (pip install -e '.[dev]')
```

After install the CLI is on your PATH:

```bash
velantrim ingest "Water boils at 100C at sea level"
velantrim ask    "how does water behave"
# Dependency-free, on-disk canon that survives restarts:
VELANTRIM_L3_BACKEND=sqlite VELANTRIM_L3_PATH=./data/canon.db velantrim ask "..."
```

No data leaves your machine. See [DEMO.md](./DEMO.md) for a walkthrough of the
ingest → evidence → trace → answer chain.

## MCP integration (read-only)

Velantrim ships a **dependency-free MCP server** (Model Context Protocol) so
agents — Claude Desktop, Cursor, any MCP client — can query the verifiable
memory over the standard stdio transport. It is **pure stdlib**: no SDK, nothing
extra to install.

```bash
python -m core.mcp_server          # speaks JSON-RPC 2.0 over stdio
```

Wire it into Claude Desktop (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "velantrim": { "command": "python", "args": ["-m", "core.mcp_server"] }
  }
}
```

The server exposes **read-only** tools only — `search`, `memory_report`,
`get_fact`, `fact_history`, `find_conflicts`, `verify_receipt` — so an agent can
read and *verify* memory but cannot mutate the canon. Following the
capability-based design, write/curate tools (ingest / validate / supersede /
erase) are **not registered** at this `reader` capability: a tool a role cannot
use is never exposed, so a model cannot call it by accident. Capability-gated
write access **behind the TruthGate** is the next step on the roadmap.

## ESM — Epistemic State Machine (core)

Facts move through 8 states with validated transitions:

```
Observed → Hypothesized → Supported → Validated → ImmutableCore
                                    ↘ Contradicted → Deprecated → Collapsed
```

`claim_type` (world-fact / experience / emotion / opinion / …) is an
orthogonal axis to ESM: a feeling is *real as a feeling* and can become
`Validated`, but it never becomes a `WORLD_FACT`. This is how Velantrim avoids
laundering subjective input into objective truth.

## Key invariants

| ID     | Name                  | Status                                                       |
|--------|-----------------------|-------------------------------------------------------------|
| I1     | Graph = Truth         | ✅ real L3 graph; single entry via TruthGate                 |
| I6     | Ring Zero Immutable   | ✅ enforced (`VALUES_CORE` / `RING_ZERO` cannot transition)  |
| E1     | Epigenetic Adaptation | ✅ wired into adaptive TruthGate (`core/adaptation.py`)       |
| I1-prov| Provenance preserved  | ✅ every fact has source + source_status + trace             |

## Roadmap

Three to five fundable, verifiable deliverables (see [ROADMAP.md](./ROADMAP.md)
for the full breakdown and honest implemented-vs-designed split):

1. **Verifiable provenance & audit trail** — any answer can be replayed back to
   its sources: `core/provenance.py` seals each answer into a tamper-evident,
   optionally HMAC-signed **receipt** and re-verifies it against the canon,
   detecting facts later erased / restricted / modified / contradicted.
   *(implemented: `core/trace.py`, `core/provenance.py`)*
2. **GDPR data-subject operations** — rectification, **physical erasure**
   (cascade + content-free tombstone), **processing restriction**, an
   **Art. 30 record-of-processing** export, **opt-in encryption at rest**
   (Art. 32), a **tamper-evident audit log** (Art. 5(2)/24), and **PII redaction
   at ingest** (Art. 5 data minimisation). *(implemented: `core/erasure.py`,
   `core/compliance.py`, `core/crypto.py`, `core/audit.py`, `core/pii.py`)*
3. **Local-first persistence & packaging** — a **dependency-free, on-disk SQLite
   L3 backend** (`VELANTRIM_L3_BACKEND=sqlite`, the `auto` fallback when LadybugDB
   is absent) keeps the canon across restarts with zero external deps; `pip install .`
   ships the `velantrim` console script. Embedded LadybugDB remains the scale
   option. *(implemented: `core/l3_graph.py` `SqliteL3Graph`, `pyproject.toml`)*
4. **Conflict / hallucination detection** — a deterministic, dependency-free
   contradiction classifier (`core/contradiction.py`) labels each `find_conflicts`
   candidate as CONTRADICTION / REFINEMENT / RELATED via negation, antonym and
   numeric signals; opt-in auto-linking of detected contradictions at ingest
   (`VELANTRIM_AUTO_CONTRADICT`). *(implemented; NLI-model upgrade is future work)*
5. **Documentation, security audit & CI** — sustained test coverage, security
   review (see [SECURITY.md](./SECURITY.md)), and reproducible CI.

## Documentation

- [PRIVACY.md](./PRIVACY.md) — what data is stored, where, and what never leaves the device
- [PERSISTENT_MEMORY.md](./docs/PERSISTENT_MEMORY.md) — persistent vs canonical vs immutable memory model
- [GDPR.md](./GDPR.md) — article-by-article mapping of the design to GDPR
- [SECURITY.md](./SECURITY.md) — threat model and responsible disclosure
- [TEST_REPORT.md](./TEST_REPORT.md) — current, un-inflated test results
- [ROADMAP.md](./ROADMAP.md) — implemented vs. designed, sprint by sprint

## Research inspiration

The longer-term design draws on biological memory systems — hippocampal
episodic memory, insect associative learning (mushroom bodies), plant
epigenetic adaptation, and CRISPR-style immune recognition of contradictions.
These are *research directions and metaphors*, not current runtime features;
see [HYBRID_VISION.md](./HYBRID_VISION.md) and [FUTURE.md](./FUTURE.md). The
shippable infrastructure described above does not depend on any of them.

## Contributing

1. Read this README and [ROADMAP.md](./ROADMAP.md).
2. Open an issue before large changes.
3. Keep the honesty invariant: `ROADMAP.md` distinguishes *implemented* from
   *designed* — please preserve that distinction.

## License

**AGPL-3.0** — see [LICENSE](./LICENSE). The copyleft open core keeps community
work open (no closed-source cloud re-hosting); integrations may be released under
permissive terms (Apache-2.0) where noted.

---

> **Graph = Truth** · **Provenance = Trust** · **Local-first = Privacy**
