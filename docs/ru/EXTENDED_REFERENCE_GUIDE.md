<!-- translation-source: docs/EXTENDED_REFERENCE_POLICY.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- d5-locale: ru -->
<!-- d5-boundary: physical-l3-not-strict-canon -->
<!-- d5-boundary: retrieval-score-not-evidence -->
<!-- d5-boundary: model-output-not-source-truth -->
<!-- d5-boundary: migration-proof-not-claim-proof -->
<!-- d5-nonclaim: import-is-not-activation -->
<!-- d5-nonclaim: nlnet-not-awarded -->
<!-- d5-nonclaim: security-legal-gdpr-not-certified -->
<!-- d5-nonclaim: native-speaker-editorial-not-certified -->
<!-- d5-reader: rc1-skeleton-implemented -->
<!-- d5-reader: rc2-structural-map-implemented -->
<!-- d5-reader: rc3-multi-pass-mechanics-implemented -->
<!-- d5-reader: rc4-proposition-extraction-implemented -->
<!-- d5-reader: rc5-relation-candidates-implemented -->
<!-- d5-nonclaim: dedicated-reader-core-not-implemented -->
<!-- rc6-translation-source: docs/EXTENDED_REFERENCE_POLICY.md@ed96a88369f841bdb2ffd79ca020acef174685fc -->
<!-- rc7-translation-source: docs/EXTENDED_REFERENCE_POLICY.md@ab3ad31c437647535030e371d58f456faf14017b -->
<!-- rc7-status: CURRENT -->
<!-- current-translation-source: main@9666781d390e3276a111cb5ee1735f6606a76283 -->
# 🇷🇺 Extended Reference Guide — Crystal

Extended reviewer/reference boundary: provenance и explicit authority важнее удобного нарратива; новая Reader/retrieval/evaluation capability не получает authority автоматически.

## Core boundary

```text
physical L3 != strict Canon
retrieval score != evidence
model output != source truth
migration proof != claim proof
import != activation
ranking != epistemic authority
evaluation pass != runtime authorization
```

SQLite ordinary active local-first; PostgreSQL/pgvector inactive `active=false`.

## Reader lineage

RC-1 связывает source/session. RC-2 — caller-supplied structure. RC-3 — explicit passes. RC-4 — source-linked `EXTRACTED_PROPOSITION`. RC-5 — relation candidates. RC-6 — bounded working sets + caller SUMMARY. RC-7 — explicit cross-document link candidates с exact two-sided provenance. RC-8 — retrieval architecture/research decision. RC-9 — deterministic lexical PRE-ADMISSION candidate discovery.

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
```

## RC-7 retained relation vocabulary

| Kind | Symmetry | Boundary |
|---|---|---|
| SUPPORTS | directional | comparison candidate, not admitted evidence |
| CONTRADICTS | symmetric | candidate, not confirmed contradiction |
| ELABORATES | directional | elaboration candidate |
| REFERENCES | directional | reference candidate |
| DEFINES | directional | definition candidate |
| EXAMPLE_OF | directional | example candidate |
| PREREQUISITE_FOR | directional | prerequisite candidate |
| SAME_TOPIC | symmetric | same topic, not same proposition |
| POSSIBLE_SAME_CLAIM | symmetric | inspection hypothesis, not identity |

RC-7 требует different `document_id`, current registered RC-4 candidates, OPEN ReaderSession, exact SourceVersion/privacy, registered SegmentCard, completed RC-3 pass, substantive target outcome, recovered RC-2 node и current substantive coverage. Exact session/candidate/pass/node/source/locator provenance и non-empty rationale обязательны.

```text
cross-document link != Canon relation
same-topic != same proposition
possible-same-claim != claim identity
similarity signal != identity proof
repetition across sources != corroboration
```

## RC-9 retrieval evidence

RC-9 — offline stdlib-only deterministic in-memory BM25 baseline. Он не использует admitted-memory retrieval как identity authority и не auto-register RC-7 links.

Historical K=5 control:

| Metric | Result |
|---|---:|
| Recall@5 | 0.937500 |
| Precision@5 | 0.187500 |
| MRR | 0.895833 |
| Useful hits | 15/16 |
| Hard negatives | 4/4 |

Classification: `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`.

Evaluation Surface v2 фиксирует multi-stratum retrieval gaps; эти benchmark results не являются truth/evidence/identity accuracy.

## Comparator v1 / NLI v1

Comparator v1 восстановил semantic recall на frozen surface, но failed proposition-level hard-negative discrimination. Classification: `SEMANTIC_RECALL_RECOVERED_DISCRIMINATION_GATE_FAILED`.

NLI neutral-filter v1 уменьшил hard-negative leakage, но потерял useful recall. Classification: `NLI_NEUTRAL_FILTER_GATE_FAILED`.

```text
NLI label != proposition identity
NLI contradiction != contradiction adjudication
filtering != epistemic authority
```

Оба — evaluation evidence only. Runtime integration rejected/not authorized.

## RRTIC-v1

Post-NLI reassessment выявил relation-contract mismatch, а не доказал необходимость «ещё более большой модели».

RRTIC-v1 фиксирует suspicion-only relation families:

```text
EQUIVALENCE_SUSPECT
RELATED_SUSPECT
CONTRADICTION_SUSPECT
QUALIFICATION_SUSPECT
TOPIC_ONLY_SUSPECT
UNKNOWN
```

и structural qualifier dimensions:

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

Qualifier state: `MATCH | MISMATCH | UNKNOWN | NOT_APPLICABLE`.

```text
RRTIC suspicion != adjudicated relation
RRTIC diagnostic != RC-5 registered relation
qualifier mismatch != truth decision
rrtic_runtime_authorization = false
```

RRTIC-v1 не выполняет model execution, filtering, reranking, identity, evidence admission, contradiction adjudication или Canon mutation.

## Authority / evidence path

```text
Reader candidate / RC-9 retrieval / RRTIC inspection
→ explicit evidence/review process (если отдельно инициирован)
→ Guardian
→ TruthGate
→ physical L3 / TrustSnapshot
→ strict Canon projection
```

```text
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
summary != evidence
retrieval match != evidence
similarity != identity
candidate discovery != candidate adjudication
```

## Storage / privacy

PostgreSQL import/equivalence не означает activation. Reader RC-1…RC-9 и RRTIC-v1 не создают PostgreSQL Reader runtime, ANN/vector DB, automatic switching/cutover или new trust boundary.

Source restriction/sensitivity metadata сохраняется; retrieval rank или RRTIC qualifier не ослабляет privacy policy.

## Grant / non-claims

NLnet — **submitted / under review / not awarded**. Приблизительно **€50,000** planning only; **budget change: none**. Pre-agreement merged work — existing baseline.

Не заявляются security/legal/GDPR certification, native-speaker editorial certification, AGI/consciousness, universal truth, active PostgreSQL runtime, semantic/hybrid/vector Reader runtime, completed dedicated/full Reader, automatic identity/corroboration/adjudication/evidence admission.

## Localization provenance

Русская historical RC-7 surface была `CURRENT` against `main@ab3ad31c437647535030e371d58f456faf14017b`. Этот source marker сохраняется как immutable evidence. Текущий Russian refresh выполнен against `main@9666781d390e3276a111cb5ee1735f6606a76283` и не меняет остальные восемь locales.
