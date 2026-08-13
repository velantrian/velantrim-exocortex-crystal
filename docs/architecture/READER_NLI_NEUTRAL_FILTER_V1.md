# Reader NLI Neutral-Filter Evaluation v1

Status: **IN PROGRESS — PREREGISTERED BEFORE RESULT**

Tracking issue: #388.

## Purpose

Evaluate one offline proposition-relation filter after the frozen semantic Comparator v1, while preserving all semantic useful recall. This is evaluation only and does not authorize Reader runtime changes.

## Frozen rule

1. Reuse Comparator v1 semantic top-5 unchanged.
2. Classify each query/candidate pair in both directions with the pinned NLI model.
3. Filter only when both directional argmax labels are `neutral`.
4. Otherwise retain the candidate in its original semantic order.
5. No threshold fitting, score fusion, qrel-informed tuning or backfill.

## Frozen identity

Semantic model: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` at revision `e8f8c211226b894fcb81acc59f3b34ba3efd5f42`.

NLI model: `MoritzLaurer/multilingual-MiniLMv2-L6-mnli-xnli` at revision `0a71e92a985b6e1ad1828cf67ce9c459639c1dca`; safetensors SHA-256 `91b323ccf247ec1e3b5925d566230bae7c52de8147e6062b42e250089a3fc80b`.

Dependency lock: `eval/reader_nli_neutral_filter_v1_requirements.txt`, 59 packages, SHA-256 `9a2902d1b7d5b7ca5b5105be46d1a1151fddf683e0ed67b078a09c948b3f4bd9`.

Machine-readable preregistration: `eval/reader_nli_neutral_filter_v1_preregistration.json`, committed before any qualifying result.

## Execution and gates

Qualifying execution is CPU-only, uses preloaded immutable assets, offline Transformers/Hugging Face mode, network namespace isolation, zero query-time network calls, and no external Reader source-text transmission. Two complete passes must have the same discrete fingerprint.

The historical RC-10 gate and frozen Evaluation Surface v2 gate remain unchanged. The additional no-recall-loss overlay requires 48/48 useful retained, Recall@5=1.0, all-useful-query rate=1.0, MRR=1.0, and retention of all six Comparator-v1 recovered RC-9 misses.

## Authority boundary

NLI labels are diagnostic signals, not identity or adjudication. Filtering is not epistemic authority. PASS means only `ELIGIBLE_FOR_ARCHITECTURE_REVIEW_ONLY`, never runtime authorization.

## Non-scope and STOP

No Reader runtime, hybrid runtime, FTS, ANN, vectors, pgvector, fine-tuning, second model, generic reranker, LLM judge, evidence admission, Canon/TruthGate/Guardian mutation, or #155/#165/#214 implementation. After complete closure of this bounded evaluation: STOP.
