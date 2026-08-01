# 🔱 Velantrim ExoCortex — Crystal

> 🌐 🇬🇧 [English](./README.md) · 🇷🇺 **Русский**

### Проверяемая local-first инфраструктура памяти для надёжных ИИ-систем

`v0.3.0` · 🧪 **1838 тестов пройдено / 12 пропущено** · 🎯 **100% покрытия** · 🧬 **7/7 мутаций уничтожены** · ✅ **9 CI jobs** · 🐍 **pure-stdlib runtime по умолчанию** · ⚖️ **AGPL-3.0**

> Crystal — не чат-бот, а граница памяти, доказательств и решений. Она хранит,
> что представляет собой утверждение, откуда оно получено, в каком состоянии
> находится, можно ли использовать его как строгое основание ответа и как было
> явно разрешено противоречие.

**Проверенный runtime-checkpoint:** `b10a7446dc6c88fd319161ac983263554f93107b` — PR #300.  
**Истина реализации:** код и тесты в GitHub `main`.  
**Точные доказательства:** [TEST_REPORT.md](./TEST_REPORT.md) и
[implementation manifest](./docs/status/implementation-manifest.json).

## 🎯 Какую проблему решает Crystal

Обычные ИИ-системы часто смешивают документы, слова пользователя, вывод модели,
гипотезы, найденные фрагменты и долговременную память. Из-за этого убедительный
текст может получить больше доверия, чем позволяет его источник.

```text
Красивое утверждение ≠ проверенный факт
Узел графа ≠ строгий Canon
Retrieval score ≠ доказательство
Вывод модели ≠ независимый источник
Противоречие ≠ автоматический победитель
```

## 🧠 Что реализовано

- типизированные утверждения и эпистемические состояния;
- источники, evidence spans и provenance;
- Guardian и TruthGate как границы допуска;
- физический многостатусный L3-граф отдельно от strict Canon;
- неизменяемый `TrustSnapshot` для read-time reconciliation;
- read-only HTTP, CLI и MCP query surfaces;
- TRACE и воспроизводимые Receipt;
- restriction, erasure, audit и import sessions;
- review queue и возобновляемые review sessions;
- неизменяемый `ContradictionReport`;
- явные решения `COEXIST`, `CONTEXTUALIZE`, `SUPERSEDE`;
- CLI и аутентифицируемый HTTP surface разрешения конфликтов;
- машиночитаемая ESM-спецификация из runtime-матрицы;
- deterministic eval, 100% line coverage и Ring Zero mutation gate;
- scheduled/manual история L3 benchmark.

## 🏛️ Архитектура

```text
явный ingest
→ classification + evidence
→ L0/L1 Observed
→ Guardian → TruthGate → restriction/contradiction checks
→ физический L3 multi-status graph

публичный query/search
→ read-only retrieval
→ immutable TrustSnapshot
→ Guardian + CanonicalView STRICT
→ FactsPack + TRACE
→ ответ / ограниченный отказ / Receipt

неразрешённое противоречие
→ immutable ContradictionReport
→ явное решение куратора + actor + reason
→ аудируемый canonical write path
```

## ⚖️ Разрешение противоречий

Обычный `approve()` fail-closed при конфликте. Куратор должен явно выбрать
решение и указать ответственного и причину.

```bash
python -m core.conflict_surfaces FACT_ID \
  --disposition COEXIST \
  --actor alice \
  --reason "утверждения относятся к разным контекстам" \
  --expected-report-id REPORT_ID
```

Для FastAPI доступен `POST /review/resolve-conflict`, который регистрируется с
authentication dependency приложения. Подробности:
[CONFLICT_RESOLUTION_SURFACES.md](./docs/CONFLICT_RESOLUTION_SURFACES.md).

## 🚀 Быстрый запуск

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
```

## 📚 Куда читать дальше

- [Карта документации](./docs/DOCUMENTATION_MAP.md)
- [Текущий статус](./docs/STATUS.md)
- [Статус реализации](./docs/IMPLEMENTATION_STATUS.md)
- [Архитектура](./docs/ARCHITECTURE.md)
- [Разрешение конфликтов](./docs/CONFLICT_RESOLUTION_SURFACES.md)
- [Отчёт тестирования](./TEST_REPORT.md)
- [NLnet scope](./docs/GRANT_NLNET_SCOPE.md)

## ✅ Проверенный baseline

```text
Python 3.11: 1838 passed / 12 skipped
Python 3.12: 1838 passed / 12 skipped
Statements:  7051
Coverage:    100.00%
Mutation:    7/7
CI jobs:     9
```

## 🚧 Чего Crystal не заявляет

Crystal не является универсальным детектором истины, гарантией отсутствия
галлюцинаций, юридической или security-сертификацией, готовой multi-tenant
платформой, Titan/Full Exo-Cortex или реализацией искусственного сознания.

Англоязычные code-facing документы нормативны; при расхождениях действуют
GitHub `main`, [STATUS.md](./docs/STATUS.md) и [TEST_REPORT.md](./TEST_REPORT.md).
