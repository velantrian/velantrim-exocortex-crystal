# 🧭 Статус реализации: Crystal и будущая работа Exo-Cortex

<!-- translation-source: docs/IMPLEMENTATION_STATUS.md@6b45bdd196eb42dea7bc30f58d69799b4b1712f2 -->
<!-- translation-status: CURRENT -->
<!-- d1-locale: ru -->

**Дата статуса:** 10 августа 2026 года  
**Проверенный runtime checkpoint:** `bbd816c` / PR #337  
**Точные evidence:** [TEST_REPORT.md](../../TEST_REPORT.md)  
**Machine-readable status:** [implementation-manifest.json](../status/implementation-manifest.json)

| Компонент | Статус | Текущая граница |
|---|---|---|
| Guardian / TruthGate / strict read projection | Реализовано | storage, migration и Reader artifacts не обходят authority |
| Read-only HTTP/CLI/MCP query boundary | Реализовано | обычные queries не изменяют Canon |
| SQLite backup/verify/inactive restore | Реализовано и протестировано | restore неактивен и не является admission |
| Bounded-streaming SQLite logical export/verify | Реализовано и протестировано | canonical backend-neutral bundle |
| PostgreSQL optional dependency и preflight | Реализовано и протестировано | explicit extra, lazy load, поддерживаемые pinned versions |
| Inactive PostgreSQL/pgvector import | Реализовано и протестировано | только новая неактивная schema; обычных reads/writes нет |
| Exact target-state equivalence | Реализовано и протестировано | approved bundle datasets; независимый read-only re-hash |
| Active PostgreSQL runtime adapter | Не реализовано | target не зарегистрирован в normal runtime composition |
| Automatic SQLite/PostgreSQL switching | Запрещено | availability и import success не являются selection |
| Exact-vs-ANN retrieval evaluation | Не реализовано | отдельная будущая фаза |
| Cutover / rollback / dual-write | Не реализовано | только отдельные явно проверяемые фазы |
| PostgreSQL server lifecycle | Не реализовано | backup/restore/upgrade/pooling остаются будущей работой |
| Reader Core RC-0 architecture contract | Документирован | нормативный architecture/authority baseline |
| Reader Core RC-1 minimal evidence-linked skeleton | Реализован и протестирован | `core/reader_core.py`; source/version/locator, fidelity, coverage, bookmarks/open loops, stale/failure/privacy; без admission side effects |
| Reader Core RC-2 Structural Document Map | Реализован и протестирован | `core/reader_structure.py`; caller-supplied version-bound hierarchy/order/ambiguity; без parser и admission side effects |
| Dedicated multi-pass Reader Core / Semantic Reading runtime | Не реализован | нет parser/orchestration/model/vector runtime; `dedicated_reader_core=false` |

## Текущая storage sequence

```text
SQLite lifecycle
→ backup / independent verify / inactive restore

logical portability
→ bounded canonical bundle
→ PostgreSQL preflight
→ inactive transactional import
→ independent exact-state equivalence
→ non-secret receipts
```

Issues #331 и #332 реализованы PR #335 и PR #337. Обычная установка остаётся
на стандартной библиотеке Python; PostgreSQL support — optional operator path.
`active=false` закреплён в target control state, а successful equivalence не
может активировать backend или изменить Guardian, TruthGate либо strict Canon.

## Реализованная граница query path

```text
HTTP /ask
CLI ask
MCP search
    ↓
core.query_pipeline.query()
    ↓
strict read-only canonical projection
```

Эти публичные query surfaces не выполняют admission-capable writes.
Явный `ingest` остаётся отдельным write path.

## Reader Core — реализованная bounded-граница

RC-1 и RC-2 — не «полный Reader», а две проверенные foundation-фазы:

```text
SourceVersion(document_id + source_uri + SHA-256)
→ SourceLocator(exact span / replayable structural locator)
→ ReaderSession
   ├─ SegmentCard + SourceFidelity
   ├─ CoverageEntry / CoverageTelemetry
   ├─ ReaderBookmark
   └─ OpenLoop

SourceVersion + SourceLocator
→ DocumentStructuralMap
   ├─ StructuralNode(kind + order + parent)
   ├─ RECOVERED / AMBIGUOUS / UNSUPPORTED
   ├─ cycle / missing-parent / duplicate validation
   ├─ exact-span containment validation
   └─ immutable traversal + structural telemetry
```

Machine truth:

```text
reader_core_rc1_skeleton = true
reader_core_rc2_structural_map = true
dedicated_reader_core = false
```

Reader artifacts не могут менять `truth_status`/ESM, писать strict Canon, обходить Guardian/TruthGate, разрешать contradictions или становиться planner/belief-update authority. RC-1/RC-2 не хранят source body и не добавляют durable Reader storage schema, публичный Reader API/CLI/background worker, LLM/provider integration, embeddings, ANN/vector DB или multi-pass orchestration. `coverage != comprehension proof`; structural position/order/prominence — metadata, а не truth/confidence authority.

## Будущая работа

```text
exact-vs-ANN retrieval evaluation
→ explicit cutover + source/target fencing
→ rollback proof + expiry policy
→ PostgreSQL backup/restore/upgrade lifecycle
→ multi-process concurrency + production observability
```

Отдельно остаются production IdP/multi-tenancy, supply-chain release evidence и следующий отдельно bounded Reader milestone — RC-3 explicit multi-pass reading mechanics. RC-3 ещё не начат и не является implementation authority.

## Чего Crystal не заявляет

Crystal не заявляет:

- active PostgreSQL runtime backend;
- automatic migration или automatic backend switching;
- production multi-tenancy;
- universal truth или zero hallucinations;
- legal, GDPR или security certification;
- automatic Reader parser/OCR или multimodal comprehension;
- Reader LLM/provider orchestration, embeddings/ANN/vector DB;
- completed dedicated multi-pass Reader Core;
- consciousness.

NLnet остаётся `submitted / under review / not awarded`; приблизительно €50,000 — planning only, budget change none. RC-0/RC-1/RC-2, смерженные до соглашения, являются existing baseline и не могут повторно считаться future funded delivery.

## Authority переводов

Этот документ — поддерживаемая русская публичная поверхность. При расхождении
приоритет имеют merged GitHub code, exact CI, [TEST_REPORT.md](../../TEST_REPORT.md),
[machine-readable manifest](../status/implementation-manifest.json) и английский
[IMPLEMENTATION_STATUS.md](../IMPLEMENTATION_STATUS.md). Native-speaker editorial certification не заявляется.
