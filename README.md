# 🔱 Velantrim ExoCortex — Crystal

> 🌐 🇬🇧 **English** · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 [Español](./README.es.md) · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 [Русский](./README.ru.md) · 🇨🇳 [简体中文](./README.zh-CN.md) · 🇸🇦 [العربية](./README.ar.md) · 🇯🇵 [日本語](./README.ja.md) · 🇮🇳 [हिन्दी](./README.hi.md)

### Verifiable, local-first memory infrastructure for trustworthy AI systems

`v0.3.0` · 🧪 **1853 passed / 12 skipped** · 🎯 **100% coverage** · 🧬 **7/7 declared mutants killed** · ✅ **9 CI jobs** · 🐍 **pure-stdlib default runtime** · ⚖️ **AGPL-3.0**

> Crystal is not another chatbot. It is a memory, evidence and decision boundary
> that records what a claim is, where it came from, what state it is in, whether
> it may ground an answer, and how contradictions were explicitly resolved.

**Verified runtime checkpoint:** `f91299c44a1a1850fa516f3abb96c916326f7a8c` — merged PR #302.  
**Implementation truth:** code and tests merged into GitHub `main`.  
**Exact evidence:** [TEST_REPORT.md](./TEST_REPORT.md) and the
[machine-readable implementation manifest](./docs/status/implementation-manifest.json).

> 🤖 **AI coding agent or automated auditor:** start with
> [`docs/ai/README.md`](./docs/ai/README.md), then follow the mandatory reading and
> verification contract in [`AGENTS.md`](./AGENTS.md). Do not begin by loading the
> entire repository or treating issues/research PRs as implemented runtime.

> **Localization contract:** every top-level translated README follows this
> document's capability, safety and status boundaries. Stable API identifiers
> remain in English/code form; explanatory prose is translated naturally.

---

## 🎯 Why Crystal exists

Many AI systems mix source documents, user claims, model output, hypotheses,
retrieved fragments and durable memory in one context or vector store. When
those categories are not separated, fluent text can silently acquire authority
that its evidence does not support.

Crystal makes the boundaries explicit:

```text
A fluent claim is not automatically trusted.
A graph node is not automatically strict Canon.
A retrieval score is not evidence.
A model output is not an independent source.
A contradiction does not select its own winner.
A topic label is not a truth verdict.
```

## 🧠 What Crystal provides

- typed claims and an explicit epistemic lifecycle;
- source, evidence-span and provenance metadata;
- Guardian and TruthGate admission boundaries;
- a multi-status physical L3 graph separated from strict Canon;
- immutable, deny-dominant `TrustSnapshot` read reconciliation;
- read-only public HTTP, CLI and MCP query surfaces;
- TRACE and replayable, tamper-evident Receipts;
- restriction, erasure, audit and import-session controls;
- review queues and resumable review sessions;
- typed immutable contradiction reports;
- explicit `COEXIST`, `CONTEXTUALIZE` and `SUPERSEDE` decisions;
- CLI and authenticated HTTP conflict-resolution surfaces;
- scoped curator roles/capabilities and in-process decision leases;
- advisory multi-label topic facets that never grant authority;
- a machine-readable ESM specification derived from runtime transitions;
- deterministic evaluation, 100% line coverage and a Ring Zero mutation gate;
- scheduled/manual L3 benchmark history with versioned artifacts.

## 🏛️ Architecture at a glance

The three maps below show the same system from complementary viewpoints:
**purpose**, **information flow**, and **module relationships**.

### 🧠 Mindmap — purpose and capability boundaries

```text
🧠 Velantrim ExoCortex — Crystal
│
├── 🎯 Purpose
│   ├── Verifiable memory for AI
│   ├── Local-first trust infrastructure
│   └── Evidence-backed answers and decisions
│
├── 🏛️ Memory Model
│   ├── L0 — in-process working cache
│   ├── L1 — operational lifecycle memory
│   ├── L2 — pending and review boundary
│   └── L3 — graph-backed multi-status memory
│
├── 🛡️ Trust Boundary
│   ├── Guardian — structural and policy checks
│   ├── TruthGate — admission-policy boundary
│   ├── TrustSnapshot — immutable read reconciliation
│   └── CanonicalView — strict trusted projection
│
├── 📜 Evidence and Auditability
│   ├── Provenance and evidence spans
│   ├── TRACE — grounding lineage
│   └── Receipt — replay and tamper evidence
│
├── ⚖️ Review and Contradictions
│   ├── Review queues and resumable sessions
│   ├── Immutable ContradictionReport
│   ├── COEXIST
│   ├── CONTEXTUALIZE
│   └── SUPERSEDE
│
├── 🏷️ Advisory Navigation
│   └── TopicFacet — multi-label, non-authoritative metadata
│
├── 🔐 Governance and Coordination
│   ├── Scoped curator roles and capabilities
│   ├── Authenticated actor binding
│   └── Process-local decision leases
│
└── 📊 Verification
    ├── Deterministic tests and evaluation
    ├── 100% line coverage
    ├── Ring Zero mutation gate
    └── Versioned benchmark history
```

### 🏗️ ASCII architecture — how information moves

```text
┌─────────────────────────────────────────────────────────────────────┐
│              🔱 Velantrim ExoCortex — Crystal                      │
│      Local-first verifiable memory infrastructure for AI           │
└─────────────────────────────────────────────────────────────────────┘

                         📥 Explicit ingest
                                │
                                ▼
                 🧾 Claim type + source + evidence span
                                │
                                ▼
                      🧠 L0 / L1 Observed state
                                │
                                ▼
             🛡️ Guardian ──► ⚖️ TruthGate ──► 🚧 restrictions
                                │
                  ┌─────────────┴─────────────┐
                  │                           │
                  ▼                           ▼
        ⏳ L2 pending / review       🏛️ Physical L3 graph
                  │                           │
                  │                           ▼
                  │                 📜 provenance / TRACE
                  │                           │
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
          💬 Grounded answer        🚫 Bounded refusal
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

🏷️ TopicFacet metadata ──► navigation / filtering / grouping only
                         └─► never truth, ESM, evidence or Canon authority
```

### 🌳 Relation tree — how the modules connect

```text
🌳 Crystal System Relations
│
├── 🧠 Memory Layer
│   ├── L0 ──► fast, rebuildable working cache
│   ├── L1 ──► lifecycle, restrictions and pending work
│   ├── L2 ──► logical review boundary
│   └── L3 ──► graph-backed multi-status storage
│
├── 🛡️ Trust Layer
│   ├── Guardian ──► structural and policy validation
│   ├── TruthGate ──► admission decision
│   ├── TrustSnapshot ──► deny-dominant L1/L3 reconciliation
│   └── CanonicalView ──► strict grounding projection
│
├── 📜 Evidence Layer
│   ├── Source metadata
│   ├── Evidence spans
│   ├── Provenance
│   ├── TRACE
│   └── Receipt
│
├── ⚖️ Review Layer
│   ├── Review queue
│   ├── Resumable review session
│   ├── ContradictionReport
│   └── Explicit disposition
│       ├── COEXIST
│       ├── CONTEXTUALIZE
│       └── SUPERSEDE
│
├── 🔐 Authorization Layer
│   ├── CuratorPrincipal
│   ├── Role and scoped capability
│   ├── authenticated actor match
│   └── process-local decision lease
│
├── 🏷️ Advisory Layer
│   └── TopicFacet
│       ├── multi-label
│       ├── relevance-only score
│       └── no authority over truth or admission
│
├── 🔎 Public Query Layer
│   ├── HTTP /ask and /receipt
│   ├── CLI ask and receipt
│   └── MCP search
│       └── shared read-only query pipeline
│
└── 📊 Verification Layer
    ├── Python 3.11 / 3.12 tests
    ├── coverage gate
    ├── Ring Zero mutation gate
    ├── security and container checks
    └── benchmark history
```

### Central distinctions

```text
Physical L3 graph ≠ strict Canon
query ≠ ingest
confidence ≠ independent evidence
LLM output ≠ independent factual source
contradiction ≠ automatic winner
topic relevance ≠ truth or evidence quality
local lease ≠ distributed coordination guarantee
```

TruthGate is an admission-policy gate, not an oracle that independently knows
objective truth. Strict Canon is a policy-allowed read projection over evidence,
status, ESM state, confidence shape and processing restrictions.

## 🧱 Memory and evidence surfaces

| Surface | Role | Boundary |
|---|---|---|
| L0 | in-process working cache | fast and rebuildable |
| L1 | SQLite/WAL operational memory | lifecycle, restriction and pending work |
| L2 | logical review boundary | not automatically strict Canon |
| L3 | graph-backed multi-status memory | admission only through policy gates |
| TrustSnapshot | immutable read reconciliation | deny-dominant L1/L3 resolution |
| CanonicalView | strict grounding projection | graph membership does not imply trust |
| TRACE / Receipt | proof and replay layer | grounding, drift and tamper evidence |
| ContradictionReport | immutable conflict object | no confidence-only winner selection |
| TopicFacet | navigation metadata | never changes truth, ESM or Canon |
| CuratorPrincipal / lease | authorization and coordination helper | host identity + external lease required at scale |

## 🔎 Crystal versus classic RAG

| Question | Classic RAG | Crystal |
|---|---|---|
| Find relevant material | primary strength | supported through retrieval adapters |
| Separate user claim from verified fact | application-specific | explicit typed boundary |
| Track lifecycle and contradictions | usually external logic | first-class state and reports |
| Prevent generated text becoming its own source | not inherent | Ring Zero admission invariant |
| Replay answer evidence | optional | TRACE and Receipt architecture |
| Resolve contradictions accountably | application-specific | explicit authorized and audited dispositions |
| Organize by topic without changing trust | application-specific | advisory topic facets |
| Run without a mandatory cloud/model provider | varies | pure-stdlib local-first baseline |

## 🛡️ Public read-only query boundary

These surfaces share `core.query_pipeline`:

```text
HTTP /ask and /receipt
CLI ask and receipt
MCP search
```

They do not create facts, transition ESM, write L3, operate the outbox, record
episodes, initialize an embedding fingerprint, store unknown candidates or
mutate adaptive verification state.

See [Read-Only Query Boundary](./docs/architecture/read-only-query-boundary.md).

## ⚖️ Explicit contradiction decisions

Normal approval fails closed when a contradiction is unresolved. The curator
must choose an explicit disposition and provide an actor and reason.

```bash
python -m core.conflict_surfaces FACT_ID \
  --disposition COEXIST \
  --actor alice \
  --reason "the claims describe different contexts" \
  --expected-report-id REPORT_ID
```

For hosted FastAPI deployments, register `POST /review/resolve-conflict` with the
host application's authentication dependency. `core.curator_auth` can map a
host-authenticated principal to scoped capabilities; `CuratorLeaseRegistry`
prevents parallel decisions only within one process. Distributed deployments
must supply an external lease adapter.

See [Conflict-resolution surfaces](./docs/CONFLICT_RESOLUTION_SURFACES.md) and
[Topic facets and curator IAM](./docs/TOPIC_FACETS_AND_CURATOR_IAM.md).

## 🏷️ Advisory topic facets

`core.topic_facets` attaches normalized multi-label metadata for navigation,
filtering and grouping. Facet score means topic relevance only. It never changes
truth status, evidence, ESM state, contradiction outcomes or strict Canon
membership.

## 🚀 Quick start

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
```

Continue with [QUICKSTART.md](./docs/QUICKSTART.md).

## 📚 Documentation path

### 🤖 AI agents and automated auditors

- [AI agent entry point](./docs/ai/README.md)
- [Mandatory agent contract](./AGENTS.md)
- [Current state](./docs/ai/CURRENT_STATE.md)
- [Component map](./docs/ai/COMPONENT_MAP.md)
- [Known risks](./docs/ai/KNOWN_RISKS.md)
- [Audit playbook](./docs/ai/AUDIT_PLAYBOOK.md)
- [Compact work log](./docs/ai/WORK_LOG.md)

### Project and reviewer documentation

- [Documentation map](./docs/DOCUMENTATION_MAP.md)
- [Current status](./docs/STATUS.md)
- [Implementation status](./docs/IMPLEMENTATION_STATUS.md)
- [Architecture](./docs/ARCHITECTURE.md)
- [Read-only query boundary](./docs/architecture/read-only-query-boundary.md)
- [Conflict-resolution surfaces](./docs/CONFLICT_RESOLUTION_SURFACES.md)
- [Topic facets and curator IAM](./docs/TOPIC_FACETS_AND_CURATOR_IAM.md)
- [Test report](./TEST_REPORT.md)
- [Evaluation](./docs/EVAL.md)
- [Failure modes](./docs/FAILURE_MODES.md)
- [NLnet grant scope](./docs/GRANT_NLNET_SCOPE.md)

## ✅ Verified baseline

```text
Python 3.11: 1853 passed / 12 skipped
Python 3.12: 1853 passed / 12 skipped
Statements:  7236
Coverage:    100.00%
Mutation:    7/7 declared Ring Zero mutants killed
CI jobs:     9
```

## 🚧 Boundary of the claim

Crystal does not claim universal truth detection, zero hallucinations, legal
GDPR certification, security certification, production multi-tenant readiness,
artificial consciousness or Titan/Full ExoCortex functionality. Current
curator leases are process-local; production distributed coordination, external
identity-provider integration, broader provenance wiring and Titan integration
remain independent roadmap work.

## 🤝 Contributing and license

See [CONTRIBUTING.md](./CONTRIBUTING.md), [SECURITY.md](./SECURITY.md),
[GOVERNANCE.md](./GOVERNANCE.md) and [AGPL-3.0](./LICENSE).
