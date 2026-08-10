# 🚀 Быстрый старт — Velantrim Crystal

<!-- translation-source: docs/QUICKSTART.md@16d71e731ee658b1faa65c9ea45c0d8cca290f7c -->
<!-- translation-status: CURRENT -->

> 🌐 🇬🇧 [English](../QUICKSTART.md) · 🇩🇪 [Deutsch](../de/QUICKSTART.md) · 🇫🇷 [Français](../fr/QUICKSTART.md) · 🇪🇸 [Español](../es/QUICKSTART.md) · 🇮🇹 [Italiano](../it/QUICKSTART.md) · 🇷🇺 **Русский** · 🇨🇳 [简体中文](../zh-CN/QUICKSTART.md) · 🇸🇦 [العربية](../ar/QUICKSTART.md) · 🇯🇵 [日本語](../ja/QUICKSTART.md) · 🇮🇳 [हिन्दी](../hi/QUICKSTART.md)

Это руководство запускает локальную baseline без обязательных внешних сервисов,
явно добавляет один claim, выполняет запрос через read-only границу и проверяет Receipt.

## Требования

- Python 3.11 или 3.12;
- Git;
- локальная файловая система для репозитория и SQLite-данных.

Обычный runtime не требует LLM, внешнего embedding provider или cloud-сервиса.
Extras для разработки и полного набора тестов устанавливают дополнительные пакеты,
используемые репозиторием.

## 1. Установка

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e '.[dev]'
```

В Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

## 2. Проверка репозитория

```bash
pytest tests/ --cov=. --cov-fail-under=100
python scripts/eval_gate.py --out-dir eval-artifacts
bash scripts/ring_zero_mutation_gate.sh
bash scripts/check_docs_status.sh
```

Точный проверенный checkpoint и актуальные метрики находятся в
[TEST_REPORT.md](../../TEST_REPORT.md). Они не дублируются здесь как неизменное
требование, потому что меняются вместе с реализацией.

## 3. Выбор постоянного локального хранилища

Linux/macOS:

```bash
export VELANTRIM_L3_BACKEND=sqlite
export VELANTRIM_L3_PATH=./data/canon.db
```

PowerShell:

```powershell
$env:VELANTRIM_L3_BACKEND = "sqlite"
$env:VELANTRIM_L3_PATH = ".\data\canon.db"
```

SQLite является обычным активным local-first профилем. PostgreSQL/pgvector в
текущей baseline доступен только как явная неактивная цель импорта и проверки
эквивалентности с `active=false`; он не выбирается этим Quick Start.

## 4. Явное добавление claim

```bash
velantrim ingest "Water boils at 100C at sea level"
```

`ingest` — операция записи. Claim входит в операционное состояние и проходит
настроенный путь допуска Guardian/TruthGate. Команда не означает, что Crystal
самостоятельно доказал объективную истинность утверждения: допуск зависит от
evidence и политики.

## 5. Запрос через read-only границу

```bash
velantrim ask "how does water behave"
```

Публичный `ask` использует `core.query_pipeline.query()` и не должен:

- создавать или обновлять L0/L1 facts;
- переводить ESM;
- писать в L3;
- обрабатывать outbox;
- сохранять episode links;
- инициализировать отсутствующий embedding fingerprint;
- сохранять неизвестных кандидатов.

Если строгого canonical grounding недостаточно, ожидается ограниченный отказ.
Такой отказ — корректный результат trust boundary, а не обязательно ошибка runtime.

## 6. Создание и проверка Receipt

```bash
velantrim receipt "how does water behave" > receipt.json
velantrim verify-receipt receipt.json
```

Receipt связывает query, answer и идентификаторы использованных facts с digest
и позволяет повторно проверить citations против текущего состояния памяти. Он
обнаруживает изменение данных; опциональная HMAC-подпись требует локально
настроенного provenance key.

## 7. Опциональный API

```bash
pip install '.[api]'
velantrim-api
```

Основные routes:

| Метод | Route | Граница |
|---|---|---|
| `GET` | `/health` | liveness/readiness |
| `POST` | `/ingest` | явный admission/write path |
| `POST` | `/ask` | строгий read-only query |
| `GET` | `/receipt?q=...` | read-only query + Receipt |
| `POST` | `/verify-receipt` | replay Receipt |
| `GET` | `/evidence/{fact_id}` | policy-aware evidence view |

API использует baseline с bearer token. Это не полный production-ready
multi-tenant authorization model.

## 8. MCP-поверхность для инспекции

```bash
python -m core.mcp_server
```

MCP предоставляет read-only search, memory reports, историю facts, поиск
конфликтов и проверку Receipt. Канонического write tool в этой поверхности нет.

## Частые ошибки понимания границ

### Query — не ingestion

```text
ask / receipt / MCP search → read-only
explicit ingest            → admission-capable write path
```

### Physical L3 — не strict Canon

Физический graph node может иметь неверифицированное или неактивное состояние.
Уверенные factual answers должны опираться на строгую проекцию `CanonicalView`.

### Confidence — не независимое evidence

Высокая confidence, частое повторение или retrieval similarity сами по себе не
повышают claim до verified truth.

### Import — не activation

```text
SQLite logical bundle
→ inactive PostgreSQL import
→ exact equivalence receipt
≠ runtime backend selection
≠ ordinary PostgreSQL reads/writes
```

## Следующие документы

- [Русский README](../../README.ru.md) — обзор проекта.
- [Русский статус](./STATUS.md) — текущая проверенная baseline.
- [Статус реализации](./IMPLEMENTATION_STATUS.md) — implemented / future boundaries.
- [Карта документации](../DOCUMENTATION_MAP.md) — маршруты по аудитории.
- [Архитектура](../ARCHITECTURE.md) — нормативные trust boundaries.
- [Отчёт о тестах](../../TEST_REPORT.md) — точные evidence.
- [Security policy](../../SECURITY.md) и [threat model](../security/threat-model.md).

> При расхождении действует актуальный GitHub `main` и английский исходный
> документ, указанный в `translation-source`.
