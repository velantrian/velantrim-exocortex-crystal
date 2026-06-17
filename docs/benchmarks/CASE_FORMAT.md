# Evaluation Case Format

This document defines a **minimal, reproducible case schema** for verifiability
benchmark cases (see [BENCHMARK_METHODOLOGY.md](./BENCHMARK_METHODOLOGY.md) for
the A/B/C framing). It does not change the evaluation harness or its metrics;
metric definitions, thresholds, and baseline values remain authoritative in
**[../EVAL.md](../EVAL.md)** and `core/eval.py`.

## Schema

A case is a single YAML (or equivalent JSON) document:

```yaml
case_id:                # stable unique id, e.g. "geo-capital-distractor-01"
fixture:                # path/name of the bundled fixture corpus slice this case uses
query:                  # the input question / utterance
arm: A                  # one of: A | B | C  (retrieval-only | +TruthGate | +Trace/Receipt)
expected_evidence:      # list of expected supporting fact ids / source spans
expected_receipt_fields: # receipt fields expected to be present/replayable (Arm C); omit for A
metrics:                # list of metric names this case asserts (see below)
validity_checks:        # list of preconditions, e.g. "distractors present", "boundary block present"
```

`expected_receipt_fields` is only meaningful for Arm C. For Arm A it should be
omitted.

## Metric names

Use **only** existing metric names from `core/eval.py`. Do not invent parallel
terminology.

**Higher-is-better (floor) metrics:**

- `retrieval.hit@1`
- `retrieval.hit@3`
- `retrieval.mrr`
- `trace_completeness`
- `metadata_completeness`
- `source_span_coverage`
- `receipt_replay_survival`
- `contradiction.precision`
- `contradiction.recall`

**Lower-is-better (ceiling) metrics:**

- `unsupported_provenance`
- `contradiction.false_positive_rate`

**Optional boundary metrics** — valid **only** when the fixture's report carries
a `boundary` block; the gate skips them otherwise, so they must not be required
for every case:

- `boundary.refusal_correctness` (optional, higher-is-better)
- `boundary.violations` (optional, lower-is-better)

**Report-only metric** — available in the aggregate report and the Markdown
summary, but **not** a `DEFAULT_GATE` threshold; reference it as report-only, not
as a gate floor:

- `retrieval.hit@5`

## Forbidden / invented names

Do not use names that do not exist in `core/eval.py`:

- `evidence_coverage`
- `answer_grounding`
- flat `refusal_correctness` (use `boundary.refusal_correctness` instead)

## Notes

- "report block vs gate metric": `retrieval`, `contradiction`, and `boundary`
  are grouped **report blocks**; the dotted names above (e.g.
  `contradiction.precision`) are the **threshold/gate** identifiers used by the
  harness.
- For concrete current floors, ceilings, and baseline values, see
  [../EVAL.md](../EVAL.md). They are intentionally not duplicated here.
