<!-- translation-source: docs/ARCHITECTURE_OVERVIEW.md@0c3d537831e4f1cb5a43d61bc2cbc8b05c080df5 -->
<!-- translation-status: CURRENT -->
<!-- d3-locale: ru -->
<!-- d3-boundary: physical-l3-not-strict-canon -->
<!-- d3-boundary: public-query-read-only -->
<!-- d3-boundary: postgresql-active=false -->
<!-- d3-nonclaim: import-is-not-activation -->
<!-- d3-reader: rc1-skeleton-implemented -->
<!-- d3-reader: rc2-structural-map-implemented -->
<!-- d3-reader: rc3-multi-pass-mechanics-implemented -->
<!-- d3-nonclaim: dedicated-reader-core-not-implemented -->
<!-- d3-nonclaim: nlnet-not-awarded -->
# Crystal — обзор архитектуры

**Дата статуса:** 2026-08-10  
**Назначение:** стабильная архитектурная точка входа, пригодная для перевода.  
**Источник истины:** смерженный код, точный CI и machine-readable implementation manifest остаются authoritative runtime truth.

## Центральная модель

```text
identity источника/документа + точная версия/hash
        ↓
RC-1 evidence-linked Reader artifacts
        ↓
RC-2 caller-supplied Structural Document Map
        ↓
RC-3 explicit multi-pass mechanics над declared structural targets
        ↓
обычный ingest/review/evidence path
        ↓
проверки политик Guardian
        ↓
решение TruthGate о допуске
        ↓
операционное состояние L1 + многостатусный physical L3
        ↓
deny-dominant проекция чтения strict Canon
        ↓
read-only retrieval / ответ / ограниченный отказ
```

Reader artifacts, structural metadata и pass ledger остаются upstream observation/process state. Они не получают authority над истиной, admission, разрешением противоречий или planner-решениями.

Crystal не считает истинным каждый сохранённый узел, найденный результат или model output. Physical L3 хранит несколько статусов. Strict Canon — доверенная read-проекция, формируемая текущей политикой и evidence-ограничениями.

## Слои памяти и ревью

| Слой | Роль | Граница authority |
|---|---|---|
| Reader RC-1 | source/version/session artifacts, fidelity и coverage | source-linked observation/candidate, не истина |
| Reader RC-2 | version-bound структурная иерархия и порядок | структура и prominence — metadata, не confidence |
| Reader RC-3 | explicit pass attempts, declared targets и coverage outcomes | process audit, не comprehension или admission |
| L0 | process-local рабочее состояние | эфемерно, не durable truth |
| L1 | операционная память SQLite | durable facts, ESM, evidence, audit, receipts, import/review и outbox state |
| L2 | pending/review staging | candidate или quarantined claims до окончательного admission |
| L3 | графовое многостатусное хранилище | физическое хранение, не тождественное strict Canon |
| Strict read view | TrustSnapshot / CanonicalView | deny-dominant grounding surface |

## Разделение чтения и записи

```text
ask / receipt / MCP inspection → core.query_pipeline.query() → read-only
явный ingest                    → Guardian / TruthGate → admission-capable write
Reader RC-1 / RC-2 / RC-3       → source-linked artifacts/process state → без admission side effects
```

Публичный запрос не должен изменять facts, ESM, L3, outbox, связи эпизодов, embedding identity или unknown candidates. Если strict grounding недостаточен, ожидается ограниченный отказ.

## Профили хранения

SQLite — обычный активный local-first профиль. При первом устойчивом выборе `auto` может использоваться опциональный LadybugDB, если он установлен, иначе SQLite; после этого выбранный backend и несекретная locator identity сохраняются. Последующие конфликты backend или locator fail closed. Тихий fallback на эфемерный Mock запрещён; явный Mock остаётся состоянием для разработки/тестов.

Remote Neo4j — явный выбор оператора, расширяющий trust boundary.

## Переносимость и PostgreSQL

Проверенная цепочка переносимости:

```text
SQLite backup / verify / inactive restore
→ bounded deterministic logical export
→ PostgreSQL 16 + pgvector 0.8.2 preflight
→ новая неактивная target schema
→ serializable import
→ независимый read-only target re-hash
→ exact equivalence receipt
→ target остаётся active=false
```

PostgreSQL target отсутствует в обычной runtime composition. Успешный import или exact equivalence — evidence операции, а не activation, backend selection, TruthGate admission, strict Canon membership, cutover, rollback, dual-write или production readiness.

## Source-grounded Reader foundation

Source spans и evidence import-session входят в реализованный baseline. RC-1 даёт ограниченный evidence-linked каркас источника/сессии: точную source-version identity, locators, SegmentCards, source-fidelity classes, coverage states, bookmarks/open loops, stale handling и fail-visible failure/privacy semantics.

RC-2 добавляет caller-supplied Structural Document Map, привязанный к тем же точным семантикам SourceVersion и SourceLocator. Он моделирует иерархию/порядок и явные состояния `RECOVERED`, `AMBIGUOUS` и `UNSUPPORTED`, не заявляя автоматического parsing.

RC-3 добавляет deterministic explicit multi-pass mechanics, совместимые с архитектурным контрактом: `ORIENTATION`, `BROAD_READ`, `FOCUSED_READ`, `CROSS_CHECK` и `TARGETED_REREAD`. Pass заранее объявляет structural targets, записывает `ATTEMPTED` / `COMPLETED` / `INTERRUPTED` / `DEGRADED` и применяет только явные legal RC-1 coverage outcomes. Partial progress сохраняется при interruption/degradation. Cross-check и targeted re-read требуют prior substantive processing; targeted re-read требует explicit rationale. Pass counts — telemetry, а не comprehension scores.

Dedicated/full autonomous Reader / Semantic Reading runtime остаётся будущей работой. Нет автоматического parser/semantic chunker, LLM/provider-driven reading agent, embeddings/ANN/vector DB, automatic cross-document reasoning engine или automatic belief update.

```text
coverage != comprehension proof
pass completion != comprehension proof
structure/order/prominence != epistemic authority
```

## Безопасность и приватность

У стандартной установки нет обязательной зависимости от cloud, LLM, telemetry или analytics. Опциональные remote adapters, более широкая API-exposure и migration targets требуют явной настройки оператора. Шифрование отдельных полей L1 не является универсальным шифрованием. Удаление из active store не означает глобальное удаление из backups, exports, remote systems или provider copies.

RC-1/RC-2/RC-3 Reader не удерживают тело source-документа, а производные Reader artifacts и pass records наследуют restriction и sensitivity metadata источника. Структура/порядок/prominence Reader и pass completion не могут ослаблять privacy или epistemic policy.

## Текущие non-claims

Crystal не заявляет:

- AGI, сознание, универсальную истину или нулевые hallucinations;
- активный PostgreSQL runtime или automatic backend switching;
- cutover, rollback, dual-write или принятый production ANN profile;
- production multi-tenancy или distributed exactly-once coordination;
- завершённый dedicated/full autonomous Reader Core или automatic document comprehension;
- security, legal или GDPR certification;
- присуждённое финансирование NLnet.

## Подробные английские контракты

- [Полная архитектура](../ARCHITECTURE.md)
- [Архитектурный контракт Reader Core](../architecture/READER_CORE_ARCHITECTURE.md)
- [Границы хранения и authority](../STORAGE_AND_AUTHORITY_BOUNDARIES.md)
- [Статус реализации](../IMPLEMENTATION_STATUS.md)
- [Сводка по безопасности, приватности и отказам](../SAFETY_PRIVACY_AND_FAILURES.md)
