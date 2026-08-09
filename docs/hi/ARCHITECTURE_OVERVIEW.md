<!-- translation-source: docs/ARCHITECTURE_OVERVIEW.md@208f1c772ee3a112cb803d2413c120bef23adb05 -->
<!-- translation-status: CURRENT -->
<!-- d3-locale: hi -->
<!-- d3-boundary: physical-l3-not-strict-canon -->
<!-- d3-boundary: public-query-read-only -->
<!-- d3-boundary: postgresql-active=false -->
<!-- d3-nonclaim: import-is-not-activation -->
<!-- d3-nonclaim: reader-core-not-implemented -->
<!-- d3-nonclaim: nlnet-not-awarded -->
# Crystal — Architecture Overview

यह अनुवाद orientation layer है। किसी टकराव में merged code, executable tests, exact CI और अंग्रेज़ी contracts निर्णायक हैं।

## मुख्य मॉडल

```text
sources + explicit ingest
→ provenance + normalization
→ Guardian checks
→ TruthGate decision
→ operational L1 state + multi-status physical L3
→ deny-dominant strict Canon read projection
→ read-only retrieval / answer / bounded refusal
```

physical L3 में record होना strict Canon membership नहीं है। Retrieval score, vector similarity और model output स्वतंत्र evidence नहीं हैं।

## memory और review layers

- **L0:** process का ephemeral context।
- **L1:** SQLite/WAL में operational state, evidence, audit, receipts, import/review sessions और outbox।
- **L2:** candidate या quarantined claims के लिए pending/review staging; अंतिम truth layer नहीं।
- **L3:** graph-oriented multi-status storage; strict Canon के समान नहीं।
- **TrustSnapshot / CanonicalView:** deny-dominant trusted read surface।

## read/write separation

`HTTP /ask`, `CLI ask` और MCP `core.query_pipeline.query()` के माध्यम से read-only चलते हैं। Query facts, ESM, L3, outbox, episode links या embedder identity को नहीं बदल सकती। केवल explicit `ingest` Guardian और TruthGate से गुजरने वाले admission-capable write path में जाता है।

## storage profiles और portability

SQLite सामान्य active local-first profile है। पहले durable `auto` पर optional LadybugDB या SQLite चुना जा सकता है और backend/locator identity lock होती है। Ephemeral Mock पर silent fallback निषिद्ध है।

Verified PostgreSQL/pgvector path केवल inactive target तक जाता है:

```text
verified SQLite bundle
→ transactional PostgreSQL import
→ independent read-only re-hash
→ exact equivalence
→ active=false
```

Import या equivalence activation, backend selection, TruthGate admission, cutover, rollback या dual-write नहीं है। PostgreSQL सामान्य runtime composition में नहीं है।

## document reading

Source spans, document records, import sessions और dry-run/review flows implemented baseline हैं। Coverage maps, contradiction-aware rereading और document-level synthesis वाला dedicated multi-pass Reader Core implemented नहीं है।

## non-claims

Crystal AGI, consciousness, zero hallucinations, active PostgreSQL runtime, automatic switching, accepted production ANN, cutover/rollback/dual-write, security/legal/GDPR certification या awarded NLnet funding का दावा नहीं करता।

## अंग्रेज़ी स्रोत

- [पूर्ण Architecture](../ARCHITECTURE.md)
- [Storage और Authority सीमाएँ](../STORAGE_AND_AUTHORITY_BOUNDARIES.md)
- [Implementation Status](../IMPLEMENTATION_STATUS.md)
- [Inactive PostgreSQL Import](../architecture/POSTGRESQL_INACTIVE_IMPORT.md)
