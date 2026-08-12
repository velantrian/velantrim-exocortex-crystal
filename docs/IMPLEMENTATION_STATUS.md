# Implementation Status: Crystal vs Future Exo-Cortex Work

**Status date:** 2026-08-12  
**Retained runtime checkpoint:** `bbd816c` / PR #337  
**RC-7 signed Reader baseline:** `main@b5541ce504af9002c8d3e2dcfa44ef4c0ead86c1` / PR #372  
**RC-7 post-merge CI:** `31572918731` — 9/9 successful  
**RC-8 signed decision merge / RC-9 audited start:** `main@bd85479e014c26ddebd0f4ae06385ce6625f5ab6` / PR #374  
**RC-8 exact-head/post-merge CI:** `31581756932` / `31582325275` — successful  
**Current bounded milestone:** RC-9 / issue #375  
**Machine-readable status:** [status/implementation-manifest.json](./status/implementation-manifest.json)

| Component | Status | Current boundary |
|---|---|---|
| Guardian / TruthGate / strict read projection | Implemented | Reader/storage/retrieval artifacts cannot bypass authority |
| Read-only HTTP/CLI/MCP query boundary | Implemented | ordinary queries do not mutate Canon |
| SQLite local-first storage | Implemented | ordinary active local profile |
| Inactive PostgreSQL/pgvector import | Implemented/tested | target remains `active=false` |
| Active PostgreSQL runtime adapter | Not implemented | absent from ordinary runtime composition |
| Reader Core RC-1 skeleton | Implemented/merged | `core/reader_core.py` |
| Reader Core RC-2 structural map | Implemented/merged | `core/reader_structure.py` |
| Reader Core RC-3 multi-pass mechanics | Implemented/merged | `core/reader_passes.py` |
| Reader Core RC-4 proposition extraction | Implemented/merged | `core/reader_extraction.py` |
| Reader Core RC-5 relation candidates | Implemented/merged | `core/reader_relations.py` |
| Reader Core RC-6 long-context strategy | Implemented/merged | `core/reader_long_context.py` |
| Reader Core RC-7 cross-document candidates | Implemented/merged | `core/reader_cross_document.py` |
| Reader RC-8 retrieval architecture decision | Completed architecture/research | no Reader semantic/vector runtime |
| Reader RC-9 lexical candidate discovery | Implemented in bounded milestone | stdlib in-memory BM25 PRE-ADMISSION baseline; issue #375 |
| Reader semantic/hybrid/vector retrieval | Not implemented | separate future authorization required |
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
   ├─ RC-7 explicit cross-document candidate links
   └─ RC-9 lexical candidate discovery → inspection only
→ normal explicit review/evidence/admission path
→ Guardian → TruthGate → strict Canon projection
```

RC-5 preserves `POSSIBLE_CONTRADICTION`, `EXCEPTION`, `QUALIFICATION`, `TENSION` and `contradiction candidate != confirmed contradiction`.

RC-7 preserves `cross-document link != Canon relation`, `same-topic != same proposition`, `possible-same-claim != claim identity`, `similarity signal != identity proof`, `repetition across sources != corroboration`.

## RC-9 implementation contract

`core/reader_lexical_discovery.py` provides a deterministic in-memory lexical ranker over Reader PRE-ADMISSION proposition snapshots. Normalization is NFKC + casefold + whitespace collapse. Tokenization intentionally avoids semantic rewriting, stemming, translation, entity resolution and unit conversion. Material lexical distinctions such as negation, modal/quantifier words, dates, versions and numbers are retained.

`ReaderLexicalMatch` contains only query/candidate/source identifiers, lexical score, rank, retrieval method/version, matched terms and privacy metadata. It contains no identity/truth/corroboration/adjudication fields.

```text
retrieval match          != evidence
similarity               != identity
repetition               != corroboration
cross-document candidate != Canon relation
ranking                  != epistemic authority
candidate discovery      != candidate adjudication
```

The module does not call `core/embedding.py`, `core/legacy_retrieval.py`, L3, TruthGate, Guardian or evidence mutation. Existing admitted-memory retrieval remains a separate authority domain.

## RC-9 benchmark evidence

Runner: `scripts/bench_reader_rc9_lexical.py`. Frozen RC-8 input: `../eval/reader_rc8_retrieval_adversarial.jsonl`. Frozen RC-9 result: `../eval/reader_rc9_lexical_baseline.json`.

At K=5: Recall 0.937500, Precision 0.217391, MRR 0.895833, paired hard-negative rate 1.000000. The cross-lingual pair is missed; all four paired SAME_TOPIC/MERELY_SIMILAR hard negatives are retrieved in top-5.

Architecture classification: `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`. The benchmark is retrieval evidence only and does not authorize embeddings/hybrid/ANN/vector DB.

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

No new `dedicated_reader_core` claim is introduced. RC-9 is documented as a bounded implementation baseline rather than a full Reader runtime flag.

## Backlog / storage / localization / grant isolation

#155, #165 and #214 remain separate. SQLite stays ordinary active local-first; PostgreSQL/pgvector remains inactive `active=false`; no dependency was added. Russian Reader-dependent RC-7 documentation remains current; eight other Reader-dependent locale packs remain `REFRESH_NEEDED` (64 documents). Broad localization is separate.

NLnet remains **submitted / under review / not awarded**. Approximate €50,000 is planning only and budget change is none.

## Explicit non-features after RC-9

No Reader embeddings/semantic similarity/ANN/vector DB, automatic entity resolution/claim identity/corroboration/contradiction winner, durable Reader index, public Reader retrieval API/CLI/worker, evidence/Canon/ESM write path, PostgreSQL activation or dedicated/full autonomous Reader is implemented by RC-9.
