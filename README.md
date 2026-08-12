# 🔱 Velantrim ExoCortex — Crystal

> 🌐 🇬🇧 **English** · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 [Español](./README.es.md) · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 [Русский](./README.ru.md) · 🇨🇳 [简体中文](./README.zh-CN.md) · 🇸🇦 [العربية](./README.ar.md) · 🇯🇵 [日本語](./README.ja.md) · 🇮🇳 [हिन्दी](./README.hi.md)

### Verifiable, local-first memory, evidence and decision infrastructure for trustworthy AI systems

`v0.3.0` · 🎯 **100% line-coverage gate** · 🧬 **Ring Zero mutation gate** · ✅ **9 permanent CI jobs** · 🐍 **pure-standard-library default runtime** · ⚖️ **AGPL-3.0**

> Crystal is not a chatbot and not an autonomous truth oracle. It keeps source identity,
> evidence, epistemic state, review decisions and Reader artifacts separate so generated or
> extracted material cannot silently acquire authority it has not earned.

## 📌 Current authoritative Reader line

**Signed merged Reader baseline:** `main@1f5129d3276af28608b16e369fd38d21fe38c0d5` — RC-6 merged by PR #370; exact post-merge CI `31566408978` was 9/9 successful.  
**RC-7 tracking:** issue #371 / draft PR #372. Runtime/test head `b75811e09323adbe2c74184ae0470dfb703fcf4c` passed smoke exact-head CI `31568205231` 9/9; final RC-7 implementation truth still requires the final exact-head CI, guarded merge, verified merge signature and exact post-merge push CI.  
**Dedicated/full autonomous Reader: not implemented.**

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

The last line matters: bounded Reader primitives are real, but Crystal does not claim an autonomous semantic reader.

## 🧱 Non-equalities that define authority

```text
physical L3             != strict Canon
retrieval score         != evidence
Reader structure        != epistemic authority
pass completion         != comprehension proof
working-set coverage != comprehension proof
EXTRACTED_PROPOSITION   != verified fact
Reader candidate        != admitted evidence
relation candidate      != admitted evidence
contradiction candidate != confirmed contradiction
summary                 != source text
summary                 != evidence
summary                 != verified fact
summary                 != Canon admission
cross-document link     != Canon relation
cross-document support  != admitted evidence
same-topic              != same proposition
possible-same-claim     != claim identity
similarity signal       != identity proof
repetition across sources != corroboration
```

## 📖 Reader Core — bounded implementation

RC-0 remains the normative architecture contract: [READER_CORE_ARCHITECTURE.md](./docs/architecture/READER_CORE_ARCHITECTURE.md).

### RC-1 → RC-4

- **RC-1** — exact `SourceVersion`, replayable `SourceLocator`, Reader sessions, fidelity, coverage, bookmarks/open loops and privacy/stale semantics.
- **RC-2** — caller-supplied, source-version-bound Structural Document Map; structural order is metadata, not truth.
- **RC-3** — explicit deterministic `ORIENTATION`, `BROAD_READ`, `FOCUSED_READ`, `CROSS_CHECK`, `TARGETED_REREAD` mechanics with auditable outcomes.
- **RC-4** — source-linked caller-supplied `EXTRACTED_PROPOSITION` candidates anchored to completed substantive RC-3 context; source presentation is preserved without verification authority.

### RC-5 — exception / qualification / tension / contradiction candidates

Runtime module: `core/reader_relations.py`.

RC-5 registers explicit same-session / same-exact-source-version PRE-ADMISSION relation candidates over valid RC-4 candidates:

- `POSSIBLE_CONTRADICTION`;
- `TENSION`;
- `EXCEPTION`;
- `QUALIFICATION`.

It preserves exact candidate IDs, pass/node IDs, replayable two-sided provenance and rationale. Symmetric relations canonicalize order; directional relations retain direction. It does not admit evidence or resolve a contradiction.

```text
relation candidate      != admitted evidence
contradiction candidate != confirmed contradiction
```

### RC-6 — bounded long-context strategy

Runtime module: `core/reader_long_context.py`.

RC-6 is merged and tested. It revalidates current RC-4 leaves within one OPEN ReaderSession / exact SourceVersion, orders by RC-2 structure with candidate-ID tie-break, and packs deterministic working sets under explicit candidate and source-locator budgets. Candidate provenance is atomic; an oversized candidate fails closed.

Caller-supplied `SourceFidelity.SUMMARY` artifacts preserve direct RC-4 leaf provenance. RC-5 relations are context only when both endpoints are already in the same working set. RC-6 adds no automatic summarization, model-token/context-window claim or epistemic authority.

### RC-7 — bounded cross-document candidate links

Runtime module: `core/reader_cross_document.py`. Detailed contract: [RC-7 cross-document note](./docs/architecture/READER_RC7_CROSS_DOCUMENT.md).

RC-7 accepts explicit caller-supplied link candidates only between current registered RC-4 candidates from **different document identities**. It revalidates both Reader sessions, exact source versions, candidate registration, completed RC-3 pass state, recovered RC-2 structure and current substantive coverage before registering the link.

Candidate vocabulary follows RC-0:

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

`CONTRADICTS`, `SAME_TOPIC` and `POSSIBLE_SAME_CLAIM` are symmetric candidates and canonicalize side order deterministically. Other kinds remain directional. Each link stores exact two-sided session/candidate/pass/node/source-version/locator provenance plus an explicit rationale. Optional inspection basis is descriptive metadata only; there is no numeric similarity score or identity field.

RC-7 performs **no automatic semantic matching, entity resolution, claim deduplication, corroboration, contradiction resolution or evidence admission**.

## 🏛️ Authority flow

```text
SourceVersion + SourceLocator
        │
        ▼
RC-1 ReaderSession
        │
        ▼
RC-2 Structural Map
        │
        ▼
RC-3 explicit passes
        │
        ▼
RC-4 proposition candidates
   ┌────┼──────────────┐
   ▼    ▼              ▼
 RC-5  RC-6           RC-7
within- long-context  cross-document
source  working sets  link candidates
   │       │              │
   └───────┴──────┬───────┘
                  ▼
      normal explicit evidence/review path
                  ▼
        Guardian → TruthGate → strict read projection
```

Reader layers stay upstream of admission. None can call itself verified fact/evidence/Canon.

## 🗄️ Storage boundary

```text
SQLite
└── ordinary active local-first runtime

PostgreSQL 16 + pgvector
└── optional inactive migration/equivalence target
    └── active=false
```

Successful PostgreSQL import/equivalence is operation evidence, **not activation**. Automatic backend switching remains absent.

## 🔎 Public query boundary

HTTP `/ask` and `/receipt`, CLI `ask` / `receipt`, and MCP search remain read-only query surfaces. They do not create facts, alter ESM state, write L3 or bypass Guardian/TruthGate.

## 🌍 Localization truth

English is the primary source language. Russian Reader-dependent root + D1/D3/D4/D5 surfaces are currently `CURRENT` against the immutable RC-6 English checkpoint `ed96a88369f841bdb2ffd79ca020acef174685fc`. This RC-7 English source change must be committed first; a later Russian parity commit pins the exact RC-7 English source SHA. Eight other Reader-dependent locale packs preserve rich translations as `REFRESH_NEEDED` — 64 tracked documents. D2 and Quick Start remain current across all nine supported locales.

See [Localization policy](./docs/LOCALIZATION_POLICY.md) and [Translation status](./docs/TRANSLATION_STATUS.md).

## 🎓 Grant boundary

NLnet remains **submitted / under review / not awarded**. Approximate **€50,000** is planning only, not an approved budget/payment commitment; **budget change: none**. RC-0 through RC-6 are existing pre-agreement baseline. If RC-7 merges before an agreement, RC-7 also becomes existing baseline and cannot be counted again as future funded delta.

## 🚫 Still not claimed

Crystal does not claim:

- universal objective-truth detection or zero hallucinations;
- legal/GDPR/security certification;
- artificial consciousness or AGI;
- active PostgreSQL runtime selection, automatic cutover/rollback or automatic backend switching;
- automatic Reader parser/OCR/multimodal understanding;
- automatic NLP/LLM/provider proposition, relation, summary or cross-document link generation;
- embeddings/ANN/vector-database Reader retrieval or accepted semantic/vector thresholds;
- semantic equivalence / claim identity from RC-7 candidate links;
- automatic evidence admission, contradiction winner selection or planner/belief-update authority;
- a completed dedicated/full autonomous Reader Core.

## 📚 Evidence and navigation

- [Current status](./docs/STATUS.md)
- [Implementation matrix](./docs/IMPLEMENTATION_STATUS.md)
- [Machine-readable implementation manifest](./docs/status/implementation-manifest.json)
- [Reader Core architecture contract](./docs/architecture/READER_CORE_ARCHITECTURE.md)
- [RC-7 cross-document contract note](./docs/architecture/READER_RC7_CROSS_DOCUMENT.md)
- [Architecture overview](./docs/ARCHITECTURE_OVERVIEW.md)
- [Storage and authority boundaries](./docs/STORAGE_AND_AUTHORITY_BOUNDARIES.md)
- [Current AI context](./docs/ai/CURRENT_STATE.md)
- [Known risks](./docs/ai/KNOWN_RISKS.md)
- [NLnet scope](./docs/GRANT_NLNET_SCOPE.md)
- [Roadmap](./ROADMAP.md)
- [Translation status](./docs/TRANSLATION_STATUS.md)

## ✅ Retained historical runtime evidence

The older PostgreSQL integration checkpoint remains historical evidence rather than the Reader milestone head:

```text
Verified retained runtime checkpoint: bbd816c09dd39a02e6de6c1014438490572f40f6 (PR #337)
Retained Python 3.11: 2078 passed / 13 skipped / 0 failed
Retained Python 3.12: 2078 passed / 13 skipped / 0 failed
Retained statements: 9756
Retained coverage: 100.00%
PostgreSQL integration CI: 31256316532
Reader RC-6 signed merge: 1f5129d3276af28608b16e369fd38d21fe38c0d5
Reader RC-6 post-merge CI: 31566408978 (9/9)
RC-7 runtime smoke head: b75811e09323adbe2c74184ae0470dfb703fcf4c
RC-7 runtime smoke CI: 31568205231 (9/9)
```

Final RC-7 implementation authority will be the signed merged `main` plus exact final-head and post-merge CI evidence, not this pre-merge README statement.
