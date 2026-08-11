<!-- translation-source: docs/ARCHITECTURE_OVERVIEW.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- d3-locale: ru -->
<!-- d3-boundary: physical-l3-not-strict-canon -->
<!-- d3-boundary: public-query-read-only -->
<!-- d3-boundary: postgresql-active=false -->
<!-- d3-nonclaim: import-is-not-activation -->
<!-- d3-reader: rc1-skeleton-implemented -->
<!-- d3-reader: rc2-structural-map-implemented -->
<!-- d3-reader: rc3-multi-pass-mechanics-implemented -->
<!-- d3-reader: rc4-proposition-extraction-implemented -->
<!-- d3-reader: rc5-relation-candidates-implemented -->
<!-- d3-nonclaim: dedicated-reader-core-not-implemented -->
<!-- d3-nonclaim: nlnet-not-awarded -->
# Crystal — обзор архитектуры

**Дата статуса:** 2026-08-11  
**Назначение:** стабильная архитектурная точка входа, пригодная для перевода.  
**Источник истины:** merged code, exact CI и machine-readable implementation manifest остаются authoritative implementation truth.

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
RC-4 source-linked EXTRACTED_PROPOSITION candidates
        ↓
RC-5 explicit same-session/same-version relation candidates
        ↓
обычный ingest/review/evidence path остаётся отдельным
        ↓
проверки политик Guardian
        ↓
решение TruthGate о допуске
        ↓
операционное состояние L1 + multi-status physical L3
        ↓
deny-dominant strict Canon read projection
        ↓
read-only retrieval / ответ / bounded refusal
```

Reader artifacts, structural metadata, pass ledger, extracted propositions и relation candidates остаются upstream observation/process/candidate state. Они не получают authority над truth, evidence admission, contradiction disposition или planner decisions.

## Слои памяти и Reader

| Слой | Роль | Граница authority |
|---|---|---|
| Reader RC-1 | source/version/session artifacts, fidelity и coverage | source-linked observation/candidate, не truth |
| Reader RC-2 | version-bound structural hierarchy/order | structure/prominence — metadata, не confidence |
| Reader RC-3 | explicit pass attempts, declared targets и outcomes | process audit, не comprehension/admission |
| Reader RC-4 | source-linked proposition candidates из completed substantive regions | source presentation/candidate state, не verified fact/admitted evidence |
| Reader RC-5 | explicit relations между valid RC-4 candidates | relation suspicion, не confirmed contradiction/winner |
| L0 | process-local working state | ephemeral, не durable truth |
| L1 | operational SQLite memory | durable operational state, но не автоматически strict Canon |
| L2 | pending/review staging | candidate/quarantined claims до admission |
| L3 | graph-oriented multi-status storage | physical storage ≠ strict Canon |
| Strict read view | TrustSnapshot / CanonicalView | deny-dominant grounding surface |

## Разделение чтения и записи

```text
ask / receipt / MCP inspection             → core.query_pipeline.query() → read-only
explicit ingest                             → Guardian / TruthGate → admission-capable write
Reader RC-1 / RC-2 / RC-3 / RC-4 / RC-5   → source/process/candidate artifacts only → no admission side effects
```

Public query не должен изменять facts, ESM, L3, outbox, episode links, embedding identity или unknown candidates. Если strict grounding недостаточен, ожидается bounded refusal.

## Durable storage profiles

SQLite — ordinary active local-first profile. Существующие optional adapters не меняют Reader authority. Remote Neo4j остаётся explicit operator choice, расширяющим trust boundary.

## Переносимость и PostgreSQL

Проверенная цепочка:

```text
SQLite backup / verify / inactive restore
→ bounded deterministic logical export
→ PostgreSQL 16 + pgvector 0.8.2 preflight
→ fresh inactive target schema
→ serializable import
→ independent read-only target re-hash
→ exact equivalence receipt
→ active=false
```

PostgreSQL target отсутствует в ordinary runtime composition. Successful import/equivalence — operation evidence, не backend activation, selection, TruthGate admission, strict Canon membership, cutover, rollback, dual-write или production readiness. RC-5 не меняет storage schema и не активирует PostgreSQL.

## Source-grounded Reader foundation

RC-1 даёт bounded evidence-linked source/session skeleton: exact source-version identity, locators, SegmentCards, fidelity classes, coverage states, bookmarks/open loops, stale handling и fail-visible failure/privacy semantics.

RC-2 добавляет caller-supplied Structural Document Map, привязанный к тем же exact SourceVersion/SourceLocator semantics. Он моделирует hierarchy/order и `RECOVERED`, `AMBIGUOUS`, `UNSUPPORTED`, не заявляя automatic parsing.

RC-3 добавляет deterministic explicit multi-pass mechanics: `ORIENTATION`, `BROAD_READ`, `FOCUSED_READ`, `CROSS_CHECK`, `TARGETED_REREAD`. Pass заранее объявляет structural targets, записывает `ATTEMPTED` / `COMPLETED` / `INTERRUPTED` / `DEGRADED` и применяет только explicit legal RC-1 coverage outcomes. Partial progress сохраняется. Cross-check и targeted reread требуют prior substantive processing; targeted reread требует rationale. Pass counts — telemetry, не comprehension scores.

RC-4 добавляет deterministic pre-admission proposition extraction. Candidate регистрируется только для target из `COMPLETED` RC-3 pass, если recorded outcome и current matching coverage = `PROCESSED` либо `REVISITED`. Candidate остаётся `SegmentCard` с `EXTRACTED_PROPOSITION` fidelity, replayable primary/supporting locators, source owner, proposition-presentation category, negation и qualifiers. `FACTUAL_ASSERTION` описывает presentation источника, не Crystal verification.

RC-5 добавляет `core/reader_relations.py`: explicit relation registration только поверх candidates, уже зарегистрированных одним RC-4 extractor. Registry требует OPEN session, same exact source version и current candidate/card provenance. Он сохраняет обе стороны и rationale.

```text
POSSIBLE_CONTRADICTION  — symmetric candidate suspicion
TENSION                 — symmetric non-resolution tension
EXCEPTION               — directional: right limits left
QUALIFICATION           — directional: right refines left
```

`POSSIBLE_CONTRADICTION`/`TENSION` canonicalize candidate-ID order. `EXCEPTION`/`QUALIFICATION` preserve direction. Duplicate symmetric registration fail closed и не становится corroboration.

```text
coverage != comprehension proof
pass completion != comprehension proof
structure/order/prominence != epistemic authority
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
similarity != identity
repetition != corroboration
```

RC-5 не сравнивает raw source text автоматически, не использует semantic similarity как proof, не создаёт cross-document identity и не invokes contradiction resolution. `core.evidence.attach_evidence()` остаётся за пределами Reader.

Dedicated/full autonomous Reader / Semantic Reading runtime остаётся будущей работой. Нет automatic parser/semantic chunker, NLP/LLM extraction, provider-driven reading agent, embeddings/ANN/vector DB, automatic cross-document reasoning engine, contradiction resolution или automatic belief update.

## Безопасность и privacy

У стандартной установки нет обязательной зависимости от cloud, LLM, telemetry или analytics. Optional remote adapters расширяют trust boundary только при explicit operator configuration. Field-level encryption не является universal encryption; active-store erasure не означает deletion backups/exports/remote/provider copies.

RC-1..RC-5 не удерживают source body. Derived artifacts наследуют restriction/sensitivity metadata. Structure/order/prominence, pass completion, proposition extraction и relation registration не могут ослаблять privacy или epistemic policy.

## Текущие non-claims

Crystal не заявляет:

- AGI, consciousness, universal truth или zero hallucinations;
- active PostgreSQL runtime или automatic backend switching;
- cutover, rollback, dual-write или accepted production ANN profile;
- production multi-tenancy или distributed exactly-once coordination;
- dedicated/full autonomous Reader Core;
- automatic parsing/NLP/LLM contradiction detection/resolution;
- semantic cross-document identity;
- security, legal или GDPR certification;
- awarded NLnet funding.

## Подробные английские контракты

- [Полная архитектура](../ARCHITECTURE.md)
- [Reader Core architecture contract](../architecture/READER_CORE_ARCHITECTURE.md)
- [Storage and authority boundaries](../STORAGE_AND_AUTHORITY_BOUNDARIES.md)
- [Implementation status](../IMPLEMENTATION_STATUS.md)
- [Safety/privacy/failures](../SAFETY_PRIVACY_AND_FAILURES.md)
