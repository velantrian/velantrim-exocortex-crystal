<!-- translation-source: docs/IMPLEMENTATION_STATUS.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- rc6-translation-source: docs/IMPLEMENTATION_STATUS.md@ed96a88369f841bdb2ffd79ca020acef174685fc -->
<!-- rc7-translation-source: docs/IMPLEMENTATION_STATUS.md@ab3ad31c437647535030e371d58f456faf14017b -->
<!-- rc7-status: CURRENT -->
<!-- current-translation-source: docs/IMPLEMENTATION_STATUS.md@9666781d390e3276a111cb5ee1735f6606a76283 -->
# 🇷🇺 Crystal — Implementation Status

**Текущий signed architecture checkpoint:** `main@76a9493b8ba64b832472ef9bfc1f1c23ebe6654e` / PR #392; post-merge CI `31771677028` — 9/9 SUCCESS.  
**Historical RC-7 localization source:** `main@ab3ad31c437647535030e371d58f456faf14017b`.  
**Signed RC-9 implementation baseline:** `main@f8b7d7ea36625b6589a4cf02f12b94c5f98fdb61` / PR #376; post-merge CI `31594027040`.  
**Latest completed model-backed evaluation:** NLI neutral-filter v1 / PR #389 — frozen gate FAIL.  
**Current frozen architecture contract:** RRTIC-v1 / Issue #391 / PR #392 — no runtime authorization.

## Реально implemented Reader capabilities

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

| Capability | Status | Primary implementation / meaning |
|---|---|---|
| RC-1 source/session skeleton | **IMPLEMENTED** | `core/reader_core.py` |
| RC-2 structural map | **IMPLEMENTED** | `core/reader_structure.py` |
| RC-3 multi-pass mechanics | **IMPLEMENTED** | `core/reader_passes.py` |
| RC-4 proposition extraction | **IMPLEMENTED** | `core/reader_extraction.py` |
| RC-5 relation candidates | **IMPLEMENTED** | `core/reader_relations.py` |
| RC-6 bounded long-context strategy | **IMPLEMENTED** | `core/reader_long_context.py` |
| RC-7 explicit cross-document candidate links | **IMPLEMENTED** | `core/reader_cross_document.py` |
| RC-9 lexical candidate discovery | **IMPLEMENTED** | `core/reader_lexical_discovery.py` |
| Dedicated/full autonomous Reader | **NOT IMPLEMENTED** | `dedicated_reader_core=false` |
| Semantic/hybrid Reader runtime | **NOT AUTHORIZED / NOT IMPLEMENTED** | — |
| Reader FTS / ANN / vector DB | **NOT AUTHORIZED / NOT IMPLEMENTED** | — |
| NLI runtime filter / CrossEncoder reranker | **NOT AUTHORIZED / NOT IMPLEMENTED** | — |
| RRTIC runtime provider | **NOT AUTHORIZED / NOT IMPLEMENTED** | — |

## Research/evaluation evidence — не implementation

| Evidence / contract | Result | Runtime meaning |
|---|---|---|
| RC-8 retrieval decision | architecture/research complete | deterministic lexical baseline selected first |
| Evaluation Surface v2 | frozen judged surface | no runtime added |
| Comparator v1 | `SEMANTIC_RECALL_RECOVERED_DISCRIMINATION_GATE_FAILED` | semantic comparator rejected as runtime authorization |
| NLI neutral-filter v1 | `NLI_NEUTRAL_FILTER_GATE_FAILED` | filter rejected as Reader retrieval stage |
| RRTIC-v1 | frozen typed inspection architecture contract | no model/filter/reranker/provider added |

## RC-9 retained evidence

- Recall@5 `0.937500`;
- Precision@5 `0.187500`;
- MRR `0.895833`;
- paired hard-negative rate@5 `1.000000`;
- useful hits `15/16`;
- hard-negative hits `4/4`;
- classification `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`.

Это retrieval measurements, не semantic/adjudication accuracy.

## Evaluation Surface v2

Frozen surface: 24 queries, 12 primary strata ×2, 6 candidates/query, 144/144 explicit qrels, judgment coverage `1.0`, K=5, SHA-256 `753cc550bc5fc47697aa6d7b1cda294bf11abaa08d515816e5e1db59eb526cdd`.

RC-9 v2 control:

- useful hits **42 / 48**;
- Recall@5 **0.875000**;
- fixed-slot Precision@5 **0.350000**;
- judged precision-over-returned **0.355932**;
- MRR **0.857639**;
- hard-negative hits **38 / 48**;
- hard-negative rate@5 **0.791667**.

## Comparator v1

Comparator recovered `48/48` useful v2 candidates with Recall@5 `1.0` and MRR `1.0`, но surfaced `41/48` hard negatives. Historical RC-10 screen surfaced `4/4` hard negatives.

Classification: `SEMANTIC_RECALL_RECOVERED_DISCRIMINATION_GATE_FAILED`.

Semantic/hybrid Reader runtime не был authorized.

## NLI neutral-filter v1

Preregistered filter снизил v2 hard-negative hits до `18/48`, но useful hits снизились до `46/48`; historical useful hits — до `15/16`. No-recall-loss overlay и frozen gates FAIL.

Classification: `NLI_NEUTRAL_FILTER_GATE_FAILED`.

## RRTIC-v1 contract

RRTIC-v1 отвечает на post-NLI **relation-contract mismatch**. Он фиксирует six suspicion-only relation families и ten structural qualifier dimensions, чтобы будущий discriminator оценивался против explicit relation/qualifier contract, а не одного scalar similarity score.

```text
EQUIVALENCE_SUSPECT
RELATED_SUSPECT
CONTRADICTION_SUSPECT
QUALIFICATION_SUSPECT
TOPIC_ONLY_SUSPECT
UNKNOWN

MATCH | MISMATCH | UNKNOWN | NOT_APPLICABLE
```

RRTIC-v1 не filter, не rerank, не model execution, не identity engine, не evidence admission, не contradiction adjudication, не Canon mutation и не auto-register RC-5 relations.

## Retained authority firewall

```text
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
working-set coverage != comprehension proof
summary != evidence
cross-document link != Canon relation
same-topic != same proposition
possible-same-claim != claim identity
similarity signal != identity proof
repetition across sources != corroboration
retrieval match != evidence
similarity != identity
NLI label != proposition identity
RRTIC suspicion != adjudicated relation
qualifier mismatch != truth decision
ranking != epistemic authority
candidate discovery != candidate adjudication
evaluation pass != runtime authorization
```

PostgreSQL/pgvector остаётся `active=false`. SQLite ordinary local-first остаётся active.

## Localization / grant

Русская D1/D3/D4/D5 documentation обновляется в Issue #410 к current repository truth `main@9666781d390e3276a111cb5ee1735f6606a76283`; historical RC-7 source остаётся immutable provenance. Остальные восемь locale packs этим milestone не изменяются.

NLnet остаётся **submitted / under review / not awarded**. Приблизительно €50,000 — planning only.

## Stop boundary

Localization parity не создаёт новых capabilities и не подразумевает следующий model/discriminator/runtime milestone.
