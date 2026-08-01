# 🔱 Velantrim ExoCortex — Crystal

> 🌐 🇬🇧 [English](./README.md) · 🇩🇪 [Deutsch](./README.de.md) · 🇫🇷 [Français](./README.fr.md) · 🇪🇸 [Español](./README.es.md) · 🇮🇹 [Italiano](./README.it.md) · 🇷🇺 [Русский](./README.ru.md) · 🇨🇳 [简体中文](./README.zh-CN.md) · 🇸🇦 [العربية](./README.ar.md) · 🇯🇵 **日本語** · 🇮🇳 [हिन्दी](./README.hi.md)

### 信頼できる AI システムのための、検証可能でローカルファーストなメモリ基盤

`v0.3.0` · 🧪 **1853 件成功 / 12 件スキップ** · 🎯 **カバレッジ 100%** · 🧬 **宣言済み変異 7/7 を検出** · ✅ **CI 9 ジョブ** · 🐍 **既定ランタイムは Python 標準ライブラリのみ** · ⚖️ **AGPL-3.0**

> Crystal は、単なるチャットボットではありません。主張の内容、出典、
> 認識論的状態、回答の根拠として利用できるかどうか、そして矛盾がどの
> 明示的な判断によって処理されたかを記録する、メモリ・証拠・意思決定の
> 境界です。

**検証済みランタイム・チェックポイント:** `f91299c44a1a1850fa516f3abb96c916326f7a8c` — PR #302 マージ済み。  
**正確な検証結果:** [TEST_REPORT.md](./TEST_REPORT.md) と
[機械可読の実装マニフェスト](./docs/status/implementation-manifest.json)。

> この翻訳は、英語版 README と同じ機能・安全性・状態の境界を維持します。
> 安定した API 識別子はコード表記のまま残し、説明文は自然な日本語で記述しています。

---

## 🎯 Crystal が必要な理由

多くの AI システムは、原資料、ユーザーの主張、モデル出力、仮説、検索で
得た断片、永続メモリを、同じコンテキストやベクトルストアに混在させます。
その結果、流暢な文章が、証拠に裏付けられていない権威を獲得することがあります。

```text
説得力のある主張が、自動的に信頼できるわけではない。
グラフのノードが、自動的に厳格な Canon になるわけではない。
検索スコアは証拠ではない。
モデル出力は独立した情報源ではない。
矛盾が自動的に勝者を決めることはない。
トピックラベルは真偽判定ではない。
```

## 🧠 主な機能

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
- 権威を付与しない複数ラベルのトピック facet;
- ランタイム遷移から生成される機械可読 ESM 仕様;
- 決定論的評価、100% 行カバレッジ、Ring Zero mutation gate;
- バージョン管理された L3 ベンチマーク履歴。

## 🏛️ アーキテクチャ概要

```text
明示的な ingest
→ 主張分類 + 証拠メタデータ
→ L0/L1 の Observed 状態
→ Guardian → TruthGate → 制限/矛盾チェック
→ 多状態の物理 L3 グラフ

公開クエリ
→ 読み取り専用 retrieval
→ 不変 TrustSnapshot
→ Guardian + CanonicalView STRICT
→ FactsPack + TRACE
→ 回答 / 拒否 / Receipt

未解決の矛盾
→ 不変 ContradictionReport
→ actor/役割/scope の認可 + decision lease
→ キュレーターによる明示的判断 + 理由
→ 監査可能な canonical 書き込み経路

トピックによるナビゲーション
→ 助言的な TopicFacet
→ 絞り込み/分類のみ — Canon への登録には使わない
```

```text
物理 L3 グラフ ≠ 厳格な Canon
query ≠ ingest
confidence ≠ 独立した証拠
LLM 出力 ≠ 独立した事実情報源
トピック関連度 ≠ 真実性
ローカル lease ≠ 分散協調の保証
```

TruthGate は登録方針を適用するゲートであり、客観的真実を独立に知る
オラクルではありません。厳格な Canon は、証拠、状態、ESM、処理制限に
基づいて方針が許可した読み取り投影です。

## 🛡️ 公開クエリの読み取り専用境界

`HTTP /ask`、`HTTP /receipt`、`CLI ask`、`CLI receipt`、`MCP search` は
`core.query_pipeline` を共有します。これらは事実を作成せず、ESM を遷移
させず、L3 に書き込まず、outbox を処理せず、embedding fingerprint を
初期化しません。

詳細は [Read-Only Query Boundary](./docs/architecture/read-only-query-boundary.md) を参照してください。

## ⚖️ 矛盾の明示的な解決

```bash
python -m core.conflict_surfaces FACT_ID \
  --disposition COEXIST \
  --actor alice \
  --reason "各主張は異なる文脈を説明している" \
  --expected-report-id REPORT_ID
```

FastAPI の `POST /review/resolve-conflict` は、ホストアプリケーションの
認証機構とともに登録する必要があります。`core.curator_auth` は actor、
権限、scope を検証します。`CuratorLeaseRegistry` が保護できるのは単一
プロセス内だけであり、分散構成では外部 lease アダプターが必要です。

[競合解決サーフェス](./docs/CONFLICT_RESOLUTION_SURFACES.md) と
[トピック facet / curator IAM](./docs/TOPIC_FACETS_AND_CURATOR_IAM.md) を参照してください。

## 🏷️ 助言的なトピック facet

`core.topic_facets` は、ナビゲーション、絞り込み、分類のための正規化
ラベルを提供します。スコアはトピック関連度のみを表し、truth status、
証拠、ESM、厳格な Canon への所属を変更しません。

## 🚀 クイックスタート

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
```

## 📚 ドキュメント

- [ドキュメントマップ](./docs/DOCUMENTATION_MAP.md)
- [現在の状態](./docs/STATUS.md)
- [アーキテクチャ](./docs/ARCHITECTURE.md)
- [テストレポート](./TEST_REPORT.md)
- [評価](./docs/EVAL.md)
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
現在の lease はプロセス内に限定されます。分散協調と外部 ID プロバイダー
との統合は、独立した今後の作業です。

## 🤝 コントリビューションとライセンス

[CONTRIBUTING.md](./CONTRIBUTING.md)、[SECURITY.md](./SECURITY.md)、
[GOVERNANCE.md](./GOVERNANCE.md)、[AGPL-3.0](./LICENSE) を参照してください。
