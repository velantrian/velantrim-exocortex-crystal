# Spark Layer — RFC (Future Research Direction)

**Status:** Future RFC only. Not current runtime.
**Planned for:** v0.3.0+ / post-grant research roadmap.
**Requires:** Separate design RFC and Mode Layer RFC before implementation.
**Runtime impact in v0.2.0:** None.

> None of the features described in this document are current runtime behaviour.
> They must not be presented as implemented in README, Reviewer Overview or grant
> materials. Everything below is a design direction for future research.

> **Scope boundary.** The Spark layer is a *technology* component of the
> Velantrim Exo-Cortex architecture — a sandboxed cognitive engine for
> exploration, hypothesis generation and creative reasoning. It is not the same
> as Velantrim Culture. Velantrim Culture (symbols, myths, rituals, language,
> ways of life) is a *human and social layer* that exists independently of
> any software system and is explicitly outside the Crystal grant core (see
> [IMPLEMENTATION_STATUS.md](./IMPLEMENTATION_STATUS.md)).

---

## 1. What is Spark?

Spark is the future *exploratory and generative* layer of the Velantrim
Exo-Cortex — the cognitive space where the system can reason speculatively,
generate hypotheses, draw analogies, explore connections, and produce creative
output **without those outputs contaminating the verified canon**.

Crystal (the current grant core) is the *verified knowledge layer*: it stores
only what has passed the TruthGate. Spark is the complementary *generative
reasoning layer*: it works with what might be true, what is interesting to
explore, what the system does not yet know but can reason about.

The two layers are architecturally separated by a hard boundary.

```
┌─────────────────────────────────────────────────────┐
│                  Spark Layer (future)               │
│  hypothesis generation · analogy · exploration      │
│  speculative connections · creative drafts          │
│         (sandboxed — no direct L3 write)            │
└──────────────────────┬──────────────────────────────┘
                       │  Plausibility Pre-Filter
                       │  (future Spark-to-Crystal bridge)
                       ▼
┌─────────────────────────────────────────────────────┐
│         Guardian + TruthGate (implemented)          │
│      the only automatic path into L3 canon          │
└──────────────────────┬──────────────────────────────┘
                       │  on pass only
                       ▼
┌─────────────────────────────────────────────────────┐
│            Crystal L3 Canon (implemented)           │
│       VERIFIED · WORLD_FACT · HYPOTHESIS            │
└─────────────────────────────────────────────────────┘
```

---

## 2. Imagination Mode

Imagination Mode is the operational mode in which the Exo-Cortex runs Spark.
It is a *sandboxed context*: the system knows it is exploring rather than
asserting. Outputs produced in Imagination Mode carry an implicit
`epistemic_state = HYPOTHESIS` or lower — they are never auto-promoted.

### What Imagination Mode can produce

| Output type | Example | Can enter L3 canon? |
|---|---|---|
| Hypothesis | "This pattern may indicate X" | Only via Guardian + TruthGate + curator approval |
| Analogy | "This structure resembles Y in domain Z" | Only if independently verified |
| Speculative connection | "If A and B, then perhaps C" | Only if evidence found |
| Creative draft | A proposal, sketch, design fiction | Never automatically |
| Question / gap signal | "We do not have data on X" | As a Known Unknown (future RFC) |

### What Imagination Mode cannot do

- Write directly to L3 canon.
- Produce `VERIFIED` or `WORLD_FACT` claims without Guardian + TruthGate.
- Bypass the Ring Zero invariant (see [ARCHITECTURE.md](./ARCHITECTURE.md)).
- Promote its own output by self-confirmation.

This is the same constraint that governs `LLM_OUTPUT` today: an LLM cannot
make itself `VERIFIED`. Spark cannot either, even when the LLM is used
internally to drive Spark reasoning.

---

## 3. Spark-to-Crystal Bridge (Plausibility Pre-Filter)

Before a Spark-generated claim can be considered for TruthGate evaluation,
a lightweight plausibility pre-filter classifies it:

| Label | Meaning |
|---|---|
| `impossible_under_known_constraints` | Directly contradicts verified canon — discard |
| `highly_speculative` | No supporting evidence, contradicts priors — flag |
| `research_required` | Plausible but unverifiable without new sources |
| `partially_supported_by_canon` | Some L3 evidence supports it but not conclusive |
| `plausible_enough_for_deep_check` | Worth full Guardian + TruthGate evaluation |

Only claims labelled `plausible_enough_for_deep_check` proceed to the full
gate pipeline. All others are either discarded, flagged for curator review, or
added to the Known Unknowns map (see
[EPISTEMIC_INFRASTRUCTURE_UPGRADE.md](./EPISTEMIC_INFRASTRUCTURE_UPGRADE.md)).

---

## 4. Spark outputs that stay sandboxed forever

Some Spark outputs are not intended for canon promotion at all. They serve
the cognitive and exploratory function of the system without ever needing
to be "true" in the canonical sense:

- **Analogies and metaphors** used to explain concepts.
- **Design fiction** — speculative scenarios exploring future states.
- **Thought experiments** — counterfactual reasoning ("what if X were false?").
- **Generative proposals** — drafts, sketches, suggestions for human review.

These stay in the Spark layer, tagged as `SPARK_OUTPUT`, and are never
eligible for `VERIFIED`, `WORLD_FACT`, or even `HYPOTHESIS` without an
explicit curator decision and a full gate pass.

---

## 5. Relationship to the Mode Layer (future RFC)

Spark operates within the future *Mode Layer* — the architectural component
that governs which reasoning mode the Exo-Cortex is currently in:

| Mode | Purpose | Canon write? |
|---|---|---|
| **Crystal Mode** (default) | Retrieval from verified canon | Read-only |
| **Ingest Mode** | Structured import through gates | Via TruthGate only |
| **Imagination Mode / Spark** | Exploration and hypothesis generation | Never automatic |
| **Review Mode** | Curator decision-making | Explicit approve/reject only |

The Mode Layer RFC (future) will define explicit triggers, fallback rules,
and the Mode Router. Spark is one of the modes the Mode Layer governs.

---

## 6. Spark vs Velantrim Culture

These are two entirely different things and must not be conflated.

| | Spark Layer | Velantrim Culture |
|---|---|---|
| **What it is** | A technology component — a sandboxed cognitive layer within the Exo-Cortex software architecture | A human and social layer — symbols, myths, language, rituals, ways of life, creative traditions |
| **Where it lives** | Inside the Velantrim Exo-Cortex codebase (future) | Outside any software system |
| **Who uses it** | The AI system itself, as an internal reasoning mode | People — communities, practitioners, researchers |
| **In this repo** | Future RFC / roadmap | Explicitly `Out of scope` |
| **Can enter L3 canon?** | Only via Guardian + TruthGate | Never — wrong category entirely |

Velantrim Culture is not a feature. It is not implemented, not planned for
implementation, and not part of the grant core. It exists independently of
Crystal and of the Exo-Cortex software.

---

## 7. Non-goals

This RFC does not describe:

- implementing Spark or Imagination Mode in Crystal v0.2.0 or any current release;
- a creative writing assistant, chatbot, or general-purpose LLM interface;
- replacing the TruthGate with probabilistic pre-filters;
- automatic promotion of speculative output to canon;
- Velantrim Culture, myths, rituals, or any social/human layer;
- consciousness, sentience, or guaranteed creativity detection;
- any change to the current runtime schema, enums, or test baseline.

---

## 8. Implementation prerequisites

Before Spark can be designed in detail, the following must exist:

1. **Mode Layer RFC** — defines the mode boundary contract and Mode Router.
2. **WRITE_POLICY RFC** — defines allowed write targets per mode (Spark: none to L3).
3. **EPISTEMIC_INFRASTRUCTURE_UPGRADE** — Plausibility Pre-Filter fields and
   Known Unknowns map must be in place as the Spark-to-Crystal bridge.
4. **GUARDIAN_CONTRACT** — the formal Guardian detect → flag/block/pass
   contract that Spark output must pass through.

None of these exist as runtime features today. See
[IMPLEMENTATION_STATUS.md](./IMPLEMENTATION_STATUS.md) for the current status
of all components.
