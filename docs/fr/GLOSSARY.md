<!-- translation-source: docs/GLOSSARY.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- historical-translation-source: docs/GLOSSARY.md@151b41c680190f7f3de729bf63e8e80a9d2285ce -->
<!-- current-translation-source: docs/GLOSSARY.md@7d03cce2c89f7a4c3fda85742eb358e6b49961f2 -->
<!-- d4-locale: fr -->
<!-- d4-boundary: physical-l3-not-strict-canon -->
<!-- d4-boundary: retrieval-score-not-evidence -->
<!-- d4-boundary: model-output-not-source-truth -->
<!-- d4-boundary: migration-proof-not-claim-proof -->
<!-- d4-nonclaim: import-is-not-activation -->
<!-- d4-nonclaim: reader-core-not-implemented -->
<!-- d4-nonclaim: nlnet-not-awarded -->
<!-- d4-nonclaim: security-legal-gdpr-not-certified -->
<!-- d4-nonclaim: native-speaker-editorial-not-certified -->
# 🇫🇷 Glossaire Crystal

## Authority / Storage

**physical L3** — surface physique de graphe/storage multi-status ; la présence physique n’implique pas l’appartenance au **strict Canon**.  
**strict Canon** — deny-dominant trusted read projection.  
**Guardian** — structural/safety admission boundary.  
**TruthGate** — policy admission boundary, pas un objective-truth oracle.  
**TrustSnapshot / CanonicalView** — trusted reconciliation/read surfaces.  
**`active=false`** — un backend/import target n’est pas l’ordinary active runtime.

## Reader Core

**Reader Core RC-1** — bounded evidence-linked source/session skeleton.  
**Reader Core RC-2** — source-version-bound caller-supplied Structural Document Map.  
**Reader Core RC-3** — explicit deterministic multi-pass ledger.  
**Reader Core RC-4** — source-linked PRE-ADMISSION proposition candidate registration.  
**Reader Core RC-5** — same-session/same-version explicit relation candidate registry.  
**Reader Core RC-6** — bounded working sets + caller-supplied `SUMMARY` avec provenance directe vers les RC-4 leaves.  
**Reader Core RC-7** — explicit cross-document candidate links entre différentes document identities.  
**Reader Core RC-8** — décision retrieval architecture/research terminée.  
**Reader Core RC-9** — deterministic offline BM25 PRE-ADMISSION candidate discovery implémentée.  
**Dedicated/full Reader Core** — Reader semantic autonome plus large ; non implémenté (`dedicated_reader_core=false`).

## RC-4 / RC-5 Vocabulary

**`EXTRACTED_PROPOSITION`** — RC-4 fidelity class ; pas un verified fact.  
**source owner** — attribution explicite Author/Speaker/Reported-source.  
**proposition presentation category** — catégorie de présentation de la source, pas une vérification Crystal.  
**`POSSIBLE_CONTRADICTION`** — suspicion RC-5 symétrique, pas une confirmed contradiction.  
**`EXCEPTION`** — directional RC-5 limiter.  
**`QUALIFICATION`** — directional RC-5 refinement.  
**`TENSION`** — symmetric tension candidate.  
**relation rationale** — raison explicite du caller et contexte d’audit, pas un truth proof.

```text
EXTRACTED_PROPOSITION != verified fact
Reader candidate != admitted evidence
contradiction candidate != confirmed contradiction
```

RC-7 kinds : `SUPPORTS`, `CONTRADICTS`, `ELABORATES`, `REFERENCES`, `DEFINES`, `EXAMPLE_OF`, `PREREQUISITE_FOR`, `SAME_TOPIC`, `POSSIBLE_SAME_CLAIM`.

**inspection basis** — descriptive caller metadata, pas un numeric similarity/confidence/identity score.  
**cross-document link provenance** — exact two-sided session/candidate/pass/node/source/locator provenance.

## Retrieval / Evaluation

**RC-9 lexical candidate discovery** — deterministic in-memory BM25 ranking sur un Reader proposition snapshot ; produit des inspection candidates, pas des Evidence Verdicts.  
**Evaluation Surface v2** — frozen judged adversarial retrieval surface.  
**Comparator v1** — pinned multilingual semantic comparator ; recall recovered, discrimination gate failed.  
**NLI neutral-filter v1** — preregistered bidirectional filter ; discrimination improved, useful-recall safety failed.

`LEXICAL_BASELINE_EXPOSES_MEASURED_GAP` — classification RC-9 conservée.  
`SEMANTIC_RECALL_RECOVERED_DISCRIMINATION_GATE_FAILED` — classification Comparator v1.  
`NLI_NEUTRAL_FILTER_GATE_FAILED` — classification NLI v1.

## RRTIC-v1

**Reader Retrieval Typed Inspection Contract v1** — architecture-only typed inspection contract gelé après relation-contract mismatch reassessment.

Relation families : `EQUIVALENCE_SUSPECT`, `RELATED_SUSPECT`, `CONTRADICTION_SUSPECT`, `QUALIFICATION_SUSPECT`, `TOPIC_ONLY_SUSPECT`, `UNKNOWN`.

Les qualifier dimensions couvrent entity/predicate binding, argument roles, polarity, modality/quantifier, temporal/version, jurisdiction, condition direction, units/thresholds et attribution/causality. State : `MATCH | MISMATCH | UNKNOWN | NOT_APPLICABLE`.

RRTIC-v1 n’est ni un modèle, ni reranker, ni truth engine, ni Accept/Reject policy, ni runtime provider.

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

Compatibilité RC-7 historique :

```text
cross-document link != Canon relation
same-topic != same proposition
possible-same-claim != claim identity
similarity signal != identity proof
repetition across sources != corroboration
```

## Grant / Localization

**Funded delta** — nouveau travail mesurable au-delà de la verified pre-agreement baseline ; le travail déjà fusionné ne peut pas être budgeté de nouveau.  
**NLnet state** — **submitted / under review / not awarded**. Environ **€50,000** est planning only ; **budget change: none** ; award reste **not awarded**.  
**`CURRENT` translation** — current contre son source/parity marker explicite ; les anciens markers peuvent rester immutable provenance.  
**`REFRESH_NEEDED` translation** — traduction riche dont la governing English semantics a avancé.  
**Native-speaker editorial certification** — revue linguistique humaine indépendante ; son existence n’est pas impliquée par la présence d’une traduction.

Historical French glossary source : `151b41c680190f7f3de729bf63e8e80a9d2285ce`. Current French refresh audit source : `main@7d03cce2c89f7a4c3fda85742eb358e6b49961f2`.