# 🔱 Velantrim ExoCortex — Crystal

> 🌐 🇬🇧 [English](./README.md) · 🇩🇪 **Deutsch** · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 [Español](./README.es.md) · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 [Русский](./README.ru.md) · 🇨🇳 [简体中文](./README.zh-CN.md) · 🇸🇦 [العربية](./README.ar.md) · 🇯🇵 [日本語](./README.ja.md) · 🇮🇳 [हिन्दी](./README.hi.md)

<!-- localization-source: main@6b45bdd196eb42dea7bc30f58d69799b4b1712f2 -->
<!-- localization-status: CURRENT -->

### Verifizierbare, local-first Infrastruktur für Gedächtnis, Evidenz und Entscheidungen in vertrauenswürdigen KI-Systemen

`v0.3.0` · 🧪 **2078 passed / 13 skipped / 0 failed** · 🎯 **9756 statements / 100.00% line coverage** · 🧬 **7/7 Ring Zero mutants killed** · ✅ **9 CI jobs** · 🐍 stdlib-only default runtime · ⚖️ **AGPL-3.0**

> Crystal ist kein Chatbot und kein autonomes Wahrheitsorakel. Es ist eine Memory-, Evidence- und Decision-Boundary, die Herkunft, epistemischen Zustand, Grounding-Berechtigung und explizit auditierte Konfliktentscheidungen festhält.

**Verified runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6` — PR #337.  
**Reader foundation:** RC-1 evidence-linked Skeleton und RC-2 caller-supplied Structural Document Map sind implementiert/getestet; der dedicated multi-pass Reader ist nicht implementiert.  
**Grant:** `submitted / under review / not awarded`.  
**Evidence:** [TEST_REPORT.md](./TEST_REPORT.md), [STATUS.md](./docs/STATUS.md), [implementation manifest](./docs/status/implementation-manifest.json).

> Englisch ist die primäre Quelle und entscheidet Konflikte. Diese Datei ist eine vollständige öffentliche Darstellung, keine Kurzorientierung. Siehe [docs/LOCALIZATION_POLICY.md](./docs/LOCALIZATION_POLICY.md) und [docs/TRANSLATION_STATUS.md](./docs/TRANSLATION_STATUS.md).

---

## 🎯 Warum Crystal existiert

Viele AI/RAG-Systeme vermischen Quellen, Benutzerbehauptungen, model output, Hypothesen und Memory. Dadurch kann flüssiger Text Autorität erhalten, die seine Evidenz nicht trägt.

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

## 🧠 Was Crystal bereitstellt

- typed claims und expliziten epistemic lifecycle;
- Source identity, evidence spans und provenance;
- Guardian und TruthGate als Admission-Boundaries;
- physical L3 als Multi-Status-Speicher getrennt von strict Canon;
- TrustSnapshot und CanonicalView mit deny-dominant Reconciliation;
- read-only HTTP /ask, CLI ask und MCP search;
- TRACE und replayable tamper-evident Receipts;
- Review Queue/Session und ContradictionReport;
- COEXIST / CONTEXTUALIZE / SUPERSEDE als explizite Entscheidungen;
- scoped curator capabilities und process-local leases;
- SQLite lifecycle und bounded logical migration;
- optionalen PostgreSQL/pgvector Import mit `active=false`;
- RC-1 Source/Version/Session, SegmentCard, Fidelity, Coverage, Bookmarks/Open Loops, stale/failure/privacy semantics;
- RC-2 version-bound caller-supplied Struktur mit RECOVERED / AMBIGUOUS / UNSUPPORTED.

RC-1/RC-2 speichern keinen Source Body und besitzen keine Canon/ESM/Planner-Autorität. Sie bringen keine Reader API/CLI/Worker, kein durable Reader schema, keinen automatic parser/OCR, keine LLM/provider Reader orchestration und keinen embeddings/ANN/vector DB oder multi-pass/cross-document Runtime mit.

## 🏛️ Architektur in drei Ansichten

### 🧠 Mind Map

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

### 🏗️ Informationsfluss

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

### 🌳 Modulbaum

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

## 🧱 Memory- und Authority-Oberflächen

| Oberfläche | Rolle | Grenze |
|---|---|---|
| Reader RC-1 | source-linked artifacts | candidate ≠ truth |
| Reader RC-2 | structural map | order ≠ authority |
| L0 | Working Cache | ephemeral |
| L1 | Operational State | durable |
| L2 | Review/Pending | keine automatische Aufnahme |
| L3 | Physical Graph | multi-status |
| TrustSnapshot | Reconciliation | deny-dominant |
| CanonicalView | Grounding | policy-allowed only |
| TRACE / Receipt | Audit/Replay | evidence, kein truth generator |
| ContradictionReport | Konfliktobjekt | kein automatischer winner |

## 🗄️ SQLite und PostgreSQL/pgvector

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

Import-Erfolg bedeutet nicht activation, cutover, rollback, dual-write, automatic switching, ANN acceptance oder TruthGate admission. Ein normaler PostgreSQL runtime adapter ist nicht aktiv.

## 🔎 Crystal vs. klassisches RAG

| Frage | Classic RAG | Crystal |
|---|---|---|
| Relevantes Material finden | Kernstärke | über Adapter |
| Claim vs trusted fact | app-spezifisch | typed boundary |
| Provenance | oft partiell | first-class |
| Reader structure/coverage | chunk-centric | RC-1/RC-2 foundation |
| Model self-source verhindern | nicht inherent | Ring Zero |
| Konflikte | externe Logik | explicit dispositions |
| Evidence replay | optional | TRACE / Receipt |
| Pflicht-Cloud/Model | variiert | nein im default runtime |

## 🛡️ Read-only Query Boundary

```text
HTTP /ask
CLI ask
MCP search
     ↓
core.query_pipeline.query()
     ↓
strict read-only canonical projection
```

Diese Oberflächen erzeugen keine Fakten, mutieren kein ESM und schreiben nicht in L3. Explicit ingest bleibt der getrennte Write Path.

## ⚖️ Konfliktentscheidungen

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

## 🚀 Schnellstart

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
```

Optional: `pip install -e '.[postgresql]'`.

## ✅ Verifizierter Baseline

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

## 🚧 Nicht-Behauptungen

Crystal behauptet keine universal truth, zero hallucinations, AGI/consciousness, legal/GDPR/security certification, production multi-tenancy, distributed exactly-once coordination, aktive PostgreSQL runtime, automatic switching/cutover/rollback/dual-write, automatische Reader parsing, embeddings/ANN/vector Reader stack oder einen completed dedicated multi-pass Reader Core.

NLnet bleibt **submitted / under review / not awarded**; ungefähr €50,000 sind planning only, budget change none. Vor einer Vereinbarung gemergte Arbeit bleibt Baseline.

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

## 🤝 Mitwirken und Lizenz

Änderungen müssen Authority-Boundaries, Tests/Coverage und exakte Claims erhalten. Siehe [CONTRIBUTING.md](./CONTRIBUTING.md). Lizenz: [AGPL-3.0](./LICENSE).
