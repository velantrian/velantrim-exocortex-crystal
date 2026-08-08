# 📌 Velantrim Crystal — текущий статус

<!-- translation-source: docs/STATUS.md@16d71e731ee658b1faa65c9ea45c0d8cca290f7c -->
<!-- translation-status: CURRENT -->

> 🌐 🇬🇧 [English](../STATUS.md) · 🇩🇪 [Deutsch](../de/STATUS.md) · 🇫🇷 [Français](../fr/STATUS.md) · 🇪🇸 [Español](../es/STATUS.md) · 🇮🇹 [Italiano](../it/STATUS.md) · 🇷🇺 **Русский** · 🇨🇳 [简体中文](../zh-CN/STATUS.md) · 🇸🇦 [العربية](../ar/STATUS.md) · 🇯🇵 [日本語](../ja/STATUS.md) · 🇮🇳 [हिन्दी](../hi/STATUS.md)

**Дата статуса:** 8 августа 2026 года  
**Проверенный runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6`  
**Проверенное tree:** `f57e58a6f4d1954b649ba324996fcde42ac287b8`  
**Валидированный implementation head:** `d7af7c80722274f9217bc5545d150f92e9363f37`  
**Runtime PR / CI:** #337 / `31256316536`  
**PostgreSQL integration CI:** `31256316532`

## Проверка

- Python 3.11: **2078 passed / 13 skipped / 0 failed**;
- Python 3.12: **2078 passed / 13 skipped / 0 failed**;
- **9756 statements / 100.00% line coverage**;
- `core/postgresql_migration.py`: **44/44 statements**;
- `core/postgresql_migration_impl.py`: **336/336 statements**;
- **7/7** заявленных Ring Zero mutants уничтожены;
- **9/9** постоянных CI jobs завершились успешно;
- **1/1** реальный PostgreSQL/pgvector integration job завершился успешно.

Точные evidence: [TEST_REPORT.md](../../TEST_REPORT.md) и
[machine-readable manifest](../status/implementation-manifest.json).

## Текущая проверенная граница возможностей

Crystal сохраняет local-first SQLite baseline и реализует фазу 1 issue #332:

```text
проверенный завершённый logical bundle
→ preflight PostgreSQL 16 / pgvector 0.8.2
→ новая неактивная target schema
→ serializable import
→ независимый read-only canonical re-hash цели
→ точная equivalence по count / byte / SHA-256
→ receipts без секретов
```

PostgreSQL driver является optional extra и lazy-load выполняется только
явными operator commands. Обычная установка остаётся на стандартной библиотеке
Python. Импортированная цель:

- не регистрируется в обычной runtime composition;
- остаётся `active=false`;
- не обслуживает normal reads или writes;
- не становится выбранным backend из-за доступности, импорта или equivalence.

## Граница authority

```text
storage profile         = deployment identity
migration bundle        = operation evidence
physical L3             = multi-status storage
strict Canon            = trusted read projection
migration/import        != TruthGate admission
successful equivalence  != backend activation
```

Guardian, TruthGate, restrictions, TrustSnapshot и CanonicalView не изменены.
Перевод документа также не создаёт отдельную authority над кодом или evidence.

## Что ещё отсутствует

- active PostgreSQL read/write runtime selection;
- exact-vs-ANN retrieval evaluation и принятые ANN thresholds;
- activation, cutover, source/target fencing, rollback и dual-write;
- PostgreSQL backup/restore/upgrade lifecycle, production pooling и distributed fencing;
- production IdP/multi-tenancy;
- legal, security или GDPR certification;
- dedicated verified Reader Core / Semantic Reading Layer.

## Граница публичных claims

Crystal можно описывать как:

- local-first инфраструктуру памяти ИИ с provenance и auditability;
- систему с явными admission и read-only query boundaries;
- SQLite-baseline с проверенной backup/restore и logical portability;
- систему с неактивным PostgreSQL import/equivalence operator path;
- open-source baseline, которую можно независимо тестировать.

Crystal нельзя описывать как:

- активный PostgreSQL runtime;
- систему с automatic backend switching;
- production-ready multi-tenant service;
- юридически или security-сертифицированный продукт;
- универсальный источник истины или гарантию zero hallucinations;
- сознательную систему.

## Статус гранта

Проект подан в NLnet и находится на рассмотрении. **Получение гранта или
изменение бюджета не заявляется.**

PR #337 и issue #332 уже являются merged baseline и не могут повторно
учитываться как будущий funded delta. Следующая storage-фаза должна быть
отдельно специфицирована, проверена и находиться за пределами inactive import
и exact equivalence.

## Навигация

- [Быстрый старт](./QUICKSTART.md)
- [Статус реализации](./IMPLEMENTATION_STATUS.md)
- [Русский README](../../README.ru.md)
- [Английский нормативный статус](../STATUS.md)
- [Отчёт о тестах](../../TEST_REPORT.md)
- [Архитектура inactive PostgreSQL import](../architecture/POSTGRESQL_INACTIVE_IMPORT.md)
- [Политика локализации](../LOCALIZATION_POLICY.md)

> При расхождении действует актуальный GitHub `main`, executable tests и
> английский исходный документ, указанный в `translation-source`.
