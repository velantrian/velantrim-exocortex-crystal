<!-- translation-source: docs/SAFETY_PRIVACY_AND_FAILURES.md@b7e6574dd7aefa2f32783ab79054fac6b3b4109f -->
<!-- translation-status: CURRENT -->
<!-- d2-locale: zh-CN -->
<!-- d2-boundary: public-ask-read-only -->
<!-- d2-boundary: postgresql-active=false -->
<!-- d2-boundary: erasure-not-global -->
<!-- d2-nonclaim: security-legal-gdpr-not-certified -->
<!-- d2-nonclaim: nlnet-not-awarded -->
# 安全、隐私与失败边界

**源：** `docs/SAFETY_PRIVACY_AND_FAILURES.md@b7e6574dd7aefa2f32783ab79054fac6b3b4109f`

本概览不能替代测试、安全审查或法律意见。

## Epistemic safety

```text
physical L3 != strict Canon
retrieval score != evidence
model output != verified fact
migration bundle != claim evidence
successful import != activation
```

Guardian 与 TruthGate 仍是 admission boundaries。公开 query 为 read-only；explicit
ingest 是分离的 write path。Crystal 不保证真理或零幻觉；无支撑状态应被 block、
label、refuse 或保持可审计。

## Local boundary

默认安装不强制依赖 cloud、LLM、telemetry 或 analytics。SQLite 是普通 active profile。
Durable `auto` 可选择 optional LadybugDB 或 SQLite 并锁定 choice；Mock 是明确 dev/test
state。PostgreSQL/pgvector 只是 operator inactive target，保持 `active=false`。

## Data 与 optional expansion

可存储 claims、metadata、provenance、epistemic state、graph、restrictions、
erasure/audit records、Receipts、outbox、bundles、backups 与 exports。数据只有在明确
启用 Anthropic、remote Neo4j、Wikidata、Redis、PostgreSQL migration、wider API 或
external copies 时离开 local boundary。

## Encryption 与 secrets

`VELANTRIM_ENCRYPTION_KEY` 保护 selected L1 fields，不自动覆盖 L3、backups、exports、
Receipts、logs 或 temporary files。必要时仍需 host encryption 与 key management。
Credentials 不得进入 profiles、bundles、receipts、logs、issues 或 Notion。

## API、privacy 与 erasure

API baseline 使用 authentication 与 loopback。External exposure 需要 TLS、reviewed
authentication、least privilege、limits、monitoring 与 incident handling。Access、
rectification、restriction、erasure 与 processing record 是工程控制，不是 GDPR
certification。Active store erasure 不会全局删除 independent copies。

## Safe failure responses

| 类别 | 预期行为 |
|---|---|
| Unsupported claim | block、label 或 bounded refusal |
| Read-only mutation | reject / no state change |
| Profile conflict | backend cache 前失败 |
| Missing dependency | explicit error，无 hidden Mock |
| Import failure | rollback，`active=false` |
| Evidence mismatch | verification failure |
| Receipt/audit tampering | digest/hash failure |
| Oversized migration | limits 处 fail closed |
| Network exposure | 仅 explicit 与 authenticated |
| Copy after erasure | separate inventory/deletion |

## Non-claims

Crystal 不是 security/legal/GDPR certification、arbitrary-scale proof、active PostgreSQL
runtime、automatic migration system、perfect truth guarantee、AGI/consciousness 或已获
NLnet grant 的证据。

详情：[Security](../../SECURITY.md)、[Privacy](../../PRIVACY.md)、[GDPR](../../GDPR.md)、
[Failure Modes](../FAILURE_MODES.md) 与
[英语 summary](../SAFETY_PRIVACY_AND_FAILURES.md)。
