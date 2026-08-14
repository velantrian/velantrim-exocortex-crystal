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

RC-5 relation vocabulary remains explicit:

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

## Retained provenance/authority contract

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

RC-7 requires different document identity, current RC-4 candidates and exact two-sided source/session/pass/node/locator provenance. Inspection basis remains descriptive, not a numeric truth/identity score.

## RC-9 retrieval evidence

RC-9 — deterministic offline in-memory BM25 baseline. Historical K=5 control: Recall@5 `0.937500`, Precision@5 `0.187500`, MRR `0.895833`, useful hits `15/16`, hard negatives `4/4`; classification `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`.

Evaluation Surface v2 exposes multi-stratum lexical gaps. These benchmark results are retrieval evidence, not truth/evidence/identity accuracy.

## Comparator / NLI

Comparator v1 recovered semantic recall but failed proposition-level hard-negative discrimination: `SEMANTIC_RECALL_RECOVERED_DISCRIMINATION_GATE_FAILED`.

NLI neutral-filter v1 reduced hard-negative leakage but lost useful recall: `NLI_NEUTRAL_FILTER_GATE_FAILED`.

```text
NLI label != proposition identity
NLI contradiction != contradiction adjudication
filtering != epistemic authority
```

Both remain frozen evaluation evidence, not runtime components.

## RRTIC-v1

Post-NLI reassessment classified the missing capability as relation-contract mismatch. RRTIC-v1 freezes suspicion-only relation families and structural qualifier dimensions, with states `MATCH | MISMATCH | UNKNOWN | NOT_APPLICABLE`.

```text
RRTIC suspicion != adjudicated relation
RRTIC diagnostic != RC-5 registered relation
qualifier mismatch != truth decision
rrtic_runtime_authorization = false
```

RRTIC-v1 performs no model execution, filtering, reranking, identity decision, evidence admission, contradiction adjudication or Canon mutation.

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

## Grant / non-claims / localization

NLnet **submitted / under review / not awarded**. Approximately **€50,000** planning only; **budget change: none**.

No security/legal/GDPR certification, native-speaker editorial certification, AGI/consciousness, universal truth, active PostgreSQL runtime, semantic/hybrid/vector Reader runtime, completed dedicated/full Reader, automatic identity/corroboration/adjudication/evidence admission is claimed.

Eight non-Russian Reader-dependent locale packs remain `REFRESH_NEEDED`; this Russian refresh does not change them.

Historical Russian RC-7 source: `main@ab3ad31c437647535030e371d58f456faf14017b`. Current Russian refresh source: `main@9666781d390e3276a111cb5ee1735f6606a76283`.
