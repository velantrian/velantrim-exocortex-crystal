# Velantrim Crystal — Evaluation Plan

This document defines how Velantrim Crystal should be evaluated beyond unit-test
coverage. The goal is not only to prove that functions run, but to measure
whether memory answers remain grounded, replayable and auditable.

## Current baseline

The repository currently reports:

- 717 passing tests;
- 12 skipped optional-backend tests;
- 0 failing tests;
- 100% coverage, enforced by a 100% gate in CI;
- standard-library runtime path;
- tests for memory, TruthGate, L3, provenance, receipts, GDPR operations, MCP,
  external ingestion and biological-memory layers.

See [../TEST_REPORT.md](../TEST_REPORT.md) for the reproducible test summary.

A **baseline evaluation harness now exists** (`core/eval.py`, run with `velantrim
eval`). It runs over a **curated, multi-domain fixture corpus** bundled with the
package (`core/_eval_fixtures/`): **16 retrieval cases** (physics, geography,
astronomy, chemistry, biology, history, mathematics) with ranking **distractors**
so retrieval is non-trivial, and **12 labelled contradiction pairs** including
hard negatives (same-numeric-value, different-subject, refinement). It reports
retrieval `hit@1/3/5` + MRR, trace completeness, metadata completeness,
source-span coverage, receipt-replay survival and contradiction
precision/recall — the current baseline:

```json
{"cases": 16, "retrieval": {"hit@1": 0.875, "hit@3": 0.9375, "hit@5": 1.0, "mrr": 0.9115},
 "trace_completeness": 1.0, "metadata_completeness": 1.0, "source_span_coverage": 1.0,
 "unsupported_provenance": 0,
 "receipt_replay_survival": 1.0,
 "contradiction": {"pairs": 12, "precision": 0.8333, "recall": 0.8333, "false_positive_rate": 0.1667}}
```

(The deterministic classifier catches negation, numeric and known-antonym
signals; rarer antonyms such as *heavier/lighter* are a documented limitation,
which is why recall is 0.83 rather than 1.0 — the corpus does not cherry-pick
only easy positives.)

`unsupported_provenance` counts facts that present high-confidence provenance
(`truth_status == VERIFIED`) while carrying **no** source-span evidence (#61). A
healthy corpus keeps this at zero: a VERIFIED claim must be backed by a source.
The complementary receipt-level guard is `verify_receipt(receipt,
strict_provenance=True)`, which flags such a citation as `unsupported_provenance`
and fails verification.

### Quality gate (CI)

`scripts/eval_gate.py` (also `velantrim eval --gate`) runs the harness in an
isolated, ephemeral canon, writes `metrics.jsonl` + `eval_report.md`, and exits
non-zero if any metric falls below its regression floor (or above its ceiling).
A dedicated **`eval-gate` CI job** runs it on every push and pull request, so
retrieval / grounding / contradiction quality cannot silently drop between
releases. The thresholds (`core.eval.DEFAULT_GATE` / `_GATE_MAX`) sit just below
the current baseline and are tightened as the corpus and embedder improve:

| metric | floor | baseline |
|---|---|---|
| retrieval.hit@1 | 0.80 | 0.875 |
| retrieval.hit@3 | 0.85 | 0.9375 |
| retrieval.mrr | 0.85 | 0.9115 |
| trace / metadata / source-span / receipt-replay | 1.0 | 1.0 |
| contradiction.precision | 0.75 | 0.8333 |
| contradiction.recall | 0.75 | 0.8333 |
| unsupported_provenance (ceiling) | ≤ 0 | 0 |
| contradiction.false_positive_rate (ceiling) | ≤ 0.25 | 0.1667 |

This is still a **curated fixture**, not a broad external benchmark. The
dimensions below define where the harness is extended next: larger corpora across
more domains and languages, adversarial contradiction cases and a grounding score
for generated answers.

## Evaluation dimensions

### 1. Trace completeness

Every answer that claims factual grounding should have a trace path.

Suggested metric:

```text
trace_completeness = answers_with_trace / factual_answers_total
```

Target for curated factual fixtures: **≥ 0.95**.

### 2. Receipt replay survival

A receipt should replay successfully when the supporting canon has not changed,
and should detect drift when a supporting fact is changed, restricted, erased or
contradicted.

Suggested metric:

```text
receipt_replay_survival = valid_replays / unchanged_receipts_total
receipt_drift_detection = detected_drifts / modified_receipts_total
```

Target for curated fixtures: **≥ 0.95** replay survival and **≥ 0.95** drift
detection.

### 3. Retrieval quality

For a query set with known relevant facts, measure retrieval rank quality.

Suggested metrics:

```text
hit@1
hit@3
hit@5
MRR
```

Target values depend on the fixture, but every release should publish the same
fixture result so regressions are visible.

### 4. Source and claim typing accuracy

For imported knowledge and user statements, verify that facts preserve:

- `source`;
- `source_status`;
- `claim_type`;
- epistemic state;
- confidence and significance where provided.

Suggested metric:

```text
metadata_completeness = facts_with_required_metadata / facts_total
```

Target for curated fixtures: **1.0**.

### 5. Contradiction handling

Evaluate deterministic contradictions such as negation, antonym and numeric
conflicts.

Suggested metrics:

```text
contradiction_precision
contradiction_recall_on_fixture
false_quarantine_rate
```

### 6. External ingestion safety

Evaluate file ingestion across supported dependency-free formats:

- `.txt`;
- `.md` / `.markdown`;
- `.json`;
- `.jsonl` / `.ndjson`;
- `.csv`.

Required checks:

- unsupported formats are rejected;
- blank records are skipped;
- low-confidence claims are blocked;
- duplicates reinforce instead of duplicating;
- imported facts carry `source_status = EXTERNAL`.

Future eval extension: dry-run imports, batch/session provenance and source-span
coverage.

### 7. Local-first / offline operation

The default path should work without network access and without mandatory third-
party services.

Checks:

- install package locally;
- run CLI ingest/ask/receipt with no API keys;
- use SQLite L3 persistence;
- run tests without optional cloud providers;
- verify that optional LLM providers are not invoked unless explicitly selected.

### 8. Privacy and GDPR-relevant operations

Evaluate:

- Art. 17 erasure removes L0/L1/L3 fact material and records a tombstone;
- Art. 18 restriction changes processing behaviour;
- Art. 30 record-of-processing is inspectable;
- audit log detects tampering;
- opt-in encryption detects modified ciphertext.

## Minimal release evaluation report

Each public release should include a small report with the **implemented baseline
fixture metrics** and clearly separated future benchmark extensions:

```json
{
  "version": "0.1.x",
  "tests_passing": 717,
  "coverage": "100%",
  "baseline_fixture": {
    "cases": 4,
    "retrieval_hit_at_1": 0.5,
    "retrieval_hit_at_3": 1.0,
    "retrieval_hit_at_5": 1.0,
    "retrieval_mrr": 0.75,
    "trace_completeness": 1.0,
    "metadata_completeness": 1.0,
    "source_span_coverage": 1.0,
    "receipt_replay_survival": 1.0,
    "contradiction_precision": 1.0,
    "contradiction_recall": 1.0,
    "contradiction_false_positive_rate": 0.0
  },
  "future_extensions": [
    "curated external fixture corpora",
    "per-case metrics.jsonl",
    "human-readable eval_report.md",
    "CI regression gates for trace and receipt survival"
  ]
}
```

## Evaluation harness — status

**Delivered (baseline):** `core/eval.py` (`velantrim eval`) ingests a deterministic
fixture, runs the real retrieval/answer/receipt path, and returns a machine-readable
report with retrieval (hit@k, MRR), trace completeness, metadata completeness,
**source-span coverage** (WP1) and **contradiction precision/recall** (WP3), plus
receipt-replay survival. Pure metric functions (`hit_at_k`, `reciprocal_rank`,
`aggregate`, `source_span_coverage`, `contradiction_eval`) are unit-tested.

**Planned (extensions):**

- `metrics.jsonl` for per-case results and `eval_report.md` for human review;
- curated fixture corpora under `eval/fixtures/` (beyond the built-in set);
- automatic source-span extraction and additional contradiction cases;
- CI-friendly regression checks for trace completeness and receipt replay.

## Non-goals

This evaluation plan does not claim:

- human-level intelligence;
- consciousness;
- zero hallucinations;
- universal truth detection;
- legal certification of GDPR compliance.

The measurable goal is narrower: **make AI memory auditable, local, replayable and
harder to corrupt silently**.
