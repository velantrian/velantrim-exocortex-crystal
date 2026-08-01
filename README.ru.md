# 🔱 Velantrim ExoCortex — Crystal

> 🌐 🇬🇧 [English](./README.md) · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 [Español](./README.es.md) · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 **Русский** · 🇨🇳 [简体中文](./README.zh-CN.md) · 🇸🇦 [العربية](./README.ar.md) · 🇯🇵 [日本語](./README.ja.md) · 🇮🇳 [हिन्दी](./README.hi.md)

### Проверяемая local-first инфраструктура памяти для надёжных ИИ-систем

`v0.3.0` · 🧪 **1780 тестов пройдено / 12 пропущено** · 🎯 **100% покрытия** · 🧬 **7/7 мутаций уничтожены** · ✅ **9 CI jobs** · 🐍 **pure-stdlib runtime по умолчанию** · ⚖️ **AGPL-3.0**

> Crystal — не очередной чат-бот. Это граница памяти и доказательств, которая
> хранит, что представляет собой утверждение, откуда оно получено, в каком
> эпистемическом состоянии находится и разрешено ли использовать его как строгое
> основание ответа.

**Проверенный runtime-checkpoint:** `916097f` — слитый PR #292.  
**Истина реализации:** код и тесты, слитые в GitHub `main`.  
**Точные доказательства:** [TEST_REPORT.md](./TEST_REPORT.md) и
[машиночитаемый implementation manifest](./docs/status/implementation-manifest.json).

> Англоязычные code-facing документы нормативны. Эта русская версия является
> поддерживаемой входной страницей; при расхождениях действуют `main`,
> [docs/STATUS.md](./docs/STATUS.md) и [TEST_REPORT.md](./TEST_REPORT.md).

---

## 🎯 Какую проблему решает Crystal

Во многих ИИ-приложениях в одном контекстном окне или векторной базе смешиваются:

- исходные документы;
- слова пользователя;
- текст, сгенерированный моделью;
- гипотезы и интерпретации;
- найденные фрагменты;
- долговременная память;
- итоговые ответы.

При таком смешивании убедительно звучащая фраза может незаметно получить больше
авторитета, чем позволяет её доказательная база. Пользовательское утверждение
может выглядеть как проверенный факт, устаревший факт — остаться активным, а ответ
модели — вернуться в память как будто он является независимым источником.

Crystal разделяет **наблюдение, допуск, хранение, поиск и grounding ответа**.

```text
Красивый текст не является доказательством.
Наличие узла в графе не делает его строгим Canon.
Высокий score не является evidence.
Вывод модели не является независимым источником.
```

---

## 🧠 Что такое Crystal

Crystal — публичное грантовое local-first ядро памяти для систем, которым нужны:

- типизированные claims и явное эпистемическое состояние;
- source и provenance metadata;
- policy-controlled допуск в графовую память;
- строгая read-проекция для factual grounding;
- TRACE и воспроизводимые Receipts;
- evidence spans и подотчётные import sessions;
- review queue и resumable review sessions;
- механизмы restriction и erasure;
- детерминированная оценка и исполняемые trust-invariants;
- опциональные интерфейсы HTTP, CLI и MCP.

### Чем Crystal не является

Crystal **не является**:

- Titan или полным Personal Exo-Cortex;
- автономной когнитивной операционной системой;
- симуляцией сознания или личности;
- универсальным детектором истины;
- гарантией отсутствия галлюцинаций;
- юридической GDPR-сертификацией;
- security-сертификацией;
- готовой multi-tenant платформой без дополнительного IAM;
- системой, обязательно зависящей от LLM, embedding provider или cloud.

Исследовательские идеи могут становиться RFC, но не являются runtime-функциями,
пока код, тесты и документация не слиты в этот репозиторий.

---

## 🏛️ Архитектура одним взглядом

```text
┌──────────────────────────────────────────────────────────┐
│ 📥 Input / документ / явный ingest                      │
└───────────────────────────┬──────────────────────────────┘
                            ▼
                 ┌────────────────────────┐
                 │ Claim classification   │
                 │ + evidence metadata    │
                 └───────────┬────────────┘
                             ▼
                 ┌────────────────────────┐
                 │ L0/L1 operational      │
                 │ state: Observed        │
                 └───────────┬────────────┘
                             ▼
                 ┌────────────────────────┐
                 │ Guardian               │
                 │ structural contract    │
                 └───────────┬────────────┘
                             ▼
                 ┌────────────────────────┐
                 │ TruthGate              │
                 │ admission policy       │
                 └───────────┬────────────┘
                             ▼
                 ┌────────────────────────┐
                 │ contradiction /        │
                 │ restriction checks     │
                 └───────────┬────────────┘
                             ▼
                 ┌────────────────────────┐
                 │ Physical L3 graph      │
                 │ multi-status memory    │
                 └───────────┬────────────┘
                             │ read-only
                             ▼
                 ┌────────────────────────┐
                 │ immutable              │
                 │ TrustSnapshot          │
                 └───────────┬────────────┘
                             ▼
                 ┌────────────────────────┐
                 │ Guardian +             │
                 │ CanonicalView STRICT   │
                 └───────────┬────────────┘
                             ▼
                 ┌────────────────────────┐
                 │ FactsPack + TRACE      │
                 │ ответ + Receipt        │
                 └────────────────────────┘
```

### Центральное различие

```text
Physical L3 graph ≠ strict Canon
```

Физический граф может содержать разные truth statuses и lifecycle states.
Строгий Canon — это разрешённая политикой проекция, удовлетворяющая требованиям
к truth status, ESM, provenance, confidence и processing restriction.

Crystal не утверждает, что вычисляет абсолютную истину. Он контролирует,
**какие claims, при каких доказательствах и ограничениях можно использовать как
доверенную память и строгое основание ответа**.

---

## 🧱 Модель памяти

| Поверхность | Роль | Важная граница |
|---|---|---|
| **L0** | рабочий cache внутри процесса | быстрый и восстанавливаемый |
| **L1** | SQLite/WAL operational memory | состояния, restrictions и pending work |
| **L2** | логическая pending/review boundary | не становится строгим Canon автоматически |
| **L3** | graph-backed multi-status memory | автоматический допуск только через policy gates |
| **CanonicalView** | строгая read-проекция | физическое membership не означает доверие |
| **TRACE / Receipt** | слой доказательств и replay | объясняет grounding и выявляет drift |

SQLite является dependency-free baseline. Доступны pluggable L3 adapters; выбор
backend не должен менять trust contract.

---

## 🛡️ Границы доверия

### Допуск выполняется явно

```text
explicit ingest
→ pending operational state
→ Guardian
→ TruthGate
→ contradiction / restriction checks
→ L3 graph admission
```

Guardian проверяет структурный контракт. TruthGate применяет admission policy.
Ни один из них не является oracle, который самостоятельно знает объективную
истинность каждого утверждения источника.

### Model output не получает factual authority автоматически

LLM или другой generator может извлекать, классифицировать, суммировать,
сравнивать и формулировать. Но он не может самостоятельно повысить собственный
вывод до `VERIFIED WORLD_FACT`.

Исторический runtime-bypass `ENABLE_TRUTH_POLICY=off` удалён. Блокировка
LLM-origin теперь является неизменяемым Ring Zero invariant.

### Public query surfaces являются read-only

Один zero-durable-mutation service используется для:

```text
HTTP /ask и /receipt
CLI ask и receipt
MCP search
        ↓
core.query_pipeline
```

Обычный вопрос или поиск не должен:

- создавать или обновлять факты L0/L1;
- переводить ESM;
- записывать L3 facts, relations, entities или mentions;
- изменять L3 outbox;
- добавлять episodic links;
- инициализировать отсутствующий embedding fingerprint;
- сохранять неизвестные retrieval candidates;
- менять adaptive verification state.

`core.pipeline.run()` остаётся явной legacy/internal admission-capable функцией.
Публичные CLI-команды запросов её больше не используют.

См. [Read-Only Query Boundary](./docs/architecture/read-only-query-boundary.md).

### Immutable read reconciliation

Содержимое L3 и deny-dominant состояние L1 сначала объединяются в frozen/slotted
`TrustSnapshot`, и лишь затем создаётся compatibility mapping для Guardian и
CanonicalView.

Это предотвращает partially mutated hybrid records и делает store disagreement
явным через content-free conflict categories.

---

## 🔎 Crystal и классический RAG

RAG и Crystal решают разные части задачи.

| Вопрос | Классический RAG | Crystal |
|---|---|---|
| Найти релевантный текст | основная сильная сторона | поддерживается retrieval adapters |
| Отличить user claim от verified fact | обычно application-specific | явная typed boundary |
| Отслеживать lifecycle и contradiction | обычно внешняя логика | first-class metadata |
| Не дать generated text стать своим источником | не встроено | Ring Zero invariant |
| Выдать replayable evidence | опционально | TRACE и Receipt |
| Соблюдать processing restriction при чтении | application-specific | обязательная read boundary |
| Работать без обязательного cloud/model provider | зависит от стека | pure-stdlib local-first baseline |

Crystal можно использовать вместе с lexical, vector или graph retrieval.
Retrieval score остаётся ranking metadata и никогда не превращается в truth,
качество evidence или authority источника.

---

## 🌍 Где можно применять Crystal

### 🤖 Память агентов и ассистентов

- разделять user-reported сведения и independently verified facts;
- сохранять source history между сессиями;
- предотвращать query-time writes и self-reinforcing memory loops;
- выдавать Receipts для важных ответов.

### 🔬 Исследовательские и evidence-workspaces

- хранить точные evidence spans;
- разделять hypotheses, interpretations и conflicts;
- проводить review перед strict use;
- отслеживать изменение источников и доказательств.

### 🏢 Внутренние knowledge systems

- строить local-first institutional memory;
- давать policy-aware retrieval инструментам и агентам;
- сохранять подотчётные review decisions;
- не допускать утечки restricted/erased данных через answer generation.

### 🧪 AI safety и evaluation

- тестировать admission boundary независимо от качества модели;
- replay provenance после изменений памяти;
- измерять retrieval и contradiction behavior детерминированно;
- запускать targeted semantic mutations против Ring Zero invariants.

Crystal является инфраструктурой, а не готовым вертикальным продуктом. Для
production нужны доменные policy, deployment controls и IAM.

---

## 🚀 Быстрый старт

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
python scripts/eval_gate.py --out-dir eval-artifacts
bash scripts/ring_zero_mutation_gate.sh
```

Базовый CLI-flow:

```bash
velantrim ingest "Water boils at 100C at sea level"
velantrim ask "how does water behave"
velantrim receipt "how does water behave" > receipt.json
velantrim verify-receipt receipt.json
```

Постоянное локальное хранилище L3:

```bash
VELANTRIM_L3_BACKEND=sqlite \
VELANTRIM_L3_PATH=./data/canon.db \
velantrim ask "..."
```

Подробнее: [русский Quick Start](./docs/ru/QUICKSTART.md).

---

## 🔌 Опциональные интерфейсы

### FastAPI

```bash
pip install '.[api]'
velantrim-api
```

| Метод | Путь | Контракт |
|---|---|---|
| `GET` | `/health` | liveness/readiness |
| `POST` | `/ingest` | явный admission через Guardian + TruthGate |
| `POST` | `/ask` | strict read-only canonical query |
| `GET` | `/receipt?q=...` | read-only query + Receipt |
| `POST` | `/verify-receipt` | replay относительно текущего состояния |
| `GET` | `/evidence/{fact_id}` | policy-aware evidence view |

### MCP

```bash
python -m core.mcp_server
```

MCP предоставляет read-only search, memory reports, fact history, conflict lookup
и Receipt verification. Canonical write tool отсутствует.

---

## 🧪 Проверочные доказательства

Checkpoint `916097f` прошёл **9 CI jobs**:

| CI job | Что проверяет |
|---|---|
| `test (3.11)` | 1780 тестов пройдено / 12 пропущено, 6484 statements, 100% coverage |
| `test (3.12)` | совместимость с тем же результатом |
| `code-quality` | Ruff |
| `security` | Gitleaks, Bandit и pip-audit |
| `docker-build` | hardened image build |
| `eval-gate` | retrieval, grounding, contradiction и refusal metrics |
| `jsonl-integrity` | структура корпуса и duplicate ids |
| `Ring Zero mutation gate` | **7/7 мутаций уничтожены** |
| `docs-status` | согласованность README/STATUS/TEST_REPORT/manifest |

Mutation gate намеренно меняет семь критических условий: thresholds TruthGate,
LLM-origin rejection, strict Canon requirements, processing restriction, ESM
allowlist, malformed-confidence handling и Receipt digest verification.

Эти проверки доказывают поведение конкретного checkpoint, но не отсутствие всех
ошибок, универсальную истину, юридическую compliance или production security.

---

## 📌 Текущий статус реализации

### Реализовано и протестировано

- единый read-only boundary для HTTP, CLI и MCP search;
- non-configurable LLM-origin invariant TruthGate;
- immutable `TrustSnapshot`;
- strict `CanonicalView`;
- TRACE и replayable Receipts;
- evidence spans, import sessions и review queue;
- resumable review sessions;
- local-first SQLite/WAL baseline и pluggable L3 adapters;
- deterministic evaluation;
- targeted Ring Zero mutation gate.

### Частично или требует hardening

- roles и multi-curator authorization;
- расширенная lifecycle-интеграция provenance chain;
- формальный contradiction decision contract;
- fixed-runner performance history;
- автоматизация translation freshness.

### Только RFC / research

- Mode Layer и Observer action policy;
- bi-temporal reasoning;
- provenance grades;
- autonomous question generation;
- advanced ontology и causal conflict resolution;
- distributed replication;
- Titan и Full Exo-Cortex integration.

Полная классификация: [Implementation Status](./docs/IMPLEMENTATION_STATUS.md).

---

## 🗺️ Карта документации

| Читатель | С чего начать |
|---|---|
| Новый пользователь | [Русский Quick Start](./docs/ru/QUICKSTART.md) |
| Инженер | [Architecture](./docs/ARCHITECTURE.md) и [ADR index](./docs/ADR.md) |
| Reviewer | [Русский Reviewer Guide](./docs/ru/REVIEWER_GUIDE.md) |
| Security reviewer | [SECURITY](./SECURITY.md) и [Threat Model](./docs/security/threat-model.md) |
| Grant reviewer | [NLnet Scope](./docs/GRANT_NLNET_SCOPE.md) и [Test Report](./TEST_REPORT.md) |
| Исследователь | [Implementation Status](./docs/IMPLEMENTATION_STATUS.md) и [Roadmap](./ROADMAP.md) |
| Все документы | [Documentation Map](./docs/DOCUMENTATION_MAP.md) |

```text
merged code and tests
→ TEST_REPORT + implementation manifest
→ STATUS + IMPLEMENTATION_STATUS
→ README и reviewer guides
→ translations
→ RFC и roadmap
```

---

## 💶 Граница гранта

Проект подан в **NLnet NGI0 Commons Fund** и находится на рассмотрении.
Репозиторий не утверждает, что финансирование уже предоставлено.

```text
ТЕКУЩАЯ BASELINE
    +
ИЗМЕРИМЫЙ FUNDED DELTA
    =
НЕЗАВИСИМО ПРОВЕРЯЕМЫЙ DELIVERABLE
```

Уже слитая работа остаётся baseline. Titan, cognitive и neuromorphic research не
добавляются скрытно в grant scope Crystal.

- [Grant Scope](./docs/GRANT_NLNET_SCOPE.md)
- [Baseline/Funded Delta Matrix](./docs/grants/baseline-funded-delta-matrix.md)
- [Funding Use Plan](./docs/grants/funding-use-plan.md)

---

## 🤝 Участие и governance

Crystal распространяется по лицензии **AGPL-3.0**.

- [CONTRIBUTING](./CONTRIBUTING.md)
- [GOVERNANCE](./GOVERNANCE.md)
- [SECURITY](./SECURITY.md)
- [PRIVACY](./PRIVACY.md)
- [CODE OF CONDUCT](./CODE_OF_CONDUCT.md)

> **📊 Canon = проверенная policy-admitted проекция**  
> **🔗 Provenance = проверяемая опора, а не автоматическая истина**  
> **🏠 Local-first = контроль над памятью и evidence**

---

> 🌐 🇬🇧 [English](./README.md) · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 [Español](./README.es.md) · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 **Русский** · 🇨🇳 [简体中文](./README.zh-CN.md) · 🇸🇦 [العربية](./README.ar.md) · 🇯🇵 [日本語](./README.ja.md) · 🇮🇳 [हिन्दी](./README.hi.md)
