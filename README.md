# 🔱 Velantrim ExoCortex — Crystal

> 🌐 🇬🇧 **English** · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 [Español](./README.es.md) · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 [Русский](./README.ru.md) · 🇨🇳 [简体中文](./README.zh-CN.md) · 🇸🇦 [العربية](./README.ar.md) · 🇯🇵 [日本語](./README.ja.md) · 🇮🇳 [हिन्दी](./README.hi.md)

### Verifiable, local-first memory infrastructure for trustworthy AI systems

`v0.3.0` · 🧪 **2078 passed / 13 skipped** · 🎯 **100.00% coverage** · 🧬 **7/7 declared mutants killed** · ✅ **9 permanent CI jobs** · 🐘 **real PostgreSQL/pgvector integration** · 🐍 **pure-standard-library default runtime** · ⚖️ **AGPL-3.0**

**Verified runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6` — merged PR #337.  
**Validated head / CI:** `d7af7c80722274f9217bc5545d150f92e9363f37` / `31256316536` — 9/9 successful.  
**PostgreSQL integration:** `31256316532` — successful against PostgreSQL 16 and pgvector 0.8.2.

Crystal separates physical memory, evidence, epistemic admission and trusted reads. Storage
presence, retrieval score or migration success cannot bypass Guardian, TruthGate or strict
Canon reconciliation.

> **Documentation language policy:** English is the sole authoritative working language for
> engineering, architecture, status, security, grant and AI-agent documentation. Localized
> READMEs are concise, non-authoritative orientation summaries derived from a recorded English
> checkpoint; they are not full mirrors of the documentation corpus. See the
> [localization policy](./docs/LOCALIZATION_POLICY.md).

## 🎯 Current verified baseline

- typed claims, provenance, evidence spans and explicit epistemic states;
- Guardian and TruthGate admission boundaries;
- physical L3 separated from immutable `TrustSnapshot` / `CanonicalView` reads;
- read-only public HTTP, CLI and MCP query paths;
- TRACE, receipts, restrictions, erasure and contradiction decisions;
- durable storage-profile identity;
- SQLite backup, independent verification, inactive restore and lock recovery;
- bounded-streaming SQLite logical export and independent bundle verification;
- optional, lazy-loaded PostgreSQL/pgvector inactive import and independent exact-state
  equivalence for the approved bundle datasets.

## 🗃️ Storage and migration boundary

```text
SQLite
  = verified local-first/lightweight default
  = ordinary current storage profile

PostgreSQL + pgvector
  = optional institutional migration target
  = inactive import/equivalence tooling implemented
  = not selected by ordinary runtime composition
  = not an active read/write backend
```

```text
verified SQLite logical bundle
→ PostgreSQL preflight
→ new inactive target schema
→ serializable import
→ independent read-only canonical re-hash
→ exact count / byte / SHA-256 equivalence
→ non-secret receipts
```

The driver is installed only through `[postgresql]` and loaded only by explicit operator
commands. The default installation remains pure standard library. Production credentials
and credential-bearing connection strings must not enter profiles, bundles, receipts,
application logs, issues or Notion.

Successful import is operational evidence only. It is not activation, ordinary runtime
availability, claim evidence, TruthGate admission or strict Canon membership. The target
remains `active=false` and cannot serve normal reads or writes.

Issue #331 was implemented by PR #335. Issue #332 was implemented by PR #337 and is now
merged baseline. Still separate: exact-vs-ANN evaluation, cutover/fencing, rollback,
PostgreSQL backup/restore/upgrade lifecycle, production pooling/IdP/multi-tenancy and
distributed coordination.

## 🛡️ Central non-claims

```text
physical L3          != strict Canon
retrieval score      != evidence
migration receipt    != claim evidence
successful import    != activation
backend availability != backend selection
```

Crystal does not claim universal truth, zero hallucinations, an active PostgreSQL runtime
backend, production multi-tenancy, distributed exactly-once behavior, legal/GDPR/security
certification, Titan integration or artificial consciousness.

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

## 📚 Evidence and navigation

- [Verification report](./TEST_REPORT.md)
- [Current status](./docs/STATUS.md)
- [Implementation matrix](./docs/IMPLEMENTATION_STATUS.md)
- [Machine-readable manifest](./docs/status/implementation-manifest.json)
- [Documentation map](./docs/DOCUMENTATION_MAP.md)
- [Localization policy](./docs/LOCALIZATION_POLICY.md)
- [Inactive PostgreSQL import contract](./docs/architecture/POSTGRESQL_INACTIVE_IMPORT.md)
- [PostgreSQL/pgvector RFC](./docs/architecture/POSTGRESQL_PGVECTOR_PROFILE_RFC.md)
- [Current AI context](./docs/ai/CURRENT_STATE.md)
- [Known risks](./docs/ai/KNOWN_RISKS.md)
- [NLnet scope](./docs/GRANT_NLNET_SCOPE.md)
- [Baseline → funded-delta matrix](./docs/grants/baseline-funded-delta-matrix.md)
- [Roadmap](./ROADMAP.md)
- [Security policy](./SECURITY.md)

## 🎓 Grant status

The NLnet application is submitted and under review. No award or budget change is claimed.
Merged PR #337 cannot be counted again as future funded delivery.
