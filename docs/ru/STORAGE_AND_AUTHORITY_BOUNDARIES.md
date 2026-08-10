<!-- translation-source: docs/STORAGE_AND_AUTHORITY_BOUNDARIES.md@166fab5551c4b86ee0a546b2e1d3dc7adc240c86 -->
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
<!-- d3-nonclaim: dedicated-reader-core-not-implemented -->
<!-- d3-nonclaim: nlnet-not-awarded -->
# Границы хранения и authority

**Дата статуса:** 10 августа 2026 года  
**Назначение:** стабильный архитектурный контракт для хранения, миграций и epistemic authority.  
**Runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6`.

## 1. Раздельные идентичности

```text
storage profile      = deployment identity
physical L3          = multi-status graph state
strict Canon         = trusted read projection
migration bundle     = operation evidence
retrieval score      = ranking signal
model output         = generated text
Reader artifact      = source-linked candidate/observation
Reader structure     = version-bound document metadata
Reader pass ledger   = version-bound reading-process audit state
Reader proposition   = pre-admission source-linked extracted candidate
```

Ни одна из этих идентичностей автоматически не подразумевает другую. Storage, retrieval, migration, model output, Reader artifacts, structure, pass state и extracted propositions не могут обходить Guardian или TruthGate.

## 2. Durable runtime profile

SQLite — обычный активный local-first профиль. При первом durable выборе `auto` может использоваться опциональный LadybugDB, если он установлен, иначе SQLite. Выбранный backend и несекретная locator identity сохраняются атомарно и повторно используются.

Runtime fail closed при конфликте backend или locator. Он не переключается тихо на эфемерный Mock. Явный Mock остаётся доступным для целенаправленной разработки и CI, когда durable profile не заявляется.

Neo4j — явный опциональный remote/server adapter, расширяющий trust boundary.

## 3. Physical L3 и strict Canon

Physical L3 может содержать verified, user-claimed, unverified, hypothetical, subjective, contested, superseded или restricted records. Erasure удаляет материал active store в рамках реализованного erasure contract; независимые копии требуют отдельной обработки.

Strict Canon — deny-dominant проекция, допускающая только записи, разрешённые текущими evidence и policy.

```text
stored in L3          ≠ trusted answer material
retrieved             ≠ admitted
high score            ≠ evidence
frequent copy         ≠ independent corroboration
Reader card           ≠ admitted fact
structure             ≠ truth/confidence
Reader pass complete  ≠ comprehension or truth
EXTRACTED_PROPOSITION ≠ verified fact
Reader candidate      ≠ admitted evidence
```

## 4. Разделение чтения и записи

Публичные query surfaces проходят через `core.query_pipeline.query()` и остаются read-only относительно canonical truth state.

```text
HTTP /ask
CLI ask
MCP search / inspection
→ read-only retrieval
→ trace / answer / bounded refusal
```

Явный ingest — admission-capable path:

```text
source-linked candidate
→ Guardian
→ TruthGate
→ operational state + physical L3
→ strict read projection
```

Reader RC-1/RC-2/RC-3/RC-4 остаются upstream domain layers. Создание Reader artifact, structural node, pass record или extracted proposition никогда само по себе не выполняет TruthGate admission, не прикрепляет evidence к admitted fact и не меняет canonical truth state.

## 5. Жизненный цикл SQLite

Текущий проверенный local-first lifecycle:

```text
active SQLite store
→ backup
→ independent verification
→ inactive restore
→ bounded logical export
→ deterministic bundle verification
```

Inactive restore и logical export сохраняют состояние для операций. Они не выполняют TruthGate admission и не выбирают другой runtime backend.

## 6. Cross-backend migration

Реализованная фаза переносимости physical L3 поддерживает verified logical bundle и опциональную неактивную PostgreSQL/pgvector target:

```text
completed verified bundle
→ PostgreSQL version / pgvector / TLS preflight
→ fresh inactive target schema
→ serializable import
→ independent read-only canonical re-hash
→ exact count / byte / SHA-256 equivalence
→ non-secret receipt
→ active=false
```

Она покрывает только bounded approved physical-L3 datasets. Она не мигрирует автоматически каждую подсистему, включая всё L1 operational state, audit/outbox state, encryption metadata или deployment configuration.

## 7. Явно отсутствующие lifecycle stages

Не реализованы:

- active PostgreSQL read/write runtime adapter;
- automatic SQLite/PostgreSQL selection или switching;
- source fencing и explicit cutover receipt;
- rollback proof и rollback-expiry policy;
- dual-write;
- accepted exact-vs-ANN production retrieval profile;
- PostgreSQL production backup/restore/upgrade lifecycle;
- production role provisioning, pooling, IdP/multi-tenancy или distributed fencing.

## 8. Source-grounded document ingestion и Reader foundation

Source spans и import-session evidence входят в реализованный baseline. Document records и candidate claims остаются upstream от обычного Guardian и TruthGate admission.

RC-1 реализует ограниченный evidence-linked Reader source/session skeleton с точной привязкой source version/hash, replayable locators, SegmentCards, fidelity classes, coverage states, bookmarks/open loops и stale/failure/privacy semantics. RC-2 реализует bounded caller-supplied Structural Document Map с hierarchy/order, exact-span containment и явной структурой `RECOVERED` / `AMBIGUOUS` / `UNSUPPORTED`.

RC-3 реализует bounded deterministic multi-pass mechanics над OPEN RC-1 ReaderSession и RC-2 structural map той же точной source version. Он записывает пять pass kinds, заранее объявленные structural targets, per-target RC-1 coverage outcomes и pass state (`ATTEMPTED`, `COMPLETED`, `INTERRUPTED`, `DEGRADED`). Один pass активен за раз; interrupted/degraded pass сохраняет уже завершённые region outcomes. Cross-check и targeted re-read требуют prior substantive processing. Unresolved structure допускает только fail-visible `NEEDS_REVIEW`.

RC-4 реализует bounded deterministic proposition candidate registration из completed substantive RC-3 regions. Candidate требует declared target завершённого pass, а recorded outcome и текущий matching coverage должны быть `PROCESSED` или `REVISITED`. Candidate использует fidelity `EXTRACTED_PROPOSITION`, сохраняет primary/supporting replayable locators, source owner, source-presentation category, explicit negation и qualifiers, а также наследует source restriction/sensitivity metadata.

`FACTUAL_ASSERTION` в RC-4 описывает то, как источник подаёт proposition; это не verification result Crystal. RC-4 не вызывает `core.evidence.attach_evidence()`, не пишет `evidence_spans`, не создаёт admitted fact, не меняет `truth_status`/ESM и не устанавливает evidence sufficiency.

```text
coverage != comprehension proof
pass completion != comprehension proof
structure/order/prominence != epistemic authority
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
```

Dedicated/full autonomous Reader / Semantic Reading runtime не реализован. RC-1/RC-2/RC-3/RC-4 не добавляют automatic parser/chunker/OCR, automatic NLP/LLM extraction, provider-driven reader, embeddings/ANN/vector DB, automatic cross-document proposition identity/reasoning engine или planner/belief-update authority.

## 9. Secret и privacy boundary

Credentials и credential-bearing DSNs не должны попадать в profiles, bundles, receipts, logs, issues или Notion. Endpoint identity представляется через non-secret digests.

Migration и backup создают дополнительные копии. Erasure из active store не стирает эти копии автоматически. Операторам нужны inventory, retention и deletion procedures.

Шифрование отдельных полей L1 не является универсальным шифрованием. Reader RC-1/RC-2/RC-3/RC-4 не удерживают source body; производные Reader artifacts, pass records и proposition candidates наследуют source restriction/sensitivity metadata.

## 10. Таблица authority

| Событие | Что оно доказывает | Чего оно не доказывает |
|---|---|---|
| Reader artifact существует | bounded source-linked observation/candidate | truth, admission или comprehension |
| structural node существует | recovered/caller-supplied document metadata | confidence, truth или importance authority |
| Reader pass завершается | declared targets получили явные legal coverage outcomes | comprehension, truth, evidence sufficiency или admission |
| RC-4 proposition candidate существует | caller-supplied proposition привязана к eligible completed substantive Reader context | verified world fact, admitted evidence, confidence или Canon membership |
| record хранится в L3 | physical persistence | strict Canon membership |
| retrieval result | candidate relevance | evidence sufficiency |
| backup verified | backup integrity | claim truth |
| inactive restore verified | restored state integrity | admission или activation |
| PostgreSQL import succeeds | transactional import | runtime selection |
| exact equivalence receipt | approved dataset equality | production readiness или cutover |
| curator override | explicit audited governance action | rewritten TruthGate policy |

## 11. Текущие non-claims

Crystal не заявляет active PostgreSQL runtime, automatic migration, accepted ANN production quality, cutover, rollback, dual-write, production multi-tenancy, distributed exactly-once coordination, завершённый dedicated/full autonomous Reader runtime или automatic NLP proposition extraction, security/legal/GDPR certification или присуждённое финансирование NLnet.

## 12. Подробные английские источники

- [Полная архитектура](../ARCHITECTURE.md)
- [Обзор архитектуры](../ARCHITECTURE_OVERVIEW.md)
- [Архитектурный контракт Reader Core](../architecture/READER_CORE_ARCHITECTURE.md)
- [Durable storage profile](../architecture/DURABLE_STORAGE_PROFILE.md)
- [SQLite lifecycle](../architecture/SQLITE_STORAGE_LIFECYCLE.md)
- [Cross-backend migration contract](../architecture/CROSS_BACKEND_MIGRATION_CONTRACT.md)
- [Inactive PostgreSQL import](../architecture/POSTGRESQL_INACTIVE_IMPORT.md)
- [PostgreSQL/pgvector RFC](../architecture/POSTGRESQL_PGVECTOR_PROFILE_RFC.md)
- [ADR-021](../adr/ADR-021-CROSS-BACKEND-MIGRATION-CONTRACT.md)
