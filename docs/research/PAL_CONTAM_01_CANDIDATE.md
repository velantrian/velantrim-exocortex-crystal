# PAL-CONTAM-01 — Interaction-Induced Adaptation Bias

> **Status:** CANDIDATE EXPERIMENT · NOT RUN · NOT AUTHORIZED · NOT ARCHITECTURE DECISION · NOT RUNTIME CHANGE

## Research question

Can a personal adapter learn prior model framing indirectly through user-authored training data when the user's wording was produced after model exposure?

This is distinct from actor/authority substitution. The user may genuinely author the training sample while the sample is still causally shaped by prior model framing.

Candidate failure label: `INTERACTION_INDUCED_ADAPTATION_BIAS`.

Core invariant:

`ACTOR = USER` does not establish `SIGNAL IS INDEPENDENT OF PRIOR MODEL INFLUENCE`.

## Distinction from adjacent failure classes

- **Memory error:** a fact is lost or distorted.
- **Authority/status error:** a model proposal is promoted into a user decision/rejection.
- **Interaction-induced adaptation bias:** a correctly attributed user sample may carry prior model framing into parameter adaptation.

## Minimal paired design

Freeze one base model, one adapter recipe, one training budget, and one held-out probe set.

### Condition A — INDEPENDENT

- Capture the user's position before any model framing or explanation.
- Use only those user-authored samples as training candidates for Adapter A.

### Condition B — MODEL-EXPOSED

- Present a model framing / terminology / preference first.
- Then collect the user's own response.
- Train Adapter B only on user-authored messages; do not train on model messages.

Use isolated adapters and identical held-out prompts.

## Primary oracle

The primary reference is `USER_BEFORE_EXPOSURE + raw provenance`, not an LLM judge.

Without a pre-exposure user state, the experiment cannot distinguish genuine user change from model-induced framing.

## Probes

1. **Direct probe:** test expressed priority/position on novel wording.
2. **Behavioral probe:** use a new task whose action depends on the learned priority without naming it directly.
3. **Lexical probe:** test transfer of model-specific terminology/framing into new outputs.

## Candidate metrics

- `independent_user_fidelity`
- `model_frame_leakage`
- `lexical_leakage`
- `behavioral_drift`

## Hypotheses

**H1:** Adapter B shows more model-frame leakage / behavioral drift than Adapter A, even though both are trained only on user-authored samples.

**H0:** After controlling the pre-exposure user state, Adapter B shows no meaningful additional transfer of model framing.

## Admission boundary

Memory/learning admission still applies before any weight update. However, ordinary actor/status admission is not sufficient to establish causal independence: correct `actor=user` attribution does not prove absence of prior model influence.

## Relation to Crystal / TCE

- This record does not authorize a Personal Adapter implementation in Crystal.
- Crystal is relevant only as a donor for provenance/admission boundaries.
- TCE methods are relevant for source freezing, direct-vs-behavioral probes, and human audit.
- This candidate does not replace or reorder existing research priorities.

## Stop rule / next bounded action

Do not run automatically. Only after a separate explicit GO, prepare a small frozen pilot package with:

- pre-exposure user baseline;
- matched A/B conditions;
- fixed adapter recipe;
- preregistered scoring;
- source/provenance manifest.

`NOT RUN != FAILED`

`CANDIDATE != ROADMAP COMMITMENT`

`RESEARCH NOTE != IMPLEMENTATION AUTHORIZATION`