# 🗺️ Velantrim ExoCortex — Roadmap

> **Honesty rule.** This document is the honest split between what is **implemented
> and tested** and what is **designed but not yet coded**. The README documents
> only the former; this file tracks both.

**Status:** 🧪 **624 tests passing** · 🎯 **99% coverage** (gate 95%) · 🐍 stdlib-only
runtime · every delivered item below ships with tests and a CLI surface.

---

## ✅ Delivered (running & tested today)

### 🏗️ Foundation — store, retrieve, answer
- **Memory layers** (`core/memory.py`): L0 (in-memory LRU) + L1 (SQLite/WAL);
  `update_fact`; the 8-state ESM with validated transitions; Ring Zero
  immutability (I6) for `VALUES_CORE` / `RING_ZERO`.
- **Claim-modality axis** (`claim_type` / `source_status` / `significance`),
  orthogonal to ESM → a **type-aware TruthGate** (subjective ≠ world-fact).
- **L3 canonical graph** (`core/l3_graph.py`): swappable backend
  `auto`→**LadybugDB** / **on-disk SQLite (dependency-free)** / `mock` / `neo4j`;
  nodes, edges, `vector_search`, persistence (`VELANTRIM_L3_PATH`). The SQLite
  backend keeps the canon across restarts with **no native deps** and is the
  `auto` fallback.
- **Retrieval** (cosine vector + recall from L3); **swappable embedder**
  (`auto`→sentence-transformers / dependency-free hashing) and **answerer**
  (extractive default / Claude LLM opt-in).
- **Ingestion** (`core/ingest.py`): utterance → claim_type → gate → L3.
- **External knowledge ingestion** (`core/knowledge.py`, RFC0063): bulk-import
  `.txt` / `.md` / `.json` / `.jsonl` / `.csv` knowledge files through the SAME
  TruthGate; imported facts carry `source_status = EXTERNAL` + the source file as
  provenance. Stdlib-only parsers (PDF/YAML/RDF left to optional adapters); CLI `learn`.
- **Import sessions & dry-run review** (`core/imports.py`, WP2): preview a corpus
  (`learn --dry-run`) — predict accept/reinforce/block/conflict through the SAME
  validators with **zero writes**; real imports get a session id so a whole batch
  can be reviewed and restricted/erased together; CLI `import-session` /
  `session-restrict` / `session-erase`.
- **Packaging**: `pip install .` exposes the `velantrim` console script
  (`pyproject.toml`, PEP 440 version, explicit package surface).

### 🛡️ Trust & truth
- **Truth maintenance** (`core/reconcile.py`): reinforce / supersede / contradict
  / find_conflicts.
- **Contradiction detection** (`core/contradiction.py`): deterministic,
  dependency-free classifier (negation / antonym / numeric behind a same-subject
  gate) → CONTRADICTION / REFINEMENT / RELATED; opt-in auto-linking
  (`VELANTRIM_AUTO_CONTRADICT`); CLI `conflicts`.
- **Verifiable provenance** (`core/trace.py`, `core/provenance.py`): `build_receipt`
  seals answer + query + cited facts under SHA-256 (optional HMAC); `verify_receipt`
  replays each citation and flags facts later erased / restricted / modified /
  contradicted; CLI `receipt` / `verify-receipt`.
- **Evidence span store + Receipt v2** (`core/evidence.py`, WP1 baseline): attach
  source-span provenance to a fact (`source_uri`/kind, chunk, span offsets, source
  & claim SHA-256); content-light. Receipt v2 seals attached evidence into citations
  and replays it (detects removed/drifted source links). `learn` auto-attaches the
  source file as evidence; CLI `evidence [--verify]`. Richer auto span-offset
  extraction (PDF/Markdown) remains future work.
- **SleepCycle** (`core/consolidate.py`): significance-weighted FSRS-style decay.
- **Immune / CRISPR Guard** (`core/immune.py`, RFC0072): adaptive threat memory
  that blocks known hallucination/harmful/refuted patterns before the canon;
  truth-first (contradiction → advisory QUARANTINE); opt-in `IMMUNE_STRICT` /
  `IMMUNE_LEARN`; audited; CLI `immune-*`.

### ⚖️ Privacy & GDPR
- **Art. 17 erasure** (`core/erasure.py`): `erase_fact` purges across L0/L1/L3 +
  outbox, writes a content-free tombstone; `--cascade`.
- **Art. 18 + Art. 30** (`core/compliance.py`): processing restriction +
  record-of-processing export; CLI `restrict` / `unrestrict` / `ropa`.
- **Art. 32 encryption at rest** (`core/crypto.py`): opt-in field-level
  encryption (Fernet/AES or stdlib HMAC-SHA256); off by default.
- **Tamper-evident audit log** (`core/audit.py`, Art. 5(2)/24/30): append-only
  hash chain; `verify_audit_log`; optional HMAC signing; CLI `audit` / `audit-verify`.
- **PII redaction** (`core/pii.py`, Art. 5): email/phone/card(Luhn)/IPv4/IBAN;
  opt-in at ingest; CLI `redact`.

### 🧬 Living memory — biologically-inspired (all implemented & tested)
- **Fractal Memory** (`core/fractal.py`, RFC0070): multi-scale anchoring
  SHORT→MEDIUM→LONG→CORE with fractal capacities; CORE anchors are exempt from
  decay → anti-catastrophic-forgetting; CLI `fractal-*`.
- **Epigenetic Adaptation** (`core/adaptation.py`, RFC0071): adaptive TruthGate
  threshold — stress raises rigor, health relaxes it.
- **Immune / CRISPR Guard** (RFC0072) — see Trust & truth.
- **Neurogenesis** (`core/neurogenesis.py`, RFC0073): plasticity/maturation,
  pattern separation (`SEPARATED_FROM`), growth & capacity reporting, prune
  candidates; CLI `neuro-*`.
- **Concept Emergence** (`core/concept.py`, RFC0066): ProtoConcepts from Hebbian
  co-activation → CONCEPT nodes with MEMBER_OF; 0 tokens, no LLM; CLI `concepts*`.
- **Memory Volition** (`core/volition.py`, RFC0065): `write_voluntary()` through
  the gates + salience-ranked rehearsal that slows forgetting without fabricating
  evidence; CLI `volition-*`.
- **Velum L1.5** (`core/velum.py`, RFC0016): in-memory synaptic pre-graph of
  entity co-occurrence (LTP-style) + `_degree_cache`; a pure hint layer, never a
  source of facts; CLI `velum-*`.
- **Analogy Graph + Semantic Bridges + CREATIVE mode** (`core/analogy.py`,
  RFC0067 v2.0): METAPHOR_OF / ANALOGOUS_TO edges (associations, never facts),
  deterministic bridges, advisory creative temperature with facts kept
  Validated-only; CLI `analogy-*`.
- **NeuroCore — Phase 0 passive tracker** (`core/neurocore.py`, RFC0068): logs the
  norm of the would-be plastic weight delta (ΔW) when surprise > θ to
  `neurocore_delta_log`. Off by default (`VELANTRIM_NEUROCORE`); the model is never
  touched and the L3 graph is never written (invariant **I68**); CLI
  `neurocore-report`. Active adaptation (Phase 1+) remains future work.

### 🩹 Sprint-A hardening (production safety)
- **A9 — LLM call safety** (`core/generation.py`): bounded retry with exponential
  backoff on transient API failures (429 / timeout / overload), no retry for
  non-transient errors, output ceiling, graceful degradation to extractive.
- **A1 / A2 / A3** already satisfied by the architecture (idempotent ingest,
  parameterised SQLite, overlap-safe PII); **A8** in its erasure form (Art. 17
  hard delete + tombstones). Full per-patch triage:
  **[docs/SPRINT_A_STATUS.md](./docs/SPRINT_A_STATUS.md)**.

### 🔌 Ops & integration
- **Pluggable re-merge queue** (`core/queue.py`): self-healing outbox,
  `auto`→Redis (shared, optional `[redis]`) / SQLite (dependency-free default).
- **Async entry points** (`core/aio.py`): `arun` / `aingest` / `adrain_l3_outbox`
  for asyncio / FastAPI / MCP (interface async today; stores still sync).
- **Read-only MCP server** (`core/mcp_server.py`): pure stdlib, JSON-RPC 2.0 over
  stdio; read/verify only, cannot mutate the canon.
- **Observability** (`core/observe.py`, `core/metrics.py`) + full CLI (`core/cli.py`).
- **Evaluation harness** (`core/eval.py`): retrieval (hit@k / MRR), trace
  completeness, metadata completeness, **source-span coverage** and
  **contradiction precision/recall**, plus receipt-replay survival over a
  deterministic fixture; CLI `eval`. Extensions tracked in
  **[docs/EVAL.md](./docs/EVAL.md)**.

---

## ⬜ Next (designed, not yet coded)

| RFC / item | What it adds | Target |
|---|---|---|
| 🌾 **RFC0063+** | Additional external-ingestion adapters: PDF / YAML / Wikidata RDF (core text/JSON/JSONL/CSV already shipped in `core/knowledge.py`) | S5+ |
| 🧠 **RFC0068 Phase 1+** | **NeuroCore** active model adaptation + consolidation (Phase 0 passive tracker already shipped in `core/neurocore.py`) | S6+ |
| 🩹 **A6 / A7 / A10** | Sprint-A patches for the optional Phase‑1 stack (Neo4j locks, async EventBus backpressure, aioredis pool) — N/A to the dependency-free core; wired only if those components are activated. See **[docs/SPRINT_A_STATUS.md](./docs/SPRINT_A_STATUS.md)** | S6+ |
| ⚙️ async core | Full async/await rewrite of the stores (async *entry points* already shipped) | S3+ |

---

## 🗺️ Sprint history

- **S1** ✅ — Honesty pass: README, ESM fixes, tests / CI / LICENSE.
- **S2** ✅ — Vector retrieval + L3 recall, swappable backends, FSRS decay,
  ingestion, truth maintenance, Redis/SQLite queue, async entry points.
- **S3** ✅ — RFC0066 Concept Emergence, RFC0065 Memory Volition, RFC0016 Velum
  L1.5. *(remaining: A1–A10 wiring)*
- **S4** ✅ — RFC0067 Analogy Graph + Semantic Bridge + CREATIVE mode; RFC0063
  external knowledge ingestion (`core/knowledge.py`).
- **S5** ✅ — RFC0068 NeuroCore Phase 0 passive tracker (`core/neurocore.py`).
- **S6+** ⬜ — RFC0068 Phase 1+ (active NeuroCore adaptation + consolidation);
  extra ingestion adapters (PDF / YAML / RDF); A1–A10 wiring.

---

## 🧬 Hybrid Biological Memory Vision — ✅ complete

The strategic biological line (issue #7) is **fully delivered** — all four RFCs
are implemented, dependency-free, and tested:

| RFC | Component | Status |
|---|---|---|
| RFC0070 | Fractal Memory Layer | ✅ `core/fractal.py` |
| RFC0071 | Epigenetic Adaptation | ✅ `core/adaptation.py` |
| RFC0072 | Immune / CRISPR Memory Guard | ✅ `core/immune.py` |
| RFC0073 | Neurogenesis Dynamic Growth | ✅ `core/neurogenesis.py` |

See **[HYBRID_VISION.md](./HYBRID_VISION.md)** for the architecture and biological
sources (human / dolphin / insect / plant / bacteria / fractal brain).

---

## 📊 Invariant enforcement

- **I1** (Graph = Truth): ✅ real L3 graph; single entry via TruthGate.
- **I6** (Ring Zero Immutable): ✅ enforced in `core/memory.py` + test.
- **E1 / RFC0071** (Epigenetic Adaptation): ✅ wired into the adaptive TruthGate.
- **I2** and deeper spec invariants (I38–I65, I66/I70/I-K3/I68): 🟡/❌ partial or
  pending — tracked against the remaining RFCs above.

---

## 🛠️ Metadata tooling (not part of the runtime)

- `audit_metadata.py`, `fill_dependencies.py`, `check_rfc_duplicates.py`
- `velantrim_migrate_v3_1.py` — production migration tool with rollback
- Metadata hardening: Cyrillic → ASCII (39→0), layers 55→1 null, deps 54→27
