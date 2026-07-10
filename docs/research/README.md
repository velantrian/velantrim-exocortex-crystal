# Research documentation

**Status:** `RESEARCH / DOCUMENTED_ONLY`

Documents in this directory describe bounded architecture research. They do not
change Crystal runtime behaviour and must not be cited as implemented
capabilities unless a separate implementation PR, tests and status sync exist on
`main`.

## Boundary

```text
Research docs may define candidates, schemas, invariants, threat models and metrics.
They may not claim runtime implementation.
They may not create a direct Canon write path.
They may not bypass TruthGate, Guardian, provenance or human review.
```

## Documents

- [`dialogue-cultivation-layer.md`](./dialogue-cultivation-layer.md) — dialogue
  continuity, anti-sycophancy and user-state hypothesis boundaries; documented
  research only.
- [`COGNITIVE_STATE_AND_PLANNING_LAYERS.md`](./COGNITIVE_STATE_AND_PLANNING_LAYERS.md)
  — neutral research contracts for current-state projection, capability
  snapshots, strategy outcomes, bounded plans and user-intent hypotheses.

## Promotion rule

```text
research note
→ neutral primitive
→ separate RFC
→ invariants and threat model
→ bounded prototype
→ tests and evaluation
→ audit
→ implementation PR
→ merge to main
→ status and test-report sync
```

If a document is not backed by code and tests listed in the repository's status
sources, assume it is not a Crystal runtime feature.