<!-- translation-source: docs/STORAGE_AND_AUTHORITY_BOUNDARIES.md@208f1c772ee3a112cb803d2413c120bef23adb05 -->
<!-- translation-status: CURRENT -->
<!-- d3-locale: ja -->
<!-- d3-boundary: physical-l3-not-strict-canon -->
<!-- d3-boundary: public-query-read-only -->
<!-- d3-boundary: postgresql-active=false -->
<!-- d3-nonclaim: import-is-not-activation -->
<!-- d3-nonclaim: reader-core-not-implemented -->
<!-- d3-nonclaim: nlnet-not-awarded -->
# ストレージと権限の境界

## 分離された識別子

```text
storage profile = deployment identity
physical L3 = multi-status graph state
strict Canon = trusted read projection
migration bundle = operation-integrity evidence
retrieval score = ranking signal
model output = generated text
```

どの識別子も、他の権限を自動的に付与しません。

## durable profile

SQLiteが通常のactive local-first profileです。最初のdurable `auto`はoptional LadybugDBまたはSQLiteを選び、backendとnon-secret locatorを固定できます。後の競合はfail-closedになります。Mockは明示的なdevelopment/CI状態に限られます。

## physical L3とstrict Canon

physical L3はVERIFIED、USER_CLAIMED、UNVERIFIED、HYPOTHESIS、SUBJECTIVE、contested、superseded、restrictedを保持できます。strict Canonは現在のevidenceとpolicyに基づくdeny-dominant projectionです。保存、retrieval、高いscoreだけでは不十分です。

## 読み取りと書き込み

Public queryは`core.query_pipeline.query()`をread-onlyで通ります。明示的`ingest`がadmission-capable write pathであり、GuardianとTruthGateが構造的・認識論的境界を適用します。

## SQLiteライフサイクルと移行

Backup、independent verification、inactive restore、bounded deterministic logical export、bundle verificationが実装されています。承認されたphysical-L3 datasetsは新しいinactive PostgreSQL schemaへimportし、exact comparisonできます。targetは`active=false`のままです。

これはL1全体、audit/outbox、encryption metadata、configuration、independent copiesのwhole-system migrationではありません。Active PostgreSQL runtime、ANN acceptance、automatic switching、cutover、fencing、rollback、dual-writeはありません。

## secretsとcopies

Passwords、tokens、private keys、credential-bearing DSNsをprofiles、bundles、receipts、logs、GitHub、Notionへ入れてはいけません。Backups、exports、migrationsは追加copyを作り、active storeからの削除では自動的に消えません。Selected L1 field encryptionはuniversal encryptionではありません。

## operation evidence

| 事象 | 証明すること | 証明しないこと |
|---|---|---|
| L3 record | physical persistence | strict Canon membership |
| retrieval result | candidate relevance | sufficient evidence |
| verified backup | backup integrity | claim truth |
| successful import | import integrity | activation / runtime selection |
| exact equivalence | approved datasets equality | production readiness / cutover |

専用Reader Coreは未実装で、NLnetはsubmitted / under review / not awardedです。

## 詳細な英語契約

- [完全なアーキテクチャ](../ARCHITECTURE.md)
- [Durable Storage Profile](../architecture/DURABLE_STORAGE_PROFILE.md)
- [Migration Contract](../architecture/CROSS_BACKEND_MIGRATION_CONTRACT.md)
- [Inactive PostgreSQL Import](../architecture/POSTGRESQL_INACTIVE_IMPORT.md)
- [ADR-021](../adr/ADR-021-CROSS-BACKEND-MIGRATION-CONTRACT.md)
