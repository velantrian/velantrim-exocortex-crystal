<!-- translation-source: docs/STATUS.md@a497b7d3cfbe59ca75b11d7449d5a728455b3130 -->
<!-- translation-status: CURRENT -->
<!-- d1-locale: zh-CN -->
<!-- d1-boundary: public-ask-read-only -->
<!-- d1-boundary: postgresql-active=false -->
<!-- d1-nonclaim: import-is-not-activation -->
<!-- d1-nonclaim: nlnet-not-awarded -->
# Velantrim Crystal — 当前状态

**日期：** 2026-08-08  
**已验证 runtime checkpoint：** `bbd816c09dd39a02e6de6c1014438490572f40f6`  
**已验证 tree：** `f57e58a6f4d1954b649ba324996fcde42ac287b8`  
**已验证 implementation head：** `d7af7c80722274f9217bc5545d150f92e9363f37`  
**Runtime PR / CI：** #337 / `31256316536`  
**PostgreSQL integration CI：** `31256316532`

## 验证

- Python 3.11：**2078 passed / 13 skipped / 0 failed**；
- Python 3.12：**2078 passed / 13 skipped / 0 failed**；
- **9756 statements / 100.00% line coverage**；
- `core/postgresql_migration.py`：**44/44 statements**；
- `core/postgresql_migration_impl.py`：**336/336 statements**；
- Ring Zero mutants **7/7** killed；
- permanent CI jobs **9/9** successful；
- real PostgreSQL/pgvector integration **1/1** successful。

精确证据：[TEST_REPORT.md](../../TEST_REPORT.md) 与
[machine-readable manifest](../status/implementation-manifest.json)。

## 当前已验证 capability boundary

Crystal 保留 local-first SQLite baseline，并实现 issue #332 phase 1：

```text
verified completed logical bundle
→ PostgreSQL 16 / pgvector 0.8.2 preflight
→ new inactive target schema
→ serializable import
→ independent read-only canonical target re-hash
→ exact count / byte / SHA-256 equivalence
→ non-secret receipts
```

PostgreSQL driver 是可选 extra，只在显式 operator command 中 lazy-load。
默认安装仍是 pure standard library。导入目标不注册到普通 runtime composition，
保持 `active=false`，不能提供普通 reads/writes。

## Authority boundary

```text
storage profile         = deployment identity
migration bundle        = operation evidence
physical L3             = multi-status storage
strict Canon            = trusted read projection
migration/import        != TruthGate admission
successful equivalence  != backend activation
```

Guardian、TruthGate、restrictions、TrustSnapshot 与 CanonicalView 不变。

## 仍未实现

- active PostgreSQL read/write runtime selection；
- exact-vs-ANN evaluation 与已接受 ANN thresholds；
- activation、cutover、fencing、rollback 或 dual-write；
- PostgreSQL backup/restore/upgrade lifecycle、production pooling 与 distributed fencing；
- production IdP/multi-tenancy 或 legal/security/GDPR certification；
- 专用 verified Reader Core。

## 资助状态

项目已提交并正在审查。**不声称已获资助或预算发生变化。** PR #337 与
issue #332 已是 merged baseline，不能再次计入未来资助工作。
