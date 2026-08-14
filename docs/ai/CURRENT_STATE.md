# 🤖 Crystal AI Current State

**Status date:** 2026-08-14  
**Document role:** compact technical state snapshot; live GitHub + tests + exact CI override this file if repository state has advanced.  
**Current docs-only repository main at milestone start:** `58a137fe96cb92b121d4f75b97990ecaf3f962a3`  
**Current architecture checkpoint:** `76a9493b8ba64b832472ef9bfc1f1c23ebe6654e` — RRTIC-v1 / PR #392.

Do not treat a historical SHA as current HEAD. Do not treat this document as a substitute for `docs/status/implementation-manifest.json`.

## Current Reader position

```text
RC-1 through RC-7 bounded Reader layers   MERGED
RC-9 lexical discovery baseline           COMPLETE
Evaluation Surface v2                     COMPLETE / FROZEN
Comparator v1                             COMPLETE / FROZEN GATE FAIL
NLI neutral-filter v1                     COMPLETE / FROZEN GATE FAIL
RRTIC-v1 typed inspection contract        FROZEN ARCHITECTURE CONTRACT
dedicated_reader_core                     false
semantic/hybrid Reader runtime            NOT AUTHORIZED
NLI Reader runtime filter                 NOT AUTHORIZED
RRTIC runtime provider                    NOT AUTHORIZED
Reader FTS / ANN / vector DB              NOT AUTHORIZED
PostgreSQL/pgvector Reader activation     NOT AUTHORIZED
```

Machine boundary names retained:

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
**RC-9 — deterministic lexical candidate discovery: COMPLETE.**
RC-9 remains the deterministic lexical candidate-discovery implementation baseline.

## Current architecture contract — RRTIC-v1

RRTIC-v1 is a model-free retrieval-side typed inspection contract. It freezes six suspicion-only relation families:

```text
EQUIVALENCE_SUSPECT
RELATED_SUSPECT
CONTRADICTION_SUSPECT
QUALIFICATION_SUSPECT
TOPIC_ONLY_SUSPECT
UNKNOWN
```

and ten qualifier dimensions:

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

Qualifier states are limited to:

```text
MATCH | MISMATCH | UNKNOWN | NOT_APPLICABLE
```

Authority flags remain false:

```text
identity_claimed=false
evidence_admitted=false
adjudication_performed=false
runtime_authorization=false
```

RRTIC-v1 does not filter, rerank, infer proposition identity, admit evidence, adjudicate contradiction, mutate Canon or auto-register RC-5 relations.

```text
RRTIC suspicion != adjudicated relation
qualifier mismatch != truth decision
```

## Frozen evaluation chain

```text
RC-9 lexical baseline
        ↓
Comparator v1
semantic recall recovered
hard-negative discrimination gate FAIL
        ↓
NLI neutral-filter v1
hard-negative leakage reduced
useful-recall safety gate FAIL
        ↓
post-NLI architecture reassessment
RELATION-CONTRACT MISMATCH
        ↓
RRTIC-v1
contract-first / no runtime authorization
```

### RC-9 retained implementation evidence

Historical signed RC-9 merge: `f8b7d7ea36625b6589a4cf02f12b94c5f98fdb61`  
Post-merge CI: `31594027040`  
Historical result classification: `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`.

Historical paired K=5 control:

```text
useful hits:               15 / 16
Recall@5:                  0.937500
Precision@5:               0.187500
MRR:                       0.895833
paired hard-negative rate: 1.000000
```

RC-9 provides deterministic lexical PRE-ADMISSION discovery, not semantic identity or evidence admission.

### RC-7 retained provenance

Historical signed RC-7 merge: `b5541ce504af9002c8d3e2dcfa44ef4c0ead86c1`  
Post-merge CI: `31572918731`.

RC-7 authority vocabulary remains explicit:

```text
cross-document link != Canon relation
same-topic != same proposition
possible-same-claim != claim identity
similarity signal != identity proof
repetition across sources != corroboration
```

RC-7 retains **no automatic semantic matching** and does not authorize embeddings/ANN/vector Reader runtime.

### RC-10 preregistration history

Issue `#377` / PR #378 froze the comparison screen before comparator execution.

```text
comparison pass != runtime authorization
```

Later evaluation results do not rewrite that historical preregistration.

### Post-RC-10 reassessment

Issue `#382` selected **Reader Retrieval Evaluation Surface v2** as the next bounded evaluation/research milestone at that historical checkpoint. It did not execute a comparator and did not authorize runtime change.

### Evaluation Surface v2

Frozen surface:

```text
24 queries
12 primary strata
6 candidates/query
144/144 explicit qrels
judgment coverage = 1.0
K = 5
surface sha256 = 753cc550bc5fc47697aa6d7b1cda294bf11abaa08d515816e5e1db59eb526cdd
```

RC-9 v2 control:

```text
useful hits:                    42 / 48
Recall@5:                       0.875000
fixed-slot Precision@5:         0.350000
judged precision-over-returned: 0.355932
MRR:                            0.857639
hard-negative hits:             38 / 48
hard-negative rate:             0.791667
classification:                 LEXICAL_CONTROL_EXPOSES_MULTI_STRATUM_GAPS
```

### Comparator v1

Frozen classification: `SEMANTIC_RECALL_RECOVERED_DISCRIMINATION_GATE_FAILED`.

Evaluation Surface v2:

```text
useful hits:          48 / 48
Recall@5:             1.000000
MRR:                  1.000000
hard-negative hits:   41 / 48
hard-negative rate:   0.854167
```

The comparator recovered all six measured RC-9 useful misses but did not satisfy proposition-level hard-negative discrimination.

### NLI neutral-filter v1

Frozen classification: `NLI_NEUTRAL_FILTER_GATE_FAILED`.

Evaluation Surface v2:

```text
useful hits:          46 / 48
Recall@5:             0.958333
MRR:                  1.000000
hard-negative hits:   18 / 48
hard-negative rate:   0.375000
```

The signal improved discrimination but the frozen rule was not recall-safe. It is evaluation evidence only, not an NLI Reader runtime stage.

## Permanent authority firewall

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

No retrieval, ranking, similarity, NLI or RRTIC diagnostic may bypass evidence admission, Guardian, TruthGate or Canon authority.

## Storage truth

```text
SQLite ordinary local-first             ACTIVE
PostgreSQL/pgvector import target        INACTIVE
PostgreSQL/pgvector Reader activation    NOT AUTHORIZED
active=false
```

Physical L3 is not automatically strict Canon. Successful import/equivalence does not imply runtime backend activation.

## Localization truth

Immutable phased localization source checkpoint: `51c205fe048fd69d39fcd47b43e042a50de432bc`.

Russian Reader-dependent public/detail documentation is refreshed under the recorded phased contract. Russian D1/D3/D4/D5 detail pack is current. D2 reviewer/safety translations remain current across all nine supported locales.

The **eight other localized root README files and Reader-dependent detail packs** remain `REFRESH_NEEDED` at their recorded source checkpoints; eight other locale detail packs require Reader refresh.

A visually stronger old translation may be used as a layout reference only. It must not be treated as newer technical truth.

## Grant / residual backlog

NLnet remains submitted / under review / not awarded. Approximate €50,000 remains planning context only.

Separate residual issues:

```text
#155 Epistemic Router RFC
#165 normalized-id migration / dedupe
#214 PII fixture + supply-chain hygiene
```

They are not auto-started by Reader or documentation work.

## Documentation architecture v1

Current bounded docs milestone: Issue `#395` — **Human / AI / Machine Documentation Architecture v1**.

```text
👤 README + docs/OVERVIEW.md
🤖 docs/ai/README.md + this state snapshot
⚙ docs/status/implementation-manifest.json
🧾 STATUS + IMPLEMENTATION_STATUS + TEST_REPORT + CI + eval/history
```

```text
overview != current state != machine truth != evidence != history
```

The documentation milestone may reorganize explanation and navigation. It does not authorize any Reader runtime, model, storage backend activation or epistemic-authority change.

## Stop boundary

Complete #395 through docs/tests → exact-head CI → review gate → guarded merge → post-merge CI → authorized Notion 3/3 reconciliation/read-back if affected → STOP.

No next model, discriminator, reranker, Reader backend or residual issue is authorized by this documentation milestone.
