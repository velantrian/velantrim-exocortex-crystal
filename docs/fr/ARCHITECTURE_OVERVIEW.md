<!-- translation-source: docs/ARCHITECTURE_OVERVIEW.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- historical-translation-source: docs/ARCHITECTURE_OVERVIEW.md@208f1c772ee3a112cb803d2413c120bef23adb05 -->
<!-- current-translation-source: docs/ARCHITECTURE_OVERVIEW.md@7d03cce2c89f7a4c3fda85742eb358e6b49961f2 -->
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
# 🇫🇷 Crystal — vue d’ensemble de l’architecture

**Authority :** le code fusionné, l’exact CI, `docs/ai/CURRENT_STATE.md` et l’implementation manifest restent la vérité technique. Cette traduction ne crée aucune Authority propre.

## Architecture

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

`core.query_pipeline.query()` reste le public read-only path.

## Reader Capability Map

| Layer | État | Frontière |
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

`dedicated_reader_core=false`; un semantic/hybrid Reader runtime n’est ni implémenté ni autorisé.

## Frontière de compatibilité RC-1…RC-7 conservée

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

RC-5 conserve `POSSIBLE_CONTRADICTION`, `EXCEPTION`, `QUALIFICATION`, `TENSION` comme PRE-ADMISSION relation candidates. RC-7 conserve exact two-sided provenance et caller rationale ; automatic semantic matching reste absent.

## Post-RC-9 Evidence

RC-9 a exposé un lexical retrieval gap mesuré. Comparator v1 a rétabli useful recall mais a échoué sur hard-negative discrimination. NLI neutral-filter v1 a amélioré la discrimination mais a échoué sur useful-recall safety. Le post-NLI reassessment a classé la capability manquante comme **relation-contract mismatch**.

RRTIC-v1 gèle donc typed relation suspicion et dix qualifier dimensions. Il n’exécute aucun model execution, filtering, reranking, evidence admission, contradiction adjudication ou Canon mutation.

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

## Storage et Authority

| Surface | Rôle | Frontière |
|---|---|---|
| L0 | working cache | ephemeral |
| L1 | SQLite operational state | durable operational memory |
| L2 | pending/review | candidate staging |
| physical L3 | multi-status graph | not strict Canon |
| TrustSnapshot | reconciliation | deny-dominant |
| CanonicalView | trusted read | policy-allowed projection |

SQLite reste ordinary active local-first. PostgreSQL/pgvector reste inactif `active=false`; Import/Equivalence n’est ni Activation, ni cutover/rollback, ni Admission Authority.

## Non-claims / Grant

Aucun dedicated/full autonomous Reader, semantic/hybrid Reader runtime, Reader FTS/ANN/vector DB, NLI/CrossEncoder runtime, RRTIC runtime provider, automatic identity/evidence/adjudication/Canon mutation, active PostgreSQL runtime, security/legal/GDPR certification ou awarded grant n’est revendiqué.

NLnet reste **submitted / under review / not awarded** ; environ €50,000 est planning only.

Historical French source : `main@208f1c772ee3a112cb803d2413c120bef23adb05`. Current French refresh audit source : `main@7d03cce2c89f7a4c3fda85742eb358e6b49961f2`.