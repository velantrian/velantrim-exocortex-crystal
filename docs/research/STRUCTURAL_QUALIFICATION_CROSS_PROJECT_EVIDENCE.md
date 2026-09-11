# 🔬 Structural Qualification — Cross-Project Evidence from Graphiti Fractal

**Status:** RESEARCH / CROSS-PROJECT EVIDENCE / DOCS-ONLY / NON-RUNTIME  
**Date:** 2026-09-11  
**Crystal repository baseline when added:** `b48690dc8ed36d9133370c305faa948b790d70f4`  
**Source research repository:** `velantrian/Graphiti_fractal_lab`  
**Primary source line:** FM-15 → FM-16 → FM-17-pre  
**Runtime authorization:** false  
**Crystal architecture promotion:** none  
**Grant award implication:** none

> This note records research evidence and a cross-project architectural correspondence. It does **not** make Graphiti Fractal mechanisms part of Crystal, does not validate RRTIC-v1, does not authorize a semantic/structural Reader runtime, and does not create a funded NLnet deliverable.

---

## 1. Why this belongs in Crystal

Crystal already separates candidate discovery from epistemic authorization:

```text
retrieval match          != evidence
similarity               != identity
ranking                  != epistemic authority
candidate discovery      != candidate adjudication
```

That separation is central to the current Reader line. The implemented Reader baseline reaches RC-9 deterministic lexical PRE-ADMISSION candidate discovery, while later semantic-discrimination work remains research/evaluation rather than active Reader runtime.

The frozen RC-9 benchmark exposes a useful retrieval gap: high useful-candidate recall can coexist with substantial hard-negative pressure. Crystal therefore already has a concrete reason to study **candidate qualification** separately from candidate discovery.

The Graphiti Fractal FM-15/FM-16/FM-17-pre sequence studies a closely related but independently developed problem:

> A scoring mechanism may rank useful candidates ahead of weaker candidates without providing a reliable rule for deciding whether a candidate is sufficiently relevant to accept.

This makes the Graphiti work relevant to Crystal as **research donor evidence**, especially for the existing RRTIC-v1 direction.

---

## 2. Crystal-side baseline relevant to this note

### RC-9 — deterministic lexical PRE-ADMISSION candidate discovery

Crystal's current grant-scope documentation records the frozen RC-9 benchmark as:

| Metric | Frozen result |
|---|---:|
| Recall@5 | `0.937500` |
| Precision@5 | `0.187500` |
| MRR | `0.895833` |
| Paired hard-negative rate@5 | `1.000000` |
| Useful paired hits | `15 / 16` |
| Paired hard-negative hits | `4 / 4` |

Classification:

```text
LEXICAL_BASELINE_EXPOSES_MEASURED_GAP
```

Safe interpretation:

```text
candidate found
!=
candidate qualified

candidate ranked highly
!=
candidate safe to admit or treat as evidence
```

These are bounded retrieval metrics, not semantic-understanding, truth, identity, contradiction-resolution or evidence-admission metrics.

### Comparator v1 / NLI neutral-filter v1

Crystal preserves failed evaluation gates instead of converting them into runtime claims. The post-NLI reassessment concluded that the missing capability was better described as a **relation-contract mismatch** than as a simple lack of another scalar relevance score.

### RRTIC-v1

[Reader Retrieval Typed Inspection Contract v1](../architecture/READER_RETRIEVAL_TYPED_INSPECTION_CONTRACT_V1.md) is a frozen, model-free architecture contract. It lets a future inspection mechanism represent suspected relation type and explicit structural qualifier agreement/disagreement before any later discriminator is evaluated.

RRTIC-v1 is not a runtime provider. It does not itself filter, rerank, adjudicate identity, admit evidence, decide truth, or write Canon.

This boundary must remain intact.

---

## 3. External/internal donor research: Graphiti FM-15 → FM-17-pre

The relevant source is the separate experimental repository:

`velantrian/Graphiti_fractal_lab`

The donor work is not Crystal implementation evidence.

### FM-15 — pairwise CrossEncoder signal

FM-15 found a useful pairwise CrossEncoder signal on the frozen Graphiti fixture. The important bounded conclusion was not "the CrossEncoder solves relevance", but that it carried meaningful pairwise discrimination on that fixture.

Safe donor lesson:

```text
PAIRWISE RANKING SIGNAL
!=
GLOBAL QUALIFICATION POLICY
```

### FM-16 — global raw threshold infeasibility on a mixed fixture

FM-16 compared the frozen CrossEncoder and embedding score families under one global raw-threshold qualification rule across heterogeneous query types.

The reproduced result was that neither score family yielded a feasible global threshold under the frozen mixed-corpus qualification constraints.

The CrossEncoder still showed better ranking metrics than the embedding baseline on the bounded fixture, but that did not make one global raw-score threshold sufficient.

The safe interpretation is:

```text
BETTER RANKING
!=
SUFFICIENT QUALIFICATION
```

and more specifically:

```text
FM16_GLOBAL_CE_THRESHOLD = NOT_FEASIBLE_ON_FROZEN_MIXED_CORPUS
FM16_GLOBAL_EMBED_THRESHOLD = NOT_FEASIBLE_ON_FROZEN_MIXED_CORPUS
```

This result does **not** prove that all thresholding is impossible, that every query must use structural filtering, or that RRTIC-v1 is correct.

### FM-17-pre — structural oracle ceiling experiment

FM-17-pre was designed to test a distinct question:

> If query interpretation and fact structural representation were oracle-correct, would explicit structure provide measurable qualification value beyond CE-only ranking?

The frozen research arms are:

```text
A0 = frozen CE-only baseline
A1 = structural oracle qualification
A2 = structural qualification -> CE residual ranking
A3 = oracle component-identity ceiling diagnostic
```

Important boundaries:

```text
ORACLE STRUCTURAL VALUE
!=
REAL QUERY UNDERSTANDING

ORACLE FACT STRUCTURE
!=
REAL EXTRACTION ACCURACY

ORACLE VALUE
!=
DEPLOYABILITY

A3 COMPONENT RETENTION
!=
MULTI-HOP REASONING
```

As of the final integrity review, the FM-17-pre experimental gate is ready for a later one-shot offline ablation, but the real annotation and A0-A3 execution have **not** occurred.

Therefore:

```text
STRUCTURAL_VALUE = NOT_ESTABLISHED
QUERY_UNDERSTANDING = NOT_ESTABLISHED
EXTRACTION_ACCURACY = NOT_ESTABLISHED
HONEST_EMPTY = NOT_ESTABLISHED
MULTI_HOP = NOT_PROVEN
```

Primary source record:

https://github.com/velantrian/Graphiti_fractal_lab/blob/experiment/falkordblite-deterministic-memory/docs/research/fm17_pre/FM17_PRE_V1_3_1_FINAL_INTEGRITY_REVIEW_2026-09-11.md

The exact implementation SHA independently reviewed for the final FM-17-pre integrity gate was:

`080e1959fe6a3d996f2690059fcdc687dd5c832e`

Later Graphiti Lab documentation commits do not redefine that reviewed implementation SHA.

---

## 4. Cross-project mapping

The strongest correspondence is not "copy FM-17 into Crystal". It is a mapping between research questions.

| Graphiti Fractal evidence/question | Crystal analogue | Safe consequence for Crystal |
|---|---|---|
| FM-16: ranking signal can be useful while one global qualification threshold is infeasible | RC-9: useful candidates surface together with hard negatives | Keep ranking and qualification as separate evaluation dimensions |
| FM-17-pre: structural oracle before residual semantic ranking | RRTIC-v1: typed relation suspicion + structural qualifier differences | Treat structural qualification as a bounded candidate research direction, not an established mechanism |
| DIRECT vs COMPONENT vs RELATED vs NONANSWER distinctions | Reader candidate/evidence/authority separation | Avoid collapsing "related" or "supporting" into "direct answer" or evidence admission |
| `UNKNOWN != MISMATCH` / `UNRESOLVED != REJECT` | fail-closed Crystal inspection boundaries | Preserve uncertainty without silently converting it into negative truth claims |
| Integrity gate + frozen external root | Crystal's reproducibility / replay / reviewer discipline | Useful methodology donor for future evaluation artifacts, not a Reader runtime feature |

The cross-project relation can be summarized as:

```text
Crystal RC-9
broad candidate discovery
        |
        v
measured hard-negative pressure
        |
        v
RRTIC-v1
explicit typed inspection contract
        |
        +------ research question ------+
                                       |
Graphiti FM-16                        |
ranking != qualification             |
        |                              |
        v                              |
Graphiti FM-17-pre -------------------+
structural oracle -> residual CE
```

This is a **research crosswalk**, not an architecture merge.

---

## 5. What Crystal may learn from this work

### 5.1 Separate ranking quality from qualification quality

Future Reader evaluations should not assume that MRR/Recall improvements imply a safe accept/reject mechanism.

A useful evaluation can report separately:

- whether a useful candidate is found;
- where it is ranked;
- whether known non-answer/hard-negative candidates are rejected or left unresolved;
- whether useful component/context candidates are preserved;
- whether a failure is retrieval failure, qualification failure, ambiguity or evaluator failure.

This is compatible with Crystal's existing authority separation.

### 5.2 Structural inspection is a plausible donor mechanism, not yet a validated Crystal mechanism

RRTIC-v1 already freezes relation and qualifier vocabulary. FM-17-pre provides a way to ask whether an idealized structural signal has enough value to justify later real implementation work.

However:

```text
GRAPHITI FM17 POSITIVE RESULT
!=
CRYSTAL RRTIC VALIDATED
```

A positive Graphiti result would justify a Crystal-specific bounded experiment, not direct runtime adoption.

A negative Graphiti result would also need careful interpretation because the fixtures, data lifecycle, ontology and evaluation objective differ.

### 5.3 Preserve residual semantic ranking as a separate role

The FM-17-pre design explicitly separates:

```text
STRUCTURAL QUALIFICATION ROLE
from
SEMANTIC RANKING ROLE
```

That distinction is potentially useful for Crystal because RRTIC-v1 is an inspection contract, not a semantic scorer.

The donor hypothesis is therefore closer to:

```text
explicit structure handles formal compatibility where applicable
+
semantic model ranks residual unresolved candidates
```

than to:

```text
structure replaces semantics
```

No Crystal implementation decision follows from this note.

### 5.4 Preserve multi-hop / component evidence

A locally strict qualification layer can accidentally discard facts that do not directly answer a query but are useful as intermediate components.

Crystal should therefore preserve the distinction between:

```text
DIRECT ANSWER
COMPONENT / SUPPORTING CANDIDATE
RELATED CONTEXT
NONANSWER
```

if a later Reader qualification experiment evaluates structural rejection.

Retention of a component is not proof of multi-hop reasoning.

### 5.5 Evaluator integrity matters independently from retrieval quality

FM-17-pre's enforcement work yielded useful methodology lessons:

```text
PASSING TEST SUITE != THREAT MODEL COMPLETE
HASH FIELD PRESENT != HASH VERIFIED
INTERNAL HASH CONSISTENCY != FROZEN-STATE AUTHENTICITY
VALIDATOR PASS != SCIENTIFIC SUCCESS
```

These are directly compatible with Crystal's own reviewer/replay philosophy.

For future Crystal retrieval studies, a frozen corpus, expected metrics, exact model/backend identity, artifact hashes and explicit failure modes should remain separate from authority/runtime activation.

---

## 6. Relation to Crystal's grant scope

Crystal's public grant documentation currently records:

```text
NLnet NGI0 Commons Fund
status = submitted / under review / not awarded
approx. EUR 50,000 = planning context only
```

See:

- [NLnet Scope — Crystal](../GRANT_NLNET_SCOPE.md)
- [Baseline → funded delta → acceptance matrix](../grants/baseline-funded-delta-matrix.md)
- [Funding Use Plan](../grants/funding-use-plan.md)

This cross-project research note is relevant to the grant framing because Crystal's planning documents already include:

- stronger frozen/reproducible evaluation surfaces;
- model-independence / retrieval comparison work where later evidence still justifies it;
- source-span/replay and integrity-oriented acceptance evidence;
- explicit separation between evaluation evidence and runtime authorization.

The Graphiti work therefore supports the **research rationale** behind possible future Crystal evaluation work.

It does **not** change the submitted grant scope, award state, budget, or funded milestones.

### Pre-agreement accounting boundary

This document is being added before any recorded NLnet award/agreement.

Therefore it is part of Crystal's **pre-agreement research baseline**.

It must not later be represented as work newly funded by an agreement.

```text
MERGED PRE-AGREEMENT RESEARCH NOTE
!=
FUTURE FUNDED DELIVERABLE
```

If a future funded milestone includes a Crystal-specific structural-qualification or retrieval-comparison experiment, the funded delta must be work that is genuinely new at agreement time and must be reconciled against live `main` before acceptance criteria are frozen.

---

## 7. Grant-facing claim discipline

### Safe / GREEN

The following are safe when accurately dated and source-linked:

- Crystal maintains a deterministic lexical PRE-ADMISSION Reader baseline with a frozen adversarial benchmark.
- The project preserves failed evaluation gates rather than treating them as runtime success.
- Cross-project Velantrim research has produced evidence that ranking and qualification should be evaluated separately.
- A separate Graphiti laboratory has prepared a fail-closed structural-oracle ablation to test whether typed structure adds value beyond CE ranking.
- Crystal's RRTIC-v1 is a frozen architecture-only typed inspection contract that may inform a future bounded qualification study.

### Context required / YELLOW

Use only with explicit limitations:

- structural qualification;
- semantic residual ranking;
- intelligent retrieval;
- document understanding;
- relation-aware relevance.

These phrases must not imply existing Reader runtime capability or validated semantic understanding.

### Unsafe / RED as current Crystal claims

Do not claim:

- Crystal currently uses CrossEncoder reranking in Reader;
- Crystal currently runs structural qualification in Reader;
- FM-17 proves RRTIC-v1 correct;
- Crystal has solved relevance qualification;
- Crystal has validated Honest Empty;
- Crystal performs automatic semantic identity or truth adjudication;
- this research is an awarded NLnet deliverable;
- the approximate grant planning amount is approved funding.

---

## 8. Future Crystal-specific experiment, if separately authorized

A later bounded Crystal study may be justified if the live evidence still supports it.

A safe staged question would be:

> Given Crystal's PRE-ADMISSION Reader corpus and RRTIC-v1 contract, does explicit typed structural inspection reduce known hard-negative acceptance while preserving useful candidates, compared with the frozen lexical/other approved baseline?

Possible comparison roles could be studied without pre-authorizing a production design:

```text
A0 = frozen Crystal baseline
A1 = structural inspection only
A2 = structural restriction + residual semantic discriminator
```

But this is only a future research sketch.

Before execution, Crystal would need its own:

- frozen Crystal-specific corpus;
- claim/role taxonomy appropriate to Reader lifecycle;
- preregistered metrics;
- failure and abstention semantics;
- provenance and evaluator-integrity boundary;
- exact model/backend identity if any semantic model is used;
- explicit runtime non-authorization;
- independent review.

Graphiti artifacts must not be silently reused as if they were Crystal benchmark evidence.

---

## 9. Current classification

```text
CROSS_PROJECT_RESEARCH_RELEVANCE = HIGH
RRTIC_RESEARCH_RELEVANCE = HIGH
RC9_GAP_RELEVANCE = HIGH
GRANT_EVALUATION_RELEVANCE = HIGH

CRYSTAL_IMPLEMENTATION_CHANGED = NO
CRYSTAL_RUNTIME_CHANGED = NO
RRTIC_RUNTIME_AUTHORIZED = NO
SEMANTIC_HYBRID_READER_RUNTIME_AUTHORIZED = NO
CANON_AUTHORITY_CHANGED = NO
TRUTHGATE_CHANGED = NO
GUARDIAN_CHANGED = NO
GRANT_SCOPE_CHANGED = NO
GRANT_AWARD_STATUS_CHANGED = NO
FUNDED_DELIVERABLE_CREATED = NO
```

---

## 10. Source map

### Crystal

- [README](../../README.md)
- [Reader Retrieval Typed Inspection Contract v1](../architecture/READER_RETRIEVAL_TYPED_INSPECTION_CONTRACT_V1.md)
- [Crystal Memory Evaluation — Adversarial Profile v0](./MEMORY_EVAL_ADVERSARIAL_PROFILE_V0.md)
- [NLnet Scope — Crystal](../GRANT_NLNET_SCOPE.md)
- [Grant baseline → funded delta → acceptance matrix](../grants/baseline-funded-delta-matrix.md)
- [Funding Use Plan](../grants/funding-use-plan.md)

### Graphiti Fractal Lab donor research

- [FM-17-pre final integrity review](https://github.com/velantrian/Graphiti_fractal_lab/blob/experiment/falkordblite-deterministic-memory/docs/research/fm17_pre/FM17_PRE_V1_3_1_FINAL_INTEGRITY_REVIEW_2026-09-11.md)
- Independently reviewed FM-17-pre integrity implementation: `080e1959fe6a3d996f2690059fcdc687dd5c832e`
- Current laboratory branch contains later documentation-only follow-ups; the reviewed implementation SHA remains the evidence anchor above.

---

## 11. Bottom line

The Graphiti FM-15/FM-16/FM-17-pre line is relevant to Crystal because it studies the same broad boundary from another experimental surface:

```text
DISCOVERY / RANKING
!=
QUALIFICATION
!=
EVIDENCE
!=
AUTHORITY
```

The strongest present use inside Crystal is **not implementation reuse**. It is to preserve a precise research hypothesis:

> explicit typed structural compatibility may be useful as a qualification layer before residual semantic ranking, but its value must be measured independently and must not be confused with truth, evidence admission, query understanding, extraction accuracy, multi-hop reasoning, or runtime authorization.

Until a Crystal-specific experiment is separately authorized and executed, this remains cross-project research evidence only.
