# 🔱 Velantrim ExoCortex — Crystal

> 🌐 [English — 正式な基準](./README.md) · 🇯🇵 **日本語概要**

<!-- localization-source: main@e521440e9bb188d88475f17dd5bcdd161b314605 -->

### 信頼できる AI システムのための、検証可能でローカル優先の記憶基盤

このファイルは**簡潔な非規範的ガイド**であり、文書全体の翻訳ではありません。
技術判断、アーキテクチャ、状態、セキュリティ、助成金に関する主張は英語で管理されます。
差異がある場合は [README.md](./README.md) と英語の証拠が優先されます。

`v0.3.0` · 🧪 **2078 成功 / 13 スキップ** · 🎯 **100.00% カバレッジ** · ✅ **9 CI ジョブ**

**検証済み runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6` — PR #337。

Crystal は物理ストレージ、証拠、認識論的な受理、信頼された読み取りを分離します。
データの存在、検索順位、移行成功によって Guardian、TruthGate、厳格な Canon の調整を
迂回することはできません。

## 検証済み範囲

- 型付き主張、来歴、正確な出典範囲；
- Guardian と TruthGate の受理境界；
- 不変の `TrustSnapshot` / `CanonicalView` 読み取り；
- 読み取り専用の公開 HTTP、CLI、MCP クエリ；
- TRACE、receipt、制限、消去、明示的な矛盾判断；
- 通常のローカルプロファイルとしての SQLite；
- 検証済みバックアップ/復元と資源制限付き論理エクスポート；
- 非アクティブな対象 schema への任意 PostgreSQL/pgvector インポートと独立した厳密状態検証。

## ストレージ境界

```text
SQLite = 現在の通常 local-first プロファイル
PostgreSQL + pgvector = 任意の移行先
active=false
通常の runtime reads/writes はない
自動 switching、cutover、rollback、dual-write はない
```

PostgreSQL ドライバは `[postgresql]` でのみインストールされ、明示的な運用コマンドでのみ
ロードされます。successful import は運用上の証拠であり、activation や厳格な Canon への
受理ではありません。

## 不変の意味境界

```text
physical L3          != strict Canon
retrieval score      != evidence
migration receipt    != claim evidence
successful import    != activation
backend availability != backend selection
```

Crystal は普遍的真理、ゼロ・ハルシネーション、アクティブな PostgreSQL runtime、
本番 multi-tenancy、distributed exactly-once、法的/GDPR/セキュリティ認証、Titan 統合、
人工意識を主張しません。

## クイックスタート

```bash
git clone https://github.com/velantrian/velantrim-exocortex-crystal.git
cd velantrim-exocortex-crystal
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
```

## 現在の英語証拠

- [正式 README](./README.md)
- [検証レポート](./TEST_REPORT.md)
- [現在の状態](./docs/STATUS.md)
- [実装マトリクス](./docs/IMPLEMENTATION_STATUS.md)
- [セキュリティ方針](./SECURITY.md)
- [ローカライズ方針](./docs/LOCALIZATION_POLICY.md)
- [日本語文書ルート](./docs/ja/README.md)

NLnet 申請は提出済みで審査中です。採択や予算変更は主張していません。
