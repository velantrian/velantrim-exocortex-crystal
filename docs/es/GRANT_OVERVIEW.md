<!-- translation-source: docs/PROJECT_GRANT_AND_GOVERNANCE.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- historical-translation-source: docs/PROJECT_GRANT_AND_GOVERNANCE.md@151b41c680190f7f3de729bf63e8e80a9d2285ce -->
<!-- current-translation-source: docs/PROJECT_GRANT_AND_GOVERNANCE.md@bbe6b0d3d90d80b3c669ddab5fc56aa1bfe419eb -->
<!-- d4-locale: es -->
<!-- d4-boundary: physical-l3-not-strict-canon -->
<!-- d4-boundary: retrieval-score-not-evidence -->
<!-- d4-boundary: model-output-not-source-truth -->
<!-- d4-boundary: migration-proof-not-claim-proof -->
<!-- d4-nonclaim: import-is-not-activation -->
<!-- d4-nonclaim: reader-core-not-implemented -->
<!-- d4-nonclaim: nlnet-not-awarded -->
<!-- d4-nonclaim: security-legal-gdpr-not-certified -->
<!-- d4-nonclaim: native-speaker-editorial-not-certified -->
# 🇪🇸 Crystal — resumen de financiación y gobernanza

## 🎓 Funding truth

```text
programme: NLnet NGI0 Commons Fund
proposal: submitted
review: in progress
award: not awarded
budget change: none
```

NLnet sigue **submitted / under review / not awarded**. Aproximadamente **€50,000** es únicamente planning/transparency context, no approved budget, grant award ni payment commitment.

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

Comparator v1, NLI neutral-filter v1 y RRTIC-v1 también pertenecen al existing pre-agreement research/architecture history. No pueden relabelarse después como una nueva runtime delivery financiada.

```text
reader_rc9_lexical_candidate_discovery = true
dedicated_reader_core = false
semantic_hybrid_reader_runtime = false
rrtic_runtime_authorization = false
nli_reader_runtime_filter = false
```

La expresión «dedicated Reader not implemented» se refiere al **Reader completo/autónomo**, no a las bounded RC-1…RC-7 y RC-9 layers que sí están implementadas.

## Evidence / Authority Boundary

Control RC-9 histórico conservado: Recall@5 `0.937500`, Precision@5 `0.187500`, MRR `0.895833`, useful hits `15/16`, hard-negative hits `4/4`; classification `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`.

Comparator v1 recuperó useful recall pero falló hard-negative discrimination. NLI neutral-filter v1 mejoró discrimination pero falló useful-recall safety. RRTIC-v1 congela, después del relation-contract mismatch reassessment, un typed-inspection contract.

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

Compatibilidad histórica cross-document:

```text
cross-document link != Canon relation
same-topic != same proposition
possible-same-claim != claim identity
similarity signal != identity proof
repetition across sources != corroboration
```

SQLite sigue ordinary active local-first. PostgreSQL/pgvector sigue inactivo `active=false`; Import/Equivalence no significa Activation ni funded runtime delivery.

## Future funded delta

Solo trabajo realmente ausente en el momento de un acuerdo y medible por separado puede convertirse en future funded delta. Las categorías posibles pueden incluir reproducible release/audit evidence, source-span/replay improvements, larger evaluation fixtures, operational-storage lifecycle proof, reviewer-facing evidence tooling, accessibility/localization o retrieval experiments autorizados por separado bajo preregistered gates.

El historial RC-1…RC-9 / Comparator / NLI / RRTIC ya merged no puede presupuestarse una segunda vez.

## Governance

Los cambios significativos de arquitectura/invariant empiezan con Issue/RFC y requieren executable evidence, current docs y exact CI. La presentation puede mejorar claridad, pero no crea Capability, Authority ni Funding State.

## Localization provenance

Historical Spanish grant source: `151b41c680190f7f3de729bf63e8e80a9d2285ce`. Current Spanish refresh audit source: `main@bbe6b0d3d90d80b3c669ddab5fc56aa1bfe419eb`. Los cinco idiomas que permanecen refresh-needed no se actualizan en Issue #417.