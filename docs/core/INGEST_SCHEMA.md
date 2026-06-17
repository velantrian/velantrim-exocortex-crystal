# Ingest Schema Contract

> Date: 2026-06-17
> Scope: source-first fact ingestion contract for Crystal
> Status: docs-only; implementation must be verified separately.

## Purpose

Crystal ingestion must preserve enough metadata for later review, TruthGate decisions and TRACE/Receipt output.

```text
No source -> no confident answer.
No evidence path -> no verified canon claim.
```

## Minimal KnowledgeUnit fields

| Field | Required | Meaning |
|---|---:|---|
| `fact_id` | yes | stable, meaningful identifier |
| `claim` | yes | self-contained factual statement |
| `source` | yes | origin of the claim |
| `confidence` | yes | reliability estimate, not salience |
| `claim_type` | recommended | kind of statement |
| `origin_type` | recommended | where the claim came from |
| `evidence_ref` | recommended | page/span/row/url/reference |
| `truth_status` | yes | current verification status |
| `review_status` | recommended | workflow status |

## Self-contained claim rule

The `claim` must contain the distinguishing fact. It must not rely on a neighbouring title or table column.

Bad:

```text
claim = "capital, euro"
```

Good:

```text
claim = "The capital of France is Paris; the currency is the euro."
```

## Source rule

The source must identify where the claim came from. A parser label, type label, or generated batch marker is not enough by itself for verified factual status.

## Default status

Imported claims should default to non-verified states unless the import path has review and evidence.

Recommended default:

```text
truth_status = UNVERIFIED or PENDING_REVIEW
review_status = pending
```

## High-risk factual domains

For important factual claims, require stronger evidence metadata before verified use.

## Verifier checklist

The ingest verifier should check:

1. required fields exist;
2. `claim` is not empty and is self-contained;
3. `source` is not empty and is not merely a type label;
4. duplicate IDs are rejected;
5. duplicate normalized claims are flagged;
6. evidence requirements are enforced for important domains;
7. generated or derived claims remain pending until reviewed.

## Public wording

Safe:

```text
Crystal defines a source-first ingestion contract for reviewable AI memory.
```

Avoid unless implemented and tested:

```text
All imported corpora are already verified knowledge.
```
