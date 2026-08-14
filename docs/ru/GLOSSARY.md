<!-- translation-source: docs/GLOSSARY.md@51c205fe048fd69d39fcd47b43e042a50de432bc -->
<!-- translation-status: CURRENT -->
<!-- d4-locale: ru -->
<!-- rc6-translation-source: docs/GLOSSARY.md@ed96a88369f841bdb2ffd79ca020acef174685fc -->
<!-- rc7-translation-source: docs/GLOSSARY.md@ab3ad31c437647535030e371d58f456faf14017b -->
<!-- rc7-status: CURRENT -->
<!-- current-translation-source: main@9666781d390e3276a111cb5ee1735f6606a76283 -->
# 🇷🇺 Crystal Glossary

## Authority и storage

**physical L3** — multi-status physical graph/storage surface; physical presence не означает strict Canon membership.  
**strict Canon** — deny-dominant trusted read projection после explicit admission/reconciliation.  
**Guardian** — structural/safety admission boundary.  
**TruthGate** — policy admission boundary; не objective-truth oracle.  
**TrustSnapshot / CanonicalView** — trusted grounding/read-policy surfaces.  
**`active=false`** — backend/import target не является ordinary active runtime.

## Reader Core

**Reader Core RC-1** — bounded evidence-linked source/session skeleton.  
**Reader Core RC-2** — caller-supplied, source-version-bound Structural Document Map.  
**Reader Core RC-3** — explicit deterministic multi-pass ledger.  
**Reader Core RC-4** — source-linked PRE-ADMISSION proposition candidate registration.  
**Reader Core RC-5** — same-session/same-version explicit relation candidates.  
**Reader Core RC-6** — bounded long-context working sets + caller-supplied `SUMMARY` с direct RC-4 leaf provenance.  
**Reader Core RC-7** — explicit cross-document candidate links над current RC-4 propositions из разных document identities.  
**Reader Core RC-8** — completed architecture/research retrieval decision и evaluation contract.  
**Reader Core RC-9** — implemented deterministic offline BM25 PRE-ADMISSION candidate discovery.  
**Dedicated/full Reader Core** — wider autonomous semantic Reader; not implemented (`dedicated_reader_core=false`).

## Proposition / relation terms

**`EXTRACTED_PROPOSITION`** — RC-4 fidelity class; не verified fact.  
**source owner** — author/speaker/reported-source attribution.  
**proposition presentation category** — source presentation, не Crystal verification.  
**`POSSIBLE_CONTRADICTION`** — symmetric RC-5 suspicion, не confirmed contradiction.  
**`EXCEPTION`** — directional RC-5 limiter.  
**`QUALIFICATION`** — directional refinement.  
**`TENSION`** — symmetric tension candidate.  
**relation rationale** — explicit caller reason, audit context, not truth proof.

RC-7 vocabulary: **SUPPORTS**, **CONTRADICTS**, **ELABORATES**, **REFERENCES**, **DEFINES**, **EXAMPLE_OF**, **PREREQUISITE_FOR**, **SAME_TOPIC**, **POSSIBLE_SAME_CLAIM**.

**inspection basis** — descriptive caller metadata (`EXPLICIT_SOURCE_REFERENCE`, `CALLER_COMPARISON`, `LEXICAL_SIMILARITY_SIGNAL`, `SHARED_TOPIC_SIGNAL`, `OTHER`); не numeric similarity/confidence/identity score.  
**cross-document link provenance** — exact session/candidate/pass/node/source/locator provenance обеих сторон.

## Retrieval / evaluation terms

**RC-9 lexical candidate discovery** — deterministic in-memory BM25 ranking over Reader proposition snapshot; выдаёт inspection candidates, не evidence verdicts.  
**Evaluation Surface v2** — frozen judged adversarial surface для сравнения retrieval behavior.  
**Comparator v1** — pinned multilingual semantic comparator; recall recovery succeeded, discrimination gate failed.  
**NLI neutral-filter v1** — preregistered bidirectional neutral-neutral filter; hard-negative leakage improved, useful-recall safety failed.

`LEXICAL_BASELINE_EXPOSES_MEASURED_GAP` — retained RC-9 historical classification.  
`SEMANTIC_RECALL_RECOVERED_DISCRIMINATION_GATE_FAILED` — Comparator v1 classification.  
`NLI_NEUTRAL_FILTER_GATE_FAILED` — NLI v1 classification.

## RRTIC-v1

**Reader Retrieval Typed Inspection Contract v1 (RRTIC-v1)** — frozen architecture-only typed inspection contract после relation-contract mismatch reassessment.

Relation families:

```text
EQUIVALENCE_SUSPECT
RELATED_SUSPECT
CONTRADICTION_SUSPECT
QUALIFICATION_SUSPECT
TOPIC_ONLY_SUSPECT
UNKNOWN
```

Qualifier dimensions:

```text
entity_binding
predicate_binding
argument_roles
polarity
modality_quantifier
temporal_version
jurisdiction
condition_direction
units_thresholds
attribution_causality
```

Qualifier state: `MATCH | MISMATCH | UNKNOWN | NOT_APPLICABLE`.

RRTIC-v1 не является model, reranker, truth engine, accept/reject policy или runtime provider.

## Critical distinctions

```text
Reader coverage         != comprehension proof
pass completion         != comprehension proof
working-set coverage    != comprehension proof
EXTRACTED_PROPOSITION   != verified fact
Reader candidate        != admitted evidence
relation candidate      != admitted evidence
contradiction candidate != confirmed contradiction
summary                 != evidence
retrieval match         != evidence
similarity              != identity
ranking                 != epistemic authority
NLI label               != proposition identity
RRTIC suspicion         != adjudicated relation
qualifier mismatch      != truth decision
evaluation pass         != runtime authorization
```

Historical RC-7 compatibility literals:

```text
cross-document link != Canon relation
same-topic != same proposition
possible-same-claim != claim identity
similarity signal != identity proof
repetition across sources != corroboration
```

## Grant / localization terms

**Funded delta** — new measurable work performed under agreement beyond verified existing baseline; pre-agreement merged work нельзя считать второй раз.  
**NLnet state** — **submitted / under review / not awarded**. Приблизительно €50,000 — planning only.  
**`CURRENT` translation** — localized surface current against its explicit current source marker; исторические source markers могут сохраняться отдельно как provenance.  
**`REFRESH_NEEDED` translation** — rich translation сохранён, но known to lag governing English semantics.  
**Native-speaker editorial certification** — independent qualified human language-quality review; не заявляется просто потому, что translation существует.

Historical RC-7 Russian source: `main@ab3ad31c437647535030e371d58f456faf14017b`. Current Russian refresh source: `main@9666781d390e3276a111cb5ee1735f6606a76283`.
