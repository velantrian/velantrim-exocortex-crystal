<!-- translation-source: docs/STATUS.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- historical-translation-source: docs/STATUS.md@a497b7d3cfbe59ca75b11d7449d5a728455b3130 -->
<!-- current-translation-source: docs/STATUS.md@5903e90f3e0f2884f4ba257a71808d19fc439ebc -->
<!-- d1-locale: ja -->
<!-- d1-boundary: public-ask-read-only -->
<!-- d1-boundary: postgresql-active=false -->
<!-- d1-nonclaim: import-is-not-activation -->
<!-- d1-nonclaim: nlnet-not-awarded -->
# 🇯🇵 Crystal — 現在の状態

**状態日:** 2026-08-15  
**Frozen Reader architecture checkpoint:** `76a9493b8ba64b832472ef9bfc1f1c23ebe6654e` — Reader Retrieval Typed Inspection Contract v1 / PR #392  
**RRTIC exact-head CI:** `31754798549` — 9/9 SUCCESS  
**RRTIC post-merge CI:** `31771677028` — 9/9 SUCCESS  
**Japanese parity audit base:** `main@5903e90f3e0f2884f4ba257a71808d19fc439ebc`

> 📎 次の runtime 数値は retained historical compatibility evidence であり、現在の repository test count ではありません。

```text
bbd816c09dd39a02e6de6c1014438490572f40f6
2078 passed / 13 skipped / 0 failed
9756 statements / 100.00% line coverage
```

## 📖 Current Reader position

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

RC-1…RC-7 は bounded implemented Reader layers。RC-9 は implemented deterministic lexical **PRE-ADMISSION** candidate discovery です。Comparator v1 と NLI neutral-filter v1 は frozen evaluation evidence で、どちらも gate FAIL。RRTIC-v1 は frozen typed-inspection architecture contract であり runtime provider はありません。

## 🔬 Evidence chain

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

Retained RC-9 control K=5: Recall@5 `0.937500`, Precision@5 `0.187500`, MRR `0.895833`, useful hits `15/16`, hard-negative hits `4/4`; classification `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`。

Comparator classification: `SEMANTIC_RECALL_RECOVERED_DISCRIMINATION_GATE_FAILED`。  
NLI classification: `NLI_NEUTRAL_FILTER_GATE_FAILED`。

## 🧬 RRTIC-v1

RRTIC-v1 は suspicion-only relation families `EQUIVALENCE_SUSPECT`, `RELATED_SUSPECT`, `CONTRADICTION_SUSPECT`, `QUALIFICATION_SUSPECT`, `TOPIC_ONLY_SUSPECT`, `UNKNOWN` と qualifier states `MATCH | MISMATCH | UNKNOWN | NOT_APPLICABLE` を定義します。

model execution、filtering、reranking、identity decision、evidence admission、contradiction adjudication、Canon mutation は行いません。

## 🛡 Authority boundaries

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

Guardian、TruthGate、TrustSnapshot、CanonicalView は独立した authority/read roles を維持します。Public `HTTP /ask`, `CLI ask`, `MCP search` は read-only です。

## 💾 Storage / grant / localization

SQLite は ordinary active local-first path。PostgreSQL/pgvector は inactive target で `active=false`。automatic backend switching はありません。`physical L3 != strict Canon` であり successful import も backend activation ではありません。

NLnet は **submitted / under review / not awarded**。約 €50,000 は planning context only、budget change: none。

Current Japanese parity audit base は `main@5903e90f3e0f2884f4ba257a71808d19fc439ebc`。旧 source marker `a497b7d3cfbe59ca75b11d7449d5a728455b3130` は historical provenance のみです。Live repository lifecycle state は GitHub から解決してください。