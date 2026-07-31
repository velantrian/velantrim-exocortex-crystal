# 🔱 Velantrim ExoCortex — Crystal

> 🌐 🇬🇧 **English** · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 [Español](./README.es.md) · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 [Русский](./README.ru.md) · 🇨🇳 [简体中文](./README.zh-CN.md) · 🇸🇦 [العربية](./README.ar.md)   · 🇯🇵 [日本語](./README.ja.md) · 🇮🇳 [हिन्दी](./README.hi.md)
> 📚 [German documentation](./docs/de/README.md) · [Documentation française](./docs/fr/README.md) · [Documentación en español](./docs/es/README.md) · [Documentazione italiana](./docs/it/README.md) · [Документация на русском](./docs/ru/README.md) · [简体中文文档](./docs/zh-CN/README.md) · [التوثيق العربي](./docs/ar/README.md) · [日本語ドキュメント](./docs/ja/README.md) · [हिन्दी दस्तावेज़](./docs/hi/README.md)

### *Verifiable, local-first, open-source memory infrastructure for trustworthy AI*

`v0.3.0` · 🧪 **1713 passed / 12 skipped** · 🎯 **100% coverage** · 🐍 **pure-stdlib default runtime** · ⚖️ **AGPL-3.0** · 🔒 **local-first**

> Crystal is a verifiable memory layer, not another chatbot. Facts carry source,
> epistemic state and provenance metadata. Automatic admission into the canonical
> graph remains governed by Guardian + TruthGate.

> **Implementation truth:** GitHub `main`. The published audited implementation
> checkpoint is commit `cd6fd44` from merged PR #265. Exact verification evidence
> is maintained in [TEST_REPORT.md](./TEST_REPORT.md); newer corrective revisions
> remain subject to their own repository CI evidence.

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
→ admitted L3 graph memory
```

### Read-only query service

PR #265 introduced the strict HTTP boundary. The same service now defines the
supported installed CLI query commands and MCP search:

```text
HTTP POST /ask, GET /receipt
→ core.aio.arun()
→ core.query_pipeline.query()

velantrim ask / receipt
→ core.cli_entry
→ core.query_pipeline.query()

MCP search
→ core.mcp_server
→ core.query_pipeline.search()
```

For these surfaces, asking or searching does not ingest into L0/L1, transition
ESM, write L3 facts or edges, drain the outbox, record episode links, initialize
an unset embedding fingerprint, or mutate adaptive verification state.

MCP search is an inspection surface, not a strict-Canon assertion: it returns
explicit epistemic metadata and excludes processing-restricted rows before
returning stored claim/source content. Confident answers still require the
Guardian structural check and CanonicalView strict projection in `query()`.

### Explicit compatibility residual

The public guarantee is narrow and testable:

- `core.pipeline.run()` remains an admission-capable compatibility path;
- direct `python -m core.cli` or direct imports of `core.cli.main` preserve the
  historical module behaviour;
- the supported installed CLI surface is the `velantrim` console command routed
  through `core.cli_entry`.

Removing or renaming the legacy admitting path requires a separate deprecation
cycle. See [docs/architecture/read-only-query-boundary.md](./docs/architecture/read-only-query-boundary.md).

---

## 🧠 Memory model

| Layer | Role | Boundary |
|---|---|---|
| **L0** | in-process working cache | fast, rebuildable |
| **L1** | SQLite/WAL operational memory | states, restrictions, updates |
| **L2** | pending and curator-review path | not automatically canonical |
| **L3** | graph-backed memory | automatic admission only through TruthGate |
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
conflict lookup and receipt verification. It has no canonical write tool. Search
uses the zero-durable-mutation service and does not initialize an unset embedding
fingerprint merely because a client searched memory.

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

Localized reviewer paths:

- 🇩🇪 [German reviewer guide](./docs/de/REVIEWER_GUIDE.md) · [Quickstart](./docs/de/QUICKSTART.md) · [Grant overview](./docs/de/GRANT_OVERVIEW.md)
- 🇫🇷 [Guide reviewer français](./docs/fr/REVIEWER_GUIDE.md) · [Démarrage rapide](./docs/fr/QUICKSTART.md) · [Vue subvention](./docs/fr/GRANT_OVERVIEW.md)
- 🇪🇸 [Guía para reviewers](./docs/es/REVIEWER_GUIDE.md) · [Inicio rápido](./docs/es/QUICKSTART.md) · [Resumen de subvención](./docs/es/GRANT_OVERVIEW.md)
- 🇮🇹 [Guida per reviewer](./docs/it/REVIEWER_GUIDE.md) · [Avvio rapido](./docs/it/QUICKSTART.md) · [Panoramica della sovvenzione](./docs/it/GRANT_OVERVIEW.md)
- 🇷🇺 [Руководство reviewer](./docs/ru/REVIEWER_GUIDE.md) · [Быстрый старт](./docs/ru/QUICKSTART.md) · [Обзор гранта](./docs/ru/GRANT_OVERVIEW.md)
- 🇨🇳 [Reviewer 指南](./docs/zh-CN/REVIEWER_GUIDE.md) · [快速开始](./docs/zh-CN/QUICKSTART.md) · [Grant 概览](./docs/zh-CN/GRANT_OVERVIEW.md)
- 🇸🇦 [دليل المراجع](./docs/ar/REVIEWER_GUIDE.md) · [البدء السريع](./docs/ar/QUICKSTART.md) · [نظرة عامة على المنحة](./docs/ar/GRANT_OVERVIEW.md)
- 🇯🇵 [日本語 reviewer guide](./docs/ja/REVIEWER_GUIDE.md) · [クイックスタート](./docs/ja/QUICKSTART.md) · [Grant 概要](./docs/ja/GRANT_OVERVIEW.md)
- 🇮🇳 [हिन्दी reviewer guide](./docs/hi/REVIEWER_GUIDE.md) · [Quickstart](./docs/hi/QUICKSTART.md) · [Grant overview](./docs/hi/GRANT_OVERVIEW.md)

The pre-synchronization long-form README is preserved under
`docs/archive/grant-sync/README_PRE_SYNC_2026-07-30.md` for historical context.

---

## ⚖️ License and contribution

Crystal is licensed under **AGPL-3.0**. See [LICENSE](./LICENSE),
[CONTRIBUTING.md](./CONTRIBUTING.md), [GOVERNANCE.md](./GOVERNANCE.md),
[SECURITY.md](./SECURITY.md), and [PRIVACY.md](./PRIVACY.md).

> **📊 Canon = admitted truth** · **🔗 Provenance = trust** · **🏠 Local-first = control**

---

> 🌐 🇬🇧 **English** · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 [Español](./README.es.md) · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 [Русский](./README.ru.md) · 🇨🇳 [简体中文](./README.zh-CN.md) · 🇸🇦 [العربية](./README.ar.md) · 🇯🇵 [日本語](./README.ja.md) · 🇮🇳 [हिन्दी](./README.hi.md)