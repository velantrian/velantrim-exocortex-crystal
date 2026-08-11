<!-- translation-source: docs/STATUS.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- d1-locale: ru -->
# Velantrim Crystal — текущий статус

**Дата статуса:** 11 августа 2026 года  
**Проверенный runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6`  
**Проверенное дерево:** `f57e58a6f4d1954b649ba324996fcde42ac287b8`  
**Проверенный implementation head:** `d7af7c80722274f9217bc5545d150f92e9363f37`  
**Runtime PR / CI:** #337 / `31256316536`  
**PostgreSQL integration CI:** `31256316532`  
**Reader RC-5 tracking:** issue #367 / PR #368

GitHub merged `main`, executable tests, exact CI и machine-readable implementation manifest остаются implementation truth. Числовой storage/runtime checkpoint ниже — сохранённый исторический evidence; Reader milestones имеют собственные exact-head и post-merge CI evidence.

## Верификация сохранённого runtime checkpoint

- Python 3.11: **2078 passed / 13 skipped / 0 failed**;
- Python 3.12: **2078 passed / 13 skipped / 0 failed**;
- **9756 statements / 100.00% line coverage**;
- `core/postgresql_migration.py`: **44/44 statements**;
- `core/postgresql_migration_impl.py`: **336/336 statements**;
- **7/7** заявленных Ring Zero mutants уничтожены;
- **9/9** постоянных CI jobs успешны;
- **1/1** реальный PostgreSQL/pgvector integration job успешен.

Точные исторические evidence: [`TEST_REPORT.md`](../../TEST_REPORT.md) и [machine-readable manifest](../status/implementation-manifest.json). Reader RC-5 принимается только по собственному exact-head 9/9 CI, guarded merge и post-merge 9/9 CI на точном merge SHA.

## Текущая проверенная storage-граница

Crystal сохраняет local-first SQLite baseline и проверенный неактивный путь PostgreSQL import/equivalence:

```text
проверенный завершённый logical bundle
→ PostgreSQL 16 / pgvector 0.8.2 preflight
→ новая неактивная target schema
→ serializable import
→ независимый read-only canonical target re-hash
→ точная эквивалентность count / byte / SHA-256
→ non-secret receipts
→ active=false
```

PostgreSQL driver — optional extra и lazy-load только для явных операторских команд. Стандартная установка остаётся на pure standard library. Импортированная target не регистрируется в обычной runtime composition и не может обслуживать обычные reads/writes. Import/equivalence не означает activation, automatic switching, cutover, rollback или dual-write.

## Bounded implementation Reader Core

RC-0 — нормативный архитектурный контракт. Пять ограниченных Reader-слоёв образуют текущую pre-admission implementation line:

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

RC-4
→ completed substantive RC-3 pass context
→ source-linked EXTRACTED_PROPOSITION candidate
→ explicit source owner + proposition presentation category
→ explicit negation + scope/exception qualifiers
→ primary + supporting replayable locators
→ count-only extraction telemetry

RC-5
→ один OPEN ReaderSession + один exact SourceVersion
→ только зарегистрированные RC-4 proposition candidate IDs
→ POSSIBLE_CONTRADICTION / EXCEPTION / QUALIFICATION / TENSION
→ exact linkage обеих сторон + pass/node IDs
→ primary + supporting replayable provenance обеих сторон
→ explicit non-empty rationale
→ count-only relation telemetry
```

Machine truth:

```text
reader_core_rc1_skeleton               = true
reader_core_rc2_structural_map         = true
reader_core_rc3_multi_pass_mechanics   = true
reader_core_rc4_proposition_extraction = true
reader_core_rc5_relation_candidates    = true
dedicated_reader_core                  = false
```

### RC-3 process semantics

RC-3 — deterministic orchestration mechanics, а не автономный агент чтения. Он не вызывает model/provider, не обнаруживает структуру сам, не выбирает research objective и не выводит hidden targets. Каждый pass, structural target и region outcome объявляет caller. RC-1 coverage rules остаются authority допустимых coverage transitions.

`CROSS_CHECK` и `TARGETED_REREAD` требуют substantive prior processing; targeted reread требует явный rationale. Pass нельзя завершить, пока каждый declared target не получил legal outcome. Interrupted/degraded pass сохраняет уже полученные outcomes и оставляет пробелы видимыми.

```text
pass completion != comprehension proof
coverage        != comprehension proof
```

### RC-4 proposition candidate boundary

RC-4 — deterministic validation/registration layer, а не automatic NLP/model extractor. Candidate разрешён только из target завершённого (`COMPLETED`) RC-3 pass, если pass outcome и текущий matching coverage равны `PROCESSED` или `REVISITED`. Неопределённая структура, `SEEN`, `NEEDS_REVIEW`, незавершённый pass, source/session mismatch или mismatched provenance завершаются fail closed.

Каждый RC-4 candidate остаётся `SegmentCard` с fidelity `EXTRACTED_PROPOSITION`. `source_owner`, категория подачи proposition, negation и scope/exception qualifiers сохраняются явно. Категории включают factual assertion, author opinion, hypothesis, conditional, example, quoted speech, reported position, definition и uncertain assertion.

`FACTUAL_ASSERTION` означает лишь, что **источник подаёт** высказывание как факт; это не означает, что Crystal его проверил. RC-4 не вызывает `core.evidence.attach_evidence()`, не пишет fact evidence / `evidence_spans`, не устанавливает evidence sufficiency и не выполняет admission.

### RC-5 relation candidate boundary

RC-5 runtime находится в `core/reader_relations.py`. `ReaderRelationRegistry` привязан к одному RC-4 `ReaderPropositionExtractor`, поэтому relation остаётся внутри одного ReaderSession и одного exact SourceVersion. Он принимает только candidate IDs, реально зарегистрированные этим extractor, и повторно проверяет OPEN session, session identity, source version, supporting locator versions и наличие candidate SegmentCard в ReaderSession.

Типы relation deliberately малы:

| Kind | Семантика | Направление | Authority |
|---|---|---|---|
| `POSSIBLE_CONTRADICTION` | явное подозрение на возможный конфликт | symmetric | candidate only |
| `TENSION` | напряжение без утверждения contradiction | symmetric | candidate only |
| `EXCEPTION` | right candidate — исключение к left | directional | candidate only |
| `QUALIFICATION` | right candidate уточняет/сужает left | directional | candidate only |

Для symmetric kinds порядок candidate IDs канонизируется детерминированно. Повторная регистрация той же symmetric semantic pair fail closed и не превращается в corroboration. `EXCEPTION` и `QUALIFICATION` сохраняют направление.

Relation artifact хранит `relation_id`, `session_id`, оба exact RC-4 candidate IDs, pass IDs, structural node IDs, primary/supporting source locators обеих сторон и explicit rationale. Restriction/sensitivity наследуются от exact source context. Telemetry — только counts by kind; truth probability, confidence или evidence sufficiency не вычисляются.

```text
EXTRACTED_PROPOSITION   != verified fact
Reader candidate        != admitted evidence
relation candidate      != admitted evidence
contradiction candidate != confirmed contradiction
similarity              != identity
repetition              != corroboration
```

RC-5 не сравнивает raw source text автоматически, не выполняет semantic equivalence, не выводит cross-document identity, не вызывает LLM/provider, embeddings/ANN или parser/OCR. Он не вызывает существующий contradiction-resolution workflow и не выбирает winner.

## Граница authority

```text
storage profile         = deployment identity
migration bundle        = operation evidence
physical L3             = multi-status storage
strict Canon            = trusted read projection
Reader artifact         = source-linked candidate/observation
Reader structure        = document metadata
Reader pass ledger      = reading-process audit state
Reader proposition      = pre-admission source-linked candidate
Reader relation         = pre-admission relation candidate
migration/import        != TruthGate admission
successful equivalence  != backend activation
Reader coverage         != comprehension proof
Reader pass completion  != comprehension proof
Reader structure        != epistemic authority
EXTRACTED_PROPOSITION   != verified fact
Reader candidate        != admitted evidence
contradiction candidate != confirmed contradiction
```

Guardian, TruthGate, restrictions, TrustSnapshot и CanonicalView остаются неизменными. RC-1/RC-2/RC-3/RC-4/RC-5 не имеют метода или runtime wiring, который меняет `truth_status`/ESM, пишет strict Canon, обходит Guardian/TruthGate, присоединяет fact evidence, повышает confidence, устанавливает evidence sufficiency, разрешает contradictions или создаёт planner/belief-update authority.

## Privacy / persistence boundary

RC-1..RC-5 не удерживают source body. Производные Reader artifacts наследуют exact source restriction/sensitivity context. RC-5 не добавляет durable Reader storage schema, public Reader API/CLI/background worker или PostgreSQL activation.

## Что всё ещё отсутствует

- active PostgreSQL read/write runtime selection;
- exact-vs-ANN retrieval evaluation и accepted ANN thresholds;
- activation, cutover, source/target fencing, rollback или dual-write;
- PostgreSQL backup/restore/upgrade lifecycle, production pooling и distributed fencing;
- production IdP/multi-tenancy и legal/security/GDPR certification;
- automatic Reader parser/semantic chunker/OCR/PDF-layout или multimodal understanding;
- dedicated/full autonomous Reader / Semantic Reading runtime;
- automatic NLP/LLM proposition или contradiction extraction;
- Reader provider/model routing;
- embeddings, ANN/vector database или automatic cross-document proposition identity/reasoning engine;
- automatic evidence attachment к fact или admission Reader candidates;
- automatic contradiction resolution/winner selection;
- planner/autonomous research/belief-update authority.

## Localization truth

Русский root README и Reader-dependent D1/D3/D4/D5 detail docs полностью refreshed к immutable English source checkpoint `51c205fe048fd69d39fcd47b43e042a50de432bc` и имеют `CURRENT`. D2 и Quick Start остаются `CURRENT` во всех 9 locale. Восемь других Reader-dependent locale packs сохраняют rich предыдущие переводы и имеют `REFRESH_NEEDED`; tracked debt = 64 docs.

## Статус гранта

NLnet остаётся **submitted / under review / not awarded**. Приблизительно **€50,000** — planning only, не approved budget и не payment commitment. **Budget change: none.** RC-0/RC-1/RC-2/RC-3/RC-4/RC-5, merged до любого grant agreement, являются existing pre-agreement baseline и не могут повторно считаться future funded delta.
