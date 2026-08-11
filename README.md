# 🔱 Velantrim ExoCortex — Crystal

> 🌐 🇬🇧 **English** · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 [Español](./README.es.md) · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 [Русский](./README.ru.md) · 🇨🇳 [简体中文](./README.zh-CN.md) · 🇸🇦 [العربية](./README.ar.md) · 🇯🇵 [日本語](./README.ja.md) · 🇮🇳 [हिन्दी](./README.hi.md)

### Verifiable, local-first memory, evidence and decision infrastructure for trustworthy AI systems

`v0.3.0` · 🧪 retained checkpoint **2078 passed / 13 skipped / 0 failed** · 🎯 **9756 statements / 100.00% line coverage** · 🧬 **7/7 Ring Zero mutants killed** · ✅ **9 permanent CI jobs** · 🐘 optional PostgreSQL/pgvector migration support · 🐍 pure-standard-library default runtime · ⚖️ AGPL-3.0

> Crystal is not a chatbot and not an autonomous “truth oracle.” It is infrastructure for keeping source identity, evidence, epistemic state, review, storage and trusted read authority distinct.

**Retained verified runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6` — merged PR #337.  
**Reader foundation:** RC-1 evidence-linked skeleton, RC-2 caller-supplied Structural Document Map, RC-3 explicit deterministic multi-pass mechanics, RC-4 source-linked proposition extraction, and RC-5 explicit pre-admission relation candidates are bounded implemented layers.  
**Dedicated/full autonomous Reader: not implemented.**  
**Exact status:** [docs/STATUS.md](./docs/STATUS.md) · [implementation manifest](./docs/status/implementation-manifest.json) · [Reader architecture contract](./docs/architecture/READER_CORE_ARCHITECTURE.md)

> **Documentation language policy:** English is the primary/source technical language. Russian is the fully refreshed Reader secondary surface for the RC-5 source checkpoint recorded in [TRANSLATION_STATUS.md](./docs/TRANSLATION_STATUS.md). Eight other Reader-dependent locale surfaces preserve rich translations as explicit `REFRESH_NEEDED` debt; D2 and Quick Start remain current across all nine locales.

---

## 🎯 Why Crystal exists

AI systems often mix source text, user statements, retrieved fragments, hypotheses, model output and durable memory. When those categories blur, fluent language can silently gain authority that the evidence does not justify.

Crystal makes the boundaries explicit:

```text
source statement        != verified fact
segment                 != claim
summary                 != evidence
importance              != truth
retrieval score         != authority
model output             != source truth
Reader observation      != Canon admission
Reader coverage         != comprehension proof
Reader pass completion  != comprehension proof
EXTRACTED_PROPOSITION   != verified fact
Reader candidate        != admitted evidence
relation candidate      != admitted evidence
contradiction candidate != confirmed contradiction
cross-document similarity != identity
repetition              != corroboration
```

## 🧠 What Crystal provides

- typed claims and explicit epistemic lifecycle;
- source identity, evidence spans and provenance;
- Guardian and TruthGate admission boundaries;
- multi-status physical L3 separated from strict Canon;
- deny-dominant `TrustSnapshot` and `CanonicalView` reads;
- read-only `HTTP /ask`, `CLI ask` and `MCP search` query surfaces;
- TRACE and replayable receipts;
- review queues and explicit contradiction dispositions;
- SQLite local-first storage lifecycle and logical portability;
- optional PostgreSQL/pgvector inactive import/equivalence path with `active=false`;
- deterministic evaluation, full line-coverage gate, security and Docker checks;
- a bounded five-stage Reader foundation through RC-5.

## 📖 Reader foundation

```text
RC-0 architecture contract
        ↓
RC-1 exact source/version/session/provenance skeleton
        ↓
RC-2 caller-supplied structural document map
        ↓
RC-3 explicit deterministic multi-pass mechanics
        ↓
RC-4 source-linked proposition extraction
        ↓
RC-5 explicit same-session/same-version relation candidates
        ↓
normal evidence/admission path remains separate
```

### RC-1 — evidence-linked skeleton

`core/reader_core.py` provides `SourceVersion`, `SourceLocator`, `SegmentCard`, coverage state/telemetry, bookmarks/open loops and `ReaderSession`. Source body is not retained. Source hash/version changes invalidate old Reader context rather than silently reusing it.

### RC-2 — caller-supplied Structural Document Map

`core/reader_structure.py` models document/section/subsection/paragraph/dialogue/list/table/code/quotation/note/reference/figure/caption structure with explicit `RECOVERED`, `AMBIGUOUS`, `UNSUPPORTED` state and deterministic hierarchy/order validation.

Structure/order/prominence is metadata, not truth or confidence authority. RC-2 is not an automatic parser, OCR engine or layout reconstruction system.

### RC-3 — explicit deterministic multi-pass mechanics

`core/reader_passes.py` records `ORIENTATION`, `BROAD_READ`, `FOCUSED_READ`, `CROSS_CHECK`, `TARGETED_REREAD` attempts with explicit target regions and explicit coverage outcomes. Partial progress is preserved for interrupted/degraded passes. `Reader pass completion is not comprehension proof`.

### RC-4 — source-linked proposition extraction

`core/reader_extraction.py` registers caller-supplied normalized proposition candidates only from completed substantive RC-3 regions with matching `PROCESSED` / `REVISITED` state. Candidates use `EXTRACTED_PROPOSITION` fidelity and keep attribution, source-presentation category, negation, qualifiers and replayable locators.

**EXTRACTED_PROPOSITION is not a verified fact.**  
**Reader candidate is not admitted evidence.**

RC-4 does not call `core.evidence.attach_evidence()` and does not write fact evidence.

### RC-5 — exception / qualification / tension / contradiction candidates

`core/reader_relations.py` is the smallest PRE-ADMISSION relation layer over valid RC-4 candidates.

| Relation kind | Meaning inside Reader | Authority |
|---|---|---|
| `POSSIBLE_CONTRADICTION` | explicit suspicion that two propositions may conflict | candidate only |
| `TENSION` | explicit tension without asserting contradiction | candidate only |
| `EXCEPTION` | right-hand proposition is registered as an exception to the left | directional candidate |
| `QUALIFICATION` | right-hand proposition narrows/refines the left | directional candidate |

RC-5 requires one OPEN `ReaderSession`, one exact `SourceVersion`, candidate IDs already registered by one RC-4 extractor, both sides' exact provenance and an explicit rationale. Symmetric relations use deterministic candidate-ID order; duplicate symmetric re-registration fails rather than becoming “corroboration.”

RC-5 is **not** automatic contradiction detection from raw text. It does not infer semantic equivalence or identity, does not use similarity as proof, and does not create the broader cross-document Reader stage.

```text
POSSIBLE_CONTRADICTION
        !=
confirmed contradiction
        !=
resolved contradiction / winner
```

## 🛡️ Reader authority firewall

Reader RC-1 through RC-5 do **not**:

- mutate `truth_status` or ESM;
- write strict Canon;
- bypass Guardian or TruthGate;
- attach fact evidence or declare evidence sufficiency;
- promote confidence from Reader output;
- select a contradiction winner;
- treat repetition as corroboration;
- infer cross-document identity from similarity;
- create planner/research/belief-update authority.

RC-5 has no truth/confidence/evidence-sufficiency/winner fields and does not invoke the existing contradiction-resolution workflow.

## 🏛️ Architecture in three views

### Mind map

```text
🔱 Crystal
├── 📖 Reader foundation
│   ├── RC-1 exact source/provenance
│   ├── RC-2 structure
│   ├── RC-3 reading-process ledger
│   ├── RC-4 proposition candidates
│   ├── RC-5 relation candidates
│   └── full autonomous Reader — absent
├── 🛡️ Trust boundary
│   ├── Guardian
│   ├── TruthGate
│   ├── TrustSnapshot
│   └── CanonicalView
├── 📜 Evidence / audit
│   ├── source + spans
│   ├── provenance
│   ├── TRACE
│   └── Receipt
├── ⚖️ Review / contradiction
│   ├── review queue
│   ├── ContradictionReport
│   └── explicit COEXIST / CONTEXTUALIZE / SUPERSEDE
├── 🗄️ Storage
│   ├── SQLite ordinary active local-first
│   └── PostgreSQL/pgvector inactive target
└── 📊 Verification
    ├── Python 3.11 / 3.12
    ├── 100% line-coverage gate
    ├── Ring Zero
    ├── security / Docker / eval
    └── exact-head CI
```

### Information flow

```text
Reader source/version
  ↓
RC-1 artifacts
  ↓
RC-2 declared structure
  ↓
RC-3 explicit passes
  ↓
RC-4 proposition candidates
  ↓
RC-5 relation candidates
  │
  └── PRE-ADMISSION ONLY

Explicit ingest/evidence
  ↓
Guardian
  ↓
TruthGate
  ↓
L1 + physical L3
  ↓
TrustSnapshot / CanonicalView
  ↓
read-only query / answer / bounded refusal
```

### Module tree

```text
core/reader_core.py       — RC-1 source/session/fidelity/coverage
core/reader_structure.py  — RC-2 structural map
core/reader_passes.py     — RC-3 pass ledger
core/reader_extraction.py — RC-4 proposition candidates
core/reader_relations.py  — RC-5 relation candidates

Reader modules
  != core.evidence admission
  != contradiction resolution
  != Guardian/TruthGate policy owner
```

## ⚖️ Contradiction candidates vs contradiction decisions

RC-5 can record a suspicion between Reader propositions. The existing contradiction workflow remains a different authority surface.

```text
Reader RC-5 relation candidate
        ↓
(no automatic promotion)
        ↓
normal source/evidence/admission path if a later workflow promotes material
        ↓
implemented contradiction report/review machinery
        ↓
explicit authorized disposition
```

A relation candidate never marks one side false and never selects `COEXIST`, `CONTEXTUALIZE` or `SUPERSEDE` by itself.

## 🗄️ SQLite and PostgreSQL/pgvector

```text
SQLite
└── ordinary active local-first runtime
    ├── runtime reads/writes
    ├── backup / verify / inactive restore
    └── bounded logical export

PostgreSQL 16 + pgvector
└── optional migration/equivalence target
    ├── optional dependency
    ├── lazy driver
    ├── fresh inactive schema
    ├── active=false
    └── independent exact-state verification
```

Import support does not mean runtime activation. RC-5 changes no Reader DB schema and activates no PostgreSQL path.

## 🔎 Crystal versus classic RAG

| Question | Classic RAG | Crystal |
|---|---|---|
| Retrieve relevant material | primary strength | supported through adapters |
| Distinguish source presentation from verified truth | application-specific | explicit boundary |
| Track version-bound reading artifacts | application-specific | RC-1–RC-5 bounded chain |
| Preserve attribution/negation/qualifiers | application-specific | RC-4 |
| Preserve exception/tension/contradiction suspicion without resolving it | application-specific | RC-5 |
| Prevent generated text becoming its own source | not inherent | admission invariants |
| Replay evidence | optional | TRACE / Receipt |
| Resolve contradictions accountably | application-specific | explicit authorized dispositions |

## 🚫 What RC-5 still does not implement

- full autonomous Semantic Reader;
- automatic NLP/LLM proposition or contradiction extraction;
- provider/model routing inside Reader;
- automatic parser/chunker, OCR or PDF layout reconstruction;
- multimodal image understanding;
- embeddings, ANN or Reader vector database;
- automatic semantic cross-document identity;
- automatic contradiction resolution;
- autonomous research planner or belief update;
- public Reader API/CLI/background worker;
- durable Reader database schema;
- PostgreSQL runtime activation/switching.

## 💶 Grant boundary

NLnet state remains **submitted / under review / not awarded**. Approximate **€50,000** is planning only; there is no approved budget/payment commitment and budget change is none.

Anything merged before a grant agreement is existing baseline. Therefore RC-0 through RC-5, when merged pre-agreement, cannot later be counted again as future funded delta. Any future funded Reader work must start after the actually merged RC-5 baseline.

## 🌍 Localization truth

English is the authoritative source language. Russian Reader-dependent root/detail documentation is refreshed against the immutable RC-5 English checkpoint recorded in [docs/TRANSLATION_STATUS.md](./docs/TRANSLATION_STATUS.md). The other eight localized Reader-dependent surfaces remain `REFRESH_NEEDED`; their rich previous translations are preserved. D2 reviewer/safety and Quick Start remain current for all nine locales.

## 📚 Further reading

- [Current status](./docs/STATUS.md)
- [Implementation status](./docs/IMPLEMENTATION_STATUS.md)
- [Architecture overview](./docs/ARCHITECTURE_OVERVIEW.md)
- [Reader Core architecture contract](./docs/architecture/READER_CORE_ARCHITECTURE.md)
- [Storage and authority boundaries](./docs/STORAGE_AND_AUTHORITY_BOUNDARIES.md)
- [Roadmap](./ROADMAP.md)
- [Grant scope](./docs/GRANT_NLNET_SCOPE.md)
- [Project/grant/governance overview](./docs/PROJECT_GRANT_AND_GOVERNANCE.md)
- [Glossary](./docs/GLOSSARY.md)
- [Documentation map](./docs/DOCUMENTATION_MAP.md)
- [Localization policy](./docs/LOCALIZATION_POLICY.md)
- [Translation status](./docs/TRANSLATION_STATUS.md)
