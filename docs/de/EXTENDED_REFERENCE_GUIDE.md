<!-- translation-source: docs/EXTENDED_REFERENCE_POLICY.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- historical-translation-source: docs/EXTENDED_REFERENCE_POLICY.md@d5f7f1c4c0908d24f8994e4fbec45c102b9ab7d9 -->
<!-- current-translation-source: docs/EXTENDED_REFERENCE_POLICY.md@ad8cec8c868f64b6dfbdc3bf3087230f59c3861c -->
<!-- d5-locale: de -->
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
# 🇩🇪 Extended Reference Guide — Crystal

Diese Reviewer-/Reference-Surface hält Provenienz und explizite Authority über einer bequemen Erzählung: Neue Reader-, Retrieval- oder Evaluation-Capability erhält nicht automatisch epistemische Autorität.

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

SQLite bleibt ordinary active local-first; PostgreSQL/pgvector bleibt inaktiv `active=false`.

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

RC-5 relation vocabulary bleibt explizit:

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

RC-7 verlangt unterschiedliche document identity, current RC-4 candidates und exact two-sided source/session/pass/node/locator provenance. Inspection basis bleibt deskriptiv und ist kein numerischer Truth-/Identity-Score.

## RC-9 Retrieval Evidence

RC-9 ist eine deterministische offline in-memory BM25 baseline. Erhaltener K=5 control: Recall@5 `0.937500`, Precision@5 `0.187500`, MRR `0.895833`, useful hits `15/16`, hard negatives `4/4`; classification `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`.

Evaluation Surface v2 zeigt multi-stratum lexical gaps. Diese Benchmark-Ergebnisse sind Retrieval Evidence, keine Truth-/Evidence-/Identity-Accuracy.

## Comparator / NLI

Comparator v1 stellte semantic recall wieder her, scheiterte aber an proposition-level hard-negative discrimination: `SEMANTIC_RECALL_RECOVERED_DISCRIMINATION_GATE_FAILED`.

NLI neutral-filter v1 verringerte hard-negative leakage, verlor aber useful recall: `NLI_NEUTRAL_FILTER_GATE_FAILED`.

```text
NLI label != proposition identity
NLI contradiction != contradiction adjudication
filtering != epistemic authority
```

Beide bleiben eingefrorene Evaluation Evidence und sind keine Runtime-Komponenten.

## RRTIC-v1

Das post-NLI reassessment klassifizierte die fehlende Capability als relation-contract mismatch. RRTIC-v1 friert suspicion-only relation families und strukturelle qualifier dimensions mit den States `MATCH | MISMATCH | UNKNOWN | NOT_APPLICABLE` ein.

```text
RRTIC suspicion != adjudicated relation
RRTIC diagnostic != RC-5 registered relation
qualifier mismatch != truth decision
rrtic_runtime_authorization = false
```

RRTIC-v1 führt kein model execution, filtering, reranking, identity decision, evidence admission, contradiction adjudication oder Canon mutation aus.

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

## Grant / Non-claims / Localization

NLnet bleibt **submitted / under review / not awarded**. Ungefähr **€50,000** sind planning only; **budget change: none**.

Es wird keine security/legal/GDPR certification, native-speaker editorial certification, AGI/consciousness, universal truth, active PostgreSQL runtime, semantic/hybrid/vector Reader runtime, completed dedicated/full Reader oder automatic identity/corroboration/adjudication/evidence admission behauptet.

Nach diesem German milestone bleiben sieben Reader-dependent locale packs `REFRESH_NEEDED`; Russian und German sind die current localized detail packs. Dieses Dokument ändert keine andere Sprache.

Historischer deutscher D5 source: `d5f7f1c4c0908d24f8994e4fbec45c102b9ab7d9`. Current German refresh audit source: `main@ad8cec8c868f64b6dfbdc3bf3087230f59c3861c`.

Routen: [Policy](../EXTENDED_REFERENCE_POLICY.md), [Map](../DOCUMENTATION_MAP.md), [Status](../STATUS.md), [Architecture](../ARCHITECTURE.md), [ADR](../ADR.md), [Security](../../SECURITY.md), [Privacy](../../PRIVACY.md), [GDPR](../../GDPR.md), [Archive](../archive/README.md).
