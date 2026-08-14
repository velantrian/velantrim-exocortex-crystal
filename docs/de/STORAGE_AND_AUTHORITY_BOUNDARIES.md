<!-- translation-source: docs/STORAGE_AND_AUTHORITY_BOUNDARIES.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- historical-translation-source: docs/STORAGE_AND_AUTHORITY_BOUNDARIES.md@208f1c772ee3a112cb803d2413c120bef23adb05 -->
<!-- current-translation-source: docs/STORAGE_AND_AUTHORITY_BOUNDARIES.md@ad8cec8c868f64b6dfbdc3bf3087230f59c3861c -->
<!-- d3-locale: de -->
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
# 🇩🇪 Storage- und Authority-Grenzen

Crystal setzt Storage Presence nicht mit Vertrauen gleich und erlaubt Retrieval/Inspection nicht, Admission zu umgehen.

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

`core.query_pipeline.query()` ist der read-only public query path. `HTTP /ask`, `CLI ask` und `MCP search` führen keine Reader-Admission-Writes aus.

## Erhaltene Reader-Kompatibilität

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

RC-9 liefert nur deterministisches lexikalisches Ranking und Provenienz-Metadaten. RRTIC-v1 fügt nur architecture-level typed suspicion / qualifier vocabulary hinzu.

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

| Surface | Rolle | Grenze |
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

Import/Equivalence ist operation evidence, **keine Activation**, kein automatic switching, cutover, rollback, dual-write, Reader vector runtime und keine admission authority.

## Isolation rules

Reader-, retrieval- und evaluation layers dürfen keinen Truth-Status verändern, nur weil ein Candidate hoch gerankt ist; ein NLI label nicht in proposition identity umwandeln; keinen contradiction winner wählen; keine Evidence admitten; Guardian/TruthGate nicht umgehen und strict Canon nicht schreiben.

Comparator v1 und NLI neutral-filter v1 bleiben eingefrorene failed evaluation evidence. `dedicated_reader_core=false`; `semantic_hybrid_reader_runtime=false`; `rrtic_runtime_authorization=false`.

## Privacy / Non-claims

Source restriction/sensitivity context bleibt Policy-Metadatum; Rank, Working-Set-Füllung oder RRTIC qualifier schwächen Privacy nicht. Es wird keine aktive PostgreSQL Reader runtime, kein automatic switching, kein semantic/hybrid Reader runtime, keine FTS/ANN/vector DB, kein RRTIC runtime provider, keine automatic evidence/identity/Canon authority, keine security/legal/GDPR certification und kein awarded funding behauptet.

NLnet bleibt **submitted / under review / not awarded**; ungefähr €50,000 sind planning only.

Historischer deutscher Source: `main@208f1c772ee3a112cb803d2413c120bef23adb05`. Current German refresh audit source: `main@ad8cec8c868f64b6dfbdc3bf3087230f59c3861c`.
