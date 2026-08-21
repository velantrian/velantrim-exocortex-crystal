<!-- translation-source: docs/STATUS.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- historical-translation-source: docs/STATUS.md@a497b7d3cfbe59ca75b11d7449d5a728455b3130 -->
<!-- current-translation-source: docs/STATUS.md@ad8cec8c868f64b6dfbdc3bf3087230f59c3861c -->
<!-- truthgate-v1-source: docs/STATUS.md@b4be6831a8b9f87cea815b6a0ef2c497a2d5059a -->
<!-- truthgate-v1-status: CURRENT -->
<!-- d1-locale: de -->
<!-- d1-boundary: public-ask-read-only -->
<!-- d1-boundary: postgresql-active=false -->
<!-- d1-nonclaim: import-is-not-activation -->
<!-- d1-nonclaim: nlnet-not-awarded -->
# 🇩🇪 Crystal — aktueller Status

**Statusdatum:** 2026-08-15  
**Aktueller eingefrorener Architecture-Checkpoint:** `76a9493b8ba64b832472ef9bfc1f1c23ebe6654e` — Reader Retrieval Typed Inspection Contract v1 / PR #392  
**RRTIC exact-head CI:** `31754798549` — 9/9 SUCCESS  
**RRTIC post-merge CI:** `31771677028` — 9/9 SUCCESS  
**German parity audit base:** `main@ad8cec8c868f64b6dfbdc3bf3087230f59c3861c`.

## TruthGate v1 — erneute Prüfung nach PR #440

Diese D1-Seite wurde erneut gegen die materielle Änderung der englischen Policy in `main@b4be6831a8b9f87cea815b6a0ef2c497a2d5059a` geprüft. Die standardmäßige TruthGate-Policy für `WORLD_FACT` ist nun fest und versioniert: `DEFAULT_MIN_CONFIDENCE = 0.05`, `TRUTH_GATE_POLICY_VERSION = "truth-gate-v1-fixed-0.05"`. Prozesslokale Adaptation bleibt Telemetrie/Research und ändert die standardmäßige Admission-Autorität nicht stillschweigend. Diese Klarstellung aktiviert keinen Reader/RAG/Retrieval-Runtime, kein PostgreSQL/pgvector, erweitert Canon nicht und überträgt keine Autorität an Titan. Frühere Source-Marker bleiben historische Provenienz.

> 📎 Die folgenden Runtime-Zahlen sind retained historical compatibility evidence, nicht der aktuelle Repository-Teststand.

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

RC-1…RC-7 sind implementierte bounded Reader layers. RC-8 ist eine abgeschlossene Architektur-/Research-Entscheidung. RC-9 ist implementierte deterministische lexikalische PRE-ADMISSION discovery. Comparator v1 und NLI neutral-filter v1 sind abgeschlossene, eingefrorene Evaluierungen mit failed gates. RRTIC-v1 ist ein eingefrorener typed-inspection Architekturvertrag ohne Runtime-Provider.

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

Erhaltener RC-9 K=5 control: Recall@5 `0.937500`, Precision@5 `0.187500`, MRR `0.895833`, useful hits `15/16`, hard-negative hits `4/4`; classification `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`.

Comparator-v1 classification: `SEMANTIC_RECALL_RECOVERED_DISCRIMINATION_GATE_FAILED`. NLI-v1 classification: `NLI_NEUTRAL_FILTER_GATE_FAILED`.

## RRTIC-v1

RRTIC-v1 definiert suspicion-only relation families `EQUIVALENCE_SUSPECT`, `RELATED_SUSPECT`, `CONTRADICTION_SUSPECT`, `QUALIFICATION_SUSPECT`, `TOPIC_ONLY_SUSPECT`, `UNKNOWN` und qualifier states `MATCH | MISMATCH | UNKNOWN | NOT_APPLICABLE`.

Der Vertrag führt kein model execution, filtering, reranking, identity decision, evidence admission, contradiction adjudication oder Canon mutation aus.

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

Guardian, TruthGate, TrustSnapshot und CanonicalView bleiben getrennte Authority-/Read-Surfaces. Public `HTTP /ask`, `CLI ask` und `MCP search` bleiben read-only.

## Storage / grant / localization

SQLite bleibt ordinary active local-first. PostgreSQL/pgvector bleibt inaktiv `active=false`; automatic backend switching ist nicht vorhanden.

NLnet bleibt **submitted / under review / not awarded**; ungefähr €50,000 sind planning only; budget change none.

Die deutsche current parity ist gegen `main@ad8cec8c868f64b6dfbdc3bf3087230f59c3861c` geprüft. Der ältere Source-Marker `a497b7d3cfbe59ca75b11d7449d5a728455b3130` bleibt historische Provenienz. Current repository lifecycle state muss weiterhin aus live GitHub aufgelöst werden.