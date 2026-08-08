<!-- translation-source: docs/STATUS.md@a497b7d3cfbe59ca75b11d7449d5a728455b3130 -->
<!-- translation-status: CURRENT -->
<!-- d1-locale: ja -->
<!-- d1-boundary: public-ask-read-only -->
<!-- d1-boundary: postgresql-active=false -->
<!-- d1-nonclaim: import-is-not-activation -->
<!-- d1-nonclaim: nlnet-not-awarded -->
# Velantrim Crystal — 現在の状態

**日付:** 2026-08-08  
**検証済み runtime checkpoint:** `bbd816c09dd39a02e6de6c1014438490572f40f6`  
**検証済み tree:** `f57e58a6f4d1954b649ba324996fcde42ac287b8`  
**検証済み implementation head:** `d7af7c80722274f9217bc5545d150f92e9363f37`  
**Runtime PR / CI:** #337 / `31256316536`  
**PostgreSQL integration CI:** `31256316532`

## 検証

- Python 3.11: **2078 passed / 13 skipped / 0 failed**
- Python 3.12: **2078 passed / 13 skipped / 0 failed**
- **9756 statements / 100.00% line coverage**
- `core/postgresql_migration.py`: **44/44 statements**
- `core/postgresql_migration_impl.py`: **336/336 statements**
- Ring Zero mutant **7/7** killed
- permanent CI **9/9** successful
- real PostgreSQL/pgvector integration **1/1** successful

正確な証拠: [TEST_REPORT.md](../../TEST_REPORT.md) と
[machine-readable manifest](../status/implementation-manifest.json)。

## 現在の検証済み capability boundary

Crystal は local-first SQLite baseline を維持し、issue #332 phase 1 を実装しています。

```text
verified completed logical bundle
→ PostgreSQL 16 / pgvector 0.8.2 preflight
→ new inactive target schema
→ serializable import
→ independent read-only canonical target re-hash
→ exact count / byte / SHA-256 equivalence
→ non-secret receipts
```

PostgreSQL driver は任意 extra で、明示的 operator command のときだけ lazy-load
されます。標準 install は pure standard library のままです。import target は通常の
runtime composition に登録されず、`active=false` のままで通常 read/write を行いません。

## Authority boundary

```text
storage profile         = deployment identity
migration bundle        = operation evidence
physical L3             = multi-status storage
strict Canon            = trusted read projection
migration/import        != TruthGate admission
successful equivalence  != backend activation
```

Guardian、TruthGate、restrictions、TrustSnapshot、CanonicalView は変更されません。

## 未実装

- active PostgreSQL read/write runtime selection
- exact-vs-ANN evaluation と accepted ANN threshold
- activation、cutover、fencing、rollback、dual-write
- PostgreSQL backup/restore/upgrade lifecycle、production pooling、distributed fencing
- production IdP/multi-tenancy、法務・security・GDPR certification
- 専用 verified Reader Core

## 助成状態

プロジェクトは提出済みで審査中です。**採択や budget change は主張しません。**
PR #337 と issue #332 は既に merged baseline で、将来の funded work として再計上できません。
