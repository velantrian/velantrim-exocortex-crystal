# Evaluation Metrics

Current evaluation exists (`velantrim eval`, `scripts/eval_gate.py` — a
CI-gated harness over curated retrieval/contradiction fixtures with per-case
`metrics.jsonl`; see [EVAL.md](./EVAL.md)). This document defines **target
metrics** for T3/T4 evaluation expansion and the future ReplayBench
([RFC_HARNESS_REPLAY_OPTIMIZATION.md](./RFC_HARNESS_REPLAY_OPTIMIZATION.md)).

**These metrics do not prove perfect truth. They measure whether the system
enforces evidence, traceability, and boundary behavior.**

## Target metric definitions

| Metric | Definition |
|---|---|
| `evidence_coverage` | `claims_with_evidence / total_factual_claims` |
| `trace_completeness` | `claims_with_trace / total_confident_factual_claims` |
| `unsupported_claim_count` | number of factual claims without acceptable evidence |
| `unsupported_claim_penalty` | `unsupported_claim_count * penalty_weight` |
| `contradiction_exposure_rate` | `detected_relevant_contradictions_shown / known_relevant_contradictions` |
| `refusal_correctness` | `correct_refusals_or_downgrades / cases_without_sufficient_evidence` |
| `answer_grounding_score` | how well the answer text is supported by the cited FactsPack (extractive overlap or judged grounding) |
| `latency_budget` | per-query latency ceiling; exceeding it incurs `latency_penalty` |
| `safety_boundary_violations` | count of boundary breaches in a run (e.g. an unsupported claim presented confidently, a gate bypass in a candidate configuration); the target is always zero and any violation disqualifies a candidate |

Notes on intent:

- `refusal_correctness` rewards the system for *correctly* abstaining — an
  abstention on an unanswerable case is a success, not a failure;
- `contradiction_exposure_rate` rewards surfacing known conflicts to the user
  instead of silently picking one side;
- `unsupported_claim_count` is an absolute counter on purpose: averages can
  hide individual violations.

## Relation to the current harness

The implemented harness already reports retrieval quality (hit@k, MRR),
grounding (trace/metadata/span/receipt completeness, unsupported-provenance
count) and contradiction precision/recall against fixture corpora, and is
enforced as a CI gate. The metrics above extend this toward trajectory-level
evaluation: refusal behaviour, contradiction exposure, and explicit safety
counters.

## Future composite score (sketch — not implemented scoring)

```text
overall_score =
  answer_quality
+ evidence_coverage
+ trace_completeness
+ contradiction_handling
+ refusal_correctness
- unsupported_claim_penalty
- safety_boundary_violations
- latency_penalty
```

This formula is a direction, not an implemented scorer. Per the Harness Replay
RFC, single composite scores invite silent trade-offs: future candidate
comparison should remain multi-objective (Pareto) with hard floors —
`safety_boundary_violations > 0` disqualifies a candidate outright rather than
being traded off against quality gains.

## Future research umbrella: Meta-Cognitive Monitor

**Meta-Cognitive Monitor is a future research umbrella, not a current runtime
module.** It groups existing and future evaluation/boundary-monitoring concepts:

| Meta-Cognitive Monitor aspect | Existing / future Velantrim mapping |
|---|---|
| Contradiction Detection | FactsPack Conflict Policy (future RFC) / Causal Spine (research) |
| Grounding Quality Scoring | Evaluation Metrics (this document) / ReplayBench (RFC) |
| Knowledge Boundary Detection | TruthGate / answer policy (implemented baseline) |
| Epistemic Drift Monitoring | Temporal Layer / Observer (future RFC) |
| Health Dashboard | Future reviewer demo / UI |
| Mode-Aware Monitoring | Mode Layer (future RFC) |

No `core/meta_monitor.py`, tests or schemas exist for this umbrella, and none
are proposed here.
