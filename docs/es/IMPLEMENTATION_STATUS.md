<!-- translation-source: docs/IMPLEMENTATION_STATUS.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- historical-translation-source: docs/IMPLEMENTATION_STATUS.md@a497b7d3cfbe59ca75b11d7449d5a728455b3130 -->
<!-- current-translation-source: docs/IMPLEMENTATION_STATUS.md@bbe6b0d3d90d80b3c669ddab5fc56aa1bfe419eb -->
<!-- truthgate-v1-source: docs/IMPLEMENTATION_STATUS.md@b4be6831a8b9f87cea815b6a0ef2c497a2d5059a -->
<!-- truthgate-v1-status: CURRENT -->
<!-- d1-locale: es -->
<!-- d1-boundary: public-ask-read-only -->
<!-- d1-boundary: postgresql-active=false -->
<!-- d1-nonclaim: import-is-not-activation -->
<!-- d1-nonclaim: nlnet-not-awarded -->
# 🇪🇸 Crystal — estado de implementación

**Architecture checkpoint congelado:** `main@76a9493b8ba64b832472ef9bfc1f1c23ebe6654e` / PR #392; post-merge CI `31771677028` — 9/9 SUCCESS.  
**Signed RC-9 implementation baseline:** `main@f8b7d7ea36625b6589a4cf02f12b94c5f98fdb61` / PR #376; post-merge CI `31594027040`.  
**Última model-backed evaluation completada:** NLI neutral-filter v1 / PR #389 — frozen gate FAIL.  
**Architecture contract actual congelado:** RRTIC-v1 / Issue #391 / PR #392 — sin runtime authorization.  
**Spanish parity audit base:** `main@bbe6b0d3d90d80b3c669ddab5fc56aa1bfe419eb`.

## TruthGate v1 — reconciliación de implementación después de PR #440

Esta página D1 se volvió a revisar contra el cambio material de la política inglesa en `main@b4be6831a8b9f87cea815b6a0ef2c497a2d5059a`. La admission predeterminada de `WORLD_FACT` usa una política fija y versionada: `DEFAULT_MIN_CONFIDENCE = 0.05`, `TRUTH_GATE_POLICY_VERSION = "truth-gate-v1-fixed-0.05"`. La adaptación local al proceso sigue siendo telemetría/investigación y no cambia el threshold de admission predeterminado. El `min_confidence` explícito sigue siendo un parámetro bounded del caller para flujos internos/tests existentes. Esto no añade Reader/RAG/retrieval runtime, no activa PostgreSQL/pgvector, no amplía Canon y no transfiere autoridad a Titan. Los source markers anteriores se conservan como provenance histórica.

## Reader capabilities realmente implementadas

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
nli_reader_runtime_filter              = false
```

| Capability | Estado | Implementación / significado |
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

## Research / Evaluation Evidence — no runtime implementation

| Evidence / Contract | Resultado | Significado runtime |
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

Son medidas de retrieval, no semantic/adjudication accuracy.

## Evaluation Surface v2

Frozen surface: 24 queries, 12 primary strata ×2, 6 candidates/query, 144/144 explicit qrels, judgment coverage `1.0`, K=5, SHA-256 `753cc550bc5fc47697aa6d7b1cda294bf11abaa08d515816e5e1db59eb526cdd`.

RC-9 v2 control: useful hits **42 / 48**, Recall@5 **0.875000**, fixed-slot Precision@5 **0.350000**, judged precision-over-returned **0.355932**, MRR **0.857639**, hard-negative hits **38 / 48**, hard-negative rate@5 **0.791667**.

## Comparator v1

Comparator v1 alcanzó `48/48` useful v2 candidates con Recall@5 `1.0` y MRR `1.0`, pero recuperó `41/48` hard negatives. El historical RC-10 screen recuperó `4/4` hard negatives.

Classification: `SEMANTIC_RECALL_RECOVERED_DISCRIMINATION_GATE_FAILED`. No se autorizó semantic/hybrid Reader runtime.

## NLI neutral-filter v1

El filtro preregistered redujo los v2 hard-negative hits a `18/48`, pero los useful hits a `46/48`; historical useful hits a `15/16`. No-recall-loss overlay y frozen gates FAIL.

Classification: `NLI_NEUTRAL_FILTER_GATE_FAILED`.

## RRTIC-v1 Contract

RRTIC-v1 responde al **relation-contract mismatch** post-NLI. Congela seis suspicion-only relation families y diez structural qualifier dimensions para que un futuro discriminator se evalúe contra un contrato explícito de relaciones/qualifiers y no contra un simple scalar similarity score.

```text
EQUIVALENCE_SUSPECT
RELATED_SUSPECT
CONTRADICTION_SUSPECT
QUALIFICATION_SUSPECT
TOPIC_ONLY_SUSPECT
UNKNOWN

MATCH | MISMATCH | UNKNOWN | NOT_APPLICABLE
```

RRTIC-v1 no es filter, reranker, model execution, identity engine, evidence admission, contradiction adjudication ni Canon mutation; tampoco registra automáticamente RC-5 relations.

## Retained Authority Firewall

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

PostgreSQL/pgvector sigue `active=false`. SQLite sigue ordinary active local-first.

## Localization / Grant

La documentación española D1/D3/D4/D5 se actualiza en Issue #417 contra `main@bbe6b0d3d90d80b3c669ddab5fc56aa1bfe419eb`. Los historical source markers siguen siendo provenance. Los cinco locale packs restantes refresh-needed no se actualizan en este milestone.

NLnet sigue **submitted / under review / not awarded**. Aproximadamente €50,000 es planning only.

## Stop Boundary

La localization parity no crea ninguna capability nueva ni autoriza ningún nuevo model/discriminator/runtime milestone.