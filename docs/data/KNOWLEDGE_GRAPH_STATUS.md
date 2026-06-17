# Knowledge Graph Status

> Date: 2026-06-17
> Scope: data-quality and claim-status boundary for Crystal
> Status: docs-only.

## Rule

A graph is not a verified canon merely because it has nodes and edges.

```text
Graph structure is not evidence.
Autolinked relations are not verified truth.
Synthetic labels are not external provenance.
```

Crystal should distinguish:

| Data state | Meaning |
|---|---|
| `VERIFIED_CANON` | reviewed, source-grounded, trace-valid facts |
| `UNVERIFIED_GRAPH_DRAFT` | imported graph without sufficient evidence |
| `AUTOLINKER_PROTOTYPE` | heuristic or inferred edges |
| `PENDING_REVIEW` | candidate knowledge awaiting review |
| `QUARANTINED` | blocked from confident use |

## Source requirement

A source should point to a real origin, such as a document identifier, page/span, dataset row, URL, publication metadata, or curator note.

The following is not sufficient as evidence by itself:

```text
wsc:METHOD
wsc:invariant
wsc:variant
source == type
source == parser label
```

## Evidence requirement

Important factual domains need stricter evidence metadata.

Recommended fields:

```json
{
  "source": "...",
  "evidence_ref": "page/span/row/url",
  "claim_type": "WORLD_FACT",
  "origin_type": "EXTERNAL",
  "truth_status": "UNVERIFIED | VERIFIED",
  "review_status": "pending | reviewed | rejected"
}
```

## Autolinker edges

Autolinker output should default to:

```text
truth_status = UNVERIFIED
knowledge_status = inferred
origin_type = DERIVED or SYSTEM_GENERATED
review_status = pending_review
```

It must not become `VERIFIED` or canonical L3 truth only because a heuristic linked two nodes.

## Verifier requirements

Future data validation should check:

1. allowed type vocabulary;
2. non-empty source field;
3. evidence_ref for important factual claims;
4. self-contained claim text;
5. no heading accidentally stored as `type`;
6. no synthetic source mistaken for external evidence;
7. no autolinker edges promoted without review.

## Public wording

Safe:

```text
Crystal can ingest and review knowledge graphs with provenance and evidence controls.
```

Avoid unless separately proven:

```text
Crystal ships a verified universal knowledge graph.
```

## Claude Code follow-up

Claude Code should inspect actual data files and add a verifier only after confirming the concrete schema. The verifier should reject malformed type, source, and evidence fields instead of silently promoting heuristic edges.
