# 🔱 Velantrim ExoCortex — Crystal

> 🌐 🇬🇧 **English** · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 [Español](./README.es.md) · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 [Русский](./README.ru.md) · 🇨🇳 [简体中文](./README.zh-CN.md) · 🇸🇦 [العربية](./README.ar.md) · 🇯🇵 [日本語](./README.ja.md) · 🇮🇳 [हिन्दी](./README.hi.md)

### Verifiable, local-first memory infrastructure for trustworthy AI systems

`v0.3.0` · 🧪 **1780 passed / 12 skipped** · 🎯 **100% coverage** · 🧬 **7/7 declared mutants killed** · ✅ **9 CI jobs** · 🐍 **pure-stdlib default runtime** · ⚖️ **AGPL-3.0**

> Crystal is not another chatbot. It is a memory and evidence boundary that
> records what a claim is, where it came from, what state it is in, and whether
> the system is allowed to use it as strict grounding.

**Verified runtime checkpoint:** `916097f` — merged PR #292.  
**Implementation truth:** code and tests merged into GitHub `main`.  
**Exact evidence:** [TEST_REPORT.md](./TEST_REPORT.md) and the
[machine-readable implementation manifest](./docs/status/implementation-manifest.json).

---

## 🎯 The problem Crystal addresses

Many AI applications mix several different things inside one context window or
vector store:

- source documents;
- user statements;
- model-generated text;
- hypotheses and interpretations;
- retrieved fragments;
- durable memory;
- final answers.

When those categories are not separated, a fluent sentence can silently acquire
more authority than its evidence supports. A user claim can look like a verified
fact, a stale fact can remain active, or a generated answer can be written back
into memory as if it were an independent source.

Crystal introduces explicit boundaries between **observation, admission,
storage, retrieval and answer grounding**.

```text
A claim is not trusted because it is fluent.
A node is not strict Canon because it exists in a graph.
A high score is not evidence.
A model output is not an independent source.
```

---

## 🧠 What Crystal is

Crystal is a public, grant-facing, local-first memory core for systems that need:

- typed claims and explicit epistemic state;
- source and provenance metadata;
- policy-controlled admission into graph memory;
- strict read projection for factual grounding;
- TRACE and replayable answer receipts;
- evidence spans and import-session accountability;
- review queues and resumable review sessions;
- processing restriction and erasure mechanisms;
- deterministic evaluation and executable trust invariants;
- optional HTTP, CLI and MCP interfaces.

### What Crystal is not

Crystal is **not**:

- Titan or the Full Personal Exo-Cortex;
- an autonomous cognitive operating system;
- a consciousness or personality simulation;
- a universal truth detector;
- a guarantee of zero hallucinations;
- a legal GDPR certification;
- a security certification;
- a production multi-tenant platform without additional identity and access
  controls;
- dependent on a mandatory LLM, embedding provider or cloud service.

Research concepts may inform future RFCs, but they are not current runtime claims
unless code, tests and documentation are merged into this repository.

---

## 🏛️ Architecture at a glance

```text
┌─────────────────────────────────────────────────────────────┐
│ 📥 Input / document / explicit ingest                       │
└──────────────────────────────┬──────────────────────────────┘
                               ▼
                    ┌──────────────────────┐
                    │ Claim classification │
                    │ + evidence metadata  │
                    └──────────┬───────────┘
                               ▼
                    ┌──────────────────────┐
                    │ L0/L1 operational    │
                    │ state: Observed      │
                    └──────────┬───────────┘
                               ▼
                    ┌──────────────────────┐
                    │ Guardian             │
                    │ structural contract  │
                    └──────────┬───────────┘
                               ▼
                    ┌──────────────────────┐
                    │ TruthGate            │
                    │ admission policy     │
                    └──────────┬───────────┘
                               ▼
                    ┌──────────────────────┐
                    │ contradiction /      │
                    │ restriction checks   │
                    └──────────┬───────────┘
                               ▼
                    ┌──────────────────────┐
                    │ Physical L3 graph    │
                    │ multi-status memory  │
                    └──────────┬───────────┘
                               │ read only
                               ▼
                    ┌──────────────────────┐
                    │ immutable            │
                    │ TrustSnapshot        │
                    └──────────┬───────────┘
                               ▼
                    ┌──────────────────────┐
                    │ Guardian +           │
                    │ CanonicalView STRICT │
                    └──────────┬───────────┘
                               ▼
                    ┌──────────────────────┐
                    │ FactsPack + TRACE    │
                    │ answer + Receipt     │
                    └──────────────────────┘
```

### The central distinction

```text
Physical L3 graph ≠ strict Canon
```

The physical graph may contain different truth statuses and lifecycle states.
Strict Canon is the policy-allowed projection that satisfies the required truth
status, ESM state, provenance structure, confidence shape and processing
restriction rules.

Crystal therefore does not claim to compute absolute truth. It controls **which
claims, under which evidence and policy conditions, may be treated as trusted
memory and strict answer grounding**.

---

## 🧱 Memory model

| Surface | Role | Important boundary |
|---|---|---|
| **L0** | in-process working cache | fast and rebuildable |
| **L1** | SQLite/WAL operational memory | states, restrictions and pending work |
| **L2** | logical pending/review boundary | not automatically strict Canon |
| **L3** | graph-backed multi-status memory | automatic admission only through policy gates |
| **CanonicalView** | strict read projection | physical membership does not imply trust |
| **TRACE / Receipt** | proof and replay layer | explains grounding and detects drift |

The project supports a dependency-free SQLite baseline and pluggable graph
adapters. Storage backend choice does not change the trust contract.

---

## 🛡️ Trust boundaries

### Admission is explicit

```text
explicit ingest
→ pending operational state
→ Guardian
→ TruthGate
→ contradiction / restriction checks
→ L3 graph admission
```

Guardian checks structural and contract requirements. TruthGate applies admission
policy. Neither component is an oracle that independently knows whether every
source statement is objectively true.

### Model output has no automatic factual authority

An LLM or other generator may help extract, classify, summarize, compare or
phrase information. It cannot independently promote its own output into a
`VERIFIED WORLD_FACT`.

The historical `ENABLE_TRUTH_POLICY=off` runtime bypass has been removed. The
LLM-origin block is now a non-configurable Ring Zero invariant.

### Querying is read-only on public surfaces

The following surfaces use the same zero-durable-mutation query service:

```text
HTTP /ask and /receipt
CLI ask and receipt
MCP search
        ↓
core.query_pipeline
```

A public question or search does not:

- create or update L0/L1 facts;
- transition ESM state;
- write L3 facts, relations, entities or mentions;
- drain or modify the L3 outbox;
- record episodic links;
- initialize an unset embedding fingerprint;
- store unknown retrieval candidates;
- mutate adaptive verification state.

`core.pipeline.run()` remains an explicit legacy/internal admission-capable
compatibility function. Public CLI query commands no longer call it.

See [Read-Only Query Boundary](./docs/architecture/read-only-query-boundary.md).

### Immutable read reconciliation

Physical L3 content and deny-dominant L1 state are reconciled into a frozen,
slotted `TrustSnapshot` before a compatibility mapping reaches Guardian or
CanonicalView.

```text
L3 claim and verdict
        +
L1 terminal state / restriction / metadata drift
        ↓
immutable TrustSnapshot
        ↓
fresh compatibility mapping
```

This prevents partially mutated hybrid records and makes store disagreement
explicit through content-free conflict categories.

---

## 🔎 Crystal versus classic RAG

Classic RAG and Crystal solve different parts of the problem.

| Question | Classic RAG | Crystal |
|---|---|---|
| Find relevant text | primary strength | supported through retrieval adapters |
| Distinguish user claim from verified fact | usually application-specific | explicit typed status boundary |
| Track lifecycle and contradiction state | usually external logic | first-class memory metadata |
| Prevent generated text becoming its own source | not inherent | Ring Zero admission invariant |
| Produce replayable answer evidence | optional | TRACE and Receipt architecture |
| Enforce processing restriction on reads | application-specific | trust/read boundary requirement |
| Work without mandatory cloud/model provider | varies | pure-stdlib local-first baseline |

Crystal can be used **with** lexical, vector or graph retrieval. Retrieval score is
ranking metadata; it never becomes truth status, evidence quality or source
authority.

---

## 🌍 Where Crystal can be used

Crystal is most useful where long-lived AI memory must remain inspectable.

### 🤖 Agent and assistant memory

- separate user-reported information from independently verified facts;
- preserve source history across sessions;
- prevent query-time writes and self-reinforcing memory loops;
- issue receipts for important answers.

### 🔬 Research and evidence workspaces

- retain exact evidence spans;
- mark hypotheses, interpretations and conflicts separately;
- review claims before strict use;
- track evidence and source drift.

### 🏢 Internal knowledge systems

- build local-first institutional memory;
- expose policy-aware retrieval to tools and agents;
- retain accountable review decisions;
- support restricted or erased records without silently leaking them through
  answer generation.

### 🧪 AI safety and evaluation

- test admission boundaries independently of model quality;
- replay provenance after memory changes;
- measure retrieval and contradiction behavior deterministically;
- execute targeted semantic mutations against Ring Zero invariants.

Crystal is infrastructure, not a finished vertical product. Authentication,
organization-specific policy, deployment controls and domain review procedures
must be added for production use.

---

## 🚀 Quick start

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
python scripts/eval_gate.py --out-dir eval-artifacts
bash scripts/ring_zero_mutation_gate.sh
```

Basic CLI flow:

```bash
velantrim ingest "Water boils at 100C at sea level"
velantrim ask "how does water behave"
velantrim receipt "how does water behave" > receipt.json
velantrim verify-receipt receipt.json
```

Persistent dependency-free L3 storage:

```bash
VELANTRIM_L3_BACKEND=sqlite \
VELANTRIM_L3_PATH=./data/canon.db \
velantrim ask "..."
```

For setup details, see [Quick Start](./docs/QUICKSTART.md).

---

## 🔌 Optional interfaces

### FastAPI

```bash
pip install '.[api]'
velantrim-api
```

| Method | Path | Contract |
|---|---|---|
| `GET` | `/health` | liveness/readiness |
| `POST` | `/ingest` | explicit admission through Guardian + TruthGate |
| `POST` | `/ask` | strict read-only canonical query |
| `GET` | `/receipt?q=...` | read-only query plus Receipt |
| `POST` | `/verify-receipt` | replay Receipt against current state |
| `GET` | `/evidence/{fact_id}` | policy-aware evidence view |

### MCP

```bash
python -m core.mcp_server
```

MCP exposes inspection-oriented tools such as read-only search, memory reports,
fact history, conflict lookup and receipt verification. It exposes no canonical
write tool.

---

## 🧪 Verification evidence

Verified checkpoint `916097f` completed **9 CI jobs** successfully:

| CI job | Boundary |
|---|---|
| `test (3.11)` | 1780 passed / 12 skipped, 6484 statements, 100% coverage |
| `test (3.12)` | supported-version compatibility with the same result |
| `code-quality` | Ruff lint |
| `security` | Gitleaks, Bandit and pip-audit |
| `docker-build` | hardened image build |
| `eval-gate` | retrieval, grounding, contradiction and refusal metrics |
| `jsonl-integrity` | corpus structure and duplicate identifiers |
| `Ring Zero mutation gate` | **7/7 declared mutants killed** |
| `docs-status` | README/STATUS/TEST_REPORT/manifest consistency |

The mutation gate intentionally changes seven load-bearing conditions, including
TruthGate thresholds, LLM-origin rejection, strict Canon requirements, processing
restriction, ESM allowlisting, malformed-confidence handling and Receipt digest
verification. A mutant is accepted as killed only when its focused tests fail for
a normal assertion result; collection and infrastructure errors fail the gate.

These controls demonstrate tested behavior at a named checkpoint. They do not
prove absence of every defect, universal truth, legal compliance or production
security.

---

## 📌 Current implementation status

### Implemented and tested

- unified read-only HTTP, CLI and MCP-search query boundary;
- non-configurable LLM-origin TruthGate invariant;
- immutable `TrustSnapshot` for read reconciliation;
- strict `CanonicalView` projection;
- TRACE and replayable Receipts;
- evidence spans, import sessions and review queue;
- resumable review sessions;
- local-first SQLite/WAL baseline and pluggable L3 adapters;
- deterministic evaluation;
- targeted Ring Zero mutation gate.

### Partial or requiring hardening

- roles and multi-curator authorization;
- broader provenance-chain lifecycle wiring;
- formal contradiction decision policy;
- fixed-runner performance history and regression reporting;
- translation freshness automation.

### RFC / research only

- Mode Layer and Observer action policy;
- bi-temporal reasoning;
- provenance grades;
- autonomous question generation;
- advanced ontology and causal conflict resolution;
- distributed replication;
- Titan and Full Exo-Cortex cognitive integration.

The exact classification is maintained in
[Implementation Status](./docs/IMPLEMENTATION_STATUS.md).

---

## 🗺️ Documentation by reader

| Reader | Start here |
|---|---|
| New user | [Quick Start](./docs/QUICKSTART.md) |
| Engineer | [Architecture](./docs/ARCHITECTURE.md) and [ADR index](./docs/ADR.md) |
| Reviewer | [Reviewer Guide](./docs/REVIEWER_GUIDE.md) and [Reviewer Demo](./docs/REVIEWER_DEMO.md) |
| Security reviewer | [SECURITY](./SECURITY.md) and [Threat Model](./docs/security/threat-model.md) |
| Grant reviewer | [NLnet Scope](./docs/GRANT_NLNET_SCOPE.md) and [Test Report](./TEST_REPORT.md) |
| Researcher | [Implementation Status](./docs/IMPLEMENTATION_STATUS.md) and [Roadmap](./ROADMAP.md) |
| Everyone | [Complete Documentation Map](./docs/DOCUMENTATION_MAP.md) |

The authority hierarchy is:

```text
merged code and tests
→ TEST_REPORT + implementation manifest
→ STATUS + IMPLEMENTATION_STATUS
→ README and reviewer guides
→ translations
→ RFC and roadmap documents
```

---

## 💶 Grant boundary

The project has been submitted to the **NLnet NGI0 Commons Fund** and is under
review. This repository does not claim that funding has been awarded.

```text
BASELINE TODAY
    +
MEASURABLE FUNDED DELTA
    =
INDEPENDENTLY VERIFIABLE DELIVERABLE
```

Already-merged work remains baseline and is not counted again as paid delivery.
Titan, cognitive or neuromorphic research is not silently added to the Crystal
grant scope.

- [Grant scope](./docs/GRANT_NLNET_SCOPE.md)
- [Baseline/funded-delta matrix](./docs/grants/baseline-funded-delta-matrix.md)
- [Funding use plan](./docs/grants/funding-use-plan.md)

---

## 🤝 Contributing and governance

Crystal is licensed under **AGPL-3.0**.

- [Contributing](./CONTRIBUTING.md)
- [Governance](./GOVERNANCE.md)
- [Security policy](./SECURITY.md)
- [Privacy](./PRIVACY.md)
- [Code of Conduct](./CODE_OF_CONDUCT.md)

> **📊 Canon = policy-admitted verified projection**  
> **🔗 Provenance = inspectable support, not automatic truth**  
> **🏠 Local-first = control over memory and evidence**

---

> 🌐 🇬🇧 **English** · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 [Español](./README.es.md) · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 [Русский](./README.ru.md) · 🇨🇳 [简体中文](./README.zh-CN.md) · 🇸🇦 [العربية](./README.ar.md) · 🇯🇵 [日本語](./README.ja.md) · 🇮🇳 [हिन्दी](./README.hi.md)
