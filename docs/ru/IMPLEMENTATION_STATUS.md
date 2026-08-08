# 🧭 Статус реализации: Crystal и будущая работа Exo-Cortex

<!-- translation-source: docs/IMPLEMENTATION_STATUS.md@16d71e731ee658b1faa65c9ea45c0d8cca290f7c -->
<!-- translation-status: CURRENT -->

**Дата статуса:** 8 августа 2026 года  
**Проверенный runtime checkpoint:** `bbd816c` / PR #337  
**Точные evidence:** [TEST_REPORT.md](../../TEST_REPORT.md)  
**Machine-readable status:** [implementation-manifest.json](../status/implementation-manifest.json)

| Компонент | Статус | Текущая граница |
|---|---|---|
| Guardian / TruthGate / strict read projection | Реализовано | storage и migration не обходят authority |
| Read-only HTTP/CLI/MCP query boundary | Реализовано | обычные queries не изменяют Canon |
| SQLite backup/verify/inactive restore | Реализовано и протестировано | restore неактивен и не является admission |
| Bounded-streaming SQLite logical export/verify | Реализовано и протестировано | canonical backend-neutral bundle |
| PostgreSQL optional dependency и preflight | Реализовано и протестировано | explicit extra, lazy load, поддерживаемые pinned versions |
| Inactive PostgreSQL/pgvector import | Реализовано и протестировано | только новая неактивная schema; обычных reads/writes нет |
| Exact target-state equivalence | Реализовано и протестировано | approved bundle datasets; независимый read-only re-hash |
| Active PostgreSQL runtime adapter | Не реализовано | target не зарегистрирован в normal runtime composition |
| Automatic SQLite/PostgreSQL switching | Запрещено | availability и import success не являются selection |
| Exact-vs-ANN retrieval evaluation | Не реализовано | отдельная будущая фаза |
| Cutover / rollback / dual-write | Не реализовано | только отдельные явно проверяемые фазы |
| PostgreSQL server lifecycle | Не реализовано | backup/restore/upgrade/pooling остаются будущей работой |
| Reader Core / Semantic Reading Layer | Не реализовано | candidate layer до обычного admission |

## Текущая storage sequence

```text
SQLite lifecycle
→ backup / independent verify / inactive restore

logical portability
→ bounded canonical bundle
→ PostgreSQL preflight
→ inactive transactional import
→ independent exact-state equivalence
→ non-secret receipts
```

Issues #331 и #332 реализованы PR #335 и PR #337. Обычная установка остаётся
на стандартной библиотеке Python; PostgreSQL support — optional operator path.
`active=false` закреплён в target control state, а successful equivalence не
может активировать backend или изменить Guardian, TruthGate либо strict Canon.

## Реализованная граница query path

```text
HTTP /ask
CLI ask
MCP search
    ↓
core.query_pipeline.query()
    ↓
strict read-only canonical projection
```

Эти публичные query surfaces не должны выполнять admission-capable writes.
Явный `ingest` остаётся отдельным write path.

## Будущая работа

```text
exact-vs-ANN retrieval evaluation
→ explicit cutover + source/target fencing
→ rollback proof + expiry policy
→ PostgreSQL backup/restore/upgrade lifecycle
→ multi-process concurrency + production observability
```

Отдельно остаются production IdP/multi-tenancy, supply-chain release evidence
и dedicated Reader Core с source-linked coverage до Guardian/TruthGate.

## Чего Crystal не заявляет

Crystal не заявляет:

- active PostgreSQL runtime backend;
- automatic migration или automatic backend switching;
- production multi-tenancy;
- universal truth или zero hallucinations;
- legal, GDPR или security certification;
- consciousness.

## Authority переводов

Этот документ — поддерживаемая русская публичная поверхность. При расхождении
приоритет имеют merged GitHub code, exact CI, [TEST_REPORT.md](../../TEST_REPORT.md)
и английский [IMPLEMENTATION_STATUS.md](../IMPLEMENTATION_STATUS.md).
