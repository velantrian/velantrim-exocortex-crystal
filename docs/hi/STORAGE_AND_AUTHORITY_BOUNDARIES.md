<!-- translation-source: docs/STORAGE_AND_AUTHORITY_BOUNDARIES.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- d3-locale: hi -->
<!-- d3-boundary: physical-l3-not-strict-canon -->
<!-- d3-boundary: public-query-read-only -->
<!-- d3-boundary: postgresql-active=false -->
<!-- d3-nonclaim: import-is-not-activation -->
<!-- d3-nonclaim: reader-core-not-implemented -->
<!-- d3-nonclaim: dedicated-reader-core-not-implemented -->
<!-- d3-nonclaim: nlnet-not-awarded -->
<!-- d3-reader: rc1-skeleton-implemented -->
<!-- d3-reader: rc2-structural-map-implemented -->
<!-- d3-reader: rc3-multi-pass-mechanics-implemented -->
<!-- d3-reader: rc4-proposition-extraction-implemented -->
<!-- d3-reader: rc5-relation-candidates-implemented -->
# Storage और Authority सीमाएँ

Crystal में persistence, retrieval और epistemic authority अलग identities हैं।

```text
storage profile = deployment identity
physical L3 = multi-status storage
strict Canon = trusted read projection
retrieval score = ranking signal
Reader candidate != admitted evidence
migration proof != claim proof
```

## Authority firewall

```text
coverage != comprehension proof
pass completion != comprehension proof
EXTRACTED_PROPOSITION != verified fact
retrieval match != evidence
similarity != identity
ranking != epistemic authority
repetition != corroboration
candidate discovery != candidate adjudication
Reader candidate != admitted evidence
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
NLI label != proposition identity
RRTIC suspicion != adjudicated relation
physical L3 != strict Canon
```

Guardian structural integrity/policy boundary है, truth oracle नहीं। TruthGate L3 admission authority है। TrustSnapshot deny-dominant reconciliation और CanonicalView strict trusted projection देते हैं। Trace/provenance audit evidence है, truth proof नहीं।

## Reader और storage interaction

RC-1…RC-7 bounded Reader artifacts तथा RC-9 lexical PRE-ADMISSION discovery केवल candidates/inspection surfaces देते हैं। Frozen semantic comparator `SEMANTIC_RECALL_RECOVERED_DISCRIMINATION_GATE_FAILED` और NLI result `NLI_NEUTRAL_FILTER_GATE_FAILED` runtime authorization नहीं देते। RRTIC-v1 architecture-only है।

```text
RC-1
RC-2
RC-3
RC-4
RC-5
dedicated_reader_core=false
semantic_hybrid_reader_runtime=false
rrtic_runtime_authorization=false
nli_reader_runtime_filter=false
```

## Active / inactive storage truth

SQLite सामान्य active local-first profile है। PostgreSQL 16 + pgvector optional inactive target है:

```text
verified bundle
→ transactional inactive import
→ independent exact-state equivalence
→ active=false
```

Successful import/equivalence activation, backend selection, TruthGate admission, cutover, rollback, fencing या dual-write नहीं है।

## Read/write separation

Public queries `core.query_pipeline.query()` से read-only जाती हैं। Explicit `ingest` अलग admission-capable write path है।

## Secrets और copies

Credentials profiles, bundles, receipts, logs, GitHub या Notion में नहीं रखने चाहिए। Backup/export/migration independent copies बना सकते हैं; active-store erasure उन्हें globally delete नहीं करता। Selected L1 encryption universal encryption नहीं है।

## Non-claims

Crystal active PostgreSQL runtime, automatic backend switching, dedicated Reader Core, semantic/vector Reader runtime, RRTIC/NLI runtime authorization, production multi-tenancy, universal truth या legal/security/GDPR certification का दावा नहीं करता। NLnet submitted / under review / not awarded है।
