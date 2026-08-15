<!-- translation-source: docs/ARCHITECTURE_OVERVIEW.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- historical-translation-source: docs/ARCHITECTURE_OVERVIEW.md@208f1c772ee3a112cb803d2413c120bef23adb05 -->
<!-- current-translation-source: docs/ARCHITECTURE_OVERVIEW.md@bbe6b0d3d90d80b3c669ddab5fc56aa1bfe419eb -->
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
# 🇪🇸 Crystal — visión general de arquitectura

**Authority:** el código merged, el exact CI, `docs/ai/CURRENT_STATE.md` y el implementation manifest siguen siendo la verdad técnica. Esta traducción no crea Authority propia.

## Arquitectura

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

`core.query_pipeline.query()` sigue siendo el public read-only path.

## Reader Capability Map

| Layer | Estado | Frontera |
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

`dedicated_reader_core=false`; un semantic/hybrid Reader runtime no está implementado ni autorizado.

## Frontera de compatibilidad RC-1…RC-7 preservada

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

RC-5 conserva `POSSIBLE_CONTRADICTION`, `EXCEPTION`, `QUALIFICATION`, `TENSION` como PRE-ADMISSION relation candidates. RC-7 conserva exact two-sided provenance y caller rationale; automatic semantic matching sigue ausente.

## Post-RC-9 Evidence

RC-9 expuso un lexical retrieval gap medido. Comparator v1 recuperó useful recall pero falló hard-negative discrimination. NLI neutral-filter v1 mejoró discrimination pero falló useful-recall safety. El post-NLI reassessment clasificó la capability ausente como **relation-contract mismatch**.

RRTIC-v1 congela typed relation suspicion y diez qualifier dimensions. No ejecuta model execution, filtering, reranking, evidence admission, contradiction adjudication ni Canon mutation.

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

## Storage y Authority

| Superficie | Rol | Frontera |
|---|---|---|
| L0 | working cache | ephemeral |
| L1 | SQLite operational state | durable operational memory |
| L2 | pending/review | candidate staging |
| physical L3 | multi-status graph | not strict Canon |
| TrustSnapshot | reconciliation | deny-dominant |
| CanonicalView | trusted read | policy-allowed projection |

SQLite sigue ordinary active local-first. PostgreSQL/pgvector sigue inactivo `active=false`; Import/Equivalence no es Activation, cutover/rollback ni Admission Authority.

## Non-claims / Grant

No se reivindican dedicated/full autonomous Reader, semantic/hybrid Reader runtime, Reader FTS/ANN/vector DB, NLI/CrossEncoder runtime, RRTIC runtime provider, automatic identity/evidence/adjudication/Canon mutation, active PostgreSQL runtime, security/legal/GDPR certification ni awarded grant.

NLnet sigue **submitted / under review / not awarded**; aproximadamente €50,000 es planning only.

Historical Spanish source: `main@208f1c772ee3a112cb803d2413c120bef23adb05`. Current Spanish refresh audit source: `main@bbe6b0d3d90d80b3c669ddab5fc56aa1bfe419eb`.