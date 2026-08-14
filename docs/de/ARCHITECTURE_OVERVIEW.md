<!-- translation-source: docs/ARCHITECTURE_OVERVIEW.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- historical-translation-source: docs/ARCHITECTURE_OVERVIEW.md@208f1c772ee3a112cb803d2413c120bef23adb05 -->
<!-- current-translation-source: docs/ARCHITECTURE_OVERVIEW.md@ad8cec8c868f64b6dfbdc3bf3087230f59c3861c -->
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
# 🇩🇪 Crystal — Architekturüberblick

**Authority:** Gemergter Code, exact CI, `docs/ai/CURRENT_STATE.md` und das implementation manifest bleiben technische Wahrheit. Diese Übersetzung erzeugt keine eigene Authority.

## Architektur

```text
exact source/document identity
→ RC-1 source/session
→ RC-2 structure
→ RC-3 passes
→ RC-4 EXTRACTED_PROPOSITION
→ RC-5 relation candidates
→ RC-6 bounded working sets / SUMMARY
→ RC-7 explicit cross-document candidate links
→ RC-9 lexical PRE-ADMISSION discovery
→ RRTIC-v1 typed inspection contract (architecture only)
→ evidence/admission boundary
→ Guardian → TruthGate
→ physical L3 → TrustSnapshot → CanonicalView
→ strict Canon read projection
```

`core.query_pipeline.query()` bleibt der public read-only path.

## Reader Capability Map

| Layer | State | Boundary |
|---|---|---|
| RC-1 | implemented | source/session identity |
| RC-2 | implemented | structure, not truth |
| RC-3 | implemented | explicit pass mechanics |
| RC-4 | implemented | proposition candidate, not evidence |
| RC-5 | implemented | relation suspicion |
| RC-6 | implemented | bounded context + caller SUMMARY |
| RC-7 | implemented | cross-document comparison candidates |
| RC-8 | research complete | retrieval/evaluation decision |
| RC-9 | implemented | deterministic BM25 candidate discovery |
| Comparator v1 | frozen FAIL | no runtime authorization |
| NLI v1 | frozen FAIL | no runtime authorization |
| RRTIC-v1 | architecture only | no provider/filter/reranker |

`dedicated_reader_core=false`; ein semantic/hybrid Reader runtime ist weder implementiert noch autorisiert.

## Erhaltene RC-1…RC-7-Kompatibilitätsgrenze

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

RC-5 hält `POSSIBLE_CONTRADICTION`, `EXCEPTION`, `QUALIFICATION`, `TENSION` als PRE-ADMISSION relation candidates. RC-7 hält exact two-sided provenance und caller rationale; automatic semantic matching bleibt abwesend.

## Post-RC-9 Evidence

RC-9 hat einen gemessenen lexikalischen Retrieval-Gap sichtbar gemacht. Comparator v1 stellte useful recall wieder her, scheiterte aber an hard-negative discrimination. NLI neutral-filter v1 verbesserte die Trennung, scheiterte jedoch an useful-recall safety. Das post-NLI reassessment klassifizierte die fehlende Capability als **relation-contract mismatch**.

RRTIC-v1 friert deshalb typed relation suspicion und zehn qualifier dimensions ein. Es führt kein model execution, filtering, reranking, evidence admission, contradiction adjudication oder Canon mutation aus.

```text
retrieval match != evidence
similarity != identity
ranking != epistemic authority
candidate discovery != candidate adjudication
NLI label != proposition identity
RRTIC suspicion != adjudicated relation
qualifier mismatch != truth decision
evaluation pass != runtime authorization
```

## Storage und Authority

| Surface | Rolle | Grenze |
|---|---|---|
| L0 | working cache | ephemeral |
| L1 | SQLite operational state | durable operational memory |
| L2 | pending/review | candidate staging |
| physical L3 | multi-status graph | not strict Canon |
| TrustSnapshot | reconciliation | deny-dominant |
| CanonicalView | trusted read | policy-allowed projection |

SQLite bleibt ordinary active local-first. PostgreSQL/pgvector bleibt inaktiv `active=false`; Import/Equivalence ist keine Activation, kein Cutover, Rollback und keine Admission Authority.

## Non-claims / Grant

Es wird kein dedicated/full autonomous Reader, semantic/hybrid Reader runtime, Reader FTS/ANN/vector DB, NLI/CrossEncoder runtime, RRTIC runtime provider, automatic identity/evidence/adjudication/Canon mutation, active PostgreSQL runtime, security/legal/GDPR certification oder awarded grant behauptet.

NLnet bleibt **submitted / under review / not awarded**; ungefähr €50,000 sind planning only.

Historischer deutscher Source: `main@208f1c772ee3a112cb803d2413c120bef23adb05`. Current German refresh audit source: `main@ad8cec8c868f64b6dfbdc3bf3087230f59c3861c`.
