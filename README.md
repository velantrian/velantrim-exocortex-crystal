# 🔱 Velantrim ExoCortex — Crystal

> 🌐 🇬🇧 **English** · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 [Español](./README.es.md) · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 [Русский](./README.ru.md) · 🇨🇳 [简体中文](./README.zh-CN.md) · 🇸🇦 [العربية](./README.ar.md) · 🇯🇵 [日本語](./README.ja.md) · 🇮🇳 [हिन्दी](./README.hi.md)

### Verifiable, local-first memory infrastructure for trustworthy AI systems

`v0.3.0` · 🧪 **2047 passed / 12 skipped** · 🎯 **100.00% coverage** · 🧬 **7/7 declared mutants killed** · ✅ **9 CI jobs** · 🐍 **pure-standard-library default runtime** · ⚖️ **AGPL-3.0**

**Verified runtime checkpoint:** `c612c1f7de067b05ed7d01ad82d47a7bc39af23a` — merged PR #330.  
**Validated implementation head / CI:** `e70c31bf517039f0dd3f77f7bc4b6d3f03936736` / `31213056560` — 9/9 successful.

Crystal is a memory, evidence and decision boundary. It records what a claim is, where it
came from, what epistemic state it is in, whether it may ground an answer, and how a
contradiction was explicitly resolved.

> **Documentation language policy:** English is the authoritative actively maintained
> GitHub documentation language during engineering. Existing localized READMEs are frozen
> snapshots and may lag until a dedicated final reconciliation pass.

## 🎯 Current verified baseline

Crystal currently provides:

- typed claims, provenance, evidence spans and an explicit epistemic lifecycle;
- Guardian and TruthGate admission boundaries;
- physical L3 multi-status storage separated from strict Canon;
- immutable deny-dominant `TrustSnapshot` and `CanonicalView` reads;
- read-only public HTTP, CLI and MCP query paths;
- TRACE, replayable receipts, restriction, erasure and audit controls;
- explicit contradiction reports and authorized `COEXIST`, `CONTEXTUALIZE` and
  `SUPERSEDE` decisions;
- scoped curator roles/capabilities with process-local decision leases;
- a durable storage-profile lock;
- verified SQLite backup, independent verification, inactive restore and guarded
  stale-lock recovery;
- deterministic SQLite logical export and independent bundle verification.

```text
explicit ingest
→ Guardian
→ TruthGate
→ physical L3 multi-status storage
→ immutable TrustSnapshot
→ strict CanonicalView
→ grounded answer or bounded refusal
→ replayable Receipt
```

## 🗃️ Storage profiles and migration boundary

```text
SQLite
  = verified local-first/lightweight default

PostgreSQL + pgvector
  = proposed optional institutional profile
  = not current runtime
```

PR #330 adds a canonical backend-neutral JSONL export for nodes, vectors, edges, entities,
mentions and metadata, plus independent fail-closed verification. The bundle is operation
evidence only: it is not claim evidence, TruthGate admission or backend activation.

The merged implementation has an explicit local-first resource envelope:

| Resource | Limit |
|---|---:|
| profile/control JSON | 1 MiB |
| source SQLite file | 64 MiB |
| one canonical record | 1 MiB |
| records per dataset | 200,000 |
| one dataset | 64 MiB |
| aggregate JSONL | 384 MiB |

This is not a streaming or institution-scale migration engine. Issue #331 tracks bounded
cursor batching, incremental verification and disk-backed referential checks. Issue #332
tracks future inactive PostgreSQL/pgvector import and exact-state equivalence. Cutover,
rollback, dual-write and automatic backend switching remain absent.

## 🛡️ Central non-claims

```text
physical L3           != strict Canon
retrieval score       != evidence
model output          != independent source
migration receipt     != claim evidence
successful verify     != activation
backend availability  != backend selection
```

Crystal does not claim universal truth detection, zero hallucinations, production
multi-tenancy, distributed exactly-once behavior, legal/GDPR/security certification,
PostgreSQL runtime, Titan integration or artificial consciousness.

## 🚀 Quick start

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
```

## 📚 Evidence and navigation

- [Verification report](./TEST_REPORT.md)
- [Current status](./docs/STATUS.md)
- [Implementation matrix](./docs/IMPLEMENTATION_STATUS.md)
- [Machine-readable manifest](./docs/status/implementation-manifest.json)
- [Architecture](./docs/ARCHITECTURE.md)
- [Reviewer guide](./docs/REVIEWER_GUIDE.md)
- [AI-agent entry point](./docs/ai/README.md)
- [Current AI context](./docs/ai/CURRENT_STATE.md)
- [Known risks](./docs/ai/KNOWN_RISKS.md)
- [NLnet scope](./docs/GRANT_NLNET_SCOPE.md)
- [Baseline → funded-delta matrix](./docs/grants/baseline-funded-delta-matrix.md)
- [Roadmap](./ROADMAP.md)
- [Security policy](./SECURITY.md)

## 🎓 Grant status

The NLnet application is submitted and under review. No award or budget change is claimed.
Already merged baseline functionality must not be counted again as future funded delivery.
