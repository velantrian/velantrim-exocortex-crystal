<!-- translation-source: docs/SAFETY_PRIVACY_AND_FAILURES.md@b7e6574dd7aefa2f32783ab79054fac6b3b4109f -->
<!-- translation-status: CURRENT -->
<!-- d2-locale: ru -->
<!-- d2-boundary: public-ask-read-only -->
<!-- d2-boundary: postgresql-active=false -->
<!-- d2-boundary: erasure-not-global -->
<!-- d2-nonclaim: security-legal-gdpr-not-certified -->
<!-- d2-nonclaim: nlnet-not-awarded -->
# Границы безопасности, приватности и отказов

**Источник:** `docs/SAFETY_PRIVACY_AND_FAILURES.md@b7e6574dd7aefa2f32783ab79054fac6b3b4109f`  
Этот документ — локализованная обзорная поверхность. Он не заменяет тесты, security review,
юридическую оценку или подробные английские контракты.

## Эпистемическая безопасность

```text
physical L3 storage != strict Canon
retrieval score      != evidence
model output         != verified world fact
migration bundle     != claim evidence
successful import    != backend activation
```

Guardian и TruthGate остаются admission boundaries. Публичные query surfaces read-only;
explicit ingest — отдельная запись. Curator override должен быть явным, атрибутированным
и аудируемым. Crystal не гарантирует истину или отсутствие галлюцинаций: измеримая цель —
блокировать, маркировать, отказывать или делать неподтверждённое состояние аудируемым.

## Локальная граница доверия

У default installation нет обязательного cloud, LLM, telemetry или analytics. Обычный
активный профиль — SQLite. Durable `auto` может выбрать optional LadybugDB или SQLite и
фиксирует выбор; ephemeral Mock — только явный dev/test state. PostgreSQL/pgvector не является
обычным runtime backend и остаётся operator-only inactive target с `active=false`.

## Данные и расширение границы

Система может хранить claims, metadata, source/provenance, epistemic state, graph nodes/edges,
restrictions, erasure/audit records, receipts, outbox state, migration bundles, backups и
exports. Local-first не делает персональные данные безвредными.

Данные выходят за локальную границу только при явном включении Anthropic, remote Neo4j,
Wikidata, Redis, PostgreSQL migration, wider HTTP API либо при копировании backup/export.
Sentence-transformers может скачать weights при первом использовании, но inference локален.

## Encryption и secrets

`VELANTRIM_ENCRYPTION_KEY` защищает выбранные поля L1; защита выключена по умолчанию и не
охватывает автоматически все L3, backups, exports, receipts, logs и temporary files.
Требуются host disk encryption и key management по уровню чувствительности.

Secrets и credential-bearing connection strings не должны попадать в profiles, bundles,
receipts, application logs, public issues или Notion.

## API и deployment

Документированный API baseline использует authentication и loopback binding. Перед внешним
доступом необходимы TLS, проверенная authentication, least privilege, secret rotation,
resource limits, monitoring, incident handling и проверенные backup/restore/deletion.
Production IdP, полная multi-tenancy и security certification не заявлены.

## Privacy operations

Есть инженерные механизмы access/export, rectification/supersession, restriction, erasure
и record of processing. Это не legal/GDPR certification. Erasure активного store не удаляет
автоматически backups, bundles, operator copies, remote systems, provider data, logs или
receipts — для копий нужна отдельная политика.

## Матрица безопасных отказов

| Класс | Ожидаемое поведение |
|---|---|
| Unsupported claim | block, label или bounded refusal |
| Read-only mutation | reject / no state change |
| Profile conflict | fail до backend cache |
| Optional dependency absent | явная ограниченная ошибка, без скрытого Mock fallback |
| Import failure | rollback, target остаётся `active=false` |
| Evidence mismatch | verification failure |
| Receipt/audit tampering | digest/hash-chain failure |
| Oversized migration | fail closed по лимитам |
| Network exposure | только явная authenticated operator configuration |
| Erasure copy survives | отдельный inventory и deletion process |

## Явные non-claims

Crystal не является security/legal/GDPR certification, доказательством arbitrary scale,
активным PostgreSQL runtime, системой automatic migration, гарантией perfect truth,
AGI/сознанием или доказательством присуждённого NLnet grant.

Подробности: [Security](../../SECURITY.md), [Privacy](../../PRIVACY.md),
[GDPR](../../GDPR.md), [Failure Modes](../FAILURE_MODES.md) и
[английский summary](../SAFETY_PRIVACY_AND_FAILURES.md).
