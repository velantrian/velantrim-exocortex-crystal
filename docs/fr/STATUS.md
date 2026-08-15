<!-- translation-source: docs/STATUS.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- historical-translation-source: docs/STATUS.md@a497b7d3cfbe59ca75b11d7449d5a728455b3130 -->
<!-- current-translation-source: docs/STATUS.md@7d03cce2c89f7a4c3fda85742eb358e6b49961f2 -->
<!-- d1-locale: fr -->
<!-- d1-boundary: public-ask-read-only -->
<!-- d1-boundary: postgresql-active=false -->
<!-- d1-nonclaim: import-is-not-activation -->
<!-- d1-nonclaim: nlnet-not-awarded -->
# 🇫🇷 Crystal — état actuel

**Date d’état :** 2026-08-15  
**Architecture checkpoint gelé :** `76a9493b8ba64b832472ef9bfc1f1c23ebe6654e` — Reader Retrieval Typed Inspection Contract v1 / PR #392  
**RRTIC exact-head CI :** `31754798549` — 9/9 SUCCESS  
**RRTIC post-merge CI :** `31771677028` — 9/9 SUCCESS  
**French parity audit base :** `main@7d03cce2c89f7a4c3fda85742eb358e6b49961f2`.

> 📎 Les chiffres runtime suivants sont des retained historical compatibility evidence, pas le nombre courant de tests du dépôt.

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

RC-1…RC-7 sont des bounded Reader layers implémentées. RC-8 est une décision architecture/research terminée. RC-9 est une deterministic lexical PRE-ADMISSION discovery implémentée. Comparator v1 et NLI neutral-filter v1 sont des évaluations gelées avec failed gates. RRTIC-v1 est un typed-inspection architecture contract gelé sans runtime provider.

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

Contrôle RC-9 K=5 conservé : Recall@5 `0.937500`, Precision@5 `0.187500`, MRR `0.895833`, useful hits `15/16`, hard-negative hits `4/4`; classification `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`.

Comparator-v1 classification : `SEMANTIC_RECALL_RECOVERED_DISCRIMINATION_GATE_FAILED`. NLI-v1 classification : `NLI_NEUTRAL_FILTER_GATE_FAILED`.

## RRTIC-v1

RRTIC-v1 définit les suspicion-only relation families `EQUIVALENCE_SUSPECT`, `RELATED_SUSPECT`, `CONTRADICTION_SUSPECT`, `QUALIFICATION_SUSPECT`, `TOPIC_ONLY_SUSPECT`, `UNKNOWN` et les qualifier states `MATCH | MISMATCH | UNKNOWN | NOT_APPLICABLE`.

Le contrat n’exécute aucun model execution, filtering, reranking, identity decision, evidence admission, contradiction adjudication ou Canon mutation.

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

Guardian, TruthGate, TrustSnapshot et CanonicalView restent des Authority/read surfaces distinctes. Public `HTTP /ask`, `CLI ask` et `MCP search` restent read-only.

## Storage / grant / localization

SQLite reste ordinary active local-first. PostgreSQL/pgvector reste inactif `active=false`; aucun automatic backend switching n’est présent.

NLnet reste **submitted / under review / not awarded** ; environ €50,000 est planning only ; budget change none.

La French current parity est auditée contre `main@7d03cce2c89f7a4c3fda85742eb358e6b49961f2`. L’ancien source marker `a497b7d3cfbe59ca75b11d7449d5a728455b3130` reste une provenance historique. Le lifecycle state courant du dépôt doit toujours être résolu depuis GitHub live.