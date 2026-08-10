# 🔱 Velantrim ExoCortex — Crystal

> 🌐 🇬🇧 [English](./README.md) · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 **Español** · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 [Русский](./README.ru.md) · 🇨🇳 [简体中文](./README.zh-CN.md) · 🇸🇦 [العربية](./README.ar.md) · 🇯🇵 [日本語](./README.ja.md) · 🇮🇳 [हिन्दी](./README.hi.md)

<!-- localization-source: main@6b45bdd196eb42dea7bc30f58d69799b4b1712f2 -->
<!-- localization-status: CURRENT -->

### Infraestructura local-first verificable de memoria, evidencia y decisión para sistemas de IA confiables

`v0.3.0` · 🧪 **2078 passed / 13 skipped / 0 failed** · 🎯 **9756 statements / 100.00% line coverage** · 🧬 **7/7 Ring Zero mutants killed** · ✅ **9 CI jobs** · 🐍 runtime stdlib-only por defecto · ⚖️ **AGPL-3.0**

> Crystal no es un chatbot ni un «oráculo de verdad» autónomo. Es una boundary de memoria, evidence y decisiones que conserva procedencia, estado epistémico, elegibilidad de grounding y decisiones auditadas sobre contradicciones.

**Verified runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6` — PR #337.  
**Reader foundation:** RC-1 evidence-linked skeleton y RC-2 caller-supplied Structural Document Map están implementados/probados; el Reader multi-pass dedicado no está implementado.  
**Grant:** `submitted / under review / not awarded`.  
**Evidence:** [TEST_REPORT.md](./TEST_REPORT.md), [STATUS.md](./docs/STATUS.md), [implementation manifest](./docs/status/implementation-manifest.json).

> El inglés sigue siendo la fuente primaria y resuelve discrepancias. Esta es una presentación pública completa, no un resumen reducido. Véase [docs/LOCALIZATION_POLICY.md](./docs/LOCALIZATION_POLICY.md) y [docs/TRANSLATION_STATUS.md](./docs/TRANSLATION_STATUS.md).

---

## 🎯 Por qué existe Crystal

Muchos sistemas AI/RAG mezclan documentos, afirmaciones del usuario, model output, hipótesis y memoria. Un texto fluido puede adquirir autoridad que su evidence no respalda.

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

## 🧠 Qué ofrece Crystal

- claims tipados y lifecycle epistémico explícito;
- source identity, evidence spans y provenance;
- Guardian y TruthGate como admission boundaries;
- physical L3 multi-status separado de strict Canon;
- TrustSnapshot y CanonicalView deny-dominant;
- HTTP /ask, CLI ask y MCP search read-only;
- TRACE y Receipts reproducibles y tamper-evident;
- review queue/session y ContradictionReport;
- decisiones COEXIST / CONTEXTUALIZE / SUPERSEDE;
- capacidades curator scoped y process-local leases;
- lifecycle SQLite y migración lógica acotada;
- import PostgreSQL/pgvector opcional e inactivo con `active=false`;
- RC-1: source/version/session, SegmentCard, fidelity, coverage, bookmarks/open loops, stale/failure/privacy;
- RC-2: estructura caller-supplied ligada a versión con RECOVERED / AMBIGUOUS / UNSUPPORTED.

RC-1/RC-2 no almacenan source body, no crean API/CLI/worker Reader ni schema durable Reader y no tienen autoridad Canon/ESM/planner. No hay parser/OCR automático, Reader LLM/provider orchestration, embeddings/ANN/vector DB ni runtime multi-pass/cross-document.

## 🏛️ Arquitectura en tres vistas

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

### 🏗️ Flujo de información

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

### 🌳 Árbol de módulos

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

## 🧱 Superficies de memory y authority

| Superficie | Función | Límite |
|---|---|---|
| Reader RC-1 | source-linked artifacts | candidate ≠ truth |
| Reader RC-2 | structural map | order ≠ authority |
| L0 | working cache | ephemeral |
| L1 | operational state | durable |
| L2 | review/pending | sin admisión automática |
| L3 | physical graph | multi-status |
| TrustSnapshot | reconciliation | deny-dominant |
| CanonicalView | grounding | policy-allowed only |
| TRACE / Receipt | audit/replay | evidence, no truth generator |
| ContradictionReport | conflicto | no winner automático |

## 🗄️ SQLite y PostgreSQL/pgvector

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

Un import exitoso no significa activation, cutover, rollback, dual-write, automatic switching, ANN acceptance o TruthGate admission. El runtime adapter normal de PostgreSQL no está activo.

## 🔎 Crystal frente al RAG clásico

| Pregunta | Classic RAG | Crystal |
|---|---|---|
| Encontrar material | fortaleza principal | adapters |
| Claim vs trusted fact | app-specific | typed boundary |
| Provenance | variable | first-class |
| Reader structure/coverage | chunk-centric | RC-1/RC-2 foundation |
| Evitar model self-source | no inherente | Ring Zero |
| Contradicciones | lógica externa | explicit dispositions |
| Replay evidence | optional | TRACE / Receipt |
| Cloud/model obligatorio | depende | no en default runtime |

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

Estas superficies no crean hechos, no mutan ESM ni escriben L3. Explicit ingest sigue siendo el write path separado.

## ⚖️ Decisiones de contradicción

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

## 🚀 Inicio rápido

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
```

Opcional PostgreSQL: `pip install -e '.[postgresql]'`.

## ✅ Baseline verificada

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

Crystal no afirma universal truth, zero hallucinations, AGI/consciousness, certificación legal/GDPR/security, production multi-tenancy, distributed exactly-once, runtime PostgreSQL activo, automatic switching/cutover/rollback/dual-write, parsing Reader automático, stack embeddings/ANN/vector Reader ni completed dedicated multi-pass Reader Core.

NLnet sigue **submitted / under review / not awarded**; aproximadamente €50,000 es planning only, budget change none. El trabajo merged antes del acuerdo permanece baseline.

## 📚 Navegación

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

## 🤝 Contribución y licencia

Los cambios deben conservar authority boundaries, tests/coverage y claims exactos. Véase [CONTRIBUTING.md](./CONTRIBUTING.md). Licencia: [AGPL-3.0](./LICENSE).
