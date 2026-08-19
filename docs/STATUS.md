# Velantrim Crystal — Current Status

**Status date:** 2026-08-19  
**Current signed architecture checkpoint:** `76a9493b8ba64b832472ef9bfc1f1c23ebe6654e`, `verified=true`, reason `valid`  
**Current architecture milestone:** Reader Retrieval Typed Inspection Contract v1 — Issue #391 / PR #392 — complete  
**RRTIC exact-head CI:** `31754798549` — 9/9 SUCCESS  
**RRTIC post-merge CI:** `31771677028` — 9/9 SUCCESS  
**Historical RC-7 merged baseline:** `main@b5541ce504af9002c8d3e2dcfa44ef4c0ead86c1` — PR #372; post-merge CI `31572918731`; retained as immutable cross-document Reader provenance.  
**Historical signed RC-9 implementation baseline:** `main@f8b7d7ea36625b6589a4cf02f12b94c5f98fdb61` — PR #376; post-merge CI `31594027040`; retained RC-10 architecture decision #377  
**Historical post-RC-10 reassessment:** Issue #382 selected an **orchestration-only** evaluation path; it authorized no new retrieval runtime and is retained as provenance, not as the current next action.  
**Retained storage-runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6` / PR #337  
**Repository-head rule:** resolve live GitHub before treating any docs-only merge SHA as the current repository HEAD.

## Current Reader position

RC-1 through RC-7 are bounded implemented Reader/domain layers. RC-8 is a completed architecture/research decision. RC-9 is the implemented deterministic lexical PRE-ADMISSION retrieval baseline. Comparator v1 and NLI neutral-filter v1 are completed frozen evaluations with failed admission gates. RRTIC-v1 is the current frozen architecture contract for typed inspection and does not add a runtime stage.

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

RC-5 remains implemented in `core/reader_relations.py`. RC-9 remains implemented in `core/reader_lexical_discovery.py`.

## Reader evidence chain

```text
RC-9 lexical discovery
        ↓
Evaluation Surface v2
        ↓
Comparator v1
  recall recovered
  hard-negative discrimination FAIL
        ↓
NLI neutral-filter v1
  discrimination improved
  useful-recall safety FAIL
        ↓
post-NLI reassessment
  RELATION-CONTRACT MISMATCH
        ↓
RRTIC-v1
  typed inspection contract only
  runtime_authorization=false
```

## RC-9 deterministic lexical baseline — retained control

Historical RC-8 K=5 evidence remains:

| Metric | Result |
|---|---:|
| Recall@5 | 0.937500 |
| Precision@5 | 0.187500 |
| MRR | 0.895833 |
| Paired hard-negative rate@5 | 1.000000 |
| Useful hits | 15 / 16 |
| Hard-negative hits | 4 / 4 |

Classification: `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`.

## Reader Retrieval Evaluation Surface v2 — retained frozen evidence

The fully judged v2 surface remains frozen at SHA-256 `753cc550bc5fc47697aa6d7b1cda294bf11abaa08d515816e5e1db59eb526cdd` with 24 queries, 12 primary strata, 6 candidates/query and 144/144 explicit qrels.

Unchanged RC-9 on v2:

| Metric | Result |
|---|---:|
| Useful hits | **42 / 48** |
| Useful Recall@5 | **0.875000** |
| Precision@5 — fixed K slots | **0.350000** |
| Judged precision over returned | **0.355932** |
| MRR | **0.857639** |
| Hard-negative hits | **38 / 48** |
| Hard-negative hit rate@5 | **0.791667** |

Classification: `LEXICAL_CONTROL_EXPOSES_MULTI_STRATUM_GAPS`.

## Comparator v1 — completed evaluation / frozen gate fail

Pinned multilingual semantic similarity recovered all useful v2 candidates (`48/48`, Recall@5 `1.0`, MRR `1.0`) but surfaced `41/48` hard negatives.

Classification: `SEMANTIC_RECALL_RECOVERED_DISCRIMINATION_GATE_FAILED`.

Historical RC-10 screen also failed because all `4/4` hard negatives surfaced. This comparator is research evidence only; it is not a Reader backend.

## NLI neutral-filter v1 — completed evaluation / frozen gate fail

The preregistered bidirectional neutral-neutral filter reduced v2 hard negatives from `41/48` to `18/48`, but useful candidates regressed to `46/48`; historical useful hits regressed from `16/16` to `15/16`. The no-recall-loss overlay and frozen gate therefore failed.

Classification: `NLI_NEUTRAL_FILTER_GATE_FAILED`.

```text
NLI label         != proposition identity
NLI contradiction != contradiction adjudication
filtering          != epistemic authority
```

## RRTIC-v1 — current frozen architecture contract

RRTIC-v1 freezes a retrieval-side diagnostic envelope after the post-NLI reassessment classified the missing capability as a relation-contract mismatch.

Six suspicion-only relation families:

```text
EQUIVALENCE_SUSPECT
RELATED_SUSPECT
CONTRADICTION_SUSPECT
QUALIFICATION_SUSPECT
TOPIC_ONLY_SUSPECT
UNKNOWN
```

Ten qualifier dimensions:

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

Each qualifier is `MATCH | MISMATCH | UNKNOWN | NOT_APPLICABLE`.

RRTIC-v1 has no accept/reject policy, scalar truth/confidence score, reranking, model execution, runtime provider, identity decision, evidence admission, contradiction adjudication or Canon mutation. Existing RC-5 semantics are unchanged.

```text
RRTIC suspicion    != adjudicated relation
RRTIC diagnostic   != RC-5 registered relation
qualifier mismatch != truth decision
comparison pass    != runtime authorization
```

## Reader authority boundaries

```text
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
working-set coverage != comprehension proof
summary != source text
summary != evidence
summary != verified fact
summary != Canon admission
cross-document link != Canon relation
same-topic != same proposition
possible-same-claim != claim identity
similarity signal != identity proof
repetition across sources != corroboration
retrieval match != evidence
similarity != identity
ranking != epistemic authority
candidate discovery != candidate adjudication
comparison pass != runtime authorization
evaluation pass != runtime authorization
```

Guardian, TrustSnapshot and CanonicalView retain their existing authority roles. TruthGate's default WORLD_FACT confidence policy is now explicitly fixed and versioned at `DEFAULT_MIN_CONFIDENCE = 0.05` / `TRUTH_GATE_POLICY_VERSION = "truth-gate-v1-fixed-0.05"`; process-local adaptation remains telemetry/research and does not silently change default admission authority. Public `HTTP /ask`, `CLI ask` and `MCP search` remain admitted-memory read-only query surfaces, not Reader evaluation/inspection authority interfaces.

## Storage truth

```text
SQLite ordinary active local-first
→ backup / verify / inactive restore
→ bounded logical export
→ PostgreSQL 16 + pgvector inactive import/equivalence
→ active=false
```

Reader SQLite FTS is not implemented. No Reader ANN/vector DB is introduced. Automatic L3 storage backend switching remains absent.

The bounded logical migration verifier now binds its final file recheck to both filesystem identity and the already-established SHA-256 content digest. This strengthens the existing fail-closed migration proof against same-size rewrites on filesystems with coarse timestamp precision; it does not activate another backend or make a migration bundle claim evidence.

Direct `ingest()` now reuses the existing L3 outbox when a post-gate merge fails after the L1 ESM transition. The request fails closed while preserving an explicit repair path; this is cross-store recovery parity with the main query pipeline, not a new admission path or authority mechanism.

Issue #434 reproduced that environment-selected `VELANTRIM_QUEUE_BACKEND=auto` could silently switch the Outbox between Redis and SQLite across a restart and thereby hide pending recovery work from the normal drain path. The bounded repair persists only the first automatically selected queue backend family. A later restart keeps SQLite if SQLite was locked; if Redis was locked and becomes unavailable, queue construction fails closed instead of silently falling back to an empty SQLite queue. Programmatic explicit backend construction remains a fresh one-off path. This is recovery continuity for the reproduced backend-family switch only: it is not queue migration, locator identity, federation, dual-write or distributed exactly-once behavior.

Exact-normalized ingest compatibility now includes historical `ing:*` rows through a **derived, rebuildable normalized-claim index**. The existing normalization contract remains NFC → trim → collapse whitespace → casefold. A future case/whitespace variant may route to an already-`Validated` historical raw-id fact as an occurrence instead of creating a second node. Existing fact IDs are not re-keyed; pre-existing collisions are preserved; a current normalized `fact_id` wins when present; multiple legacy collisions route future occurrences deterministically to the oldest existing row. The index is not evidence, identity inference, semantic matching or Canon authority, and dry-run resolves the same target without writing the index.

## Current validation baseline

The RRTIC architecture checkpoint push CI `31771677028` completed **9/9 SUCCESS**. Python 3.11 collected 2244 tests and completed **2231 passed / 13 skipped / 0 failed** at **100% measured line coverage**. Later bounded fixes/docs reconciliations have their own exact-head/post-merge CI and do not redefine the RRTIC architecture checkpoint. PR #440 must be judged on its own exact-head CI after every policy/test/documentation change; a prior green child commit is not evidence for a newer head.

## Backlog boundaries

- #434: **COMPLETED / CLOSED on 2026-08-16** — Outbox `auto` backend-family restart continuity only; no queue federation/migration or distributed exactly-once claim.
- #165: **COMPLETED / CLOSED by PR #431 after guarded merge** — exact normalized historical `ing:*` compatibility index only; no semantic matching and no historical re-key/merge.
- #155: **COMPLETED / CLOSED on 2026-08-14** — EPIS-001 architecture contract only; EPIS runtime remains `NOT IMPLEMENTED / NOT AUTHORIZED`.
- #214: **COMPLETED / CLOSED on 2026-08-14** — residual fixture/PII review and reproducible supply-chain pinning were reconciled in their own completed scope.

These completed scopes do not authorize EPIS runtime, a new Reader runtime, PostgreSQL activation, semantic dedupe, queue federation, or unrelated security claims. Resolve live GitHub before selecting any later work.

## Localization truth

Localization state is tracked separately in `docs/TRANSLATION_STATUS.md`; a locale's checkpoint marker must not be used as current English architecture authority. The 2026-08-19 English TruthGate/current-status reconciliation materially changes current English implementation/status prose. Localized D1 status documents therefore require a separate freshness reassessment before their prior checkpoint can be treated as proof of parity; this PR does not claim that unchanged translations already express the new policy. The bounded reassessment is tracked by Issue #441. The bounded reassessment is tracked in Issue #441 and does not authorize a nine-locale rewrite inside PR #440.

## Grant status

NLnet remains **submitted / under review / not awarded**. Approximate **€50,000** is planning context only. Budget change: none. RC-1 through RC-9, Comparator v1, NLI v1 and RRTIC-v1 are existing pre-agreement repository/research history if completed before an agreement.

## Stop boundary

RRTIC-v1 remains the frozen Reader architecture contract. The Crystal freeze closure fixes default TruthGate admission policy at the versioned `0.05` threshold and explicitly separates process-local adaptation telemetry from default admission authority. No discriminator/model/Reader runtime implementation is authorized by this scope. Do not automatically add semantic/hybrid/vector Reader runtime, FTS/ANN, activate PostgreSQL/pgvector, implement EPIS runtime, federate queues, or treat adaptive telemetry as an implicit authority source.
