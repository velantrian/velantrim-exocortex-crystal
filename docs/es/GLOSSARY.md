<!-- translation-source: docs/GLOSSARY.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- historical-translation-source: docs/GLOSSARY.md@151b41c680190f7f3de729bf63e8e80a9d2285ce -->
<!-- current-translation-source: docs/GLOSSARY.md@bbe6b0d3d90d80b3c669ddab5fc56aa1bfe419eb -->
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
# 🇪🇸 Glosario de Crystal

## Authority / Storage

**physical L3** — superficie física de graph/storage multi-status; la presencia física no implica pertenencia al **strict Canon**.  
**strict Canon** — deny-dominant trusted read projection.  
**Guardian** — structural/safety admission boundary.  
**TruthGate** — policy admission boundary, no objective-truth oracle.  
**TrustSnapshot / CanonicalView** — trusted reconciliation/read surfaces.  
**`active=false`** — un backend/import target no es el ordinary active runtime.

## Reader Core

**Reader Core RC-1** — bounded evidence-linked source/session skeleton.  
**Reader Core RC-2** — source-version-bound caller-supplied Structural Document Map.  
**Reader Core RC-3** — explicit deterministic multi-pass ledger.  
**Reader Core RC-4** — source-linked PRE-ADMISSION proposition candidate registration.  
**Reader Core RC-5** — same-session/same-version explicit relation candidate registry.  
**Reader Core RC-6** — bounded working sets + caller-supplied `SUMMARY` con provenance directa hacia RC-4 leaves.  
**Reader Core RC-7** — explicit cross-document candidate links entre diferentes document identities.  
**Reader Core RC-8** — decisión retrieval architecture/research completada.  
**Reader Core RC-9** — deterministic offline BM25 PRE-ADMISSION candidate discovery implementado.  
**Dedicated/full Reader Core** — Reader semantic autónomo más amplio; no implementado (`dedicated_reader_core=false`).

## RC-4 / RC-5 Vocabulary

**`EXTRACTED_PROPOSITION`** — RC-4 fidelity class; no verified fact.  
**source owner** — atribución explícita Author/Speaker/Reported-source.  
**proposition presentation category** — categoría de presentación de la fuente, no verificación de Crystal.  
**`POSSIBLE_CONTRADICTION`** — sospecha RC-5 simétrica, no confirmed contradiction.  
**`EXCEPTION`** — directional RC-5 limiter.  
**`QUALIFICATION`** — directional RC-5 refinement.  
**`TENSION`** — symmetric tension candidate.  
**relation rationale** — razón explícita del caller y contexto de auditoría, no truth proof.

```text
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
contradiction candidate != confirmed contradiction
```

RC-7 kinds: `SUPPORTS`, `CONTRADICTS`, `ELABORATES`, `REFERENCES`, `DEFINES`, `EXAMPLE_OF`, `PREREQUISITE_FOR`, `SAME_TOPIC`, `POSSIBLE_SAME_CLAIM`.

**inspection basis** — descriptive caller metadata, no numeric similarity/confidence/identity score.  
**cross-document link provenance** — exact two-sided session/candidate/pass/node/source/locator provenance.

## Retrieval / Evaluation

**RC-9 lexical candidate discovery** — deterministic in-memory BM25 ranking sobre un Reader proposition snapshot; produce inspection candidates, no Evidence Verdicts.  
**Evaluation Surface v2** — frozen judged adversarial retrieval surface.  
**Comparator v1** — pinned multilingual semantic comparator; recall recovered, discrimination gate failed.  
**NLI neutral-filter v1** — preregistered bidirectional filter; discrimination improved, useful-recall safety failed.

`LEXICAL_BASELINE_EXPOSES_MEASURED_GAP` — clasificación RC-9 preservada.  
`SEMANTIC_RECALL_RECOVERED_DISCRIMINATION_GATE_FAILED` — clasificación Comparator v1.  
`NLI_NEUTRAL_FILTER_GATE_FAILED` — clasificación NLI v1.

## RRTIC-v1

**Reader Retrieval Typed Inspection Contract v1** — architecture-only typed inspection contract congelado después del relation-contract mismatch reassessment.

Relation families: `EQUIVALENCE_SUSPECT`, `RELATED_SUSPECT`, `CONTRADICTION_SUSPECT`, `QUALIFICATION_SUSPECT`, `TOPIC_ONLY_SUSPECT`, `UNKNOWN`.

Las qualifier dimensions cubren entity/predicate binding, argument roles, polarity, modality/quantifier, temporal/version, jurisdiction, condition direction, units/thresholds y attribution/causality. State: `MATCH | MISMATCH | UNKNOWN | NOT_APPLICABLE`.

RRTIC-v1 no es model, reranker, truth engine, Accept/Reject policy ni runtime provider.

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
NLI label != proposition identity
RRTIC suspicion != adjudicated relation
qualifier mismatch != truth decision
evaluation pass != runtime authorization
```

Compatibilidad RC-7 histórica:

```text
cross-document link != Canon relation
same-topic != same proposition
possible-same-claim != claim identity
similarity signal != identity proof
repetition across sources != corroboration
```

## Grant / Localization

**Funded delta** — trabajo nuevo medible más allá de la verified pre-agreement baseline; trabajo ya merged no puede presupuestarse de nuevo.  
**NLnet state** — **submitted / under review / not awarded**. Aproximadamente **€50,000** es planning only; **budget change: none**; award sigue **not awarded**.  
**`CURRENT` translation** — current contra su source/parity marker explícito; markers antiguos pueden mantenerse como immutable provenance.  
**`REFRESH_NEEDED` translation** — traducción rica cuya governing English semantics ha avanzado.  
**Native-speaker editorial certification** — revisión lingüística humana independiente; su existencia no se implica por tener una traducción.

Historical Spanish glossary source: `151b41c680190f7f3de729bf63e8e80a9d2285ce`. Current Spanish refresh audit source: `main@bbe6b0d3d90d80b3c669ddab5fc56aa1bfe419eb`.