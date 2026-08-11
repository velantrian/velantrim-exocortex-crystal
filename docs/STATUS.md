# Velantrim Crystal — Current Status

**Status date:** 2026-08-11  
**Retained verified runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6`  
**Retained validated head / CI:** `d7af7c80722274f9217bc5545d150f92e9363f37` / `31256316536`  
**PostgreSQL integration CI:** `31256316532`  
**Reader RC-5 tracking:** issue #367 / PR #368

GitHub merged `main`, executable tests, exact CI and the machine-readable implementation manifest are implementation truth. The retained storage/runtime checkpoint remains historical evidence; later Reader milestones carry their own exact-head and post-merge CI evidence.

## Verification baseline

- Python 3.11 / 3.12: **2078 passed / 13 skipped / 0 failed** at the retained runtime checkpoint;
- **9756 statements / 100.00% line coverage** at that checkpoint;
- **7/7** declared Ring Zero mutants killed;
- **9/9** permanent CI jobs;
- **1/1** real PostgreSQL/pgvector integration job.

Exact historical evidence: [`TEST_REPORT.md`](../TEST_REPORT.md). Reader RC-5 is accepted only with its own exact-head 9/9 CI and post-merge 9/9 CI; those run IDs are recorded in PR/issue completion evidence rather than pre-written here.

## Current storage truth

```text
SQLite ordinary active local-first runtime
→ backup / verify / inactive restore
→ bounded logical export
→ optional PostgreSQL 16 + pgvector inactive import
→ independent exact-state equivalence
→ active=false
```

PostgreSQL/pgvector is not an active ordinary runtime backend. Automatic SQLite/PostgreSQL switching, cutover, rollback, dual-write and accepted ANN production semantics remain absent.

## Reader Core bounded implementation

RC-0 is the normative architecture contract. RC-1 through RC-5 are separate bounded layers:

```text
RC-1  SourceVersion / SourceLocator / ReaderSession / SegmentCard
      fidelity + coverage + bookmarks/open loops + stale/privacy semantics
        ↓
RC-2  caller-supplied DocumentStructuralMap
      hierarchy/order + RECOVERED / AMBIGUOUS / UNSUPPORTED
        ↓
RC-3  explicit ORIENTATION / BROAD_READ / FOCUSED_READ / CROSS_CHECK / TARGETED_REREAD
      declared targets + explicit outcomes + pass state + count-only telemetry
        ↓
RC-4  source-linked EXTRACTED_PROPOSITION candidates
      source owner + presentation category + negation/qualifiers + replayable locators
        ↓
RC-5  explicit same-session/same-version Reader relation candidates
      POSSIBLE_CONTRADICTION / EXCEPTION / QUALIFICATION / TENSION
      exact RC-4 candidate IDs + both-side provenance + explicit rationale
```

Machine truth:

```text
reader_core_rc1_skeleton              = true
reader_core_rc2_structural_map        = true
reader_core_rc3_multi_pass_mechanics  = true
reader_core_rc4_proposition_extraction = true
reader_core_rc5_relation_candidates   = true
dedicated_reader_core                 = false
```

RC-5 runtime lives in `core/reader_relations.py`. It is deterministic **registration**, not automatic semantic contradiction detection. It accepts only proposition candidates already registered by one RC-4 `ReaderPropositionExtractor`, requires one OPEN `ReaderSession` and one exact `SourceVersion`, preserves both sides' candidate IDs and replayable provenance, requires a non-empty rationale, and fails closed when source/session context is stale or mismatched.

`POSSIBLE_CONTRADICTION` and `TENSION` are symmetric candidate relations and are stored in deterministic candidate-ID order. `EXCEPTION` and `QUALIFICATION` are directional and remain distinct from contradiction. Re-registering the same symmetric pair does not become corroboration.

RC-5 does not compare raw source text, infer semantic identity, call an LLM/provider, use embeddings/ANN, or perform a cross-document Reader stage. It does not invoke the existing contradiction-resolution workflow and does not choose a winner.

## Authority boundary

```text
source statement        != verified fact
Reader artifact         != admitted fact
Reader coverage         != comprehension proof
Reader pass completion  != comprehension proof
Reader structure        != epistemic authority
EXTRACTED_PROPOSITION   != verified fact
Reader candidate        != admitted evidence
relation candidate      != admitted evidence
contradiction candidate != confirmed contradiction
similarity              != identity
repetition              != corroboration
```

RC-1/RC-2/RC-3/RC-4/RC-5 retain no source body and add no durable Reader DB schema, public Reader API/CLI/background worker, automatic parser/chunker/OCR/PDF-layout/multimodal understanding, autonomous NLP/LLM extraction, provider routing, embeddings/ANN/vector database, automatic cross-document identity/reasoning, planner or belief-update authority.

They cannot mutate `truth_status`/ESM, write strict Canon, bypass Guardian/TruthGate, promote confidence, assert evidence sufficiency, attach fact evidence, or resolve contradictions automatically. `core.evidence.attach_evidence()` remains outside Reader RC-5.

## Localization

English is the primary/source technical language. Russian is the fully refreshed Reader secondary surface for the accepted RC-5 source checkpoint recorded in `docs/TRANSLATION_STATUS.md`. Eight other localized root/detail Reader surfaces preserve their rich prior translations but remain honestly `REFRESH_NEEDED`; the tracked Reader-related debt remains 64 documents. D2 and Quick Start stay `CURRENT` for all nine locales because RC-5 does not change those source semantics.

## Still absent

- dedicated/full autonomous Semantic Reading runtime;
- automatic contradiction resolution or winner selection;
- automatic semantic equivalence or cross-document Reader identity;
- active PostgreSQL runtime or automatic backend switching;
- accepted ANN production profile;
- public Reader API/CLI/background worker or durable Reader persistence;
- security/legal/GDPR certification;
- awarded NLnet funding.

## Grant status

NLnet remains **submitted / under review / not awarded**. Approximate **€50,000** remains planning only, not an approved budget or payment commitment. Budget change: none. Reader RC-0 through RC-5, when merged before any agreement, are existing pre-agreement baseline and cannot be counted again as future funded delta. Any funded Reader work must begin after the actually merged RC-5 baseline.
