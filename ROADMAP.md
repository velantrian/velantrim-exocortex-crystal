# Velantrim ExoCortex — Roadmap

This document is the **honest truth** about what's implemented vs designed.

## ✅ Implemented (`core/`, 230+ tests)

- L0 (in-memory LRU) + L1 (SQLite, WAL) memory layers; `update_fact`
- ESM state machine with 8 states and transition validation
- Ring Zero immutability guard (I6) for `VALUES_CORE` / `RING_ZERO` fact IDs
- Claim-modality axis (`claim_type` / `source_status` / `significance`),
  orthogonal to ESM; **type-aware TruthGate** (subjective ≠ world-fact)
- Vector/semantic retrieval (cosine) over a seed corpus **+ recall from L3**
- L3 canonical graph adapter — swappable backend `auto`→**LadybugDB** / `sqlite` /
  `mock` / `neo4j`; nodes, edges, `vector_search`, persistence (`VELANTRIM_L3_PATH`)
- Dependency-free on-disk persistence (`core/l3_graph.py` `SqliteL3Graph`): the
  L3 canon survives restarts on the Python-stdlib SQLite backend (no native deps);
  it is the `auto` fallback when LadybugDB is absent, and persists the embedder
  fingerprint across restarts. Reproducible packaging: `pip install .` exposes the
  `velantrim` console script (`pyproject.toml`, PEP 440 version, explicit package surface)
- Swappable embedder (`auto`→sentence-transformers / hashing) and answer
  generator (extractive / Claude LLM)
- Ingestion (`core/ingest.py`): utterance → claim_type → gate → L3
- Truth maintenance (`core/reconcile.py`): reinforce / supersede / contradict /
  find_conflicts (immune candidate detection)
- Contradiction detection (`core/contradiction.py`): deterministic, dependency-free
  classifier labelling a candidate CONTRADICTION / REFINEMENT / RELATED via negation,
  antonym and numeric signals behind a same-subject gate (high precision); enriches
  `find_conflicts`; opt-in auto CONTRADICTS-linking at ingest
  (`VELANTRIM_AUTO_CONTRADICT`); CLI `conflicts`
- SleepCycle (`core/consolidate.py`): significance-weighted confidence decay (FSRS-style)
- Episodic linking + `recall_episode` / `recall_by_entity`
- Guardian (structural check), provenance trace (`core/trace.py`)
- Verifiable answer provenance (`core/provenance.py`): `build_receipt` seals an
  answer + query + the exact cited facts under a SHA-256 digest (optional
  HMAC via `VELANTRIM_PROVENANCE_KEY`); `verify_receipt` replays each citation
  against the canon and flags facts later erased / restricted / modified /
  contradicted; CLI `receipt` / `verify-receipt`
- GDPR Art. 17 physical erasure (`core/erasure.py`): `erase_fact` purges a fact
  across L0/L1/L3 + outbox and writes a content-free audit tombstone
  (`erasure_log`); `--cascade` erases derived facts (`DERIVED_FROM`)
- GDPR Art. 18 processing restriction + Art. 30 record-of-processing
  (`core/compliance.py`): `restrict_processing` excludes a fact from recall
  without deletion; `record_of_processing` exports an aggregate content-free
  RoPA; CLI `restrict` / `unrestrict` / `ropa`
- GDPR Art. 32 encryption at rest (`core/crypto.py`): opt-in, authenticated
  field-level encryption of claim/metadata in L1 SQLite (`VELANTRIM_ENCRYPTION_KEY`);
  Fernet/AES when `cryptography` is installed, dependency-free HMAC-SHA256 otherwise;
  off by default (runtime stays stdlib-only)
- Tamper-evident audit log (`core/audit.py`, Art. 5(2)/24/30): append-only hash
  chain of erase/restrict/unrestrict events; `verify_audit_log` detects any edit,
  deletion or reordering; optional HMAC signing (`VELANTRIM_AUDIT_KEY`); CLI
  `audit` / `audit-verify`
- PII detection & redaction (`core/pii.py`, Art. 5 data minimisation): overlap-safe
  detection of email/phone/credit-card(Luhn)/IPv4/IBAN; opt-in redaction at ingest
  (`VELANTRIM_REDACT_PII`); CLI `redact`
- Pluggable L3 re-merge queue (`core/queue.py`): the self-healing outbox behind a
  swappable backend `auto`→**Redis** (when a server answers PING) / **sqlite** /
  **redis** (`VELANTRIM_QUEUE_BACKEND`, `VELANTRIM_REDIS_URL`). The dependency-free
  persistent SQLite outbox is the default and the `auto` fallback; Redis (optional
  `pip install '.[redis]'`) lets several pipeline workers share one queue
- Async-friendly entry points (`core/aio.py`): `arun` / `aingest` / `adrain_l3_outbox`
  run the sync pipeline off the event loop via `asyncio.to_thread`, so Velantrim
  embeds in an asyncio service / FastAPI / MCP server without blocking. (Interface
  is async today; the underlying stdlib I/O is still synchronous — a full async
  rewrite of the stores remains future work.)
- RFC0072 Immune / CRISPR Memory Guard (`core/immune.py`): persistent, adaptive
  threat memory ("spacers") that screens claims BEFORE the canon and blocks known
  hallucination / harmful / refuted patterns; high-precision contradiction check
  reuses `core/contradiction.py`. Non-destructive by default (contradiction →
  advisory QUARANTINE, link-don't-overwrite); opt-in hard blocking
  (`VELANTRIM_IMMUNE_STRICT`) and adaptive learning (`VELANTRIM_IMMUNE_LEARN`).
  Accountable via the audit log; CLI `immune-block` / `immune-allow` /
  `immune-check` / `immune-report`
- RFC0070 Fractal Memory Layer (`core/fractal.py`): recursive anchoring across
  self-similar scales (SHORT → MEDIUM → LONG → CORE) with fractal capacities
  (base, base/2, base/4, base/8). `reanchor()` sorts canonical facts by a
  deterministic `anchor_strength` (significance · reinforcement · confidence) into
  the scales; SleepCycle then protects deeper anchors from decay (CORE is exempt
  → anti-catastrophic-forgetting). Inert until reanchored; CLI `fractal-reanchor`
  / `fractal-report` / `fractal-anchors`

## ✅ Implemented (metadata tooling, not runtime)

- `audit_metadata.py`, `fill_dependencies.py`, `check_rfc_duplicates.py`
- `velantrim_migrate_v3_1.py` — production migration tool with rollback
- Metadata hardening: Cyrillic → ASCII (39→0), layers 55→1 null, deps 54→27

## 📋 Designed in spec, NOT yet coded

| RFC | Component | Sprint target |
|-----|-----------|---------------|
| RFC0016 | Velum L1.5 synaptic pre-graph, `_degree_cache` | S2 |
| RFC0066 | Concept Emergence, ProtoConcept, Hebbian learning | S3 |
| RFC0065 | Memory Volition, `write_voluntary()`, VolitionWorker | S3 |
| RFC0067 v2.0 | Analogy Graph, Semantic Bridge Engine, Adaptive Decoder | S4 |
| RFC0068 | NeuroCore (plastic memory, Phase 0 passive tracker) | S5+ |
| — | Full async/await rewrite of the stores (async entry points already shipped) | S3+ |
| — | Sprint A patches A1–A10 (documented, not wired) | S3 |

> ✅ **Now done** (were in this table): RFC0017 FSRS-style decay → `core/consolidate.py`;
> RFC0063 Ingestion → `core/ingest.py`; L3 graph adapter + LadybugDB backend
> (`core/l3_graph.py`, Kuzu frozen Oct'25 → LadybugDB successor, Neo4j optional);
> Redis + fallback queue → `core/queue.py`; async entry points → `core/aio.py`;
> RFC0072 Immune / CRISPR Memory Guard → `core/immune.py` and RFC0070 Fractal
> Memory Layer → `core/fractal.py` (issue #7, Hybrid Vision).

## 📊 Invariant enforcement status

- **I6** (RingZeroImmutable): ✅ enforced in `memory.py` + test
- **I1** (Graph = Truth): ✅ real L3 graph (auto→LadybugDB / mock / neo4j); single entry via TruthGate
- **I2**: 🟡 partial
- **I50, I50-b, I66, I70, I-K3, I68**: ❌ components not yet coded
- **I38–I65**: ❌ pending Sprint 3+

## Sprint plan

- **S1**: Honesty — fix README, ESM bugs, add tests/CI/LICENSE
- **S2**: ✅ vector retrieval + L3 recall, swappable L3/embedder/generator
  backends (LadybugDB default, Neo4j optional), FSRS-style decay, ingestion,
  truth maintenance, pluggable Redis/SQLite re-merge queue (`core/queue.py`),
  async entry points (`core/aio.py`)
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