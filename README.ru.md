# 🔱 Velantrim ExoCortex — Crystal

> 🌐 🇬🇧 [English](./README.md) · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 [Español](./README.es.md) · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 **Русский**  
> 📚 [Документация на немецком](./docs/de/README.md) · [на французском](./docs/fr/README.md) · [на испанском](./docs/es/README.md) · [на итальянском](./docs/it/README.md) · [на русском](./docs/ru/README.md)

### *Проверяемая, локальная и открытая инфраструктура памяти для надёжного ИИ*

`v0.3.0` · 🧪 **1713 тестов пройдено / 12 пропущено** · 🎯 **100% покрытия** · 🐍 **стандартный runtime только на стандартной библиотеке** · ⚖️ **AGPL-3.0** · 🔒 **local-first**

> Crystal — это проверяемый слой памяти, а не ещё один чат-бот. Каждый claim
> сохраняет источник, эпистемический статус и метаданные происхождения.
> Автоматический допуск в канонический граф по-прежнему контролируется
> **Guardian + TruthGate**.

> **Нормативный источник:** код, слитый в GitHub `main`, и англоязычные документы
> определяют состояние реализации и границы гранта. Эта русская версия —
> поддерживаемый перевод для русскоязычных reviewers, организаций и участников.
> При расхождениях действуют [README.md](./README.md),
> [docs/STATUS.md](./docs/STATUS.md) и [TEST_REPORT.md](./TEST_REPORT.md).

---

## 🧭 Crystal за одну минуту

Crystal — публичное ядро Velantrim, ориентированное на грантовую проверяемость:

- локальная оперативная память L0/L1;
- локальные backend-реализации канонического графа L3;
- контроль допуска через Guardian и TruthGate;
- `CanonicalView` для строго обоснованных ответов;
- TRACE, provenance и воспроизводимые Receipt;
- Evidence Span, очереди review и сессии импорта;
- технические механизмы удаления и ограничения обработки, релевантные GDPR;
- детерминированная оценка и quality gates в CI;
- опциональные интерфейсы FastAPI и MCP.

Crystal **не является** Titan, полным Personal ExoCortex, автономной когнитивной
операционной системой, проектом сознания или самoизменяющимся агентом.
Исследовательские идеи могут стать основой будущих RFC, но не являются текущими
возможностями runtime.

```text
GitHub Crystal main = публичная истина реализации
Notion Crystal       = синхронизированная карта стратегии и гранта
Titan / Full         = отдельное исследовательское направление
```

---

## 🛡️ Текущая граница доверия

### Путь допуска

```text
ввод / документ / событие агента
→ классификация и evidence
→ Guardian + TruthGate
→ оперативная память L0/L1
→ допущенный канонический граф L3
```

### Путь HTTP-запроса

PR #265 ввёл отдельный строгий контракт чтения для HTTP:

```text
POST /ask, GET /receipt
→ core.aio.arun()
→ core.query_pipeline.query()
→ только уже существующий Canon
→ CanonicalView
→ ответ или ограниченный отказ
```

Для этих HTTP-поверхностей вопрос не выполняет ingest в L0/L1, не переводит ESM,
не записывает факты или рёбра L3, не обрабатывает outbox, не регистрирует
эпизодические связи, не инициализирует embedding fingerprint и не изменяет
состояние адаптивной верификации.

### Явно указанные остаточные границы

- CLI-команды `ask` и `receipt` всё ещё используют исторический путь
  `core.pipeline.run()`, способный выполнять допуск;
- `core.pipeline.run()` остаётся доступным;
- MCP не предоставляет явных инструментов канонической записи, но поиск может
  инициализировать ещё не заданный embedding fingerprint.

Гарантия read-only намеренно узкая и не распространяется автоматически на все
callers. См. [read-only-query-boundary.md](./docs/architecture/read-only-query-boundary.md).

---

## 🧠 Модель памяти

| Уровень | Роль | Граница |
|---|---|---|
| **L0** | рабочий cache внутри процесса | быстрый, восстанавливаемый |
| **L1** | оперативная память SQLite/WAL | состояния, ограничения, обновления |
| **L2** | ожидающие claims и curator review | не становятся Canon автоматически |
| **L3** | канонический граф | автоматический допуск только через TruthGate |
| **TRACE / Receipt** | слой доказательств | объясняет grounding и выявляет drift |

Физический граф может содержать объекты с разными truth status. В строгом смысле
**Canon** — только проверенная, TRACE-valid и разрешённая политикой проекция, а
не любой узел в graph backend.

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
```

Базовое использование CLI:

```bash
velantrim ingest "Water boils at 100C at sea level"
velantrim ask "how does water behave"
velantrim receipt "how does water behave" > receipt.json
velantrim verify-receipt receipt.json
```

Постоянный локальный backend L3 на SQLite:

```bash
VELANTRIM_L3_BACKEND=sqlite \
VELANTRIM_L3_PATH=./data/canon.db \
velantrim ask "..."
```

Подробная инструкция: [docs/ru/QUICKSTART.md](./docs/ru/QUICKSTART.md).

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
| `POST` | `/ingest` | допуск через Guardian + TruthGate |
| `POST` | `/ask` | строго read-only запрос к Canon |
| `GET` | `/receipt?q=...` | чтение с Receipt |
| `POST` | `/verify-receipt` | replay Receipt относительно текущего состояния |
| `GET` | `/evidence/{fact_id}` | публичное представление evidence с учётом policy |

FastAPI и Uvicorn являются опциональными extras. Стандартный runtime не требует
cloud-сервиса или стороннего model provider.

### MCP

```bash
python -m core.mcp_server
```

MCP предоставляет инструменты инспекции для поиска, отчётов памяти, истории
фактов, конфликтов и проверки Receipt. Остаточная граница embedding fingerprint
остаётся применимой.

---

## 🧪 Оценка

Crystal уже включает детерминированную baseline:

- retrieval `hit@k` и MRR;
- полнота TRACE и метаданных;
- покрытие Evidence Span;
- выживаемость Receipt replay;
- precision и recall обнаружения противоречий;
- проверки корректного отказа на границах доверия;
- минимумы и потолки регрессии в CI.

Детерминированный replay из Titan рассмотрен как предшествующая техническая
работа, а не скопированный runtime Crystal. Любая будущая реализация должна
расширять существующий evaluation stack, оставаться offline и неавторитетной,
сохраняя TruthGate и границы query-path.

---

## 💶 Граница гранта

Проект подан на рассмотрение в **NLnet NGI0 Commons Fund**. Репозиторий не
утверждает, что финансирование уже предоставлено.

```text
ТЕКУЩАЯ BASELINE
    +
ИЗМЕРИМЫЙ ФИНАНСИРУЕМЫЙ DELTA
    =
НЕЗАВИСИМО ПРОВЕРЯЕМЫЙ DELIVERABLE
```

Уже слитая работа остаётся baseline и не учитывается повторно как оплачиваемая
поставка. Когнитивные, нейроморфные или Titan-механизмы не добавляются скрытно в
границы Crystal.

Русское резюме: [docs/ru/GRANT_OVERVIEW.md](./docs/ru/GRANT_OVERVIEW.md)  
Нормативные источники:

- [docs/GRANT_NLNET_SCOPE.md](./docs/GRANT_NLNET_SCOPE.md)
- [docs/grants/baseline-funded-delta-matrix.md](./docs/grants/baseline-funded-delta-matrix.md)
- [docs/grants/funding-use-plan.md](./docs/grants/funding-use-plan.md)
- [docs/grants/evaluation-replay-adoption.md](./docs/grants/evaluation-replay-adoption.md)

---

## ✅ Проверочные gates

| Gate | Назначение |
|---|---|
| pytest + coverage | полный набор тестов с обязательным порогом 100% |
| Ruff | lint production-кода и инструментов репозитория |
| Gitleaks | обнаружение закоммиченных secrets |
| Bandit | статический security-анализ Python |
| pip-audit | аудит уязвимостей зависимостей |
| Docker build | воспроизводимая сборка hardened-образа |
| eval-gate | контроль регрессий retrieval, grounding и противоречий |
| JSONL integrity | структура corpus и дублирующиеся идентификаторы |

Эти проверки снижают риск, но не доказывают отсутствие всех дефектов и не
являются юридической или security-сертификацией.

---

## 📚 Путь reviewer на русском

1. [docs/ru/REVIEWER_GUIDE.md](./docs/ru/REVIEWER_GUIDE.md)
2. [docs/ru/QUICKSTART.md](./docs/ru/QUICKSTART.md)
3. [docs/ru/STATUS.md](./docs/ru/STATUS.md)
4. [docs/ru/GRANT_OVERVIEW.md](./docs/ru/GRANT_OVERVIEW.md)
5. [docs/ru/GLOSSARY.md](./docs/ru/GLOSSARY.md)
6. [TEST_REPORT.md](./TEST_REPORT.md) — нормативные результаты
7. [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md) — нормативная архитектура

---

## ⚖️ Лицензия и участие

Crystal распространяется по лицензии **AGPL-3.0**. См. [LICENSE](./LICENSE),
[CONTRIBUTING.md](./CONTRIBUTING.md), [GOVERNANCE.md](./GOVERNANCE.md),
[SECURITY.md](./SECURITY.md) и [PRIVACY.md](./PRIVACY.md).

> **📊 Canon = допущенная истина** · **🔗 Provenance = доверие** · **🏠 Local-first = контроль**

---

> 🌐 🇬🇧 [English](./README.md) · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 [Español](./README.es.md) · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 **Русский**