<!-- translation-source: docs/STORAGE_AND_AUTHORITY_BOUNDARIES.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- historical-translation-source: docs/STORAGE_AND_AUTHORITY_BOUNDARIES.md@208f1c772ee3a112cb803d2413c120bef23adb05 -->
<!-- current-translation-source: docs/STORAGE_AND_AUTHORITY_BOUNDARIES.md@7d03cce2c89f7a4c3fda85742eb358e6b49961f2 -->
<!-- d3-locale: fr -->
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
# 🇫🇷 Frontières du stockage et de l’autorité

Crystal n’assimile pas la présence en storage à la confiance et n’autorise pas Retrieval/Inspection à contourner Admission.

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

`core.query_pipeline.query()` est le read-only public query path. `HTTP /ask`, `CLI ask` et `MCP search` n’effectuent aucune Reader-Admission write.

## Compatibilité Reader conservée

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

RC-9 fournit uniquement deterministic lexical ranking et provenance metadata. RRTIC-v1 ajoute uniquement un vocabulaire architecture-level typed suspicion / qualifier.

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

| Surface | Rôle | Frontière |
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

Import/Equivalence est operation evidence, **pas Activation**, pas automatic switching, cutover, rollback, dual-write, Reader vector runtime ou admission authority.

## Isolation rules

Les Reader/retrieval/evaluation layers ne peuvent pas modifier un Truth Status parce qu’un candidate est bien ranked ; transformer un NLI label en proposition identity ; choisir un contradiction winner ; admettre une Evidence ; contourner Guardian/TruthGate ; ou écrire directement le strict Canon.

Comparator v1 et NLI neutral-filter v1 restent des frozen failed evaluation evidence. `dedicated_reader_core=false`; `semantic_hybrid_reader_runtime=false`; `rrtic_runtime_authorization=false`; `nli_reader_runtime_filter=false`.

## Privacy / Non-claims

Le source restriction/sensitivity context reste policy metadata ; rank, working-set filling ou RRTIC qualifier n’affaiblissent pas Privacy. Aucun active PostgreSQL Reader runtime, automatic switching, semantic/hybrid Reader runtime, FTS/ANN/vector DB, RRTIC runtime provider, automatic evidence/identity/Canon authority, security/legal/GDPR certification ou awarded funding n’est revendiqué.

NLnet reste **submitted / under review / not awarded** ; environ €50,000 est planning only.

Historical French source : `main@208f1c772ee3a112cb803d2413c120bef23adb05`. Current French refresh audit source : `main@7d03cce2c89f7a4c3fda85742eb358e6b49961f2`.