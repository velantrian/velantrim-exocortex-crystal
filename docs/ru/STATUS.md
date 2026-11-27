<!-- translation-source: docs/STATUS.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- rc6-translation-source: docs/STATUS.md@ed96a88369f841bdb2ffd79ca020acef174685fc -->
<!-- rc7-translation-source: docs/STATUS.md@ab3ad31c437647535030e371d58f456faf14017b -->
<!-- rc7-status: CURRENT -->
<!-- current-translation-source: docs/STATUS.md@9666781d390e3276a111cb5ee1735f6606a76283 -->
<!-- truthgate-v1-source: docs/STATUS.md@b4be6831a8b9f87cea815b6a0ef2c497a2d5059a -->
<!-- truthgate-v1-status: CURRENT -->
# 🇷🇺 Crystal — текущий статус

**Дата статуса:** 2026-08-15  
**Текущий signed architecture checkpoint:** `76a9493b8ba64b832472ef9bfc1f1c23ebe6654e`, `verified=true`, reason `valid`  
**Current architecture milestone:** Reader Retrieval Typed Inspection Contract v1 — Issue #391 / PR #392 — complete  
**RRTIC exact-head CI:** `31754798549` — 9/9 SUCCESS  
**RRTIC post-merge CI:** `31771677028` — 9/9 SUCCESS  
**Historical RC-7 localization source:** `main@ab3ad31c437647535030e371d58f456faf14017b`.

## TruthGate v1 — сверка после PR #440

Эта D1-страница повторно сверена с материальным изменением английской политики в `main@b4be6831a8b9f87cea815b6a0ef2c497a2d5059a`. Политика TruthGate по умолчанию для `WORLD_FACT` теперь фиксирована и версионирована: `DEFAULT_MIN_CONFIDENCE = 0.05`, `TRUTH_GATE_POLICY_VERSION = "truth-gate-v1-fixed-0.05"`. Локальная для процесса адаптация остаётся телеметрией/исследовательским поведением и не может незаметно менять полномочия admission по умолчанию. Это уточнение не активирует Reader/RAG/retrieval runtime, PostgreSQL/pgvector, не расширяет Canon и не передаёт Crystal полномочия Titan. Более ранние translation-source markers ниже/выше сохраняются как историческое provenance.

> 📎 Retained runtime evidence ниже — historical compatibility evidence, а не текущий repository test count.

```text
bbd816c09dd39a02e6de6c1014438490572f40f6
2078 passed / 13 skipped / 0 failed
9756 statements / 100.00% line coverage
```

## Current Reader position

```text
reader_core_rc1_skeleton = true
reader_core_rc2_structural_map = true
reader_core_rc3_multi_pass_mechanics = true
reader_core_rc4_proposition_extraction = true
reader_core_rc5_relation_candidates = true
reader_core_rc6_long_context_strategy = true
reader_core_rc7_cross_document_links = true
reader_rc9_lexical_candidate_discovery = true
dedicated_reader_core = false
semantic_hybrid_reader_runtime = false
rrtic_runtime_authorization = false
```

RC-1…RC-7 — implemented bounded Reader layers. RC-8 — completed retrieval architecture/research decision. RC-9 — implemented deterministic lexical PRE-ADMISSION discovery. Comparator v1 и NLI neutral-filter v1 — completed frozen evaluations с failed gates. RRTIC-v1 — frozen typed-inspection architecture contract без runtime provider.

## Evidence chain

```text
RC-9 lexical discovery
        ↓
Evaluation Surface v2
        ↓
Comparator v1
recall recovered · discrimination FAIL
        ↓
NLI neutral-filter v1
discrimination improved · recall-safety FAIL
        ↓
post-NLI reassessment
relation-contract mismatch
        ↓
RRTIC-v1
architecture contract only
```

Retained RC-9 historical K=5 control: Recall@5 `0.937500`, Precision@5 `0.187500`, MRR `0.895833`, useful hits `15/16`, hard-negative hits `4/4`; classification `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`.

Comparator v1 classification: `SEMANTIC_RECALL_RECOVERED_DISCRIMINATION_GATE_FAILED`. NLI v1 classification: `NLI_NEUTRAL_FILTER_GATE_FAILED`.

## RRTIC-v1

RRTIC-v1 фиксирует suspicion-only relation families `EQUIVALENCE_SUSPECT`, `RELATED_SUSPECT`, `CONTRADICTION_SUSPECT`, `QUALIFICATION_SUSPECT`, `TOPIC_ONLY_SUSPECT`, `UNKNOWN` и qualifier states `MATCH | MISMATCH | UNKNOWN | NOT_APPLICABLE`.

Он не выполняет model execution, filtering, reranking, identity decision, evidence admission, contradiction adjudication или Canon mutation.

## Authority boundaries

```text
coverage != comprehension proof
pass completion != comprehension proof
working-set coverage != comprehension proof
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
summary != evidence
cross-document link != Canon relation
same-topic != same proposition
possible-same-claim != claim identity
similarity signal != identity proof
repetition across sources != corroboration
retrieval match != evidence
similarity != identity
ranking != epistemic authority
candidate discovery != candidate adjudication
NLI label != proposition identity
RRTIC suspicion != adjudicated relation
evaluation pass != runtime authorization
```

Guardian, TruthGate, TrustSnapshot и CanonicalView остаются отдельными authority/read surfaces. Public `HTTP /ask`, `CLI ask`, `MCP search` read-only.

## Storage / grant / localization

SQLite ordinary active local-first. PostgreSQL/pgvector inactive `active=false`; automatic backend switching отсутствует.

NLnet **submitted / not selected / not awarded**; ~€50,000 planning only; budget change none.

Русская current parity refresh привязана к `main@9666781d390e3276a111cb5ee1735f6606a76283`, а historical RC-5/6/7 markers остаются immutable provenance. Остальные восемь locale packs этим milestone не меняются.
### NLnet grant-only update

> Grant-only update; the full translation checkpoint remains historical and is not being declared newly current.

```text
proposal: submitted
submitted: true
under_review: false
awarded: false
status: submitted / not selected / not awarded
review: completed
decision: NOT_SELECTED
award status: NOT_AWARDED
decision date: 2026-10-09
```

<!-- post-v1-parity-audit: 2026-11-27; code-base: 78088e029b86d8f923178d19e9cecabd650a4f61; english-doc-source: 90f423b53ffdc364680a5e49b9ffa70e853413f9 -->
## 🧩 Дополнения после V1

Reader Product Bridge v0.1 и локальные источники UTF-8 (TXT/Markdown) и PDF v0.1 реализованы (#455, #457, #458). Это ограниченные компоненты чтения до допуска: они не разрешают семантическое выполнение моделей, допуск свидетельств, запись в Canon или production.

Для обоснования публичного фактического ответа `VERIFIED` требует актуального пригодного к воспроизведению свидетельства, привязанного к точному утверждению, разрешённому `TrustSnapshot` (#464). Совпадение ID, прежний вердикт или квитанция недостаточны; потеря поддержки не доказывает ложность. Исторические решения не переписываются.

#507/#505 сверяет L0 с общей SQLite L1 при каждом `get_fact()`; #512 изолирует возвращаемые данные глубоким копированием и закрывает соединение при ошибке схемы; #513 отклоняет обычный повторный ingest уже restricted-записи до записи; #511 проверяет tombstone перед разрешением результата канонического поиска. Это ограниченные исправления: начатые ранее чтения, гонка ограничения и записи, другие пути, восстановление и независимые копии не покрыты полностью. Каскад следует только зарегистрированным `DERIVED_FROM`; полнота происхождения и прерывания остаются открытыми (#504). Завершение V1 и зелёный CI не доказывают отсутствие дефектов, юридическое соответствие или production-авторизацию.

[Английский источник](../STATUS.md)
