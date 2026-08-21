# 🤖 Crystal AI Current State

**Status date:** 2026-08-21  
**Document role:** compact technical state snapshot; live GitHub + tests + exact CI override this file if repository state has advanced.  
**Repository HEAD:** `RESOLVE_LIVE_GITHUB`.  
**Repository lifecycle provenance:** `RESOLVE_LIVE_GITHUB` for current main, exact CI, latest closure, open PRs/issues and active milestone.  
**Current architecture checkpoint:** `76a9493b8ba64b832472ef9bfc1f1c23ebe6654e` — RRTIC-v1 / PR #392.  
**Active milestone:** `RESOLVE_LIVE_GITHUB`.  
**Next milestone selected:** `RESOLVE_LIVE_GITHUB`.

Do not treat a historical SHA as current HEAD. Do not treat this document as a substitute for `docs/status/implementation-manifest.json`. Do not hard-code a latest repository/docs closure here as an indefinitely-current invariant; resolve volatile lifecycle state from live GitHub before acting.

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

The logical migration verifier's final file recheck is content-bound as well as metadata-bound: it reuses the existing SHA-256 verification signal in a bounded reread, so a same-size rewrite does not rely on filesystem timestamp precision for detection. Migration bundles remain operational evidence only and do not authorize activation.

Direct `ingest()` reuses the existing L3 outbox when an L3 merge fails after the L1 ESM transition. The call returns a failed result and leaves an explicit secondary-sync repair record instead of silently leaving `Validated` L1 state without a recovery path. This changes recovery parity only; it does not bypass Guardian, TruthGate or Canon authority.

Issue #165 is closed by a bounded exact-normalized compatibility implementation. Current auto-ingest still derives identity from NFC → trim → internal-whitespace collapse → casefold. When the current normalized `fact_id` does not exist, a derived/rebuildable SQLite index can map that exact normalized claim to an already-`Validated` historical `ing:*` row. Historical IDs are not re-keyed; existing collisions are not merged; current normalized IDs take precedence; multiple legacy collisions route future occurrence-only hits deterministically to the oldest row. Dry-run uses the same resolver without writing the derived index, and full erasure removes its mapping. `exact normalized equality != semantic identity`; the index grants no evidence, corroboration or Canon authority.

## Localization truth

Immutable phased localization source checkpoint: `51c205fe048fd69d39fcd47b43e042a50de432bc`.  
D2 translation checkpoint: `main@b7e6574dd7aefa2f32783ab79054fac6b3b4109f`.

Arabic, German, French, Spanish, Hindi, Italian, Japanese, Simplified Chinese and Russian Reader-dependent public/detail documentation is refreshed under recorded parity/source contracts. All nine supported D1/D3/D4/D5 detail packs are current. D2 reviewer/safety translations remain current across all nine supported locales.

**TruthGate-v1 D1 reassessment: COMPLETE.** All 18 affected localized `STATUS.md` / `IMPLEMENTATION_STATUS.md` documents were reassessed against the material English policy source `main@b4be6831a8b9f87cea815b6a0ef2c497a2d5059a` under Issue #441. Their older checkpoint markers remain historical provenance; the explicit TruthGate-v1 markers are the policy-freshness evidence for this change.

No localized root README or Reader-dependent detail pack remains `REFRESH_NEEDED` for the recorded semantics. This is a documentation-parity claim, not native-speaker editorial certification and not runtime authorization.

Arabic current parity audit base: `main@9e048c21fb929f7d299e3af0ef03d76c1df899d6`. German current parity audit base: `main@ad8cec8c868f64b6dfbdc3bf3087230f59c3861c`. French current parity audit base: `main@7d03cce2c89f7a4c3fda85742eb358e6b49961f2`. Spanish current parity audit base: `main@bbe6b0d3d90d80b3c669ddab5fc56aa1bfe419eb`. Hindi current parity audit base: `main@e1df11219ee4fc3b9c175b05c7569e568cf6f512`. Italian current parity audit base: `main@e436577dc5ada4692e8fe399da861a44f800e2f1`. Japanese current parity audit base: `main@5903e90f3e0f2884f4ba257a71808d19fc439ebc`. Simplified Chinese current parity audit base: `main@5e6301f0eaee1a6c85d8543be89dc2e606dc05a8`. Russian current parity audit source: `main@9666781d390e3276a111cb5ee1735f6606a76283`. Human-first English README source: `main@3bc9f4c3b7ad30a3d0cc7a59904f26509a5a1883`.

### Retained post-German localization compatibility literal

The exact phrases **`German and Russian Reader-dependent public/detail documentation is refreshed`** and **`seven other localized root README files and Reader-dependent detail packs`** are retained here solely as historical compatibility evidence for the closed German parity checkpoint. This sentence is retained as immutable post-German compatibility evidence only; it is **not current localization truth** after later parity refreshes.

### Retained post-French localization compatibility literal

The exact phrases **`German, French and Russian Reader-dependent public/detail documentation is refreshed`** and **`six other localized root README files and Reader-dependent detail packs`** are retained here solely as historical compatibility evidence for the closed French parity checkpoint. This sentence is retained as immutable post-French compatibility evidence only; it is **not current localization truth** after later parity refreshes.

### Retained post-Spanish localization compatibility literal

The exact phrases **`German, French, Spanish and Russian Reader-dependent public/detail documentation is refreshed`** and **`five other localized root README files and Reader-dependent detail packs`** are retained here solely as historical compatibility evidence for the closed Spanish parity checkpoint. This sentence is retained as immutable post-Spanish compatibility evidence only; it is **not current localization truth** after later parity refreshes.

### Retained post-Italian localization compatibility literal

The exact phrases **`German, French, Spanish, Italian and Russian Reader-dependent public/detail documentation is refreshed`** and **`four other localized root README files and Reader-dependent detail packs`** are retained here solely as historical compatibility evidence for the closed Italian parity checkpoint. This sentence is retained as immutable post-Italian compatibility evidence only; it is **not current localization truth** after later parity refreshes.

### Retained post-Simplified-Chinese localization compatibility literal

The exact phrases **`German, French, Spanish, Italian, Simplified Chinese and Russian Reader-dependent public/detail documentation is refreshed`** and **`three other localized root README files and Reader-dependent detail packs`** are retained here solely as historical compatibility evidence for the closed Simplified Chinese parity checkpoint. This sentence is retained as immutable post-Simplified-Chinese compatibility evidence only; it is **not current localization truth** after later parity refreshes.

### Retained post-Japanese localization compatibility literal

The exact phrases **`German, French, Spanish, Italian, Japanese, Simplified Chinese and Russian Reader-dependent public/detail documentation is refreshed`** and **`two other localized root README files and Reader-dependent detail packs`** are retained here solely as historical compatibility evidence for the closed Japanese parity checkpoint. This sentence is retained as immutable post-Japanese compatibility evidence only; it is **not current localization truth** after later parity refreshes.

### Retained post-Arabic localization compatibility literal

The exact phrases **`Arabic, German, French, Spanish, Italian, Japanese, Simplified Chinese and Russian Reader-dependent public/detail documentation is refreshed`** and **`one other localized root README file and Reader-dependent detail pack`** are retained here solely as historical compatibility evidence for the closed Arabic parity checkpoint. This sentence is retained as immutable post-Arabic compatibility evidence only; it is **not current localization truth** after Hindi parity.

### Retained Evaluation-Surface-v2 localization compatibility literal

The exact phrase **`eight other localized root README files`** is retained here solely as historical compatibility evidence for the older Evaluation Surface v2 documentation contract, when Russian was the only refreshed locale. It is **not current localization truth** after later parity milestones; the current refresh-needed count is zero.

A visually stronger old translation may be used as a layout reference only. It must not be treated as newer technical truth.

## Grant / residual backlog

NLnet remains submitted / under review / not awarded. Approximate €50,000 remains planning context only.

Residual scope ledger:

```text
#155 CLOSED / completed — EPIS-001 architecture contract only; runtime not authorized
#165 CLOSED / completed — exact normalized historical ing:* compatibility only; no re-key/semantic dedupe
#214 CLOSED / completed — fixture/PII + supply-chain verification hygiene
```

These three historical residual scopes are closed/completed. Their closure does not auto-select a new milestone or authorize EPIS runtime, semantic/hybrid/vector Reader runtime, PostgreSQL activation, semantic dedupe or authority expansion. Resolve live GitHub before acting because newer issues/PRs may exist.

## Documentation interface lifecycle

The maintained interface remains:

```text
👤 README + docs/OVERVIEW.md
🤖 docs/ai/README.md + this state snapshot
⚙ docs/status/implementation-manifest.json
🧾 STATUS + IMPLEMENTATION_STATUS + TEST_REPORT + CI + eval/history
```

```text
overview != current state != machine truth != evidence != history
```

Volatile repository lifecycle facts are deliberately **not** persisted here as “latest/current” constants. Resolve them before work:

```text
repository HEAD + exact CI       → RESOLVE_LIVE_GITHUB
latest completed PR/issue        → RESOLVE_LIVE_GITHUB
open PRs/issues                  → RESOLVE_LIVE_GITHUB
active milestone / next selected → RESOLVE_LIVE_GITHUB
```

Synchronized Notion may preserve checkpoint provenance, but live GitHub remains authoritative and can supersede it.

## Stop boundary

This file does not authorize or select the next workstream. The nine-locale documentation parity program being complete does not authorize runtime, model, storage or authority expansion. The bounded audit-remediation fixes and the exact-normalized #165 compatibility closure do not select another architecture or backlog milestone. Before any new bounded work, resolve live GitHub/Notion, perform a fresh architecture reassessment, select exactly one scope, and preserve the authority firewall.

No next model, discriminator, reranker, Reader backend, storage activation, authority expansion or residual issue is automatically authorized by a historical closure or by this static snapshot.
