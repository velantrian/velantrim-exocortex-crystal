<!-- translation-source: docs/REVIEWER_GUIDE.md@b7e6574dd7aefa2f32783ab79054fac6b3b4109f -->
<!-- translation-status: CURRENT -->
<!-- d2-locale: hi -->
<!-- d2-boundary: public-ask-read-only -->
<!-- d2-boundary: postgresql-active=false -->
<!-- d2-boundary: erasure-not-global -->
<!-- d2-nonclaim: security-legal-gdpr-not-certified -->
<!-- d2-nonclaim: nlnet-not-awarded -->
# Reviewer Guide — Velantrim Exo-Cortex Crystal

**English source checkpoint:** `main@b7e6574dd7aefa2f32783ab79054fac6b3b4109f`  
यह maintained orientation है। Implementation evidence अभी भी `main` का code, executable
tests, exact CI, [TEST_REPORT.md](../../TEST_REPORT.md) और
[manifest](../status/implementation-manifest.json) है।

## 1. क्या review करना है

Crystal AI systems के लिए public, local-first, source-grounded और auditable memory
infrastructure है। Verified baseline में typed claims, Guardian/TruthGate, multi-status L3
पर strict Canon read projection, read-only public queries, अलग explicit ingest path,
Receipts और auditable provenance शामिल हैं।

Crystal AGI, consciousness, universal truth, zero hallucinations, active PostgreSQL runtime,
automatic switching, production multi-tenancy, security/GDPR certification या awarded NLnet
grant का दावा नहीं करता।

## 2. Baseline reproduce करें

```bash
python -m pip install --upgrade pip
pip install -e '.[dev]'
pytest tests/ --cov=. --cov-fail-under=100
python scripts/eval_gate.py --out-dir eval-artifacts
bash scripts/ring_zero_mutation_gate.sh
bash scripts/check_docs_status.sh
```

बदलने वाली metrics केवल English test report से लें।

## 3. Read/write boundary

```text
ask / receipt / MCP inspection → read-only
explicit ingest                → admission-capable write path
curator override               → explicit, attributed, audited
```

Public `ask` `core.query_pipeline.query()` उपयोग करता है और facts, ESM, L3, outbox,
episode links, embedding identity या unknown candidates को mutate नहीं कर सकता। Strict
grounding कम होने पर bounded refusal सुरक्षित expected behaviour है।

`ingest` लिखता है, पर admission evidence, claim type, policy और TruthGate पर निर्भर है।
Model output स्वयं को verified world fact प्रमाणित नहीं कर सकता।

## 4. Storage और migration

SQLite ordinary active local-first profile है। पहला durable `auto` optional LadybugDB
चुन सकता है यदि installed हो, अन्यथा SQLite; choice और non-secret locator lock होते हैं।
Ephemeral Mock में silent fallback निषिद्ध है।

PostgreSQL/pgvector अलग operator path है: verified bundle → version/TLS preflight → नया
inactive schema → serializable import → independent read-only re-hash → exact equivalence;
target `active=false` रहता है।

Import/equivalence activation, selection, TruthGate admission, strict Canon, cutover,
rollback, dual-write या production readiness नहीं है।

## 5. Security और privacy

Default operation को cloud, LLM, telemetry या analytics आवश्यक नहीं। Remote Neo4j,
Anthropic, Wikidata, Redis, PostgreSQL migration, wider API या copied backup/export केवल
explicit operator choice से boundary बढ़ाते हैं।

`VELANTRIM_ENCRYPTION_KEY` selected L1 fields की रक्षा करता है, हर L3, backup, bundle,
Receipt, log या temporary file की नहीं। Credentials और secret DSNs profiles, bundles,
receipts, logs, issues या Notion में नहीं जाने चाहिए।

Active local store से erasure backups, exports, operator copies, remote systems या third-party
data को स्वतः नहीं मिटाता।

## 6. Fail-closed checks

- Unsupported claims block, label या bounded refusal हों।
- Profile/locator conflict backend cache से पहले fail हो।
- Import failure rollback करे और `active=false` बनाए रखे।
- Evidence mismatch और Receipt/audit tampering detect हों।
- Oversized input limits पर fail हो।
- Missing optional dependency hidden durable switch न करे।
- External exposure के लिए TLS, authentication, least privilege और monitoring हों।

## 7. Checklist

- [ ] Current `main` और exact CI पहचाने गए।
- [ ] Read-only query और explicit ingest अलग हैं।
- [ ] Physical L3 और strict Canon अलग हैं।
- [ ] Inactive PostgreSQL import और activation अलग हैं।
- [ ] Network, secrets, encryption और erasure limits review हुए।
- [ ] Certification, production readiness या grant award infer नहीं किया गया।

English sources: [Reviewer Guide](../REVIEWER_GUIDE.md), [Security](../../SECURITY.md),
[Privacy](../../PRIVACY.md), [Failure Modes](../FAILURE_MODES.md) और
[Safety Summary](../SAFETY_PRIVACY_AND_FAILURES.md)।
