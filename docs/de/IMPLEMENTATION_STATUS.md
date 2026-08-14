<!-- translation-source: docs/IMPLEMENTATION_STATUS.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- historical-translation-source: docs/IMPLEMENTATION_STATUS.md@a497b7d3cfbe59ca75b11d7449d5a728455b3130 -->
<!-- current-translation-source: docs/IMPLEMENTATION_STATUS.md@ad8cec8c868f64b6dfbdc3bf3087230f59c3861c -->
<!-- d1-locale: de -->
<!-- d1-boundary: public-ask-read-only -->
<!-- d1-boundary: postgresql-active=false -->
<!-- d1-nonclaim: import-is-not-activation -->
<!-- d1-nonclaim: nlnet-not-awarded -->
# 🇩🇪 Crystal — Implementierungsstatus

**Eingefrorener Architecture-Checkpoint:** `main@76a9493b8ba64b832472ef9bfc1f1c23ebe6654e` / PR #392; post-merge CI `31771677028` — 9/9 SUCCESS.  
**Signed RC-9 implementation baseline:** `main@f8b7d7ea36625b6589a4cf02f12b94c5f98fdb61` / PR #376; post-merge CI `31594027040`.  
**Letzte abgeschlossene model-backed Evaluation:** NLI neutral-filter v1 / PR #389 — frozen gate FAIL.  
**Aktueller frozen Architecture Contract:** RRTIC-v1 / Issue #391 / PR #392 — keine Runtime-Autorisierung.  
**German parity audit base:** `main@ad8cec8c868f64b6dfbdc3bf3087230f59c3861c`.

## Tatsächlich implementierte Reader Capabilities

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

| Capability | Status | Primäre Implementierung / Bedeutung |
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

## Research / Evaluation Evidence — keine Implementierung

| Evidence / Contract | Result | Runtime-Bedeutung |
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

Das sind Retrieval-Messungen, keine semantic/adjudication accuracy.

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

Der Comparator erreichte `48/48` useful v2 candidates mit Recall@5 `1.0` und MRR `1.0`, brachte aber `41/48` hard negatives an die Oberfläche. Der historische RC-10 screen brachte `4/4` hard negatives an die Oberfläche.

Classification: `SEMANTIC_RECALL_RECOVERED_DISCRIMINATION_GATE_FAILED`.

Ein semantic/hybrid Reader runtime wurde nicht autorisiert.

## NLI neutral-filter v1

Der preregistrierte Filter senkte v2 hard-negative hits auf `18/48`, senkte aber useful hits auf `46/48`; historical useful hits sanken auf `15/16`. No-recall-loss overlay und frozen gates FAIL.

Classification: `NLI_NEUTRAL_FILTER_GATE_FAILED`.

## RRTIC-v1 Contract

RRTIC-v1 adressiert den post-NLI **relation-contract mismatch**. Der Vertrag friert sechs suspicion-only relation families und zehn strukturelle qualifier dimensions ein, damit ein zukünftiger Discriminator gegen einen expliziten Relation-/Qualifier-Vertrag und nicht nur gegen einen scalar similarity score evaluiert wird.

```text
EQUIVALENCE_SUSPECT
RELATED_SUSPECT
CONTRADICTION_SUSPECT
QUALIFICATION_SUSPECT
TOPIC_ONLY_SUSPECT
UNKNOWN

MATCH | MISMATCH | UNKNOWN | NOT_APPLICABLE
```

RRTIC-v1 ist kein Filter, kein Reranker, kein model execution, keine identity engine, keine evidence admission, keine contradiction adjudication, keine Canon mutation und registriert RC-5 relations nicht automatisch.

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

PostgreSQL/pgvector bleibt `active=false`. SQLite bleibt ordinary active local-first.

## Localization / Grant

Die deutsche D1/D3/D4/D5-Dokumentation wird in Issue #412 gegen `main@ad8cec8c868f64b6dfbdc3bf3087230f59c3861c` aktualisiert. Historische Source-Marker bleiben Provenienz. Die sieben übrigen nicht-russischen und nicht-deutschen locale packs werden in diesem Milestone nicht aktualisiert.

NLnet bleibt **submitted / under review / not awarded**. Ungefähr €50,000 sind planning only.

## Stop Boundary

Localization parity erzeugt keine neue Capability und autorisiert keinen nächsten model/discriminator/runtime milestone.
