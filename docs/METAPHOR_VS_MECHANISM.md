# Metaphor vs Mechanism

> Velantrim uses some biologically inspired names as engineering metaphors.
> These names do not claim biological implementation.

## 1. Purpose

This document separates the **software mechanisms** Velantrim Crystal actually
implements from the **biological inspiration** behind some of their names. Its
goals are to:

- prevent overclaim and protect grant/reviewer clarity;
- make explicit that Crystal does **not** implement biology, cognition,
  consciousness, or a brain model;
- preserve the implemented-vs-research distinction that
  [`IMPLEMENTATION_STATUS.md`](./IMPLEMENTATION_STATUS.md) already maintains as
  the single source of implementation truth.

Names such as "CRISPR Guard", "Neurogenesis", or "Immune Layer" are engineering
metaphors for ordinary software mechanisms (signature matching, capacity
allocation, anomaly detection). They are not claims about biology.

## 2. Non-claims

Velantrim Crystal does **not** claim to:

- model the human brain;
- implement biological cognition;
- implement a nervous system;
- implement an immune system;
- implement genetics or CRISPR;
- create consciousness;
- create AGI;
- eliminate hallucinations completely;
- replace expert judgment;
- operate as an autonomous mind.

## 3. Table A — Implemented software mechanisms

Each row below is backed by code in `core/` **and** tests in `tests/`. Status
is verified against the current branch.

| Name | Status | Actual software mechanism | Inspiration / analogy | Explicit non-claim |
|---|---|---|---|---|
| **Fractal Memory** | Implemented (baseline) | Multi-scale anchoring: a deterministic `anchor_strength` sorts facts into SHORT→MEDIUM→LONG→CORE bands written to `metadata['fractal_scale']`; `core/consolidate.py` reads that scale to lengthen each fact's decay half-life, with CORE anchors exempt from decay (`core/fractal.py`, RFC0070) | Forgetting curves, spacing effects, multi-scale organization | Not a biological memory model; not a hippocampal simulation; not the broader Research-Mode "Fractal Memory = Structure + Attention + Consolidation" concept |
| **Epigenetic Adaptation** | Implemented | A single global verification tag — raised by gate blocks, relaxed by successful answers — adjusts the WORLD_FACT confidence threshold used by TruthGate; never rewrites verified facts (`core/adaptation.py`, RFC0071) | High-level metaphor of contextual regulation | Not biological epigenetics; does not mutate truth; not per-fact metadata weighting |
| **Immune Layer** | Implemented | Threat-pattern memory that screens incoming claims against recorded hallucination/harmful patterns and canon contradictions, with advisory quarantine and risk flags (`core/immune.py`, RFC0072) | Immune-system metaphor | Not a biological immune system |
| **CRISPR Guard** | Implemented | Targeted threat-signature matching with quarantine / rejection of recognized patterns (part of `core/immune.py`, RFC0072) | Metaphor for targeted protective recognition | Not CRISPR, genetics, gene editing, or irreversible biological deletion (erasure/tombstones live in `core/erasure.py`, not here) |
| **Neurogenesis** | Implemented | Plasticity / maturation reporting over existing facts, pattern separation via `SEPARATED_FROM` edges, and growth & advisory prune-candidate reporting (`core/neurogenesis.py`, RFC0073) | Metaphor for adding representational capacity | Not biological neurogenesis; not creating neurons; does not itself allocate clusters or nodes |
| **Concept Emergence** | Implemented | Hebbian co-activation clustering that materializes CONCEPT entity nodes with `MEMBER_OF` links from member facts (`core/concept.py`, RFC0066) | Concept formation | Not consciousness; not spontaneous semantic understanding; no human review/promotion step in this path |
| **Memory Volition** | Implemented | `write_voluntary()` writes self-authored facts through the same Guardian → TruthGate path; a separate salience-ranked rehearsal pass (`volition_cycle()`) refreshes the decay clock via `update_fact()` without inventing evidence (confidence untouched) (`core/volition.py`, RFC0065) | Voluntary-rehearsal metaphor | Not will, agency, or conscious intention; rehearsal is not itself re-gated through TruthGate |
| **NeuroCore (Phase-0 passive tracker)** | Implemented (Phase 0) | Logs the norm of the would-be plastic weight delta when surprise > θ; off by default; never writes L3 (`core/neurocore.py`, RFC0068) | Nervous-system metaphor | Not a nervous system or brain core; active adaptation (Phase 1+) is future work |

A baseline significance-weighted FSRS-style decay also exists as
`core/consolidate.py` ("SleepCycle"). It is a decay scheduler, not biological
sleep — see Table B, row "Sleep Cycle v2", for the distinction from the
out-of-scope reconsolidation engine.

## 4. Table B — RFC / Vision / Not in Crystal runtime

These are design-only concepts. None is a runtime feature; none is wired into
`core/`. They are listed so reviewers can tell apart what is shipped from what
is merely proposed.

| Name | Status | Concept (if designed) | Inspiration / analogy | Explicit non-claim |
|---|---|---|---|---|
| **Sleep Cycle v2** | Not in Crystal runtime | A meaning / reconsolidation engine, explicitly out of scope per [`IMPLEMENTATION_STATUS.md`](./IMPLEMENTATION_STATUS.md). The shipped baseline (`core/consolidate.py`, FSRS-style decay) is a separate, narrower mechanism. | Sleep-consolidation metaphor | Not biological sleep; not autonomous dreaming |
| **Fractal Attention** | RFC / Vision | Multi-scale attention / salience prioritization. Distinct from the implemented Fractal Memory **anchoring** baseline. | Multi-scale attention metaphor | Not human attention simulation |
| **Spark / Imagination** | RFC | Sandboxed speculative generation that never writes directly to L3 (`docs/SPARK_RFC.md`) | Imagination / creativity metaphor | Not consciousness, soul, AGI, autonomous mind, or truth engine |
| **Pulse / Substrate** | RFC / Vision | A typed event-envelope / coordination-protocol concept | Pulse / signalling metaphor | Not a biological pulse, nervous system, or unified brain |

Status vocabulary, used precisely: `Implemented` · `Partially implemented
(baseline)` · `RFC` · `Future research` · `Not in Crystal runtime`. Nothing is
marked "Implemented" unless `core/` and `tests/` prove it.

## 5. Grant-safe language

**Use:** engineering metaphor · biologically inspired naming · software
mechanism · audit layer · verification gate · metadata weighting · anomaly
detection · contradiction detection · source-grounded memory · local-first
verifiable infrastructure.

**Avoid:** digital brain · biological brain implementation · consciousness ·
AGI · artificial mind · zero hallucinations · true neurogenesis · CRISPR
implementation · self-evolving intelligence · "production-ready" (unless
independently verified).

Precise, reproducible claims are **not** overclaims and are kept as-is: the
exact test count and 100% coverage gate (see [`TEST_REPORT.md`](../TEST_REPORT.md),
the single source for the current figure), the standard-library-only runtime,
local-first / no-telemetry-by-default operation, and AGPL-3.0 licensing.

## 6. Public documentation rule

Whenever a biological metaphor appears in grant- or reviewer-facing material,
either link to this file or add a short parenthetical, for example:

> Fractal Memory (engineering metaphor; not a biological memory model)

## 7. Relationship to Research Mode

Research Mode may explore biologically inspired analogies. Its outputs are
**not** Crystal runtime unless they are implemented and tested. Research Mode
cannot bypass TruthGate, Guardian, provenance, or human review, and no research
metaphor can promote data into the verified canon.

## 8. Canonical principle

> Metaphors may guide design language, but mechanisms define implementation.
> Truth status is determined by evidence, provenance, review, and
> TruthGate-compatible policy — not by metaphor.
