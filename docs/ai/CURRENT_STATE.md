# Crystal AI Current State

**Status date:** 2026-08-14  
**Audited pre-RRTIC base:** `d8bc98cb7643019b34ffacde2e87c3e81a5556ba`  
**Base signature:** `verified=true`, reason `valid`  
**Rule:** re-resolve live GitHub and the three existing authoritative Notion pages before treating this dated checkpoint as evergreen truth.

GitHub merged `main`, executable tests and exact CI are authoritative for implementation truth. Notion is a synchronized documentation surface, not a substitute for repository evidence.

## Current Reader position

```text
RC-1 through RC-7 bounded Reader layers   MERGED
RC-9 lexical discovery baseline           COMPLETE
Evaluation Surface v2                     COMPLETE / FROZEN
Comparator v1                             COMPLETE / FROZEN GATE FAIL
NLI neutral-filter v1                     COMPLETE / FROZEN GATE FAIL
RRTIC-v1 typed inspection contract        FROZEN CONTRACT / PR #392
dedicated_reader_core                     false
semantic/hybrid Reader runtime            NOT AUTHORIZED
NLI Reader runtime filter                 NOT AUTHORIZED
Reader FTS / ANN / vector DB               NOT AUTHORIZED
PostgreSQL/pgvector Reader activation      NOT AUTHORIZED
```

The latest completed evaluation milestone remains **Reader NLI Neutral-Filter Evaluation v1** (Issue `#388`, merged PR `#389`). It was bounded, preregistered, offline, reproducible, CPU-only evaluation research. It did not add a Reader backend or runtime stage.

The current architecture milestone is **Reader Retrieval Typed Inspection Contract v1 (RRTIC-v1)**, tracked by Issue `#391` and PR `#392`. RRTIC-v1 freezes a model-free retrieval-side inspection envelope with six suspicion-only relation families and ten qualifier dimensions. It does not filter, rerank, infer identity, admit evidence, adjudicate contradictions, register RC-5 relations automatically, or authorize runtime work.

## RRTIC-v1 — current architecture contract

Artifacts:

```text
docs/architecture/READER_RETRIEVAL_TYPED_INSPECTION_CONTRACT_V1.md
eval/reader_retrieval_typed_inspection_contract_v1.json
tests/test_reader_retrieval_typed_inspection_contract_v1.py
```

Frozen relation families:

```text
EQUIVALENCE_SUSPECT
RELATED_SUSPECT
CONTRADICTION_SUSPECT
QUALIFICATION_SUSPECT
TOPIC_ONLY_SUSPECT
UNKNOWN
```

Frozen qualifier dimensions:

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

Each qualifier is limited to `MATCH | MISMATCH | UNKNOWN | NOT_APPLICABLE`.

Authority flags remain:

```text
identity_claimed=false
evidence_admitted=false
adjudication_performed=false
runtime_authorization=false
```

RRTIC diagnostic `!=` RC-5 registered relation `!=` adjudicated contradiction `!=` admitted evidence. Prior frozen RC-8/v2/NLI cases are explanatory provenance only; RRTIC-v1 makes no new performance claim. Any future discriminator requires a new experiment identity, preregistration and fresh validation design.

## Latest frozen evidence — NLI neutral-filter v1

Merged result: PR `#389`  
Exact validated PR head: `2a13ce498aa1af6190bf878ddafbecc5340ce9b6`  
Signed squash-merge main: `567ff95305cc4b0333d67ae8a54329db4748fae8`  
Exact-head CI: `31750910147` — 9/9 SUCCESS  
Post-merge CI: `31751382430` — 9/9 SUCCESS  
Tracking issue: `#388` — CLOSED / completed  
Frozen result artifact: `eval/reader_nli_neutral_filter_v1_result.json`  
Classification: `NLI_NEUTRAL_FILTER_GATE_FAILED`  
Runtime authorization: `false`

Pinned model identity:

```text
model:     MoritzLaurer/multilingual-MiniLMv2-L6-mnli-xnli
revision:  0a71e92a985b6e1ad1828cf67ce9c459639c1dca
device:    CPU
mode:      offline / preloaded local assets
rule:      reject iff query→candidate AND candidate→query argmax are both NEUTRAL
backfill:  forbidden
```

Frozen historical RC-10 result:

```text
useful hits:          15 / 16
Recall@5:             0.937500
MRR:                  0.937500
hard-negative hits:    1 / 4
frozen gate:          FAIL
```

Frozen Evaluation Surface v2 result:

```text
useful hits:          46 / 48
Recall@5:             0.958333
MRR:                  1.000000
hard-negative hits:   18 / 48
hard-negative rate:    0.375000
recovered RC-9 misses retained: 5 / 6
frozen gate:          FAIL
```

The NLI signal materially reduced measured hard-negative leakage, but the preregistered neutral-neutral filter was not recall-safe. Four v2 strata remained above the frozen per-stratum hard-negative ceiling. The correct conclusion is not “NLI does not work”; the evidence says the relation signal is diagnostically useful while this frozen filter is not admissible as a Reader retrieval stage.

No rule, threshold, model, qrel or gate was relaxed after observing the qualifying result.

## Comparator v1 — retained predecessor evidence

Tracking issue: `#386`  
Merged result: PR `#387`  
Frozen result artifact: `eval/reader_retrieval_comparator_v1_result.json`  
Classification: `SEMANTIC_RECALL_RECOVERED_DISCRIMINATION_GATE_FAILED`

The pinned offline multilingual sentence-embedding comparator used:

```text
model:      sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
revision:   e8f8c211226b894fcb81acc59f3b34ba3efd5f42
device:     CPU
similarity: cosine
K:          5
index:      NO_INDEX_EXACT_POOL_SCORING
```

Qualifying execution: GitHub Actions run `31728139139`.

Historical RC-10 screen:

```text
useful hits:          16 / 16
Recall@5:             1.000000
MRR:                  1.000000
hard-negative hits:    4 / 4
hard-negative rate:    1.000000
frozen gate:          FAIL
```

Evaluation Surface v2 comparator result:

```text
useful hits:          48 / 48
Recall@5:             1.000000
MRR:                  1.000000
hard-negative hits:   41 / 48
hard-negative rate:    0.854167
```

Comparator v1 recovered all six RC-9 v2 useful misses but worsened proposition-level discrimination. It solved the measured lexical recall ceiling without establishing proposition identity.

## Historical Reader implementation truth retained

```text
reader_core_rc1_skeleton               = true
reader_core_rc2_structural_map         = true
reader_core_rc3_multi_pass_mechanics   = true
reader_core_rc4_proposition_extraction = true
reader_core_rc5_relation_candidates    = true
reader_core_rc6_long_context_strategy  = true
reader_core_rc7_cross_document_links   = true
dedicated_reader_core                  = false
```

RC-1 through RC-7 are merged bounded Reader layers.
RC-7 remains signed `main@b5541ce504af9002c8d3e2dcfa44ef4c0ead86c1`, post-merge CI `31572918731`.
**RC-9 — deterministic lexical candidate discovery: COMPLETE.**
RC-9 remains the deterministic lexical candidate-discovery implementation baseline in `core/reader_lexical_discovery.py`; signed `main@f8b7d7ea36625b6589a4cf02f12b94c5f98fdb61`, post-merge CI `31594027040`.
Historical RC-9 K=5 evidence remains Recall@5 `0.937500`, Precision@5 `0.187500`, MRR `0.895833`, useful hits `15 / 16`, and paired hard-negative rate@5 `1.000000`.
Historical classification: `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`.
RC-9 is empirical and intentionally modest.

Issue `#377` / PR `#378` froze the RC-10 comparator screen without executing a comparator. Issue `#382` / PR `#383` completed the post-RC-10 architecture reassessment and selected Evaluation Surface v2 as a separate bounded evaluation milestone. Those historical decisions remain evidence; later Comparator/NLI results do not rewrite them.

## Reader Retrieval Evaluation Surface v2 — retained frozen surface

Issue `#384` / PR `#385`. Evaluation/research only.

```text
24 queries
12 primary strata
6 candidates/query
144/144 explicit qrels
judgment coverage = 1.0
K = 5
surface sha256 = 753cc550bc5fc47697aa6d7b1cda294bf11abaa08d515816e5e1db59eb526cdd
```

Final RC-9 v2 control: useful hits `42 / 48`; Recall@5 `0.875000`; fixed-slot Precision@5 `0.350000`; judged precision-over-returned `0.355932`; MRR `0.857639`; hard-negative hits `38 / 48`; hard-negative rate@5 `0.791667`; any-useful-query `1.000000`; all-useful-query `0.750000`.
Classification: `LEXICAL_CONTROL_EXPOSES_MULTI_STRATUM_GAPS`.

Reviewed q04 refund-scope and q23 unconditional cache-scope pairs are useful `POSSIBLE_CONTRADICTION` candidates. Candidate IDs are content-derived and qrel-label-independent.

## Authority firewall

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
NLI contradiction != contradiction adjudication
RRTIC suspicion != adjudicated relation
qualifier mismatch != truth decision
ranking != epistemic authority
candidate discovery != candidate adjudication
comparison pass != runtime authorization
evaluation pass != runtime authorization
```

Comparator/NLI/RRTIC research does not authorize semantic/hybrid Reader runtime, an NLI runtime filter, RRTIC runtime provider, FTS, ANN/vector DB, PostgreSQL/pgvector activation, automatic proposition identity, automatic contradiction adjudication, evidence admission, Guardian/TruthGate bypass or Canon mutation.

## Localization truth

Immutable phased localization source checkpoint: `51c205fe048fd69d39fcd47b43e042a50de432bc`.
D2 checkpoint: `main@b7e6574dd7aefa2f32783ab79054fac6b3b4109f`.
Russian Reader-dependent public/detail documentation is refreshed. Russian D1/D3/D4/D5 detail pack is current. D2 reviewer/safety translations remain current across all nine supported locales.
The eight other localized root README files and Reader-dependent detail packs remain `REFRESH_NEEDED`; eight other locale detail packs require Reader refresh.
Tracked Reader detail debt remains 64 documents.

## Grant / backlog truth

NLnet remains `submitted / under review / not awarded`.
Approximate €50,000 remains planning context only, not awarded funding.
Open residual issues `#155`, `#165` and `#214` remain separate scopes and must not be auto-started by this architecture workstream.

## Documentation contract

Use `docs/ai/project_manifest.yaml` for machine navigation and `docs/ai/DOCUMENTATION_STANDARD.md` for human/AI maintenance semantics.

```text
HUMAN LANDING LAYER
        ↓
AI READ / UPDATE CONTRACT
        ↓
CURRENT TECHNICAL TRUTH
        ↓
PR / CI / EVIDENCE
        ↓
HISTORICAL CHECKPOINTS
```

`overview != current state != evidence != history`.

- `STRUCTURAL_CHANGE` requires checking the maintained project portrait and refreshing only representations whose meaning became stale.
- `STATE_CHANGE` requires current/top surfaces to stop implying obsolete phase, runtime, authorization, funding or admission state.
- `EVIDENCE_ONLY` updates evidence/checkpoints without mechanically rewriting a still-correct project portrait.
- Historical checkpoints are retained rather than rewritten to resemble current state.
- Live GitHub and the existing authoritative Notion pages override handoffs when they differ.

## Stop boundary

The NLI neutral-filter v1 milestone is closed. Do not tune its frozen rule on the same evaluation surface and call that unbiased validation. Any different rule/model/threshold is a new experiment identity requiring a new preregistration and validation design.

Current bounded action is to validate and close **RRTIC-v1 (#391 / PR #392)**. After that closure, STOP. No discriminator/model/runtime implementation is authorized by this contract, and issues `#155`, `#165`, `#214` remain separate backlog items.
