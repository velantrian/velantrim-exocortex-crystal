<!-- translation-source: docs/STORAGE_AND_AUTHORITY_BOUNDARIES.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- historical-translation-source: docs/STORAGE_AND_AUTHORITY_BOUNDARIES.md@208f1c772ee3a112cb803d2413c120bef23adb05 -->
<!-- current-translation-source: docs/STORAGE_AND_AUTHORITY_BOUNDARIES.md@bbe6b0d3d90d80b3c669ddab5fc56aa1bfe419eb -->
<!-- d3-locale: es -->
<!-- d3-boundary: physical-l3-not-strict-canon -->
<!-- d3-boundary: public-query-read-only -->
<!-- d3-boundary: postgresql-active=false -->
<!-- d3-nonclaim: import-is-not-activation -->
<!-- d3-nonclaim: nlnet-not-awarded -->
<!-- d3-reader: rc1-skeleton-implemented -->
<!-- d3-reader: rc2-structural-map-implemented -->
<!-- d3-reader: rc3-multi-pass-mechanics-implemented -->
<!-- d3-reader: rc4-proposition-extraction-implemented -->
<!-- d3-reader: rc5-relation-candidates-implemented -->
<!-- d3-nonclaim: dedicated-reader-core-not-implemented -->
# 🇪🇸 Límites de almacenamiento y autoridad

Crystal no equipara la presencia en storage con confianza y no permite que Retrieval/Inspection eludan Admission.

## Surface identities

```text
storage profile        = deployment identity
physical L3            = multi-status graph state
strict Canon           = trusted read projection
migration bundle       = operation evidence
retrieval score        = ranking signal
Reader artifact        = source-linked candidate
RC-9 retrieval result  = PRE-ADMISSION inspection candidate
RRTIC diagnostic       = typed inspection metadata
```

`core.query_pipeline.query()` es el read-only public query path. `HTTP /ask`, `CLI ask` y `MCP search` no realizan Reader-Admission writes.

## Compatibilidad Reader preservada

```text
RC-1 source/session
RC-2 structure
RC-3 pass ledger
RC-4 proposition
RC-5 relation candidate
RC-6 working set / SUMMARY
RC-7 cross-document candidate
RC-9 lexical candidate discovery
```

```text
coverage != comprehension proof
pass completion != comprehension proof
working-set coverage != comprehension proof
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
summary != evidence
cross-document link != Canon relation
same-topic != same proposition
possible-same-claim != claim identity
similarity signal != identity proof
repetition across sources != corroboration
```

RC-9 aporta únicamente deterministic lexical ranking y provenance metadata. RRTIC-v1 añade únicamente vocabulario architecture-level typed suspicion / qualifier.

```text
retrieval match != evidence
ranking != epistemic authority
candidate discovery != candidate adjudication
NLI label != proposition identity
RRTIC diagnostic != RC-5 registered relation
RRTIC suspicion != adjudicated relation
qualifier mismatch != truth decision
evaluation pass != runtime authorization
```

## Memory / Authority

| Superficie | Rol | Frontera |
|---|---|---|
| L0 | working cache | ephemeral |
| L1 | SQLite operational state | durable operational memory |
| L2 | pending/review | candidate state |
| physical L3 | multi-status graph | not strict Canon |
| Guardian | structural/safety | admission boundary |
| TruthGate | admission policy | not objective oracle |
| TrustSnapshot | reconciliation | deny-dominant |
| CanonicalView | read projection | trusted grounding surface |

## SQLite / PostgreSQL

```text
SQLite active local-first
→ backup / independent verification / inactive restore
→ bounded logical export
→ PostgreSQL 16 + pgvector inactive import
→ independent exact equivalence
→ active=false
```

Import/Equivalence es operation evidence, **no Activation**, no automatic switching, cutover, rollback, dual-write, Reader vector runtime ni admission authority.

## Isolation rules

Las Reader/retrieval/evaluation layers no pueden modificar un Truth Status porque un candidate esté bien ranked; convertir un NLI label en proposition identity; elegir un contradiction winner; admitir Evidence; eludir Guardian/TruthGate; ni escribir directamente strict Canon.

Comparator v1 y NLI neutral-filter v1 siguen siendo frozen failed evaluation evidence. `dedicated_reader_core=false`; `semantic_hybrid_reader_runtime=false`; `rrtic_runtime_authorization=false`; `nli_reader_runtime_filter=false`.

## Privacy / Non-claims

El source restriction/sensitivity context sigue siendo policy metadata; rank, working-set filling o RRTIC qualifier no debilitan Privacy. No se reivindican active PostgreSQL Reader runtime, automatic switching, semantic/hybrid Reader runtime, FTS/ANN/vector DB, RRTIC runtime provider, automatic evidence/identity/Canon authority, security/legal/GDPR certification ni awarded funding.

NLnet sigue **submitted / under review / not awarded**; aproximadamente €50,000 es planning only.

Historical Spanish source: `main@208f1c772ee3a112cb803d2413c120bef23adb05`. Current Spanish refresh audit source: `main@bbe6b0d3d90d80b3c669ddab5fc56aa1bfe419eb`.