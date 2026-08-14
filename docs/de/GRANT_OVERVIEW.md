<!-- translation-source: docs/PROJECT_GRANT_AND_GOVERNANCE.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- historical-translation-source: docs/PROJECT_GRANT_AND_GOVERNANCE.md@151b41c680190f7f3de729bf63e8e80a9d2285ce -->
<!-- current-translation-source: docs/PROJECT_GRANT_AND_GOVERNANCE.md@ad8cec8c868f64b6dfbdc3bf3087230f59c3861c -->
<!-- d4-locale: de -->
<!-- d4-boundary: physical-l3-not-strict-canon -->
<!-- d4-boundary: retrieval-score-not-evidence -->
<!-- d4-boundary: model-output-not-source-truth -->
<!-- d4-boundary: migration-proof-not-claim-proof -->
<!-- d4-nonclaim: import-is-not-activation -->
<!-- d4-nonclaim: reader-core-not-implemented -->
<!-- d4-nonclaim: nlnet-not-awarded -->
<!-- d4-nonclaim: security-legal-gdpr-not-certified -->
<!-- d4-nonclaim: native-speaker-editorial-not-certified -->
# 🇩🇪 Crystal — Förder- und Governance-Überblick

## 🎓 Funding truth

```text
programme: NLnet NGI0 Commons Fund
proposal: submitted
review: in progress
award: not awarded
budget change: none
```

NLnet bleibt **submitted / under review / not awarded**. Ungefähr **€50,000** sind ausschließlich planning/transparency context, kein approved budget, grant award oder payment commitment.

## 🧬 Existing baseline

```text
RC-1 = bounded source/session skeleton
RC-2 = bounded structural map
RC-3 = bounded pass mechanics
RC-4 = bounded proposition candidates
RC-5 = bounded relation candidates
RC-6 = bounded long-context working sets
RC-7 = explicit cross-document candidates
RC-8 = completed architecture/research decision
RC-9 = implemented lexical PRE-ADMISSION discovery
```

Comparator v1, NLI neutral-filter v1 und RRTIC-v1 gehören ebenfalls zur existing pre-agreement research/architecture history. Sie dürfen später nicht als neu finanzierte Runtime-Lieferung umetikettiert werden.

```text
reader_rc9_lexical_candidate_discovery = true
dedicated_reader_core = false
semantic_hybrid_reader_runtime = false
rrtic_runtime_authorization = false
```

Der Ausdruck „dedicated Reader not implemented“ bezieht sich auf den **vollständigen/autonomen Reader**, nicht auf die bounded RC-1…RC-7- und RC-9-Layer, die implementiert sind.

## Evidence / Authority Boundary

Erhaltener RC-9 historical control: Recall@5 `0.937500`, Precision@5 `0.187500`, MRR `0.895833`, useful hits `15/16`, hard-negative hits `4/4`; classification `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`.

Comparator v1 stellte useful recall wieder her, scheiterte aber an hard-negative discrimination. NLI neutral-filter v1 verbesserte discrimination, scheiterte aber an useful-recall safety. RRTIC-v1 friert nach dem relation-contract mismatch reassessment einen typed-inspection Vertrag ein.

```text
physical L3 != strict Canon
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
contradiction candidate != confirmed contradiction
retrieval match != evidence
similarity != identity
ranking != epistemic authority
candidate discovery != candidate adjudication
NLI label != proposition identity
RRTIC suspicion != adjudicated relation
qualifier mismatch != truth decision
evaluation pass != runtime authorization
```

Historische Cross-document-Kompatibilität bleibt:

```text
cross-document link != Canon relation
same-topic != same proposition
possible-same-claim != claim identity
similarity signal != identity proof
repetition across sources != corroboration
```

SQLite bleibt ordinary active local-first. PostgreSQL/pgvector bleibt inaktiv `active=false`; Import/Equivalence bedeutet weder Activation noch funded runtime delivery.

## Future funded delta

Nur Arbeit, die zum Zeitpunkt einer Vereinbarung tatsächlich fehlt und separat messbar ist, kann future funded delta werden. Mögliche Kategorien können reproduzierbare Release-/Audit-Evidence, Source-Span-/Replay-Verbesserungen, größere Evaluation-Fixtures, Operational-Storage-Lifecycle-Proof, reviewer-facing Evidence Tooling, Accessibility/Localization oder separat autorisierte Retrieval-Experimente unter preregistered gates umfassen.

Bereits gemergte RC-1…RC-9 / Comparator / NLI / RRTIC-Historie darf nicht doppelt budgetiert werden.

## Governance

Bedeutende Architektur-/Invariant-Änderungen beginnen mit Issue/RFC und benötigen executable evidence, current docs und exact CI. Präsentation darf Klarheit verbessern, aber keine Capability, Authority oder Funding State erzeugen.

## Localization provenance

Historischer deutscher Grant-Source: `151b41c680190f7f3de729bf63e8e80a9d2285ce`. Current German refresh audit source: `main@ad8cec8c868f64b6dfbdc3bf3087230f59c3861c`. Die übrigen sieben refresh-needed Sprachen werden durch Issue #412 nicht aktualisiert.
