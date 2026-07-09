# Dialogue Board v0 / Essence Workdesk L0.5

Status: `RESEARCH_ONLY / PROTOTYPE_ONLY`
Runtime impact: none
Canon write path: none
TruthGate replacement: no
Crystal runtime claim: no

This is a tiny in-memory prototype for the Essence Workdesk / L0.5 research direction.

It exists to test one practical question:

```text
Can a small active board preserve the current essence of long Velantrim dialogues
while reducing context pressure and avoiding unsafe fast paths?
```

## What this prototype does

- stores small `BoardItem` objects;
- routes items as `FAST` or `DEEP`;
- prunes the board to a bounded size;
- checks whether the board lost its `essence` anchor.

## What this prototype does not do

- no Crystal runtime wiring;
- no Canon writes;
- no TruthGate replacement;
- no SQL;
- no Pydantic;
- no sqlite-vec;
- no embeddings;
- no LLM calls;
- no Mentaury integration.

## Minimal routing rule

```text
FAST = local continuation / current essence / local decision / valid receipt claim
DEEP = new or changed claim / conflict / high risk / verification request / Canon write request
```

## Metrics to collect outside this module

```text
latency_ms
input_tokens
fast_path_rate
wrong_fast_path_count
essence_retention_failures
```

This module is not sufficient to claim that Essence Workdesk is a Crystal capability. Promotion requires real-dialogue measurement, tests, audit, and a separate operator decision.
