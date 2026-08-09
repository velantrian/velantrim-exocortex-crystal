<!-- translation-source: docs/ARCHITECTURE_OVERVIEW.md@208f1c772ee3a112cb803d2413c120bef23adb05 -->
<!-- translation-status: CURRENT -->
<!-- d3-locale: ru -->
<!-- d3-boundary: physical-l3-not-strict-canon -->
<!-- d3-boundary: public-query-read-only -->
<!-- d3-boundary: postgresql-active=false -->
<!-- d3-nonclaim: import-is-not-activation -->
<!-- d3-nonclaim: reader-core-not-implemented -->
<!-- d3-nonclaim: nlnet-not-awarded -->
# Crystal — обзор архитектуры

Этот перевод — навигационный слой. При расхождении приоритет имеют смерженный код, исполняемые тесты, точный CI и английские контракты.

## Центральная модель

```text
источники + явный ingest
→ provenance + нормализация
→ проверки Guardian
→ решение TruthGate
→ операционное состояние L1 + многостатусный physical L3
→ deny-dominant проекция чтения strict Canon
→ read-only retrieval / ответ / ограниченный отказ
```

Наличие записи в physical L3 не означает автоматическое членство в strict Canon. Retrieval score, векторное сходство и model output не являются независимым доказательством.

## Слои памяти и ревью

- **L0:** временный контекст процесса.
- **L1:** SQLite/WAL для операционного состояния, evidence, аудита, receipts, import/review sessions и outbox.
- **L2:** pending/review staging для кандидатов и карантина; это не финальный слой истины.
- **L3:** графовое многостатусное хранилище; не тождественно strict Canon.
- **TrustSnapshot / CanonicalView:** доверенная deny-dominant поверхность чтения.

## Разделение чтения и записи

`HTTP /ask`, `CLI ask` и MCP идут read-only через `core.query_pipeline.query()`. Запрос не может создавать или усиливать факты, менять ESM, L3, outbox, связи эпизодов или идентичность embedder. Только явный `ingest` входит в admission-capable write path, контролируемый Guardian и TruthGate.

## Профили хранения и переносимость

SQLite — обычный активный local-first профиль. При первом устойчивом `auto` может быть выбран опциональный LadybugDB или SQLite, после чего фиксируются backend и несекретная locator identity. Тихий fallback на эфемерный Mock запрещён.

Проверенный путь PostgreSQL/pgvector заканчивается на неактивной цели:

```text
проверенный SQLite bundle
→ транзакционный импорт PostgreSQL
→ независимый read-only re-hash
→ точная эквивалентность
→ active=false
```

Import или equivalence не являются activation, выбором backend, допуском TruthGate, cutover, rollback или dual-write. PostgreSQL отсутствует в обычной runtime composition.

## Работа с документами

Source spans, записи документов, import sessions и dry-run/review flows входят в реализованный baseline. Отдельный multi-pass Reader Core с картами покрытия, повторным чтением с учётом противоречий и синтезом на уровне документа не реализован.

## Что не заявляется

Crystal не заявляет AGI, сознание, нулевые hallucinations, активный PostgreSQL runtime, автоматическое switching, принятый production ANN, cutover/rollback/dual-write, security/legal/GDPR certification или присуждённый грант NLnet.

## Английские источники

- [Полная архитектура](../ARCHITECTURE.md)
- [Границы хранения и власти](../STORAGE_AND_AUTHORITY_BOUNDARIES.md)
- [Статус реализации](../IMPLEMENTATION_STATUS.md)
- [Неактивный импорт PostgreSQL](../architecture/POSTGRESQL_INACTIVE_IMPORT.md)
