# Velantrim Crystal — Current Status

**Status date:** 2026-08-12  
**Retained runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6` / PR #337  
**Signed RC-7 Reader baseline:** `b5541ce504af9002c8d3e2dcfa44ef4c0ead86c1` / PR #372  
**RC-7 post-merge CI:** `31572918731` — 9/9 successful  
**Signed RC-8 merge:** `bd85479e014c26ddebd0f4ae06385ce6625f5ab6` / PR #374  
**RC-8 exact-head/post-merge CI:** `31581756932` / `31582325275` — successful  
**Signed RC-9 merge:** `f8b7d7ea36625b6589a4cf02f12b94c5f98fdb61` / PR #376  
**RC-9 exact validated head:** `1956cbd45e5a5b794852354ed2233bf1fb6e318f`  
**RC-9 exact-head/post-merge CI:** `31593097846` / `31594027040` — 9/9 successful  
**Audited start for current docs milestone:** `main@430e643a2a3759da793f700617a327d419439dde`, CI `31603785427` — 9/9 successful  
**Current bounded milestone:** issue #379 — post-RC-9 grant presentation truth reconciliation

## Verification

The audited starting main `430e643…` is signed with `verified=true`, reason `valid`. It contains
PR #378, an RC-10 retrieval-reuse / future-comparison **preregistration contract only**. No
semantic/hybrid comparator was executed and no Reader retrieval runtime was added.

The current Reader retrieval **implementation baseline remains RC-9**. Both Python 3.11 and
3.12 passed the repository 100% coverage gate on RC-9 exact-head and post-merge CI. Ring Zero,
code-quality, security, eval, JSONL-integrity, Docker and docs-status were green.

Historical retained runtime evidence remains 2078 passed / 13 skipped / 0 failed, 9756
statements / 100.00% coverage at `bbd816c...`; later Reader milestones carry separate exact
evidence instead of rewriting that historical checkpoint.

## Storage truth

```text
SQLite ordinary active local-first
→ backup / verify / inactive restore
→ bounded logical export
→ PostgreSQL 16 + pgvector inactive import/equivalence
→ active=false
```

The PostgreSQL target is not registered for ordinary runtime reads/writes. Automatic backend
switching, cutover and rollback are absent. Issue #379 adds no storage/index schema or runtime
change.

## Reader Core bounded implementation

RC-0 is normative architecture. RC-1 through RC-7 are merged bounded runtime/domain milestones.
RC-8 is the completed retrieval architecture/research decision. RC-9 is the completed bounded
PRE-ADMISSION lexical candidate-discovery implementation baseline. PR #378's RC-10 content is
architecture/evaluation preregistration only.

```text
RC-1 → SourceVersion / SourceLocator / ReaderSession / fidelity / coverage
RC-2 → caller-supplied version-bound Structural Document Map
RC-3 → explicit deterministic multi-pass ledger and substantive outcomes
RC-4 → source-linked EXTRACTED_PROPOSITION candidates
RC-5 → same-session/same-version explicit relation candidates (`core/reader_relations.py`)
RC-6 → bounded long-context working sets + caller-supplied SUMMARY
RC-7 → explicit cross-document candidate links with exact two-sided provenance
RC-8 → discovery/identity/retrieval architecture decision
RC-9 → deterministic lexical candidate discovery + benchmark; inspection only
PR #378 → reuse matrix + frozen future comparison gate; no comparison run/runtime
```

Machine implementation truth:

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

RC-8/RC-9/PR #378 do not turn `dedicated_reader_core` true and do not create a complete
autonomous Reader machine flag.

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
cross-document support != admitted evidence
cross-document contradiction candidate != confirmed contradiction
same-topic != same proposition
possible-same-claim != claim identity
similarity signal != identity proof
repetition across sources != corroboration
retrieval match != evidence
similarity != identity
ranking != epistemic authority
candidate discovery != candidate adjudication
comparison pass != runtime authorization
```

Guardian, TruthGate, TrustSnapshot and CanonicalView remain unchanged. Public `HTTP /ask`, `CLI
ask` and `MCP search` remain admitted-memory read-only query surfaces, not Reader RC-9 interfaces.

## RC-8 architecture decision — COMPLETE

Issue #373 / PR #374 completed. Durable decision:
`docs/architecture/READER_RC8_RETRIEVAL_DECISION.md`. Corpus:
`eval/reader_rc8_retrieval_adversarial.jsonl`.

Existing admitted-memory retrieval (`core/embedding.py`, `core/legacy_retrieval.py`,
`core/retrieval_config.py`, `core/query_pipeline.py`, `core/rrf.py` and related composition) is
a different authority/data lifecycle from PRE-ADMISSION Reader artifacts.

RC-8 required deterministic lexical candidate discovery before any separately authorized
semantic/vector comparison.

## RC-9 deterministic lexical baseline — COMPLETE

Runtime: `core/reader_lexical_discovery.py`. Runner: `scripts/bench_reader_rc9_lexical.py`.
Architecture/result: `docs/architecture/READER_RC9_LEXICAL_BASELINE.md`. Frozen result:
`eval/reader_rc9_lexical_baseline.json`.

RC-9 performs conservative NFKC/case/whitespace normalization, stable tokenization and
deterministic in-memory BM25 ranking over Reader proposition snapshots. It adds no network/model
dependency, FTS/vector schema, public Reader API or authority mutation.

Frozen K=5 result:

| Metric | Result |
|---|---:|
| Recall@5 | 0.937500 |
| Precision@5 | 0.187500 |
| MRR | 0.895833 |
| Paired hard-negative rate@5 | 1.000000 |
| Useful paired hits | 15 / 16 |
| Hard-negative paired hits | 4 / 4 |

The measured architecture classification is `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`. The
cross-lingual paraphrase `rc8-004` is missed and all four paired hard negatives surface at K=5.
These are retrieval metrics, not semantic/adjudication accuracy.

## PR #378 reuse compatibility / comparison preregistration

Tracking issue #377 remains separate. Contract:
`docs/architecture/READER_RC10_RETRIEVAL_REUSE_PREREGISTRATION.md`. Machine-readable gate:
`eval/reader_rc10_retrieval_comparison_preregistration.json`.

The contract freezes future comparison requirements before results and records which existing
admitted-memory helpers may be evaluated. It explicitly does **not** execute a semantic/hybrid
comparison, implement Reader FTS/vector runtime, add a model dependency, or activate
PostgreSQL/pgvector.

```text
comparison pass != runtime authorization
```

## Current grant-presentation milestone — #379

The live audit found public/grant surfaces behind the signed Reader implementation truth:

- root README still showed RC-6 authoritative / RC-7 draft;
- grant scope and baseline-funded-delta matrix still stopped at RC-5 / RC-6-in-progress;
- the D4 docs-status validator itself required stale RC-5 grant wording.

Issue #379 reconciles English public/grant surfaces to RC-9, adds exact benchmark naming and
limitations, adds a reviewer reproduction path and hardens semantic docs-status markers against
regression. It is documentation-heavy and must not change `core/**`.

## Backlog boundaries

- #165: exact normalized admitted-fact dedupe/migration only; no semantic matching.
- #155: downstream Epistemic Router / Evidence State RFC.
- #214: fixture/PII/supply-chain hygiene.
- #377: separate RC-10 preregistration/completion bookkeeping; #379 does not execute its comparator.

## Localization truth

Russian root + Reader-dependent D1/D3/D4/D5 surfaces remain tied to the immutable RC-7 English
checkpoint `ab3ad31c437647535030e371d58f456faf14017b`. Eight other Reader-dependent locale packs
remain rich `REFRESH_NEEDED` translations — 64 tracked detail documents. D2 and Quick Start
remain current where source semantics did not change.

Issue #379 advances English root/grant meaning to post-RC-9 truth but deliberately does not run
a broad translation refresh. Localized files must not be represented as newer than their
recorded source checkpoints.

## Grant status

NLnet is **submitted / under review / not awarded**. Approximate **€50,000** is planning only;
budget change none. RC-1 through RC-9 merged pre-agreement are existing baseline and cannot be
counted again as future funded delivery. PR #378's preregistration is existing pre-agreement
history, not a funded Reader runtime.

## Completion boundary

Issue #379 is complete only after exact-head CI, independent semantic review, guarded merge to
verified `main`, exact post-merge CI, synchronization/read-back of the three existing Crystal
Notion pages, completion evidence, closure and final live audit.

No semantic/hybrid comparison, embeddings/vector Reader runtime, FTS, PostgreSQL/pgvector
activation, #155/#165/#214 or broad localization starts automatically.
