# 🔱 Velantrim ExoCortex — Crystal

> 🌐 🇬🇧 [English](./README.md) · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 [Español](./README.es.md) · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 **Русский** · 🇨🇳 [简体中文](./README.zh-CN.md) · 🇸🇦 [العربية](./README.ar.md) · 🇯🇵 [日本語](./README.ja.md) · 🇮🇳 [हिन्दी](./README.hi.md)

<!-- localization-source: main@e521440e9bb188d88475f17dd5bcdd161b314605 -->
<!-- localization-status: CURRENT -->

### Проверяемая local-first инфраструктура памяти, доказательств и решений для надёжных ИИ-систем

`v0.3.0` · 🧪 **2078 passed / 13 skipped / 0 failed** · 🎯 **9756 statements / 100.00% line coverage** · 🧬 **7/7 заявленных Ring Zero mutants уничтожены** · ✅ **9 CI jobs** · 🐍 **runtime по умолчанию использует только стандартную библиотеку Python** · ⚖️ **AGPL-3.0**

> Crystal — не очередной чат-бот и не самостоятельный «оракул истины». Это граница
> памяти, доказательств и решений, которая фиксирует, что представляет собой
> утверждение, откуда оно получено, в каком эпистемическом состоянии находится,
> может ли служить основанием ответа и каким явным решением было урегулировано
> противоречие.

**Проверенный runtime-checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6` — смерженный PR #337.  
**Текущая публичная документационная база:** `main@e521440e9bb188d88475f17dd5bcdd161b314605`.  
**Точные доказательства:** [TEST_REPORT.md](./TEST_REPORT.md),
[STATUS.md](./docs/STATUS.md) и
[машиночитаемый manifest реализации](./docs/status/implementation-manifest.json).

> **Контракт перевода:** этот README является полноформатным русским представлением
> проекта, а не сокращённой сводкой. Английская версия остаётся первичным рабочим
> источником и разрешает расхождения. Прогресс остальных переводов отслеживается в
> [TRANSLATION_STATUS.md](./docs/TRANSLATION_STATUS.md).

---

## 🎯 Зачем нужен Crystal

Многие ИИ-системы смешивают исходные документы, слова пользователя, выводы модели,
гипотезы, найденные фрагменты и долговременную память в одном контексте или
векторном хранилище. Тогда убедительно сформулированный текст может незаметно
получить авторитет, которого его доказательства не подтверждают.

Crystal делает границы явными:

```text
Убедительное утверждение не становится автоматически надёжным.
Узел физического графа не становится автоматически строгим Canon.
Оценка retrieval-релевантности не является доказательством.
Вывод модели не является независимым фактическим источником.
Противоречие не выбирает победителя самостоятельно.
Тематическая метка не является вердиктом об истинности.
Успешный импорт данных не означает активацию backend.
```

## 🧠 Что предоставляет Crystal

- типизированные утверждения и явный эпистемический жизненный цикл;
- сведения об источнике, evidence spans и provenance;
- границы допуска Guardian и TruthGate;
- физический многостатусный граф L3, отделённый от строгого Canon;
- неизменяемый deny-dominant `TrustSnapshot` для согласования чтения;
- публичные read-only поверхности запросов HTTP, CLI и MCP;
- TRACE и воспроизводимые tamper-evident Receipts;
- ограничения обработки, удаление, аудит и import sessions;
- очереди проверки и возобновляемые review sessions;
- типизированные неизменяемые отчёты о противоречиях;
- явные решения `COEXIST`, `CONTEXTUALIZE` и `SUPERSEDE`;
- scoped curator roles/capabilities и process-local decision leases;
- рекомендательные многометочные TopicFacet без власти над истиной;
- детерминированную оценку, 100% покрытия строк и Ring Zero mutation gate;
- проверенные SQLite backup/restore и bounded logical migration;
- опциональный PostgreSQL/pgvector inactive import с независимой exact-state equivalence.

## 🏛️ Архитектура в трёх представлениях

### 🧠 Mindmap — назначение и границы

```text
🧠 Velantrim ExoCortex — Crystal
│
├── 🎯 Назначение
│   ├── Проверяемая память для ИИ
│   ├── Local-first инфраструктура доверия
│   └── Ответы и решения, связанные с доказательствами
│
├── 🏛️ Модель памяти
│   ├── L0 — быстрый рабочий cache
│   ├── L1 — операционная память и lifecycle
│   ├── L2 — граница ожидания и проверки
│   └── L3 — физический многостатусный graph
│
├── 🛡️ Граница доверия
│   ├── Guardian — структура и safety constraints
│   ├── TruthGate — политика допуска
│   ├── TrustSnapshot — deny-dominant reconciliation
│   └── CanonicalView — строгая доверенная проекция
│
├── 📜 Доказательства и аудит
│   ├── Source identity и evidence spans
│   ├── Provenance
│   ├── TRACE
│   └── Receipt
│
├── ⚖️ Проверка и противоречия
│   ├── Review queue
│   ├── Resumable review session
│   ├── ContradictionReport
│   └── COEXIST / CONTEXTUALIZE / SUPERSEDE
│
├── 🗄️ Профили хранения
│   ├── SQLite — обычный local-first профиль
│   └── PostgreSQL/pgvector — inactive migration target
│
├── 🔐 Управление
│   ├── Scoped curator capability
│   ├── Authenticated actor binding
│   └── Process-local decision lease
│
└── 📊 Верификация
    ├── Python 3.11 / 3.12
    ├── 100% line coverage
    ├── Ring Zero mutation gate
    ├── Security и Docker gates
    └── Exact-head CI evidence
```

### 🏗️ ASCII-архитектура — движение информации

```text
┌──────────────────────────────────────────────────────────────────────┐
│               🔱 Velantrim ExoCortex — Crystal                      │
│        Память → доказательства → проверка → доверенное чтение        │
└──────────────────────────────────────────────────────────────────────┘

                         📥 Явный ingest
                                │
                                ▼
           🧾 Claim type + source + exact evidence span
                                │
                                ▼
                    🧠 Observed state в L0 / L1
                                │
                                ▼
        🛡️ Guardian ──► ⚖️ TruthGate ──► 🚧 restrictions
                                │
                  ┌─────────────┴─────────────┐
                  │                           │
                  ▼                           ▼
       ⏳ L2: ожидание / review       🏛️ Физический L3 graph
                  │                           │
                  │                           ▼
                  │                 📜 provenance / TRACE
                  └─────────────┬─────────────┘
                                │
                                ▼
                    📐 Immutable TrustSnapshot
                                │
                                ▼
                  🛡️ Guardian + CanonicalView STRICT
                                │
                   ┌────────────┴────────────┐
                   │                         │
                   ▼                         ▼
          💬 Обоснованный ответ      🚫 Ограниченный отказ
                   │
                   ▼
          🧾 Воспроизводимый Receipt

⚖️ Неразрешённое противоречие
        │
        ▼
📋 Immutable ContradictionReport
        │
        ▼
🔐 scoped principal + capability + decision lease
        │
        ▼
🧑‍⚖️ явное COEXIST / CONTEXTUALIZE / SUPERSEDE
        │
        ▼
📜 аудируемый canonical write path
```

### 🌳 Дерево модулей — кто за что отвечает

```text
🌳 Crystal
│
├── 🧠 Memory surfaces
│   ├── L0 — rebuildable working cache
│   ├── L1 — SQLite/WAL operational state
│   ├── L2 — logical review boundary
│   └── L3 — multi-status physical graph
│
├── 🛡️ Trust surfaces
│   ├── Guardian
│   ├── TruthGate
│   ├── TrustSnapshot
│   └── CanonicalView
│
├── 📜 Evidence surfaces
│   ├── Source metadata
│   ├── Evidence spans
│   ├── Provenance
│   ├── TRACE
│   └── Receipt
│
├── ⚖️ Review and contradiction
│   ├── Review queue/session
│   ├── ContradictionReport
│   └── Explicit audited disposition
│
├── 🔎 Public query
│   ├── HTTP /ask and /receipt
│   ├── CLI ask and receipt
│   └── MCP search
│
├── 🗄️ Storage portability
│   ├── SQLite backup/restore
│   ├── Canonical logical bundle
│   ├── Bounded verification
│   └── PostgreSQL inactive exact-equivalence import
│
└── 📊 Verification
    ├── Tests and coverage
    ├── Mutation gate
    ├── Security scans
    ├── Docker build
    └── Documentation/status gate
```

## 🧭 Ключевые различия

```text
Физический graph L3 ≠ строгий Canon
query ≠ ingest
confidence ≠ независимое доказательство
LLM output ≠ независимый фактический источник
contradiction detection ≠ автоматический победитель
TopicFacet relevance ≠ истинность
migration receipt ≠ claim evidence
successful import ≠ backend activation
process-local lease ≠ distributed coordination
```

TruthGate — шлюз политики допуска, а не оракул, самостоятельно знающий
объективную истину. Строгий Canon — разрешённая политикой проекция чтения,
учитывающая доказательства, статус, ESM state, форму confidence и ограничения
обработки.

## 🧱 Поверхности памяти и доказательств

| Поверхность | Назначение | Критическая граница |
|---|---|---|
| L0 | рабочий cache внутри процесса | быстрый и восстанавливаемый |
| L1 | SQLite/WAL operational memory | lifecycle, restrictions и pending work |
| L2 | логическая граница review | не становится строгим Canon автоматически |
| L3 | физическая многостатусная память | наличие записи не означает доверие |
| TrustSnapshot | immutable reconciliation | deny-dominant разрешение L1/L3 |
| CanonicalView | строгая grounding projection | только policy-allowed чтение |
| TRACE / Receipt | доказательство и replay | grounding, drift и tamper evidence |
| ContradictionReport | immutable conflict object | confidence не выбирает победителя |
| TopicFacet | навигационные metadata | не меняет truth, ESM или Canon |
| CuratorPrincipal / lease | authorization/coordination | для масштаба нужен внешний lease adapter |

## 🗄️ SQLite и PostgreSQL/pgvector

```text
SQLite
└── текущий обычный local-first storage profile
    ├── runtime reads/writes
    ├── backup/restore
    ├── lock recovery
    └── bounded canonical logical export

PostgreSQL 16 + pgvector
└── optional migration/equivalence profile
    ├── optional dependency [postgresql]
    ├── lazy driver loading
    ├── new target schema
    ├── active=false
    ├── SERIALIZABLE import
    └── independent count / byte / SHA-256 equivalence
```

PostgreSQL target отсутствует в обычной runtime composition и не может обслуживать
обычные reads/writes. Успешный импорт является операционным migration evidence,
но не означает:

- activation или automatic backend selection;
- cutover, rollback или dual-write;
- admission в TruthGate или строгий Canon;
- ANN quality acceptance;
- production multi-tenancy или distributed exactly-once guarantees.

## 🔎 Crystal и классический RAG

| Вопрос | Классический RAG | Crystal |
|---|---|---|
| Найти релевантный материал | основная сильная сторона | поддерживается retrieval adapters |
| Отличить слова пользователя от проверенного факта | зависит от приложения | явная typed boundary |
| Отслеживать lifecycle и противоречия | обычно внешняя логика | first-class states и reports |
| Не позволить generated text стать собственным источником | не гарантируется | Ring Zero admission invariant |
| Воспроизвести доказательства ответа | необязательно | TRACE и Receipt architecture |
| Ответственно разрешать противоречия | зависит от приложения | explicit authorized dispositions |
| Группировать по темам без изменения доверия | зависит от приложения | advisory TopicFacet |
| Работать без обязательного cloud/model provider | по-разному | pure-stdlib local-first baseline |

## 🛡️ Публичная read-only граница

Эти поверхности используют общий `core.query_pipeline`:

```text
HTTP /ask и /receipt
CLI ask и receipt
MCP search
```

Они не создают факты, не переводят ESM state, не записывают L3, не обслуживают
outbox, не фиксируют episodes, не инициализируют embedding fingerprint, не
сохраняют unknown candidates и не изменяют adaptive verification state.

Подробнее: [Read-Only Query Boundary](./docs/architecture/read-only-query-boundary.md).

## ⚖️ Явное разрешение противоречий

Обычный approve завершается fail-closed, пока противоречие не разрешено. Куратор
должен явно выбрать disposition и указать actor и причину.

```bash
python -m core.conflict_surfaces FACT_ID \
  --disposition COEXIST \
  --actor alice \
  --reason "утверждения описывают разные контексты" \
  --expected-report-id REPORT_ID
```

Для hosted FastAPI-приложения `POST /review/resolve-conflict` регистрируется с
authentication dependency хоста. Текущий `CuratorLeaseRegistry` предотвращает
параллельные решения только в пределах одного процесса; distributed deployment
требует внешнего lease adapter.

## 🚀 Быстрый запуск

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
```

Продолжение: [русский Quick Start](./docs/ru/QUICKSTART.md) и
[английский QUICKSTART.md](./docs/QUICKSTART.md).

## 📚 Куда читать дальше

### На русском

- [Русский индекс документации](./docs/ru/README.md)
- [Quick Start](./docs/ru/QUICKSTART.md)
- [Статус](./docs/ru/STATUS.md)
- [Руководство для reviewer](./docs/ru/REVIEWER_GUIDE.md)
- [Глоссарий](./docs/ru/GLOSSARY.md)
- [Обзор гранта](./docs/ru/GRANT_OVERVIEW.md)

### Авторитетные английские источники

- [Documentation map](./docs/DOCUMENTATION_MAP.md)
- [Current status](./docs/STATUS.md)
- [Implementation status](./docs/IMPLEMENTATION_STATUS.md)
- [Architecture](./docs/ARCHITECTURE.md)
- [Test report](./TEST_REPORT.md)
- [Evaluation](./docs/EVAL.md)
- [Failure modes](./docs/FAILURE_MODES.md)
- [NLnet grant scope](./docs/GRANT_NLNET_SCOPE.md)
- [Localization policy](./docs/LOCALIZATION_POLICY.md)
- [Translation status](./docs/TRANSLATION_STATUS.md)

## ✅ Проверенная базовая линия

```text
Runtime merge: bbd816c09dd39a02e6de6c1014438490572f40f6 (PR #337)
Python 3.11: 2078 passed / 13 skipped / 0 failed
Python 3.12: 2078 passed / 13 skipped / 0 failed
Statements:  9756
Coverage:    100.00%
Mutation:    7/7 declared Ring Zero mutants killed
CI jobs:     9/9
PostgreSQL integration: successful against PostgreSQL 16 + pgvector 0.8.2
```

## 🚧 Граница заявлений

Crystal не заявляет:

- универсальное распознавание объективной истины;
- полное отсутствие hallucinations;
- юридическую GDPR- или security-сертификацию;
- production-ready multi-tenant deployment;
- distributed locking или exactly-once orchestration;
- artificial consciousness, AGI или «живую цифровую личность»;
- active PostgreSQL runtime, automatic switching, cutover или rollback;
- готовый dedicated multi-pass Reader Core;
- возможности Titan, Full Exo-Cortex, Mentaury или Native Kernel как текущий runtime.

NLnet proposal остаётся **submitted / under review / not awarded**. Смерженная
функциональность является существующей baseline и не должна повторно выдаваться
за будущую funded delivery.

## 🌍 Переводы

Переводы выполняются поэтапно. Цель каждого поддерживаемого языка — полноценный
README с эквивалентным смысловым и визуальным покрытием, а затем постепенный
перевод Quick Start, Status, Reviewer Guide, architecture, safety и grant-документов.
Временная краткая версия не считается конечным состоянием.

См. [политику локализации](./docs/LOCALIZATION_POLICY.md) и
[реестр прогресса](./docs/TRANSLATION_STATUS.md).

## 🤝 Участие и лицензия

См. [CONTRIBUTING.md](./CONTRIBUTING.md), [SECURITY.md](./SECURITY.md),
[GOVERNANCE.md](./GOVERNANCE.md) и [AGPL-3.0](./LICENSE).
