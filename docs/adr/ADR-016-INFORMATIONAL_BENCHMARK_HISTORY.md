# ADR-016: Keep retrieval performance history informational and reproducible

- **Status:** Accepted baseline
- **Date:** 2026-08-01
- **Scope:** SQLite L3 retrieval smoke benchmark history

## Context

Crystal already has a deterministic `scripts/bench_l3_retrieval.py` benchmark and
historical local measurements. Running it only by hand makes trends easy to miss,
but enforcing absolute latency thresholds on shared GitHub-hosted runners would
create a noisy and misleading merge gate.

A second benchmark methodology would also make old and new results difficult to
compare.

## Decision

Crystal retains the existing benchmark as the sole workload generator and adds:

- a weekly/manual `L3 Benchmark History` workflow;
- versioned history envelopes containing the unchanged raw result plus
  content-light run metadata;
- Markdown summaries and 90-day Actions artifacts;
- an offline comparison command for shared fact counts;
- ratio warnings that remain informational.

The normal pull-request CI matrix does not gain a latency threshold.

## Comparison rules

- compare only shared fact sizes;
- expose backend/embedder comparability;
- require identical measured-search, template, `top_k` and warmup workload before
  issuing a ratio warning;
- report p50 and p95 ratios;
- do not fail because a hosted-runner ratio crosses the warning threshold;
- reproduce suspected regressions on controlled hardware before making a
  performance conclusion.

## Consequences

- performance runs become visible and repeatable;
- raw and packaged results remain separately inspectable;
- history tooling cannot change admission, truth or retrieval ranking policy;
- hosted-runner variance does not block ordinary code review;
- artifacts are retained for a bounded period and may be exported for releases.

## Non-goals

- no production SLO;
- no promise of stable GitHub-hosted hardware;
- no ANN or backend optimization;
- no benchmark of answer correctness, Guardian, TruthGate or full query latency;
- no replacement for the historical local A/B evidence;
- no automatic claim that a warning is a confirmed regression.
