<!-- translation-source: docs/STORAGE_AND_AUTHORITY_BOUNDARIES.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- historical-translation-source: docs/STORAGE_AND_AUTHORITY_BOUNDARIES.md@208f1c772ee3a112cb803d2413c120bef23adb05 -->
<!-- current-translation-source: docs/STORAGE_AND_AUTHORITY_BOUNDARIES.md@e436577dc5ada4692e8fe399da861a44f800e2f1 -->
<!-- d3-locale: it -->
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
# 🇮🇹 Limiti dello storage e dell’autorità

Crystal non equipara la presenza nello storage alla fiducia e non permette a Retrieval/Inspection di aggirare Admission.

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

`core.query_pipeline.query()` è il read-only public query path. `HTTP /ask`, `CLI ask` e `MCP search` non eseguono Reader-Admission writes.

## Compatibilità Reader preservata

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

RC-9 fornisce soltanto deterministic lexical ranking e provenance metadata. RRTIC-v1 aggiunge soltanto vocabulary architecture-level per typed suspicion / qualifier.

```text
retrieval match != evidence
similarity != identity
ranking != epistemic authority
candidate discovery != candidate adjudication
NLI label != proposition identity
RRTIC diagnostic != RC-5 registered relation
RRTIC suspicion != adjudicated relation
qualifier mismatch != truth decision
evaluation pass != runtime authorization
```

## Memory / Authority

| Superficie | Ruolo | Boundary |
|---|---|---|
| L0 | working cache | ephemeral |
| L1 | SQLite operational state | durable operational memory |
| L2 | pending/review | candidate state |
| physical L3 | multi-status graph | not strict Canon |
| Guardian | structural integrity / structural policy boundary | not truth oracle |
| TruthGate | L3 admission authority | not objective oracle |
| TrustSnapshot | reconciliation | deny-dominant |
| CanonicalView | read projection | strict trusted grounding surface |
| TRACE / provenance | audit / replay evidence | provenance != proof of truth |

## SQLite / PostgreSQL

```text
SQLite active local-first
→ backup / independent verification / inactive restore
→ bounded logical export
→ PostgreSQL 16 + pgvector inactive import
→ independent exact equivalence
→ active=false
```

Import/Equivalence è operation evidence, **non Activation**: nessun automatic switching, cutover, rollback, dual-write, Reader vector runtime o admission authority.

## Isolation rules

Le Reader/retrieval/evaluation layers non possono modificare un Truth Status perché un candidate è ben ranked; convertire un NLI label in proposition identity; scegliere un contradiction winner; ammettere Evidence; aggirare Guardian/TruthGate; o scrivere direttamente strict Canon.

Comparator v1 e NLI neutral-filter v1 restano frozen failed evaluation evidence. `dedicated_reader_core=false`; `semantic_hybrid_reader_runtime=false`; `rrtic_runtime_authorization=false`; `nli_reader_runtime_filter=false`.

## Privacy / Non-claims

Il source restriction/sensitivity context resta policy metadata; ranking, working-set filling o un RRTIC qualifier non indeboliscono Privacy. Non vengono rivendicati active PostgreSQL Reader runtime, automatic switching, semantic/hybrid Reader runtime, FTS/ANN/vector DB, RRTIC runtime provider, automatic evidence/identity/Canon authority, security/legal/GDPR certification o awarded funding.

NLnet resta **submitted / under review / not awarded**; circa €50,000 è planning only.

Historical Italian source: `main@208f1c772ee3a112cb803d2413c120bef23adb05`. Current Italian refresh audit source: `main@e436577dc5ada4692e8fe399da861a44f800e2f1`.
