<!-- translation-source: docs/EXTENDED_REFERENCE_POLICY.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- historical-translation-source: docs/EXTENDED_REFERENCE_POLICY.md@d5f7f1c4c0908d24f8994e4fbec45c102b9ab7d9 -->
<!-- current-translation-source: docs/EXTENDED_REFERENCE_POLICY.md@e436577dc5ada4692e8fe399da861a44f800e2f1 -->
<!-- d5-locale: it -->
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
# 🇮🇹 Extended Reference Guide — Crystal

Questa superficie reviewer/reference mette provenance e Authority esplicite davanti alla narrazione pratica: una nuova Reader/retrieval/evaluation capability non riceve mai automaticamente autorità epistemica.

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

SQLite resta ordinary active local-first; PostgreSQL/pgvector resta inattivo `active=false`.

## Reader lineage

```text
RC-1 source/session
RC-2 caller-supplied structure
RC-3 explicit passes
RC-4 EXTRACTED_PROPOSITION
RC-5 relation candidates
RC-6 working sets + SUMMARY
RC-7 cross-document link candidates
RC-8 architecture/research decision
RC-9 lexical PRE-ADMISSION discovery
```

Il vocabolario RC-5 resta esplicito:

```text
POSSIBLE_CONTRADICTION
EXCEPTION
QUALIFICATION
TENSION
```

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
nli_reader_runtime_filter = false
rrtic_runtime_authorization = false
```

## Retained provenance / authority contract

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
```

RC-7 richiede differenti document identities, current RC-4 candidates ed exact two-sided source/session/pass/node/locator provenance. Inspection basis resta descrittiva e non è numeric Truth/Identity score.

## RC-9 Retrieval Evidence

RC-9 è una deterministic offline in-memory BM25 baseline. Control K=5 conservato: Recall@5 `0.937500`, Precision@5 `0.187500`, MRR `0.895833`, useful hits `15/16`, hard negatives `4/4`; classification `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`.

Evaluation Surface v2 mostra multi-stratum lexical gaps. Questi benchmark results sono Retrieval Evidence, non Truth/Evidence/Identity accuracy.

## Comparator / NLI

Comparator v1 ha ripristinato semantic recall ma ha fallito proposition-level hard-negative discrimination: `SEMANTIC_RECALL_RECOVERED_DISCRIMINATION_GATE_FAILED`.

NLI neutral-filter v1 ha ridotto hard-negative leakage ma ha perso useful recall: `NLI_NEUTRAL_FILTER_GATE_FAILED`.

```text
NLI label != proposition identity
NLI contradiction != contradiction adjudication
filtering != epistemic authority
```

Entrambi restano frozen Evaluation Evidence e non runtime components.

## RRTIC-v1

Il post-NLI reassessment ha classificato la capability mancante come relation-contract mismatch. RRTIC-v1 congela suspicion-only relation families e structural qualifier dimensions con states `MATCH | MISMATCH | UNKNOWN | NOT_APPLICABLE`.

```text
RRTIC suspicion != adjudicated relation
RRTIC diagnostic != RC-5 registered relation
qualifier mismatch != truth decision
rrtic_runtime_authorization = false
```

RRTIC-v1 non esegue model execution, filtering, reranking, identity decision, evidence admission, contradiction adjudication o Canon mutation.

## Authority path

```text
Reader / RC-9 / RRTIC inspection
→ explicit evidence/review process if separately initiated
→ Guardian
→ TruthGate
→ physical L3 / TrustSnapshot
→ CanonicalView / strict Canon projection
```

```text
retrieval match != evidence
similarity != identity
candidate discovery != candidate adjudication
```

Guardian resta structural integrity / structural policy boundary, non truth oracle. TruthGate resta L3 admission authority. TrustSnapshot è deny-dominant reconciliation; CanonicalView è strict trusted read-time projection. TRACE/provenance conserva auditability, ma provenance != proof of truth.

## Grant / Non-claims / Localization

NLnet resta **submitted / under review / not awarded**. Circa **€50,000** è planning only; **budget change: none**.

Non vengono rivendicati security/legal/GDPR certification, native-speaker editorial certification, AGI/consciousness, universal truth, active PostgreSQL runtime, semantic/hybrid/vector Reader runtime, completed dedicated/full Reader o automatic identity/corroboration/adjudication/evidence admission.

Dopo questo Italian milestone, quattro Reader-dependent locale packs restano `REFRESH_NEEDED`; German, Spanish, French, Italian e Russian sono i current localized detail packs. Questo documento non modifica nessun altro linguaggio.

Historical Italian D5 source: `d5f7f1c4c0908d24f8994e4fbec45c102b9ab7d9`. Current Italian refresh audit source: `main@e436577dc5ada4692e8fe399da861a44f800e2f1`.

Routes: [Policy](../EXTENDED_REFERENCE_POLICY.md), [Map](../DOCUMENTATION_MAP.md), [Status](../STATUS.md), [Architecture](../ARCHITECTURE.md), [ADR](../ADR.md), [Security](../../SECURITY.md), [Privacy](../../PRIVACY.md), [GDPR](../../GDPR.md), [Archive](../archive/README.md).
