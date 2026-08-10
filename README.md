# 🔱 Velantrim ExoCortex — Crystal

> 🌐 🇬🇧 **English** · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 [Español](./README.es.md) · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 [Русский](./README.ru.md) · 🇨🇳 [简体中文](./README.zh-CN.md) · 🇸🇦 [العربية](./README.ar.md) · 🇯🇵 [日本語](./README.ja.md) · 🇮🇳 [हिन्दी](./README.hi.md)

### Verifiable, local-first memory, evidence and decision infrastructure for trustworthy AI systems

`v0.3.0` · 🧪 **2078 passed / 13 skipped / 0 failed** · 🎯 **9756 statements / 100.00% line coverage** · 🧬 **7/7 declared Ring Zero mutants killed** · ✅ **9 permanent CI jobs** · 🐘 **real PostgreSQL/pgvector integration** · 🐍 **pure-standard-library default runtime** · ⚖️ **AGPL-3.0**

> Crystal is not another chatbot and it is not an autonomous “truth oracle.” It is a
> memory, evidence and decision boundary that records what a claim is, where it came
> from, what epistemic state it is in, whether it may ground an answer, and how a
> contradiction was resolved through an explicit audited decision.

**Verified runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6` — merged PR #337.  
**Validated runtime head / CI:** `d7af7c80722274f9217bc5545d150f92e9363f37` / `31256316536` — 9/9 successful.  
**PostgreSQL integration:** `31256316532` — successful against PostgreSQL 16 and pgvector 0.8.2.  
**Reader foundation:** RC-1 evidence-linked skeleton, RC-2 caller-supplied Structural Document Map, RC-3 explicit deterministic multi-pass mechanics and RC-4 source-linked proposition extraction are implemented/tested bounded layers; the dedicated/full autonomous Semantic Reading runtime remains **not implemented**.  
**Exact public evidence:** [TEST_REPORT.md](./TEST_REPORT.md), [STATUS.md](./docs/STATUS.md) and the [machine-readable implementation manifest](./docs/status/implementation-manifest.json).

> **Documentation language policy:** English is the primary working and source language,
> not the only intended documentation language. Completed root README translations target
> full visual and semantic parity. Other stable documents are translated progressively in
> separate phases. See the [localization policy](./docs/LOCALIZATION_POLICY.md) and
> [translation status ledger](./docs/TRANSLATION_STATUS.md).

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
EXTRACTED_PROPOSITION is not a verified fact.
Reader candidate is not admitted evidence.
```

## 🧠 What Crystal provides

- typed claims and an explicit epistemic lifecycle;
- source identity, evidence spans and provenance;
- bounded Reader RC-1 source/session artifacts with fidelity and coverage semantics;
- bounded Reader RC-2 caller-supplied structural document maps with explicit ambiguity;
- bounded Reader RC-3 explicit multi-pass process mechanics with auditable coverage effects;
- bounded Reader RC-4 source-linked `EXTRACTED_PROPOSITION` candidates with explicit attribution/category/negation/qualifiers;
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
- deterministic evaluation, 100% line coverage and a Ring Zero mutation gate;
- verified SQLite backup/restore and bounded logical migration;
- optional PostgreSQL/pgvector inactive import with independent exact-state equivalence.

Reader RC-1/RC-2/RC-3/RC-4 retain no source body, add no public Reader API/CLI or durable Reader
storage schema, and have no truth/Canon/ESM/planner authority. RC-3 provides explicit deterministic
pass mechanics; RC-4 validates caller-supplied proposition candidates against completed substantive
Reader context. These layers do **not** provide an automatic parser, automatic NLP/LLM extraction,
autonomous model-driven reader, embeddings, ANN/vector-database Reader stack or automatic
cross-document reasoning. RC-4 does not call `core.evidence.attach_evidence()` or write fact evidence.
`coverage != comprehension proof`; `pass completion != comprehension proof`;
`EXTRACTED_PROPOSITION != verified fact`; `Reader candidate != admitted evidence`.

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
├── 🔐 Governance
│   ├── Scoped curator capability
│   ├── Authenticated actor binding
│   └── Process-local decision lease
│
└── 📊 Verification
    ├── Python 3.11 / 3.12
    ├── 100% line coverage
    ├── Ring Zero mutation gate
    ├── Security and Docker gates
    └── Exact-head CI evidence
```

### 🏗️ ASCII architecture — information flow

```text
┌──────────────────────────────────────────────────────────────────────┐
│               🔱 Velantrim ExoCortex — Crystal                      │
│          Memory → evidence → review → trusted read projection       │
└──────────────────────────────────────────────────────────────────────┘

                         📥 Explicit ingest
                                │
                                ▼
             🧾 Claim type + source + exact evidence span
                                │
                                ▼
                      🧠 Observed state in L0 / L1
                                │
                                ▼
        🛡️ Guardian ──► ⚖️ TruthGate ──► 🚧 restrictions
                                │
                  ┌─────────────┴─────────────┐
                  │                           │
                  ▼                           ▼
          ⏳ L2 waiting / review       🏛️ Physical L3 graph
                  │                           │
                  │                           ▼
                  │                 📜 provenance / TRACE
                  └─────────────┬─────────────┘
                                │
                                ▼
                    📐 Immutable TrustSnapshot
                                │
                                ▼
                  🛡️ Guardian + CanonicalView STRICT
                                │
                   ┌────────────┴────────────┐
                   │                         │
                   ▼                         ▼
             💬 Grounded answer       🚫 Restricted refusal
                   │
                   ▼
              🧾 Replayable Receipt

⚖️ Unresolved contradiction
        │
        ▼
📋 Immutable ContradictionReport
        │
        ▼
🔐 scoped principal + capability + decision lease
        │
        ▼
🧑‍⚖️ explicit COEXIST / CONTEXTUALIZE / SUPERSEDE
        │
        ▼
📜 audited canonical write path
```

### 🌳 Module tree — ownership and connections

```text
🌳 Crystal
│
├── 📖 Reader foundation
│   ├── core/reader_core.py — RC-1 source/session artifacts
│   ├── core/reader_structure.py — RC-2 Structural Document Map
│   ├── core/reader_passes.py — RC-3 explicit multi-pass mechanics
│   └── core/reader_extraction.py — RC-4 source-linked proposition candidates
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
├── 🗄️ Storage portability
│   ├── SQLite backup/restore
│   ├── Canonical logical bundle
│   ├── Bounded verification
│   └── PostgreSQL inactive exact-equivalence import
│
└── 📊 Verification
    ├── Tests and coverage
    ├── Mutation gate
    ├── Security scans
    ├── Docker build
    └── Documentation/status gate
```

## 🧭 Central distinctions

```text
physical L3 graph     != strict Canon
query                 != ingest
confidence            != independent evidence
LLM output            != independent factual source
contradiction detect  != automatic winner
TopicFacet relevance  != truth
migration receipt     != claim evidence
successful import     != backend activation
process-local lease   != distributed coordination
Reader coverage       != comprehension proof
Reader structure      != truth/confidence authority
Reader pass complete  != comprehension proof
EXTRACTED_PROPOSITION != verified fact
Reader candidate      != admitted evidence
```

TruthGate is an admission-policy gate, not an oracle that independently knows
objective truth. Strict Canon is a policy-allowed read projection over evidence,
status, ESM state, confidence shape and processing restrictions.

## 🧱 Memory and evidence surfaces

| Surface | Role | Critical boundary |
|---|---|---|
| Reader RC-1 | evidence-linked source/session artifacts | observations and coverage do not admit truth |
| Reader RC-2 | version-bound structural map | order/prominence is metadata, not authority |
| Reader RC-3 | explicit pass ledger over declared targets | pass completion is process state, not comprehension/truth |
| Reader RC-4 | source-linked extracted proposition candidates | source presentation/candidate state, not verified fact or admitted evidence |
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

The PostgreSQL target is absent from ordinary runtime composition and cannot serve
normal reads or writes. Successful import is operational migration evidence, but it
does not establish:

- activation or automatic backend selection;
- cutover, rollback or dual-write;
- TruthGate admission or strict Canon membership;
- ANN quality acceptance;
- production multi-tenancy or distributed exactly-once guarantees.

The driver is installed only through `[postgresql]` and lazy-loaded by explicit
operator migration commands. The default installation remains pure standard library.
Production credentials and credential-bearing connection strings must not enter
profiles, bundles, receipts, application logs, GitHub issues or Notion.

## 🔎 Crystal versus classic RAG

| Question | Classic RAG | Crystal |
|---|---|---|
| Find relevant material | primary strength | supported through retrieval adapters |
| Separate user claim from verified fact | application-specific | explicit typed boundary |
| Track lifecycle and contradictions | usually external logic | first-class states and reports |
| Preserve version-bound reading/process artifacts | application-specific | RC-1/RC-2/RC-3/RC-4 bounded Reader foundation |
| Preserve proposition attribution/qualifiers before admission | application-specific | RC-4 explicit source-presentation metadata |
| Prevent generated text becoming its own source | not inherent | Ring Zero admission invariant |
| Replay answer evidence | optional | TRACE and Receipt architecture |
| Resolve contradictions accountably | application-specific | explicit authorized dispositions |
| Group by topic without changing trust | application-specific | advisory TopicFacet metadata |
| Run without a mandatory cloud/model provider | varies | pure-stdlib local-first baseline |

## 🛡️ Public read-only query boundary

These surfaces share `core.query_pipeline`:

```text
HTTP /ask and /receipt
CLI ask and receipt
MCP search
```

They do not create facts, transition ESM state, write L3, operate the outbox,
record episodes, initialize an embedding fingerprint, store unknown candidates
or mutate adaptive verification state.

See [Read-Only Query Boundary](./docs/architecture/read-only-query-boundary.md).

## ⚖️ Explicit contradiction decisions

Normal approval fails closed while a contradiction is unresolved. A curator must
choose an explicit disposition and provide an actor and reason.

```bash
python -m core.conflict_surfaces FACT_ID \
  --disposition COEXIST \
  --actor alice \
  --reason "the claims describe different contexts" \
  --expected-report-id REPORT_ID
```

For hosted FastAPI deployments, register `POST /review/resolve-conflict` with the
host application's authentication dependency. The current `CuratorLeaseRegistry`
prevents concurrent decisions only inside one process; distributed deployments
require an external lease adapter.

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
- [Inactive PostgreSQL import contract](./docs/architecture/POSTGRESQL_INACTIVE_IMPORT.md)
- [PostgreSQL/pgvector RFC](./docs/architecture/POSTGRESQL_PGVECTOR_PROFILE_RFC.md)
- [Current AI context](./docs/ai/CURRENT_STATE.md)
- [Known risks](./docs/ai/KNOWN_RISKS.md)
- [NLnet scope](./docs/GRANT_NLNET_SCOPE.md)
- [Baseline → funded-delta matrix](./docs/grants/baseline-funded-delta-matrix.md)
- [Localization policy](./docs/LOCALIZATION_POLICY.md)
- [Translation status](./docs/TRANSLATION_STATUS.md)
- [Roadmap](./ROADMAP.md)
- [Security policy](./SECURITY.md)

## ✅ Verified baseline

```text
Runtime merge: bbd816c09dd39a02e6de6c1014438490572f40f6 (PR #337)
Python 3.11: 2078 passed / 13 skipped / 0 failed
Python 3.12: 2078 passed / 13 skipped / 0 failed
Statements:  9756
Coverage:    100.00%
Mutation:    7/7 declared Ring Zero mutants killed
CI jobs:     9/9
PostgreSQL integration: successful against PostgreSQL 16 + pgvector 0.8.2
Reader RC-1: implemented/tested bounded evidence-linked skeleton
Reader RC-2: implemented/tested bounded Structural Document Map
Reader RC-3: implemented/tested bounded explicit multi-pass mechanics
Reader RC-4: implemented/tested bounded source-linked proposition extraction
Dedicated/full autonomous Reader: not implemented
```

The numeric runtime/test block above is the retained PR #337 verification checkpoint; later Reader
milestones use their own exact-head and post-merge CI evidence.

## 🚧 Boundary of the claim

Crystal does not claim:

- universal objective-truth detection;
- zero hallucinations;
- legal GDPR or security certification;
- production-ready multi-tenant deployment;
- distributed locking or exactly-once orchestration;
- artificial consciousness, AGI or a “living digital personality”;
- an active PostgreSQL runtime, automatic switching, cutover or rollback;
- a completed dedicated/full autonomous Reader Core;
- automatic Reader parsing, automatic NLP/LLM proposition extraction, embeddings/ANN/vector search, automatic cross-document reasoning or comprehension proof;
- that RC-4 extracted candidates are verified facts or admitted evidence;
- Titan, Full Exo-Cortex, Mentaury or Native Kernel functionality as current runtime.

The NLnet proposal remains **submitted / under review / not awarded**. Merged
functionality is existing baseline and must not be counted again as future funded
delivery.

## 🌍 Translation program

Translation is progressive. The target for every supported root language is a full
README with equivalent semantic and visual coverage, followed by staged translation of
Quick Start, Status, Reviewer Guide, architecture, safety and grant documents. A temporary
short orientation file is not considered the final state.

See [LOCALIZATION_POLICY.md](./docs/LOCALIZATION_POLICY.md) and
[TRANSLATION_STATUS.md](./docs/TRANSLATION_STATUS.md).

## 🤝 Contributing and license

See [CONTRIBUTING.md](./CONTRIBUTING.md), [SECURITY.md](./SECURITY.md),
[GOVERNANCE.md](./GOVERNANCE.md) and [AGPL-3.0](./LICENSE).