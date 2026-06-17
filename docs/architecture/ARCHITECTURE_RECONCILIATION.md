# Architecture Reconciliation

> Date: 2026-06-17
> Scope: terminology and public-claim boundary for Crystal
> Status: docs-only. Existing code names should not be renamed by this document.

## Purpose

Velantrim has multiple design lines: Crystal, Titan, V8.x, V9/V10 research notes, Noetic/Research Mode and private Full Exo-Cortex pages. Crystal needs one public reading rule.

## Canonical formula

```text
Graph = Truth
LLM = Voice
Memory = Physiology
Cognition = Meta-Layer
Volition = Agency
```

For Crystal public wording, use the formula carefully:

```text
LLM is a speech/synthesis layer, not the source of verified truth.
```

## Current truth source

For Crystal, the repository implementation and `TEST_REPORT.md` are the public technical source of truth.

Notion is strategy and planning.
Titan is private/full research.
V9/V10 documents are research or roadmap unless implemented and tested in Crystal.

## Naming rules

1. Do not rename existing implemented components without a migration reason.
2. Map future research concepts onto existing names instead of creating parallel terms.
3. Use explicit status labels: `IMPLEMENTED`, `FEATURE_FLAGGED`, `DOCUMENTED_ONLY`, `RESEARCH`, `LEGACY`, `SUPERSEDED`.
4. If a concept exists only in Research Mode, do not describe it as current Crystal runtime.

## Essence vs Cognition

Use this distinction:

| Term | Meaning | Crystal status |
|---|---|---|
| `Essence` | answer-facing gist or summary from available facts | only where implemented/tested |
| `Cognition Layer` | future meta-layer for goal, situation, causality and uncertainty | research/RFC unless implemented |
| `Working Notebook` | model of active user/task context | research/RFC unless implemented |

## OpenClaw boundary

OpenClaw-related memory-fabric ideas are external unless explicitly ported through a controlled Crystal RFC and tests.

## Public non-claims

Crystal should not claim:

- new Transformer architecture;
- AGI or consciousness;
- autonomous mind;
- NoeticCore as current runtime;
- full BICA implementation;
- production Titan UI;
- verified universal knowledge graph.

## What Crystal may extract from Titan

Crystal may extract:

- epistemic contracts;
- evidence/source rules;
- provenance and receipt requirements;
- deployment hardening lessons;
- lightweight algorithms that do not change truth boundaries;
- reviewer-safe documentation.

Crystal should not import Titan wholesale.
