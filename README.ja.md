# 🔱 Velantrim ExoCortex — Crystal

> 🌐 🇬🇧 [English](./README.md) · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 [Español](./README.es.md) · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 [Русский](./README.ru.md) · 🇨🇳 [简体中文](./README.zh-CN.md) · 🇸🇦 [العربية](./README.ar.md) · 🇯🇵 **日本語** · 🇮🇳 [हिन्दी](./README.hi.md)

### 信頼できる AI システムのための、検証可能でローカルファーストなメモリ基盤

`v0.3.0` · 🧪 **1853 件成功 / 12 件スキップ** · 🎯 **カバレッジ 100%** · 🧬 **宣言済み変異 7/7 を検出** · ✅ **CI 9 ジョブ** · 🐍 **既定ランタイムは Python 標準ライブラリのみ** · ⚖️ **AGPL-3.0**

> Crystal は、単なるチャットボットではありません。主張の内容、出典、
> 認識論的状態、回答の根拠として利用できるかどうか、そして矛盾がどの
> 明示的な判断によって処理されたかを記録する、メモリ・証拠・意思決定の
> 境界です。

**検証済みランタイム・チェックポイント:** `f91299c44a1a1850fa516f3abb96c916326f7a8c` — PR #302 マージ済み。  
**実装上の正本:** GitHub `main` にマージされたコードとテスト。  
**正確な検証結果:** [TEST_REPORT.md](./TEST_REPORT.md) と
[機械可読の実装マニフェスト](./docs/status/implementation-manifest.json)。

> **ローカライズ契約:** 各翻訳 README は、英語版と同じ機能・安全性・
> 状態の境界を維持します。安定した API 識別子はコード表記のまま残し、
> 説明文は自然な日本語で記述します。

---

## 🎯 Crystal が必要な理由

多くの AI システムは、原資料、ユーザーの主張、モデル出力、仮説、検索で
得た断片、永続メモリを、同じコンテキストやベクトルストアに混在させます。
その結果、流暢な文章が、証拠に裏付けられていない権威を獲得することがあります。

Crystal は、これらの境界を明示します。

```text
説得力のある主張が、自動的に信頼できるわけではない。
グラフのノードが、自動的に厳格な Canon になるわけではない。
検索スコアは証拠ではない。
モデル出力は独立した情報源ではない。
矛盾が自動的に勝者を決めることはない。
トピックラベルは真偽判定ではない。
```

## 🧠 Crystal が提供するもの

- 型付き主張と明示的な認識論的ライフサイクル;
- 出典、evidence span、provenance のメタデータ;
- Guardian と TruthGate による登録境界;
- 厳格な Canon と分離された多状態の物理 L3 グラフ;
- 不変かつ deny-dominant な `TrustSnapshot` 読み取り調停;
- 厳密に読み取り専用の公開 HTTP・CLI・MCP クエリ;
- TRACE と、再実行可能で改ざんを検出できる Receipt;
- 処理制限、消去、監査、インポートセッション;
- レビューキューと再開可能なレビューセッション;
- 型付きで不変の矛盾レポート;
- 明示的な `COEXIST`、`CONTEXTUALIZE`、`SUPERSEDE` 判断;
- CLI と認証付き HTTP による競合解決;
- scope で制限されたキュレーター権限とプロセス内 decision lease;
- 権威を付与しない複数ラベルの `TopicFacet`;
- ランタイム遷移から生成される機械可読 ESM 仕様;
- 決定論的評価、100% 行カバレッジ、Ring Zero mutation gate;
- バージョン管理された L3 ベンチマーク履歴。

## 🏛️ アーキテクチャ概要

以下の 3 つの図は、同じシステムを **目的**、**情報の流れ**、
**モジュール間の関係**という補完的な視点から示します。

### 🧠 マインドマップ — 目的と機能境界

```text
🧠 Velantrim ExoCortex — Crystal
│
├── 🎯 目的
│   ├── AI のための検証可能なメモリ
│   ├── ローカルファーストな信頼基盤
│   └── 証拠に基づく回答と意思決定
│
├── 🏛️ メモリモデル
│   ├── L0 — プロセス内の高速ワーキングキャッシュ
│   ├── L1 — ライフサイクルを扱う運用メモリ
│   ├── L2 — 保留とレビューの境界
│   └── L3 — グラフ型の多状態メモリ
│
├── 🛡️ 信頼境界
│   ├── Guardian — 構造・ポリシー検証
│   ├── TruthGate — 登録ポリシー境界
│   ├── TrustSnapshot — 不変の読み取り調停
│   └── CanonicalView — 厳格な信頼済み投影
│
├── 📜 証拠と監査可能性
│   ├── 出典・evidence span・provenance
│   ├── TRACE — 根拠の系譜
│   └── Receipt — 再実行と改ざん検出
│
├── ⚖️ レビューと矛盾
│   ├── レビューキューと再開可能なセッション
│   ├── 不変の ContradictionReport
│   ├── COEXIST
│   ├── CONTEXTUALIZE
│   └── SUPERSEDE
│
├── 🏷️ 助言的ナビゲーション
│   └── TopicFacet — 複数ラベル・非権威的メタデータ
│
├── 🔐 ガバナンスと調整
│   ├── scope 付きキュレーター役割・権限
│   ├── 認証済み actor との対応付け
│   └── プロセス内 decision lease
│
└── 📊 検証
    ├── 決定論的テストと評価
    ├── 100% 行カバレッジ
    ├── Ring Zero mutation gate
    └── バージョン管理されたベンチマーク履歴
```

### 🏗️ ASCII アーキテクチャ — 情報の流れ

```text
┌─────────────────────────────────────────────────────────────────────┐
│              🔱 Velantrim ExoCortex — Crystal                      │
│        AI のためのローカルファーストな検証可能メモリ基盤           │
└─────────────────────────────────────────────────────────────────────┘

                         📥 明示的な ingest
                                │
                                ▼
                 🧾 主張タイプ + 出典 + evidence span
                                │
                                ▼
                      🧠 L0 / L1 の Observed 状態
                                │
                                ▼
             🛡️ Guardian ──► ⚖️ TruthGate ──► 🚧 制限
                                │
                  ┌─────────────┴─────────────┐
                  │                           │
                  ▼                           ▼
          ⏳ L2 保留 / レビュー       🏛️ 物理 L3 グラフ
                  │                           │
                  │                           ▼
                  │                 📜 provenance / TRACE
                  │                           │
                  └─────────────┬─────────────┘
                                │
                                ▼
                       📐 不変の TrustSnapshot
                                │
                                ▼
                  🛡️ Guardian + CanonicalView STRICT
                                │
                   ┌────────────┴────────────┐
                   │                         │
                   ▼                         ▼
            💬 根拠付き回答          🚫 境界付き拒否
                   │
                   ▼
               🧾 再実行可能な Receipt

⚖️ 未解決の矛盾
        │
        ▼
📋 不変の ContradictionReport
        │
        ▼
🔐 scope 付き principal + capability + decision lease
        │
        ▼
🧑‍⚖️ 明示的な COEXIST / CONTEXTUALIZE / SUPERSEDE
        │
        ▼
📜 監査可能な canonical 書き込み経路

🏷️ TopicFacet ──► ナビゲーション / 絞り込み / 分類のみに使用
                └─► truth・ESM・evidence・Canon の権威にはならない
```

### 🌳 関係ツリー — モジュールの接続

```text
🌳 Crystal システムの関係
│
├── 🧠 メモリ層
│   ├── L0 ──► 高速で再構築可能なワーキングキャッシュ
│   ├── L1 ──► ライフサイクル・制限・保留作業
│   ├── L2 ──► 論理的なレビュー境界
│   └── L3 ──► グラフ型の多状態ストレージ
│
├── 🛡️ 信頼層
│   ├── Guardian ──► 構造・ポリシー検証
│   ├── TruthGate ──► 登録判断
│   ├── TrustSnapshot ──► deny-dominant な L1/L3 調停
│   └── CanonicalView ──► 厳格な grounding 投影
│
├── 📜 証拠層
│   ├── 出典メタデータ
│   ├── evidence span
│   ├── provenance
│   ├── TRACE
│   └── Receipt
│
├── ⚖️ レビュー層
│   ├── レビューキュー
│   ├── 再開可能なレビューセッション
│   ├── ContradictionReport
│   └── 明示的な disposition
│       ├── COEXIST
│       ├── CONTEXTUALIZE
│       └── SUPERSEDE
│
├── 🔐 認可層
│   ├── CuratorPrincipal
│   ├── role と scope 付き capability
│   ├── 認証済み actor の一致
│   └── プロセス内 decision lease
│
├── 🏷️ 助言層
│   └── TopicFacet
│       ├── 複数ラベル
│       ├── スコアはトピック関連度のみ
│       └── truth や登録判断への権限を持たない
│
├── 🔎 公開クエリ層
│   ├── HTTP /ask と /receipt
│   ├── CLI ask と receipt
│   └── MCP search
│       └── 共通の読み取り専用 query pipeline
│
└── 📊 検証層
    ├── Python 3.11 / 3.12 テスト
    ├── coverage gate
    ├── Ring Zero mutation gate
    ├── security / container チェック
    └── ベンチマーク履歴
```

### 中心となる区別

```text
物理 L3 グラフ ≠ 厳格な Canon
query ≠ ingest
confidence ≠ 独立した証拠
LLM 出力 ≠ 独立した事実情報源
矛盾 ≠ 自動的な勝者
トピック関連度 ≠ 真実性や証拠品質
ローカル lease ≠ 分散協調の保証
```

TruthGate は登録方針を適用するゲートであり、客観的真実を独立に知る
オラクルではありません。厳格な Canon は、証拠、状態、ESM、confidence
の構造、処理制限に基づいて方針が許可した読み取り投影です。

## 🛡️ 公開クエリの読み取り専用境界

`HTTP /ask`、`HTTP /receipt`、`CLI ask`、`CLI receipt`、`MCP search` は
`core.query_pipeline` を共有します。これらは事実を作成せず、ESM を遷移
させず、L3 に書き込まず、outbox を処理せず、episode を記録せず、
embedding fingerprint を初期化せず、unknown candidate を保存せず、
adaptive verification state を変更しません。

詳細は [Read-Only Query Boundary](./docs/architecture/read-only-query-boundary.md) を参照してください。

## ⚖️ 矛盾の明示的な解決

未解決の矛盾がある間、通常の approval は fail-closed になります。
キュレーターは disposition を明示的に選択し、actor と理由を示す必要があります。

```bash
python -m core.conflict_surfaces FACT_ID \
  --disposition COEXIST \
  --actor alice \
  --reason "各主張は異なる文脈を説明している" \
  --expected-report-id REPORT_ID
```

FastAPI の `POST /review/resolve-conflict` は、ホストアプリケーションの
認証機構とともに登録する必要があります。`core.curator_auth` は認証済み
principal を scope 付き capability に対応付けます。`CuratorLeaseRegistry`
が並行判断を防げるのは単一プロセス内だけであり、分散構成では共有の外部
lease アダプターが必要です。

[競合解決サーフェス](./docs/CONFLICT_RESOLUTION_SURFACES.md) と
[トピック facet / curator IAM](./docs/TOPIC_FACETS_AND_CURATOR_IAM.md) を参照してください。

## 🏷️ 助言的なトピック facet

`core.topic_facets` は、ナビゲーション、絞り込み、分類のための正規化された
複数ラベルメタデータを提供します。facet score はトピック関連度のみを
表し、truth status、証拠、ESM、矛盾の結果、厳格な Canon への所属を変更しません。

## 🚀 クイックスタート

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
```

続きは [QUICKSTART.md](./docs/QUICKSTART.md) を参照してください。

## 📚 ドキュメント

- [ドキュメントマップ](./docs/DOCUMENTATION_MAP.md)
- [現在の状態](./docs/STATUS.md)
- [実装状態](./docs/IMPLEMENTATION_STATUS.md)
- [アーキテクチャ](./docs/ARCHITECTURE.md)
- [読み取り専用クエリ境界](./docs/architecture/read-only-query-boundary.md)
- [競合解決サーフェス](./docs/CONFLICT_RESOLUTION_SURFACES.md)
- [Topic facets と curator IAM](./docs/TOPIC_FACETS_AND_CURATOR_IAM.md)
- [テストレポート](./TEST_REPORT.md)
- [評価](./docs/EVAL.md)
- [障害モード](./docs/FAILURE_MODES.md)
- [NLnet の範囲](./docs/GRANT_NLNET_SCOPE.md)

## ✅ 検証済みベースライン

```text
Python 3.11: 1853 passed / 12 skipped
Python 3.12: 1853 passed / 12 skipped
Statements:  7236
Coverage:    100.00%
Mutation:    7/7 declared Ring Zero mutants killed
CI jobs:     9
```

## 🚧 主張の範囲

Crystal は、普遍的な真偽判定、あらゆる幻覚の排除、GDPR/セキュリティ認証、
本番マルチテナント対応、人工意識、Titan/Full ExoCortex の実装を主張しません。
現在の lease はプロセス内に限定されます。分散協調、外部 ID プロバイダー統合、
より広い provenance 接続、Titan 統合は独立した今後の作業です。

## 🤝 コントリビューションとライセンス

[CONTRIBUTING.md](./CONTRIBUTING.md)、[SECURITY.md](./SECURITY.md)、
[GOVERNANCE.md](./GOVERNANCE.md)、[AGPL-3.0](./LICENSE) を参照してください。
