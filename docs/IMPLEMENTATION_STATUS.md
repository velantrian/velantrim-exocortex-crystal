# Implementation Status: Crystal vs Future Exo-Cortex Work

**Status date:** 2026-08-13  
**Retained runtime checkpoint:** `bbd816c` / PR #337  
**Signed RC-7 Reader baseline:** `main@b5541ce504af9002c8d3e2dcfa44ef4c0ead86c1` / PR #372  
**RC-7 post-merge CI:** `31572918731` — 9/9 successful  
**Signed RC-8 merge:** `main@bd85479e014c26ddebd0f4ae06385ce6625f5ab6` / PR #374  
**RC-8 exact-head/post-merge CI:** `31581756932` / `31582325275` — successful  
**Signed RC-9 merge:** `main@f8b7d7ea36625b6589a4cf02f12b94c5f98fdb61` / PR #376  
**RC-9 exact validated head:** `1956cbd45e5a5b794852354ed2233bf1fb6e318f`  
**RC-9 exact-head/post-merge CI:** `31593097846` / `31594027040` — 9/9 successful  
**RC-10 preregistration merge:** `main@430e643a2a3759da793f700617a327d419439dde` / PR #378; issue #377 closed / completed  
**Post-grant-reconciliation checkpoint:** `main@59cf060629c25ddf0747ca46ea1fadf87fa86857`, CI `31620098274` — 9/9 successful  
**Current bounded milestone:** issue #382 — post-RC-10 evaluation adequacy architecture decision; **no runtime capability**  
**Machine-readable status:** [status/implementation-manifest.json](./status/implementation-manifest.json)

| Component | Status | Current boundary |
|---|---|---|
| Guardian / TruthGate / strict read projection | Implemented | Reader/storage/retrieval artifacts cannot bypass authority |
| Read-only HTTP/CLI/MCP query boundary | Implemented | ordinary queries do not mutate Canon |
| SQLite backup/verify/inactive restore | Implemented/tested | restore is inactive and never admission |
| Bounded-streaming logical export | Implemented/tested | canonical backend-neutral bundle |
| Inactive PostgreSQL/pgvector import | Implemented/tested | target remains `active=false` |
| Active PostgreSQL runtime adapter | Not implemented | absent from ordinary runtime composition |
| Automatic SQLite/PostgreSQL switching | Forbidden | import/equivalence success is not selection |
| Exact-vs-ANN / semantic Reader comparison | Not executed | PR #378 preregisters the frozen screen; #382 does not execute it |
| Reader Core RC-0 architecture | Documented | normative authority/validation contract |
| Reader Core RC-1 skeleton | Implemented/merged | `core/reader_core.py` |
| Reader Core RC-2 structural map | Implemented/merged | `core/reader_structure.py` |
| Reader Core RC-3 multi-pass mechanics | Implemented/merged | `core/reader_passes.py` |
| Reader Core RC-4 proposition extraction | Implemented/merged | `core/reader_extraction.py` |
| Reader Core RC-5 relation candidates | Implemented/merged | `core/reader_relations.py` |
| Reader Core RC-6 long-context strategy | Implemented/tested/merged | `core/reader_long_context.py` |
| Reader Core RC-7 cross-document candidate links | Implemented/tested/merged | `core/reader_cross_document.py`; PR #372 |
| Reader RC-8 retrieval architecture decision | Completed architecture/research | PR #374; no semantic/vector runtime |
| Reader RC-9 lexical candidate discovery | Implemented/tested/merged bounded baseline | `core/reader_lexical_discovery.py`; PR #376; PRE-ADMISSION inspection only |
| RC-10 reuse/comparison preregistration | Completed architecture/eval contract | PR #378; issue #377 closed; no comparison execution/runtime |
| Post-RC-10 evaluation adequacy decision | Current architecture/research | issue #382; no comparator/model/runtime |
| Reader Retrieval Evaluation Surface v2 | Selected next bounded milestone, NOT STARTED | stronger pre-frozen judged evaluation + RC-9 control reproduction |
| Reader semantic/hybrid/vector retrieval | Not implemented | separate future authorization/evidence required |
| Reader SQLite FTS index | Not implemented | future feature-detected scaling option only after measured scale need |
| Dedicated/full Semantic Reading runtime | Not implemented | `dedicated_reader_core=false` |
| Post-RC-9 grant presentation reconciliation | Completed | issue #379 / PR #380 / PR #381; final checkpoint `59cf0606...` |

## Reader implementation chain

```text
SourceVersion + SourceLocator
→ RC-1 ReaderSession
→ RC-2 DocumentStructuralMap
→ RC-3 explicit reading passes
→ RC-4 EXTRACTED_PROPOSITION candidates
   ├─ RC-5 same-source relation candidates
   ├─ RC-6 bounded working sets / caller-supplied SUMMARY
   ├─ RC-7 explicit cross-document candidate links
   └─ RC-9 deterministic lexical candidate discovery → inspection only
→ PR #378 reuse/preregistration contract → no comparison executed
→ #382 evaluation-adequacy architecture decision → Evaluation Surface v2 selected, not started
→ explicit downstream review/evidence/admission path
→ Guardian → TruthGate → strict Canon projection
```

RC-8 defined the discovery/identity boundary. RC-9 measured the deterministic lexical baseline.
PR #378 freezes reuse constraints and a future comparison gate before any semantic/hybrid result
is observed. #382 does not execute that gate; it determines what evidence should precede a model
comparison.

## RC-4 through RC-7 retained authority markers

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
cross-document support != admitted evidence
cross-document contradiction candidate != confirmed contradiction
same-topic != same proposition
possible-same-claim != claim identity
similarity signal != identity proof
repetition across sources != corroboration
```

RC-5 relation kinds remain `POSSIBLE_CONTRADICTION`, `TENSION`, `EXCEPTION`, `QUALIFICATION`.
No contradiction winner/evidence admission is implied.

## RC-8 post-RC-7 architecture decision

Durable decision: [READER_RC8_RETRIEVAL_DECISION.md](./architecture/READER_RC8_RETRIEVAL_DECISION.md).
Existing admitted-memory retrieval (`core/embedding.py`, `core/legacy_retrieval.py`,
`core/retrieval_config.py`, `core/query_pipeline.py`, `core/rrf.py`) is a separate authority
domain.

```text
retrieval match          != evidence
similarity               != identity
repetition               != corroboration
cross-document candidate != Canon relation
ranking                  != epistemic authority
candidate discovery      != candidate adjudication
```

Semantic/hybrid retrieval may be compared later under separately frozen evidence gates;
embeddings/ANN/vector do not become Reader authority by reuse.

## RC-9 deterministic lexical candidate-discovery baseline — COMPLETE

Architecture/result: [READER_RC9_LEXICAL_BASELINE.md](./architecture/READER_RC9_LEXICAL_BASELINE.md).
Runtime: `core/reader_lexical_discovery.py`. Frozen result:
`../eval/reader_rc9_lexical_baseline.json`.

RC-9 is stdlib-only/offline/in-memory deterministic BM25 candidate discovery. It adds no
model/provider, FTS/vector schema, network call, public Reader interface, evidence write or RC-7
auto-registration.

Frozen K=5:

| Metric | Result |
|---|---:|
| Recall@5 | 0.937500 |
| Precision@5 | 0.187500 |
| MRR | 0.895833 |
| Paired hard-negative rate@5 | 1.000000 |
| Useful paired hits | 15 / 16 |
| Hard-negative paired hits | 4 / 4 |

Classification: `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`. Candidate discovery remains separate
from candidate adjudication. The cross-lingual pair `rc8-004` is missed and all four paired
hard negatives surface at K=5.

These metrics are retrieval evidence, not semantic accuracy, identity accuracy, truth accuracy
or evidence-admission accuracy.

## PR #378 / issue #377 — RC-10 preregistration COMPLETE, NO COMPARISON

Contract: [READER_RC10_RETRIEVAL_REUSE_PREREGISTRATION.md](./architecture/READER_RC10_RETRIEVAL_REUSE_PREREGISTRATION.md).
Machine-readable preregistration: `../eval/reader_rc10_retrieval_comparison_preregistration.json`.

Reuse disposition remains:

- `core/rrf.py`: future isolated Reader comparison ordering helper only;
- hashing/trigram embedders: comparator signals only;
- SentenceTransformer: future optional comparator only after separate pinned model/dependency/privacy authorization;
- `get_embedder("auto")`: forbidden for a qualifying preregistered comparison;
- admitted-memory pipeline/query/legacy-retrieval modules: no direct PRE-ADMISSION Reader wiring;
- SQLite FTS: not implemented for Reader;
- PostgreSQL/pgvector: inactive and not authorized.

The frozen future gate requires retaining RC-9's 15 useful hits, recovering `rc8-004` to 16/16
Recall@5, MRR >=0.895833, paired hard-negative hits <=2/4, zero authority violations, exact
backend identity, zero query-time network calls and no external source-text transmission.

```text
comparison pass != runtime authorization
```

No semantic/hybrid comparison has been executed. Issue #377 is closed / completed as bookkeeping
for this already-merged preregistration milestone.

## Post-RC-9 public/grant reconciliation — COMPLETE

Issue #379 / PR #380 / PR #381 reconciled public/grant truth to the signed Reader baseline.
Final signed checkpoint: `main@59cf060629c25ddf0747ca46ea1fadf87fa86857`; exact push CI
`31620098274` — 9/9 successful.

The milestone added no runtime capability and is no longer the current work item.

## Post-RC-10 evaluation adequacy decision — #382

Durable decision: [READER_POST_RC10_REASSESSMENT.md](./architecture/READER_POST_RC10_REASSESSMENT.md).
Machine-readable decision: `../eval/reader_post_rc10_reassessment.json`.

The central finding is:

```text
measured retrieval-quality gap != measured scaling gap
```

RC-9 demonstrates a cross-lingual recall gap and hard-negative behavior. It does not demonstrate
a Reader scale/latency blocker. Therefore SQLite FTS/ANN/server infrastructure is not the
smallest justified next mechanism.

The existing deterministic hash/trigram embedders remain lexical/morphological comparison
signals. `core/rrf.py` remains a pure ranking fusion utility. A future multilingual semantic
comparator is plausible for the cross-lingual gap, but no exact model/revision/dependency/privacy
contract is selected or executed here.

The selected next bounded milestone is **Reader Retrieval Evaluation Surface v2**. It must freeze
a stronger judged evaluation surface before model-backed comparator results, preserve the RC-8
fixture and RC-10 screen unchanged, and reproduce RC-9 as control. It is **NOT STARTED** by #382.

A later comparator requires a separate issue/authorization and must pass both the unchanged
RC-10 screen and the stronger evaluation before architecture review. Even then:

```text
comparison pass != runtime authorization
```

## Machine truth

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

No `reader_core_rc9_*`, `reader_core_rc10_*` or post-RC-10 machine flag is added because these do
not represent a complete dedicated autonomous Reader runtime.

## Backlog isolation

- #165: exact normalized ingest dedupe/migration only; no semantic matching.
- #155: downstream Epistemic Router/Evidence State RFC.
- #214: PII fixture / reproducible supply-chain hygiene.
- #382: architecture/evaluation decision only.

## Explicit non-features

No automatic Reader parser/chunker/OCR/PDF-layout/multimodal engine, model/provider proposition
generation, semantic/hybrid/vector Reader runtime, automatic semantic identity/entity resolution,
contradiction winner, planner/belief-update authority, evidence/Canon/ESM mutation, durable Reader
retrieval schema, public Reader API/CLI/worker, active PostgreSQL runtime selection or dedicated/
full autonomous Reader exists.

Evaluation Surface v2 is selected but not started. No model-backed comparator has been executed.

## Localization

Russian Reader-dependent D1/D3/D4/D5 surfaces remain tied to the immutable RC-7 English source
checkpoint `ab3ad31c437647535030e371d58f456faf14017b`; eight other Reader-dependent locale packs
remain `REFRESH_NEEDED`, 64 tracked detail documents. The grant reconciliation advanced the
English root/grant presentation to post-RC-9 truth. #382 adds English architecture/evaluation
truth only; broad localization remains separate and localized files must not be represented as
newer than their recorded checkpoints.

## Grant truth

NLnet remains **submitted / under review / not awarded**. Approximate €50,000 is planning only;
budget change none. RC-1 through RC-9 are existing pre-agreement Reader baseline, not awarded
delivery. PR #378's preregistration and #382's architecture decision are existing pre-agreement
repository history if merged before any agreement, not funded Reader runtime capability.