<!-- translation-source: docs/STATUS.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- historical-translation-source: docs/STATUS.md@a497b7d3cfbe59ca75b11d7449d5a728455b3130 -->
<!-- current-translation-source: docs/STATUS.md@e436577dc5ada4692e8fe399da861a44f800e2f1 -->
<!-- d1-locale: it -->
<!-- d1-boundary: public-ask-read-only -->
<!-- d1-boundary: postgresql-active=false -->
<!-- d1-nonclaim: import-is-not-activation -->
<!-- d1-nonclaim: nlnet-not-awarded -->
# 🇮🇹 Crystal — stato attuale

**Data dello stato:** 2026-08-15  
**Architecture checkpoint congelato:** `76a9493b8ba64b832472ef9bfc1f1c23ebe6654e` — Reader Retrieval Typed Inspection Contract v1 / PR #392  
**RRTIC exact-head CI:** `31754798549` — 9/9 SUCCESS  
**RRTIC post-merge CI:** `31771677028` — 9/9 SUCCESS  
**Italian parity audit base:** `main@e436577dc5ada4692e8fe399da861a44f800e2f1`.

> 📎 Le cifre runtime seguenti sono retained historical compatibility evidence, non il conteggio corrente dei test del repository.

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

RC-1…RC-7 sono bounded Reader layers implementati. RC-8 è una decisione architecture/research completata. RC-9 è deterministic lexical PRE-ADMISSION discovery implementato. Comparator v1 e NLI neutral-filter v1 sono valutazioni congelate con failed gates. RRTIC-v1 è un typed-inspection architecture contract congelato senza runtime provider.

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

Control RC-9 K=5 conservato: Recall@5 `0.937500`, Precision@5 `0.187500`, MRR `0.895833`, useful hits `15/16`, hard-negative hits `4/4`; classification `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`.

Comparator-v1 classification: `SEMANTIC_RECALL_RECOVERED_DISCRIMINATION_GATE_FAILED`. NLI-v1 classification: `NLI_NEUTRAL_FILTER_GATE_FAILED`.

## RRTIC-v1

RRTIC-v1 definisce le suspicion-only relation families `EQUIVALENCE_SUSPECT`, `RELATED_SUSPECT`, `CONTRADICTION_SUSPECT`, `QUALIFICATION_SUSPECT`, `TOPIC_ONLY_SUSPECT`, `UNKNOWN` e i qualifier states `MATCH | MISMATCH | UNKNOWN | NOT_APPLICABLE`.

Il contratto non esegue model execution, filtering, reranking, identity decision, evidence admission, contradiction adjudication o Canon mutation.

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

Guardian, TruthGate, TrustSnapshot e CanonicalView restano Authority/read surfaces distinte. Public `HTTP /ask`, `CLI ask` e `MCP search` restano read-only.

## Storage / grant / localization

SQLite resta ordinary active local-first. PostgreSQL/pgvector resta inattivo `active=false`; non esiste automatic backend switching.

NLnet resta **submitted / under review / not awarded**; circa €50,000 è planning only; budget change none.

La parity italiana corrente è auditata contro `main@e436577dc5ada4692e8fe399da861a44f800e2f1`. Il vecchio source marker `a497b7d3cfbe59ca75b11d7449d5a728455b3130` resta provenance storica. Il lifecycle state corrente del repository va sempre risolto da GitHub live.
