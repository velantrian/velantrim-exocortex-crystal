<!-- translation-source: docs/STATUS.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- historical-translation-source: docs/STATUS.md@a497b7d3cfbe59ca75b11d7449d5a728455b3130 -->
<!-- current-translation-source: docs/STATUS.md@bbe6b0d3d90d80b3c669ddab5fc56aa1bfe419eb -->
<!-- d1-locale: es -->
<!-- d1-boundary: public-ask-read-only -->
<!-- d1-boundary: postgresql-active=false -->
<!-- d1-nonclaim: import-is-not-activation -->
<!-- d1-nonclaim: nlnet-not-awarded -->
# 🇪🇸 Crystal — estado actual

**Fecha de estado:** 2026-08-15  
**Architecture checkpoint congelado:** `76a9493b8ba64b832472ef9bfc1f1c23ebe6654e` — Reader Retrieval Typed Inspection Contract v1 / PR #392  
**RRTIC exact-head CI:** `31754798549` — 9/9 SUCCESS  
**RRTIC post-merge CI:** `31771677028` — 9/9 SUCCESS  
**Spanish parity audit base:** `main@bbe6b0d3d90d80b3c669ddab5fc56aa1bfe419eb`.

> 📎 Las siguientes cifras de runtime son retained historical compatibility evidence, no el recuento actual de tests del repositorio.

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
nli_reader_runtime_filter = false
```

RC-1…RC-7 son bounded Reader layers implementadas. RC-8 es una decisión architecture/research completada. RC-9 es deterministic lexical PRE-ADMISSION discovery implementado. Comparator v1 y NLI neutral-filter v1 son evaluaciones congeladas con failed gates. RRTIC-v1 es un typed-inspection architecture contract congelado sin runtime provider.

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

Control RC-9 K=5 conservado: Recall@5 `0.937500`, Precision@5 `0.187500`, MRR `0.895833`, useful hits `15/16`, hard-negative hits `4/4`; classification `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`.

Comparator-v1 classification: `SEMANTIC_RECALL_RECOVERED_DISCRIMINATION_GATE_FAILED`. NLI-v1 classification: `NLI_NEUTRAL_FILTER_GATE_FAILED`.

## RRTIC-v1

RRTIC-v1 define las suspicion-only relation families `EQUIVALENCE_SUSPECT`, `RELATED_SUSPECT`, `CONTRADICTION_SUSPECT`, `QUALIFICATION_SUSPECT`, `TOPIC_ONLY_SUSPECT`, `UNKNOWN` y los qualifier states `MATCH | MISMATCH | UNKNOWN | NOT_APPLICABLE`.

El contrato no ejecuta model execution, filtering, reranking, identity decision, evidence admission, contradiction adjudication ni Canon mutation.

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

Guardian, TruthGate, TrustSnapshot y CanonicalView siguen siendo Authority/read surfaces distintas. Public `HTTP /ask`, `CLI ask` y `MCP search` siguen read-only.

## Storage / grant / localization

SQLite sigue ordinary active local-first. PostgreSQL/pgvector sigue inactivo `active=false`; no existe automatic backend switching.

NLnet sigue **submitted / under review / not awarded**; aproximadamente €50,000 es planning only; budget change none.

La Spanish current parity se audita contra `main@bbe6b0d3d90d80b3c669ddab5fc56aa1bfe419eb`. El antiguo source marker `a497b7d3cfbe59ca75b11d7449d5a728455b3130` permanece como provenance histórica. El lifecycle state actual del repositorio siempre debe resolverse desde GitHub live.