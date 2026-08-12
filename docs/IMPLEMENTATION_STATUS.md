# Implementation Status: Crystal vs Future Exo-Cortex Work

**Status date:** 2026-08-12  
**Retained runtime checkpoint:** `bbd816c` / PR #337  
**Signed Reader baseline:** `main@1f5129d3276af28608b16e369fd38d21fe38c0d5` / PR #370  
**RC-6 exact post-merge CI:** `31566408978` — 9/9 successful  
**Machine-readable status:** [status/implementation-manifest.json](./status/implementation-manifest.json)

| Component | Status | Current boundary |
|---|---|---|
| Guardian / TruthGate / strict read projection | Implemented | Reader/storage artifacts cannot bypass authority |
| Read-only HTTP/CLI/MCP query boundary | Implemented | ordinary queries do not mutate Canon |
| SQLite backup/verify/inactive restore | Implemented/tested | restore is inactive and never admission |
| Bounded-streaming logical export | Implemented/tested | canonical backend-neutral bundle |
| Inactive PostgreSQL/pgvector import | Implemented/tested | target remains `active=false` |
| Active PostgreSQL runtime adapter | Not implemented | absent from ordinary runtime composition |
| Automatic SQLite/PostgreSQL switching | Forbidden | import/equivalence success is not selection |
| Exact-vs-ANN retrieval evaluation | Not implemented | separately reviewed future work |
| Reader Core RC-0 architecture | Documented | normative authority/validation contract |
| Reader Core RC-1 skeleton | Implemented/merged | `core/reader_core.py` |
| Reader Core RC-2 structural map | Implemented/merged | `core/reader_structure.py` |
| Reader Core RC-3 multi-pass mechanics | Implemented/merged | `core/reader_passes.py` |
| Reader Core RC-4 proposition extraction | Implemented/merged | `core/reader_extraction.py` |
| Reader Core RC-5 relation candidates | Implemented/merged | `core/reader_relations.py` |
| Reader Core RC-6 long-context strategy | Implemented/tested/merged | `core/reader_long_context.py`; signed PR #370 merge |
| Reader Core RC-7 cross-document candidate links | Implemented/tested on PR #372 branch; final merge evidence pending | `core/reader_cross_document.py`; explicit cross-source candidates only |
| Dedicated/full Semantic Reading runtime | Not implemented | `dedicated_reader_core=false` |

## Reader implementation chain

```text
SourceVersion + SourceLocator
→ RC-1 ReaderSession
→ RC-2 DocumentStructuralMap
→ RC-3 explicit reading passes
→ RC-4 EXTRACTED_PROPOSITION candidates
   ├─ RC-5 same-source relation candidates
   ├─ RC-6 bounded working sets / caller-supplied SUMMARY
   └─ RC-7 explicit cross-document candidate links
→ normal evidence/review/admission path
→ Guardian → TruthGate → strict Canon projection
```

### RC-4

RC-4 is deterministic validation/registration, not autonomous NLP extraction. It requires completed substantive RC-3 context and current matching provenance. Candidates retain source owner, proposition presentation category, negation and qualifiers.

```text
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
```

### RC-5

`core/reader_relations.py` registers `POSSIBLE_CONTRADICTION`, `TENSION`, `EXCEPTION`, `QUALIFICATION` over valid registered RC-4 candidates inside one OPEN ReaderSession and exact SourceVersion. Exact candidate/pass/node IDs, primary/supporting locators and explicit relation rationale are preserved.

Symmetric candidates canonicalize order; directional `EXCEPTION` / `QUALIFICATION` retain direction. RC-5 has no truth/confidence/evidence-sufficiency/resolved/winner field and does not call `core.evidence.attach_evidence()`.

```text
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
```

### RC-6

`core/reader_long_context.py` is merged baseline. It plans deterministic bounded working sets from current registered RC-4 candidates inside one OPEN ReaderSession / exact SourceVersion, revalidating completed pass state, recovered RC-2 structure and current substantive coverage.

Machine details retained for executable RC-6 evidence:

```text
max_candidates_per_working_set = 128
max_source_locators_per_working_set = 512
candidate_atomicity = true
direct_rc4_leaf_provenance = true
caller_supplied_summary_only = true
summary_fidelity = SUMMARY
automatic_cross_document_reasoning = false
evidence_admission = false
truth_or_canon_authority = false
```

```text
working-set coverage != comprehension proof
summary != source text
summary != evidence
summary != verified fact
summary != Canon admission
```

### RC-7

`core/reader_cross_document.py` is the bounded RC-7 implementation tracked by issue #371 / PR #372. It accepts only current registered RC-4 candidate IDs from explicit extractor/session/source bindings and requires different document identities on the two sides.

Link vocabulary:

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

Each side preserves exact:

```text
session_id
candidate_id
pass_id
node_ids
SourceVersion
primary SourceLocator
supporting SourceLocator values
```

Before registration RC-7 revalidates OPEN session state, `EXTRACTED_PROPOSITION` fidelity, source/privacy binding, SegmentCard membership, completed pass, declared targets/substantive outcomes, recovered structure and current matching coverage.

`CONTRADICTS`, `SAME_TOPIC`, `POSSIBLE_SAME_CLAIM` are symmetric and canonicalize side ordering. `SUPPORTS`, `ELABORATES`, `REFERENCES`, `DEFINES`, `EXAMPLE_OF`, `PREREQUISITE_FOR` preserve direction. Duplicate semantic candidates fail closed.

Optional inspection basis is descriptive metadata only. No similarity score, identity field, confidence, evidence sufficiency, resolution or winner is present.

```text
cross-document link != Canon relation
cross-document support != admitted evidence
cross-document contradiction candidate != confirmed contradiction
same-topic != same proposition
possible-same-claim != claim identity
similarity signal != identity proof
repetition across sources != corroboration
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

The RC-7 branch flag is not a merge claim. Signed merged `main` plus final exact-head and post-merge CI remain final authority.

## Explicit non-features

RC-1 through RC-7 add no source-body storage, Reader durable schema, public Reader API/CLI/background worker, automatic parser/chunker/OCR/PDF-layout/multimodal engine, LLM/provider/model routing, embeddings/ANN/vector database, automatic semantic identity/entity resolution/deduplication, automatic corroboration, contradiction winner selection, planner/belief-update authority or evidence/Canon/ESM write path.

## Storage sequence

```text
SQLite ordinary active local-first
→ backup / independent verify / inactive restore
→ bounded canonical logical bundle
→ PostgreSQL preflight
→ inactive transactional import
→ independent exact-state equivalence
→ active=false
```

Successful equivalence cannot activate a backend or change Guardian, TruthGate or strict Canon.

## Localization

Russian Reader-dependent public/detail surfaces are `CURRENT` at the immutable RC-6 English source checkpoint `ed96a88369f841bdb2ffd79ca020acef174685fc`. The RC-7 English source commit is separate and precedes Russian RC-7 parity. Eight other Reader-dependent locale packs remain rich `REFRESH_NEEDED` translations; D2 and Quick Start remain current across all nine locales.

## Grant truth

NLnet remains **submitted / under review / not awarded**. Approximate €50,000 is planning only; budget change is none. RC-0 through RC-6 are existing pre-agreement baseline. If RC-7 merges pre-agreement, it also becomes existing baseline and cannot be budgeted again as future funded delta.
