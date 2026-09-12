# Continuum Current State vs Trajectory — Cross-Project Research Evidence

**Status:** `RESEARCH / CROSS-PROJECT EVIDENCE / DOCS-ONLY / NON-RUNTIME`  
**Date:** 2026-09-12  
**Crystal repository baseline when authored:** `6947c24961888afe9bf200a410778c66b36d989d`  
**Source research repository:** `velantrian/Velantrim-Continuum`  
**Source branch:** `research/cont-e0t-prereg-v22`  
**Frozen preregistration SHA:** `6847eb759d747955b8618021d2414f5ffa840584`  
**Source document:** `docs/research/CONT_E0T_FINAL_PREREGISTRATION.md`  
**Experiment status:** `READY_FOR_OWNER_GO / NOT_AUTHORIZED / NOT_EXECUTED`  
**Crystal runtime authorization:** false  
**Crystal architecture promotion:** none  
**Crystal grant scope / award / budget change:** none

> This note records a relevant cross-project research milestone for Crystal reviewers. It does **not** import Continuum into Crystal, does not change Crystal memory or Reader semantics, does not authorize a Continuum experiment, does not prove that historical trajectory improves memory or continuity, and does not create a funded NLnet deliverable.

---

## 1. Why this belongs in Crystal

Crystal is designed around durable, inspectable memory state with explicit provenance, epistemic status, revision boundaries, receipts and authority separation. That creates an adjacent long-horizon question:

> When a fresh or replaceable reasoning model must continue work, is a competent representation of the **current trusted state** sufficient, or can a bounded record of **how that state changed** provide additional practical value?

Crystal does not own this continuity question. The owning research project is **Velantrim Continuum**. The relevance to Crystal is architectural and evaluative rather than runtime ownership.

Crystal already preserves distinctions such as:

```text
stored != current
retrieved != evidence
revision != overwrite-without-history
receipt != truth
model output != Canon
```

Continuum asks a different but complementary question:

```text
current state != state trajectory
rebuildability != continuation benefit
history availability != proof that history is needed
```

For reviewers, this is useful because it shows how the wider Velantrim research program treats long-horizon memory questions: by separating durable state, historical lineage, model utilization and authority rather than collapsing them into one generic "memory" claim.

---

## 2. The research question

The preregistered Continuum experiment, `CONT-E0T`, tests a deliberately narrow **Claim B**:

> For a protocol-frozen, fallible, replaceable reader, does adding a bounded genuine accepted trajectory to the same competent current-state representation improve practical resume adequacy on the frozen test surface?

The two arms are conceptually:

```text
CONT-T1
= competent bounded current state

CONT-T2
= byte-identical current-state semantics
+ bounded genuine accepted transition trajectory
```

In this note, **genuine trajectory** means that the experimenter-authored Evidence scenarios contain substantive intermediate state evolution rather than a snapshot-derived `SET`-from-final encoding. It does **not** mean naturally observed production history or a real user's historical log.

The experiment is **not** designed to prove:

- that history is semantically necessary;
- that event sourcing is required;
- that every AI memory system should retain a trajectory;
- that no stronger current-state representation could perform as well;
- that temporal ordering alone is the causal mechanism of any observed benefit;
- that a positive result generalizes across models, domains or production workloads.

The safer architectural interpretation before evidence is:

```text
TRAJECTORY-CAPABLE != TRAJECTORY-REQUIRED
HISTORY SEMANTICS != EVENT-SOURCING REQUIREMENT
CURRENT STATE != STATE TRAJECTORY
T2 > T1 != UNIVERSAL MEMORY LAW
```

---

## 3. An important correction made before the confirmatory run

An earlier **pre-freeze candidate design** for Continuum E0-T included an event-log representation derived from an already-final current-state snapshot. Inspection showed that this older T2 representation did **not** contain genuine temporal state evolution: `event_projection()` emitted a snapshot-derived / `SET`-from-final event encoding in deterministic field order.

Therefore, a hypothetical `T2 > T1` under that older design could not have established independent value from real transition history. It could have reflected representation, redundancy or salience effects.

That problem was treated as a scientific identifiability failure rather than hidden behind a stronger claim.

The successor `CONT-E0T` design was rebuilt around a cleaner contrast:

- T1 remains a competent, schema-complete current-state representation;
- T1 is not intentionally impoverished;
- T2 contains the same current-state semantics;
- only T2 receives bounded genuine accepted trajectory information;
- trajectory entries use thin ID references rather than repeating the current answer in prose;
- provenance/audit snapshots remain validator-only rather than becoming extra reader hints;
- list ordering in T1 is explicitly non-temporal;
- model screening during Evidence construction is forbidden.

This correction is itself a useful **methodological finding** about experimental design:

```text
REPRESENTATION ADVANTAGE != HISTORY ADVANTAGE
SNAPSHOT-DERIVED EVENTS != TRANSITION HISTORY
EQUIVALENCE != ADEQUACY
```

It is **not**, however, an experimental result about whether genuine trajectory helps. That remains unmeasured until an authorized run occurs.

---

## 4. Frozen preregistration status

The final preregistration freeze is recorded at:

`velantrian/Velantrim-Continuum@6847eb759d747955b8618021d2414f5ffa840584`

with:

```text
READY_FOR_OWNER_GO       = YES
EXPERIMENT_AUTHORIZATION = NOT_AUTHORIZED
NO READER / NO SCORING / NO OUTPUTS
SNAPSHOT_PINNED          = NO
ALIAS_MUTABLE            = YES
```

The confirmatory set contains exactly four frozen Evidence fixtures, promoted by hash without rewriting their reviewed bytes. The experiment uses one primary resume probe per fixture.

The frozen decision rule is intentionally bounded. A positive experiment-level outcome requires all four pairs to complete, at least three `T2_SUPERIOR` pairs, and zero `T2_INFERIOR` pairs.

At the arm level, **adequate** means `PRIMARY_PASS` **and** no HARD FAIL. `PRIMARY_PASS` requires the frozen resume decision plus all required `must_compose` relations; a correct binary May/No action by itself is not sufficient. HARD FAIL classes include loss/override of a binding constraint, dishonest resolution of required UNKNOWN, or fabricated authorization.

The reader contract uses `deepseek-flash` / provider-labelled DeepSeek-V4.1-Flash with thinking disabled, temperature zero, no tools, no web, no memory and one fresh stateless invocation per arm/probe. The **protocol is frozen, not the model weights**: the model alias is mutable and no immutable weight snapshot is available; the protocol therefore records the returned model identity and aborts on an identity change during the run.

Scorer-A, Scorer-B and the Adjudicator are **Grok Bot agents, not humans**. Blinded scoring roles are separated procedurally from fixture construction and arm permutation. This is procedural isolation, not a claim of hard physical independence.

As of this note:

```text
CONFIRMATORY MODEL OUTPUTS = NONE
BLINDED SCORES             = NONE
CLAIM_B_RESULT              = NOT_ESTABLISHED
```

---

## 5. What is already learned, and what is not

### Established before the run

The research process has established that the question must be split more carefully than "does more memory help?"

A valid comparison must separate at least:

1. the quality of the current-state representation;
2. the presence or absence of genuine trajectory information;
3. the reader's ability to use that information;
4. the cost and attention burden of the richer package;
5. state authority from model interpretation.

It has also established that snapshot-derived event re-encoding of a final state cannot be used as evidence for independent trajectory value.

### Not established

No current **CONT-E0T evidence on the frozen source set** supports the statements:

```text
history is necessary for continuation
trajectory improves Crystal
trajectory improves AI memory in general
event sourcing is the correct architecture
current state alone is sufficient in general
```

Those would exceed the preregistered evidence ceiling. This statement is scoped to the present Continuum experiment and its evidence state; it is not a claim about all external literature.

---

## 6. Cross-project mapping to Crystal

The strongest relationship is a **research crosswalk**, not an implementation merge.

| Continuum question / distinction | Crystal analogue | Safe Crystal consequence |
|---|---|---|
| Competent current state vs same state + genuine trajectory | Strict/current memory state vs inspectable revision/provenance lineage | Preserve the distinction between what is current and how it became current |
| `CURRENT STATE != STATE TRAJECTORY` | Current Canon projection vs history/provenance/revision records | Do not assume that one representation substitutes for the other in every reader task |
| `MODEL OUTPUT != STATE AUTHORITY` | Existing Crystal Guardian/TruthGate boundary | A model's reconstructed rationale cannot mutate trusted state merely because it sounds coherent |
| Thin trajectory as optional reader input | Crystal receipts/history/provenance may be available as supporting context | Whether lineage should be surfaced to a reader is an evaluation question, not an automatic runtime rule |
| Frozen, adversarial preregistration | Crystal reviewer/replay/evidence discipline | Cross-project methodology is relevant to future Crystal evaluation design |
| Positive result is bounded to one reader and four fixtures | Crystal grant-safe claim discipline | Avoid converting a small research result into a production or SOTA claim |

A possible future whole-system pattern, still only a research possibility, is:

```text
CURRENT TRUSTED STATE
        +
HISTORY / LINEAGE ON DEMAND
        -> bounded reader/orientation context
        -> replaceable model
        -> proposal only
        -> existing owner-specific admission / authority gates
```

This pattern is **not** being added to Crystal by this note.

---

## 7. Why this matters to reviewer-facing Crystal research

Crystal's public grant-facing position is not merely "store more memory." It emphasizes auditable, source-grounded, authority-aware memory infrastructure.

The Continuum study is relevant because it asks a practical next-order question that appears once durable trusted state exists:

> What is the smallest durable representation that lets a future model continue correctly without requiring the original context window, and when—if ever—does historical trajectory materially help beyond the current state?

This supports Crystal's reviewer-facing research story in three ways:

1. **Memory is evaluated as a system property, not a storage-volume claim.** More retained text is not assumed to be better.
2. **Lineage is separated from current truth.** Historical path can be valuable for audit or reconstruction without automatically being current state or authority.
3. **The project family uses preregistered falsifiable tests.** The current Continuum design was corrected before model outputs, Evidence was frozen before the confirmatory run, and interpretation ceilings were locked in advance.

This is relevant research methodology and ecosystem evidence. It is not implementation evidence for Crystal.

---

## 8. Relation to Crystal's grant scope

Crystal's current public grant documentation records the NLnet NGI0 Commons Fund proposal as **submitted / under review / not awarded**, with no approved budget change.

This Continuum cross-project record:

- does **not** alter the submitted Crystal grant scope;
- does **not** create or expand a funded milestone;
- does **not** imply that NLnet has approved Continuum or trajectory work;
- does **not** change Crystal V1 completion or runtime status;
- does **not** authorize a Crystal continuity implementation;
- does **not** convert research findings into Reader, Canon, Guardian or TruthGate behaviour.

Because this note is recorded before any grant agreement, it belongs to the **pre-agreement research baseline**.

```text
MERGED PRE-AGREEMENT RESEARCH NOTE
!=
FUTURE FUNDED DELIVERABLE
```

If a future agreement includes continuity-, history-, replay- or reader-context work, the funded delta must be defined against then-live `main` and must consist of genuinely new work with explicit acceptance evidence.

---

## 9. Grant- and reviewer-safe claim discipline

### Safe / GREEN

The following are safe when source-linked and correctly dated:

- A separate Velantrim Continuum research line has reached a frozen preregistration for testing current-state-only resume against the same current state plus bounded genuine transition trajectory.
- The Continuum experiment has **not yet run** and no trajectory benefit is currently claimed.
- The preregistration explicitly prevents a positive result from being interpreted as universal event-sourcing necessity.
- Cross-project Continuum work is relevant to Crystal because both projects distinguish current trusted state from provenance/history/lineage, while preserving separate ownership and authority.
- The experiment design demonstrates a falsification-first, preregister-before-output methodology relevant to reviewer-grade AI-memory research.

### Context required / YELLOW

Use only with the limitations above:

- state trajectory;
- historical continuity;
- long-horizon memory;
- resumable AI processes;
- lineage-aware context;
- trajectory-assisted reasoning.

These phrases must not imply a measured benefit until the authorized confirmatory run exists.

### Unsafe / RED as current Crystal claims

Do not claim:

- Crystal implements Continuum;
- Crystal currently uses transition history to improve answers;
- Continuum has proven trajectory improves resume quality;
- event sourcing is required for AI memory;
- history is semantically necessary for cognition;
- the experiment is complete;
- the Continuum work is an awarded or funded NLnet deliverable;
- a future positive result would prove production readiness or generalize to all models.

---

## 10. Current classification

```text
CROSS_PROJECT_RESEARCH_RELEVANCE = HIGH [EDITORIAL ASSESSMENT]
CRYSTAL_REVIEWER_RELEVANCE       = HIGH [EDITORIAL ASSESSMENT]
GRANT_RESEARCH_RATIONALE         = RELEVANT [EDITORIAL ASSESSMENT]

CONT_E0T_PREREGISTRATION         = FROZEN_PENDING_OWNER_GO
CONT_E0T_READY_FOR_OWNER_GO      = YES
CONT_E0T_AUTHORIZED              = NO
CONT_E0T_EXECUTED                = NO
CONT_E0T_RESULT                  = NOT_ESTABLISHED

CRYSTAL_IMPLEMENTATION_CHANGED   = NO
CRYSTAL_RUNTIME_CHANGED          = NO
CRYSTAL_CANON_CHANGED            = NO
CRYSTAL_READER_CHANGED           = NO
CRYSTAL_TRUTHGATE_CHANGED        = NO
CRYSTAL_GRANT_SCOPE_CHANGED      = NO
CRYSTAL_GRANT_AWARD_CHANGED      = NO
FUNDED_DELIVERABLE_CREATED       = NO
```

---

## 11. Source map

### Continuum — primary research and protocol sources

All detailed Continuum links below are pinned to immutable commits so an external reviewer can trace the claims without reconstructing the research history from branch state.

- Repository: https://github.com/velantrian/Velantrim-Continuum
- Frozen preregistration commit: https://github.com/velantrian/Velantrim-Continuum/commit/6847eb759d747955b8618021d2414f5ffa840584
- Final preregistration: https://github.com/velantrian/Velantrim-Continuum/blob/6847eb759d747955b8618021d2414f5ffa840584/docs/research/CONT_E0T_FINAL_PREREGISTRATION.md
- V2 candidate / correction record: https://github.com/velantrian/Velantrim-Continuum/blob/6847eb759d747955b8618021d2414f5ffa840584/docs/research/CONT_E0T_PREREGISTRATION_V2_CANDIDATE.md
- Fields 1–4 + run integrity: https://github.com/velantrian/Velantrim-Continuum/blob/6847eb759d747955b8618021d2414f5ffa840584/docs/research/CONT_E0T_FIELDS_1_4_RUN_INTEGRITY.md
- Fields 6–10 / pre-Evidence rules: https://github.com/velantrian/Velantrim-Continuum/blob/6847eb759d747955b8618021d2414f5ffa840584/docs/research/CONT_E0T_PRE_EVIDENCE_RULES.md
- Field 5 reader contract: https://github.com/velantrian/Velantrim-Continuum/blob/6847eb759d747955b8618021d2414f5ffa840584/docs/research/CONT_E0T_FIELD5_READER_CONTRACT.md
- Legacy snapshot-derived `event_projection()` implementation: https://github.com/velantrian/Velantrim-Continuum/blob/6847eb759d747955b8618021d2414f5ffa840584/scripts/e0/prepare_transfer.py
- V2.2 correction commit: https://github.com/velantrian/Velantrim-Continuum/commit/2bb4aabd7772498278648be3b8cf36b2cbc2b9fa
- Confirmatory Evidence manifest: https://github.com/velantrian/Velantrim-Continuum/blob/6847eb759d747955b8618021d2414f5ffa840584/docs/research/cont_e0t_v2/EVIDENCE_MANIFEST.json

### Crystal — relevant boundaries

- [Reviewer Guide](../REVIEWER_GUIDE.md)
- [Project, Grant and Governance Overview](../PROJECT_GRANT_AND_GOVERNANCE.md)
- [NLnet Reviewer Q&A](../grants/reviewer-qa.md)
- [NLnet Scope](../GRANT_NLNET_SCOPE.md)
- [Baseline → funded delta matrix](../grants/baseline-funded-delta-matrix.md)
- [Structural Qualification — Cross-Project Evidence](./STRUCTURAL_QUALIFICATION_CROSS_PROJECT_EVIDENCE.md)

---

**Bottom line for reviewers:** Crystal itself remains unchanged. The relevant ecosystem research has advanced from an ambiguous "more history may help" intuition to a frozen, falsifiable test of **competent current state vs the same current state plus genuine bounded trajectory**, with no model outputs yet and explicit limits on what any future positive result would mean.
