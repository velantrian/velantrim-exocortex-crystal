<!-- translation-source: docs/ARCHITECTURE_OVERVIEW.md@208f1c772ee3a112cb803d2413c120bef23adb05 -->
<!-- translation-status: CURRENT -->
<!-- d3-locale: ja -->
<!-- d3-boundary: physical-l3-not-strict-canon -->
<!-- d3-boundary: public-query-read-only -->
<!-- d3-boundary: postgresql-active=false -->
<!-- d3-nonclaim: import-is-not-activation -->
<!-- d3-nonclaim: reader-core-not-implemented -->
<!-- d3-nonclaim: nlnet-not-awarded -->
# Crystal — アーキテクチャ概要

この翻訳は案内層です。競合時は、マージ済みコード、実行可能テスト、exact CI、英語契約が優先されます。

## 中核モデル

```text
source + 明示的 ingest
→ provenance + 正規化
→ Guardian checks
→ TruthGate decision
→ operational L1 state + multi-status physical L3
→ deny-dominant strict Canon read projection
→ read-only retrieval / answer / bounded refusal
```

physical L3に保存されたことはstrict Canon所属を意味しません。Retrieval score、vector similarity、model outputは独立した証拠ではありません。

## メモリとレビュー層

- **L0:** プロセス内の一時的コンテキスト。
- **L1:** SQLite/WALによる運用状態、証拠、監査、receipts、import/review sessions、outbox。
- **L2:** 候補または隔離されたclaimのpending/review staging。最終的な真実層ではありません。
- **L3:** graph-oriented multi-status storage。strict Canonとは別です。
- **TrustSnapshot / CanonicalView:** deny-dominantな信頼済み読み取り面。

## 読み取りと書き込みの分離

`HTTP /ask`、`CLI ask`、MCPは`core.query_pipeline.query()`をread-onlyで通ります。Queryはfact、ESM、L3、outbox、episode link、embedder identityを変更できません。明示的な`ingest`だけがGuardianとTruthGateに管理されたadmission-capable write pathに入ります。

## ストレージプロファイルと可搬性

SQLiteが通常のactive local-first profileです。最初のdurable `auto`ではoptional LadybugDBまたはSQLiteを選択し、backendとnon-secret locator identityを固定します。ephemeral Mockへのsilent fallbackは禁止です。

検証済みPostgreSQL/pgvector経路はinactive targetで止まります。

```text
verified SQLite bundle
→ transactional PostgreSQL import
→ independent read-only re-hash
→ exact equivalence
→ active=false
```

Importやequivalenceはactivation、backend selection、TruthGate admission、cutover、rollback、dual-writeではありません。PostgreSQLは通常runtime compositionに含まれません。

## 文書読解

Source spans、document records、import sessions、dry-run/review flowsは実装済みbaselineです。Coverage map、contradiction-aware rereading、document-level synthesisを持つ専用multi-pass Reader Coreは未実装です。

## 非主張

CrystalはAGI、意識、ゼロhallucination、active PostgreSQL runtime、automatic switching、production ANN acceptance、cutover/rollback/dual-write、security/legal/GDPR certification、NLnet採択を主張しません。

## 英語ソース

- [完全なアーキテクチャ](../ARCHITECTURE.md)
- [ストレージと権限の境界](../STORAGE_AND_AUTHORITY_BOUNDARIES.md)
- [実装状況](../IMPLEMENTATION_STATUS.md)
- [非アクティブPostgreSQLインポート](../architecture/POSTGRESQL_INACTIVE_IMPORT.md)
