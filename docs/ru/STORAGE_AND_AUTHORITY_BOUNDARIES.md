<!-- translation-source: docs/STORAGE_AND_AUTHORITY_BOUNDARIES.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
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
# Границы хранения и authority

**Дата статуса:** 11 августа 2026 года  
**Назначение:** стабильный архитектурный контракт для storage, migrations и epistemic authority.  
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
Reader relation      = pre-admission relation candidate
```

Ни одна из этих идентичностей автоматически не подразумевает другую. Storage, retrieval, migration, model output и Reader layers не могут обходить Guardian или TruthGate.

## 2. Durable runtime profile

SQLite — ordinary active local-first profile. Existing optional local/remote adapters не меняют authority. Runtime fail closed при конфликте durable backend/locator identity и не переключается тихо на ephemeral Mock. Explicit Mock остаётся development/CI state. Neo4j — explicit optional remote/server adapter, расширяющий trust boundary.

## 3. Physical L3 и strict Canon

Physical L3 может содержать verified, user-claimed, unverified, hypothetical, subjective, contested, superseded или restricted records. Strict Canon — deny-dominant projection, допускающая только material, разрешённый current evidence/policy.

```text
stored in L3           != trusted answer material
retrieved              != admitted
high score             != evidence
frequent copy          != independent corroboration
Reader card            != admitted fact
structure              != truth/confidence
Reader pass complete   != comprehension or truth
EXTRACTED_PROPOSITION  != verified fact
Reader candidate       != admitted evidence
relation candidate     != admitted evidence
contradiction candidate != confirmed contradiction
```

## 4. Разделение чтения и записи

Public query surfaces проходят через `core.query_pipeline.query()` и остаются read-only относительно canonical truth state:

```text
HTTP /ask
CLI ask
MCP search / inspection
→ read-only retrieval
→ trace / answer / bounded refusal
```

Explicit ingest — admission-capable path:

```text
source-linked candidate
→ Guardian
→ TruthGate
→ operational state + physical L3
→ strict read projection
```

Reader RC-1..RC-5 остаются upstream domain layers. Создание Reader artifact, structure, pass record, proposition или relation candidate само по себе не выполняет TruthGate admission, не прикрепляет evidence к admitted fact и не меняет canonical truth state.

## 5. Жизненный цикл SQLite

```text
active SQLite store
→ backup
→ independent verification
→ inactive restore
→ bounded logical export
→ deterministic bundle verification
```

Inactive restore/logical export сохраняют state для operator operations. Они не выполняют TruthGate admission и не выбирают другой runtime backend.

## 6. Cross-backend migration

Реализованная portability phase поддерживает verified logical bundle и optional inactive PostgreSQL/pgvector target:

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

Она покрывает bounded approved physical-L3 datasets. Она не мигрирует автоматически весь L1 operational/audit/outbox/encryption/deployment state.

## 7. Явно отсутствующие lifecycle stages

Не реализованы:

- active PostgreSQL read/write runtime adapter;
- automatic SQLite/PostgreSQL selection или switching;
- source fencing и explicit cutover receipt;
- rollback proof и expiry policy;
- dual-write;
- accepted exact-vs-ANN production retrieval profile;
- PostgreSQL production backup/restore/upgrade lifecycle;
- production roles/pooling/IdP/multi-tenancy/distributed fencing.

## 8. Source-grounded ingestion и Reader foundation

Source spans/import-session evidence входят в baseline. Document records и candidates остаются upstream от Guardian/TruthGate admission.

RC-1 реализует evidence-linked source/session skeleton: exact version/hash, replayable locators, SegmentCards, fidelity, coverage, bookmarks/open loops, stale/failure/privacy semantics.

RC-2 реализует caller-supplied Structural Document Map с hierarchy/order, exact-span containment и `RECOVERED` / `AMBIGUOUS` / `UNSUPPORTED`.

RC-3 реализует deterministic multi-pass mechanics над OPEN RC-1 session и same-source RC-2 map: five pass kinds, declared targets, per-target coverage outcomes, pass states `ATTEMPTED`, `COMPLETED`, `INTERRUPTED`, `DEGRADED`, one active pass, partial progress preservation, prior-processing gates и fail-visible `NEEDS_REVIEW` для unresolved structure.

RC-4 реализует deterministic proposition candidate registration из completed substantive RC-3 regions. Candidate требует declared target и `PROCESSED`/`REVISITED` recorded+current coverage, uses `EXTRACTED_PROPOSITION`, preserves primary/supporting locators, source owner, presentation category, negation/qualifiers и inherits restriction/sensitivity.

RC-5 реализует deterministic relation candidate registration поверх valid RC-4 candidates в одном OPEN ReaderSession и exact SourceVersion. `ReaderRelationRegistry` сохраняет обе стороны relation — exact candidate/pass/node IDs, primary/supporting locators — и explicit rationale. Unknown, stale, detached или mismatched artifacts fail closed.

```text
POSSIBLE_CONTRADICTION = symmetric candidate suspicion only
TENSION                = symmetric tension only
EXCEPTION              = directional right→left limiting relation
QUALIFICATION          = directional right→left refinement relation
```

RC-5 symmetric relations canonicalize candidate-ID pair order; duplicate pair does not create corroboration. No truth probability/confidence/evidence-sufficiency/winner field exists.

`FACTUAL_ASSERTION` в RC-4 описывает source presentation, не Crystal verification. RC-4/RC-5 не вызывают `core.evidence.attach_evidence()`, не пишут `evidence_spans`, не создают admitted fact, не меняют `truth_status`/ESM и не выполняют TruthGate admission.

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

Dedicated/full autonomous Reader не реализован. RC-1..RC-5 не добавляют automatic parser/chunker/OCR/PDF layout, NLP/LLM/provider-driven Reader, embeddings/ANN/vector DB, automatic semantic equivalence, cross-document identity/reasoning, contradiction resolution или planner/belief-update authority.

## 9. Secret и privacy boundary

Credentials/credential-bearing DSNs не должны попадать в profiles, bundles, receipts, logs, issues или Notion. Endpoint identity использует non-secret digests.

Migration/backup создают дополнительные copies. Erasure active store не стирает их автоматически; нужны operator inventory/retention/deletion procedures.

Field-level L1 encryption не является universal encryption. RC-1..RC-5 не удерживают source body; derived artifacts inherit source restriction/sensitivity.

## 10. Таблица authority

| Событие | Что доказывает | Чего не доказывает |
|---|---|---|
| Reader artifact exists | bounded source-linked observation/candidate | truth/admission/comprehension |
| structural node exists | caller-supplied document metadata | confidence/truth/importance |
| Reader pass completes | declared targets получили legal outcomes | comprehension/truth/evidence sufficiency/admission |
| RC-4 proposition candidate exists | proposition anchored to eligible completed substantive Reader context | verified fact/admitted evidence/confidence/Canon |
| RC-5 relation candidate exists | caller registered auditable relation suspicion between valid RC-4 candidates | confirmed contradiction/winner/evidence sufficiency/truth/Canon |
| record stored in L3 | physical persistence | strict Canon membership |
| retrieval result | candidate relevance | evidence sufficiency |
| backup verified | backup integrity | claim truth |
| inactive restore verified | restored-state integrity | admission/activation |
| PostgreSQL import succeeds | transactional import | runtime selection |
| exact equivalence receipt | approved dataset equality | production readiness/cutover |
| curator override | explicit audited governance action | rewritten TruthGate policy |

## 11. Текущие non-claims

Crystal не заявляет active PostgreSQL runtime, automatic migration/switching, accepted ANN production quality, cutover/rollback/dual-write, production multi-tenancy, distributed exactly-once coordination, dedicated/full autonomous Reader runtime, automatic NLP/LLM contradiction detection/resolution, semantic cross-document identity, security/legal/GDPR certification или awarded NLnet funding.

## 12. Подробные English sources

- [Полная архитектура](../ARCHITECTURE.md)
- [Architecture overview](../ARCHITECTURE_OVERVIEW.md)
- [Reader Core architecture contract](../architecture/READER_CORE_ARCHITECTURE.md)
- [Durable storage profile](../architecture/DURABLE_STORAGE_PROFILE.md)
- [SQLite lifecycle](../architecture/SQLITE_STORAGE_LIFECYCLE.md)
- [Cross-backend migration contract](../architecture/CROSS_BACKEND_MIGRATION_CONTRACT.md)
- [Inactive PostgreSQL import](../architecture/POSTGRESQL_INACTIVE_IMPORT.md)
- [PostgreSQL/pgvector RFC](../architecture/POSTGRESQL_PGVECTOR_PROFILE_RFC.md)
- [ADR-021](../adr/ADR-021-CROSS-BACKEND-MIGRATION-CONTRACT.md)
