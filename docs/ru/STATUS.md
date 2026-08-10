<!-- translation-source: docs/STATUS.md@6b45bdd196eb42dea7bc30f58d69799b4b1712f2 -->
<!-- translation-status: CURRENT -->
<!-- d1-locale: ru -->
# Velantrim Crystal — текущий статус

**Дата статуса:** 10 августа 2026 года  
**Проверенный runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6`  
**Проверенное дерево:** `f57e58a6f4d1954b649ba324996fcde42ac287b8`  
**Проверенный implementation head:** `d7af7c80722274f9217bc5545d150f92e9363f37`  
**Runtime PR / CI:** #337 / `31256316536`  
**PostgreSQL integration CI:** `31256316532`

## Верификация

- Python 3.11: **2078 passed / 13 skipped / 0 failed**;
- Python 3.12: **2078 passed / 13 skipped / 0 failed**;
- **9756 statements / 100.00% line coverage**;
- `core/postgresql_migration.py`: **44/44 statements**;
- `core/postgresql_migration_impl.py`: **336/336 statements**;
- **7/7** заявленных Ring Zero mutants уничтожены;
- **9/9** постоянных CI jobs успешны;
- **1/1** реальный PostgreSQL/pgvector integration job успешен.

Точные evidence: [`TEST_REPORT.md`](../../TEST_REPORT.md) и
[machine-readable manifest](../status/implementation-manifest.json).

## Текущая проверенная граница возможностей

Crystal сохраняет local-first SQLite baseline и проверенный неактивный путь PostgreSQL import/equivalence:

```text
проверенный завершённый logical bundle
→ PostgreSQL 16 / pgvector 0.8.2 preflight
→ новая неактивная target schema
→ serializable import
→ независимый read-only canonical target re-hash
→ точная эквивалентность count / byte / SHA-256
→ non-secret receipts
```

PostgreSQL driver — optional extra и lazy-load только для явных операторских команд. Стандартная установка остаётся на pure standard library. Импортированная target не регистрируется в обычной runtime composition, остаётся `active=false` и не может обслуживать обычные reads или writes.

## Bounded implementation Reader Core

RC-0 — нормативный архитектурный контракт. Два ограниченных implementation milestone теперь смержены и протестированы:

```text
RC-1
→ SourceVersion / SourceLocator
→ ReaderSession / SegmentCard
→ fidelity classes + coverage states
→ bookmarks / open loops
→ stale, failure и privacy semantics

RC-2
→ caller-supplied DocumentStructuralMap
→ version-bound nodes, hierarchy и document order
→ exact-span containment
→ RECOVERED / AMBIGUOUS / UNSUPPORTED
→ structural traversal / telemetry
```

Machine truth отличает эти foundation-слои от более крупной Reader capability:

```text
reader_core_rc1_skeleton       = true
reader_core_rc2_structural_map = true
dedicated_reader_core          = false
```

RC-1/RC-2 не удерживают source body и не добавляют durable Reader storage schema, public API/CLI/background worker, LLM/provider integration, embeddings/ANN/vector DB или multi-pass orchestration. У них нет метода или runtime wiring, который меняет `truth_status`/ESM, пишет strict Canon, обходит Guardian/TruthGate, разрешает contradictions или создаёт planner/belief-update authority. `coverage != comprehension proof`; structural position/order/prominence — metadata, а не truth/confidence authority.

## Граница authority

```text
storage profile         = deployment identity
migration bundle        = operation evidence
physical L3             = multi-status storage
strict Canon            = trusted read projection
Reader artifact         = source-linked candidate/observation
Reader structure        = document metadata
migration/import        != TruthGate admission
successful equivalence  != backend activation
Reader coverage         != comprehension proof
Reader structure        != epistemic authority
```

Guardian, TruthGate, restrictions, TrustSnapshot и CanonicalView остаются неизменными.

## Что всё ещё отсутствует

- active PostgreSQL read/write runtime selection;
- exact-vs-ANN retrieval evaluation и accepted ANN thresholds;
- activation, cutover, source/target fencing, rollback или dual-write;
- PostgreSQL backup/restore/upgrade lifecycle, production pooling и distributed fencing;
- production IdP/multi-tenancy и legal/security/GDPR certification;
- automatic Reader parser/semantic chunker/OCR/PDF-layout или multimodal understanding;
- dedicated multi-pass Reader orchestration / Semantic Reading runtime;
- Reader LLM/provider, embeddings, ANN/vector database или cross-document reasoning engine.

## Статус гранта

Проект подан и находится на рассмотрении. **Award или budget change не заявляются.** PR #337,
Reader RC-0/RC-1/RC-2 и другая работа, смерженная до любого соглашения, являются existing baseline и не могут повторно считаться future funded delta. Будущее финансирование должно начинаться с отдельно рассмотренной работы за пределами проверенного pre-agreement baseline.
