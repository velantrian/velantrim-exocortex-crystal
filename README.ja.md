# 🔱 Velantrim ExoCortex — Crystal

> 🌐 🇬🇧 [English](./README.md) · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 [Español](./README.es.md) · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 [Русский](./README.ru.md) · 🇨🇳 [简体中文](./README.zh-CN.md) · 🇸🇦 [العربية](./README.ar.md) · 🇯🇵 **日本語** · 🇮🇳 [हिन्दी](./README.hi.md)

<!-- localization-source: main@6b45bdd196eb42dea7bc30f58d69799b4b1712f2 -->
<!-- localization-status: CURRENT -->

### 信頼できるAIシステムのための、検証可能な local-first メモリ・evidence・意思決定インフラ

`v0.3.0` · 🧪 **2078 passed / 13 skipped / 0 failed** · 🎯 **9756 statements / 100.00% line coverage** · 🧬 **7/7 Ring Zero mutants killed** · ✅ **9 CI jobs** · 🐍 stdlib-only default runtime · ⚖️ **AGPL-3.0**

> Crystal はチャットボットでも自律的な「真実のオラクル」でもありません。claim の由来、epistemic state、grounding 可否、矛盾に対する監査可能な決定を扱う memory/evidence/decision boundary です。

**Verified runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6` — PR #337.  
**Reader foundation:** RC-1 evidence-linked skeleton と RC-2 caller-supplied Structural Document Map は実装・テスト済み。dedicated multi-pass Reader は未実装です。  
**Grant:** `submitted / under review / not awarded`.  
**Evidence:** [TEST_REPORT.md](./TEST_REPORT.md), [STATUS.md](./docs/STATUS.md), [implementation manifest](./docs/status/implementation-manifest.json).

> 不一致がある場合、英語版が一次ソースです。この README は短い orientation ではなく、完全な公開プレゼンテーションです。[docs/LOCALIZATION_POLICY.md](./docs/LOCALIZATION_POLICY.md) と [docs/TRANSLATION_STATUS.md](./docs/TRANSLATION_STATUS.md) を参照してください。

---

## 🎯 Crystal が必要な理由

多くの AI/RAG システムは、文書、ユーザー発言、model output、hypothesis、memory を同じコンテキストに混在させます。その結果、流暢な文章が evidence に裏付けられない authority を得ることがあります。

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

## 🧠 Crystal が提供するもの

- typed claims と明示的な epistemic lifecycle;
- source identity, evidence spans, provenance;
- admission boundaries としての Guardian / TruthGate;
- strict Canon と分離された multi-status physical L3;
- deny-dominant TrustSnapshot / CanonicalView;
- read-only HTTP /ask, CLI ask, MCP search;
- TRACE と replayable tamper-evident Receipts;
- review queue/session と ContradictionReport;
- COEXIST / CONTEXTUALIZE / SUPERSEDE の明示的決定;
- scoped curator capabilities と process-local leases;
- SQLite lifecycle と bounded logical migration;
- `active=false` の optional PostgreSQL/pgvector inactive import;
- RC-1: source/version/session, SegmentCard, fidelity, coverage, bookmarks/open loops, stale/failure/privacy;
- RC-2: RECOVERED / AMBIGUOUS / UNSUPPORTED を持つ version-bound caller-supplied structure。

RC-1/RC-2 は source body を保持せず、Reader API/CLI/worker や durable Reader schema を追加せず、Canon/ESM/planner authority を持ちません。automatic parser/OCR、Reader LLM/provider orchestration、embeddings/ANN/vector DB、multi-pass/cross-document runtime はありません。

## 🏛️ 3つのアーキテクチャビュー

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

### 🏗️ 情報フロー

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

### 🌳 モジュールツリー

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

## 🧱 Memory / authority surface

| Surface | Role | Boundary |
|---|---|---|
| Reader RC-1 | source-linked artifacts | candidate ≠ truth |
| Reader RC-2 | structural map | order ≠ authority |
| L0 | working cache | ephemeral |
| L1 | operational state | durable |
| L2 | review/pending | automatic admission なし |
| L3 | physical graph | multi-status |
| TrustSnapshot | reconciliation | deny-dominant |
| CanonicalView | grounding | policy-allowed only |
| TRACE / Receipt | audit/replay | evidence, not truth generator |
| ContradictionReport | conflict object | automatic winner なし |

## 🗄️ SQLite と PostgreSQL/pgvector

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

import success は activation、cutover、rollback、dual-write、automatic switching、ANN acceptance、TruthGate admission を意味しません。通常の PostgreSQL runtime adapter は active ではありません。

## 🔎 Classic RAG との比較

| Question | Classic RAG | Crystal |
|---|---|---|
| 関連資料の検索 | 主機能 | adapters |
| claim vs trusted fact | app-specific | typed boundary |
| provenance | 可変 | first-class |
| Reader structure/coverage | chunk-centric | RC-1/RC-2 foundation |
| model self-source 防止 | inherent ではない | Ring Zero |
| contradiction | 外部ロジック | explicit dispositions |
| evidence replay | optional | TRACE / Receipt |
| cloud/model 必須 | varies | default runtime では不要 |

## 🛡️ Read-only query boundary

```text
HTTP /ask
CLI ask
MCP search
     ↓
core.query_pipeline.query()
     ↓
strict read-only canonical projection
```

これらは fact を作成せず、ESM を変更せず、L3 に書き込みません。Explicit ingest は独立した write path です。

## ⚖️ Contradiction decisions

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

## 🚀 Quick start

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
```

Optional PostgreSQL: `pip install -e '.[postgresql]'`.

## ✅ Verified baseline

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

Crystal は universal truth、zero hallucinations、AGI/consciousness、legal/GDPR/security certification、production multi-tenancy、distributed exactly-once、active PostgreSQL runtime、automatic switching/cutover/rollback/dual-write、automatic Reader parsing、embeddings/ANN/vector Reader stack、completed dedicated multi-pass Reader Core を主張しません。

NLnet は **submitted / under review / not awarded**。約 €50,000 は planning only、budget change none。agreement 前に merged された仕事は baseline です。

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

## 🤝 Contributing / License

変更は authority boundaries、tests/coverage、正確な claims を維持する必要があります。[CONTRIBUTING.md](./CONTRIBUTING.md) を参照してください。License: [AGPL-3.0](./LICENSE).
