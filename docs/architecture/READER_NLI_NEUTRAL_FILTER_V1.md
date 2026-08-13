# Reader NLI Neutral-Filter Evaluation v1

Status: **COMPLETED — FROZEN GATE FAIL**

Tracking issue: #388. Pull request: #389.

## Purpose

Evaluate exactly one bounded offline proposition-relation filter after frozen Reader Retrieval Comparator v1. The filter was preregistered before the qualifying result and was required to improve discrimination **without losing semantic useful recall**. This evaluation does not authorize Reader runtime changes.

## Frozen rule

1. Reuse Comparator v1 semantic top-5 unchanged.
2. Classify each query/candidate pair in both directions with the pinned NLI model.
3. Filter only when both directional argmax labels are `neutral`.
4. Otherwise retain the candidate in its original semantic order.
5. No backfill, threshold fitting, score fusion, qrel-informed tuning, or post-result rule changes.

## Frozen identity

Semantic model: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` at revision `e8f8c211226b894fcb81acc59f3b34ba3efd5f42`; safetensors SHA-256 `eaa086f0ffee582aeb45b36e34cdd1fe2d6de2bef61f8a559a1bbc9bd955917b`.

NLI model: `MoritzLaurer/multilingual-MiniLMv2-L6-mnli-xnli` at revision `0a71e92a985b6e1ad1828cf67ce9c459639c1dca`; safetensors SHA-256 `91b323ccf247ec1e3b5925d566230bae7c52de8147e6062b42e250089a3fc80b`.

Dependency lock: `eval/reader_nli_neutral_filter_v1_requirements.txt`, 59 exact packages, SHA-256 `9a2902d1b7d5b7ca5b5105be46d1a1151fddf683e0ed67b078a09c948b3f4bd9`.

Machine-readable preregistration: `eval/reader_nli_neutral_filter_v1_preregistration.json`, committed before qualifying execution.

## Qualifying evidence

- GitHub Actions run: `31736269934`
- Qualifying job: `94568540864` (`test (3.11)`)
- Exact qualifying head: `9520d3d8b93020e8570702e7dcf13459b3bf6d18`
- Preserved Actions artifact: `pytest-3.11-log`, artifact id `9195428397`
- Artifact ZIP SHA-256: `0fe8ade137aec6c2caab85f8ec5ef4f9ab988140c0b870044a6924f4bb322e5b`
- Full runner-generated qualifying result SHA-256: `4f1e1391c3c4983d4a090429aae2f67d430d9d7891ca6f0da1e90457033dc315`
- Frozen repository summary: `eval/reader_nli_neutral_filter_v1_result.json`

The qualifying run used CPU, preloaded immutable model assets, `HF_HUB_OFFLINE=1`, `TRANSFORMERS_OFFLINE=1`, a network namespace isolation requirement, and no external Reader source-text transmission. Two complete evaluation passes produced the same discrete fingerprint: `cae703bd3cb38aa80334c013b5f17860f9e36c013092a2ea6f81b2426c71b132`.

## Result

Frozen classification: **`NLI_NEUTRAL_FILTER_GATE_FAILED`**.

| Surface | Comparator v1 | NLI neutral filter v1 | Outcome |
|---|---:|---:|---|
| Historical useful / positive hits | 16 / 16 | 15 / 16 | recall regression |
| Historical Recall@5 | 1.000000 | 0.937500 | fail |
| Historical MRR | 1.000000 | 0.937500 | gate threshold met, but recall lost |
| Historical hard negatives | 4 / 4 | 1 / 4 | discrimination improved |
| v2 useful hits | 48 / 48 | 46 / 48 | recall regression |
| v2 useful Recall@5 | 1.000000 | 0.958333 | minimum gate met, no-recall overlay failed |
| v2 MRR | 1.000000 | 1.000000 | retained |
| v2 hard negatives | 41 / 48 | 18 / 48 | discrimination improved |
| v2 hard-negative rate | 0.854167 | 0.375000 | overall discrimination gate met |
| RC-9 misses retained after prior recovery | 6 / 6 | 5 / 6 | fail |

The historical useful case lost by the filter was `rc8-020`. On Evaluation Surface v2 the lost useful candidates were `v2-c-0a8ace12cae2f46b` and `v2-c-7dd0f1454ab1266a`; the first was one of the six Comparator-v1 recovered RC-9 misses.

The v2 overall hard-negative count/rate passed, but the frozen per-stratum hard-negative gate failed. `boilerplate_same_topic`, `cross_lingual_paraphrase`, `homonym_entity_collision`, and `negation_polarity` each retained `3/4` hard negatives (`0.75`), above the allowed `0.50`.

## Gate verdict

- Historical gate: **FAIL** — 15/16 positive hits and Recall@5 0.9375.
- Evaluation Surface v2 gate: **FAIL** — per-stratum hard-negative gate failed and prior useful recovery was not fully retained.
- No-recall-loss overlay: **FAIL** — 46/48 useful, all-useful-query rate 0.916667, Recall@5 0.958333, and only 5/6 recovered RC-9 misses retained.
- Repeatability: **PASS**.
- Authority violations: **0**.
- Overall gate: **FAIL**.

The result is informative rather than null: bidirectional neutral filtering sharply reduced hard negatives, but the frozen rule is not recall-safe and is therefore **not admissible as the next Reader retrieval stage**.

## Authority boundary

NLI labels remain diagnostic signals only:

- NLI label ≠ proposition identity;
- NLI label ≠ evidence adjudication;
- filtering ≠ epistemic authority;
- evaluation result ≠ runtime authorization.

`runtime_authorization = false`. No Reader semantic/hybrid runtime, FTS, ANN, vectors, pgvector, evidence admission, Canon mutation, TruthGate mutation, Guardian bypass, or other authority expansion is authorized by this milestone.

## Security and closure

The qualifying transient runner triggered Bandit B615 because local `from_pretrained()` calls did not carry an explicit revision argument. The qualifying assets were already immutable-checksum-pinned and offline, but the security gate is not suppressed or weakened. The transient runner, qualifying test, and temporary coverage configuration are removed after freezing the result; only static evidence remains.

## Non-scope and STOP

No fine-tuning, second NLI model, generic reranker, LLM judge, hand-authored discriminator, score fusion, fitted threshold, qrel tuning, benchmark rewrite, runtime integration, or implementation of #155/#165/#214 is part of this closure.

After merge, post-merge CI, Notion synchronization/read-back, completion evidence, issue closure, and final live audit: **STOP**.
