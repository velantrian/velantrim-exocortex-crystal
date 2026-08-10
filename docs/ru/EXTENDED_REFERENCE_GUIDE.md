<!-- translation-source: docs/EXTENDED_REFERENCE_POLICY.md@6b45bdd196eb42dea7bc30f58d69799b4b1712f2 -->
<!-- d5-locale: ru -->
<!-- translation-status: CURRENT -->
<!-- d5-boundary: physical-l3-not-strict-canon -->
<!-- d5-boundary: retrieval-score-not-evidence -->
<!-- d5-boundary: model-output-not-source-truth -->
<!-- d5-boundary: migration-proof-not-claim-proof -->
<!-- d5-nonclaim: import-is-not-activation -->
<!-- d5-reader: rc1-skeleton-implemented -->
<!-- d5-reader: rc2-structural-map-implemented -->
<!-- d5-nonclaim: dedicated-reader-core-not-implemented -->
<!-- d5-nonclaim: nlnet-not-awarded -->
<!-- d5-nonclaim: security-legal-gdpr-not-certified -->
<!-- d5-nonclaim: native-speaker-editorial-not-certified -->
# Руководство по расширенным источникам

Этот документ направляет к подробным английским источникам, не дублируя изменчивые implementation evidence, CI logs, ADR bodies, machine-readable status, legal mappings или grant evidence только ради видимости многоязычной полноты. Английский остаётся primary working/source/conflict-resolving language.

## Статусы документации

| Статус | Значение |
|---|---|
| `CURRENT` | Поддерживаемая public/routing surface, reconciled с immutable source checkpoint. |
| `REFRESH_NEEDED` | Reader-relevant surface, которая известным образом отстаёт от governing source; это всегда явный статус. |
| `RETIRED` | Сохранённый исторический snapshot/handoff; не current authority, capability или grant evidence. |
| `ENGLISH_ONLY_BY_DESIGN` | Подробный или изменчивый технический, security, test, CI, machine-readable, research, RFC, ADR или grant-evidence материал, намеренно поддерживаемый только на английском. |

Machine-readable inventory находится в [`../status/d5-inventory.json`](../status/d5-inventory.json). Не классифицированная documentation-like surface является validation failure.

## Reader Core boundary

Текущая machine truth намеренно различает bounded реализованные foundations и отсутствующую полную Reader capability:

```text
reader_core_rc1_skeleton       = true
reader_core_rc2_structural_map = true
dedicated_reader_core          = false
```

RC-1 реализует минимальный evidence-linked source/session skeleton. RC-2 реализует caller-supplied, source-version-bound Structural Document Map. Ни один слой не имеет truth/Canon/ESM/planner authority.

RC-1/RC-2 не удерживают source body и не добавляют durable Reader storage schema, public Reader API/CLI/background worker, automatic parser/OCR, LLM/provider orchestration, embeddings/ANN/vector database или multi-pass/cross-document reasoning runtime. `coverage != comprehension proof`; structural position/order/prominence — metadata, а не truth/confidence authority.

## Неизменные границы

```text
physical L3 != strict Canon
retrieval score != evidence
model output != source truth
migration proof != claim proof
import success != activation
Reader artifact != admitted fact
Reader coverage != comprehension proof
Reader structure != epistemic authority
```

SQLite остаётся ordinary active local-first profile. Mock остаётся явным development/CI backend. PostgreSQL/pgvector остаётся неактивной target с `active=false`. Dedicated multi-pass Reader / Semantic Reading runtime не реализован.

## Грант и certification non-claims

NLnet остаётся `submitted / under review / not awarded`. Приблизительно €50,000 — planning only, не approved budget и не payment commitment. Текущая grant-safe граница: **budget change: none**. Работа, смерженная до соглашения, включая RC-0/RC-1/RC-2, не может повторно считаться funded delta.

Не заявляются legal, GDPR, security или native-speaker editorial certification.

## Retired и English-only материалы

`RETIRED` материалы сохраняются для attribution/audit history, но не доказывают implementation, test coverage, maturity, grant status, Canon membership или deployment readiness.

`ENGLISH_ONLY_BY_DESIGN` применяется к подробным техническим и evidence-семействам, где перевод каждого изменчивого артефакта повысил бы риск stale claims. Для актуальной публичной ориентации используйте D1–D5 переводные поверхности, а для решения конфликтов — английские source contracts и merged code/CI.

## Маршруты к authoritative источникам

- [D5 policy](../EXTENDED_REFERENCE_POLICY.md)
- [Карта документации](../DOCUMENTATION_MAP.md)
- [Текущий статус](./STATUS.md)
- [Статус реализации](./IMPLEMENTATION_STATUS.md)
- [Обзор архитектуры](./ARCHITECTURE_OVERVIEW.md)
- [Полная архитектура](../ARCHITECTURE.md)
- [Reader Core architecture contract](../architecture/READER_CORE_ARCHITECTURE.md)
- [ADR index](../ADR.md)
- [Security policy](../../SECURITY.md)
- [Privacy](../../PRIVACY.md)
- [GDPR technical mapping](../../GDPR.md)
- [Archive routing](../archive/README.md)

При расхождении приоритет имеют merged GitHub code, executable tests, exact CI, machine-readable manifests и governing English source.
