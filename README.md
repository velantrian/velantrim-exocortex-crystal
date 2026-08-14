# 🔱 Velantrim ExoCortex — Crystal

> 🌐 🇬🇧 **English** · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 [Español](./README.es.md) · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 [Русский](./README.ru.md) · 🇨🇳 [简体中文](./README.zh-CN.md) · 🇸🇦 [العربية](./README.ar.md) · 🇯🇵 [日本語](./README.ja.md) · 🇮🇳 [हिन्दी](./README.hi.md)

## 💠 Memory and evidence infrastructure that keeps retrieval separate from truth

Crystal is a **local-first, evidence-first Exo-Cortex research and implementation line** for AI systems that need durable memory, provenance, explicit epistemic boundaries and auditable decisions.

The central idea is simple: finding something relevant must never silently make it true. A Reader can discover material, compare candidates and expose structural differences, while **evidence admission, contradiction adjudication and Canon authority remain separate decisions**.

> 💬 **For a human reader:** start here and follow the diagrams. You should understand the project in a few minutes without reading CI logs or historical SHAs.
>
> 🤖 **AI / agents / automated auditors:** do not infer current project state from this human overview. Start with **[Special for AI →](./docs/ai/README.md)**.
>
> 📖 **Want the deeper human explanation?** Open **[Deep System Overview →](./docs/OVERVIEW.md)**.

`v0.3.0` · 🎯 **100% line-coverage gate** · 🧬 **Ring Zero mutation gate** · ✅ **9 permanent CI jobs** · 🐍 **pure-standard-library default runtime** · ⚖️ **AGPL-3.0**

---

## 🎯 Why Crystal exists

Many AI and RAG systems are very good at finding plausible context. That is useful, but relevance alone does not prove that two claims are identical, that a source is admissible evidence, that a contradiction is resolved, or that a statement belongs in trusted memory.

Crystal treats these as different layers:

```text
🔎 discovery       → “worth inspecting”
🧾 provenance      → “where did this come from?”
🛡️ evidence gate   → “may this support a claim?”
⚖️ adjudication    → “what does the conflict mean?”
🏛️ Canon           → “what is authorized trusted state?”
💬 presentation    → “what may be answered?”
```

The design rule is:

> **Discovery proposes what deserves inspection; authority is a separate decision path.**

---

## 🗺️ Architecture in one view

```text
📥 Source / document
       │
       ▼
📖 Reader RC-1…RC-7
source identity · structure · passes · propositions · explicit links
       │
       ▼
🔎 RC-9 lexical PRE-ADMISSION discovery
“which extracted propositions are worth inspecting together?”
       │
       ▼
🧬 RRTIC-v1 typed inspection contract
relation suspicion + structural qualifier differences
architecture contract only — no runtime provider
       │
       ▼
🧾 explicit evidence / admission boundary
       │
       ▼
🛡️ Guardian → TruthGate
       │
       ▼
🏛️ physical L3 → strict Canon projection
       │
       ▼
💬 grounded answer / bounded refusal
       │
       ▼
🧾 TRACE + Receipt
```

---

## 🌳 Project tree

```text
💠 Crystal
├── 📖 Reader
│   ├── RC-1…RC-7 bounded implemented layers
│   ├── RC-9 deterministic lexical discovery
│   └── RRTIC-v1 typed inspection contract
├── 🧾 Evidence & provenance
├── 🛡️ Guardian / TruthGate
├── 🏛️ Memory / Canon
│   ├── SQLite — ordinary active local-first
│   └── PostgreSQL/pgvector — inactive target, active=false
├── 💬 Read-only query / presentation
├── 🧪 Evaluations
│   ├── RC-9 lexical baseline
│   ├── Comparator v1 — frozen gate FAIL
│   └── NLI neutral-filter v1 — frozen gate FAIL
├── 🤖 AI documentation interface
├── ⚙ Machine-readable implementation truth
└── 🎓 Grant / public truth surfaces
```

---

## 📊 What exists today

| Area | State | What that means |
|---|---|---|
| 📖 Reader RC-1…RC-7 | ✅ **Implemented** | bounded source, structure, pass, proposition, relation, long-context and explicit cross-document layers |
| 🔎 Reader RC-9 | ✅ **Implemented** | deterministic offline BM25 PRE-ADMISSION candidate discovery |
| 🧪 Comparator v1 | 🧊 **Frozen evaluation** | semantic recall recovered; discrimination gate failed |
| 🧪 NLI neutral-filter v1 | 🧊 **Frozen evaluation** | discrimination improved; recall-safety gate failed |
| 🧬 RRTIC-v1 | 📐 **Frozen architecture contract** | typed relation suspicion + 10 qualifier dimensions; no runtime provider |
| 🏛️ SQLite | ✅ **Active local-first** | ordinary active storage/runtime path |
| 🗄 PostgreSQL/pgvector | ⛔ **Inactive** | import/equivalence target only, `active=false` |
| 🧠 Semantic/hybrid Reader runtime | ❌ **Not authorized** | no Reader FTS/ANN/vector backend, NLI runtime filter or RRTIC runtime provider |
| 🤖 Dedicated/full autonomous Reader | ❌ **Not implemented** | `dedicated_reader_core=false` |

### ⚙ Compact machine truth

```text
reader_core_rc1_skeleton               = true
reader_core_rc2_structural_map         = true
reader_core_rc3_multi_pass_mechanics   = true
reader_core_rc4_proposition_extraction = true
reader_core_rc5_relation_candidates    = true
reader_core_rc6_long_context_strategy  = true
reader_core_rc7_cross_document_links   = true
reader_rc9_lexical_candidate_discovery = true
dedicated_reader_core                  = false
semantic_hybrid_reader_runtime         = false
rrtic_runtime_authorization            = false
```

For exact current state and evidence, use [STATUS](./docs/STATUS.md), [Implementation Status](./docs/IMPLEMENTATION_STATUS.md), [TEST_REPORT](./TEST_REPORT.md) and the [implementation manifest](./docs/status/implementation-manifest.json).

---

## 🧬 RRTIC-v1 — architecture contract, not runtime

The current Reader architecture contract is **Reader Retrieval Typed Inspection Contract v1 (RRTIC-v1)**.

After RC-9, a multilingual semantic comparator recovered the measured recall gap but failed proposition-level hard-negative discrimination. A later bidirectional NLI neutral filter improved discrimination but lost useful recall. The architecture reassessment therefore identified the missing capability as a **relation-contract mismatch**, not simply “use a stronger similarity model.”

RRTIC-v1 freezes:

- **6 suspicion-only relation families** — `EQUIVALENCE_SUSPECT`, `RELATED_SUSPECT`, `CONTRADICTION_SUSPECT`, `QUALIFICATION_SUSPECT`, `TOPIC_ONLY_SUSPECT`, `UNKNOWN`;
- **10 qualifier dimensions** — entity, predicate, argument roles, polarity, modality/quantifier, temporal/version, jurisdiction, condition direction, units/thresholds, attribution/causality;
- qualifier states `MATCH | MISMATCH | UNKNOWN | NOT_APPLICABLE`.

It has **no accept/reject policy, no scalar truth score, no reranking, no model execution and no runtime authorization**. Classification from the latest frozen model-backed evaluation remains `NLI_NEUTRAL_FILTER_GATE_FAILED`.

Current signed architecture checkpoint: `76a9493b8ba64b832472ef9bfc1f1c23ebe6654e` (PR #392). Later docs-only repository commits do not redefine that architecture checkpoint.

---

## 🛡️ Authority firewall

These are architectural invariants, not wording preferences:

```text
retrieval match          != evidence
similarity               != identity
repetition               != corroboration
cross-document candidate != Canon relation
ranking                  != epistemic authority
candidate discovery      != candidate adjudication
NLI label                != proposition identity
NLI contradiction        != contradiction adjudication
RRTIC suspicion          != adjudicated relation
qualifier mismatch       != truth decision
evaluation pass          != runtime authorization
```

The retained RC-7 boundary remains **no automatic semantic matching**. Reader cross-document candidates provide no automatic entity resolution, no adjudication, and no Reader embeddings/ANN/vector runtime or vector DB.

---

## 🧠 How Crystal differs from common memory/retrieval patterns

This is an **architectural emphasis comparison, not a claim of universal superiority**.

| Approach | Primary strength | Crystal’s different emphasis |
|---|---|---|
| 📦 Classic vector RAG | retrieve relevant chunks | relevance must remain separate from evidence, identity and Canon authority |
| 🧠 Agent memory systems | preserve useful agent/user context | Crystal focuses on provenance, admission boundaries and auditable trusted-state transitions |
| 🕸️ Graph / temporal-memory systems | structured relationships and evolving context | Crystal treats discovered relations as candidates until explicit authority boundaries are satisfied |
| 💠 Crystal | evidence-first memory + Reader boundaries | local-first truth-state separation, deny-safe authority and explicit research/runtime distinction |

Named systems such as Letta/MemGPT and Graphiti solve overlapping but different problems. The deeper overview contains a dated, source-linked comparison so this README does not turn changing external products into permanent project truth.

---

## 🧪 Evidence chain — short version

```text
RC-9 lexical baseline
        ↓
Comparator v1
semantic recall recovered
hard-negative discrimination FAIL
        ↓
NLI neutral-filter v1
hard-negative leakage reduced
useful-recall safety FAIL
        ↓
architecture reassessment
RELATION-CONTRACT MISMATCH
        ↓
RRTIC-v1
contract-first / no runtime authorization
```

### ✅ Reviewer validation

**Current implemented Reader retrieval baseline:** **RC-9 deterministic lexical PRE-ADMISSION candidate discovery**. The retained frozen RC-9 control records Recall@5 `0.937500`, Precision@5 `0.187500`, MRR `0.895833`, with classification `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`.

Those metrics describe a bounded synthetic retrieval benchmark, not semantic accuracy or epistemic correctness. Detailed immutable evidence lives in [TEST_REPORT](./TEST_REPORT.md), [`eval/**`](./eval/) and the Reader architecture documents.

---

## 🚀 Quick start

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e '.[dev]'
python -m pytest -q
python scripts/eval_gate.py --out-dir eval-artifacts
```

The default runtime stays dependency-free / standard-library-first. Optional integrations expand the trust or dependency boundary and are not implied by the default setup.

---

## 🚫 What Crystal does **not** claim

Crystal does not claim:

- semantic understanding or automatic semantic equivalence / claim identity;
- automatic truth verification, corroboration or evidence admission from retrieval;
- automatic contradiction resolution or winner selection;
- semantic/hybrid/vector Reader runtime, Reader FTS, ANN/FAISS/HNSW or Reader vector DB;
- an NLI runtime filter, CrossEncoder reranker or RRTIC runtime provider;
- a completed dedicated/full autonomous Reader;
- automatic Reader parser/OCR/PDF-layout/multimodal understanding;
- active PostgreSQL runtime selection, pgvector Reader activation or automatic cutover;
- universal objective-truth detection, zero hallucinations, legal/GDPR/security certification, or “fully secure” operation;
- production-scale retrieval quality from the frozen synthetic evaluation surfaces.

NLnet remains **submitted / under review / not awarded**. Approximate **€50,000** is planning context only, not an approved budget or payment commitment.

Residual issues #155, #165 and #214 remain separate scopes and are not implemented by this documentation work.

---

## 📚 Where to read next

### 👤 Human path

1. **[Deep System Overview](./docs/OVERVIEW.md)** — concepts, visual model, examples and careful external comparison.
2. **[Architecture Overview](./docs/ARCHITECTURE_OVERVIEW.md)** — tighter technical architecture map.
3. **[Full Architecture](./docs/ARCHITECTURE.md)** — detailed contracts.
4. **[Reviewer Guide](./docs/REVIEWER_GUIDE.md)** — validation and review procedure.

### 🤖 AI / agent path

1. **[Special for AI](./docs/ai/README.md)** — exact reading order and forbidden inferences.
2. **[AI Current State](./docs/ai/CURRENT_STATE.md)** — detailed technical state/evidence snapshot.
3. **[Machine-readable implementation manifest](./docs/status/implementation-manifest.json)**.

### 🧾 Evidence / state path

- [Current Status](./docs/STATUS.md)
- [Implementation Status](./docs/IMPLEMENTATION_STATUS.md)
- [TEST_REPORT](./TEST_REPORT.md)
- [Roadmap](./ROADMAP.md)
- [Documentation Map](./docs/DOCUMENTATION_MAP.md)
- [Translation Status](./docs/TRANSLATION_STATUS.md)

---

## 🌍 Localization truth

English is the primary source language. Localized README/detail surfaces remain tied to the exact source checkpoints recorded in [Translation Status](./docs/TRANSLATION_STATUS.md); a visually useful older translation must not be mistaken for newer implementation truth.

The Spanish README is intentionally useful as a historical human-layout reference, but its recorded source checkpoint is older than the current RRTIC-era English source.

---

## 🤝 Contributing and license

Changes must preserve authority boundaries, executable tests, coverage gates and truthful public claims. See [CONTRIBUTING](./CONTRIBUTING.md), [Governance](./GOVERNANCE.md) and [Security](./SECURITY.md).

License: [AGPL-3.0](./LICENSE).
