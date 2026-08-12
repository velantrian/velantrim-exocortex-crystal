# 🔱 Velantrim ExoCortex — Crystal

> 🌐 🇬🇧 **English** · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 [Español](./README.es.md) · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 [Русский](./README.ru.md) · 🇨🇳 [简体中文](./README.zh-CN.md) · 🇸🇦 [العربية](./README.ar.md) · 🇯🇵 [日本語](./README.ja.md) · 🇮🇳 [हिन्दी](./README.hi.md)

### Verifiable, local-first memory, evidence and decision infrastructure for trustworthy AI systems

`v0.3.0` · 🎯 **100% line-coverage gate** · 🧬 **Ring Zero mutation gate** · ✅ **9 permanent CI jobs** · 🐘 **real PostgreSQL/pgvector integration** · 🐍 **pure-standard-library default runtime** · ⚖️ **AGPL-3.0**

> Crystal is not another chatbot and it is not an autonomous “truth oracle.” It is a
> memory, evidence and decision boundary that records what a claim is, where it came
> from, what epistemic state it is in, whether it may ground an answer, and how a
> contradiction was resolved through an explicit audited decision.

**Verified retained runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6` — merged PR #337.  
**Validated retained runtime head / CI:** `d7af7c80722274f9217bc5545d150f92e9363f37` / `31256316536` — 9/9 successful.  
**PostgreSQL integration:** `31256316532` — successful against PostgreSQL 16 and pgvector 0.8.2.  
**Reader foundation:** RC-1 evidence-linked skeleton, RC-2 caller-supplied Structural Document Map, RC-3 explicit deterministic multi-pass mechanics, RC-4 source-linked proposition extraction and RC-5 explicit same-session/same-version relation candidates are merged bounded layers. RC-6 bounded long-context strategy is the current separately authorized milestone under issue #369 / PR #370; the dedicated/full autonomous Semantic Reading runtime remains **not implemented**.  
**Exact public evidence:** [TEST_REPORT.md](./TEST_REPORT.md), [STATUS.md](./docs/STATUS.md) and the [machine-readable implementation manifest](./docs/status/implementation-manifest.json).

> **Documentation language policy:** English is the primary working and source language,
> not the only intended documentation language. Russian Reader-dependent root/detail surfaces
> are current against the immutable RC-5 English source checkpoint recorded in
> [TRANSLATION_STATUS.md](./docs/TRANSLATION_STATUS.md). The RC-6 English source is committed first;
> Russian RC-6 parity is pinned to that exact SHA in a separate follow-up commit. Eight other
> Reader-dependent locale surfaces preserve their rich translations as `REFRESH_NEEDED`; D2 and
> Quick Start remain current across all nine supported locales.

---

## 🎯 Why Crystal exists

Many AI systems mix source documents, user statements, model output, hypotheses,
retrieved fragments and durable memory in one context or vector store. When those
categories are not separated, fluent text can silently acquire authority that its
evidence does not support.

Crystal makes the boundaries explicit:

```text
A fluent claim is not automatically trusted.
A physical graph node is not automatically strict Canon.
A retrieval score is not evidence.
A model output is not an independent factual source.
A contradiction does not select its own winner.
A topic label is not a truth verdict.
A successful data import is not backend activation.
Reader structure or coverage is not epistemic authority.
Reader pass completion is not comprehension proof.
Working-set coverage is not comprehension proof.
EXTRACTED_PROPOSITION is not a verified fact.
Reader candidate is not admitted evidence.
relation candidate      != admitted evidence
contradiction candidate != confirmed contradiction
summary                  != source text
summary                  != evidence
summary                  != verified fact
summary                  != Canon admission
Cross-document similarity is not identity.
Repetition is not corroboration.
```

## 🧠 What Crystal provides

- typed claims and an explicit epistemic lifecycle;
- source identity, evidence spans and provenance;
- bounded Reader RC-1 source/session artifacts with fidelity and coverage semantics;
- bounded Reader RC-2 caller-supplied structural document maps with explicit ambiguity;
- bounded Reader RC-3 explicit multi-pass process mechanics with auditable coverage effects;
- bounded Reader RC-4 source-linked `EXTRACTED_PROPOSITION` candidates with explicit attribution/category/negation/qualifiers;
- bounded Reader RC-5 explicit `POSSIBLE_CONTRADICTION`, `TENSION`, `EXCEPTION` and `QUALIFICATION` relation candidates with exact two-sided provenance and rationale;
- bounded Reader RC-6 deterministic rolling working sets over valid RC-4 leaves, with caller-supplied provenance-preserving `SUMMARY` candidates;
- Guardian and TruthGate admission boundaries;
- a multi-status physical L3 graph separated from strict Canon;
- immutable deny-dominant `TrustSnapshot` read reconciliation;
- read-only public HTTP, CLI and MCP query surfaces;
- TRACE and replayable tamper-evident Receipts;
- restriction, erasure, audit and import-session controls;
- review queues and resumable review sessions;
- typed immutable contradiction reports;
- explicit `COEXIST`, `CONTEXTUALIZE` and `SUPERSEDE` decisions;
- scoped curator roles/capabilities and process-local decision leases;
- advisory multi-label TopicFacet metadata with no truth authority;
- deterministic evaluation, 100% line-coverage enforcement and a Ring Zero mutation gate;
- verified SQLite backup/restore and bounded logical migration;
- optional PostgreSQL/pgvector inactive import with independent exact-state equivalence.

### RC-5 — exception / qualification / tension / contradiction candidates

Reader RC-1/RC-2/RC-3/RC-4/RC-5 retain no source body, add no public Reader API/CLI or durable Reader
storage schema, and have no truth/Canon/ESM/planner authority. RC-3 provides explicit deterministic
pass mechanics; RC-4 validates caller-supplied proposition candidates against completed substantive
Reader context; RC-5 registers explicit relations only between already-registered RC-4 candidates
inside one OPEN ReaderSession and exact SourceVersion. These layers do **not** provide an automatic
parser, automatic NLP/LLM extraction, autonomous model-driven reader, embeddings, ANN/vector-database
Reader stack, semantic equivalence engine, automatic cross-document identity/reasoning or contradiction
resolution. RC-4/RC-5 do not call `core.evidence.attach_evidence()` or write fact evidence.

Runtime module: `core/reader_relations.py`.

```text
coverage != comprehension proof
pass completion != comprehension proof
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
similarity != identity
repetition != corroboration
```

### RC-6 — bounded long-context strategy

RC-6 is designed around the architecture contract's rule that long documents must not assume an
infinite model context window. `core/reader_long_context.py` operates only on the current registered
RC-4 proposition candidates of one existing extractor, therefore one OPEN ReaderSession and one exact
SourceVersion.

Before planning, RC-6 re-validates direct leaves against:

- RC-4 `EXTRACTED_PROPOSITION` fidelity and ReaderSession card membership;
- the original `COMPLETED` RC-3 pass;
- recovered RC-2 structural nodes;
- exact current source-version provenance;
- current `PROCESSED` / `REVISITED` coverage.

Deterministic order is:

```text
RC-2 structural order
→ candidate_id lexical tie-break
```

Rolling working sets are bounded by two explicit Reader-artifact budgets:

```text
1 <= max_candidates_per_set <= 128
1 <= max_source_locators_per_set <= 512
```

These limits are **not model-token or context-window claims**. Candidate atomicity means one RC-4
candidate and all of its direct unique replayable source locators stay together; if the candidate
alone cannot fit the caller-declared locator budget, planning fails closed rather than splitting
provenance.

A matching RC-5 `ReaderRelationRegistry` is optional context only. An existing relation ID is carried
into a working set only when both endpoints are already members of that set. A relation crossing a
working-set boundary is not copied into either set and RC-6 does not infer a replacement relation.

A caller may register explicit `SourceFidelity.SUMMARY` text for one current working set. Before the
summary is accepted, RC-6 compares current direct RC-4 leaf locators with the immutable working-set
snapshot and re-validates those leaves. The summary keeps direct leaf candidate IDs and replayable
source provenance. Another summary cannot become its only support path and RC-6 does not generate
summary text automatically.

```text
working-set coverage != comprehension proof
summary              != source text
summary              != evidence
summary              != verified fact
summary              != Canon admission
```

RC-6 imports only Reader layers and carries no truth/confidence/evidence-sufficiency/resolution/winner
authority fields. It adds no evidence admission, truth/ESM/Canon mutation, contradiction resolution,
Guardian/TruthGate bypass, planner authority, parser/OCR, LLM/provider/model routing, embeddings/ANN,
RC-7 cross-document reading, Reader persistence/API/CLI/worker or PostgreSQL activation.

## 🏛️ Architecture in three views

### 🧠 Mind map — purpose and authority boundaries

```text
🧠 Velantrim ExoCortex — Crystal
│
├── 🎯 Purpose
│   ├── Verifiable memory for AI systems
│   ├── Local-first trust infrastructure
│   └── Answers and decisions linked to evidence
│
├── 📖 Reader foundation
│   ├── RC-1 — evidence-linked source/session skeleton
│   ├── RC-2 — caller-supplied Structural Document Map
│   ├── RC-3 — explicit deterministic multi-pass mechanics
│   ├── RC-4 — source-linked proposition extraction
│   ├── RC-5 — explicit pre-admission relation candidates
│   ├── RC-6 — bounded long-context working sets + SUMMARY candidates
│   └── dedicated/full autonomous Reader — not implemented
│
├── 🏛️ Memory model
│   ├── L0 — fast working cache
│   ├── L1 — operational memory and lifecycle
│   ├── L2 — waiting/review boundary
│   └── L3 — physical multi-status graph
│
├── 🛡️ Trust boundary
│   ├── Guardian — structure and safety constraints
│   ├── TruthGate — admission policy
│   ├── TrustSnapshot — deny-dominant reconciliation
│   └── CanonicalView — strict trusted projection
│
├── 📜 Evidence and audit
│   ├── Source identity and evidence spans
│   ├── Provenance
│   ├── TRACE
│   └── Receipt
│
├── ⚖️ Review and contradiction
│   ├── Review queue
│   ├── Resumable review session
│   ├── ContradictionReport
│   └── COEXIST / CONTEXTUALIZE / SUPERSEDE
│
├── 🗄️ Storage profiles
│   ├── SQLite — ordinary local-first profile
│   └── PostgreSQL/pgvector — inactive migration target
│
└── 📊 Verification
    ├── Python 3.11 / 3.12
    ├── 100% line-coverage gate
    ├── Ring Zero mutation gate
    ├── Security and Docker gates
    └── exact-head CI evidence
```

### 🏗️ ASCII architecture — Reader and authority flow

```text
SourceVersion + replayable SourceLocator
              │
              ▼
      RC-1 ReaderSession
              │
              ▼
  RC-2 Structural Document Map
              │
              ▼
   RC-3 explicit reading passes
              │
              ▼
 RC-4 EXTRACTED_PROPOSITION leaves
              │
        ┌─────┴─────┐
        ▼           ▼
 RC-5 relations   RC-6 bounded working sets
        │           │
        └─────┬─────┘
              ▼
 optional caller-supplied SUMMARY
              │
              ▼
 normal ingest/review/evidence path
              │
              ▼
     Guardian → TruthGate
              │
              ▼
 physical L3 + strict read reconciliation
              │
              ▼
 grounded answer / bounded refusal
```

Reader layers remain upstream candidate/process state. They do not admit themselves.

### 🌳 Module tree — ownership and connections

```text
🌳 Crystal
│
├── 📖 Reader foundation
│   ├── core/reader_core.py — RC-1 source/session artifacts
│   ├── core/reader_structure.py — RC-2 Structural Document Map
│   ├── core/reader_passes.py — RC-3 explicit multi-pass mechanics
│   ├── core/reader_extraction.py — RC-4 source-linked proposition candidates
│   ├── core/reader_relations.py — RC-5 explicit relation candidates
│   └── core/reader_long_context.py — RC-6 bounded working sets + SUMMARY candidates
│
├── 🧠 Memory surfaces
│   ├── L0 — rebuildable working cache
│   ├── L1 — SQLite/WAL operational state
│   ├── L2 — logical review boundary
│   └── L3 — multi-status physical graph
│
├── 🛡️ Trust surfaces
│   ├── Guardian
│   ├── TruthGate
│   ├── TrustSnapshot
│   └── CanonicalView
│
├── 📜 Evidence surfaces
│   ├── Source metadata
│   ├── Evidence spans
│   ├── Provenance
│   ├── TRACE
│   └── Receipt
│
├── ⚖️ Review and contradiction
│   ├── Review queue/session
│   ├── ContradictionReport
│   └── Explicit audited disposition
│
├── 🔎 Public query
│   ├── HTTP /ask and /receipt
│   ├── CLI ask and receipt
│   └── MCP search
│
└── 🗄️ Storage portability
    ├── SQLite backup/restore
    ├── Canonical logical bundle
    ├── Bounded verification
    └── PostgreSQL inactive exact-equivalence import
```

## 🧭 Central distinctions

```text
physical L3 graph       != strict Canon
query                   != ingest
confidence              != independent evidence
LLM output              != independent factual source
contradiction detect    != automatic winner
TopicFacet relevance    != truth
migration receipt       != claim evidence
successful import       != backend activation
process-local lease     != distributed coordination
Reader coverage         != comprehension proof
Reader structure        != truth/confidence authority
Reader pass complete    != comprehension proof
working-set coverage    != comprehension proof
EXTRACTED_PROPOSITION   != verified fact
Reader candidate        != admitted evidence
relation candidate      != admitted evidence
contradiction candidate != confirmed contradiction
summary                 != source text/evidence/truth/Canon admission
similarity              != identity
repetition              != corroboration
```

TruthGate is an admission-policy gate, not an oracle that independently knows objective truth.
Strict Canon is a policy-allowed read projection over evidence, status, ESM state, confidence shape
and processing restrictions.

## 🧱 Memory and evidence surfaces

| Surface | Role | Critical boundary |
|---|---|---|
| Reader RC-1 | evidence-linked source/session artifacts | observations and coverage do not admit truth |
| Reader RC-2 | version-bound structural map | order/prominence is metadata, not authority |
| Reader RC-3 | explicit pass ledger over declared targets | pass completion is process state, not comprehension/truth |
| Reader RC-4 | source-linked extracted proposition candidates | source presentation/candidate state, not verified fact or admitted evidence |
| Reader RC-5 | typed relation candidates between valid RC-4 candidates | relation suspicion is not contradiction confirmation/resolution or evidence admission |
| Reader RC-6 | bounded working sets and caller-supplied summaries over direct RC-4 leaves | context/synthesis artifacts, not comprehension/evidence/truth |
| L0 | in-process working cache | fast and rebuildable |
| L1 | SQLite/WAL operational memory | lifecycle, restrictions and pending work |
| L2 | logical review boundary | not automatically strict Canon |
| L3 | physical multi-status memory | record presence does not imply trust |
| TrustSnapshot | immutable reconciliation | deny-dominant L1/L3 resolution |
| CanonicalView | strict grounding projection | policy-allowed reads only |
| TRACE / Receipt | proof and replay | grounding, drift and tamper evidence |
| ContradictionReport | immutable conflict object | confidence does not select a winner |
| TopicFacet | navigation metadata | cannot change truth, ESM or Canon |
| CuratorPrincipal / lease | authorization and coordination | external lease adapter required for scale |

## 🗄️ SQLite and PostgreSQL/pgvector

```text
SQLite
└── current ordinary local-first storage profile
    ├── runtime reads/writes
    ├── backup/restore
    ├── lock recovery
    └── bounded canonical logical export

PostgreSQL 16 + pgvector
└── optional migration/equivalence profile
    ├── optional [postgresql] dependency
    ├── lazy driver loading
    ├── new target schema
    ├── active=false
    ├── SERIALIZABLE import
    └── independent count / byte / SHA-256 equivalence
```

The PostgreSQL target is absent from ordinary runtime composition and cannot serve normal reads or
writes. Successful import is operational migration evidence; it does not establish activation,
automatic backend selection, cutover, rollback, dual-write, TruthGate admission, strict Canon
membership, ANN quality acceptance or production multi-tenancy.

The default installation remains pure standard library. Production credentials and
credential-bearing connection strings must not enter profiles, bundles, receipts, application logs,
GitHub issues or Notion.

## 🔎 Crystal versus classic RAG

| Question | Classic RAG | Crystal |
|---|---|---|
| Find relevant material | primary strength | supported through retrieval adapters |
| Separate user claim from verified fact | application-specific | explicit typed boundary |
| Track lifecycle and contradictions | usually external logic | first-class states and reports |
| Preserve version-bound reading/process artifacts | application-specific | RC-1 through RC-6 bounded Reader foundation |
| Preserve proposition attribution/qualifiers before admission | application-specific | RC-4 explicit source-presentation metadata |
| Preserve explicit relation suspicion without resolving it | application-specific | RC-5 typed relation candidates with exact provenance |
| Process long sources without infinite-context claims | application-specific | RC-6 bounded working sets + direct leaf provenance |
| Preserve summary provenance | application-specific | RC-6 SUMMARY retains direct RC-4 leaf links |
| Prevent generated text becoming its own source | not inherent | Ring Zero admission invariant |
| Replay answer evidence | optional | TRACE and Receipt architecture |
| Resolve contradictions accountably | application-specific | explicit authorized dispositions |
| Run without a mandatory cloud/model provider | varies | pure-stdlib local-first baseline |

## 🛡️ Public read-only query boundary

These surfaces share `core.query_pipeline`:

```text
HTTP /ask and /receipt
CLI ask and receipt
MCP search
```

They do not create facts, transition ESM state, write L3, operate the outbox, record episodes,
initialize an embedding fingerprint, store unknown candidates or mutate adaptive verification state.

See [Read-Only Query Boundary](./docs/architecture/read-only-query-boundary.md).

## ⚖️ Explicit contradiction decisions

Normal approval fails closed while a contradiction is unresolved. A curator must choose an explicit
disposition and provide an actor and reason.

RC-5 does not change that authority surface. `POSSIBLE_CONTRADICTION` is only a Reader candidate
relation; it never selects the true/false side and never chooses `COEXIST`, `CONTEXTUALIZE` or
`SUPERSEDE`. RC-6 may carry that relation ID as working-set context only; it cannot resolve it.

```bash
python -m core.conflict_surfaces FACT_ID \
  --disposition COEXIST \
  --actor alice \
  --reason "the claims describe different contexts" \
  --expected-report-id REPORT_ID
```

For hosted FastAPI deployments, register `POST /review/resolve-conflict` with the host application's
authentication dependency. The current `CuratorLeaseRegistry` prevents concurrent decisions only
inside one process; distributed deployments require an external lease adapter.

## 🚀 Quick start

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
```

Optional inactive PostgreSQL migration tooling:

```bash
pip install -e '.[postgresql]'
```

Continue with [QUICKSTART.md](./docs/QUICKSTART.md).

## 📚 Evidence and navigation

- [Documentation map](./docs/DOCUMENTATION_MAP.md)
- [Verification report](./TEST_REPORT.md)
- [Current status](./docs/STATUS.md)
- [Implementation matrix](./docs/IMPLEMENTATION_STATUS.md)
- [Machine-readable manifest](./docs/status/implementation-manifest.json)
- [Reader Core architecture contract](./docs/architecture/READER_CORE_ARCHITECTURE.md)
- [Architecture](./docs/ARCHITECTURE.md)
- [Architecture overview](./docs/ARCHITECTURE_OVERVIEW.md)
- [Storage and authority boundaries](./docs/STORAGE_AND_AUTHORITY_BOUNDARIES.md)
- [Inactive PostgreSQL import contract](./docs/architecture/POSTGRESQL_INACTIVE_IMPORT.md)
- [Current AI context](./docs/ai/CURRENT_STATE.md)
- [Known risks](./docs/ai/KNOWN_RISKS.md)
- [NLnet scope](./docs/GRANT_NLNET_SCOPE.md)
- [Baseline → funded-delta matrix](./docs/grants/baseline-funded-delta-matrix.md)
- [Localization policy](./docs/LOCALIZATION_POLICY.md)
- [Translation status](./docs/TRANSLATION_STATUS.md)
- [Roadmap](./ROADMAP.md)
- [Security policy](./SECURITY.md)

## ✅ Verified baseline and current Reader line

```text
Retained runtime merge: bbd816c09dd39a02e6de6c1014438490572f40f6 (PR #337)
Retained Python 3.11: 2078 passed / 13 skipped / 0 failed
Retained Python 3.12: 2078 passed / 13 skipped / 0 failed
Retained statements: 9756
Retained coverage:   100.00%
Mutation gate:       7/7 declared Ring Zero mutants killed
Permanent CI jobs:   9
PostgreSQL integration: successful against PostgreSQL 16 + pgvector 0.8.2
Reader RC-1: implemented/tested bounded evidence-linked skeleton
Reader RC-2: implemented/tested bounded Structural Document Map
Reader RC-3: implemented/tested bounded explicit multi-pass mechanics
Reader RC-4: implemented/tested bounded source-linked proposition extraction
Reader RC-5: implemented/tested bounded explicit relation candidates
Reader RC-6: bounded long-context strategy implemented/tested on PR #370 branch; final merge evidence pending
Dedicated/full autonomous Reader: not implemented
```

The numeric runtime block above is the retained PR #337 verification checkpoint; later Reader
milestones use their own exact-head and post-merge CI evidence. RC-6 is not final implementation
truth until its final exact-head CI, guarded merge signature and exact post-merge push CI all pass.

Current RC-6 branch machine truth:

```text
reader_core_rc1_skeleton               = true
reader_core_rc2_structural_map         = true
reader_core_rc3_multi_pass_mechanics   = true
reader_core_rc4_proposition_extraction = true
reader_core_rc5_relation_candidates    = true
reader_core_rc6_long_context_strategy  = true
dedicated_reader_core                  = false
```

## 🚧 Boundary of the claim

Crystal does not claim:

- universal objective-truth detection or zero hallucinations;
- legal GDPR or security certification;
- production-ready multi-tenant deployment;
- distributed locking or exactly-once orchestration;
- artificial consciousness, AGI or a “living digital personality”;
- an active PostgreSQL runtime, automatic switching, cutover or rollback;
- a completed dedicated/full autonomous Reader Core;
- automatic Reader parsing, automatic NLP/LLM proposition/relation/summary generation, embeddings/ANN/vector search or comprehension proof;
- semantic equivalence or RC-7 automatic cross-document identity/reasoning;
- that RC-4 extracted candidates are verified facts or admitted evidence;
- that RC-5 relation candidates are confirmed/resolved contradictions or admitted evidence;
- that RC-6 working sets prove comprehension or that RC-6 summaries are source text/evidence/truth/Canon admission;
- Titan, Full Exo-Cortex, Mentaury or Native Kernel functionality as current runtime.

The NLnet proposal remains **submitted / under review / not awarded**. Approximate **€50,000** remains
planning only, not an approved budget/payment commitment; budget change is none. Merged functionality,
including RC-0 through RC-5, is existing pre-agreement baseline. If RC-6 merges before an agreement,
RC-6 also becomes existing baseline and must not be counted again as future funded delivery.

## 🌍 Translation program

English is the primary source language. Russian Reader-dependent root and D1/D3/D4/D5 detail
surfaces are currently pinned to immutable RC-5 English checkpoint
`51c205fe048fd69d39fcd47b43e042a50de432bc`. The RC-6 English source checkpoint is committed first;
a subsequent Russian parity commit updates those Russian surfaces and translation ledgers to the
exact RC-6 checkpoint SHA. Eight other locale root/Reader-detail surfaces retain their rich prior
translations and remain explicitly `REFRESH_NEEDED` (64 tracked documents). D2 and Quick Start remain
current across all nine supported locales because RC-6 does not change those source contracts.

See [LOCALIZATION_POLICY.md](./docs/LOCALIZATION_POLICY.md) and
[TRANSLATION_STATUS.md](./docs/TRANSLATION_STATUS.md).

## 🤝 Contributing and license

See [CONTRIBUTING.md](./CONTRIBUTING.md), [SECURITY.md](./SECURITY.md),
[GOVERNANCE.md](./GOVERNANCE.md) and [AGPL-3.0](./LICENSE).
