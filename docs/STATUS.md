# Velantrim Crystal — Current Status

**Status date:** 2026-08-13  
**Retained runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6` / PR #337  
**Signed RC-7 Reader baseline:** `b5541ce504af9002c8d3e2dcfa44ef4c0ead86c1` / PR #372  
**RC-7 post-merge CI:** `31572918731` — 9/9 successful  
**Signed RC-8 merge:** `bd85479e014c26ddebd0f4ae06385ce6625f5ab6` / PR #374  
**RC-8 exact-head/post-merge CI:** `31581756932` / `31582325275` — successful  
**Signed RC-9 merge:** `f8b7d7ea36625b6589a4cf02f12b94c5f98fdb61` / PR #376  
**RC-9 exact validated head:** `1956cbd45e5a5b794852354ed2233bf1fb6e318f`  
**RC-9 exact-head/post-merge CI:** `31593097846` / `31594027040` — 9/9 successful  
**RC-10 preregistration merge:** `430e643a2a3759da793f700617a327d419439dde` / PR #378; issue #377 closed / completed  
**Post-grant-reconciliation checkpoint:** `main@59cf060629c25ddf0747ca46ea1fadf87fa86857`, CI `31620098274` — 9/9 successful  
**Current bounded milestone:** issue #382 — post-RC-10 evaluation adequacy / next-milestone architecture decision

## Verification

The current audited main entering #382 is signed with `verified=true`, reason `valid`. It contains
RC-9 as the implemented Reader retrieval baseline, PR #378 as the RC-10 retrieval-reuse /
future-comparison **preregistration contract only**, and the completed post-RC-9 grant
presentation reconciliation (#379 / PR #380 / PR #381).

Issue #377 is now closed / completed after the missing completion-evidence bookkeeping step was
repaired. That closure creates no comparator or runtime authorization.

The current Reader retrieval **implementation baseline remains RC-9**. Both Python 3.11 and
3.12 passed the repository 100% coverage gate on RC-9 exact-head and post-merge CI. Ring Zero,
code-quality, security, eval, JSONL-integrity, Docker and docs-status were green. Current-main
push CI `31620098274` is also 9/9 successful.

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
switching, cutover and rollback are absent. Issue #382 adds no storage/index schema or runtime
change. Reader SQLite FTS remains unimplemented.

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
#382 → post-RC-10 evaluation adequacy decision; no comparator run/runtime
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

RC-8/RC-9/PR #378/#382 do not turn `dedicated_reader_core` true and do not create a complete
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

## PR #378 / issue #377 — RC-10 preregistration COMPLETE

Contract: `docs/architecture/READER_RC10_RETRIEVAL_REUSE_PREREGISTRATION.md`. Machine-readable
gate: `eval/reader_rc10_retrieval_comparison_preregistration.json`.

The contract freezes future comparison requirements before results and records which existing
admitted-memory helpers may be evaluated. It explicitly does **not** execute a semantic/hybrid
comparison, implement Reader FTS/vector runtime, add a model dependency, or activate
PostgreSQL/pgvector.

Issue #377 is closed / completed. Its closure is completion bookkeeping for PR #378, not a future
execution gate.

```text
comparison pass != runtime authorization
```

## Post-RC-9 grant presentation reconciliation — COMPLETE

Issue #379 / PR #380 plus final-audit repair PR #381 completed the public/grant truth
reconciliation. Final signed checkpoint is `main@59cf060629c25ddf0747ca46ea1fadf87fa86857`;
exact push CI `31620098274` is 9/9 successful.

No `core/**`, Reader runtime, dependency, storage schema, backend activation or epistemic
authority was added by that milestone.

## Current post-RC-10 architecture reassessment — #382

Durable decision: `docs/architecture/READER_POST_RC10_REASSESSMENT.md`. Machine-readable decision:
`eval/reader_post_rc10_reassessment.json`.

The audit separates two questions:

```text
measured retrieval-quality gap != measured scaling gap
```

RC-9 has measured retrieval-quality gaps: the EN/RU cross-lingual useful pair `rc8-004` is
missed, and all four paired hard negatives surface at K=5. No current benchmark demonstrates a
Reader corpus-size/latency/resource blocker that would justify FTS/ANN/server infrastructure as
the next mechanism.

The option decision is therefore:

- keep RC-9 as frozen deterministic control/fallback;
- defer SQLite FTS until scale evidence exists;
- keep `core/rrf.py` as a future pure ordering utility only;
- keep hashing/trigram embedders as comparator control signals only;
- do not execute the current optional SentenceTransformer path as a qualifying Reader comparator
  without separately pinned model/dependency/privacy authorization;
- do not authorize ANN/vector DB or PostgreSQL/pgvector for Reader;
- select **Reader Retrieval Evaluation Surface v2** as the smallest next bounded milestone.

Evaluation Surface v2 is **NOT STARTED by #382**. It must be separately authorized and must freeze
a stronger judged evaluation surface plus reproduce the unchanged RC-9 control before any
model-backed comparator result is observed.

The original RC-10 screen remains unchanged. Any later comparator still must retain the RC-9
15 useful hits, recover `rc8-004`, maintain MRR >=0.895833, reduce hard-negative hits to <=2/4,
introduce zero authority violations, use exact backend identity, make zero query-time network
calls and send no Reader source text externally.

## Backlog boundaries

- #165: exact normalized admitted-fact dedupe/migration only; no semantic matching.
- #155: downstream Epistemic Router / Evidence State RFC.
- #214: fixture/PII/supply-chain hygiene.
- #382: current architecture/evaluation decision only; no comparator execution/runtime.

## Localization truth

Russian root + Reader-dependent D1/D3/D4/D5 surfaces remain tied to the immutable RC-7 English
checkpoint `ab3ad31c437647535030e371d58f456faf14017b`. Eight other Reader-dependent locale packs
remain rich `REFRESH_NEEDED` translations — 64 tracked detail documents. D2 and Quick Start
remain current where source semantics did not change.

The post-RC-9 grant reconciliation advanced English root/grant meaning only. #382 adds an English
architecture decision; it does not run a broad translation refresh. Localized files must not be
represented as newer than their recorded source checkpoints.

## Grant status

NLnet is **submitted / under review / not awarded**. Approximate **€50,000** is planning only;
budget change none. RC-1 through RC-9 merged pre-agreement are existing baseline and cannot be
counted again as future funded delivery. PR #378's preregistration and #382's architecture
decision are existing pre-agreement history if merged before an agreement, not funded Reader
runtime.

## Completion boundary

Issue #382 is complete only after exact-head CI, evidence-grounded semantic review, guarded merge
to verified `main`, exact post-merge CI, synchronization/read-back of the three existing Crystal
Notion pages, completion evidence, closure and final live audit.

After that, STOP. **Evaluation Surface v2 remains not started** until separately authorized.
No semantic/hybrid comparison, embeddings/vector Reader runtime, FTS, PostgreSQL/pgvector
activation, #155/#165/#214 or broad localization starts automatically.