# Velantrim Crystal — Evaluation Plan

This document defines how Velantrim Crystal should be evaluated beyond unit-test
coverage. The goal is not only to prove that functions run, but to measure
whether memory answers remain grounded, replayable and auditable.

## Current baseline

The repository currently reports:

- 591 passing tests;
- 12 skipped optional-backend tests;
- 0 failing tests;
- ~99% coverage with a 95% gate;
- standard-library runtime path;
- tests for memory, TruthGate, L3, provenance, receipts, GDPR operations, MCP,
  external ingestion and biological-memory layers.

See [../TEST_REPORT.md](../TEST_REPORT.md) for the reproducible test summary.

A **baseline evaluation harness now exists** (`core/eval.py`, run with `velantrim
eval`). On a built-in deterministic fixture it reports retrieval `hit@1/3/5` + MRR,
trace completeness, metadata completeness and receipt-replay survival — for
example:

```json
{"cases": 4, "retrieval": {"hit@1": 0.5, "hit@3": 1.0, "hit@5": 1.0, "mrr": 0.75},
 "trace_completeness": 1.0, "metadata_completeness": 1.0, "source_span_coverage": 1.0,
 "receipt_replay_survival": 1.0,
 "contradiction": {"pairs": 4, "precision": 1.0, "recall": 1.0, "false_positive_rate": 0.0}}
```

The dimensions below define where this harness is extended next (curated fixtures,
contradiction recall, source-span coverage).

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

Each public release should include a small report with:

```json
{
  "version": "0.1.x",
  "tests_passing": 591,
  "coverage": "~99%",
  "trace_completeness": null,
  "receipt_replay_survival": null,
  "retrieval_hit_at_3": null,
  "metadata_completeness": null,
  "notes": "Metrics marked null are planned evaluation harness outputs."
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
