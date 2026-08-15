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

यह Hindi architecture orientation current post-RC-9 / post-NLI / RRTIC-v1 truth को दर्शाती है।

## मुख्य flow

```text
Source / document
→ Reader RC-1 … RC-7 bounded artifacts
→ RC-9 lexical PRE-ADMISSION discovery
→ RRTIC-v1 typed suspicion / inspection
→ explicit evidence / review path
→ Guardian → TruthGate
→ physical L3
→ TrustSnapshot → CanonicalView STRICT
→ grounded output / bounded refusal
```

Discovery path authority path नहीं है।

## Reader layers

- **RC-1:** source/version/session + evidence-linked artifacts.
- **RC-2:** caller-supplied Structural Document Map.
- **RC-3:** deterministic bounded multi-pass mechanics.
- **RC-4:** source-linked pre-admission propositions.
- **RC-5:** same-session relation candidates.
- **RC-6:** bounded long-context strategy.
- **RC-7:** cross-document candidate links.
- **RC-9:** deterministic lexical PRE-ADMISSION candidate discovery.

```text
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
relation candidate != admitted evidence
cross-document link != Canon relation
```

Semantic comparator frozen result: `SEMANTIC_RECALL_RECOVERED_DISCRIMINATION_GATE_FAILED`.

NLI frozen result: `NLI_NEUTRAL_FILTER_GATE_FAILED`.

RRTIC-v1 architecture contract typed inspection/suspicion तक सीमित है; यह runtime provider, semantic retriever, proposition identity, evidence admission, contradiction adjudication या Canon writing नहीं करता।

```text
dedicated_reader_core=false
semantic_hybrid_reader_runtime=false
rrtic_runtime_authorization=false
nli_reader_runtime_filter=false
```

## Memory और authority

- **L0:** ephemeral working context.
- **L1:** operational SQLite/WAL state.
- **L2:** pending/review staging.
- **physical L3:** multi-status graph storage.
- **TrustSnapshot:** deny-dominant reconciliation.
- **CanonicalView:** strict trusted read projection.

```text
physical L3 != strict Canon
retrieval match != evidence
similarity != identity
ranking != epistemic authority
provenance != proof of truth
```

Guardian structural/policy boundary है; TruthGate L3 admission authority है।

## Read/write separation

`HTTP /ask`, `CLI ask` और MCP search `core.query_pipeline.query()` के माध्यम से read-only हैं। Explicit ingest अलग admission-capable write path है।

## Storage

SQLite ordinary active local-first profile है। PostgreSQL/pgvector optional inactive import/equivalence target है और `active=false` रहता है। Import/equivalence activation, cutover, rollback, dual-write या automatic switching नहीं है।

## Grant / non-claims

NLnet submitted / under review / not awarded है। Crystal dedicated Reader Core, semantic/vector Reader runtime, RRTIC runtime authorization, NLI runtime filter, universal truth, zero hallucinations या legal/security/GDPR certification का दावा नहीं करता।
