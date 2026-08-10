# 🔱 Velantrim ExoCortex — Crystal

> 🌐 🇬🇧 [English](./README.md) · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 [Español](./README.es.md) · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 **Русский** · 🇨🇳 [简体中文](./README.zh-CN.md) · 🇸🇦 [العربية](./README.ar.md) · 🇯🇵 [日本語](./README.ja.md) · 🇮🇳 [हिन्दी](./README.hi.md)

<!-- localization-source: main@6b45bdd196eb42dea7bc30f58d69799b4b1712f2 -->
<!-- localization-status: CURRENT -->

### Проверяемая local-first инфраструктура памяти, доказательств и решений для надёжных ИИ-систем

`v0.3.0` · 🧪 **2078 passed / 13 skipped / 0 failed** · 🎯 **9756 statements / 100.00% line coverage** · 🧬 **7/7 Ring Zero mutants killed** · ✅ **9 CI jobs** · 🐍 stdlib-only default runtime · ⚖️ **AGPL-3.0**

> Crystal — не чат-бот и не автономный «оракул истины». Это инфраструктура памяти, evidence и decision boundaries: она фиксирует происхождение утверждения, его эпистемическое состояние, допустимость для grounding и явные audited решения по противоречиям.

**Проверенный runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6` — PR #337.  
**Reader foundation:** RC-1 evidence-linked skeleton и RC-2 caller-supplied Structural Document Map реализованы и протестированы; dedicated multi-pass Reader остаётся не реализован.  
**Grant:** `submitted / under review / not awarded`.  
**Evidence:** [TEST_REPORT.md](./TEST_REPORT.md), [STATUS.md](./docs/STATUS.md), [implementation manifest](./docs/status/implementation-manifest.json).

> Английская версия остаётся первичным source/conflict resolver. Эта версия — полная публичная поверхность, а не краткое резюме. См. [docs/LOCALIZATION_POLICY.md](./docs/LOCALIZATION_POLICY.md) и [docs/TRANSLATION_STATUS.md](./docs/TRANSLATION_STATUS.md).

---

## 🎯 Зачем нужен Crystal

Обычные AI/RAG-системы часто смешивают документы, слова пользователя, model output, hypotheses и memory. Тогда убедительный текст может получить authority без достаточного evidence. Crystal делает границы явными:

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

## 🧠 Что уже предоставляет Crystal

- typed claims и явный epistemic lifecycle;
- source identity, evidence spans и provenance;
- Guardian и TruthGate как admission boundaries;
- multi-status physical L3 отдельно от strict Canon;
- immutable deny-dominant TrustSnapshot и CanonicalView;
- read-only HTTP /ask, CLI ask и MCP search;
- TRACE и replayable tamper-evident Receipts;
- review queue/session и typed ContradictionReport;
- явные COEXIST / CONTEXTUALIZE / SUPERSEDE решения;
- scoped curator capabilities и process-local leases;
- verified SQLite lifecycle и bounded logical migration;
- optional PostgreSQL/pgvector inactive import с `active=false`;
- RC-1: source/version/session, SegmentCard, fidelity, coverage, bookmarks/open loops, stale/failure/privacy semantics;
- RC-2: version-bound caller-supplied structural hierarchy/order с RECOVERED / AMBIGUOUS / UNSUPPORTED.

RC-1/RC-2 не хранят source body, не добавляют Reader API/CLI/worker или durable Reader schema и не имеют Canon/ESM/planner authority. Нет automatic parser/OCR, LLM/provider Reader orchestration, embeddings/ANN/vector DB, multi-pass или cross-document reasoning runtime.

## 🏛️ Архитектура в трёх представлениях

### 🧠 Mind map

```text
🧠 Crystal
├── 📖 Reader foundation
│   ├── RC-1 evidence-linked skeleton
│   ├── RC-2 Structural Document Map
│   └── dedicated multi-pass Reader — NOT IMPLEMENTED
├── 🏛️ Memory
│   ├── L0 — rebuildable working cache
│   ├── L1 — operational SQLite/WAL state
│   ├── L2 — pending/review boundary
│   └── L3 — physical multi-status graph
├── 🛡️ Trust
│   ├── Guardian
│   ├── TruthGate
│   ├── TrustSnapshot
│   └── CanonicalView
├── 📜 Evidence
│   ├── Source / SourceSpan
│   ├── Provenance
│   ├── TRACE
│   └── Receipt
└── 🗄️ Storage
    ├── SQLite — ordinary active local-first
    └── PostgreSQL/pgvector — inactive active=false target
```

### 🏗️ Information flow

```text
Source / document
      ↓
RC-1 source/version + Reader artifacts
      ↓
RC-2 structural metadata
      ↓
explicit ingest / review / evidence path
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
├── evidence.py          # source/evidence semantics
├── truth_gate.py        # admission policy
├── pipeline.py          # Guardian path
├── query_pipeline.py    # read-only public query
└── storage/...          # local-first/storage lifecycle
```

## 🧱 Поверхности памяти и authority

| Поверхность | Роль | Критическая граница |
|---|---|---|
| Reader RC-1 | source-linked artifacts | observation/candidate ≠ truth |
| Reader RC-2 | structural map | structure/order ≠ authority |
| L0 | working cache | ephemeral |
| L1 | operational state | durable, но не весь strict Canon |
| L2 | review/pending | ожидание решения |
| L3 | physical graph | multi-status storage |
| TrustSnapshot | reconciliation | deny-dominant |
| CanonicalView | grounding projection | policy-allowed only |
| TRACE / Receipt | audit/replay | evidence, не truth generator |
| ContradictionReport | conflict object | не выбирает winner сам |

## 🗄️ SQLite и PostgreSQL/pgvector

```text
SQLite
└── ordinary active local-first runtime
    ├── normal reads/writes
    ├── backup/restore
    └── bounded logical export

PostgreSQL 16 + pgvector
└── optional inactive migration/equivalence target
    ├── explicit optional dependency
    ├── SERIALIZABLE import
    ├── exact target re-hash
    └── active=false
```

Успешный PostgreSQL import не означает activation, cutover, rollback, dual-write, automatic switching, ANN acceptance или TruthGate admission. Обычный runtime adapter для PostgreSQL не активирован.

## 🔎 Crystal и классический RAG

| Вопрос | Classic RAG | Crystal |
|---|---|---|
| Найти релевантный материал | основная функция | поддерживается adapter-ами |
| Разделить claim и trusted fact | application-specific | typed boundary |
| Source/version provenance | часто частично | first-class |
| Reader coverage/structure | обычно chunk-centric | RC-1/RC-2 bounded foundation |
| Prevent model self-source | не inherent | Ring Zero invariant |
| Contradiction governance | внешняя логика | explicit dispositions |
| Replay evidence | optional | TRACE / Receipt |
| Mandatory cloud/model | часто да | нет в default runtime |

## 🛡️ Public read-only query boundary

```text
HTTP /ask
CLI ask
MCP search
     ↓
core.query_pipeline.query()
     ↓
strict read-only canonical projection
```

Эти surfaces не создают факты, не меняют ESM, не пишут L3 и не запускают admission. Explicit ingest остаётся отдельным write path.

## ⚖️ Противоречия

```text
unresolved contradiction
        ↓
immutable ContradictionReport
        ↓
scoped curator + capability + lease
        ↓
COEXIST / CONTEXTUALIZE / SUPERSEDE
        ↓
audited canonical write path
```

## 🚀 Быстрый старт

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
```

Optional PostgreSQL tooling: `pip install -e '.[postgresql]'`.

## ✅ Проверенный baseline

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

## 🚧 Что Crystal не заявляет

Crystal не заявляет universal truth, zero hallucinations, AGI/consciousness, legal/GDPR/security certification, production multi-tenancy, distributed exactly-once coordination, active PostgreSQL runtime, automatic switching/cutover/rollback/dual-write, automatic Reader parsing, embeddings/ANN/vector Reader stack или completed dedicated multi-pass Reader Core.

NLnet остаётся **submitted / under review / not awarded**; около €50,000 — planning only, budget change none. Merged pre-agreement work является baseline, а не будущим funded delta.

## 📚 Навигация

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

## 🤝 Вклад и лицензия

Изменения должны сохранять authority boundaries, green tests/coverage и точные claims. См. [CONTRIBUTING.md](./CONTRIBUTING.md). Лицензия — [AGPL-3.0](./LICENSE).
