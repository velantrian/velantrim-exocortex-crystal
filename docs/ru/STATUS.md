<!-- translation-source: docs/STATUS.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- rc6-translation-source: docs/STATUS.md@ed96a88369f841bdb2ffd79ca020acef174685fc -->
<!-- rc7-translation-source: docs/STATUS.md@ab3ad31c437647535030e371d58f456faf14017b -->
<!-- rc7-status: CURRENT -->
<!-- current-translation-source: docs/STATUS.md@9666781d390e3276a111cb5ee1735f6606a76283 -->
# 🇷🇺 Crystal — текущий статус

**Дата статуса:** 2026-08-15  
**Текущий signed architecture checkpoint:** `76a9493b8ba64b832472ef9bfc1f1c23ebe6654e`, `verified=true`, reason `valid`  
**Текущий architecture milestone:** Reader Retrieval Typed Inspection Contract v1 — Issue #391 / PR #392 — complete  
**RRTIC exact-head CI:** `31754798549` — 9/9 SUCCESS  
**RRTIC post-merge CI:** `31771677028` — 9/9 SUCCESS  
**Historical RC-7 localization source:** `main@ab3ad31c437647535030e371d58f456faf14017b` — сохраняется как immutable provenance.  
**Historical signed RC-9 implementation baseline:** `main@f8b7d7ea36625b6589a4cf02f12b94c5f98fdb61` — PR #376; post-merge CI `31594027040`.  
**Repository-head rule:** перед операционными действиями всегда разрешать live GitHub; docs-only SHA не следует автоматически считать текущим HEAD.

## Текущая Reader position

RC-1…RC-7 — bounded implemented Reader/domain layers. RC-8 — завершённое architecture/research решение. RC-9 — implemented deterministic lexical PRE-ADMISSION retrieval baseline. Comparator v1 и NLI neutral-filter v1 — completed frozen evaluations с failed admission gates. RRTIC-v1 — текущий frozen architecture contract для typed inspection; runtime stage он не добавляет.

```text
reader_core_rc1_skeleton               = true
reader_core_rc2_structural_map         = true
reader_core_rc3_multi_pass_mechanics   = true
reader_core_rc4_proposition_extraction = true
reader_core_rc5_relation_candidates    = true
reader_core_rc6_long_context_strategy  = true
reader_core_rc7_cross_document_links   = true
reader_rc9_lexical_candidate_discovery = true
dedicated_reader_core                  = false
semantic_hybrid_reader_runtime         = false
rrtic_runtime_authorization            = false
```

RC-5 остаётся implemented в `core/reader_relations.py`. RC-9 остаётся implemented в `core/reader_lexical_discovery.py`.

## Reader evidence chain

```text
RC-9 lexical discovery
        ↓
Evaluation Surface v2
        ↓
Comparator v1
  recall recovered
  hard-negative discrimination FAIL
        ↓
NLI neutral-filter v1
  discrimination improved
  useful-recall safety FAIL
        ↓
post-NLI reassessment
  RELATION-CONTRACT MISMATCH
        ↓
RRTIC-v1
  typed inspection contract only
  runtime_authorization=false
```

## RC-9 deterministic lexical baseline — retained control

| Metric | Result |
|---|---:|
| Recall@5 | 0.937500 |
| Precision@5 | 0.187500 |
| MRR | 0.895833 |
| Paired hard-negative rate@5 | 1.000000 |
| Useful hits | 15 / 16 |
| Hard-negative hits | 4 / 4 |

Classification: `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`.

Эти значения — retrieval measurements, а не semantic/adjudication accuracy.

## Evaluation Surface v2 — frozen evidence

Surface остаётся frozen: 24 queries, 12 primary strata, 6 candidates/query, 144/144 explicit qrels, K=5, composite SHA-256 `753cc550bc5fc47697aa6d7b1cda294bf11abaa08d515816e5e1db59eb526cdd`.

RC-9 control на v2:

| Metric | Result |
|---|---:|
| Useful hits | **42 / 48** |
| Useful Recall@5 | **0.875000** |
| Precision@5 — fixed K slots | **0.350000** |
| Judged precision over returned | **0.355932** |
| MRR | **0.857639** |
| Hard-negative hits | **38 / 48** |
| Hard-negative hit rate@5 | **0.791667** |

Classification: `LEXICAL_CONTROL_EXPOSES_MULTI_STRATUM_GAPS`.

## Comparator v1 — frozen gate FAIL

Pinned multilingual semantic similarity восстановил все useful v2 candidates (`48/48`, Recall@5 `1.0`, MRR `1.0`), но surfaced `41/48` hard negatives.

Classification: `SEMANTIC_RECALL_RECOVERED_DISCRIMINATION_GATE_FAILED`.

Comparator является research evidence, не Reader backend.

## NLI neutral-filter v1 — frozen gate FAIL

Preregistered bidirectional neutral-neutral filter снизил v2 hard negatives с `41/48` до `18/48`, но useful candidates регрессировали до `46/48`; historical useful hits — до `15/16`. Frozen no-recall-loss overlay и admission gate поэтому FAIL.

Classification: `NLI_NEUTRAL_FILTER_GATE_FAILED`.

```text
NLI label         != proposition identity
NLI contradiction != contradiction adjudication
filtering          != epistemic authority
```

## RRTIC-v1 — frozen architecture contract

RRTIC-v1 фиксирует retrieval-side diagnostic envelope после того, как post-NLI reassessment классифицировал missing capability как relation-contract mismatch.

Relation families:

```text
EQUIVALENCE_SUSPECT
RELATED_SUSPECT
CONTRADICTION_SUSPECT
QUALIFICATION_SUSPECT
TOPIC_ONLY_SUSPECT
UNKNOWN
```

Qualifier dimensions:

```text
entity_binding
predicate_binding
argument_roles
polarity
modality_quantifier
temporal_version
jurisdiction
condition_direction
units_thresholds
attribution_causality
```

State: `MATCH | MISMATCH | UNKNOWN | NOT_APPLICABLE`.

RRTIC-v1 не имеет accept/reject policy, scalar truth/confidence score, reranking, model execution, runtime provider, identity decision, evidence admission, contradiction adjudication или Canon mutation.

## Authority boundaries

```text
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
working-set coverage != comprehension proof
summary != source text
summary != evidence
summary != verified fact
summary != Canon admission
cross-document link != Canon relation
same-topic != same proposition
possible-same-claim != claim identity
similarity signal != identity proof
repetition across sources != corroboration
retrieval match != evidence
similarity != identity
ranking != epistemic authority
candidate discovery != candidate adjudication
evaluation pass != runtime authorization
```

Guardian, TruthGate, TrustSnapshot и CanonicalView не изменены. Public `HTTP /ask`, `CLI ask` и `MCP search` остаются read-only admitted-memory query surfaces, а не Reader evaluation/inspection authority interfaces.

## Storage truth

```text
SQLite ordinary active local-first
→ backup / verify / inactive restore
→ bounded logical export
→ PostgreSQL 16 + pgvector inactive import/equivalence
→ active=false
```

Reader SQLite FTS не implemented. Reader ANN/vector DB не введён. Automatic backend switching отсутствует.

## Localization truth

Русская public/Reader-dependent D1/D3/D4/D5 поверхность обновляется в Issue #410 против current repository truth `main@9666781d390e3276a111cb5ee1735f6606a76283`; historical RC-5/6/7 source markers сохранены. Восемь других Reader-dependent locale packs этим milestone не меняются и остаются `REFRESH_NEEDED` там, где это зафиксировано ledger.

## Grant status

NLnet остаётся **submitted / under review / not awarded**. Приблизительно **€50,000** — planning context only. Budget change: none.

## Stop boundary

RRTIC-v1 закрыт. Этот localization refresh не авторизует discriminator/model/runtime implementation, semantic/hybrid/vector Reader runtime, FTS/ANN, PostgreSQL activation, EPIS runtime или изменение epistemic authority.
