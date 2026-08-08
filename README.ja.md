# 🔱 Velantrim ExoCortex — Crystal

> 🌐 🇬🇧 [English](./README.md) · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 [Español](./README.es.md) · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 [Русский](./README.ru.md) · 🇨🇳 [简体中文](./README.zh-CN.md) · 🇸🇦 [العربية](./README.ar.md) · 🇯🇵 **日本語** · 🇮🇳 [हिन्दी](./README.hi.md)

<!-- localization-source: main@e521440e9bb188d88475f17dd5bcdd161b314605 -->
<!-- localization-status: IN_PROGRESS -->

### 信頼できる AI システムのための、検証可能で local-first な記憶・証拠・意思決定インフラストラクチャ

`v0.3.0` · 🧪 **2078 passed / 13 skipped / 0 failed** · 🎯 **9756 statements / 100.00% line coverage** · 🧬 **宣言済み Ring Zero mutants 7/7 を排除** · ✅ **恒久 CI jobs 9 個** · 🐍 **既定 runtime は Python 標準ライブラリのみ** · ⚖️ **AGPL-3.0**

> Crystal は別のチャットボットでも、自律的な「真実の神託」でもありません。claim が何であるか、どこから来たか、どの epistemic state にあるか、回答を根拠づけられるか、矛盾が明示的かつ監査可能な決定でどう処理されたかを記録する、記憶・証拠・意思決定の境界です。

**検証済み runtime checkpoint：** `bbd816c09dd39a02e6de6c1014438490572f40f6` — merged PR #337。  
**検証済み head / CI：** `d7af7c80722274f9217bc5545d150f92e9363f37` / `31256316536` — 9/9 successful。  
**PostgreSQL integration：** `31256316532` — PostgreSQL 16 + pgvector 0.8.2。  
**一次証拠：** [TEST_REPORT.md](./TEST_REPORT.md)、[STATUS.md](./docs/STATUS.md)、[machine-readable manifest](./docs/status/implementation-manifest.json)。

> **翻訳契約：** この README は短い要約ではなく、英語版と同等の視覚的・意味的カバレッジを目標にしています。英語は主要な作業・競合解決ソースです。他の安定文書は段階的に翻訳します。[Localization policy](./docs/LOCALIZATION_POLICY.md) と [Translation status](./docs/TRANSLATION_STATUS.md) を参照してください。

---

## 🎯 Crystal が必要な理由

多くの AI システムは、ソース文書、ユーザー発言、モデル出力、仮説、retrieval 断片、永続記憶を同じ context や vector store に混在させます。境界が明示されないと、流暢な文章が証拠以上の権威を得てしまいます。

```text
流暢な claim は自動的に信頼されない。
physical graph node は自動的に strict Canon にならない。
retrieval score は evidence ではない。
model output は独立した事実ソースではない。
contradiction は自分で勝者を選ばない。
TopicFacet label は真実の判定ではない。
successful import は backend activation ではない。
```

## 🧠 Crystal が提供するもの

- typed claims と明示的 epistemic lifecycle；
- source identity、exact evidence spans、provenance；
- Guardian / TruthGate admission boundaries；
- strict Canon から分離された multi-status physical L3 graph；
- immutable deny-dominant `TrustSnapshot`；
- read-only の HTTP、CLI、MCP query surfaces；
- TRACE と replayable tamper-evident Receipts；
- restriction、erasure、audit、import sessions；
- review queues と resumable review sessions；
- immutable `ContradictionReport`；
- `COEXIST`、`CONTEXTUALIZE`、`SUPERSEDE`；
- scoped curator capabilities と process-local decision leases；
- truth authority を持たない advisory TopicFacet；
- deterministic evaluation、100% line coverage、Ring Zero mutation gate；
- 検証済み SQLite backup/restore と bounded logical migration；
- optional inactive PostgreSQL/pgvector import と independent exact-state equivalence。

## 🏛️ 3 つのアーキテクチャビュー

### 🧠 マインドマップ

```text
🧠 Crystal
├── 🎯 目的
│   ├── AI のための検証可能な記憶
│   ├── local-first trust infrastructure
│   └── evidence に結びついた回答と決定
├── 🏛️ Memory
│   ├── L0 — 高速 working cache
│   ├── L1 — operational state / lifecycle
│   ├── L2 — waiting / review boundary
│   └── L3 — physical multi-status graph
├── 🛡️ Trust
│   ├── Guardian
│   ├── TruthGate
│   ├── TrustSnapshot
│   └── CanonicalView
├── 📜 Evidence
│   ├── source + exact span
│   ├── provenance
│   ├── TRACE
│   └── Receipt
├── ⚖️ Contradiction
│   ├── review queue / session
│   ├── ContradictionReport
│   └── COEXIST / CONTEXTUALIZE / SUPERSEDE
├── 🗄️ Storage
│   ├── SQLite — 通常の local-first profile
│   └── PostgreSQL/pgvector — inactive target
└── 📊 Verification
    ├── Python 3.11 / 3.12
    ├── 100% coverage
    ├── mutation / security / Docker
    └── exact-head CI evidence
```

### 🏗️ 情報フロー

```text
📥 explicit ingest
        ↓
🧾 claim type + source + exact evidence span
        ↓
🧠 observed state in L0/L1
        ↓
🛡️ Guardian → ⚖️ TruthGate → 🚧 restrictions
        ↓                         ↓
⏳ L2 review               🏛️ physical L3 graph
        └──────────────┬──────────┘
                       ↓
             📐 immutable TrustSnapshot
                       ↓
          🛡️ Guardian + CanonicalView STRICT
                  ↓                 ↓
          💬 grounded answer      🚫 grounded refusal
                  ↓
             🧾 replayable Receipt
```

### 🌳 モジュールツリー

```text
🌳 Crystal
├── 🧠 Memory：L0 / L1 / L2 / L3
├── 🛡️ Trust：Guardian / TruthGate / TrustSnapshot / CanonicalView
├── 📜 Evidence：Source / Span / Provenance / TRACE / Receipt
├── ⚖️ Review：Queue / Session / ContradictionReport / Disposition
├── 🔎 Query：HTTP / CLI / MCP
├── 🗄️ Portability：SQLite lifecycle / logical bundle / inactive PostgreSQL import
└── 📊 Verification：tests / coverage / mutation / security / Docker / docs-status
```

## 🧭 中心的な区別

```text
physical L3 graph    != strict Canon
query                != ingest
confidence           != independent evidence
LLM output           != independent factual source
contradiction detect != automatic winner
TopicFacet relevance != truth
migration receipt    != claim evidence
successful import    != backend activation
process-local lease  != distributed coordination
```

TruthGate は admission policy gate であり、客観的真実を自律的に知る oracle ではありません。Strict Canon は evidence、status、ESM state、confidence shape、processing restrictions に基づく policy-allowed read projection です。

## 🧱 記憶と証拠のサーフェス

| Surface | 役割 | 重要な境界 |
|---|---|---|
| L0 | process 内 working cache | 高速で再構築可能 |
| L1 | SQLite/WAL operational memory | lifecycle、restrictions |
| L2 | logical review boundary | 自動的に Canon ではない |
| L3 | physical multi-status memory | 存在 ≠ 信頼 |
| TrustSnapshot | immutable reconciliation | deny-dominant resolution |
| CanonicalView | strict grounding projection | policy-allowed reads のみ |
| TRACE / Receipt | proof と replay | grounding、drift、tamper evidence |
| ContradictionReport | immutable conflict | confidence は勝者を選ばない |
| TopicFacet | navigation | truth / ESM / Canon を変更しない |

## 🗄️ SQLite と PostgreSQL/pgvector

```text
SQLite
└── 現在の通常 local-first runtime profile
    ├── reads / writes
    ├── backup / restore
    ├── lock recovery
    └── bounded canonical logical export

PostgreSQL 16 + pgvector
└── optional migration / equivalence profile
    ├── optional [postgresql] extra
    ├── lazy driver loading
    ├── new target schema
    ├── active=false
    ├── SERIALIZABLE import
    └── independent count / byte / SHA-256 equivalence
```

PostgreSQL target は通常の runtime composition に存在せず、通常の reads/writes を提供できません。import 成功は activation、automatic selection、cutover、rollback、dual-write、TruthGate admission、strict Canon membership、ANN acceptance、production multi-tenancy を意味しません。

## 🔎 Crystal と従来の RAG

| 質問 | 従来の RAG | Crystal |
|---|---|---|
| 関連資料を見つける | 主な強み | retrieval adapters |
| user claim と verified fact を分ける | application-specific | explicit typed boundary |
| lifecycle と矛盾を追跡 | 外部ロジックが多い | first-class states / reports |
| 生成テキストが自己ソースになるのを防ぐ | 非内在 | Ring Zero invariant |
| 回答の証拠を再現 | 任意 | TRACE / Receipt |
| 矛盾を説明責任付きで解決 | application-specific | authorized dispositions |
| 必須 cloud/model provider なしで動作 | 実装次第 | pure-stdlib local-first baseline |

## 🛡️ 公開 read-only 境界

`HTTP /ask`、`HTTP /receipt`、`CLI ask`、`CLI receipt`、`MCP search` は `core.query_pipeline` を共有します。facts を作成せず、ESM state を変更せず、L3 に書き込まず、Canon を変更しません。

## ⚖️ 明示的な矛盾決定

```bash
python -m core.conflict_surfaces FACT_ID \
  --disposition COEXIST \
  --actor alice \
  --reason "claims describe different contexts" \
  --expected-report-id REPORT_ID
```

`CuratorLeaseRegistry` は単一 process 内だけを調整します。distributed deployment には external lease adapter が必要です。

## 🚀 クイックスタート

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
```

オプションの inactive PostgreSQL tooling：`pip install -e '.[postgresql]'`。

## 📚 ナビゲーション

- [日本語ドキュメント索引](./docs/ja/README.md)
- [English documentation map](./docs/DOCUMENTATION_MAP.md)
- [Test report](./TEST_REPORT.md)
- [Current status](./docs/STATUS.md)
- [Implementation status](./docs/IMPLEMENTATION_STATUS.md)
- [Architecture](./docs/ARCHITECTURE.md)
- [Security](./SECURITY.md)
- [NLnet scope](./docs/GRANT_NLNET_SCOPE.md)
- [Localization policy](./docs/LOCALIZATION_POLICY.md)
- [Translation status](./docs/TRANSLATION_STATUS.md)

## ✅ 検証済みベースライン

```text
Runtime merge: bbd816c09dd39a02e6de6c1014438490572f40f6 (PR #337)
Python 3.11: 2078 passed / 13 skipped / 0 failed
Python 3.12: 2078 passed / 13 skipped / 0 failed
Statements: 9756
Coverage: 100.00%
Mutation: 7/7
CI: 9/9
PostgreSQL integration: PostgreSQL 16 + pgvector 0.8.2 successful
```

## 🚧 claim の境界

Crystal は universal objective-truth detection、zero hallucinations、法的 GDPR/security certification、production-ready multi-tenancy、distributed locking、AGI / consciousness、active PostgreSQL runtime、automatic switching、cutover/rollback、完成済み dedicated Reader Core を主張しません。NLnet proposal は **submitted / under review / not awarded** のままです。

## 🤝 コントリビューションとライセンス

[CONTRIBUTING.md](./CONTRIBUTING.md)、[SECURITY.md](./SECURITY.md)、[GOVERNANCE.md](./GOVERNANCE.md)、[AGPL-3.0](./LICENSE) を参照してください。
