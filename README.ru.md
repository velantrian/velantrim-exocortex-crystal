# 🔱 Velantrim ExoCortex — Crystal

> 🌐 🇬🇧 [English](./README.md) · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 [Español](./README.es.md) · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 **Русский** · 🇨🇳 [简体中文](./README.zh-CN.md) · 🇸🇦 [العربية](./README.ar.md) · 🇯🇵 [日本語](./README.ja.md) · 🇮🇳 [हिन्दी](./README.hi.md)

<!-- localization-source: main@166fab5551c4b86ee0a546b2e1d3dc7adc240c86 -->
<!-- localization-status: CURRENT -->

### Проверяемая local-first инфраструктура памяти, доказательств и решений для надёжных ИИ-систем

`v0.3.0` · 🧪 **2078 passed / 13 skipped / 0 failed** · 🎯 **9756 statements / 100.00% line coverage** · 🧬 **7/7 Ring Zero mutants killed** · ✅ **9 CI jobs** · 🐍 stdlib-only default runtime · ⚖️ **AGPL-3.0**

> Crystal — не чат-бот и не автономный «оракул истины». Это инфраструктура памяти, evidence и decision boundaries: она фиксирует происхождение утверждения, его эпистемическое состояние, допустимость для grounding и явные audited решения по противоречиям.

**Проверенный runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6` — PR #337.  
**Reader foundation:** RC-1 evidence-linked skeleton, RC-2 caller-supplied Structural Document Map, RC-3 explicit deterministic multi-pass mechanics и RC-4 source-linked proposition extraction являются bounded реализованными/протестированными слоями; dedicated/full autonomous Semantic Reading runtime остаётся не реализован.  
**Grant:** `submitted / under review / not awarded`.  
**Evidence:** [TEST_REPORT.md](./TEST_REPORT.md), [STATUS.md](./docs/STATUS.md), [implementation manifest](./docs/status/implementation-manifest.json).

> Английская версия остаётся первичным source/conflict resolver. Эта версия — полная публичная поверхность, а не краткое резюме. См. [docs/LOCALIZATION_POLICY.md](./docs/LOCALIZATION_POLICY.md) и [docs/TRANSLATION_STATUS.md](./docs/TRANSLATION_STATUS.md).

---

## 🎯 Зачем нужен Crystal

Обычные AI/RAG-системы часто смешивают документы, слова пользователя, model output, hypotheses и memory. Тогда убедительный текст может получить authority без достаточного evidence. Crystal делает границы явными:

```text
fluent claim          != trusted fact
physical L3           != strict Canon
retrieval score       != evidence
model output          != independent source truth
migration receipt     != claim evidence
import success        != backend activation
Reader coverage       != comprehension proof
Reader structure      != truth/confidence authority
Reader pass complete  != comprehension proof
EXTRACTED_PROPOSITION != verified fact
Reader candidate      != admitted evidence
```

## 🧠 Что уже предоставляет Crystal

- typed claims и явный epistemic lifecycle;
- source identity, evidence spans и provenance;
- RC-1: source/version/session, SegmentCard, fidelity, coverage, bookmarks/open loops, stale/failure/privacy semantics;
- RC-2: version-bound caller-supplied structural hierarchy/order с `RECOVERED` / `AMBIGUOUS` / `UNSUPPORTED`;
- RC-3: explicit deterministic multi-pass mechanics над declared structural targets;
- RC-4: source-linked `EXTRACTED_PROPOSITION` candidates с explicit attribution/category/negation/qualifiers;
- Guardian и TruthGate как admission boundaries;
- multi-status physical L3 отдельно от strict Canon;
- immutable deny-dominant TrustSnapshot и CanonicalView;
- read-only HTTP /ask, CLI ask и MCP search;
- TRACE и replayable tamper-evident Receipts;
- review queue/session и typed ContradictionReport;
- явные COEXIST / CONTEXTUALIZE / SUPERSEDE решения;
- scoped curator capabilities и process-local leases;
- verified SQLite lifecycle и bounded logical migration;
- optional PostgreSQL/pgvector inactive import с `active=false`.

RC-3 поддерживает пять явно объявляемых pass types:

```text
ORIENTATION
BROAD_READ
FOCUSED_READ
CROSS_CHECK
TARGETED_REREAD
```

Каждый pass заранее объявляет RC-2 structural targets и хранит audit-state:

```text
ATTEMPTED
COMPLETED
INTERRUPTED
DEGRADED
```

Один pass активен за раз. Completion разрешён только после explicit outcome для каждого declared target. Partial outcomes не исчезают при interruption/degradation. `CROSS_CHECK` и `TARGETED_REREAD` требуют prior substantive processing; targeted re-read требует explicit rationale. `AMBIGUOUS` / `UNSUPPORTED` structure не может молча считаться прочитанной и остаётся fail-visible через `NEEDS_REVIEW`.

RC-4 создаёт candidate только из target `COMPLETED` RC-3 pass, если recorded outcome и текущий matching coverage равны `PROCESSED` или `REVISITED`. Candidate остаётся `SegmentCard` с fidelity `EXTRACTED_PROPOSITION`, exact primary/supporting locators, `source_owner`, source-presentation category, explicit negation и qualifiers.

RC-4 различает `FACTUAL_ASSERTION`, `AUTHOR_OPINION`, `HYPOTHESIS`, `CONDITIONAL`, `EXAMPLE`, `QUOTED_SPEECH`, `REPORTED_POSITION`, `DEFINITION` и `UNCERTAIN_ASSERTION`. Это категории подачи источника, а не truth verdict. `FACTUAL_ASSERTION` означает лишь, что источник подаёт proposition как фактическую; Crystal не подтверждает её автоматически.

RC-4 не является automatic NLP/model extraction. Он не вызывает `core.evidence.attach_evidence()`, не пишет fact `evidence_spans`, не устанавливает evidence sufficiency и не выполняет TruthGate admission.

RC-1/RC-2/RC-3/RC-4 не хранят source body, не добавляют Reader API/CLI/worker или durable Reader schema и не имеют Canon/ESM/planner authority. Нет automatic parser/OCR, automatic NLP/LLM/provider Reader agent, embeddings/ANN/vector DB или automatic cross-document reasoning runtime. Telemetry — только counts/state, а не comprehension/truth/confidence score.

## 🏛️ Архитектура в трёх представлениях

### 🧠 Mind map

```text
🧠 Crystal
├── 📖 Reader foundation
│   ├── RC-1 evidence-linked skeleton
│   ├── RC-2 Structural Document Map
│   ├── RC-3 explicit multi-pass mechanics
│   ├── RC-4 source-linked proposition extraction
│   └── dedicated/full autonomous Reader — NOT IMPLEMENTED
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
RC-3 explicit pass ledger + coverage effects
      ↓
RC-4 source-linked EXTRACTED_PROPOSITION candidates
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

Reader RC-1/RC-2/RC-3/RC-4 остаются upstream normal admission path. Pass completion и proposition extraction не переводят observation/candidate в verified fact и не создают admission.

### 🌳 Module tree

```text
🌳 core
├── reader_core.py        # RC-1 source/session artifacts
├── reader_structure.py   # RC-2 Structural Document Map
├── reader_passes.py      # RC-3 explicit multi-pass mechanics
├── reader_extraction.py  # RC-4 source-linked proposition candidates
├── evidence.py           # source/evidence semantics
├── truth_gate.py         # admission policy
├── pipeline.py           # Guardian path
├── query_pipeline.py     # read-only public query
└── storage/...           # local-first/storage lifecycle
```

## 🧱 Поверхности памяти и authority

| Поверхность | Роль | Критическая граница |
|---|---|---|
| Reader RC-1 | source-linked artifacts | observation/candidate ≠ truth |
| Reader RC-2 | structural map | structure/order ≠ authority |
| Reader RC-3 | explicit pass ledger | pass completion ≠ comprehension/truth |
| Reader RC-4 | source-linked extracted proposition candidates | source presentation/candidate state ≠ verified fact/admitted evidence |
| L0 | working cache | ephemeral |
| L1 | operational state | durable, но не весь strict Canon |
| L2 | review/pending | ожидание решения |
| L3 | physical graph | multi-status storage |
| TrustSnapshot | reconciliation | deny-dominant |
| CanonicalView | grounding projection | policy-allowed only |
| TRACE / Receipt | audit/replay | evidence, не truth generator |
| ContradictionReport | conflict object | не выбирает winner сам |

## 🔐 Authority firewall Reader RC-4

```text
Reader artifact       != admitted fact
Reader coverage       != comprehension proof
Reader structure      != epistemic authority
Reader pass complete  != comprehension proof
Reader pass complete  != TruthGate admission
EXTRACTED_PROPOSITION != verified fact
Reader candidate      != admitted evidence
source locator        != evidence sufficiency
importance            != truth
repetition            != corroboration
```

RC-3 не вызывает model/provider и не может выбирать собственную objective, создавать undeclared target, писать strict Canon, менять `truth_status`/ESM, обходить Guardian/TruthGate, разрешать `ContradictionReport` или становиться planner/belief-update authority.

RC-4 дополнительно не может прикреплять evidence к fact, превращать `FACTUAL_ASSERTION` в verification, схлопывать quotation/opinion/hypothesis/conditional в unqualified world fact или считать количество candidates доказательством понимания/истины.

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
| Явный multi-pass audit | обычно application-specific | RC-3 deterministic pass ledger |
| Сохранить attribution/qualifiers до admission | application-specific | RC-4 explicit proposition metadata |
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

RC-3 может использовать `CROSS_CHECK` как процесс чтения, а RC-4 может сохранять contradiction-relevant proposition candidates, но ни один слой не может выбрать winner или изменить contradiction disposition.

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
reader_core_rc3_multi_pass_mechanics = true
reader_core_rc4_proposition_extraction = true
dedicated_reader_core = false
PostgreSQL target: active=false
```

Числовой test/runtime block выше — сохранённый checkpoint PR #337. RC-1/RC-2/RC-3/RC-4 имеют собственные exact-head/post-merge CI evidence и не должны притворяться частью старого числового checkpoint.

## 🚧 Что Crystal не заявляет

Crystal не заявляет universal truth, zero hallucinations, AGI/consciousness, legal/GDPR/security certification, production multi-tenancy, distributed exactly-once coordination, active PostgreSQL runtime, automatic switching/cutover/rollback/dual-write, automatic Reader parsing/OCR, automatic NLP/LLM proposition extraction, autonomous provider-driven reading, embeddings/ANN/vector Reader stack, automatic cross-document reasoning, что RC-4 candidates являются verified facts/admitted evidence, или completed dedicated/full autonomous Reader Core.

NLnet остаётся **submitted / under review / not awarded**; около €50,000 — planning only, budget change none. RC-0/RC-1/RC-2/RC-3 и RC-4, если он merged pre-agreement, являются existing baseline, а не будущим funded delta.

## 🌍 Состояние переводов после RC-4

Русский root README и Reader-dependent D1/D3/D4/D5 pack обновлены к source checkpoint RC-4 `main@166fab5551c4b86ee0a546b2e1d3dc7adc240c86` и имеют `CURRENT`. D2 и Quick Start остаются `CURRENT` на всех девяти локалях, потому что RC-4 не меняет их semantics. Восемь других root README и Reader-dependent detail pack сохраняют полный прежний текст, но требуют RC-4 semantic refresh и отмечены центральным ledger как `REFRESH_NEEDED`. Тот же набор translation debt остаётся равен 64 documents.

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