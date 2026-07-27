# Intrinsic-Noise Consolidation — Crystal Research Boundary

**Status:** external research note · documentation only · not implemented  
**Runtime impact:** none  
**Grant impact:** none; not an NLnet deliverable or budget item  
**Canon impact:** no L1/L3 writes, no TruthGate change, no truth-status change

## External research reference

This note records a potentially relevant research direction from:

> Gunner Levi Howe, *Intrinsic-Noise Consolidation: A
> Doob-Barrier-Conditioned Diffusion Turns Analog Device Noise into a
> Continual-Learning Resource*, arXiv:2607.06924, submitted 8 July 2026.

Primary source: <https://arxiv.org/abs/2607.06924>

The paper studies whether intrinsic analog-device noise can become a memory
consolidation resource rather than only an accuracy cost. It reports an inverted-U
retention effect under a barrier-conditioned stochastic rule on Split-MNIST and a
single-seed BrainScaleS-2 hardware experiment. The hardware result is described as a
stability–plasticity shift at matched average accuracy, not a general net-accuracy
improvement.

This is a new preprint and should be treated as a falsifiable research hypothesis,
not as production evidence for Crystal.

## Relationship to current Crystal

Crystal already contains two distinct mechanisms that must not be conflated with the
paper:

1. `core/consolidate.py` applies deterministic, time-based confidence decay with
   significance and anchoring protection.
2. `core/neurocore.py` Phase 0 is a disabled-by-default passive tracker that logs the
   norm of a hypothetical plastic update and never changes a model or L3.

Neither mechanism implements Doob barrier-conditioning or claims an intrinsic-noise
retention effect.

```text
Current Crystal
├── deterministic confidence maintenance
├── source-tracked canonical memory
├── TruthGate admission
└── passive NeuroCore telemetry only

External hypothesis
└── stochastic barrier-conditioned synaptic consolidation
```

## Safe research placement

Any exploration belongs outside the audited Crystal core, for example:

```text
prototypes/research_mode/intrinsic_noise_consolidation/
├── README.md
├── simulator.py
├── metrics.py
├── fixtures/
└── tests/
```

Required isolation:

- disabled by default;
- synthetic or separately copied experiment state only;
- no import from `core.l3_graph` for writes;
- no mutation of stored `confidence`, `epistemic_state`, `truth_status` or receipts;
- no automatic promotion into L3;
- no use in grant demonstrations as implemented Crystal capability;
- no biological-cognition, consciousness or “living memory” claim.

## Proposed Phase 0 experiment

The only safe first phase is an observe-only simulation comparing deterministic and
stochastic retention under controlled seeds.

### Candidate conditions

- current deterministic decay baseline;
- matched anchored-drift control;
- barrier-conditioned stochastic rule;
- conditioning ablation;
- several noise levels spanning low, intermediate and high regimes.

### Required metrics

| Metric | Purpose |
|---|---|
| Prior-task retention | Detect whether previously learned associations survive. |
| New-task plasticity | Ensure retention does not merely freeze learning. |
| Average task accuracy | Separate stability–plasticity trade-offs from net quality gains. |
| Inverted-U reproducibility | Test the paper's distinctive falsifiable prediction across seeds. |
| False promotion count | Must remain zero because the prototype has no Canon admission authority. |
| Receipt/trace impact | Must remain none because the prototype is isolated from Crystal receipts. |
| Compute/energy accounting | Prevent an apparent benefit from hiding disproportionate cost. |

### Go/no-go criteria

Proceed beyond documentation only when all of the following are true:

1. the inverted-U effect reproduces across a pre-declared seed count;
2. the result survives a conditioning ablation and matched control;
3. plasticity is not reduced below the declared floor;
4. the prototype remains structurally unable to write to Crystal L3;
5. the experiment has deterministic replay metadata and published negative results;
6. an independent review finds no path from stochastic state to factual promotion.

Failure to reproduce the effect closes the experiment without changing Crystal.

## Promotion gate

Even a successful prototype is not automatically a Crystal feature. Promotion would
require:

```text
external result
→ independent replication
→ Crystal-specific RFC
→ threat model and invariants
→ isolated prototype
→ evaluation report
→ Operator GO
→ implementation PR
→ full tests and audit
→ explicit implementation-status update
→ separate grant approval if funding scope changes
```

A future runtime proposal must explain why stochastic consolidation belongs in a
verifiable symbolic memory system rather than only in a trainable neural substrate.
Until that question is answered, the research remains separate.

## Grant-safe wording

Safe:

> Separate Research Mode work may evaluate whether controlled stochastic dynamics
> improve retention in a non-canonical experimental memory substrate. This research
> is isolated from Crystal's TruthGate, canonical graph and funded MVP scope.

Unsafe:

- Crystal uses intrinsic noise to consolidate memory.
- Crystal has neuromorphic continual learning.
- The grant funds a self-adapting cognitive memory.
- Stochastic dynamics can modify verified facts.
- The cited preprint proves production improvement for Crystal.

## Final boundary

```text
Research may perturb experimental weights.
Crystal Canon changes only through evidence, provenance and TruthGate.
```
