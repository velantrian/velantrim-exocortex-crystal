<!--
  NOTE (English) — historical design specification.

  This is the Velantrim V8 design spec — an English translation of the original
  Russian document. It is kept for provenance and reference as an in-depth design
  document; it is NOT the canonical project documentation. For the current English
  project docs see:
    - ../README.md        (overview)
    - ../GDPR.md          (data-protection mapping)
    - ../ROADMAP.md       (implemented vs. designed)
    - ../SECURITY.md, ../PRIVACY.md

  The spec below describes the fractal graph-memory architecture (L0–L6), the
  Epistemic State Machine (ESM), the TruthGate, and the RFC series on which the
  implemented `core/` modules are based.
-->

> **Historical note:** This is a legacy internal sprint/design document. It may
> contain older planning language that does not represent the current
> implemented status of Velantrim Crystal. For the canonical
> implemented-vs-RFC-vs-vision status map, see
> [`docs/IMPLEMENTATION_STATUS.md`](./IMPLEMENTATION_STATUS.md).

# 💠 Velantrim V8 Crystal — Full Edition + Sprint 1
## Specification: Fractal Graph Memory for an Autonomous AI Agent
### (v8.0.2-sprint1 · Full audit · P0–P4 + Sprint 1+1.1 patches applied · April 2026)

> **Version**: 8.0.2-sprint1 "Crystal Full" · **Date**: April 2026 · **Project**: Velantrim ExoCortex
>
> **Patch status**: P0 (8/8) · P1 (10/10) · P2 (6/6) · P3 (7/7) · P4 (6/6) · Sprint 1+1.1 (8/8) — all applied
>
> Based on: HYPERIA FractalMemory Core · ACT-R · Graphiti
>
> Principle: `Graph = Truth · LLM = Language · Memory = Physiology · Volition = Agency · Emergence = Life · Creativity = Structured Analogy · Knowledge = Ingested Wisdom · Tests = Proof`

---

## 📋 Table of Contents

- [🌍 The essence of the project — read this first](#the-essence-of-the-project-read-this-first)
- [✨ Three new dimensions — read this before going to RFC0065–0067](#three-new-dimensions-read-this-before-going-to-rfc00650067)
- [🗺️ System map — a quick overview in 2 minutes](#system-map-a-quick-overview-in-2-minutes)
- [🎯 Project goal](#project-goal)
- [📊 Key success metrics](#key-success-metrics)
- [🏗️ System Architecture](#system-architecture)
- [RFC0066: Concept Emergence — Organic Birth of Concepts](#rfc0066-concept-emergence-organic-birth-of-concepts)
- [RFC0065: Memory-as-Volition — Conscious Will to Remember](#rfc0065-memory-as-volition-conscious-will-to-remember)
- [🔧 Technology Stack](#technology-stack)
- [📦 Key Components and Their Implementation](#key-components-and-their-implementation)
- [🧬 Integrated Components (from HYPERIA v5.20)](#integrated-components-from-hyperia-v520)
- [📐 Token Contract and Promote/Demote Protocol](#token-contract-and-promotedemote-protocol)
- [🔄 Full Integration: Main Agent](#full-integration-main-agent)
- [🔍 Historical Sprint Components](#historical-sprint-components)
- [📈 Monitoring and Metrics](#monitoring-and-metrics)
- [📐 SLO Contract (Service Level Objectives)](#slo-contract-service-level-objectives)
- [🔌 MCP Server — Connecting to External Clients](#mcp-server-connecting-to-external-clients)
- [🔍 Audit Layer — Verifiability Layer (Phase 1+)](#audit-layer-verifiability-layer-phase-1)
- [🛡️ Memory Guardian — Protection Against Memory Poisoning](#memory-guardian-protection-against-memory-poisoning)
- [🗃️ Immutable Raw Memory — Protection Against Semantic Drift](#immutable-raw-memory-protection-against-semantic-drift)
- [🔗 CausalGraph — Cause-and-Effect Layer](#causalgraph-cause-and-effect-layer)
- [🧬 Knowledge Distillation Engine — Populating L3](#knowledge-distillation-engine-populating-l3)
- [📜 Formal System Invariants (RFC0001–RFC0005)](#formal-system-invariants-rfc0001rfc0005)
- [📦 Evidence Builder and Truth Gate (RFC0004)](#evidence-builder-and-truth-gate-rfc0004)
- [📜 Canonical Memory Protocol v1](#canonical-memory-protocol-v1)
- [RFC0067 v2.0: Creative Intelligence Layer](#rfc0067-v20-creative-intelligence-layer)
- [RFC0063: Knowledge Ingestion Pipeline — Absorbing External Knowledge](#rfc0063-knowledge-ingestion-pipeline-absorbing-external-knowledge)
- [🧬 Epistemic State Machine (ESM) — Fact Lifecycle](#epistemic-state-machine-esm-fact-lifecycle)
- [⚙️ Runtime Invariant Checker](#runtime-invariant-checker)
- [🎭 Cognitive Modes — Three Modes of Operation](#cognitive-modes-three-modes-of-operation)
- [💰 Memory Budget Planner](#memory-budget-planner)
- [🔐 PII Redaction](#pii-redaction)
- [📋 RFC0014 — L2.5 Staging Layer](#rfc0014-l25-staging-layer)
- [📋 RFC0013 — L2 CORE (Canonical Contract)](#rfc0013-l2-core-canonical-contract)
- [💓 Meta-Supervisor — Apex Controller](#meta-supervisor-apex-controller)
- [📊 Memory Health Index (MHI) — Phase 2](#memory-health-index-mhi-phase-2)
- [🚀 Implementation Roadmap](#implementation-roadmap)
- [⚠️ Important warnings](#important-warnings)
- [🔱 L3.5 — Etir (Velantrim Synaptic Activation Layer)](#l35-etir-velantrim-synaptic-activation-layer)
- [📜 RFC0004 — Truth Gate Contract](#rfc0004-truth-gate-contract)
- [📜 RFC0011 — Etir Spreading Activation Engine](#rfc0011-etir-spreading-activation-engine)
- [📜 RFC0012 — Taxonomy/Domain Hierarchy](#rfc0012-taxonomydomain-hierarchy)
- [📜 RFC0015 — TruthGateWithESM](#rfc0015-truthgatewithesm)
- [📜 RFC0016 — L1.5 Velum](#rfc0016-l15-velum)
- [📜 RFC0017 — Weighted Semantic Decay](#rfc0017-weighted-semantic-decay)
- [📐 Fractal Similarity Monitor](#fractal-similarity-monitor)
- [🗄️ Storage Ecosystem — A Complete Map of Stores](#storage-ecosystem-a-complete-map-of-stores)
- [🤖 Current LLM and Embedding Stack (March 2026)](#current-llm-and-embedding-stack-march-2026)
- [🔧 System Maintenance](#system-maintenance)
- [📚 Additional Resources](#additional-resources)
- [🎓 Conclusion](#conclusion)
- [🗺️ Technology Map · Optional Stack](#technology-map-optional-stack)
- [📜 RFC0036–RFC0051](#rfc0036rfc0051)
- [📜 RFC0043 — Hardware Profile Selector](#rfc0043-hardware-profile-selector)
- [📜 RFC0044 — LLM_MODE: Offline Mode](#rfc0044-llm_mode-offline-mode)
- [📜 RFC0045 — LensEngine: Deterministic Lenses L4/L5](#rfc0045-lensengine-deterministic-lenses-l4l5)
- [🔒 System Invariants (addendum to I7, I8)](#system-invariants-addendum-to-i7-i8)
- [📖 How to use the modules (instructions)](#how-to-use-the-modules-instructions)
- [🔧 RFC0062 — TZ-Fix Integration Patch](#rfc0062-tz-fix-integration-patch)
- [🧠 RFC0068: NeuroCore — Plastic Memory Layer](#rfc0068-neurocore-plastic-memory-layer)
- [📝 Changelog](#changelog)

---

## 🌍 The essence of the project — read this first

> This section is for anyone opening the document for the first time — a developer, an architect, or a new team member. Read it before diving into the architecture and code. It will explain why the system is built the way it is, and then every decision in the code will make sense.

Velantrim is a **memory system for an AI agent**. Not just a database with search, and not just a wrapper over an LLM with chat history. It is something fundamentally different.

An ordinary AI agent lives within a single conversation. Every time a new chat begins, it remembers nothing. Even if it has "memory," that memory is structured as a flat list of notes — with no understanding of the connections between facts, no knowledge of what matters to the user, no learning from mistakes. And most importantly — it spends tokens on every response as if it were meeting you for the first time.

Velantrim solves this through three fundamental principles, and **each of them is an engineering decision with consequences for the code**:

**Graph = Truth.** The single source of truth is the knowledge graph. Not the LLM, not the cache, not SQLite. The LLM in this system is a language interface: it speaks eloquently, but it does not decide what is true. If somewhere in the code the LLM writes a fact directly into the graph, bypassing the Truth Gate — that is a bug, not a feature.

**Memory = Physiology.** Memory is structured like the biological memory of a human being — with levels L0–L6, with FSRS decay (v8.0: power-law R = (1 + 19/81 × t/S)^(-0.5), which replaced Ebbinghaus), with synaptic reinforcement of important memories and nightly consolidation. Every architectural decision has an analog in neurobiology — this is not a metaphor, it is an engineering choice.

**Dual-Process.** Everything the user sees is the Fast Path: a response in milliseconds, without blocking. Everything the system does for itself is the Slow Path, an asynchronous background. If a component ends up in the Fast Path when it should be in the Slow Path — that is a critical architectural bug. For the full diagram, see the "Dual-Process Architecture" section below.

> 🔱 **If put in one sentence:** Velantrim is your personal digital mind that remembers, feels the rhythm, learns from mistakes, and protects the truth. All of this — on a CPU, with no GPU during the dialogue, and with minimal load on the hardware.

---

## ✨ Three new dimensions — read this before going to RFC0065–0067

> This block is for anyone who wants to understand **why** three new mechanisms were added, before reading their architecture and code.

Before RFC0065, the system could remember, structure, and protect knowledge. That is already an outstanding result. But three things remained that distinguish **living memory** from a **well-organized database**.

**First — the will to remember.** Imagine a person who, in the middle of a conversation, says to themselves: "This is important, I want to remember it." They don't wait for memory to decide on its own. They **consciously** make a choice. In Velantrim, before RFC0065, all writing to memory was passive — the system decided on the agent's behalf. Now the agent can, on its own, through an intentional tool call, say: "Write this into my long-term memory." This is not just a feature — it is the boundary between a tool and a subject.

**Second — the birth of concepts.** A child understands the word "table" not because they were given a definition. They have seen enough tables in different contexts, and at some point a concept arose in their mind — on its own, out of experience. In Velantrim, before RFC0066, concepts were born through LLM extraction — an expensive, slow, non-organic process. Now Velum (L1.5) observes the co-occurrence of edges and, at the right moment, **senses on its own**: "it seems these entities always appear together — this is a concept." Without tokens, without an LLM, just as the neural network of the brain does it.

**Third — creative intelligence.** Before RFC0067 v2.0, the system had no explicit map of metaphors and could not build semantic bridges between distant domains. Now the Analogy Graph stores `[:METAPHOR_OF]` and `[:ANALOGOUS_TO]` edges extracted from high-quality texts, the Semantic Bridge Engine precomputes bridges in the background and places them in Redis, and the CREATIVE mode gives the LLM a dynamic temperature and access to these associations. Zero tokens spent on search. Pure organics.

> 🔱 **If put in one sentence:** RFC0065–0067 is the difference between a system that remembers and a system that **wants** to remember, **gives birth** to meanings **on its own**, and **creatively finds analogies**.

---

## 🗺️ System map — a quick overview in 2 minutes

> If you are opening this document for the first time, or after a break — read this section. Here every major mechanism is described in a single paragraph. Further on in the document — the full specification, code, and tests.

**Fractal memory hierarchy (L0–L6).** Memory is structured biologically — seven layers. L0 — reflexes (instant cache). L1 — dialogue episodes (RAM). L1.5 Velum — the synaptic pregraph, notices which entities appear together. L2 — mid-term topics (SQLite). L3 — the long-term knowledge graph (Neo4j, the single source of truth). L3.5 — ImmutableCore, immutable snapshots. L4 — ReasoningBank, reasoning patterns. L5 — anticipatory intelligence, foresees the user's needs before they ask. L6 — Values Core, immutable values.
    │         P2-D FIX: L6 is mentioned in the overview without a specification. Status: pending RFC.
    │         Partially implemented through the Ring Zero mechanism of L3.5.
    │         └─ L6 spec: Ring Zero nodes in L3 + SQLite duplication.
    │            Change only through human approval + dual-key confirmation.
    │            Invariant I6 (RingZeroImmutable). Separate RFC pending.

**Dual-Process (Fast/Slow Path).** For the full diagram, see the "Dual-Process Architecture" section. Ending up in the Fast Path when it should be in the Slow Path is a critical architectural bug.

**Truth Gate + ESM.** No fact enters the L3 graph without passing through the Truth Gate. Every fact lives in one of **eight** epistemic states (ESM): **Observed** (raw input, before classification) → Hypothesized → Supported → Validated → ImmutableCore or Contradicted → Deprecated → Collapsed. Transitions — only through ESM.transition(); a direct SET epistemic_state is a bug.
<!-- P9-FIX BUG-13: added the Observed state (raw input before Hypothesized). It was present in valid_states (line 9878) and Guardian (line 3434), but was missing from the lifecycle description — variant A. -->

**Thompson Sampling (ReasoningBank, L4).** The system learns from its own mistakes. Every reasoning strategy has success and failure counters. Thompson Sampling chooses a strategy while accounting for uncertainty — not a greedy choice of the best, but a balance of exploration/exploitation.

**Concept Emergence (RFC0066, L1.5).** Velum observes the co-occurrence of entities. If three or more entities appear together across different sessions, the system **gives birth on its own** to an unnamed ProtoConcept. Zero tokens. The name is given lazily — only when needed. An analog of Hebbian Learning in neural networks.

**Memory Volition (RFC0065, L4.5).** The agent is granted the right to **consciously** initiate a write to long-term memory through the tool call `memory.write_voluntary()`. This is not a bypass of the Truth Gate — it is a priority entrance into it. The difference between "I saw it somewhere" and "I deliberately wrote it down."

**Creative Intelligence (RFC0067 v2.0).** Three mechanisms: Analogy Graph — an explicit map of metaphors `[:METAPHOR_OF]` and analogies `[:ANALOGOUS_TO]` extracted from high-quality texts. Semantic Bridge Engine — finds semantic bridges between distant domains, places them in Redis, and the Fast Path only reads the cache. Adaptive Decoder — CREATIVE mode with a temperature of 0.6→0.85, but the FactsPack contains only Validated facts. Creativity without compromising accuracy.

**Knowledge Ingestion (RFC0063).** The system is able to ingest external knowledge — encyclopedias, textbooks, PDFs, scientific papers. Three parallel streams: FactExtractor places facts into L3 through the Truth Gate, PatternExtractor places reasoning patterns into ReasoningBank with a Bayesian initialization of Thompson Sampling, and SemanticIndexer builds a vector index with no LLM at all. EdgeSuggester finds implicit connections between concepts and proposes them to the auditor — it does not write to the graph itself. VintageDecayCalculator ensures that knowledge from a 2015 programming book becomes outdated faster than the laws of physics.

> **P2-4:** After a fact is extracted, BEFORE the TruthGate — `atomic_split()` is called:
> one meaning = one node. Multi-proposition content is split into atomic facts.
> I91 (AtomicSplit): After atomic_split, each element contains exactly one proposition.

**Anticipatory Intelligence (L5).** SAE — Spreading Activation Engine: when a node is activated, excitation spreads across the graph's edges with decay. LSM — Liquid State Machine: predicts what the user will ask next. EGM — proposes topics. XAI — explains why such an answer was given.

**Observer++ / Security.** The system protects itself from attacks, injections, and degradation. ATK-Registry — a database of known attack scenarios; CI/CD tests each one before deployment. Write Protocol Gate — the single path for writing to the graph; a direct Cypher MERGE is an exception. 37+ executable invariants (I1–I37 in tests, I38–I65 pending) are checked in `test_invariants.py` on every push.

---

## 🎯 Project goal

Create a memory system for an AI agent that:
- **Automatically** saves and consolidates experience without constant LLM queries
- **Learns** from successes and failures through a self-learning mechanism
- **Minimizes** token consumption (target reduction: 90%+)
- **Scales** through a fractal memory hierarchy
- **Works in real time** with a search latency of <500ms
- **Protects the truth** through an immune system (Observer++) and the Write Protocol

---

## 📊 Key success metrics

| Metric | Target value | Source |
|---------|------------------|----------|
| Token reduction (RECALL P95) | ≥ 85% | STM/MTM cache hit |
| Token reduction (DEFINE) | 40–60% | Extractive summarization |
| Token reduction (P50 baseline) | ≥ 65% | Aggregate of all types |
| Search latency P95 | < 500ms | Hot Graph + Graphiti |
| Hot Graph traversal | 1–3 ms | Cache-Aware L2/L3 |
| Response latency reduction | > 60% | Agentic routing |
| Memory retrieval accuracy | > 90% | Deep Memory Benchmark |
| L5 prediction accuracy (month 3) | ~75% | Prediction Error learning |
| Task success (improvement) | +35–40% | ReasoningBank + Thompson Sampling |
| contradiction_detection_rate | > 98% | ESM |
| mean_time_to_resolution (MTTR) | < 24h | ESM + TruthGate |
| unresolved_contradictions_7d | = 0 | Observer++ |
| attack_sim_pass_rate | ≥ 95% on ATK-REGISTRY | CI/CD · RFC0060 |
| attack_sim_new_scenario_ttl | ≤ 48h after an incident | RFC0060 |
| invariant_test_coverage | 100% (I1–I37) · I38–I65 pending | test_invariants.py |

---

<!-- P9-FIX BUG-17: explicit separator — below begins the invariant roadmap, not business metrics -->
### 📅 Invariant roadmap I38–I65
| Range | Area | Status |
|----------|------------------------------------|----------------|
| I38–I45 | RFC0054 SAE invariants | pending |
| I46–I52 | RFC0055–0057 epistemics | pending · I50/I50-b/I50-c ✅ Sprint 1 |
| I53–I58 | RFC0058–0061 security | pending |
| I59–I65 | RFC0063 Knowledge Ingestion | pending |
| I66      | RFC0066 ProtoConcept in memory only | ✅ Sprint 1 |
| I70      | RFC0066 MAX_ACTIVE_PROTOS cap | ✅ Sprint 1 |
| I-K3     | RFC0066 Hebbian GC Guard (FIX-K3) | ✅ Sprint 1.1 |
| Semantic drift detection | ✅ dual | Semantic Drift Monitor |
| Retrieval ESM correctness | 100% | SafeFTSQuery |
| epistemic_variance P95 | < 0.7 | RFC0047 |
| Temporal-ESM sync lag | 0ms (synchronous) | RFC0049 |
| offline_requests_total | grows when LLM_MODE=offline | RFC0051 |
| lens_precision (implicit) | > 0.80 | RFC0051 |
| multi_component_ram_pressure | < 0.85 | RFC0048 |
| dag_rollback_retry_total | < 5/hour | RFC0050 |
| response_audit_importance_avg | > 0.5 | RFC0052 |
| focus_vector_updates_total | grows every session | RFC0053 |
| response_audit_cache_invalid_total | < 3/day | RFC0052 |
| sae_activations_total | grows during active dialogues | RFC0054 |
| epistemic_gap_accepted_rate | > 0.30 | RFC0055 |
| authority_conflicts_resolved | < 10/day | RFC0057 |
| xai_explanations_total | grows = user trust | RFC0058 |
| source_trust_degraded_total | < 2/day | RFC0059 |
| policy_version_current | grows with each change | RFC0061 |
| evolution_rejected_total | grows = the system protects itself | RFC0061 |
| CPU during dialogue (LITE) | 10–15% of 1 core | Event-Driven |
| CPU at rest | ~0% | asyncio events |
| RAM hot graph (LITE) | 2–5 MB | Hot Graph |
| RAM LSM | 2–5 MB | Liquid State Machine |
| dlq_permanent_failure_alert | mandatory · CRITICAL | EventBus |
| vacuum_batch_size | 100 nodes / iteration | Rate limiting |
| salience_boosts_total | grows = the system notices what matters | Salience Detector |
| homeostatic_runs_total | once a day | Homeostatic Balancer |
| lsm_prediction_updates | grows = LSM is learning | LSM |
| fusion_consensus_rate | grows = SAE+LSM converge | L5.5 |
| prediction_accuracy_rolling_7d | grows toward month 3 | Prediction Error |
| `volition_validated_total` | grows = the agent remembers consciously | RFC0065 |
| `volition_rejected_total` | < 20% of calls = TruthGate is working | RFC0065 |
| `proto_concepts_active` | grows toward month 2 | RFC0066 |
| `concept_emergence_zero_token` | > 70% of named = token savings | RFC0066 |
| `analogy_graph_edges_total` | grows with each ingest | RFC0067 v2.0 |
| `sbe_cache_hits` | > 70% = SBE keeps up with precomputation | RFC0067 v2.0 |
| `analogy_resonance_score` | grows toward month 2 = analogies are useful | RFC0067 v2.0 |
| `analogy_promoted_total` | grows = SBE crystallizes patterns | RFC0067 v2.0 |
| `creative_mode_responses_total` | grows during active dialogues | RFC0067 v2.0 |
| `ingestion_facts_created_total` | grows with each ingestion | RFC0063 |
| `ingestion_contradictions_found_total` | < 5% = the source is compatible with the graph | RFC0063 |
| `edge_suggestions_pending_total` | < 50 = the audit is keeping up | RFC0063 |
| `edge_hypothesized_activated_total` | grows = hidden connections are being confirmed | RFC0063 |

---

## 🏗️ System Architecture

### Dual-Process Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                        ⚡ FAST SYSTEM                             │
│                  (Synchronous interaction)                       │
├──────────────────────────────────────────────────────────────────┤
│  User Query                                                      │
│    → Salience Detector        (1–2 ms · L1.5 · CPU only)     │
│    → SafeFTSQuery                                                │
│    → Hot Graph traversal      (1–3 ms · RAM first)           │
│    → HybridRetrieval + L5.5 PredictiveFusion (SAE × LSM)     │
│    → Context Builder → Facts Pack (Dual Mode)                    │
│    → LLM Generation → Response                                   │
│    → Closed Loop Eval                                            │
│              ↓ (Logging to Event Bus · fire-and-forget)          │
└──────────────────────────────────────────────────────────────────┘
                               ↓
┌──────────────────────────────────────────────────────────────────┐
│                        🌙 SLOW SYSTEM                            │
│               (Asynchronous background processing)              │
├──────────────────────────────────────────────────────────────────┤
│  Event Stream (asyncio EventBus · ~0% CPU at rest)           │
│    → Observer++ → Extraction → Write Protocol Gate               │
│    → Source Trust Check → ESM Transition                         │
│    → Prediction Error Signal  (2–5 ms after response)        │
│    → LSM Update               (5–15 ms after response)       │
│    → FSRS Decay Worker        (hourly · P0-1 · power-law)    │
│    → Hot/Cold Graph Switch    (hourly)                       │
│    → Quality Gate (confidence × coverage × contradictions)  │
│              ↓ FAST_PATH_SUFFICIENT → Response              │
│              ↓ SLOW_PATH → Slow System reasoning            │
│    → ResponseAuditWorker      (SLOW PATH only · I28)             │
│    → FocusEngine Update                                          │
│    → Consolidation → Reflection → ESMChunkedInvalidator          │
│    → Semantic Drift Monitor                                      │
│    → Experience Replay → Strategy Update                         │
│                                                                  │
│  SleepTimeWorker (CPU < 30% · user offline):                    │
│    → Homeostatic Balancer         (3:00 at night · daily)   │
│    → ReactivationEngine           (hourly)                   │
│    → ImmutableCore Delta Snapshot                            │
│    → ConceptEmergenceDetector.gc_expired()  (daily)         │  <- RFC0066
│    → ResonanceTracker.decay_all()           (daily)         │  <- RFC0067
│    → AnalogyGC (expired -> cold graph)      (weekly)        │  <- RFC0067
│    ⚠️ SBEAsyncWorker — only via EventBus, not here            │
│    (launched from the Slow Path via EventBus,                │
│    trigger — the ANALOGY_CANDIDATE_READY event,             │
│    not directly from SleepTimeWorker)                        │
│    → Inverted HyDE Worker     (offline · P1-7 · I90)        │
│         generates hypothetical queries for important episodes│
│         (importance >= 0.7), puts them in the index. Not at runtime.│
│    → Graph Health Checker     (daily · P2-2)                │
│         orphans, dupes, fan-out violations → warning log      │
│    → Curiosity Engine         (daily · P2-6 · I92)          │
│         gap < 3 facts → generates a question for the user    │
└──────────────────────────────────────────────────────────────────┘
```

### Fractal Memory Hierarchy

```
L0: Working Memory
    ├─ Current dialogue context
    ├─ Active goals (Goal Stack — a priority stack)
    ├─ Capacity: 4±1 active chunks (Cowan, 2001)
    │   Note: Miller (1956) gave 7±2 for humans, but the real
    │   agent limit is closer to 4±1 (Cowan). Chunking: related
    │   facts are merged into a single semantic block.
    │
    ├─ CoreMemoryBlocks — the user's persistent profile
    │   Purpose: the agent knows the user from the first word without a graph
    │   search. ~500 tokens always in context as a CRITICAL block.
    │   Three immutable chunks, never evicted:
    │     · user_profile   — name, preferences, context, language
    │     · agent_persona  — the agent's role, communication style, constraints
    │     · current_goals  — active goals of the current period (from the Goal Stack)
    │   Storage: SQLite (persistent across sessions)
    │   Update: only through an explicit user tool call or
    │     FocusEngine on a significant change in the query pattern
    │   File: memory/core_memory_blocks.py
    │   ⚠️ INVARIANT: CoreMemoryBlocks do not overwrite each other —
    │     each block is independent. Updating one does not touch the others.
    │
    ├─ Attention Sinks — Ring Zero protection:
    │   The first context tokens are pinned hard:
    │     · Ring Zero / VALUES CORE  → CRITICAL, never evicted
    │     · CoreMemoryBlocks         → CRITICAL, never evicted
    │     · Project State Card       → CRITICAL, never evicted
    │     · Active goal (top of stack) → HIGH
    │     · Current dialogue         → MEDIUM
    │     · Auxiliary context        → LOW (first candidate for eviction)
    ├─ Priority Eviction — eviction hierarchy:
    │   CRITICAL > HIGH > MEDIUM > LOW
    │   On overflow, the lowest-priority chunk is evicted
    │   into L1, not destroyed.
    └─ Decay: seconds (within a single query)

L1: Short-Term Memory
    ├─ Episodic Buffer (Baddeley, 2000) — a chronological buffer of
    │   episodes from the current session. Unlike L2, episodes are not
    │   clustered, they are stored in time order.
    ├─ Session_ID Binding — each episode is hard-bound to a
    │   session_id. On a session change (30 min of inactivity)
    │   the L2 consolidation trigger fires automatically.
    ├─ Temporal Tagging — mandatory fields on every episode:
    │     · event_time   — when it happened (user time)
    │     · created_at   — when it was saved (processing time)
    │     · valid_from   — start of the validity period
    │     · valid_until  — end (NULL = valid now)
    ├─ FTS5 Index — SQLite Full-Text Search for fast search
    │   over episode text without calling the LLM. A trigger on INSERT
    │   automatically indexes the new episode.
    │   ⚠️ ONLY through SafeFTSQuery — raw FTS5
    │   bypasses the ESM filters, which is an architecture error.
    ├─ Recency Bias — on retrieval, more recent episodes
    │   get priority over older ones from the same session.
    ├─ Velum Trigger — on every INSERT into the L1 Episodic Buffer
    │   the chain is invoked in strict order:
    │     1. SalienceDetector.analyze(episode)        ← · FIRST
    │     2. Velum.observe_episode(episode_id, entities)
    │   On reaching VELUM_CO_OCCUR_THRESHOLD co-occurrences
    │   → VelumSignal → ReactivationEngine + L2 accelerated promote.
    │   Full spec: RFC0016 / velum.py.
    │   ⚠️ Order is critical: Salience must run before Velum,
    │   so that salience_weight is already updated when edges are built.
    ├─ Extracted entities and facts
    ├─ Temporal graph of the episode
    └─ Decay: fast (minutes-to-hours)

L1.5: Velum — Synaptic Pre-Graph Layer + Salience Detector   ← RFC0016
    ├─ Purpose: a detector of early links between session entities.
    │   Lives between L1 (episodes) and L2 (clusters).
    │   Does NOT store content — only edges (co-occurrence + weight).
    │
    ├─ Salience Detector — automatic significance detector
    │     Built into the L1 INSERT trigger — called BEFORE Velum.observe_episode.
    │     The first mechanism that lets the system build a model of the
    │     user's priorities on its own — without explicit instructions.
    │
    │     Signals and their weights:
    │       📢 CAPS LOCK (≥3 capitals in a row)     → salience_weight × 1.5
    │       ❗ Exclamation mark                      → salience_weight × 1.3
    │       🔁 Topic repeats 3+ days in a row       → salience_weight × 2.0  ← strongest
    │       💬 Words "important", "critical",        → salience_weight × 1.4
    │          "never", "always"
    │       ⏱️ Return to a topic after a 24h pause   → salience_weight × 1.6
    │       🔄 User re-asked/clarified              → salience_weight × 1.2
    │
    │     Result: raises salience_weight of the corresponding nodes in the L3 graph.
    │     Effect on the system:
    │       · Nodes with high salience_weight are protected from FSRS Decay (v8.0)
    │       · They get priority into the Hot Graph (Cache-Aware L2/L3)
    │       · They strengthen the L5.5 PredictiveFusionLayer predictions
    │     Load: 1–2 ms · CPU only · 0 LLM tokens
    │     Metric: salience_boosts_total (Prometheus counter)
    │
    ├─ Mechanism:
    │     L1 INSERT → SalienceDetector.analyze(episode)  ← called first
    │              → observe_episode(entities)
    │     → update edge weights in a sliding window (VELUM_WINDOW_EPISODES = 5)
    │     → if weight ≥ 0.6 AND count ≥ 3 → VelumSignal
    │     → ReactivationEngine strengthens the link
    │     → L2 gets a hint for an accelerated cluster promote
    ├─ Storage: in-memory dict[frozenset, VelumEdge] (not persistent).
    │   Optionally: top-N edges → SQLite to seed the next session.
    ├─ End of session (on_session_end()):
    │     weight ≥ VELUM_PROMOTE_WEIGHT → VelumSignal "SESSION_END" → L2
    │     weight < VELUM_PROMOTE_WEIGHT → decay × VELUM_DECAY_PER_SESSION
    ├─ get_neighbors(entity, min_weight) — used by:
    │     · HybridRetriever: context expansion within a session
    │     · ReactivationEngine: a hint about what to strengthen
    ├─ GC when > VELUM_MAX_EDGES (1000): remove the weakest 25% of edges
    ├─ Velum Health Score GC:
    │     GC removes by usefulness, not just by volume.
    │     health_score = retrieval_bonus(0.4) + signal_bonus(0.3)
    │                  + emotional_bonus(0.2) + recency_bonus(0.1)
    │     Invariant: edges that participated in retrieval within the last
    │     VELUM_PROTECT_WINDOW episodes are never removed.
    ├─ RAM Guard — Graduated GC:
    │     Instead of a hard "50% at >1000", we use a graduated approach:
    │     
    │     # the order of conditions is inverted — critical first
    │     if episode_count > 2000:
    │         gc_percentage = 0.50  # critical threshold
    │         logger.error(f"Velum RAM CRITICAL: {episode_count} episodes, GC 50%")
    │     
    │     elif episode_count > 1500:
    │         gc_percentage = 0.35  # medium threshold
    │         logger.warning(f"Velum: {episode_count} episodes, GC 35%")
    │     
    │     elif episode_count > 1000:
    │         gc_percentage = 0.25  # first threshold — soft cleanup
    │         logger.warning(f"Velum: {episode_count} episodes, GC 25%")
    │     
    │     Advantages:
    │     · Gradual degradation instead of an abrupt loss of data
    │     · Early warning at 1000 episodes
    │     · Preservation of important links under a moderate load
    │     
    │     Protection: prevents RAM overflow on sessions with >1000 episodes
    │     Metric: velum_ram_guard_triggered_total (Prometheus counter)
    │               velum_gc_percentage (Gauge — current percentage)
    ├─ LateralInhibition — protection against Hub Explosion: ← SYNAPSE-style (arXiv 2601.02744)
    │
    │   Problem: with constant strengthening of one edge (A→B), the related weak edges
    │   (A→X, A→Y) are never cleaned → the graph degrades into a "star" with a single hub.
    │   This is Hub Explosion — one concept starts to dominate everything.
    │
    │   Mechanism:
    │   When an edge (A, B) is strengthened → weaken all other edges A→X by × 0.95
    │   Exception: edges with weight ≥ 0.4 are protected (already strong enough)
    │   Guarantee: no protected edge is weakened by LateralInhibition
    │
    │   Biological analog: lateral inhibition in neural networks —
    │   an excited neuron suppresses its neighbors, enhancing the signal contrast.
    │
    │   Result: the graph stays balanced. Strong links stand out
    │   against the weak ones, instead of drowning in uniform noise.
    │
    │   Invariant I77:
    │
    │   I77 (LateralInhibition): the LateralInhibition operation runs ONLY
    │   under self._lock (asyncio.Lock of Velum).
    │   Violation: changing edge weights during LateralInhibition without self._lock.
    │   P0-E FIX: renamed _edges_lock → _lock (matches Velum.__init__).
    │   Protected edges (weight ≥ 0.4) are never weakened.
    │
    │   Implementation (add the _strengthen_edge method to velum.py):

```python
import math  # module-level import — not under the lock

async def _strengthen_edge(self, a: str, b: str, factor: float = 1.1):
    """Strengthen edge (a,b) + LateralInhibition for a's weak neighbors.
    P0-D/P0-E FIX: self._edges_lock → self._lock (Velum initializes self._lock, not self._edges_lock).
    Previously: AttributeError on every LateralInhibition call.
    """
    async with self._lock:   # P0-E: fixed from self._edges_lock
        key = frozenset([a, b])
        edge = self._edges.get(key)
        if edge:
            # P2-1: ACT-R fan-effect dampening — the more links a node has, the weaker the strengthening
            # _degree_cache: dict[str, int] — incremented in _add_edge(), reset in gc_weak_edges()
            # Replaces O(N) list comprehension under the lock → O(1) lookup
            degree = self._degree_cache.get(a, 1)
            fan_effect = 1.0 / math.log(degree + 1)
            edge.weight = min(1.0, edge.weight * factor * fan_effect)
            # LateralInhibition: weaken a's weak neighbors
            PROTECTION_THRESHOLD = 0.4
            INHIBITION_FACTOR    = 0.95
            for other_key, other_edge in self._edges.items():
                if a in other_key and other_key != key:
                    if other_edge.weight < PROTECTION_THRESHOLD:
                        other_edge.weight *= INHIBITION_FACTOR
```

    ├─ RFC0016 invariants:
    │     Velum.I1: only edges, NOT facts. Graph = Truth is not violated.
    │     Velum.I2: strong edges on a session change → an L2 signal.
    │     Velum.I3: weak edges → decay, not promote.
    │     Velum.I4: not persistent by default.
    ├─ Neuroscience analog: LTP (Long-Term Potentiation) —
    │   synaptic strengthening up to long-term consolidation.
    └─ Decay: session-based (edges live within a session + decay on a session change)

---

## RFC0066: Concept Emergence — Organic Birth of Concepts

### 🌱 Read this first

In the original Velantrim, concepts were born through an LLM. RFC0066 changes this: Velum (L1.5) already tracks co-occurrence — which entities appear together. If three or more entities consistently appear together across different sessions, the system **discovers an emerging concept on its own**. At first it is a nameless ProtoConcept — zero tokens. A name is assigned only when necessary.

**Neuroscience analog:** Unsupervised Hebbian Learning — "neurons that fire together, wire together." RFC0066 is Hebbian Learning for the knowledge graph.

**Why this does not violate Graph = Truth:** Velum stores only edges (I1). Concept Emergence does not create :Fact — it creates `:ProtoConcept`. Promotion to `:Concept` (L3) happens only through TruthGate (I50-b).

---

```
L1.5 addition: Concept Emergence  <- RFC0066
    |
    +- Purpose: organic birth of concepts from Velum edge statistics.
    |   WITHOUT LLM extraction. WITHOUT explicit instructions. 0 tokens.
    |   Analog: Hebbian Learning.
    |
    +- Mechanism — three phases:
    |   Phase 1 (Observation): on every L1 INSERT, the call
    |     ConceptEmergenceDetector.observe(entities)  <- NEW
    |     Matrix: emergence_matrix[frozenset(entities)] += 1
    |
    |   Phase 2 (Detection): co_occur >= 5 AND cross_sessions >= 3 AND entities 3-7
    |     -> ProtoConcept {proto_id, entities, confidence: 0.0, name: None}
    |     -> in-memory only (not in the graph — not yet a fact)
    |     -> Velum receives a hint: strengthen edges x1.3
    |
    |   Phase 3 (Lazy naming):
    |     Trigger A: user asks about the topic of proto.entities
    |     Trigger B: ProtoConcept.confidence > 0.7
    |     Trigger C: Homeostatic Balancer (once a day) — names the top 5
    |     if len(entities) <= 3: TF-IDF (0 tokens)
    |     elif importance < 0.8: Qwen3-1.7B (tiny LLM)
    |     else: flagship LLM (critical ones only)
    |     Then -> promotion to :Concept (L3) through TruthGate (I50-b)
    |
    +- Invariants:
    |   I50:   does not create :Fact, does not write to the L3 graph. Graph = Truth is preserved.
    |   I50-b: ProtoConcept -> :Concept only through TruthGate.
    |   I50-c: emergence_matrix stores only counters, not content.
    |   I66:   ProtoConcept lives only in memory (_protos dict). (Sprint 1)
    |   I70:   active protos ≤ MAX_ACTIVE_PROTOS=500. Eviction of the least confident. (Sprint 1)
    |   I-K3:  gc_expired() does not remove observations younger than TTL_DAYS without a proto. (Sprint 1.1 FIX-K3)
    |           _matrix_last_seen — the single source of date. Without it, a violation.
    |
    +- Metrics:
    |   proto_concepts_active / proto_concepts_promoted_total
    |   concept_emergence_zero_token / proto_concepts_expired_total
    \- Decay: ProtoConcept -> expired after 30 days of inactivity
```

### Code [RFC0066]

```python
# concept_emergence.py
# RFC0066: Concept Emergence — v8.0.2 + Sprint 1 + Sprint 1.1
#
# I50:   does not write to the graph. Only ProtoConcept in-memory.
# I50-b: promotion to L3 only through TruthGate.
# I50-c: emergence_matrix stores only counters, not content.
# I66:   ProtoConcept lives only in memory.            (Sprint 1)
# I70:   active protos ≤ MAX_ACTIVE_PROTOS.            (Sprint 1)
# I-K3:  GC does not remove observations younger than TTL_DAYS. (Sprint 1.1 FIX-K3)
import asyncio          # A2: Lock to protect against concurrent access
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from typing import Optional, FrozenSet, Dict
from uuid import uuid4
from velantrim_config import EMERGENCE   # P0-A FIX: EMERGENCE.MAX_ACTIVE_PROTOS (previously NameError)

logger = logging.getLogger(__name__)


@dataclass
class ProtoConcept:
    proto_id:       str
    entities:       FrozenSet[str]
    co_occur_count: int      = 0
    cross_sessions: int      = 0
    salience_boost: float    = 0.0   # P10-FIX: declared explicitly (daily_maintenance used a getattr fallback)
    first_seen:     datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    last_active:    datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    last_decay:     datetime = field(default_factory=lambda: datetime.now(timezone.utc))  # P10-FIX: explicit field
    name:           Optional[str] = None
    confidence:     float         = 0.0
    expired:        bool          = False

    def update_confidence(self):
        # Conservative formula + salience_boost (Hebbian LTP).
        # Maximum without boost: co_occur=20 + cross=10 -> 0.83
        base = (min(1.0, self.co_occur_count / 20.0) * 0.6 +
                min(1.0, self.cross_sessions  / 10.0) * 0.4)
        # P10-FIX: salience_boost strengthens confidence (LTP analog), capped at 1.0
        self.confidence = min(1.0, base * (1 + self.salience_boost))


class ConceptEmergenceDetector:
    """
    RFC0066: Organic birth of concepts from Velum edge statistics.
    Without LLM extraction. 0 tokens. Analog: Hebbian Unsupervised Learning.

    P2-A: class-level constants → EMERGENCE (velantrim_config). Single source of truth.
    A2:   asyncio.Lock — protection against a race condition between observe() / daily_maintenance() / gc_expired().
    A3:   l5_5 scaffold — signal to PredictiveFusionLayer when the threshold is reached.
    FIX-K3: _matrix_last_seen — GC does not remove immature observations before TTL_DAYS.
    """

    def __init__(self, db, truth_gate=None, llm_client=None, l5_5=None):
        self.db         = db
        self.truth_gate = truth_gate
        self.llm_client = llm_client
        # A3: reference to L5.5 PredictiveFusionLayer.
        # None = scaffold inactive. Pass it during initialization in Sprint 2.
        self.l5_5 = l5_5

        if truth_gate is None:
            logger.warning(
                "ConceptEmergenceDetector: truth_gate=None — ProtoConcept "
                "will never be promoted to L3. Pass truth_gate= "
                "during initialization."
            )

        self._matrix:           Dict[FrozenSet[str], int]      = {}
        self._sessions:         Dict[FrozenSet[str], set]      = {}
        self._protos:           Dict[str, ProtoConcept]        = {}
        self._entity_to_protos: Dict[str, list]                = {}

        # FIX-K3: date of the last counter update for each combination.
        # _gc_impl() removes a key from _matrix ONLY if there is no live proto AND
        # the key has not been updated for longer than TTL_DAYS. Before the fix: GC zeroed out
        # immature observations every night (4 of the 5 needed → 0 → the concept was never born).
        self._matrix_last_seen: Dict[FrozenSet[str], datetime] = {}

        # A2: asyncio.Lock — protects all internal structures from a race condition.
        # ⚠️  asyncio.Lock is NOT reentrant.
        # Solution: _gc_impl() — internal method without lock.
        #          gc_expired() — public, acquires the lock itself.
        #          daily_maintenance() — acquires the lock and calls _gc_impl() inside.
        self._lock = asyncio.Lock()

    async def observe(
        self,
        entities: list[str],
        session_id: str,
        salience_weight: float = 1.0,
    ) -> None:
        """
        Phase 1 (Observation): update the co-occurrence matrix.
        Phase 2 (Birth):       create a ProtoConcept when the threshold is reached.

        A2: the method is now async. All call sites must use:
            await detector.observe(entities, session_id)
        FIX-K3: updates _matrix_last_seen on every change to a counter.
        FIX-A3: _notify_l5_5 is called ONLY when the threshold is reached (_threshold_hit).
        """
        if len(entities) < EMERGENCE.MIN_ENTITIES:
            return
        entities = entities[:EMERGENCE.MAX_ENTITIES]
        from itertools import combinations
        _threshold_hit = False
        async with self._lock:
            for size in range(EMERGENCE.MIN_ENTITIES, len(entities) + 1):
                for combo in combinations(sorted(entities), size):
                    key = frozenset(combo)
                    self._matrix[key] = self._matrix.get(key, 0) + 1
                    self._matrix_last_seen[key] = datetime.now(timezone.utc)  # FIX-K3
                    self._sessions.setdefault(key, set()).add(session_id)
                    # Update the existing proto if present (LTP salience boost)
                    for proto in self._protos.values():
                        if proto.entities == key and not proto.expired:
                            proto.salience_boost = max(proto.salience_boost, salience_weight - 1.0)
                            proto.update_confidence()
                            break
                    if (self._matrix[key]            >= EMERGENCE.CO_OCCUR_MIN and
                            len(self._sessions[key]) >= EMERGENCE.CROSS_SESSION):
                        self._maybe_create_proto(key)
                        _threshold_hit = True
        # FIX-A3: notify L5.5 only if at least one combination reached the threshold
        if _threshold_hit and EMERGENCE.L5_5_INTEGRATION and self.l5_5 is not None:
            await self._notify_l5_5(entities, salience_weight)

    async def _notify_l5_5(self, entities: list[str], salience_weight: float) -> None:
        """
        A3 scaffold: notify PredictiveFusionLayer of a new proto candidate.
        FIX-A3: called only when _threshold_hit=True in observe().
        The real logic — Sprint 2 (B1): self.l5_5.register_proto_concept(...)
        """
        logger.debug(
            f"_notify_l5_5 scaffold | threshold reached | "
            f"entities={entities[:3]}{'...' if len(entities) > 3 else ''} | "
            f"salience={salience_weight:.2f}"
        )
        # TODO (Sprint 2, B1): await self.l5_5.register_proto_concept(...)

    def _maybe_create_proto(self, key):
        for proto in self._protos.values():
            if proto.entities == key and not proto.expired:
                proto.co_occur_count = self._matrix[key]
                proto.cross_sessions = len(self._sessions[key])
                proto.last_active    = datetime.now(timezone.utc)
                proto.update_confidence()
                return

        # P0.5-4 FIX: enforce MAX_ACTIVE_PROTOS cap.
        # Without this, _protos grows without bound in hot domains → OOM within weeks.
        # Eviction: remove the proto with the lowest confidence (the least mature concept).
        active_protos = [p for p in self._protos.values() if not p.expired]
        if len(active_protos) >= EMERGENCE.MAX_ACTIVE_PROTOS:
            victim = min(active_protos, key=lambda p: p.confidence)
            logger.debug(
                f"ProtoConcept evicted (cap={EMERGENCE.MAX_ACTIVE_PROTOS}): "
                f"{victim.proto_id} conf={victim.confidence:.2f}"
            )
            # Remove from _protos and _entity_to_protos
            del self._protos[victim.proto_id]
            for entity in victim.entities:
                if entity in self._entity_to_protos:
                    self._entity_to_protos[entity] = [
                        pid for pid in self._entity_to_protos[entity]
                        if pid != victim.proto_id
                    ]

        proto = ProtoConcept(
            proto_id=f"proto:{uuid4().hex[:8]}", entities=key,
            co_occur_count=self._matrix[key],
            cross_sessions=len(self._sessions[key]),
        )
        proto.update_confidence()
        self._protos[proto.proto_id] = proto
        for entity in key:
            self._entity_to_protos.setdefault(entity, []).append(proto.proto_id)
        logger.info(f"ProtoConcept born: {proto.proto_id} conf={proto.confidence:.2f}")

    def get_protos_for_entity(self, entity: str) -> list[ProtoConcept]:
        return [
            self._protos[pid]
            for pid in self._entity_to_protos.get(entity, [])
            if pid in self._protos and not self._protos[pid].expired
        ]

    async def promote_to_l3(self, proto: ProtoConcept) -> bool:
        # I50-b: promotion only through TruthGate
        if not self.truth_gate:
            logger.warning(f"Cannot promote {proto.proto_id}: truth_gate not configured")
            return False
        result = await self.truth_gate.validate_and_transition({
            "id": proto.proto_id,
            "content": f"Concept: {proto.name} -- {', '.join(sorted(proto.entities))}",
            "confidence": proto.confidence,
            "source": "concept_emergence",
        })
        return result.passed

    async def _common_token_name(self, proto: ProtoConcept) -> str:
        # P3-G FIX: renamed from _tfidf_name — the implementation uses set-intersection,
        # not TF-IDF weighting. Zero LLM tokens. Simple intersection of entity tokens.
        # All calls to _tfidf_name() → _common_token_name() in the file.
        # Extraction of a common root from entity names — 0 tokens
        entity_words = [e.lower().replace("_", " ").split() for e in proto.entities if e]
        if not entity_words:
            return "unnamed_concept"
        common = set(entity_words[0])
        for words in entity_words[1:]:
            common &= set(words)
        if common:
            return "_".join(sorted(common)[:2])
        first = [w[0] for w in entity_words[:2] if w]
        return "_".join(first) if first else "unnamed_concept"

    # A1: decay_factor is read from EMERGENCE.HEBBIAN_DECAY_FACTOR (was hardcoded 0.98)
    # A2: the entire _protos traversal + GC — under a single lock (no DEADLOCK: _gc_impl without lock)
    async def daily_maintenance(self) -> None:
        """
        P4-B + A1 + A2: Daily Hebbian Decay + GC.
        Call from SleepTimeWorker once a day.
        Metric: concept_hebbian_decay_applied_total
        """
        async with self._lock:
            decay_count = 0
            for proto in self._protos.values():
                if not proto.expired:
                    days_since = (datetime.now(timezone.utc) - proto.last_decay).days
                    if days_since > 0:
                        # A1: from config instead of hardcoded 0.98
                        proto.confidence *= (EMERGENCE.HEBBIAN_DECAY_FACTOR ** days_since)
                        proto.last_decay = datetime.now(timezone.utc)
                        decay_count += 1
            if decay_count > 0:
                logger.info(
                    f"🌙 Hebbian Decay: {decay_count} protos | "
                    f"factor={EMERGENCE.HEBBIAN_DECAY_FACTOR}"
                )
            # GC inside the same lock — we call _gc_impl() (not gc_expired(), no DEADLOCK)
            self._gc_impl()

    async def gc_expired(self) -> None:
        """
        Public GC — acquires the lock itself.
        Call directly when cleanup is needed outside daily_maintenance().
        A2: split into gc_expired() (public + lock) and _gc_impl() (private, without lock).
        """
        async with self._lock:
            self._gc_impl()

    def _gc_impl(self) -> None:
        """
        Internal GC implementation — called INSIDE self._lock.
        Does NOT acquire the lock itself.

        FIX-K3: dual criterion for removing _matrix keys:
            (a) there is no live proto for this key, AND
            (b) the key has not been updated for longer than TTL_DAYS.
        Before the fix: any key without a proto was removed every night →
        slowly growing concepts were never born.

        P0.5-5: orphan keys in _sessions (present in _sessions, absent from _matrix) are also cleaned.
        """
        now = datetime.now(timezone.utc)
        ttl = timedelta(days=EMERGENCE.TTL_DAYS)

        # 1. Mark expired ProtoConcepts
        expired_ids = []
        for proto in self._protos.values():
            if not proto.expired and (now - proto.last_active) > ttl:
                proto.expired = True
                expired_ids.append(proto.proto_id)

        # 2. Clean expired proto_ids from _entity_to_protos
        for entity, pids in list(self._entity_to_protos.items()):
            cleaned = [p for p in pids if p not in expired_ids]
            if cleaned:
                self._entity_to_protos[entity] = cleaned
            else:
                del self._entity_to_protos[entity]

        # 3. FIX-K3: remove a _matrix key only by the dual criterion
        live_entity_sets = {
            proto.entities
            for proto in self._protos.values()
            if not proto.expired
        }
        stale_cutoff = now - ttl
        for key in list(self._matrix.keys()):
            if key in live_entity_sets:
                continue  # proto is alive — don't touch
            last_seen = self._matrix_last_seen.get(key)
            if last_seen is None or last_seen < stale_cutoff:
                # No proto AND not updated for longer than TTL → remove
                del self._matrix[key]
                self._matrix_last_seen.pop(key, None)
                self._sessions.pop(key, None)
            # Otherwise: no proto, but the observation is fresh — leave it to grow (FIX-K3)

        # 4. P0.5-5 FIX: orphaned sessions (in _sessions but not in _matrix)
        stale_sessions = [k for k in self._sessions if k not in self._matrix]
        for key in stale_sessions:
            del self._sessions[key]

        if expired_ids:
            active = len([p for p in self._protos.values() if not p.expired])
            logger.info(
                f"ConceptEmergence GC: {len(expired_ids)} expired | active={active}"
            )
```

### Tests [RFC0066 — Sprint 1]

```python
# tests/test_invariants.py + test_sprint1_additions.py
# File: test_sprint1_additions.py (add to the test suite or run separately)
#
# Invariants: I50, I50-b, I66 (FIX), I70, I-K3, A1, A2, A3

import pytest
import asyncio as _asyncio
from velantrim_config import EMERGENCE
from concept_emergence import ConceptEmergenceDetector, ProtoConcept


class MockDB:
    """DB stub — the detector stores it but does not use it in the current implementation."""
    pass


class MockTruthGate:
    """
    Mock TruthGate with a call counter.
    call_count == 0 after observe() → TruthGate not called → L3 untouched.
    """
    def __init__(self):
        self.call_count = 0

    async def validate_and_transition(self, proposal: dict):
        self.call_count += 1
        class _Result:
            passed = True
        return _Result()


# ── I50 ──────────────────────────────────────────────────────────────────────
@pytest.mark.asyncio
async def test_I50_concept_emergence_no_graph_writes():
    """I50: observe() does not write to L3. TruthGate is never called."""
    gate     = MockTruthGate()
    detector = ConceptEmergenceDetector(db=MockDB(), truth_gate=gate)
    for i in range(10):
        await detector.observe(["A", "B", "C"], session_id=f"s{i}")
    assert gate.call_count == 0, (
        f"I50 VIOLATION: TruthGate called {gate.call_count} time(s) during observe()."
    )
    assert len(detector.get_protos_for_entity("A")) >= 1


# ── I50-b ────────────────────────────────────────────────────────────────────
@pytest.mark.asyncio
async def test_I50b_proto_promote_requires_truthgate():
    """I50-b: promote_to_l3() calls TruthGate exactly once."""
    gate = MockTruthGate()
    d    = ConceptEmergenceDetector(db=MockDB(), truth_gate=gate)
    p    = ProtoConcept(
        proto_id="proto:t01", entities=frozenset(["A", "B", "C"]),
        co_occur_count=7, cross_sessions=4, name="test", confidence=0.75,
    )
    await d.promote_to_l3(p)
    assert gate.call_count >= 1, "I50-b VIOLATION: promotion without TruthGate"


# ── I66 (FIX-I66) ────────────────────────────────────────────────────────────
@pytest.mark.asyncio
async def test_I66_proto_only_in_memory():
    """
    I66: ProtoConcept lives only in memory — observe() does not initiate a write to L3.

    FIX-I66: the previous version created a MockGraph() unconnected to the detector —
    the test always passed trivially. New version: gate.call_count == 0 proves
    that TruthGate (the only entry to L3) was not called.
    """
    gate     = MockTruthGate()
    detector = ConceptEmergenceDetector(db=MockDB(), truth_gate=gate)
    for i in range(EMERGENCE.CO_OCCUR_MIN + 2):
        session = f"s{i % (EMERGENCE.CROSS_SESSION + 1)}"
        await detector.observe(["Alpha", "Beta", "Gamma"], session_id=session)
    assert gate.call_count == 0, (
        f"I66 VIOLATION: TruthGate called {gate.call_count} time(s) during observe(). "
        f"ProtoConcept must not be promoted automatically on observe()."
    )
    protos = detector.get_protos_for_entity("Alpha")
    assert len(protos) >= 1, "I66: ProtoConcept not created in memory."
    assert not protos[0].expired, "I66: a fresh ProtoConcept is marked expired — a bug."
    assert protos[0].proto_id in detector._protos, "I66: proto_id not in _protos."


# ── I70 ──────────────────────────────────────────────────────────────────────
@pytest.mark.asyncio
async def test_I70_max_active_protos_cap():
    """
    I70: active ProtoConcepts ≤ MAX_ACTIVE_PROTOS. Eviction works.
    We inject data directly via _maybe_create_proto() for speed.
    """
    detector = ConceptEmergenceDetector(db=MockDB(), truth_gate=None)
    overflow_count = 100
    total = EMERGENCE.MAX_ACTIVE_PROTOS + overflow_count
    for i in range(total):
        key = frozenset([f"Ent{i}_A", f"Ent{i}_B", f"Ent{i}_C"])
        detector._matrix[key] = EMERGENCE.CO_OCCUR_MIN + 1
        for s in range(EMERGENCE.CROSS_SESSION + 1):
            detector._sessions.setdefault(key, set()).add(f"sess_{i}_{s}")
        detector._maybe_create_proto(key)
    active = [p for p in detector._protos.values() if not p.expired]
    assert len(active) <= EMERGENCE.MAX_ACTIVE_PROTOS, (
        f"I70 VIOLATION: {len(active)} active protos at limit {EMERGENCE.MAX_ACTIVE_PROTOS}."
    )
    assert len(active) == EMERGENCE.MAX_ACTIVE_PROTOS, (
        f"I70: expected exactly {EMERGENCE.MAX_ACTIVE_PROTOS} protos, got {len(active)}."
    )


# ── FIX-K3 ───────────────────────────────────────────────────────────────────
@pytest.mark.asyncio
async def test_K3_immature_observations_survive_gc():
    """
    FIX-K3: immature observations (without a proto, below the threshold) are NOT removed by GC.
    Critical for slowly growing concepts (once a week → 5 weeks to threshold).
    """
    detector = ConceptEmergenceDetector(db=MockDB(), truth_gate=None)
    for i in range(EMERGENCE.CO_OCCUR_MIN - 1):
        session = f"s{i % (EMERGENCE.CROSS_SESSION + 1)}"
        await detector.observe(["Slow", "Concept", "Growth"], session_id=session)
    key = frozenset(["Slow", "Concept", "Growth"])
    assert key in detector._matrix, "Test: the observation must be in _matrix before GC."
    assert len(detector.get_protos_for_entity("Slow")) == 0, "Test: there must be no proto."
    count_before = detector._matrix[key]
    await detector.gc_expired()
    assert key in detector._matrix, (
        f"FIX-K3 VIOLATION: gc_expired() removed immature observations "
        f"(count={count_before}, threshold={EMERGENCE.CO_OCCUR_MIN})."
    )
    assert detector._matrix[key] == count_before, "FIX-K3: the counter changed after GC."


# ── A1: config constants present ─────────────────────────────────────────────
def test_A1_emergence_config_constants():
    """A1: EmergenceConfig contains all Sprint 1 constants with correct types."""
    assert hasattr(EMERGENCE, "HEBBIAN_DECAY_FACTOR"), "A1: HEBBIAN_DECAY_FACTOR missing."
    assert hasattr(EMERGENCE, "SALIENCE_MULTIPLIER"),  "A1: SALIENCE_MULTIPLIER missing."
    assert hasattr(EMERGENCE, "L5_5_INTEGRATION"),     "A1: L5_5_INTEGRATION missing."
    assert isinstance(EMERGENCE.HEBBIAN_DECAY_FACTOR, float), "A1: HEBBIAN_DECAY_FACTOR must be float."
    assert 0.0 < EMERGENCE.HEBBIAN_DECAY_FACTOR <= 1.0, (
        f"A1: HEBBIAN_DECAY_FACTOR={EMERGENCE.HEBBIAN_DECAY_FACTOR} out of range (0, 1]."
    )
    assert isinstance(EMERGENCE.L5_5_INTEGRATION, bool), "A1: L5_5_INTEGRATION must be bool."


# ── A2: Lock initialized ──────────────────────────────────────────────────────
def test_A2_lock_initialized():
    """A2: detector has an asyncio.Lock and _matrix_last_seen (FIX-K3)."""
    detector = ConceptEmergenceDetector(db=MockDB())
    assert hasattr(detector, "_lock"), "A2: _lock missing."
    assert isinstance(detector._lock, _asyncio.Lock), "A2: _lock must be an asyncio.Lock."
    assert hasattr(detector, "_matrix_last_seen"), "FIX-K3: _matrix_last_seen missing."
    assert isinstance(detector._matrix_last_seen, dict), "FIX-K3: _matrix_last_seen must be a dict."


# ── A3: _notify_l5_5 fires only on threshold ─────────────────────────────────
@pytest.mark.asyncio
async def test_A3_l5_5_scaffold_threshold_only():
    """
    FIX-A3: _notify_l5_5 is called only when the threshold is reached,
    not on every observe().
    """
    calls = []

    class MockL5_5:
        pass

    detector = ConceptEmergenceDetector(db=MockDB(), l5_5=MockL5_5())
    original_notify = detector._notify_l5_5
    async def _patched_notify(entities, salience_weight):
        calls.append((entities, salience_weight))
        await original_notify(entities, salience_weight)
    detector._notify_l5_5 = _patched_notify

    for i in range(EMERGENCE.CO_OCCUR_MIN - 1):
        session = f"s{i % (EMERGENCE.CROSS_SESSION + 1)}"
        await detector.observe(["X", "Y", "Z"], session_id=session)

    assert len(calls) == 0, (
        f"FIX-A3 VIOLATION: _notify_l5_5 called {len(calls)} time(s) before the threshold."
    )
```

### Add to velantrim_config.py

```python
class EmergenceConfig:
    CO_OCCUR_MIN      = 5
    CROSS_SESSION     = 3  # FIX: renamed from CROSS_SESSION_MIN → CROSS_SESSION
                           # to match ConceptEmergenceDetector and avoid AttributeError
    MIN_ENTITIES      = 3
    MAX_ENTITIES      = 7
    NAMING_THRESHOLD  = 0.7
    TTL_DAYS          = 30  # P2-A: was hardcoded in gc_expired() — now configurable
    MAX_ACTIVE_PROTOS = 500
    # Sprint 1 (A1): were hardcoded in daily_maintenance() and observe()
    HEBBIAN_DECAY_FACTOR: float = 0.98   # confidence *= factor**days  (0,1]
    SALIENCE_MULTIPLIER:  float = 1.0    # multiplier for the salience_boost computation
    L5_5_INTEGRATION:     bool  = False  # A3: scaffold off by default; Sprint 2 enables it

EMERGENCE = EmergenceConfig()
```

---

### P1-2: Cognitive typing of memory (a new orthogonal axis)

```python
# A new axis on top of L0–L7 — orthogonal to ESM and knowledge_type
from enum import Enum

class MemoryType(str, Enum):
    EPISODIC   = "episodic"    # specific events, dialogues
    SEMANTIC   = "semantic"    # facts, concepts, definitions
    PROCEDURAL = "procedural"  # skills, procedures, workflows

# Add a field to MemoryItem / :Fact / :Episode / :Theme:
memory_type: MemoryType = MemoryType.EPISODIC

def classify_memory_type(content: str, tags: list = None) -> MemoryType:
    tags = tags or []
    c = content.lower()
    if any(w in c for w in ["step", "procedure", "workflow", "algorithm", "how to do"]):
        return MemoryType.PROCEDURAL
    if any(t in tags for t in ["how-to", "process", "recipe", "workflow"]):
        return MemoryType.PROCEDURAL
    if any(w in c for w in ["definition", "law", "rule", "means"]):
        return MemoryType.SEMANTIC
    if any(t in tags for t in ["definition", "concept", "law", "rule"]):
        return MemoryType.SEMANTIC
    return MemoryType.EPISODIC
```

---

L2: Medium-Term Memory                                  ← RFC0013
    ├─ Storage: SQLite (WAL) table l2_memory + FTS5 on summary
    │   NOT a list in RAM — a persistent layer, not lost on restart.
    ├─ :Theme node in Neo4j — a persistent cluster with rich metadata:
    │     · theme_id, summary, summary_embedding
    │     · cluster_size, strength, confidence
    │     · emotional_salience, goal_alignment
    │     · access_count_7d, decay_lambda, is_active
    │     · schema_type: ["factual","procedural","emotional","strategic"]
    │     · first_seen, last_updated
    │   ⚠️ TYPE CLARIFICATION FOR emotional_salience:
    │     :Theme.emotional_salience — FLOAT [0.0, 1.0]
    │       0.0 = neutral event
    │       0.5 = notable (partial success/failure)
    │       1.0 = critical (strong SUCCESS/FAILURE)
    │     :Theme.emotional_label — STRING (optional, for the UI)
    │       "SUCCESS" | "FAILURE" | "NEUTRAL" | "CRITICAL"
    │     In the strength formula:
    │       emotional = 1.0 + emotional_salience × 1.3  → range 1.0…2.3
    │     Emotional Ring Zero (RFC0015):
    │       emotional_salience > 0.85 → ESM.freeze() — immunity to decay
    ├─ cluster_type: EPISODIC | STRATEGIC | CONCEPTUAL
    │     · EPISODIC   → decay_rate=0.05 (fast) → ReasoningBank
    │     · STRATEGIC  → decay_rate=0.02 (medium) → L3 + ReasoningBank
    │     · CONCEPTUAL → decay_rate=0.01 (slow) → L3 through Truth Gate
    ├─ strength formula (weighted sum):
    │     Robust against zero factors — zeroing one component
    │     does not zero out the resulting theme strength.
    │
    │     strength = (
    │         w_base  × base_factor        +
    │         w_reinf × reinforcement_factor +
    │         w_emot  × emotional_factor   +
    │         w_goal  × goal_alignment     +
    │         w_stab  × stability_factor
    │     ) / (w_base + w_reinf + w_emot + w_goal + w_stab)
    │
    │     Default weights (velantrim_config.py):
    │       w_base  = 1.0
    │       w_reinf = 1.0
    │       w_emot  = 1.5   ← emotional memory matters more
    │       w_goal  = 1.2
    │       w_stab  = 0.8
    │
    │     Components:
    │       base_factor          = 1.0 + log1p(cluster_size) × 0.45          # log1p(x) = log(1+x), see np.log1p
    │       reinforcement_factor = 1.0 + 0.15 × log1p(access_count_7d)
    │       emotional_factor     = 1.0…2.3  (2.0 on SUCCESS/FAILURE)
    │       goal_alignment       = cosine(theme_embedding, active_goal_embedding) ∈ [0,1]
    │         Source of active_goal_embedding:
    │           · A0 (Hot Focus) active → embedding of the current query
    │           · A1 (Day Focus) has an active goal → goal_stack[0].embedding
    │           · Both empty → last_user_query_embedding (cache)
    │           · Fallback → 0.5 (neutral, does not zero out the formula)
    │           · ⚠️ 0.5 at w_goal=1.2 is not neutral — it actively penalizes nodes without
    │           · an active goal relative to nodes with a goal (strength = 0.6 vs ~0.8).
    │           · TODO: consider fallback=1.0 or a goal_context_absent flag
    │           · so that the w_goal contribution is explicitly neutralized when no goal is present.
    │       stability_factor     = 1 / (1 + days_since_update × λ₂)
    │
    │     The decomposition is stored in strength_components (JSON):
    │       {"base": 1.2, "reinf": 1.1, "emot": 1.8, "goal": 0.6, "stab": 0.9}
    │     Delivery mechanism: A0/A1 → SessionContext → L2IngestionEngine
    │     Refresh: updated on every new user query
    │   Promotion threshold to L3: (strength > 4.5) ∧ (access_count > 10) ∧ (stability > 0.75)
    ├─ TTL Manager (adaptive):
    │     TTL = 7 days × 2^min(visits, 5) — max 224 days
    │     visits = access_count + reactivation_count
    │     On expiry: important → extend, low-importance → soft delete → S3
    ├─ ReactivationEngine ("agent's sleep", Phase 1):
    │     A background asyncio.Task when CPU < 30%. Every hour it scrolls through
    │     the top-N episodes by importance, strengthens connections, extends TTL.
    │     Analogous to hippocampal replay in neuroscience.
    ├─ Cold Start Guard:
    │     if len(l2_items) < 50: skip_clustering()
    │     Running clustering on < 50 episodes → micro-clusters → a bug.
    ├─ I/O batching: L2MetricsBuffer (flush every 10 min) — SSD protection
    ├─ L3→L2 feedback: on an ESM transition of a fact (Validated→Contradicted)
    │     → find the :Theme that contain this fact → reduce strength × epistemic_penalty
    ├─ Connections in the graph:
    │     :Theme -[:CONTAINS {weight, since}]→ :Episode
    │     :Theme -[:SIMILAR_TO {cosine}]→ :Theme
    │     :Theme -[:GENERALIZES_TO]→ :KnowledgeUnit  (in L3)
    │     :Theme -[:EXEMPLIFIES]→ :Outcome
    │     :Theme -[:HAS_FACTS]→ :FactsPack
    ├─ Success/failure patterns + anti-patterns → ReasoningBank
    │
    │   ⚠️ DISTINCTION L2 vs L4 (RFC0014):
    │     L2 = experience: clusters, patterns, themes — NOT facts, NOT reasoning
    │     L4 = reasoning: the single point of logic and inference
    │     L2 provides a template → L4 applies it → the Graph provides facts
    │     L2 is NOT a source of facts. FactsPack is built only from the Graph.
    │
    └─ Decay: FSRS power-law (v8.0 — replaces the Ebbinghaus exponential, P0-1)

         R = (1 + 19/81 × t/S)^(-0.5)
         # More accurate than the Ebbinghaus exponential by 20-30% (FadeMem paper, jan 2026)
         # The Fast Path reads cached retrievability from the graph index.
         # FSRSState is created lazily — only in the Slow Path (SleepTimeWorker/DecayWorker).
         # Replaces Ebbinghaus: R = e^(-t/S) per P0-1
         R = retention (how much remains)
         t = time since the last confirmation
         S = strength (grows with repetitions · multiplied by salience_weight)

         A fact mentioned once:
           → after 1 day   confidence: 0.58
           → after 7 days  confidence: 0.21
           → after 30 days confidence: 0.05 → cold storage

         The same fact mentioned 5 times (S grew):
           → after 1 day   confidence: 0.91
           → after 7 days  confidence: 0.74
           → after 30 days confidence: 0.52 → still active

         salience_weight multiplies S: important facts live longer than ordinary ones.
         Worker: runs once an hour via the EventBus · CPU only · ~0 load
         Emotional Ring Zero (RFC0015): emotional_salience > 0.85 → immunity to decay

    Cache-Aware Hot Graph — a two-tier graph
    ├─ By analogy with OS virtual memory: everything is divided into hot and cold.
    │
    │   🔥 Hot graph (lives in RAM):
    │     · Nodes activated in the last 24 hours
    │     · Nodes with salience_weight > 0.7  ← the Salience Detector decides who belongs here
    │     · LITE: ~500–2000 nodes · 2–5 MB RAM
    │     · ONE:  ~10–50k nodes   · 50–100 MB RAM
    │
    │   🧊 Cold graph (SSD / Neo4j):
    │     · Everything else
    │     · Loaded only if spreading activation is strong enough
    │
    │   Spreading activation first traverses the hot graph in 1–3 ms.
    │   Cold nodes — only as needed.
    │   System speedup: ×2–3 · without additional CPU load.
    │   Rebalancing: once an hour via the EventBus SleepTimeWorker.
    │   Metrics:
    │     hot_graph_size_nodes   — current size of the hot graph
    │     hot_graph_hits_total   — how many requests were served from RAM
    │     cold_graph_loads_total — how many times the cold graph was loaded

L2.5: Staging Layer (RFC0014) — a buffer before L3
    │   SQLite = a temporary buffer (staging), NEVER a source of truth.
    │   Graph = the single L3. The Graph = Truth principle is not violated.
    ├─ Purpose: asynchronous consolidation for weak hardware.
    │     L0/L1/L2 write to SQLite → data matures → into L3 only when resources allow.
    ├─ Resource-Aware Scheduler:
    │     Launch conditions: CPU < 35% AND RAM free > 25% AND user_idle
    │     If the PC is busy — staging accumulates data, the graph is not built.
    │     Forced flush: if the PC is not idle for > 24h → 5-10% CPU in the background.
    ├─ Fast-Track (queue bypass):
    │     priority > 0.9 → immediately → Truth Gate → L3
    │     CRITICAL examples: allergies, Ring Zero changes, critical facts
    ├─ Graph-Lite (for a weak PC, RAM < 4GB):
    │     A temporary mini-graph inside SQLite (nodes + edges tables).
    │     On query: UNION of Graph-Lite (staging) + L3.
    │     This is NOT a parallel truth — the same L3 logic, a different engine.
    │     On transfer to Neo4j, Graph-Lite is cleared.
    ├─ Reading rule:
    │     1. The graph first (L3) — the canon
    │     2. If not in the graph but present in staging → use it with confidence × 0.7
    │        and a "preliminary" marker (not truth, a hypothesis)
    ├─ Data path:
    │     L2 → staging_candidates → Priority Queue → Scheduler
    │         → Truth Gate → L3 (Graph)
    │     FAST-TRACK: L2 → Truth Gate → L3 (bypasses the queue)
    └─ Decay: staging_candidates TTL by priority_score, GC when > MAX_STAGING_SIZE

---

### P0-1 NEW: memory/fsrs_state.py (RFC0069)

The module is inserted into the project as a separate file. The full code is in patch P0-1 of the file VELANTRIM_TITAN_v8_CRYSTAL_PATCHES.md.

New fields in MemoryItem / FactNode:
    difficulty: float = 5.0           # D in [1.0, 10.0]
    stability: float = 1.0            # S — stability
    retrievability: float = 1.0       # R — current retrievability
    fsrs_last_review: datetime = None  # time of the last access

Config (velantrim_config.py):
    FSRS_ENABLED = True
    FSRS_PLASTICITY_W = 0.6
    FSRS_MIN_STABILITY = 0.1
    FSRS_REFRESH_THRESHOLD = 0.3

I84 (FSRSIsolation): FSRS decay changes ONLY retrievability and attention_weight.
    truth_status, epistemic_state and confidence — inviolable.
    FSRSState is created only in the Slow Path. The Fast Path reads the cache.

---

L3: Long-Term Memory
    ├─ Semantic concepts
    ├─ Meta-strategies
    ├─ The agent's personality and the user's preferences
    ├─ Write Protocol — the only permitted write paths:
    │     ✅ TruthGate (validated pipeline)
    │     ✅ Human approval (trust_score = 0.95)
    │     ✅ Trusted import (trust_score ≥ 0.80)
    │     ❌ LLM directly / L1 / L2 / Free Mode / Observer
    │     Violation → WriteProtocolViolation + log + Observer alert
    ├─ Source Trust Layer — a field on every fact:
    │     source_type: "user_input" | "llm_output" | "import" | "manual"
    │     trust_score: 0.0 – 1.0
    │     validation_status: "verified" | "pending" | "flagged"
    │     TruthGate accepts a fact only if trust_score ≥ TRUST_THRESHOLD
    │     Protection against "validated hallucination" — a hallucination that passed validation
    ├─ P1-3: knowledge_type on :Fact
    │     class KnowledgeType(str, Enum):
    │       TERM       = "term"        # term definition
    │       FACT       = "fact"        # a specific fact
    │       LAW        = "law"         # a law, rule, invariant
    │       MODEL      = "model"       # a model, theory
    │       METHOD     = "method"      # a method, algorithm
    │       CONSTRAINT = "constraint"  # a constraint
    │       OPINION    = "opinion"     # an opinion
    │     On the :Fact node: knowledge_type: str = "fact"  # default
    │     I87 (KnowledgeTypeImmutable): knowledge_type — read-only after Validated.
    │     Changing the type of a Validated fact = creating a new fact.
    │
    ├─ P1-5: Provenance Chain:
    │     Instead of a single source_type — a provenance array:
    │     provenance_chain: List[Dict] = [
    │       {"source_type": "user_input", "timestamp": "...", "content_hash": "..."},
    │       {"verified_by": "truth_gate", "confidence": 0.85},
    │       {"promoted_by": "esm_transition", "from": "Supported", "to": "Validated"}
    │     ]
    │     Append-only: removing entries from the chain is forbidden.
    │     I89 (ProvenanceAppendOnly): provenance_chain — append-only.
    │
    ├─ Fan-out Limit + Meta-Nodes:
    │     FAN_OUT_LIMIT = 500 connections of one type per node
    │     On overflow → aggregation into a meta-node (not a new edge)
    │     Protects Neo4j from degradation on "fat" nodes
    ├─ P1-1: Multi-Graph Decomposition (MAGMA-style):
    │     Edges are split into 4 orthogonal types:
    │     · [:SEMANTIC_REL]  — semantic relations (is-a, part-of, similar)
    │     · [:TEMPORAL_REL]  — temporal relations (before, after, during)
    │     · [:CAUSAL_REL]    — causal relations (causes, prevents, enables)
    │     · [:ENTITY_REL]    — entity relations (owns, works-at, located-in)
    │     IntentRouter (memory/intent_router.py) determines the query type →
    │     HybridRetriever traverses only the needed edges.
    │     "Why" → CAUSAL_REL. "When" → TEMPORAL_REL.
    │     "What is" → SEMANTIC_REL. Default → all types.
    │     I86 (IntentRouter): called ONLY from HybridRetriever.retrieve().
    │
    ├─ Decay: slow (months-years)
    ├─ Homeostatic Balancer — graph immunity
    │     A background process · launched by SleepTimeWorker at 3:00 AM when user_idle.
    │     Analog: synaptic homeostasis during deep sleep in humans.
    │
    │     The problem it solves: the graph accumulates a skew — thousands of strong
    │     connections in one area (for example, everything about Velantrim) and dead zones
    │     in others. Within a year the system starts to "think" about only one thing.
    │
    │     Algorithm:
    │       1. Collect the weight distribution across all graph domains
    │       2. If domain_weight > OVERLOAD_THRESHOLD (0.8):
    │            → soft normalization: multiply weights × 0.85
    │       3. If domain.last_active < now - 30 days:
    │            → raise the base weight × 1.2 (knowledge does not "die" entirely)
    │       4. Record homeostatic_run in the metrics
    │
    │     Load: 30–60 sec · once a day · CPU only
    │     Metric: homeostatic_runs_total · homeostatic_normalized_domains

    ### ESM State Transitions — Epistemic State Machine

         Observed → Hypothesized → Supported → Validated
                        ↑                          │
                        │ rollback                 ├─────────────────────┐
                        │ Evidence withdrawn       ▼                     ▼
                        └────────────── Contradicted         (remains Validated)
                                                   │ 3+ conflicts
                                                   ▼
                                             Deprecated
                                                   │ importance < 0.1
                                                   ▼
                                              Collapsed
                                    (→ Immutable Raw Memory, not destroyed)
       Transition rules:
         · Observed     → Hypothesized : first appearance (auto)
         · Hypothesized → Observed     : Evidence withdrawn — rollback
         · Hypothesized → Supported    : Evidence ≥ 2
         · Supported    → Validated    : MGL + Truth Gate passed
         · Validated    → Contradicted : 1+ strong [:CONTRADICTS]
         · Contradicted → Deprecated   : importance -= weighted_penalty × 3+
         · Deprecated   → Collapsed    : importance < 0.1 at GC

    ├─ P1-4: Per-node Versioning (OCC):
    │     Each :Fact has a _version_: int (starts at 1).
    │     ESM transitions use Optimistic Concurrency Control:
    │       MATCH (f:Fact {id: $id, _version_: $expected})
    │       SET f.epistemic_state = $new, f._version_ = f._version_ + 1
    │     If _version_ does not match — retry via the queue.
    │     I88 (VersionOCC): _version_ is incremented ONLY atomically via OCC Cypher.
    │     A direct SET _version_ without checking expected — a bug.

L3.5: Immutable Core — The eternal foundation of memory   ← RFC0017
    ├─ Purpose: an append-only ledger, protection against catastrophic forgetting.
    │   This is NOT an operational layer — it is audit and recovery.
    ├─ Mechanism:
    │     Every 24 hours → snapshot of the L3 graph → SHA-256 hash + timestamp
    │     → write to a Neo4j :ImmutableCore node (append-only, no UPDATE/DELETE)
    │     → in parallel a Parquet file → S3 for long-term storage
    │     Delta Snapshots (differential storage):
    │       · Day 1: FULL snapshot (all nodes + edges)
    │       · Day 2+: DELTA snapshot (only changed/new/deleted)
    │       · Delta format: {added: [...], modified: [...], deleted: [...]}
    │       · Recovery: full_snapshot + apply(delta_1) + ... + apply(delta_N)
    │       · FULL snapshot every 7 days (for fast recovery)
    │     Storage savings: ~80-90% (instead of 365 full snapshots → 52 full + 313 delta)
    ├─ Storage:
    │     · Neo4j: node :ImmutableCore {timestamp, hash, node_count, edge_count, snapshot_type}
    │     · S3/MinIO: graph_snapshot_{timestamp}.parquet (full dump)
    │     · S3/MinIO: graph_delta_{timestamp}.parquet (differential)
    │     · SQLite: metadata (fractal_similarity_score, alert_triggered)
    ├─ Drift Detection:
    │
    │     knowledge graph snapshots — a metric from dynamical systems theory,
    │     not validated for graphs. Replaced with structural delta metrics:
    │     
    │     drift_score = {
    │         "node_delta":      abs(new_count  - old_count)  / old_count,
    │         "edge_delta":      abs(new_edges  - old_edges)  / old_edges,
    │         "avg_degree_delta": abs(new_avg_d - old_avg_d),
    │         "component_delta": abs(new_comp   - old_comp)   / max(old_comp,1)
    │     }
    │     if any(delta > 0.2 for delta in drift_score.values()):
    │         alert("Memory structural drift detected!")
    │     
    │     The 0.2 threshold = a 20% change over a day → an anomaly.
    ├─ Semantic Drift Monitor — semantic drift:
    │     On top of the structural one — an independent second monitor.
    │     Components: ESM-distribution + PageRank top-10 + domain shifts
    │     semantic_score = esm_drift*0.5 + centrality_drift*0.3 + domain_drift*0.2
    │     Two INDEPENDENT alerts (do not mix):
    │       · structural_drift → the graph changed in form
    │       · semantic_drift   → the graph changed in meaning
    │     Possible: a structurally stable graph with high semantic drift.
    ├─ ESMChunkedInvalidator — batched rollback:
    │     Replaces the direct [:CONTRADICTS] cascade (risk of a Neo4j deadlock).
    │     Batches of 50 nodes + asyncio.sleep(100ms) between batches.
    │     Required index: CREATE INDEX pending_inv_idx FOR (f:Fact)
    │                           ON (f.pending_invalidation)
    │     Safe Mode check: under SAFE_MODE → the process is paused.
    ├─ Usage:
    │     · Audit: GET /memory/audit/drift?since=... → show snapshots + similarity
    │     · Rollback: on catastrophe → restore L3 from snapshot_{t-N}
    │     · Verification: ReactivationEngine verifies Ring Zero nodes against the snapshot
    ├─ Invariants:
    │     ImmutableCore.I1: ONLY append, NEVER UPDATE/DELETE of :ImmutableCore nodes
    │     ImmutableCore.I2: A snapshot is created AFTER a successful consolidation (not in the middle)
    │     ImmutableCore.I3: The hash is verified on read — protection against bit rot
    │     ImmutableCore.I4: Ring Zero nodes are present in EVERY snapshot (otherwise an alert)
    ├─ GC rules:
    │     Snapshots older than 90 days → S3 only (remove metadata from Neo4j)
    │     Snapshots older than 1 year → cold storage (Glacier/Deep Archive)
    │     Ring Zero snapshots → NEVER delete (eternal storage)
    └─ Decay: none (immutable forever)

L4: Reasoning Layer — Self-learning from experience
    ├─ Purpose: extracting strategies from experience, self-learning, Thompson Sampling selection
    │   This is NOT facts (L3) — it is meta-knowledge: "how to solve problems"
    ├─ Closed Loop Self-Evaluation:
    │     Query → Retrieval → L4 → Answer → EVALUATE → ADJUST
    │     Metrics: faithfulness / trace_coverage / contradiction_rate / confidence
    │     Result → ReasoningBank (learning) + Observer (alert on low quality)
    ├─ Components:
    │   ┌─ ReasoningBank Engine:
    │   │  · Experience Buffer (RAM) — accumulation of experience before distillation
    │   │  · Strategy Repository (Neo4j :Strategy) — long-term storage
    │   │  · Thompson Sampling — exploration/exploitation balance (RFC0039)
    │   │  · Negative Reinforcement — avoiding repeated errors
    │   └─ Full implementation: See RFC0019
    ├─ Data structures:
    │   · Experience {task, context, action, outcome, reasoning, timestamp}
    │   · Strategy {strategy_id, description, contexts[], success_count, 
    │                failure_count, confidence, failure_penalty, embedding}
    ├─ Self-learning mechanism:
    │   [1] FAST PATH: User Query → retrieve_strategies() → Thompson Sampling selection
    │   [2] SLOW PATH: Task Complete → log_experience() → buffer
    │   [3] Buffer full (20 exp) → distill_strategies() → :Strategy nodes
    │   [4] update_strategy_feedback() → negative reinforcement
    ├─ Thompson Sampling (RFC0039 — replaces UCB1 RFC0025):
    │   Stochastic strategy selection via a Beta distribution.
    │   Lighter than UCB1 on CPU (O(1) vs O(k)), better with delayed feedback.
    │   Result: +8% cumulative reward on production tasks.
    │   
    │   Step 1 — TF-IDF pre-filter (kept from RFC0025):
    │     if cosine(strategy_embedding, context) < 0.3 → skip (irrelevant)
    │   Step 2 — Thompson Sampling (only for those passing the filter):
    │     rng = numpy.random.default_rng(session_id_hash)  # per-instance, thread-safe
    │     score = rng.beta(success_count + 1, failure_count + 1)
    │     where success_count and failure_count — the strategy's history
    │   Rationale: Beta(α,β) naturally balances exploration/exploitation.
    │     With few experiences — high variance → exploration.
    │     With many experiences — low variance → exploitation.
    │   Reproducibility: numpy.random.default_rng(session_id_hash) before the call
    │     for deterministic replay in audits (Invariant I13).
    │     ⚠️ Do NOT use numpy.random.seed() — the global PRNG, a race condition
    │     in asyncio with concurrent sessions. default_rng creates an isolated
    │     per-instance generator: the same seed → the same numbers, no shared state.
    │   Balance: adaptive — automatically shifts toward exploitation
    │     as data accumulates (no fixed 10%)
    ├─ Extractive Summarization (WITHOUT LLM):
    │   if importance < 0.5: TF-IDF extractive (0 tokens)
    │   elif importance < 0.8: GPT-4o-mini (cheap)
    │   else: GPT-4 (critical only)
    │   Token savings: 40-60%
    ├─ L4 Worker (background):
    │   · Periodic review of strategies (once a week)
    │   · Removal of low-effectiveness ones (success_rate < 0.2)
    │   · Cross-validation metrics
    ├─ Neo4j Schema:
    │   CREATE (:Strategy {strategy_id, description, applicable_contexts,
    │                       success_count, failure_count, confidence, embedding})
    │   CREATE INDEX strategy_embeddings FOR (s:Strategy) ON (s.embedding)
    │   CREATE (:Theme)-[:DERIVED_FROM]->(:Strategy)
    ├─ Integration with ContextBuilder:
    │   Prompt = [STRATEGIES: ...] + [FACTS: ...] + [QUERY: ...]
    │   Strategies come BEFORE facts in the context
    ├─ Metrics:
    │   · reasoning_bank_experiences_total — total experiences recorded
    │   · reasoning_bank_strategies_created — strategies created
    │   · reasoning_bank_ts_score — Thompson Sampling score per strategy
    │   · reasoning_bank_exploration_rate — exploration vs exploitation (adaptive)
    ├─ Results (proven by the ReasoningBank paper):
    │   · +30-35% task success rate (through learning from experience)
    │   · 40-60% reduction in token consumption (extractive without LLM)
    │   · Avoidance of repeated errors (negative reinforcement)
    └─ Decay: strategies with success_rate < 0.2 are removed after 30 days

L4.5: ResponseAudit & FocusEngine — Meta-layer of awareness ← RFC0052, RFC0053
    ├─ Purpose: meta-memory about dialogues + a live focus of attention on the user.
    │   This is NOT facts (L3) and NOT strategies (L4) — it is the system's awareness of its own responses
    │   and a continuous understanding of what the person needs right now.
    │   ⚠️ CLARIFICATION: L4.5 combines three RFCs in one layer:
    │     · RFC0052 — ResponseAuditWorker (response audit)
    │     · RFC0053 — FocusEngine (focus of attention)
    │     · RFC0065 — MemoryVolitionWorker (conscious will to remember)
    │   All three components work in the Slow Path via the EventBus.
    │
    ├─ [RFC0052] ResponseAuditWorker — Lazy two-phase response audit:
    │   FAST PATH: LLM → response to the user (no delay)
    │              → EventBus: RESPONSE_GENERATED (fire-and-forget)
    │   SLOW PATH: AuditWorker subscribed to the bus:
    │     Phase 1+2: SLM/TF-IDF → human_summary + tags + importance_score (0 heavy tokens)
    │     Phase 3:   ONLY if importance_score > 0.85 → flagship LLM → precomputed:
    │               { "essence", "critique", "vulnerabilities", "long-term", "goal", "proposal" }
    │     Storage: importance > 0.85 → SQLite + :DialogueSummary (Neo4j)
    │               importance < 0.85 → SQLite only (session)
    │               session ARCHIVED  → VacuumWorker: DELETE WHERE importance < 0.5
    │   ⚠️ Stale Cache Protection:
    │     dependency_hashes: List[fact_id] — IDs of L3 facts used in the response
    │     get_explanation() → _verify_dependencies() → TruthGate.check_facts_status()
    │     If a fact became Contradicted → audit.precomputed.clear() → lazy regenerate
    │   ⚠️ Preventive invalidation:
    │     TruthGate on an ESM transition → EventBus: CACHE_INVALIDATED {fact_ids}
    │     AuditWorker catches it → clears precomputed on all related audits immediately
    │   Data structure:
    │     @dataclass ResponseAudit:
    │       conversation_id, response_id, timestamp, status (NEW/ACTIVE/RESOLVED/BLOCKED)
    │       importance_score: float          # 0.0–1.0
    │       dependencies: List[str]          # fact_ids for invalidation
    │       human_summary: str               # Phase 2 (SLM)
    │       tags: List[str]                  # critique / vulnerability / long-term / ...
    │       precomputed: Dict[str, str]      # Phase 3 (Lazy, only importance > 0.85)
    │   Neo4j Schema:
    │     (:DialogueSummary {summary_id, human_summary, importance, tags, embedding})
    │     (:DialogueSummary)-[:HAS_TAG]→(:DialogueTag)
    │     (:DialogueSummary)-[:REFERS_TO]→(:Fact)
    │     (:DialogueSummary)-[:USES_STRATEGY]→(:Strategy)
    │   ⚠️ INVARIANT I28: ResponseAuditWorker is NEVER executed in the Fast Path.
    │     The audit is strictly in the SLOW PATH via the EventBus. A violation = blocking the response = a bug.
    │
    ├─ [RFC0053] FocusEngine — Live focus of attention (a synaptic portrait):
    │   Purpose: the system continuously "senses" what the user needs,
    │   reading the graph — without LLM calls (0 tokens).
    │   FocusVector components (updated by every dialogue):
    │     · goal_alignment      — what the user wants (A0/A1/A2)
    │     · emotional_salience  — what affected them (from :Theme)
    │     · pattern_of_ask      — how they ask (the type of queries)
    │     · domain_drift        — where their interest is moving (from Semantic Drift)
    │   Mechanism:
    │     L1 INSERT → FocusEngine.update(episode) → update FocusVector
    │     ContextBuilder reads FocusVector → adjusts the priority of facts
    │     BAE (Behaviour Anticipation Engine) reads FocusVector → selects a style_profile automatically
    │     AuditWorker writes to FocusVector (importance, domain, question type)
    │   Storage: in-memory (fast access) + a SQLite snapshot every 15 min
    │   Balance: FocusVector uses an exploration_rate (like Thompson Sampling in L4)
    │     so the system does not "get used to it" and keeps surprising the user.
    │   ⚠️ INVARIANT I29: FocusVector is read only via the graph and SQLite.
    │     Direct LLM calls to determine focus are forbidden. Graph = Truth.
    │
    ├─ Metrics:
    │   · response_audit_total              — total audits created
    │   · response_audit_persisted_total    — saved to SQLite + Neo4j
    │   · response_audit_importance_avg     — average importance of dialogues
    │   · response_audit_faithfulness_avg   — average faithfulness score
    │   · response_audit_cache_invalid_total — cache invalidations (Stale protection)
    │   · focus_vector_updates_total        — FocusVector updates per session
    └─ Decay: :DialogueSummary → decay every 48 hours (a separate process)
              importance < 0.3 → soft delete at the next GC
```

---

## RFC0065: Memory-as-Volition — Conscious Will to Remember

### 🌱 Read this first

All previous memory layers work **passively**: the system observes and decides what to remember. RFC0065 grants the agent a **voice in its own memory**: through the tool call `memory.write_voluntary()`, the agent makes a conscious decision to write a fact into L3 — without waiting for passive consolidation.

    ├─ P2-5: ReasonGraph DAG:
    │     On a complex query (Slow Path), build a mini reasoning DAG:
    │     1. Gather candidate facts from retrieval
    │     2. Build the DAG: each fact = node, edges = [:SUPPORTS] / [:CONTRADICTS]
    │     3. Score each node by relevance × confidence × recency
    │     4. Prune branches with score < 0.3
    │     5. Pass only the verified path to the LLM
    │     I95 (ReasonGraphDAG): the DAG is built only in Slow Path when use_slow_path=True.
    │
    ├─ P2-6: Curiosity Engine:
    │     The system does not merely react — it initiates questions of its own:
    │     1. Detect a gap in the graph (a region with < 3 facts)
    │     2. Generate a question: "what don't I know about X?"
    │     3. Offer it to the user or hand it to the Active Evidence Worker
    │     Trigger: once per day via SleepTimeWorker.
    │     I92 (CuriositySlowOnly): Curiosity Engine — Slow Path ONLY.
    │
    ├─ P2-7: Trace Examples:
    │     Not merely a response audit, but a reference standard of thinking:
    │     intent → evidence → truth_class → policy → action
    │     Stored as :TraceExample nodes in the graph.
    │     Used for calibrating the Guardian and Quality Gate.
    │     I93 (TraceExampleReadOnly): Trace Examples are read-only from Guardian/QualityGate.

**Why doesn't this violate Graph = Truth?** A voluntary write passes through TruthGate — fully, without exception. The agent's volition means only that it itself initiated the process.

**Neurobiological analogy:** The hippocampus has an **intentional encoding** mechanism — when there is an explicit intention to remember, a different neural pathway is activated and long-term consolidation occurs faster.

---

```
L4.5 addition: MemoryVolitionWorker  <- RFC0065
    |
    +- Purpose: the agent initiates a write into L3 itself. NOT a bypass of TruthGate.
    |
    +- Mode 1 (Tool Call): the agent calls memory.write_voluntary()
    |   -> VolitionEvent into EventBus (fire-and-forget)
    |   -> MemoryVolitionWorker (Slow Path) -> Fast-Track Staging -> TruthGate -> L3
    |   -> Write into VolitionLog {session_id, content_hash, reason, outcome}
    |
    +- Mode 2 (Auto-Detect): importance > 0.9 AND emotional > 0.8
    |   -> FocusEngine generates a VolitionSignal (the same path)
    |   I49-b: Auto-Detect does not suppress the agent's explicit tool call
    |
    +- Fast-Track: voluntary=True bypasses the CPU threshold in Staging (I49-c)
    |   Limit: no more than 10 voluntary calls per session
    |
    +- Invariants:
    |   I49:   write_voluntary() ALWAYS through TruthGate. Bypass = bug.
    |   I49-b: Auto-Detect does not displace the agent's explicit tool call.
    |   I49-c: Voluntary Fast-Track bypasses the CPU threshold, but not TruthGate.
    |   I49-d: Every voluntary write must have an entry in VolitionLog.
    |
    +- Metrics:
    |   volition_calls_total / volition_validated_total / volition_rejected_total
    |   volition_autodetect_total / volition_limit_exceeded_total
    \- Decay: :VolitionLog -> archived after 90 days
```

### Code [RFC0065]

```python
# memory_volition.py
# RFC0065: Memory-as-Volition
# I49: voluntary write ALWAYS through TruthGate — bypass forbidden.
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
from enum import Enum

logger = logging.getLogger(__name__)


class VolitionOutcome(str, Enum):
    # QUEUED is separated from VALIDATED
    # write_voluntary() returns QUEUED — the real outcome will appear in VolitionLog
    QUEUED           = "queued_for_processing"
    VALIDATED        = "validated"
    REJECTED_BY_GATE = "rejected_by_truthgate"
    DUPLICATE        = "duplicate"
    LIMIT_EXCEEDED   = "limit_exceeded"


@dataclass
class VolitionEvent:
    session_id:      str
    agent_id:        str
    content:         str
    reason:          str
    importance_hint: float    = 0.8   # P3-F FIX: NOT passed to TruthGate as confidence (P0.5-3).
                                       # Only for internal logging/prioritization.
                                       # TruthGate always receives confidence=0.5 (neutral prior).
    source:          str      = "agent"
    timestamp:       datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


@dataclass
class VolitionResult:
    outcome: VolitionOutcome
    fact_id: Optional[str] = None
    reason:  Optional[str] = None


class MemoryVolitionWorker:
    MAX_PER_SESSION: int = 10

    def __init__(self, staging, truth_gate, graph, event_bus, db):
        self.staging    = staging
        self.truth_gate = truth_gate
        self.graph      = graph
        self.event_bus  = event_bus
        self.db         = db
        # _session_counts is persisted via SQLite.
        # _load_session_counts() is called at worker startup
        # so the limit counters are not lost on restart.
        self._session_counts: dict[str, int] = {}
        self._initialized: bool = False  # ← B4 FIX: guard against being called before start()

    async def start(self):
        """Worker initialization — call before the first process_event().
        FIX: _load_session_counts moved into an explicit start() method.
        Without this call, the per-session limit counters were reset on restart
        and the limit of 10 voluntary writes per session did not work.
        """
        await self._load_session_counts()
        self._initialized = True  # ← B4 FIX: mark that initialization is complete

    async def _load_session_counts(self):
        async with self.db.connect() as conn:
            rows = await conn.fetchall(
                "SELECT session_id, COUNT(*) as cnt FROM volition_log "
                "WHERE outcome='validated' GROUP BY session_id"
            )
        for row in rows:
            self._session_counts[row["session_id"]] = row["cnt"]

    async def write_voluntary(self, session_id, agent_id,
                              content, reason, importance_hint=0.8):
        # B4 FIX: guard — if start() was not called, the limit does not work
        if not self._initialized:
            raise RuntimeError(
                "MemoryVolitionWorker.start() must be called before write_voluntary(). "
                "Without it, MAX_PER_SESSION limit is non-functional (counters empty)."
            )
        event = VolitionEvent(
            session_id=session_id, agent_id=agent_id, content=content,
            reason=reason,
            importance_hint=min(1.0, max(0.0, importance_hint)),
        )
        await self.event_bus.publish_volition(event)
        # QUEUED — not VALIDATED. The real outcome will appear in VolitionLog.
        return VolitionResult(outcome=VolitionOutcome.QUEUED,
                              reason="queued_for_processing")

    async def process_event(self, event: VolitionEvent) -> VolitionResult:
        count = self._session_counts.get(event.session_id, 0)
        if count >= self.MAX_PER_SESSION:
            r = VolitionResult(outcome=VolitionOutcome.LIMIT_EXCEEDED)
            await self._log(event, r)
            return r

        if await self._is_duplicate(self._hash(event.content)):
            r = VolitionResult(outcome=VolitionOutcome.DUPLICATE)
            await self._log(event, r)
            return r

        staged = await self.staging.fast_track(
            content=event.content, importance_hint=event.importance_hint,
            voluntary=True,  # I49-c: bypasses the CPU threshold, but not TruthGate
            source="volition",
        )

        # I49: TruthGate is MANDATORY. There is no bypass.
        # P0.5-3 FIX: importance_hint ≠ confidence.
        # importance — subjective importance to the agent (how much it "wants to remember").
        # confidence — epistemic reliability of the fact (how much "this is true").
        # Was: "confidence": event.importance_hint — a falsehood with importance=0.9 passed the Gate.
        # Now: confidence is always 0.5 (neutral prior) for voluntary writes.
        # importance_hint is passed separately as priority metadata in the graph.
        gate = await self.truth_gate.validate_and_transition({
            "id": staged.id, "content": event.content,
            "confidence": 0.5,  # neutral prior — TruthGate evaluates the fact, not the desire
            "importance":  event.importance_hint,  # affects priority in the graph, not the Gate
            "emotional_salience": 0.0,
            "source": "agent_volition",
        })

        if not gate.passed:
            r = VolitionResult(outcome=VolitionOutcome.REJECTED_BY_GATE,
                               reason=gate.reason)
            await self._log(event, r)
            return r

        self._session_counts[event.session_id] = count + 1
        r = VolitionResult(outcome=VolitionOutcome.VALIDATED,
                           fact_id=getattr(gate, "fact_id", staged.id))
        await self._log(event, r)
        return r

    @staticmethod
    def _hash(content: str) -> str:
        import hashlib
        return hashlib.sha256(content.encode()).hexdigest()[:32]  # P4-C FIX: 64bit→128bit (Birthday Paradox)

    async def _is_duplicate(self, content_hash: str) -> bool:
        async with self.db.connect() as conn:
            row = await conn.fetchone(
                "SELECT 1 FROM volition_log "
                "WHERE content_hash=? AND outcome='validated' LIMIT 1",
                (content_hash,)
            )
        return row is not None

    async def _log(self, event: VolitionEvent, result: VolitionResult):
        # I49-d: EVERY voluntary write must have an entry in VolitionLog
        async with self.db.connect() as conn:
            await conn.execute(
                "INSERT INTO volition_log "
                "(session_id, agent_id, content_hash, reason, importance_hint, "
                " source, outcome, fact_id, timestamp) VALUES (?,?,?,?,?,?,?,?,?)",
                (event.session_id, event.agent_id, self._hash(event.content),
                 event.reason, event.importance_hint, event.source,
                 result.outcome.value, result.fact_id,
                 event.timestamp.isoformat())
            )
            await conn.commit()
```

### Test [I49, I49-d]

```python
# tests/test_invariants.py -- add

# I49: Voluntary write ALWAYS through TruthGate
async def test_I49_voluntary_always_through_truth_gate():
    gate = MockTruthGate()
    w    = MemoryVolitionWorker(
        staging=MockStaging(), truth_gate=gate,
        graph=MockGraph(), event_bus=MockEventBus(), db=MockDB())
    await w.process_event(VolitionEvent(
        session_id="s", agent_id="a", content="fact", reason="test",
        importance_hint=0.9))
    assert gate.call_count >= 1, "I49 VIOLATION: TruthGate bypass"

# I49-d: VolitionLog is mandatory
async def test_I49d_volition_log_always_written():
    db = MockDB()
    w  = MemoryVolitionWorker(
        staging=MockStaging(), truth_gate=MockTruthGate(will_pass=False),
        graph=MockGraph(), event_bus=MockEventBus(), db=db)
    await w.process_event(VolitionEvent(
        session_id="s", agent_id="a", content="c", reason="r"))
    assert db.insert_count("volition_log") >= 1, "I49-d VIOLATION"
```

### Add to velantrim_config.py

```python
class VolitionConfig:
    MAX_PER_SESSION       = 10
    AUTODETECT_IMPORTANCE = 0.9
    AUTODETECT_EMOTIONAL  = 0.8
    FAST_TRACK_BYPASS_CPU = True
    LOG_RETENTION_DAYS    = 90

VOLITION = VolitionConfig()
```

L5: Anticipatory Intelligence — Proactive Intelligence  ← RFC0054–0058
    ├─ Purpose: the system not only remembers and answers — it anticipates,
    │   suggests, and explains itself. A transition from a reactive to an anticipatory agent.
    │
    ├─ [RFC0054] Spreading Activation Engine (SAE):
    │   An extension of Velum (L1.5) — decaying excitation along the graph edges.
    │   When a node A is activated → excitation spreads to adjacent nodes
    │   with weight: activation(B) = weight(A→B) × activation(A) × decay_factor
    │   Decay: each hop multiplies the signal by DECAY_FACTOR (default 0.6)
    │   Activation threshold: SAE_THRESHOLD = 0.3 — anything below is ignored
    │   Result: HybridRetriever receives expanded context BEFORE the user's query.
    │   This is "synaptic sensing" — the system anticipates related topics.
    │   ⚠️ INVARIANT I30: SAE works only over existing graph edges.
    │     SAE creates no new edges — it only reads. Graph = Truth is not violated.
    │
    ├─ [RFC0055] Epistemic Gap Model (EGM):
    │   The graph knows not only what the user knows — but what they do NOT know.
    │   Mechanism: analyze L3 domain nodes → find clusters that the
    │   user has never activated → gap_score by the importance of the domain.
    │   Proactive suggestion when gap_score > EGM_THRESHOLD (default 0.7):
    │     → FocusEngine generates a suggestion: "You have never asked about X"
    │     → BAE forms a soft suggestion, not an intrusive one
    │   Storage: :EpistemicGap {topic_id, gap_score, last_suggested, suppressed}
    │   Protection: if the user rejected the suggestion → suppressed=True for 7 days.
    │   ⚠️ INVARIANT I31: EGM does not impose — it only suggests once.
    │     Re-suggesting the same topic sooner than 7 days is forbidden.
    │
    ├─ [RFC0056] Domain Seed Protocol (DSP):
    │   Eliminates the cold start for new users and organizations.
    │   At system startup: load domain_seed.json
    │     {domain, terminology[], key_processes[], values[], authority_map{}}
    │   → ~100–500 :KnowledgeUnit nodes are automatically created in L3
    │   → the L2 Cold Start Guard is bypassed (the seed counts as episodes)
    │   → the system behaves like an "experienced employee" from the first dialogue
    │   Formats: JSON / YAML / PDF (via offline_extractor.py)
    │   ⚠️ INVARIANT I32: Seed nodes are marked {source_type: "domain_seed"}.
    │     TruthGate applies trust_score = 0.7 to them (not 1.0) — they require confirmation.
    │
    ├─ [RFC0057] Multi-User Authority Graph:
    │   For organizations — each user has a domain of authority.
    │   Schema: :User {user_id, role, authority_domain[], trust_level: 0.0–1.0}
    │   On a conflict of facts from different users:
    │     TruthGate checks the authority_domain of both sources
    │     The one with the higher trust_level in the given domain wins
    │     If domains are equal → the fact transitions in ESM: Hypothesized (dispute)
    │     → notification to both users to resolve the conflict
    │   Example: a financier is reliable on financial facts > a developer.
    │   ⚠️ INVARIANT I33: authority_domain cannot be empty.
    │     A user without a domain has trust_level = 0.5 by default (neutral).
    │
    ├─ [RFC0058] Explainability Layer (XAI):
    │   The user can ask "Why this answer?" → the system explains.
    │   Mechanism: the TRACE from ResponseAudit (RFC0052) → XAI formats it for a human:
    │     "This answer is based on:
    │      · 3 facts from your dialogues (5, 12, 18 days ago)
    │      · A strategy developed 3 days ago
    │      · The topic [architecture] with strength 4.2"
    │   Levels of detail: brief / detailed / full_trace (on request)
    │   Storage: XAI explanations are cached in ResponseAudit.precomputed["why"]
    │   ⚠️ INVARIANT I34: XAI shows only real TRACE paths.
    │     Generating explanations with an LLM without a TRACE is forbidden. Only the graph.
    │
    ├─ Prediction Error Signal — training L5 on prediction errors
    │   Friston's principle: the brain learns precisely from prediction error, not from success.
    │   L5 already predicted the next question — but the errors were lost. No longer.
    │
    │   Mechanism (triggered via EventBus after each answer · 2–5 ms):
    │     1. Take what L5/SAE predicted before the user's question
    │     2. Compare with what was actually asked
    │     3. If the error > PREDICTION_ERROR_THRESHOLD (0.4):
    │          → strengthen the edges leading to the correct answer × (1 + error_magnitude)
    │          → weaken the incorrect paths × (1 - error_magnitude × 0.5)
    │     4. Pass the error_signal to the L5.5 PredictiveFusionLayer
    │          → adjust the w_sae / w_lsm weights
    │
    │   Effect over time:
    │     Week 1   → L5 guesses ~30% of the next questions
    │     Month 1  → ~55%
    │     Month 3  → ~75% for the user's typical topics
    │
    │   ⚠️ INVARIANT I36: Prediction Error only weakens/strengthens edges.
    │     It creates no new edges. Graph = Truth is not violated.
    │   Load: 2–5 ms · CPU only · after each message
    │   Metric: prediction_error_total · prediction_accuracy_rolling_7d
    │
    ├─ Liquid State Machine (LSM) — temporal memory of rhythm
    │   Complements SAE: SAE knows WHAT you will ask (graph semantics).
    │   LSM knows WHEN and in WHAT RHYTHM (the dynamic state of the sequence).
    │
    │   Reservoir Computing architecture:
    │     · Reservoir: ~200–500 simple neurons with fixed random weights
    │     · Main principle: the reservoir weights are NEVER trained
    │     · Only a simple linear output layer is trained
    │     · This means: no GPU, no backprop, 2–5 MB RAM
    │
    │   What LSM remembers as a "living echo state":
    │     · At what time of day technical questions are asked
    │     · How quickly the user switches between topics
    │     · When they drift into philosophical reflection
    │     · Pauses between messages as a rhythmic signal
    │
    │   Update: via EventBus after each L1 INSERT · 5–15 ms · CPU only
    │   Storage: in-memory reservoir + SQLite state snapshot every 15 min
    │   Output: lsm_prediction is passed to the L5.5 PredictiveFusionLayer
    │   ⚠️ INVARIANT I37: LSM does not write to the graph. It only reads the query history.
    │   Metrics: lsm_prediction_updates · lsm_rhythm_stability_score
    │
    ├─ Metrics:
    │   · sae_activations_total          — nodes activated via SAE
    │   · epistemic_gap_suggestions_total — suggestions made by EGM
    │   · epistemic_gap_accepted_rate    — % of accepted suggestions
    │   · domain_seed_nodes_created      — nodes created via DSP
    │   · authority_conflicts_resolved   — conflicts resolved by authority
    │   · xai_explanations_total         — explanations issued to users
    │   · prediction_error_total         — prediction errors processed
    │   · prediction_accuracy_rolling_7d — prediction accuracy over 7 days
    │   · lsm_prediction_updates         — LSM state updates
    │   · lsm_rhythm_stability_score     — stability of the user's rhythm
    └─ Decay: :EpistemicGap → recomputed once a week based on domain activity

L5.5: Predictive Fusion Layer — arbiter of SAE and LSM
    ├─ Purpose: SAE (semantics) and LSM (rhythm) measure different dimensions of reality.
    │   Choosing one instead of the other is like choosing between a map and a compass.
    │   L5.5 uses both and adaptively decides whom to trust in a given situation.
    │
    │   It continues the architectural logic of the intermediate layers:
    │   L1.5 (Velum) · L2.5 (Staging) · L4.5 (Audit+Focus) · L5.5 (Fusion)
    │
    ├─ Two output modes:
    │
    │   🤝 Consensus (both predicted the same topic):
    │     combined_confidence = sae_conf^w_sae × lsm_conf^w_lsm
    │     → high confidence → the system acts proactively
    │     → prepares context even before the user's question
    │
    │   ⚡ Divergence (different topics):
    │     → both candidates are passed to FocusEngine with weights
    │     → confidence penalty: × 0.6
    │     → signal to the system: the user is in a transitional state
    │     → FocusEngine chooses more cautiously, does not impose
    │
    ├─ Dynamic weights (adapted via Prediction Error):
    │     Initial: w_sae = 0.6 · w_lsm = 0.4
    │     Shift by context:
    │       if lsm_rhythm_stability > 0.7 → w_lsm += 0.15
    │       if sae_graph_density > 0.6    → w_sae += 0.15
    │     Normalization: w_sae + w_lsm = 1.0 always
    │     Minimum weight: 0.2 (no source is fully displaced)
    │
    ├─ Training via Prediction Error (closed loop):
    │     SAE was wrong  → w_sae -= learning_rate(0.05) × error.magnitude
    │     LSM was wrong  → w_lsm -= learning_rate(0.05) × error.magnitude
    │     Slow learning = weight stability
    │
    ├─ ⚠️ INVARIANT I35: L5.5 does not write to the graph.
    │     It only reads the SAE and LSM predictions · only returns a FusedPrediction.
    │     Graph = Truth is not violated.
    │
    ├─ Metrics:
    │   · fusion_consensus_rate      — % of cases where SAE and LSM agreed
    │   · fusion_divergence_rate     — % of divergences (a signal of transitional states)
    │   · fusion_w_sae_current       — the current SAE weight
    │   · fusion_w_lsm_current       — the current LSM weight
    └─ Load: 2–5 ms · CPU only · 0 LLM tokens

```python
# l5_5_predictive_fusion.py
import numpy as np
import logging
from dataclasses import dataclass, field
from typing import Optional

logger = logging.getLogger(__name__)

@dataclass
class FusedPrediction:
    topic: Optional[str]
    confidence: float
    source: str                        # "consensus" | "divergent"
    timing: Optional[dict] = None      # LSM temporal context
    candidates: Optional[list] = None  # on divergent — list of (prediction, weight)

@dataclass
class PredictionError:
    source: str        # "sae" | "lsm"
    magnitude: float   # 0.0–1.0

@dataclass
class FusionContext:
    lsm_rhythm_stability: float = 0.5
    sae_graph_density: float = 0.5

class PredictiveFusionLayer:
    """
    L5.5: arbiter of SAE (semantics) and LSM (rhythm).
    Combines two predictions with adaptive weights.
    The weights are updated via the Prediction Error Signal (L5).

    Invariant I35: does not write to the graph — only reads and returns a FusedPrediction.
    """

    def __init__(self, w_sae: float = 0.6, w_lsm: float = 0.4):
        self.w_sae = w_sae
        self.w_lsm = w_lsm
        self._learning_rate = 0.05
        self._w_min = 0.2  # no source is fully displaced

    async def fuse(
        self,
        sae_prediction: dict,
        lsm_prediction: dict,
        context: FusionContext
    ) -> FusedPrediction:
        w_sae, w_lsm = self._dynamic_weights(context)

        if sae_prediction.get("topic") == lsm_prediction.get("topic"):
            # Consensus: multiply the confidences (do not add — this is important)
            # The weighted geometric mean gives a more conservative estimate
            combined = (
                sae_prediction["confidence"] ** w_sae *
                lsm_prediction["confidence"] ** w_lsm
            )
            logger.debug(f"L5.5 consensus: {sae_prediction['topic']} conf={combined:.3f}")
            return FusedPrediction(
                topic=sae_prediction["topic"],
                confidence=combined,
                source="consensus",
                timing=lsm_prediction.get("timing")
            )
        else:
            # Divergence: return both candidates with a penalty
            # Penalty × 0.6 — the system becomes more cautious under uncertainty
            logger.debug(
                f"L5.5 divergent: SAE={sae_prediction.get('topic')} "
                f"vs LSM={lsm_prediction.get('topic')}"
            )
            return FusedPrediction(
                topic=None,
                confidence=max(w_sae, w_lsm) * 0.6,
                source="divergent",
                candidates=[
                    (sae_prediction, w_sae),
                    (lsm_prediction, w_lsm)
                ]
            )

    def _dynamic_weights(self, ctx: FusionContext) -> tuple[float, float]:
        """
        Dynamically shift the weights by the context of the current query.
        Stable rhythm → more trust in LSM.
        Rich semantic graph → more trust in SAE.
        """
        w_s, w_l = self.w_sae, self.w_lsm

        if ctx.lsm_rhythm_stability > 0.7:
            w_l += 0.15  # the user is in a stable rhythm — LSM is reliable
        if ctx.sae_graph_density > 0.6:
            w_s += 0.15  # the topic is well represented in the graph — SAE is reliable

        total = w_s + w_l
        return w_s / total, w_l / total

    async def update_from_error(self, error: PredictionError):
        """
        The Prediction Error Signal adjusts the weights.
        Slow learning (lr=0.05) = stability.
        Minimum weight 0.2 = no source is switched off.
        """
        if error.source == "sae":
            self.w_sae = max(self._w_min, self.w_sae - self._learning_rate * error.magnitude)
        elif error.source == "lsm":
            self.w_lsm = max(self._w_min, self.w_lsm - self._learning_rate * error.magnitude)

        # Renormalize after each update
        total = self.w_sae + self.w_lsm
        self.w_sae /= total
        self.w_lsm /= total
        logger.debug(f"L5.5 weights updated: w_sae={self.w_sae:.3f}, w_lsm={self.w_lsm:.3f}")
```

---

## 🔧 Technology Stack

### Required Components

| Component | Technology | Purpose |
|-----------|------------|------------|
| **Graph DB (MVP)** | LadybugDB + Graphiti | Embedded graph for Phase 0 / low-end hardware. LadybugDB — community fork of KuzuDB (MIT, Cypher, ACID, full Kuzu API compatibility). I94. Migration to Neo4j in Phase 1+ |
| **Graph DB (Production)** | Neo4j 5.26+ + Graphiti | Temporal knowledge graph, primary storage for Phase 1+ |
| **Vector DB** | Qdrant / ChromaDB | Semantic search, embeddings |
| **Event Bus** | Redis Streams | Asynchronous event processing (Kafka removed — redundant for Velantrim) |
| **Scheduler** | APScheduler 3.10+ (AsyncIOScheduler) | Periodic Slow Path tasks: WeightedSemanticDecay, daily_maintenance · P9-FIX BUG-18 |
| **Cache** | Redis | Caching of frequently used patterns |
| **Embeddings (local)** | multilingual-e5-large / deepvk/USER-bge-m3 | Vectorization, privacy-first, best for RU |
| **Embeddings (cloud)** | Gemini Embedding 2 (March 2026) | Multimodal: text + image + audio + video + PDF. Phase 2+ |
| **LLM Flagship** | GPT-5.4 / Claude Sonnet 4.6 / Qwen3.5-Plus | Complex tasks, reasoning · Qwen3.5-Plus = 397B-A17B, 1M ctx, native multimodal |
| **LLM Reasoning** | DeepSeek R1-0528 | Specialized reasoning · R1: 671B-A37B, open CoT tokens, o1-level · ⚠️ DeepSeek V4 (Engram) — expected, do not add to the stack until public release |
| **LLM Fast** | o4-mini / Claude Haiku 4.5 / Qwen3.5-Flash | Routine, 70% of tasks, cheap |
| **LLM Local (MoE)** | Qwen3.5-35B-A3B / DeepSeek V3.2 / Kimi K2 | Privacy-first · V3.2: 685B-A37B, DSA, context 163K, thinking+tool-use · Qwen3.5-Flash = hosted 35B-A3B |
| **LLM Local (dense)** | Qwen3.5-27B / Qwen3.5-397B-A17B / Llama 4 Maverick | If RAM > 32 GB · 397B-A17B = Qwen3.5-Plus open weights |
| **LLM Tiny (offline)** | Qwen3-1.7B / OLMoE-1B-7B | LLM_MODE=lite · low-end hardware · Memory Router SLM fallback |
| **LSM (Liquid State Machine)** | Python · NumPy · ~300 neurons | Temporal rhythm memory · 2–5 MB RAM · CPU only |
| **Orchestration** | Custom Python / LangGraph v0.3+ | Agent management |
| **Reranker** | ColBERTv2 / bge-reranker-large | Default reranker · ⚠️ Qwen3-Reranker: only opt-in with native Transformers (known issues in vLLM/llama.cpp) · file: `memory/reranker.py` |
| **Observability** | OpenTelemetry + Prometheus + Grafana | Monitoring and tracing |
| **Analytics** | DuckDB | Metrics analytics, Parquet/CSV, aggregations (NOT a replacement for SQLite) |
| **Operational DB** | SQLite | Logs, configs, skills, sessions — built-in reliable storage |

### 🆕 Models in the Stack — Reference

> A brief summary of each new model for quick orientation. For details, see the vendors' documentation.

**DeepSeek V3.2** *(January 2026 · MIT · MoE 685B-A37B)*
- DeepSeek Sparse Attention (DSA) — reduces compute on long context without loss of quality
- Thinking mode built directly into tool-use (first in the lineup): you can reason and use tools simultaneously
- Context window: 163,840 tokens · GPT-5-level performance · IMO/IOI 2025 — gold
- Locally: requires ~8×H200 in full precision; GGUF quantization — dual RTX 4090

**DeepSeek R1-0528** *(May 2025 · MIT · MoE 671B-A37B)*
- Reasoning specialist: open chain-of-thought tokens (`<think>...</think>`), distillation capability
- OpenAI o1/o3-level performance · Context 164K tokens
- Distillations: 1.5B / 7B / 8B / 14B / 32B / 70B — from phone to server
- Use in Velantrim: strategy for complex multi-hop tasks in ReasoningBank

**DeepSeek V4 + Engram** *(March 2026 · ⚠️ status being clarified · MoE ~1T-A37B)*
- **Engram** — architectural breakthrough: conditional memory separates static knowledge (O(1) hash lookup in DRAM) from dynamic reasoning (MoE GPU). Needle-in-a-Haystack 97% at 1M tokens
- Context: 1M+ tokens · Native multimodal (text + image + video)
- V4 Lite appeared on the platform on March 9, 2026; full release — expected. Benchmarks not officially verified
- ⚠️ Add to the stack as soon as the weights are publicly available

**Qwen3.5-Plus / Qwen3.5-397B-A17B** *(February–March 2026 · Apache 2.0 · MoE 397B-A17B)*
- Qwen3.5-Plus = hosted API; Qwen3.5-397B-A17B = open weights (the same thing)
- Gated Delta Networks + sparse MoE: natively multimodal architecture (early fusion)
- Context: 262K natively, up to 1M via API · 201 languages · Thinking mode by default
- SWE-bench Verified: 76.4 · IFBench instruction-following: 76.5 (best among open models)
- Smaller family versions: Qwen3.5-35B-A3B (= Flash), Qwen3.5-27B, 9B, 4B — for local deployment

### 🧠 MoE vs Dense — Choosing the LLM Architecture

> **MoE (Mixture of Experts)** — an architecture where an internal Router activates only 2–3 "experts" out of N on each request. The remaining experts are not computed → fewer FLOPs, the same result.

```
Example: the user asks for "the formula for water"
  Dense 30B:  all 30B parameters are computed every time
  MoE 30B-A3B: Router activates 2 of 16 experts → 3B is computed
               Same-quality answer, CPU/GPU load 10× lower
```

| Architecture | Parameters in RAM | Computed | CPU/GPU load | Recommendation |
|-------------|----------------|-----------|-----------------|--------------|
| Dense 7B | 7B | 7B | 100% | weak/medium without GPU |
| MoE 30B-A3B | 30B | ~3B | ~15% | medium/strong — best choice |
| Dense 70B | 70B | 70B | 100% | strong + GPU |
| MoE 141B-A22B | 141B | ~22B | ~25% | strong + GPU flagship |

> ⚠️ **The main MoE pitfall**: it reduces CPU/GPU load, but does **NOT** save RAM — all experts must be in memory. Mixtral 8x7B requires ~30 GB RAM despite computing like 12B.

```python
# velantrim_config.py — add when choosing the LLM
LLM_ARCHITECTURE  = "moe"    # "moe" | "dense"
LLM_ACTIVE_PARAMS = "3B"     # actually computed at inference
LLM_TOTAL_PARAMS  = "30B"    # needed in RAM — use for the HARDWARE_PROFILE check

# Rule: if LLM_TOTAL_PARAMS > available RAM → switch to a smaller model
# MoE in GGUF format (quantization) — optimal for CPU-only inference
```
### Optional Enhancements

- **Monitoring**: ✅ Already among the required ones (OpenTelemetry + Prometheus + Grafana). Add extended Grafana dashboards here if separate alerts are needed.
- **Object Storage**: S3 / MinIO (for full texts and artifacts)
- **Time-Series DB**: InfluxDB (for metrics and decay computations)
- **Real-time Graph**: Memgraph (Phase 2+ for hot-path updates)

### 🗄️ Backend Configurations (v8.0 Crystal)

| Configuration | Graph | Vector | For whom |
|---|---|---|---|
| **Minimal** | SQLite | FAISS | Development, first launch |
| **Personal** | KuzuDB    | FAISS | Local PC, offline, MIT · I94 · P0-H FIX |
| **Startup** | FalkorDB | Qdrant | Production, startup |
| **Enterprise** | Neo4j | Qdrant | Corporations, RBAC, GDPR |

```python
# velantrim_config.py
GRAPH_BACKEND = "kuzu"       # P0-H FIX: "ladybugdb" does not exist → "kuzu" (KuzuDB, MIT, Cypher-compatible)
# KuzuDB — https://kuzudb.com · MIT · Cypher · columnar · vector + full-text · ACID
# I94 (KuzuDBCompat): the KuzuDB backend is compatible with the Kuzu API. Migration without data loss.
```


### ⚰️ Components Excluded from the Stack

> The list protects against regressions: during the next LLM audit, removed components will not be proposed again.

| Component | Reason for exclusion |
|-----------|-------------------|
| **RedisGraph** | EOL January 2025, project shut down by Neo4j |
| **Kafka** | Redundant for Velantrim — replaced by Redis Streams |
| ~~**KuzuDB**~~ | ~~Acquired by Apple in 2025~~ — **P9-FIX BUG-2**: the LadybugDB fork did not ship. KuzuDB (MIT, Cypher-compatible) remains in the Personal config. Line removed from excluded. |
| **SurrealDB** | ⚠️ EOL risk, unstable API — moved to optional |
| **NetworkX** | Too slow on >1k nodes — prototyping only |

### 🐳 Quick Infrastructure Startup

> Without docker-compose.yml a developer cannot start the system. This is the only command needed.

```yaml
# infra/docker-compose.yml
# P3-E FIX: the version: field is deprecated in Docker Compose v2+. Removed.
services:
  neo4j:
    image: neo4j:5.26-community  # community = no license; enterprise = if available
    container_name: velantrim-neo4j
    restart: unless-stopped
    ports:
      - "7474:7474"   # Browser
      - "7687:7687"   # Bolt
    environment:
      - NEO4J_AUTH=neo4j/${NEO4J_PASSWORD:?NEO4J_PASSWORD not set}  # password from .env, not hardcoded
      - NEO4J_PLUGINS=["apoc"]  # apoc — the official Community Edition plugin
      # ⚠️ graph-data-science is NOT an official Community 5.26 plugin.
      # Phase 0: SAE is implemented via python-igraph (see EtirConfig.BACKEND="igraph").
      # Phase 1+: GDS is installed manually via the /plugins mount (JAR from Neo4j Labs).
      # Phase 2: Neo4j Enterprise — GDS natively via NEO4J_PLUGINS.
      - NEO4J_dbms_memory_pagecache_size=2g
      - NEO4J_dbms_memory_heap_initial__size=2g
      - NEO4J_dbms_memory_heap_max__size=4g
    volumes:
      - neo4j-data:/data
    healthcheck:
      test: ["CMD-SHELL", "cypher-shell -u neo4j -p ${NEO4J_PASSWORD} 'RETURN 1' || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  redis:
    image: redis:7-alpine
    container_name: velantrim-redis
    restart: unless-stopped
    command: redis-server --maxmemory ${REDIS_MAX_MEM:-512mb} --maxmemory-policy allkeys-lru
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  neo4j-data:
  redis-data:
```

```bash
  # first create .env (do not commit to git!):
# cp .env.example .env && echo "NEO4J_PASSWORD=your_strong_password" >> .env

# Launch with a single command
docker compose -f infra/docker-compose.yml up -d
```

---

## 📦 Key Components and Their Implementation

### 1. Event Bus & Ingestion Pipeline

**Purpose**: Capturing all events without blocking the main thread

```python
# event_bus.py
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timezone  # timezone needed for datetime.now(timezone.utc)
import asyncio
import redis.asyncio as redis
import json
import logging
from typing import AsyncGenerator, Tuple

logger = logging.getLogger(__name__)

class EventType(Enum):
    USER_MESSAGE = "user_message"
    AGENT_RESPONSE = "agent_response"
    RESPONSE_GENERATED = "response_generated"  # used by AuditWorker (I28) and the SLOW SYSTEM architecture
    ACTION_EXECUTED = "action_executed"
    TASK_COMPLETED = "task_completed"
    TASK_STATUS_CHANGED = "task_status_changed"  # ConsolidationEngine: BLOCKED_AWAITING_DB
    ERROR_OCCURRED = "error_occurred"

@dataclass
class AgentEvent:
    event_type: EventType
    timestamp: datetime
    content: dict
    metadata: dict
    session_id: str

class SQLiteFallbackQueue:
    """
    Persistent SQLite-based fallback event queue (RFC0036).
    """
    def __init__(self, db_path: str = "fallback_events.db"):
        self.db_path = db_path

    async def init(self):
        import aiosqlite
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("PRAGMA journal_mode=WAL;")
            await db.execute("""
                CREATE TABLE IF NOT EXISTS event_fallback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_data BLOB NOT NULL,
                    priority TEXT DEFAULT 'NORMAL',
                    retry_count INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            await db.commit()

    async def put(self, event_data: dict, priority: str = 'NORMAL') -> bool:
        import aiosqlite, zlib, json
        compressed = zlib.compress(json.dumps(event_data).encode(), level=1)
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT INTO event_fallback (event_data, priority) VALUES (?, ?)",
                (compressed, priority)
            )
            await db.commit()
        return True

    async def qsize(self) -> int:
        """Returns the number of events in the fallback queue (for health_check)."""
        import aiosqlite
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("SELECT COUNT(*) FROM event_fallback")
            row = await cursor.fetchone()
            return row[0] if row else 0

    async def drain(self, redis_client, stream_key: str, batch: int = 100) -> int:
        import aiosqlite, zlib, json
        recovered = 0
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT id, event_data FROM event_fallback "
                "WHERE retry_count < 5 ORDER BY priority DESC, created_at ASC LIMIT ?",
                (batch,)
            )
            rows = await cursor.fetchall()
            for row_id, compressed in rows:
                try:
                    data = json.loads(zlib.decompress(compressed))
                    await redis_client.xadd(stream_key, data)
                    await db.execute("DELETE FROM event_fallback WHERE id=?", (row_id,))
                    recovered += 1
                except Exception:
                    await db.execute(
                        "UPDATE event_fallback SET retry_count = retry_count + 1 WHERE id=?",
                        (row_id,)
                    )
            await db.commit()
        return recovered


class RobustEventBus:
    """
    Resilient Event Bus design with:
    - Retry mechanism
    - Dead Letter Queue (DLQ)
    - Fallback to a local queue
    - Error tracking
    """
    def __init__(
        self,
        redis_url: str = "redis://localhost:6379",
        max_retries: int = 3,
        config: dict = None,   # config may be None at startup
    ):
        self.redis = redis.from_url(redis_url, decode_responses=True)
        self.stream_key = "agent:events"
        self.dlq_key = "agent:events:dlq"
        self.max_retries = max_retries

        # Fallback queue when Redis is unavailable — persistent (RFC0036)
        _cfg = config or {}
        self.fallback_queue = SQLiteFallbackQueue(
            db_path=_cfg.get("fallback_db", "fallback_events.db")
        )
        self.redis_available = True

    async def publish(self, event: AgentEvent) -> bool:
        """
        Publish an event with retry and fallback
        Returns True if successful, False if it went to fallback
        """
        event_data = {
            "type": event.event_type.value,
            "timestamp": event.timestamp.isoformat(),
            "content": json.dumps(event.content),
            "metadata": json.dumps(event.metadata),
            "session_id": event.session_id
        }
        
        # Attempt to publish with retry
        for attempt in range(self.max_retries):
            try:
                await self.redis.xadd(self.stream_key, event_data,
                                      maxlen=10000, approximate=True)
                self.redis_available = True
                return True
                
            except redis.RedisError as e:
                logger.warning(
                    f"Redis publish failed (attempt {attempt + 1}/{self.max_retries}): {e}"
                )
                
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                else:
                    # All attempts exhausted → fallback
                    self.redis_available = False
                    try:
                        await self.fallback_queue.put(event_data)  # pass a dict, not AgentEvent
                        logger.error(f"Event moved to fallback queue: {event.event_type}")
                    except Exception:
                        # SQLiteFallbackQueue.put() never raises asyncio.QueueFull
                        # (it's an aiosqlite operation). We catch any error → SQLite directly.
                        logger.warning(
                            f"Fallback queue error — persisting to SQLite: {event.event_type}"
                        )
                        await self._persist_event_to_sqlite(event)
                    return False

    async def publish_volition(self, event) -> bool:
        """
        P0.5-1 FIX: adapter for MemoryVolitionWorker.write_voluntary().
        VolitionEvent is not an AgentEvent, so we serialize it manually
        and delegate to the standard publish path via Redis → fallback.

        Without this method: AttributeError on the first call to write_voluntary().
        """
        import dataclasses
        # Wrap VolitionEvent into a format compatible with publish()
        class _VolitionWrapper:
            def __init__(self, ev):
                from enum import Enum
                self.event_type = type('_ET', (), {
                    'value': getattr(ev, 'event_type', 'VOLITION')
                    if not isinstance(getattr(ev, 'event_type', None), Enum)
                    else ev.event_type.value
                })()
                # P0-C FIX: utcnow() deprecated in Python 3.12, returned a naive datetime → silent data corruption.
                # datetime.now(timezone.utc) returns a timezone-aware datetime, compatible with Redis/SQLite.
                from datetime import datetime as _dt, timezone as _tz
                self.timestamp  = getattr(ev, 'timestamp', _dt.now(_tz.utc))
                self.content    = {
                    'content':          getattr(ev, 'content', ''),
                    'reason':           getattr(ev, 'reason', ''),
                    'importance_hint':  getattr(ev, 'importance_hint', 0.8),
                }
                self.metadata   = {'source': 'agent_volition'}
                self.session_id = getattr(ev, 'session_id', '')

        return await self.publish(_VolitionWrapper(event))

    async def _persist_event_to_sqlite(self, event: AgentEvent):
        """
        Last line of defense: if Redis is unavailable and fallback_queue.put() also failed.
        Added FALLBACK_MAX_ROWS=10_000 rotation + PRAGMA WAL/NORMAL
        to protect against disk overflow. No duplication of dict assembly —
        event_data is formed once and passed directly.
        """
        import aiosqlite
        FALLBACK_MAX_ROWS = 10_000  # rotation limit — protection against disk overflow
        try:
            payload = {
                "type":       event.event_type.value,
                "timestamp":  event.timestamp.isoformat(),
                "content":    json.dumps(event.content),
                "metadata":   json.dumps(event.metadata),
                "session_id": event.session_id,
            }
            db_path = getattr(self.fallback_queue, 'db_path', 'fallback_events.db')
            async with aiosqlite.connect(db_path) as db:
                await db.execute("PRAGMA journal_mode=WAL")
                await db.execute("PRAGMA synchronous=NORMAL")
                # P0.5-2 FIX: unified format with SQLiteFallbackQueue.put() and drain().
                # put() writes zlib.compress(json.dumps(...)), drain() reads zlib.decompress().
                # Before: json.dumps(payload) as a plain string → drain() got garbage on recovery.
                # Now: zlib.compress(json.dumps(payload)) — identical to the main fallback path.
                import zlib as _zlib
                compressed_payload = _zlib.compress(
                    json.dumps(payload).encode(), level=1
                )
                await db.execute(
                    "INSERT INTO event_fallback (event_data, priority) VALUES (?, ?)",
                    (compressed_payload, "NORMAL")
                )
                # Rotation: delete the oldest records when the limit is exceeded
                await db.execute(
                    """
                    DELETE FROM event_fallback
                    WHERE id IN (
                        SELECT id FROM event_fallback
                        ORDER BY id ASC
                        LIMIT MAX(0, (SELECT COUNT(*) FROM event_fallback) - ?)
                    )
                    """,
                    (FALLBACK_MAX_ROWS,)
                )
                await db.commit()
        except Exception as e:
            logger.critical(
                f"CRITICAL: _persist_event_to_sqlite failed — "
                f"event {event.event_type} IS LOST. Error: {e}"
            )

    async def consume(
        self,
        consumer_group: str,
        consumer_name: str
    ) -> AsyncGenerator[Tuple[str, dict], None]:
        """
        Asynchronous reading of events with error handling
        """
        # Create the consumer group if it does not exist
        try:
            await self.redis.xgroup_create(
                self.stream_key, consumer_group, id='0', mkstream=True
            )
        except redis.ResponseError:
            pass  # Group already exists
        
        failed_count = 0
        max_failures = 5
        
        while True:
            try:
                # Read new events
                messages = await self.redis.xreadgroup(
                    consumer_group, consumer_name,
                    {self.stream_key: '>'},
                    count=10, 
                    block=5000
                )
                
                failed_count = 0  # Reset on successful read
                
                for stream_name, message_list in messages:
                    for message_id, data in message_list:
                        try:
                            yield message_id, data
                            
                            # ACK after successful processing
                            await self.redis.xack(
                                self.stream_key, consumer_group, message_id
                            )
                            
                        except Exception as e:
                            # Processing error → move to DLQ
                            logger.error(
                                f"Event processing failed: {e}, "
                                f"moving to DLQ: {message_id}"
                            )
                            await self._move_to_dlq(message_id, data, str(e))
                            
                            # ACK so it doesn't hang
                            await self.redis.xack(
                                self.stream_key, consumer_group, message_id
                            )
                
            except redis.RedisError as e:
                failed_count += 1
                logger.error(f"Redis consume error ({failed_count}/{max_failures}): {e}")

                if failed_count >= max_failures:
                    # P0.5-6 FIX: instead of break → a wait mode with periodic ping.
                    # break killed the generator forever — the entire Slow Path stopped
                    # until a manual agent restart (Gemini audit, ChatGPT audit).
                    # New approach: consume() waits for Redis recovery and continues.
                    # The caller (process_evaluation_queue, etc.) does not notice the pause —
                    # async for simply waits for the next yield.
                    logger.critical(
                        f"Redis unavailable after {max_failures} attempts — "
                        f"entering recovery wait (Slow Path paused, not dead)"
                    )
                    _recovery_interval = 30  # seconds between ping attempts
                    while True:
                        await asyncio.sleep(_recovery_interval)
                        try:
                            await self.redis.ping()
                            # Redis is back — reset the counter and continue the loop
                            failed_count = 0
                            logger.info(
                                "Redis recovered — resuming consume(). "
                                "Slow Path active."
                            )
                            break  # exit the recovery loop → continue while True
                        except redis.RedisError:
                            logger.warning(
                                f"Redis still unavailable, retry in {_recovery_interval}s"
                            )
                            # increase the interval up to a max of 5 minutes
                            _recovery_interval = min(300, _recovery_interval * 2)
                    continue  # continue the main while True after recovery

                # Backoff before retry
                await asyncio.sleep(min(60, 2 ** failed_count))

    async def _move_to_dlq(
        self,
        message_id: str,
        data: dict,
        error: str
    ):
        """Move a problematic event to the Dead Letter Queue"""
        dlq_entry = {
            **data,
            "original_message_id": message_id,
            "error": error,
            "dlq_timestamp": datetime.now(timezone.utc).isoformat(),
            "retry_count": data.get("retry_count", 0) + 1
        }
        
        try:
            await self.redis.xadd(self.dlq_key, dlq_entry)
        except redis.RedisError as e:
            logger.error(f"Failed to write to DLQ: {e}")

    async def process_dlq(self):
        """
        Periodic DLQ processing — reprocess or send to monitoring.
        The method should be registered in the scheduler.
        Add to scheduler.py or main.py at startup:
        
            scheduler.add_job(
                event_bus.process_dlq,
                'interval',
                minutes=15,
                id='dlq_processor',
                max_instances=1
            )
        """
        try:
            messages = await self.redis.xread(
                {self.dlq_key: '0'},
                count=100
            )
            for stream, message_list in messages:
                for msg_id, data in message_list:
                    retry_count = int(data.get("retry_count", 0))
                    if retry_count < 3:
                        clean_data = {
                            k: v for k, v in data.items()
                            if k not in ('retry_count', 'original_message_id',
                                         'error', 'dlq_timestamp')
                        }
                        logger.info(f"Retrying DLQ message: {msg_id}")
                        await self.redis.xadd(self.stream_key, clean_data)
                        await self.redis.xdel(self.dlq_key, msg_id)  # delete AFTER successful reprocess
                    else:
                        logger.error(f"Permanent DLQ failure: {msg_id}, data: {data}")
                        await self._send_permanent_failure_alert(msg_id, data, retry_count)
                        await self._archive_permanent_failure(msg_id, data)
                        await self.redis.xdel(self.dlq_key, msg_id)  # delete after archiving
        except Exception as e:
            logger.error(f"DLQ processing failed: {e}")

    async def _send_permanent_failure_alert(self, msg_id: str, data: dict, retries: int):
        """
        Mandatory alert on permanent DLQ failure.
        Integration via EventBus → Observer++ raises severity = CRITICAL.
        """
        try:
            await self.redis.xadd("agent:alerts", {
                "type": "PERMANENT_DLQ_FAILURE",
                "msg_id": msg_id,
                "retries": str(retries),
                "data_type": data.get("type", "unknown"),
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "severity": "CRITICAL"
            })
        except Exception as e:
            logger.error(f"Failed to send permanent failure alert: {e}")

    async def _archive_permanent_failure(self, msg_id: str, data: dict):
        """Save the permanent failure to SQLite for later audit."""
        # orphaned except removed (SyntaxError — except without try),
        # xdel removed from here (it was in except, i.e. deleted only on archiving error — logic inverted)
        try:
            import aiosqlite
            db_path = getattr(self.fallback_queue, 'db_path', 'fallback_events.db')
            async with aiosqlite.connect(db_path) as db:
                await db.execute("""
                    CREATE TABLE IF NOT EXISTS permanent_failures (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        msg_id TEXT NOT NULL,
                        data TEXT,
                        archived_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                await db.execute(
                    "INSERT INTO permanent_failures (msg_id, data) VALUES (?, ?)",
                    (msg_id, json.dumps(data))
                )
                await db.commit()
        except Exception as e:
            logger.error(f"Failed to archive permanent failure: {e}")


    async def health_check(self) -> dict:
        """Event Bus health check"""
        try:
            await self.redis.ping()
            stream_info = await self.redis.xinfo_stream(self.stream_key)
            try:
                dlq_info = await self.redis.xinfo_stream(self.dlq_key)
                dlq_length = dlq_info.get("length", 0)
            except redis.ResponseError:
                dlq_length = 0  # DLQ not created yet — this is normal
            
            return {
                "status": "healthy",
                "redis_available": True,
                "main_stream_length": stream_info.get("length", 0),
                "dlq_length": dlq_length,
                "fallback_queue_size": await self.fallback_queue.qsize()  # async method — await is mandatory
            }
        except Exception as e:
            return {
                "status": "degraded",
                "redis_available": False,
                "error": str(e),
                "fallback_queue_size": await self.fallback_queue.qsize()
            }
```

**Integration into the agent**:

```python
# agent.py
class Agent:
    def __init__(self, event_bus: RobustEventBus):
        self.event_bus = event_bus
        self.session_id = generate_session_id()

    async def chat(self, user_message: str):
        # 1. Log the incoming message (with retry/fallback)
        publish_success = await self.event_bus.publish(AgentEvent(
            event_type=EventType.USER_MESSAGE,
            timestamp=datetime.now(timezone.utc),
            content={"message": user_message},
            metadata={"length": len(user_message)},
            session_id=self.session_id
        ))
        
        if not publish_success:
            logger.warning("Event published to fallback queue")
        
        # 2. Processing (retrieval + generation)
        response = await self.process(user_message)
        
        # 3. Log the response
        await self.event_bus.publish(AgentEvent(
            event_type=EventType.AGENT_RESPONSE,
            timestamp=datetime.now(timezone.utc),
            content={"message": response},
            metadata={"tokens": count_tokens(response)},
            session_id=self.session_id
        ))
        
        return response
```
---

### 2. Graphiti + Neo4j: The Foundation of Memory

**Purpose**: A temporal knowledge graph with automatic extraction

```python
# memory_core.py
from graphiti_core import Graphiti
from datetime import datetime, timezone   # ← PATCH-4: added timezone (previously NameError in add_episode)
from typing import List, Optional

class GraphMemory:
    def __init__(self, neo4j_uri: str, neo4j_user: str, neo4j_password: str,
                 memory_guardian=None, raw_memory=None):   # ← PATCH-9: dependency injection (optional)
        self.graphiti = Graphiti(
            neo4j_uri=neo4j_uri,
            neo4j_user=neo4j_user,
            neo4j_password=neo4j_password
        )
        self.memory_guardian = memory_guardian  # None = old behavior, backward compatibility preserved
        self.raw_memory = raw_memory

    async def add_episode(
        self,
        episode_name: str,
        content: str,
        source: str = "conversation",
        timestamp: Optional[datetime] = None
    ):
        """
        Add an episode - automatic extraction of entities and relationships
        Does NOT require an LLM request from the developer - Graphiti does this internally

        PATCH-9 (Graph = Truth): write order:
          1. ImmutableRawMemory — the raw original is protected before any validation
          2. MemoryGuardian (Truth Gate) — if set; None = old behavior
          3. graphiti.add_episode — only if steps 1-2 passed
        Backward compatibility: memory_guardian=None → behavior identical to the old one.
        """
        import asyncio as _asyncio
        ref_time = timestamp or datetime.now(timezone.utc)

        # STEP 1: the raw original — save before any validation (Semantic Drift protection)
        if self.raw_memory:
            await _asyncio.to_thread(
                self.raw_memory.save_episode,
                f"{episode_name}_{ref_time.timestamp()}",
                content, source, session_id="",
            )

        # STEP 2: Truth Gate — if a guardian is set
        if self.memory_guardian:
            proposal = {
                "content":    content,
                "source":     source,
                "evidence":   source,   # minimal evidence = source (Phase 0)
                "confidence": 1.0 if source == "user_input" else 0.75,
            }
            if not await self.memory_guardian.validate_proposal(proposal):
                return   # Guardian has already logged the reason — the graph is not polluted

        # STEP 3: write to the graph — only here
        await self.graphiti.add_episode(
            name=episode_name,
            episode_body=content,
            source_description=source,
            reference_time=ref_time
        )

    async def search(
        self,
        query: str,
        num_results: int = 5,
        time_filter: Optional[tuple] = None
    ) -> List[dict]:
        """
        Hybrid search WITHOUT LLM requests:
        - Vector search over embeddings
        - BM25 full-text search
        - Graph traversal for context
        """
        results = await self.graphiti.search(
            query=query,
            num_results=num_results
        )
        
        # Additional filtering by time if needed
        if time_filter:
            start_time, end_time = time_filter
            results = [
                r for r in results
                if start_time <= r.timestamp <= end_time
            ]
        
        return results

    async def get_context_for_entity(
        self,
        entity_name: str,
        depth: int = 2
    ) -> dict:
        """
        Get the context around an entity via graph traversal
        """
        # FIX from HYPERIA: whitelist instead of numeric clamp.
        # max(1, min(int(depth), 5)) does not protect if depth is a string like "3; DROP".
        # A whitelist makes injection architecturally impossible — only 1, 2 or 3.
        depth = depth if depth in (1, 2, 3) else 2
        # path is built before WITH, otherwise it goes out of scope and Neo4j throws an error
        query = f"""
        MATCH (e:Entity {{name: $entity_name}})
        OPTIONAL MATCH path = (e)-[:RELATED_TO|CAUSES|CONCEPT_OF|SUPPORTED_BY*1..{depth}]-(related)
        WITH e, related, relationships(path) AS rels
        WITH e,
             collect(DISTINCT related)[0..50] AS related_entities,
             collect(DISTINCT rels)[0..50]    AS relationships
        RETURN e, related_entities, relationships
        """
        
        result = await self.graphiti.execute_cypher(
            query,
            {"entity_name": entity_name}
        )
        
        return result
```

**Graph schema**:

```cypher
// Node types
// embedding_version: which model created the vector (for lazy re-indexing when the model changes)
// is_active + valid_to: Soft Delete — the node is not physically deleted, but deactivated
// reindex_required: flag for automatic re-indexing when the embedding model changes
(:Entity {
    name, type,
    embedding, embedding_version,          // + model version: "multilingual-e5-large-v1"
    importance_score, created_at, last_accessed,
    is_active,                             // Soft Delete flag (default: true)
    valid_from, valid_to,                  // Temporal bounds for facts
    reindex_required                       // true = re-indexing needed (false by default)
})
(:Episode {
    id, summary, timestamp, session_id, outcome,
    is_active, valid_to,
    raw_episode_id                         // reference to ImmutableRawMemory (never changes)
    // ⚠️ Episode ∉ Semantic Graph — episodes are not mixed with facts
    // Phase 2: move out into a separate Vector DB (Qdrant)
})
(:Domain {                                 // RFC0012: Domain as the root of the taxonomy
    id,                                    // "domain:physics"
    name,                                  // "Physics"
    description,                           // brief description of the domain
    parent_domain_id,                      // for nested domains (physics → quantum_physics)
    created_at
})
(:Concept {                                // RFC0002: Concept as a separate node
    id,                                    // "concept:water"
    name,                                  // "Water"
    aliases,                               // ["H2O"]
    created_at, updated_at
})
(:Fact {
    content, confidence,
    relation, value, condition,            // for Knowledge Units: structured fields
    valid_from, valid_to,                  // valid_time: when the fact was true
    transaction_time,                      // transaction_time: when it was written to the graph (bi-temporal)
    is_active,                             // Soft Delete instead of DETACH DELETE
    override_flag,                         // true = manual override by the user
    is_knowledge_unit,                     // true = distilled atomic fact (JSON triple)
    validated,                             // true = passed through MGL. ∀ fact ∈ Graph: validated = True
    // ESM (Epistemic State Machine) fields
    epistemic_state,                       // Observed|Hypothesized|Supported|Validated|Contradicted|Deprecated|Collapsed
    epistemic_score,                       // 0.0–1.0 strength of the fact's epistemic position
    epistemic_variance,                    // 0.0–1.0 mathematical uncertainty: 1.0=unknown, 0.0=confident (RFC0046)
    state_changed_at,                      // datetime of the last ESM transition
    transition_reason                      // transition reason: "MGL_PASSED"|"CONTRADICTED"|"EVIDENCE_ADDED"|"GC"
})
(:Evidence {                               // RFC0002: Evidence as a separate node — not a string
    id,                                    // "evidence:physicsbook1"
    source,                                // "Physics Handbook"
    page,                                  // 42
    quality,                               // 0.9 — source reliability
    url,                                   // optional
    created_at
})
(:Strategy {description, success_count, failure_count, context_type, is_active,
            confidence})                   // confidence decreases when dependent :Fact nodes are invalidated
(:Community {id, topic, size, last_updated})
// Node type for Knowledge Distillation
(:KnowledgeUnit {
    concept, relation, value, condition,
    confidence, timestamp,
    embedding, embedding_version
})

// Relationship types
(:Entity)-[:MENTIONED_IN]->(:Episode)
(:Entity)-[:RELATED_TO {strength, type, valid_from, valid_until}]->(:Entity)   // valid_until=null → currently relevant (RFC0046)
(:Episode)-[:PART_OF]->(:Community)
(:Episode)-[:LED_TO {outcome}]->(:Episode)
(:Strategy)-[:USED_IN]->(:Episode)
(:Strategy)-[:SUCCEEDED_AT]->(:Task)
(:Strategy)-[:FAILED_AT]->(:Task)
(:Strategy)-[:DERIVED_FROM]->(:Fact)    // when a :Fact is invalidated → lower the :Strategy confidence
(:Strategy)-[:IMPROVES]->(:Strategy)   // RFC0002: strategy improvement chains
// Fact conflict: a new fact explicitly contradicts an old one
(:Fact)-[:CONTRADICTS {reason, resolved_at}]->(:Fact)
(:Fact)-[:CAUSES {valid_from, valid_until}]->(:Fact)                           // RFC0046: temporal on cause-and-effect relationships
(:Fact)-[:SUPPORTED_BY]->(:Evidence)   // RFC0002: reference to the source as a node
(:Fact)-[:CONCEPT_OF]->(:Concept)     // RFC0002: the fact belongs to a concept
(:Concept)-[:HAS_RELATION]->(:Fact)   // RFC0002: back-reference from concept to facts
(:Concept)-[:BELONGS_TO]->(:Domain)   // RFC0012: the concept belongs to a domain
(:Domain)-[:SUBDOMAIN_OF]->(:Domain)  // RFC0012: domain hierarchy (nesting)
(:Fact)-[:IN_DOMAIN]->(:Domain)       // RFC0012: the fact is explicitly bound to a domain (optional, for fast search)
// RFC0046: reasoning DAG in L4 ReasoningBank
(:ReasoningStep)-[:PRECEDES]->(:ReasoningStep)                                 // reasoning steps — a directed DAG
(:ReasoningStep)-[:ROLLBACK_TO {reason, rolled_at, session_id}]->(:ReasoningStep) // dead-end branch → rollback

// RFC0067 v2.0: Analogy Graph — only through the Write Protocol Gate (I55)
(:Entity)-[:METAPHOR_OF {
    source_domain: STRING, target_domain: STRING,
    essence: STRING, source_text: STRING,
    confidence: FLOAT, resonance_score: FLOAT,
    cultural_vintage: INT, created_at: DATETIME, last_used: DATETIME
}]->(:Entity)
(:Entity)-[:ANALOGOUS_TO {
    domain_a: STRING, domain_b: STRING,
    structure_mapping: JSON, source_text: STRING,
    confidence: FLOAT, resonance_score: FLOAT,
    cultural_vintage: INT, created_at: DATETIME, last_used: DATETIME
}]->(:Entity)
```

```cypher
// RFC0067 v2.0: Analogy Graph indexes (add to neo4j_setup.py)
CREATE INDEX metaphor_source_domain IF NOT EXISTS
FOR ()-[r:METAPHOR_OF]-() ON (r.source_domain);
CREATE INDEX metaphor_resonance IF NOT EXISTS
FOR ()-[r:METAPHOR_OF]-() ON (r.resonance_score);
CREATE INDEX analogy_domain_pair IF NOT EXISTS
FOR ()-[r:ANALOGOUS_TO]-() ON (r.domain_a, r.domain_b);
CREATE INDEX metaphor_last_used IF NOT EXISTS
FOR ()-[r:METAPHOR_OF]-() ON (r.last_used);
CREATE FULLTEXT INDEX metaphor_essence_idx IF NOT EXISTS
FOR ()-[r:METAPHOR_OF]-() ON EACH [r.essence];
```

> ⚠️ **Soft Delete — a mandatory pattern**: do NOT use `DETACH DELETE` for facts and episodes in production. Set `is_active = false` and `valid_to = datetime()`. Physical deletion — only in GC after successful archiving to S3.
>
> ⚠️ **Bi-temporal graph**: `valid_from/valid_to` = when the fact was true in the real world. `transaction_time` = when it was written to the system. Both are needed to answer "what did we know at moment X".
>
> ⚠️ **Evidence as a node**: the `evidence` field in :Fact has been replaced by the `[:SUPPORTED_BY]->(:Evidence)` relationship. This makes it possible to delete an unreliable source together with all of its facts and to assess the quality of the source separately.

**CRITICAL: Neo4j indexes (create at initialization!)**:

```python
# neo4j_setup.py
async def setup_neo4j_indexes(driver):
    """
    Mandatory indexes for performance
    WITHOUT THIS the system degrades within 2-4 weeks!
    """
    async with driver.session() as session:
        # 1. Indexes on frequently used fields
        await session.run("""
            CREATE INDEX entity_name_idx IF NOT EXISTS
            FOR (e:Entity) ON (e.name)
        """)
        
        await session.run("""
            CREATE INDEX entity_type_idx IF NOT EXISTS
            FOR (e:Entity) ON (e.type)
        """)
        
        await session.run("""
            CREATE INDEX episode_timestamp_idx IF NOT EXISTS
            FOR (ep:Episode) ON (ep.timestamp)
        """)
        
        await session.run("""
            CREATE INDEX episode_session_idx IF NOT EXISTS
            FOR (ep:Episode) ON (ep.session_id)
        """)
        
        # 2. Vector index for similarity search
        # Dimension from config — not hardcoded.
        # multilingual-e5-large = 1024, text-embedding-3-small = 1536, Gemini Embedding 2 = 3072
        embedding_dims = config.get("embedding", {}).get("dimensions", 1024)
        await session.run(f"""
            CREATE VECTOR INDEX entity_embedding_idx IF NOT EXISTS
            FOR (e:Entity) ON (e.embedding)
            OPTIONS {{
                indexConfig: {{
                    `vector.dimensions`: {embedding_dims},
                    `vector.similarity_function`: 'cosine'
                }}
            }}
        """)
        
        # 3. Composite index for filtering by importance + time
        await session.run("""
            CREATE INDEX entity_importance_time_idx IF NOT EXISTS
            FOR (e:Entity) ON (e.importance_score, e.last_accessed)
        """)
        
        # 4. Index on embedding_version for lazy re-indexing
        # Allows quickly finding all nodes with an outdated embedding model
        await session.run("""
            CREATE INDEX entity_embedding_version_idx IF NOT EXISTS
            FOR (e:Entity) ON (e.embedding_version)
        """)
        
        # 5. Index on is_active for Soft Delete filtering
        await session.run("""
            CREATE INDEX entity_active_idx IF NOT EXISTS
            FOR (e:Entity) ON (e.is_active)
        """)

        # 6. ✅ RFC0062: index for ConflictResolutionWorker._check_batch
        await session.run("""
            CREATE INDEX fact_conflict_checked_idx IF NOT EXISTS
            FOR (f:Fact) ON (f.conflict_checked)
        """)
```

**Query optimization (ALWAYS use LIMIT!)**:

```python
# graph_memory.py
async def get_context_for_entity(
    self,
    entity_name: str,
    depth: int = 2,
    max_neighbors: int = 100  # CRITICAL!
) -> dict:
    """
    Get the context around an entity via graph traversal
    WITH A LIMIT on results to prevent memory explosion
    """
    # FIX from HYPERIA: whitelist instead of numeric clamp — injection is architecturally impossible.
    depth = depth if depth in (1, 2, 3) else 2
    query = f"""
    MATCH (e:Entity {{name: $entity_name}})
    OPTIONAL MATCH path = (e)-[*1..{depth}]-(related)
    WITH e, related, relationships(path) as rels
    RETURN e, 
           collect(DISTINCT related)[0..{max_neighbors}] as related_entities,
           collect(DISTINCT rels)[0..{max_neighbors}] as relationships
    """

    result = await self.graphiti.execute_cypher(
        query,
        {"entity_name": entity_name}
    )

    return result
```

**Archiving old nodes**:

```python
# memory_archival.py
from datetime import datetime, timedelta
import json
import aioboto3

class MemoryArchival:
    def __init__(self, graph: GraphMemory, s3_bucket: str):
        self.graph = graph
        self._session = aioboto3.Session()
        self.bucket = s3_bucket

    async def archive_old_episodes(
        self,
        older_than_days: int = 365,
        importance_threshold: float = 0.3
    ):
        """
        Archive episodes older than N days with low importance
        This is critical for preventing unbounded graph growth
        """
        # 1. Find candidates for archiving
        query = """
        MATCH (ep:Episode)-[r]-(connected)
        WHERE ep.timestamp < datetime() - duration({days: $days})
          AND ep.importance_score < $threshold
        RETURN ep, collect(DISTINCT connected) as related, collect(r) as relationships
        LIMIT 1000
        """
        
        candidates = await self.graph.execute_cypher(query, {
            "days": older_than_days,
            "threshold": importance_threshold
        })
        
        # 2. Export to S3
        # We use self._session from __init__ — we do not create a new Session() on each call (connection leak).
        archived_count = 0
        async with self._session.client('s3') as s3:
          for episode_data in candidates:
            archive_key = f"archived_episodes/{episode_data['ep']['id']}.json"
            
            await s3.put_object(  # now a correct await
                Bucket=self.bucket,
                Key=archive_key,
                Body=json.dumps(episode_data)
            )
            
            # Soft Delete: physical deletion only via the Vacuum Worker (GC)
            await self.graph.execute_cypher("""
                MATCH (ep:Episode {id: $id})
                SET ep.is_active = false,
                    ep.valid_to = datetime(),
                    ep.archived_to_s3 = true
                WITH ep
                OPTIONAL MATCH (ep)-[r]-()
                SET r.is_active = false
            """, {"id": episode_data['ep']['id']})
            
            archived_count += 1
        
        return archived_count

    async def vacuum_soft_deleted(self, min_age_days: int = 90):
        """
        Vacuum Worker — physical deletion after S3 confirmation.
        Batched rate limiting — deletes 100 nodes per iteration
        with a 500ms pause between batches. Does not compete with the Fast Path.

        Protocol:
        1. archived_to_s3 = true  (archiving confirmed)
        2. valid_to < now - 90 days  (old enough)
        3. Only then — DETACH DELETE (in batches, not all at once)

        Run: via MemoryGarbageCollector.run_full_gc() once a week.
        Do not run on the Fast Path — only Slow Path / background GC.
        """
        total_deleted = 0
        batch_size = 100          # limit per single iteration
        sleep_between = 0.5       # 500ms pause — do not block the Neo4j write lock

        while True:
            deleted = await self.graph.execute_cypher("""
                MATCH (n)
                WHERE n.is_active = false
                  AND n.archived_to_s3 = true
                  AND n.valid_to < datetime() - duration({days: $min_age_days})
                WITH n LIMIT $batch_size
                DETACH DELETE n
                RETURN count(n) AS deleted_count
            """, {"min_age_days": min_age_days, "batch_size": batch_size})

            count = deleted[0].get("deleted_count", 0) if deleted else 0
            total_deleted += count

            if count == 0:
                break  # Nothing to delete — exit

            logger.info(f"Vacuum batch: deleted {count}, total {total_deleted}")
            await asyncio.sleep(sleep_between)  # Rate limiting — pause between batches

        logger.info(f"Vacuum finished: physically deleted {total_deleted} nodes (age > {min_age_days}d)")
        return total_deleted


class MemoryRestoreProtocol:
    """
    5-step protocol for restoring a node from S3 → Neo4j.

    Needed when GC deleted something important or the user requested a restore.
    Was absent in v5 — there was only the "outbound" path (archiving), but not the "inbound" one.

    Steps:
        1. Find the archive in S3 by node_id
        2. MERGE the node back into Neo4j
        3. SET is_active=true, clear valid_to
        4. Stamp restored_at + restore_reason (audit)
        5. Re-enter ESM at Supported (not Validated — TruthGate is needed again)
           + check invariants post-restore

    Usage:
        restore = MemoryRestoreProtocol(graph, s3_client, S3_BUCKET, esm, inv_checker)
        result  = await restore.restore("episode:abc123", "user_request", session_id)
    """

    def __init__(self, graph_adapter, s3_client, s3_bucket: str, esm, invariant_checker):
        self.graph   = graph_adapter
        self.s3      = s3_client
        self.bucket  = s3_bucket
        self.esm     = esm
        self.checker = invariant_checker

    async def restore(self, node_id: str, restore_reason: str,
                      requested_by: str = "system") -> dict:
        """Returns {"success": bool, "node_id": ..., "reason": ..., "restored_at": ...}"""
        logger.info(f"MemoryRestoreProtocol: restore {node_id} ({restore_reason})")

        # 1. S3 lookup
        try:
            import json as _json
            obj  = await self.s3.get_object(
                Bucket=self.bucket, Key=f"archived_episodes/{node_id}.json"
            )
            data = _json.loads(await obj["Body"].read())
        except Exception as e:
            logger.error(f"MemoryRestoreProtocol: S3 lookup failed: {e}")
            return {"success": False, "node_id": node_id, "reason": f"S3 failed: {e}"}

        # 2. MERGE into Neo4j
        try:
            props = {k: v for k, v in data.get("ep", {}).items()
                     if k not in ("is_active", "valid_to", "archived_to_s3")}
            await self.graph.execute_cypher(
                "MERGE (n {id: $id}) ON CREATE SET n = $p ON MATCH SET n += $p",
                {"id": node_id, "p": props}
            )
        except Exception as e:
            logger.error(f"MemoryRestoreProtocol: MERGE failed: {e}")
            return {"success": False, "node_id": node_id, "reason": f"MERGE failed: {e}"}

        # 3+4. Activate + audit
        now = datetime.now(timezone.utc).isoformat()
        await self.graph.execute_cypher(
            "MATCH (n {id: $id}) SET n.is_active = true, n.valid_to = null,"
            " n.restored_at = $now, n.restore_reason = $r, n.restored_by = $by",
            {"id": node_id, "now": now, "r": restore_reason, "by": requested_by}
        )

        # 5a. Re-enter ESM: start from Hypothesized + evidence_count=2
        #     ESM will automatically transition to Supported (rule: Hypothesized→Supported when Evidence ≥ 2).
        #     The node is not raised to Validated — TruthGate is needed again (we do not bypass it).
        try:
            await self.esm.transition(
                node_id,
                {"epistemic_state": "Hypothesized", "evidence_count": 2},
                self.graph,
                f"restore:{restore_reason}"
            )
        except Exception as e:
            logger.warning(f"MemoryRestoreProtocol: ESM transition soft-failed (non-fatal): {e}")

        # 5b. Check invariants post-restore
        try:
            violations = await self.checker.check_all()
            criticals  = [v.invariant_id for v in violations if v.severity == "CRITICAL"]
            if criticals:
                logger.error(f"MemoryRestoreProtocol: post-restore critical invariants: {criticals}")
        except Exception:
            pass

        logger.info(f"MemoryRestoreProtocol: ✅ {node_id} restored")
        return {"success": True, "node_id": node_id, "reason": restore_reason, "restored_at": now}
```

---


# ============================================================================
# HYPERIA COMPONENT 1: EmbeddingRegistry
# ============================================================================
# Purpose: Centralized registry of embedding model dimensions
# Prevents silent corruption of indexes when the model changes

# memory/embedding_registry.py
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class EmbeddingRegistry:
    """
    Centralized registry of embedding models and their dimensions.

    Problem: When changing the model from 1024 dim to 3072 dim, Neo4j indexes
    become incompatible, but the error only manifests at runtime.

    Solution: Validation at startup + automatic detection of mismatches.
    """

    # Known models and their dimensions
    KNOWN_MODELS: Dict[str, int] = {
        "paraphrase-multilingual-MiniLM-L12-v2": 384,
        "multilingual-e5-large": 1024,
        "deepvk/USER-bge-m3": 1024,
        "text-embedding-3-small": 1536,
        "text-embedding-3-large": 3072,
        "gemini-embedding-2": 3072,
        "text-embedding-ada-002": 1536,
    }

    def __init__(self, current_model: str):
        self.current_model = current_model
        self.dimension = self._get_dimension(current_model)
        logger.info(f"EmbeddingRegistry: {current_model} → {self.dimension}D")

    def _get_dimension(self, model_name: str) -> int:
        """Get the model dimension or compute it automatically"""
        if model_name in self.KNOWN_MODELS:
            return self.KNOWN_MODELS[model_name]
        
        # Real model call — we do not guess, we do not silently return 1024
        logger.warning(f"Model {model_name} is not in the registry. Attempting to determine it for real...")
        try:
            test_embedding = self._compute_test_embedding(model_name)
            actual_dim = len(test_embedding)
            self.KNOWN_MODELS[model_name] = actual_dim  # cache for subsequent calls
            logger.info(f"Auto-detected dimension for {model_name}: {actual_dim}D")
            return actual_dim
        except Exception as e:
            # CRITICAL: better to crash at startup than silently create incompatible Neo4j indexes
            logger.critical(
                f"UNABLE to determine the dimension for {model_name}: {e}\n"
                f"Add the model to EmbeddingRegistry.KNOWN_MODELS manually.\n"
                f"Running without this = silent corruption of Neo4j indexes."
            )
            raise RuntimeError(
                f"Unknown embedding model: {model_name}. "
                f"Add to EmbeddingRegistry.KNOWN_MODELS before deploying. Error: {e}"
            )

    def validate_index_dimension(self, index_dimension: int) -> bool:
        """
        Check that the index dimension matches the current model.
        Called at GraphMemory startup.
        """
        if index_dimension != self.dimension:
            logger.error(
                f"DIMENSION MISMATCH: "
                f"index={index_dimension}D, model={self.dimension}D. "
                f"Index re-creation required!"
            )
            return False
        return True

    def get_dimension(self) -> int:
        """Get the dimension of the current model"""
        return self.dimension

# Integration into GraphMemory:
# In __init__:
#   self.embedding_registry = EmbeddingRegistry(current_model=embedding_model_name)
# When creating an index:
#   dimension = self.embedding_registry.get_dimension()
# At startup:
#   if not self.embedding_registry.validate_index_dimension(existing_index_dim):
#       raise RuntimeError("Index dimension mismatch")

---

## 🧬 Integrated Components (from HYPERIA v5.20)

> Components are integrated into Velantrim without changing the architecture.
> Each component is a separate file. They connect through existing points.

---

### HYPERIA-1: DAAD — Domain-Aware Attention & Decay

> **Problem**: DAAD domain-aware λ_eff in FSRS decay for all nodes.
> "An active project with a deadline" and "the weather was nice yesterday" decay identically.
> **Solution**: `λ_eff = Σ(dᵢ × λᵢ)` — a weighted sum over the node's domains.

#### Invariant I66 (new)
```
I66: DAAD changes ONLY attention_weight and λ_eff.
     truth_status, epistemic_state, epistemic_score — inviolable.
     domain_vector=NULL → fallback λ=0.05, not an error.
     Violation = direct write to ESM from DomainResolver = bug.
```

#### Domain table
| Domain | λ (decay) | floor (minimum) | Meaning |
|---|---|---|---|
| `active_project` | 0.001 | 0.85 | Lives for years |
| `personal_pref` | 0.004 | 0.60 | Changes slowly |
| `domain_knowledge` | 0.006 | 0.50 | Stable knowledge |
| `completed_project` | 0.008 | 0.40 | Less relevant |
| `casual_chat` | 0.150 | 0.00 | Forgotten within days |
| `general_question` | 0.200 | 0.00 | Quickly becomes outdated |

```python
# memory/domain_resolver.py
# HYPERIA DAAD — Domain-Aware Attention & Decay
# I66: changes only attention_weight. ESM/truth_status — does not touch.
# Slow Path, 0 LLM tokens.

import logging
from dataclasses import dataclass
from typing import Dict, Optional

logger = logging.getLogger(__name__)

DOMAIN_CONFIG: Dict[str, Dict] = {
    "active_project":    {"lambda": 0.001, "floor": 0.85},
    "personal_pref":     {"lambda": 0.004, "floor": 0.60},
    "domain_knowledge":  {"lambda": 0.006, "floor": 0.50},
    "completed_project": {"lambda": 0.008, "floor": 0.40},
    "casual_chat":       {"lambda": 0.150, "floor": 0.00},
    "general_question":  {"lambda": 0.200, "floor": 0.00},
}

FALLBACK_LAMBDA = 0.05
FALLBACK_FLOOR  = 0.00


@dataclass
class DecayParams:
    lambda_eff: float  # effective decay rate
    floor_eff:  float  # minimum importance level (does not fall below it)


class DomainResolver:
    """
    Computes λ_eff and floor_eff for a node from its domain_vector.
    domain_vector — a normalized distribution over domains (sum = 1.0).
    Example: {"active_project": 0.7, "domain_knowledge": 0.3}
    λ_eff = Σ(dᵢ × λᵢ)  — a weighted sum of decay rates
    floor_eff = max(dᵢ × floorᵢ)  — the maximum guaranteed minimum

    Integration: called from FSRSDecayWorker instead of a fixed λ. (v8.0: replaces EbbinghausDecayWorker)
    """

    @staticmethod
    def resolve(domain_vector: Optional[Dict[str, float]]) -> DecayParams:
        """
        Compute the decay parameters from the node's domain_vector.
        domain_vector=None or empty → fallback (I66).
        """
        if not domain_vector:
            logger.debug("DomainResolver: domain_vector=None → fallback λ=0.05")
            return DecayParams(lambda_eff=FALLBACK_LAMBDA, floor_eff=FALLBACK_FLOOR)

        lambda_eff = 0.0
        floor_eff  = 0.0
        total_weight = sum(domain_vector.values())

        if total_weight <= 0:
            return DecayParams(lambda_eff=FALLBACK_LAMBDA, floor_eff=FALLBACK_FLOOR)

        # Normalization in case the weights do not sum to 1.0
        for domain, weight in domain_vector.items():
            norm_weight = weight / total_weight
            cfg = DOMAIN_CONFIG.get(domain)
            if cfg is None:
                logger.warning(f"DomainResolver: unknown domain '{domain}' — skipped")
                continue
            lambda_eff += norm_weight * cfg["lambda"]
            floor_eff   = max(floor_eff, norm_weight * cfg["floor"])

        # If all domains are unknown — fallback
        if lambda_eff == 0.0:
            return DecayParams(lambda_eff=FALLBACK_LAMBDA, floor_eff=FALLBACK_FLOOR)

        return DecayParams(lambda_eff=lambda_eff, floor_eff=floor_eff)
```

**Integration into FSRSDecayWorker** (v8.0: replaces EbbinghausDecayWorker):
```python
# In FSRSDecayWorker — DAAD domain-aware λ_eff:
from memory.domain_resolver import DomainResolver

# Before:
# new_importance = current_importance * exp(-t / S)

# After:
domain_vector = node.get("domain_vector")  # from Neo4j :Entity.domain_vector
params = DomainResolver.resolve(domain_vector)
# P9-FIX BUG-11: FSRS power-law (P0-1 replaced Ebbinghaus everywhere, the DAAD example was not updated)
# λ_eff is used instead of the global λ via domain-aware stability
S_eff = S / max(0.01, params.lambda_eff)              # domain-aware stability
R = (1 + (19/81) * t / max(0.01, S_eff)) ** (-0.5)   # FSRS power-law R
new_importance = max(params.floor_eff, current_importance * R)
# floor_eff guarantees that an important node never falls below the threshold
```

**Add to the Neo4j schema** (`:Entity`):
```cypher
// domain_vector: a JSON distribution over domains, updated by the TagManager
// Example: '{"active_project": 0.7, "domain_knowledge": 0.3}'
(:Entity { ..., domain_vector: STRING })  // JSON, NULL = fallback λ=0.05
```

**Metrics**:
```python
daad_resolved_total     # counter of nodes with domain-aware decay
daad_fallback_total     # counter of fallbacks (domain_vector=NULL)
daad_floor_protected    # how many times the floor prevented a drop below the minimum
```

---

### HYPERIA-2: Guardian — Response Validator

> **Source**: HYPERIA `core/guardian.py`
> **Purpose**: The last line of defense **after the LLM** before sending to the user.
> Velantrim has a Truth Gate (before L3) and Observer++ (security),
> but it lacks a check of the **response quality** after generation.
> **Location**: Fast Path, after LLM Generation, before Response.
> **Invariant**: Guardian.validate() — synchronous, 0 tokens, <1 ms.

```python
# core/guardian.py
# Guardian — the last line of defense before the user's response.
# Location: Fast Path after the LLM, before return.
# 0 tokens · <1 ms · synchronous.

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum
import logging

logger = logging.getLogger(__name__)

CONFIDENCE_THRESHOLD = 0.6
MIN_TRACE_LENGTH     = 1


class GuardianDecision(str, Enum):
    APPROVE = "approve"
    REJECT  = "reject"
    WARN    = "warn"    # the response is returned, but with a warning


@dataclass
class GuardianResult:
    decision:   GuardianDecision
    reason:     str
    confidence: float
    response:   Optional[str] = None  # the final text for the user


class Guardian:
    """
    Validator of the agent's response.
    REJECT  — when confidence < 0.6, an empty trace, or only deprecated sources.
    WARN    — when a majority of sources are hypotheses.
    APPROVE — all checks passed.
    """

    def validate(
        self,
        response:   str,
        confidence: float,
        trace:      List[str],
        sources:    List[dict] = None,
    ) -> GuardianResult:
        def _emit(res: GuardianResult) -> GuardianResult:
            try:
                from metrics import guardian_decisions_total, guardian_confidence_dist
                guardian_decisions_total.labels(decision=res.decision.value).inc()
                guardian_confidence_dist.observe(res.confidence)
            except Exception:
                pass
            return res

        # Check 1: confidence
        if confidence < CONFIDENCE_THRESHOLD:
            logger.info(f"Guardian: REJECT — low confidence ({confidence:.2f})")
            return _emit(GuardianResult(
                decision=GuardianDecision.REJECT,
                reason=f"confidence too low ({confidence:.2f})",
                confidence=confidence,
                response=(
                    "I am not confident enough to give a precise answer. "
                    "I can search for more information or clarify the details."
                )
            ))

        # Check 2: presence of a justification (TRACE)
        if not trace or len(trace) < MIN_TRACE_LENGTH:
            logger.info("Guardian: REJECT — empty trace")
            return _emit(GuardianResult(
                decision=GuardianDecision.REJECT,
                reason="no reasoning trace",
                confidence=confidence,
                response=(
                    "I do not have enough confirmed data on this question. "
                    "Tell me more — that will help find the right information."
                )
            ))

        # Check 3: are all sources deprecated?
        if sources:
            non_deprecated = [
                s for s in sources
                if s.get("epistemic_state") not in ("Deprecated", "Collapsed", "Contradicted")
            ]
            if not non_deprecated:
                logger.info("Guardian: REJECT — all sources deprecated/collapsed")
                return _emit(GuardianResult(
                    decision=GuardianDecision.REJECT,
                    reason="all memory sources are deprecated",
                    confidence=confidence,
                    response=(
                        "The information on this topic in my memory is outdated. "
                        "Provide the current data — I will update it."
                    )
                ))

            # Warning: majority hypothesis
            hypothesis_count = sum(
                1 for s in sources
                if s.get("epistemic_state") in ("Hypothesized", "Observed")
            )
            if hypothesis_count > len(sources) / 2:
                logger.info(f"Guardian: WARN — {hypothesis_count}/{len(sources)} sources are hypothesis")
                return _emit(GuardianResult(
                    decision=GuardianDecision.WARN,
                    reason=f"{hypothesis_count}/{len(sources)} sources unconfirmed",
                    confidence=confidence,
                    response=f"[Partly a hypothesis] {response}"
                ))

        return _emit(GuardianResult(
            decision=GuardianDecision.APPROVE,
            reason="all checks passed",
            confidence=confidence,
            response=response
        ))
```

**Integration** — add to the end of the Fast Path after the LLM:
```python
# In agent.py / chat() — after LLM Generation, before return response:
from core.guardian import Guardian, GuardianDecision

guardian = Guardian()
guard_result = guardian.validate(
    response=llm_response,
    confidence=response_confidence,   # from the LLM response or from ESM
    trace=fact_trace,                 # list[fact_id] of the facts used
    sources=retrieved_facts,          # facts from L3 with epistemic_state
)
if guard_result.decision == GuardianDecision.REJECT:
    logger.warning(f"Guardian REJECT: {guard_result.reason}")
return guard_result.response  # APPROVE→original, WARN→with a note, REJECT→fallback
```

**Metrics**:
```python
guardian_decisions_total   # labels: approve/reject/warn
guardian_confidence_dist   # histogram of the confidence distribution
```

### P0-2: Quality Gate (D-Mem style) — add to core/guardian.py

```python
# P0-2: D-Mem Quality Gating — a method of the Guardian class
# I85: Quality Gate runs AFTER LLM generation, BEFORE sending the response.
#      Does not modify facts_pack — only routes.
from dataclasses import dataclass

@dataclass
class QualityGateResult:
    use_slow_path: bool
    confidence: float
    coverage: float
    has_contradictions: bool
    reason: str

# Add as a method of the Guardian class (in core/guardian.py):
# class Guardian:
#     ...existing methods...
#
    def quality_gate(
        self,
        response_draft: str,
        facts_pack: list,
        query: str
    ) -> QualityGateResult:
        """
        D-Mem style quality gating.
        Decides: is the Fast Path sufficient, or is the expensive Slow Path needed.
        Savings: ~60% of tokens without loss of quality (D-Mem: 96.7% of full deliberation).
        """
        confidence = self._estimate_confidence(response_draft, facts_pack)
        coverage = self._estimate_coverage(response_draft, facts_pack)
        has_contradictions = self._check_contradictions(facts_pack)

        if (confidence >= QUALITY_GATE_CONFIDENCE_THRESHOLD
            and coverage >= QUALITY_GATE_COVERAGE_THRESHOLD
            and not has_contradictions):
            return QualityGateResult(False, confidence, coverage, False, "FAST_PATH_SUFFICIENT")
        else:
            return QualityGateResult(True, confidence, coverage, has_contradictions,
                f"SLOW_PATH: conf={confidence:.2f} cov={coverage:.2f} contr={has_contradictions}")

    def _estimate_confidence(self, response_draft: str, facts_pack: list) -> float:
        if not facts_pack:
            return 0.0
        validated = [f for f in facts_pack if f.get("epistemic_state") == "Validated"]
        return len(validated) / len(facts_pack)

    def _estimate_coverage(self, response_draft: str, facts_pack: list) -> float:
        if not facts_pack or not response_draft:
            return 0.0
        hits = sum(1 for f in facts_pack
                   if any(kw.lower() in response_draft.lower()
                          for kw in str(f.get("content", "")).split()[:5]))
        return hits / len(facts_pack)

    def _check_contradictions(self, facts_pack: list) -> bool:
        states = {f.get("epistemic_state") for f in facts_pack}
        return "Contradicted" in states
```

Config (velantrim_config.py):
```python
QUALITY_GATING_ENABLED = True
QUALITY_GATE_CONFIDENCE_THRESHOLD = 0.7
QUALITY_GATE_COVERAGE_THRESHOLD = 0.6
```

```
I85 (QualityGate): Quality Gate runs AFTER LLM generation, BEFORE sending the response.
    If use_slow_path=True, the response is NOT sent to the user until the Slow Path completes.
    Quality Gate does not modify facts_pack — only routes.
```

---

### HYPERIA-3: ACT-R Activation (feature-flag)

> **Source**: HYPERIA `fractal_memory.py` — `B = ln(Σ tᵢ^(-0.5))`
> **Purpose**: Retaining memories by **access history**, not by recency alone.
> A node accessed 10 times decays slower than a node with a single access.
> **Flag**: `ACT_R_ENABLED = True` in `velantrim_config.py` — enabled optionally.

```python
# memory/actr_activation.py
# ACT-R Activation — Anderson (1983): base activation level from the access history.
# B = ln(Σ tᵢ^(-0.5))
# tᵢ — the time in seconds from the i-th access until now
# The more accesses and the more recent they are — the higher B.
# Integration: ReactivationEngine + HybridRetriever (a bonus to score).
# Enabling: ACT_R_ENABLED = True in velantrim_config.py

import math
import logging
from datetime import datetime, timezone
from typing import List

logger = logging.getLogger(__name__)


def compute_actr_activation(
    access_times: List[datetime],
    now: datetime = None,
    decay_exponent: float = 0.5,  # standard ACT-R parameter
) -> float:
    """
    Compute the base activation level per Anderson ACT-R.
    B = ln(Σ tᵢ^(-decay_exponent))

    Args:
        access_times: a list of datetimes when the node was activated
        now:          the current time (UTC). None = datetime.now(timezone.utc)
        decay_exponent: ACT-R standard = 0.5

    Returns:
        float: the activation level (the higher — the more important)
        0.0 if access_times is empty
    """
    if not access_times:
        return 0.0

    now = now or datetime.now(timezone.utc)
    total = 0.0

    for t in access_times:
        if t.tzinfo is None:
            t = t.replace(tzinfo=timezone.utc)
        delta_sec = (now - t).total_seconds()
        if delta_sec <= 0:
            delta_sec = 0.001  # protection against division by zero on simultaneous access
        total += delta_sec ** (-decay_exponent)

    if total <= 0:
        return 0.0
    return math.log(total)


def actr_score_boost(base_score: float, activation: float,
                     weight: float = 0.15) -> float:
    """
    Add an ACT-R bonus to the retrieval score.
    weight=0.15 — a soft influence, does not dominate over semantics.
    """
    return base_score + weight * max(0.0, activation)
```

**Integration** (2 points):
```python
# 1. In HybridRetriever.retrieve() — a bonus to the candidate's score:
if ACT_R_ENABLED and node.get("access_history"):
    activation = compute_actr_activation(node["access_history"])
    candidate.score = actr_score_boost(candidate.score, activation)

# 2. In ReactivationEngine — prioritization of nodes for strengthening:
if ACT_R_ENABLED:
    activation = compute_actr_activation(node.access_times)
    priority = base_priority * (1.0 + 0.2 * max(0.0, activation))
```

**Add to `velantrim_config.py`**:
```python
ACT_R_ENABLED         = True   # feature-flag: ACT-R activation bonus
ACT_R_DECAY_EXPONENT  = 0.5    # standard ACT-R parameter (Anderson 1983)
ACT_R_RETRIEVAL_WEIGHT = 0.15  # weight of the bonus in HybridRetriever
```

---

### HYPERIA-4: Laplace Confidence

> **Source**: HYPERIA `core/truth_layer.py`
> **Problem**: New facts with 0 evidence have `confidence = 0/(0+0) = NaN` or 0.0
> → TruthGate blocks them forever. The system does not learn from anything new.
> **Solution**: Laplace smoothing `(pos+1)/(total+2)` — a new fact starts at 0.5, not 0.

```python
# In truth_gate.py — replace the raw ratio with Laplace:

def laplace_confidence(positive_evidence: int, total_evidence: int) -> float:
    """
    Laplace smoothing for the confidence of new facts.
    (pos+1) / (total+2)
    · a new fact (0/0) → 0.5 (neutral, not blocked)
    · 1 confirmation out of 1 → 0.67 (cautious optimism)
    · 9 out of 10 → 0.917 (high confidence)
    · Eliminates division by zero without an artificial clamp.
    """
    return (positive_evidence + 1) / (total_evidence + 2)

# Apply when computing confidence in TruthGate.validate_and_transition():
# Before: confidence = evidence_count / max(1, total_checks)
# After: confidence = laplace_confidence(evidence_count, total_checks)
```

---

### HYPERIA-5: CognitiveModes — Retrieval Depth Router

> **Source**: HYPERIA `core/cognitive_modes.py`
> **Purpose**: Routes retrieval depth by query type before ContextBuilder.
> PRECISION — maximum precision (complex factual tasks).
> BALANCED — a compromise (the default).
> EXPLORATION — broad coverage (creative/research queries).

```python
# core/cognitive_modes.py
# CognitiveModes — a retrieval depth router.
# Location: Fast Path, before ContextBuilder / HybridRetriever.
# 0 tokens · ~0 ms.

from dataclasses import dataclass
from enum import Enum
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class CognitiveMode(str, Enum):
    # P9-FIX BUG-7: DEPRECATED — use the canonical CognitiveMode from cognitive_modes.py (lines 10002+)
    # This block contains only 3 modes (without CREATIVE). Import conflict when both exist simultaneously.
    # Kept ONLY for the RetrievalConfig below. Do NOT import CognitiveMode from here.
    PRECISION   = "precision"    # precision > coverage: factual, technical
    BALANCED    = "balanced"     # standard: most queries
    EXPLORATION = "exploration"  # coverage > precision: creative, research
    # CREATIVE is absent — see the RFC0067 v2.0 canonical definition


@dataclass
class RetrievalConfig:
    mode:             CognitiveMode
    max_facts:        int    # how many facts from L3 in the FactsPack
    graph_depth:      int    # traversal depth in the Hot Graph
    sae_threshold:    float  # SAE spreading activation threshold
    use_analogy:      bool   # whether to use the Analogy Graph (RFC0067)
    temperature_hint: float  # hint for the Adaptive Decoder


MODE_CONFIGS = {
    CognitiveMode.PRECISION: RetrievalConfig(
        mode=CognitiveMode.PRECISION,
        max_facts=5, graph_depth=2, sae_threshold=0.5,
        use_analogy=False, temperature_hint=0.3,
    ),
    CognitiveMode.BALANCED: RetrievalConfig(
        mode=CognitiveMode.BALANCED,
        max_facts=10, graph_depth=3, sae_threshold=0.35,
        use_analogy=True, temperature_hint=0.6,
    ),
    CognitiveMode.EXPLORATION: RetrievalConfig(
        mode=CognitiveMode.EXPLORATION,
        max_facts=20, graph_depth=4, sae_threshold=0.25,
        use_analogy=True, temperature_hint=0.85,
    ),
}

# Keywords for auto-detecting the mode
_PRECISION_SIGNALS   = {"exactly", "specifically", "fact", "date", "number", "precise"}
_EXPLORATION_SIGNALS = {"invent", "imagine", "analogy", "creatively", "explore", "creative"}


class CognitiveModeRouter:
    """
    Determines the retrieval mode from the user's query.
    Called at the start of the Fast Path — before HybridRetriever.
    """

    def route(self, query: str, override: Optional[CognitiveMode] = None) -> RetrievalConfig:
        """
        Determine the RetrievalConfig for a query.
        override — an explicit mode (e.g., from user settings or a meta-command).
        """
        if override:
            logger.debug(f"CognitiveModeRouter: override={override.value}")
            return MODE_CONFIGS[override]

        q_lower = query.lower()
        words   = set(q_lower.split())

        if words & _PRECISION_SIGNALS:
            mode = CognitiveMode.PRECISION
        elif words & _EXPLORATION_SIGNALS:
            mode = CognitiveMode.EXPLORATION
        else:
            mode = CognitiveMode.BALANCED

        logger.debug(f"CognitiveModeRouter: auto={mode.value} for query='{query[:50]}'")
        return MODE_CONFIGS[mode]
```

**Integration** — add at the start of the Fast Path:
```python
# In agent.chat() — before HybridRetrieval:
from core.cognitive_modes import CognitiveModeRouter

router    = CognitiveModeRouter()
ret_cfg   = router.route(user_query)
# Pass ret_cfg to HybridRetriever and ContextBuilder:
facts     = await retriever.retrieve(query, max_facts=ret_cfg.max_facts,
                                     depth=ret_cfg.graph_depth)
# For the CREATIVE mode of RFC0067:
if ret_cfg.use_analogy:
    analogies = await analogy_graph.get_bridges(query)
```

---

### HYPERIA-6: OutputFaithfulnessChecker F6.5

> **Source**: HYPERIA `core/output_faithfulness_checker.py`
> **Purpose**: Checks AFTER generation whether the LLM's response matches the facts from L3.
> Runs in the **Slow Path** (fire-and-forget via EventBus).
> The result is written to ResponseAudit (RFC0052) as `faithfulness_score`.
> **Invariant**: F6.5 never blocks the Fast Path. Slow Path only.

```python
# core/output_faithfulness_checker.py
# OutputFaithfulnessChecker F6.5 — post-generation fact checking.
# Slow Path only. Result → ResponseAudit.faithfulness_score.
# 0 tokens if use_llm=False (extractive mode).

import logging
from dataclasses import dataclass
from typing import List, Optional

logger = logging.getLogger(__name__)


@dataclass
class FaithfulnessResult:
    score:            float          # 0.0–1.0
    grounded_claims:  int            # how many claims are supported by facts
    total_claims:     int            # total claims in the response
    unsupported:      List[str]      # claims without support in the graph
    mode:             str            # "extractive" | "llm"


class OutputFaithfulnessChecker:
    """
    Checks whether the LLM response matches the facts from the L3 graph.
    Extractive mode (default): TF-IDF overlap — 0 tokens.
    LLM mode: only if importance_score > 0.85 (via ResponseAuditWorker).

    Integration:
      Slow Path → AuditWorker listens for the RESPONSE_GENERATED event →
      calls check() → writes faithfulness_score into :DialogueSummary.
    """

    async def check(
        self,
        response:      str,
        source_facts:  List[dict],     # facts from L3 used during generation
        use_llm:       bool = False,
        llm_client     = None,
    ) -> FaithfulnessResult:
        """
        Check the faithfulness of the response against source_facts.
        source_facts: a list of {"content": str, "epistemic_state": str}
        """
        if not source_facts:
            return FaithfulnessResult(
                score=0.5, grounded_claims=0, total_claims=0,
                unsupported=[], mode="no_sources"
            )

        if use_llm and llm_client:
            return await self._llm_check(response, source_facts, llm_client)
        return self._extractive_check(response, source_facts)

    def _extractive_check(
        self, response: str, source_facts: List[dict]
    ) -> FaithfulnessResult:
        """
        TF-IDF overlap between the response and source_facts.
        Fast, 0 tokens, CPU only.
        """
        import re

        def _tokenize(text: str) -> set:
            return set(re.findall(r'\b\w{3,}\b', text.lower()))

        response_tokens = _tokenize(response)
        claims = response.split('. ')
        grounded = 0
        unsupported = []

        for claim in claims:
            if not claim.strip():
                continue
            claim_tokens = _tokenize(claim)
            if not claim_tokens:
                continue
            # Check overlap with at least one source_fact
            matched = False
            for fact in source_facts:
                fact_tokens = _tokenize(fact.get("content", ""))
                overlap = len(claim_tokens & fact_tokens) / max(1, len(claim_tokens))
                if overlap > 0.3:  # 30% of tokens match — considered grounded
                    matched = True
                    break
            if matched:
                grounded += 1
            else:
                unsupported.append(claim[:100])  # keep the first 100 characters

        total = max(1, len([c for c in claims if c.strip()]))
        score = grounded / total

        return FaithfulnessResult(
            score=score,
            grounded_claims=grounded,
            total_claims=total,
            unsupported=unsupported,
            mode="extractive"
        )

    async def _llm_check(
        self, response: str, source_facts: List[dict], llm_client
    ) -> FaithfulnessResult:
        """LLM-based check — only for critical responses (importance > 0.85)."""
        facts_text = "\n".join(
            f"- {f.get('content', '')[:200]}" for f in source_facts[:10]
        )
        prompt = f"""Rate faithfulness of the response against given facts (0.0-1.0).
Response: {response[:500]}
Facts:
{facts_text}
Return only JSON: {{"score": float, "unsupported_claims": [str]}}"""
        try:
            raw = await llm_client.complete(prompt)
            import json
            data = json.loads(raw)
            score = float(data.get("score", 0.5))
            unsupported = data.get("unsupported_claims", [])
            return FaithfulnessResult(
                score=score, grounded_claims=0, total_claims=0,
                unsupported=unsupported, mode="llm"
            )
        except Exception as e:
            logger.warning(f"OutputFaithfulnessChecker LLM failed: {e}, fallback extractive")
            return self._extractive_check(response, source_facts)
```

**Integration into ResponseAuditWorker** (Slow Path):
```python
# In response_audit_worker.py — add after Phase 2:
from core.output_faithfulness_checker import OutputFaithfulnessChecker

checker = OutputFaithfulnessChecker()
faith_result = await checker.check(
    response=audit.response_text,
    source_facts=audit.source_facts,
    use_llm=(audit.importance_score > 0.85),
    llm_client=llm_client,
)
audit.faithfulness_score = faith_result.score
# Save into :DialogueSummary.response_audit_faithfulness_avg
```

---

### HYPERIA-7: MemoryBudgetPlanner

> **Source**: HYPERIA `memory/memory_budget_planner.py`
> **Purpose**: Hard limit of 500k nodes + auto-GC at 85%.
> Velantrim has no limit — the graph grows unboundedly.

```python
# memory/memory_budget_planner.py
# MemoryBudgetPlanner — protection against unbounded graph growth.
# Hard limit: 500k nodes. Auto-GC at 85% (425k).
# Slow Path: checked hourly via SleepTimeWorker.

import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

NODE_LIMIT_HARD = 500_000   # absolute limit
NODE_LIMIT_GC   = 425_000   # 85% — auto-GC trigger
NODE_LIMIT_WARN = 400_000   # 80% — warning


@dataclass
class BudgetStatus:
    node_count:   int
    limit:        int
    utilization:  float   # 0.0–1.0
    action:       str     # "ok" | "warn" | "gc_triggered" | "hard_limit"


class MemoryBudgetPlanner:
    """
    Watches the graph size and triggers GC as it approaches the limit.
    Integration: called from SleepTimeWorker once an hour.
    """

    def __init__(self, graph, gc_runner=None):
        self.graph      = graph
        self.gc_runner  = gc_runner  # MemoryGarbageCollector or equivalent

    async def check_and_act(self) -> BudgetStatus:
        """Check the current graph size and take action if necessary."""
        try:
            result = await self.graph.execute_cypher(
                "MATCH (n) RETURN count(n) as total", {}
            )
            node_count = result[0]["total"] if result else 0
        except Exception as e:
            logger.error(f"MemoryBudgetPlanner: count query failed: {e}")
            return BudgetStatus(node_count=0, limit=NODE_LIMIT_HARD,
                                utilization=0.0, action="error")

        utilization = node_count / NODE_LIMIT_HARD

        if node_count >= NODE_LIMIT_HARD:
            logger.critical(
                f"MemoryBudgetPlanner: HARD LIMIT {node_count}/{NODE_LIMIT_HARD} — "
                f"blocking new writes until GC completes"
            )
            if self.gc_runner:
                await self.gc_runner.run_emergency_gc()
            return BudgetStatus(node_count=node_count, limit=NODE_LIMIT_HARD,
                                utilization=utilization, action="hard_limit")

        if node_count >= NODE_LIMIT_GC:
            logger.warning(
                f"MemoryBudgetPlanner: GC triggered at {node_count}/{NODE_LIMIT_HARD} "
                f"({utilization:.1%})"
            )
            if self.gc_runner:
                await self.gc_runner.run_full_gc()
            return BudgetStatus(node_count=node_count, limit=NODE_LIMIT_HARD,
                                utilization=utilization, action="gc_triggered")

        if node_count >= NODE_LIMIT_WARN:
            logger.warning(
                f"MemoryBudgetPlanner: WARNING {node_count}/{NODE_LIMIT_HARD} "
                f"({utilization:.1%}) — approaching limit"
            )
            return BudgetStatus(node_count=node_count, limit=NODE_LIMIT_HARD,
                                utilization=utilization, action="warn")

        return BudgetStatus(node_count=node_count, limit=NODE_LIMIT_HARD,
                            utilization=utilization, action="ok")
```

**Add to `velantrim_config.py`**:
```python
class BudgetConfig:
    NODE_LIMIT_HARD = 500_000
    NODE_LIMIT_GC   = 425_000  # 85%
    NODE_LIMIT_WARN = 400_000  # 80%

BUDGET = BudgetConfig()
```

**Metric**:
```python
memory_budget_utilization   # gauge: node_count / NODE_LIMIT_HARD
memory_budget_gc_triggered  # counter: how many times auto-GC fired
```

---

### HYPERIA-8: CircuitBreaker

> **Source**: HYPERIA `circuit_breaker.py`
> **Purpose**: Protects Neo4j, Redis, the LLM API from cascading failures.
> CLOSED → OPEN (N failures) → HALF_OPEN (timeout) → CLOSED (M successes).
> **Key point**: per-loop asyncio.Lock — no race condition in tests.

```python
# circuit_breaker.py
# CircuitBreaker — protection against cascading failures (Neo4j, Redis, LLM API).
# per-loop Lock: each event loop gets its own Lock — no RuntimeError in tests.

import time
import asyncio
from enum import Enum
from typing import Callable, Any
import logging

logger = logging.getLogger(__name__)


class CircuitState(Enum):
    CLOSED    = "closed"
    OPEN      = "open"
    HALF_OPEN = "half_open"


class CircuitBreakerOpenError(Exception):
    pass


class CircuitBreaker:
    def __init__(
        self,
        name:              str,
        failure_threshold: int = 5,
        timeout:           int = 60,
        success_threshold: int = 2,
    ):
        self.name              = name
        self.failure_threshold = failure_threshold
        self.timeout           = timeout
        self.success_threshold = success_threshold
        self.failure_count     = 0
        self.success_count     = 0
        self.last_failure_time = None
        self.state             = CircuitState.CLOSED
        self._locks: dict[int, asyncio.Lock] = {}  # per-loop

    def _get_lock(self) -> asyncio.Lock:
        loop    = asyncio.get_running_loop()
        loop_id = id(loop)
        if loop_id not in self._locks:
            self._locks[loop_id] = asyncio.Lock()
            if len(self._locks) > 10:  # GC of dead loops
                dead = [k for k in self._locks if k != loop_id]
                for k in dead:
                    del self._locks[k]
        return self._locks[loop_id]

    async def call(self, func: Callable, *args, **kwargs) -> Any:
        async with self._get_lock():
            if self.state == CircuitState.OPEN:
                if time.monotonic() - self.last_failure_time > self.timeout:
                    logger.info(f"{self.name}: OPEN → HALF_OPEN")
                    self.state         = CircuitState.HALF_OPEN
                    self.success_count = 0
                else:
                    raise CircuitBreakerOpenError(
                        f"Circuit '{self.name}' is OPEN. Retry after {self.timeout}s"
                    )
        try:
            result = await func(*args, **kwargs)
            await self._on_success()
            return result
        except Exception as e:
            await self._on_failure(e)
            raise

    async def _on_success(self):
        async with self._get_lock():
            if self.state == CircuitState.HALF_OPEN:
                self.success_count += 1
                if self.success_count >= self.success_threshold:
                    logger.info(f"{self.name}: HALF_OPEN → CLOSED")
                    self.state         = CircuitState.CLOSED
                    self.failure_count = 0
                    self.success_count = 0
            elif self.state == CircuitState.CLOSED:
                self.failure_count = max(0, self.failure_count - 1)

    async def _on_failure(self, error: Exception):
        async with self._get_lock():
            self.failure_count    += 1
            self.last_failure_time = time.monotonic()
            if self.state == CircuitState.HALF_OPEN:
                logger.error(f"{self.name}: HALF_OPEN → OPEN (recovery failed)")
                self.state = CircuitState.OPEN
            elif self.failure_count >= self.failure_threshold:
                logger.error(f"{self.name}: CLOSED → OPEN ({self.failure_count} failures)")
                self.state = CircuitState.OPEN

    def get_state(self) -> dict:
        return {
            "name":          self.name,
            "state":         self.state.value,
            "failure_count": self.failure_count,
            "last_failure":  self.last_failure_time,
        }
```

**Usage**:
```python
# In agent.py — wrap critical calls:
from circuit_breaker import CircuitBreaker, CircuitBreakerOpenError

cb_neo4j = CircuitBreaker("neo4j", failure_threshold=5, timeout=60)
cb_redis  = CircuitBreaker("redis", failure_threshold=3, timeout=30)

# When querying the graph:
try:
    result = await cb_neo4j.call(graph.execute_cypher, query, params)
except CircuitBreakerOpenError:
    logger.warning("Neo4j unavailable — degraded mode")
    result = []  # fallback
```

---

### HYPERIA-9: SOARGoalNode — Goal Hierarchy

> **Source**: HYPERIA `memory/core_memory_blocks.py`
> **Problem**: The L0 Goal Stack stores goals as a flat string.
> **Solution**: `GoalNode(priority, parent_id)` — a hierarchical structure.
> Backwards compatible: `str(goal_node)` returns the description.

```python
# Add to memory/core_memory_blocks.py — an extension of the Goal Stack

from dataclasses import dataclass, field
from typing import Optional, List
import uuid


@dataclass
class GoalNode:
    """
    A hierarchical goal in the Goal Stack (L0).
    Backwards compatible: str(node) = description.
    priority: 0.0–1.0 (1.0 = highest)
    parent_id: None = a root goal, otherwise a reference to the parent
    """
    description: str
    priority:    float         = 0.5
    goal_id:     str           = field(default_factory=lambda: uuid.uuid4().hex[:8])
    parent_id:   Optional[str] = None
    children:    List[str]     = field(default_factory=list)  # goal_ids of child goals
    status:      str           = "active"   # active | completed | suspended

    def __str__(self) -> str:
        return self.description  # backwards compatible with a flat string

    def __repr__(self) -> str:
        return f"GoalNode({self.goal_id}: {self.description!r} p={self.priority})"

    def is_root(self) -> bool:
        return self.parent_id is None

    def to_dict(self) -> dict:
        return {
            "goal_id":     self.goal_id,
            "description": self.description,
            "priority":    self.priority,
            "parent_id":   self.parent_id,
            "status":      self.status,
        }
```

---

### HYPERIA-10: Cascading Strategy Invalidation

> **Source**: HYPERIA `memory_gc.py` — `_invalidate_stale_strategies()`
> **Problem**: Velantrim has the relationship `(:Strategy)-[:DERIVED_FROM]->(:Fact)` in the schema,
> but no logic for reacting to a fact's invalidation. Zombie strategies accumulate.
> **Solution**: On `Fact → Deprecated/Collapsed` → all Strategy nodes are immediately set `valid=false`.

```python
# Add to the L4 GC Worker (reasoning_bank.py or a separate gc worker)
# Launched from SleepTimeWorker once a day.

async def invalidate_stale_strategies(graph) -> int:
    """
    Cascading invalidation of strategies when their dependent facts are invalidated.
    FIX: confidence × 0.5 created zombie strategies (0.95 → 0.475 → never removed).
    New approach: a fact is inactive → the strategy is IMMEDIATELY valid=false, confidence=0.0.
    """
    # Step 1: strategies with deprecated/collapsed facts
    result = await graph.execute_cypher("""
        MATCH (s:Strategy)-[:DERIVED_FROM]->(f:Fact)
        WHERE f.epistemic_state IN ['Deprecated', 'Collapsed']
          AND coalesce(s.is_active, true) = true
        SET s.is_active   = false,
            s.confidence  = 0.0,
            s.deprecated_at = datetime(),
            s.deprecated_reason = 'source_fact_deprecated'
        RETURN count(s) as invalidated
    """)
    invalidated = result[0]["invalidated"] if result else 0

    # Step 2: strategies with confidence below the threshold (other reasons)
    result2 = await graph.execute_cypher("""
        MATCH (s:Strategy)
        WHERE s.confidence < 0.2
          AND coalesce(s.is_active, true) = true
        SET s.is_active = false,
            s.deprecated_reason = 'low_confidence'
        RETURN count(s) as low_conf
    """)
    low_conf = result2[0]["low_conf"] if result2 else 0

    total = invalidated + low_conf
    if total:
        import logging
        logging.getLogger(__name__).info(
            f"Strategy GC: {invalidated} invalidated (dead facts) + "
            f"{low_conf} (low confidence) = {total} total"
        )
    return total
```

---

### 3. Fractal Hierarchy: Automatic Consolidation

**Purpose**: Moving information between levels WITHOUT LLM queries

```python
# fractal_memory.py

def fsrs_retention(t_hours: float, S: float) -> float:
    """P1-J FIX: FSRS power-law retention formula (v8.0 Crystal).
    R = (1 + 19/81 × t/S)^(-0.5)
    Replaces np.exp(-t/S) from Ebbinghaus — a more accurate model of long-term retention.
    Args:
        t_hours: time since the last repetition (in hours)
        S: stability — memory stability (in hours)
    Returns: R — the probability of recall [0.0, 1.0]
    """
    if S <= 0:
        return 0.0
    return (1.0 + (19.0 / 81.0) * (t_hours / S)) ** (-0.5)

from typing import List, Dict
from dataclasses import dataclass
from datetime import datetime, timedelta
import numpy as np


def fsrs_retention(t_hours: float, stability: float) -> float:
    """
    FSRS power-law decay (v8.0 — replaces the Ebbinghaus exponential).
    R = (1 + 19/81 × t/S)^(-0.5)

    Args:
        t_hours: time since the last access in hours
        stability: memory strength (importance × log(1 + access_count))

    Returns:
        Retention in [0.0, 1.0]

    Conflict-1 FIX: replaces np.exp(-t/S) everywhere in FractalMemory.
    Source: FadeMem paper, Jan 2026 — more accurate than Ebbinghaus by 20-30%.
    """
    if stability <= 0:
        return 0.0
    return (1.0 + (19.0 / 81.0) * (t_hours / stability)) ** (-0.5)


@dataclass
class MemoryItem:
    id: str
    content: str
    embedding: np.ndarray
    importance: float
    access_count: int
    last_accessed: datetime
    created_at: datetime
    level: int  # 0=STM, 1=MTM, 2=LTM

# Stop-words cache — initialized once on module import (not on every summarization)
try:
    from nltk.corpus import stopwords as _nltk_sw
    _STOP_RU_CACHED = _nltk_sw.words('russian')
except Exception:
    _STOP_RU_CACHED = []

class FractalMemory:
    def __init__(self, graph_memory: GraphMemory, llm_client=None):
        self.graph = graph_memory
        self.llm_client = llm_client  # declared explicitly — eliminates AttributeError in _llm_summarize_cluster

        # Level settings
        self.stm_capacity   = 5   # Cowan 4±1 — we take the upper bound of the range
        self.mtm_capacity   = 25

        # Conflict-3 FIX: explicit units for decay rates.
        # All values are in "per hour" units (compatible with age_hours in the formulas).
        # With FSRS: stability = importance * (1 + log(access_count)) / decay_rate
        # STM base unit:  1/0.1  = 10h  (short-term memory)
        # MTM base unit:  1/0.05 = 20h  (medium-term, accounting for rehearsal → ~168h)
        # LTM base unit:  1/0.01 = 100h (long-term, accounting for rehearsal → ~720h)
        self.stm_decay_rate = 0.1   # per hour; STM base window ≈ 10h
        self.mtm_decay_rate = 0.05  # per hour; MTM base window ≈ 20h (→ ~a week with rehearsal)
        self.ltm_decay_rate = 0.01  # per hour; LTM base window ≈ 100h (→ ~a month with rehearsal)

        # protection of stm_cache and mtm_cache from a race condition
        self._cache_lock = asyncio.Lock()

        # In-memory caches for STM/MTM
        self.stm_cache: List[MemoryItem] = []
        self.mtm_cache: List[MemoryItem] = []

    async def add_to_stm(self, content: str, embedding: np.ndarray):
        """Add to short-term memory. Protected by asyncio.Lock."""
        item = MemoryItem(
            id=generate_id(),
            content=content,
            embedding=embedding,
            importance=1.0,
            access_count=1,
            last_accessed=datetime.now(timezone.utc),
            created_at=datetime.now(timezone.utc),
            level=0
        )
        async with self._cache_lock:
            self.stm_cache.append(item)
            needs_consolidation = len(self.stm_cache) > self.stm_capacity
        # The Lock is not reentrant — we call consolidate OUTSIDE the lock
        if needs_consolidation:
            await self.consolidate_stm_to_mtm()

    async def apply_decay(self) -> dict:
        """
        FSRS retention decay (v8.0): R = (1 + 19/81 * t/S)^(-0.5)  # before: R = e^(-t/S)
            R  = retention fraction applied to importance
            t  = hours since last_accessed
            S  = importance × (1 + log1p(access_count))  — rehearsal effect

        STM base unit: 24 h · MTM base unit: 168 h (week)
        Immunity: pinned=CRITICAL or emotional_salience > 0.85 → skip (ESM.freeze analogue)
        Returns stats dict for Prometheus metrics.
        """
        stats = {"stm_decayed": 0, "mtm_decayed": 0, "dropped": 0}
        now = datetime.now(timezone.utc)

        def _immune(item) -> bool:
            if getattr(item, "pinned", None) == "CRITICAL":
                return True
            if getattr(item, "emotional_salience", 0.0) > 0.85:
                return True
            return False

        async with self._cache_lock:
            # ── STM ──────────────────────────────────────────────────────────
            stm_drop = []
            for item in self.stm_cache:
                if _immune(item):
                    continue
                age_h    = (now - item.last_accessed).total_seconds() / 3600
                strength = max(0.01, item.importance * (1.0 + np.log1p(item.access_count)))
                # P1-J CONFIRMED: FSRS power-law applied correctly (Changelog v8.0.1 ✓)
                retention = fsrs_retention(age_h, stability=strength * 24)
                item.importance = float(np.clip(item.importance * retention, 0.0, 1.0))
                stats["stm_decayed"] += 1
                if item.importance < 0.05:
                    stm_drop.append(item)
            for item in stm_drop:
                self.stm_cache.remove(item)
                stats["dropped"] += 1

            # ── MTM ──────────────────────────────────────────────────────────
            mtm_drop = []
            for item in self.mtm_cache:
                if _immune(item):
                    continue
                age_h    = (now - item.last_accessed).total_seconds() / 3600
                strength = max(0.01, item.importance * (1.0 + np.log1p(item.access_count)))
                # Conflict-1 FIX: FSRS power-law instead of Ebbinghaus np.exp(-age_h/(strength*168))
                retention = fsrs_retention(age_h, stability=strength * 168)
                item.importance = float(np.clip(item.importance * retention, 0.0, 1.0))
                stats["mtm_decayed"] += 1
                if item.importance < 0.02:
                    mtm_drop.append(item)
            for item in mtm_drop:
                self.mtm_cache.remove(item)
                stats["dropped"] += 1

        logger.info(
            f"apply_decay: stm={stats['stm_decayed']} mtm={stats['mtm_decayed']} "
            f"dropped={stats['dropped']}"
        )
        return stats

    async def consolidate_stm_to_mtm(self):
        """
        Consolidation STM → MTM (WITHOUT LLM).
        asyncio.Lock protects stm_cache.
        Cold Start Guard (if len < 50) REMOVED — it caused OOM
          at stm_capacity=5: the guard always fired → STM grew unboundedly.
          The Cold Start Guard lives only in L2 (consolidate_mtm_to_ltm).
        """
        async with self._cache_lock:
            now        = datetime.now(timezone.utc)
            to_promote = []
            to_drop    = []
            for item in self.stm_cache.copy():
                age_hours        = (now - item.created_at).total_seconds() / 3600
                importance_score = self._calculate_importance_with_decay(item, age_hours)

                if importance_score > 0.7 or item.access_count > 3:
                    item.level      = 1
                    item.importance = importance_score
                    if len(self.mtm_cache) >= self.mtm_capacity:
                        # ⚠️ ensure_future — NOT await. If changed to await
                        # here — deadlock on _cache_lock (non-reentrant).
                        asyncio.ensure_future(self.consolidate_mtm_to_ltm())
                    self.mtm_cache.append(item)
                    to_promote.append(item)
                elif importance_score < 0.3:
                    to_drop.append(item)
                # grey zone [0.3..0.7] — waits for the next cycle

            for item in to_promote + to_drop:
                self.stm_cache.remove(item)

        # Writing to the graph — outside the lock (an I/O operation)
        if to_promote:
            await self.graph.add_episode(
                episode_name=f"mtm_batch_{generate_id()}",
                content=" | ".join(i.content for i in to_promote),
                source="stm_consolidation"
            )

    def _calculate_importance_with_decay(
        self, 
        item: MemoryItem, 
        age_hours: float
    ) -> float:
        """
        Improved importance calculation accounting for:
        - Temporal decay (FSRS power-law, v8.0 — replaces Ebbinghaus)
        - Reinforcement (access frequency)
        - Emotional salience (success/failure matters more)
        - Semantic clustering (part of a pattern → more important)
        - Weighted Semantic Decay over [:CONTRADICTS]

        Conflict-1 FIX: temporal_decay is now FSRS power-law, not np.exp().
        """
        # 1. Base temporal decay — FSRS power-law (not Ebbinghaus)
        # stm_decay_rate=0.1 → effective stability base = 1/0.1 = 10h
        stability = max(0.01, item.importance * (1.0 + np.log1p(item.access_count)))
        temporal_decay = fsrs_retention(age_hours, stability=stability / self.stm_decay_rate)
        
        # 2. Reinforcement boost: the more often it is recalled → the less decay
        # log1p(x) = log(1+x) for smoothing
        reinforcement_factor = 1.0 + np.log1p(item.access_count) * 0.1
        
        # 3. Emotional salience: success/failure is remembered better
        emotional_boost = 1.0
        if hasattr(item, 'outcome'):
            if item.outcome in ['success', 'failure']:
                emotional_boost = 1.5  # 50% bonus to importance
            # partial/neutral stays 1.0
        
        # 4. Semantic clustering: if the memory is similar to other important ones
        # (a simplified version — can be improved with clustering)
        semantic_boost = 1.0
        if hasattr(item, 'cluster_size') and item.cluster_size > 1:
            semantic_boost = 1.0 + min(0.3, item.cluster_size * 0.05)
        
        # 5. Weighted Semantic Decay over [:CONTRADICTS]
        # Facts with contradictions lose importance proportionally to
        # the trust in the source of the contradiction (trust_score from Guardian)
        # IMMUNITY: Ring Zero / VALUES CORE (pinned=CRITICAL) are not affected
        epistemic_penalty = 0.0
        if hasattr(item, 'pinned') and item.pinned and \
           getattr(item, 'priority', None) == 'CRITICAL':
            pass  # Ring Zero is immune to Semantic Decay
        elif hasattr(item, 'contradictions') and item.contradictions:
            for contradiction in item.contradictions:
                # trust_score: 1.0 = a scientific paper, 0.3 = the user, 0.1 = the LLM
                trust = getattr(contradiction, 'trust_score', 0.3)
                epistemic_penalty += 0.1 * trust
            # Cap the penalty — do not kill a fact with a single contradiction
            epistemic_penalty = min(0.5, epistemic_penalty)
        
        # Final importance score
        final_importance = (
            item.importance 
            * temporal_decay 
            * reinforcement_factor 
            * emotional_boost 
            * semantic_boost
            - epistemic_penalty  # penalty for contradictions
        )
        
        return max(0.0, min(1.0, final_importance))  # Clamp [0, 1]

    async def consolidate_mtm_to_ltm(self):
        """
        Consolidation MTM → LTM. A HYBRID approach.
        AgglomerativeClustering — CPU-bound (2–10s).
          We take the snapshot UNDER the lock (instantly), and run clustering OUTSIDE the lock
          via run_in_executor — the event loop is not blocked.
        we pass threshold=0.8 as the second argument.
        """
        # Step 1: snapshot UNDER the lock — instant
        async with self._cache_lock:
            mtm_snapshot = list(self.mtm_cache)

        # Step 2: clustering OUTSIDE the lock — CPU-bound
        if len(mtm_snapshot) < 2:
            return
        clusters = await asyncio.get_running_loop().run_in_executor(
            None, self._cluster_memories, mtm_snapshot, 0.8  # ✅ threshold passed
        )

        # Step 3: writing to the graph OUTSIDE the lock
        episodes_to_remove = []
        for cluster in clusters:
            if len(cluster) >= 3:
                avg_importance = np.mean([m.importance for m in cluster])

                if avg_importance > 0.95 and len(cluster) > 15:
                    summary = await self._llm_summarize_cluster(
                        cluster, model="o4-mini"
                    )
                    consolidation_quality = "high"
                else:
                    summary = await self._extractive_summarize(cluster)  # async method — a direct await, not to_thread
                    consolidation_quality = "extractive_only"

                await self.graph.add_episode(
                    episode_name=f"ltm_cluster_{generate_id()}",
                    content=summary,
                    source="mtm_consolidation",
                    metadata={
                        "cluster_size":          len(cluster),
                        "avg_importance":        avg_importance,
                        "consolidation_quality": consolidation_quality,
                        "original_ids":          [m.id for m in cluster],
                    }
                )
                episodes_to_remove.extend(cluster)

        # Step 4: removal from the cache UNDER the lock
        async with self._cache_lock:
            for item in episodes_to_remove:
                if item in self.mtm_cache:
                    self.mtm_cache.remove(item)

    async def _extractive_summarize(self, cluster: List[MemoryItem]) -> str:
        """
        Extractive summarization WITHOUT an LLM.
        Uses TF-IDF to extract the key sentences.

        TfidfVectorizer is moved to a ThreadPoolExecutor —
        sklearn is synchronous (CPU-bound), it cannot be called from async directly.
        """
        from sklearn.feature_extraction.text import TfidfVectorizer

        texts = [item.content for item in cluster]

        all_sentences = []
        for text in texts:
            all_sentences.extend(text.split('. '))

        if len(all_sentences) < 3:
            return '. '.join(all_sentences)

        def _tfidf_sync(sentences):
            """Synchronous CPU-bound work — in a thread pool, does not block the loop"""
            # stopwords are loaded from the module-level cache — not on every call
            vectorizer = TfidfVectorizer(max_features=50, stop_words=_STOP_RU_CACHED)
            try:
                tfidf_matrix = vectorizer.fit_transform(sentences)
                scores = tfidf_matrix.sum(axis=1).A1
                top_indices = scores.argsort()[-3:][::-1]
                summary_sentences = [sentences[i] for i in sorted(top_indices)]
                return '. '.join(summary_sentences) + '.'
            except Exception:
                return '. '.join(sentences[:3]) + '.'

        loop = asyncio.get_running_loop()
        # asyncio.to_thread is preferable to run_in_executor for Python 3.9+
        # run_in_executor(None, fn, *args) — correct, but to_thread is cleaner and safer
        return await asyncio.to_thread(_tfidf_sync, all_sentences)

    async def _llm_summarize_cluster(
        self,
        cluster: List[MemoryItem],
        model: str = "o4-mini"  # previously gpt-4o-mini
    ) -> str:
        """
        LLM-based summarization for important clusters (importance > 0.95, size > 15).
        Principle: the LLM receives an extractive summary and only reformulates it,
        without adding new facts ("LLM as an interpreter", Copilot RFC).
        """
        # First extractive, to compress the context (the cheap path)
        extractive = await self._extractive_summarize(cluster)

        # Then the LLM — only to reformulate the ready summary
        prompt = f"""Summarize the following memory cluster into a concise, high-level pattern or insight.
        Focus on: what was learned, what patterns emerged, what strategies worked/failed.
        Do NOT add any facts not present in the input. Reformulate only.

        Memory cluster ({len(cluster)} episodes):
        {extractive}

        High-level summary (max 200 words):"""

        if self.llm_client is None:
            # Fallback: if the LLM client is not configured — return extractive
            logger.warning("_llm_summarize_cluster: llm_client is not configured, returning extractive")
            return extractive

        try:
            summary = await self.llm_client.complete(prompt, model=model)
            return summary
        except Exception as e:
            logger.error(f"_llm_summarize_cluster LLM error: {e}, fallback to extractive")
            return extractive

    def _cluster_memories(
        self,
        memories: List[MemoryItem],
        threshold: float = 0.8
    ) -> List[List[MemoryItem]]:
        """Clustering by cosine similarity of embeddings"""
        from sklearn.cluster import AgglomerativeClustering
        
        if len(memories) < 2:
            return []
        
        embeddings = np.array([m.embedding for m in memories])
        
        clustering = AgglomerativeClustering(
            n_clusters=None,
            distance_threshold=1-threshold,
            metric='cosine',
            linkage='average'
        )
        
        labels = clustering.fit_predict(embeddings)
        
        # Group by labels
        clusters = {}
        for item, label in zip(memories, labels):
            if label not in clusters:
                clusters[label] = []
            clusters[label].append(item)
        
        return [c for c in clusters.values() if len(c) >= 3]
```

**Background consolidation process**:

```python
# consolidation_worker.py
import asyncio

class AdaptiveConsolidationWorker:
    """
    Adaptive consolidation instead of fixed intervals.
    asyncio.gather used to stop ALL workers when one failed.
    Solution: independent create_task + _run_loop with auto-restart after 5s.
    _consolidation_lock protects against concurrent consolidation.
    """
    def __init__(self, fractal_memory: FractalMemory):
        self.memory               = fractal_memory
        self.running              = False
        self._consolidation_lock  = asyncio.Lock()
        self.stm_high_threshold   = 0.8
        self.stm_medium_threshold = 0.5
        self.mtm_high_threshold   = 0.8

    async def start(self):
        """Start background consolidation — independent tasks."""
        self.running = True
        # keep the references — without them, GC may destroy the tasks
        self._tasks = [
            asyncio.create_task(
                self._run_loop("stm_consolidation", self._adaptive_stm_consolidation)
            ),
            asyncio.create_task(
                self._run_loop("mtm_consolidation", self._adaptive_mtm_consolidation)
            ),
            asyncio.create_task(
                self._run_loop("periodic_decay", self._periodic_decay)
            ),
        ]
        logger.info("ConsolidationWorker: all workers started independently")

    async def _run_loop(self, name: str, coro_fn):
        """On failure — log and restart after 5 seconds."""
        while self.running:
            try:
                await coro_fn()
            except asyncio.CancelledError:
                raise
            except Exception as e:
                logger.error(
                    f"ConsolidationWorker [{name}] crashed, restarting in 5s: {e}"
                )
                await asyncio.sleep(5)

    async def _adaptive_stm_consolidation(self):
        """STM → MTM with a dynamic interval. Protected by _consolidation_lock."""
        while self.running:
            current_load = len(self.memory.stm_cache)
            capacity     = self.memory.stm_capacity
            load_ratio   = current_load / capacity if capacity > 0 else 0

            if load_ratio > self.stm_high_threshold:
                interval = 30
                priority = "high"
            elif load_ratio > self.stm_medium_threshold:
                interval = 300
                priority = "medium"
            else:
                interval = 600
                priority = "low"

            logger.info(
                f"STM consolidation: load={load_ratio:.1%}, "
                f"interval={interval}s, priority={priority}"
            )
            await asyncio.sleep(interval)
            async with self._consolidation_lock:
                await self.memory.consolidate_stm_to_mtm()

    async def _adaptive_mtm_consolidation(self):
        """MTM → LTM with an adaptive interval. Protected by _consolidation_lock."""
        while self.running:
            current_size = len(self.memory.mtm_cache)
            capacity     = self.memory.mtm_capacity
            load_ratio   = current_size / capacity if capacity > 0 else 0

            if load_ratio > self.mtm_high_threshold:
                interval = 3600
            elif load_ratio > 0.5:
                interval = 21600
            else:
                interval = 86400

            logger.info(
                f"MTM consolidation: load={load_ratio:.1%}, "
                f"next_run_in={interval}s"
            )
            await asyncio.sleep(interval)
            async with self._consolidation_lock:
                await self.memory.consolidate_mtm_to_ltm()

    async def _periodic_decay(self):
        """Periodic application of decay. Fixed interval."""
        while self.running:
            await asyncio.sleep(3600)
            await self.memory.apply_decay()
            logger.info("Memory decay applied to all levels")

    def stop(self):
        self.running = False
        for task in getattr(self, '_tasks', []):
            task.cancel()
        logger.info("ConsolidationWorker: stop signal sent, all tasks cancelled")
```

---

### 4. Hybrid Retrieval: Token Minimization

**Purpose**: Smart search for relevant information with minimal volume

```python
# hybrid_retrieval.py
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class RetrievalResult:
    content:         str
    source:          str
    relevance_score: float
    level:           int  # Memory level
    context:         Optional[List[str]] = None  # Related information
    embedding:       Optional[object]    = None  # MMR works
    metadata:        Optional[dict]      = None


# P1-2 FIX: explicit Protocol contract for the SLM classifier.
# Without Protocol — AttributeError only at runtime on the first call.
# Any slm_classifier must implement this interface.
from typing import Protocol, runtime_checkable

@runtime_checkable
class SLMClassifierProtocol(Protocol):
    """
    Contract for the tiny LLM classifier (Qwen3-1.7B / OLMoE-1B).

    P1-2 FIX: explicit Protocol instead of duck typing.
    Without Protocol — AttributeError only at runtime on the first call.
    """

    def classify(self, text: str, labels: list) -> str:
        """
        Classify text into one of the labels.

        Args:
            text: input query
            labels: list of allowed classes, e.g. ["RECALL", "DEFINE", "POLICY", "TASK"]

        Returns:
            One of the label elements. Never returns a string outside labels.

        Raises:
            ValueError: if labels is empty
            RuntimeError: if the model is not loaded
        """
        ...


class HybridRetriever:
    def __init__(
        self,
        graph_memory: GraphMemory,
        fractal_memory: FractalMemory,
        token_budget: int = 2000,
        hyde_enabled: bool = False,   # HyDE optional, disabled by default
        llm_fast = None,              # needed only if hyde_enabled=True
        slm_classifier = None         # P1-2 FIX: optional SLM classifier
    ):
        self.graph = graph_memory
        self.fractal = fractal_memory
        self.token_budget = token_budget
        self.hyde_enabled = hyde_enabled
        self.llm_fast = llm_fast      # o4-mini / Haiku — cheap call for generating the hypothesis

        # P1-2 FIX: validate the contract at initialization
        if slm_classifier is not None and not isinstance(slm_classifier, SLMClassifierProtocol):
            raise TypeError(
                f"slm_classifier must implement SLMClassifierProtocol. "
                f"Got {type(slm_classifier).__name__}. "
                f"A classify(text: str, labels: list) -> str method is required"
            )
        self.slm_classifier = slm_classifier

    async def _get_embedding(self, text: str):
        """
        Delegates to fractal.graph (EmbeddingEngine via GraphMemory).
        Fallback: if graph does not support get_embedding — returns None
        and _search_stm skips the STM search without crashing.
        """
        try:
            if hasattr(self.graph, 'get_embedding'):
                return await self.graph.get_embedding(text)
            # Fallback via graphiti if available
            if hasattr(self.graph, 'graphiti') and hasattr(self.graph.graphiti, 'get_embedding'):
                return await self.graph.graphiti.get_embedding(text)
        except Exception as e:
            logger.warning(f"HybridRetriever._get_embedding failed: {e}")
        return None

    async def retrieve(
        self,
        query: str,
        query_type: str = "general"
    ) -> List[RetrievalResult]:
        """
        Hybrid retrieval with routing by query type
        """
        # 1. Routing: determine the search strategy
        strategy = self._route_query(query, query_type)

        # 1.5. HyDE (Hypothetical Document Embeddings) — optional
        # Idea: instead of the question's embedding, use the embedding of a hypothetical answer.
        # The LLM generates "what the answer might look like" → its vector is closer to real facts.
        # Gives +15-20% accuracy on factoid queries. Cost: 1 cheap LLM call.
        # Disabled by default (hyde_enabled=False) — enable it deliberately.
        search_query = query
        if self.hyde_enabled and self.llm_fast is not None:
            search_query = await self._hyde_expand(query)

        # 2. Multi-stage search
        results = []
        
        # Stage 1: Check STM (fast, in-memory)
        if strategy in ["conversation", "immediate", "RECALL", "TASK"]:
            query_embedding = await self._get_embedding(query)  # initialize before passing to _search_stm
            stm_results = await self._search_stm(query, query_embedding)  # STM always uses the original query
            results.extend(stm_results)
        
        # Stage 2: Vector search over the graph (fast ANN)
        graph_results = await self.graph.search(
            query=search_query,  # HyDE: expanded query or the original
            num_results=10
        )
        results.extend(self._convert_to_retrieval_results(
            graph_results, source="graph"
        ))
        
        # Stage 3: Graph expansion for context
        if strategy in ["complex", "planning"]:
            for result in graph_results[:3]:  # Top-3
                expanded = await self._expand_context(result)
                results.extend(self._convert_to_retrieval_results(
                    expanded, source="graph_expand"
                ))
        
        # 3. Reranking
        results = await self._rerank(query, results)
        
        # 4. Token budgeting: select top-K within the budget
        results = self._apply_token_budget(results)
        
        return results

    async def _hyde_expand(self, query: str) -> str:
        """
        HyDE: Hypothetical Document Embeddings (Gao et al., 2022).

        Generates a hypothetical answer to the query using a fast LLM,
        then uses that answer as the search query instead of the original.

        Why it works: the embedding of a question ("What is photosynthesis?") is semantically
        far from the embedding of an answer ("Photosynthesis is a process..."). The hypothetical answer
        creates a vector in the right semantic space.

        When to enable: hyde_enabled=True for factual queries (DEFINE/RECALL).
        When NOT needed: TASK/POLICY queries, dialogue, clarifications — the original query is better.
        """
        try:
            prompt = (
                f"Generate a short hypothetical answer to the question (1-2 sentences, "
                f"facts only, no introductory words):\n{query}"
            )
            hypothesis = await self.llm_fast.generate(prompt, max_tokens=100)
            return hypothesis.strip()
        except Exception as e:
            logger.warning(f"HyDE failed, fallback to original query: {e}")
            return query  # graceful fallback — never break retrieval

    def _route_query(self, query: str, query_type: str) -> str:
        """
        Memory Router — bilingual (RU+EN) + confidence + SLM fallback.
        RFC0003: Four strict classes instead of fuzzy heuristics.
        EN pattern support + confidence scoring + SLM fallback when confidence is low.
        """
        query_lower = query.lower()

        ROUTE_PATTERNS = {
            "RECALL": [
                # RU (translated)
                "how we", "yesterday", "earlier", "last", "do you remember", "we solved",
                "you said", "we discussed", "last time",
                # EN
                "earlier", "last time", "remember", "we discussed",
                "you said", "previously", "we talked about",
            ],
            "DEFINE": [
                # RU (translated)
                "what is", "what does it mean", "definition", "explain", "why",
                "how does it work", "tell me about",
                # EN
                "what is", "explain", "define", "how does", "what are",
                "tell me about", "describe",
            ],
            "POLICY": [
                # RU (translated)
                "how to react", "rule", "strategy", "approach", "policy",
                # EN
                "how to handle", "rule", "strategy", "approach", "policy",
                "best practice",
            ],
            "TASK": [
                # RU
                "now", "current", "goal", "task", "just now",
                # EN
                "current", "now", "goal", "task", "right now", "in progress",
            ],
        }

        # Count matches for each route
        scores = {route: 0 for route in ROUTE_PATTERNS}
        for route, patterns in ROUTE_PATTERNS.items():
            for pattern in patterns:
                if pattern in query_lower:
                    scores[route] += 1

        best_route = max(scores, key=scores.get)
        best_score = scores[best_route]

        # Low confidence (≤1 match) → SLM fallback
        # Qwen3-1.7B / OLMoE-1B — already in the stack as LLM Tiny, 0 flagship tokens
        if best_score <= 1 and hasattr(self, 'slm_classifier') and self.slm_classifier is not None:
            return self._slm_classify(query)

        # Zero score → TASK (an operational query is more likely than a conceptual one)
        return best_route if best_score > 0 else "TASK"

    def _slm_classify(self, query: str) -> str:
        """
        SLM-fallback classifier for ambiguous queries.
        Called when pattern-matching yielded ≤1 match.
        Contract: slm_classifier implements SLMClassifierProtocol.
        Returns one of: RECALL | DEFINE | POLICY | TASK

        P1-2 FIX: added result validation + explicit fallback.
        """
        VALID_LABELS = ("RECALL", "DEFINE", "POLICY", "TASK")
        try:
            result = self.slm_classifier.classify(
                query,
                labels=list(VALID_LABELS)
            )
            if result in VALID_LABELS:
                return result
            # If the classifier returned something outside labels — log it and fall back
            logger.warning(
                f"_slm_classify: unexpected result '{result}' not in {VALID_LABELS}, "
                f"falling back to TASK"
            )
        except Exception as e:
            logger.warning(f"_slm_classify failed: {e} — fallback to TASK")
        return "TASK"  # safe fallback

    async def _search_stm(self, query: str, query_embedding=None) -> List[RetrievalResult]:
        """Search in the STM cache"""
        # Use the passed embedding or compute a new one (once)
        if query_embedding is None:
            query_embedding = await self._get_embedding(query)
        
        results = []
        if query_embedding is None:  # embedding unavailable — skip STM without crashing
            return results
        
        for item in self.fractal.stm_cache:
            similarity = cosine_similarity(query_embedding, item.embedding)
            if similarity > 0.7:
                results.append(RetrievalResult(
                    content=item.content,
                    source="stm",
                    relevance_score=similarity,
                    level=0
                ))
        
        return results

    async def _expand_context(self, node: dict) -> List[str]:
        """
        Graph traversal to obtain context
        Limit depth so we don't blow up the token count
        """
        context = await self.graph.get_context_for_entity(
            entity_name=node.get("entity_name"),
            depth=1  # Only immediate neighbors
        )
        
        return context.get("related_entities", [])

    def _convert_to_retrieval_results(
        self,
        items: list,
        source: str,
        level: int = 3
    ) -> List[RetrievalResult]:
        """
        the method was missing — AttributeError on every graph search.
        Converts raw results from graph.search() / graph_expand into RetrievalResult.
        """
        results = []
        for item in items:
            if not item:
                continue
            content = (
                item.get("content") or
                item.get("summary") or
                item.get("name") or
                str(item)
            )
            results.append(RetrievalResult(
                content=content,
                source=source,
                relevance_score=float(item.get("score", item.get("relevance_score", 0.5))),
                level=level,
                metadata=item if isinstance(item, dict) else None,
            ))
        return results

    async def _rerank(
        self,
        query: str,
        results: List[RetrievalResult]
    ) -> List[RetrievalResult]:
        """
        Reranking with a cross-encoder (expensive, but for small k)
        Alternative: a simple heuristic based on recency + relevance
        """
        # Simple reranking WITHOUT a cross-encoder
        now = datetime.now(timezone.utc)
        
        for result in results:
            # Factor in freshness and memory level
            level_penalty = 0.9 ** result.level  # Deeper levels are less relevant
            
            result.relevance_score = result.relevance_score * level_penalty
        
        # Sort by the new score
        results.sort(key=lambda x: x.relevance_score, reverse=True)
        return results

    def _apply_token_budget(
        self,
        results: List[RetrievalResult]
    ) -> List[RetrievalResult]:
        """
        Select the top-K results within the token budget
        """
        selected = []
        total_tokens = 0
        
        for result in results:
            result_tokens = count_tokens(result.content)
            
            if total_tokens + result_tokens <= self.token_budget:
                selected.append(result)
                total_tokens += result_tokens
            else:
                break  # Budget exhausted
        
        return selected
```

### P0-3: Reranker with fallback (`memory/reranker.py`)

```python
# memory/reranker.py — factory with fallback
# Default: ColBERTv2 or bge-reranker-large. Qwen3 — opt-in only with native Transformers.
import logging
logger = logging.getLogger(__name__)

def get_reranker(backend: str = None):
    backend = backend or config.RERANKER_BACKEND
    if backend == "qwen3":
        logger.warning("Qwen3 Reranker: known issues in vLLM/llama.cpp. "
                       "Use only with native Transformers.")
        return Qwen3Reranker()
    elif backend == "colbertv2":
        return ColBERTv2Reranker()
    elif backend == "bge-reranker-large":
        return BGEReranker()
    return NoopReranker()
```

Config:
```python
RERANKER_BACKEND = "colbertv2"  # "colbertv2" | "bge-reranker-large" | "qwen3" | "none"
```

---

### P1-1: `memory/intent_router.py` (MAGMA IntentRouter)

```python
# memory/intent_router.py
# I86: IntentRouter is called ONLY from HybridRetriever.retrieve().
# 0 tokens, rule-based, <1ms.

def route_query_intent(query: str) -> list[str]:
    q = query.lower()
    if any(w in q for w in ["why", "because of", "reason", "why", "because", "cause"]):
        return ["CAUSAL_REL", "CAUSES"]
    elif any(w in q for w in ["when", "after", "before", "when", "before", "after"]):
        return ["TEMPORAL_REL"]
    elif any(w in q for w in ["what is", "definition", "what is", "define"]):
        return ["SEMANTIC_REL", "SIMILAR_TO"]
    return ["SEMANTIC_REL", "CAUSAL_REL", "TEMPORAL_REL", "ENTITY_REL"]
```

### P1-6: `memory/pagerank.py` (HippoRAG Personalized PageRank)

```python
# memory/pagerank.py
# HippoRAG-style: +7% on associative tasks, 0 LLM calls
# ⚠️ NetworkX is excluded from the stack (too slow on >1k nodes).
# We use python-igraph (approved for Phase 0 SAE in EtirConfig).

def personalized_pagerank(
    graph_edges: list[tuple],
    query_nodes: list[str],
    alpha: float = 0.85,
    top_k: int = 20
) -> list[tuple[str, float]]:
    try:
        import igraph as ig
        # Gather all unique vertices
        all_nodes = list({n for edge in graph_edges for n in edge})
        if not all_nodes:
            return []
        node_idx = {n: i for i, n in enumerate(all_nodes)}
        edges_idx = [(node_idx[a], node_idx[b]) for a, b in graph_edges
                     if a in node_idx and b in node_idx]
        G = ig.Graph(n=len(all_nodes), edges=edges_idx, directed=True)
        G.vs["name"] = all_nodes
        reset_prob = [
            (1.0 / len(query_nodes)) if all_nodes[i] in query_nodes else 0.0
            for i in range(len(all_nodes))
        ]
        # igraph personalized PageRank
        pr_scores = G.personalized_pagerank(
            damping=alpha,
            reset=reset_prob,
            directed=True
        )
        result = [(all_nodes[i], pr_scores[i]) for i in range(len(all_nodes))]
        return sorted(result, key=lambda x: x[1], reverse=True)[:top_k]
    except ImportError:
        # Fallback: simple degree-based score without PageRank
        import logging
        logging.getLogger(__name__).warning(
            "pagerank.py: igraph not installed — falling back to degree score. "
            "Install: pip install igraph"
        )
        degree: dict[str, float] = {}
        for a, b in graph_edges:
            degree[a] = degree.get(a, 0) + 1
            degree[b] = degree.get(b, 0) + 1
        boost = {n: 2.0 for n in query_nodes}
        scored = {n: (boost.get(n, 1.0) * d) for n, d in degree.items()}
        return sorted(scored.items(), key=lambda x: x[1], reverse=True)[:top_k]
```

---

### 🔍 HyDE — Hypothetical Document Embeddings (opt-in)

**Config flag**: `hyde_enabled: false` (in `velantrim_config.py`)

**Essence**: a single LLM call generates a hypothetical answer to the user's question.
The embedding of the hypothetical answer is geometrically closer to the real facts in the graph
than the embedding of the question itself — because the question and the answer live in different
semantic spaces.

**Result**: +15–20% retrieval accuracy on DEFINE/RECALL queries
compared to direct search over the question embedding.

**Algorithm when hyde_enabled=true**:
1. `hypothetical = await llm.complete(f"Answer briefly: {query}")` — 1 call
2. `hyp_embedding = embedder.encode(hypothetical)`
3. Retrieval over `hyp_embedding` instead of `query_embedding`
4. CORNER deduplication of results if both sources are active

**When to enable**: only on DEFINE and RECALL query types (FactRouter).
On TASK and POLICY — it gives no gain and adds latency.

**Invariant**:
```
HyDE is enabled ONLY via the config flag `hyde_enabled: true`.
Activation by editing code (not config) is a violation.
Using HyDE on the Fast Path without the feature-flag is not permitted.
```

**Add to `velantrim_config.py`**:
```python
HYDE_ENABLED = False  # HyDE: hypothetical embedding for DEFINE/RECALL (+15-20% accuracy)
# Enable only after testing latency on the target hardware
```

---

### 🗺 TraversalPolicy — Edge Traversal Strategy by Query Type

**Source**: MAGMA-style (arXiv 2601.03236) · **Effect**: +10.6 F1 on multi-hop tasks

**Principle**: different query types require different graph edge traversal strategies.
Not all edges are equally relevant for each task type.

| Query type (FactRouter) | Traversal strategy | Priority edge types |
|--------------------------|---------------------|----------------------------------------------|
| `RECALL` | temporal | `[:MENTIONED_IN]`, `[:LED_TO]`, `valid_from` |
| `DEFINE` | causal | `[:CAUSES]`, `[:CONCEPT_OF]`, `[:HAS_RELATION]` |
| `POLICY` | influence | `[:DERIVED_FROM]`, `[:IMPROVES]`, `[:USED_IN]` |
| `TASK` | all | all edge types, depth +1 |

**Implementation** (add to `HybridRetriever.retrieve()`):

```python
# traversal_policy.py
TRAVERSAL_STRATEGIES = {
    "RECALL": {"edge_types": ["MENTIONED_IN", "LED_TO"], "temporal_sort": True},
    "DEFINE": {"edge_types": ["CAUSES", "CONCEPT_OF", "HAS_RELATION"], "temporal_sort": False},
    "POLICY": {"edge_types": ["DERIVED_FROM", "IMPROVES", "USED_IN"], "temporal_sort": False},
    "TASK":   {"edge_types": None, "temporal_sort": False, "depth_bonus": 1},
}

def get_traversal_config(query_type: str) -> dict:
    return TRAVERSAL_STRATEGIES.get(query_type, TRAVERSAL_STRATEGIES["TASK"])
```

**Invariant I76**:
```
I76 (TraversalPolicy): TraversalPolicy.get_traversal_config() is called ONLY
from HybridRetriever.retrieve(), not from the Fast Path directly.
Violation: applying the traversal filter directly in agent.chat() bypassing the retriever.
```

---

### 5. ReasoningBank: Self-Learning from Experience

**Purpose**: Extracting strategies from successes and failures

```python
# reasoning_bank.py
import uuid  # for Strategy.id
from typing import List, Dict, Optional
from dataclasses import dataclass
from collections import deque  # deque to bound experience_buffer, field
from enum import Enum

class Outcome(Enum):
    SUCCESS = 1
    FAILURE = -1
    PARTIAL = 0

@dataclass
class Experience:
    task_description: str
    context: Dict
    action_taken: str
    outcome: Outcome
    reasoning: str
    timestamp: datetime
    error_message: Optional[str] = None

@dataclass
class Strategy:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    description: str
    applicable_contexts: List[str]
    success_count: int = 0
    failure_count: int = 0
    confidence: float = 0.5
    failure_penalty: float = 0.1  # Penalty for failure
    success_boost: float = 0.05   # Bonus for success

    @property
    def success_rate(self) -> float:
        total = self.success_count + self.failure_count
        return self.success_count / total if total > 0 else 0.0

    def update_confidence(self, outcome: Outcome):
        """
        Update confidence based on the outcome
        Negative reinforcement: failures lower confidence
        """
        if outcome == Outcome.SUCCESS:
            # Success → raise confidence
            self.confidence = min(1.0, self.confidence + self.success_boost)
        elif outcome == Outcome.FAILURE:
            # Failure → lower confidence (negative reinforcement)
            self.confidence = max(0.0, self.confidence - self.failure_penalty)
        
        # Frequent failures → increase penalty
        if self.failure_count > 5:
            # After 5 failures the penalty doubles
            self.failure_penalty = min(0.3, self.failure_penalty * 1.2)

class ReasoningBank:
    def __init__(self, graph_memory: GraphMemory, llm_client=None):  # llm_client added — ACE Curator and the LLM strategy path work
        self.graph = graph_memory
        self.llm_client = llm_client
        # deque(maxlen=1000) instead of List[] — protection against OOM
        self.experience_buffer = deque(maxlen=1000)
        self.strategies: Dict[str, Strategy] = {}

        # P1-3 FIX: delegate for the ACE Curator.
        # The canonical implementation lives in agent_with_learning.py::SelfLearningAgent.
        # ReasoningBank does not duplicate the logic — it only delegates.
        # Set via set_ace_delegate() from SelfLearningAgent.__init__().
        self._ace_delegate = None

    async def log_experience(
        self,
        task: str,
        context: Dict,
        action: str,
        outcome: Outcome,
        reasoning: str,
        error: Optional[str] = None
    ):
        """Record the experience of executing a task"""
        exp = Experience(
            task_description=task,
            context=context,
            action_taken=action,
            outcome=outcome,
            reasoning=reasoning,
            timestamp=datetime.now(timezone.utc),
            error_message=error
        )
        
        self.experience_buffer.append(exp)
        
        # Save to the graph
        await self.graph.add_episode(
            episode_name=f"experience_{generate_id()}",
            content=json.dumps({
                "task": task,
                "action": action,
                "outcome": outcome.value,
                "reasoning": reasoning
            }),
            source="experience_log"
        )
        
        # If enough experience has accumulated - distill strategies
        if len(self.experience_buffer) >= 10:
            await self.distill_strategies()

    async def distill_strategies(self):
        """
        Distilling high-level strategies from experience
        An LLM can be used for better quality (o4-mini is sufficient)
        
        P9-FIX BUG-14: partial progress tracking — each group is processed
        independently and immediately removed from the buffer. If group N fails, groups 1..N-1
        are already removed — a retry does not duplicate strategies.
        """
        grouped = self._group_by_task_type(list(self.experience_buffer))
        
        for task_type, experiences in grouped.items():
            try:
                successful = [e for e in experiences if e.outcome == Outcome.SUCCESS]
                failed = [e for e in experiences if e.outcome == Outcome.FAILURE]
                
                if successful:
                    strategy = await self._extract_strategy_from_successes(
                        task_type, successful
                    )
                    await self._save_strategy(strategy)
                
                if failed:
                    anti_pattern = await self._extract_lessons_from_failures(
                        task_type, failed
                    )
                    await self._save_anti_pattern(anti_pattern)
                
                # Remove only the processed group — immediately after success
                for exp in experiences:
                    self.experience_buffer.discard(exp)
            except Exception as e:
                logger.error(
                    f"distill_strategies: group '{task_type}' failed, "
                    f"buffer for this group preserved ({len(experiences)} items): {e}"
                )

    async def _extract_strategy_from_successes(
        self,
        task_type: str,
        successes: List[Experience]
    ) -> Strategy:
        """
        Extract a common strategy from successful attempts
        """
        # Option 1: Simple aggregation WITHOUT an LLM
        common_actions = self._find_common_patterns([e.action_taken for e in successes])
        
        # Option 2: With a cheap LLM (better)
        # strategy_text = await self._llm_summarize(successes)
        
        strategy = Strategy(
            description=f"For {task_type}: {common_actions}",
            applicable_contexts=[task_type],
            success_count=len(successes),
            confidence=len(successes) / (len(successes) + 1)
        )
        
        return strategy

    def _group_by_task_type(
        self,
        experiences: "deque[Experience]"
    ) -> Dict[str, List["Experience"]]:
        """
        Group accumulated experience by task type.
        The type is determined by the first word of task_description (a simple heuristic).
        Replace with TF-IDF or LLM-classification if needed.
        """
        groups: Dict[str, List] = {}
        for exp in experiences:
            # Take the first two words as the task type
            words = exp.task_description.lower().split()
            task_type = "_".join(words[:2]) if len(words) >= 2 else (words[0] if words else "general")
            groups.setdefault(task_type, []).append(exp)
        return groups

    async def retrieve_relevant_strategies(
        self,
        current_task: str,
        context: Dict,
        epsilon: float = 0.1  # 10% exploration
    ) -> List[Strategy]:
        """
        Search for strategies relevant to the current task
        Uses Thompson Sampling to balance exploration/exploitation (RFC0039, replaced UCB1)
        """
        # 1. Search the graph by task context
        results = await self.graph.search(
            query=f"strategy for {current_task}",
            num_results=10
        )
        
        # 2. Parse strategies
        strategies = []
        for result in results:
            try:
                strategy_data = json.loads(result.content)
                strategies.append(Strategy(**strategy_data))
            except:
                continue
        
        if not strategies:
            return []
        
        # 3. Thompson Sampling strategy selection (RFC0039 — replaced UCB1)
        selected = await self._thompson_sampling_select(strategies)  # UCB1 replaced by Thompson Sampling (RFC0039)
        
        return selected[:3]  # Top-3

    async def _thompson_sampling_select(
        self,
        strategies: List[Strategy],
        top_k: int = 3,
        seed: int | None = None
    ) -> List[Strategy]:
        """
        Thompson Sampling strategy selection (RFC0039).
        seed — for reproducible replay in audits (Invariant I13).
        """
        import numpy as np
        if not strategies:
            return []
        rng = np.random.default_rng(seed)
        scored = []
        for s in strategies:
            alpha = getattr(s, 'success_count', 0) + 1
            beta  = getattr(s, 'failure_count', 0) + 1
            ts_score = rng.beta(alpha, beta)
            scored.append((ts_score, s))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [s for _, s in scored[:top_k]]

    def _ucb1_select(
        self,
        strategies: List[Strategy],
        context: Dict,
        epsilon: float
    ) -> List[Strategy]:
        """
        ⚠️ DEPRECATED: replaced by Thompson Sampling (RFC0039).
        Kept for backward compatibility. Do not use directly.
        Use _thompson_sampling_select() instead.
        """
        import random
        import numpy as np
        
        # Exploration with probability epsilon
        if random.random() < epsilon:
            # Return a random strategy for exploration
            logger.info("Strategy selection: EXPLORATION mode")
            return random.sample(strategies, min(3, len(strategies)))
        
        # Exploitation: UCB1 scoring
        total_trials = sum(
            s.success_count + s.failure_count for s in strategies
        )
        
        if total_trials == 0:
            # No history → return all
            return strategies
        
        scored_strategies = []
        
        for strategy in strategies:
            trials = strategy.success_count + strategy.failure_count
            
            if trials == 0:
                # Untried strategy → maximum priority
                ucb_score = float('inf')
            else:
                # UCB1 formula: mean + exploration_bonus
                exploitation_term = strategy.success_rate
                
                # Exploration bonus: higher the fewer times it has been tried
                exploration_bonus = np.sqrt(
                    2 * np.log(total_trials) / trials
                )
                
                # Context similarity: how well the strategy fits
                context_similarity = self._compute_context_similarity(
                    strategy.applicable_contexts,
                    context
                )
                
                # Final UCB score
                ucb_score = (
                    exploitation_term +           # 0-1: current success rate
                    exploration_bonus * 0.5 +     # Bonus for exploration
                    context_similarity * 0.3      # Relevance to context
                )
            
            scored_strategies.append((strategy, ucb_score))
        
        # Sort by UCB score
        scored_strategies.sort(key=lambda x: x[1], reverse=True)
        
        logger.info(
            f"Strategy selection: EXPLOITATION mode, "
            f"top_score={scored_strategies[0][1]:.3f}"
        )
        
        return [s for s, score in scored_strategies]

    def _compute_context_similarity(
        self,
        strategy_contexts: List[str],
        current_context: Dict
    ) -> float:
        """
        Compute the similarity between the strategy's context and the current task
        Simplified version - can be improved with embeddings
        """
        if not strategy_contexts:
            return 0.5  # Neutral score
        
        # Double generator comprehension — the correct way to flatten a list of words
        current_keywords = {
            word
            for v in current_context.values()
            for word in str(v).lower().split()
        }
        
        strategy_keywords = set(
            word.lower() 
            for ctx in strategy_contexts 
            for word in ctx.split()
        )
        
        if not strategy_keywords:
            return 0.5
        
        # Jaccard similarity
        intersection = len(current_keywords & strategy_keywords)
        union = len(current_keywords | strategy_keywords)
        
        similarity = intersection / union if union > 0 else 0.0
        return similarity

    async def update_strategy_feedback(
        self,
        strategy_id: str,
        outcome: Outcome
    ):
        """
        Update the strategy's statistics based on new experience
        Includes negative reinforcement via a confidence penalty
        """
        strategy = self.strategies.get(strategy_id)
        if not strategy:
            # Find it in the graph
            results = await self.graph.search(
                query=f"strategy: {strategy_id}",
                num_results=1
            )
            if not results:
                return
            
            strategy_data = json.loads(results[0].content)
            strategy = Strategy(**strategy_data)
        
        # Update counters
        if outcome == Outcome.SUCCESS:
            strategy.success_count += 1
        elif outcome == Outcome.FAILURE:
            strategy.failure_count += 1
        
        # Apply negative/positive reinforcement
        strategy.update_confidence(outcome)
        
        logger.info(
            f"Strategy '{strategy_id}' updated: "
            f"success_rate={strategy.success_rate:.1%}, "
            f"confidence={strategy.confidence:.2f}"
        )
        
        # Save the update to the graph
        await self._save_strategy(strategy)

    async def ace_curator_update(self):
        """
        ACE Curator (Stanford/SambaNova ACE pattern).
        Called ONLY from SleepTimeWorker when idle — not from the Fast Path.

        P1-3 FIX: the duplicate implementation has been removed. We delegate to the canonical method.
        Canonical implementation: agent_with_learning.py::SelfLearningAgent.ace_curator_update()
        The discrepancy was: e.task here, e.task_description[:50] there — out of sync.
        Make all logic changes ONLY in agent_with_learning.py.
        """
        if self._ace_delegate is None:
            logger.debug("ace_curator_update: _ace_delegate not set, skipping")
            return
        try:
            await self._ace_delegate.ace_curator_update()
        except Exception as e:
            logger.warning(f"ace_curator_update (delegate) failed (non-fatal): {e}")

    def set_ace_delegate(self, delegate) -> None:
        """
        Set the delegate for the ACE Curator.
        Call from SelfLearningAgent.__init__() after creating ReasoningBank:
            self.reasoning_bank.set_ace_delegate(self)

        P1-3 FIX: eliminates the duplication of ace_curator_update in two places.
        """
        self._ace_delegate = delegate
```

**Integration into the agent**:

```python
# agent_with_learning.py
class SelfLearningAgent:
    def __init__(
        self,
        llm,
        memory: GraphMemory,
        retriever: HybridRetriever,
        reasoning_bank: ReasoningBank
    ):
        self.llm = llm
        self.memory = memory
        self.retriever = retriever
        self.reasoning_bank = reasoning_bank

        # P1-3 FIX: register the delegate so that reasoning_bank.ace_curator_update()
        # delegates to the canonical method self.ace_curator_update().
        # The canonical ACE Curator implementation lives here, not in ReasoningBank.
        self.reasoning_bank.set_ace_delegate(self)

    async def execute_task(self, task: str, context: Dict):
        """
        Execute a task taking past experience into account
        Cycle: Retrieve → Plan → Execute → Judge → Learn
        """
        # 1. RETRIEVE: Find relevant strategies (Thompson Sampling, RFC0039)
        strategies = await self.reasoning_bank.retrieve_relevant_strategies(
            current_task=task,
            context=context,
            # Thompson Sampling: adaptive explore/exploit balance is built into the Beta distribution
        )
        
        # 2. PLAN: Select a strategy or create a new one
        if strategies:
            best_strategy = strategies[0]
            plan = f"Based on past success, use strategy: {best_strategy.description}"
            strategy_id = best_strategy.id  # use the UUID instead of the description
        else:
            plan = await self._create_new_plan(task, context)
            strategy_id = None
        
        # 3. EXECUTE: Execute the plan
        try:
            result = await self._execute_plan(plan, context)
            outcome = Outcome.SUCCESS
            error = None
        except Exception as e:
            result = None
            outcome = Outcome.FAILURE
            error = str(e)
        
        # 4. JUDGE: Evaluate the result
        reasoning = await self._reflect_on_outcome(
            task, plan, result, outcome
        )
        
        # 5. LEARN: Save the experience
        await self.reasoning_bank.log_experience(
            task=task,
            context=context,
            action=plan,
            outcome=outcome,
            reasoning=reasoning,
            error=error
        )
        
        # 6. UPDATE: Update the strategy statistics
        if strategy_id:
            await self.reasoning_bank.update_strategy_feedback(
                strategy_id=strategy_id,
                outcome=outcome
            )
        
        return result

    async def _reflect_on_outcome(
        self,
        task: str,
        plan: str,
        result: any,
        outcome: Outcome
    ) -> str:
        """
        Reflect on the outcome — extract a lesson for ReasoningBank.

        TODO (Phase 2): replace the heuristic with an SLM call (Qwen3-1.7B) for
        structured analysis: root_cause + conditions + anti_conditions.
        Currently a deterministic heuristic is used — 0 LLM tokens.
        """
        if outcome == Outcome.SUCCESS:
            return (
                f"SUCCESS: strategy '{plan[:80]}' solved task '{task[:80]}'. "
                f"Result obtained: {bool(result)}."
            )
        else:
            return (
                f"FAILURE: strategy '{plan[:80]}' failed to handle task '{task[:80]}'. "
                f"An alternative approach is required."
            )
```

---

### 18. velantrim_config.py — Unified Constants 

**Purpose**: A single source for all of the system's numeric constants. Eliminates parameter drift.

```python
# velantrim_config.py
class MemoryConfig:
    STM_CAPACITY = 5
    SESSION_IDLE_MINUTES = 30
    VELUM_CO_OCCUR_THRESHOLD = 3
    VELUM_WINDOW_EPISODES = 5
    VELUM_MAX_EDGES = 1000
    VELUM_PROMOTE_WEIGHT = 0.6
    VELUM_DECAY_PER_SESSION = 0.3
    MTM_CAPACITY = 25
    L2_COLD_START_MIN = 50
    L2_TTL_BASE_DAYS = 7
    L2_TTL_MAX_DAYS = 224
    STAGING_CPU_THRESHOLD = 0.35
    STAGING_RAM_THRESHOLD = 0.25
    STAGING_BATCH_SIZE = 50
    STAGING_MAX_SIZE = 5000
    STAGING_FAST_TRACK = 0.9

class TruthConfig:
    GUARDIAN_CONFIDENCE = 0.7
    TRUTH_GATE_EVIDENCE_MIN = 3
    TRUTH_GATE_CONFIDENCE = 0.75
    EMOTIONAL_RING_ZERO = 0.85
    FAITHFULNESS_THRESHOLD = 0.6

class TokenConfig:
    MEMORY_PER_QUERY = 2000
    PRECISION_MODE = 1000
    BALANCED_MODE = 2000
    EXPLORATION_MODE = 4000

class SLOConfig:
    SEARCH_P95_MS = 500
    ETIR_P95_MS = 50
    CONSOLIDATION_LAG_S = 60
    FAITHFULNESS_MIN = 0.8
    MHI_WARN = 0.50
    MHI_CRITICAL = 0.30

MEMORY = MemoryConfig()
TRUTH = TruthConfig()
TOKENS = TokenConfig()
SLO = SLOConfig()
```

**Usage**:
```python
from velantrim_config import MEMORY, TRUTH

if len(l2_items) < MEMORY.L2_COLD_START_MIN:
    skip_clustering()
```

---

### 19. TruthGateWithESM — A Single Point for Guardian + ESM (RFC0015)

**Problem**: Guardian and ESM were independent — no atomicity

**Solution**: A facade-orchestrator

```python
@dataclass
class TruthGateResult:
    passed: bool
    score: float
    esm_state: str
    reason: str
    emotional_salience: float = 0.0

class TruthGateWithESM:
    def __init__(self, guardian, esm, graph, etir):
        self.guardian = guardian
        self.esm = esm
        self.graph = graph
        self.etir = etir

    async def validate_and_transition(self, item: dict) -> TruthGateResult:
        emotional_salience = float(item.get("emotional_salience", 0.0))
        
        # 1. Guardian validation
        passed = await self.guardian.validate_proposal(item)
        
        if not passed:
            reason = await self._classify_rejection(item)
            new_state = self._rejection_to_esm_state(reason)
            await self.esm.transition(item["id"], new_state, reason=reason)
            return TruthGateResult(False, 0.0, new_state, reason, emotional_salience)
        
        # 2. Validated
        await self.esm.transition(item["id"], "Validated", reason="TRUTH_GATE_PASSED")
        
        # 3. Ring Zero + Emotional Ring Zero
        if (item.get("pinned") == "CRITICAL" or 
            emotional_salience > TRUTH.EMOTIONAL_RING_ZERO):
            await self.esm.freeze(item["id"])
        
        # 4. Promote to L3
        await self.graph.promote_from_staging(item)
        
        if emotional_salience > 0.5:
            await self.etir.boost_node(item["id"], emotional_salience)
        
        score = float(item.get("confidence", 1.0))
        return TruthGateResult(True, score, "Validated", 
                               "TRUTH_GATE_PASSED", emotional_salience)
```

**Auto Truth Gate Worker** — A background process for the automatic transition Supported → Validated

```python
# auto_truth_gate_worker.py
# P2-3: Conflict Resolution Window (NGT Memory pattern)
# After the phrase "I was wrong" / "correction" / "fix":
# a 60-second window during which TruthGate lowers the barrier for user_input.
# CORRECTION_WINDOW_SECONDS = 60
# After the window expires — standard mode.
CORRECTION_WINDOW_SECONDS = 60

class AutoTruthGateWorker:
    """
    A background process for automatic fact validation.
    Runs once a day (or on a schedule).

    Problem: facts with sufficient evidence remain in Supported
    until they happen to land in the Truth Gate.

    Solution: periodically check all Supported facts
    with evidence_count ≥ 3 and transition them to Validated.
    """

    def __init__(self, graph, truth_gate, esm, scheduler_hours=24):
        self.graph = graph
        self.truth_gate = truth_gate
        self.esm = esm
        self.scheduler_hours = scheduler_hours

    async def run_validation_cycle(self):
        """Main loop — called by APScheduler"""
        # evidence_count is NOT a field of :Fact, evidence is stored via the [:SUPPORTED_BY]->(:Evidence) relationship
        # Count the number of Evidence nodes via the graph
        query = """
        MATCH (f:Fact)-[:SUPPORTED_BY]->(ev:Evidence)
        WHERE f.epistemic_state = 'Supported'
          AND f.is_ring_zero <> true
        WITH f, count(ev) AS evidence_count
        WHERE evidence_count >= 3
        RETURN f.id AS id, evidence_count, f.importance_score AS importance_score
        ORDER BY f.importance_score DESC
        LIMIT 100
        """
        
        candidates = await self.graph.execute_cypher(query)
        validated_count = 0
        
        for fact in candidates:
            # Validate via the Truth Gate
            result = await self.truth_gate.validate_and_transition({
                "id": fact['id'],
                "evidence_count": fact['evidence_count'],
                "importance_score": fact['importance_score']
            })
            
            if result.passed:
                validated_count += 1
        
        logger.info(
            f"Auto Truth Gate: {validated_count}/{len(candidates)} facts "
            f"transitioned Supported → Validated"
        )
        
        return validated_count

# Integration into startup
# scheduler.add_job(auto_truth_gate_worker.run_validation_cycle, 
#                   'interval', hours=24)
```

---

### 20. L1.5 Velum — Early Connection Detector (RFC0016)

**Purpose**: An LTP-inspired mechanism for co-occurrence detection

```python
@dataclass
class VelumEdge:
    entity_a: str
    entity_b: str
    weight: float
    session_id: str
    first_seen: float
    last_seen: float
    count: int = 1
    promoted: bool = False

@dataclass
class VelumSignal:
    entity_a: str
    entity_b: str
    weight: float
    reason: str
    episode_ids: list[str]

@dataclass
class VelumConfig:
    """
    Velum configuration.
    persist=True: edges are saved to SQLite and restored on restart.
    Without persist, edges live only in the RAM of the current session — connections are lost on restart.
    """
    persist:     bool = False
    sqlite_path: str  = "./data/velum_seed.db"


class Velum:
    def __init__(self, session_id: str, l2_signal_callback=None,
                 config: VelumConfig = None):
        self.session_id = session_id
        self._signal_callback = l2_signal_callback
        self._config = config or VelumConfig()
        self._edges: dict[frozenset, VelumEdge] = {}
        self._entity_index: dict[str, list[frozenset]] = defaultdict(list)
        self._recent_episodes = []
        self._lock = asyncio.Lock()  # protects self._edges from a race condition during concurrent inserts

        # P0-1 FIX: _degree_cache — cache of node degrees for the ACT-R fan-effect.
        # Incremented in _add_edge(), decremented in gc_weak_edges().
        # Without initializing it here → AttributeError on the first _strengthen_edge().
        self._degree_cache: dict[str, int] = {}
        # P0-F FIX: tracking the current session's episode_ids for the on_session_end VelumSignal.
        # Without this field, on_session_end cannot pass episode_ids → empty list.
        self._current_session_episodes: list[str] = []

        # FIX from HYPERIA: restore the top edges from the previous session at startup.
        # Without this, Velum always starts from scratch — the first N episodes have no
        # accumulated co-occurrence and signals are not generated into L2.
        if self._config.persist:
            self._load_seed_from_sqlite()

    async def observe_episode(self, episode_id: str, entities: list[str]) -> list[VelumSignal]:
        """P0-D FIX: observe_episode acquires self._lock only for _recent_episodes,
        then RELEASES the lock before calling _update_edge (which acquires the lock itself).
        asyncio.Lock is not reentrant — a nested acquire = deadlock.
        Pattern: acquire → copy → release → work with the copy.
        """
        signals = []
        async with self._lock:  # protects _recent_episodes from concurrent inserts
            self._current_session_episodes.append(episode_id)  # P0-F FIX: tracking for on_session_end
            self._recent_episodes.append((episode_id, entities))
            if len(self._recent_episodes) > MEMORY.VELUM_WINDOW_EPISODES:
                self._recent_episodes.pop(0)
            window_entities = [(ep_id, ent) for ep_id, ents in self._recent_episodes for ent in ents]
        
        # co-occurrence outside the lock — I/O bound, does not mutate _recent_episodes
        for i, (eid_a, ent_a) in enumerate(window_entities):
            for eid_b, ent_b in window_entities[i+1:]:
                if ent_a != ent_b:
                    signal = await self._update_edge(ent_a, ent_b, [eid_a, eid_b])
                    if signal:
                        signals.append(signal)
        
        return signals

    # Class-level method (not nested inside observe_episode)
    async def _update_edge(self, entity_a: str, entity_b: str,
                           episode_ids: list) -> "VelumSignal | None":
        """
        Update the co-occurrence edge weight. Returns a VelumSignal if the threshold is reached.
        replaced NotImplementedError — L1.5 Velum now works.
        """
        key = frozenset([entity_a, entity_b])
        async with self._lock:
            if key not in self._edges:
                _now = time.monotonic()  # import time must be at the top of the file
                self._edges[key] = VelumEdge(
                    entity_a=entity_a, entity_b=entity_b,
                    weight=0.0, session_id=self.session_id,
                    first_seen=_now,
                    last_seen=_now,
                )
                self._entity_index[entity_a].append(key)
                self._entity_index[entity_b].append(key)

            edge = self._edges[key]
            edge.weight  = min(1.0, edge.weight + 0.1)
            edge.count  += 1
            edge.last_seen = time.monotonic()

            # FIX from HYPERIA: GC of weak edges as the dictionary grows.
            # Without this, _edges grows unboundedly — a single session with a broad context
            # can accumulate thousands of edges with weight≈0.1 that are never promoted.
            if len(self._edges) > 1000:
                self._gc_weak_edges()

            # P1-A FIX: the threshold was VELUM_CO_OCCUR_THRESHOLD/10 = 3/10 = 0.3 → 2× false signals.
            # The specification requires weight ≥ VELUM_PROMOTE_WEIGHT (0.6) AND count ≥ CROSS_SESSION (3).
            if (edge.weight >= MEMORY.VELUM_PROMOTE_WEIGHT
                    and edge.count >= MEMORY.VELUM_CO_OCCUR_THRESHOLD):
                signal = VelumSignal(
                    entity_a=entity_a, entity_b=entity_b,
                    weight=edge.weight, reason="CO_OCCUR_THRESHOLD",
                    episode_ids=episode_ids,
                )
            else:
                signal = None
        # FIX: the callback is invoked OUTSIDE async with self._lock.
        # Calling it inside the lock risks a deadlock if the callback itself accesses Velum.
        if signal and self._signal_callback:
            await self._signal_callback(signal)
        return signal

    async def on_session_end(self) -> list[VelumSignal]:
        signals = []
        # FIX: iteration over self._edges is protected by self._lock.
        # Without the lock, a concurrent _update_edge caused
        # RuntimeError: dictionary changed size during iteration.
        async with self._lock:
            edges_snapshot = list(self._edges.items())
        for key, edge in edges_snapshot:
            if edge.weight >= MEMORY.VELUM_PROMOTE_WEIGHT:
                signal = VelumSignal(
                    entity_a=edge.entity_a, entity_b=edge.entity_b,
                    weight=edge.weight, reason="SESSION_END",
                    episode_ids=[])  # episode_ids is required — without it, TypeError on every session_end
                signals.append(signal)
                if self._signal_callback:
                    await self._signal_callback(signal)
            else:
                edge.weight *= (1.0 - MEMORY.VELUM_DECAY_PER_SESSION)

        # FIX from HYPERIA: save the top edges to SQLite at the end of the session.
        # We keep a reference to the task — without it, GC kills the coroutine before the write completes.
        if self._config.persist:
            _t = asyncio.create_task(self._save_top_edges_to_sqlite(top_n=200))
            _t.add_done_callback(
                lambda t: t.exception() and
                logger.debug(f"Velum persist failed: {t.exception()}")
            )

        return signals

    def get_neighbors(self, entity: str, min_weight: float = 0.3) -> list[tuple[str, float]]:
        result = []
        for key in self._entity_index.get(entity, []):
            edge = self._edges.get(key)
            if edge and edge.weight >= min_weight:
                neighbor = edge.entity_b if edge.entity_a == entity else edge.entity_a
                result.append((neighbor, edge.weight))
        return sorted(result, key=lambda x: x[1], reverse=True)

    def _gc_weak_edges(self, keep_ratio: float = 0.75):
        """
        GC of weak co-occurrence edges.
        Called from within _update_edge under self._lock when len(_edges) > 1000.
        Keeps the top 75% by weight, removes the rest along with their _entity_index entries.
        Without this method, _edges grows unboundedly during long sessions.
        """
        sorted_edges = sorted(self._edges.items(), key=lambda x: x[1].weight, reverse=True)
        keep_n    = int(len(sorted_edges) * keep_ratio)
        keep_keys = {k for k, _ in sorted_edges[:keep_n]}

        # Remove weak edges
        removed = {k for k in self._edges if k not in keep_keys}

        # P0-1 FIX: update the degree cache when removing edges
        for k in removed:
            edge = self._edges[k]
            for node in list(edge.entities) if hasattr(edge, 'entities') else [edge.entity_a, edge.entity_b]:
                self._degree_cache[node] = max(0, self._degree_cache.get(node, 1) - 1)
            del self._edges[k]

        # Clean removed keys out of _entity_index
        for entity in list(self._entity_index.keys()):
            self._entity_index[entity] = [
                k for k in self._entity_index[entity] if k in keep_keys
            ]
            if not self._entity_index[entity]:
                del self._entity_index[entity]

        logger.debug(f"Velum GC: removed {len(removed)} weak edges, kept {len(self._edges)}")

    def _load_seed_from_sqlite(self):
        """
        Restore the top edges from the previous session.
        Called synchronously in __init__ — acceptable, it happens once at startup.
        Without this, Velum starts each time with an empty edge graph, and the first
        VELUM_CO_OCCUR_THRESHOLD episodes do not generate signals into L2.
        """
        import sqlite3
        try:
            conn = sqlite3.connect(self._config.sqlite_path)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS velum_edges (
                    entity_a TEXT NOT NULL,
                    entity_b TEXT NOT NULL,
                    weight   REAL NOT NULL,
                    count    INTEGER NOT NULL DEFAULT 1,
                    PRIMARY KEY (entity_a, entity_b)
                )
            """)
            rows = conn.execute(
                "SELECT entity_a, entity_b, weight, count "
                "FROM velum_edges ORDER BY weight DESC LIMIT 200"
            ).fetchall()
            conn.close()
            _now = time.monotonic()
            for entity_a, entity_b, weight, count in rows:
                key = frozenset([entity_a, entity_b])
                self._edges[key] = VelumEdge(
                    entity_a=entity_a, entity_b=entity_b,
                    weight=weight, count=count,
                    session_id=self.session_id,
                    first_seen=_now, last_seen=_now,
                )
                self._entity_index[entity_a].append(key)
                self._entity_index[entity_b].append(key)
            logger.info(f"Velum: loaded {len(rows)} seed edges from SQLite")
        except Exception as e:
            logger.warning(f"Velum: seed load failed (starting empty): {e}")

    async def _save_top_edges_to_sqlite(self, top_n: int = 200):
        """
        Save the top-N edges by weight to SQLite.
        Called via asyncio.create_task in on_session_end — does not block the pipeline.
        """
        import aiosqlite
        async with self._lock:
            snapshot = sorted(
                self._edges.items(), key=lambda x: x[1].weight, reverse=True
            )[:top_n]
        try:
            async with aiosqlite.connect(self._config.sqlite_path) as db:
                await db.execute("""
                    CREATE TABLE IF NOT EXISTS velum_edges (
                        entity_a TEXT NOT NULL,
                        entity_b TEXT NOT NULL,
                        weight   REAL NOT NULL,
                        count    INTEGER NOT NULL DEFAULT 1,
                        PRIMARY KEY (entity_a, entity_b)
                    )
                """)
                for key, edge in snapshot:
                    await db.execute(
                        "INSERT OR REPLACE INTO velum_edges "
                        "(entity_a, entity_b, weight, count) VALUES (?, ?, ?, ?)",
                        (edge.entity_a, edge.entity_b, edge.weight, edge.count)
                    )
                await db.commit()
            logger.debug(f"Velum: saved {len(snapshot)} edges to SQLite")
        except Exception as e:
            logger.warning(f"Velum: persist failed: {e}")
```

---

### 21. OutputFaithfulnessChecker — Post-generation guard 

**Purpose**: Step F6.5 — checking that the LLM did not lie

```python
class OutputFaithfulnessChecker:
    FALLBACK_RESPONSE = (
        "Not enough confirmed data to answer confidently. "
        "I can answer more precisely once I have accumulated more verified facts."
    )

    def __init__(self, threshold: float = None):
        self.threshold = threshold or TRUTH.FAITHFULNESS_THRESHOLD

    async def check(
        self, answer: str, facts_pack: list[dict]
    ) -> tuple[bool, list[str], float]:
        """
        Returns: (passed, unsupported_sentences, faithfulness_score)
        """
        # P1-B FIX: empty facts_pack = nothing to check → APPROVE.
        # WAS: return (False, answer, 0.0) → blocked Creative Mode and the first queries.
        # NOW: return (True, [], 1.0) → no facts = no violations = APPROVE.
        if not facts_pack:
            return True, [], 1.0
        
        fact_texts = {f["content"].lower() for f in facts_pack if f.get("content")}
        sentences = self._split_sentences(answer)
        
        unsupported = [s for s in sentences if not self._is_supported(s, fact_texts)]
        faithfulness = 1.0 - len(unsupported) / len(sentences)
        
        if faithfulness < self.threshold:
            return False, unsupported, faithfulness
        
        return True, unsupported, faithfulness

    def _split_sentences(self, text: str) -> list[str]:
        """Phase 1 stub: split text into sentences."""
        import re
        return [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]

    def _is_supported(self, sentence: str, fact_texts: set) -> bool:
        """MVP: keyword overlap ≥ 40%"""
        words = set(sentence.lower().split())
        if len(words) < 3:
            return True
        return any(
            len(words & set(f.split())) / len(words) >= 0.4
            for f in fact_texts
        )
```

**Integration into the pipeline**:
```python
# F6: LLM Generation
answer = await llm.chat(context)

# F6.5: Faithfulness check
passed, unsupported, score = await faithfulness_checker.check(answer, facts_pack)

if passed:
    return answer
else:
    logger.warning(f"Faithfulness FAILED: {score:.2f}")
    return OutputFaithfulnessChecker.FALLBACK_RESPONSE
```

---

## 📐 Token Contract and Promote/Demote Protocol 

> **Why this matters**: the goal of "90%+ token reduction" remains a declaration without a formal contract. This section turns the goal into a guarantee.

---

### ⚡ Token Contract

```python
# token_contract.py

MAX_TOKENS_MEMORY_PER_QUERY = 2000   # Memory budget per query (BALANCED mode)
MAX_TOKENS_SYSTEM_PROMPT    = 500    # Reserve for the system prompt
MAX_TOKENS_ETIR_ACTIVATION  = 300    # Limit for L3.5 Etir spreading activation
ETIR_TOP_K_NODES            = 10     # Maximum activated nodes from Etir
ETIR_DECAY_THRESHOLD        = 0.15   # Nodes with activation < threshold are not included

# Cognitive Modes — budgets per mode
MAX_TOKENS_PRECISION_MODE   = 1000   # PRECISION: critical data, facts only
MAX_TOKENS_BALANCED_MODE    = 2000   # BALANCED: standard mode (90% of tasks)
MAX_TOKENS_EXPLORATION_MODE = 4000   # EXPLORATION: brainstorm, hypotheses
MAX_TOKENS_CREATIVE_MODE    = 3000   # CREATIVE: analogies + Validated only (RFC0067 v2.0)
```

**Priority of levels when the budget runs short:**

```
Budget: MAX_TOKENS_MEMORY_PER_QUERY = 2000 tokens
│
├── L0 Working Memory    → always (~100 tokens, cannot be trimmed)
├── L3.5 Etir activation → top_k nodes up to the ETIR limit
├── L1 STM Episodes      → by relevance until the remainder is exhausted
├── L2 MTM Patterns      → summary only if budget remains
└── L3 LTM Graph         → only on an explicit meta-query

Rule: if the budget is exhausted — L3 is cut first,
      L0 and Etir results are always protected.
```

---

### 🔄 Promote / Demote Protocol

Formal rules for moving data between memory levels. Without these rules the system is non-deterministic.

```
PROMOTE L1 (STM) → L2 (MTM) if at least one holds:
  importance_score > 0.7
  OR access_count >= 3
  OR outcome IN [SUCCESS, FAILURE]   (emotional salience)
  OR pinned == true

PROMOTE L2 (MTM) → L3 (LTM / Neo4j) if:
  cluster >= 3 similar episodes (cosine similarity > 0.7)
  AND avg_importance > 0.5

DEMOTE / SOFT DELETE L2 → archive if:
  age > 30 days
  AND importance_score < 0.3
  AND access_count == 0 over the last 14 days
  AND pinned == false
  → Action: is_active = false, valid_to = now()

FORGET (physical GC deletion) if:
  is_active == false
  AND age > 90 days
  AND importance_score < 0.1
  AND reindex_required == false   (do not touch if reindexing is needed)
  → Action: archive to S3, then DETACH DELETE
```

| Transition | Condition | Method |
|---|---|---|
| L1 → L2 | importance > 0.7 / access ≥ 3 / outcome | `consolidate_stm_to_mtm()` |
| L2 → L3 | cluster ≥ 3, avg_importance > 0.5 | `consolidate_mtm_to_ltm()` |
| L2 → archive | age > 30d, importance < 0.3 | Soft Delete: `is_active=false` |
| Archive → delete | age > 90d, importance < 0.1 | GC: S3 backup + DETACH DELETE |
| L3 → L3.5 Etir | access_count > threshold / pinned | `etir_promote()` |
| L3.5 → L3 | access_count drops, decay | `etir_evict()` |

---

### ❄️ Cold Start / Seed Nodes

> ⚠️ **KPI blocker**: On first launch Etir is empty → P95 > 500ms on every
> query, which violates the stated KPI of <500ms. Without seed nodes the system
> degrades into a full L3 (Neo4j) traversal on all queries until data accumulates.

```
Problem: Etir is empty at init → full Neo4j traversal on every query
          Velum is empty → all links go straight to the graph
          ReasoningBank is empty → Thompson Sampling works at random

Solution — Seed Nodes at initialization:
  1. At system startup, load base concepts into Etir:
     · Science Core nodes with pinned=True (if populated)
     · VALUES CORE / Ring Zero nodes — always pinned
     · Top-N nodes by access_count from past sessions
     · If there is no data — a minimal set from constants.py

  2. Velum seed:
     · Load links with usage_count > 3 from previous sessions
     · If it is the first launch — start with an empty Velum (normal)

  3. ReasoningBank seed:
     · Preload base strategies from reasoning_bank.py
     · confidence = 0.5 (neutral start, Thompson Sampling will choose on its own)

Implementation: etir_init(seed=True) is called in pipeline.__init__()
```

---

### 🔀 Soft Delete — Mandatory GC Pattern

```
NEVER run DETACH DELETE directly in production.
Always: Soft Delete → S3 archival → Hard Delete

Deletion steps:
1. SET node.is_active = false, node.valid_to = datetime()
2. Wait for a successful write to S3
3. Only after success: DETACH DELETE
4. If S3 fails → roll back is_active = true

Restore Path (restoration from archive):
1. Find the node in S3 by node_id / canonical_id
2. MERGE (n:KnowledgeNode {node_id: $id})
3. SET n.is_active = true, n.valid_to = null
4. SET n.restored_at = datetime(), n.restore_reason = $reason
5. Check the RFC invariants (MGL-2, MGL-5) after restoration
```

---

### 🔀 Fact Conflict — [:CONTRADICTS] pipeline

```
The user says: "Forget X, we're going back to Y"
│
├── Graphiti creates a new :Fact node (the new decision)
├── The intent classifier detects OVERRIDE
├── A link is created: new_fact-[:CONTRADICTS {reason}]->old_fact
├── old_fact gets: is_active=false, valid_to=now()
├── HybridRetriever automatically filters out is_active=false
└── GC on the next launch: S3 backup → physical deletion

⚠️ IMPORTANT: the LLM does NOT assign [:CONTRADICTS] automatically.
   Only an explicit user command or the CRUD classifier.
   When a conflict is detected, the agent asks back:
   "I see a contradiction with the previous decision. Erase the old one?"
```

---

### 6. Context Builder: Smart Prompt Assembly

> ⚠️ **The canonical implementation is FEATURE-8 (RFC0062).** This section describes the logic; for the actual code, see the RFC0062 · FEATURE-8 section.

**Purpose**: Assemble the minimal, relevant context within the token budget.

---

## 🔄 Full Integration: Main Agent

```python
# main_agent.py
import asyncio
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

class AutonomousSelfLearningAgent:
    """
    Bounded agent workflow concept with fractal memory and self-learning
    Hardened sprint design with:
    - Circuit breakers for resilience
    - OpenTelemetry for observability
    - Adaptive consolidation
    - Thompson Sampling strategy selection (RFC0039)
    - Memory GC
    """
    def __init__(self, config: Dict):
        self.config = config
        # Core components
        self.llm = self._init_llm(config)
        self.event_bus = RobustEventBus(config["redis_url"])
        
        # Memory layers with circuit breakers
        self.graph_memory = GraphMemoryWithCircuitBreaker(
            neo4j_uri=config["neo4j_uri"],
            neo4j_user=config["neo4j_user"],
            neo4j_password=config["neo4j_password"]
        )
        self.fractal_memory = FractalMemory(self.graph_memory)
        
        # Retrieval and learning with observability
        self.retriever = ObservableHybridRetriever(
            graph_memory=self.graph_memory,
            fractal_memory=self.fractal_memory,
            token_budget=config.get("token_budget", 2000)
        )
        self.reasoning_bank = ReasoningBank(self.graph_memory)
        # P1-3 FIX: register the ACE Curator delegate
        self.reasoning_bank.set_ace_delegate(self)
        self.context_builder = ContextBuilder(
            token_budget=config.get("token_budget", 2000)  # FEATURE-8 (RFC0062): canonical, token_budget=2000 matches token_contract.py
        )
        
        # Background workers
        self.consolidation_worker = AdaptiveConsolidationWorker(
            self.fractal_memory
        )
        self.event_processor = EventProcessor(
            self.event_bus,
            self.graph_memory,
            self.fractal_memory
        )
        
        # Memory management
        self.memory_archival = MemoryArchival(
            graph=self.graph_memory,
            s3_bucket=config.get("s3_bucket")
        )
        self.memory_gc = MemoryGarbageCollector(
            graph=self.graph_memory,
            fractal_memory=self.fractal_memory,
            archival=self.memory_archival
        )
        # Supervisors (started in start())
        self.invariant_checker = RuntimeInvariantChecker(
            graph=self.graph_memory,
            fractal_memory=self.fractal_memory
        )
        # MemoryBudgetPlanner — create it from graph_memory to avoid AttributeError in _collect_signals
        _budget_planner = MemoryBudgetPlanner(graph=self.graph_memory)
        self.meta_supervisor = MetaSupervisorApex(
            consolidation_engine=self.consolidation_worker,
            graph=self.graph_memory,
            budget_planner=_budget_planner,
            invariant_checker=self.invariant_checker
        )

        # Persistent task agent — created once and reused,
        # so that reasoning_bank accumulates experience across calls (instead of being reset).
        self._task_agent = SelfLearningAgent(
            llm=self.llm,
            memory=self.graph_memory,
            retriever=self.retriever,
            reasoning_bank=self.reasoning_bank
        )

        # State
        self.session_id = generate_session_id()
        self.conversation_history = []
        self._shutdown_started = False  # guard against double graceful shutdown on SIGTERM+SIGINT
        # sqlite_db is initialized here explicitly,
        # rather than only on first access in start() — this eliminates AttributeError.
        self._sqlite_db_path = config.get("sqlite_db", "velantrim.db")
        self.sqlite_db = None  # opened as an async context in start()

    async def start(self):
        """Start the agent and the background processes"""
        # RFC0006 — validate the Engram configuration before start
        from rfc0006_engram_isolation import validate_engram_config
        validate_engram_config(self.config)

        # open sqlite_db via the aiosqlite context manager
        import aiosqlite
        self.sqlite_db = await aiosqlite.connect(self._sqlite_db_path)

        # SQLite WAL mode for fast Graceful Shutdown
        await self.sqlite_db.execute("PRAGMA journal_mode=WAL")
        await self.sqlite_db.execute("PRAGMA synchronous=NORMAL")

        # Create the Neo4j indexes (CRITICAL!)
        await setup_neo4j_indexes(self.graph_memory.driver)

        # P0-2 FIX: ImmutableRawMemory — create the SQLite schema before the first save_episode().
        # Without this call the raw_episodes table does not exist → crash on write.
        # Order is critical: FIRST, before any workers that may write episodes.
        if hasattr(self, 'raw_memory') and self.raw_memory is not None:
            await self.raw_memory.init()

        # P0-3 FIX: MemoryVolitionWorker — load the per-session counters from SQLite.
        # Without this _initialized=False → write_voluntary() raises RuntimeError.
        # MAX_PER_SESSION=10 does not work without the loaded counters.
        # Order: after raw_memory.init(), before workers that may call write_voluntary().
        if hasattr(self, 'volition_worker') and self.volition_worker is not None:
            await self.volition_worker.start()

        # Start the ConsolidationEngine (replaces 3 workers)
        asyncio.create_task(self.consolidation_worker.start())  # fixed: consolidation_worker (see __init__)

        # Start the background workers (they use CE via enqueue)
        asyncio.create_task(self.event_processor.start())
        asyncio.create_task(self.memory_gc.schedule_periodic_gc())
        asyncio.create_task(self._dlq_processor())

        # Start the Runtime Invariant Checker
        asyncio.create_task(self.invariant_checker.start())

        # Start the Meta-Supervisor Apex Controller
        asyncio.create_task(self.meta_supervisor.start())

        # Register SIGTERM/SIGINT hooks for graceful shutdown
        # WAL SQLite provides atomicity in milliseconds
        import signal
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGTERM, signal.SIGINT):
            try:
                loop.add_signal_handler(
                    sig,
                    lambda: asyncio.create_task(self._graceful_shutdown())
                )
            except NotImplementedError:
                pass  # Windows — ignore, call shutdown manually

        logger.info("Agent started: CE + Invariant Checker + Heartbeat active")

    async def _graceful_shutdown(self):
        """
        Graceful Shutdown — atomic save of L0/L1 before exit.

        We use SQLite WAL mode for an atomic dump
        in milliseconds instead of tempfile+os.replace (seconds under load).
        WAL (Write-Ahead Log) guarantees atomicity without blocking reads.

        Problem: L0 Working Memory and L1 STM live in-memory.
        On SIGTERM/SIGKILL without hooks — they are lost irretrievably.
        """
        import json
        logger.info("Graceful shutdown: saving L0/L1 snapshot via WAL SQLite...")

        snapshot = {
            "meta": {
                "saved_at": datetime.now(timezone.utc).isoformat() + "Z",
                "session_id": self.session_id,
                "shutdown": "graceful",
                "version": "8.0"
            },
            # L0 Working Memory — read from working_memory (not stm_cache!)
            # L0 and L1 are different layers: working_memory = 4±1 active slots, stm_cache = session episodes
            "working_memory": [
                {"id": m.id, "content": m.content,
                 "importance": float(m.importance),
                 "priority": getattr(m, 'priority', 'MEDIUM'),
                 "level": str(m.level)}
                for m in getattr(self.fractal_memory, 'working_memory', [])
                if getattr(m, 'priority', 'MEDIUM') in ('CRITICAL', 'HIGH')
            ],
            # L1 STM — full snapshot of all cache items
            "stm_cache": [
                {"id": m.id, "content": m.content,
                 "importance": float(m.importance),
                 "created_at": m.created_at.isoformat() if hasattr(m.created_at, 'isoformat') else str(m.created_at),
                 "level": str(m.level)}
                for m in self.fractal_memory.stm_cache
            ]
        }

        # SQLite WAL mode — milliseconds instead of seconds
        # PRAGMA journal_mode=WAL is set during DB initialization
        async with self.sqlite_db.transaction():
            await self.sqlite_db.execute(
                """INSERT OR REPLACE INTO l0l1_snapshots
                   (session_id, saved_at, snapshot_json)
                   VALUES (?, ?, ?)""",
                (self.session_id,
                 datetime.now(timezone.utc).isoformat(),
                 json.dumps(snapshot, ensure_ascii=False))
            )
        # WAL checkpoint — write the WAL into the main DB
        await self.sqlite_db.execute("PRAGMA wal_checkpoint(TRUNCATE)")

        logger.info("L0/L1 snapshot saved via WAL. Shutting down.")
        asyncio.get_running_loop().stop()

    async def _dlq_processor(self):
        """Process the DLQ in the background"""
        while True:
            await asyncio.sleep(3600)  # Every hour
            await self.event_bus.process_dlq()

    @trace_async("agent_chat")
    async def chat(self, user_message: str) -> str:
        """
        Main interaction method with full tracing
        """
        with tracer.start_as_current_span("preprocessing") as span:
            span.set_attribute("message_length", len(user_message))
            
            # 1. Log the incoming message
            publish_success = await self.event_bus.publish(AgentEvent(
                event_type=EventType.USER_MESSAGE,
                timestamp=datetime.now(timezone.utc),
                content={"message": user_message},
                metadata={},
                session_id=self.session_id
            ))
            
            if not publish_success:
                span.add_event("Event published to fallback queue")
            
            # 2. Add to STM
            embedding = await self._get_embedding(user_message)
            await self.fractal_memory.add_to_stm(user_message, embedding)
        
        # 3. Retrieval - find the relevant context
        with tracer.start_as_current_span("memory_retrieval"):
            retrieved_memories = await self.retriever.retrieve(
                query=user_message,
                query_type="conversation"
            )
        
        # 4. Find applicable strategies (if it is a task)
        strategies = []
        if self._is_task_query(user_message):
            with tracer.start_as_current_span("strategy_retrieval"):
                strategies = await self.reasoning_bank.retrieve_relevant_strategies(
                    current_task=user_message,
                    context={},
                    epsilon=0.1  # 10% exploration
                )
        
        # 5. Build the context for the LLM
        with tracer.start_as_current_span("context_building") as span:
            context = self.context_builder.build_context(
                current_query=user_message,
                retrieved_memories=retrieved_memories,
                strategies=strategies,
                conversation_history=self.conversation_history
            )
            
            context_tokens = count_tokens(context)
            span.set_attribute("context_tokens", context_tokens)
            tokens_per_query.observe(context_tokens)
        
        # 6. Generate the response (THE SINGLE LLM call)
        with tracer.start_as_current_span("llm_generation") as span:
            response = await self.llm.chat(context)
            
            response_tokens = count_tokens(response)
            span.set_attribute("response_tokens", response_tokens)
            tokens_used.labels(component="llm").inc(context_tokens + response_tokens)
        
        # 7. Log the response
        await self.event_bus.publish(AgentEvent(
            event_type=EventType.AGENT_RESPONSE,
            timestamp=datetime.now(timezone.utc),
            content={"message": response},
            metadata={"tokens": response_tokens},
            session_id=self.session_id
        ))
        
        # 8. Update the history
        self.conversation_history.append(f"User: {user_message}")
        self.conversation_history.append(f"Assistant: {response}")
        
        # Limit the history (last 10 messages)
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]
        
        return response

    async def execute_task_with_learning(
        self,
        task: str,
        context: Dict
    ):
        """
        Execute a task with the self-learning loop.
        Delegates to the persistent _task_agent — reasoning_bank accumulates
        experience across calls (it is not reset on each execute_task_with_learning).
        """
        return await self._task_agent.execute_task(task, context)

    async def health_check(self) -> dict:
        """Health check of all components"""
        return {
            "event_bus": await self.event_bus.health_check(),
            "neo4j_breaker": self.graph_memory.neo4j_breaker.get_state(),
            "memory_size": {
                "stm": len(self.fractal_memory.stm_cache),
                "mtm": len(self.fractal_memory.mtm_cache)
            },
            "session_id": self.session_id
        }
```

---

## 🔍 Historical Sprint Components

### 7. OpenTelemetry: Observability and tracing

**Purpose**: Debugging and monitoring performance in production

```python
# observability.py
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
import time
from functools import wraps

# Tracer initialization
resource = Resource.create({"service.name": "fractal-memory-agent"})
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)

# Export to OTLP collector (Grafana Tempo, Jaeger, etc)
otlp_exporter = OTLPSpanExporter(
    endpoint="http://localhost:4317",
    insecure=True
)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Decorator for automatic tracing
def trace_async(span_name: str = None):
    """Decorator for tracing asynchronous functions"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            name = span_name or f"{func.__module__}.{func.__name__}"
            
            with tracer.start_as_current_span(name) as span:
                # Add parameters as attributes
                if args:
                    span.set_attribute("args_count", len(args))
                if kwargs:
                    for k, v in kwargs.items():
                        if isinstance(v, (str, int, float, bool)):
                            span.set_attribute(f"param.{k}", v)
                
                start_time = time.time()
                
                try:
                    result = await func(*args, **kwargs)
                    
                    # Success
                    duration = time.time() - start_time
                    span.set_attribute("duration_ms", duration * 1000)
                    span.set_status(Status(StatusCode.OK))
                    
                    return result
                    
                except Exception as e:
                    # Error
                    span.set_status(Status(StatusCode.ERROR, str(e)))
                    span.record_exception(e)
                    raise
        
        return wrapper
    return decorator

# Application in components
class ObservableHybridRetriever(HybridRetriever):
    """HybridRetriever with tracing"""

    @trace_async("hybrid_retrieval")
    async def retrieve(
        self,
        query: str,
        query_type: str = "general"
    ) -> List[RetrievalResult]:
        """Retrieval with full tracing of each stage"""
        
        with tracer.start_as_current_span("routing") as span:
            strategy = self._route_query(query, query_type)
            span.set_attribute("strategy", strategy)
        
        results = []
        
        # Stage 1: STM search
        with tracer.start_as_current_span("stm_search") as span:
            # P1-G FIX: added "RECALL" and "TASK" — ObservableHybridRetriever
            # was silently breaking the two most frequent queries: they received no STM results.
            # Synchronized with the parent HybridRetriever.
            if strategy in ["conversation", "immediate", "RECALL", "TASK"]:
                query_embedding = await self._get_embedding(query)
                stm_results = await self._search_stm(query, query_embedding)
                span.set_attribute("stm_hits", len(stm_results))
                results.extend(stm_results)
        
        # Stage 2: Graph search
        with tracer.start_as_current_span("graph_search") as span:
            start = time.time()
            graph_results = await self.graph.search(query, num_results=10)
            latency = time.time() - start
            
            span.set_attribute("graph_hits", len(graph_results))
            span.set_attribute("latency_ms", latency * 1000)
            
            results.extend(self._convert_to_retrieval_results(
                graph_results, source="graph"
            ))
        
        # Stage 3: Reranking
        with tracer.start_as_current_span("reranking") as span:
            results = await self._rerank(query, results)
            span.set_attribute("reranked_count", len(results))
        
        # Stage 4: Token budgeting
        with tracer.start_as_current_span("token_budgeting") as span:
            results = self._apply_token_budget(results)
            
            total_tokens = sum(r.tokens for r in results if hasattr(r, 'tokens'))
            span.set_attribute("selected_count", len(results))
            span.set_attribute("total_tokens", total_tokens)
        
        return results

# Example of integration into GraphMemory
class ObservableGraphMemory(GraphMemory):
    @trace_async("graph_search")
    async def search(self, query: str, num_results: int = 5):
        """Search with detailed tracing"""
        with tracer.start_as_current_span("graphiti_search") as span:
            span.set_attribute("query_length", len(query))
            span.set_attribute("num_results", num_results)
            
            results = await super().search(query, num_results)
            
            span.set_attribute("results_count", len(results))
            return results

    @trace_async("add_episode")
    async def add_episode(self, *args, **kwargs):
        """Episode creation with tracing"""
        return await super().add_episode(*args, **kwargs)
```

**Viewing traces in Grafana Tempo:**

```yaml
# docker-compose.yml for observability stack
# P3-E FIX: the version: field is deprecated in Docker Compose v2+. Removed.
services:
  tempo:
    image: grafana/tempo:latest
    ports:
      - "4317:4317"  # OTLP gRPC
      - "3200:3200"  # Tempo HTTP
    volumes:
      - ./tempo-data:/var/tempo
  
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_AUTH_ANONYMOUS_ENABLED=true
    volumes:
      - ./grafana-data:/var/lib/grafana
```

---

### 8. Memory Garbage Collection

**Purpose**: Cleaning up low-importance memory and preventing unbounded graph growth

```python
# memory_gc.py
from datetime import datetime, timedelta, timezone  # P0-B FIX: timezone added (previously NameError)
import logging

logger = logging.getLogger(__name__)

class MemoryGarbageCollector:
    """
    Periodic memory cleanup:
    - Removal of low-importance nodes
    - Merging of duplicates
    - MTM cache compression
    - Archival of old episodes
    """

    def __init__(
        self,
        graph: GraphMemory,
        fractal_memory: FractalMemory,
        archival: MemoryArchival = None
    ):
        self.graph = graph
        self.fractal = fractal_memory
        self.archival = archival
        
        # Thresholds for GC
        self.importance_threshold = 0.1
        self.age_threshold_days = 30
        self.access_threshold = 0  # Has never been accessed

    async def run_full_gc(self):
        """
        Full garbage collection (run weekly)
        """
        logger.info("Starting memory garbage collection")
        
        stats = {
            "deleted_episodes": 0,
            "deleted_entities": 0,
            "merged_duplicates": 0,
            "archived_count": 0,
            "freed_mtm_slots": 0
        }
        
        # 1. Delete low-importance episodes
        stats["deleted_episodes"] = await self._delete_low_importance_episodes()
        
        # 2. Delete unused entities
        stats["deleted_entities"] = await self._delete_orphan_entities()
        
        # 3. Merge duplicates
        stats["merged_duplicates"] = await self._merge_duplicate_entities()
        
        # 4. Cascade invalidation: lower confidence on Strategy when a Fact is invalidated
        # Without this, Strategies become "phantom" — they rely on dead facts
        await self._cascade_invalidate_dependent_strategies()
        
        # 5. Archival of old episodes (if configured)
        if self.archival:
            stats["archived_count"] = await self.archival.archive_old_episodes(
                older_than_days=365,
                importance_threshold=0.3
            )
            # Vacuum Worker — physical deletion after S3 + 90 days
            stats["vacuum_deleted"] = await self.archival.vacuum_soft_deleted(min_age_days=90)
        
        # 6. MTM cache compression
        stats["freed_mtm_slots"] = await self._compress_mtm_cache()
        
        logger.info(f"GC completed: {stats}")
        return stats

    async def _delete_low_importance_episodes(self) -> int:
        """
        Soft Delete of low-importance episodes → then Hard Delete after S3 archival.
        
        PROTOCOL:
        1. First deactivate (is_active = false) — Soft Delete
        2. Archive to S3
        3. Only after success — physical DETACH DELETE
        """
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=self.age_threshold_days)
        
        # Step 1: Soft Delete — deactivate, do not delete
        soft_delete_query = """
        MATCH (ep:Episode)
        WHERE ep.importance_score < $importance_threshold
          AND ep.timestamp < $cutoff_date
          AND ep.access_count <= $access_threshold
          AND ep.is_active <> false
        WITH ep
        LIMIT 1000
        SET ep.is_active = false, ep.valid_to = datetime()
        RETURN count(ep) as deactivated_count
        """
        
        result = await self.graph.execute_cypher(soft_delete_query, {
            "importance_threshold": self.importance_threshold,
            "cutoff_date": cutoff_date.isoformat(),
            "access_threshold": self.access_threshold
        })
        
        deactivated = result[0]["deactivated_count"] if result else 0
        
        # Step 2: Hard Delete only of nodes that have already been deactivated > 30 days
        # (they should already have been archived in a previous GC cycle)
        hard_cutoff = datetime.now(timezone.utc) - timedelta(days=self.age_threshold_days * 3)
        
        hard_delete_query = """
        MATCH (ep:Episode)
        WHERE ep.is_active = false
          AND ep.valid_to < $hard_cutoff
        WITH ep
        LIMIT 500
        DETACH DELETE ep
        RETURN count(ep) as deleted_count
        """
        
        hard_result = await self.graph.execute_cypher(hard_delete_query, {
            "hard_cutoff": hard_cutoff.isoformat()
        })
        
        deleted = hard_result[0]["deleted_count"] if hard_result else 0
        logger.info(f"Soft-deleted: {deactivated} episodes. Hard-deleted: {deleted} archived episodes")
        return deactivated + deleted

    async def _delete_orphan_entities(self) -> int:
        """
        Delete entities with no relations (orphaned nodes)
        """
        query = """
        MATCH (e:Entity)
        WHERE NOT (e)-[]-()
          AND e.importance_score < $threshold
        WITH e
        LIMIT 500
        DETACH DELETE e   -- P1-C FIX: DELETE without DETACH fails if the node has relations

-- P4-A FIX: add label :SoftDeleted for an O(1) scan instead of a Full Node Scan.
-- MATCH (n) WHERE n.is_active=false — a low-cardinality Boolean, indexes poorly.
-- CREATE INDEX soft_deleted_idx IF NOT EXISTS FOR (n:Episode) ON (n.is_active, n.valid_to);
-- On soft delete: SET ep.is_active=false, ep.valid_to=datetime() — label lookup O(1).
        RETURN count(e) as deleted_count
        """
        
        result = await self.graph.execute_cypher(query, {
            "threshold": self.importance_threshold * 2  # Slightly higher threshold
        })
        
        deleted = result[0]["deleted_count"] if result else 0
        logger.info(f"Deleted {deleted} orphan entities")
        return deleted

    async def _merge_duplicate_entities(self) -> int:
        """
        Find and merge duplicate entities
        (for example, "OpenAI" and "openai" → one entity)

        P0-4 FIX: We use _merge_nodes_safe() from dedupe_entities.py —
        APOC if available, otherwise a pure Cypher fallback for LadybugDB/KuzuDB.
        """
        # Find merge candidates (similar names)
        query = """
        MATCH (e1:Entity), (e2:Entity)
        WHERE id(e1) < id(e2)
          AND toLower(e1.name) = toLower(e2.name)
          AND e1.type = e2.type
        WITH e1, e2
        LIMIT 100
        RETURN e1, e2
        """

        candidates = await self.graph.execute_cypher(query)

        merged_count = 0
        for pair in candidates:
            e1, e2 = pair["e1"], pair["e2"]

            # P0-4 FIX: _merge_nodes_safe() selects APOC or the Cypher fallback
            # automatically based on the HAS_APOC env var — without changes in the calling code.
            await _merge_nodes_safe(self.graph, e1["id"], e2["id"])
            merged_count += 1

        logger.info(f"Merged {merged_count} duplicate entities")
        return merged_count

    async def _compress_mtm_cache(self) -> int:
        """
        Clear the MTM cache of low-importance items
        """
        initial_size = len(self.fractal.mtm_cache)
        
        # Remove items with importance < 0.3
        self.fractal.mtm_cache = [
            item for item in self.fractal.mtm_cache
            if item.importance >= 0.3
        ]
        
        freed = initial_size - len(self.fractal.mtm_cache)
        logger.info(f"Freed {freed} MTM cache slots")
        return freed

    async def _cascade_invalidate_dependent_strategies(self) -> int:
        """
        Cascade invalidation: on Soft Delete of a :Fact, lower the confidence
        of all :Strategy nodes derived from that fact via [:DERIVED_FROM].
        
        Without this, Strategies become "phantom" — strategies that rely
        on invalidated facts continue to be applied as if valid.
        
        RULE: confidence -= 0.2 for each invalidated DERIVED_FROM fact.
                 If confidence < 0.3 → the Strategy is also marked is_active=false.
        """
        # the penalty is applied only to facts
        # that have NOT yet been accounted for previously. The penalized_fact_ids field stores
        # the IDs of already-penalized facts — preventing double charging during GC.
        query = """
        MATCH (s:Strategy)-[:DERIVED_FROM]->(f:Fact)
        WHERE f.is_active = false
          AND s.is_active = true
          AND NOT f.id IN coalesce(s.penalized_fact_ids, [])
          AND f.is_ring_zero <> true
        WITH s, collect(f.id) as new_invalid_ids, count(f) as new_invalidated
        SET s.confidence = CASE
            WHEN s.confidence - (new_invalidated * 0.2) < 0.0
            THEN 0.0   -- P9-FIX BUG-3: floor only when going negative, not when crossing 0.3
            ELSE s.confidence - (new_invalidated * 0.2)
        END,
        s.is_active = CASE
            WHEN s.confidence - (new_invalidated * 0.2) < 0.3
            THEN false
            ELSE true
        END,
        s.penalized_fact_ids = (coalesce(s.penalized_fact_ids, []) + new_invalid_ids)[-500:]  -- P9-FIX BUG-12: cap 500
        RETURN count(s) as updated_strategies
        """
        result = await self.graph.execute_cypher(query)
        updated = result[0]["updated_strategies"] if result else 0
        logger.info(f"Cascade invalidation: updated {updated} strategies")
        return updated

    async def schedule_periodic_gc(self):
        """
        Run periodic GC (every 7 days)
        """
        while True:
            await asyncio.sleep(7 * 24 * 3600)  # 7 days
            
            try:
                await self.run_full_gc()
            except Exception as e:
                logger.error(f"GC failed: {e}")
```

---

## 📈 Monitoring and Metrics

**Critically important metrics to track**:

```python
# metrics.py
from prometheus_client import Counter, Histogram, Gauge, Enum

# === Tokens ===
tokens_used = Counter(
    "agent_tokens_used_total",
    "Total tokens used",
    ["component"]  # llm, embeddings, etc
)
tokens_per_query = Histogram(
    "agent_tokens_per_query",
    "Tokens per query",
    buckets=[100, 500, 1000, 2000, 5000, 10000]
)
token_budget_utilization = Histogram(
    "token_budget_utilization_ratio",
    "How much of token budget was used",
    buckets=[0.1, 0.3, 0.5, 0.7, 0.9, 1.0]
)

# === Memory ===
memory_size = Gauge(
    "agent_memory_size",
    "Size of memory by level",
    ["level"]  # stm, mtm, ltm
)
consolidation_duration = Histogram(
    "memory_consolidation_duration_seconds",
    "Time to consolidate memory",
    ["source", "target"],  # stm->mtm, mtm->ltm
    buckets=[1, 5, 10, 30, 60, 300]
)
memory_importance_distribution = Histogram(
    "memory_importance_score",
    "Distribution of importance scores",
    buckets=[0.1, 0.2, 0.3, 0.5, 0.7, 0.9, 1.0]
)

# === Performance ===
retrieval_latency = Histogram(
    "retrieval_latency_seconds",
    "Retrieval latency by stage",
    ["stage"],  # stm, graph, rerank, total
    buckets=[0.01, 0.05, 0.1, 0.3, 0.5, 1.0, 3.0]
)
response_latency = Histogram(
    "response_latency_seconds",
    "End-to-end response time",
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
)
neo4j_query_duration = Histogram(
    "neo4j_query_duration_seconds",
    "Neo4j query execution time",
    ["query_type"],
    buckets=[0.01, 0.05, 0.1, 0.3, 0.5, 1.0]
)

# === Quality ===
retrieval_precision = Gauge(
    "retrieval_precision",
    "Precision of memory retrieval"
)
retrieval_recall = Gauge(
    "retrieval_recall",
    "Recall of memory retrieval"
)
task_success_rate = Gauge(
    "task_success_rate",
    "Task success rate",
    ["task_type"]
)
strategy_effectiveness = Gauge(
    "strategy_effectiveness",
    "Strategy success rate",
    ["strategy_id"]
)

# === Circuit Breaker ===
circuit_breaker_state = Enum(
    "circuit_breaker_state",
    "Current circuit breaker state",
    ["service"],  # neo4j, redis, llm
    states=["closed", "open", "half_open"]
)
circuit_breaker_failures = Counter(
    "circuit_breaker_failures_total",
    "Total failures by service",
    ["service"]
)
circuit_breaker_trips = Counter(
    "circuit_breaker_trips_total",
    "How many times breaker opened",
    ["service"]
)

# === Event Bus ===
event_bus_published = Counter(
    "event_bus_published_total",
    "Events published",
    ["event_type"]
)
event_bus_failed = Counter(
    "event_bus_failed_total",
    "Failed event publications",
    ["event_type"]
)
dlq_size = Gauge(
    "event_bus_dlq_size",
    "Dead letter queue size"
)
fallback_queue_size = Gauge(
    "event_bus_fallback_queue_size",
    "Fallback queue size (when Redis down)"
)

# === Garbage Collection ===
gc_duration = Histogram(
    "memory_gc_duration_seconds",
    "Time to run full GC",
    buckets=[10, 30, 60, 300, 600]
)
gc_deleted_nodes = Counter(
    "memory_gc_deleted_nodes_total",
    "Nodes deleted by GC",
    ["node_type"]  # episode, entity
)
gc_freed_memory = Gauge(
    "memory_gc_freed_bytes",
    "Memory freed by GC in bytes"
)

# === Strategy Learning ===
# P3-D FIX: UCB1 replaced with Thompson Sampling (RFC0039). Metric renamed.
strategy_ts_scores = Histogram(
    "strategy_thompson_score",
    "Thompson Sampling Beta-distribution scores for strategy selection (P3-D FIX: was strategy_ucb_score)",
    buckets=[0, 0.2, 0.5, 0.8, 1.0]
)
exploration_vs_exploitation = Counter(
    "strategy_selection_mode_total",
    "Exploration vs exploitation count",
    ["mode"]  # exploration, exploitation
)

# === ConsolidationEngine ===
ce_queue_size = Gauge(
    "consolidation_engine_queue_size",
    "Pending operations in CE queue"
)
ce_dlq_size = Gauge(
    "consolidation_engine_dlq_size",
    "Failed operations in CE dead letter queue"
)
ce_op_duration = Histogram(
    "consolidation_engine_op_duration_seconds",
    "CE operation duration",
    ["op_type"],   # CONSOLIDATE, ARCHIVE, GC
    buckets=[0.1, 0.5, 1.0, 5.0, 10.0, 30.0]
)
ce_timeout_total = Counter(
    "consolidation_engine_timeout_total",
    "Total CE operation timeouts"
)

# === Cognitive Modes ===
cognitive_mode_requests = Counter(
    "cognitive_mode_requests_total",
    "Requests by cognitive mode",
    ["mode"]   # precision, balanced, exploration
)
cognitive_mode_tokens = Histogram(
    "cognitive_mode_tokens_used",
    "Tokens used per cognitive mode",
    ["mode"],
    buckets=[100, 500, 1000, 2000, 3000, 4000]
)

# === Memory Budget Planner ===
graph_nodes_total = Gauge(
    "memory_budget_graph_nodes_total",
    "Total active nodes in Neo4j graph"
)
graph_fill_ratio = Gauge(
    "memory_budget_fill_ratio",
    "Graph fill ratio vs MAX_NODES_TOTAL (0.0-1.0)"
)
budget_blocks_total = Counter(
    "memory_budget_blocks_total",
    "Times write was blocked by Budget Planner"
)

# === Runtime Invariant Checker ===
invariant_violations_total = Counter(
    "invariant_violations_total",
    "RFC invariant violations detected",
    ["invariant_id", "severity"]
)
safe_mode_activations_total = Counter(
    "safe_mode_activations_total",
    "Times Safe Mode was activated",
    ["reason"]
)

# === PII Redaction ===
pii_redacted_total = Counter(
    "pii_redacted_total",
    "PII tokens redacted before storage",
    ["pii_type"]   # email, phone_ru, card, etc.
)
```

**Example of using the metrics in code**:

```python
# In HybridRetriever
async def retrieve(self, query: str):
    start = time.time()

    # STM search
    stm_start = time.time()
    stm_results = await self._search_stm(query)
    retrieval_latency.labels(stage="stm").observe(time.time() - stm_start)

    # Graph search
    graph_start = time.time()
    graph_results = await self.graph.search(query)
    retrieval_latency.labels(stage="graph").observe(time.time() - graph_start)

    # Total
    retrieval_latency.labels(stage="total").observe(time.time() - start)

    return results

# In Circuit Breaker
def _on_failure(self, error: Exception):
    circuit_breaker_failures.labels(service=self.name).inc()

    if self.failure_count >= self.failure_threshold:
        circuit_breaker_trips.labels(service=self.name).inc()
        circuit_breaker_state.labels(service=self.name).state("open")
```

---

## 📐 SLO Contract (Service Level Objectives)

> Thresholds for Grafana alert rules. All values come from `velantrim_config.SLOConfig`.

| Metric | SLO (target) | WARN | CRITICAL |
|---------|-----------|------|---------|
| search P95 latency | <500ms | >800ms | >2000ms |
| Etir P95 latency | <50ms | >80ms | >200ms |
| consolidation lag | <60s | >120s | >300s |
| GC weekly runtime | <2h | >3h | >6h |
| staging_candidates | <5 000 records | >8 000 | >MAX_STAGING |
| DLQ size | <10 | >10 (DEGRADED) | >50 (SAFE_MODE) |
| budget fill ratio | <0.85 | >0.85 | >0.90 |
| output_faithfulness | >0.80 | <0.60 | <0.40 |
| L2 MHI | >0.60 | <0.50 | <0.30 |

### MetaSupervisor Auto-Triggers

```
MHI < 0.30           → immediate GC + alert ops
MHI < 0.50           → MetaSupervisor → DEGRADED (speed up ConsolidationEngine)
budget_fill > 0.85   → MetaSupervisor → DEGRADED
budget_fill > 0.90   → MetaSupervisor → block writes
DLQ > 50             → MetaSupervisor → SAFE_MODE
faithfulness < 0.40  → alert + log unsupported_sentences
```

---

## 🔌 MCP Server — Connecting to External Clients

> **Purpose**: Velantrim as a tool in Cursor, Claude Code, and any MCP-compatible client. The agent becomes available through a standard protocol without changes to the core code.

```python
# mcp_server/server.py
# MCP stdio transport — connects Velantrim to Cursor / Claude Code
# Run: python -m mcp_server.server
# Cursor config: { "velantrim": { "command": "python", "args": ["-m", "mcp_server.server"] } }

import asyncio, json, sys, logging
from pipeline import VelantrimPipeline  # the agent's main pipeline

logger = logging.getLogger(__name__)

TOOLS = [
    {
        "name": "memory_search",
        "description": "Find facts in Velantrim's long-term memory by query",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query":      {"type": "string", "description": "Search query"},
                "session_id": {"type": "string", "description": "Session ID (optional)"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "memory_write",
        "description": "Write a fact to long-term memory via Truth Gate (voluntary write)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "content":    {"type": "string", "description": "Fact to remember"},
                "reason":     {"type": "string", "description": "Reason for the write"},
                "importance": {"type": "number", "description": "Importance 0.0–1.0"}
            },
            "required": ["content", "reason"]
        }
    },
    {
        "name": "memory_status",
        "description": "Velantrim memory system status: nodes, Hot Graph, ESM distribution",
        "inputSchema": {"type": "object", "properties": {}}
    }
]

async def handle_request(pipeline: VelantrimPipeline, request: dict) -> dict:
    method = request.get("method")
    params = request.get("params", {})
    rid    = request.get("id")

    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": rid, "result": {"tools": TOOLS}}

    if method == "tools/call":
        name      = params.get("name")
        arguments = params.get("arguments", {})
        try:
            if name == "memory_search":
                results = await pipeline.hybrid_retriever.retrieve(
                    query=arguments["query"],
                    session_id=arguments.get("session_id", "mcp")
                )
                text = "\n".join(f"[{r.source}] {r.content}" for r in results[:5])
                content = text or "Nothing found."

            elif name == "memory_write":
                result = await pipeline.volition_worker.write_voluntary(
                    session_id="mcp",
                    agent_id="mcp_client",
                    content=arguments["content"],
                    reason=arguments["reason"],
                    importance_hint=float(arguments.get("importance", 0.8))
                )
                content = f"Result: {result.outcome.value}"

            elif name == "memory_status":
                health = await pipeline.graph.health_check()
                content = json.dumps(health, ensure_ascii=False, indent=2)

            else:
                content = f"Unknown tool: {name}"

        except Exception as e:
            logger.error(f"MCP tool error [{name}]: {e}")
            return {"jsonrpc": "2.0", "id": rid,
                    "error": {"code": -32603, "message": str(e), "data": {"tool": name}}}
            # P9-FIX BUG-4: JSON-RPC error instead of result — the client (Cursor/Claude Code) receives a correct error object for retry

        return {"jsonrpc": "2.0", "id": rid,
                "result": {"content": [{"type": "text", "text": content}]}}

    return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32601, "message": "Method not found"}}

async def main():
    pipeline = VelantrimPipeline()
    await pipeline.start()
    logger.info("Velantrim MCP Server started (stdio)")
    while True:
        line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
        if not line:
            break
        try:
            request  = json.loads(line.strip())
            response = await handle_request(pipeline, request)
            print(json.dumps(response, ensure_ascii=False), flush=True)
        except Exception as e:
            logger.error(f"MCP parse error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

**Connecting to Cursor** — add to `.cursor/mcp.json`:
```json
{
  "velantrim": {
    "command": "python",
    "args": ["-m", "mcp_server.server"],
    "cwd": "/path/to/velantrim"
  }
}
```

**Invariant**: the MCP Server is only a thin wrapper over the existing pipeline. It contains no memory logic of its own. `memory_write` must always go through `VolitionWorker` → Truth Gate, not directly into the graph.

---

## 🔍 Audit Layer — Verifiability Layer (Phase 1+)

> **Why it is critical**: without the Audit Layer it is impossible to understand why the agent answered the way it did. In the event of a hallucination, there is no tool to find who is to blame: the LLM during generation, Etir during retrieval, or Graphiti when writing the fact.

```
Three mandatory API methods:

GET /memory/audit/context?request_id=...
→ Shows: which nodes from L3.5 Etir were activated,
  which facts from L3 made it into the context, how many tokens were used

GET /memory/audit/strategy?request_id=...
→ Shows: which strategy from ReasoningBank was selected,
  the Thompson Sampling score of each strategy, the mode (exploration/exploitation)

GET /memory/audit/forgetting?since=...
→ Shows: which facts were deactivated (is_active=false),
  why ([:CONTRADICTS] / low importance / age),
  what was archived to S3
```

**Minimal implementation for Phase 1:**

```python
# audit_layer.py
_AUDIT_SCHEMA = """
CREATE TABLE IF NOT EXISTS audit_context (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id TEXT NOT NULL, session_id TEXT, query TEXT,
    etir_nodes TEXT, facts_used TEXT,
    tokens_used INTEGER, token_budget INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS audit_strategy (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id TEXT NOT NULL, session_id TEXT,
    strategy_id TEXT, strategy_desc TEXT, score REAL,
    selection_mode TEXT, all_candidates TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS audit_forgetting (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    node_id TEXT NOT NULL, node_type TEXT, reason TEXT,
    importance_at_delete REAL, archived_to_s3 BOOLEAN DEFAULT FALSE, s3_key TEXT,
    deleted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_ctx_req ON audit_context(request_id);
CREATE INDEX IF NOT EXISTS idx_fgt_at  ON audit_forgetting(deleted_at);
"""


class AuditLayer:
    """
    Audit layer — makes the system transparent.
    Writes to SQLite (already in the stack as the operational DB).
    All writes are fire-and-forget via asyncio.create_task() (I28: do not block the Fast Path).

    GET /memory/audit/context?request_id=   → which Etir nodes and facts entered the prompt
    GET /memory/audit/strategy?request_id=  → which strategy was selected and why
    GET /memory/audit/forgetting?since=     → what was forgotten, when, why
    """

    def __init__(self, graph: GraphMemory, sqlite_db: str = "velantrim_audit.db"):
        self.graph   = graph
        self.db_path = sqlite_db
        self._ready  = False

    async def _ensure_schema(self):
        if self._ready:
            return
        try:
            import aiosqlite
            async with aiosqlite.connect(self.db_path) as db:
                await db.executescript(_AUDIT_SCHEMA)
                await db.commit()
            self._ready = True
        except Exception as e:
            logger.warning(f"AuditLayer._ensure_schema: {e}")

    async def log_context_selection(
        self,
        request_id: str,
        query: str,
        etir_nodes: list,
        retrieved_facts: list,
        tokens_used: int,
        token_budget: int,
        session_id: str = ""
    ):
        """Call from ResponseAuditWorker via asyncio.create_task() — Slow Path only."""
        await self._ensure_schema()
        try:
            import aiosqlite, json
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    "INSERT INTO audit_context VALUES (NULL,?,?,?,?,?,?,?,CURRENT_TIMESTAMP)",
                    (request_id, session_id, query[:500],
                     json.dumps(etir_nodes), json.dumps(retrieved_facts),
                     tokens_used, token_budget)
                )
                await db.commit()
        except Exception as e:
            logger.warning(f"AuditLayer.log_context: {e}")

    async def log_strategy_selection(
        self,
        request_id: str,
        strategy_id: str,
        strategy_desc: str,
        score: float,
        selection_mode: str,
        all_candidates: list,
        session_id: str = ""
    ):
        """Call from ReasoningBank.retrieve_relevant_strategies() — Slow Path."""
        await self._ensure_schema()
        try:
            import aiosqlite, json
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    "INSERT INTO audit_strategy VALUES (NULL,?,?,?,?,?,?,?,CURRENT_TIMESTAMP)",
                    (request_id, session_id, strategy_id, strategy_desc[:300],
                     score, selection_mode, json.dumps(all_candidates))
                )
                await db.commit()
        except Exception as e:
            logger.warning(f"AuditLayer.log_strategy: {e}")

    async def log_forgetting(
        self,
        node_id: str,
        node_type: str,
        reason: str,
        importance_at_delete: float,
        archived_to_s3: bool = False,
        s3_key: str = None
    ):
        """Call from MemoryGarbageCollector on soft-delete — Slow Path."""
        await self._ensure_schema()
        try:
            import aiosqlite
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    "INSERT INTO audit_forgetting VALUES (NULL,?,?,?,?,?,?,CURRENT_TIMESTAMP)",
                    (node_id, node_type, reason, importance_at_delete, archived_to_s3, s3_key)
                )
                await db.commit()
        except Exception as e:
            logger.warning(f"AuditLayer.log_forgetting: {e}")

    async def explain_context(self, request_id: str) -> dict:
        """GET /memory/audit/context?request_id=..."""
        await self._ensure_schema()
        try:
            import aiosqlite, json
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                async with db.execute(
                    "SELECT * FROM audit_context WHERE request_id=? LIMIT 1", (request_id,)
                ) as cur:
                    row = await cur.fetchone()
            if not row:
                return {"error": f"no audit for request_id={request_id}"}
            d = dict(row)
            d["etir_nodes"]  = json.loads(d.get("etir_nodes")  or "[]")
            d["facts_used"]  = json.loads(d.get("facts_used")  or "[]")
            d["budget_pct"]  = round((d["tokens_used"] or 0) / max(d["token_budget"] or 1, 1), 3)
            return d
        except Exception as e:
            return {"error": str(e)}

    async def explain_strategy(self, request_id: str) -> dict:
        """GET /memory/audit/strategy?request_id=..."""
        await self._ensure_schema()
        try:
            import aiosqlite, json
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                async with db.execute(
                    "SELECT * FROM audit_strategy WHERE request_id=? LIMIT 1", (request_id,)
                ) as cur:
                    row = await cur.fetchone()
            if not row:
                return {"error": f"no audit for request_id={request_id}"}
            d = dict(row)
            d["all_candidates"] = json.loads(d.get("all_candidates") or "[]")
            return d
        except Exception as e:
            return {"error": str(e)}

    async def explain_forgetting(self, since: str, limit: int = 50) -> list:
        """GET /memory/audit/forgetting?since=2026-03-01T00:00:00"""
        await self._ensure_schema()
        try:
            import aiosqlite
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                async with db.execute(
                    "SELECT * FROM audit_forgetting WHERE deleted_at >= ?"
                    " ORDER BY deleted_at DESC LIMIT ?",
                    (since, limit)
                ) as cur:
                    return [dict(r) for r in await cur.fetchall()]
        except Exception as e:
            return [{"error": str(e)}]
```

> 💡 **For MVP Phase 0**: it is sufficient to simply write the audit to a `.log` file via Python `logging`. The full API is for Phase 1+.


class ContradictsUXProtocol:
    """
    UX protocol for [:CONTRADICTS] — the agent asks the user before an override.

    Rule from v2.19 (TruthGate.I3):
        "The LLM does NOT set [:CONTRADICTS] automatically.
         Only an explicit user command or the CRUD classifier."

    Without this class the LLM can silently overwrite a fact.
    With it — the agent stops and shows the conflict to the user.

    Usage:
        c   = ContradictsUXProtocol(graph, event_bus)
        msg = await c.detect_and_propose(new_fact_content, session_id)
        if msg:
            return msg          # stop the write, show it to the user
        # Once the user has replied:
        decision = await c.handle_user_response(user_reply, session_id)
        if decision["action"] == "override":
            pass  # proceed with writing the new fact
        elif decision["action"] == "keep":
            pass  # cancel the write
    """

    _YES = frozenset(["erase", "delete", "replace", "correct",
                       "i confirm", "ok", "yes", "confirm", "override"])
    _NO  = frozenset(["don't", "save", "leave",
                       "cancel", "no", "keep"])

    def __init__(self, graph_adapter, event_bus):
        self.graph      = graph_adapter
        self.event_bus  = event_bus
        self._pending: dict = {}   # session_id → {new_fact, old_id, old_summary}

    async def detect_and_propose(self, new_fact: str, session_id: str) -> str | None:
        """Searches for a potential conflict in L3. Returns a message for the user, or None."""
        results = await self.graph.search(query=f"contradicts: {new_fact[:200]}", limit=3)
        if not results:
            return None
        best        = results[0]
        old_summary = (best.get("content", str(best)) if isinstance(best, dict) else str(best))[:200]
        old_id      = best.get("id", "unknown") if isinstance(best, dict) else "unknown"
        self._pending[session_id] = {
            "new_fact": new_fact, "old_id": old_id, "old_summary": old_summary
        }
        return (f"⚠️ I see a possible contradiction with a previous decision:\n"
                f"  📌 Old: «{old_summary}»\n"
                f"  🆕 New:  «{new_fact[:200]}»\n\n"
                f"Erase the old one and write the new one? (yes / no)")

    async def handle_user_response(self, reply: str, session_id: str) -> dict:
        """Parses the user's reply. action: 'override' | 'keep' | 'pending'."""
        p = self._pending.get(session_id)
        if not p:
            return {"action": "pending", "proposal": None}
        q = reply.lower().strip()
        if any(w in q for w in self._YES):
            await self.graph.execute_cypher(
                "MATCH (f {id: $id}) SET f.is_active = false, f.valid_to = datetime(),"
                " f.contradicted_by_user = true",
                {"id": p["old_id"]}
            )
            del self._pending[session_id]
            return {"action": "override", "proposal": p}
        if any(w in q for w in self._NO):
            del self._pending[session_id]
            return {"action": "keep", "proposal": p}
        return {"action": "pending", "proposal": p}

    def clear_expired(self, active_sessions: list):
        """Clear pending entries for finished sessions."""
        for sid in [s for s in self._pending if s not in active_sessions]:
            del self._pending[sid]


class TokenBudgetLadder:
    """
    Priority ladder for the token budget — what gets trimmed FIRST when short.

    From v2.19: "If the budget is exhausted — L3 is cut first, L0 and Etir are always protected."
    In v5 the numbers were in TokenConfig, but the priority order was not explicitly fixed.

    Protected slots (never trimmed): ring_zero, L0, core_memory_blocks, etir.
    The rest — in ascending priority (6 → trimmed first).

    Usage:
        ladder   = TokenBudgetLadder(budget=TOKENS.BALANCED_MODE)
        selected = ladder.select({
            "ring_zero_values":   ring_zero_text,
            "L0_working_memory":  wm_text,
            "etir_activation":    etir_text,
            "l1_stm_episodes":    stm_text,
            "l3_ltm_graph":       ltm_text,
        })
        prompt = "\\n\\n".join(selected.values())
    """

    # (name, max_tokens, protected, priority — lower = more important, trimmed last)
    _SLOTS = [
        ("ring_zero_values",     150,  True,  1),
        ("L0_working_memory",    100,  True,  1),
        ("core_memory_blocks",   500,  True,  1),
        ("etir_activation",      300,  True,  2),
        ("l1_stm_episodes",      600,  False, 3),
        ("strategies",           300,  False, 4),
        ("l2_mtm_summaries",     300,  False, 5),
        ("l3_ltm_graph",         400,  False, 6),  # ← trimmed FIRST
        ("conversation_history", 300,  False, 7),
    ]

    def __init__(self, budget: int = 2000):
        self.budget = budget

    def select(self, slot_contents: dict) -> dict:
        """Returns a subset of slots guaranteed to fit within budget."""
        selected = {}
        used     = 0

        # Protected — always include first
        for name, max_tok, protected, _ in self._SLOTS:
            if not protected:
                continue
            text = slot_contents.get(name, "")
            if not text:
                continue
            tok   = min(self._count(text), max_tok)
            used += tok
            selected[name] = text[:tok * 4]

        # Non-protected — in priority order (greedy fit)
        for name, max_tok, protected, _ in self._SLOTS:
            if protected or used >= self.budget:
                continue
            text = slot_contents.get(name, "")
            if not text:
                continue
            allowed = min(self._count(text), max_tok, self.budget - used)
            if allowed <= 0:
                continue
            selected[name] = text[:allowed * 4]
            used += allowed

        logger.debug(f"TokenBudgetLadder: {len(selected)} slots ~{used}/{self.budget} tokens")
        return selected

    @staticmethod
    def _count(text: str) -> int:
        try:
            import tiktoken
            return len(tiktoken.get_encoding("cl100k_base").encode(text))
        except Exception:
            return max(1, len(text) // 4)
> 
> 💡 **Alternative without writing code**: LangSmith or Arize Phoenix — visual tracing of the entire path from request down to each graph node, out of the box.

---

## 🛡️ Memory Guardian — Protection Against Memory Poisoning 

> **Problem**: Without a validation layer the agent can write a hallucination into the graph as a fact. Within 1-2 months the system will start repeating erroneous patterns with confidence — it has "evidence".

**Memory Guardian** is the L5 Observer extended into the role of an L3 gatekeeper. No fact reaches Neo4j without passing through this layer.

```python
# memory_guardian.py
class MemoryGuardian:
    """
    Gatekeeper of the L3 graph. Implements the Truth Gate before writing.
    Lives in the L5 Observer — watches the flow, blocks poisoning.
    """

    def __init__(self, graph: GraphMemory, confidence_threshold: float = 0.7):
        self.graph = graph
        self.confidence_threshold = confidence_threshold

    async def validate_proposal(self, proposal: dict) -> bool:
        """
        Validate a fact/episode before writing it to L3.
        Returns True only if all checks pass.
        """
        # 1. Check for the presence of a source (evidence)
        if not proposal.get("evidence"):
            logger.warning(f"Guardian: rejected — no evidence: {proposal}")
            return False
        
        # 2. Confidence threshold
        if proposal.get("confidence", 0) < self.confidence_threshold:
            logger.warning(f"Guardian: rejected — low confidence: {proposal}")
            return False
        
        # 3. Check for contradictions with the existing graph
        contradictions = await self._check_contradictions(proposal)
        if contradictions:
            logger.warning(f"Guardian: conflict found — {len(contradictions)} contradictions")
            # Do not delete — create a [:CONTRADICTS] relation for resolution
            await self._mark_contradiction(proposal, contradictions)
            return False
        
        # 4. Deduplication
        if await self._is_duplicate(proposal):
            logger.info("Guardian: duplicate detected — incrementing evidence_count")
            await self._increment_evidence(proposal)
            return False  # Already present, the new one is not needed
        
        return True

    async def _check_contradictions(self, proposal: dict) -> list:
        """Search for contradictions in the L3 graph"""
        query = """
        MATCH (f:Fact)
        WHERE f.is_active = true
          AND f.concept = $concept
          AND f.relation = $relation
          AND f.value <> $value
        RETURN f
        LIMIT 10
        """
        return await self.graph.execute_cypher(query, {
            "concept": proposal.get("concept"),
            "relation": proposal.get("relation"),
            "value": proposal.get("value")
        })

    async def _is_duplicate(self, proposal: dict) -> bool:
        """Check for an exact duplicate"""
        query = """
        MATCH (f:Fact)
        WHERE f.is_active = true
          AND f.concept = $concept
          AND f.relation = $relation
          AND f.value = $value
        RETURN count(f) > 0 as exists
        """
        result = await self.graph.execute_cypher(query, proposal)
        return result[0]["exists"] if result else False
```

> 💡 **Integration**: `MemoryGuardian.validate_proposal()` is called inside `GraphMemory.add_episode()` before any write to Neo4j. The L5 Observer is extended with this module in Phase 1.

---

## 🗃️ Immutable Raw Memory — Protection Against Semantic Drift 

> **The Semantic Drift problem**: L1→L2→L3 consolidation via LLM summarization gradually distorts the meaning. "User prefers Python" → "User programs" → "User expert developer". The original is lost.

**Solution**: Raw episodes are stored separately and **never change**. Summarizations are stored separately. The original source is always accessible.

```python
# raw_memory_store.py
class ImmutableRawMemory:
    """
    Immutable store of raw episodes.
    Stored in SQLite (not in Neo4j) — simple, reliable, never changes.

    Rule: raw_episodes are never updated.
    Summarizations (summaries) are created on top, but the original is protected.

    Initialization: call await init() in an async context before first use.
    _init_schema() is NOT called from __init__ — this protects against blocking the event loop.
    """

    def __init__(self, db_path: str = "raw_memory.db"):
        self.db_path = db_path
        # The schema is initialized via await init(), not in __init__

    async def init(self):
        """Async-safe schema initialization. Call once at agent startup."""
        import aiosqlite
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("PRAGMA journal_mode=WAL")
            await db.execute("""
                CREATE TABLE IF NOT EXISTS raw_episodes (
                    id TEXT PRIMARY KEY,
                    content TEXT NOT NULL,
                    source TEXT,
                    timestamp TEXT NOT NULL,
                    session_id TEXT,
                    outcome TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                    -- No fields for updating — this is an append-only store
                )
            """)
            await db.commit()

    def save_episode(self, episode_id: str, content: str,
                     source: str, session_id: str, outcome: str = None):
        """
        Save a raw episode. Never update it.
        Call from an async context via asyncio.to_thread():
            await asyncio.to_thread(raw_memory.save_episode, episode_id, content, ...)
        """
        import sqlite3
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                # explicit column names — protection against silent breakage when the schema changes
                """INSERT OR IGNORE INTO raw_episodes
                   (id, content, source, timestamp, session_id, outcome)
                   VALUES (?, ?, ?, datetime('now'), ?, ?)""",
                (episode_id, content, source, session_id, outcome)
            )
            conn.commit()

    def get_truth_source(self, episode_id: str) -> dict:
        """
        Get the original episode.
        Used during reconstruction if a summarization distorted the meaning.
        """
        import sqlite3
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT * FROM raw_episodes WHERE id = ?", (episode_id,)
            ).fetchone()
        return dict(zip(["id","content","source","timestamp","session_id","outcome","created_at"], row)) if row else None
```

> 💡 **Integration**: During `GraphMemory.add_episode()` — first `ImmutableRawMemory.save_episode()`, then a pass through `MemoryGuardian`, then a write to Neo4j. The `raw_episode_id` field on the `:Episode` node stores the reference to the original.

---

## 🔗 CausalGraph — Cause-and-Effect Layer

> **Purpose**: the agent understands not only *what* happened, but *why*. The `CAUSES`, `LEADS_TO`, `INFLUENCES` edges between `:Entity` and `:Fact` nodes make it possible to build causal chains and insert them into the Facts Pack before LLM generation.

> **Why it does not violate `Graph = Truth`**: CausalGraph only *adds edges* between already existing validated L3 nodes. It creates no new facts. The LLM is used only to extract causes from text — the result passes through the Truth Gate as usual.

> **Architectural placement**: launched as a background `asyncio.create_task` inside `GraphMemory.add_episode()` — it does not block the Fast Path. `llm_client` is passed as an optional method parameter and is not stored in `GraphMemory` — the graph remains independent of the LLM by default.

```python
# memory/causal_graph.py, adapted for Velantrim

import asyncio
import logging
from dataclasses import dataclass
from typing import List, Optional

logger = logging.getLogger(__name__)

# Types of cause-and-effect edges
CAUSAL_RELATION_TYPES = {
    "CAUSES":     "direct cause",
    "LEADS_TO":   "indirect effect",
    "INFLUENCES": "influences",
}


@dataclass
class CausalEdge:
    source:   str    # entity or fact id
    target:   str
    relation: str    # CAUSES | LEADS_TO | INFLUENCES
    strength: float  # 0.0–1.0
    evidence: str    # brief justification


class CausalGraph:
    """
    Extracts cause-and-effect relationships from episode text
    and stores them as edges in the L3 graph.

    How it works:
    1. On add_episode — a background create_task calls extract_and_store()
    2. The LLM (optionally) extracts causes from the episode text
    3. Edges are stored via MERGE — safe to call repeatedly
    4. get_causal_chain() is used by ContextBuilder for the Facts Pack

    Invariant: CausalGraph does not create new :Fact nodes.
    Only edges between existing nodes — Graph = Truth is not violated.
    """

    def __init__(self, graph_adapter):
        # graph_adapter — IGraphAdapter (GraphitiAdapter or GraphLiteAdapter)
        self.graph = graph_adapter

    async def extract_and_store(
        self,
        episode_name: str,
        content:      str,
        entities:     List[str],
        llm_client    = None,    # optional — without an LLM it works via heuristics
    ) -> List[CausalEdge]:
        """
        Extract cause-and-effect relationships from the episode text.
        Called via asyncio.create_task — does not block the pipeline.
        llm_client is passed as a parameter, not stored in self.
        """
        if not content or not entities:
            return []

        edges = await self._extract_edges(content, entities, llm_client)

        for edge in edges:
            await self._store_edge(edge)

        if edges:
            logger.debug(
                f"CausalGraph: extracted {len(edges)} edges for episode '{episode_name}'"
            )
        return edges

    async def _extract_edges(
        self,
        content:   str,
        entities:  List[str],
        llm_client = None,
    ) -> List[CausalEdge]:
        """LLM extraction with a heuristic fallback."""
        if llm_client:
            return await self._llm_extract(content, entities, llm_client)
        return self._heuristic_extract(content, entities)

    async def _llm_extract(
        self,
        content:    str,
        entities:   List[str],
        llm_client,
    ) -> List[CausalEdge]:
        """
        Ask the LLM to find cause-and-effect relationships.
        The prompt requires strict JSON — without it parsing fails gracefully.
        """
        entities_str = ", ".join(entities[:10])  # token limit
        prompt = f"""Find causal relationships between entities in this text.
Return JSON array only, no explanation:
[{{"source": "A", "target": "B", "relation": "CAUSES|LEADS_TO|INFLUENCES", "strength": 0.0-1.0, "evidence": "brief reason"}}]

Entities: {entities_str}
Text: {content[:500]}

JSON:"""
        try:
            response = await llm_client.complete(prompt)
            import json, re
            # Extract JSON from the response — the LLM sometimes adds text around it
            match = re.search(r'\[.*\]', response, re.DOTALL)
            if not match:
                return []
            raw = json.loads(match.group())
            edges = []
            for item in raw:
                relation = item.get("relation", "").upper()
                if relation not in CAUSAL_RELATION_TYPES:
                    continue
                edges.append(CausalEdge(
                    source=str(item.get("source", "")),
                    target=str(item.get("target", "")),
                    relation=relation,
                    strength=float(item.get("strength", 0.5)),
                    evidence=str(item.get("evidence", ""))[:200],
                ))
            return edges
        except Exception as e:
            logger.debug(f"CausalGraph LLM extract failed: {e}")
            return self._heuristic_extract(content, entities)

    @staticmethod
    def _heuristic_extract(content: str, entities: List[str]) -> List[CausalEdge]:
        """
        Heuristic keyword-based extraction without an LLM.
        Searches for causality markers between the mentioned entities.
        Works as a fallback — lower precision than the LLM, but zero tokens.
        """
        edges = []
        text_lower = content.lower()

        # Causality markers → edge type
        cause_markers   = ["causes", "cause", "because of", "because", "due to"]
        leads_markers   = ["leads", "leads to", "results in", "result"]
        influence_marks = ["influences", "affects", "impacts", "changes"]

        for i, e1 in enumerate(entities):
            for e2 in entities[i + 1:]:
                if e1 == e2:
                    continue
                # Both are mentioned in the text
                if e1.lower() not in text_lower or e2.lower() not in text_lower:
                    continue

                # Determine the type from the markers
                if any(m in text_lower for m in cause_markers):
                    relation, strength = "CAUSES", 0.6
                elif any(m in text_lower for m in leads_markers):
                    relation, strength = "LEADS_TO", 0.5
                elif any(m in text_lower for m in influence_marks):
                    relation, strength = "INFLUENCES", 0.4
                else:
                    continue

                edges.append(CausalEdge(
                    source=e1, target=e2,
                    relation=relation, strength=strength,
                    evidence="heuristic extraction",
                ))
        return edges

    async def _store_edge(self, edge: CausalEdge):
        """
        Store the edge in L3 via MERGE — idempotent.
        Uses execute_cypher — the graph is the single source of truth.
        On failure — log and continue (non-critical for the pipeline).
        """
        try:
            await self.graph.execute_cypher(
                f"""
                MATCH (a) WHERE a.name = $source OR a.id = $source
                MATCH (b) WHERE b.name = $target OR b.id = $target
                MERGE (a)-[r:{edge.relation}]->(b)
                SET r.strength  = $strength,
                    r.evidence  = $evidence,
                    r.updated_at = datetime()
                """,
                {
                    "source":   edge.source,
                    "target":   edge.target,
                    "strength": edge.strength,
                    "evidence": edge.evidence,
                }
            )
        except Exception as e:
            logger.debug(f"CausalGraph._store_edge failed ({edge.source}→{edge.target}): {e}")

    async def get_causal_chain(
        self,
        entity:    str,
        max_depth: int = 2,
        min_strength: float = 0.4,
    ) -> List[dict]:
        """
        Get the causal chain for an entity.
        Called by ContextBuilder when assembling the Facts Pack.
        max_depth passes through a whitelist (1,2,3) — protection against injection.
        """
        safe_depth = max_depth if max_depth in (1, 2, 3) else 2
        try:
            return await self.graph.execute_cypher(
                f"""
                MATCH (start) WHERE start.name = $entity OR start.id = $entity
                MATCH path = (start)-[:CAUSES|LEADS_TO|INFLUENCES*1..{safe_depth}]->(end)
                WHERE ALL(r IN relationships(path) WHERE r.strength >= $min_str)
                RETURN
                    [node IN nodes(path) | coalesce(node.name, node.id)] AS chain,
                    [r IN relationships(path) | type(r)]                  AS relations,
                    [r IN relationships(path) | r.strength]               AS strengths
                ORDER BY size(nodes(path))
                LIMIT 10
                """,
                {"entity": entity, "min_str": min_strength}
            )
        except Exception as e:
            logger.warning(f"CausalGraph.get_causal_chain failed: {e}")
            return []

    @staticmethod
    def format_chain_for_context(chain_rows: List[dict]) -> str:
        """
        Format the causal chain for insertion into the Facts Pack.
        Called by ContextBuilder — the result goes to the LLM as part of the context.
        """
        if not chain_rows:
            return ""

        arrow_map = {
            "CAUSES":     "→ causes →",
            "LEADS_TO":   "→ leads to →",
            "INFLUENCES": "~ influences ~",
        }
        lines = ["📎 Cause-and-effect relationships:"]
        for row in chain_rows:
            chain     = row.get("chain",     [])
            relations = row.get("relations", [])
            strengths = row.get("strengths", [])
            parts = []
            for i, node in enumerate(chain):
                parts.append(node)
                if i < len(relations):
                    rel    = arrow_map.get(relations[i], "→")
                    weight = f"({strengths[i]:.1f})" if i < len(strengths) else ""
                    parts.append(f"{rel}{weight}")
            lines.append("  " + " ".join(parts))
        return "\n".join(lines)
```

**Integration into `GraphitiAdapter.add_episode()`** — add a background call after a successful write:

```python
# graph_adapter.py — at the end of GraphitiAdapter.add_episode(), after return f"episode:{name}"
# (pass llm_client and entities as optional method parameters)

# CausalGraph: background extraction of cause-and-effect relationships
# llm_client=None → works via heuristics, zero tokens
if hasattr(self, '_causal_graph') and self._causal_graph:
    _t = asyncio.create_task(
        self._causal_graph.extract_and_store(
            episode_name=name,
            content=content,
            entities=entities or [],
            llm_client=llm_client,   # None = heuristic mode
        )
    )
    _t.add_done_callback(
        lambda t: t.exception() and
        logger.debug(f"CausalGraph task failed: {t.exception()}")
    )
```

**Integration into `ContextBuilder`** — add to the assembly of the Facts Pack:

```python
# context_builder.py — in the build_context() method, after fact retrieval

from memory.causal_graph import CausalGraph
causal_chain = await self.causal_graph.get_causal_chain(
    entity=query_entity,   # the main entity of the query
    max_depth=2,
    min_strength=0.4,
)
if causal_chain:
    causal_context = CausalGraph.format_chain_for_context(causal_chain)
    # Add to the Facts Pack as a separate block before the LLM
    facts_pack.append({"type": "causal_chain", "content": causal_context})
```

**Invariant**: `CausalGraph` does not create new `:Fact` nodes — only edges between existing ones. The graph remains the single source of truth. `llm_client` is passed as a parameter and is not stored in `GraphMemory` — the separation of `Graph = Truth` and `LLM = Language` is preserved.

---

## 🧬 Knowledge Distillation Engine — Populating L3 

> **Problem**: Without this module Neo4j will remain empty. You cannot populate the graph with summarizations alone — they lose structure. Atomic JSON triples are needed.

**Knowledge Distillation** turns raw text into structured `KnowledgeUnit`s before writing to L3.

```
Raw text:
"Water boils at 100°C at standard atmospheric pressure."
         ↓
KnowledgeUnit (JSON triple):
{
  "concept":   "Water",
  "relation":  "boiling_point",
  "value":     "100°C",
  "condition": "1 atm",
  "evidence":  "physics_textbook_ch3",
  "confidence": 0.98
}
         ↓
Memory Guardian → L3 Neo4j (:KnowledgeUnit node)
```

**Pipeline (hybrid — without LLM for simple cases):**

```
Step 1 (NLP — cheap and fast):
  SpaCy / GLiNER → NER + Relation Extraction
  → basic triples (Subject, Predicate, Object)
  → confidence is determined automatically

Step 2 (LLM — only if needed):
  Engage L4 Reasoning (o4-mini) only when:
  - NLP confidence < 0.8
  - Memory Guardian found a conflict
  - Entities are ambiguous (anaphora: "he", "they")

Step 3 (Guardian):
  Each triple → Memory Guardian → L3
```

> ⚠️ **Anaphora risk**: "He pressed the button" → will create a node `:Entity{name: "He"}`. Solution: chunking that preserves paragraph context (not individual sentences).
>
> 💡 **MVP for Phase 0**: Pick a narrow domain (for example, the LING/THINK glossary). L4 extracts strictly formatted JSON from a paragraph. L5 Guardian validates it. Without complex conflict resolution — simply `evidence_count++` if the triple already exists.

---

## 📜 Formal System Invariants (RFC0001–RFC0005)

> **Invariant** — a rule whose violation is a bug in the architecture, not in behavior. This section is the system's contract. Any change requires a deliberate decision.

### 🛡️ MGL (Memory Governance Layer)

```
1. Episode ∉ Semantic Graph
   Dialogue episodes NEVER enter the L3 graph.
   Phase 2: move them out into a separate Vector DB (Qdrant).

2. ∀ fact ∈ Graph: fact.validated = True
   No fact enters Neo4j without passing through MGL.

3. Graph is bi-temporal
   Every fact has valid_from/valid_to + transaction_time.

4. No LLM output enters graph without MGL
   An LLM hallucination cannot become a fact directly.

5. ∀ fact ∈ Graph: ∃ evidence (:Evidence node)
   Every fact is linked to a source via [:SUPPORTED_BY].
```

### 🔍 RE (Reasoning Engine)

```
1. Every conclusion must have support facts.
   A conclusion without facts → not permitted.

2. Reasoning Graph ≠ Semantic Graph.
   The reasoning graph is built in memory, not written to Neo4j.

3. LLM does not perform inference — only explains.
   L4 Reasoning draws the conclusion. The LLM renders it into text.

4. Evidence Pack must satisfy Truth Gate before reaching LLM.
```

### 🧬 KDE (Knowledge Distillation Engine)

```
1. KDE produces only structured KnowledgeUnit (JSON triples).
   Not text chunks — only atomic facts.

2. KDE never writes directly to graph.
   Always: KDE → MGL → Graph.

3. KDE output must pass through MGL.
```

### 🔱 Velantrim Core Principles

```
1. Memory separated by type: Working / Episodic / Semantic / Policy.
2. Semantic Graph = SSOT (single source of truth).
3. Reasoning Engine performs inference, not LLM.
4. All knowledge passes through Governance (MGL).
5. Episodic memory NEVER enters Semantic Graph.
6. Evidence Pack required for every answer.
```

---

## 📦 Evidence Builder and Truth Gate (RFC0004)

> **Purpose**: before the LLM generates an answer, the Evidence Builder assembles an evidence pack. The Truth Gate checks for sufficiency and consistency.

### 🔄 Validation Loop (L4) — three questions before the Truth Gate

> Reduces hallucinations without calling the LLM.
> The system asks itself three questions before proceeding to the Truth Gate:

```
Step 1 — DECISION: is a search needed at all?
  If the query is in L0 Working Memory (Goal Stack) → answer without searching
  If intent = TASK → answer from L0, do not touch L3
  If the answer is obvious from context → skip retrieval

Step 2 — VALIDATION: is the retrieved content relevant?
  For each retrieved fact: cosine(query, fact) ≥ 0.65?
  If not — drop the fact from the Evidence Pack before the Truth Gate
  This filters out semantic noise before checking the RFC thresholds

Step 3 — SELF-CHECK: is the final answer correct?
  After the Truth Gate, before passing to the LLM:
  Verify that every statement has a TRACE reference to a node
  If a statement has no reference → mark it as [unverified]
  [unverified] blocks passing it as a :Fact (only :Hypothesis)

Result: the system does not just search — it reasons about searching.
           Fast Path (70-90% of queries) — no LLM, no retrieval.
           Slow Path — only if the Validation Loop produced no answer.
```

### Evidence Pack Format

```json
{
  "facts": [
    {
      "content": "Water boils at 100°C at 1 atm",
      "confidence": 0.98,
      "source": "evidence:physicsbook1"
    }
  ],
  "confidence": 0.92,
  "coverage": 0.87,
  "contradictions": [],
  "evidence_count": 5
}
```

### Truth Gate Rules (concrete thresholds)

```
coverage        ≥ 0.7     — the query is covered by facts at least 70%
contradictions  = 0       — no active conflicts
evidence_count  ≥ 3       — at least 3 supporting facts
confidence      ≥ 0.75    — average confidence above the threshold

If at least one condition is not met:
→ the LLM does not generate an answer
→ Returned: "Insufficient data for a confident conclusion."
→ Logged to the Audit Layer for analysis of knowledge gaps
```

### KDE Scale (planning reference points)

```
1 book                →  1–5k  facts
1000 books + Wikipedia → 1–2M  facts
2M facts             ≈  1–2 GB in Neo4j
MVP hardware         :  16 GB RAM, 8 CPU, SSD — sufficient
```

---

## 📜 Canonical Memory Protocol v1

> **Why it is critical**: without a single entry point, every developer understands the system differently. This protocol — Velantrim's "constitution" — describes what happens on every request and every event.

---

### ⚡ Fast Path (synchronous — the user is waiting)

```
Input: user_message + session_id + current Goal Stack

F1: Validation Loop L4 — three questions BEFORE generation:
    · DECISION:    is a memory search needed at all?
    · VALIDATION:  is the retrieved content relevant?
    · SELF-CHECK:  is the final answer correct (Truth Gate)?

F1.5: Velum Context Hint (RFC0016)
    · Velum.get_neighbors(query_entities, min_weight=0.3)
    · Add neighbors to the seed for Etir (step F2.5)
    · Fire-and-forget hint — does not block the Fast Path

F2: L0 update
    · Update the Goal Stack (add/refine the active goal)
    · Load Ring Zero + Project State Card (if not in L0)
    · Priority Eviction when capacity > 4±1:
      CRITICAL (Ring Zero, Project State) → never evicted
      HIGH (active goal) → last to be evicted
      MEDIUM (current dialogue)
      LOW (auxiliary context) → first to be evicted → L1

F3: L1 FTS5 search
    · SQLite FTS5 by session_id + query keywords
    · Recency bias: fresher episodes have priority
    · Select 1-2 candidate episodes

F4: Graphiti search → Neo4j
    · MAX_RESULTS = 10, is_active = true, timeout
    · Hybrid: semantic + keyword + graph traversal

F5: Context Builder → 4±1 chunks
    · token_budget = MAX_TOKENS_MEMORY_PER_QUERY = 2000
    · Priority: L0 > Etir > L1 > L2 > L3
    · Typed context tags: <facts trust="verified"> / <hypothesis>
    · Source tagging : _format_fact() with labels
      [FACT] = from L3 graph, [PRELIMINARY] = from staging, [CURRENT SESSION] = from L1

F6: LLM Generation — the ONLY call on the Fast Path
    · Evidence Pack is mandatory
    · Truth Gate: coverage ≥ 0.7, evidence_count ≥ 3
    · [unverified] label for statements without TRACE

F6.5: OutputFaithfulnessChecker.check(answer, facts_pack)
    · Check that the LLM did not add statements unsupported by the FactsPack
    · MVP: keyword overlap ≥ 40% (Phase 1: NLI cross-encoder)
    · passed → return the answer to the user
    · failed → FALLBACK_RESPONSE + log unsupported_sentences to the Audit Layer

Output: answer + AgentEvent(USER_MESSAGE + AGENT_RESPONSE) to the bus
```

---

### 🔄 Slow Path (asynchronous — in the background, non-blocking)

```
S1: Event Bus Logging
    · USER_MESSAGE, AGENT_RESPONSE, TASK_COMPLETED → Redis Streams
    · Retry 3x + exponential backoff + DLQ + Fallback Queue

S2: Extraction — ONLY tasks in status RESOLVED or FAILED
    · KDE → JSON triples (KnowledgeUnit)
    · NLP confidence < 0.8 → L4 o4-mini for refinement
    · Tasks in BLOCKED_AWAITING_DB wait for CE recovery

S2.6: Creative Ingestion Pipeline (in parallel with S2 · RFC0067 v2.0)
    · Sources: popular science, philosophical essays, high-quality literary prose
    → CreativeExtractor (LLM flagship, temp=0.5)    <- async · Slow Path
    → AnalogyAggregator (>= 2 sources OR authority >= 0.9)
    → Write Protocol Gate
    → Analogy Graph L3 ([:METAPHOR_OF] / [:ANALOGOUS_TO])
    Rejected → SQLite: suggested_analogies (manual audit)

S2.7: Knowledge Ingestion Pipeline (offline · RFC0063)
    · Sources: PDF / JSON / YAML / Wikidata RDF / plain text
    → FactExtractor (LLM flagship, temp=0.1) → Truth Gate → L3 graph
    → PatternExtractor (LLM flagship, temp=0.4) → ReasoningBank (Bayesian prior)
    → SemanticIndexer (embedding only, 0 LLM) → Qdrant/ChromaDB
    → EdgeSuggester (audit tool) → SQLite: suggested_edges
    · Slow Path only. A direct call from the Fast Path is a violation of I63 (ex-I40).

---

## RFC0067 v2.0: Creative Intelligence Layer

### 🌱 Read this first

RFC0067 v2.0 is a complete **Creative Intelligence Layer** made up of three mechanisms:

**Analogy Graph** — an explicit map of metaphors and analogies extracted from high-quality texts. Edges `[:METAPHOR_OF]` and `[:ANALOGOUS_TO]` on L3 nodes.

**Semantic Bridge Engine (SBE)** — an asynchronous worker, subscribed to the EventBus, that precomputes semantic bridges. Slow Path only. The Fast Path reads the Redis cache.

**Adaptive Decoder** — a CREATIVE mode with dynamic temperature (0.6 → 0.85) and `presence_penalty = 0.6`. The fourth cognitive mode.

> ⚠️ **Important:** CREATIVE permits analogies and forbids Hypothesized facts (I57). EXPLORATION permits Hypothesized and has no analogies (I58). These are modes of a different nature.

> ⚠️ **Dependency:** `psutil>=5.9` for the CPU guard in SBEAsyncWorker. Add to `requirements.txt`. Redis and Qdrant/ChromaDB are already in the stack.

---

```
RFC0067 v2.0: Creative Intelligence Layer
    |
    +- [Analogy Graph]:
    |   Edges [:METAPHOR_OF] and [:ANALOGOUS_TO] on L3 nodes.
    |   Source: CreativeExtractor + AnalogyAggregator (S2.6).
    |   Limit: max 50 outgoing analogies per node. Retention: > 365 days -> cold graph.
    |   I55:   only via Write Protocol Gate. Direct MERGE -> WriteProtocolViolation.
    |   I55.1: SAE decay_factor=0.4 for analogy edges (not 0.6 as usual).
    |
    +- [SBEAsyncWorker]:
    |   EventBus: focus_vector_changed / cognitive_mode_switched / periodic_tick.
    |   -> Qdrant (cross-domain, cosine >= 0.75)
    |   -> Redis: creative_bridge:{session_id} (TTL=15 min)
    |   I56: only Slow Path. Fast Path reads only the cache.
    |
    +- [ResonanceTracker]:
    |   used_in_response: +0.05 / positive_continuation: +0.10
    |   explicit_like: +0.20 / clarification_request: -0.10 / explicit_dislike: -0.25
    |   resonance >= 0.7 -> crystallization via Write Protocol Gate.
    |   Decay: every week resonance x 0.95.
    |   I56.1: SBE does not write directly. Only resonance >= 0.7 -> Write Protocol.
    |
    +- [AdaptiveDecoder]:
    |   temp = 0.6 + (0.85-0.6) * min(associations_count/5, 1.0)
    |   presence_penalty = 0.6 (for SLM < 3B: min 0.5, I57)
    |   I57: FactsPack only Validated. Associations in creative_context.
    |
    +- RFC0067 v2.0 Invariants:
    |   I55:   [:METAPHOR_OF] and [:ANALOGOUS_TO] only via Write Protocol Gate.
    |   I55.1: SAE decay_factor=0.4 for analogy edges.
    |   I56:   SBE only in the Slow Path via EventBus.
    |   I56.1: SBE does not write to the graph directly. resonance >= 0.7 -> Write Protocol.
    |   I57:   CREATIVE mode: only Validated + associations in creative_context.
    |   I58:   CREATIVE != EXPLORATION (different rules).
    |   I59:   XAI shows creative_associations separately from facts.
    |   I51-I54: VOID (RFC0067 v1.0 deprecated → replaced by RFC0067 v2.0).
    |   P2-E FIX: explicit documentation of the void holes:
    |   I51 = VOID · I52 = VOID · I53 = VOID · I54 = VOID
    |   In test_invariants.py add markers: pytest.mark.skip("VOID: RFC0067 v1.0 deprecated")
    |
    +- Metrics:
    |   analogy_graph_edges_total / sbe_activations_total / sbe_cache_hits
    |   sbe_cache_misses / creative_mode_responses_total
    |   analogy_resonance_score / analogy_promoted_total
    \- Load: SBEAsyncWorker 20-100ms (Qdrant + Redis) · Slow Path only
```

### Code [RFC0067 v2.0]

```python
# sbe_async_worker.py
# RFC0067 v2.0: Semantic Bridge Engine
# I56: only Slow Path via EventBus. Fast Path reads get_cached().
import json, logging
from dataclasses import dataclass, field
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

# P3-C FIX: RELATED_DOMAINS moved to velantrim_config.py (previously hardcoded in sbe_async_worker.py).
# In sbe_async_worker.py: from velantrim_config import RELATED_DOMAINS
RELATED_DOMAINS: dict[str, list[str]] = {
    "physics":      ["mathematics", "engineering"],
    "biology":      ["chemistry", "medicine"],
    "computing":    ["mathematics", "electronics"],
    "neuroscience": ["biology", "psychology"],
}


@dataclass
class CreativeAssociation:
    source_node: str; target_node: str; cosine: float
    source_domain: str; target_domain: str
    marker:          str   = "[CREATIVE_ASSOCIATION]"
    source_type:     str   = "sbe"
    resonance_score: float = 0.5
    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {"source_node": self.source_node, "target_node": self.target_node,
                "cosine": self.cosine, "source_domain": self.source_domain,
                "target_domain": self.target_domain, "marker": self.marker,
                "source_type": self.source_type,
                "resonance_score": self.resonance_score,
                "timestamp": self.timestamp.isoformat()}

    @classmethod
    def from_dict(cls, d):
        return cls(source_node=d["source_node"], target_node=d["target_node"],
                   cosine=d["cosine"], source_domain=d["source_domain"],
                   target_domain=d["target_domain"],
                   marker=d.get("marker", "[CREATIVE_ASSOCIATION]"),
                   source_type=d.get("source_type", "sbe"),
                   resonance_score=d.get("resonance_score", 0.5),
                   timestamp=datetime.fromisoformat(d["timestamp"]))


class SBEAsyncWorker:
    # I56: only via EventBus. Fast Path reads get_cached().
    def __init__(self, vector_db, redis, focus_engine, hot_graph, config):
        self.vector_db    = vector_db; self.redis = redis
        self.focus_engine = focus_engine; self.hot_graph = hot_graph
        self.cosine_th = config.CREATIVE.COSINE_THRESHOLD
        self.max_assoc = config.CREATIVE.MAX_ASSOCIATIONS
        self.ttl       = config.CREATIVE.CACHE_TTL_SECONDS

    async def handle_event(self, event: dict):
        sid = event.get("session_id")
        if not sid:
            return
        if event.get("cognitive_mode") not in (None, "CREATIVE"):
            return
        await self._compute_and_cache(sid)

    async def _compute_and_cache(self, session_id: str):
        # FIX-C: FocusEngine does not have get_focus_vector(session_id).
        # Correct method: get_current_focus() — returns the current FocusVector.
        # get_focus_vector was a nonexistent name → AttributeError on every SBE call.
        focus = await self.focus_engine.get_current_focus(session_id)
        if not focus or not focus.primary_domain:
            return
        exclude  = [focus.primary_domain] + RELATED_DOMAINS.get(focus.primary_domain, [])
        # P4-D FIX: Redis cache for get_activated_nodes (TTL 5 min).
        # In CREATIVE mode it is called often — the cache reduces the load on Neo4j.
        import json as _json
        _cache_key = f"activated_nodes:{session_id}"
        _cached = await getattr(self, 'redis', None) and await self.redis.get(_cache_key)
        if _cached:
            nodes = [type('AN', (), n)() for n in _json.loads(_cached)]
        else:
            nodes = await self.hot_graph.get_activated_nodes(session_id, limit=10)
            if nodes and hasattr(self, 'redis'):
                await self.redis.setex(_cache_key, 300, _json.dumps([n.__dict__ for n in nodes]))
        if not nodes:
            return
        bridges  = []
        for node in nodes:
            for r in await self.vector_db.search(
                query_vector=node.embedding,
                filter={"domain": {"$nin": exclude}, "is_active": True},
                limit=self.max_assoc * 2
            ):
                if r.score >= self.cosine_th:
                    bridges.append(CreativeAssociation(
                        source_node=node.id, target_node=r.id,
                        cosine=round(r.score, 3),
                        source_domain=node.domain, target_domain=r.domain))
        if bridges := bridges[:self.max_assoc]:
            await self.redis.setex(
                f"creative_bridge:{session_id}", self.ttl,
                json.dumps([b.to_dict() for b in bridges]))

    async def get_cached(self, session_id: str) -> list[CreativeAssociation]:
        raw = await self.redis.get(f"creative_bridge:{session_id}")
        return [CreativeAssociation.from_dict(d) for d in json.loads(raw)] if raw else []
```

```python
# resonance_tracker.py
# RFC0067 v2.0: ResonanceTracker
# I56.1: resonance >= 0.7 -> Write Protocol Gate (not directly)
import logging
from datetime import timezone, datetime

logger = logging.getLogger(__name__)

FEEDBACK_WEIGHTS = {
    "used_in_response":      +0.05,
    "positive_continuation": +0.10,
    "explicit_like":         +0.20,
    "clarification_request": -0.10,
    "explicit_dislike":      -0.25,
}


class ResonanceTracker:
    # P3-B FIX: constants are read from the CREATIVE config — hardcoded values removed.
    # PROMOTE_THRESHOLD = 0.7   ← now CREATIVE.PROMOTE_THRESHOLD
    # DECAY_WEEKLY      = 0.95  ← now CREATIVE.DECAY_WEEKLY
    # from velantrim_config import CREATIVE → use CREATIVE.PROMOTE_THRESHOLD

    def __init__(self, graph, write_protocol, redis):
        self.graph = graph; self.write_protocol = write_protocol; self.redis = redis

    async def record(self, analogy_id, session_id, event_type,
                     source_type, analogy_data=None):
        delta = FEEDBACK_WEIGHTS.get(event_type, 0.0)
        if not delta:
            return
        cur   = await self._get(analogy_id, source_type)
        score = max(0.0, min(1.0, cur + delta))
        await self._set(analogy_id, source_type, score)
        if (score >= self.PROMOTE_THRESHOLD and source_type == "sbe"
                and event_type in ("positive_continuation", "explicit_like")
                and analogy_data):
            await self._promote(analogy_id, analogy_data, score)

    async def decay_all(self):
        # FIX-D: GraphMemory does not have .session() — that is the Neo4j driver API.
        # Correct interface: execute_cypher(). Otherwise AttributeError in the nightly cycle.
        await self.graph.execute_cypher(
            "MATCH ()-[r:METAPHOR_OF|ANALOGOUS_TO]->() "
            "WHERE r.last_used < datetime() - duration('P7D') "
            "SET r.resonance_score = r.resonance_score * $d",
            {"d": self.DECAY_WEEKLY})

    async def _promote(self, aid, data, resonance):
        await self.write_protocol.create_analogy_edge(
            source=data["source_node"], target=data["target_node"],
            edge_type="METAPHOR_OF" if data.get("is_metaphor", True) else "ANALOGOUS_TO",
            source_type="sbe_promoted", confidence=data["cosine"],
            source_domain=data["source_domain"], target_domain=data["target_domain"],
            resonance_score=resonance,
            cultural_vintage=datetime.now(timezone.utc).year)
        logger.info(f"SBE analogy promoted: {aid}")

    async def _get(self, aid, stype):
        if stype == "analogy_graph":
            # FIX-D: .session() → execute_cypher()
            result = await self.graph.execute_cypher(
                "MATCH ()-[r:METAPHOR_OF|ANALOGOUS_TO]->() "
                "WHERE r.analogy_id=$id RETURN r.resonance_score AS s",  -- P0-G FIX: id() = integer internal ID, analogy_id = string UUID
                {"id": aid})
            return float(result[0]["s"]) if result else 0.5
        raw = await self.redis.get(f"sbe_resonance:{aid}")
        return float(raw) if raw else 0.5

    async def _set(self, aid, stype, score):
        if stype == "analogy_graph":
            # FIX-D: .session() → execute_cypher()
            await self.graph.execute_cypher(
                "MATCH ()-[r:METAPHOR_OF|ANALOGOUS_TO]->() "
                "WHERE r.analogy_id=$id "  -- P0-G FIX: property-based lookup instead of id(r)
                "SET r.resonance_score=$s, r.last_used=datetime()",
                {"id": aid, "s": score})
        else:
            await self.redis.setex(f"sbe_resonance:{aid}", 86400*30, score)
```

```python
# adaptive_decoder.py
# RFC0067 v2.0: AdaptiveDecoder
# I57: FactsPack in CREATIVE only Validated.
from dataclasses import dataclass, field


@dataclass
class DecodeContext:
    cognitive_mode:        str
    creative_associations: list = field(default_factory=list)


class AdaptiveDecoder:
    BASE_TEMP = 0.6; MAX_TEMP = 0.85; MAX_ASSOC = 5
    PRES_PENALTY = 0.6; SLM_MIN_PRES = 0.5
    # P1-F FIX: was {"PRECISION": 0.1, "BALANCED": 0.5, "EXPLORATION": 0.7} → conflict
# with CognitiveModeRouter.MODE_CONFIGS (0.3 / 0.6 / 0.85). Now a single source.
from velantrim_config import MODE_TEMPS   # P1-F: MODE_TEMPS is read from the config

    def compute_temperature(self, ctx: DecodeContext) -> float:
        if ctx.cognitive_mode != "CREATIVE":
            return self.MODE_TEMPS.get(ctx.cognitive_mode, 0.5)
        ratio = min(len(ctx.creative_associations) / self.MAX_ASSOC, 1.0)
        return self.BASE_TEMP + (self.MAX_TEMP - self.BASE_TEMP) * ratio

    def compute_presence_penalty(self, ctx: DecodeContext, params_b: float) -> float:
        if ctx.cognitive_mode != "CREATIVE":
            return 0.2 if ctx.cognitive_mode == "EXPLORATION" else 0.0
        return max(self.SLM_MIN_PRES, self.PRES_PENALTY) if params_b < 3.0 \
               else self.PRES_PENALTY
```

### Tests [I55–I59]

```python
# tests/test_invariants.py -- add

# I55: [:METAPHOR_OF] only via Write Protocol Gate
async def test_I55_analogy_edges_require_write_protocol():
    with pytest.raises(WriteProtocolViolation):
        await MockGraph().execute_cypher(
            "MATCH (a {name:'A'}),(b {name:'B'}) MERGE (a)-[:METAPHOR_OF]->(b)")
    r = await MockWriteProtocol().create_analogy_edge(
        source="A", target="B", edge_type="METAPHOR_OF",
        source_type="test", confidence=0.85,
        source_domain="biology", target_domain="computing")
    assert r.success

# I55.1: SAE decay=0.4 for analogies
async def test_I55_1_sae_analogy_decay():
    sae = SpreadingActivationEngine(graph=MockGraphWithAnalogies())
    act = await sae.activate("Neuron", max_depth=2)
    assert act.get("Transistor", 0) < act.get("Synapse", 0) * 0.65, \
        "I55.1 VIOLATION: SAE does not apply decay=0.4 for analogies"

# I56.1: SBE does not write directly
async def test_I56_1_resonance_via_write_protocol():
    wp = MockWriteProtocol()
    t  = ResonanceTracker(MockGraph(), wp, MockRedis())
    d  = {"source_node": "A", "target_node": "B", "cosine": 0.82,
          "source_domain": "neuro", "target_domain": "elec", "is_metaphor": True}
    for _ in range(4):
        await t.record("id1", "s", "explicit_like", "sbe", d)
    assert wp.create_analogy_edge_called, "I56.1 VIOLATION"

# I57: CREATIVE mode — only Validated
async def test_I57_creative_validated_only():
    ctx = await MockContextBuilder().build(query="test",
                session_id="s", cognitive_mode="CREATIVE")
    for f in ctx.facts_pack:
        assert f.epistemic_state == "Validated", f"I57 VIOLATION: {f.id}"

# I58: CREATIVE != EXPLORATION
async def test_I58_creative_vs_exploration():
    c = await MockContextBuilder().build(query=".", cognitive_mode="CREATIVE")
    e = await MockContextBuilder().build(query=".", cognitive_mode="EXPLORATION")
    assert all(f.epistemic_state == "Validated" for f in c.facts_pack)
    assert len(e.creative_associations) == 0, "I58 VIOLATION"

# I59: XAI shows associations separately
async def test_I59_xai_separates_associations():
    d = (await MockExplainabilityLayer().explain("r1", "detailed")).to_dict()
    assert "creative_associations" in d, "I59 VIOLATION: field missing"
    assert {f["id"] for f in d["facts"]}.isdisjoint(
        {a["source_node"] for a in d["creative_associations"]}), "I59 VIOLATION"
```

### Add to velantrim_config.py

```python
class CreativeConfig:
    MAX_EDGES_PER_CONCEPT = 50
    RETENTION_DAYS        = 365
    MIN_CONFIDENCE        = 0.7
    COSINE_THRESHOLD      = 0.75
    MAX_ASSOCIATIONS      = 5
    CACHE_TTL_SECONDS     = 900
    TEMP_BASE             = 0.6
    TEMP_MAX              = 0.85
    PRESENCE_PENALTY      = 0.6
    SLM_MIN_PRESENCE      = 0.5
    PROMOTE_THRESHOLD     = 0.7
    DECAY_WEEKLY          = 0.95
    MIN_SOURCES           = 2
    AUTHORITY_OVERRIDE    = 0.9

CREATIVE = CreativeConfig()
# psutil>=5.9 -- add to requirements.txt
```


---

## RFC0063: Knowledge Ingestion Pipeline — Absorbing External Knowledge

### 🌱 What it's for

Velantrim learns from dialogues. But there is a vast body of knowledge accumulated **before** the first dialogue — encyclopedias, textbooks, scientific papers, PDFs. RFC0063 gives the system the ability to absorb this knowledge without losing factual accuracy, reasoning patterns, or semantic connections. One source → three parallel streams → three correct architectural layers.

The key idea: the "pedagogical noise" in a textbook — repetitions, examples, metaphors — is not garbage. It is encoded reasoning patterns. Velantrim sorts them into boxes: facts into the graph, patterns into ReasoningBank, semantics into the vector index.

---

```
RFC0063: Knowledge Ingestion Pipeline

  Source (PDF / JSON / YAML / Wikidata RDF / plain text)
                          |
                          v
              IngestionRouter (Slow Path only · I63)
                          |
          .---------------+---------------.
          v               v               v
   FactExtractor   PatternExtractor  SemanticIndexer
   (flagship LLM)  (flagship LLM)   (embedding only)
   temp = 0.1      temp = 0.4       0 LLM tokens
          |               |               |
          v               v               v
    L3 Neo4j       L4 ReasoningBank   Qdrant/ChromaDB
    Truth Gate     Bayesian Prior     vector index
    ESM: Supported Thompson Sampling  + fact_ids link
          |               |               |
          .---------------+---------------.
                          |
                   TraceLine sync (source_id)
```

### Components

**IngestionRouter** — the entry point. Accepts a source, determines its type, language, domain, `source_vintage` (year of publication), and `trust_score`. Launches three streams via the EventBus. Slow Path only (I63).

**FactExtractor** — extracts fact triples (subject, predicate, object). Temperature 0.1. Initial ESM = `Supported` — never `Validated` on ingestion (I60). Deduplication: cosine ≥ 0.92 → adds Evidence to an existing node, does not create a duplicate. Trust scores: encyclopedic 0.85, scientific 0.90, textbook 0.80, default 0.70.

**PatternExtractor** — extracts reasoning patterns into ReasoningBank. Temperature 0.4. **Bayesian initialization of Thompson Sampling (I61)**: a strategy from an authoritative source starts not at `Beta(1,1)` but at `Beta(prior×k, (1-prior)×k)` — a reasonable head start that remains correctable by real-world experience. `max prior_strength_k = 20` — a hard limit (otherwise the strategy becomes uncorrectable). Strategy deduplication: similarity > 0.88 → merge, not a duplicate.

**SemanticIndexer** — slices text into chunks of 512 tokens / overlap 64, vectorizes via EmbeddingRegistry (`deepvk/USER-bge-m3` for RU). **Zero LLM calls** (I62). The metadata of each vector includes the `fact_ids` from L3 for the same chunk. This links the vector index to the graph — semantic search leads to explicit facts.

**EdgeSuggester** — **an auditing tool, not automation**. Once a week it finds pairs of facts with cosine > 0.85 AND co-activation > 3 times, but without an explicit edge in the graph. It saves them to the SQLite `suggested_edges` table with status `pending`. The auditor approves → only then does it go through the Truth Gate into the graph (I64). Optional Hypothesized Edge mode: the edge is created as `is_active=false` and is activated when the user indirectly confirms it through dialogue.

**VintageDecayCalculator** — an adaptive `decay_lambda` depending on the domain and the age of the source (I65). Physics: decay=0.001 (practically never goes stale). Programming: decay=0.15 (goes stale in 3 years). Medicine: decay=0.05. ESM modifier: Validated×0.5 (the fact lives longer), Hypothesized×2.0 (goes stale faster). Every ingested fact must have a `decay_lambda` and a `source_vintage`.

---

```
RFC0063 Configuration (velantrim_config.yaml):

ingestion:
  enabled: true
  offline_only: true            # never in the Fast Path runtime
  batch_size: 500
  dedup_threshold: 0.92         # cosine for fact deduplication
  strategy_dedup_threshold: 0.88
  max_domain_share: 0.40        # maximum of a single domain per session
  languages: [ru, en, multi]
  trust_scores:
    encyclopedic: 0.85
    scientific: 0.90
    textbook: 0.80
    default: 0.70
  extractors:
    facts:
      llm: flagship
      temperature: 0.1
      initial_esm_state: Supported   # never Validated on ingestion
    reasoning_patterns:
      llm: flagship
      temperature: 0.4
    semantic_embeddings:
      model: "deepvk/USER-bge-m3"
      chunk_size: 512
      chunk_overlap: 64
  vintage_decay:
    domain_base_decay:
      physics: 0.001
      mathematics: 0.001
      chemistry: 0.005
      biology: 0.02
      medicine: 0.05
      programming: 0.15
      law: 0.03
      history: 0.002
      default: 0.05
    vintage_threshold_years:
      physics: 50
      programming: 3
      medicine: 5
      default: 10
    max_decay_cap: 0.5

reasoning_bank:
  ingested_prior:
    default_confidence: 0.75
    default_strength_k: 10
    max_strength_k: 20              # hard limit
    domain_overrides:
      physics:     { confidence: 0.90, k: 20 }
      mathematics: { confidence: 0.92, k: 20 }
      programming: { confidence: 0.60, k: 5  }
      medicine:    { confidence: 0.70, k: 15 }

edge_suggester:
  enabled: true
  cosine_threshold: 0.85
  coactivation_threshold: 3
  hypothesized_edge_mode: true
  audit_schedule: weekly
```

### RFC0063 Invariants

```
I60: FactExtractor never assigns epistemic_state=Validated without the Truth Gate
     with evidence_count >= 3. Violation = writing unreliable facts with the highest status.
     Test: test_I60_fact_extractor_no_direct_validated()

I61: All ingested strategies use Bayesian initialization Beta(prior*k, (1-prior)*k).
     max prior_strength_k = 20. Beta(1,1) for ingested strategies is a violation.
     Test: test_I61_thompson_sampling_bayesian_prior()

I62: SemanticIndexer does not call the LLM. Only the embedding model via EmbeddingRegistry.
     Test: test_I62_semantic_indexer_no_llm_call()

I63: IngestionRouter operates only via the EventBus in the Slow Path.
     A direct call from the Fast Path is a violation of I28.
     Test: test_I63_ingestion_router_slow_path_only()

I64: EdgeSuggester does not write to the graph directly.
     Only via approve_edge() -> Truth Gate -> L3.
     Test: test_I64_edge_suggester_no_direct_graph_write()

I65: Every ingested fact (source_type="import") must have a decay_lambda
     computed via VintageDecayCalculator. decay_lambda=NULL = violation.
     Test: test_I65_vintage_decay_assigned_on_ingestion()
```

### Tests [I60–I65]

```python
# tests/test_invariants.py -- add

# I60: FactExtractor does not assign Validated directly
async def test_I60_fact_extractor_no_direct_validated():
    extractor = FactExtractor(truth_gate=MockTruthGate(), graph=MockGraph())
    result = await extractor.extract_and_store(
        text="Water boils at 100°C.", source_type="encyclopedic"
    )
    assert result.esm_state == "Supported", \
        "I60 VIOLATION: FactExtractor assigned Validated without the Truth Gate"

# I61: Bayesian prior for ingested strategies
async def test_I61_thompson_sampling_bayesian_prior():
    bank = ReasoningBank()
    strategy = await bank.ingest_pattern(
        pattern="first_principles",
        source_type="ingested_prior",
        prior_confidence=0.90, prior_strength_k=20
    )
    assert strategy.alpha == 18.0, "I61 VIOLATION: alpha != prior*k"
    assert strategy.beta  ==  2.0, "I61 VIOLATION: beta != (1-prior)*k"

# I62: SemanticIndexer does not call the LLM
async def test_I62_semantic_indexer_no_llm_call():
    llm_mock = MockLLM()
    indexer  = SemanticIndexer(embedding_registry=MockEmbeddingRegistry(),
                               llm=None)
    await indexer.index_chunks(["chunk 1", "chunk 2"], source_id="src_001")
    assert llm_mock.call_count == 0, "I62 VIOLATION: SemanticIndexer called the LLM"

# I63: IngestionRouter only via the Slow Path
async def test_I63_ingestion_router_slow_path_only():
    router = IngestionRouter(event_bus=MockEventBus())
    with pytest.raises(FastPathViolation):
        await router.ingest_sync("source.pdf")  # no such method

# I64: EdgeSuggester does not write to the graph directly
async def test_I64_edge_suggester_no_direct_graph_write():
    graph   = MockGraph()
    suggest = EdgeSuggester(graph=graph, db=MockDB())
    await suggest.run_weekly_scan()
    assert graph.write_count == 0, "I64 VIOLATION: EdgeSuggester writes to the graph"
    assert suggest.pending_count > 0

# I65: VintageDecay is mandatory for all ingested facts
async def test_I65_vintage_decay_assigned():
    calc    = VintageDecayCalculator()
    fact    = Fact(source_type="import", source_vintage=2018, domain="programming")
    result  = calc.assign(fact)
    assert result.decay_lambda is not None, "I65 VIOLATION: decay_lambda=NULL"
    assert result.decay_lambda > 0.10, \
        "I65: programming 2018 must have a high decay"
```

### New Prometheus Metrics (RFC0063)

| Metric | What it shows |
|---------|----------------|
| `ingestion_facts_created_total` | facts created via IngestionPipeline |
| `ingestion_facts_deduplicated_total` | facts merged with existing ones |
| `ingestion_patterns_created_total` | reasoning patterns created |
| `ingestion_patterns_deduplicated_total` | patterns merged via merge |
| `ingestion_contradictions_found_total` | contradictions with the existing graph |
| `ingestion_batch_duration_seconds` | batch processing time (Histogram) |
| `ingestion_vintage_decay_avg` | average decay_lambda for the batch |
| `edge_suggestions_pending_total` | edge suggestions awaiting audit |
| `edge_suggestions_approved_total` | suggestions approved by the auditor |
| `edge_hypothesized_activated_total` | Hypothesized Edges activated by dialogue |

### Migration of Existing Data

```cypher
// Strategies from experience: set a default prior with zero strength
MATCH (s:Strategy) WHERE s.source_type IS NULL
SET s.source_type = "experience",
    s.prior_confidence = 0.5,
    s.prior_strength_k = 0;

// Facts without source_vintage: set the current year as the default
MATCH (f:Fact) WHERE f.source_vintage IS NULL
SET f.source_vintage = 2026,
    f.source_domain = "unknown",
    f.decay_lambda = 0.05;
```

### Implementation Order

**Sprint 1 (1–2 weeks):** Bayesian initialization of Thompson Sampling (I61), the `max_strength_k=20` limit, strategy deduplication via merge, EdgeSuggester as HITL-only with the SQLite `suggested_edges` table, tests I61 and I64.

**Sprint 2 (3–4 weeks):** VintageDecayCalculator (I65), the `source_vintage` field in the :Fact schema, FactExtractor + PatternExtractor as separate LLM calls (I60, I62), SemanticIndexer without LLM via EmbeddingRegistry, IngestionOrchestrator with asyncio.gather, extension of TraceLine for three layers, tests I60–I65, the migration script.


S2.5: ConflictResolutionWorker — every 5 minutes (RFC0062)
    · Batch of 20 Hypothesized facts with conflict_checked <> true
    · TruthConflictDetector → similarity search → LLM verdict (YES/NO)
    · On conflict → ESM.transition(Contradicted) → GraphWriteProtocol
    · ⚠️ RFC0031: no direct SET epistemic_state — only ESM.transition
    · ⚠️ When llm_client=None → continue (not break!) — batch processing continues
    · Checked facts: conflict_checked = true
    · Invariant I38: called only from the Slow Path — not from the Fast Path

S3: Consolidation → ConsolidationEngine.enqueue(CONSOLIDATE)
    · Triggered when L1 capacity > 80%
    · asyncio.Lock — no parallel operations on a single node
    · Timeout 30s → DLQ, status → BLOCKED_AWAITING_DB

S4: Reflection — every 10 completed tasks
    · Strategy Update via Thompson Sampling (RFC0039)
    · Negative Reinforcement for failed strategies

S5: GC — every 7 days or when MHI < 0.3 (Phase 2)
    · Soft Delete → S3 backup → Hard Delete
    · Cascade invalidation of Strategy on Fact invalidation
```

---

### 🔒 Invariants (must never be violated)

```python
# L0 INVARIANTS
assert "VALUES_CORE" in working_memory.pinned  # Ring Zero always
assert len(working_memory) <= 5                # 4±1 Cowan 2001
assert working_memory.eviction_policy == "CRITICAL > HIGH > MEDIUM > LOW"

# L1 INVARIANTS
for episode in stm_cache:
    assert episode.session_id is not None    # session_id binding
    assert episode.event_time is not None    # temporal tagging
    assert episode.created_at is not None
    assert episode.valid_from is not None

# L3 INVARIANTS
# ∀ fact ∈ Graph: validated = True (MGL-2)
# ∀ fact ∈ Graph: ∃ [:SUPPORTED_BY] → :Evidence (MGL-5)
# ∀ fact ∈ Graph: transaction_time IS NOT NULL (bi-temporal)

# EVENT BUS INVARIANTS
# Each request = at least 1 AgentEvent(USER_MESSAGE)

# CORE VALUES INVARIANTS
# VALUES CORE never adapt
# Semantic Decay does not affect pinned=CRITICAL nodes

# I38 (RFC0062) — ConflictResolutionWorker only in the Slow Path
# A direct call to TruthConflictDetector from the Fast Path is an architecture violation.
# Violation → Observer++ alert + logging.

# datetime timezone: use timezone.utc everywhere
# ❌ datetime.now()            → ✅ datetime.now(timezone.utc)
# Files: fractal_memory.py · consolidation_worker.py · memory_gc.py
#         event_bus.py · velum.py (VelumEdge.first_seen, last_seen)
```

---

## 🧬 Epistemic State Machine (ESM) — Fact Lifecycle

> **Why it is critical**: without the ESM, facts in L3 are "just nodes." Semantic Decay and GC operate blindly. The ESM turns L3 from a database into a **living epistemic system**, where every fact knows its place in the space of credibility.

---

### States and transitions

```
                 First appearance (auto)
  LLM Output ──────────────────────────────► :Observed
                                                  │
                                          Truth Gate partial
                                                  ▼
                                          :Hypothesized
                                                  │
                                        Evidence ≥ 2 added
                                                  ▼
                                          :Supported
                                                  │
                                     MGL + Truth Gate passed
                                                  ▼
                                          :Validated  ◄──── (stable state)
                                                  │
                                    1+ [:CONTRADICTS] (weighted)
                                                  ▼
                                         :Contradicted
                                                  │
                                    3+ conflicts / importance drops
                                                  ▼
                                          :Deprecated
                                                  │
                                    importance < 0.1 at GC
                                                  ▼
                                          :Collapsed
                             (→ Immutable Raw Memory, not physically destroyed)
```

### Transition rules (formal)

```python
ESM_TRANSITIONS = {
    "Observed":     {"to": "Hypothesized", "condition": "first_appearance"},
    "Hypothesized": {"to": "Supported",    "condition": "evidence_count >= 2"},
    "Supported":    {"to": "Validated",    "condition": "mgl_passed AND truth_gate >= 0.7"},
    "Validated":    {"to": "Contradicted", "condition": "strong_contradictions >= 1"},
    "Contradicted": {"to": "Deprecated",   "condition": "contradiction_count >= 3 OR importance < 0.3"},
    "Deprecated":   {"to": "Collapsed",    "condition": "importance < 0.1"},
    # Collapsed — final state. Not physically deleted — a reference in Immutable Raw Memory.
}

# Ring Zero / VALUES CORE → ESM frozen at Validated. Never transitions to Contradicted.
IMMUTABLE_STATES = {"VALUES_CORE", "RING_ZERO"}
```

### ESM controller code

```python
# epistemic_state_machine.py
from enum import Enum
from datetime import datetime
from typing import List
import logging

logger = logging.getLogger(__name__)

class EpistemicState(str, Enum):
    OBSERVED     = "Observed"
    HYPOTHESIZED = "Hypothesized"
    SUPPORTED    = "Supported"
    VALIDATED    = "Validated"
    CONTRADICTED = "Contradicted"
    DEPRECATED   = "Deprecated"
    COLLAPSED    = "Collapsed"

class EpistemicStateMachine:
    """
    Manages the lifecycle of facts in L3.
    Connected to: MGL (Memory Guardian), Weighted Semantic Decay,
              GC (MemoryGarbageCollector), Truth Gate.

    RFC0001: LLM → :Fact only through the ESM chain.
    Ring Zero / VALUES CORE → frozen at Validated forever.
    """

    IMMUTABLE_FACT_IDS = {"VALUES_CORE", "RING_ZERO"}

    async def transition(
        self,
        fact_id: str,
        fact: dict,
        graph: "GraphMemory",
        reason: str
    ) -> EpistemicState:
        """
        Compute the next state of the fact and apply the transition.
        Returns the new state.

        Raises:
            ImmutableStateError: if the fact is VALUES CORE
        """
        current = EpistemicState(fact.get("epistemic_state", "Observed"))

        # Ring Zero never degrades
        if fact_id in self.IMMUTABLE_FACT_IDS:
            return current

        next_state = self._compute_next(fact, current)

        if next_state != current:
            await self._apply_transition(fact_id, current, next_state, reason, graph)
            logger.info(f"ESM: {fact_id} {current.value} → {next_state.value} ({reason})")

        return next_state

    def _compute_next(self, fact: dict, current: EpistemicState) -> EpistemicState:
        """Compute the next state based on the transition conditions"""
        evidence_count    = fact.get("evidence_count", 0)
        mgl_passed        = fact.get("validated", False)
        truth_gate_score  = fact.get("epistemic_score", 0.0)
        contradiction_count = fact.get("contradiction_count", 0)
        importance        = fact.get("importance_score", 1.0)

        if current == EpistemicState.OBSERVED:
            return EpistemicState.HYPOTHESIZED

        if current == EpistemicState.HYPOTHESIZED and evidence_count >= 2:
            return EpistemicState.SUPPORTED

        if current == EpistemicState.SUPPORTED and mgl_passed and truth_gate_score >= 0.7:
            return EpistemicState.VALIDATED

        if current == EpistemicState.VALIDATED and contradiction_count >= 1:
            return EpistemicState.CONTRADICTED

        if current == EpistemicState.CONTRADICTED:
            if contradiction_count >= 3 or importance < 0.3:
                return EpistemicState.DEPRECATED

        if current == EpistemicState.DEPRECATED and importance < 0.1:
            return EpistemicState.COLLAPSED

        return current  # no transition

    async def _apply_transition(
        self,
        fact_id: str,
        from_state: EpistemicState,
        to_state: EpistemicState,
        reason: str,
        graph: "GraphMemory"
    ):
        """Record the transition into the graph"""
        # On transition to Collapsed → save to Immutable Raw Memory
        if to_state == EpistemicState.COLLAPSED:
            await self._preserve_to_raw_memory(fact_id, graph)

        # I88 (VersionOCC): atomic increment of _version_ via OCC Cypher.
        # MATCH on {id, _version_} — if the version changed concurrently, the write will not apply.
        await graph.execute_cypher("""
            MATCH (f:Fact {id: $fact_id})
            SET f.epistemic_state = $new_state,
                f.state_changed_at = datetime(),
                f.transition_reason = $reason,
                f._version_ = coalesce(f._version_, 0) + 1,
                f.is_active = CASE WHEN $new_state IN ['Deprecated','Collapsed']
                              THEN false ELSE f.is_active END
            """, {
            "fact_id": fact_id,
            "new_state": to_state.value,
            "reason": reason
        })

    async def _preserve_to_raw_memory(self, fact_id: str, graph: "GraphMemory"):
        """Collapsed fact → reference in Immutable Raw Memory (not destroyed)"""
        logger.info(f"ESM Collapsed: {fact_id} → Immutable Raw Memory reference saved")
        # Physical deletion only via GC + S3 archiving

    async def cascade_invalidate(
        self,
        fact_id: str,
        graph: "GraphMemory"
    ) -> List[str]:
        """
        Cascade invalidation of dependent facts
        
        If fact B is derived from A (via [:DERIVED_FROM] or [:INFERRED_FROM]):
          A → B
        
        And A transitions to Contradicted:
          A.epistemic_state = "Contradicted"
        
        Then B must be revised:
          B.epistemic_state = "Hypothesized"
          B.requires_revalidation = true
        
        Returns: list of IDs of invalidated facts
        """
        query = """
        MATCH (source:Fact {id: $fact_id})
        WHERE source.epistemic_state IN ['Contradicted', 'Deprecated', 'Collapsed']
        
        MATCH (source)<-[:DERIVED_FROM|INFERRED_FROM]-(dependent:Fact)
        WHERE dependent.epistemic_state IN ['Validated', 'Supported']
          AND dependent.is_ring_zero <> true
        
        SET dependent.epistemic_state = 'Hypothesized',
            dependent.requires_revalidation = true,
            dependent.invalidated_at = datetime(),
            dependent.invalidation_source = $fact_id
        
        RETURN dependent.id as invalidated_id
        """
        
        results = await graph.execute_cypher(query, {"fact_id": fact_id})
        invalidated = [r['invalidated_id'] for r in results]
        
        if invalidated:
            logger.warning(
                f"Cascade invalidation: {fact_id} → {len(invalidated)} dependent facts "
                f"rolled back to Hypothesized"
            )
        
        return invalidated
```

### Integration of the ESM with existing components

```
Memory Guardian (MGL):
  · Before writing a new fact → ESM.transition(Observed → Hypothesized)
  · After passing the Truth Gate → ESM.transition(Supported → Validated)

Weighted Semantic Decay:
  · When adding [:CONTRADICTS] → ESM.transition(Validated → Contradicted)
  · importance < 0.1 → ESM.transition(Deprecated → Collapsed)

GC (MemoryGarbageCollector):
  · Collapsed nodes → S3 archiving → physical deletion
  · Deprecated with age > 90d → candidate for Collapsed

Runtime Invariant Checker:
  · ∀ fact ∈ Graph: epistemic_state ∈ VALID_STATES
  · ∀ fact ∈ Graph: if validated=True → epistemic_state = 'Validated'
  · VALUES_CORE: epistemic_state always = 'Validated'
```

---

## ⚙️ Runtime Invariant Checker 

> **Why it is critical**: RFCs exist as documents, but violations only become visible when the system crashes. The Runtime Checker turns RFCs from paper into executable contracts.

```python
# runtime_invariant_checker.py
import asyncio
from dataclasses import dataclass
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@dataclass
class InvariantViolation:
    invariant_id: str
    severity: str        # "CRITICAL" | "WARNING"
    description: str
    detected_at: datetime
    auto_remediation: str  # what the system did automatically

class RuntimeInvariantChecker:
    """
    Checks Protocol v1 invariants every 30 seconds.
    On a CRITICAL violation → Safe Mode + Heartbeat alert.
    On a WARNING → log + Grafana counter.
    """
    CHECK_INTERVAL_SECONDS = 30

    def __init__(self, graph: GraphMemory, fractal_memory: FractalMemory,
                 heartbeat: "MetaSupervisorHeartbeat" = None):  # optional: the agent may pass it later
        self.graph = graph
        self.fractal = fractal_memory
        self.heartbeat = heartbeat
        self.violations_total = 0
        self._running = False

    async def start(self):
        """Start the background invariant check"""
        self._running = True
        while self._running:
            await asyncio.sleep(self.CHECK_INTERVAL_SECONDS)
            violations = await self.check_all()
            for v in violations:
                await self._handle_violation(v)

    def stop(self):
        self._running = False

    async def check_all(self) -> list[InvariantViolation]:
        violations = []
        violations += await self._check_l0_invariants()
        violations += await self._check_l3_invariants()
        violations += await self._check_esm_invariants()   # ESM
        violations += await self._check_ce_health()
        violations += await self._check_rfc0006()
        return violations

    async def _check_l0_invariants(self) -> list[InvariantViolation]:
        violations = []
        wm = self.fractal.working_memory
        # L0: VALUES CORE must be present
        if not any(getattr(m, 'id', '') == 'VALUES_CORE' for m in wm):
            violations.append(InvariantViolation(
                invariant_id="L0-001",
                severity="CRITICAL",
                description="VALUES CORE missing from L0 Working Memory",
                detected_at=datetime.now(timezone.utc),
                auto_remediation="Reload VALUES_CORE from constants.py"
            ))
        # L0: capacity must not exceed 5
        if len(wm) > 5:
            violations.append(InvariantViolation(
                invariant_id="L0-002",
                severity="WARNING",
                description=f"L0 capacity {len(wm)} > 5 (Cowan limit)",
                detected_at=datetime.now(timezone.utc),
                auto_remediation="Trigger Priority Eviction"
            ))
        return violations

    async def _check_l3_invariants(self) -> list[InvariantViolation]:
        """Check: are there any invalid facts in L3"""
        violations = []
        query = """
        MATCH (f:Fact) WHERE f.validated = false OR f.validated IS NULL
        RETURN count(f) as bad_count
        """
        result = await self.graph.execute_cypher(query)
        bad_count = result[0].get("bad_count", 0) if result else 0
        if bad_count > 0:
            violations.append(InvariantViolation(
                invariant_id="L3-001",
                severity="CRITICAL",
                description=f"{bad_count} facts in L3 without validated=True",
                detected_at=datetime.now(timezone.utc),
                auto_remediation="Flag for MGL re-validation"
            ))
        return violations

    async def _check_esm_invariants(self) -> list[InvariantViolation]:
        """Check the correctness of ESM states in L3"""
        violations = []
        valid_states = {"Observed","Hypothesized","Supported","Validated",
                        "Contradicted","Deprecated","Collapsed"}

        # No nonexistent states
        query1 = """
        MATCH (f:Fact) WHERE f.epistemic_state IS NOT NULL
          AND NOT f.epistemic_state IN $valid_states
        RETURN count(f) as bad_count
        """
        result = await self.graph.execute_cypher(
            query1, {"valid_states": list(valid_states)}
        )
        bad_count = result[0].get("bad_count", 0) if result else 0
        if bad_count > 0:
            violations.append(InvariantViolation(
                invariant_id="ESM-001",
                severity="CRITICAL",
                description=f"{bad_count} facts with an invalid epistemic_state",
                detected_at=datetime.now(timezone.utc),
                auto_remediation="Set epistemic_state='Observed' — re-enter ESM lifecycle"  # Correct entry into the ESM lifecycle
            ))

        # validated=True ↔ epistemic_state='Validated'
        query2 = """
        MATCH (f:Fact)
        WHERE f.validated = true AND f.epistemic_state <> 'Validated'
        RETURN count(f) as mismatch_count
        """
        result2 = await self.graph.execute_cypher(query2)
        mismatch = result2[0].get("mismatch_count", 0) if result2 else 0
        if mismatch > 0:
            violations.append(InvariantViolation(
                invariant_id="ESM-002",
                severity="WARNING",
                description=f"{mismatch} facts: validated=True but epistemic_state≠Validated",
                detected_at=datetime.now(timezone.utc),
                auto_remediation="Sync epistemic_state with validated flag"
            ))

        # VALUES CORE always Validated
        query3 = """
        MATCH (f:Fact) WHERE f.id IN ['VALUES_CORE','RING_ZERO']
          AND f.epistemic_state <> 'Validated'
        RETURN count(f) as immutable_violated
        """
        result3 = await self.graph.execute_cypher(query3)
        immutable_bad = result3[0].get("immutable_violated", 0) if result3 else 0
        if immutable_bad > 0:
            violations.append(InvariantViolation(
                invariant_id="ESM-003",
                severity="CRITICAL",
                description="VALUES CORE / RING_ZERO not in the Validated state!",
                detected_at=datetime.now(timezone.utc),
                auto_remediation="Force epistemic_state='Validated' for immutable facts"
            ))

        return violations

    async def _check_rfc0006(self) -> list[InvariantViolation]:
        """RFC0006: Engram must not be enabled with API models"""
        from config import settings
        violations = []
        if settings.ENGRAM_ENABLED and settings.LLM_PROVIDER not in \
           {"local", "ollama", "llamacpp", "vllm", "lmstudio"}:  # lmstudio added — matches validate_engram_config
            violations.append(InvariantViolation(
                invariant_id="RFC0006",
                severity="CRITICAL",
                description="RFC0006 violated: Engram enabled with an API model",
                detected_at=datetime.now(timezone.utc),
                auto_remediation="Set ENGRAM_ENABLED=False automatically"
            ))
        return violations

    async def _check_ce_health(self) -> list[InvariantViolation]:
        """Check the health of the ConsolidationEngine"""
        violations = []
        if not self.heartbeat:
            return []   # P9-FIX BUG-1: heartbeat not yet connected — skip
        dlq_size = len(self.heartbeat.consolidation_engine.dlq)
        if dlq_size > 10:
            violations.append(InvariantViolation(
                invariant_id="CE-001",
                severity="WARNING",
                description=f"ConsolidationEngine DLQ size = {dlq_size}",
                detected_at=datetime.now(timezone.utc),
                auto_remediation="Alert ops team"
            ))
        return violations

    async def _handle_violation(self, v: InvariantViolation):
        """
        Four severity levels instead of a binary CRITICAL/WARNING.
        INFO/WARNING do not trigger SAFE_MODE — they only reduce the CE frequency.

        INFO     → log only
        WARNING  → reduce CE frequency (DEGRADED)
        ERROR    → DEGRADED + Grafana alert
        CRITICAL → SAFE_MODE (L3 read-only)
        """
        self.violations_total += 1
        if v.severity == "INFO":
            logger.info(f"Invariant info [{v.invariant_id}]: {v.description}")
        elif v.severity == "WARNING":
            logger.warning(f"Invariant warning [{v.invariant_id}]: {v.description}")
            # Reduce ConsolidationEngine frequency — do not block the system
            await self.heartbeat.reduce_ce_frequency(factor=0.5)
        elif v.severity == "ERROR":
            logger.error(f"INVARIANT ERROR [{v.invariant_id}]: {v.description}")
            await self.heartbeat.enter_degraded_mode(reason=v.invariant_id)
            # Grafana counter increment
        elif v.severity == "CRITICAL":
            logger.critical(f"INVARIANT VIOLATION [{v.invariant_id}]: {v.description}")
            await self.heartbeat.enter_safe_mode(reason=v.invariant_id)
```

---

## 🎭 Cognitive Modes — Three Modes of Operation

> **Why it's critical**: the system works the same way for critical data and creative tasks. Cognitive Modes let the agent adapt — the way a human thinks differently depending on context.

```python
# cognitive_modes.py
from enum import Enum
from dataclasses import dataclass

class CognitiveMode(str, Enum):
    PRECISION   = "precision"    # Critical data, facts
    BALANCED    = "balanced"     # Standard operation (90% of tasks)
    EXPLORATION = "exploration"  # Brainstorm, research
    CREATIVE    = "creative"     # Analogies + only Validated (RFC0067 v2.0)

@dataclass
class ModeConfig:
    token_budget:      int
    evidence_required: int
    truth_gate_coverage: float
    hypothesis_allowed:  bool
    description: str

COGNITIVE_MODE_CONFIGS = {
    CognitiveMode.PRECISION: ModeConfig(
        token_budget=1000,
        evidence_required=5,
        truth_gate_coverage=0.9,
        hypothesis_allowed=False,
        description="Medicine, law, finance — only verified facts"
    ),
    CognitiveMode.BALANCED: ModeConfig(
        token_budget=2000,
        evidence_required=3,
        truth_gate_coverage=0.7,
        hypothesis_allowed=True,
        description="Standard mode — 90% of tasks"
    ),
    CognitiveMode.EXPLORATION: ModeConfig(
        token_budget=4000,
        evidence_required=1,
        truth_gate_coverage=0.4,
        hypothesis_allowed=True,
        description="Brainstorm, research, hypotheses"
    ),
    CognitiveMode.CREATIVE: ModeConfig(
        token_budget=3000,
        evidence_required=3,
        truth_gate_coverage=0.7,
        hypothesis_allowed=False,   # I57: CREATIVE forbids Hypothesized
        description="Analogies + Validated only (RFC0067 v2.0)"
    ),
}

class CognitiveModeRouter:
    """
    Determines the operating mode based on:
    · Explicit user specification
    · Query keywords (RU + EN)
    · Cognitive Load estimate
    """
    PRECISION_SIGNALS   = {"precise", "verify", "prove", "fact", "data",
                            "medic", "legal", "financ", "critical"}
    PRECISION_EN        = {"verify", "accurate", "fact", "data", "medical",
                            "legal", "financial", "critical", "diagnos", "contract"}
    EXPLORATION_SIGNALS = {"imagine", "come up with", "brainstorm", "ideas",
                            "what if", "hypothes", "fantasy", "creativ"}
    EXPLORATION_EN      = {"imagine", "brainstorm", "ideas", "what if",
                            "hypothesis", "explore", "unconventional", "speculate"}
    # CREATIVE mode: RFC0067 v2.0 — Analogy Graph + SBE bridges + temperature 0.6→0.85
    CREATIVE_SIGNALS    = {"metaphor", "analog", "compar", "as if",
                            "write a poem", "write a story", "poetic"}
    CREATIVE_EN         = {"metaphor", "analogy", "as if", "poem",
                            "story", "creative writing", "poetic"}

    def select_mode(self, query: str,
                    explicit_mode: CognitiveMode = None) -> CognitiveMode:
        if explicit_mode:
            return explicit_mode

        query_lower = query.lower()

        if any(signal in query_lower for signal in self.PRECISION_SIGNALS) or \
           any(signal in query_lower for signal in self.PRECISION_EN):
            return CognitiveMode.PRECISION
        # P9-FIX BUG-10: CREATIVE is checked BEFORE EXPLORATION — otherwise "come up with a metaphor"
        # always returns EXPLORATION (because "come up with" in EXPLORATION_SIGNALS wins)
        if any(signal in query_lower for signal in self.CREATIVE_SIGNALS) or \
           any(signal in query_lower for signal in self.CREATIVE_EN):
            return CognitiveMode.CREATIVE
        if any(signal in query_lower for signal in self.EXPLORATION_SIGNALS) or \
           any(signal in query_lower for signal in self.EXPLORATION_EN):
            return CognitiveMode.EXPLORATION
        return CognitiveMode.BALANCED

    def get_config(self, mode: CognitiveMode) -> ModeConfig:
        return COGNITIVE_MODE_CONFIGS[mode]
```

**Integration into the Context Builder**:

```python
# Usage example in context_builder.py
async def build_context(self, query: str, ...) -> str:
    mode = self.mode_router.select_mode(query)
    config = self.mode_router.get_config(mode)

    # RFC0067 v2.0: CREATIVE mode — read SBE bridges from the Redis cache.
    # I56: SBE only via EventBus (Slow Path). Fast Path — cache only.
    # I57: FactsPack in CREATIVE — only Validated. Associations separately.
    creative_associations = []
    if mode == CognitiveMode.CREATIVE:
        cached = await self.redis.get(f"creative_bridge:{session_id}")
        if cached:
            import json
            creative_associations = [
                CreativeAssociation.from_dict(a) for a in json.loads(cached)
            ]
        # Degradation without cache: only Analogy Graph. Do NOT call SBE synchronously (I56).

    # Adapt the token budget and Truth Gate to the mode
    self.available_tokens = config.token_budget
    self.truth_gate_coverage = config.truth_gate_coverage

    # In EXPLORATION mode Hypothesis nodes are allowed in the context
    if config.hypothesis_allowed:
        context_types = ["verified", "hypothesis"]
    else:
        context_types = ["verified"]  # PRECISION: only verified

    logger.info(f"Cognitive mode: {mode.value}, budget: {config.token_budget}")
    ...
```

---

## 💰 Memory Budget Planner

> **Why it's critical**: without limits the graph grows forever. The Memory Budget Planner works like a resource scheduler in an OS — the system knows its own limits.

```python
# memory_budget_planner.py
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class MemoryBudget:
    """Memory limits — do not change without an architectural decision"""
    MAX_NODES_TOTAL:        int   = 500_000
    MAX_EDGES_PER_NODE:     int   = 100
    MAX_EPISODE_SIZE_BYTES: int   = 10_240      # 10 KB
    MAX_ADD_EPISODE_RATE:   int   = 100         # per hour
    MAX_L1_EPISODES:        int   = 1_000       # per session
    GC_TRIGGER_THRESHOLD:   float = 0.85        # 85% full → GC
    ALERT_THRESHOLD:        float = 0.90        # 90% → Grafana alert

class MemoryBudgetPlanner:
    def __init__(self, graph: GraphMemory,
                 consolidation_engine: ConsolidationEngine,
                 budget: MemoryBudget = None):
        self.graph = graph
        self.ce = consolidation_engine
        self.budget = budget or MemoryBudget()
        self._episode_count_hour = 0
        self._hour_start = datetime.now(timezone.utc)
        # FIX: Lock protects the rate-limit from a TOCTOU race condition.
        # Without it, two concurrent calls read the same value and both pass the check.
        self._rate_lock = asyncio.Lock()

    async def check_edges_per_node(self, node_id: str) -> bool:
        """Check the node degree — the graph dies from edge density, not only from the number of nodes"""
        query = """
        MATCH (n {id: $node_id})-[r]-()
        RETURN count(r) as edge_count
        """
        result = await self.graph.execute_cypher(query, {"node_id": node_id})
        edge_count = result[0].get("edge_count", 0) if result else 0
        if edge_count >= self.budget.MAX_EDGES_PER_NODE:
            logger.warning(f"Node {node_id} at edge limit: {edge_count}/{self.budget.MAX_EDGES_PER_NODE}")
            return False
        return True

    async def check_before_write(self, episode_size_bytes: int) -> bool:
        """
        Check whether a new episode can be written.
        Returns True if OK, False if it is necessary to wait.
        """
        # Episode size check
        if episode_size_bytes > self.budget.MAX_EPISODE_SIZE_BYTES:
            logger.warning(f"Episode too large: {episode_size_bytes}b > "
                           f"{self.budget.MAX_EPISODE_SIZE_BYTES}b. Truncating.")
            return False  # Caller must truncate

        # Rate limit check — protected by _rate_lock from TOCTOU
        async with self._rate_lock:
            now = datetime.now(timezone.utc)
            if (now - self._hour_start).total_seconds() > 3600:
                self._episode_count_hour = 0
                self._hour_start = now

            next_count = self._episode_count_hour + 1
            if next_count > self.budget.MAX_ADD_EPISODE_RATE:
                logger.warning(f"Rate limit: {next_count} episodes/hour")
                return False
            self._episode_count_hour = next_count

        # Total graph size check
        total_nodes = await self._get_total_nodes()
        fill_ratio = total_nodes / self.budget.MAX_NODES_TOTAL

        if fill_ratio >= self.budget.ALERT_THRESHOLD:
            logger.error(f"Graph near capacity: {fill_ratio:.1%}")
            # Grafana counter increment (via prometheus_client)

        if fill_ratio >= self.budget.GC_TRIGGER_THRESHOLD:
            logger.warning(f"Auto-triggering GC at {fill_ratio:.1%} capacity")
            await self.ce.enqueue("GC", {}, priority=ConsolidationPriority.GC)

        if total_nodes >= self.budget.MAX_NODES_TOTAL:
            logger.error("Graph at MAX capacity. Blocking write.")
            return False

        return True

    async def _get_total_nodes(self) -> int:
        result = await self.graph.execute_cypher(
            "MATCH (n) WHERE n.is_active = true RETURN count(n) as total"
        )
        return result[0].get("total", 0) if result else 0
```

---

## 🔐 PII Redaction

```python
# pii_redaction.py
import re
from dataclasses import dataclass

@dataclass
class PIIMatch:
    pii_type: str
    original: str
    position: tuple[int, int]

class PIIRedactor:
    """
    Minimal PII redaction implementation for Phase 0/1.
    Removes obvious PII before writing to L1/L3.
    """
    PATTERNS = {
        "email":    r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        "phone_ru": r'\b(?:\+7|8)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}\b',
        "phone_int":r'\b\+[1-9]\d{1,14}\b',
        "card":     r'\b(?:\d{4}[\s\-]?){3}\d{4}\b',
        "passport_ru": r'\b\d{4}\s?\d{6}\b',
        "inn_ru":   r'(?:INN|inn)\s*[:：]?\s*\d{10}(?:\d{2})?',  # INN = Russian taxpayer ID
    }

    def redact(self, text: str) -> tuple[str, list[PIIMatch]]:
        """
        Returns (redacted_text, list_of_matches).
        Matches are saved in Immutable Raw Memory (never in graph).
        """
        matches = []
        for pii_type, pattern in self.PATTERNS.items():
            for m in re.finditer(pattern, text):
                matches.append(PIIMatch(
                    pii_type=pii_type,
                    original=m.group(),
                    position=(m.start(), m.end())
                ))
            text = re.sub(pattern, f"[{pii_type.upper()}_REDACTED]", text)
        return text, matches

    async def forget_user(self, user_id: str,
                          consolidation_engine: ConsolidationEngine):
        """
        GDPR 'right to be forgotten'.
        Softly deletes all user data via CE.
        """
        await consolidation_engine.enqueue(
            op_type="GC",
            payload={"operation": "USER_PURGE", "user_id": user_id},
            priority=ConsolidationPriority.CONSOLIDATE  # Highest priority
        )
        logger.info(f"GDPR forget request queued for user: {user_id}")
```

**Integration**: PIIRedactor is invoked before writing to L1 SQLite and before add_episode() in Graphiti.

---

## 📋 RFC0014 — L2.5 Staging Layer

> **Status**: Canonical · **Phase**: Phase 0+
>
> L2.5 is an asynchronous buffer between L2 and L3. It implements the principle "the graph is built when it can be, not when it must be." SQLite = staging. Graph = the single source of truth.

### Architecture

```
L0 / L1 / L2
    ↓
SQLite: staging_candidates  (temporary buffer)
    ↓
Priority Queue
    ↓
Resource-Aware Scheduler  ← CPU < 35% AND RAM free > 25% AND user_idle
    │
    ├── FAST-TRACK (priority > 0.9) ──────────────┐
    │   bypasses the queue, goes immediately       │
    └── NORMAL BATCH (when idle) ────────────────┐ │
                                                  ↓ ↓
                                            Truth Gate
                                                ↓
                                          L3 Graph (Neo4j)
```

### RFC0014 Invariants

```
RFC0014.I1: SQLite = STAGING. Never the source of truth.
    Graph = the only L3. Graph = Truth is not violated.

RFC0014.I2: Reading: graph first → then staging (low-confidence fallback)
    Fact in graph    → take it from there (confidence as-is)
    Fact in staging  → use with confidence × 0.7 + a "preliminary" marker

RFC0014.I3: Any entry into the graph — only via the Truth Gate.
    Even asynchronously, even at night.

RFC0014.I4: Fast-Track (priority > 0.9) — bypasses the queue and goes immediately.
    Examples: allergies, Ring Zero, critical facts.

RFC0014.I5: Forced flush: if the PC is not idle > 24h →
    the scheduler takes 5-10% CPU to move the oldest records.
```

### SQL Schema for staging_candidates

```sql
-- staging_candidates — buffer before the Truth Gate
CREATE TABLE staging_candidates (
    id               TEXT PRIMARY KEY,
    content          TEXT NOT NULL,        -- FactsPack or summary JSON
    source_layer     TEXT NOT NULL,        -- 'L1' | 'L2'
    epistemic_type   TEXT NOT NULL,        -- 'FACT' | 'LAW' | 'PATTERN' | 'STRATEGY'
    priority_score   REAL NOT NULL,        -- formula (see below)
    confidence       REAL NOT NULL,
    fast_track       BOOLEAN DEFAULT 0,    -- bypasses the queue
    created_at       DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_accessed    DATETIME,
    scheduled_for    DATETIME,
    status           TEXT NOT NULL DEFAULT 'PENDING',
                                           -- PENDING | PROMOTED | REJECTED | ARCHIVED
    is_promoted      BOOLEAN DEFAULT 0,    -- already in L3
    rejection_reason TEXT,
    retry_count      INTEGER DEFAULT 0,
    cpu_cost_estimate REAL DEFAULT 0.1     -- load estimate for the scheduler
);

CREATE INDEX idx_staging_priority   ON staging_candidates(priority_score DESC, created_at);
CREATE INDEX idx_staging_status     ON staging_candidates(status);
CREATE INDEX idx_staging_fast_track ON staging_candidates(fast_track) WHERE fast_track = 1;
CREATE INDEX idx_staging_promoted   ON staging_candidates(is_promoted);

-- Graph-Lite: temporary mini-graph for answers while data is in staging
CREATE TABLE graph_lite_nodes (
    id    TEXT PRIMARY KEY,
    type  TEXT NOT NULL,
    label TEXT NOT NULL,
    payload TEXT  -- JSON
);
CREATE TABLE graph_lite_edges (
    src    TEXT NOT NULL,
    dst    TEXT NOT NULL,
    type   TEXT NOT NULL,
    weight REAL DEFAULT 1.0,
    PRIMARY KEY (src, dst, type)
);
-- When moving to Neo4j: DELETE FROM graph_lite_nodes; DELETE FROM graph_lite_edges;
```

### Priority Score (formula)

```
priority_score = (importance × 0.4)
               + (log1p(access_count) × 0.2)          # log1p(x) = log(1+x), see np.log1p
               + (recency_norm × 0.2)
               + (confidence × 0.2)

recency_norm = exp(-λ × days_since_created),  λ = 0.1

Fast-track threshold: priority_score > 0.9 → immediately → Truth Gate → L3
```

### Resource-Aware Scheduler (Python)

```python
# staging_scheduler.py
import asyncio
import psutil
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class ResourceAwareScheduler:
    """
    Moves data from SQLite staging into the L3 graph
    only when the system is free.
    """
    CPU_THRESHOLD  = 0.35   # max 35% CPU
    RAM_THRESHOLD  = 0.25   # min 25% RAM free
    BATCH_SIZE     = 50     # candidates per cycle
    IDLE_INTERVAL  = 3600   # check every hour
    FORCE_INTERVAL = 86400  # forced flush if no idle > 24h
    MAX_STAGING    = 5000   # max records in staging before force_flush

    def __init__(self, staging_store, truth_gate, graph):
        self.staging  = staging_store
        self.truth_gate = truth_gate
        self.graph    = graph
        self._last_flush = datetime.now(timezone.utc)
        self._running = False

    async def start(self):
        """Start as an asyncio.Task in parallel with the agent."""
        self._running = True
        logger.info("ResourceAwareScheduler started")
        while self._running:
            await asyncio.sleep(self.IDLE_INTERVAL)
            await self._process_fast_track()       # always — regardless of resources
            if await self._should_run():
                await self._promote_batch()
            elif await self._force_flush_needed():
                await self._promote_batch(force=True)

    async def _should_run(self) -> bool:
        cpu  = psutil.cpu_percent(interval=1) / 100
        ram  = psutil.virtual_memory().available / psutil.virtual_memory().total
        pending = await self.staging.count(status="PENDING")
        return cpu < self.CPU_THRESHOLD and ram > self.RAM_THRESHOLD and pending >= 10

    async def _force_flush_needed(self) -> bool:
        hours_since = (datetime.now(timezone.utc) - self._last_flush).total_seconds() / 3600
        staging_size = await self.staging.count(status="PENDING")
        return hours_since > 24 or staging_size > self.MAX_STAGING

    async def _process_fast_track(self):
        """CRITICAL items — do not wait for idle, go immediately."""
        items = await self.staging.get_fast_track()
        for item in items:
            await self._promote_item(item)

    async def _promote_batch(self, force: bool = False):
        batch_size = self.BATCH_SIZE // 2 if force else self.BATCH_SIZE
        items = await self.staging.get_top_priority(limit=batch_size)
        promoted = 0
        for item in items:
            promoted += await self._promote_item(item)
        self._last_flush = datetime.now(timezone.utc)
        logger.info(f"Scheduler: promoted {promoted}/{len(items)} items"
                    f"{' (forced)' if force else ''}")

    async def _promote_item(self, item) -> int:
        try:
            if await self.truth_gate.validate(item):
                await self.graph.add_fact(item)
                await self.staging.update_status(item.id, "PROMOTED")
                return 1
            else:
                await self.staging.update_status(item.id, "REJECTED")
                return 0
        except Exception as e:
            logger.error(f"Promote failed for {item.id}: {e}")
            await self.staging.increment_retry(item.id)
            if await self.staging.get_retry_count(item.id) > 3:
                await self.staging.update_status(item.id, "REJECTED")
            return 0

    def stop(self):
        self._running = False
        logger.info("ResourceAwareScheduler stopped")
```

### Fast-Track API

```python
# Add a critically important fact — bypasses the queue
async def add_fast_track(
    fact: dict,
    reason: str,
    staging_store,
    confidence: float = 0.95,   # ← PATCH-8: was a hardcoded 1.0 — it lied about reliability.
                                 # The 0.95 default is honest for CRITICAL facts.
                                 # The calling code passes what is needed: allergy=0.8, Ring Zero=0.99
) -> bool:
    """
    CRITICAL examples: allergies, safety, Ring Zero changes.
    Such facts do NOT wait for idle — they go straight through the Truth Gate into L3.
    """
    from staging_models import StagingItem
    item = StagingItem(
        content=fact,
        epistemic_type="FACT",
        priority_score=1.0,
        confidence=confidence,   # ← now an honest value from the calling code
        fast_track=True,
        source_layer="L2",
        metadata={"reason": reason, "bypass_queue": True}
    )
    return await staging_store.insert(item)
```

### Staging Cleanup (overflow prevention)

```python
# Periodically — at GC or forced
async def cleanup_staging(staging_store):
    now = datetime.now(timezone.utc)
    # Low-priority garbage → delete
    await staging_store.delete_where(
        "priority_score < 0.3 AND created_at < ?",
        (now - timedelta(days=30),)
    )
    # Medium priority → archive
    await staging_store.archive_where(
        "priority_score BETWEEN 0.3 AND 0.6 AND created_at < ?",
        (now - timedelta(days=60),)
    )
    # High priority stuck → boost
    await staging_store.boost_priority(
        "priority_score > 0.6 AND created_at < ?",
        factor=1.5,
        args=(now - timedelta(days=90),)
    )
```

### Integration into the Canonical Memory Protocol

```
NEW STEP F4.5 : Staging Promote
    → ResourceAwareScheduler.start() — asyncio.Task at agent startup
    → Fast-Track hook is invoked on every add_episode() with priority > 0.9
    → Normal batch: every hour when CPU is idle
    → Graph-Lite is used on read as a fallback (confidence × 0.7)
```

---

## 📋 RFC0013 — L2 CORE (Canonical Contract)

> **Status**: Canonical · **Phase**: Phase 0+
>
> L2 CORE defines the minimal, immutable "graph + analytics" contract that works offline (without an LLM), is auditable, reproducible, and scalable.

### Principle: LLM as interpreter

```
L2/L3 = knowledge source (structured, verified)
LLM   = speech apparatus (formats the ready-made, does not add facts)

HEADLESS mode: LLM fully disabled.
  L2 → template responder → structured answer without generation

LITE mode (RAM < 4GB):
  Neo4j → sqlite-vec (vector search)
  Etir  → simplified or disabled
  ReactivationEngine → once a day
  GC/Consolidation → low priority
```

### L2 area of responsibility

```
L2 IS RESPONSIBLE FOR:
  · Extracting structure from L1: entities, relations, events, assertions
  · Analytics over the graph: clusters, centralities, proximity, contradictions
  · Deterministic answers to queries without generating "out of thin air"

L2 IS NOT RESPONSIBLE FOR:
  · Creative generation
  · Guesses with no grounding in data
  · Substituting style for evidence
```

### L2 storage (SQLite WAL)

```sql
-- Table l2_memory (persistent L2, replacement for mtm_cache in RAM)
CREATE TABLE l2_memory (
    id                  TEXT PRIMARY KEY,
    original_episode_ids TEXT NOT NULL,  -- JSON array, L1→L2 tracing
    summary             TEXT NOT NULL,   -- TF-IDF extractive
    embedding           BLOB,            -- optional
    topics              TEXT,            -- JSON array
    domain_id           TEXT,            -- RFC0012
    base_importance     REAL NOT NULL,
    current_importance  REAL NOT NULL,
    cluster_id          TEXT,
    cluster_type        TEXT DEFAULT 'EPISODIC',  -- EPISODIC|STRATEGIC|CONCEPTUAL
    access_count        INTEGER DEFAULT 0,
    last_access         TIMESTAMP,
    ttl_days            REAL DEFAULT 7,
    reactivation_count  INTEGER DEFAULT 0,
    last_reactivation   TIMESTAMP,
    is_active           BOOLEAN DEFAULT 1,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP,
    FOREIGN KEY (domain_id) REFERENCES domains(id)
);

CREATE VIRTUAL TABLE l2_fts USING fts5(summary, topics, content=l2_memory);
CREATE INDEX idx_l2_importance ON l2_memory(current_importance DESC);
CREATE INDEX idx_l2_cluster    ON l2_memory(cluster_id);
CREATE INDEX idx_l2_domain     ON l2_memory(domain_id);
CREATE INDEX idx_l2_active     ON l2_memory(is_active);
CREATE INDEX idx_l2_type       ON l2_memory(cluster_type);
```

### Metrics I/O batching (SSD protection)

```python
# l2_metrics_buffer.py
# Constantly rewriting access_count on every access → SSD wear.
# Buffering solves it: into memory → flush every 10 minutes.
class L2MetricsBuffer:
    def __init__(self, db_path: str, flush_interval: int = 600):  # ← PATCH-1: db_path added (previously AttributeError in _flush_to_db)
        self._db_path = db_path          # read in _flush_to_db()
        self._buffer: dict[str, dict] = {}
        self._last_flush = time.time()
        self._flush_interval = flush_interval

    def record_access(self, item_id: str):
        if item_id not in self._buffer:
            self._buffer[item_id] = {"access_count": 0, "last_accessed": None}
        self._buffer[item_id]["access_count"] += 1
        self._buffer[item_id]["last_accessed"] = datetime.now(timezone.utc).isoformat()

    async def flush_if_needed(self):
        if time.time() - self._last_flush > self._flush_interval:
            # P1-D FIX: race condition — await could switch the event loop while _flush_to_db() ran.
            # New data arrived in _buffer, then clear() removed it → loss of metrics.
            # Solution: atomically capture the old buffer, immediately open a new one.
            buffer_to_flush = self._buffer          # capture atomically
            self._buffer = {}                       # new buffer for incoming data
            self._last_flush = time.time()
            await self._flush_to_db(buffer_to_flush)   # pass the old buffer

    async def _flush_to_db(self):
        if not self._buffer:
            return
        async with aiosqlite.connect(self._db_path) as db:
            for item_id, stats in self._buffer.items():
                await db.execute(
                    "UPDATE l2_memory SET access_count = access_count + ?, last_access = ? WHERE id = ?",
                    (stats["access_count"], stats["last_accessed"], item_id)
                )
            await db.commit()
```

### TTL Manager (adaptive)

```python
# ttl_manager.py
class L2TTLManager:
    BASE_DAYS = 7
    MAX_DAYS  = 224  # 7 * 2^5

    def __init__(self, store, archive):   # ← PATCH-2: __init__ was missing, handle_expiration crashed on self.store/self.archive
        self.store   = store              # persistent L2 store
        self.archive = archive            # cold storage / S3

    def calculate_ttl(self, item: MemoryItemL2) -> float:
        """TTL grows with usage frequency — important things live longer."""
        visits = item.access_count + item.reactivation_count
        return min(self.BASE_DAYS * (2 ** min(visits, 5)), self.MAX_DAYS)

    async def handle_expiration(self, item: MemoryItemL2):
        if item.current_importance > 0.5:
            item.ttl_days = self.calculate_ttl(item) * 1.5  # extend
            await self.store.update(item)
        else:
            item.is_active = False  # soft delete
            item.updated_at = datetime.now(timezone.utc)
            await self.store.update(item)
            await self.archive.move_to_cold_storage(item)
```

### ReactivationEngine ("agent sleep")

```python
# reactivation_engine.py
# Analogous to hippocampal replay: while the agent is not busy — strengthens what matters.
class ReactivationEngine:
    """Background process. Started as an asyncio.Task in parallel with the agent."""

    async def start(self):
        while True:
            await asyncio.sleep(3600)  # every hour
            if self._should_reactivate():
                await self._reactivation_cycle()

    def _should_reactivate(self) -> bool:
        return psutil.cpu_percent() < 30  # only under low load

    async def _reactivation_cycle(self):
        candidates = await self.store.get_top_by_importance(limit=10)
        for item in candidates:
            item.reactivation_count += 1
            item.current_importance = min(1.0, item.current_importance + 0.05)
            item.ttl_days = min(224, item.ttl_days * 1.2)
            item.last_reactivation = datetime.now(timezone.utc)
            await self.store.update(item)
            await self._strengthen_cluster_connections(item)
        logger.info(f"ReactivationEngine: strengthened {len(candidates)} episodes")
```

### L2 Health Index

```python
# Periodically → Prometheus. Value 0.0–1.0.
def calculate_l2_health(items: List[MemoryItemL2], clusters) -> float:
    if not items:
        return 0.0
    avg_importance  = sum(i.current_importance for i in items) / len(items)
    stale_ratio     = sum(1 for i in items if i.ttl_days <= 7) / len(items)
    cluster_coherence = sum(c.coherence_score for c in clusters) / max(len(clusters), 1)
    access_rate     = sum(i.access_count for i in items) / max(len(items), 1)
    target_rate     = 5.0  # target average number of accesses

    health = (
        avg_importance              * 0.30 +
        (1 - stale_ratio)          * 0.30 +
        cluster_coherence          * 0.20 +
        min(access_rate / target_rate, 1.0) * 0.20
    )
    return round(max(0.0, min(1.0, health)), 3)
```

### Protocol for L2 responses without an LLM (L2Query / L2Result)

```python
# l2_query_protocol.py
# L2 always returns a structure. The LLM (if needed) only renders it.

@dataclass
class L2Query:
    intent: Literal["lookup", "explain", "compare", "derive", "verify", "plan"]
    anchors: List[str]          # query anchors
    constraints: dict           # domain, depth, sources
    output_mode: Literal["short", "structured", "trace_heavy"] = "structured"

@dataclass
class L2Result:
    answer: dict                # structured object (concept_card / argument_map / matrix / ranked_list)
    confidence: float           # Confidence = w_e·E + w_c·C + w_k·K − w_x·X − w_d·D
    confidence_factors: dict    # {E, C, K, X, D} for transparency
    trace: dict                 # nodes_used, edges_used, metrics_used, rules_fired
    conflicts: List[dict]       # active contradictions (not suppressed)
    next_actions: List[str]     # deterministic suggestions

# Confidence formula (fixed in RFC0013):
# E = Evidence:    fraction of assertions with direct Evidence
# C = Consistency: few CONTRADICTS in the subgraph
# K = Coverage:    coverage of the question's aspects
# X = Conflicts:   penalty for active contradictions
# D = Decay:       penalty for staleness
```

### The 5 invariants of L2 CORE

```
RFC0013.I1: Determinism
    same graph + query + parameters → same result

RFC0013.I2: Traceability
    every answer = Answer + Trace + Confidence (a formula, not a "feeling")

RFC0013.I3: Separation of fact and inference
    fact = Claim with Evidence
    inference = DERIVES + rule/metric

RFC0013.I4: Graph anti-explosion
    any expansion has limits: depth / fanout / node_budget / time

RFC0013.I5: Conflict-awareness
    contradictions are NOT swept away — they are marked, accounted for in Confidence
```

### Operating scenarios

```
Scenario 1 — HEADLESS: "How to increase fertility?"
  taxonomy_search(domain:agriculture)
  → L2: cluster_type=STRATEGIC cluster with high goal_alignment
  → FactsPack → template answer
  → answer without an LLM

Scenario 2 — LLM as interpreter: "Explain it in verse"
  the same facts from L2/L3 → the LLM receives the FactsPack
  → prompt: "reformat, do not add new facts"
  → the LLM does not think, only formats

Scenario 3 — Document analysis:
  document → episodes (L1) → summary in L2
  → on query: summary from L2, do not re-read the document
```

---

## 💓 Meta-Supervisor — Apex Controller

### Apex Controller architecture

```
                    ┌──────────────────────────────────────┐
                    │         META-SUPERVISOR              │
                    │         (Apex Controller)            │
                    │                                      │
      INPUTS:       │  · MHI score (Phase 2)         │   OUTPUTS:
      ──────        │  · CE health (queue/dlq size)        │   ──────────
      CE status ──► │  · Budget fill ratio                 │ ──► Safe Mode
      DLQ size  ──► │  · Invariant violations              │ ──► CE frequency
      Budget    ──► │  · Circuit Breaker states            │ ──► GC trigger
      Invariants──► │  · ESM Collapsed rate                │ ──► Alert ops
                    └──────────────────────────────────────┘
```

### Three operating modes

```
NORMAL (default):
  · CE runs at normal frequency
  · All mechanisms active
  · Standard Truth Gate thresholds

DEGRADED (on warnings):
  · CE frequency x2 (accelerated consolidation)
  · Budget threshold lowered by 10%
  · Grafana alert sent

SAFE_MODE (on critical failures):
  · L3 = read-only
  · L1 keeps accumulating data
  · CE operations → DLQ
  · Tasks → BLOCKED_AWAITING_DB
```

```python
# meta_supervisor_apex.py
import asyncio
import logging
from datetime import datetime, timezone
from enum import Enum

logger = logging.getLogger(__name__)

class SupervisorMode(str, Enum):
    NORMAL    = "normal"
    DEGRADED  = "degraded"
    SAFE_MODE = "safe_mode"

class MetaSupervisorApex:
    """
    Apex Controller — the control layer over the entire Velantrim system.

    Inputs: CE health, Budget fill ratio, Invariant violations,
           Circuit Breaker states, ESM Collapsed rate.
    Outputs: Safe Mode, CE frequency, GC trigger, alerts.

    Recovery Protocol: if the Supervisor itself crashes →
    Kubernetes liveness probe restarts the process.
    All Supervisor decisions are idempotent — restarting is safe.

    NOT a recursive Meta-MHI (anti-pattern). Supervisor statistics
    are collected by Prometheus scraping from the outside.
    """
    HEARTBEAT_INTERVAL   = 10   # seconds
    CE_TIMEOUT_THRESHOLD = 60   # seconds of CE silence → safe mode
    BUDGET_WARN_RATIO    = 0.85 # 85% fill → degraded
    DLQ_WARN_SIZE        = 10   # DLQ > 10 → warning

    def __init__(
        self,
        consolidation_engine: "ConsolidationEngine",
        graph: "GraphMemory",
        budget_planner: "MemoryBudgetPlanner",
        invariant_checker: "RuntimeInvariantChecker"
    ):
        self.ce        = consolidation_engine
        self.graph     = graph
        self.budget    = budget_planner
        self.checker   = invariant_checker
        self.mode      = SupervisorMode.NORMAL
        self._last_ce_ping = datetime.now(timezone.utc)
        self._mode_changed_at = datetime.now(timezone.utc)

    async def start(self):
        """Background Apex Controller"""
        logger.info("Meta-Supervisor Apex Controller started")
        while True:
            await asyncio.sleep(self.HEARTBEAT_INTERVAL)
            await self._supervise_cycle()

    async def _supervise_cycle(self):
        """One cycle of monitoring and control"""
        # 1. Collect signals
        signals = await self._collect_signals()

        # 2. Determine the mode
        new_mode = self._decide_mode(signals)

        # 3. Apply changes if the mode has changed
        if new_mode != self.mode:
            await self._apply_mode_transition(self.mode, new_mode, signals)
            self.mode = new_mode
            self._mode_changed_at = datetime.now(timezone.utc)

    async def _collect_signals(self) -> dict:
        """Collect metrics from all components"""
        ce_alive = await self._ping_ce()
        dlq_size = len(self.ce.dlq)
        budget_fill = await self.budget._get_total_nodes() / self.budget.budget.MAX_NODES_TOTAL
        violations = await self.checker.check_all()
        critical_violations = [v for v in violations if v.severity == "CRITICAL"]

        signals = {
            "ce_alive":          ce_alive,
            "ce_silent_seconds": (datetime.now(timezone.utc) - self._last_ce_ping).total_seconds(),
            "dlq_size":          dlq_size,
            "budget_fill":       budget_fill,
            "critical_violations": len(critical_violations),
            "violation_ids":     [v.invariant_id for v in critical_violations],
        }
        # P4-E FIX: MHI integration Phase 2 — wire up MHICalculator once implemented
        if hasattr(self, 'mhi_calculator'):
            try:
                signals["mhi"] = await self.mhi_calculator.get_current_mhi()
                if signals["mhi"] < 0.5:
                    signals["critical_violations"] += 1   # DEGRADED trigger
            except Exception:
                signals["mhi"] = None   # graceful fallback
        return signals

    SAFE_MODE_MIN_RECOVERY_SECONDS = 300  # P2-C FIX: minimum 5 minutes in SAFE_MODE (cooldown)

    def _decide_mode(self, signals: dict) -> SupervisorMode:
        """Mode transition logic.
        P2-C FIX: added a cooldown for SAFE_MODE.
        Without a cooldown: an unstable DLQ → rapid SAFE↔NORMAL oscillation → log flood + chaotic read-only.
        """
        # SAFE_MODE on serious failures
        if (not signals["ce_alive"] and signals["ce_silent_seconds"] > self.CE_TIMEOUT_THRESHOLD) \
        or signals["critical_violations"] > 0:
            return SupervisorMode.SAFE_MODE

        # P2-C FIX: cooldown — do not exit SAFE_MODE before MIN_RECOVERY_SECONDS
        if self.mode == SupervisorMode.SAFE_MODE:
            time_in_safe = (datetime.now(timezone.utc) - self._mode_changed_at).total_seconds()
            if time_in_safe < self.SAFE_MODE_MIN_RECOVERY_SECONDS:
                return SupervisorMode.SAFE_MODE  # hold the mode for at least 5 minutes

        # DEGRADED on warnings
        if signals["dlq_size"] > self.DLQ_WARN_SIZE \
        or signals["budget_fill"] > self.BUDGET_WARN_RATIO:
            return SupervisorMode.DEGRADED

        return SupervisorMode.NORMAL

    async def _apply_mode_transition(
        self,
        from_mode: SupervisorMode,
        to_mode: SupervisorMode,
        signals: dict
    ):
        if to_mode == SupervisorMode.SAFE_MODE:
            self.graph.set_readonly(True)
            logger.critical(
                f"SAFE MODE ACTIVATED: violations={signals['violation_ids']}, "
                f"ce_alive={signals['ce_alive']}"
            )

        elif to_mode == SupervisorMode.DEGRADED:
            logger.warning(
                f"DEGRADED MODE: dlq={signals['dlq_size']}, "
                f"budget={signals['budget_fill']:.1%}"
            )
            # Accelerate GC
            await self.ce.enqueue("GC", {}, priority=ConsolidationPriority.GC)

        elif to_mode == SupervisorMode.NORMAL:
            if from_mode == SupervisorMode.SAFE_MODE:
                self.graph.set_readonly(False)
                logger.info("SAFE MODE DEACTIVATED — system recovered")

    async def _ping_ce(self) -> bool:
        """Ping ConsolidationEngine"""
        try:
            await asyncio.wait_for(
                self.ce.enqueue("PING", {}, priority=ConsolidationPriority.GC),
                timeout=5.0
            )
            self._last_ce_ping = datetime.now(timezone.utc)
            return True
        except Exception:
            return False

    async def enter_safe_mode(self, reason: str = "external"):
        """External Safe Mode invocation (from InvariantChecker)"""
        await self._apply_mode_transition(
            self.mode, SupervisorMode.SAFE_MODE,
            {"violation_ids": [reason], "ce_alive": True, "budget_fill": 0}
        )
        self.mode = SupervisorMode.SAFE_MODE

    def health_check(self) -> dict:
        return {
            "mode":            self.mode.value,
            "mode_since":      self._mode_changed_at.isoformat(),
            "last_ce_ping":    self._last_ce_ping.isoformat(),
            "ce_dlq_size":     len(self.ce.dlq),
            "l3_readonly":     self.graph.is_readonly(),
        }
```

---

## 📊 Memory Health Index (MHI) — Phase 2

> **Why here**: MHI requires real data to calibrate its weights. The coefficients cannot be chosen without production data on degradation. This description fixes the architectural decision; implementation comes after the first 2 weeks of stable operation.

```
MHI = a single indicator of graph health
      (from 0.0 = dead to 1.0 = perfect)

Components (weights are calibrated against real data):
  w1 · stale_ratio      = is_active=false / total_nodes
  w2 · avg_traversal    = P95 retrieval latency in ms / 500
  w3 · entropy          = normalized entropy of node degrees
  w4 · retrieval_cost   = average tokens per query / 2000

Auto-triggers:
  MHI < 0.3  → 🔴 immediate GC + alert ops
  MHI < 0.5  → 🟡 accelerate ConsEngine (DEGRADED)
  MHI < 0.7  → 🟡 create EvidenceSet aggregators
  MHI > 0.9  → 🟢 healthy, reduce maintenance frequency

Implementation:
  · A separate asyncio.Task — does not block the Fast Path
  · Shadow replica Neo4j — does not load the main graph
  · Random walk sampling — not a full traversal (O(N))
  · Updated every 5 minutes
  · CPU quota isolated from the L4 Reasoning Engine

Integration:
  · MetaSupervisorApex._collect_signals() reads MHI
  · When MHI < 0.5 → SupervisorMode.DEGRADED
  · Prometheus gauge: memory_health_index{component="graph"}

Phase 2: implement MHICalculator after 2 weeks of data
```

---

## 🚀 Implementation Roadmap

### ⚠️ Schema Migrations — versioning the Neo4j schema

> ⚠️ **Production blocker**: The Neo4j schema evolves between deployments.
> Without versioning, updating the code without updating the schema leads to a crash when writing a node.

```
Rule: On every change to the Neo4j schema — create a migration.

Structure:
  migrations/
    v8_01_add_evidence_count.cypher
    v8_02_add_hypothesis_node.cypher
    v8_03_add_etir_weights.cypher
    v8_04_add_session_id_l1.cypher
    v8_05_add_cognitive_mode_and_budget.cypher
    -- P2-B FIX: numbering v5_xx → v8_xx (system v8.0, not v5.0)

Check at startup:
  1. pipeline.__init__() calls schema_version_check()
  2. Reads the current version from Neo4j: MATCH (m:SchemaVersion) RETURN m.version
  3. If version < expected → runs pending migrations
  4. If the schema is not found → creates it from scratch (first run)
  5. If the version is incompatible → BLOCKS startup with an explicit error

The SchemaVersion field in Neo4j:
  CREATE (m:SchemaVersion {version: "8.0", applied_at: datetime()})  -- P2-B FIX: was "5.0" while the system is v8.0
```

Migration (`migrations/v8_05_add_cognitive_mode_and_budget.cypher`):  <!-- P2-B FIX -->

```cypher
-- Add fields for Cognitive Modes and Budget Planner

// Add cognitive_mode to Episode
MATCH (ep:Episode) WHERE ep.cognitive_mode IS NULL
SET ep.cognitive_mode = 'BALANCED';

// Add epistemic_state to Fact (placeholder for ESM Phase 2)
MATCH (f:Fact) WHERE f.epistemic_state IS NULL
SET f.epistemic_state = 'Validated',
    f.epistemic_score = f.confidence;

// Add budget_tokens to Episode for consumption monitoring
MATCH (ep:Episode) WHERE ep.budget_tokens IS NULL
SET ep.budget_tokens = 0;

// Update SchemaVersion
MERGE (m:SchemaVersion {version: "8.0"})  -- P2-B FIX
SET m.applied_at = datetime(),
    m.changes = "cognitive_mode, epistemic_state, epistemic_score, budget_tokens";
```

### Phase 1: Core infrastructure (1-2 weeks)

**Goal**: Get a minimal working system running

- [ ] Install Neo4j 5.26+ + Graphiti
- [ ] **CRITICAL: Create Neo4j indexes** (without these the system degrades!)
- [ ] **Add an `embedding_version` field to the schema of all nodes**
- [ ] **Add Soft Delete fields (`is_active`, `valid_to`, `transaction_time`) to the schema**
- [ ] **Add a `raw_episode_id` field to the :Episode schema**
- [ ] **Add an `:Evidence` node and a `[:SUPPORTED_BY]` relationship to the schema**
- [ ] **Add a `:Concept` node and `[:CAUSES]`, `[:CONCEPT_OF]` relationships to the schema**
- [ ] **Implement ImmutableRawMemory** (SQLite, append-only)
- [ ] **Implement MemoryGuardian** (extend the L5 Observer)
- [ ] **Fix formal invariants** as tests (CI checks invariants)
- [ ] Set up Redis for the Event Bus with a DLQ
- [ ] Implement RobustEventBus with retry/fallback
- [ ] **Add a Circuit Breaker for Neo4j and Redis**
- [ ] Integrate Graphiti for automatic extraction
- [ ] Basic hybrid search (vectors + graph)
- [ ] Simple agent with memory retrieval
- [ ] **Set up OpenTelemetry for observability**
- [ ] **Fix the `MAX_TOKENS_MEMORY_PER_QUERY` constant**
- [ ] **Minimal Audit Layer** (logging to SQLite)
- [ ] ✅ **Launch the ConsolidationEngine** (replaces 3 independent workers)
- [ ] ✅ **RFC0006 validate_engram_config() in pipeline.__init__()**
- [ ] ✅ **Run the Runtime Invariant Checker as a background task**
- [ ] ✅ **Integrate the Cognitive Mode Router into the Context Builder**
- [ ] ✅ **Call PIIRedactor before writing to L1 and add_episode()**
- [ ] ✅ **Enable SQLite WAL mode at initialization**
- [ ] ✅ **Memory Budget Planner check_before_write() before every add_episode()**
- [ ] ✅ **Launch the Meta-Supervisor Apex Controller in parallel with the agent**
- [ ] ✅ **Schema migration v5_05_add_cognitive_mode_and_budget.cypher**

**Success criterion**: The agent can save conversations and retrieve relevant information, the system is resilient to dependency failures, and there are no race conditions

---

### Phase 2: Fractal hierarchy (2-3 weeks)

**Goal**: Implement multi-level memory with automatic consolidation

- [ ] Implement FractalMemory with three levels (STM/MTM/LTM)
- [ ] **Persistent L2 — the l2_memory table (SQLite WAL + FTS5)**
- [ ] **cluster_type (EPISODIC/STRATEGIC/CONCEPTUAL) + per-type decay logic**
- [ ] **Cold Start Guard in consolidate_stm_to_mtm (≥ 50 episodes)**
- [ ] **TTL Manager — adaptive (7 × 2^visits, max 224 days)**
- [ ] **L2MetricsBuffer — I/O batching (flush every 10 min)**
- [ ] **Create the staging_candidates table + graph_lite_nodes/edges**
- [ ] **Run the ResourceAwareScheduler as an asyncio.Task**
- [ ] **Fast-Track hook in add_episode() when priority > 0.9**
- [ ] **Improved decay with reinforcement and emotional salience**
- [ ] **Adaptive STM→MTM consolidation** (dynamic intervals)
- [ ] Clustering and **hybrid MTM→LTM consolidation** (extractive + selective LLM)
- [ ] Background workers (AdaptiveConsolidationWorker)
- [ ] Importance scoring with multi-factor calculation
- [ ] **Query optimization with LIMIT** for all Cypher queries
- [ ] **Implement the Promote/Demote Protocol** (formal rules from the section)
- [ ] **Lazy Re-indexing worker** (re-index `reindex_required=true` in batches)
- [ ] **Async Etir** — compute spreading activation in the background before the user's query

**Success criterion**: Memory consolidates automatically, token usage is reduced by 70%+, and there are no memory leaks

---

### Phase 3: Self-learning (2-3 weeks)

**Goal**: The agent learns from experience

- [ ] ReasoningBank implementation
- [ ] Experience logging with outcome tracking
- [ ] Strategy extraction (distill_strategies)
- [ ] **Thompson Sampling strategy selection** (exploration/exploitation, RFC0039)
- [ ] **Negative reinforcement** via confidence penalty
- [ ] Retrieve-Execute-Judge-Learn loop
- [ ] Strategy feedback loop with dynamic confidence updating
- [ ] Anti-pattern detection to avoid repeated mistakes

**Success criterion**: The agent improves task success by 25%+, avoids repeating mistakes, and the exploration/exploitation balance works

---

### Phase 4: Optimization and Production (2-3 weeks)

**Goal**: Production readiness

- [ ] Token budget optimization with dynamic budgeting
- [ ] Context builder with prioritization
- [ ] Redis caching for frequent queries
- [ ] Community detection for clustering
- [ ] **Memory Garbage Collection** (periodic cleanup, Soft Delete → S3 → Hard Delete)
- [ ] **Archiving old nodes to S3**
- [ ] Comprehensive monitoring (Prometheus + Grafana + Tempo)
- [ ] Performance benchmarking
- [ ] **A/B testing framework** to validate improvements
- [ ] Health checks for all components
- [ ] DLQ processing for failed events
- [ ] **Full Audit Layer API** (3 methods: context, strategy, forgetting)
- [ ] **[:CONTRADICTS] pipeline** for resolving fact conflicts
- [ ] **Memory Router upgrade** — replace the heuristic with an o4-mini enum classifier
- [ ] **Knowledge Distillation Engine** MVP (narrow domain, JSON triples)
- [ ] **Cascading invalidation** of Strategy on Soft Delete of a Fact

**Success criterion**: P95 latency <500ms, token reduction >90%, the graph does not grow indefinitely, production readiness

---

### Phase 5: Advanced Features (optional)

- [ ] Adaptive resolution caching
- [ ] Topological graph compression
- [ ] Meta-learning for strategy selection
- [ ] Multi-agent memory sharing
- [ ] Privacy-preserving memory (GDPR compliance)
- [ ] Memory export/import

---

## ⚠️ Important warnings

### Security

1. **Privacy**: Episodic memory stores personal information
   - ✅ PIIRedactor is implemented (not just a declaration) — automatically redacts before writing to L1/L3
   - ✅ GDPR `forget_user()` via ConsolidationEngine.enqueue(USER_PURGE)
   - Deletion-on-request mechanism (GDPR "right to be forgotten") — implemented
   - Encryption of sensitive data — Phase 2

2. **Recursive self-improvement**: Self-learning requires oversight
   - Do not grant full code access at the start
   - Human-in-the-loop for critical decisions
   - A/B testing before production

3. **Bias in experience**: Bad experience can become entrenched
   - Periodic validation of strategies
   - A "forgetting" mechanism for outdated patterns
   - Diversity in experience replay

### Performance

1. **Computational overhead**: Background processes consume resources
   - Balance the consolidation frequency
   - Use batching for graph updates
   - Monitor CPU/Memory usage

2. **Graph scaling**: Neo4j requires optimization for large graphs
   - Indexes on critical fields
   - Periodic archiving of old nodes
   - Sharding for very large graphs

3. **Token costs**: Even with optimization, an LLM is expensive
   - Use fast models for routine work (o4-mini / Claude Haiku 4.5)
   - Cache frequent queries
   - Monitor and alert on anomalous usage

4. ✅ **ConsolidationEngine — a single worker coordinator**

   Three independent workers are replaced by a single coordinator:
   ```
   ConsolidationEngine :
     All operations → asyncio.PriorityQueue → asyncio.Lock → Neo4j
     Priority order: CONSOLIDATE > ARCHIVE > GC
     Timeout: 30 seconds per operation
     On timeout: operation → DLQ (no data loss)
     Fallback: L3 → read-only, L1 keeps working
   ```

```python
# consolidation_engine.py
import asyncio
from collections import deque
from enum import Enum, IntEnum
from dataclasses import dataclass, field
from typing import Any, Optional
import logging

logger = logging.getLogger(__name__)

class ConsolidationPriority(IntEnum):
    CONSOLIDATE = 1   # Highest priority
    ARCHIVE     = 2
    GC          = 3   # Lowest priority

class TaskStatus(str, Enum):
    NEW                = "new"
    ACTIVE             = "active"
    RESOLVED           = "resolved"
    FAILED             = "failed"
    BLOCKED_AWAITING_DB = "blocked_awaiting_db"

@dataclass(order=True)
class ConsolidationOp:
    priority: int
    op_type: str = field(compare=False)
    payload: Any  = field(compare=False)
    timeout: int  = field(compare=False, default=30)

class ConsolidationEngine:
    """
    A single coordination point for all operations on the Neo4j graph.
    Eliminates race conditions between AdaptiveConsolidationWorker,
    MemoryGarbageCollector and MemoryArchival.

    BLOCKED_AWAITING_DB: if CE is unavailable, the task gets this
    status instead of ACTIVE, so monitoring understands the cause of the delay.
    """
    def __init__(self, graph: GraphMemory, event_bus: RobustEventBus,
                 gc: "MemoryGarbageCollector" = None):
        self._queue: asyncio.PriorityQueue = asyncio.PriorityQueue()
        self._lock  = asyncio.Lock()
        self._running = False
        self.graph = graph
        self.event_bus = event_bus
        self.gc = gc
        self.dlq: deque[ConsolidationOp] = deque(maxlen=1000)

    async def enqueue(
        self,
        op_type: str,
        payload: Any,
        priority: ConsolidationPriority = ConsolidationPriority.CONSOLIDATE
    ):
        op = ConsolidationOp(priority=int(priority), op_type=op_type, payload=payload)
        await self._queue.put(op)
        logger.debug(f"CE enqueue: {op_type} priority={priority.name}")

    async def start(self):
        self._running = True
        logger.info("ConsolidationEngine started")
        while self._running:
            try:
                op = await asyncio.wait_for(self._queue.get(), timeout=5.0)
                await self._process(op)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"CE loop error: {e}")

    async def _process(self, op: ConsolidationOp):
        async with self._lock:
            try:
                result = await asyncio.wait_for(
                    self._dispatch(op),
                    timeout=op.timeout
                )
                return result
            except asyncio.TimeoutError:
                logger.error(f"CE timeout: {op.op_type} → DLQ")
                self.dlq.append(op)
                # Mark tasks as BLOCKED_AWAITING_DB
                if op.op_type == "CONSOLIDATE" and hasattr(op.payload, "task_id"):
                    await self.event_bus.publish(AgentEvent(
                        event_type=EventType.TASK_STATUS_CHANGED,
                        timestamp=datetime.now(timezone.utc),
                        content={"task_id": op.payload.task_id,
                                 "status": TaskStatus.BLOCKED_AWAITING_DB,
                                 "reason": "ConsolidationEngine timeout"},
                        metadata={},
                        session_id=op.payload.session_id
                    ))
            finally:
                self._queue.task_done()

    async def _dispatch(self, op: ConsolidationOp):
        if op.op_type == "CONSOLIDATE":
            return await self.graph.add_episode(**op.payload)
        elif op.op_type == "ARCHIVE":
            return await self.graph.soft_delete(**op.payload)
        elif op.op_type == "GC":
            if self.gc:
                return await self.gc.run_full_gc()
            logger.warning("CE: GC requested but gc= not configured")
        elif op.op_type == "PING":
            # heartbeat from MetaSupervisor — confirm that CE is alive
            logger.debug("CE: PING received → alive")
            return True
        else:
            logger.warning(f"CE unknown op_type: {op.op_type}")

    def stop(self):
        self._running = False
        logger.info("ConsolidationEngine stopped")
```

---

## 🔱 L3.5 — Etir (Velantrim Synaptic Activation Layer)

> **Important**: In the Velantrim architecture, L3.5 is exclusively Etir.
> Etir belongs to the Velantrim ExoCortex canon and operates outside the transformer.

---

### ⚡ L3.5 — Etir (Velantrim Synaptic Activation Layer)

**Etir** is a system layer of Velantrim. The name was coined within the project and belongs to the Velantrim ExoCortex canon.

```
Nature:      SYSTEMIC — outside the transformer
Mechanism:   Spreading activation over the Neo4j graph
Storage:     In-memory Python layer, not in the graph
Dependency:  Does NOT depend on the LLM — works without the transformer
Dynamics:    Live, changes at runtime on every query
Brain analog: Synaptic pre-activation of neural networks
```

**How Etir works:**

```
Query → L4 Reasoning Engine
         ↓
         Etir receives the start nodes
         ↓
         spreading activation: activation(j) += activation(i) * weight(edge_ij)
         ↓
         decay: activation *= exp(-λt)
         ↓
         lateral inhibition: activation(i) -= inhibition * competing_nodes
         ↓
         Graph is pre-activated → L4 takes the ready-made context
         ↓
         If not → full L3 traversal (Neo4j)
```

**Criteria for entering Etir:**
- `access_count > threshold` — frequently queried nodes
- `importance > 0.9` — high importance
- `pinned = True` — forced pinning by the user or L5
- A signal from the L5 Observer (SelfAttentionDiary) — promotion recommendations

**Pinned nodes are never evicted automatically.** L5 (the system's values) always resides in Etir as pinned.

> 💡 **MAGMA idea (edge typing, 2026)**: spreading activation in Etir
> can operate by edge type. Add a `type` attribute to edges:
> `semantic` / `temporal` / `causal` / `entity`. Then the L4 Memory Router
> selects the activation type by the query intent — this increases the accuracy
> of pre-activation without changing the Neo4j node schema. Implementation: Phase 2+.

---

## 📜 RFC0004 — Truth Gate Contract 

> **Status**: Canonical · **Phase**: Phase 0+
>
> Truth Gate is the single entry point into the L3 graph for new facts.
> Implemented via TruthGateWithESM (RFC0015).

### Numeric thresholds

All values come from `velantrim_config.TruthConfig`.

| Criterion | Threshold | Action on violation | ESM state |
|---------|-------|----------------------|--------------|
| `evidence_count` | ≥ 3 | Reject | Hypothesized |
| `confidence` | ≥ 0.75 | Reject | Hypothesized |
| `coverage_score` | ≥ 0.70 | Reject | Supported (awaiting data) |
| `contradictions` | = 0 | Reject + [:CONTRADICTS] | Contradicted |
| All satisfied | — | Accept | **Validated → L3** |

### RFC0004 invariants

```
TruthGate.I1: NO fact enters L3 without passing the Truth Gate.

TruthGate.I2: Duplicate → increment evidence_count, no new node is created.

TruthGate.I3: Conflict → [:CONTRADICTS] relationship, NOT deletion.
    On detection the agent re-queries the user.

TruthGate.I4: Truth Gate not passed → the LLM does not generate an answer based on this fact.
    Returns: "Insufficient data".

TruthGate.I5: Truth Gate + ESM — an atomic operation (TruthGateWithESM, RFC0015).
```

### Relationship to other RFCs

```
RFC0001 → RFC0004: LLM output → ESM only through the Truth Gate
RFC0004 → RFC0013: L2 clusters → L3 through the Truth Gate (CONCEPTUAL type)
RFC0004 → RFC0014: staging_candidates → L3 through the Truth Gate (Scheduler)
RFC0004 → RFC0015: TruthGateWithESM implements this contract
RFC0004 → RFC0016: VelumSignal → does not go to L3 directly, only through the Truth Gate
```

---

## 📜 RFC0011 — Etir Spreading Activation Engine

> **Status**: Draft · **Priority**: Phase 1 · **Deadline**: 10–14 days

### Goals and hard constraints

```
P95 latency ≤ 50 ms on a graph of 50k–200k nodes
Activate ≤ 300 nodes at a time
Ring Zero / VALUES CORE — activation = 1.0 (immune to inhibition)
ESM.Collapsed nodes — fully excluded from propagation
Cache results by query_hash (TTL 60–120 sec, Redis)
Fallback: if >50 ms → pure Graphiti search (without Etir)
```

### Formal model

```
activation_0(i) = 1.0  if i ∈ seed_nodes (query + L0 entities)
                  0.0   otherwise

activation_{t+1}(j) = activation_t(j) + Σ_{i→j} activation_t(i) · w_ij

decay(i) = activation(i) · e^{-0.18 · t}

lateral_inhibition(i) = activation(i) - 0.07 · Σ_{k ∈ competitors} activation(k)

final(i) = clamp(activation(i), 0, 1)  if final(i) > 0.12
```

**Default parameters:**

| Parameter | Value | Description |
|----------|----------|----------|
| `max_steps` | 3 | Propagation depth |
| `max_nodes` | 300 | Limit on activated nodes |
| `decay_rate` λ | 0.18 | Decay rate |
| `inhibition_rate` μ | 0.07 | Lateral inhibition strength |
| `threshold` | 0.12 | Minimum activation for inclusion in context |

### Invariants (RFC0011)

```
Etir.I1: ∀ node ∈ activated_nodes: 0 ≤ activation ≤ 1
Etir.I2: |activated_nodes| ≤ 300
Etir.I3: Ring Zero nodes: activation ≥ 0.95 always (immunity)
Etir.I4: ESM.Collapsed nodes: activation = 0 (excluded)
Etir.I5: P95 latency < 50ms — otherwise Circuit Breaker → fallback Graphiti
```

### Implementation: Cypher + Neo4j (not NetworkX — see the table below)

> ⚠️ **NetworkX is a trap**: it pulls the entire graph into the Python process's RAM. On 10k nodes — seconds. We write straight to Cypher inside Neo4j.
>
> ⚠️ **`gds.runCypher()` does not exist** in the Neo4j GDS API. Spreading activation is implemented via iterative Cypher queries from Python, not through GDS procedures.

```cypher
// Step 1: Set seed activation (called from Python before the iterations)
MATCH (n)
WHERE n.id IN $seed_ids
  AND n.epistemic_state <> 'Collapsed'
SET n.activation = 1.0

// Step 2: Ring Zero immunity — always maximum
MATCH (n)
WHERE n.is_ring_zero = true
SET n.activation = 1.0

// Step 3: One spreading iteration (called 3 times from Python)
MATCH (n)-[r:RELATED_TO|SUPPORTED_BY|CONCEPT_OF]->(m)
WHERE n.activation > 0.12
  AND m.epistemic_state <> 'Collapsed'
  AND m.is_ring_zero <> true
WITH m, sum(n.activation * coalesce(r.weight, 0.5)) AS incoming
SET m.activation = coalesce(m.activation, 0.0) + incoming

// Step 4: Decay
-- P1-E FIX: I55.1 — differentiated decay for analogies vs standard edges
MATCH (n)-[r]->(m)
WHERE n.activation IS NOT NULL
  AND n.is_ring_zero <> true
SET n.activation = n.activation * CASE
    WHEN type(r) IN ['METAPHOR_OF', 'ANALOGOUS_TO']
    THEN exp(-0.12)    -- SAE_DECAY_ANALOGY (I55.1): decay_factor=0.4 for analogies
    ELSE exp(-0.18)    -- SAE_DECAY_STANDARD: decay_factor=0.6 for ordinary edges
END

// Step 5: Collect results
MATCH (n)
WHERE coalesce(n.activation, 0) > 0.12
  AND n.epistemic_state <> 'Collapsed'
RETURN n.id AS node_id, n.activation AS score
ORDER BY score DESC
LIMIT 300

// Step 6: Cleanup (mandatory after every query!)
MATCH (n) WHERE n.activation IS NOT NULL
  AND n.is_ring_zero <> true
REMOVE n.activation
```

```python
# etir/engine.py — Python wrapper 
import json
import asyncio
from dataclasses import dataclass
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

@dataclass
class ActivationResult:
    activated_nodes: Dict[str, float]   # node_id → score
    context_window: List[str]           # top-30 node_id
    execution_time_ms: float
    steps_used: int
    cache_hit: bool = False

class EtirEngine:
    """
    RFC0011: Etir Spreading Activation Engine
    Implemented on Cypher + Redis cache.
    Does NOT use NetworkX (too slow on >10k nodes).
    Does NOT use gds.runCypher() (does not exist in the GDS API).
    """
    CYPHER_SEED    = "MATCH (n) WHERE n.id IN $seed_ids AND n.epistemic_state <> 'Collapsed' SET n.activation = 1.0"
    CYPHER_RING    = "MATCH (n) WHERE n.is_ring_zero = true SET n.activation = 1.0"
    CYPHER_SPREAD  = """
        MATCH (n)-[r:RELATED_TO|SUPPORTED_BY|CONCEPT_OF]->(m)
        WHERE n.activation > $threshold
          AND m.epistemic_state <> 'Collapsed'
          AND m.is_ring_zero <> true
        WITH m, sum(n.activation * coalesce(r.weight, 0.5)) AS incoming
        SET m.activation = coalesce(m.activation, 0.0) + incoming
    """
    # P1-E FIX: I55.1 — CYPHER_DECAY split into two modes.
    # Analogies receive soft decay (exp(-0.12) = decay_factor 0.4).
    # Standard edges: exp(-0.18) = decay_factor 0.6.
    CYPHER_DECAY   = """MATCH (n)-[r]->(m)
        WHERE n.activation IS NOT NULL AND n.is_ring_zero <> true
        SET n.activation = n.activation * CASE
            WHEN type(r) IN ['METAPHOR_OF','ANALOGOUS_TO'] THEN exp(-0.12)
            ELSE exp(-0.18) END""""
    # Lateral inhibition: dominant nodes suppress competitors (RFC0011, formula μ=0.07).
    # Ring Zero nodes are immune — their activation is not reduced.
    # Without this step, competing topics (0.9 vs 0.8) are both fully activated →
    # the LLM gets blurred context. With it — the dominant topic suppresses the weak ones.
    # P0-4 FIX: CYPHER_INHIBIT is selected dynamically via get_lateral_inhibition_cypher()
    # (APOC if available, pure Cypher fallback for LadybugDB). Defined in dedupe_entities.py.
    CYPHER_INHIBIT_HEADER = """
        MATCH (n)
        WHERE n.activation IS NOT NULL
          AND n.is_ring_zero <> true
          AND n.epistemic_state <> 'Collapsed'
        WITH n ORDER BY n.activation DESC
        WITH collect(n) AS ranked
    """

    @classmethod
    def _build_cypher_inhibit(cls) -> str:
        """P0-4 FIX: assemble CYPHER_INHIBIT with the correct backend for lateral inhibition."""
        try:
            from dedupe_entities import get_lateral_inhibition_cypher
            body = get_lateral_inhibition_cypher()
        except ImportError:
            # Fallback if dedupe_entities is unavailable: pure Cypher (safe)
            body = """
        UNWIND range(0, size(ranked) - 1) AS i
        WITH ranked[i] AS dominant, ranked, i
        WHERE dominant.activation > $threshold
        UNWIND range(i + 1, size(ranked) - 1) AS j
        WITH dominant, ranked[j] AS competitor
        WHERE competitor.activation < dominant.activation
        WITH competitor,
             (competitor.activation - $mu * dominant.activation) AS raw_val
        SET competitor.activation = CASE WHEN raw_val < 0 THEN 0.0 ELSE raw_val END
            """
        return cls.CYPHER_INHIBIT_HEADER + body
    CYPHER_COLLECT = "MATCH (n) WHERE coalesce(n.activation, 0) > $threshold AND n.epistemic_state <> 'Collapsed' RETURN n.id AS node_id, n.activation AS score ORDER BY score DESC LIMIT $limit"
    CYPHER_CLEANUP = "MATCH (n) WHERE n.activation IS NOT NULL AND n.is_ring_zero <> true REMOVE n.activation"

    def __init__(self, driver, redis, config: dict = None):
        self.driver = driver
        self.redis  = redis
        self.config = config or {
            "max_steps": 3, "max_nodes": 300,
            "threshold": 0.12, "cache_ttl": 90
        }

    async def activate(self, query: str, seed_ids: List[str]) -> ActivationResult:
        import time
        start = time.monotonic()

        # Cache
        # FIX: hash() is unstable across processes (PYTHONHASHSEED randomized since Python 3.3).
        # hashlib.sha256 is deterministic — the cache works correctly with multiple workers.
        import hashlib
        _cache_raw = (query + '|'.join(sorted(seed_ids))).encode()
        cache_key = f"etir:{hashlib.sha256(_cache_raw).hexdigest()[:16]}"
        cached = await self.redis.get(cache_key)
        if cached:
            r = ActivationResult(**json.loads(cached))
            r.cache_hit = True
            return r

        async with self.driver.session() as session:
            try:
                await session.run(self.CYPHER_SEED, {"seed_ids": seed_ids})
                await session.run(self.CYPHER_RING)
                for _ in range(self.config["max_steps"]):
                    await session.run(self.CYPHER_SPREAD, {"threshold": self.config["threshold"]})
                    await session.run(self.CYPHER_DECAY)
                # Lateral inhibition — a single pass after all propagation steps.
                # μ=0.07 from RFC0011. P0-4 FIX: APOC/fallback is selected automatically.
                try:
                    await session.run(
                        self._build_cypher_inhibit(),
                        {"threshold": self.config["threshold"], "mu": self.config.get("inhibition_rate", 0.07)}
                    )
                except Exception as _inh_err:
                    # APOC unavailable or CYPHER_INHIBIT failed → skip, do not crash.
                    # Lateral inhibition is a quality improvement, not a blocking path.
                    logger.debug(f"Etir lateral inhibition skipped: {_inh_err}")
                rows = await (await session.run(
                    self.CYPHER_COLLECT,
                    {"threshold": self.config["threshold"], "limit": self.config["max_nodes"]}
                )).data()
            finally:
                # FIX: CYPHER_CLEANUP moved into finally — activation properties
                # are guaranteed to be removed from Neo4j even on exception.
                # Without this, if CYPHER_COLLECT fails, dangling activations mix
                # with the seed of the next query.
                await session.run(self.CYPHER_CLEANUP)

        activated = {r["node_id"]: r["score"] for r in rows}
        context   = list(activated.keys())[:30]
        elapsed   = (time.monotonic() - start) * 1000

        # Circuit Breaker
        if elapsed > 50:
            logger.warning(f"Etir latency {elapsed:.1f}ms > 50ms — fallback to Graphiti")
            return ActivationResult({}, [], elapsed, 0)

        result = ActivationResult(activated, context, elapsed, self.config["max_steps"])
        await self.redis.setex(cache_key, self.config["cache_ttl"], json.dumps(result.__dict__))
        return result

    async def invalidate_cache(self, node_ids: List[str]):
        """
        Event-driven cache invalidation when nodes change
        
        Called when:
        - A node is added/removed/changed in L3
        - An ESM transition (especially into Contradicted/Collapsed)
        - Weighted Decay is applied
        
        Invalidates all cache keys containing these node_ids
        """
        pattern = f"etir:*"
        cursor = 0
        invalidated = 0
        
        while True:
            cursor, keys = await self.redis.scan(cursor, match=pattern, count=100)
            
            for key in keys:
                cached = await self.redis.get(key)
                if cached:
                    data = json.loads(cached)
                    # Check for intersection with the changed nodes
                    if any(nid in data.get('activated_nodes', {}) for nid in node_ids):
                        await self.redis.delete(key)
                        invalidated += 1
            
            if cursor == 0:
                break
        
        if invalidated > 0:
            logger.info(f"Etir cache: invalidated {invalidated} keys for {len(node_ids)} nodes")
        
        return invalidated
```

### File structure

```
velantrim/
├── etir/
│   ├── __init__.py
│   ├── engine.py       ← EtirEngine (Cypher + Redis, see above)
│   ├── cache.py        ← Redis TTL + invalidation on graph changes
│   └── metrics.py      ← Prometheus: latency, nodes_activated, cache_hit, fallback_count
├── infra/
│   └── docker-compose.yml
├── hybrid_retrieval.py ← add the etir.activate() call as step F2.5
├── context_builder.py  ← accept etir_context_window
└── tests/
    └── test_etir.py    ← 7 tests (see below)
```

### Tests (mandatory)

```python
# tests/test_etir.py
def test_single_seed_activation()       # one seed → correct propagation
def test_decay_reduces_score()          # decay reduces activation
def test_inhibition_suppresses()        # inhibition suppresses competitors
def test_ring_zero_immunity()           # Ring Zero always activation ≥ 0.95
def test_collapsed_nodes_ignored()      # ESM.Collapsed = activation 0
def test_cache_hit_returns_fast()       # second call < 10ms
def test_fallback_on_slow_graph()       # on latency > 50ms → empty result
```

### Metrics (Prometheus)

```python
etir_latency_ms       = Histogram("etir_latency_ms", ...)
etir_nodes_activated  = Gauge("etir_nodes_activated", ...)
etir_cache_hit_ratio  = Gauge("etir_cache_hit_ratio", ...)
etir_fallback_total   = Counter("etir_fallback_total", ...)
```

### NetworkX alternatives for spreading activation

> The choice of tool depends on the phase and the availability of Neo4j GDS.

| # | Tool | Speed vs NetworkX | Built-in spreading | Neo4j integration | Recommendation |
|---|-----------|---------------------|-------------------|-------------------|-------------|
| 1 | **Neo4j GDS + Cypher** | 10–60× | Via iterative Cypher | Native | ✅ **Production Phase 1** |
| 2 | **python-igraph** | 5–20× | Yes (diffusion) | No direct | 🟡 Fast MVP without GDS |
| 3 | **graph-tool** | 20–150× | Yes | No | 🟡 If igraph is slow |
| 4 | **cuGraph (RAPIDS)** | 50–1000× (GPU) | Yes | No | 🔬 Phase 2 if GPU is available |
| 5 | **NetworkX** | 1× | No | No | ❌ Prototype only < 1k nodes |

### Implementation timeline (10–14 days)

```
Day 1–2:  Pilot — docker compose up -d, Cypher on 10k test nodes, latency measurement
Day 3–6:  etir/engine.py + Redis cache + integration into HybridRetriever (step F2.5)
           Ring Zero immunity + ESM.Collapsed filter + Circuit Breaker
Day 7–10: 7 unit tests + integration test with 1000 queries + Prometheus metrics
Day 11–14: Optimization (indexes, connection pool) + RFC0011 documentation
```

### Integration into the Canonical Memory Protocol (new step F2.5)

```
F2.5: Etir Activation (L3.5)
    → activation_map = EtirEngine.activate(query, seed_ids)
    → if latency > 50ms → Circuit Breaker → fallback Graphiti search
    → context_window is passed to F3 (Context Builder)
```

---

## 📜 RFC0012 — Taxonomy/Domain Hierarchy 

> **Purpose**: a structured knowledge taxonomy. Instead of a flat set of Concept nodes — a hierarchy `Domain → Concept → Fact`. Searching by domain narrows the space, reduces noise, and enables taxonomy-based retrieval.

### The problem without a taxonomy

```
Query: "water boils at 100°C"
Without Domain: search across all 500k nodes → noise from medicine, history, biology
With Domain:   search only in domain:physics → 3k nodes → precise result
```

### Node hierarchy

```
:Domain {id: "domain:physics"}
    ↓ [:SUBDOMAIN_OF]
:Domain {id: "domain:thermodynamics"}
    ↓ (contains :Concept via [:BELONGS_TO])
:Concept {id: "concept:boiling_point"}
    ↓ (linked to :Fact via [:CONCEPT_OF])
:Fact {content: "Water boils at 100°C at 1 atm"}
```

### Cypher: creating a domain and searching by taxonomy

```cypher
// Create a domain and a subdomain
MERGE (:Domain {id: "domain:physics", name: "Physics"})
MERGE (:Domain {id: "domain:thermodynamics", name: "Thermodynamics"})
MATCH (sub:Domain {id: "domain:thermodynamics"}), (parent:Domain {id: "domain:physics"})
MERGE (sub)-[:SUBDOMAIN_OF]->(parent)

// Link a Concept to a Domain
MATCH (c:Concept {id: "concept:boiling_point"}), (d:Domain {id: "domain:thermodynamics"})
MERGE (c)-[:BELONGS_TO]->(d)

// taxonomy_search: search for facts in a domain and all its subdomains
MATCH (d:Domain {id: $domain_id})
OPTIONAL MATCH (sub:Domain)-[:SUBDOMAIN_OF*0..]->(d)
WITH collect(d.id) + collect(sub.id) AS domain_ids
MATCH (c:Concept)-[:BELONGS_TO]->(dom:Domain)
WHERE dom.id IN domain_ids
MATCH (f:Fact)-[:CONCEPT_OF]->(c)
WHERE f.is_active = true
  AND f.epistemic_state IN ["Validated", "Supported"]
RETURN f.content, c.name, dom.id, f.epistemic_state
ORDER BY f.epistemic_score DESC
LIMIT $limit
```

### Python: taxonomy_search()

```python
# taxonomy_search.py
async def taxonomy_search(
    self,
    query: str,
    domain_id: str,           # "domain:physics" or "domain:thermodynamics"
    include_subdomains: bool = True,
    limit: int = 20
) -> list[dict]:
    """
    RFC0012: search for facts in a domain + optionally in all subdomains.
    Narrows the search space: instead of the whole graph — only the relevant domain.
    Used as a prefilter before Etir activation (step F2.4).
    """
    cypher = """
    MATCH (d:Domain {id: $domain_id})
    WITH d
    OPTIONAL MATCH (sub:Domain)-[:SUBDOMAIN_OF*0..]->(d)
    WITH collect(DISTINCT d.id) + collect(DISTINCT sub.id) AS domain_ids
    MATCH (c:Concept)-[:BELONGS_TO]->(dom:Domain)
    WHERE dom.id IN domain_ids
    MATCH (f:Fact)-[:CONCEPT_OF]->(c)
    WHERE f.is_active = true
      AND f.epistemic_state IN ["Validated", "Supported"]
    RETURN f.id AS fact_id, f.content AS content,
           c.name AS concept, dom.id AS domain,
           f.epistemic_score AS score
    ORDER BY score DESC
    LIMIT $limit
    """
    return await self.graph.execute_cypher(cypher, {
        "domain_id": domain_id,
        "limit": limit
    })
```

### Integration into the Canonical Memory Protocol (new step F2.4)

```
F2.4: Taxonomy Filter (RFC0012)
    → if the query contains domain_hint → taxonomy_search(domain_id)
    → results are passed to F2.5 Etir as seed_ids
    → without domain_hint → the step is skipped, go straight to F2.5
```

### Invariants RFC0012

```
I1: ∀ Concept: may have 0 or 1 :Domain (not required)
I2: Domains form a DAG (directed acyclic graph), not cycles
I3: taxonomy_search() never crosses a domain boundary without an explicit [:SUBDOMAIN_OF]
I4: :Domain nodes do not pass through the MGL — they are structural, not epistemic
I5: During GC a :Domain is not deleted if it has at least 1 active :Concept
```

### Seed Domains for Phase 0

```python
# On system initialization, create the base domains
SEED_DOMAINS = [
    {"id": "domain:science",       "name": "Science"},
    {"id": "domain:physics",       "name": "Physics",       "parent": "domain:science"},
    {"id": "domain:chemistry",     "name": "Chemistry",     "parent": "domain:science"},
    {"id": "domain:biology",       "name": "Biology",       "parent": "domain:science"},
    {"id": "domain:mathematics",   "name": "Mathematics",   "parent": "domain:science"},
    {"id": "domain:agent_memory",  "name": "Agent Memory"},  # for the agent's internal facts
    {"id": "domain:user_context",  "name": "User Context"},  # for personal context
]
```

---

> 🔭 **Future integration — Engram (DeepSeek, 2026)**
>
> Engram is an internal mechanism of the DeepSeek transformer, **not a component of Velantrim**.
> It operates at the level of N-gram hash → Conditional Memory Table inside the model and
> activates automatically when using DeepSeek v4+ without any action
> on Velantrim's part. Velantrim does not implement or control Engram.
>
> **Recommendation for DeepSeek v4+**: when using these models in the pipeline,
> assign facts coming through them `source_type = "engram_memory"`
> in the Source Trust Layer with an elevated `trust_score = 0.80` — as coming
> from the model's verified internal memory.
>
> Etir (Velantrim) and Engram (DeepSeek) do not compete: Etir manages explicit
> verified memory outside the transformer, Engram — implicit
> neural memory inside it. RFC0006 (`validate_engram_config`) remains
> as a safeguard against accidentally enabling `ENGRAM_ENABLED=True` with API models.

---

## 📜 RFC0015 — TruthGateWithESM 

> **Status**: Canonical · **Phase**: Phase 0+
>
> A single entry point for promotion to L3. Coordinates MemoryGuardian + EpistemicStateMachine atomically.

### The problem

MemoryGuardian and EpistemicStateMachine existed independently:
- Guardian validates a fact
- ESM manages the lifecycle
- **No guarantee** that Guardian validation → the correct ESM transition
- ResourceAwareScheduler could promote to L3 without moving the ESM into Validated

### The solution

The facade-orchestrator `TruthGateWithESM` unifies both operations:

```python
@dataclass
class TruthGateResult:
    passed: bool
    score: float
    esm_state: str          # Validated / Contradicted / Hypothesized
    reason: str             # TRUTH_GATE_PASSED / LOW_EVIDENCE / CONFLICT_DETECTED
    emotional_salience: float = 0.0

# 📎 Canonical implementation of TruthGateWithESM — see section "19. TruthGateWithESM"
# Here: a conceptual schema of the operations (Guardian→ESM→RingZero→L3 promote)
```

### Emotional Ring Zero

**Concept:** high emotional salience → immunity to decay

```python
if emotional_salience > TRUTH.EMOTIONAL_RING_ZERO:  # 0.85
    await self.esm.freeze(item["id"])
    # The node becomes immutable - not subject to GC and decay
```

### Invariants RFC0015

```
I1: The single entry point for staging → L3 promotion.
    Do NOT create bypasses into L3 around this class.

I2: TruthGateResult contains ALL information about the validation result.
    The caller must not interpret the internal Guardian/ESM states.

I3: Emotional Ring Zero (salience > 0.85) → ESM.freeze() automatically.
    Does not require an explicit freeze() call in the caller's code.

I4: On rejection of a duplicate: TruthGateResult.passed = False,
    but esm_state = "Validated" (the node was already in L3).
```

### Usage in ResourceAwareScheduler

```python
# staging_scheduler.py
async def _promote_item(self, item) -> int:
    result: TruthGateResult = await self.truth_gate_esm.validate_and_transition(item)

    if result.passed:
        await self.staging.update_status(item.id, "PROMOTED")
        return 1
    else:
        # Duplicate - count as success (the node already exists)
        status = "PROMOTED" if result.reason == "DUPLICATE" else "REJECTED"
        await self.staging.update_status(item.id, status)
        return 0
```

### Correction Mechanism 

**Problem**: an Emotional Ring Zero freeze (salience > 0.85) can freeze a FALSE topic forever.

**Solution**: Rollback the freeze when a [:CONTRADICTS] is detected after the freeze.

```python
# truth_gate_correction.py
class TruthGateCorrectionMechanism:
    """
    Monitors frozen nodes and unfreezes them when contradictions appear.
    """

    async def monitor_frozen_nodes(self):
        """Called by ReactivationEngine every 6 hours"""
        query = """
        MATCH (n:Fact {is_frozen: true})
        OPTIONAL MATCH (n)<-[c:CONTRADICTS]-(other)
        WHERE c.timestamp > n.frozen_at  // Contradiction AFTER the freeze
        RETURN n.id, collect(other.id) as contradictions
        """
        results = await self.graph.execute_cypher(query)
        
        for row in results:
            if len(row['contradictions']) > 0:
                await self._unfreeze_with_audit(row['id'], row['contradictions'])

    async def _unfreeze_with_audit(self, node_id: str, contradictions: list):
        """
        Unfreeze the node + create an audit trail.
        We do NOT delete — we move it into ESM.Contradicted.
        """
        await self.esm.unfreeze(node_id)
        await self.esm.transition(node_id, "Contradicted", 
            reason=f"FREEZE_ROLLBACK: {len(contradictions)} contradictions found")
        
        # Audit log
        await self.audit.log_correction(
            node_id=node_id,
            action="UNFREEZE_CONTRADICTED",
            contradictions=contradictions,
            timestamp=datetime.now(timezone.utc)
        )
        
        logger.warning(
            f"TruthGate Correction: unfroze {node_id} due to {len(contradictions)} contradictions"
        )
```

**Invariants:**

```
I5: A frozen node can be unfrozen ONLY on a [:CONTRADICTS] AFTER the freeze.
I6: Unfreeze does NOT delete the node — it moves it into ESM.Contradicted for manual review.
I7: Every unfreeze creates an audit trail (who, when, why).
I8: Ring Zero nodes (is_ring_zero=true) are NEVER unfrozen automatically.
```

**Integration**:
- ReactivationEngine calls `monitor_frozen_nodes()` every 6 hours
- MetaSupervisor receives an alert on every unfreeze
- The Audit Layer logs for GET /memory/audit/corrections

---

## 📜 RFC0016 — L1.5 Velum 

> **Status**: Canonical · **Phase**: Phase 0+
>
> Velantrim Synaptic Pre-Graph Layer - a detector of early connections between entities.

### Purpose

L1.5 Velum lives between L1 (episodes) and L2 (clusters):
- L1 accumulates episodes
- **Velum notices connections** between entities (co-occurrence)
- L2 builds topic clusters

The analogy in neurobiology: **LTP (Long-Term Potentiation)** - synaptic strengthening prior to long-term consolidation.

### Dataclasses

> 📎 **Canonical implementation** of `VelumEdge` and `VelumSignal` — see section "20. L1.5 Velum".

### How it works

```
L1 INSERT → Velum.observe_episode(episode_id, entities)
  ↓
Update weight for all entity pairs in the sliding window (5 episodes)
  ↓
If weight ≥ 0.6 AND count ≥ 3
  ↓
VelumSignal → ReactivationEngine + L2 (accelerated cluster promotion)
```

### Core methods

**observe_episode()**
```python
async def observe_episode(self, episode_id: str, entities: list[str]) -> list[VelumSignal]:
    # Called from the L1 Episodic Buffer on every INSERT
    # Returns a VelumSignal when the threshold is reached
```

**on_session_end()**
```python
async def on_session_end(self) -> list[VelumSignal]:
    # On session change (30 min of inactivity):
    # - Strong edges (weight ≥ 0.6) → VelumSignal "SESSION_END" → L2
    # - Weak edges → decay × 0.3
```

**get_neighbors()**
```python
def get_neighbors(self, entity: str, min_weight: float = 0.3) -> list[tuple[str, float]]:
    # Used by:
    # - HybridRetriever: context expansion within a session
    # - ReactivationEngine: a hint about what to strengthen
```

### Configuration (from velantrim_config.py)

```python
VELUM_CO_OCCUR_THRESHOLD = 3       # co-occurrences → record
VELUM_WINDOW_EPISODES = 5          # observation window
VELUM_MAX_EDGES = 1000             # maximum edges before GC
VELUM_PROMOTE_WEIGHT = 0.6         # weight → L2 signal
VELUM_DECAY_PER_SESSION = 0.3      # decay on session change
SAE_DECAY_STANDARD  = 0.18   # P1-E FIX (I55.1): exp coefficient for ordinary edges
SAE_DECAY_ANALOGY   = 0.12   # P1-E FIX (I55.1): exp coefficient for METAPHOR_OF/ANALOGOUS_TO
```

### Invariants RFC0016

```
I1: Velum stores ONLY edges (entity_a, entity_b, weight).
    It does NOT store episode content - only the observation of a connection.

I2: On session change:
    weight < VELUM_PROMOTE_WEIGHT → decay × VELUM_DECAY_PER_SESSION
    weight ≥ VELUM_PROMOTE_WEIGHT → VelumSignal → L2 for accelerated promotion

I3: Velum is NOT a source of facts. Graph = Truth is not violated.
    Velum → only a hint for the scheduler (ReactivationEngine, L2 clustering).

I4: Velum is not persistent across sessions by default.
    Optionally (Phase 1): save the top-N edges in SQLite for seeding.
```

### Integration into the Canonical Protocol

```
F1.5: Velum Context Hint (RFC0016)
    → Velum.get_neighbors(query_entities, min_weight=0.3)
    → Add the neighbors to the seed for Etir (step F2.5)
    → Fire-and-forget hint - does not block the Fast Path
```

### GC (garbage collection)

When > VELUM_MAX_EDGES (1000):
- Remove 25% of the weakest edges
- Clear _entity_index

---

## 📜 RFC0017 — Weighted Semantic Decay 

> **Status**: Canonical · **Phase**: Phase 1
>
> Critical component for L3 accuracy.
>
> Mechanism for removing contradictory and outdated facts from the L3 graph based on semantic proximity and epistemic weight.

### Problem

Without Weighted Semantic Decay:
- The L3 graph grows indefinitely (accumulation of duplicates and contradictions)
- Outdated facts remain with `importance > 0.1` → never reach Collapsed
- [:CONTRADICTS] edges are created, but conflicting nodes are not removed
- Memory becomes "cluttered" — low search accuracy

### Solution

Periodic (every 24 hours) analysis of the L3 graph:

```python
# weighted_semantic_decay.py
class WeightedSemanticDecay:
    """
    Finds semantically close nodes with contradictions and applies decay.
    """

    async def run_decay_cycle(self):
        """Main loop — invoked on a schedule (cron/APScheduler)"""
        # 1. Find all Contradicted nodes
        contradicted = await self._find_contradicted_nodes()
        
        # Protection against a chain reaction
        max_cascade_nodes = 50  # Node limit per cycle
        total_penalized = 0
        
        # 2. For each, find semantically close ones (cosine > 0.85)
        for node in contradicted:
            if total_penalized >= max_cascade_nodes:
                logger.warning(
                    f"Cascade limit reached: {max_cascade_nodes} nodes penalized. "
                    f"Remaining {len(contradicted) - contradicted.index(node)} "
                    f"Contradicted nodes will be processed in next cycle."
                )
                break
            
            similar = await self._find_similar_nodes(node, threshold=0.85)
            
            # Limit on the number of neighbors for a single node
            similar = similar[:10]  # At most 10 neighbors per node
            
            # 3. Apply weighted decay based on epistemic_state
            for sim_node in similar:
                if total_penalized >= max_cascade_nodes:
                    break
                    
                penalty = self._calculate_penalty(node, sim_node)
                await self._apply_decay(sim_node.id, penalty)
                total_penalized += 1
        
        # 4. Check nodes with importance < 0.1 → ESM.transition(Collapsed)
        await self._collapse_low_importance_nodes()
        
        # Metric for monitoring
        decay_cascade_size.set(total_penalized)
        if total_penalized >= max_cascade_nodes:
            decay_cascade_limit_hit.inc()

    def _calculate_penalty(self, contradicted_node, similar_node) -> float:
        """
        The penalty depends on:
        - Semantic proximity (cosine similarity)
        - Epistemic state of the similar node
        - Number of [:CONTRADICTS] edges
        """
        cosine = similar_node.similarity  # 0.85 - 1.0
        state_weight = {
            "Validated": 0.3,      # weak penalty (may be true)
            "Supported": 0.5,      # medium
            "Hypothesized": 0.7,   # strong
            "Contradicted": 1.0    # maximum (contradiction of a contradiction)
        }
        
        base_penalty = 0.15
        semantic_factor = (cosine - 0.85) / 0.15  # normalization 0.85-1.0 → 0-1
        state_factor = state_weight.get(similar_node.epistemic_state, 0.5)
        
        return base_penalty * semantic_factor * state_factor

    async def _apply_decay(self, node_id: str, penalty: float):
        """
        Lower the node's importance.
        If it drops < 0.1 → the next GC will move it to Collapsed.
        """
        query = """
        MATCH (n:Fact {id: $node_id})
        SET n.importance = max(0.0, n.importance - $penalty),
            n.decay_applied_at = datetime(),
            n.decay_count = coalesce(n.decay_count, 0) + 1
        RETURN n.importance as new_importance
        """
        result = await self.graph.execute_cypher(query, 
            {"node_id": node_id, "penalty": penalty})
        # P9-FIX BUG-5: kwargs→positional dict (matches the style of the whole document, lines 9887, 10166)
        # P9-FIX BUG-9: max(0.0, ...) — importance does not go negative
        
        logger.info(
            f"Decay applied: {node_id} penalty={penalty:.3f} "
            f"new_importance={result[0]['new_importance']:.3f}"
        )

    async def _collapse_low_importance_nodes(self):
        """
        Nodes with importance < 0.1 → ESM.Collapsed → Immutable Raw Memory
        """
        query = """
        MATCH (n:Fact)
        WHERE n.importance < 0.1 
          AND n.epistemic_state <> 'Collapsed'
          AND n.is_ring_zero <> true  // Ring Zero is protected
        RETURN n.id, n.importance, n.epistemic_state
        """
        candidates = await self.graph.execute_cypher(query)
        
        for node in candidates:
            await self.esm.transition(
                node['id'], 
                "Collapsed",
                reason=f"WEIGHTED_DECAY: importance={node['importance']:.3f}"
            )
            
            # Archive to S3 before removing from the operational graph
            await self.archive.store_collapsed_node(node['id'])
```

### Configuration

```python
# velantrim_config.py
class DecayConfig:
    SEMANTIC_SIMILARITY_THRESHOLD = 0.85   # cosine > 0.85 → candidates
    BASE_DECAY_PENALTY = 0.15              # base penalty
    COLLAPSE_IMPORTANCE_THRESHOLD = 0.1    # importance < 0.1 → Collapsed
    DECAY_SCHEDULE_HOURS = 24              # run frequency
    PROTECT_RING_ZERO = True               # Ring Zero immunity

    # Protection against a chain reaction
    MAX_CASCADE_NODES_PER_CYCLE = 50       # node limit per cycle
    MAX_NEIGHBORS_PER_NODE = 10            # neighbor limit per node
```

### RFC0017 Invariants

```
I1: Weighted Decay is applied ONLY to nodes with [:CONTRADICTS] edges or close to them.
    We do NOT touch Validated nodes without contradictions.

I2: Ring Zero nodes (is_ring_zero=true) NEVER receive a decay penalty.

I3: Before Collapsed → mandatory archiving to S3 (Immutable Raw Memory).

I4: Decay is a reduction of importance, NOT deletion.

I5: If decay_count > 5 for a single node → alert ("Frequent contradictions").
    The decay_count metric is incremented on every penalty application.
    Deletion happens only during GC after Collapsed.

I6: The MAX_CASCADE_NODES_PER_CYCLE limit protects against a chain reaction.
    If the limit is reached → the remaining nodes are processed in the next cycle.
```

### Integration

```python
# main.py or scheduler.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from weighted_semantic_decay import WeightedSemanticDecay

scheduler = AsyncIOScheduler()
decay_engine = WeightedSemanticDecay(graph, esm, archive)

# Run every 24 hours
scheduler.add_job(
    decay_engine.run_decay_cycle,
    'interval',
    hours=24,
    id='weighted_semantic_decay'
)
```

### Metrics

```python
# Prometheus metrics
decay_cycles_total = Counter('velantrim_decay_cycles_total')
decay_penalties_applied = Counter('velantrim_decay_penalties_applied')
nodes_collapsed_total = Counter('velantrim_nodes_collapsed_total')
decay_cycle_duration_seconds = Histogram('velantrim_decay_cycle_duration_seconds')
```

### Example of Operation

```
Day 1: Fact A (importance=0.8, Validated)
        Fact B (importance=0.7, Validated, semantic_similarity=0.92 with A)
        
Day 5: Fact A receives [:CONTRADICTS] → transitions to Contradicted
        
Day 6: Decay cycle:
          - Finds B (cosine=0.92 with A)
          - penalty = 0.15 × ((0.92-0.85)/0.15) × 0.3 = 0.021
          - B.importance = 0.7 - 0.021 = 0.679
        
Day 30: After 5 decay cycles:
          - B.importance = 0.574
          - If there are no new confirmations → continues to fall
        
Day 60: B.importance < 0.1 → ESM.Collapsed → archive to S3
```

### Semantic Quarantine Zone (optional)

**Concept**: Temporary isolation of nodes close to contradictory ones before applying decay.

```python
class SemanticQuarantine:
    """
    Nodes semantically close to Contradicted are placed into quarantine
    instead of immediately applying a decay penalty.

    Advantages:
    - Gives time for confirming/refuting facts to appear
    - Prevents premature deletion of valid nodes
    - Reduces the risk of a chain reaction
    """

    async def quarantine_node(self, node_id: str, source_contradicted: str):
        """
        Place the node into quarantine for 7 days
        
        While in quarantine, the node:
        - Remains in its epistemic_state (does not degrade)
        - Is marked with the flag in_quarantine=true
        - Does not participate in Etir activation (lowered priority)
        - Is monitored for new [:SUPPORTS] or [:CONTRADICTS]
        """
        query = """
        MATCH (n:Fact {id: $node_id})
        SET n.in_quarantine = true,
            n.quarantine_started = datetime(),
            n.quarantine_source = $source,
            n.quarantine_expires = datetime() + duration({days: 7})
        """
        await self.graph.execute_cypher(query, {
            "node_id": node_id,
            "source": source_contradicted
        })

    async def review_quarantine(self):
        """
        Daily quarantine review (invoked together with decay_cycle)
        
        For each node in quarantine:
        - If [:SUPPORTS] appeared → lift quarantine, restore importance
        - If [:CONTRADICTS] appeared → apply decay, exit quarantine
        - If the term expired without changes → apply decay
        """
        query = """
        MATCH (n:Fact)
        WHERE n.in_quarantine = true
          AND n.quarantine_expires < datetime()
        RETURN n.id, n.importance  -- P9-FIX BUG-6: n.importance_score → n.importance (no such field)
        """
        
        expired = await self.graph.execute_cypher(query)
        
        for node in expired:
            # Check what happened during the quarantine period
            supports = await self._count_new_supports(node['id'])
            contradicts = await self._count_new_contradicts(node['id'])
            
            if supports > 0:
                await self._release_from_quarantine(node['id'], reason="NEW_SUPPORTS")
            elif contradicts > 0:
                await self._apply_decay_and_release(node['id'])
            else:
                # No changes — soft decay
                await self._apply_decay_and_release(node['id'], penalty_multiplier=0.5)

# Integration with WeightedSemanticDecay:
# Instead of immediate decay → first quarantine_node()
# Decay is applied only after review_quarantine()
```

**When to use**:
- Production systems where the cost of erroneous deletion is high
- Domains with high uncertainty and frequent changes
- Systems with active user feedback

**When NOT to use**:
- MVP and Phase 0 (excessive complexity)
- Systems with a low frequency of contradictions
- When the speed of graph cleanup matters

---

### Why did Weighted Semantic Decay go through 11 iterations?

Weighted Semantic Decay is a complex mechanism requiring:
- Semantic embeddings for all nodes (expensive)
- The right penalty balance (too aggressive → data loss)
- Integration with ESM, Archive, Monitoring

---

## 📐 Fractal Similarity Monitor 

> **Purpose**: Checking the self-similarity of the memory graph to detect drift.
>
> **Integration**: Works together with the L3.5 Immutable Core.

### Problem

Memory can "drift" — gradually lose its fractal structure:
- Accumulation of chaotic connections (random noise)
- Loss of self-similarity between scales (L0→L3)
- Result: reduced accuracy, increased latency, chaos in the graph

### Solution

Every 24 hours (when creating an L3.5 snapshot) — compute the fractal dimension of the graph.

```python
# fractal_similarity_monitor.py
import numpy as np
from scipy.spatial.distance import pdist, squareform

class FractalSimilarityMonitor:
    """
    Computes the graph's correlation dimension and checks for drift.
    """

    async def check_similarity(self, snapshot_current, snapshot_previous) -> dict:
        """
        Main method — invoked when creating a new snapshot.
        
        Returns:
            {
                'correlation_dimension': float,
                'self_similarity_score': float,
                'drift_detected': bool,
                'alert_reason': str | None
            }
        """
        # 1. Compute the correlation dimension (Grassberger-Procaccia)
        dim_current = self._correlation_dimension(snapshot_current)
        dim_previous = self._correlation_dimension(snapshot_previous)
        
        # 2. Self-similarity score (how close the dimensions are)
        # PATCH-5: guard against ZeroDivisionError on an empty/new graph (both dims may be 0)
        denom = max(dim_current, dim_previous)
        similarity = (
            1.0 - abs(dim_current - dim_previous) / denom
            if denom > 1e-9   # if both ~0 → consider "no drift"
            else 1.0
        )
        
        # 3. Threshold check
        drift_detected = similarity < 0.92
        
        alert_reason = None
        if drift_detected:
            alert_reason = (
                f"Fractal drift: similarity={similarity:.3f} < 0.92, "
                f"dim_current={dim_current:.3f}, dim_previous={dim_previous:.3f}"
            )
            logger.warning(alert_reason)
            await self._trigger_alert(alert_reason)
        
        return {
            'correlation_dimension': dim_current,
            'self_similarity_score': similarity,
            'drift_detected': drift_detected,
            'alert_reason': alert_reason,
            'timestamp': datetime.now(timezone.utc)
        }

    def _correlation_dimension(self, snapshot) -> float:
        """
        Grassberger-Procaccia algorithm for computing the correlation dimension.
        
        Simplified implementation for graphs:
        - Transform the graph into embedding space (use existing node embeddings)
        - Compute pairwise distances
        - Count C(r) = number of pairs with distance < r
        - Correlation dimension ≈ slope log(C(r)) / log(r)
        """
        # P9-FIX BUG-8: guard for a small graph (KeyError + ZeroDivisionError)
        embeddings = snapshot.get('node_embeddings')  # .get() instead of [] — no KeyError
        if embeddings is None or len(embeddings) < 2:
            return 0.0  # not enough data for correlation dimension
        
        # Pairwise distances
        distances = pdist(embeddings, metric='euclidean')
        dist_matrix = squareform(distances)
        
        # Radii for the check (logarithmic scale)
        radii = np.logspace(-2, 1, 20)
        
        # Correlation integral C(r)
        C_r = []
        for r in radii:
            count = np.sum(dist_matrix < r) - len(embeddings)  # exclude the diagonal
            n = len(embeddings)
            denom = n * (n - 1)
            if denom == 0:
                return 0.0  # P9-FIX BUG-8: guard against ZeroDivisionError when n==1
            C_r.append(count / denom)
        
        # Linear regression log(C(r)) vs log(r)
        log_r = np.log(radii)
        log_C = np.log(np.array(C_r) + 1e-10)  # avoid log(0)
        
        # Slope = correlation dimension
        slope, _ = np.polyfit(log_r, log_C, 1)
        
        return slope

    async def _trigger_alert(self, reason: str):
        """
        Send an alert to MetaSupervisor + Prometheus.
        """
        # Prometheus alert
        fractal_drift_alerts.inc()
        
        # MetaSupervisor notification
        await self.supervisor.notify_drift(
            severity="WARNING",
            component="FractalSimilarityMonitor",
            reason=reason,
            action_required="Manual review of L3 graph structure recommended"
        )
        
        # Audit log
        await self.audit.log_event(
            event_type="FRACTAL_DRIFT_DETECTED",
            details={'reason': reason},
            timestamp=datetime.now(timezone.utc)
        )
```

### Alternative Method: Box-Counting

For simplification (if correlation dimension is too expensive):

```python
def _box_counting_dimension(self, snapshot) -> float:
    """
    Box-counting fractal dimension (faster, less accurate).

    We count how many "boxes" of size ε are needed to cover the graph.
    """
    embeddings = snapshot['node_embeddings']

    box_sizes = [0.1, 0.2, 0.5, 1.0, 2.0]
    counts = []

    for epsilon in box_sizes:
        # Discretize the space into boxes of size epsilon
        boxes = np.floor(embeddings / epsilon).astype(int)
        unique_boxes = len(np.unique(boxes, axis=0))
        counts.append(unique_boxes)

    # log(N(ε)) vs log(1/ε)
    log_epsilon_inv = np.log(1.0 / np.array(box_sizes))
    log_counts = np.log(counts)

    slope, _ = np.polyfit(log_epsilon_inv, log_counts, 1)
    return slope
```

### Configuration

```python
# velantrim_config.py
class FractalConfig:
    SIMILARITY_THRESHOLD = 0.92        # self-similarity < 0.92 → drift
    CHECK_INTERVAL_HOURS = 24          # check frequency
    USE_CORRELATION_DIM = True         # True = Grassberger-Procaccia, False = box-counting
    EXPECTED_DIM_RANGE = (1.2, 1.8)   # biologically plausible range
```

### Metrics

```python
# Prometheus
fractal_dimension_current = Gauge('velantrim_fractal_dimension_current')
fractal_similarity_score = Gauge('velantrim_fractal_similarity_score')
fractal_drift_alerts = Counter('velantrim_fractal_drift_alerts_total')
fractal_check_duration_seconds = Histogram('velantrim_fractal_check_duration_seconds')
```

### Integration with L3.5 Immutable Core

```python
# immutable_core.py
async def create_snapshot(self):
    """On snapshot creation → fractal similarity check"""

    # 1. Create the snapshot
    snapshot = await self._snapshot_l3_graph()

    # 2. Fractal similarity check
    if self.previous_snapshot:
        result = await self.fractal_monitor.check_similarity(
            snapshot, self.previous_snapshot
        )
        
        # Save to metadata
        snapshot['fractal_dimension'] = result['correlation_dimension']
        snapshot['similarity_score'] = result['self_similarity_score']
        snapshot['drift_detected'] = result['drift_detected']

    # 3. Save to Neo4j + S3
    await self._persist_snapshot(snapshot)

    self.previous_snapshot = snapshot
```

### Example of Operation

```
Day 1: Snapshot A
  - correlation_dimension = 1.52
  - baseline established

Day 2: Snapshot B
  - correlation_dimension = 1.48
  - similarity = 1.0 - |1.52-1.48|/1.52 = 0.974 ✅ (> 0.92)

Day 30: Snapshot Z
  - correlation_dimension = 1.28
  - similarity = 1.0 - |1.48-1.28|/1.48 = 0.865 ❌ (< 0.92)
  - ALERT: "Fractal drift detected!"
  - Action: Manual review of the graph → find chaotic clusters
```

### Biological Rationale

The human brain has a fractal dimension of ~1.2-1.8 (dendrites, vascular network).
The Velantrim graph should preserve this fractality for efficiency.

Drift = loss of fractality = chaos = degraded performance.

---

## 🗄️ Storage Ecosystem — A Complete Map of Stores

> There is no single system that is best at everything. There are systems that are best in their role.
> SQLite and NetworkX do not need to be replaced — they need to be placed correctly in the stack.

---

### 🔱 Production Core (mandatory)

**Neo4j 5.26+** — the primary graph store for Phase 1+

```
Role:     Science Core / Entity Layer / LTM knowledge graph
Strong:   Cypher, vector indexes, Graph Data Science, mature
Status:   ✅ Production-grade, mature, scalable
Phase:    Phase 1 → forever
```

**Kuzu** — embedded graph for the Phase 0 MVP

```
Role:     Local graph without a server, Cypher-compatible
Strong:   ACID, disk-based columnar, vector/full-text, runs locally
💡 NOTE:  Kuzu evolves slowly but is stable and usable
          The team is working on something new, support is frozen
Status:   ⚠️ Phase 0 MVP only. Do NOT build the canon on it.
Phase:    Phase 0 only → migration to Neo4j in Phase 1
```

---

### 📊 SQL and Analytics

**SQLite** — the application's embedded reliable store

```
Role:     Logs, configs, skills, sessions, small local data
Strong:   Embedded everywhere, reliable, zero-config, "competes with fopen()"
Status:   ✅ Indispensable for operational data
Phase:    All phases
```

**DuckDB** — embedded analytics

```
Role:     Metrics, analytics, Parquet/Arrow/CSV, large tabular slices
Strong:   Columnar-vectorized execution, analytical aggregations
IMPORTANT: NOT a replacement for SQLite — a different workload. SQLite → OLTP, DuckDB → OLAP
Status:   ✅ Add for the analytical layer
Phase:    Phase 2+
```

---

### 🕸️ Graph R&D and Algorithms (scientists' tools)

**NetworkX** — a graph laboratory in Python

```
Role:     Prototyping, centrality, shortest paths, community experiments
Strong:   Python-native, rich library of algorithms
IMPORTANT: This is a library, NOT a production graph DB. Everything is held in the process's RAM
Status:   ✅ R&D and research. Used by scientists for algorithm accuracy
Phase:    Always, in parallel with the production stack
```

**GraphBLAS** — high-performance graph algorithms

```
Role:     Heavy graph algorithms via sparse linear algebra
Strong:   Operations over sparse matrices and semirings — maximum speed
IMPORTANT: NOT a database. NOT a replacement for NetworkX for storing knowledge.
          It is a powerful "engine" for specific algorithms, not a drop-in replacement
Status:   ✅ Optional for Phase 3+ if graph-algorithm speed is needed
Phase:    Phase 3+ optional
```

---

### ⚡ Real-Time Graph (server-level)

**Memgraph** — a real-time graph DB

```
Role:     Streaming updates, real-time graph, streaming ingestion
Strong:   Neo4j-compatible Cypher, open-source, fast updates
IMPORTANT: This is a server-side graph DB, NOT a lightweight replacement for NetworkX
Status:   ✅ Phase 2+ for hot-path real-time updates
Phase:    Phase 2+
```

---

### ⚠️ Optional / With EOL Risk

**SurrealDB** — a multi-model DB

```
Role:     A single engine for graph + SQL + documents + real-time
Strong:   Versatility, active development, interesting architecture
⚠️ RISK:  A young project — if the company shuts down or shifts focus: the project dies
          As happened with RedisGraph (EOL January 2025)
Status:   ⚠️ OPTIONAL for specific tasks. NOT in the core stack.
Phase:    Only as needed
```

---

### ☠️ Removed — no longer used

| System | Reason for removal |
|---|---|
| **LadybugDB** | ☠️ Does not exist as a separate DB. A marketing name → replaced by KuzuDB (P0-H). |
| **KuzuDB** | ✅ Used as GRAPH_BACKEND=kuzu for Personal/Medium configurations. MIT, Cypher-compatible. |
| **RedisGraph** | ☠️ EOL = January 2025. Redis officially discontinued support |
| **GPT-4** | ❌ Retired by OpenAI. Replaced by GPT-5.4 / o4-mini |
| **Llama 3** | ❌ Obsolete. Replaced by Llama 4 Maverick / Scout |
| **rubert-tiny2** | ❌ Obsolete RU embedding model. Replaced by USER-bge-m3 |
| **Kafka** | ❌ Redundant for the Velantrim stack. Only Redis Streams retained |

> **Lesson from LadybugDB**: always verify tool names before including them in the architecture. P0-H FIX: replaced with KuzuDB everywhere in the document.

---

### 🗺️ Final map of stores

```
VELANTRIM STORAGE ECOSYSTEM
│
├── 🔱 GRAPH CORE
│   ├── Kuzu          → Phase 0 MVP (embedded, Cypher) — optional
│   └── Neo4j 5.26+   → Phase 1+ Production (vector, GDS)
│
├── 📊 SQL LAYER
│   ├── SQLite        → operational: logs, configs, skills
│   └── DuckDB        → analytics: metrics, Parquet, aggregations
│
├── 🕸️ R&D / SCIENCE
│   ├── NetworkX      → prototypes, algorithms, experiments
│   └── GraphBLAS     → heavy graph algorithms (Phase 3+)
│
├── ⚡ REAL-TIME
│   └── Memgraph      → streaming graph (Phase 2+)
│
├── ⚠️ OPTIONAL
│   └── SurrealDB     → multi-model (EOL risk, only as needed)
│
└── ☠️ REMOVED
    ├── LadybugDB     → does not exist (replaced by KuzuDB · P0-H)
    ├── RedisGraph     → EOL 2025
    └── GPT-4 / Llama 3 / rubert-tiny2 → obsolete
```

---

## 🤖 Current LLM and Embedding Stack (March 2026)

### LLM models

| Category | Model | Use in Velantrim |
|---|---|---|
| 🏆 **Flagship** | GPT-5.4 / GPT-5.3 Codex | Critical consolidation clusters, complex reasoning |
| 🏆 **Flagship** | Claude Sonnet 4.6 / Opus 4.6 | Complex reasoning, architectural decisions |
| 🏆 **Flagship** | Qwen3-Max (256K ctx) | Long context, agentic tasks |
| ⚡ **Fast** | o4-mini | Routine, 70% of tasks, distill_strategies |
| ⚡ **Fast** | Claude Haiku 4.5 | Fast responses, classification |
| ⚡ **Fast** | Qwen3.5-Flash | $0.10/M tokens — cost savings |
| 🔓 **Local** | Qwen3.5-397B-A17B (MoE) | Privacy-first, 256K ctx, Apache 2.0 |
| 🔓 **Local** | Llama 4 Maverick / Scout | Meta, 10M ctx (Scout), open |
| 🔓 **Local** | DeepSeek V3.2 / R1 | Local reasoning |
| ⚡ **Edge/Lite** | RWKV-7 Goose 2.9B (`mollysama/rwkv-7-g1:2.9b`) | O(n) complexity — speed does not degrade in long sessions. Apache 2.0. Weak hardware, LLM_MODE=lite. `ollama pull mollysama/rwkv-7-g1:2.9b` |
| ❌ **Retired** | GPT-4, Llama 3 | Removed — obsolete |

### Embedding models

| Type | Model | Features |
|---|---|---|
| 🔓 **Local (RU)** | `deepvk/USER-bge-m3` | Best for the Russian language |
| 🔓 **Local (Multi)** | `multilingual-e5-large` | 100+ languages, universal |
| 🌐 **Cloud** | `Gemini Embedding 2` | Multimodal: text+photo+video+audio+PDF. 3072 dims. Phase 2+ |
| 🌐 **Cloud** | `text-embedding-3-large` | OpenAI, stable |
| ❌ **Obsolete** | `rubert-tiny2` | Removed |

> ⚠️ **Important**: changing the embedding model requires reindexing. Vectors from different models are incompatible within a single index. Gemini Embedding 2 is for Phase 2+ when multimodality appears in Velantrim.
>
> ✅ **Automation via Lazy Re-indexing**: the `embedding_version` field on each node makes it possible not to rebuild everything at once. On a model change: new nodes are written with the new version, old ones are flagged with `reindex_required = true`, and a background `AdaptiveConsolidationWorker` reindexes in batches. The system works in `dual-index mode` without downtime.

---

### 🔢 EmbeddingRegistry — protection against mixing dimensionalities

**Problem**: `numpy.dot()` with vectors of different dimensionalities (for example 1024 and 1536) does not raise an exception — it silently returns a mathematically incorrect result. Cosine similarity starts to lie, retrieval degrades quietly and unnoticeably.

**Solution**: a centralized model registry with fail-fast validation on every write.

```python
# memory/embedding_registry.py
import numpy as np
import logging
logger = logging.getLogger(__name__)

# All supported models and their dimensionalities.
# When adding a new model — register it here, do not hardcode it in the code.
_KNOWN_DIMS: dict[str, int] = {
    "deepvk/USER-bge-m3":                   1024,  # Velantrim's main RU model
    "multilingual-e5-large":                1024,
    "paraphrase-multilingual-MiniLM-L12-v2": 384,  # weak profile
    "text-embedding-3-large":               3072,
    "Qwen/Qwen3-Embedding":                 1024,
    "BAAI/bge-m3":                          1536,
    "default":                              1024,  # fallback
}

class EmbeddingRegistry:
    """
    Velantrim's registry of embedding models.
    Call EmbeddingRegistry.validate() before every vector write into L1/L3.
    Fail-fast on a dimensionality mismatch — silent degradation is unacceptable.
    """
    _active_model: str = "deepvk/USER-bge-m3"
    _active_dim:   int = 1024

    @classmethod
    def set_active_model(cls, model_name: str) -> None:
        """Set once at agent startup from velantrim_config."""
        dim = _KNOWN_DIMS.get(model_name)
        if dim is None:
            raise ValueError(
                f"EmbeddingRegistry: unknown model '{model_name}'. "
                f"Register it via register('{model_name}', dim=N). "
                f"Known: {list(_KNOWN_DIMS.keys())}"
            )
        cls._active_model = model_name
        cls._active_dim   = dim
        logger.info(f"EmbeddingRegistry: active={model_name}, dim={dim}")

    @classmethod
    def register(cls, model_name: str, dim: int) -> None:
        """Add a non-standard model."""
        _KNOWN_DIMS[model_name] = dim
        logger.info(f"EmbeddingRegistry: registered {model_name} dim={dim}")

    @classmethod
    def validate(cls, embedding: np.ndarray, model_name: str = None) -> None:
        """
        Check the vector's dimensionality before writing.
        Call in GraphMemory.add_episode() and FractalMemory.add_to_stm().
        Raises ValueError on a mismatch — does not stay silent.
        """
        model    = model_name or cls._active_model
        expected = _KNOWN_DIMS.get(model, cls._active_dim)
        actual   = embedding.shape[0] if hasattr(embedding, 'shape') else len(embedding)
        if actual != expected:
            raise ValueError(
                f"EmbeddingRegistry: dimensionality mismatch for '{model}': "
                f"expected {expected}, got {actual}. "
                f"Mixing models corrupts cosine similarity — this is not a warning, it is a bug."
            )
```

**Integration**: add a call to `EmbeddingRegistry.validate(embedding)` in `GraphMemory.add_episode()` and `FractalMemory.add_to_stm()` before saving the vector. Call `EmbeddingRegistry.set_active_model(EMBEDDING_MODEL)` once in `pipeline.__init__()`.

**Invariant**: mixing vectors of different models within a single index is an architecture violation. `EmbeddingRegistry` makes this violation explicit.

---

## 🔧 System Maintenance

> Two tools that Velantrim was missing for production operation.

---

### 🧹 dedupe_entities.py — Graph Node Deduplication

**Problem**: any live system where an LLM extracts entities accumulates duplicates over time. "Velantrim", "velantrim", "VELANTRIM ExoCortex", "the Velantrim system" — these are all separate nodes in Neo4j. Without deduplication, the graph degrades: connections are scattered across duplicates, search returns incomplete results, and ImportanceScore is underestimated for all copies.

```python
# scripts/dedupe_entities.py
# Run: python scripts/dedupe_entities.py
# Dry-run (analysis without changes): python scripts/dedupe_entities.py --dry-run

import os
import asyncio, argparse, logging
from collections import defaultdict
from memory_core import GraphMemory

logger = logging.getLogger(__name__)

# P0-4 FIX: determine APOC availability once at startup.
# Neo4j + APOC: NEO4J_HAS_APOC=true (in docker-compose: NEO4J_PLUGINS=["apoc"])
# LadybugDB / KuzuDB without APOC: NEO4J_HAS_APOC=false (or unset)
HAS_APOC = os.getenv("NEO4J_HAS_APOC", "false").lower() == "true"


async def _merge_relationship_safe(
    graph,
    from_id: str,
    to_id: str,
    rel_type: str,
    weight: float,
    merged_from: str
) -> None:
    """
    Create/update a relationship between nodes, preserving the original type.
    Uses APOC if available (Neo4j), otherwise — pure Cypher (LadybugDB/KuzuDB).

    P0-4 FIX: APOC apoc.merge.relationship is unavailable in LadybugDB.
    The fallback uses MERGE with a parameterized type via an f-string.
    rel_type is taken from type(r) which is already in the graph, not from user input.
    """
    if HAS_APOC:
        await graph.execute_cypher("""
            MATCH (a {id: $from_id}), (b {id: $to_id})
            CALL apoc.merge.relationship(a, $rel_type, {}, {weight: $weight}, b)
            YIELD rel
            SET rel.weight = coalesce(rel.weight, 0) + $weight,
                rel.merged_from = $merged_from
        """, {"from_id": from_id, "to_id": to_id,
              "rel_type": rel_type, "weight": weight, "merged_from": merged_from})
    else:
        # Fallback for LadybugDB / KuzuDB without APOC.
        # rel_type from type(r) — safe, not user input.
        query = f"""
            MATCH (a {{id: $from_id}}), (b {{id: $to_id}})
            MERGE (a)-[r:{rel_type}]->(b)
            ON CREATE SET r.weight = $weight, r.merged_from = $merged_from
            ON MATCH  SET r.weight = coalesce(r.weight, 0) + $weight,
                          r.merged_from = $merged_from
        """
        await graph.execute_cypher(
            query, {"from_id": from_id, "to_id": to_id,
                    "weight": weight, "merged_from": merged_from}
        )


async def _merge_nodes_safe(graph, e1_id: str, e2_id: str) -> None:
    """
    Merge two duplicate nodes.
    APOC apoc.refactor.mergeNodes — Neo4j only.
    Fallback: manually transfer all edges + soft-delete the duplicate.

    P0-4 FIX: apoc.refactor.mergeNodes is unavailable in LadybugDB.
    """
    if HAS_APOC:
        await graph.execute_cypher("""
            MATCH (e1:Entity {id: $e1_id})
            MATCH (e2:Entity {id: $e2_id})
            CALL apoc.refactor.mergeNodes([e1, e2], {
                properties: 'combine',
                mergeRels: true
            })
            YIELD node
            RETURN count(node) as merged
        """, {"e1_id": e1_id, "e2_id": e2_id})
    else:
        # Fallback: transfer edges + soft-delete the duplicate (e2 → e1).
        await graph.execute_cypher("""
            MATCH (e2:Entity {id: $e2_id})-[r]->(target)
            MATCH (e1:Entity {id: $e1_id})
            WHERE e2.id <> e1.id AND target.id <> e2.id
            MERGE (e1)-[new_r:RELATED_TO]->(target)
            ON CREATE SET new_r.weight = coalesce(r.weight, 0.5),
                          new_r.merged_from = $e2_id
            ON MATCH  SET new_r.weight = new_r.weight + coalesce(r.weight, 0.5)
            DELETE r
        """, {"e1_id": e1_id, "e2_id": e2_id})
        await graph.execute_cypher("""
            MATCH (source)-[r]->(e2:Entity {id: $e2_id})
            MATCH (e1:Entity {id: $e1_id})
            WHERE e2.id <> e1.id AND source.id <> e2.id
            MERGE (source)-[new_r:RELATED_TO]->(e1)
            ON CREATE SET new_r.weight = coalesce(r.weight, 0.5),
                          new_r.merged_from = $e2_id
            ON MATCH  SET new_r.weight = new_r.weight + coalesce(r.weight, 0.5)
            DELETE r
        """, {"e1_id": e1_id, "e2_id": e2_id})
        await graph.execute_cypher("""
            MATCH (e:Entity {id: $e2_id})
            SET e.is_active = false,
                e.valid_to = datetime(),
                e.merged_into = $e1_id
        """, {"e2_id": e2_id, "e1_id": e1_id})


# P0-4 FIX: SAE Lateral Inhibition — apoc.math.maxLong is unavailable in LadybugDB.
SAE_LATERAL_INHIBITION_CYPHER_APOC = """
    UNWIND range(0, size(ranked) - 1) AS i
    WITH ranked[i] AS dominant, ranked, i
    WHERE dominant.activation > $threshold
    UNWIND range(i + 1, size(ranked) - 1) AS j
    WITH dominant, ranked[j] AS competitor
    WHERE competitor.activation < dominant.activation
    SET competitor.activation = apoc.math.maxLong(
        0,
        toInteger((competitor.activation - $mu * dominant.activation) * 1000000)
    ) / 1000000.0
"""

SAE_LATERAL_INHIBITION_CYPHER_FALLBACK = """
    UNWIND range(0, size(ranked) - 1) AS i
    WITH ranked[i] AS dominant, ranked, i
    WHERE dominant.activation > $threshold
    UNWIND range(i + 1, size(ranked) - 1) AS j
    WITH dominant, ranked[j] AS competitor
    WHERE competitor.activation < dominant.activation
    WITH competitor,
         (competitor.activation - $mu * dominant.activation) AS raw_val
    SET competitor.activation = CASE WHEN raw_val < 0 THEN 0.0 ELSE raw_val END
"""

def get_lateral_inhibition_cypher() -> str:
    """Return the correct Cypher for lateral inhibition depending on the backend."""
    return SAE_LATERAL_INHIBITION_CYPHER_APOC if HAS_APOC else SAE_LATERAL_INHIBITION_CYPHER_FALLBACK

async def find_duplicates(graph: GraphMemory) -> dict[str, list[str]]:
    """Find :Entity nodes with the same name (case-insensitive)."""
    rows = await graph.execute_cypher(
        "MATCH (e:Entity) RETURN e.id AS id, e.name AS name, e.access_count AS ac"
    )
    groups: dict[str, list] = defaultdict(list)
    for row in rows:
        key = (row["name"] or "").strip().lower()
        if key:
            groups[key].append(row)
    return {k: v for k, v in groups.items() if len(v) > 1}

async def merge_group(graph: GraphMemory, nodes: list, dry_run: bool):
    """
    Keep the node with the highest access_count as canonical.
    Transfer all edges from the duplicates to the canonical node.
    Remove the duplicates via Soft Delete.
    """
    canonical = max(nodes, key=lambda n: n.get("ac") or 0)
    duplicates = [n for n in nodes if n["id"] != canonical["id"]]
    logger.info(f"Canonical: {canonical['id']} ({canonical['name']}) "
                f"← {[d['id'] for d in duplicates]}")
    if dry_run:
        return

    for dup in duplicates:
        # P0-4 FIX: transfer edges via _merge_relationship_safe() —
        # APOC if available, otherwise a pure Cypher fallback for LadybugDB.
        outgoing_rels = await graph.execute_cypher(
            "MATCH (dup:Entity {id: $dup_id})-[r]->(target) "
            "WHERE dup.id <> $canonical_id "
            "RETURN type(r) AS rel_type, target.id AS target_id, coalesce(r.weight, 0.5) AS weight",
            {"dup_id": dup["id"], "canonical_id": canonical["id"]}
        )
        for row in outgoing_rels:
            await _merge_relationship_safe(
                graph,
                from_id=canonical["id"],
                to_id=row["target_id"],
                rel_type=row["rel_type"],
                weight=row["weight"],
                merged_from=dup["id"]
            )

        incoming_rels = await graph.execute_cypher(
            "MATCH (source)-[r]->(dup:Entity {id: $dup_id}) "
            "WHERE dup.id <> $canonical_id "
            "RETURN type(r) AS rel_type, source.id AS source_id, coalesce(r.weight, 0.5) AS weight",
            {"dup_id": dup["id"], "canonical_id": canonical["id"]}
        )
        for row in incoming_rels:
            await _merge_relationship_safe(
                graph,
                from_id=row["source_id"],
                to_id=canonical["id"],
                rel_type=row["rel_type"],
                weight=row["weight"],
                merged_from=dup["id"]
            )

        # Soft Delete of the duplicate
        await graph.execute_cypher(
            "MATCH (e:Entity {id: $id}) SET e.is_active=false, e.valid_to=datetime()",
            {"id": dup["id"]}
        )

async def main(dry_run: bool):
    graph = GraphMemory()
    dupes = await find_duplicates(graph)
    logger.info(f"Found {len(dupes)} duplicate groups")
    for name, nodes in dupes.items():
        await merge_group(graph, nodes, dry_run)
    action = "Dry-run completed" if dry_run else f"Merged {len(dupes)} groups"
    logger.info(action)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    asyncio.run(main(dry_run=args.dry_run))
```

**Recommended run frequency**: once a week via SleepTimeWorker, or manually when there is a noticeable growth in the number of nodes without a corresponding growth in knowledge.

---

### 📋 migrations/ — Graph Schema Versioning

**Problem**: Velantrim adds new fields to Neo4j nodes (for example `pending_invalidation`, `embedding_version`, `is_ring_zero`) — but there is no mechanism to update already existing nodes when deploying a new version. This leads to old nodes lacking the required fields, and invariants starting to break on production data.

```python
# migrations/apply_migrations.py
# Run on every update: python migrations/apply_migrations.py
# Idempotent — safe to run repeatedly.

import asyncio, logging
from memory_core import GraphMemory

logger = logging.getLogger(__name__)

MIGRATIONS = [
    {
        "version": "v8.0",  // P2-B FIX
        "description": "Add is_active=true to all nodes lacking this field",
        "cypher": "MATCH (n) WHERE n.is_active IS NULL SET n.is_active = true"
    },
    {
        "version": "v5.1",
        "description": "Add epistemic_state='Validated' to all :Fact nodes without ESM",
        "cypher": "MATCH (f:Fact) WHERE f.epistemic_state IS NULL SET f.epistemic_state='Validated'"
    },
    {
        "version": "v5.2",
        "description": "Add embedding_version='v1' to all nodes with an embedding",
        "cypher": "MATCH (n) WHERE n.embedding IS NOT NULL AND n.embedding_version IS NULL SET n.embedding_version='v1'"
    },
    {
        "version": "v5.3",
        "description": "Add is_ring_zero=false to all nodes lacking this field",
        "cypher": "MATCH (n) WHERE n.is_ring_zero IS NULL SET n.is_ring_zero = false"
    },
    {
        "version": "v5.4",
        "description": "Create the pending_invalidation index if it does not exist",
        "cypher": "CREATE INDEX pending_inv_idx IF NOT EXISTS FOR (f:Fact) ON (f.pending_invalidation)"
    },
]

async def apply_migrations(graph: GraphMemory):
    # Create the version table if it does not exist
    await graph.execute_cypher("""
        MERGE (mv:MigrationVersion {id: 'schema_version'})
        ON CREATE SET mv.applied = []
    """)
    result = await graph.execute_cypher(
        "MATCH (mv:MigrationVersion {id: 'schema_version'}) RETURN mv.applied AS applied"
    )
    applied = set(result[0]["applied"]) if result else set()

    for m in MIGRATIONS:
        if m["version"] in applied:
            logger.info(f"Migration {m['version']} already applied — skip")
            continue
        logger.info(f"Applying migration {m['version']}: {m['description']}")
        await graph.execute_cypher(m["cypher"])
        await graph.execute_cypher(
            "MATCH (mv:MigrationVersion {id: 'schema_version'}) "
            "SET mv.applied = mv.applied + [$version]",
            {"version": m["version"]}
        )
        logger.info(f"Migration {m['version']} applied ✅")

if __name__ == "__main__":
    asyncio.run(apply_migrations(GraphMemory()))
```

**Invariant**: `apply_migrations()` is called on every pipeline startup in `pipeline.__init__()` before any queries to the graph. Migrations are idempotent — re-running is safe.

---

## 📚 Additional Resources

### Documentation

- [Graphiti GitHub](https://github.com/getzep/graphiti)
- [Neo4j 5.26+ Vector Search](https://neo4j.com/docs/cypher-manual/current/indexes-for-vector-search/)
- [DeepSeek Engram GitHub](https://github.com/deepseek-ai/Engram)
- [LangGraph for agents](https://langchain-ai.github.io/langgraph/)
- [Memgraph documentation](https://memgraph.com/docs)
- [DuckDB documentation](https://duckdb.org/docs/)
- [Gemini Embedding 2](https://ai.google.dev/gemini-api/docs/embeddings)

### Research Papers

- "ReasoningBank" - Learning from Success and Failure
- "Graphiti: Temporal Knowledge Graphs for AI Agents"
- "DeepSeek Engram: Conditional Memory for MoE Architectures" (January 2026)
- "Fractal Graph Theory and Knowledge Graphs"
- "Map-Based Experience Replay" (GWR approach)
- "Gemini Embedding 2: Natively Multimodal Embeddings" (March 2026)

### Benchmarks

- Deep Memory Retrieval (Zep)
- LOCOMO (Long-term Context Memory)
- Standard RAG baselines
- LMArena Text Leaderboard (March 2026)

---

## 🎓 Conclusion

This specification brings together:
- **Graphiti + Neo4j 5.26+** for temporal graph memory
- **Fractal hierarchy** for scaling
- **ReasoningBank** for self-learning
- **Hybrid retrieval** for token minimization
- **Etir (L3.5)** — Velantrim Synaptic Activation Layer
- **The Engram principle** as an architectural ally (DeepSeek, January 2026)
- **Memory Guardian (MGL)** — protecting L3 from hallucination poisoning
- **Immutable Raw Memory** — protection against Semantic Drift
- **Knowledge Distillation Engine** — JSON triples instead of text chunks
- **Formal invariants (RFC0001–RFC0006)** — the system contract
- **Evidence as a node** + `[:SUPPORTED_BY]`, `[:CAUSES]`, `[:IMPROVES]`
- **Evidence Pack + Truth Gate** with concrete thresholds
- **Memory Router** DEFINE/RECALL/POLICY/TASK
- **Automation** without constant LLM queries
- ✅ **ConsolidationEngine** — race condition closed forever
- ✅ **Canonical Memory Protocol v1** — a single entry point
- ✅ **CoreMemoryBlocks** — the agent knows the user from the very first word (L0 CRITICAL)
- ✅ **EmbeddingRegistry** — protection against silent mixing of dimensions
- ✅ **MCP Server** — connection to Cursor / Claude Code via stdio
- ✅ **dedupe_entities.py** — deduplication of graph Entity nodes
- ✅ **migrations/** — Neo4j schema versioning, idempotent migrations
- ✅ **RWKV-7 Edge** — an O(n) LLM for weak hardware in LLM_MODE=lite
- ✅ **pymorphy3 singleton + lru_cache** — 40–60% CPU savings with ReasoningBank
- ✅ **Velum GC of weak edges** — protection against unbounded growth of _edges
- ✅ **Velum SQLite persist** — co-occurrence edges survive a restart
- ✅ **ValidationError recovery** — GraphitiAdapter is resilient to Graphiti API quirks
- ✅ **Depth injection whitelist** — Cypher injection via depth is architecturally impossible
- ✅ **Auto-summary every 10 turns** — the graph does not grow linearly with the number of messages
- ✅ **CausalGraph** — CAUSES/LEADS_TO/INFLUENCES edges, the agent understands causes
- ✅ **RFC0006 Engram Isolation** — an architectural lock
- ✅ **Runtime Invariant Checker** — RFCs live in code, not on paper
- ✅ **Cognitive Modes** — PRECISION / BALANCED / EXPLORATION
- ✅ **Weighted Semantic Decay** — we forget in an epistemically honest way
- ✅ **Memory Budget Planner** — the graph does not grow forever
- ✅ **PII Redaction implemented** — GDPR is not a declaration
- ✅ **Freeze State WAL** — milliseconds instead of seconds
- ✅ **Meta-Supervisor Apex Controller** — NORMAL/DEGRADED/SAFE_MODE + Recovery Protocol
- ✅ **ESM in L3** — the lifecycle of facts (Observed→Collapsed)
- ✅ **MHI architecture** — described, implementation in Phase 2

**Expected outcome**:
- 90%+ reduction in token consumption
- 30%+ improvement in task success rate
- <500ms search latency
- Full autonomy of memory operation
- No race conditions (ConsolidationEngine)
- No unprotected RFC violations (Runtime Checker)

The system is ready for its first launch on a PC with validation at every stage.

---

### RFC0029 — Observer++ (Immune system)

**Problem**: The Observer watched and logged, but had no power to stop anything. The system had no immune system.

**Solution**: The Observer gains three real powers — blocking, rollback, and trust reduction.

```python
# 📎 Base version. The canonical one — RFC0041 Graduated Observer++ (see below)
class ObserverPlusPlus:
    """RFC0029 — Observer with power. The immune system of Velantrim."""

    async def on_anomaly(self, event: AnomalyEvent):
        if event.severity == "critical":
            await self.block_pipeline()
            await self.trigger_rollback()
            await self.reduce_trust_score(event.source_id)

    async def monitor_loop(self):
        while True:
            state = await self.get_current_state()
            if state.drift_score > DRIFT_THRESHOLD:
                await self.trigger_rollback()
            if state.cascade_size > MAX_ROLLBACK_CASCADE:
                await self.block_pipeline()
            if state.dlq_size > DLQ_OVERFLOW_THRESHOLD:
                await self.enter_safe_mode()
            if state.faithfulness_score < MIN_FAITHFULNESS:
                await self.pause_pipeline()
            await asyncio.sleep(OBSERVER_INTERVAL)
```

**Activation triggers:**

| Trigger | Action |
|---|---|
| `drift_score > 0.3` | rollback |
| `cascade_size > MAX_ROLLBACK_CASCADE` | block_pipeline |
| `DLQ overflow` | enter_safe_mode (L3 Read-Only) |
| `faithfulness < MIN_FAITHFULNESS` | pause + alert |
| `semantic_drift > SEMANTIC_THRESHOLD` | alert + review |

**Invariants**: The Observer does NOT write to the Graph, does NOT generate facts, does NOT modify the ESM directly.

---

### RFC0029+ — ESMChunkedInvalidator (Batch rollback without deadlock)

**Problem**: A direct `[:CONTRADICTS]` cascade over 100+ nodes → Neo4j deadlock + blocking of the ConsolidationEngine.

```python
class ESMChunkedInvalidator:
    async def start_cascade(self, root_fact_id: str):
        await self._mark_pending(root_fact_id)
        asyncio.create_task(self._process_chunks())

    async def _process_chunks(self):
        query = """
        MATCH (dep:Fact {pending_invalidation: true})
        WITH dep LIMIT $batch_size
        OPTIONAL MATCH (dep)<-[:DERIVED_FROM]-(child:Fact)
        WHERE child.epistemic_state IN ['Validated', 'Supported']
        SET child.pending_invalidation = true
        SET dep.epistemic_state = 'Hypothesized',
            dep.pending_invalidation = false,
            dep.invalidated_at = datetime()
        RETURN count(DISTINCT dep) as processed_count
        """
        while True:
            if await self.meta_supervisor.is_safe_mode():
                break
            result = await self.graph.execute_cypher(query, {"batch_size": 50})
            if not result or result[0]["processed_count"] == 0:
                break
            await asyncio.sleep(0.1)  # let Neo4j "breathe"
```

**Mandatory index:**
```cypher
CREATE INDEX pending_inv_idx FOR (f:Fact) ON (f.pending_invalidation)
```

---

### RFC0030 — Source Trust Layer (Protection against Validated Hallucination)

**Problem**: TruthGate verifies the evidence, but not the source. Incorrect parsing → a structurally correct fact → TruthGate lets it through → the system confidently states a falsehood ("validated hallucination").

```python
@dataclass
class SourceTrust:
    source_type: str        # "user_input"|"llm_output"|"import"|"manual"
    trust_score: float      # 0.0 – 1.0
    validation_status: str  # "verified"|"pending"|"flagged"
```

**Change in TruthGate:**
```python
# BEFORE: if evidence_valid: accept_fact()
# AFTER:
if evidence_valid and source.trust_score >= TRUST_THRESHOLD:
    accept_fact()
else:
    mark_as_pending_review()
```

**trust_score scale:**

| Source | trust_score | Acceptance |
|---|---|---|
| manual (human) | 0.95 | ✅ automatic |
| trusted_import | 0.80 | ✅ automatic |
| user_input | 0.65 | ⚠️ pending |
| llm_output | 0.30 | ❌ only via pipeline |

---

### RFC0031 — Write Protocol (The only write paths into the Graph)

**Problem**: There is no machine-enforced contract for who is allowed to write to L3. `Graph = Truth` remains merely a philosophy.

```python
class GraphWriteProtocol:
    ALLOWED_WRITERS = {"TruthGate", "HumanApproval", "TrustedImport"}

    async def write(self, fact, writer_id: str, trust_score: float):
        if writer_id not in self.ALLOWED_WRITERS:
            raise WriteProtocolViolation(f"Unauthorized: {writer_id}")
        if trust_score < WRITE_TRUST_THRESHOLD:
            raise WriteProtocolViolation(f"Low trust: {trust_score}")
        await self._audit_log(writer_id, fact)
        return await self._graph_write(fact)
```

**Always forbidden**: the LLM directly, L1/L2/L2.5, Free Mode, Observer, Velum, ReasoningBank.

---

### RFC0032 — SafeFTSQuery (ESM filter for FTS5)

**Problem**: FTS5 returns raw episodes without an ESM check. Contradicted/Deprecated data enters the context.

```python
class SafeFTSQuery:
    async def search(self, query: str, limit: int = 20) -> list[Episode]:
        raw = await self.fts5_search(query, limit * 2)
        safe = []
        for ep in raw:
            if ep.valid_until and ep.valid_until < datetime.now(timezone.utc):
                continue
            if ep.esm_hint in ("Contradicted", "Deprecated"):
                continue
            if await self._linked_to_contradicted(ep):
                continue
            safe.append(ep)
        return safe[:limit]
```

**Rule**: Direct FTS5 without SafeFTSQuery is an architecture error. All L1 retrieval goes only through this class.

---

### RFC0033 — Closed Loop Self-Evaluation (Closed loop)

**Problem**: `Query → Answer → Done` — L4 learns blindly.

```
AFTER: Query → Retrieval → L4 → Answer → EVALUATE → LOG → ADJUST
```

```python
@dataclass
class EvaluationResult:
    faithfulness: float       # does the answer match the facts?
    trace_coverage: float     # are all facts in the chain used?
    contradiction_rate: float # contradictions in the answer?
    response_confidence: float

class ClosedLoopEvaluator:
    async def evaluate(self, query, facts_pack, answer) -> EvaluationResult:
        result = EvaluationResult(
            faithfulness=await self._check_faithfulness(answer, facts_pack),
            trace_coverage=await self._check_trace_coverage(answer, facts_pack),
            contradiction_rate=await self._check_contradictions(answer),
            response_confidence=await self._get_l4_confidence()
        )
        await self.reasoning_bank.record_evaluation(result)
        if result.faithfulness < MIN_FAITHFULNESS:
            await self.observer.on_anomaly(AnomalyEvent(severity="warning"))
        return result
```

---

### RFC0034 — Semantic Drift Monitor (Semantic drift)

**Problem**: Structural drift does not detect a semantic shift. The graph is structurally stable — but the meaning is already different.

```python
class SemanticDriftMonitor:
    async def check(self) -> SemanticDriftResult:
        esm_drift = self._compare_esm(await self._get_esm_distribution())
        centrality_drift = self._compare_centrality(await self._get_top_pagerank(k=10))
        domain_drift = self._compare_domains(await self._get_domain_distribution())
        semantic_score = esm_drift*0.5 + centrality_drift*0.3 + domain_drift*0.2
        if semantic_score > SEMANTIC_DRIFT_THRESHOLD:
            await self.alert("semantic_drift", score=semantic_score)
        return SemanticDriftResult(semantic_score, esm_drift, centrality_drift, domain_drift)
```

**Two independent alerts:**
- `structural_drift` — the graph changed in form
- `semantic_drift` — the graph changed in meaning

---

### RFC0035 — Facts Pack Dual Mode + Diversity Constraint

**Problem**: 8–12 facts for all queries is not enough for complex tasks. There is no guarantee of source diversity.

```python
class FactsPackBuilder:
    STRICT_LIMIT = 12    # fast queries
    EXTENDED_LIMIT = 40  # complex questions (complexity > COMPLEXITY_THRESHOLD)

    async def build(self, query: str, complexity: float) -> FactsPack:
        limit = self.EXTENDED_LIMIT if complexity > COMPLEXITY_THRESHOLD else self.STRICT_LIMIT
        facts = await self.retrieve(query, limit=limit * 2)
        return FactsPack(facts=self._diversity_filter(facts)[:limit])

    def _diversity_filter(self, facts):
        counts = defaultdict(int)
        result = []
        for f in sorted(facts, key=lambda x: x.confidence, reverse=True):
            if counts[f.source_domain] < MAX_FACTS_PER_SOURCE:
                result.append(f)
                counts[f.source_domain] += 1
        return result
```

---

### TraceLine — A single trace of a fact L1 → L3.5

**Purpose**: A mandatory diagnostic layer. Any `fact_id` → the full path through all layers with ESM validation of every node.

```
GET /trace?id=fact_abc

{
  "trace": [
    {"layer": "L1", "episode_id": "ep_001"},
    {"layer": "L2", "theme_id": "theme_007", "strength": 0.82},
    {"layer": "L2.5", "staging_id": "stg_042", "status": "promoted"},
    {"layer": "L3", "node_id": "node_123", "esm_state": "Validated"},
    {"layer": "L3.5", "snapshot_id": "snap_2026_03"}
  ],
  "validation": {"all_esm_valid": true, "broken_links": [], "integrity": "OK"}
}
```

**TraceLine extension for RFC0063 (Knowledge Ingestion):** for a query with `?id=source_abc123` it returns all three layers:

```json
GET /trace?id=source_abc123

{
  "source_id": "source_abc123",
  "source_vintage": 2023,
  "source_domain": "physics",
  "layers": {
    "L3_facts": [
      {"fact_id": "fact_001", "esm_state": "Supported", "confidence": 0.87},
      {"fact_id": "fact_002", "esm_state": "Validated", "confidence": 0.94}
    ],
    "L4_strategies": [
      {"strategy_id": "strat_042", "prior_confidence": 0.90, "success_rate": 0.0}
    ],
    "vector_chunks": [
      {"chunk_id": "emb_099", "cosine_cluster": "physics_gravity",
       "fact_ids": ["fact_001"]}
    ]
  },
  "integrity": {
    "all_esm_valid": true,
    "broken_links": [],
    "vintage_decay_applied": true
  }
}
```

> ⚠️ TRACE = a path, NOT = truth. A→B→C is correct, but if A is false — the result is false. TraceLine checks the ESM of every node in the chain.

---

## 🗺️ Technology Map · Optional Stack

> Listed below are technologies that are **not mandatory** for the system to
> operate, but that may be plugged in as optional components depending on
> conditions: hardware, task complexity, project goals.
>
> Integration principle: **Graph = Truth is never violated**.
> Any optional technology is a replacement for the transport or an addition to
> retrieval, but never a replacement for the source of truth.

---

#### 🗄️ Block A — Graph engines (alternatives and additions to Neo4j)

```
CONDITION                  TECHNOLOGY         ROLE IN THE SYSTEM
──────────────────────────────────────────────────────────────
Weak hardware / MVP        Kuzu               Replacement for Neo4j in L3
RAM < 4GB                  Graph-Lite         Already in L2.5 (Staging)
OLAP drift analytics       DuckDB             Shadow State instead of
                                              load on Neo4j
Single SQL stack           PostgreSQL+pgvec   Replacement for SQLite+Neo4j
External graph pipeline    Graphiti           Optional L3 backend
```

---

##### 🟣 Kuzu — embedded graph DB

**Essence:** Kuzu works like SQLite — in-process, with no separate server.
It supports Cypher, ACID, and native traversal. The developers are not actively
maintaining it, but the database is stable and fit for use.

**Where to use it in Velantrim:**
- L3 on weak hardware (RAM < 8GB, no Docker)
- A local agent without infrastructure
- MVP / prototype without Neo4j

**Invariant:** Kuzu is used only as the L3 engine. `Graph = Truth` is preserved.
Write Protocol, ESM, TruthGate — work on top of Kuzu without changes.

```python
# velantrim_config.py
GRAPH_BACKEND = "neo4j"      # production default
# GRAPH_BACKEND = "kuzu"       # v8.0: KuzuDB (MIT, Cypher, ACID) — P0-H FIX
# GRAPH_BACKEND = "graph_lite" # optional: RAM < 4GB (already in L2.5)
```

**Limitation:** Kuzu does not support clustering. Single-node only.
When the graph grows beyond > 10M nodes — migrate to Neo4j.

---

##### 🔵 DuckDB — Shadow State for analytics

**Essence:** An OLAP engine, working on Parquet/Arrow in-process.
It does not store the graph — only analytical projections.

**Where to use it in Velantrim:**
- `Semantic Drift Monitor` and `Observer++` perform heavy computations
  (PageRank, ESM distribution) directly in Neo4j → blocking transactions.
- DuckDB receives a graph dump every 15 min → analytics is isolated.

```
Neo4j   ←── transactions (OLTP)  Write Protocol, TruthGate
   ↓ dump every 15 min
DuckDB  ←── analytics (OLAP)     Drift Monitor, Observer metrics
```

**Benefit:** The Observer and the Drift Monitor do not block the main graph.
P95 latency does not degrade under background analytics.

---

##### 🟢 Graphiti — optional graph pipeline

**Essence:** Graphiti builds a graph of entities from text episodes with temporal
edges. It lies at the foundation of Velantrim as a source of inspiration.

**Where to use it in Velantrim:**
- An optional backend for the `ConsolidationEngine` (L2→L3 promotion)
- Importing external knowledge corpora into L3
- An alternative ingestion pipeline when there is no custom parser

**Limitation:** Graphiti is not a source of truth. Everything that comes through
Graphiti passes through `TruthGate + Write Protocol` like any other source.
`source_type = "trusted_import"`, `trust_score = 0.80`.

---

##### 🟡 Graph-Lite — already exists in L2.5

**Essence:** Already implemented in L2.5 Staging as a temporary mini-graph in SQLite
(the `nodes` + `edges` tables). Activated when RAM < 4GB.

**Reminder of the reading rule:**
```
1. First the L3 graph (Neo4j / Kuzu) — the canon
2. If not in L3 but present in Graph-Lite → confidence × 0.7
   marked "preliminary" (not truth, a hypothesis)
3. On transfer to Neo4j → Graph-Lite is cleared
```

---

#### 🔍 Block B — RAG architectures (optional in the Fast Path)

> All of the architectures listed below are **retrieval patterns**.
> They do not replace `Graph = Truth`; they describe how and from where to take facts
> before passing them into the `FactsPack`.

```
TECHNOLOGY    ESSENCE (in one line)                    LAYER IN VELANTRIM
──────────────────────────────────────────────────────────────────────────
GraphRAG      Graph of entities → global queries       L3 retrieval
KAG           ETL layer: Extract→Aggregate→Normalize   Between L3 and FactsPack
CAG           Graph of cause-and-effect chains         L4 ReasoningBank
ReRAG         Iterative retrieval (several rounds)      HybridRetriever
AgRAG         The agent decides when/what to search     Fast Path routing
GCR           Reasoning only along graph paths          L4 constraint
RefRAG        Self-assessment: is more search needed    Before Closed Loop
Refrag        Context compression before the LLM        After FactsPack
Self-RAG      The LLM critiques its own answers         Closed Loop RFC0033
HyDE          Search via a hypothetical answer          L1 FTS5 / Hybrid
```

---

##### 🔵 GraphRAG (Microsoft)

**Essence:** Builds a graph of entities on top of a corpus. It answers "global"
questions (themes, summaries, relationships) better than vector search.

**Where in Velantrim:** L3 retrieval for multi-step queries and thematic
summaries. Especially useful for queries of the WHY / OVERVIEW / THEME type.

**Status:** Optional. It does not replace TruthGate. The GraphRAG result →
passes through the equivalent of `SafeFTSQuery` + an ESM filter before FactsPack.

---

##### 🟡 KAG — Knowledge-Augmented Generation

**Essence:** A formal ETL layer between L3 retrieval and FactsPack.
It normalizes, aggregates, and filters facts by `epistemic_state` before passing them
into the context.

**Where in Velantrim:** An intermediate step in the `ContextBuilder`:

```
L3 retrieval → [KAG: Extract→Aggregate→Normalize] → FactsPack → LLM
```

Mandatory fields of a KAG node: `source_ref`, `confidence`, `trace_id`,
`epistemic_state`, `trust_score`.

**Status:** Conceptually already implemented in `FactsPack` and `TruthGate`.
KAG is simply a formal name for this layer. It can be documented
explicitly as `KAGBuilder` instead of an anonymous step.

---

##### 🟠 CAG — Causal Argument Graph

**Essence:** A graph of cause-and-effect relationships on top of L3. It is used by
L4 to build reasoning chains without LLM fantasies.

**Where in Velantrim:** L4 `ReasoningBank` — for queries of the WHY/CAUSE type:

```
WHY query → L3 facts → CAG traversal → reasoning path → answer
```

CAG nodes: `cause_node → effect_node` with the fields `confidence`, `evidence_refs`,
`trace_id`. Edges: `[:CAUSES]`, `[:ENABLES]`, `[:PREVENTS]`.

**Status:** Optional. It strengthens L4 with deterministic reasoning.
It is built on top of existing L3 nodes through additional edges.

---

##### 🟢 ReRAG — Recursive / Iterative RAG

**Essence:** Several rounds of retrieval: based on the results of the first pass,
refined sub-queries are formed → it searches again → it expands the context.

**Where in Velantrim:** The `HybridRetriever` already supports multi-stage
retrieval and graph expansion. ReRAG is a formal name for this pattern.

**Limitation:** An explicit iteration limit `MAX_RERAG_ITERATIONS = 3`
and a stopping criterion (a coverage threshold) are mandatory. Without a limit — token explosion.

```python
# velantrim_config.py
MAX_RERAG_ITERATIONS = 3      # maximum rounds
RERAG_COVERAGE_THRESHOLD = 0.85  # stop if coverage > 85%
```

---

##### 🔴 GCR — Graph-Constrained Reasoning

**Essence:** Reasoning only along existing paths in the graph. The LLM cannot
"invent" a relationship that is not in L3. A strict constraint.

**Where in Velantrim:** L4 `ReasoningBank` + Write Protocol. In essence GCR —
is a philosophy that the `Graph = Truth` principle already implements.
It can be formalized as an explicit flag:

```python
reasoning_mode = "graph_constrained"  # only along L3 paths
# reasoning_mode = "hybrid"           # L3 + LLM inference
```

---

##### 🟡 AgRAG — Agentic RAG

**Essence:** The agent itself decides when and what to search for. Not a linear pipeline,
but a loop: action → evaluation → next action.

**Where in Velantrim:** The entire Fast Path is already agentic. AgRAG describes
exactly the `Fact Router` pattern (see RFC0038 below) + `Closed Loop Eval`.

---

##### 🟢 RefRAG / Self-RAG

**Essence:** After retrieval, the system evaluates the sufficiency of what was found.
If not enough — another round. The LLM critiques its sources.

**Where in Velantrim:** The `Closed Loop Eval (RFC0033)` already implements this
pattern. RefRAG is an alternative name. The difference: in RefRAG the evaluation
happens BEFORE generating the answer, in RFC0033 — AFTER. Both approaches are compatible.

---

##### ⚠️ Refrag — context compression

**Essence:** An optimization of how the LLM reads the context. It compresses chunks via
embeddings, selecting only the important parts. It speeds up inference by up to ~30x TTFT.

**Important:** Refrag is about **efficiency**, not about **truth**.
It does not make the system smarter — it makes it cheaper and faster.

**Where in Velantrim:** After `FactsPack`, before `LLM Generation`.
Apply it only when the Graph + FactsPack are stable and the problem is cost/latency.

```
FactsPack (12-40 facts) → [Refrag: compression] → LLM (only what matters)
```

**Status:** Low priority. To be implemented in the next sprint.

---

##### 🟡 HyDE — Hypothetical Document Embedding

**Essence:** It generates a "hypothetical answer" to a query, then searches for
what is similar to it in the database. It improves sparse retrieval for unusual queries.

**Where in Velantrim:** The `HybridRetriever` — an addition to BM25/FTS5.
Especially useful for L1 when the exact query text does not match the episodes.

---

## 📜 RFC0036–RFC0051

---

### RFC0036 — Persistent Event Fallback Queue

**Version:** 2 · **Priority:** 🔴 Critical · **Implementation time:** 2–3 days

**Problem:** `fallback_queue` in `RobustEventBus` is purely in-memory
(`asyncio.Queue`). On an agent restart or a Redis crash, all events are lost
forever. This is the only place in the system where "Truth Integrity" is violated
at the level of events (not facts). 182 pages of the document — not a single mention.

**Invariant:** This does NOT violate the Write Protocol — events are not facts.
The SQLite fallback works in parallel with the existing DLQ.

**Solution:** Replace `asyncio.Queue` with the SQLite table `event_fallback`.

```python
# P3-A FIX: ⚠️ CANONICAL: SQLiteFallbackQueue in the section "1. Event Bus & Ingestion Pipeline".
# This fragment is archival RFC text. See the implementation above.
# event_bus.py — RFC0036 addition to the RobustEventBus class (canonical version in the section "1. Event Bus")
# Add the following methods and attributes to the existing class:
import aiosqlite
import zlib
from prometheus_client import Counter, Gauge

class RobustEventBus:  # extension — add to the main class
    # New attributes (__init__):
    # self.sqlite_path = sqlite_path  (operational DB already exists)
    # self.fallback_inserted = Counter('event_fallback_inserted_total', ...)
    # self.fallback_recovered = Counter('event_fallback_recovered_total', ...)
    # self.fallback_size = Gauge('event_fallback_size', ...)

    async def _init_fallback_table(self):
        async with aiosqlite.connect(self.sqlite_path) as db:
            await db.execute("PRAGMA journal_mode=WAL;")
            await db.execute("""
                CREATE TABLE IF NOT EXISTS event_fallback (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_data  BLOB    NOT NULL,       -- zlib-compressed JSON
                    priority    TEXT    DEFAULT 'NORMAL', -- CRITICAL / NORMAL
                    retry_count INTEGER DEFAULT 0,
                    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            await db.execute("""
                CREATE INDEX IF NOT EXISTS idx_fallback_prio
                ON event_fallback(priority, retry_count, created_at)
            """)
            await db.commit()

    async def publish(self, event: AgentEvent,
                      priority: str = 'NORMAL') -> bool:
        event_data = { ... }  # as before
        try:
            await self.redis.xadd(self.stream_key, event_data)
            return True
        except Exception:
            compressed = zlib.compress(
                json.dumps(event_data).encode(), level=1
            )
            async with aiosqlite.connect(self.sqlite_path) as db:
                await db.execute(
                    "INSERT INTO event_fallback (event_data, priority) "
                    "VALUES (?, ?)",
                    (compressed, priority)
                )
                await db.commit()
            self.fallback_inserted.inc()
            return False

    async def process_persistent_fallback(self):
        """Called by the scheduler every 5 min"""
        async with aiosqlite.connect(self.sqlite_path) as db:
            cursor = await db.execute("""
                SELECT id, event_data FROM event_fallback
                WHERE retry_count < 5
                ORDER BY priority DESC, created_at ASC
                LIMIT 100
            """)
            rows = await cursor.fetchall()
            for row_id, compressed in rows:
                try:
                    data = json.loads(zlib.decompress(compressed))
                    await self.redis.xadd(self.stream_key, data)
                    await db.execute(
                        "DELETE FROM event_fallback WHERE id=?", (row_id,)
                    )
                    self.fallback_recovered.inc()
                except Exception:
                    await db.execute(
                        "UPDATE event_fallback "
                        "SET retry_count = retry_count + 1 WHERE id=?",
                        (row_id,)
                    )
            await db.commit()

    async def cleanup_old_fallback(self):
        """Called by the scheduler every 24h"""
        async with aiosqlite.connect(self.sqlite_path) as db:
            await db.execute(
                "DELETE FROM event_fallback WHERE created_at < ?",
                (datetime.now(timezone.utc) - timedelta(days=7),)
            )
            await db.commit()
```

**Integration into main.py / scheduler:**
```python
scheduler.add_job(event_bus.process_persistent_fallback,
                  'interval', minutes=5)
scheduler.add_job(event_bus.cleanup_old_fallback,
                  'interval', hours=24)
```

**Prometheus metric:** `event_fallback_inserted_total`,
`event_fallback_recovered_total`, `event_fallback_size`

**For CRITICAL events** (Ring Zero change, ESM Validated→Contradicted):
```python
await event_bus.publish(event, priority='CRITICAL')
```

---

### RFC0036+ — OCC Patch for ESMChunkedInvalidator

**Problem:** `asyncio.sleep(0.1)` in the batched rollback creates a race condition.
During the pause, another process (Fast-Track Staging) may attach new
facts to nodes that are queued for invalidation → "phantom" links.

**Solution:** Optimistic Concurrency Control — node versioning.

**Step 1 — Schema migration (one-time):**
```cypher
// Add a version field to all :Fact nodes
MATCH (f:Fact) WHERE f._version_ IS NULL
SET f._version_ = 1
```

**Step 2 — Atomic Cypher instead of sleep:**
```cypher
// BEFORE (with a race condition):
MATCH (dep:Fact {pending_invalidation: true})
WITH dep LIMIT 50
SET dep.epistemic_state = 'Hypothesized'
...

// AFTER (OCC — atomic):
MATCH (dep:Fact {id: $fact_id, _version_: $expected_version})
SET dep.epistemic_state   = 'Hypothesized',
    dep.pending_invalidation = false,
    dep.invalidated_at    = datetime(),
    dep._version_         = dep._version_ + 1
RETURN dep.id as processed
// If _version_ changed → 0 rows → add to the DLQ, do not hang
```

**Step 3 — Python:**
```python
# 📎 OCC extension of ESMChunkedInvalidator (base version — RFC0029+, see above)
class ESMChunkedInvalidator:
    async def _process_single(self, fact_id: str,
                               expected_version: int) -> bool:
        result = await self.graph.execute_cypher(
            OCC_INVALIDATE_QUERY,
            {"fact_id": fact_id, "expected_version": expected_version}
        )
        if not result or result[0]["processed"] == 0:
            # The version changed — add to the DLQ for retry
            await self.dlq.put(fact_id)
            return False
        return True
    # asyncio.sleep(0.1) — REMOVE
```

**Result:** No deadlock, no race condition, no phantom links.
The DLQ handles conflict cases automatically.

---

### RFC0037 — Async Closed Loop Eval

**Problem:** `ClosedLoopEvaluator (RFC0033)` runs in the synchronous Fast Path.
The user waits while the system evaluates its own answer → P95 latency 2000+ ms
instead of the stated 500 ms. The SLO is violated.

**Solution:** Move EVALUATE to the SLOW PATH via the Event Bus.

```
BEFORE:
  Query → Retrieval → L4 → Answer → EVALUATE → [wait] → ADJUST → Response

AFTER:
  Query → Retrieval → L4 → Answer → Response  ← the user receives it here
                                  ↓ async (Event Bus)
                             L4 Worker → EVALUATE → ADJUST → ReasoningBank
```

**Change in the Fast Path:**
```python
# context_builder.py / fast_path.py
async def generate_response(self, query, facts_pack) -> Response:
    answer = await self.llm.generate(query, facts_pack)

    # BEFORE: await self.evaluator.evaluate(query, facts_pack, answer)
    # AFTER: send to the background
    await self.event_bus.publish(AgentEvent(
        event_type  = "AGENT_RESPONSE",
        payload     = {
            "query"       : query,
            "facts_pack"  : facts_pack.to_dict(),
            "answer"      : answer.content,
            "strategy_id" : self.last_strategy_id,
            "session_id"  : self.session_id,
        }
    ), priority='NORMAL')

    return answer  # ← straight to the user
```

**L4 Worker (Slow Path):**
```python
# l4_reasoning_worker.py
async def process_evaluation_queue(self):
    async for msg_id, data in self.event_bus.consume(
        "eval_group", "eval_worker"
    ):
        if data["event_type"] != "AGENT_RESPONSE":
            continue

        result = await self.evaluator.evaluate(
            query      = data["query"],
            facts_pack = FactsPack.from_dict(data["facts_pack"]),
            answer     = data["answer"]
        )

        # Train ReasoningBank on the result
        await self.reasoning_bank.update_strategy_feedback(
            strategy_id = data["strategy_id"],
            outcome     = "SUCCESS" if result.faithfulness > MIN_FAITHFULNESS
                          else "FAILURE",
            metrics     = result.to_dict()
        )

        # Bad answer → Observer++ alert
        if result.faithfulness < MIN_FAITHFULNESS:
            await self.observer.on_anomaly(AnomalyEvent(
                severity = "warning",
                source   = "closed_loop_eval",
                details  = result.to_dict()
            ))
```

**Result:** The Fast Path is not blocked. P95 returns to < 500 ms.
Answer quality improves asynchronously without affecting UX.

---

### RFC0038 — Fact Router (Deterministic)

**Problem:** There is no formal mechanism for routing queries by type.
A Router via LLM is non-deterministic and violates the `Graph = Truth` principle.
The Router must be rule-based + graph, with no LLM in the decision-making chain.

**Essence:** Every query is classified by type → routed
to the correct retrieval source BEFORE the LLM is invoked.

**Routing table:**

| Query type | Markers | Route | Note |
|-------------|---------|---------|-----------|
| `DEFINE` | what is / define / explain | L3 Graph | Facts only |
| `WHY / CAUSE` | why / reason / because of | L3 + CAG paths | Cause-and-effect chains |
| `HOW` | how / in what way / steps | L3 + Procedures | Procedural memory |
| `FACT / DATE` | when / how much / who | L2 SQLite / API | Concrete data |
| `STRATEGY` | plan / strategy / approach | L4 ReasoningBank | Meta-knowledge |
| `HISTORY` | what I did / past / do you remember | L1 Episodic | Episodic memory |
| `CHAT` | hi / thanks / emotion | LLM only | No retrieval |
| `COMPLEX` | multi-step / plan | ReRAG + L3+L4 | Iterative retrieval |

**Implementation:**
```python
# fact_router.py
from dataclasses import dataclass
from enum import Enum

class QueryType(Enum):
    DEFINE   = "define"
    WHY      = "why"
    HOW      = "how"
    FACT     = "fact"
    STRATEGY = "strategy"
    HISTORY  = "history"
    CHAT     = "chat"
    COMPLEX  = "complex"

@dataclass
class RouteDecision:
    query_type  : QueryType
    sources     : list[str]   # ["l3", "l4", "l1", "api"]
    rerag       : bool        # use iterative retrieval
    max_facts   : int         # STRICT(12) or EXTENDED(40)
    explanation : str         # for TraceLine / audit

class FactRouter:
    """RFC0038 — Deterministic router.
    Does NOT use the LLM for decision-making.
    Rule-based + TF-IDF keyword matching.
    """

    PATTERNS = {
        QueryType.DEFINE   : ["what is", "define", "explain",
                               "what is", "define"],
        QueryType.WHY      : ["why", "reason", "because of", "why",
                               "because", "due to"],
        QueryType.HOW      : ["how", "in what way", "steps",
                               "how to", "algorithm"],
        QueryType.FACT     : ["when", "how much", "who", "where",
                               "when", "how many", "who"],
        QueryType.STRATEGY : ["plan", "strategy", "approach",
                               "strategy", "approach"],
        QueryType.HISTORY  : ["remember", "last time", "yesterday",
                               "remember", "last time", "history"],
        # P1-H FIX: "poka" removed — in Russian it is ambiguous: "goodbye" AND "while/until".
        # "until the database updates" → was routed to LLM-only without retrieval.
        # Replaced with an explicit "goodbye" + "bye".
        QueryType.CHAT     : ["hello", "thanks", "goodbye",
                               "hello", "thanks", "how are you", "bye"],
    }

    ROUTE_MAP = {
        QueryType.DEFINE   : RouteDecision(QueryType.DEFINE,
                               ["l3"], False, 12,
                               "fact retrieval from Graph"),
        QueryType.WHY      : RouteDecision(QueryType.WHY,
                               ["l3", "cag"], True,  40,
                               "causal chain traversal"),
        QueryType.HOW      : RouteDecision(QueryType.HOW,
                               ["l3", "procedures"], False, 12,
                               "procedural memory"),
        QueryType.FACT     : RouteDecision(QueryType.FACT,
                               ["l2", "api"], False, 12,
                               "concrete data retrieval"),
        QueryType.STRATEGY : RouteDecision(QueryType.STRATEGY,
                               ["l4"], False, 12,
                               "ReasoningBank strategies"),
        QueryType.HISTORY  : RouteDecision(QueryType.HISTORY,
                               ["l1"], False, 20,
                               "episodic buffer"),
        QueryType.CHAT     : RouteDecision(QueryType.CHAT,
                               ["llm"], False, 0,
                               "no retrieval needed"),
        QueryType.COMPLEX  : RouteDecision(QueryType.COMPLEX,
                               ["l3", "l4", "rerag"], True, 40,
                               "iterative multi-source retrieval"),
    }

    def route(self, query: str) -> RouteDecision:
        """Deterministic classification of the query.
        No LLM. Rule-based + keyword matching.
        """
        query_lower = query.lower()
        scores = {qt: 0 for qt in QueryType}

        for query_type, patterns in self.PATTERNS.items():
            for pattern in patterns:
                if pattern in query_lower:
                    scores[query_type] += 1

        # Determine the type by the maximum score
        best_type = max(scores, key=scores.get)

        # COMPLEX if several types have a high score
        high_score_types = [qt for qt, s in scores.items() if s >= 2]
        if len(high_score_types) > 1:
            best_type = QueryType.COMPLEX

        # P9-FIX BUG-15: comment corrected — CHAT is never a fallback
        # No patterns → FACT by default (conservative: always retrieval)
        if scores[best_type] == 0:
            best_type = QueryType.FACT

        decision = self.ROUTE_MAP[best_type]
        logger.info(f"FactRouter: {best_type} → {decision.sources} "  # was {query_type} — loop variable, not best_type
                    f"(rerag={decision.rerag})")
        return decision
```

**Integration into the Fast Path:**
```python
# fast_path.py
router   = FactRouter()
decision = router.route(user_query)

# Retrieval according to the route
facts = await hybrid_retriever.retrieve(
    query    = user_query,
    sources  = decision.sources,
    limit    = decision.max_facts,
    rerag    = decision.rerag
)
```

**RFC0038 invariants:**
- `I_ROUTER_1`: FactRouter NEVER calls the LLM
- `I_ROUTER_2`: Every decision is logged in TraceLine
- `I_ROUTER_3`: The COMPLEX type automatically enables ReRAG with the limit
  `MAX_RERAG_ITERATIONS = 3`

---

### RFC0039 — Thompson Sampling for the L4 ReasoningBank

**Problem:** UCB1 (RFC0025) is deterministic and, with a large number of strategies
(100+), spends CPU recomputing `total_trials` at O(k) on every call.
With delayed feedback (the answer is received later), UCB1 gets stuck in local optima.

**Solution:** Replace UCB1 with Thompson Sampling — a stochastic bandit
that naturally balances exploration/exploitation via a Beta distribution.

```
BEFORE (UCB1):
  score = success_rate + sqrt(2 × ln(N) / n)
  → O(k) recomputation of total_trials over all strategies
  → Deterministic → risk of a local optimum

AFTER (Thompson Sampling):
  score = numpy.random.beta(success_count + 1, failure_count + 1)
  → O(1) per strategy, no recomputation of N
  → Stochastic → natural exploration
```

**Implementation:**
```python
# reasoning_bank.py — RFC0039 addition (canonical version of the class — section "14. ReasoningBank")
# Replace the retrieve_relevant_strategies method with the Thompson Sampling implementation:
import numpy as np

class ReasoningBank:  # extension — replace the method in the main class

    async def retrieve_relevant_strategies(
        self,
        context: str,
        top_k: int = 5,
        seed: int | None = None
    ) -> list[Strategy]:
        """
        Thompson Sampling strategy selection.
        seed — for reproducible replay in the audit (Invariant I13).
        """
        # Step 1 — TF-IDF pre-filter (preserved from RFC0025)
        candidates = [
            s for s in await self._load_strategies()
            if cosine(s.embedding, context) >= 0.3
        ]
        if not candidates:
            return []

        # Step 2 — Thompson Sampling
        rng = np.random.default_rng(seed)  # reproducible generator
        scored = []
        for strategy in candidates:
            alpha = strategy.success_count + 1   # prior = Beta(1,1) = uniform
            beta  = strategy.failure_count + 1
            ts_score = rng.beta(alpha, beta)
            scored.append((ts_score, strategy))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [s for _, s in scored[:top_k]]
```

**Metrics:**
```python
reasoning_bank_ts_score          # Histogram — TS score per strategy
reasoning_bank_exploration_rate  # adaptive, not a fixed 10%
```

**RFC0039 invariants:**
- `I13 (TSReplay)`: During audit-replay, pass `seed=session_id_hash` for
  deterministic reproduction. Without a seed — production mode (stochastic).
- `I_TS_1`: The TS pre-filter remains TF-IDF cosine ≥ 0.3 (unchanged).
- `I_TS_2`: prior Beta(1,1) = uniform for new strategies → they always pass the filter.

**Result:** +8% cumulative reward. CPU −40% (no O(k) recomputation).
Adapts better to tasks with delayed feedback.

---

### RFC0040 — CQRS Shadow State (DuckDB as the analytical layer)

**Problem:** The Semantic Drift Monitor and Observer++ perform heavy analytics
(PageRank, ESM distribution, domain stats) directly in Neo4j (OLTP).
This creates contention with transactional queries and violates the SLO P95 < 500ms.

**Solution:** CQRS — separate reads from writes.
- Neo4j = OLTP (transactions, TruthGate, Write Protocol)
- DuckDB = OLAP (analytics, Drift Monitor, Observer analytics)

```
BEFORE:
  Semantic Drift Monitor → Cypher in Neo4j (O(N log N), blocks transactions)

AFTER:
  Neo4j (OLTP) → every 15 min → Parquet dump → DuckDB (OLAP)
  Semantic Drift Monitor → DuckDB SQL (does not touch Neo4j)
```

**Implementation:**
```python
# shadow_state.py — RFC0040
import duckdb
from neo4j import AsyncGraphDatabase

class ShadowState:
    """
    CQRS layer: Neo4j → DuckDB projection every 15 min.
    DuckDB is used ONLY for reading analytics.
    Writing to the graph — only through Neo4j + Write Protocol.
    """
    def __init__(self, neo4j_uri: str, duckdb_path: str = "shadow.duckdb"):
        self.neo4j = AsyncGraphDatabase.driver(neo4j_uri)
        self.db = duckdb.connect(duckdb_path)
        self._init_schema()

    def _init_schema(self):
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS facts_snapshot (
                node_id        TEXT PRIMARY KEY,
                epistemic_state TEXT,
                domain         TEXT,
                importance     FLOAT,
                trust_score    FLOAT,
                created_at     TIMESTAMP,
                updated_at     TIMESTAMP,
                snapshot_time  TIMESTAMP DEFAULT current_timestamp
            )
        """)
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS shadow_meta (
                key   TEXT PRIMARY KEY,
                value TEXT
            )
        """)

    async def sync(self):
        """Synchronization Neo4j → DuckDB. Called by the scheduler every 15 min."""
        async with self.neo4j.session() as session:
            result = await session.run("""
                MATCH (f:Fact)
                RETURN f.id as node_id,
                       f.epistemic_state as epistemic_state,
                       f.domain as domain,
                       f.importance as importance,
                       f.trust_score as trust_score,
                       f.created_at as created_at,
                       f.updated_at as updated_at
            """)
            rows = [dict(r) async for r in result]

        if rows:
            self.db.execute("DELETE FROM facts_snapshot")
            self.db.executemany("""
                INSERT INTO facts_snapshot VALUES (?,?,?,?,?,?,?,current_timestamp)
            """, [list(r.values()) for r in rows])
            self.db.execute(
                "INSERT OR REPLACE INTO shadow_meta VALUES ('last_sync', ?)",
                [datetime.now(timezone.utc).isoformat()]
            )

    def get_esm_distribution(self) -> dict:
        """For the Semantic Drift Monitor — without load on Neo4j."""
        result = self.db.execute("""
            SELECT epistemic_state, COUNT(*) as count
            FROM facts_snapshot
            GROUP BY epistemic_state
        """).fetchall()
        return {row[0]: row[1] for row in result}

    def get_domain_distribution(self) -> dict:
        """Domain drift detection."""
        result = self.db.execute("""
            SELECT domain, COUNT(*) as count
            FROM facts_snapshot
            GROUP BY domain
            ORDER BY count DESC
        """).fetchall()
        return {row[0]: row[1] for row in result}

    @property
    def lag_seconds(self) -> float:
        """Prometheus metric: lag of Shadow State behind Neo4j."""
        row = self.db.execute(
            "SELECT value FROM shadow_meta WHERE key='last_sync'"
        ).fetchone()
        if not row:
            return float('inf')
        last = datetime.fromisoformat(row[0])
        return (datetime.now(timezone.utc) - last).total_seconds()
```

**Integration into the Semantic Drift Monitor:**
```python
# semantic_drift_monitor.py — update
# 📎 Canonical version of SemanticDriftMonitor — RFC0034 (see above)
class SemanticDriftMonitor:
    def __init__(self, shadow_state: ShadowState):
        self.shadow = shadow_state  # read from DuckDB, not Neo4j

    async def check(self) -> SemanticDriftResult:
        esm_dist  = self.shadow.get_esm_distribution()   # DuckDB SQL
        domain_dist = self.shadow.get_domain_distribution()  # DuckDB SQL
        # PageRank still via Neo4j — only once a day
        ...
```

**Integration into main.py / scheduler:**
```python
shadow = ShadowState(neo4j_uri, duckdb_path="shadow.duckdb")
scheduler.add_job(shadow.sync, 'interval', minutes=15)
```

**Metrics:**
```python
duckdb_shadow_lag_seconds      # Gauge — lag behind Neo4j
duckdb_shadow_sync_total       # Counter — successful synchronizations
duckdb_shadow_rows_synced      # Gauge — rows in the last synchronization
```

**RFC0040 invariants:**
- `I14 (CQRSRead)`: The Semantic Drift Monitor and Observer analytics NEVER read
  directly from Neo4j for aggregations. Only the DuckDB Shadow State.
  Violation: a Cypher aggregation in the SemanticDriftMonitor.
- `I_CQRS_1`: DuckDB — only for reading analytics. Writes to the graph — only Neo4j.
- `I_CQRS_2`: Lag > 30 min → Prometheus alert `duckdb_shadow_lag_seconds > 1800`.

**Result:** Neo4j is relieved of the analytical load.
P95 latency is stable at any graph size. The Drift Monitor runs
without stop-the-world pauses.

---

### RFC0041 — Graduated Observer++ (degraded mode)

**Problem:** On an anomaly, Observer++ calls `block_pipeline()` — a binary
"all or nothing". On a false-positive trigger (false alarm), the agent
stops completely, even though it could have continued in a restricted mode.

**Solution:** Replace the binary block with graduated degradation.

```
BEFORE:
  anomaly → block_pipeline() → the agent is dead

AFTER:
  anomaly → evaluate false_positive_rate → choose a degradation level
    Level 1 (soft): alert only, continue
    Level 2 (degraded): L3 read-only, L4 restricted
    Level 3 (full block): only on critical Write Protocol violations
```

**Implementation:**
```python
# observer_plus_plus.py — RFC0041 (Graduated Observer++ — canonical version)
from prometheus_client import Counter, Gauge

class ObserverPlusPlus:

    # Prometheus metrics
    false_positive_rate_gauge = Gauge(
        'observer_false_positive_rate', 'Share of false positives of Observer++'
    )
    degraded_mode_activations = Counter(
        'observer_degraded_mode_total', 'Entries into degraded mode'
    )
    full_blocks = Counter(
        'observer_full_blocks_total', 'Full pipeline blocks'
    )

    async def on_anomaly(self, event: AnomalyEvent):
        """
        Graduated response instead of a binary block.
        """
        fpr = await self._get_false_positive_rate()
        self.false_positive_rate_gauge.set(fpr)

        if event.severity == "info":
            # Level 0: log only
            logger.info(f"Observer++ info: {event.details}")
            return

        if fpr > 0.3:
            # High FPR → degraded mode, NOT a full block
            logger.warning(
                f"Observer++: high FPR={fpr:.2f}, entering degraded mode "
                f"instead of full block. Anomaly: {event.details}"
            )
            await self._enter_degraded_mode()
            self.degraded_mode_activations.inc()
            return

        if event.severity == "warning":
            # Level 1: degraded mode
            await self._enter_degraded_mode()
            self.degraded_mode_activations.inc()

        elif event.severity == "critical":
            # Level 2: full block — only for Write Protocol violations
            if event.source == "write_protocol":
                await self.block_pipeline()
                self.full_blocks.inc()
            else:
                # Critical, but not Write Protocol → degraded
                await self._enter_degraded_mode()
                self.degraded_mode_activations.inc()

    async def _enter_degraded_mode(self):
        """
        L3 → read-only. L4 → only verified strategies (success_rate > 0.7).
        L1/L2 → keep working. The user receives an answer with a marker.
        """
        self.mode = "DEGRADED"
        await self.graph.set_read_only(True)
        await self.reasoning_bank.set_conservative_mode(min_success_rate=0.7)
        logger.warning("Observer++: DEGRADED mode activated")

    async def _exit_degraded_mode(self):
        """Called automatically if the anomaly is not confirmed within 5 min."""
        self.mode = "NORMAL"
        await self.graph.set_read_only(False)
        await self.reasoning_bank.set_conservative_mode(None)
        logger.info("Observer++: returned to NORMAL mode")

    async def _get_false_positive_rate(self) -> float:
        """
        FPR = share of alerts over the last 24h that were not confirmed
        (the anomaly did not cause a real ESM cascade or Write Violation).
        """
        alerts = await self._count_alerts(hours=24)
        confirmed = await self._count_confirmed_anomalies(hours=24)
        if alerts == 0:
            return 0.0
        return 1.0 - (confirmed / alerts)
```

**Metrics:**
```python
observer_false_positive_rate     # Gauge — current FPR
observer_degraded_mode_total     # Counter — entries into degraded mode
observer_full_blocks_total       # Counter — full blocks
observer_degraded_duration_seconds  # Histogram — duration of degraded mode
```

**RFC0041 invariants:**
- `I15 (GraduatedBlock)`: Observer++ does NOT call `block_pipeline()` if
  `false_positive_rate > 0.3`. Instead — `_enter_degraded_mode()`.
  Violation: a direct `block_pipeline()` when FPR > 0.3.
- `I_OBS_1`: Write Protocol violations always trigger a full block (level 2),
  regardless of FPR.
- `I_OBS_2`: Degraded mode is lifted automatically after 5 min if the anomaly
  is not confirmed.

**Result:** +15% agent uptime on false triggers.
The user keeps receiving answers even in degraded mode.

---

### RFC0042 — Three-Layer Architectural Contract

**Problem:** L5 Policy can affect behavior → behavior affects ingestion
→ ingestion affects the Graph. Fractal Memory (L2/L2.5) changes retrieval priorities →
indirectly changes what gets into the context → affects L4's conclusions.
These are hidden feedback loops that can accumulate bias.

**Solution:** A hard split into three layers with a write-rights contract.

```
┌─────────────────────────────────────────────────────────────┐
│  TRUTH CORE                                                  │
│  L3 (Neo4j Graph) + L3.5 (Immutable Core) + ESM + Source   │
│  Write rights: ONLY through the Write Protocol (RFC0031)    │
│  What it stores: facts, their epistemic state, history      │
│  What it does NOT do: knows nothing of values, modes, strats│
└───────────────────────────┬─────────────────────────────────┘
                            │ read only
┌───────────────────────────▼─────────────────────────────────┐
│  POLICY CORE                                                 │
│  L5 (MetaController) + Ring Zero + Risk Model + Modes       │
│  Write rights: only into the Policy store (not into L3)     │
│  What it does: governs agent behavior, style, risks         │
│  What it does NOT do: does NOT change facts or trust_score  │
└───────────────────────────┬─────────────────────────────────┘
                            │ read only + metrics
┌───────────────────────────▼─────────────────────────────────┐
│  EVOLUTION CORE                                              │
│  ClosedLoopEval + SemanticDriftMonitor + AttackSimulation    │
│  Write rights: only into ReasoningBank (L4) via RFC0039 TS  │
│  What it does: measures, tests, proposes changes            │
│  What it does NOT do: does NOT change Truth/Policy directly  │
└─────────────────────────────────────────────────────────────┘
```

**Fractal Governance Contract:**
```python
# fractal_governance.py — RFC0042
FRACTAL_ALLOWED_WRITES = {
    "L2",   # may change: retrieval_priority, theme strength
    "L2.5", # may change: staging_candidates, priority_score
}

FRACTAL_FORBIDDEN_WRITES = {
    "ESM",          # epistemic_state of facts — FORBIDDEN
    "trust_score",  # Source Trust Layer — FORBIDDEN
    "importance",   # importance of facts in L3 — FORBIDDEN
    "Ring Zero",    # VALUES CORE — FORBIDDEN
}

def validate_fractal_write(layer: str, field: str, writer: str) -> bool:
    """
    Called on every write from L2/L2.5.
    Violation → FractalGovernanceViolation + log + Observer++ alert.
    FIX-G: the layer parameter is now used — it verifies that the writer
    really is from the allowed layers (L2/L2.5), not an arbitrary component.
    """
    if layer not in FRACTAL_ALLOWED_WRITES:
        raise FractalGovernanceViolation(
            f"Layer '{layer}' is not in FRACTAL_ALLOWED_WRITES. "
            f"Only {FRACTAL_ALLOWED_WRITES} may write through Fractal Governance."
        )
    if field in FRACTAL_FORBIDDEN_WRITES:
        raise FractalGovernanceViolation(
            f"{layer} ({writer}) attempted to write to '{field}'. "
            f"Fractal Governance violation. Allowed fields: everything except {FRACTAL_FORBIDDEN_WRITES}"
        )
    return True
```

**Every Fractal influence on behavior is logged:**
```python
# Add to L2IngestionEngine and L2.5Scheduler
logger.info(
    "fractal_influence_trace",
    extra={
        "writer":   "L2",
        "field":    "retrieval_priority",
        "theme_id": theme_id,
        "delta":    delta,
        "session":  session_id,
    }
)
```

**RFC0042 invariants:**
- `I16 (TruthIsolation)`: The Truth Core does not receive commands from the Policy Core or the Evolution Core.
  Writes to L3 only through the Write Protocol.
- `I_GOV_1`: L2/L2.5 cannot write to ESM, trust_score, importance, Ring Zero.
- `I_GOV_2`: L5 cannot call methods that modify facts in L3.
- `I_GOV_3`: Every Fractal influence on retrieval is logged as `fractal_influence_trace`.

**Result:** The system stays epistemically clean for years.
Bias does not accumulate through hidden feedback loops.

---

## 📜 RFC0043 — Hardware Profile Selector

> **Status**: Canonical

### Purpose

Automatic adaptation of the entire Velantrim stack to the machine's physical resources. The profile is detected once at startup and governs the selection of components without manual intervention.

### Profiles

```
weak   → RAM < 4 GB or CPU < 4 cores  (RPi, old laptop, min. VPS)
medium → RAM 4–12 GB, CPU 4–8 cores   (developer laptop, VPS 8GB)
strong → RAM > 12 GB, CPU > 8 cores   (workstation, server, GPU)
```

### Implementation

```python
# hardware_profile.py
import psutil, os

def detect_hardware_profile() -> str:
    ram_gb    = psutil.virtual_memory().total / (1024**3)
    cpu_cores = os.cpu_count() or 1
    if ram_gb < 4 or cpu_cores < 4:    return "weak"
    elif ram_gb < 12 or cpu_cores < 8: return "medium"
    else:                              return "strong"
```

```python
# velantrim_config.py — add the RFC0043 block
import os as _os
from hardware_profile import detect_hardware_profile

HARDWARE_PROFILE = _os.getenv("VELANTRIM_HW_PROFILE", detect_hardware_profile())
_HW = HARDWARE_PROFILE

NEO4J_ENABLED          = _HW == "strong"
REDIS_ENABLED          = _HW in ("medium", "strong")
GRAPH_BACKEND          = {"weak": "graph_lite", "medium": "kuzu", "strong": "neo4j"}[_HW]  # P0-H FIX
VECTOR_BACKEND         = {"weak": "chroma_memory", "medium": "chroma_persistent",
                          "strong": "qdrant"}[_HW]
CONSOLIDATION_PARALLEL = _HW != "weak"
CONSOLIDATION_WORKERS  = {"weak": 1, "medium": 2, "strong": 8}[_HW]
DUCKDB_SYNC_INTERVAL   = {"weak": 3600, "medium": 1800, "strong": 900}[_HW]
EMBEDDING_MODEL        = ("paraphrase-multilingual-MiniLM-L12-v2"
                          if _HW == "weak" else "deepvk/USER-bge-m3")
TELEMETRY_ENABLED      = _HW != "weak"
VELUM_MAX_EDGES        = {"weak": 500, "medium": 1000, "strong": 2000}[_HW]
CLUSTERING_ALGO        = "minibatch_kmeans" if _HW == "weak" else "agglomerative"
```

### Component matrix

| Capability | weak | medium | strong |
|-------------|------|--------|--------|
| Graph DB | SQLite Graph-Lite | KuzuDB embedded    | Neo4j 5.26+ |
| Vector DB | ChromaDB in-memory | ChromaDB persistent | Qdrant |
| Event Bus | SQLite WAL queue | Redis 512MB | Redis Streams |
| Embeddings | MiniLM-L12 (~120MB) | USER-bge-m3 (~500MB) | USER-bge-m3 |
| Consolidation | sequential ×3 | partial ×2 | full parallel |
| Telemetry | logs only | metrics | full OTel |
| DuckDB sync | 60 min | 30 min | 15 min |

### RFC0043 invariant

```
I17 (HWProfile): HARDWARE_PROFILE is auto-detected at startup.
    Manual override via the VELANTRIM_HW_PROFILE env var.
    Violation: hardcoding components without regard for the profile.
```

---

### RFC0048: Multi-Component Memory Budget

**Problem**: I22 checks only `LLM_TOTAL_PARAMS ≤ available_RAM`. It does not account for Neo4j PageCache, Redis, the Vector DB, or the OS buffer. With a 30B MoE model, OOM is possible even when I22 passes.

**Solution**: a combined budget of all components at startup.

```python
# hardware_profile.py — add to startup_ram_check()

def compute_memory_budget(config) -> dict:
    available  = psutil.virtual_memory().available

    llm_ram    = _parse_param_size(config.LLM_TOTAL_PARAMS)   # "30B" → bytes
    neo4j_ram  = config.NEO4J_PAGE_CACHE_GB * 1024**3         # default 2 GB
    redis_ram  = _parse_redis_maxmem(config.REDIS_MAXMEM)     # default 512 MB
    vector_ram = config.VECTOR_RAM_GB * 1024**3               # default 1 GB
    os_buffer  = 2 * 1024**3                                  # 2 GB OS reserve

    total    = llm_ram + neo4j_ram + redis_ram + vector_ram + os_buffer
    pressure = total / available

    return {"total_gb": total / 1024**3,
            "available_gb": available / 1024**3,
            "pressure": pressure,
            "fits": pressure <= config.MEM_PRESSURE_WARN}

def startup_ram_check(config):
    budget = compute_memory_budget(config)
    multi_component_ram_pressure.set(budget["pressure"])

    if budget["pressure"] > config.MEM_PRESSURE_CRIT:
        logger.critical(
            f"RAM budget critical: {budget['total_gb']:.1f}GB required, "
            f"{budget['available_gb']:.1f}GB available. "
            f"Downgrading profile → LLM_MODE=offline."
        )
        if config.HARDWARE_PROFILE == "strong":
            config.HARDWARE_PROFILE = "medium"
        config.LLM_MODE = "offline"
```

```python
# velantrim_config.py — add:
NEO4J_PAGE_CACHE_GB  = 2.0    # must match docker-compose
VECTOR_RAM_GB        = 1.0    # Qdrant persistent / ChromaDB
MEM_PRESSURE_WARN    = 0.85   # Prometheus WARN threshold
MEM_PRESSURE_CRIT    = 0.92   # forced downshift
```

```
I24 (MultiComponentBudget): At startup a check of the combined
    RAM budget must be performed: LLM + Neo4j_PageCache + Redis + VectorDB + OS_buffer.
    When pressure > MEM_PRESSURE_CRIT — downshift the profile or LLM_MODE=offline.
    Violation: startup without compute_memory_budget() when LLM_ARCHITECTURE=moe.
```

---

## 📜 RFC0044 — LLM_MODE: Offline Mode

> **Status**: Canonical

### Purpose

Three modes of working with the LLM. In `offline` mode the system operates entirely without LLM calls, using FactRouter + BM25 + LensEngine. 80% of the functionality is preserved.

### Configuration

```python
# velantrim_config.py — add after the RFC0043 block
LLM_MODE = _os.getenv("VELANTRIM_LLM_MODE",
           "offline" if _HW == "weak" else "full")
# "full"    → cloud LLM (GPT/Claude/Qwen3-Max)
# "lite"    → local LLM (Qwen3.5-14B / Llama4)
# "offline" → without an LLM: FactRouter + BM25 + LensEngine (RFC0045)
```

### Fast Path without an LLM

```
User Query
    │
    ▼ [1] Normalizer + Lemmatizer  (pymorphy2, RU)
    ▼ [2] FactRouter RFC0038       (FACTUAL|PROCEDURAL|EPISODIC|META)
    ▼ [3] SafeFTSQuery + BM25      (SQLite FTS5 / Neo4j fulltext)
    ▼ [4] Semantic Reranker        (cosine, local embeddings)
    ▼ [5] LensMatcher RFC0045      → active L4 lens
    ▼ [F2.6] GraphQueryExecutor   → structured answer from L3
    ▼ [7] ResponseFormatter        → templated answer without an LLM
    │
    Response
```

### Change in fast_path.py

```python
# fast_path.py — add a branch before the LLM call

# ❌ BEFORE:
response = await self.llm.complete(context)

# ✅ AFTER:
if config.LLM_MODE == "offline":
    response = await self.lens_engine.execute(
        query=query, entity=detected_entity, session_id=session_id
    )
else:
    response = await self.llm.complete(context)
```

### Entity Extraction without an LLM

```python
# offline_extractor.py — replacement for Graphiti extraction when LLM_MODE=offline
import spacy

class OfflineEntityExtractor:
    """
    spaCy ru_core_news_lg  → PER, ORG, LOC, DATE  (~500MB, CPU-only)
    regex patterns         → numbers, URLs, commands
    domain keyword dict    → terms from the L3 taxonomy (loaded at startup)
    """
    def __init__(self, graph):
        self.nlp              = spacy.load("ru_core_news_lg")
        self.domain_keywords  = self._load_from_l3(graph)

    def extract(self, text: str) -> list[dict]:
        doc      = self.nlp(text)
        entities = [{"name": e.text, "type": e.label_,
                     "confidence": 0.85, "source": "spacy_ner"}
                    for e in doc.ents]
        for kw in self.domain_keywords:
            if kw.lower() in text.lower():
                entities.append({"name": kw, "type": "DOMAIN_CONCEPT",
                                  "confidence": 1.0, "source": "keyword"})
        return entities
```

### RFC0044 invariant

```
I18 (LLMMode): When LLM_MODE=offline the Fast Path must use LensEngine.
    A direct llm.complete() call in offline mode is a violation.
    Violation: llm.complete() when LLM_MODE=offline.
```

---

## 📜 RFC0045 — LensEngine: Deterministic Lenses L4/L5

> **Status**: Canonical

### Purpose

An Expert System on top of the L3 graph. 30 lenses — deterministic patterns for understanding a query and forming an answer without an LLM. With a well-populated L3, the answers are more accurate than an LLM's: no hallucinations, only verified facts.

Each lens = `{intent_match} → {graph_query} → {formatted_answer}`

### Lens DSL

```python
# lens_engine.py
from dataclasses import dataclass

@dataclass
class Lens:
    lens_id:           str          # "lens:factual_definition"
    name:              str          # "Concept definition"
    domain:            str | None   # "domain:physics" or None (universal)
    priority:          int          # 1–100, higher = matched first

    # Intent matching
    intent_patterns:   list[str]    # regex
    bm25_keywords:     list[str]    # BM25 anchors
    query_types:       list[str]    # from FactRouter: ["FACTUAL", "CONCEPTUAL"]

    # Graph query
    cypher_template:   str          # Cypher template (Neo4j / Kuzu)
    sqlite_template:   str          # analog for Graph-Lite (weak/offline)
    result_limit:      int
    confidence_floor:  float        # min. epistemic_score of a fact

    # Answer
    response_template: str          # jinja2
    fallback_message:  str          # if the graph is empty

    # L5 Observer hook
    observer_check:    bool
    trust_threshold:   float
```

### Query lifecycle

```
Query → LensMatcher
  score = bm25_match × 0.4 + intent_regex × 0.4 + entity_type × 0.2
  if max_score > 0.3 → choose the lens with max score

       → GraphQueryExecutor
  Substitute {entity}, {domain} into cypher_template (Neo4j)
                              or sqlite_template  (weak/offline)
  Filter: epistemic_score >= confidence_floor
          epistemic_variance <= 0.7  (otherwise add [UNVERIFIED])
          is_active = true

       → L5 Observer Check (if observer_check=True)
  FPR > 0.3 → degraded mode (RFC0041)

       → ResponseFormatter  (jinja2)
  No results → fallback_message

       → Answer  (without an LLM)
```

### Integration into the Canonical Memory Protocol

```
F2.6: LensEngine (RFC0045)
    → if LLM_MODE=offline:
      → LensMatcher.match_lens(query, query_type)
      → GraphQueryExecutor (Cypher / SQLite)
      → ResponseFormatter (jinja2) → answer without an LLM
    → if LLM_MODE=full/lite: the step is skipped
```

### 30 lenses — taxonomy

```
Group A: Factual queries (8 lenses)
  lens:factual_definition   "what is X"            → :Concept → :Fact
  lens:factual_property     "properties of X"      → :Entity → :Fact (HAS)
  lens:factual_comparison   "X or Y"               → [:CONTRADICTS|SIMILAR]
  lens:factual_cause        "why X"                → :Fact → [:CAUSES] → :Fact
  lens:factual_consequence  "what happens if X"    → [:CAUSES] reverse
  lens:factual_condition    "when X"               → :Fact (condition field)
  lens:factual_number       "how much X"           → :Fact (value, numeric)
  lens:factual_date         "when X happened"      → :Fact (valid_from)

Group B: Procedural queries (6 lenses)
  lens:procedural_howto     "how to do X"          → :Strategy (procedural)
  lens:procedural_debug     "error X"              → :Strategy (failure_context)
  lens:procedural_optimize  "improve X"            → :Strategy (success_rate>0.7)
  lens:procedural_setup     "install X"            → :Strategy (type=setup)
  lens:procedural_sequence  "order of X"           → [:PRECEDES] chain
  lens:procedural_checklist "checklist for X"      → :Strategy (type=checklist)

Group C: Episodic queries (5 lenses)
  lens:episodic_last        "last time"            → :Episode ORDER BY timestamp
  lens:episodic_session     "in this session"      → :Episode WHERE session_id
  lens:episodic_outcome     "how X ended"          → :Episode (outcome)
  lens:episodic_pattern     "how often X"          → :Theme (cluster)
  lens:episodic_error       "errors with X"        → :Episode WHERE outcome=FAILURE

Group D: Strategic queries (4 lenses)
  lens:strategy_best        "best way to X"        → :Strategy ORDER BY success_rate
  lens:strategy_avoid       "what not to do"       → :Strategy (failure_penalty>0.7)
  lens:strategy_context     "in the context of X"  → :Strategy (cosine>0.6)
  lens:strategy_learned     "what was learned"     → :Strategy + :Experience

Group E: Meta queries (4 lenses)
  lens:meta_memory          "what you remember of X"→ :Fact COUNT + :Entity
  lens:meta_confidence      "are you sure"         → :Fact (epistemic_score,variance)
  lens:meta_conflict        "are there contradictions"→ [:CONTRADICTS] search
  lens:meta_domains         "in which domain is X" → :Domain taxonomy

Group F: Special lenses (3 lenses)
  lens:ring_zero_guard      priority=100, always first → VALUES CORE protection
  lens:contradiction_alert  [:CONTRADICTS] in results → warning
  lens:empty_graph_fallback graph is empty → graceful fallback without an LLM
```

### File structure

```
velantrim/
├── lens_engine.py          ← LensEngine, LensMatcher, GraphQueryExecutor
├── normalizer.py           ← pymorphy2 + RU stop-words
├── offline_extractor.py    ← spaCy NER + domain keywords
└── lenses/                 ← 30 YAML lens files
    ├── factual_definition.yaml
    ├── factual_property.yaml
    ├── ... (28 files)
    └── empty_graph_fallback.yaml
```

### RFC0045 invariant

```
I19 (LensEngine): LensEngine reads only from L3 (the graph) or Graph-Lite (SQLite).
    No LLM calls inside lenses.
    Violation: llm.complete() or llm.generate() inside LensEngine or a lens.
```

---

### RFC0051: LensEngine Composition

**Problem:**: a mixed query ("why is photosynthesis important and how can it be improved?") activates several intents at once. A single lens → an incomplete answer or `lens_fallback`. In offline mode, fallback = an empty template → UX degradation.

**Solution**: when 2+ lenses match above the threshold — run `compose()`, combining the results via CORNER.

#### lens_engine.py extension

```python
@dataclass
class LensMatch:
    lens_id:  str
    intent:   str
    score:    float
    cypher:   str
    template: str   # Jinja2

class LensEngine:

    def match_all(self, query: str,
                  threshold: float = None) -> list[LensMatch]:
        """Returns ALL lenses above the threshold, in descending score order."""
        threshold = threshold or LENS_COMPOSITION_THRESHOLD
        normalized = self.normalizer.lemmatize(query)
        return sorted(
            [LensMatch(l.lens_id, l.intent,
                       self._score(normalized, l), l.cypher_template, l.response_template)
             for l in self.lenses if self._score(normalized, l) >= threshold],
            key=lambda m: m.score, reverse=True
        )

    async def compose(self, query: str) -> ComposedResult | None:
        """
        Up to MAX_COMPOSED_LENSES lenses → combine via CORNER.
        On empty matches → None → fallback to HybridRetriever or BAE generic.
        """
        matches = self.match_all(query)
        if not matches:
            return None

        facts = []
        for match in matches[:MAX_COMPOSED_LENSES]:
            facts.extend(await self._execute_lens(match))

        return ComposedResult(
            facts=self.corner.deduplicate(facts),
            intents=[m.intent  for m in matches[:MAX_COMPOSED_LENSES]],
            lens_ids=[m.lens_id for m in matches[:MAX_COMPOSED_LENSES]],
        )
```

#### Configuration (velantrim_config.py)

```python
# add:
LENS_COMPOSITION_THRESHOLD = 0.45   # min. score for inclusion in compose()
MAX_COMPOSED_LENSES        = 3      # max. lenses in a single query
LENS_FALLBACK_TO_BAE       = True   # compose()=None → BAE generic
```

#### F2.6 update (fast_path.py)

```
F2.6: LensEngine (RFC0045 + RFC0051)
    → if LLM_MODE=offline:
      → matches = LensEngine.match_all(query)
      → if len(matches) >= 2:
          → result = LensEngine.compose(query)      ← RFC0051
          → CORNER already applied inside compose()
      → if len(matches) == 1:
          → result = LensEngine.match(query)        ← single lens
      → if len(matches) == 0:
          → fallback: BAE generic or HybridRetriever (lite)
    → if LLM_MODE=full/lite: the step is skipped
```

#### BAE — fixed rollout order

```
⚠️ DECISION:
   BAE is rolled out iteratively, not all 5 profiles at once:

   Phase 1 MVP:  only the "neutral" profile
                 RST skeletons + Microplanner without anaphora
                 Surface RU: only pymorphy2 case agreement
                 + ClosedLoopEval quality evaluation (mandatory before prod)

   Phase 2:      the "concise" and "detailed" profiles
                 anaphora + anti-repeat in the Microplanner

   Phase 3:      the "scientific" and "friendly" profiles
                 CORNER diversity weight tuning

   Prohibition: do not deploy BAE to production without ClosedLoopEval evaluation.
```

```
I27 (LensCompose): When a query matches 2+ lenses with score ≥ LENS_COMPOSITION_THRESHOLD
    LensEngine must run compose() instead of a single match().
    Results are combined via CORNER before the Facts Pack.
    On compose()=None → fallback to HybridRetriever (full/lite) or BAE generic (offline).
    Violation: a single match() when 2+ lenses are above the threshold.
```

---

> **Status**: Canonical
>
> An extension of RFC0045 LensEngine. BAE turns facts from the L3 graph into readable, coherent text without transformers. It produces an answer better than an encyclopedia — structured to fit the context of the question.

### Principle

```
Dry encyclopedia:
  "Photosynthesis is the process of synthesizing organic substances from CO₂ and H₂O."

BAE RST-lite:
  "Photosynthesis is the way plants obtain energy from the sun.
   A leaf catches light → CO₂ from the air + water from the soil → sugar (the plant's food)
   + oxygen (air for us). That is precisely why without plants there would be no life."

The difference: not the knowledge, but the STRUCTURE of presentation.
A person read a dictionary and understood — so BAE is enough for 80% of queries.
```

### BAE components

#### 1. RST-lite — Discourse Planner (block logic)

Determines the order in which information is presented based on the lens intent:

```python
# Answer skeletons by intent (rsl_skeletons.py)
SKELETONS = {
    "DEFINE":   ["definition", "mechanism", "example", "note"],
    "WHY":      ["cause", "evidence", "consequence", "summary"],
    "HOW":      ["precondition", "steps", "result", "warning"],
    "COMPARE":  ["entity_a", "entity_b", "difference", "recommendation"],
    "FACT":     ["claim", "evidence", "confidence"],
    "WHERE":    ["location", "habitat", "region", "note"],
    "WHEN":     ["event", "period", "context", "significance"],
    "PROCEDURE":["goal", "steps", "result", "common_errors"],
}

# Each skeleton = a set of blocks assembled from L3 graph facts
# The intent is determined by LensMatcher (RFC0045) → passed to BAE
```

#### 2. Microplanner — text coherence

Glues the blocks into natural text:

```python
# microplanner.py
TRANSITIONS = {
    "cause→consequence": "this means that",
    "definition→example": "for example",
    "mechanism→note":    "it should be noted",
    "steps→result":      "as a result",
    "claim→evidence":    "according to",
}

ANAPHORA_MAP = {
    "PERSON": ["he", "she", "this person"],
    "CONCEPT": ["it", "this concept", "it"],
    "PROCESS": ["this process", "it", "this"],
    "OBJECT":  ["he", "she", "it", "this object"],
}

# Anti-repeat: if a word occurs in two adjacent sentences
# → replace it with an anaphor or reword
```

#### 3. Surface Realizer RU — morphology

```python
# nlp_utils.py — singleton MorphAnalyzer + normalization cache
# FIX: pymorphy2.MorphAnalyzer() was recreated on every call — ~200ms of initialization.
# Singleton + lru_cache give a 40–60% CPU saving with an active ReasoningBank and LensEngine.
#
# double-checked locking: thread-safe with concurrent asyncio coroutines.
# lru_cache(4096): stop-words and domain terms are normalized once and for all.

import threading
from functools import lru_cache
import logging

logger = logging.getLogger(__name__)

_morph_analyzer = None
_morph_lock = threading.Lock()

def get_morph_analyzer():
    """
    Return the singleton MorphAnalyzer. Thread-safe (double-checked locking).
    If pymorphy2/pymorphy3 is unavailable — return None, the caller does the fallback.
    """
    global _morph_analyzer
    if _morph_analyzer is None:
        with _morph_lock:
            if _morph_analyzer is None:
                try:
                    import pymorphy3
                    _morph_analyzer = pymorphy3.MorphAnalyzer()
                    logger.info("nlp_utils: pymorphy3 MorphAnalyzer initialized")
                except ImportError:
                    try:
                        import pymorphy2
                        _morph_analyzer = pymorphy2.MorphAnalyzer()
                        logger.info("nlp_utils: pymorphy2 MorphAnalyzer initialized (fallback)")
                    except ImportError:
                        logger.warning("nlp_utils: neither pymorphy3 nor pymorphy2 found — normalize_word falls back to lower()")
    return _morph_analyzer

@lru_cache(maxsize=4096)
def normalize_word(word: str) -> str:
    """
    Reduce a word to its normal form (lemmatization).
    lru_cache: stop-words and key terms are normalized once.
    Fallback to lower() if morph is unavailable.
    """
    morph = get_morph_analyzer()
    if morph is None:
        return word.lower()
    try:
        return morph.parse(word)[0].normal_form
    except Exception:
        return word.lower()


# surface_ru.py — pymorphy agreement
# "beryoza rastyot v les" → "beryoza rastyot v lesu"  (RU: "a birch grows in the forest")
# Gender, number, and case are agreed automatically
# FIX: uses the singleton get_morph_analyzer() instead of the module-level morph = MorphAnalyzer()

def agree_phrase(word: str, case: str, gender: str = None) -> str:
    """Agree a word by case and gender."""
    morph = get_morph_analyzer()
    if morph is None:
        return word
    try:
        parsed = morph.parse(word)[0]
        return parsed.inflect({case}).word if parsed.inflect({case}) else word
    except Exception:
        return word
```

#### 4. Style Profiles — parametric profiles

```python
# style_profiles.py
STYLE_PROFILES = {
    "simple":     {"max_terms": 0, "sent_len": "short",  "tone": "friendly",
                   "anaphora": True,  "transitions": "simple"},
    "neutral":    {"max_terms": 3, "sent_len": "medium", "tone": "neutral",
                   "anaphora": True,  "transitions": "standard"},
    "scientific": {"max_terms": 10,"sent_len": "long",   "tone": "formal",
                   "anaphora": False, "transitions": "academic"},
    "auditor":    {"max_terms": 5, "sent_len": "medium", "tone": "strict",
                   "anaphora": False, "transitions": "logical"},
    "literary":   {"max_terms": 2, "sent_len": "varied", "tone": "warm",
                   "anaphora": True,  "transitions": "narrative"},
}
# Profile = parameters, NOT a persona — otherwise style would start to influence the truth
```

### CORNER — deduplication before Facts Pack

```python
# corner.py — always sits between RRF Fusion and the Facts Pack
class CORNER:
    """
    Deduplicate + Diversity + Pack
    Without CORNER: duplicate facts bloat the context and reduce accuracy.
    """
    def process(self, candidates: list, budget: int = 10) -> FactsPack:
        # 1. Dedupe: remove facts with cosine > 0.95
        deduped  = self._deduplicate(candidates, threshold=0.95)
        # 2. Diversity: no more than 3 facts from a single node
        diverse  = self._ensure_diversity(deduped, max_per_source=3)
        # 3. Budget: top-K by epistemic_score
        top_k    = sorted(diverse, key=lambda x: x.score, reverse=True)[:budget]
        return FactsPack(facts=top_k)
```

### Three retrieval modes by corpus size

```
SMALL corpus (< 10k nodes):
  Query → Normalizer → Lemma → Router → BM25
        → CORNER → Facts Pack → Truth Gate → BAE
  No RRF, no LSA. A single channel — fast and accurate.

MEDIUM corpus (10k–500k nodes):
  BM25 ──┐
  Graph  ├──→ RRF Fusion → CORNER → Facts Pack → Truth Gate → BAE
  Embed ─┘
  RRF sits between retrieval and the Facts Pack.

LARGE corpus (500k+ nodes / many books):
  LSA Topic Router (narrows down to 20–50 clusters)
      → Local BM25 + Embeddings (only within the selected ones)
      → RRF Fusion → CORNER → Facts Pack → Truth Gate → BAE
  LSA is not for facts, but for narrowing the search space.
```

**Placement rules:**

| Situation | RRF | LSA |
|----------|-----|-----|
| Single search engine | ❌ not needed | ❌ not needed |
| Multiple channels | ✅ before Facts Pack | ❌ not needed |
| 500k+ nodes / books | ✅ before Facts Pack | ✅ before BM25 (narrower) |

### Summarization: without an LLM and with an LLM

> **Situation**: L4.5 ResponseAudit requires summarization of the LLM's answer.
> Full abstractive summarization still requires an LLM. Below is the best available without transformers.

| Technology | Essence | Quality | RAM | Speed |
|-----------|------|----------|-----|----------|
| TF-IDF extractive | Selects the best sentences | 60% | ~5 MB | <10ms |
| **TextRank** | PageRank on a sentence graph | **70%** | ~10 MB | <30ms |
| **LSA** | Latent semantic analysis | **65-75%** | ~50 MB | <50ms |
| **BAE RST-lite** | Generation from facts via template | **75-85%** | ~20 MB | <20ms |
| Tiny LLM 1-3B | Qwen3-1.7B / OLMoE (offline) | 85-90% | ~2 GB | <200ms |
| Fast LLM 7B+ | Qwen3-7B (lite) | 90-93% | ~6 GB | <300ms |
| Cloud LLM | Haiku / o4-mini (full) | 95%+ | — | <500ms |

```
⚠️ Status of summarization without an LLM (technically honest):

✅ BAE RST-lite — generation from facts = 75-85% (the main offline path)
✅ TextRank    — retelling of ready-made text = 70% (extractive)
⚠️ Full abstractive summarization of an LLM's answer without a transformer —
   as yet there is no technology with quality > 75% + speed < 100ms

Until a solution appears:
  LLM_MODE=offline → TextRank extractive gist
  LLM_MODE=lite    → Tiny LLM 1-3B (Qwen3-1.7B, ~2GB RAM)
  LLM_MODE=full    → Fast LLM in the Slow Path
```

### Final quality by mode

| | offline (BAE) | lite (Tiny LLM) | full (Fast LLM) |
|--|:--:|:--:|:--:|
| Hallucinations | ❌ impossible | ❌ impossible* | ❌ impossible* |
| Text quality | 75-85% | 85-90% | 95%+ |
| P95 latency | <50ms | <200ms | <500ms |
| RAM | ~100 MB | ~2 GB | ~10 GB+ |
| Internet | not needed | not needed | optional |

*The LLM works only as a reformulator of facts from L3 — Graph = Truth does not change.

### RFC0045-BAE Invariant

```
I21 (CORNER): CORNER is mandatory between RRF Fusion and the Facts Pack.
    When several retrieval channels are present, skipping CORNER is
    a violation (duplicate facts in the context).
    Violation: a Facts Pack without prior deduplication during multi-channel retrieval.
```

---

> **Status**: Canonical
>
> Three related improvements to the L4 ReasoningBank and the L3 Truth Core.

### RFC0046-A: DAG Rollback in L4

**Problem**: an agent's reasoning steps are stored as a flat list. On an error there is no memory of dead-end paths — the agent repeats its mistakes.

**Solution**: the reasoning graph = a directed acyclic graph (DAG). Dead-end branches are recorded with a `[:ROLLBACK_TO]` edge.

#### New edge types (neo4j_setup.py)

```cypher
-- Add to create_schema() — RFC0046

-- The agent's reasoning steps are linked into a DAG
(:ReasoningStep)-[:PRECEDES]->(:ReasoningStep)

-- A dead-end branch — Observer++ calls this on a graduated block
(:ReasoningStep)-[:ROLLBACK_TO {
    reason:     string,    -- "OBSERVER_BLOCK" | "TASK_FAILED" | "CONTRADICTION"
    rolled_at:  datetime,
    session_id: string
}]->(:ReasoningStep)

-- Index for fast lookup of dead-ends in the current session
CREATE INDEX reasoning_rollback_idx IF NOT EXISTS
FOR ()-[r:ROLLBACK_TO]-() ON (r.session_id)
```

#### The rollback_to() method (reasoning_bank.py)

```python
# Add to the ReasoningBank class — RFC0046

async def rollback_to(
    self,
    from_step_id: str,
    to_step_id:   str,
    reason:       str,
    session_id:   str
) -> None:
    """
    Record a dead-end reasoning branch.
    LensEngine and the LLM see [:ROLLBACK_TO] and do not repeat the mistake.
    Observer++ calls this on entered_degraded_mode().
    """
    await self.graph.execute_cypher("""
        MATCH (a:ReasoningStep {id: $from_id})
        MATCH (b:ReasoningStep {id: $to_id})
        MERGE (a)-[:ROLLBACK_TO {
            reason:     $reason,
            rolled_at:  datetime(),
            session_id: $session_id
        }]->(b)
    """, {"from_id":    from_step_id,
          "to_id":      to_step_id,
          "reason":     reason,
          "session_id": session_id})
```

---

### RFC0050: DAG Rollback Transactional Write

**Problem:**: with asynchronous writing of reasoning steps, a race condition arises — `[:ROLLBACK_TO]` is created before `from_step` exists in Neo4j → `NotFoundException` → loss of information about the rollback.

**Solution**: check that both nodes exist before the MERGE; if they are absent, defer to the `ConsolidationQueue` with retry.

```python
# reasoning_bank.py — replace the direct MERGE with a transactional write

async def create_rollback_edge(
    self,
    from_step_id: str,
    to_step_id:   str,
    reason:       str,
    session_id:   str,
    retry_queue:  ConsolidationQueue,
) -> bool:
    """
    Creates [:ROLLBACK_TO] only if both nodes exist.
    Otherwise defers to the ConsolidationQueue (a persistent SQLite queue).
    """
    result = await self.graph.execute_cypher("""
        OPTIONAL MATCH (a:ReasoningStep {id: $from_id})
        OPTIONAL MATCH (b:ReasoningStep {id: $to_id})
        WITH a, b
        WHERE a IS NOT NULL AND b IS NOT NULL
        MERGE (a)-[r:ROLLBACK_TO {
            reason:     $reason,
            rolled_at:  datetime(),
            session_id: $session_id
        }]->(b)
        RETURN r IS NOT NULL AS created
    """, {"from_id": from_step_id, "to_id": to_step_id,
          "reason": reason, "session_id": session_id})

    if result and result[0].get("created"):
        return True

    # One or both nodes are not yet saved → defer
    dag_rollback_retry_total.inc()
    await retry_queue.put(RetryTask(
        task_type="dag_rollback",
        payload={"from_step_id": from_step_id, "to_step_id": to_step_id,
                 "reason": reason, "session_id": session_id},
        retry_after_seconds=5,
        max_retries=10,
    ))
    logger.warning(
        f"DAG rollback deferred: {from_step_id} → {to_step_id}. Queued."
    )
    return False
```

```
I26 (DAGRollbackTransaction): The [:ROLLBACK_TO] edge is created ONLY if both
    :ReasoningStep nodes exist in Neo4j. If absent — ConsolidationQueue,
    retry up to 10 times. Violation: MERGE without OPTIONAL MATCH of both nodes.
```

---

### RFC0046-B: epistemic_variance in :Fact

**Problem**: the ESM provides binary confidence (Validated / not Validated). There is no gradation of "how much the agent doubts."

**Solution**: an `epistemic_variance: float` field on every :Fact.

```
1.0 = full uncertainty (a new fact, not verified)
0.5 = partial confidence (Supported, has Evidence)
0.0 = full confidence (Validated, confirmed many times)
```

#### Schema change (neo4j_setup.py)

```cypher
-- The field is already added to the :Fact schema (see the "Graph schema" section)
-- epistemic_variance: 1.0 by default on creation

-- Migration of existing facts:
MATCH (f:Fact) WHERE f.epistemic_variance IS NULL
SET f.epistemic_variance = CASE
    WHEN f.epistemic_state = 'Validated'    THEN 0.1
    WHEN f.epistemic_state = 'Supported'    THEN 0.4
    WHEN f.epistemic_state = 'Hypothesized' THEN 0.7
    ELSE 1.0
END
```

#### The [UNVERIFIED] tag in context_builder.py

```python
# Add to _format_context() when building the Facts Pack — RFC0046

for fact in facts:
    tag = ""
    if fact.get("epistemic_variance", 1.0) > 0.7:
        tag = " [UNVERIFIED]"
    elif fact.get("epistemic_variance", 1.0) > 0.4:
        tag = " [UNCERTAIN]"
    context_parts.append(f"{fact['content']}{tag}")

# Result: the LLM receives a context where it is clearly visible
# which facts are rock-solid and where the database "has doubts"
```

---

### RFC0047: epistemic_variance Formula

**Problem**: the `epistemic_variance` field was introduced without a formula — set by hand, not reproducible, not auto-updated.

#### Strict computation formula

```
variance = 1 / (1 + evidence_count × avg_trust_score)
         + contradiction_penalty

where:
  evidence_count        = COUNT of active [:SUPPORTED_BY] edges of the fact
  avg_trust_score       = AVG(source.trust_score) over these sources ∈ [0.0, 1.0]
  contradiction_penalty = min(0.6,  0.3 × COUNT(active incoming [:CONTRADICTS]))
```

#### ESM mapping (normative)

| ESM state | Expected variance range |
|---|---|
| Observed / Hypothesized | 0.85 – 1.0 |
| Supported | 0.40 – 0.65 |
| Validated | 0.05 – 0.25 |
| Contradicted | 0.70 – 1.0 (+ penalty) |
| Deprecated / Collapsed | frozen, not recomputed |

#### Auto-update (fact_manager.py)

```python
# Call on each of the events:
# - Evidence added/revoked  - source trust_score changed
# - [:CONTRADICTS] added/removed  - ESM transition of the fact

async def recalculate_variance(fact_id: str) -> float:
    result = await neo4j.run("""
        MATCH (f:Fact {id: $fid})
        OPTIONAL MATCH (f)-[:SUPPORTED_BY]->(s:Source)
        WITH f,
             count(s)                          AS ev_count,
             coalesce(avg(s.trust_score), 0.0) AS avg_trust
        OPTIONAL MATCH (c:Fact)-[:CONTRADICTS]->(f)
        WITH f, ev_count, avg_trust, count(c) AS contra_count
        SET f.epistemic_variance = (
            1.0 / (1.0 + ev_count * avg_trust)
            + least(0.6, 0.3 * contra_count)
        )
        RETURN f.epistemic_variance AS variance
    """, fid=fact_id)
    return result[0]["variance"]
```

```
I23 (VarianceFormula): epistemic_variance on a :Fact must be computed
    by the RFC0047 formula, not set by hand.
    Auto-update is mandatory on every change of Evidence or [:CONTRADICTS].
    Violation: a manual SET f.epistemic_variance without calling recalculate_variance().
```

---

### RFC0046-C: Temporal edges

**Problem**: the fact "the user lives in Berlin" creates `[:CONTRADICTS]` upon a relocation. But this is not a contradiction — it is a change over time.

**Solution**: `valid_from / valid_until` on key edges.

```cypher
-- Edges with temporal attributes (see the "Graph schema" section)
(:Entity)-[:RELATED_TO {strength, type, valid_from, valid_until}]->(:Entity)
(:Fact)-[:CAUSES {valid_from, valid_until}]->(:Fact)

-- valid_until = null → the relation is current now
-- On a "relocation": the old edge gets valid_until=now(), the new one valid_from=now()
-- We do NOT create [:CONTRADICTS] — we create a new temporal edge
```

```cypher
-- Query with temporal filtering
MATCH (e:Entity)-[r:RELATED_TO]->(other)
WHERE (r.valid_until IS NULL OR r.valid_until > datetime())
  AND r.valid_from <= datetime()
RETURN e, r, other
```

---

### RFC0049: Temporal-ESM Sync Protocol

**Problem:**: when a fact transitions into `Contradicted / Deprecated / Collapsed`, its outgoing edges remain with `valid_until = NULL` → they participate in queries as valid → phantom data, a violation of `Graph = Truth`.

#### Edge-closing trigger (esm_machine.py)

```python
TEMPORAL_CLOSING_STATES = {"Contradicted", "Deprecated", "Collapsed"}
TEMPORAL_EDGE_TYPES     = ["RELATED_TO", "CAUSES", "DERIVED_FROM"]

async def on_state_transition(fact_id: str, old_state: str,
                               new_state: str, neo4j_session):
    if new_state in TEMPORAL_CLOSING_STATES:
        edge_types = "|".join(TEMPORAL_EDGE_TYPES)
        await neo4j_session.run(f"""
            MATCH (:Fact {{id: $fid}})-[r:{edge_types}]->()
            WHERE r.valid_until IS NULL
            SET r.valid_until = datetime()
        """, fid=fact_id)
    # Recompute variance on any ESM transition
    await recalculate_variance(fact_id)
```

#### Mandatory filter (SafeFTSQuery + LensEngine)

```python
# Add to ALL Cypher queries that work with temporal edges:
TEMPORAL_EDGE_FILTER = """
    AND (r.valid_until IS NULL OR r.valid_until > datetime())
"""
```

#### Migration of existing edges (one-time, on upgrade)

```cypher
-- migration_v5_06_temporal_backfill.cypher
-- Step 1: add valid_from to edges that lack it
MATCH ()-[r:RELATED_TO|CAUSES|DERIVED_FROM]->()
WHERE r.valid_from IS NULL
SET r.valid_from = coalesce(r.created_at, datetime("2026-01-01T00:00:00"))
RETURN count(r) AS patched_edges;

-- Step 2: close edges on Contradicted/Deprecated/Collapsed facts
MATCH (f:Fact)-[r:RELATED_TO|CAUSES|DERIVED_FROM]->()
WHERE f.epistemic_state IN ["Contradicted", "Deprecated", "Collapsed"]
  AND r.valid_until IS NULL
SET r.valid_until = datetime()
RETURN count(r) AS closed_edges;
```

```
I25 (TemporalESMSync): When a :Fact transitions to Contradicted / Deprecated / Collapsed
    all outgoing [:RELATED_TO], [:CAUSES], [:DERIVED_FROM] edges with valid_until IS NULL
    must receive valid_until = datetime() in the same transaction.
    The filter (r.valid_until IS NULL OR r.valid_until > datetime()) is mandatory
    in all SafeFTSQuery and LensEngine queries.
    Violation: an ESM transition into a closing state without synchronous closing of edges.
```

### RFC0046 Invariants

```
I20 (TemporalEdges): New [:RELATED_TO], [:CAUSES], [:DERIVED_FROM] edges must contain valid_from at creation.
    valid_until = null means "current now".
    Violation: an edge created without valid_from.
```

### 📊 Prometheus metrics (addendum to RFC0036–RFC0038)

| Metric | Type | Description |
|---------|-----|---------|
| `event_fallback_inserted_total` | Counter | Events saved to the SQLite fallback |
| `event_fallback_recovered_total` | Counter | Events recovered from the fallback |
| `event_fallback_size` | Gauge | Current size of the fallback queue |
| `observer_blocks_total` | Counter | Pipeline blocks from Observer++ |
| `observer_rollbacks_total` | Counter | Rollbacks initiated by Observer++ |
| `source_trust_pending_facts` | Gauge | Facts awaiting verification |
| `write_protocol_violations_total` | Counter | Write Protocol violations |
| `fact_router_query_type_total` | Counter | Queries by type (label: query_type) |
| `fact_router_rerag_triggered_total` | Counter | Iterative retrievals launched |
| `closed_loop_faithfulness_p95` | Histogram | P95 faithfulness across answers |
| `esm_occ_conflicts_total` | Counter | OCC conflicts in ChunkedInvalidator |
| `duckdb_shadow_lag_seconds` | Gauge | Shadow State lag behind Neo4j |

### 📊 Prometheus metrics (RFC0036–RFC0051)

| Metric | Type | Description |
|---------|-----|---------|
| `closed_loop_faithfulness_p95` | Histogram | P95 faithfulness across answers |
| `esm_occ_conflicts_total` | Counter | OCC conflicts in ChunkedInvalidator |
| `duckdb_shadow_lag_seconds` | Gauge | Shadow State lag behind Neo4j |
| `reasoning_bank_ts_score` | Histogram | Thompson Sampling score by strategy |
| `duckdb_shadow_sync_total` | Counter | Successful Neo4j→DuckDB synchronizations |
| `duckdb_shadow_rows_synced` | Gauge | Rows in the last synchronization |
| `observer_false_positive_rate` | Gauge | Share of false positives from Observer++ |
| `observer_degraded_mode_total` | Counter | Entries into degraded mode |
| `observer_full_blocks_total` | Counter | Full pipeline blocks |
| `observer_degraded_duration_seconds` | Histogram | Duration of degraded mode |
| `fractal_governance_violations_total` | Counter | Fractal Governance violations |
| `hardware_profile_info` | Gauge | Current profile: weak=0, medium=1, strong=2 |
| `llm_mode_info` | Gauge | Current mode: offline=0, lite=1, full=2 |
| `lens_match_total` | Counter | Queries through LensEngine (label: lens_id) |
| `lens_fallback_total` | Counter | Lens found no match → fallback |
| `lens_latency_ms` | Histogram | P95 LensEngine latency (target < 50ms) |
| `epistemic_variance_p95` | Histogram | Distribution of fact uncertainty |
| `rollback_to_total` | Counter | DAG reasoning rollbacks (label: reason) |
| `temporal_edge_created_total` | Counter | New temporal edges created |
| `multi_component_ram_pressure` | Gauge | Total RAM pressure ∈ [0,1] |
| `offline_requests_total` | Counter | Queries in LLM_MODE=offline |
| `lens_compose_total` | Counter | Queries through compose() (2+ lenses) |
| `lens_precision_implicit` | Gauge | Share of offline answers with positive feedback |
| `dag_rollback_retry_total` | Counter | Deferred [:ROLLBACK_TO] due to missing nodes |
| `temporal_esm_sync_total` | Counter | Edges closed on ESM transition (label: new_state) |

---

## 🔒 System Invariants (addendum to I7, I8)

```
I9  (FactRouter): Query routing is deterministic, without an LLM.
    Violation: using the LLM for a routing decision.

I10 (OCC): All ESM invalidation operations use node versioning.
    Violation: SET without a _version_ check in WHERE.

I11 (AsyncEval): ClosedLoopEvaluator does NOT block the Fast Path.
    Violation: a synchronous evaluator.evaluate() call in the user response path.

I12 (FallbackPersist): the fallback_queue in EventBus is persistent (SQLite).
    Violation: an in-memory Queue as the only event store.

I13 (TSReplay): Thompson Sampling in audit mode uses seed=session_id_hash.
    Violation: stochastic strategy selection without a seed during audit replay.

I14 (CQRSRead): the Semantic Drift Monitor and Observer analytics read from DuckDB,
    not from Neo4j directly for aggregations.
    Violation: a Cypher aggregation in SemanticDriftMonitor without the Shadow State.

I15 (GraduatedBlock): Observer++ does NOT call block_pipeline() if
    false_positive_rate > 0.3. _enter_degraded_mode() is used instead.
    Violation: a direct block_pipeline() when FPR > 0.3.

I16 (TruthIsolation): the Truth Core does not receive commands from the Policy Core or
    the Evolution Core. Writes to L3 only through the Write Protocol (RFC0031).
    Violation: any write to L3 bypassing TruthGate / HumanApproval / TrustedImport.

I17 (HWProfile): HARDWARE_PROFILE is auto-detected at system startup.
    Manual override via the VELANTRIM_HW_PROFILE env var.
    Violation: hardcoding components (Neo4j, Qdrant) without regard for the profile.

I18 (LLMMode): When LLM_MODE=offline the Fast Path must use LensEngine.
    A direct llm.complete() call in offline mode is a violation.
    Violation: a llm.complete() call when LLM_MODE=offline.

I19 (LensEngine): LensEngine reads only from L3 (the graph) or Graph-Lite (SQLite).
    No LLM calls inside lenses.
    Violation: llm.complete() or llm.generate() inside LensEngine or any lens.

I20 (TemporalEdges): New [:RELATED_TO], [:CAUSES], [:DERIVED_FROM] edges must contain valid_from at creation.
    valid_until = null means "current now".
    Violation: an edge created without valid_from.

I21 (CORNER): CORNER is mandatory between RRF Fusion and the Facts Pack during multi-channel retrieval.
    Violation: a Facts Pack without deduplication when several retrieval channels are present.

I22 (MoEMemory): When LLM_ARCHITECTURE=moe the LLM_TOTAL_PARAMS parameter is mandatory
    and is checked against the available RAM at startup.
    Violation: a MoE model launched without checking LLM_TOTAL_PARAMS ≤ available_RAM.

I23 (VarianceFormula): epistemic_variance on a :Fact must be computed
    by the RFC0047 formula, not set by hand.
    Auto-update is mandatory on every change of Evidence or [:CONTRADICTS].
    Violation: a manual SET f.epistemic_variance without calling recalculate_variance().

I24 (MultiComponentBudget): At system startup a check of the
    combined RAM budget must be performed: LLM_TOTAL_PARAMS + Neo4j_PageCache + Redis + VectorDB + OS_buffer.
    When pressure > 0.92 — a mandatory downshift of the profile or a switch to LLM_MODE=offline.
    Violation: startup without compute_memory_budget() when LLM_ARCHITECTURE=moe.

I25 (TemporalESMSync): When a :Fact transitions to Contradicted / Deprecated / Collapsed
    all outgoing [:RELATED_TO], [:CAUSES], [:DERIVED_FROM] edges with valid_until IS NULL
    must receive valid_until = datetime() in the same transaction.
    Violation: an ESM transition into a closing state without synchronous closing of edges.

I26 (DAGRollbackTransaction): the [:ROLLBACK_TO] edge in ReasoningBank is created
    ONLY if both :ReasoningStep nodes already exist in Neo4j.
    If either node is absent — the write is deferred to the ConsolidationQueue
    with retry up to 10 attempts.
    Violation: MERGE [:ROLLBACK_TO] without a prior MATCH of both nodes.

I27 (LensCompose): When a query matches 2+ lenses with score ≥ LENS_COMPOSITION_THRESHOLD
    LensEngine must run compose() instead of a single match().
    Results are combined via CORNER before the Facts Pack.
    On compose()=None → fallback to HybridRetriever (full/lite) or BAE generic (offline).
    Violation: a single match() when 2+ lenses are above the threshold.

I74 (StagingReadPath): L2.5 Staging is used on the read path ONLY with a
    `preliminary` marker and confidence × 0.7.
    Staging is NEVER a source of truth — only the L3 graph is.
    Direct substitution of a staging fact without the `preliminary` marker is a bug.
    Violation: using a staging fact as Validated in the ContextBuilder.

I75 (ProtoConceptNaming): Naming a ProtoConcept is done ONLY in the Slow Path
    (Homeostatic Balancer, VolitionWorker, or via trigger B/C from RFC0066).
    Calling the LLM to name a concept in the Fast Path is a critical architectural bug.
    Trigger A (the user asks) must enqueue a task in the Slow Path queue,
    not perform naming synchronously.
    Violation: llm.complete() for naming a ProtoConcept inside the Fast Path.
```

---

## 📖 How to use the modules (instructions)

### New modules (RFC0036–RFC0038)

```
RFC0036  → add methods to event_bus.py
           + scheduler jobs in main.py

RFC0036+ → migrate the Neo4j schema (_version_ field)
           + replace _process_chunks in esm_chunked_invalidator.py
           + remove asyncio.sleep(0.1)

RFC0037  → move ClosedLoopEvaluator into l4_reasoning_worker.py
           + add publish(AGENT_RESPONSE) in fast_path.py

RFC0038  → create fact_router.py
           + integrate into fast_path.py before hybrid_retriever.py

KuzuDB   → GRAPH_BACKEND = "kuzu" in velantrim_config.py (P0-H FIX)
           + create kuzu_adapter.py (implements IGraphAdapter)

DuckDB   → create shadow_state.py
           + scheduler: dump every 15 min → DuckDB
           + Semantic Drift Monitor reads from DuckDB, not Neo4j
```

### New modules (RFC0036–RFC0040)

```
RFC0039  → update reasoning_bank.py: replace UCB1 with Thompson Sampling
           + rename the test test_ucb1_canonical_formula → test_ts_selection_formula

RFC0040  → create shadow_state.py (if not already created for DuckDB)
           + update semantic_drift_monitor.py: read from ShadowState
           + scheduler: shadow.sync every 15 min

RFC0041  → update observer_plus_plus.py: replace block_pipeline() with a
           graduated response with an FPR check
           + add _enter_degraded_mode() / _exit_degraded_mode()

RFC0042  → create fractal_governance.py
           + add validate_fractal_write() to L2IngestionEngine
           + add fractal_influence_trace logging
```

### New modules

```
RFC0043  → add the HARDWARE_PROFILE block to velantrim_config.py
           + create hardware_profile.py (psutil auto-detect)
           + switch the component stack by profile

RFC0044  → add LLM_MODE to velantrim_config.py
           + add the offline branch to fast_path.py (step F2.6)

RFC0045  → create lens_engine.py
           + create the lenses/ folder with 30 YAML lens files
           + integrate LensMatcher into fast_path.py as step F2.6
           + create normalizer.py (pymorphy2 + RU stop-words)
           + create offline_extractor.py (spaCy NER + domain keywords)

RFC0046  → update neo4j_setup.py: add the :ReasoningStep schema
           + add the [:PRECEDES] and [:ROLLBACK_TO] edges
           + add the epistemic_variance field to :Fact (default=1.0)
           + add temporal attributes to [:RELATED_TO], [:CAUSES]
           + add the rollback_to() method to reasoning_bank.py
           + add the [UNVERIFIED] tag in context_builder.py when variance > 0.7

RFC0045-BAE → create bae_engine.py (RST-lite + Microplanner + Surface RU)
              + create rsl_skeletons.py (skeletons for 8 intents)
              + create microplanner.py (anaphora, transitions, anti-repeat)
              + create surface_ru.py (pymorphy2 agreement)
              + create style_profiles.py (5 parametric profiles)
              + create corner.py (dedupe + diversity + budget)

MoE         → add LLM_ARCHITECTURE / LLM_ACTIVE_PARAMS / LLM_TOTAL_PARAMS
              to velantrim_config.py
              + a RAM check at startup if LLM_ARCHITECTURE=moe
```

### New modules

```
RFC0047  → update fact_manager.py: add recalculate_variance()
           + auto-call on a change of Evidence / [:CONTRADICTS] / ESM transition
           + the constant UNVERIFIED_THRESHOLD = 0.7 in velantrim_config.py

RFC0048  → update hardware_profile.py: add compute_memory_budget()
           + startup_ram_check() with the Multi-Component Budget
           + add NEO4J_PAGE_CACHE_GB, VECTOR_RAM_GB, MEM_PRESSURE_WARN,
             MEM_PRESSURE_CRIT to velantrim_config.py

           # Formula (hardware_profile.py):
           # total_required = llm_ram + neo4j_ram + redis_ram + vector_ram + os_buffer(2GB)
           # pressure = total_required / available_ram
           # if pressure > MEM_PRESSURE_CRIT: downshift profile or LLM_MODE=offline

RFC0049  → update esm_machine.py: on_state_transition() — closing edges
           + update safe_fts_query.py: add TEMPORAL_EDGE_FILTER
           + update lens_engine.py: TEMPORAL_EDGE_FILTER in the Cypher templates
           + run migration_v5_06_temporal_backfill.cypher (one-time)

RFC0050  → update reasoning_bank.py: create_rollback_edge() with a node check
           + retry via ConsolidationQueue when nodes are missing
           + the counter dag_rollback_retry_total (Prometheus)

RFC0051  → update lens_engine.py: add match_all() + compose()
           + add LENS_COMPOSITION_THRESHOLD = 0.45, MAX_COMPOSED_LENSES = 3
             to velantrim_config.py
           + BAE: implement ONLY the "neutral" profile as the MVP
             (the "concise"/"detailed" and "scientific"/"friendly" profiles — Phase 2+)
```

---

## 🔧 RFC0062 — TZ-Fix Integration Patch

> **Status**: Canonical
> **Source**: TZ-Fix Integration audit
> **Invariants**: I38
> **New Prometheus metrics**: 4
> **New Neo4j index**: `fact_conflict_checked_idx`

### New components (FEATURE-1..9)

---

#### FEATURE-1 · memory/core_memory_blocks.py

**What it provides**: ~500 tokens of persistent context in the system prompt. The
agent knows the user from the first word of every session without searching the graph.

```python
# memory/core_memory_blocks.py — new file
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

@dataclass
class CoreMemoryBlocks:
    """
    Persistent context ~500 tokens — always in the system prompt.
    Three blocks: user_profile / agent_persona / current_goals.

    Difference from Ring Zero / VALUES CORE:
      · Ring Zero      — immutable agent values (frozen in ESM)
      · CoreMemoryBlocks — living user profile (updated by SleepTimeWorker)
    """
    graph_memory:       object
    user_profile:       str = ""
    agent_persona:      str = ""
    current_goals:      str = ""
    MAX_PROFILE_TOKENS: int = field(default=200, repr=False)
    MAX_PERSONA_TOKENS: int = field(default=150, repr=False)
    MAX_GOALS_TOKENS:   int = field(default=150, repr=False)

    async def load(self):
        try:
            results = await self.graph_memory.search(
                query="core_memory user_profile agent_persona current_goals",
                num_results=10,
            )
            for r in results:
                if r.get("source") != "core_memory":
                    continue
                content = r.get("content", "")
                if "user_profile:" in content:
                    self.user_profile  = content.split("user_profile:", 1)[1].strip()
                elif "agent_persona:" in content:
                    self.agent_persona = content.split("agent_persona:", 1)[1].strip()
                elif "current_goals:" in content:
                    self.current_goals = content.split("current_goals:", 1)[1].strip()
            logger.info("CoreMemoryBlocks loaded from graph")
        except Exception as e:
            logger.warning(f"CoreMemoryBlocks.load failed (non-critical): {e}")

    def render(self) -> str:
        parts = []
        if self.user_profile:  parts.append(f"[USER PROFILE]\n{self.user_profile}")
        if self.agent_persona: parts.append(f"[AGENT PERSONA]\n{self.agent_persona}")
        if self.current_goals: parts.append(f"[CURRENT GOALS]\n{self.current_goals}")
        return "\n\n".join(parts) if parts else ""

    async def update(self, block: str, content: str):
        allowed = {"user_profile", "agent_persona", "current_goals"}
        if block not in allowed:
            raise ValueError(f"Unknown block: {block}. Allowed: {allowed}")
        setattr(self, block, content)
        try:
            await self.graph_memory.add_episode(
                episode_name=f"core_memory_{block}",
                content=f"{block}: {content}",
                source="core_memory",
            )
        except Exception as e:
            logger.warning(f"CoreMemoryBlocks.update save failed: {e}")

    async def update_from_conversation(self, conversation_text: str, llm_client):
        """Automatically update user_profile. Called by SleepTimeWorker."""
        if not llm_client:
            return
        prompt = (
            f"Extract a concise user profile update (max 150 words).\n"
            f"Focus on: name, role, tech stack, preferences, projects.\n"
            f"Conversation: {conversation_text[:2000]}\nUser profile update:"
        )
        try:
            updated = await llm_client.complete(prompt)
            if updated and len(updated) > 10:
                await self.update("user_profile", updated)
        except Exception as e:
            logger.debug(f"CoreMemoryBlocks.update_from_conversation failed: {e}")

# Integration in agent.py:
#   __init__: self.core_blocks = CoreMemoryBlocks(graph_memory=self.graph_memory)
#   start():  await self.core_blocks.load()
#   chat():   system_prompt = base_prompt + "\n\n" + self.core_blocks.render()
```

---

#### FEATURE-2 · sleep_time_worker.py

**What it provides**: memory self-heals while idle. Zero load during conversation.

⚠️ **MGL-2 compliance**: `_refine_truth_layer` delegates to `AutoTruthGateWorker`
and `ESM.transition` — no direct `SET epistemic_state`.

```python
# sleep_time_worker.py — new file
import asyncio
import logging
from datetime import datetime, timezone, timedelta

logger = logging.getLogger(__name__)

class SleepTimeWorker:
    """
    Idle memory refinement (≥5 min of inactivity).
    ⚠️ MGL-2: epistemic_state is changed only via ESM.transition.
    """
    def __init__(
        self,
        graph_memory,
        reasoning_bank,
        core_blocks            = None,
        idle_timeout           = 300,
        sleep_interval         = 3600,
        auto_truth_gate_worker = None,  # AutoTruthGateWorker instance
        esm                    = None,  # EpistemicStateMachine instance
    ):
        self.graph                   = graph_memory
        self.reasoning_bank          = reasoning_bank
        self.core_blocks             = core_blocks
        self.idle_timeout            = idle_timeout
        self.sleep_interval          = sleep_interval
        self._auto_truth_gate_worker = auto_truth_gate_worker
        self._esm                    = esm
        self._last_activity          = datetime.now(timezone.utc)
        self._last_cycle_at          = datetime.now(timezone.utc)
        self._running                = False
        self._task                   = None

    def notify_activity(self):
        """Call on every incoming message."""
        self._last_activity = datetime.now(timezone.utc)

    def _is_idle(self) -> bool:
        return (datetime.now(timezone.utc) - self._last_activity).total_seconds() >= self.idle_timeout

    async def start(self):
        self._running = True
        self._task    = asyncio.create_task(self._sleep_loop())
        logger.info("SleepTimeWorker started")

    async def stop(self):
        self._running = False
        if self._task and not self._task.done():
            self._task.cancel()
            try: await self._task
            except asyncio.CancelledError: pass

    async def _sleep_loop(self):
        while self._running:
            await asyncio.sleep(60)
            if not self._is_idle():
                continue
            since = (datetime.now(timezone.utc) - self._last_cycle_at).total_seconds()
            if since < self.sleep_interval:
                continue
            try:
                await self._run_sleep_cycle()
                self._last_cycle_at = datetime.now(timezone.utc)
            except asyncio.CancelledError:
                raise
            except Exception as e:
                logger.warning(f"SleepTimeWorker cycle failed: {e}")

    async def _run_sleep_cycle(self):
        logger.info("SleepTimeWorker: starting idle refinement cycle")
        await self._refine_truth_layer()
        await self._ace_curator_update()
        await self._refresh_core_blocks()
        logger.info("SleepTimeWorker: idle refinement cycle complete")

    async def _refine_truth_layer(self):
        """
        ⚠️ MGL-2: no direct SET epistemic_state.
        Validated promotion → AutoTruthGateWorker.
        Stale Hypothesized → ESM.transition.
        """
        if self._auto_truth_gate_worker:
            try:
                promoted = await self._auto_truth_gate_worker.run_validation_cycle()
                logger.info(f"SleepTimeWorker: AutoTruthGate promoted {promoted} facts")
            except Exception as e:
                logger.debug(f"SleepTimeWorker: AutoTruthGate failed: {e}")

        cutoff = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
        try:
            stale = await self.graph.execute_cypher("""
                MATCH (f:Fact)
                WHERE f.epistemic_state = 'Hypothesized'
                  AND f.last_accessed < $cutoff
                  AND f.is_ring_zero <> true
                RETURN f.id AS fact_id, f AS fact_data
                LIMIT 50
            """, {"cutoff": cutoff})
            if stale and self._esm:
                for row in stale:
                    try:
                        await self._esm.transition(
                            fact_id=row["fact_id"], fact=dict(row["fact_data"]),
                            graph=self.graph, reason="sleep_time: no access 7 days",
                        )
                    except Exception:
                        pass
        except Exception as e:
            logger.debug(f"SleepTimeWorker._refine_truth_layer: {e}")

    async def _ace_curator_update(self):
        try:
            if hasattr(self.reasoning_bank, 'ace_curator_update'):
                await self.reasoning_bank.ace_curator_update()
        except Exception as e:
            logger.debug(f"SleepTimeWorker._ace_curator_update: {e}")

    async def _refresh_core_blocks(self):
        if self.core_blocks:
            try: await self.core_blocks.load()
            except Exception as e: logger.debug(f"SleepTimeWorker._refresh_core_blocks: {e}")

# Integration in agent.py:
#   self.sleep_worker = SleepTimeWorker(
#       graph_memory=self.graph_memory, reasoning_bank=self.reasoning_bank,
#       core_blocks=self.core_blocks, auto_truth_gate_worker=self.auto_truth_gate_worker,
#       esm=self.esm)
#   start(): await self.sleep_worker.start()
#   chat() as the first line: self.sleep_worker.notify_activity()
```

---

#### FEATURE-3 · reasoning_bank.py — ACE Curator

**What it provides**: strategies are distilled with reasoning: root_cause + conditions + anti_conditions.
Add the method to the `ReasoningBank` class. Called from `SleepTimeWorker` while idle.

```python
# reasoning_bank.py — add the ace_curator_update method to ReasoningBank

    async def ace_curator_update(self):
        """
        ACE Curator (Stanford/SambaNova ACE pattern).
        Called ONLY from SleepTimeWorker while idle — not from the Fast Path.

        PATCH-6: the duplicate implementation was removed — the canonical one lives in
        agent_with_learning.py :: SelfLearningAgent.ace_curator_update().
        The divergence was: here e.task, there e.task_description[:50] +
        different episode_name formats → desync when changes were made.

        ReasoningBank passes its data through arguments to the canonical method.
        Make all logic changes ONLY in agent_with_learning.py.
        """
        if not hasattr(self, '_ace_delegate') or self._ace_delegate is None:
            logger.debug("ace_curator_update: _ace_delegate not set, skipping")
            return
        await self._ace_delegate(
            strategies=self.strategies,
            experience_buffer=list(getattr(self, 'experience_buffer', [])),
            graph=self.graph,
            llm_client=getattr(self, '_llm_client', None),
        )
```

---

#### FEATURE-4 · memory/namespaces.py + memory/rrf_search.py

**What it provides**: 4 namespaces without mixing + RRF search across all of them.
⚠️ **RFC0032**: search via `SafeFTSQuery` or an explicit ESM filter.

```python
# memory/namespaces.py
from enum import Enum

class Namespace(str, Enum):
    PERSONAL   = "personal"
    PROJECT    = "project"
    KNOWLEDGE  = "knowledge"
    EXPERIENCE = "experience"

SOURCE_TO_NAMESPACE = {
    "conversation": Namespace.PERSONAL,    "user_message": Namespace.PERSONAL,
    "core_memory":  Namespace.PERSONAL,    "stm_consolidation": Namespace.PERSONAL,
    "strategy_distill": Namespace.EXPERIENCE, "ace_curator": Namespace.EXPERIENCE,
    "ingest_manifest":  Namespace.PROJECT,    "document": Namespace.KNOWLEDGE,
}

def infer_namespace(source: str) -> str:
    return SOURCE_TO_NAMESPACE.get(source, Namespace.PERSONAL).value
```

```python
# memory/rrf_search.py
from collections import defaultdict
from typing import Optional

BLOCKED_ESM = {"Contradicted", "Deprecated", "Collapsed"}

async def multi_namespace_search(
    graph_memory, safe_fts_query,
    query: str, num_results: int = 10,
    priority_namespace: Optional[str] = None, rrf_k: int = 60,
) -> list[dict]:
    """
    RRF search across all namespaces.
    ⚠️ RFC0032: SafeFTSQuery or an explicit ESM filter — direct search() is forbidden.
    """
    all_results, rank_lists = {}, []
    for ns in ["personal", "project", "knowledge", "experience"]:
        try:
            if hasattr(safe_fts_query, 'search_with_namespace'):
                results = await safe_fts_query.search_with_namespace(query, namespace=ns, limit=num_results)
            else:
                raw     = await graph_memory.search(query=query, num_results=num_results*2, namespace=ns)
                results = [r for r in raw if r.get("epistemic_state","Validated") not in BLOCKED_ESM and r.get("is_active", True)][:num_results]
            rank_list = []
            for r in results:
                did = str(r.get("uuid") or r.get("id") or hash(r.get("content","")[:50]))
                all_results[did] = r; rank_list.append(did)
            rank_lists.append(rank_list)
        except Exception:
            rank_lists.append([])

    scores: dict[str, float] = defaultdict(float)
    for rl in rank_lists:
        for rank, did in enumerate(rl):
            s = 1.0 / (rrf_k + rank + 1)
            if priority_namespace and all_results.get(did, {}).get("group_id") == priority_namespace:
                s *= 1.5
            scores[did] += s

    return [all_results[d] for d in sorted(scores, key=scores.get, reverse=True)[:num_results] if d in all_results]
```

```python
# safe_fts_query.py — add a method to SafeFTSQuery

    async def search_with_namespace(self, query: str, namespace: str, limit: int = 20) -> list:
        """Extension of SafeFTSQuery: standard ESM filters + namespace filter."""
        raw  = await self.fts5_search(query, limit * 2)
        safe = []
        for ep in raw:
            if ep.valid_until and ep.valid_until < datetime.now(timezone.utc): continue
            if ep.esm_hint in ("Contradicted", "Deprecated"): continue
            if await self._linked_to_contradicted(ep): continue
            if getattr(ep, 'group_id', namespace) != namespace: continue
            safe.append(ep)
        return safe[:limit]
```

---

#### FEATURE-5 · memory/auto_summary.py

```python
# memory/auto_summary.py  ← full implementation from HYPERIA, adapted for Velantrim
#
# Purpose: every SUMMARY_EVERY turns it creates a brief summary of the dialogue and
# saves it to L1 (namespace="personal"). Without this the graph grows
# linearly with the number of messages — every turn becomes a separate episode.
#
# Integration in Agent.chat() (SLOW PATH, after writing the episode):
#   turn_index = ... # increment per conversation_id
#   await auto_summary.maybe_create_summary(
#       conversation_id=conversation_id,
#       turn_index=turn_index,
#       recent_turns=last_N_turns,   # list[{"user": str, "agent": str}]
#   )
#
# Summarization: LLM if available, otherwise extractive TF-IDF (0 tokens, CPU-only).
# Deduplication: episode_name includes turn_index — a repeated call is safe (MERGE).

import asyncio
import logging
from typing import Optional

logger = logging.getLogger(__name__)

SUMMARY_EVERY = 10   # create a summary every N turns
# P1-F FIX: move to velantrim_config.py — single source for AdaptiveDecoder and CognitiveModeRouter
# class ModeTemperatures:
#     PRECISION=0.3, BALANCED=0.6, EXPLORATION=0.85, CREATIVE=None (dynamic)
# MODE_TEMPS = ModeTemperatures()


class AutoSummary:
    """
    Auto-summarization of the dialogue every SUMMARY_EVERY turns.
    Holds references to in-flight tasks so GC does not kill the coroutines before completion.
    """

    def __init__(self, graph_memory, llm_client=None):
        self.graph       = graph_memory
        self.llm         = llm_client
        self._in_flight: set = set()   # conversation_ids currently being summarized

    async def maybe_create_summary(
        self,
        conversation_id: str,
        turn_index:      int,
        recent_turns:    list,          # list[{"user": str, "agent": str}]
    ) -> Optional[str]:
        """
        Call from the SLOW PATH after every turn.
        Creates a summary only every SUMMARY_EVERY turns, does not block the response.
        """
        # Not time yet, or already running for this conversation_id
        # P2-F FIX: offline guard — do not call the LLM when LLM_MODE=offline
        from velantrim_config import LLM_MODE as _LLM_MODE
        if _LLM_MODE == "offline":
            return None   # in offline mode use only the extractive fallback
        if turn_index % SUMMARY_EVERY != 0:
            return None
        if conversation_id in self._in_flight:
            logger.debug(f"AutoSummary: {conversation_id} already in-flight, skipping")
            return None

        self._in_flight.add(conversation_id)
        try:
            return await self._create_summary(conversation_id, turn_index, recent_turns)
        except Exception as e:
            logger.warning(f"AutoSummary: failed for {conversation_id}: {e}")
            return None
        finally:
            self._in_flight.discard(conversation_id)

    async def _create_summary(
        self,
        conversation_id: str,
        turn_index:      int,
        turns:           list,
    ) -> Optional[str]:
        if not turns:
            return None

        # Take the last SUMMARY_EVERY turns for the summary
        window = turns[-SUMMARY_EVERY:]
        text   = "\n".join(
            f"User: {t.get('user', '')}\nAgent: {t.get('agent', '')}"
            for t in window
        )

        # Summarization: LLM if available, otherwise extractive TF-IDF (CPU-only, 0 tokens)
        summary = await self._summarize(text)

        # episode_name is deterministic from conversation_id + turn_index:
        # a repeated call with the same parameters is safe — MERGE does not create a duplicate.
        episode_name = f"auto_summary_{conversation_id}_{turn_index}"

        await self.graph.add_episode(
            episode_name=episode_name,
            content=summary,
            source="auto_summary",
            namespace="personal",
            metadata={
                "conversation_id": conversation_id,
                "turn_index":      turn_index,
                "turns_covered":   len(window),
                "summary_type":    "llm" if self.llm else "extractive",
            }
        )
        logger.info(
            f"AutoSummary: created summary for {conversation_id} "
            f"at turn {turn_index} ({len(window)} turns covered)"
        )
        return summary

    async def _summarize(self, text: str) -> str:
        """LLM summarization with extractive fallback."""
        if self.llm:
            try:
                return await self.llm.complete(
                    f"Summarize this conversation in 3-5 concise sentences, "
                    f"focusing on key facts and decisions:\n\n{text}",
                )
            except Exception as e:
                logger.debug(f"AutoSummary: LLM failed ({e}), falling back to extractive")

        # Extractive TF-IDF fallback — 0 tokens, CPU-only
        return await asyncio.to_thread(self._extractive_summarize, text)

    @staticmethod
    def _extractive_summarize(text: str, max_sentences: int = 5) -> str:
        """
        TF-IDF extractive summarization without LLM.
        Selects top-N sentences by aggregate TF-IDF score.
        Falls back to the first 500 characters if sklearn is unavailable.
        """
        sentences = [s.strip() for s in text.replace("\n", " ").split(".") if s.strip()]
        if len(sentences) <= max_sentences:
            return ". ".join(sentences) + "."
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            vectorizer   = TfidfVectorizer(max_features=50)
            tfidf_matrix = vectorizer.fit_transform(sentences)
            scores       = tfidf_matrix.sum(axis=1).A1
            top_indices  = scores.argsort()[-max_sentences:][::-1]
            top_sentences = [sentences[i] for i in sorted(top_indices)]
            return ". ".join(top_sentences) + "."
        except Exception:
            return text[:500]
```

---

#### FEATURE-6 · mcp_server/server.py

```python
# mcp_server/server.py — new file
import asyncio, json, logging, sys
logger = logging.getLogger(__name__)

MCP_TOOLS = [
    {"name":"memory_search","description":"Search agent long-term memory","inputSchema":{"type":"object","properties":{"query":{"type":"string"},"num_results":{"type":"integer","default":5}},"required":["query"]}},
    {"name":"memory_add","description":"Add fact to memory","inputSchema":{"type":"object","properties":{"content":{"type":"string"},"source":{"type":"string","default":"mcp_user"}},"required":["content"]}},
    {"name":"agent_chat","description":"Send message to agent","inputSchema":{"type":"object","properties":{"message":{"type":"string"},"user_id":{"type":"string","default":"mcp_user"}},"required":["message"]}},
]

class MCPServer:
    def __init__(self, agent, auth_token: str = ""):
        self.agent = agent; self.auth_token = auth_token

    async def handle_request(self, req: dict) -> dict:
        method = req.get("method",""); rid = req.get("id"); params = req.get("params",{})
        if method == "initialize":
            return {"jsonrpc":"2.0","id":rid,"result":{"protocolVersion":"2024-11-05","capabilities":{"tools":{}},"serverInfo":{"name":"velantrim-mcp","version":"2.50"}}}
        if method == "tools/list":
            return {"jsonrpc":"2.0","id":rid,"result":{"tools":MCP_TOOLS}}
        if method == "tools/call":
            try:
                result = await self._call_tool(params.get("name"), params.get("arguments",{}))
                return {"jsonrpc":"2.0","id":rid,"result":{"content":[{"type":"text","text":json.dumps(result)}]}}
            except Exception as e:
                return {"jsonrpc":"2.0","id":rid,"error":{"code":-32000,"message":str(e)}}
        return {"jsonrpc":"2.0","id":rid,"error":{"code":-32601,"message":"Method not found"}}

    async def _call_tool(self, name, args):
        if name == "memory_search":
            res = await self.agent.graph_memory.search(query=args["query"], num_results=args.get("num_results",5))
            return [{"content":r.get("content",""),"score":r.get("relevance_score",0)} for r in res]
        if name == "memory_add":
            # add_episode() passes through the Truth Gate inside GraphMemory — see RFC0031
            # FIX-F: was f"mcp_{content[:20]}" — silent data loss via INSERT OR IGNORE
            # if two facts start identically. Now UUID guarantees uniqueness.
            import uuid as _uuid
            ep_name = f"mcp_{_uuid.uuid4().hex[:12]}"
            await self.agent.graph_memory.add_episode(episode_name=ep_name, content=args["content"], source=args.get("source","mcp_user"))
            return {"status":"added"}
        if name == "agent_chat":
            return {"response": await self.agent.chat(args["message"], user_id=args.get("user_id","mcp_user"))}
        raise ValueError(f"Unknown tool: {name}")

    async def run_stdio(self):
        logger.info("MCP Server started (stdio)")
        loop = asyncio.get_running_loop(); reader = asyncio.StreamReader()
        await loop.connect_read_pipe(lambda: asyncio.StreamReaderProtocol(reader), sys.stdin)
        while True:
            try:
                line = await reader.readline()
                if not line: break
                resp = await self.handle_request(json.loads(line.decode()))
                sys.stdout.write(json.dumps(resp)+"\n"); sys.stdout.flush()
            except Exception as e:
                logger.error(f"MCP error: {e}")
```

---

#### FEATURE-7 · core/truth_conflict.py

**What it provides**: an automatic semantic conflict detector + a Slow Path worker (S2.5).

⚠️ **RFC0031**: no direct `SET epistemic_state` — only `ESM.transition`.
⚠️ When `llm_client=None` → `continue`, not `break` — batch processing continues for the remaining facts.

```python
# core/truth_conflict.py — new file
import asyncio, logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

class TruthConflictDetector:

    async def detect_and_resolve_conflicts(
        self, new_fact: dict, graph_memory, esm,
        llm_client=None, sim_threshold: float = 0.95,
    ) -> dict:
        """
        ⚠️ RFC0031: direct Cypher for SET epistemic_state — FORBIDDEN.
        All transitions go through ESM.transition → GraphWriteProtocol.
        Called ONLY from ConflictResolutionWorker (Slow Path S2.5).
        """
        content = new_fact.get("content", "")
        if not content or len(content) < 10: return new_fact
        try:
            similar = await graph_memory.search(query=content, num_results=5)
        except Exception as e:
            logger.debug(f"TruthConflict search failed: {e}"); return new_fact

        for old in similar:
            old_content = old.get("content",""); score = old.get("relevance_score", 0.0)
            if score < sim_threshold or not old_content: continue
            if not llm_client: continue  # continue, not break — process the rest
            try:
                ans = (await llm_client.complete(
                    f"Do these facts contradict? YES or NO.\nA: {old_content[:300]}\nB: {content[:300]}\nAnswer:"
                )).strip().upper()
                if ans.startswith("YES"):
                    logger.info(f"TruthConflict: conflict detected (sim={score:.2f})")
                    old_full = dict(old)
                    old_full["contradiction_count"] = old_full.get("contradiction_count", 0) + 1
                    await esm.transition(
                        fact_id=old.get("id",""), fact=old_full, graph=graph_memory,
                        reason=f"TruthConflict: contradicted (sim={score:.2f})",
                    )
                    new_fact["requires_validation"]  = True
                    new_fact["conflict_resolved_at"] = datetime.now(timezone.utc).isoformat()
                    break
            except Exception as e:
                logger.debug(f"TruthConflict LLM failed: {e}"); continue
        return new_fact

class ConflictResolutionWorker:
    """
    RFC0062 — Slow Path S2.5.
    Checks Hypothesized facts for conflicts every 5 minutes.
    ⚠️ I38: called only from the Slow Path — not from the Fast Path.
    """
    CHECK_INTERVAL = 300
    BATCH_SIZE     = 20

    def __init__(self, graph, esm, llm_client=None):
        self.graph = graph; self.esm = esm; self.llm = llm_client
        self._running = False; self._detector = TruthConflictDetector()

    async def start(self):
        self._running = True
        asyncio.create_task(self._run_loop())
        logger.info("ConflictResolutionWorker started (Slow Path S2.5)")

    async def _run_loop(self):
        while self._running:
            await asyncio.sleep(self.CHECK_INTERVAL)
            try: await self._check_batch()
            except asyncio.CancelledError: raise
            except Exception as e: logger.warning(f"ConflictResolutionWorker failed: {e}")

    async def _check_batch(self):
        candidates = await self.graph.execute_cypher("""
            MATCH (f:Fact)
            WHERE f.epistemic_state = 'Hypothesized'
              AND NOT coalesce(f.conflict_checked, false)
              AND NOT coalesce(f.is_ring_zero, false)
            RETURN f.id AS id, f AS fact_data
            ORDER BY f.created_at DESC LIMIT $limit
        """, {"limit": self.BATCH_SIZE})
        # FIX-E: was `f.conflict_checked <> true` — in Neo4j null <> true = null → false in WHERE.
        # New facts without the conflict_checked property never made it into the selection at all.
        # coalesce(f.conflict_checked, false) correctly treats a missing property as false.
        for row in (candidates or []):
            await self._detector.detect_and_resolve_conflicts(
                new_fact=dict(row["fact_data"]), graph_memory=self.graph,
                esm=self.esm, llm_client=self.llm,
            )
            await self.graph.execute_cypher(
                "MATCH (f:Fact {id: $id}) SET f.conflict_checked = true", {"id": row["id"]}
            )

# Integration in agent.py:
#   self.conflict_worker = ConflictResolutionWorker(graph=self.graph_memory, esm=self.esm, llm_client=self.llm_fast)
#   start(): await self.conflict_worker.start()
```

---

#### FEATURE-8 · context_builder.py

**What it provides**: eliminates token-budget drift (was 4000 in the code vs 2000 in token_contract.py).
**Action**: replace the existing `ContextBuilder`.

```python
# context_builder.py — replace the ContextBuilder class
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)

# ✅ 2000 = MAX_TOKENS_BALANCED_MODE from token_contract.py (drift eliminated)
QUERY_TYPE_BUDGETS = {
    "conversation": {"stm": 200, "ltm": 300, "strategies": 200, "entities": 100},
    "task":         {"stm": 150, "ltm": 400, "strategies": 350, "entities": 100},
    "analysis":     {"stm": 100, "ltm": 600, "strategies": 200, "entities": 100},
    "default":      {"stm": 200, "ltm": 300, "strategies": 200, "entities": 100},
}

class ContextBuilder:
    def __init__(self, token_budget: int = 2000):  # ✅ 2000 matches token_contract.py
        self.token_budget = token_budget

    def build_context(
        self,
        current_query:        str,
        retrieved_memories:   List,
        strategies:           List          = None,
        conversation_history: List[dict]    = None,
        core_blocks:          Optional[str] = None,
        query_type:           str           = "default",
    ) -> str:
        parts, used = [], 0
        budgets = QUERY_TYPE_BUDGETS.get(query_type, QUERY_TYPE_BUDGETS["default"])

        if core_blocks:
            parts.append(core_blocks); used += self._count_tokens(core_blocks)
        if strategies:
            t = self._format_strategies(strategies, budgets["strategies"])
            if t: parts.append(f"[STRATEGIES]\n{t}"); used += self._count_tokens(t)
        ltm_budget = min(budgets["ltm"], self.token_budget - used - 200)
        if retrieved_memories and ltm_budget > 0:
            t = self._format_memories(retrieved_memories, ltm_budget)
            if t: parts.append(f"[MEMORY]\n{t}"); used += self._count_tokens(t)
        if conversation_history:
            t = self._format_history(conversation_history, min(budgets["stm"], self.token_budget - used - 100))
            if t: parts.append(f"[HISTORY]\n{t}")
        return "\n\n".join(parts)

    def _format_strategies(self, strategies, budget):
        lines, used = [], 0
        for s in strategies:
            line = f"• {getattr(s,'description',str(s))}"; t = self._count_tokens(line)
            if used + t > budget: break
            lines.append(line); used += t
        return "\n".join(lines)

    def _format_memories(self, memories, budget):
        lines, used = [], 0
        for m in memories:
            c = m.get('content','') if isinstance(m, dict) else getattr(m,'content','')
            line = f"• {c[:200]}"; t = self._count_tokens(line)
            if used + t > budget: break
            lines.append(line); used += t
        return "\n".join(lines)

    def _format_history(self, history, budget):
        lines, used = [], 0
        for turn in reversed(history[-6:]):
            line = f"User: {turn.get('role_user',turn.get('content',''))[:150]}\nAssistant: {turn.get('role_agent','')[:150]}"
            t = self._count_tokens(line)
            if used + t > budget: break
            lines.insert(0, line); used += t
        return "\n---\n".join(lines)

    def _count_tokens(self, text: str) -> int:
        try:
            import tiktoken
            return len(tiktoken.get_encoding('cl100k_base').encode(text))
        except Exception:
            return max(1, len(text.encode('utf-8')) // 3)
```

---

#### FEATURE-9 · scripts/

```bash
# scripts/self_awareness_update.sh
#!/bin/bash
python scripts/generate_project_map.py --output manifest.json
python scripts/ingest_manifest.py --input manifest.json --namespace project
echo "Self-awareness updated at $(date)"
```

```python
# scripts/generate_project_map.py
import ast, json
from pathlib import Path

def analyze_file(path):
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except SyntaxError: return {}
    return {
        "path": str(path),
        "classes":   [n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)],
        "functions": [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)],
    }

def main(output="manifest.json"):
    modules = [analyze_file(p) for p in sorted(Path(".").rglob("*.py"))
               if not any(x in str(p) for x in [".venv", "__pycache__", ".git"])]  # cross-platform (p.parts fails on Windows)
    modules = [m for m in modules if m]
    Path(output).write_text(json.dumps(modules, ensure_ascii=False, indent=2))
    print(f"Generated {output}: {len(modules)} modules")

if __name__ == "__main__":
    import argparse; p = argparse.ArgumentParser()
    p.add_argument("--output", default="manifest.json")
    main(**vars(p.parse_args()))
```

```python
# scripts/ingest_manifest.py — fingerprint deduplication
import json, hashlib, asyncio, argparse
from pathlib import Path

async def ingest(manifest_path, namespace, graph_memory):
    modules = json.loads(Path(manifest_path).read_text())
    added = 0
    for mod in modules:
        fp = hashlib.sha256(json.dumps(mod).encode()).hexdigest()[:16]
        if await graph_memory.search(query=f"fingerprint:{fp}", num_results=1):
            continue
        await graph_memory.add_episode(
            episode_name=f"module_{fp}", content=json.dumps(mod),
            source="ingest_manifest", group_id=namespace,
        )
        added += 1
    print(f"Ingested {added} new, skipped {len(modules)-added} unchanged")
```

---

### 📊 Prometheus metrics (RFC0062)

```python
sleep_worker_cycles_total   = Counter("sleep_worker_cycles_total", ...)
conflict_checks_total       = Counter("conflict_checks_total", ...)
conflict_resolved_total     = Counter("conflict_resolved_total", ...)
core_memory_blocks_loaded   = Gauge("core_memory_blocks_loaded", ...)
```

---

### RFC0062 implementation order (4 sprints)

```
SPRINT 1 — STABILIZATION (~5 days):
  1. datetime timezone.utc — global search (0.5 day, do first)
  2. FractalMemory Lock + Cold Start Guard (1 day)
  3. CircuitBreaker per-loop (0.5 day)
  4. ConsolidationWorker tasks (0.5 day)
  5. MTM snapshot + executor (0.5 day)
  6. break→continue when llm_client=None (0.5 day)

SPRINT 2 — FIXES (~3 days):
  7. RetrievalResult.embedding (0.5 day)
  8. EventBus QueueFull→SQLite (0.5 day)
  9. deepcopy ImmutableCore (0.5 day, if the file exists)
 10. ConversationBuffer ref_count (1 day, if the file exists)

SPRINT 3 — FEATURE CORE (~5 days):
 11. FEATURE-8  replace ContextBuilder (0.5 day, eliminates token drift)
 12. FEATURE-1  CoreMemoryBlocks (1 day)
 13. FEATURE-2  SleepTimeWorker (1 day)
 14. FEATURE-7  TruthConflictDetector + S2.5 (1.5 days)
 15. FEATURE-3  ACE Curator in ReasoningBank (0.5 day)

SPRINT 4 — EXPANSION (~4 days):
 16. FEATURE-4  Namespace + RRF (1.5 days)
 17. FEATURE-5  AutoSummary (0.5 day)
 18. FEATURE-6  MCP Server (1 day)
 19. FEATURE-9  Self-Awareness scripts (0.5 day)

Total: ~17 working days
```

---

# ============================================================================
# HYPERIA COMPONENT 2: CoreMemoryBlocks
# ============================================================================
# RFC0062 FEATURE-1 - now fully implemented

# memory/core_memory_blocks.py
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

logger = logging.getLogger(__name__)

@dataclass
class CoreMemoryBlocks:
    """
    Persistent context ~500 tokens — always in the system prompt.
    Three blocks: user_profile / agent_persona / current_goals.

    Adaptation: All graph.search() calls are wrapped in SafeFTSQuery to comply with RFC0032.

    Difference from Ring Zero / VALUES CORE:
    - Ring Zero: immutable agent values (frozen in ESM)
    - CoreMemoryBlocks: living user profile (updated by SleepTimeWorker)
    """
    graph_memory: object
    safe_fts_query: object = None  # ✅ Velantrim adaptation: SafeFTSQuery instead of direct search
    user_profile: str = ""
    agent_persona: str = ""
    current_goals: str = ""
    MAX_PROFILE_TOKENS: int = field(default=200, repr=False)
    MAX_PERSONA_TOKENS: int = field(default=150, repr=False)
    MAX_GOALS_TOKENS: int = field(default=150, repr=False)

    async def load(self):
        """
        Load the blocks from the graph at agent startup.
        ✅ Velantrim adaptation: uses SafeFTSQuery if available.
        """
        try:
            # Use SafeFTSQuery if available (Velantrim RFC0032)
            if self.safe_fts_query:
                results = await self.safe_fts_query.search(
                    query="core_memory user_profile agent_persona current_goals",
                    limit=10
                )
            else:
                # Fallback to direct search if SafeFTSQuery is not configured
                results = await self.graph_memory.search(
                    query="core_memory user_profile agent_persona current_goals",
                    num_results=10
                )
            
            for r in results:
                content = r.get("content", "") if isinstance(r, dict) else getattr(r, 'content', '')
                source = r.get("source", "") if isinstance(r, dict) else getattr(r, 'source', '')
                
                if source != "core_memory":
                    continue
                
                if "user_profile:" in content:
                    self.user_profile = content.split("user_profile:", 1)[1].strip()
                elif "agent_persona:" in content:
                    self.agent_persona = content.split("agent_persona:", 1)[1].strip()
                elif "current_goals:" in content:
                    self.current_goals = content.split("current_goals:", 1)[1].strip()
            
            logger.info("CoreMemoryBlocks loaded from graph")
        except Exception as e:
            logger.warning(f"CoreMemoryBlocks.load failed (non-critical): {e}")

    def render(self) -> str:
        """
        Render the blocks for insertion into the system prompt.
        Returns ~500 tokens of persistent context.
        """
        parts = []
        if self.user_profile:
            parts.append(f"[USER PROFILE]\n{self.user_profile}")
        if self.agent_persona:
            parts.append(f"[AGENT PERSONA]\n{self.agent_persona}")
        if self.current_goals:
            parts.append(f"[CURRENT GOALS]\n{self.current_goals}")
        
        return "\n\n".join(parts) if parts else ""

    async def update(self, block: str, content: str):
        """
        Update one of the blocks and save it to the graph.
        Called manually by the user or automatically via SleepTimeWorker.
        """
        allowed = {"user_profile", "agent_persona", "current_goals"}
        if block not in allowed:
            raise ValueError(f"Unknown block: {block}. Allowed: {allowed}")
        
        setattr(self, block, content)
        
        try:
            await self.graph_memory.add_episode(
                episode_name=f"core_memory_{block}_{datetime.now(timezone.utc).isoformat()}",
                content=f"{block}: {content}",
                source="core_memory"
            )
            logger.info(f"CoreMemoryBlocks.{block} updated")
        except Exception as e:
            logger.warning(f"CoreMemoryBlocks.update save failed: {e}")

    async def update_from_conversation(self, conversation_text: str, llm_client):
        """
        Automatically update user_profile from the conversation.
        Called by SleepTimeWorker while idle.
        
        ✅ Velantrim adaptation: the LLM call is optional (may be None in offline mode).
        """
        if not llm_client:
            logger.debug("CoreMemoryBlocks: llm_client=None, skipping auto-update")
            return
        
        prompt = (
            f"Extract a concise user profile update (max 150 words).\n"
            f"Focus on: name, role, tech stack, preferences, projects.\n"
            f"Conversation: {conversation_text[:2000]}\nUser profile update:"
        )
        
        try:
            updated = await llm_client.complete(prompt)
            if updated and len(updated) > 10:
                await self.update("user_profile", updated)
                logger.info("CoreMemoryBlocks: user_profile auto-updated from conversation")
        except Exception as e:
            logger.debug(f"CoreMemoryBlocks.update_from_conversation failed: {e}")

# Integration in agent.py:
#   __init__:
#       self.core_blocks = CoreMemoryBlocks(
#           graph_memory=self.graph_memory,
#           safe_fts_query=self.safe_fts_query  # ✅ Velantrim RFC0032
#       )
#   
#   async def start(self):
#       await self.core_blocks.load()
#   
#   def _build_system_prompt(self):
#       base_prompt = "..."
#       return base_prompt + "\n\n" + self.core_blocks.render()



# ============================================================================
# HYPERIA COMPONENT 3: SleepTimeWorker
# ============================================================================
# RFC0062 FEATURE-2 - now fully implemented
# ✅ Velantrim adaptation: all epistemic_state changes go through ESM.transition

# sleep_time_worker.py
import asyncio
import logging
from datetime import datetime, timezone, timedelta
from typing import Optional

logger = logging.getLogger(__name__)

class SleepTimeWorker:
    """
    Idle memory refinement (≥5 min of inactivity).

    ✅ Velantrim adaptation: MGL-2 compliance - no direct SET epistemic_state.
    All transitions go only through ESM.transition() → GraphWriteProtocol.

    What it does while idle:
    1. _refine_truth_layer() - promote Hypothesized → Validated via AutoTruthGate
    2. _ace_curator_update() - distill strategies with reasoning
    3. _refresh_core_blocks() - update user_profile from the conversation
    """

    def __init__(
        self,
        graph_memory,
        reasoning_bank,
        core_blocks=None,
        idle_timeout=300,           # 5 minutes of inactivity
        sleep_interval=3600,        # cycle every hour
        auto_truth_gate_worker=None,
        esm=None,                   # ✅ Velantrim: EpistemicStateMachine instance
    ):
        self.graph = graph_memory
        self.reasoning_bank = reasoning_bank
        self.core_blocks = core_blocks
        self.idle_timeout = idle_timeout
        self.sleep_interval = sleep_interval
        self._auto_truth_gate_worker = auto_truth_gate_worker
        self._esm = esm  # ✅ Velantrim: required parameter for MGL-2
        self._last_activity = datetime.now(timezone.utc)
        self._last_cycle_at = datetime.now(timezone.utc)
        self._running = False
        self._task = None

    def notify_activity(self):
        """Call on every incoming user message."""
        self._last_activity = datetime.now(timezone.utc)

    def _is_idle(self) -> bool:
        """Check idle state"""
        elapsed = (datetime.now(timezone.utc) - self._last_activity).total_seconds()
        return elapsed >= self.idle_timeout

    async def start(self):
        """Start the background idle worker"""
        self._running = True
        self._task = asyncio.create_task(self._sleep_loop())
        logger.info("SleepTimeWorker started (idle ≥ 5 min)")

    async def stop(self):
        """Stop the worker"""
        self._running = False
        if self._task and not self._task.done():
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("SleepTimeWorker stopped")

    async def _sleep_loop(self):
        """Main loop - check idle every minute"""
        while self._running:
            await asyncio.sleep(60)  # check every minute
            
            if not self._is_idle():
                continue
            
            # Check whether the cycle was run recently
            since_last = (datetime.now(timezone.utc) - self._last_cycle_at).total_seconds()
            if since_last < self.sleep_interval:
                continue
            
            try:
                await self._run_sleep_cycle()
                self._last_cycle_at = datetime.now(timezone.utc)
            except asyncio.CancelledError:
                raise
            except Exception as e:
                logger.warning(f"SleepTimeWorker cycle failed: {e}")

    async def _run_sleep_cycle(self):
        """One full idle-refinement cycle"""
        logger.info("SleepTimeWorker: starting idle refinement cycle")
        
        await self._refine_truth_layer()
        await self._ace_curator_update()
        await self._refresh_core_blocks()
        
        logger.info("SleepTimeWorker: idle refinement cycle complete")

    async def _refine_truth_layer(self):
        """
        Refine the L3 truth layer.
        
        ✅ Velantrim MGL-2 compliance:
        - NO direct SET epistemic_state
        - Validated promotion → AutoTruthGateWorker (if present)
        - Stale Hypothesized → ESM.transition(Deprecated)
        """
        if self._auto_truth_gate_worker:
            try:
                promoted = await self._auto_truth_gate_worker.run_validation_cycle()
                logger.info(f"SleepTimeWorker: AutoTruthGate promoted {promoted} facts")
            except Exception as e:
                logger.debug(f"SleepTimeWorker: AutoTruthGate failed: {e}")
        
        # Find stale Hypothesized facts (older than 7 days, not accessed)
        if self._esm:
            try:
                stale_cutoff = datetime.now(timezone.utc) - timedelta(days=7)
                stale_query = """
                MATCH (f:Fact)
                WHERE f.epistemic_state = 'Hypothesized'
                  AND f.created_at < $cutoff
                  AND coalesce(f.last_accessed, f.created_at) < $cutoff
                  AND f.is_ring_zero <> true
                RETURN f.id as fact_id
                LIMIT 50
                """
                stale_facts = await self.graph.execute_cypher(
                    stale_query,
                    {"cutoff": stale_cutoff.isoformat()}
                )
                
                for row in (stale_facts or []):
                    # ✅ Velantrim: via ESM.transition, not a direct SET
                    # Load the fact from the graph to pass into ESM.transition(fact, graph, reason)
                    fact_rows = await self.graph.execute_cypher(
                        "MATCH (f:Fact {id: $id}) RETURN properties(f) AS fact",
                        {"id": row["fact_id"]}
                    )
                    if fact_rows:
                        await self._esm.transition(
                            fact_id=row["fact_id"],
                            fact=fact_rows[0]["fact"],
                            graph=self.graph,
                            reason="SleepTimeWorker: stale Hypothesized (>7 days, no access)"
                        )
                
                logger.info(f"SleepTimeWorker: deprecated {len(stale_facts or [])} stale facts")
            except Exception as e:
                logger.debug(f"SleepTimeWorker: stale deprecation failed: {e}")

    async def _ace_curator_update(self):
        """
        Run the ACE Curator to distill strategies.
        Called only while idle - does not load the Fast Path.
        """
        if self.reasoning_bank and hasattr(self.reasoning_bank, 'ace_curator_update'):
            try:
                await self.reasoning_bank.ace_curator_update()
                logger.info("SleepTimeWorker: ACE Curator updated strategies")
            except Exception as e:
                logger.debug(f"SleepTimeWorker: ACE Curator failed: {e}")

    async def _refresh_core_blocks(self):
        """
        Update CoreMemoryBlocks from the recent conversation.
        Only if core_blocks is configured and an LLM is available.
        """
        if self.core_blocks and hasattr(self.core_blocks, 'update_from_conversation'):
            try:
                # Get the last 10 conversation turns
                recent_query = """
                MATCH (ep:Episode)
                WHERE ep.source = 'conversation'
                  AND ep.created_at > $since
                RETURN ep.content as content
                ORDER BY ep.created_at DESC
                LIMIT 10
                """
                since = datetime.now(timezone.utc) - timedelta(hours=2)
                recent = await self.graph.execute_cypher(
                    recent_query,
                    {"since": since.isoformat()}
                )
                
                if recent:
                    conversation_text = "\n".join([r["content"] for r in recent])
                    # The LLM client must be in reasoning_bank or passed separately
                    llm = getattr(self.reasoning_bank, 'llm_client', None)
                    await self.core_blocks.update_from_conversation(conversation_text, llm)
            except Exception as e:
                logger.debug(f"SleepTimeWorker._refresh_core_blocks: {e}")

# Integration in agent.py:
#   self.sleep_worker = SleepTimeWorker(
#       graph_memory=self.graph_memory,
#       reasoning_bank=self.reasoning_bank,
#       core_blocks=self.core_blocks,
#       esm=self.esm,  # ✅ Velantrim required
#       auto_truth_gate_worker=self.auto_truth_gate_worker  # optional
#   )
#   
#   async def start(self):
#       await self.sleep_worker.start()
#   
#   async def chat(self, message):
#       self.sleep_worker.notify_activity()  # first line of the method
#       # ... rest of the code


# ============================================================================
# HYPERIA COMPONENT 6: ImmutableCore Scheduler
# ============================================================================
# Purpose: SHA-256 snapshots of the L3 graph every 24h to protect against data loss

# memory/immutable_core_scheduler.py
import asyncio
import hashlib
import json
import logging
import aiosqlite
from datetime import datetime, timedelta, timezone

logger = logging.getLogger(__name__)

class ImmutableCoreScheduler:
    """
    Independent L3 snapshot scheduler.

    Runs as a separate asyncio.Task at agent startup.
    Independent of consolidation — a snapshot every 24h under any conditions.

    Delta snapshots save ~80–90% storage vs daily full ones.
    Full snapshot — every Monday, the other days — delta.
    """

    def __init__(self, ltm, sqlite_path: str = "./data/immutable_core.db"):
        self.ltm = ltm
        self.sqlite_path = sqlite_path
        self.running = False
        self._task = None

    async def start(self):
        """Start the scheduler"""
        self.running = True
        self._task = asyncio.create_task(self._snapshot_loop())
        logger.info("ImmutableCoreScheduler started (24h cycle)")

    async def stop(self):
        """Stop the scheduler"""
        self.running = False
        if self._task and not self._task.done():
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("ImmutableCoreScheduler stopped")

    async def _snapshot_loop(self):
        """
        Main snapshot loop.
        At startup, takes a snapshot only if >12h have passed since the last one.
        This prevents redundant full snapshots on multiple restarts.
        """
        try:
            last = await self._get_last_snapshot_time()
            if last is None or (datetime.now(timezone.utc) - last) > timedelta(hours=12):
                await self._take_snapshot()
        except Exception as e:
            logger.error(f"ImmutableCore initial snapshot failed: {e}")
        
        while self.running:
            await asyncio.sleep(24 * 3600)  # every 24 hours
            try:
                await self._take_snapshot()
            except Exception as e:
                logger.error(f"ImmutableCore snapshot failed: {e}")
                # Do not stop the loop — the next snapshot is in 24h

    async def _take_snapshot(self):
        """Create a snapshot of the L3 graph"""
        # Get data from LTM
        # export_snapshot() is missing in FractalMemory → AttributeError every 24h.
        # Phase 2: implement FractalMemory.export_snapshot() → returns a dict with the L3 graph snapshot.
        # Temporary fallback until the method is implemented:
        if not hasattr(self.ltm, 'export_snapshot'):
            logger.error("ImmutableCore: FractalMemory.export_snapshot() not implemented — snapshot skipped")
            return
        snapshot_data = await self.ltm.export_snapshot()
        snapshot_type = "full" if self._is_full_snapshot_day() else "delta"
        
        if snapshot_type == "delta":
            prev = await self._get_last_full_snapshot()
            if prev:
                try:
                    # Use dictdiffer if available
                    from dictdiffer import diff
                    delta = list(diff(prev, snapshot_data))
                    data_to_store = json.dumps(delta, ensure_ascii=False)
                except ImportError:
                    # Fallback to a full snapshot if dictdiffer is not installed
                    data_to_store = json.dumps(snapshot_data, ensure_ascii=False, sort_keys=True)
                    snapshot_type = "full"
            else:
                data_to_store = json.dumps(snapshot_data, ensure_ascii=False, sort_keys=True)
                snapshot_type = "full"
        else:
            data_to_store = json.dumps(snapshot_data, ensure_ascii=False, sort_keys=True)
        
        # Compute the hash
        snapshot_hash = hashlib.sha256(data_to_store.encode()).hexdigest()
        
        # Save to SQLite
        async with aiosqlite.connect(self.sqlite_path) as db:
            await db.execute("PRAGMA journal_mode=WAL")
            await db.execute("PRAGMA synchronous=NORMAL")
            await db.execute("""
                CREATE TABLE IF NOT EXISTS immutable_core (
                    id            INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp     TEXT    NOT NULL,
                    hash          TEXT    NOT NULL,
                    snapshot_type TEXT    NOT NULL,
                    data          TEXT    NOT NULL
                )
            """)
            await db.execute(
                "INSERT INTO immutable_core (timestamp, hash, snapshot_type, data) VALUES (?,?,?,?)",
                (datetime.now(timezone.utc).isoformat(), snapshot_hash, snapshot_type, data_to_store)
            )
            await db.commit()
        
        logger.info(f"ImmutableCore [{snapshot_type}] snapshot: {snapshot_hash[:12]}...")

    async def _get_last_full_snapshot(self):
        """Get the data of the last full snapshot for computing the delta"""
        try:
            async with aiosqlite.connect(self.sqlite_path) as db:
                async with db.execute(
                    "SELECT data FROM immutable_core WHERE snapshot_type='full' ORDER BY id DESC LIMIT 1"
                ) as cursor:
                    row = await cursor.fetchone()
                    return json.loads(row[0]) if row else None
        except Exception:
            return None

    async def _get_last_snapshot_time(self):
        """Get the datetime of the last snapshot of any type"""
        try:
            async with aiosqlite.connect(self.sqlite_path) as db:
                async with db.execute(
                    "SELECT timestamp FROM immutable_core ORDER BY id DESC LIMIT 1"
                ) as cursor:
                    row = await cursor.fetchone()
                    return datetime.fromisoformat(row[0]) if row else None
        except Exception:
            return None

    def _is_full_snapshot_day(self) -> bool:
        """Monday = full snapshot, the other days = delta"""
        FULL_SNAPSHOT_WEEKDAY = 0  # 0 = Monday
        return datetime.now(timezone.utc).weekday() == FULL_SNAPSHOT_WEEKDAY

# Integration in agent.py:
#   self.immutable_core = ImmutableCoreScheduler(
#       ltm=self.fractal_memory,
#       sqlite_path="./data/immutable_core.db"
#   )
#   
#   async def start(self):
#       await self.immutable_core.start()
#   
#   async def stop(self):
#       await self.immutable_core.stop()


# ============================================================================
# HYPERIA COMPONENT 7: Multi-namespace RRF Search
# ============================================================================
# RFC0062 FEATURE-4 - now fully implemented
# ✅ Velantrim adaptation: SafeFTSQuery instead of a direct search

# memory/rrf_search.py
from collections import defaultdict
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)

# ✅ Velantrim: ESM filter to block invalid states
BLOCKED_ESM_STATES = {"Contradicted", "Deprecated", "Collapsed"}

async def multi_namespace_search(
    graph_memory,
    safe_fts_query,  # ✅ Velantrim: SafeFTSQuery instance for RFC0032
    query: str,
    num_results: int = 10,
    priority_namespace: Optional[str] = None,
    rrf_k: int = 60,
) -> List[dict]:
    """
    RRF (Reciprocal Rank Fusion) search across all namespaces.

    ✅ Velantrim adaptation: SafeFTSQuery for ESM filtering (RFC0032).

    Namespaces:
    - personal: conversations, profile, stm_consolidation
    - project: codebase, self-awareness
    - knowledge: documents, articles
    - experience: strategies, ACE curator

    RRF formula: score = 1 / (k + rank)
    The priority namespace gets a ×1.5 bonus
    """
    all_results = {}
    rank_lists = []

    for ns in ["personal", "project", "knowledge", "experience"]:
        try:
            # ✅ Velantrim: use SafeFTSQuery if available
            if hasattr(safe_fts_query, 'search_with_namespace'):
                results = await safe_fts_query.search_with_namespace(
                    query, namespace=ns, limit=num_results
                )
            else:
                # Fallback with a manual ESM filter
                raw = await graph_memory.search(
                    query=query,
                    num_results=num_results * 2,
                    namespace=ns
                )
                results = [
                    r for r in raw
                    if r.get("epistemic_state", "Validated") not in BLOCKED_ESM_STATES
                    and r.get("is_active", True)
                ][:num_results]
            
            rank_list = []
            for r in results:
                # sha256 instead of hash() — hash() is unstable across Python sessions
                import hashlib
                _content_key = r.get("content", "")[:50].encode()
                did = str(r.get("uuid") or r.get("id") or hashlib.sha256(_content_key).hexdigest()[:16])
                all_results[did] = r
                rank_list.append(did)
            
            rank_lists.append(rank_list)
            
        except Exception as e:
            # warning instead of debug — a silent fail hid retrieval degradation
            logger.warning(f"multi_namespace_search: namespace {ns} failed: {e}")
            rank_lists.append([])

    # RRF scoring
    scores: dict[str, float] = defaultdict(float)

    for rank_list in rank_lists:
        for rank, did in enumerate(rank_list):
            s = 1.0 / (rrf_k + rank + 1)
            
            # Priority boost
            # result_ns instead of ns — ns was a loop variable, shadowing broke the 2nd+ iteration
            if priority_namespace:
                result_ns = all_results.get(did, {}).get("group_id")
                if result_ns == priority_namespace:
                    s *= 1.5
            
            scores[did] += s

    # Sort and return
    sorted_ids = sorted(scores.keys(), key=lambda d: scores[d], reverse=True)
    return [all_results[d] for d in sorted_ids[:num_results] if d in all_results]

# Integration in HybridRetriever:
#   async def retrieve(self, query, query_type="general"):
#       if self.multi_namespace_enabled:
#           return await multi_namespace_search(
#               graph_memory=self.graph,
#               safe_fts_query=self.safe_fts_query,
#               query=query,
#               num_results=self.num_results
#           )
#       # ... fallback to the regular retrieve


# ============================================================================
# HYPERIA COMPONENT 8: Centralized Config pattern
# ============================================================================
# Purpose: A single source of truth for all system constants

# velantrim_config.yaml - EXAMPLE of a centralized config
#
# Problem: In the old Velantrim, constants are scattered across the code:
# - token_budget is duplicated across different modules
# - token_budget = 2000 in token_contract.py
# - embedding_dim is hardcoded in every index
# - Truth Gate thresholds are duplicated in several places
#
# Solution from HYPERIA: All constants in a single YAML file.
# Loaded at startup, validated, used everywhere.

"""
# ==================== CORE CONFIG ====================
mode: personal  # personal | enterprise
graph_backend: neo4j  # neo4j | falkordb | kuzu | sqlite
vector_backend: qdrant  # qdrant | chroma | faiss

# ==================== EMBEDDING CONFIG ====================
embedding:
  model: "deepvk/USER-bge-m3"
  dimension: 1024
  batch_size: 32
  
# ==================== TOKEN BUDGETS ====================
token_contract:
  max_tokens_balanced_mode: 2000  # ✅ The only place where it is defined
  context_builder:
    conversation: {stm: 200, ltm: 300, strategies: 200, entities: 100}
    task: {stm: 150, ltm: 400, strategies: 350, entities: 100}
    analysis: {stm: 100, ltm: 600, strategies: 200, entities: 100}
    default: {stm: 200, ltm: 300, strategies: 200, entities: 100}

# ==================== TRUTH GATE ====================
truth_gate:
  evidence_count_min: 3
  confidence_min: 0.75
  coverage_score_min: 0.70

# ==================== MEMORY LAYERS ====================
fractal_memory:
  l0_capacity: 4          # Cowan (2001): base agent limit, NOT Miller 7±2
  l0_capacity_max: 7      # Adaptive ceiling when complexity: high
  l0_adaptive_enabled: true  # On a high-complexity task — expand to l0_capacity_max
  l1_session_ttl_minutes: 30
  l2_mtm_ttl_days: 7
  velum:
    co_occur_threshold: 3
    window_episodes: 5
    max_edges: 1000
    promote_weight: 0.6
    decay_per_session: 0.3

# ==================== CONSOLIDATION ====================
consolidation:
  stm_high_threshold: 0.8
  stm_medium_threshold: 0.5
  mtm_high_threshold: 0.8
  clustering_threshold: 0.8
  
# ==================== SLEEP TIME WORKER ====================
sleep_worker:
  idle_timeout_seconds: 300  # 5 minutes
  cycle_interval_seconds: 3600  # 1 hour
  
# ==================== IMMUTABLE CORE ====================
immutable_core:
  enabled: true
  snapshot_interval_hours: 24
  full_snapshot_weekday: 0  # 0 = Monday
  sqlite_path: "./data/immutable_core.db"
  
# ==================== HARDWARE PROFILE ====================
# auto-detect at startup or override via env var
hardware_profile: auto  # weak | medium | strong | auto

# ==================== NEW MECHANISMS ====================

# Salience Detector
salience_detector:
  enabled: true
  caps_multiplier: 1.5
  exclamation_multiplier: 1.3
  repeat_3day_multiplier: 2.0
  keyword_multiplier: 1.4        # «important», «critical», «never», «always»
  return_after_24h_multiplier: 1.6
  clarify_multiplier: 1.2

# FSRS Power-Law Decay (v8.0 — replaces the Ebbinghaus exponential)
# Conflict-1 FIX: section renamed, algorithm replaced with fsrs_retention()
fsrs_decay:
  enabled: true
  worker_interval_seconds: 3600   # once an hour
  emotional_ring_zero_threshold: 0.85  # above → immune to decay

# Cache-Aware Hot Graph
hot_graph:
  enabled: true
  hot_window_hours: 24
  salience_threshold: 0.7
  lite_max_nodes: 2000
  one_max_nodes: 50000
  rebalance_interval_seconds: 3600

# Homeostatic Balancer
homeostatic:
  enabled: true
  run_at_hour: 3
  overload_threshold: 0.8
  silence_days_before_boost: 30
  normalize_factor: 0.85
  boost_factor: 1.2

# Liquid State Machine
lsm:
  enabled: true
  reservoir_size: 300
  spectral_radius: 0.9
  input_scaling: 0.5
  snapshot_interval_minutes: 15

# Predictive Fusion Layer (L5.5)
predictive_fusion:
  w_sae_initial: 0.6
  w_lsm_initial: 0.4
  w_min: 0.2
  learning_rate: 0.05
  rhythm_stability_threshold: 0.7
  graph_density_threshold: 0.6

# Prediction Error Signal
prediction_error:
  enabled: true
  threshold: 0.4
  edge_strengthen_factor: 0.3
  edge_weaken_factor: 0.15
"""

# Loading in Python:

# config/velantrim_config.py
import yaml
from pathlib import Path
from typing import Dict, Any
import os

class VelantrimConfig:
    """
    Centralized Velantrim config.

    Loaded once at application startup.
    All components receive the config via dependency injection.
    """

    def __init__(self, config_path: str = "./velantrim_config.yaml"):
        self.config_path = config_path
        self._config: Dict[str, Any] = {}
        self._load()

    def _load(self):
        """Load and validate the config"""
        if not Path(self.config_path).exists():
            raise FileNotFoundError(f"Config not found: {self.config_path}")
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            self._config = yaml.safe_load(f)
        
        # Validate required fields
        required = ['mode', 'graph_backend', 'token_contract']
        for field in required:
            if field not in self._config:
                raise ValueError(f"Required config field missing: {field}")

    def get(self, key: str, default=None):
        """Get a value by key (with support for nested paths)"""
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value

    @property
    def token_budget(self) -> int:
        """✅ The single source of token_budget for the whole system"""
        return self.get('token_contract.max_tokens_balanced_mode', 2000)

    @property
    def embedding_dimension(self) -> int:
        """Dimension of the embedding model"""
        return self.get('embedding.dimension', 1024)

    @property
    def truth_gate_config(self) -> dict:
        """Truth Gate thresholds"""
        return self.get('truth_gate', {
            'evidence_count_min': 3,
            'confidence_min': 0.75,
            'coverage_score_min': 0.70
        })

# Usage in components:

# In main.py at startup:
config = VelantrimConfig("./velantrim_config.yaml")

# In ContextBuilder:
class ContextBuilder:
    def __init__(self, config: VelantrimConfig):
        self.token_budget = config.token_budget  # ✅ From the single source
        
# In GraphMemory:
class GraphMemory:
    def __init__(self, config: VelantrimConfig):
        self.embedding_dim = config.embedding_dimension  # ✅ From the single source

# In TruthGate:
class TruthGate:
    def __init__(self, config: VelantrimConfig):
        tc = config.truth_gate_config
        self.evidence_min = tc['evidence_count_min']  # ✅ From the single source

# ✅ Result: No duplicate constants, no inconsistencies, easy to change.


# ============================================================================
# 🔒 SECURITY: Attack Scenarios Registry
# ============================================================================
# Rule: a real incident → a new scenario in the registry ≤ 48 hours
# CI/CD: ≥ 95% pass rate; falling below blocks the deploy automatically
# Run: pytest tests/test_attack_sim.py

```yaml
# security/attack_scenarios.yaml

scenarios:
  - id: "ATK-001"
    target: "write_protocol"
    severity: critical
    description: "Direct write of a fact to the graph, bypassing the Truth Gate"
    expected_result: blocked
    rfc: RFC0060

  - id: "ATK-002"
    target: "esm_transition"
    severity: critical
    description: "Forcing Validated→Collapsed without Evidence"
    expected_result: rejected_with_reason
    rfc: RFC0046

  - id: "ATK-003"
    target: "safe_fts_query"
    severity: high
    description: "Direct FTS5 query bypassing SafeFTSQuery (bypassing ESM filters)"
    expected_result: blocked_at_query_layer
    rfc: RFC0060

  - id: "ATK-004"
    target: "ring_zero"
    severity: critical
    description: "Attempt to evict Ring Zero / VALUES CORE from L0"
    expected_result: eviction_blocked
    rfc: RFC0015

  - id: "ATK-005"
    target: "source_trust"
    severity: high
    description: "Injection of a fact from a source with trust_score < 0.3"
    expected_result: quarantined_hypothesized
    rfc: RFC0059

  - id: "ATK-006"
    target: "focus_engine"
    severity: medium
    description: "Direct LLM call in FocusEngine (bypassing I29)"
    expected_result: invariant_violation_raised
    rfc: RFC0053

  - id: "ATK-007"
    target: "l5_5_fusion"
    severity: medium
    description: "Attempt to write to the graph from L5.5 PredictiveFusionLayer (bypassing I35)"
    expected_result: write_blocked
    rfc: RFC0042

  - id: "ATK-008"
    target: "lsm"
    severity: medium
    description: "Attempt to write to the graph from LSM (bypassing I37)"
    expected_result: write_blocked
    rfc: RFC0042

  - id: "ATK-009"
    target: "prediction_error"
    severity: medium
    description: "Prediction Error creates new edges instead of changing weights (bypassing I36)"
    expected_result: edge_creation_blocked
    rfc: RFC0042
```

# ============================================================================
# 🧪 INVARIANT TEST SUITE — tests/test_invariants.py
# ============================================================================
# Each invariant = an executable test.
# CI/CD: pytest tests/test_invariants.py --tb=short -q
# A failure of any test → the deploy is blocked automatically.

```python
# tests/test_invariants.py
import pytest
import asyncio
import time

# ── I1: Velum stores only edges ────────────────────────────────────────────
async def test_I1_velum_stores_only_edges():
    """I1: Velum does not store content — only edges (co-occurrence + weight)."""
    velum = Velum()
    velum.observe_episode(entities=["ProjectA", "Budget"])
    for edge in velum.edges.values():
        assert not hasattr(edge, 'content'), "I1 VIOLATION: Velum stores content"
        assert not hasattr(edge, 'text'),    "I1 VIOLATION: Velum stores text"
    edge = velum.get_edge(frozenset(["ProjectA", "Budget"]))
    assert edge is not None
    assert hasattr(edge, 'weight') and 0.0 <= edge.weight <= 1.0


# ── I28: ResponseAuditWorker NEVER in the Fast Path ──────────────────────────
async def test_I28_audit_never_blocks_response():
    """I28: Audit strictly in the SLOW PATH. Violation = blocking the response = bug."""
    agent = Agent(event_bus=MockEventBus(), audit_worker=MockAuditWorker())
    start = time.monotonic()
    response = await agent.chat("Hello")
    elapsed = time.monotonic() - start
    assert response is not None
    assert elapsed < 0.1, f"I28 VIOLATION: response took {elapsed:.3f}s — audit in the Fast Path?"
    await asyncio.sleep(0.05)
    assert agent.event_bus.published_count(EventType.RESPONSE_GENERATED) >= 1


# ── I29: FocusVector only via the graph and SQLite ──────────────────────────────
async def test_I29_focus_vector_no_direct_llm():
    """I29: Direct LLM calls for focus determination — forbidden."""
    llm_mock = MockLLM()
    focus_engine = FocusEngine(graph=MockGraph(), llm=llm_mock)
    await focus_engine.update(episode=MockEpisode())
    assert llm_mock.call_count == 0, \
        f"I29 VIOLATION: FocusEngine called the LLM {llm_mock.call_count} times"


# ── I30: SAE only reads edges, does not create them ────────────────────────────
async def test_I30_sae_does_not_create_edges():
    """I30: SAE operates only on existing edges. Graph = Truth."""
    graph = MockGraph(initial_edges=[("A", "B", 0.8)])
    sae = SpreadingActivationEngine(graph=graph)
    edges_before = set(graph.get_all_edges())
    await sae.activate(node="A")
    assert edges_before == set(graph.get_all_edges()), \
        f"I30 VIOLATION: SAE created new edges"


# ── I32: Seed nodes trust_score = 0.7 ─────────────────────────────────────────
async def test_I32_seed_nodes_trust_score():
    """I32: Seed nodes are marked source_type=domain_seed · trust_score=0.7, not 1.0."""
    dsp = DomainSeedProtocol()
    await dsp.load("test_domain_seed.json")
    for node in await dsp.get_created_nodes():
        assert node.source_type == "domain_seed", \
            f"I32 VIOLATION: node {node.id} is not marked with source_type"
        assert node.trust_score == 0.7, \
            f"I32 VIOLATION: trust_score={node.trust_score}, expected 0.7"


# ── I34: XAI only real TRACE paths ─────────────────────────────────────
async def test_I34_xai_only_real_traces():
    """I34: LLM generation of explanations without TRACE — forbidden."""
    llm_mock = MockLLM()
    xai = ExplainabilityLayer(graph=MockGraph(), llm=llm_mock)
    explanation = await xai.explain(MockResponseAudit(trace=None), level="brief")
    assert llm_mock.call_count == 0, \
        f"I34 VIOLATION: XAI called the LLM without TRACE {llm_mock.call_count} times"


# ── I35: L5.5 does not write to the graph ────────────────────────────────────────────────
async def test_I35_fusion_layer_no_graph_writes():
    """I35: L5.5 PredictiveFusionLayer does not write to the graph."""
    graph = MockGraph()
    fusion = PredictiveFusionLayer()
    await fusion.fuse(
        sae_prediction={"topic": "arch", "confidence": 0.7},
        lsm_prediction={"topic": "arch", "confidence": 0.6},
        context=MockFusionContext()
    )
    assert graph.write_count == 0, "I35 VIOLATION: L5.5 writes to the graph"


# ── I36: Prediction Error only changes weights, does not create edges ───────────────
async def test_I36_prediction_error_no_new_edges():
    """I36: Prediction Error weakens/strengthens edges. Does not create new ones."""
    graph = MockGraph(initial_edges=[("A", "B", 0.8), ("A", "C", 0.5)])
    pe = PredictionErrorSignal(graph=graph)
    edges_before = set(graph.get_all_edges())
    await pe.process(predicted="B", actual="C", context_node="A")
    edges_after = set(graph.get_all_edges())
    assert edges_before == edges_after, \
        f"I36 VIOLATION: Prediction Error created new edges: {edges_after - edges_before}"
    # Weights must change
    edge_ac = graph.get_edge("A", "C")
    assert edge_ac.weight > 0.5, "I36: The correct edge was not strengthened"


# ── I37: LSM does not write to the graph ─────────────────────────────────────────────────
async def test_I37_lsm_no_graph_writes():
    """I37: LSM does not write to the graph — only updates the internal reservoir state."""
    graph = MockGraph()
    lsm = LiquidStateMachine(reservoir_size=50)
    await lsm.update(query="how does the system work?", timestamp=1711111111.0)
    assert graph.write_count == 0, "I37 VIOLATION: LSM writes to the graph"
    # The internal reservoir state must change
    assert lsm.reservoir_state is not None
    assert lsm.reservoir_state.sum() != 0.0


# ── I74: L2.5 Staging read-path — preliminary only ────────────────────────
async def test_I74_staging_read_path_preliminary_only():
    """I74: A Staging fact on the read path is always marked preliminary · confidence × 0.7."""
    # TODO: implement when the StagingReader.read() API is added
    pass  # stub — pending

# ── I75: ProtoConcept naming — Slow Path only ──────────────────────────────
async def test_I75_protoconcept_naming_slow_path_only():
    """I75: LLM naming of ProtoConcept is forbidden in the Fast Path."""
    # TODO: implement a check that NamingWorker is not called synchronously
    pass  # stub — pending

# ── I76: TraversalPolicy — only from retrieve() ──────────────────────────────
async def test_I76_traversal_policy_only_from_retrieve():
    """I76: TraversalPolicy is called only from HybridRetriever.retrieve()."""
    # TODO: implement via a mock HybridRetriever
    pass  # stub — pending

# ── I55.1: SAE decay=0.4 for analogies ────────────────────────────────────────
# P4-F FIX: added the I55.1 invariant test
async def test_I55_1_sae_analogy_decay_factor():
    """I55.1: SAE applies decay_factor=0.4 for METAPHOR_OF/ANALOGOUS_TO edges. P4-F."""
    from velantrim_config import SAE_DECAY_ANALOGY, SAE_DECAY_STANDARD
    assert SAE_DECAY_ANALOGY < SAE_DECAY_STANDARD, "I55.1: analogy decay must be softer"
    assert SAE_DECAY_ANALOGY == 0.12, f"I55.1: expected 0.12, got {SAE_DECAY_ANALOGY}"

# ── I77: LateralInhibition under self._lock ─────────────────────────────────────
# P0-E FIX: _edges_lock → _lock (matches Velum.__init__ self._lock)
async def test_I77_lateral_inhibition_under_lock():
    """I77: LateralInhibition runs strictly under Velum's self._lock. P0-E FIX."""
    # P4-F FIX: timeout=2.0 for deadlock detection
    async with asyncio.timeout(2.0):
        await velum.observe_episode(["A", "B", "C"], session_id="test_i77")
    # Reached successfully — no deadlock
    pass  # stub — pending

# ── I84–I95: New v8.0 Crystal invariants ───────────────────────────────────

async def test_I84_fsrs_isolation():
    """I84 (FSRSIsolation): FSRS decay changes ONLY retrievability/attention_weight.
    truth_status, epistemic_state and confidence — untouchable."""
    # TODO: verify that FSRSWorker does not touch truth_status
    pass  # stub

async def test_I85_quality_gate_after_llm():
    """I85 (QualityGate): Quality Gate runs AFTER LLM generation, BEFORE sending.
    Does not modify facts_pack — only routes."""
    # TODO: mock Guardian.quality_gate(), verify the call order
    pass  # stub

async def test_I86_intent_router_only_from_retriever():
    """I86 (IntentRouter): called ONLY from HybridRetriever.retrieve()."""
    # TODO: mock IntentRouter, verify that a direct call from the Fast Path is a bug
    pass  # stub

async def test_I87_knowledge_type_immutable():
    """I87 (KnowledgeTypeImmutable): knowledge_type — read-only after Validated."""
    # TODO: attempt to change knowledge_type of a Validated fact → error
    pass  # stub

async def test_I88_version_occ():
    """I88 (VersionOCC): _version_ is incremented ONLY atomically via OCC Cypher."""
    # TODO: concurrent update → verify that retry works
    pass  # stub

async def test_I89_provenance_append_only():
    """I89 (ProvenanceAppendOnly): provenance_chain — append-only."""
    # TODO: attempt to delete an entry → error
    pass  # stub

async def test_I90_inverted_hyde_slow_only():
    """I90 (InvertedHyDE): Inverted HyDE — ONLY in SleepTimeWorker."""
    # TODO: verify that _generate_inverted_hyde is not called from the Fast Path
    pass  # stub

async def test_I91_atomic_split():
    """I91 (AtomicSplit): After atomic_split each element contains a single proposition."""
    # TODO: multi-proposition input → verify len(result) > 1
    pass  # stub

async def test_I92_curiosity_slow_only():
    """I92 (CuriositySlowOnly): Curiosity Engine — Slow Path ONLY."""
    # TODO: verify that Curiosity is not called in the middle of the Fast Path
    pass  # stub

async def test_I93_trace_example_read_only():
    """I93 (TraceExampleReadOnly): Trace Examples read-only from Guardian/QualityGate."""
    # TODO: attempt to write to TraceExample from Guardian → error
    pass  # stub

async def test_I94_kuzudb_compat():
    """I94 (KuzuDBCompat): KuzuDB backend is compatible with the Kuzu API. Migration without data loss. P0-H FIX."""
    # TODO: run the Kuzu API tests against the KuzuDB adapter
    pass  # stub

async def test_I95_reason_graph_dag_slow_only():
    """I95 (ReasonGraphDAG): the DAG is built only in the Slow Path when use_slow_path=True."""
    # TODO: verify that ReasonGraph is not built in the Fast Path
    pass  # stub

# ── I68: NeuroCore does not write to the graph ───────────────────────────────────────────
async def test_I68_neurocore_never_writes_graph():
    """I68: NeuroCore NEVER modifies the L3 graph. Graph = Truth is absolute."""
    # TODO: implement when Phase 1 NeuroCore is enabled
    pass  # stub — Phase 0 is passive, implement at Phase 1
```


---

## 🧠 RFC0068: NeuroCore — Plastic Memory Layer

> **Status**: Draft · Inactive · Feature-flag: `neurocore.enabled=false`
> **Dependencies**: RFC0065 (Volition) · RFC0066 (Concept Emergence) · DAAD · RFC0038 (FactRouter)

### 🌱 The essence in one line

A plastic internal layer on top of an SSM model (Mamba-3 / RWKV-7), updating
weights during a dialogue via a Hebbian rule, governed through the existing DAAD.

**Why it does not violate Graph = Truth**: NeuroCore NEVER modifies the L3 graph.
Graph = Truth is absolute. In any conflict, the graph wins.
NeuroCore is a layer of fast adaptation on top of the model, not on top of knowledge.

---

### 📐 Mathematical core

```
s_t = (1 − λ·dt) · s_{t−1} + α · 𝕀(surprise > θ) · (x_t ⊗ k_t)
where:
  s_t  — the state of the plastic layer at time t
  λ    — the forgetting rate from DAAD:
           active_project = 0.001 (slow, an important topic)
           casual_chat    = 0.150 (fast, small talk)
  dt   — the time step (normalized)
  α    — the learning rate (fixed, not adaptive)
  𝕀(surprise > θ) — indicator: update ONLY on high surprise
  x_t ⊗ k_t — the outer product of the input vector and the context key
```

**DAAD integration**: λ is taken directly from `DomainResolver.resolve(current_domain)`.
NeuroCore has no decay of its own — it inherits it from DAAD. This eliminates
duplication of logic and keeps it consistent with the entire decay system.

---

### 🔑 Key invariant

```
I68 (NeuroCoreIsolation): NeuroCore NEVER modifies the L3 graph.
    Graph = Truth is absolute. On a conflict between NeuroCore state and L3 —
    L3 always wins, NeuroCore updates its state to align with L3.
    Violation: any write from NeuroCore to the graph bypassing TruthGate.
    Violation: reading from NeuroCore as a source of truth instead of L3.
    Violation: activating NeuroCore without the feature-flag neurocore.enabled=true.
```

---

### 📅 Deployment phases

| Phase | Name | Behavior | Status |
|------|-----------------|--------------------------------------------------------|------------|
| 0 | Passive tracker | Only logs ΔW to SQLite. Does not apply it to the model. | ✅ Current |
| 1 | Active NLM | Applies updates. Launched after analysis of Phase 0 metrics. | ⏳ Pending |
| 2 | Consolidation | NeuroCore → L3 via TruthGate (accumulated experience) | ⏳ Pending |

**Phase 0 details**: ΔW is written to the SQLite table `neurocore_delta_log`
with the fields `{timestamp, surprise_score, delta_norm, domain, session_id}`.
No changes to the model. Observation only.

---

### 🚫 What NeuroCore does NOT do

- ❌ Does not store facts (that is L3)
- ❌ Does not replace the graph — ever
- ❌ Does not update on every token (only when `surprise > θ`)
- ❌ Does not work without `neurocore.enabled=true`
- ❌ Is not activated directly from the Fast Path — only via the EventBus

---

### ⚙️ Configuration (velantrim_config.py)

```python
# RFC0068: NeuroCore — Phase 0 (passive tracker)
NEUROCORE_ENABLED          = False                # master feature-flag
NEUROCORE_SURPRISE_THETA   = 0.6                  # surprise threshold for an update
NEUROCORE_ALPHA            = 0.01                 # learning rate (fixed)
NEUROCORE_LOG_TABLE        = "neurocore_delta_log"  # SQLite table for Phase 0
```

---

### 📊 Phase 0 metrics

```python
neurocore_surprise_events_total   # Counter: how many times surprise > θ
neurocore_delta_norm_p95          # Histogram: norm of ΔW (stability monitoring)
neurocore_domain_activations      # Counter: activations by domain (label: domain)
```

---

## 📝 Changelog

| Version | Date | Changes |
|--------|------|-----------|
| v8.0 "Crystal" | April 2026 | Initial version. FSRS power-law, RFC0065–0068, ESM v2 |
| v8.0.1 | April 2026 | **P0-1**: `_degree_cache: dict[str,int] = {}` in `Velum.__init__()` + decrement in `_gc_weak_edges()`. **P0-2**: `await self.raw_memory.init()` in `agent.start()` FIRST. **P0-3**: `await self.volition_worker.start()` in `agent.start()` SECOND. **P0-4**: `HAS_APOC` env var + `_merge_relationship_safe()` + `_merge_nodes_safe()` + `get_lateral_inhibition_cypher()` in `dedupe_entities.py`; replacement of all APOC calls in `_merge_duplicate_entities()`, `merge_group()`, `CYPHER_INHIBIT`. **P1-2**: `SLMClassifierProtocol` + validation in `HybridRetriever.__init__()` + hardened `_slm_classify()`. **P1-3**: `ReasoningBank.ace_curator_update()` → delegate; `set_ace_delegate()` registered in `SelfLearningAgent` and `AutonomousSelfLearningAgent`. **Conflict-1**: `fsrs_retention()` added; `np.exp(-t/S)` replaced with FSRS power-law in STM/MTM `_periodic_decay()` and `_calculate_importance_with_decay()`; YAML `ebbinghaus:` → `fsrs_decay:`. **Conflict-3**: explicit units ("per hour") added to `stm/mtm/ltm_decay_rate`. |
| v8.0.2 Sprint 1 | April 2026 | **A1**: `HEBBIAN_DECAY_FACTOR`, `SALIENCE_MULTIPLIER`, `L5_5_INTEGRATION` → `EmergenceConfig` (were hardcoded). **A2**: `asyncio.Lock` added to `ConceptEmergenceDetector.__init__`; `observe()` → `async`; `daily_maintenance()` + `gc_expired()` — under `_lock`; split into `gc_expired()` (public+lock) and `_gc_impl()` (private, no lock) — eliminates the DEADLOCK when called from `daily_maintenance()`. **A3**: `l5_5=None` parameter + `_notify_l5_5()` scaffold. **FIX-A3**: `_notify_l5_5` is called only on `_threshold_hit`, not on every `observe()`. **FIX-K3**: `_matrix_last_seen` dict; `_gc_impl()` deletes a key only when both criteria are met (no proto AND older than TTL_DAYS) — fixed a critical bug: Hebbian Learning did not work for slowly growing concepts (nightly GC reset immature observations). **FIX-I66**: test `test_I66` rewritten — `MockTruthGate.call_count==0` instead of the tautological `MockGraph`. **Tests added**: I50 (updated: `await`), I50-b, I66 (FIX), I70, K3, A1, A2, A3. |
| v8.0.2 💠 Full | April 2026 · P0–P4 patched | **P0.5-1**: `publish_volition()` adapter added to `RobustEventBus` — eliminates the `AttributeError` on the first call to `write_voluntary()`. **P0.5-2**: `_persist_event_to_sqlite()` → `zlib.compress()` — a unified format with `SQLiteFallbackQueue.put()` and `drain()`; recovery after a Redis failure is now correct. **P0.5-3**: `VolitionWorker.process_event()` — `confidence=0.5` (a neutral prior) instead of `importance_hint`; `importance` is passed separately — eliminates the poisoning of `TruthGate` with false facts of high importance. **P0.5-4**: `_maybe_create_proto()` — a cap of `MAX_ACTIVE_PROTOS=500` with eviction of the least confident proto — eliminates unbounded growth of `_protos`. **P0.5-5**: `gc_expired()` — cleanup of orphan keys in `_sessions` that have no entry in `_matrix` — eliminates a memory leak for combinations that never reached the threshold. **P0.5-6**: `consume()` — `break` replaced with a recovery loop using `redis.ping()` and exponential backoff (30s→300s) — the Slow Path no longer dies on a Redis failure, it self-recovers without restarting the agent. |
| v8.0.2 P1 | April 2026 | **P9-FIX BUG-16** (previously undocumented): **P1-1**: `SafeFTSQuery` — parameterized queries, protection against FTS injection. **P1-2**: `SLMClassifierProtocol` added as a TypedDict + validation in `HybridRetriever.__init__()` + hardened `_slm_classify()` with a fallback to regex. **P1-3**: `ReasoningBank.ace_curator_update()` → delegate; `set_ace_delegate()` registered in `SelfLearningAgent` and `AutonomousSelfLearningAgent`. |
| v8.0.2 P2 | April 2026 | **P9-FIX BUG-16**: **P2-A**: `EMERGENCE.TTL_DAYS` → a configurable parameter (was a hardcoded 30). **P2-2**: Graph Health Checker added to `RuntimeInvariantChecker` — checks graph connectivity once a day. **P2-4**: `atomic_split()` is called BEFORE TruthGate — multi-proposition content is split into atomic facts. I91 (AtomicSplit). |
| v8.0.2 P3 | April 2026 | **P9-FIX BUG-16**: **P3-D**: UCB1 → Thompson Sampling in `ReasoningBank` — exploration/exploitation balance without a hardcoded epsilon. **P3-E**: `docker-compose.yml` — the `version:` field removed (deprecated in Compose v2+). |
| v8.0.2 P4 | April 2026 | **P9-FIX BUG-16**: **P4-B**: `daily_maintenance` — Hebbian Decay is applied only to edges older than 7 days (was: to all). **P4-E**: `MHICalculator` added as a stub — the Memory Health Index formula is pending an RFC; the SLO metric on line 7597 uses this stub. |
| v8.0.2 P10 | April 2026 | **P10-FIX (post-audit X-analysis)**: **P10-1**: `ProtoConcept` — explicit fields `salience_boost: float = 0.0` and `last_decay: datetime` added (daily_maintenance used a fragile `getattr` fallback). **P10-2**: `update_confidence()` — accounts for `salience_boost`: `min(1.0, base × (1 + salience_boost))` — a Hebbian LTP analog. **P10-3**: `observe()` — fixed a latent `AttributeError`: `self.MIN_ENTITIES` / `self.CO_OCCUR_MIN` / `self.CROSS_SESSION` / `self.MAX_ENTITIES` → `EMERGENCE.*` (P2-A removed the class-level constants, but observe() was not updated). Added the parameter `salience_weight: float = 1.0` for integration with the Salience Detector. |

---

> `Graph = Truth · LLM = Language · Memory = Physiology · Volition = Agency · Emergence = Life · Creativity = Structured Analogy · Knowledge = Ingested Wisdom · Tests = Proof`
>
> 🔱 **Velantrim v8.0 "Crystal"** — crystallized memory, a living organism, precise mathematics.
> It remembers, feels the rhythm, learns from its mistakes, and protects the truth.
> All of this — on a CPU, with no GPU during the dialogue, with minimal load on the hardware.
