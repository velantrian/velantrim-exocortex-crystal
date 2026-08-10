# 🔱 Velantrim ExoCortex — Crystal

> 🌐 🇬🇧 [English](./README.md) · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 [Español](./README.es.md) · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 [Русский](./README.ru.md) · 🇨🇳 [简体中文](./README.zh-CN.md) · 🇸🇦 [العربية](./README.ar.md) · 🇯🇵 [日本語](./README.ja.md) · 🇮🇳 **हिन्दी**

<!-- localization-source: main@6b45bdd196eb42dea7bc30f58d69799b4b1712f2 -->
<!-- localization-status: CURRENT -->

### भरोसेमंद AI प्रणालियों के लिए सत्यापन योग्य local-first memory, evidence और decision infrastructure

`v0.3.0` · 🧪 **2078 passed / 13 skipped / 0 failed** · 🎯 **9756 statements / 100.00% line coverage** · 🧬 **7/7 Ring Zero mutants killed** · ✅ **9 CI jobs** · 🐍 stdlib-only default runtime · ⚖️ **AGPL-3.0**

> Crystal chatbot या autonomous “truth oracle” नहीं है। यह memory/evidence/decision boundary है जो claim की provenance, epistemic state, grounding eligibility और contradictions पर audited decisions को सुरक्षित रखता है।

**Verified runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6` — PR #337.  
**Reader foundation:** RC-1 evidence-linked skeleton और RC-2 caller-supplied Structural Document Map implemented/tested हैं; dedicated multi-pass Reader implemented नहीं है।  
**Grant:** `submitted / under review / not awarded`.  
**Evidence:** [TEST_REPORT.md](./TEST_REPORT.md), [STATUS.md](./docs/STATUS.md), [implementation manifest](./docs/status/implementation-manifest.json).

> किसी अंतर पर अंग्रेज़ी primary source है। यह पूर्ण public presentation है, short orientation नहीं। [docs/LOCALIZATION_POLICY.md](./docs/LOCALIZATION_POLICY.md) और [docs/TRANSLATION_STATUS.md](./docs/TRANSLATION_STATUS.md) देखें।

---

## 🎯 Crystal क्यों

कई AI/RAG systems documents, user statements, model output, hypotheses और memory को मिला देते हैं। तब fluent text evidence के बिना authority पा सकता है।

```text
fluent claim        != trusted fact
physical L3         != strict Canon
retrieval score     != evidence
model output        != independent source truth
migration receipt   != claim evidence
import success      != backend activation
Reader coverage     != comprehension proof
Reader structure    != truth/confidence authority
```

## 🧠 Crystal क्या देता है

- typed claims और explicit epistemic lifecycle;
- source identity, evidence spans और provenance;
- Guardian और TruthGate admission boundaries;
- strict Canon से अलग multi-status physical L3;
- deny-dominant TrustSnapshot और CanonicalView;
- read-only HTTP /ask, CLI ask और MCP search;
- TRACE और replayable tamper-evident Receipts;
- review queue/session और ContradictionReport;
- explicit COEXIST / CONTEXTUALIZE / SUPERSEDE decisions;
- scoped curator capabilities और process-local leases;
- SQLite lifecycle और bounded logical migration;
- optional PostgreSQL/pgvector inactive import, `active=false`;
- RC-1: source/version/session, SegmentCard, fidelity, coverage, bookmarks/open loops, stale/failure/privacy;
- RC-2: RECOVERED / AMBIGUOUS / UNSUPPORTED वाला version-bound caller-supplied structure.

RC-1/RC-2 source body नहीं रखते, Reader API/CLI/worker या durable Reader schema नहीं जोड़ते और Canon/ESM/planner authority नहीं रखते। automatic parser/OCR, Reader LLM/provider orchestration, embeddings/ANN/vector DB या multi-pass/cross-document runtime नहीं है।

## 🏛️ Architecture के तीन views

### 🧠 Mind map

```text
🧠 Crystal
├── 📖 Reader foundation
│   ├── RC-1 evidence-linked skeleton
│   ├── RC-2 Structural Document Map
│   └── dedicated multi-pass Reader — NOT IMPLEMENTED
├── 🏛️ Memory
│   ├── L0 — working cache
│   ├── L1 — operational SQLite/WAL
│   ├── L2 — pending/review
│   └── L3 — physical multi-status graph
├── 🛡️ Trust
│   ├── Guardian
│   ├── TruthGate
│   ├── TrustSnapshot
│   └── CanonicalView
└── 🗄️ Storage
    ├── SQLite — active local-first
    └── PostgreSQL/pgvector — inactive active=false
```

### 🏗️ Information flow

```text
Source / document
      ↓
RC-1 Reader artifacts
      ↓
RC-2 structural metadata
      ↓
explicit ingest / review
      ↓
Guardian → TruthGate
      ↓
L1 + physical L3
      ↓
TrustSnapshot → CanonicalView STRICT
      ↓
Grounded answer / bounded refusal
      ↓
TRACE + Receipt
```

### 🌳 Module tree

```text
🌳 core
├── reader_core.py       # RC-1
├── reader_structure.py  # RC-2
├── evidence.py
├── truth_gate.py
├── pipeline.py
├── query_pipeline.py
└── storage/...
```

## 🧱 Memory और authority surfaces

| Surface | Role | Boundary |
|---|---|---|
| Reader RC-1 | source-linked artifacts | candidate ≠ truth |
| Reader RC-2 | structural map | order ≠ authority |
| L0 | working cache | ephemeral |
| L1 | operational state | durable |
| L2 | review/pending | no automatic admission |
| L3 | physical graph | multi-status |
| TrustSnapshot | reconciliation | deny-dominant |
| CanonicalView | grounding | policy-allowed only |
| TRACE / Receipt | audit/replay | evidence, not truth generator |
| ContradictionReport | conflict object | no automatic winner |

## 🗄️ SQLite और PostgreSQL/pgvector

```text
SQLite
└── ordinary active local-first runtime
    ├── reads/writes
    ├── backup/restore
    └── bounded logical export

PostgreSQL 16 + pgvector
└── optional inactive target
    ├── explicit optional dependency
    ├── SERIALIZABLE import
    ├── exact target re-hash
    └── active=false
```

Import success activation, cutover, rollback, dual-write, automatic switching, ANN acceptance या TruthGate admission नहीं है। normal PostgreSQL runtime adapter active नहीं है।

## 🔎 Classic RAG बनाम Crystal

| Question | Classic RAG | Crystal |
|---|---|---|
| Relevant material | primary strength | adapters |
| Claim vs trusted fact | app-specific | typed boundary |
| Provenance | variable | first-class |
| Reader structure/coverage | chunk-centric | RC-1/RC-2 foundation |
| Model self-source रोकना | not inherent | Ring Zero |
| Contradictions | external logic | explicit dispositions |
| Evidence replay | optional | TRACE / Receipt |
| Mandatory cloud/model | varies | default runtime में नहीं |

## 🛡️ Read-only query boundary

```text
HTTP /ask
CLI ask
MCP search
     ↓
core.query_pipeline.query()
     ↓
strict read-only canonical projection
```

ये surfaces facts नहीं बनातीं, ESM mutate नहीं करतीं और L3 में नहीं लिखतीं। Explicit ingest अलग write path है।

## ⚖️ Contradiction decisions

```text
unresolved contradiction
        ↓
ContradictionReport
        ↓
scoped curator + capability + lease
        ↓
COEXIST / CONTEXTUALIZE / SUPERSEDE
        ↓
audited canonical write path
```

## 🚀 Quick start

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
```

Optional PostgreSQL: `pip install -e '.[postgresql]'`.

## ✅ Verified baseline

```text
Runtime checkpoint: bbd816c09dd39a02e6de6c1014438490572f40f6
Python 3.11/3.12: 2078 passed / 13 skipped / 0 failed
Statements: 9756
Coverage: 100.00%
CI: 9/9
Ring Zero: 7/7
reader_core_rc1_skeleton = true
reader_core_rc2_structural_map = true
dedicated_reader_core = false
PostgreSQL target: active=false
```

## 🚧 Non-claims

Crystal universal truth, zero hallucinations, AGI/consciousness, legal/GDPR/security certification, production multi-tenancy, distributed exactly-once, active PostgreSQL runtime, automatic switching/cutover/rollback/dual-write, automatic Reader parsing, embeddings/ANN/vector Reader stack या completed dedicated multi-pass Reader Core का दावा नहीं करता।

NLnet **submitted / under review / not awarded** है; लगभग €50,000 planning only है, budget change none। Agreement से पहले merged work baseline है।

## 📚 Navigation

- [Documentation map](./docs/DOCUMENTATION_MAP.md)
- [Quick Start](./docs/QUICKSTART.md)
- [Status](./docs/STATUS.md)
- [Implementation Status](./docs/IMPLEMENTATION_STATUS.md)
- [Reader architecture](./docs/architecture/READER_CORE_ARCHITECTURE.md)
- [Localization policy](./docs/LOCALIZATION_POLICY.md)
- [Translation status](./docs/TRANSLATION_STATUS.md)
- [Security](./SECURITY.md)
- [Governance](./GOVERNANCE.md)
- [Contributing](./CONTRIBUTING.md)

## 🤝 Contributing और license

Changes को authority boundaries, tests/coverage और exact claims सुरक्षित रखने चाहिए। [CONTRIBUTING.md](./CONTRIBUTING.md) देखें। License: [AGPL-3.0](./LICENSE).
