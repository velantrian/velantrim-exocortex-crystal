<!-- translation-source: docs/STORAGE_AND_AUTHORITY_BOUNDARIES.md@208f1c772ee3a112cb803d2413c120bef23adb05 -->
<!-- translation-status: CURRENT -->
<!-- d3-locale: ru -->
<!-- d3-boundary: physical-l3-not-strict-canon -->
<!-- d3-boundary: public-query-read-only -->
<!-- d3-boundary: postgresql-active=false -->
<!-- d3-nonclaim: import-is-not-activation -->
<!-- d3-nonclaim: reader-core-not-implemented -->
<!-- d3-nonclaim: nlnet-not-awarded -->
# Границы хранения и власти

## Раздельные идентичности

```text
storage profile = идентичность развёртывания
physical L3 = многостатусное графовое состояние
strict Canon = доверенная проекция чтения
migration bundle = доказательство целостности операции
retrieval score = сигнал ранжирования
model output = сгенерированный текст
```

Ни одна из этих идентичностей автоматически не получает власть другой.

## Устойчивый профиль

SQLite — обычный активный local-first профиль. Первый устойчивый `auto` может выбрать опциональный LadybugDB или SQLite и зафиксировать backend и несекретный locator. Последующие конфликты завершаются fail-closed. Mock остаётся только явным состоянием для разработки/CI.

## physical L3 и strict Canon

physical L3 может содержать VERIFIED, USER_CLAIMED, UNVERIFIED, HYPOTHESIS, SUBJECTIVE, contested, superseded или restricted записи. strict Canon — deny-dominant проекция, основанная на текущих evidence и policy. Само хранение, retrieval или высокий score недостаточны.

## Чтение и запись

Публичные запросы проходят read-only через `core.query_pipeline.query()`. Явный `ingest` — admission-capable write path; Guardian и TruthGate затем применяют структурные и эпистемические границы.

## Жизненный цикл SQLite и миграция

Реализованы backup, независимая verification, inactive restore, ограниченный детерминированный logical export и проверка bundle. Утверждённые physical-L3 datasets можно импортировать в новую неактивную PostgreSQL schema и точно сравнить; цель остаётся `active=false`.

Это не whole-system migration всего L1, audit/outbox, метаданных шифрования, конфигурации или независимых копий. Активный PostgreSQL runtime, ANN acceptance, автоматическое switching, cutover, fencing, rollback и dual-write отсутствуют.

## Секреты и копии

Пароли, tokens, private keys и credential-bearing DSN не должны попадать в profiles, bundles, receipts, logs, GitHub или Notion. Backups, exports и migrations создают дополнительные копии; удаление из active store не удаляет их автоматически. Выборочное шифрование полей L1 не является универсальным шифрованием.

## Операционные доказательства

| Событие | Что доказывает | Чего не доказывает |
|---|---|---|
| запись в L3 | физическую сохранность | членство в strict Canon |
| retrieval result | релевантность кандидата | достаточность evidence |
| проверенный backup | целостность backup | истинность claim |
| успешный import | целостность import | activation или runtime selection |
| exact equivalence | равенство утверждённых datasets | production readiness или cutover |

Отдельный Reader Core не реализован; NLnet остаётся submitted / under review / not awarded.

## Подробные английские контракты

- [Полная архитектура](../ARCHITECTURE.md)
- [Устойчивый профиль хранения](../architecture/DURABLE_STORAGE_PROFILE.md)
- [Контракт миграции](../architecture/CROSS_BACKEND_MIGRATION_CONTRACT.md)
- [Неактивный импорт PostgreSQL](../architecture/POSTGRESQL_INACTIVE_IMPORT.md)
- [ADR-021](../adr/ADR-021-CROSS-BACKEND-MIGRATION-CONTRACT.md)
