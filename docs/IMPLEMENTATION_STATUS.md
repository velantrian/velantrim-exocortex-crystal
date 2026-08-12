# Implementation Status: Crystal vs Future Exo-Cortex Work

**Status date:** 2026-08-12  
**Retained runtime checkpoint:** `bbd816c` / PR #337  
**Signed Reader baseline at RC-8 audit start:** `main@b5541ce504af9002c8d3e2dcfa44ef4c0ead86c1` / PR #372  
**RC-7 exact-head CI:** `31572324596` — 9/9 successful  
**RC-7 post-merge CI:** `31572918731` — 9/9 successful  
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
| Exact-vs-ANN retrieval evaluation | Not implemented | separate future work |
| Reader Core RC-0 architecture | Documented | normative authority/validation contract |
| Reader Core RC-1 skeleton | Implemented/merged | `core/reader_core.py` |
| Reader Core RC-2 structural map | Implemented/merged | `core/reader_structure.py` |
| Reader Core RC-3 multi-pass mechanics | Implemented/merged | `core/reader_passes.py` |
| Reader Core RC-4 proposition extraction | Implemented/merged | `core/reader_extraction.py` |
| Reader Core RC-5 relation candidates | Implemented/merged | `core/reader_relations.py` |
| Reader Core RC-6 long-context strategy | Implemented/tested/merged | `core/reader_long_context.py` |
| Reader Core RC-7 cross-document candidate links | Implemented/tested/merged | `core/reader_cross_document.py`; PR #372 |
| Reader RC-8 retrieval architecture decision | Architecture/research only | no Reader discovery/vector runtime; issue #373 |
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

RC-8 does not insert a new runtime node into that chain. It defines how a future **candidate-discovery** layer must remain outside identity/evidence authority and how retrieval options must be evaluated before implementation.

### RC-4

RC-4 is deterministic validation/registration, not autonomous NLP extraction. It requires completed substantive RC-3 context and current matching provenance.

```text
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
```

### RC-5

`core/reader_relations.py` registers `POSSIBLE_CONTRADICTION`, `TENSION`, `EXCEPTION`, `QUALIFICATION` over valid registered RC-4 candidates inside one OPEN ReaderSession and exact SourceVersion.

```text
reader_core_rc5_relation_candidates = true
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
```

RC-5 has no truth/confidence/evidence-sufficiency/resolved/winner authority and does not call `core.evidence.attach_evidence()`.

### RC-6

`core/reader_long_context.py` plans deterministic bounded working sets from current registered RC-4 candidates inside one OPEN ReaderSession / exact SourceVersion. Caller-supplied `SUMMARY` retains direct RC-4 leaf provenance.

```text
working-set coverage != comprehension proof
summary != source text
summary != evidence
summary != verified fact
summary != Canon admission
```

### RC-7

`core/reader_cross_document.py` is merged under PR #372. It accepts only current registered RC-4 candidate IDs from explicit extractor/session/source bindings and requires different document identities on the two sides.

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

Each side preserves exact session/candidate/pass/node IDs, SourceVersion, primary locator and supporting locators. Before registration RC-7 revalidates OPEN session state, `EXTRACTED_PROPOSITION` fidelity, source/privacy binding, SegmentCard membership, completed pass, declared targets/substantive outcomes, recovered structure and current matching coverage.

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

## RC-8 post-RC-7 architecture/research decision

Durable decision: [READER_RC8_RETRIEVAL_DECISION.md](./architecture/READER_RC8_RETRIEVAL_DECISION.md).  
Adversarial corpus: `../eval/reader_rc8_retrieval_adversarial.jsonl`.

The audit distinguishes two retrieval domains:

```text
PRE-ADMISSION Reader artifacts
  → future candidate discovery may propose pairs for inspection
  → no evidence / identity / Canon authority

admitted L3 facts
  → existing embedding/legacy/query retrieval machinery
  → strict read-only grounding path
```

Existing `core/embedding.py`, `core/legacy_retrieval.py`, `core/retrieval_config.py`, `core/query_pipeline.py` and `core/rrf.py` therefore do not become Reader identity machinery by reuse alone.

RC-8 defines review classes:

- `SAME_PROPOSITION_CANDIDATE`;
- `PARAPHRASE_CANDIDATE`;
- `RELATED_CLAIM`;
- `SAME_TOPIC`;
- `POSSIBLE_CONTRADICTION`;
- `MERELY_SIMILAR`.

And preserves:

```text
retrieval match          != evidence
similarity               != identity
repetition               != corroboration
cross-document candidate != Canon relation
ranking                  != epistemic authority
candidate discovery      != candidate adjudication
```

Decision: deterministic lexical/token discovery is the required first future benchmark baseline. SQLite FTS is a candidate local-first backend with capability detection/fallback. Hybrid and neural semantic retrieval are deferred until a separately authorized, pre-registered benchmark comparison demonstrates material value. ANN/vector DB and PostgreSQL/pgvector are not justified as Reader defaults in RC-8.

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

RC-8 is a decision artifact, not an additional runtime capability flag.

## Backlog isolation

- #165: exact normalized ingest dedupe/migration only; no semantic matching.
- #155: downstream Epistemic Router/Evidence State RFC.
- #214: PII fixture and reproducible supply-chain hygiene.

None is merged into RC-8.

## Explicit non-features after RC-8

RC-1 through RC-8 still add no Reader durable corpus/index schema, public Reader API/CLI/background worker, automatic parser/chunker/OCR/PDF-layout/multimodal engine, automatic NLP/LLM/provider extraction, Reader embeddings/ANN/vector database, automatic semantic identity/entity resolution/deduplication, automatic corroboration, contradiction winner selection, planner/belief-update authority or evidence/Canon/ESM write path.

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

Russian root + Reader-dependent D1/D3/D4/D5 surfaces are `CURRENT` at immutable RC-7 English source checkpoint `ab3ad31c437647535030e371d58f456faf14017b`. Eight other Reader-dependent locale packs remain rich `REFRESH_NEEDED` translations; 64 documents remain tracked debt. D2 and Quick Start remain current across all nine locales.

RC-8 adds English architecture/research source only; broad localization remains separate.

## Grant truth

NLnet remains **submitted / under review / not awarded**. Approximate €50,000 is planning only; budget change is none. RC-0 through RC-7 are existing pre-agreement baseline when merged before an agreement. RC-8 is architecture/research only and is not an implemented semantic retrieval capability.