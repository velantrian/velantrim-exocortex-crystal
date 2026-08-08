<!-- translation-source: docs/SAFETY_PRIVACY_AND_FAILURES.md@b7e6574dd7aefa2f32783ab79054fac6b3b4109f -->
<!-- translation-status: CURRENT -->
<!-- d2-locale: ja -->
<!-- d2-boundary: public-ask-read-only -->
<!-- d2-boundary: postgresql-active=false -->
<!-- d2-boundary: erasure-not-global -->
<!-- d2-nonclaim: security-legal-gdpr-not-certified -->
<!-- d2-nonclaim: nlnet-not-awarded -->
# Safety・privacy・failure boundaries

**Source:** `docs/SAFETY_PRIVACY_AND_FAILURES.md@b7e6574dd7aefa2f32783ab79054fac6b3b4109f`

この overview は test、security review、legal advice の代替ではありません。

## Epistemic safety

```text
physical L3 != strict Canon
retrieval score != evidence
model output != verified fact
migration bundle != claim evidence
successful import != activation
```

Guardian と TruthGate は admission boundary。public query は read-only、explicit ingest
は分離された write path です。Crystal は truth や zero hallucinations を保証せず、
unsupported state を block、label、refuse、または auditable にします。

## Local boundary

Default installation は mandatory cloud、LLM、telemetry、analytics を持ちません。
SQLite は ordinary active profile。durable `auto` は optional LadybugDB または SQLite
を選択し lock、Mock は explicit dev/test state。PostgreSQL/pgvector は operator-only
inactive target で `active=false` です。

## Data と optional expansion

claims、metadata、provenance、epistemic state、graph、restrictions、erasure/audit records、
Receipts、outbox、bundles、backups、exports を保存可能。Data は explicit Anthropic、
remote Neo4j、Wikidata、Redis、PostgreSQL migration、wide API、external copy でのみ
local boundary を出ます。

## Encryption と secrets

`VELANTRIM_ENCRYPTION_KEY` は selected L1 fields を保護し、L3、backups、exports、
Receipts、logs、temporary files 全体は自動保護しません。host encryption と key
management が必要な場合があります。credentials は profiles、bundles、receipts、
logs、issues、Notion に保存しません。

## API、privacy、erasure

API baseline は authentication と loopback。external exposure は TLS、reviewed auth、
least privilege、limits、monitoring、incident handling が必要。access、rectification、
restriction、erasure、processing record は engineering controls で GDPR certification
ではありません。active store erasure は independent copies を global に消しません。

## Safe failure responses

| Class | Expected behaviour |
|---|---|
| Unsupported claim | block, label, bounded refusal |
| Read-only mutation | reject / no state change |
| Profile conflict | backend cache 前に failure |
| Missing dependency | explicit error, no hidden Mock |
| Import failure | rollback, `active=false` |
| Evidence mismatch | verification failure |
| Receipt/audit tampering | digest/hash failure |
| Oversized migration | limits で fail closed |
| Network exposure | explicit and authenticated only |
| Copy after erasure | separate inventory/deletion |

## Non-claims

Crystal は security/legal/GDPR certification、arbitrary-scale proof、active PostgreSQL
runtime、automatic migration、perfect truth guarantee、AGI/consciousness、awarded NLnet
grant の証拠ではありません。

Details: [Security](../../SECURITY.md), [Privacy](../../PRIVACY.md), [GDPR](../../GDPR.md),
[Failure Modes](../FAILURE_MODES.md), [English summary](../SAFETY_PRIVACY_AND_FAILURES.md).
