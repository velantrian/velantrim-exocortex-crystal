# 🔱 Velantrim ExoCortex — Crystal

> 🌐 **Language:** **English** · [Deutsch](./README.de.md)  
> 🇩🇪 [German reviewer documentation](./docs/de/README.md)

### *Verifiable, local-first, open-source memory infrastructure for trustworthy AI*

`v0.3.0` · 🧪 **1713 passed / 12 skipped** · 🎯 **100% coverage** · 🐍 **pure-stdlib default runtime** · ⚖️ **AGPL-3.0** · 🔒 **local-first**

> Crystal is a verifiable memory layer, not another chatbot. Facts carry source,
> epistemic state and provenance metadata. Automatic admission into the canonical
> graph remains governed by Guardian + TruthGate.

> **Implementation truth:** GitHub `main`. The current audited implementation
> checkpoint is commit `cd6fd44` from merged PR #265. Exact verification evidence
> is maintained in [TEST_REPORT.md](./TEST_REPORT.md).

---

## 🧭 Scope in one minute

Crystal is the public grant-facing core:

- local L0/L1 operational memory;
- local L3 canonical graph backends;
- Guardian and TruthGate admission controls;
- CanonicalView grounding;
- TRACE, provenance and replayable receipts;
- evidence spans, review queues and import sessions;
- GDPR-relevant erasure and processing-restriction mechanisms;
- deterministic evaluation and CI quality gates;
- optional FastAPI and read-only MCP surfaces.

Crystal is **not** Titan, the Full Personal Exo-Cortex, an autonomous cognitive
operating system, a consciousness project, or a self-modifying agent. Research
ideas may inform future RFCs, but they are not current runtime claims.

```text
GitHub Crystal main = implementation truth
Notion Crystal pages = synchronized strategy and grant map
Titan / Full Exo-Cortex = separate research track
```

---

## 🛡️ Current trust boundary

### Admission path

```text
input / document / agent event
→ classification and evidence
→ Guardian + TruthGate
→ L0/L1 operational memory
→ admitted L3 canonical graph
```

### HTTP query path

Merged PR #265 introduced a separate strict read-only HTTP query contract:

```text
POST /ask, GET /receipt
→ core.aio.arun()
→ core.query_pipeline.query()
→ existing Canon only
→ CanonicalView
→ answer / bounded refusal
```

For these HTTP surfaces, asking a question does not ingest into L0/L1, transition
ESM, write L3 facts or edges, drain the outbox, record episode links, initialize an
embedding fingerprint, or mutate adaptive verification state.

### Explicit residual scope

The read-only guarantee is intentionally narrow and honest:

- CLI `ask` and `receipt` still use the legacy admission-capable compatibility path;
- `core.pipeline.run()` remains available;
- MCP exposes no explicit mutation tools, but MCP search may initialize an unset
  embedding fingerprint and is therefore not described as a zero-mutation path.

See [docs/architecture/read-only-query-boundary.md](./docs/architecture/read-only-query-boundary.md).

---

## 🧠 Memory model

| Layer | Role | Boundary |
|---|---|---|
| **L0** | in-process working cache | fast, rebuildable |
| **L1** | SQLite/WAL operational memory | states, restrictions, updates |
| **L2** | pending and curator-review path | not automatically canonical |
| **L3** | canonical graph | automatic admission only through TruthGate |
| **TRACE / Receipt** | proof layer | explains grounding and detects drift |

The physical graph can carry different truth statuses. In the strict sense,
Canon means the VERIFIED, trace-valid, policy-allowed projection—not every node
that happens to exist in a graph backend.

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
```

Basic CLI:

```bash
velantrim ingest "Water boils at 100C at sea level"
velantrim ask "how does water behave"
velantrim receipt "how does water behave" > receipt.json
velantrim verify-receipt receipt.json
```

For a persistent dependency-free L3 backend:

```bash
VELANTRIM_L3_BACKEND=sqlite \
VELANTRIM_L3_PATH=./data/canon.db \
velantrim ask "..."
```

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
| `POST` | `/ingest` | admission through Guardian + TruthGate |
| `POST` | `/ask` | strict read-only canonical query |
| `GET` | `/receipt?q=...` | read-only query plus receipt |
| `POST` | `/verify-receipt` | replay receipt against current state |
| `GET` | `/evidence/{fact_id}` | policy-aware public evidence view |

FastAPI and Uvicorn are optional extras. The default runtime does not require a
cloud service or a third-party model provider.

### MCP

```bash
python -m core.mcp_server
```

MCP offers inspection-oriented tools such as search, memory reports, fact history,
conflict lookup and receipt verification. It has no explicit canonical write tool;
the embedding-fingerprint residual above still applies.

---

## 🧪 Evaluation

Crystal already ships a deterministic evaluation baseline:

- retrieval hit@k and MRR;
- trace and metadata completeness;
- source-span coverage;
- receipt replay survival;
- contradiction precision and recall;
- trust-boundary refusal checks;
- CI regression floors and ceilings.

The current grant-safe decision on broader replay is recorded in
[docs/grants/evaluation-replay-adoption.md](./docs/grants/evaluation-replay-adoption.md):
Titan's deterministic replay work is prior art, not copied Crystal runtime.
Any future implementation must extend the existing Crystal evaluation stack,
remain offline and non-authoritative, and preserve the funded baseline/delta rule.

---

## 💶 Grant boundary

The project has been submitted to the NLnet NGI0 Commons Fund for review. The
public repository does **not** claim that funding has been awarded.

The governing formula is:

```text
BASELINE TODAY
    +
MEASURABLE FUNDED DELTA
    =
INDEPENDENTLY VERIFIABLE DELIVERABLE
```

Already-merged work remains baseline and is not counted again as paid delivery.
New cognitive, neuromorphic or Titan mechanisms are not silently added to the
Crystal grant scope. See:

- [docs/GRANT_NLNET_SCOPE.md](./docs/GRANT_NLNET_SCOPE.md)
- [docs/grants/baseline-funded-delta-matrix.md](./docs/grants/baseline-funded-delta-matrix.md)
- [docs/grants/funding-use-plan.md](./docs/grants/funding-use-plan.md)
- [docs/grants/evaluation-replay-adoption.md](./docs/grants/evaluation-replay-adoption.md)

---

## ✅ Verification gates

| Gate | Purpose |
|---|---|
| pytest + coverage | full suite with a required 100% line-coverage gate |
| Ruff | production and repository-tooling lint |
| Gitleaks | committed-secret detection |
| Bandit | static Python security checks |
| pip-audit | dependency vulnerability reporting |
| Docker build | reproducible hardened image build |
| eval-gate | retrieval, grounding and contradiction regression control |
| JSONL integrity | corpus structure and duplicate-id checks |

These controls reduce risk; they do not prove the absence of every defect and do
not constitute legal or security certification.

---

## 📚 Reviewer path

Read in this order:

1. [docs/REVIEWER_GUIDE.md](./docs/REVIEWER_GUIDE.md)
2. [docs/REVIEWER_DEMO.md](./docs/REVIEWER_DEMO.md)
3. [TEST_REPORT.md](./TEST_REPORT.md)
4. [docs/STATUS.md](./docs/STATUS.md)
5. [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md)
6. [docs/EVAL.md](./docs/EVAL.md)
7. [docs/GRANT_NLNET_SCOPE.md](./docs/GRANT_NLNET_SCOPE.md)

German-language entry points:

- [README.de.md](./README.de.md)
- [docs/de/REVIEWER_GUIDE.md](./docs/de/REVIEWER_GUIDE.md)
- [docs/de/QUICKSTART.md](./docs/de/QUICKSTART.md)
- [docs/de/GRANT_OVERVIEW.md](./docs/de/GRANT_OVERVIEW.md)

The pre-synchronization long-form README is preserved under
`docs/archive/grant-sync/README_PRE_SYNC_2026-07-30.md` for historical context.

---

## ⚖️ License and contribution

Crystal is licensed under **AGPL-3.0**. See [LICENSE](./LICENSE),
[CONTRIBUTING.md](./CONTRIBUTING.md), [GOVERNANCE.md](./GOVERNANCE.md),
[SECURITY.md](./SECURITY.md), and [PRIVACY.md](./PRIVACY.md).

> **📊 Canon = admitted truth** · **🔗 Provenance = trust** · **🏠 Local-first = control**
