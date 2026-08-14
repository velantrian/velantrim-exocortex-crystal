<!-- translation-source: docs/STATUS.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- rc6-translation-source: docs/STATUS.md@ed96a88369f841bdb2ffd79ca020acef174685fc -->
<!-- rc7-translation-source: docs/STATUS.md@ab3ad31c437647535030e371d58f456faf14017b -->
<!-- rc7-status: CURRENT -->
<!-- current-translation-source: docs/STATUS.md@9666781d390e3276a111cb5ee1735f6606a76283 -->
# 🇷🇺 Crystal — текущий статус

**Дата статуса:** 2026-08-15  
**Текущий signed architecture checkpoint:** `76a9493b8ba64b832472ef9bfc1f1c23ebe6654e`, `verified=true`, reason `valid`  
**Current architecture milestone:** Reader Retrieval Typed Inspection Contract v1 — Issue #391 / PR #392 — complete  
**RRTIC exact-head CI:** `31754798549` — 9/9 SUCCESS  
**RRTIC post-merge CI:** `31771677028` — 9/9 SUCCESS  
**Historical RC-7 localization source:** `main@ab3ad31c437647535030e371d58f456faf14017b`.

> 📎 Retained runtime evidence ниже — historical compatibility evidence, а не текущий repository test count.

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

RC-1…RC-7 — implemented bounded Reader layers. RC-8 — completed retrieval architecture/research decision. RC-9 — implemented deterministic lexical PRE-ADMISSION discovery. Comparator v1 и NLI neutral-filter v1 — completed frozen evaluations с failed gates. RRTIC-v1 — frozen typed-inspection architecture contract без runtime provider.

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

Retained RC-9 historical K=5 control: Recall@5 `0.937500`, Precision@5 `0.187500`, MRR `0.895833`, useful hits `15/16`, hard-negative hits `4/4`; classification `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`.

Comparator v1 classification: `SEMANTIC_RECALL_RECOVERED_DISCRIMINATION_GATE_FAILED`. NLI v1 classification: `NLI_NEUTRAL_FILTER_GATE_FAILED`.

## RRTIC-v1

RRTIC-v1 фиксирует suspicion-only relation families `EQUIVALENCE_SUSPECT`, `RELATED_SUSPECT`, `CONTRADICTION_SUSPECT`, `QUALIFICATION_SUSPECT`, `TOPIC_ONLY_SUSPECT`, `UNKNOWN` и qualifier states `MATCH | MISMATCH | UNKNOWN | NOT_APPLICABLE`.

Он не выполняет model execution, filtering, reranking, identity decision, evidence admission, contradiction adjudication или Canon mutation.

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

Guardian, TruthGate, TrustSnapshot и CanonicalView остаются отдельными authority/read surfaces. Public `HTTP /ask`, `CLI ask`, `MCP search` read-only.

## Storage / grant / localization

SQLite ordinary active local-first. PostgreSQL/pgvector inactive `active=false`; automatic backend switching отсутствует.

NLnet **submitted / under review / not awarded**; ~€50,000 planning only; budget change none.

Русская current parity refresh привязана к `main@9666781d390e3276a111cb5ee1735f6606a76283`, а historical RC-5/6/7 markers остаются immutable provenance. Остальные восемь locale packs этим milestone не меняются.
