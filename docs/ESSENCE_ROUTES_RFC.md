# Essence Routes RFC

**Status:** RFC / roadmap  
**Runtime status:** Not implemented in the current Crystal core  
**Implementation claim:** false  
**Scope:** documentation only  
**Intended phase:** future research / post-Crystal stabilization  
**Safety boundary:** must not weaken TruthGate, Guardian, TRACE, Receipt, L3 write policy, or existing schemas

## Summary

Essence Routes is a proposed meaning-aware routing layer for Velantrim Crystal and the broader Velantrim Exo-Cortex research line.

The core idea is simple:

```text
Do not only ask: what should the system retrieve?
Ask first: what kind of epistemic path is needed for this query?
```

Traditional retrieval usually searches similar text. Graph-based retrieval can search related nodes or subgraphs. Essence Routes proposes an additional planning step before retrieval: classify the query's epistemic route, choose allowed retrievers and graph edge types, apply route-specific warnings and constraints, and document the route choice in TRACE.

This RFC does not describe a current runtime feature. It is a future design proposal.

## Non-claims

This document does **not** claim that Crystal currently implements Essence Routes.

It also does not claim:

- autonomous understanding;
- brain-like cognition;
- AGI or consciousness;
- zero hallucinations;
- production readiness;
- automatic causal reasoning;
- automatic verified truth promotion;
- route selection as a replacement for TruthGate.

Essence Routes, if implemented later, would be a control and planning layer below TruthGate and Guardian.

## Position in the architecture

Current simplified Crystal path:

```text
User query
→ normalizer / parser
→ retrieval
→ FactsPack
→ TruthGate
→ Guardian
→ TRACE / Receipt
→ answer
```

Possible future path with Essence Routes:

```text
User query
→ normalizer / parser
→ query type / essence detection
→ RoutePlan
→ route-aware retrieval
→ route-aware FactsPack
→ TruthGate
→ Guardian
→ route-aware TRACE / Receipt
→ answer
```

Essence Routes would not decide what is true. It would only propose how to search and how to label the epistemic boundary for the answer path.

## Core formula

```text
Intent Router = what the user appears to ask for.
Essence Router = what epistemic path may be needed.
Graph / retrieval = where candidate evidence is found.
TruthGate = what may support confident treatment.
Guardian = what actions and promotions are allowed.
TRACE = why the route and answer path happened.
```

## RoutePlan contract

A future implementation should center on an explicit `RoutePlan`, not on an opaque classifier.

Example shape:

```json
{
  "route_id": "CAUSE_ROUTE",
  "query_type": "WHY",
  "deep_intent": "causal_explanation",
  "allowed_retrievers": ["bm25", "graph", "evidence_store"],
  "allowed_edge_types": ["CAUSES", "ENABLES", "BLOCKS", "LEADS_TO"],
  "allowed_truth_status": ["VERIFIED", "CITED", "HYPOTHESIS"],
  "requires_trace": true,
  "requires_warning_for_hypothesis": true,
  "fallback": "gap_notice"
}
```

The RoutePlan must be auditable. TRACE should record the selected route, fallback, warnings, constraints, and whether the system used a simple or multi-route path.

## Minimal route taxonomy

The initial research taxonomy should remain small.

| Route | Purpose | Typical edge types / constraints |
|---|---|---|
| `FACT_ROUTE` | Source-grounded factual answers | `IS_A`, `HAS_PROPERTY`, `EVIDENCED_BY`; requires evidence |
| `CAUSE_ROUTE` | Why / mechanism / consequence questions | `CAUSES`, `ENABLES`, `BLOCKS`, `LEADS_TO`; causal uncertainty warnings when needed |
| `PROCEDURE_ROUTE` | How-to and stepwise processes | `STEP_OF`, `REQUIRES`, `NEXT`, `CONSTRAINT`; include risks and prerequisites |
| `MEMORY_ROUTE` | User-reported memory, decisions, episodes | requires internal `episode_ref` or trace; cannot promote to `WORLD_FACT` |
| `CONTRADICTION_ROUTE` | Audits, conflicts, stale claims | `CONTRADICTS`, `WEAKENS`, `REFUTES`, `SUPERSEDES`; requires explicit conflict surfacing |
| `ARCHITECTURE_ROUTE` | System structure and component relations | `PART_OF`, `DEPENDS_ON`, `INPUT_TO`, `OUTPUT_TO`, `PROTECTS` |
| `GAP_ROUTE` | Missing evidence / low confidence / unknowns | triggers honest uncertainty, research task, or refusal |
| `SPARK_ROUTE` | Creative or speculative exploration | mode trace required; no L3 promotion; fiction/hypothesis boundary required |

## Critical epistemic rules

### Memory is not world truth

`MEMORY_ROUTE` must not allow user-reported experience, preference, emotion, or interpretation to become `WORLD_FACT` without explicit conversion, evidence, and review.

Safer phrasing:

```text
requires_external_evidence: false
requires_episode_ref: true
cannot_promote_to: WORLD_FACT
```

Personal memory does not require an external source to be represented as personal memory, but it still requires internal provenance: episode, trace, import record, or user-stated source.

### Spark is not evidence

`SPARK_ROUTE` may support imagination, analogies, and speculative design. It must not write verified facts.

Safer phrasing:

```text
requires_fact_trace: false
requires_mode_trace: true
requires_boundary_marker: true
promotion_blocked: true
cannot_write_to: L3
```

Creative output can be useful, but it is not evidence.

### Route selection is not truth validation

A selected route cannot override TruthGate or Guardian.

Hierarchy:

```text
Guardian / invariants
→ TruthGate / epistemic admission
→ route policy
→ FactsPack
→ answer wording
```

## Suggested MVP path

Do not implement the full system first.

### Phase 0: RFC only

- Keep this document as design research.
- Do not change runtime code.
- Do not present Essence Routes as implemented.

### Phase 1: Routes Lite

Possible low-risk future step:

```text
query_type tag
+ route tag in TRACE
+ basic warnings in answer policy
```

Minimal query types:

- `FACT`
- `CAUSE`
- `MEMORY`
- `CREATIVE`
- `GAP`

This would provide some epistemic boundary value without a new routing subsystem.

### Phase 2: RoutePlan MVP

Only after real failure cases:

- `RoutePlan` dataclass / schema;
- route selection tests;
- route tags in TRACE;
- route-specific warnings;
- no graph-path expansion yet.

### Phase 3: Full Essence Routing

Only after measurement proves value:

- route registry;
- route planner;
- route-aware graph traversal;
- route-aware FactsPack assembly;
- route-aware TruthGate checks;
- evaluation harness.

## Evaluation metrics

If implemented, Essence Routes should be evaluated against a baseline. Suggested metrics:

| Metric | Meaning |
|---|---|
| Route selection accuracy | Did the system choose the expected route for labelled test queries? |
| Epistemic boundary violations | Did memory, hypothesis, or fiction become treated as verified fact? |
| Route-aware TRACE completeness | Does the trace show route choice, reasons, warnings, and fallbacks? |
| Path quality score | Are graph paths coherent, relevant, and supported by evidence? |
| Baseline lift | Does route-aware processing improve answer quality over simple retrieval? |

A full implementation should not be promoted without measured improvement or clear failure-case evidence.

## Anti-scope-creep rule

Essence Routes should not block Crystal release work.

Use this rule:

```text
Capture as RFC.
Do not implement until Crystal is stable and real failure cases justify it.
```

## Relationship to existing Crystal boundaries

Essence Routes would reuse existing Crystal principles:

- LLM output is not evidence;
- verified memory requires source / provenance / trace;
- hypotheses must remain hypotheses;
- personal memory is not world fact;
- creative mode cannot write to verified canon;
- unsupported confidence should be refused or downgraded.

## Open questions

- Should route selection be rule-based, classifier-based, or hybrid?
- How should route confidence be calibrated?
- What is the smallest useful `RoutePlan` schema?
- Which failure cases justify full Essence Routes rather than Routes Lite?
- How should multi-route fusion resolve conflicts?
- Which route decisions must be visible to users versus only in TRACE?

## Current recommendation

Keep Essence Routes as a future RFC and research direction.

Near-term safe implementation, if any, should be **Routes Lite** only: query type tags, warnings, and TRACE metadata. Full route-aware retrieval should wait for real failure cases and evaluation.
