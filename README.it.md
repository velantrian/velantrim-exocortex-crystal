# 🔱 Velantrim ExoCortex — Crystal

> 🌐 🇬🇧 [English](./README.md) · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 [Español](./README.es.md) · 🇮🇹 **Italiano** · 🇷🇺 [Русский](./README.ru.md) · 🇨🇳 [简体中文](./README.zh-CN.md) · 🇸🇦 [العربية](./README.ar.md) · 🇯🇵 [日本語](./README.ja.md) · 🇮🇳 [हिन्दी](./README.hi.md)

<!-- localization-source: main@6b45bdd196eb42dea7bc30f58d69799b4b1712f2 -->
<!-- localization-status: CURRENT -->

### Infrastruttura local-first verificabile di memoria, evidenza e decisione per sistemi di IA affidabili

`v0.3.0` · 🧪 **2078 passed / 13 skipped / 0 failed** · 🎯 **9756 statements / 100.00% line coverage** · 🧬 **7/7 Ring Zero mutants killed** · ✅ **9 CI jobs** · 🐍 runtime stdlib-only predefinito · ⚖️ **AGPL-3.0**

> Crystal non è un chatbot né un oracolo autonomo di verità. È una boundary di memoria, evidence e decisione che conserva provenance, stato epistemico, idoneità al grounding e decisioni auditabili sulle contraddizioni.

**Verified runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6` — PR #337.  
**Reader foundation:** RC-1 evidence-linked skeleton e RC-2 caller-supplied Structural Document Map sono implementati/testati; il Reader multi-pass dedicato non è implementato.  
**Grant:** `submitted / under review / not awarded`.  
**Evidence:** [TEST_REPORT.md](./TEST_REPORT.md), [STATUS.md](./docs/STATUS.md), [implementation manifest](./docs/status/implementation-manifest.json).

> L’inglese resta la fonte primaria e risolve le divergenze. Questa è una presentazione pubblica completa, non un riassunto breve. Vedi [docs/LOCALIZATION_POLICY.md](./docs/LOCALIZATION_POLICY.md) e [docs/TRANSLATION_STATUS.md](./docs/TRANSLATION_STATUS.md).

---

## 🎯 Perché esiste Crystal

Molti sistemi AI/RAG mescolano documenti, dichiarazioni utente, model output, ipotesi e memoria. Un testo fluente può ottenere un’autorità non sostenuta dalla sua evidence.

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

## 🧠 Cosa fornisce Crystal

- claims tipizzati e lifecycle epistemico esplicito;
- source identity, evidence spans e provenance;
- Guardian e TruthGate come admission boundaries;
- physical L3 multi-status separato da strict Canon;
- TrustSnapshot e CanonicalView deny-dominant;
- HTTP /ask, CLI ask e MCP search read-only;
- TRACE e Receipts replayable/tamper-evident;
- review queue/session e ContradictionReport;
- decisioni COEXIST / CONTEXTUALIZE / SUPERSEDE;
- curator capabilities scoped e process-local leases;
- lifecycle SQLite e bounded logical migration;
- import PostgreSQL/pgvector opzionale e inattivo con `active=false`;
- RC-1: source/version/session, SegmentCard, fidelity, coverage, bookmarks/open loops, stale/failure/privacy;
- RC-2: struttura caller-supplied version-bound con RECOVERED / AMBIGUOUS / UNSUPPORTED.

RC-1/RC-2 non conservano source body, non aggiungono Reader API/CLI/worker o durable Reader schema e non hanno Canon/ESM/planner authority. Nessun parser/OCR automatico, Reader LLM/provider orchestration, embeddings/ANN/vector DB o runtime multi-pass/cross-document.

## 🏛️ Architettura in tre viste

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

### 🏗️ Flusso informativo

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

### 🌳 Albero dei moduli

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

## 🧱 Superfici memory e authority

| Superficie | Ruolo | Limite |
|---|---|---|
| Reader RC-1 | source-linked artifacts | candidate ≠ truth |
| Reader RC-2 | structural map | order ≠ authority |
| L0 | working cache | ephemeral |
| L1 | operational state | durable |
| L2 | review/pending | nessuna admission automatica |
| L3 | physical graph | multi-status |
| TrustSnapshot | reconciliation | deny-dominant |
| CanonicalView | grounding | policy-allowed only |
| TRACE / Receipt | audit/replay | evidence, non truth generator |
| ContradictionReport | conflitto | nessun winner automatico |

## 🗄️ SQLite e PostgreSQL/pgvector

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

Un import riuscito non implica activation, cutover, rollback, dual-write, automatic switching, ANN acceptance o TruthGate admission. Il runtime adapter PostgreSQL normale non è attivo.

## 🔎 Crystal e RAG classico

| Domanda | Classic RAG | Crystal |
|---|---|---|
| Trovare materiale | forza principale | adapters |
| Claim vs trusted fact | app-specific | typed boundary |
| Provenance | variabile | first-class |
| Reader structure/coverage | chunk-centric | RC-1/RC-2 foundation |
| Evitare model self-source | non intrinseco | Ring Zero |
| Contraddizioni | logica esterna | explicit dispositions |
| Replay evidence | optional | TRACE / Receipt |
| Cloud/model obbligatorio | variabile | no nel default runtime |

## 🛡️ Query boundary read-only

```text
HTTP /ask
CLI ask
MCP search
     ↓
core.query_pipeline.query()
     ↓
strict read-only canonical projection
```

Queste superfici non creano fatti, non mutano ESM e non scrivono L3. Explicit ingest resta il write path separato.

## ⚖️ Decisioni sulle contraddizioni

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

## 🚀 Avvio rapido

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
```

PostgreSQL opzionale: `pip install -e '.[postgresql]'`.

## ✅ Baseline verificata

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

Crystal non dichiara universal truth, zero hallucinations, AGI/consciousness, certificazione legal/GDPR/security, production multi-tenancy, distributed exactly-once, runtime PostgreSQL attivo, automatic switching/cutover/rollback/dual-write, parsing Reader automatico, stack embeddings/ANN/vector Reader o completed dedicated multi-pass Reader Core.

NLnet resta **submitted / under review / not awarded**; circa €50,000 è planning only, budget change none. Il lavoro merged prima di un accordo resta baseline.

## 📚 Navigazione

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

## 🤝 Contributi e licenza

Le modifiche devono preservare authority boundaries, tests/coverage e claims precisi. Vedi [CONTRIBUTING.md](./CONTRIBUTING.md). Licenza: [AGPL-3.0](./LICENSE).
