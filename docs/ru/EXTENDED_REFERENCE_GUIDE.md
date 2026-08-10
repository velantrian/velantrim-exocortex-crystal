<!-- translation-source: docs/EXTENDED_REFERENCE_POLICY.md@166fab5551c4b86ee0a546b2e1d3dc7adc240c86 -->
<!-- d5-locale: ru -->
<!-- translation-status: CURRENT -->
<!-- d5-boundary: physical-l3-not-strict-canon -->
<!-- d5-boundary: retrieval-score-not-evidence -->
<!-- d5-boundary: model-output-not-source-truth -->
<!-- d5-boundary: migration-proof-not-claim-proof -->
<!-- d5-nonclaim: import-is-not-activation -->
<!-- d5-reader: rc1-skeleton-implemented -->
<!-- d5-reader: rc2-structural-map-implemented -->
<!-- d5-reader: rc3-multi-pass-mechanics-implemented -->
<!-- d5-reader: rc4-proposition-extraction-implemented -->
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
| `REFRESH_NEEDED` | Surface, которая известным образом отстаёт от governing source; это всегда явный статус. |
| `RETIRED` | Сохранённый исторический snapshot/handoff; не current authority, capability или grant evidence. |
| `ENGLISH_ONLY_BY_DESIGN` | Подробный или изменчивый технический, security, test, CI, machine-readable, research, RFC, ADR или grant-evidence материал, намеренно поддерживаемый только на английском. |

Machine-readable inventory находится в [`../status/d5-inventory.json`](../status/d5-inventory.json). Не классифицированная documentation-like surface является validation failure.

После RC-4 русский root README и Reader-dependent detail pack имеют `CURRENT`. Восемь других localized root README плюс семь Reader-dependent detail document types на каждую из восьми локалей имеют `REFRESH_NEEDED`: всего 64 отслеживаемых translation debt documents. Их rich предыдущие переводы сохранены; сокращённые замены не считаются допустимым refresh.

## Reader Core boundary

Текущая machine truth намеренно различает bounded реализованные слои и отсутствующую полную Reader capability:

```text
reader_core_rc1_skeleton = true
reader_core_rc2_structural_map = true
reader_core_rc3_multi_pass_mechanics = true
reader_core_rc4_proposition_extraction = true
dedicated_reader_core = false
```

RC-1 реализует минимальный evidence-linked source/session skeleton. RC-2 реализует caller-supplied, source-version-bound Structural Document Map. RC-3 реализует deterministic explicit multi-pass mechanics: `ORIENTATION`, `BROAD_READ`, `FOCUSED_READ`, `CROSS_CHECK`, `TARGETED_REREAD`; declared structural targets; `ATTEMPTED` / `COMPLETED` / `INTERRUPTED` / `DEGRADED` ledger; explicit legal coverage outcomes и count-only telemetry.

RC-4 реализует deterministic pre-admission proposition candidate registration из completed substantive RC-3 targets. Candidate требует pass state `COMPLETED`; recorded pass outcome и current matching coverage должны быть `PROCESSED` или `REVISITED`. Candidate остаётся source-linked `SegmentCard` с `EXTRACTED_PROPOSITION` fidelity, replayable primary/supporting locators, explicit source owner, proposition-presentation category, negation и qualifiers.

Категории factual assertion, author opinion, hypothesis, conditional, example, quoted speech, reported position, definition и uncertain assertion описывают presentation источника, а не truth admission. `FACTUAL_ASSERTION` не означает, что Crystal проверил утверждение.

RC-4 не является automatic NLP/LLM extraction. Он не вызывает `core.evidence.attach_evidence()`, не пишет fact `evidence_spans`, не устанавливает evidence sufficiency, не меняет `truth_status`/ESM и не выполняет TruthGate admission.

RC-1/RC-2/RC-3/RC-4 не имеют truth/Canon/ESM/planner authority, не удерживают source body и не добавляют durable Reader storage schema, public Reader API/CLI/background worker, automatic parser/OCR, autonomous model-driven Reader, embeddings/ANN/vector database или automatic cross-document reasoning runtime.

```text
coverage != comprehension proof
pass completion != comprehension proof
structure/order/prominence != epistemic authority
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
```

## Неизменные границы

```text
physical L3 != strict Canon
retrieval score != evidence
model output != source truth
migration proof != claim proof
import success != activation
Reader artifact != admitted fact
Reader coverage != comprehension proof
Reader pass completion != comprehension proof
Reader structure != epistemic authority
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
```

SQLite остаётся ordinary active local-first profile. Mock остаётся явным development/CI backend. PostgreSQL/pgvector остаётся неактивной target с `active=false`. Dedicated/full autonomous Reader / Semantic Reading runtime и automatic NLP/model proposition extraction не реализованы.

## Грант и certification non-claims

NLnet остаётся `submitted / under review / not awarded`. Приблизительно €50,000 — planning only, не approved budget и не payment commitment. Текущая grant-safe граница: **budget change: none**. Работа, смерженная до соглашения, включая RC-0/RC-1/RC-2/RC-3 и RC-4, если он merged pre-agreement, не может повторно считаться funded delta.

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
