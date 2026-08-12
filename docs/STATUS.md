# Velantrim Crystal — Current Status

**Status date:** 2026-08-12  
**Retained runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6` / PR #337  
**Current signed Reader baseline:** `1f5129d3276af28608b16e369fd38d21fe38c0d5` / PR #370  
**RC-6 exact post-merge CI:** `31566408978` — 9/9 successful  
**Reader RC-7 tracking:** issue #371 / draft PR #372

## Verification

Historical retained runtime evidence remains:

- Python 3.11: **2078 passed / 13 skipped / 0 failed**;
- Python 3.12: **2078 passed / 13 skipped / 0 failed**;
- **9756 statements / 100.00% line coverage**;
- **7/7** declared Ring Zero mutants killed;
- **9/9** permanent CI jobs successful;
- PostgreSQL integration CI `31256316532` successful against PostgreSQL 16 + pgvector 0.8.2.

Later Reader milestones carry their own exact-head/post-merge evidence rather than rewriting this historical checkpoint. RC-6 is fully merged. RC-7 runtime/test head `b75811e09323adbe2c74184ae0470dfb703fcf4c` passed smoke CI `31568205231` 9/9; final RC-7 implementation truth still requires final exact-head CI, guarded merge, verified signature and exact post-merge push CI.

## Storage truth

```text
SQLite ordinary active local-first
→ backup / verify / inactive restore
→ bounded logical export
→ PostgreSQL 16 + pgvector inactive import/equivalence
→ active=false
```

The PostgreSQL target is not registered for ordinary runtime reads/writes and automatic backend switching is absent.

## Reader Core bounded implementation

RC-0 is normative architecture. RC-1 through RC-6 are merged bounded milestones. RC-7 is the separately authorized current candidate-link milestone.

```text
RC-1 → SourceVersion / SourceLocator / ReaderSession / fidelity / coverage
RC-2 → caller-supplied version-bound Structural Document Map
RC-3 → explicit deterministic multi-pass ledger and substantive outcomes
RC-4 → source-linked EXTRACTED_PROPOSITION candidates
RC-5 → same-session/same-version explicit relation candidates
RC-6 → bounded long-context working sets + caller-supplied SUMMARY
RC-7 → explicit cross-document candidate links with exact two-sided provenance
```

Machine truth on the RC-7 implementation line:

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
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
```

No contradiction resolution/winner selection or evidence admission is performed.

### RC-6 boundary

Runtime: `core/reader_long_context.py`.

RC-6 revalidates current direct RC-4 leaves, orders by RC-2 structure + candidate ID and builds bounded working sets under candidate/source-locator limits. Candidate provenance is atomic. Optional RC-5 relation IDs are carried only when both endpoints are already in-set. Caller-supplied `SourceFidelity.SUMMARY` retains direct RC-4 leaf provenance.

```text
working-set coverage != comprehension proof
summary != source text
summary != evidence
summary != verified fact
summary != Canon admission
```

RC-6 is merged under PR #370; the prior “implementation pending” wording is obsolete and superseded by signed `main@1f5129d3276af28608b16e369fd38d21fe38c0d5` plus post-merge CI `31566408978`.

### RC-7 boundary

Runtime: `core/reader_cross_document.py`.

`ReaderCrossDocumentRegistry` requires explicit RC-4 extractors covering at least two different document identities. Each link names current registered RC-4 candidates from different documents and revalidates both session/source/pass/structure/coverage/card chains before registration.

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

Symmetric `CONTRADICTS`, `SAME_TOPIC`, `POSSIBLE_SAME_CLAIM` canonicalize side order; all other kinds preserve direction. Exact source/session/candidate/pass/node/primary+supporting locator provenance and explicit rationale are stored. Optional inspection basis is descriptive only.

```text
cross-document link != Canon relation
cross-document support != admitted evidence
cross-document contradiction candidate != confirmed contradiction
same-topic != same proposition
possible-same-claim != claim identity
similarity signal != identity proof
repetition across sources != corroboration
```

## Authority boundary

```text
physical L3            = multi-status storage
strict Canon           = trusted read projection
Reader artifact        = source-linked pre-admission/process state
Reader relation        = relation candidate
Reader working set     = bounded context snapshot
Reader SUMMARY         = caller-supplied synthesis candidate
Reader cross-doc link  = explicit comparison candidate
successful import      != backend activation
```

RC-1..RC-7 do not call themselves evidence/truth/Canon. Guardian, TruthGate, TrustSnapshot and CanonicalView remain unchanged. RC-7 adds no automatic semantic matching, entity resolution, claim dedupe, embeddings/ANN/vector DB, LLM/provider/parser/OCR, automatic corroboration, contradiction resolution, planner authority, Reader DB/API/CLI/worker or PostgreSQL activation.

## Localization truth

Russian Reader-dependent public/detail surfaces are current against immutable RC-6 English checkpoint `ed96a88369f841bdb2ffd79ca020acef174685fc`. RC-7 English source is committed before Russian parity. Eight other Reader-dependent locale packs remain rich `REFRESH_NEEDED` translations — 64 tracked documents. D2 and Quick Start remain current across all nine locales.

## Grant status

NLnet is **submitted / under review / not awarded**. Approximate **€50,000** is planning only, not an approved budget/payment commitment. **Budget change: none.** RC-0 through RC-6 are existing pre-agreement baseline. If RC-7 merges before an agreement, it also becomes existing baseline and cannot be counted again as future funded delta.

## Still absent

- active PostgreSQL read/write runtime selection, automatic switching/cutover/rollback;
- semantic/vector retrieval implementation or accepted ANN thresholds;
- automatic Reader parser/OCR/multimodal/model-provider generation;
- automatic cross-document semantic identity/equivalence/deduplication;
- automatic evidence admission or contradiction winner selection;
- planner/autonomous research/belief-update authority;
- dedicated/full autonomous Semantic Reading runtime.
