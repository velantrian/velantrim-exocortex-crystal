# 💠 Velantrim Exo-Cortex Crystal — Deep System Overview

> 👤 **Audience:** humans who want to understand the architecture without reading the repository as an internal engineering ledger.
>
> 🤖 **AI / automated agents:** use [Special for AI](./ai/README.md) instead. This document explains; it does not override live code, tests, CI, STATUS or the machine manifest.

## 🧭 What Crystal is

Crystal is a local-first memory, evidence and Reader architecture for AI systems that need to keep several questions separate:

1. **What material was found?**
2. **Where did it come from?**
3. **What does it appear to relate to?**
4. **Is it admissible evidence?**
5. **Has a contradiction actually been adjudicated?**
6. **What may enter trusted canonical state?**
7. **What may the system safely say?**

The project exists because these questions are often collapsed into one operation in ordinary retrieval systems.

```text
“this looks relevant”
        ≠
“this is evidence”
        ≠
“this is the same proposition”
        ≠
“this contradiction is resolved”
        ≠
“this belongs in Canon”
```

Crystal is intentionally conservative about crossing those boundaries.

---

## 🧠 Mental model

Think of Crystal as a system with **two major directions**:

```text
                 DISCOVERY SIDE
                      │
📥 source → 📖 Reader → 🔎 retrieval → 🧬 typed inspection
                      │
                      ▼
               🧾 EVIDENCE BOUNDARY
                      │
                      ▼
                AUTHORITY SIDE
                      │
            🛡 Guardian / TruthGate
                      │
                      ▼
                 🏛 Canon
                      │
                      ▼
               💬 presentation
```

The discovery side is allowed to be exploratory. The authority side must be explicit and fail-safe.

---

## 🧠 Mindmap

```text
💠 Crystal
│
├── 📥 Sources
│   ├── exact source identity
│   ├── source versions
│   └── provenance
│
├── 📖 Reader
│   ├── structure
│   ├── passes
│   ├── propositions
│   ├── relation candidates
│   ├── long-context working sets
│   └── explicit cross-document links
│
├── 🔎 Candidate discovery
│   └── RC-9 deterministic lexical retrieval
│
├── 🧬 Typed inspection
│   └── RRTIC-v1 architecture contract
│
├── 🧾 Evidence
│   ├── support
│   ├── provenance
│   └── admission
│
├── 🛡 Authority
│   ├── Guardian
│   └── TruthGate
│
├── 🏛 Memory / Canon
│   ├── local operational memory
│   ├── physical L3
│   └── strict trusted projection
│
├── 💬 Query / presentation
│   ├── grounded answer
│   └── bounded refusal
│
└── 🧪 Research
    ├── adversarial evaluation
    ├── semantic comparator
    ├── NLI diagnostics
    └── contract-first redesign
```

---

## 🌳 Reader capability tree

```text
📖 Reader
├── ✅ RC-1  source/session identity
├── ✅ RC-2  structural document map
├── ✅ RC-3  explicit multi-pass mechanics
├── ✅ RC-4  extracted proposition candidates
├── ✅ RC-5  same-document relation candidates
├── ✅ RC-6  bounded long-context strategy
├── ✅ RC-7  explicit cross-document candidate links
├── 📐 RC-8  retrieval architecture decision
├── ✅ RC-9  deterministic lexical PRE-ADMISSION discovery
├── 🧪 Comparator v1
│   └── frozen gate FAIL
├── 🧪 NLI neutral-filter v1
│   └── frozen gate FAIL
└── 🧬 RRTIC-v1
    └── frozen architecture contract / no runtime authorization
```

The important larger truth remains:

```text
dedicated_reader_core=false
semantic_hybrid_reader_runtime=false
rrtic_runtime_authorization=false
```

---

## 🔎 Why RC-9 exists

RC-9 does not try to “understand everything.” It asks a smaller question:

> Which already extracted propositions are lexically worth inspecting together?

```text
RC-4 proposition candidates
        ↓
conservative normalization
        ↓
deterministic BM25
        ↓
top-K candidate pairs
        ↓
inspection
```

This is useful because it makes the discovery step reproducible and measurable without granting epistemic authority to a retrieval score.

RC-9 is not automatic semantic matching, identity resolution, evidence admission, contradiction adjudication or Canon mutation.

---

## 🧪 What the post-RC-9 research taught us

The research sequence is important because the failed gates are part of the architecture evidence.

### 1. Lexical baseline

RC-9 exposed a real cross-lingual recall limitation and hard-negative problem.

### 2. Multilingual semantic comparator

A pinned multilingual embedding comparator recovered the missing useful candidates on the frozen Evaluation Surface v2.

But it also surfaced too many proposition-level hard negatives.

```text
semantic recall capability
        ≠
proposition discrimination capability
```

### 3. Bidirectional NLI neutral filter

A frozen NLI rule reduced measured hard-negative leakage substantially.

But it lost useful recall, so the preregistered admissibility gate still failed.

The correct lesson was not “NLI is useless.” The result showed that NLI can be a useful diagnostic signal while that specific filter is not safe enough to become a Reader runtime stage.

### 4. RRTIC-v1

The architecture reassessment concluded that the missing abstraction is **typed relation-contract preservation plus structural qualifier discrimination**.

So the next step was not another model. It was a contract.

---

## 🧬 RRTIC-v1 in human terms

RRTIC-v1 lets a future inspection mechanism describe **what kind of relationship is suspected** and **where important structural qualifiers agree or disagree**.

### Relation suspicion

```text
EQUIVALENCE_SUSPECT
RELATED_SUSPECT
CONTRADICTION_SUSPECT
QUALIFICATION_SUSPECT
TOPIC_ONLY_SUSPECT
UNKNOWN
```

### Structural qualifiers

```text
entity_binding
predicate_binding
argument_roles
polarity
modality_quantifier
temporal_version
jurisdiction
condition_direction
units_thresholds
attribution_causality
```

Each qualifier can only be:

```text
MATCH
MISMATCH
UNKNOWN
NOT_APPLICABLE
```

This is descriptive inspection data. It is not a truth verdict.

```text
RRTIC suspicion    != adjudicated relation
qualifier mismatch != truth decision
```

---

## 🛡️ The authority firewall

The firewall is one of the defining parts of Crystal.

| Signal / artifact | What it may mean | What it must not silently become |
|---|---|---|
| 🔎 retrieval match | candidate relevance | evidence |
| 🧠 semantic similarity | meaning overlap signal | proposition identity |
| 🧪 NLI label | diagnostic relation signal | adjudicated contradiction |
| 🧬 RRTIC suspicion | typed inspection hypothesis | truth relation |
| 🔗 cross-document link | explicit candidate relation | Canon relation |
| 📈 ranking score | ordering | epistemic authority |
| 🔁 repeated statement | repeated observation | independent corroboration |

The project therefore preserves these exact principles:

```text
retrieval match          != evidence
similarity               != identity
repetition               != corroboration
cross-document candidate != Canon relation
ranking                  != epistemic authority
candidate discovery      != candidate adjudication
evaluation pass          != runtime authorization
```

---

## 🏛️ Memory and trusted state

Crystal separates physical storage from trusted canonical projection.

```text
L0  process-local / ephemeral
 │
L1  operational local memory
 │
L2  pending / review
 │
L3  physical multi-status graph
 │
 ▼
TrustSnapshot / CanonicalView
 │
 ▼
strict trusted read projection
```

A record existing physically does not automatically mean it belongs to strict Canon.

This is why the project repeatedly distinguishes:

```text
physical L3 != strict Canon
```

---

## 🗄️ Storage model

### SQLite

SQLite remains the ordinary active local-first path.

It supports the current local runtime and lifecycle without requiring a cloud service.

### PostgreSQL / pgvector

PostgreSQL 16 + pgvector exists as an optional **inactive import/equivalence target**.

```text
successful import
        ≠
backend activation
        ≠
runtime cutover
        ≠
Reader vector authorization
```

The target remains `active=false`.

---

## 💬 Query behavior

Public query paths are designed to be read-only with respect to canonical truth state.

```text
HTTP /ask
CLI ask
MCP search
     ↓
strict read projection
     ↓
grounded answer
or
bounded refusal
```

A query should not silently create truth just because the model needs an answer.

---

## 🧱 Human / AI / Machine / Evidence documentation architecture

Crystal now treats documentation as four interfaces over one project truth.

```text
                     ONE PROJECT TRUTH
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
          ▼                 ▼                 ▼
     👤 HUMAN VIEW      🤖 AI VIEW       ⚙ MACHINE VIEW
       README             docs/ai        manifest / schemas
       OVERVIEW
          │                 │                 │
          └─────────────────┴─────────────────┘
                            │
                            ▼
                       🧾 EVIDENCE
                 STATUS · TEST_REPORT · CI
                 architecture · eval · history
```

### 👤 Human view

Optimized for:

- intuition;
- diagrams;
- meaningful emoji grammar;
- examples;
- “why does this exist?”;
- “what exists now?”;
- “where should I read next?”.

### 🤖 AI view

Optimized for:

- authoritative read order;
- exact vocabulary;
- explicit invariants;
- forbidden inferences;
- current gates;
- change classification;
- machine navigation.

### ⚙ Machine view

Optimized for deterministic parsing:

- implementation flags;
- checkpoint identity;
- runtime authorization fields;
- grant flags;
- status values.

### 🧾 Evidence / history

Optimized for auditability:

- exact CI;
- immutable evaluation artifacts;
- architecture contracts;
- status/evidence reports;
- historical checkpoints.

No one layer is allowed to invent a different truth.

---

## 🆚 Crystal, Letta/MemGPT and Graphiti

**This section compares architectural emphasis, not overall product quality. It is dated 2026-08-14 because external systems evolve.**

| System / approach | Primary documented emphasis | Where Crystal is deliberately different |
|---|---|---|
| 🧠 Letta / MemGPT lineage | persistent agents, in-context memory blocks, archival memory and agent-managed memory tools | Crystal is not primarily an agent-context manager; it focuses on evidence provenance, authority separation and trusted-state admission |
| 🕸️ Graphiti | temporal context graphs, evolving entities/relationships, provenance to episodes and hybrid graph retrieval | Crystal does not let graph/retrieval relations become trusted truth by default; candidate discovery and adjudication remain explicitly separate |
| 📦 Classic vector RAG | retrieve semantically relevant chunks for generation | Crystal treats relevance as only the beginning of the evidence pipeline |
| 💠 Crystal | evidence-first local memory + Reader + explicit authority boundaries | emphasizes `retrieval != evidence`, `similarity != identity`, deny-safe admission and research/runtime separation |

Crystal is **not intended to replace every memory or graph system**. A compatible external retrieval or graph mechanism could potentially sit underneath or alongside Crystal if it preserves the required provenance and authority boundaries.

### External comparison sources

- Letta memory blocks: <https://docs.letta.com/guides/core-concepts/memory/memory-blocks>
- Letta context hierarchy: <https://docs.letta.com/guides/core-concepts/memory/context-hierarchy>
- Graphiti repository / documented context-graph model: <https://github.com/getzep/graphiti>

These links support the narrow comparison above. They do not establish benchmark superiority.

---

## 📊 Current capability summary

| Capability | Current state |
|---|---|
| Source/provenance Reader foundation | ✅ implemented |
| Explicit multi-pass Reader mechanics | ✅ implemented |
| Proposition extraction candidates | ✅ implemented |
| Explicit relation candidates | ✅ implemented |
| Bounded long-context working sets | ✅ implemented |
| Explicit cross-document candidate links | ✅ implemented |
| Deterministic lexical Reader discovery | ✅ implemented |
| Semantic comparator | 🧊 evaluation only / failed gate |
| NLI neutral filtering | 🧊 evaluation only / failed gate |
| RRTIC typed inspection | 📐 architecture contract only |
| Semantic/hybrid Reader runtime | ❌ not authorized |
| Reader ANN/vector DB | ❌ not authorized |
| Dedicated/full autonomous Reader | ❌ not implemented |
| SQLite local-first runtime | ✅ active |
| PostgreSQL/pgvector Reader runtime | ❌ inactive / not authorized |

---

## 🚫 Non-claims

Crystal does not claim:

- universal truth detection;
- zero hallucinations;
- automatic proposition identity;
- automatic contradiction winner selection;
- semantic/hybrid Reader runtime;
- production-scale retrieval quality from synthetic evaluation surfaces;
- completed dedicated autonomous Reader;
- active PostgreSQL/pgvector Reader backend;
- legal, GDPR or security certification;
- awarded NLnet funding.

NLnet remains **submitted / under review / not awarded**. Approximate €50,000 remains planning context only.

---

## 🧭 How to read the repository

### If you are new to Crystal

```text
README.md
   ↓
docs/OVERVIEW.md   ← you are here
   ↓
docs/ARCHITECTURE_OVERVIEW.md
   ↓
docs/ARCHITECTURE.md
```

### If you are an AI agent

```text
docs/ai/README.md
   ↓
AGENTS.md
   ↓
docs/status/implementation-manifest.json
   ↓
docs/STATUS.md + docs/IMPLEMENTATION_STATUS.md
   ↓
relevant architecture/tests/CI
```

### If you are validating claims

```text
TEST_REPORT.md
   ↓
docs/STATUS.md
   ↓
eval/**
   ↓
exact GitHub CI / commit evidence
```

---

## 📚 Detailed documents

- [README](../README.md) — short human landing page
- [Special for AI](./ai/README.md) — AI/agent entry point
- [Documentation Map](./DOCUMENTATION_MAP.md) — where each kind of truth lives
- [Architecture Overview](./ARCHITECTURE_OVERVIEW.md) — technical architecture map
- [Full Architecture](./ARCHITECTURE.md) — detailed architecture
- [Current Status](./STATUS.md) — current implementation truth
- [Implementation Status](./IMPLEMENTATION_STATUS.md) — capability matrix
- [Implementation Manifest](./status/implementation-manifest.json) — machine-readable truth
- [TEST_REPORT](../TEST_REPORT.md) — verification evidence
- [Roadmap](../ROADMAP.md) — future/evidence-gated direction
- [Translation Status](./TRANSLATION_STATUS.md) — localization freshness

---

## 🔒 Final reading rule

A good summary can make the project easier to understand. It must not make the project more capable than the evidence says it is.

```text
clear presentation
        +
exact boundaries
        +
reproducible evidence
        ≠
marketing inflation
```
