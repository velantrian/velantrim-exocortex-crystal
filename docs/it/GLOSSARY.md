<!-- translation-source: docs/GLOSSARY.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- historical-translation-source: docs/GLOSSARY.md@151b41c680190f7f3de729bf63e8e80a9d2285ce -->
<!-- current-translation-source: docs/GLOSSARY.md@e436577dc5ada4692e8fe399da861a44f800e2f1 -->
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
# 🇮🇹 Glossario Crystal

## Authority / Storage

**physical L3** — superficie fisica graph/storage multi-status; la presenza fisica non implica appartenenza allo **strict Canon**.  
**strict Canon** — deny-dominant trusted read projection.  
**Guardian** — structural integrity / structural policy boundary; non è un truth oracle.  
**TruthGate** — L3 admission authority; non è un objective-truth oracle.  
**TrustSnapshot / CanonicalView** — trusted reconciliation/read surfaces; CanonicalView è la strict trusted read-time projection.  
**TRACE / provenance** — audit/replay provenance; provenance != proof of truth.  
**`active=false`** — un backend/import target non è l’ordinary active runtime.

## Reader Core

**Reader Core RC-1** — bounded evidence-linked source/session skeleton.  
**Reader Core RC-2** — source-version-bound caller-supplied Structural Document Map.  
**Reader Core RC-3** — explicit deterministic multi-pass ledger.  
**Reader Core RC-4** — source-linked PRE-ADMISSION proposition candidate registration.  
**Reader Core RC-5** — same-session/same-version explicit relation candidate registry.  
**Reader Core RC-6** — bounded working sets + caller-supplied `SUMMARY` con provenance diretta verso RC-4 leaves.  
**Reader Core RC-7** — explicit cross-document candidate links tra differenti document identities.  
**Reader Core RC-8** — decisione retrieval architecture/research completata.  
**Reader Core RC-9** — deterministic offline BM25 PRE-ADMISSION candidate discovery implementato.  
**Dedicated/full Reader Core** — Reader semantic autonomo più ampio; non implementato (`dedicated_reader_core=false`).

## RC-4 / RC-5 Vocabulary

**`EXTRACTED_PROPOSITION`** — RC-4 fidelity class; non un verified fact.  
**source owner** — attribuzione esplicita Author/Speaker/Reported-source.  
**proposition presentation category** — categoria di presentazione della fonte, non verifica Crystal.  
**`POSSIBLE_CONTRADICTION`** — sospetto RC-5 simmetrico, non confirmed contradiction.  
**`EXCEPTION`** — directional RC-5 limiter.  
**`QUALIFICATION`** — directional RC-5 refinement.  
**`TENSION`** — symmetric tension candidate.  
**relation rationale** — ragione esplicita del caller e contesto di audit, non truth proof.

```text
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
relation candidate != admitted evidence
contradiction candidate != confirmed contradiction
```

RC-7 kinds: `SUPPORTS`, `CONTRADICTS`, `ELABORATES`, `REFERENCES`, `DEFINES`, `EXAMPLE_OF`, `PREREQUISITE_FOR`, `SAME_TOPIC`, `POSSIBLE_SAME_CLAIM`.

**inspection basis** — descriptive caller metadata, non numeric similarity/confidence/identity score.  
**cross-document link provenance** — exact two-sided session/candidate/pass/node/source/locator provenance.

## Retrieval / Evaluation

**RC-9 lexical candidate discovery** — deterministic in-memory BM25 ranking su un Reader proposition snapshot; produce inspection candidates, non Evidence Verdicts.  
**Evaluation Surface v2** — frozen judged adversarial retrieval surface.  
**Comparator v1** — pinned multilingual semantic comparator; recall recovered, discrimination gate failed.  
**NLI neutral-filter v1** — preregistered bidirectional filter; discrimination improved, useful-recall safety failed.

`LEXICAL_BASELINE_EXPOSES_MEASURED_GAP` — classification RC-9 preservata.  
`SEMANTIC_RECALL_RECOVERED_DISCRIMINATION_GATE_FAILED` — classification Comparator v1.  
`NLI_NEUTRAL_FILTER_GATE_FAILED` — classification NLI v1.

## RRTIC-v1

**Reader Retrieval Typed Inspection Contract v1** — architecture-only typed inspection contract congelato dopo il relation-contract mismatch reassessment.

Relation families: `EQUIVALENCE_SUSPECT`, `RELATED_SUSPECT`, `CONTRADICTION_SUSPECT`, `QUALIFICATION_SUSPECT`, `TOPIC_ONLY_SUSPECT`, `UNKNOWN`.

Le qualifier dimensions coprono entity/predicate binding, argument roles, polarity, modality/quantifier, temporal/version, jurisdiction, condition direction, units/thresholds e attribution/causality. State: `MATCH | MISMATCH | UNKNOWN | NOT_APPLICABLE`.

RRTIC-v1 non è model, reranker, truth engine, Accept/Reject policy, Evidence Admission, contradiction adjudication o runtime provider.

## Critical distinctions

```text
coverage != comprehension proof
pass completion != comprehension proof
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

Compatibilità RC-7 storica:

```text
cross-document link != Canon relation
same-topic != same proposition
possible-same-claim != claim identity
similarity signal != identity proof
repetition across sources != corroboration
```

## Grant / Localization

**Funded delta** — lavoro nuovo misurabile oltre la verified pre-agreement baseline; il lavoro già merged non può essere budgettato di nuovo.  
**NLnet state** — **submitted / under review / not awarded**. Circa **€50,000** è planning only; **budget change: none**; award resta **not awarded**.  
**`CURRENT` translation** — current rispetto al suo source/parity marker esplicito; marker storici possono restare come immutable provenance.  
**`REFRESH_NEEDED` translation** — traduzione ricca la cui governing English semantics è avanzata.  
**Native-speaker editorial certification** — revisione linguistica umana indipendente; non è implicata dall’esistenza di una traduzione.

Historical Italian glossary source: `151b41c680190f7f3de729bf63e8e80a9d2285ce`. Current Italian refresh audit source: `main@e436577dc5ada4692e8fe399da861a44f800e2f1`.
