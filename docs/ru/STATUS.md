<!-- translation-source: docs/STATUS.md@0c3d537831e4f1cb5a43d61bc2cbc8b05c080df5 -->
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

Эти числовые значения остаются сохранённым runtime checkpoint PR #337. Reader milestones, смерженные позже, имеют собственные exact-head и post-merge CI evidence и не переписывают исторический checkpoint.

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

RC-0 — нормативный архитектурный контракт. Три ограниченных слоя Reader теперь представлены в RC-3 implementation и должны приниматься только с собственным exact CI evidence:

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

RC-3
→ ORIENTATION / BROAD_READ / FOCUSED_READ
→ CROSS_CHECK / TARGETED_REREAD
→ один active pass за раз
→ ATTEMPTED / COMPLETED / INTERRUPTED / DEGRADED pass ledger
→ заранее объявленные structural targets
→ явные per-region coverage outcomes
→ сохранение partial progress при interruption/degradation
→ count-only pass telemetry
```

Machine truth отличает эти bounded-слои от более крупной Reader capability:

```text
reader_core_rc1_skeleton = true
reader_core_rc2_structural_map = true
reader_core_rc3_multi_pass_mechanics = true
dedicated_reader_core = false
```

RC-3 — deterministic orchestration mechanics, а не автономный агент чтения. Он не вызывает модель/provider, не обнаруживает структуру сам, не выбирает собственную research objective и не выводит скрытые targets. Каждый pass, structural targets и region outcomes объявляет caller. RC-1 coverage rules остаются authority для допустимых переходов coverage.

`CROSS_CHECK` и `TARGETED_REREAD` требуют prior substantive processing. Targeted re-read требует явного rationale. Unresolved RC-2 structure может оставаться только fail-visible через `NEEDS_REVIEW`. Завершение pass означает лишь, что все объявленные targets получили явные допустимые outcomes.

RC-1/RC-2/RC-3 не удерживают source body и не добавляют durable Reader storage schema, public API/CLI/background worker, parser/chunker/OCR/PDF-layout engine, LLM/provider-driven Reader, embeddings/ANN/vector DB или automatic cross-document reasoning. У них нет метода или runtime wiring, который меняет `truth_status`/ESM, пишет strict Canon, обходит Guardian/TruthGate, разрешает contradictions или создаёт planner/belief-update authority.

```text
coverage != comprehension proof
pass completion != comprehension proof
structure/order/prominence != epistemic authority
```

## Граница authority

```text
storage profile         = deployment identity
migration bundle        = operation evidence
physical L3             = multi-status storage
strict Canon            = trusted read projection
Reader artifact         = source-linked candidate/observation
Reader structure        = document metadata
Reader pass ledger      = reading-process audit state
migration/import        != TruthGate admission
successful equivalence  != backend activation
Reader coverage         != comprehension proof
Reader pass completion  != comprehension proof
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
- dedicated/full autonomous Reader / Semantic Reading runtime;
- Reader LLM/provider-driven agent, embeddings, ANN/vector database или automatic cross-document reasoning engine;
- planner/autonomous research/belief-update authority.

## Статус гранта

Проект подан и находится на рассмотрении. **Award или budget change не заявляются.** PR #337,
Reader RC-0/RC-1/RC-2 и RC-3, если он будет смержен до любого соглашения, являются existing baseline и не могут повторно считаться future funded delta. Будущее финансирование должно начинаться с отдельно рассмотренной работы за пределами проверенного pre-agreement baseline.
