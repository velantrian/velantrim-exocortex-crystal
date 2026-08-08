<!-- translation-source: docs/SAFETY_PRIVACY_AND_FAILURES.md@b7e6574dd7aefa2f32783ab79054fac6b3b4109f -->
<!-- translation-status: CURRENT -->
<!-- d2-locale: hi -->
<!-- d2-boundary: public-ask-read-only -->
<!-- d2-boundary: postgresql-active=false -->
<!-- d2-boundary: erasure-not-global -->
<!-- d2-nonclaim: security-legal-gdpr-not-certified -->
<!-- d2-nonclaim: nlnet-not-awarded -->
# Safety, privacy और failure boundaries

**Source:** `docs/SAFETY_PRIVACY_AND_FAILURES.md@b7e6574dd7aefa2f32783ab79054fac6b3b4109f`

यह overview tests, security review या legal advice का विकल्प नहीं है।

## Epistemic safety

```text
physical L3 != strict Canon
retrieval score != evidence
model output != verified fact
migration bundle != claim evidence
successful import != activation
```

Guardian और TruthGate admission boundaries हैं। Public queries read-only हैं; explicit
ingest अलग write path है। Crystal truth या zero hallucinations guarantee नहीं करता;
unsupported state को block, label, refuse या auditable बनाना लक्ष्य है।

## Local boundary

Default installation में mandatory cloud, LLM, telemetry या analytics नहीं। SQLite ordinary
active profile है। Durable `auto` optional LadybugDB या SQLite चुनकर choice lock करता है;
Mock explicit dev/test state है। PostgreSQL/pgvector केवल operator inactive target है और
`active=false` रहता है।

## Data और optional expansion

Claims, metadata, provenance, epistemic state, graph, restrictions, erasure/audit records,
Receipts, outbox, bundles, backups और exports store हो सकते हैं। Data केवल explicit
Anthropic, remote Neo4j, Wikidata, Redis, PostgreSQL migration, wider API या external copies
से local boundary से बाहर जाता है।

## Encryption और secrets

`VELANTRIM_ENCRYPTION_KEY` selected L1 fields protect करता है; L3, backups, exports,
Receipts, logs और temporary files automatically covered नहीं। Host encryption और key
management आवश्यक हो सकते हैं। Credentials profiles, bundles, receipts, logs, issues या
Notion में नहीं रखने चाहिए।

## API, privacy और erasure

API baseline authentication और loopback उपयोग करता है। External exposure के लिए TLS,
reviewed authentication, least privilege, limits, monitoring और incident handling चाहिए।
Access, rectification, restriction, erasure और processing record engineering controls हैं,
GDPR certification नहीं। Active store erasure independent copies को globally नहीं मिटाता।

## Safe failure responses

| Class | Expected behaviour |
|---|---|
| Unsupported claim | block, label या bounded refusal |
| Read-only mutation | reject / no state change |
| Profile conflict | backend cache से पहले failure |
| Missing dependency | explicit error, no hidden Mock |
| Import failure | rollback, `active=false` |
| Evidence mismatch | verification failure |
| Receipt/audit tampering | digest/hash failure |
| Oversized migration | limits पर fail closed |
| Network exposure | explicit और authenticated only |
| Copy after erasure | separate inventory/deletion |

## Non-claims

Crystal security/legal/GDPR certification, arbitrary-scale proof, active PostgreSQL runtime,
automatic migration system, perfect truth guarantee, AGI/consciousness या awarded NLnet grant
का प्रमाण नहीं है।

Details: [Security](../../SECURITY.md), [Privacy](../../PRIVACY.md), [GDPR](../../GDPR.md),
[Failure Modes](../FAILURE_MODES.md) और [English summary](../SAFETY_PRIVACY_AND_FAILURES.md)।
