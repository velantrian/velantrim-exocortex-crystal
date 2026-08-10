# 🔱 Velantrim ExoCortex — Crystal

> 🌐 🇬🇧 [English](./README.md) · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 **Français** · 🇪🇸 [Español](./README.es.md) · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 [Русский](./README.ru.md) · 🇨🇳 [简体中文](./README.zh-CN.md) · 🇸🇦 [العربية](./README.ar.md) · 🇯🇵 [日本語](./README.ja.md) · 🇮🇳 [हिन्दी](./README.hi.md)

<!-- localization-source: main@6b45bdd196eb42dea7bc30f58d69799b4b1712f2 -->
<!-- localization-status: CURRENT -->

### Infrastructure local-first vérifiable de mémoire, d’évidence et de décision pour des systèmes d’IA fiables

`v0.3.0` · 🧪 **2078 passed / 13 skipped / 0 failed** · 🎯 **9756 statements / 100.00% line coverage** · 🧬 **7/7 Ring Zero mutants killed** · ✅ **9 CI jobs** · 🐍 runtime stdlib-only par défaut · ⚖️ **AGPL-3.0**

> Crystal n’est ni un chatbot ni un oracle autonome de vérité. C’est une boundary de mémoire, d’evidence et de décision qui conserve la provenance, l’état épistémique, l’autorisation de grounding et les décisions de contradiction auditées.

**Verified runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6` — PR #337.  
**Reader foundation:** le skeleton RC-1 evidence-linked et la RC-2 caller-supplied Structural Document Map sont implémentés/testés; le Reader multi-pass dédié ne l’est pas.  
**Grant:** `submitted / under review / not awarded`.  
**Evidence:** [TEST_REPORT.md](./TEST_REPORT.md), [STATUS.md](./docs/STATUS.md), [implementation manifest](./docs/status/implementation-manifest.json).

> L’anglais reste la source primaire et résout les divergences. Cette version est une présentation publique complète, pas un résumé réduit. Voir [docs/LOCALIZATION_POLICY.md](./docs/LOCALIZATION_POLICY.md) et [docs/TRANSLATION_STATUS.md](./docs/TRANSLATION_STATUS.md).

---

## 🎯 Pourquoi Crystal existe

Les systèmes AI/RAG mélangent souvent documents, déclarations utilisateur, model output, hypothèses et mémoire. Un texte fluide peut alors acquérir une autorité que son evidence ne justifie pas.

```text
fluent claim        != trusted fact
physical L3         != strict Canon
retrieval score     != evidence
model output        != independent source truth
migration receipt   != claim evidence
import success      != backend activation
Reader coverage     != comprehension proof
Reader structure    != truth/confidence authority
```

## 🧠 Ce que Crystal fournit

- claims typés et lifecycle épistémique explicite;
- source identity, evidence spans et provenance;
- Guardian et TruthGate comme admission boundaries;
- physical L3 multi-status distinct du strict Canon;
- TrustSnapshot et CanonicalView deny-dominant;
- HTTP /ask, CLI ask et MCP search read-only;
- TRACE et Receipts replayables/tamper-evident;
- review queue/session et ContradictionReport;
- décisions COEXIST / CONTEXTUALIZE / SUPERSEDE;
- curator capabilities scoped et leases process-local;
- lifecycle SQLite et migration logique bornée;
- import PostgreSQL/pgvector optionnel et inactif avec `active=false`;
- RC-1: source/version/session, SegmentCard, fidelity, coverage, bookmarks/open loops, stale/failure/privacy;
- RC-2: structure caller-supplied liée à la version avec RECOVERED / AMBIGUOUS / UNSUPPORTED.

RC-1/RC-2 ne stockent pas le source body, n’ajoutent ni API/CLI/worker Reader ni schéma durable Reader et n’ont aucune autorité Canon/ESM/planner. Il n’y a pas de parser/OCR automatique, d’orchestration LLM/provider Reader, d’embeddings/ANN/vector DB ni de runtime multi-pass/cross-document.

## 🏛️ Architecture en trois vues

### 🧠 Mind map

```text
🧠 Crystal
├── 📖 Reader foundation
│   ├── RC-1 evidence-linked skeleton
│   ├── RC-2 Structural Document Map
│   └── dedicated multi-pass Reader — NOT IMPLEMENTED
├── 🏛️ Memory
│   ├── L0 — working cache
│   ├── L1 — operational SQLite/WAL
│   ├── L2 — pending/review
│   └── L3 — physical multi-status graph
├── 🛡️ Trust
│   ├── Guardian
│   ├── TruthGate
│   ├── TrustSnapshot
│   └── CanonicalView
└── 🗄️ Storage
    ├── SQLite — active local-first
    └── PostgreSQL/pgvector — inactive active=false
```

### 🏗️ Flux d’information

```text
Source / document
      ↓
RC-1 Reader artifacts
      ↓
RC-2 structural metadata
      ↓
explicit ingest / review
      ↓
Guardian → TruthGate
      ↓
L1 + physical L3
      ↓
TrustSnapshot → CanonicalView STRICT
      ↓
Grounded answer / bounded refusal
      ↓
TRACE + Receipt
```

### 🌳 Arbre des modules

```text
🌳 core
├── reader_core.py       # RC-1
├── reader_structure.py  # RC-2
├── evidence.py
├── truth_gate.py
├── pipeline.py
├── query_pipeline.py
└── storage/...
```

## 🧱 Surfaces mémoire et authority

| Surface | Rôle | Limite |
|---|---|---|
| Reader RC-1 | source-linked artifacts | candidate ≠ truth |
| Reader RC-2 | structural map | order ≠ authority |
| L0 | working cache | ephemeral |
| L1 | operational state | durable |
| L2 | review/pending | pas d’admission automatique |
| L3 | physical graph | multi-status |
| TrustSnapshot | reconciliation | deny-dominant |
| CanonicalView | grounding | policy-allowed only |
| TRACE / Receipt | audit/replay | evidence, pas truth generator |
| ContradictionReport | conflit | pas de winner automatique |

## 🗄️ SQLite et PostgreSQL/pgvector

```text
SQLite
└── ordinary active local-first runtime
    ├── reads/writes
    ├── backup/restore
    └── bounded logical export

PostgreSQL 16 + pgvector
└── optional inactive target
    ├── explicit optional dependency
    ├── SERIALIZABLE import
    ├── exact target re-hash
    └── active=false
```

Un import réussi n’implique pas activation, cutover, rollback, dual-write, automatic switching, ANN acceptance ou TruthGate admission. L’adapter PostgreSQL normal n’est pas actif.

## 🔎 Crystal face au RAG classique

| Question | Classic RAG | Crystal |
|---|---|---|
| Trouver du contenu | force principale | adapters |
| Claim vs trusted fact | app-specific | typed boundary |
| Provenance | variable | first-class |
| Reader structure/coverage | chunk-centric | RC-1/RC-2 foundation |
| Bloquer model self-source | non inhérent | Ring Zero |
| Contradictions | logique externe | explicit dispositions |
| Replay evidence | optional | TRACE / Receipt |
| Cloud/model obligatoire | variable | non par défaut |

## 🛡️ Query boundary read-only

```text
HTTP /ask
CLI ask
MCP search
     ↓
core.query_pipeline.query()
     ↓
strict read-only canonical projection
```

Ces surfaces ne créent pas de faits, ne mutent pas ESM et n’écrivent pas L3. Explicit ingest reste le write path séparé.

## ⚖️ Décisions de contradiction

```text
unresolved contradiction
        ↓
ContradictionReport
        ↓
scoped curator + capability + lease
        ↓
COEXIST / CONTEXTUALIZE / SUPERSEDE
        ↓
audited canonical write path
```

## 🚀 Démarrage rapide

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
```

Option PostgreSQL: `pip install -e '.[postgresql]'`.

## ✅ Baseline vérifiée

```text
Runtime checkpoint: bbd816c09dd39a02e6de6c1014438490572f40f6
Python 3.11/3.12: 2078 passed / 13 skipped / 0 failed
Statements: 9756
Coverage: 100.00%
CI: 9/9
Ring Zero: 7/7
reader_core_rc1_skeleton = true
reader_core_rc2_structural_map = true
dedicated_reader_core = false
PostgreSQL target: active=false
```

## 🚧 Non-claims

Crystal ne revendique ni universal truth, zero hallucinations, AGI/consciousness, certification legal/GDPR/security, production multi-tenancy, coordination distributed exactly-once, runtime PostgreSQL actif, automatic switching/cutover/rollback/dual-write, parsing Reader automatique, stack embeddings/ANN/vector Reader, ni completed dedicated multi-pass Reader Core.

NLnet reste **submitted / under review / not awarded**; environ €50,000 reste planning only, budget change none. Le travail merged avant accord reste baseline.

## 📚 Navigation

- [Documentation map](./docs/DOCUMENTATION_MAP.md)
- [Quick Start](./docs/QUICKSTART.md)
- [Status](./docs/STATUS.md)
- [Implementation Status](./docs/IMPLEMENTATION_STATUS.md)
- [Reader architecture](./docs/architecture/READER_CORE_ARCHITECTURE.md)
- [Localization policy](./docs/LOCALIZATION_POLICY.md)
- [Translation status](./docs/TRANSLATION_STATUS.md)
- [Security](./SECURITY.md)
- [Governance](./GOVERNANCE.md)
- [Contributing](./CONTRIBUTING.md)

## 🤝 Contribution et licence

Toute modification doit préserver les authority boundaries, les tests/coverage et la précision des claims. Voir [CONTRIBUTING.md](./CONTRIBUTING.md). Licence: [AGPL-3.0](./LICENSE).
