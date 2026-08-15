<!-- translation-source: docs/PROJECT_GRANT_AND_GOVERNANCE.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- historical-translation-source: docs/PROJECT_GRANT_AND_GOVERNANCE.md@151b41c680190f7f3de729bf63e8e80a9d2285ce -->
<!-- current-translation-source: docs/PROJECT_GRANT_AND_GOVERNANCE.md@e436577dc5ada4692e8fe399da861a44f800e2f1 -->
<!-- d4-locale: it -->
<!-- d4-boundary: physical-l3-not-strict-canon -->
<!-- d4-boundary: retrieval-score-not-evidence -->
<!-- d4-boundary: model-output-not-source-truth -->
<!-- d4-boundary: migration-proof-not-claim-proof -->
<!-- d4-nonclaim: import-is-not-activation -->
<!-- d4-nonclaim: reader-core-not-implemented -->
<!-- d4-nonclaim: nlnet-not-awarded -->
<!-- d4-nonclaim: security-legal-gdpr-not-certified -->
<!-- d4-nonclaim: native-speaker-editorial-not-certified -->
# 🇮🇹 Crystal — panoramica di finanziamento e governance

## 🎓 Funding truth

```text
programme: NLnet NGI0 Commons Fund
proposal: submitted
review: in progress
award: not awarded
budget change: none
```

NLnet resta **submitted / under review / not awarded**. Circa **€50,000** è soltanto planning/transparency context, non approved budget, grant award o payment commitment.

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

Comparator v1, NLI neutral-filter v1 e RRTIC-v1 appartengono anch’essi alla existing pre-agreement research/architecture history. Non possono essere rilabelizzati in seguito come una nuova runtime delivery finanziata.

```text
reader_rc9_lexical_candidate_discovery = true
dedicated_reader_core = false
semantic_hybrid_reader_runtime = false
rrtic_runtime_authorization = false
nli_reader_runtime_filter = false
```

L’espressione «dedicated Reader not implemented» riguarda il **Reader completo/autonomo**, non le bounded RC-1…RC-7 e RC-9 layers che sono implementate.

## Evidence / Authority Boundary

Control RC-9 storico conservato: Recall@5 `0.937500`, Precision@5 `0.187500`, MRR `0.895833`, useful hits `15/16`, hard-negative hits `4/4`; classification `LEXICAL_BASELINE_EXPOSES_MEASURED_GAP`.

Comparator v1 ha recuperato useful recall ma ha fallito hard-negative discrimination: `SEMANTIC_RECALL_RECOVERED_DISCRIMINATION_GATE_FAILED`. NLI neutral-filter v1 ha migliorato discrimination ma ha fallito useful-recall safety: `NLI_NEUTRAL_FILTER_GATE_FAILED`. RRTIC-v1 congela, dopo il relation-contract mismatch reassessment, un typed-inspection contract architecture-only.

```text
physical L3 != strict Canon
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
relation candidate != admitted evidence
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

Compatibilità storica cross-document:

```text
cross-document link != Canon relation
same-topic != same proposition
possible-same-claim != claim identity
similarity signal != identity proof
repetition across sources != corroboration
```

SQLite resta ordinary active local-first. PostgreSQL/pgvector resta inattivo `active=false`; Import/Equivalence non significa Activation né funded runtime delivery.

## Future funded delta

Solo lavoro realmente assente al momento di un accordo e misurabile separatamente può diventare future funded delta. Le categorie possibili possono includere reproducible release/audit evidence, source-span/replay improvements, larger evaluation fixtures, operational-storage lifecycle proof, reviewer-facing evidence tooling, accessibility/localization o retrieval experiments autorizzati separatamente sotto preregistered gates.

La storia RC-1…RC-9 / Comparator / NLI / RRTIC già merged non può essere budgettata una seconda volta.

## Governance

I cambiamenti significativi di architecture/invariant iniziano con Issue/RFC e richiedono executable evidence, current docs ed exact CI. La presentation può migliorare la chiarezza, ma non crea Capability, Authority o Funding State.

## Localization provenance

Historical Italian grant source: `151b41c680190f7f3de729bf63e8e80a9d2285ce`. Current Italian refresh audit source: `main@e436577dc5ada4692e8fe399da861a44f800e2f1`. I quattro linguaggi che restano refresh-needed non vengono aggiornati in Issue #419.
