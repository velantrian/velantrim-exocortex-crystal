# Verifiability Benchmark Methodology

This document defines **how to benchmark the verifiability layer of Velantrim
Crystal** — that is, the added value of admitting knowledge through a TruthGate
and proving answers with traces/receipts.

It does **not** redefine the evaluation harness, the bundled fixture corpus, the
metric definitions, or the CI gate thresholds. Those already exist and are
authoritative in **[../EVAL.md](../EVAL.md)** (harness `core/eval.py`, run via
`velantrim eval`; deterministic gate `scripts/eval_gate.py`). This document only
adds the **benchmark framing** on top of that harness.

## Purpose

The question this benchmark answers is **not** "memory vs no memory" and **not**
"is RAG good". Those framings measure retrieval quality, not verifiability.

The question here is narrower and more honest:

> Given the same retrieved evidence, what does **admission control (TruthGate)**
> and what does **proof (Trace/Receipt)** add — to grounding, to refusal of
> unsupported/contradictory claims, and to auditability — and at what cost?

To isolate that, the benchmark compares three arms over the **same** inputs.

## Arms

- **Arm A — retrieval-only / RAG control.** Retrieve → answer. No TruthGate, no
  sealed receipt. This is the control condition: it shows what a conventional
  retrieval-then-generate pipeline produces on the same cases.
- **Arm B — + TruthGate.** Retrieve → TruthGate admission/refusal → answer.
  Measures whether unsupported or contradictory claims are refused or
  constrained rather than asserted.
- **Arm C — + Trace/Receipt.** Retrieve → TruthGate → Trace/Receipt. Measures
  whether auditability and replayability are added **without** degrading answer
  quality from Arm B.

The arms are cumulative (A ⊂ B ⊂ C in capability), so a metric difference
between arms is attributable to the layer that was added.

## Case Design

Each case is a single, fixed input run through one arm. Cases reuse the schema
in **[CASE_FORMAT.md](./CASE_FORMAT.md)**. A case fixes its fixture, query, arm,
expected evidence, and the metrics it asserts, so the same case is reproducible
across runs and across arms.

## Task Selection

Prefer the existing curated, multi-domain fixture corpus described in
[../EVAL.md](../EVAL.md) (retrieval cases with ranking distractors, and labelled
contradiction pairs including hard negatives). New cases should follow the same
discipline: deterministic, source-grounded, and chosen so the metric being
compared is non-trivial (e.g. distractors present, contradictions including
hard negatives).

## Run Shape

To keep the comparison about verifiability rather than model variance, prefer
the **deterministic components already in the repo**: the dependency-free
hashing embedder and extractive answerer used by `scripts/eval_gate.py` and
`core/eval.py`. This makes arm-to-arm differences reproducible and attributable
to the admission/proof layers rather than to LLM sampling noise.

This document does **not** add a benchmark runner; it specifies the shape a
future runner (or a manual run) must follow.

## Metrics

Metrics reuse the existing names from `core/eval.py` (see
[CASE_FORMAT.md](./CASE_FORMAT.md) for the full list and floor/ceiling
direction, and [../EVAL.md](../EVAL.md) for concrete current thresholds and
baseline values). At a framing level:

- **Arm A** is primarily characterised by retrieval metrics
  (`retrieval.hit@1`, `retrieval.hit@3`, `retrieval.mrr`).
- **Arm B** is characterised by `boundary.refusal_correctness` and contradiction
  `contradiction.precision` / `contradiction.recall` /
  `contradiction.false_positive_rate` (boundary metrics apply only when a
  boundary block is present).
- **Arm C** is characterised by `trace_completeness` and
  `receipt_replay_survival`, checked against the answer quality already
  established by Arm B.

For concrete current thresholds and baseline values, see [../EVAL.md](../EVAL.md);
they are not restated here to avoid creating a second source of truth.

## Validity Checks

- The three arms must run over the **same** fixtures and queries; otherwise an
  observed difference cannot be attributed to the added layer.
- Deterministic components must be used (or seeds fixed) so a run is reproducible.
- Boundary metrics are only asserted for cases whose fixtures carry a boundary
  block; they must not be required for every case.
- Reported numbers must be reproducible from the committed fixtures and harness.

## Limitations

**Benchmarks are evidence, not mathematical proof.** A favourable arm comparison
shows that admission control and proof add measurable grounding/auditability on
the chosen corpus; it does not prove correctness on arbitrary inputs, and it does
not claim zero hallucination. Results are bounded by the corpus, the deterministic
answerer, and the metric definitions in [../EVAL.md](../EVAL.md).
