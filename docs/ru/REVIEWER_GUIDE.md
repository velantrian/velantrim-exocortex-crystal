<!-- translation-source: docs/REVIEWER_GUIDE.md@b7e6574dd7aefa2f32783ab79054fac6b3b4109f -->
<!-- translation-status: CURRENT -->
<!-- d2-locale: ru -->
<!-- d2-boundary: public-ask-read-only -->
<!-- d2-boundary: postgresql-active=false -->
<!-- d2-boundary: erasure-not-global -->
<!-- d2-nonclaim: security-legal-gdpr-not-certified -->
<!-- d2-nonclaim: nlnet-not-awarded -->
# Руководство для проверяющего — Velantrim Exo-Cortex Crystal

**Контрольная точка английского источника:** `main@b7e6574dd7aefa2f32783ab79054fac6b3b4109f`  
**Назначение:** быстрый путь проверки, связанный с воспроизводимыми доказательствами.  
**Граница полномочий:** этот перевод помогает ориентироваться; доказательствами реализации
остаются код в `main`, исполняемые тесты, точный CI, [TEST_REPORT.md](../../TEST_REPORT.md)
и [implementation manifest](../status/implementation-manifest.json).

## 1. Что проверяется

Crystal — публичная local-first инфраструктура памяти для систем ИИ, ориентированная на
источники, происхождение и аудит. Текущая проверенная база включает типизированные claims,
Guardian/TruthGate, строгую read-проекцию Canon над многостатусным физическим L3,
read-only публичные запросы, отдельный явный ingest/write path, receipts и audit trail.

Crystal не заявляет AGI, сознание, универсальную истину, нулевые галлюцинации, активный
PostgreSQL runtime, автоматическое переключение backend, production multi-tenancy,
сертификацию безопасности/GDPR или получение гранта NLnet.

## 2. Воспроизведение базы

```bash
python -m pip install --upgrade pip
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
python scripts/eval_gate.py --out-dir eval-artifacts
bash scripts/ring_zero_mutation_gate.sh
bash scripts/check_docs_status.sh
```

Изменяемые числа тестов и покрытия берутся из [TEST_REPORT.md](../../TEST_REPORT.md),
а не из этого перевода.

## 3. Граница чтения и записи

```text
ask / receipt / MCP inspection → read-only
explicit ingest                → admission-capable write path
curator override               → явное, атрибутированное и аудируемое действие
```

Публичный `ask` проходит через `core.query_pipeline.query()` и не должен изменять facts,
ESM, L3, outbox, episode links, embedding identity или неизвестных кандидатов. Ограниченный
отказ при недостаточном строгом grounding — ожидаемое безопасное поведение.

`ingest` является записью, но admission всё равно зависит от evidence, claim type, policy
и TruthGate. Вывод модели не может сам сертифицировать себя как проверенный факт мира.

## 4. Хранилище и миграция

Обычный документированный активный профиль — SQLite. Первый durable `auto` может выбрать
опциональный LadybugDB, если зависимость установлена, иначе SQLite; победитель и несекретный
locator фиксируются в durable profile. Неявный переход к ephemeral Mock запрещён.

PostgreSQL/pgvector — отдельный операторский путь:

```text
verified logical bundle
→ version/TLS preflight
→ новое inactive schema
→ serializable import
→ независимый read-only re-hash
→ exact equivalence receipt
→ active=false
```

Успешный import/equivalence не означает activation, backend selection, TruthGate admission,
strict Canon membership, cutover, rollback, dual-write или production readiness.

## 5. Безопасность и приватность

По умолчанию нет обязательного cloud, LLM, telemetry или analytics. Граница расширяется
только явной настройкой remote Neo4j, Anthropic, Wikidata, Redis, PostgreSQL migration,
широкого API binding либо копированием backup/export.

`VELANTRIM_ENCRYPTION_KEY` защищает отдельные персональные поля L1, но не гарантирует
шифрование каждого L3 backend, backup, bundle, receipt, log или temporary file. Пароли,
tokens, keys и credential-bearing DSN нельзя помещать в profiles, bundles, receipts, logs,
issues или Notion.

Удаление из активного локального store не удаляет автоматически backups, exports,
операторские копии, remote systems или уже переданные third-party data. Нужны inventory,
retention schedule и отдельная процедура удаления копий.

## 6. Проверка отказов

Проверяющий должен подтвердить fail-closed поведение:

- unsupported/self-certified claims блокируются, маркируются или получают bounded refusal;
- malformed profile и locator conflict завершаются ошибкой до cache backend;
- import failure откатывает transaction и оставляет target `active=false`;
- evidence mismatch и receipt/audit tampering обнаруживаются;
- oversized migration input отклоняется лимитами;
- отсутствующая optional dependency не вызывает скрытого durable switch;
- широкая сеть требует TLS, authentication, least privilege и monitoring.

## 7. Чек-лист

- [ ] Зафиксированы текущий `main` и точный CI.
- [ ] Read-only query отделён от explicit ingest.
- [ ] Physical L3 отделён от strict Canon.
- [ ] Inactive PostgreSQL import отделён от activation.
- [ ] Проверены optional network adapters и secret handling.
- [ ] Учтены границы encryption и erasure copies.
- [ ] Не выведены certification, production readiness или grant award.

Подробные английские источники: [Reviewer Guide](../REVIEWER_GUIDE.md),
[Security](../../SECURITY.md), [Privacy](../../PRIVACY.md),
[Failure Modes](../FAILURE_MODES.md) и
[Safety/Privacy/Failure summary](../SAFETY_PRIVACY_AND_FAILURES.md).

<!-- post-v1-parity-audit: 2026-11-27; code-base: 78088e029b86d8f923178d19e9cecabd650a4f61; english-doc-source: 90f423b53ffdc364680a5e49b9ffa70e853413f9 -->
## 🧩 Дополнения после V1

Reader Product Bridge v0.1 и локальные источники UTF-8 (TXT/Markdown) и PDF v0.1 реализованы (#455, #457, #458). Это ограниченные компоненты чтения до допуска: они не разрешают семантическое выполнение моделей, допуск свидетельств, запись в Canon или production.

Для обоснования публичного фактического ответа `VERIFIED` требует актуального пригодного к воспроизведению свидетельства, привязанного к точному утверждению, разрешённому `TrustSnapshot` (#464). Совпадение ID, прежний вердикт или квитанция недостаточны; потеря поддержки не доказывает ложность. Исторические решения не переписываются.

#507/#505 сверяет L0 с общей SQLite L1 при каждом `get_fact()`; #512 изолирует возвращаемые данные глубоким копированием и закрывает соединение при ошибке схемы; #513 отклоняет обычный повторный ingest уже restricted-записи до записи; #511 проверяет tombstone перед разрешением результата канонического поиска. Это ограниченные исправления: начатые ранее чтения, гонка ограничения и записи, другие пути, восстановление и независимые копии не покрыты полностью. Каскад следует только зарегистрированным `DERIVED_FROM`; полнота происхождения и прерывания остаются открытыми (#504). Завершение V1 и зелёный CI не доказывают отсутствие дефектов, юридическое соответствие или production-авторизацию.

[Английский источник](../REVIEWER_GUIDE.md)
