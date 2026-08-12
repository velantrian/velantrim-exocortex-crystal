# Velantrim Crystal — Current Status

**Status date:** 2026-08-12  
**Retained runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6` / PR #337  
**Current signed Reader baseline at RC-8 audit start:** `b5541ce504af9002c8d3e2dcfa44ef4c0ead86c1` / PR #372  
**RC-7 exact validated head:** `b1cf79594f702194b4dce66ac2ef2546d4154f15`  
**RC-7 exact-head CI:** `31572324596` — 9/9 successful  
**RC-7 post-merge CI:** `31572918731` — 9/9 successful  
**Current bounded milestone:** issue #373 — RC-8 post-RC-7 retrieval architecture decision

## Verification

Historical retained runtime evidence remains:

- Python 3.11: **2078 passed / 13 skipped / 0 failed**;
- Python 3.12: **2078 passed / 13 skipped / 0 failed**;
- **9756 statements / 100.00% line coverage**;
- **7/7** declared Ring Zero mutants killed;
- **9/9** permanent CI jobs successful;
- PostgreSQL integration CI `31256316532` successful against PostgreSQL 16 + pgvector 0.8.2.

Later Reader milestones carry their own exact-head/post-merge evidence rather than rewriting that historical runtime checkpoint. RC-7 is fully merged and its merge commit signature is verified / valid.

## Storage truth

```text
SQLite ordinary active local-first
→ backup / verify / inactive restore
→ bounded logical export
→ PostgreSQL 16 + pgvector inactive import/equivalence
→ active=false
```

The PostgreSQL target is not registered for ordinary runtime reads/writes. Automatic backend switching, cutover and rollback are absent.

## Reader Core bounded implementation

RC-0 is normative architecture. RC-1 through RC-7 are merged bounded milestones.

```text
RC-1 → SourceVersion / SourceLocator / ReaderSession / fidelity / coverage
RC-2 → caller-supplied version-bound Structural Document Map
RC-3 → explicit deterministic multi-pass ledger and substantive outcomes
RC-4 → source-linked EXTRACTED_PROPOSITION candidates
RC-5 → same-session/same-version explicit relation candidates
RC-6 → bounded long-context working sets + caller-supplied SUMMARY
RC-7 → explicit cross-document candidate links with exact two-sided provenance
RC-8 → architecture/research decision about discovery/identity/retrieval evaluation; no runtime retrieval
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

### RC-4 boundary

RC-4 accepts caller-supplied normalized propositions only when anchored to a `COMPLETED` RC-3 pass and current matching `PROCESSED` / `REVISITED` coverage. `FACTUAL_ASSERTION` records source presentation, not Crystal verification.

```text
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
```

### RC-5 boundary

Runtime: `core/reader_relations.py`.

`ReaderRelationRegistry` accepts current registered RC-4 IDs from one OPEN ReaderSession / exact SourceVersion and registers `POSSIBLE_CONTRADICTION`, `TENSION`, `EXCEPTION`, `QUALIFICATION` with exact two-sided provenance and rationale.

```text
reader_core_rc5_relation_candidates = true
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
```

No contradiction resolution/winner selection or evidence admission is performed.

### RC-6 boundary

Runtime: `core/reader_long_context.py`.

RC-6 builds deterministic bounded working sets over current RC-4 leaves, carries only already in-set RC-5 relation context, and permits caller-supplied `SourceFidelity.SUMMARY` artifacts with direct leaf provenance.

```text
working-set coverage != comprehension proof
summary != source text
summary != evidence
summary != verified fact
summary != Canon admission
```

### RC-7 boundary

Runtime: `core/reader_cross_document.py`.

`ReaderCrossDocumentRegistry` requires explicit RC-4 extractors covering at least two different document identities. Each link names current registered RC-4 candidates from different documents and revalidates source/session/pass/structure/coverage/provenance before registration.

Candidate kinds:

```text
SUPPORTS
CONTRADICTS
ELABORATES
REFERENCES
DEFINES
EXAMPLE_OF
PREREQUISITE_FOR
SAME_TOPIC
POSSIBLE_SAME_CLAIM
```

Optional inspection basis is descriptive only. RC-7 provides no numeric similarity, evidence sufficiency, identity, winner or Canon authority.

```text
cross-document link != Canon relation
cross-document support != admitted evidence
cross-document contradiction candidate != confirmed contradiction
same-topic != same proposition
possible-same-claim != claim identity
similarity signal != identity proof
repetition across sources != corroboration
```

## RC-8 architecture decision

Tracking issue: #373. Durable decision: `docs/architecture/READER_RC8_RETRIEVAL_DECISION.md`. Synthetic adversarial corpus: `eval/reader_rc8_retrieval_adversarial.jsonl`.

The live audit found that RC-7 can **register** explicit pairs but does not **discover** useful pairs across a corpus. Reader also lacks an adjudication contract separating:

- same proposition candidate;
- paraphrase candidate;
- related claim;
- same topic;
- possible contradiction;
- merely similar.

Crystal already has admitted-memory/query retrieval machinery in `core/embedding.py`, `core/legacy_retrieval.py`, `core/retrieval_config.py`, `core/query_pipeline.py` and `core/rrf.py`. That machinery belongs to a different authority domain from PRE-ADMISSION Reader artifacts and is not directly wired into Reader by RC-8.

RC-8 decision:

```text
retrieval match          != evidence
similarity               != identity
repetition               != corroboration
cross-document candidate != Canon relation
ranking                  != epistemic authority
candidate discovery      != candidate adjudication
```

The architecture decision compares deterministic exact/token indexing, SQLite FTS, hashing-vector signals, hybrid rank fusion, neural embeddings, ANN/vector backends and PostgreSQL/pgvector. Result: **semantic/vector Reader retrieval is deferred pending measured evidence**. A separately authorized future implementation should establish the deterministic lexical candidate-discovery baseline and benchmark runner first. RC-8 does not start that implementation.

## Backlog boundaries

- #165: exact normalized ingest dedupe/migration only; explicitly not semantic matching. Separate from Reader semantic identity.
- #155: downstream Epistemic Router / Evidence State RFC. Separate from PRE-ADMISSION Reader candidate discovery.
- #214: fixture/PII/supply-chain hygiene. RC-8 adds no mandatory dependency or production data surface.

## Authority boundary

```text
physical L3            = multi-status storage
strict Canon           = trusted read projection
Reader artifact        = source-linked pre-admission/process state
Reader relation        = relation candidate
Reader working set     = bounded context snapshot
Reader SUMMARY         = caller-supplied synthesis candidate
Reader cross-doc link  = explicit comparison candidate
retrieval candidate    = item proposed for inspection
successful import      != backend activation
```

Guardian, TruthGate, TrustSnapshot and CanonicalView remain unchanged. RC-8 performs no Reader runtime mutation and grants no evidence/truth/Canon/planner authority.

## Localization truth

Russian root + Reader-dependent D1/D3/D4/D5 surfaces are `CURRENT` to the immutable RC-7 English source checkpoint `ab3ad31c437647535030e371d58f456faf14017b`. Eight other Reader-dependent locale packs remain rich `REFRESH_NEEDED` translations — **64 tracked documents**. D2 reviewer/safety and Quick Start remain current across all nine supported locales.

RC-8 adds English architecture/research source material only; it does not silently mark the eight locale packs current and does not rewrite the RC-7 localization checkpoint.

## Grant status

NLnet is **submitted / under review / not awarded**. Approximate **€50,000** is planning only, not an approved budget/payment commitment. **Budget change: none.** RC-0 through RC-7 are existing pre-agreement baseline when merged before an agreement. RC-8 is an architecture/research decision only and does not create a new implemented Reader runtime capability.

## Still absent after RC-8

- corpus-scale Reader candidate-discovery runtime;
- SQLite FTS Reader index;
- semantic/vector Reader retrieval implementation or accepted semantic thresholds;
- ANN/vector Reader index;
- automatic semantic identity/equivalence/entity resolution/deduplication;
- automatic Reader parser/OCR/multimodal/model-provider generation;
- automatic evidence admission or contradiction winner selection;
- planner/autonomous research/belief-update authority;
- active PostgreSQL read/write runtime selection, automatic switching/cutover/rollback;
- dedicated/full autonomous Semantic Reading runtime.

## Completion boundary

Issue #373 is complete only after exact-head CI, review gate, guarded merge to verified `main`, post-merge CI, synchronization/read-back of the three existing Crystal Notion pages, completion evidence and issue closure. No next Reader milestone starts automatically.