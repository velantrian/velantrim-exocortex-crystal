# Essence Workdesk / L0.5 — Research RFC v0.2

Status: `RESEARCH_ONLY / NOT_IMPLEMENTED`
Version: `0.2`
Date: `2026-07-09`
Scope: working attention, receipt-aware reuse, and verification routing for long dialogues
Runtime impact: none
Canon write path: none
TruthGate replacement: no
Crystal runtime claim: no
Grant deliverable claim: no

## Summary

Essence Workdesk / L0.5 is a non-canonical working-attention and verification-routing layer for long Velantrim dialogues.

It is not another truth store. It does not decide what is true. It decides what should remain in active focus, what may be reused through a valid receipt, what must be routed to verification, and what can decay out of active attention.

```text
Board focuses.
Router decides.
TruthGate admits.
Canon remembers.
LLM speaks.
Benchmarks decide promotion.
```

## Why this belongs outside Crystal core

Crystal is the verifiable memory core: TruthGate, Guardian, provenance, TRACE / Receipt, audit records, and Canon admission discipline.

Essence Workdesk is a research candidate for dialogue working state. It may help reduce context pressure in long sessions, but it must not weaken the admission boundary.

This RFC therefore records only a research direction and a tiny v0 experiment. It does not create a Crystal runtime capability.

## Relationship to Research Mode

Research Mode may explore dialogue situation modeling, gap detection, evidence packs, candidate claims, and future verification workflows.

Essence Workdesk is a narrower primitive inside that direction:

```text
Situation-Aware Research Loop = broad research cycle.
Essence Workdesk = compact working board for the current dialogue state.
```

## What the Workdesk may hold

A future Workdesk may hold:

```text
current_essence        # concise description of what the dialogue is about now
active_topic           # current working topic
open_questions         # unresolved questions driving the work
decisions              # local decisions made in this session
assumptions            # provisional working assumptions, not Canon
verified_claims        # only claims with valid receipt / Canon link
stale_or_resolved      # items no longer central to active focus
```

The v0 prototype intentionally implements a much smaller in-memory board.

## Non-goals

Essence Workdesk is not:

- Canon;
- L3;
- TruthGate replacement;
- durable truth;
- a biological memory claim;
- consciousness / living AI;
- Mentaury runtime;
- Crystal runtime until separately implemented, tested, audited, and synced to GitHub main.

## Invariants

```text
EW-1: Workdesk is not Canon.
EW-2: Removing from focus is not deletion.
EW-3: Receipt reuse is memoization, not TruthGate bypass.
EW-4: New or changed factual claims require deep path.
EW-5: Decay / prune must be cheap.
EW-6: No LLM call for routine board maintenance.
EW-7: Conflict detection may flag candidates; it must not resolve truth by embedding similarity alone.
EW-8: Promotion to Crystal requires normal admission discipline.
EW-9: Workdesk overhead must be benchmarked against baseline.
EW-10: Short sessions must not pay unnecessary Workdesk cost.
```

## Fast / Deep routing discipline

The research direction may later support graded routing. The v0 prototype stays binary.

FAST may be allowed for:

- continuation of current topic;
- clarification of current local state;
- current essence;
- local decision;
- valid receipt-backed claim.

DEEP is required for:

- new factual claim;
- changed factual claim;
- conflict;
- high-risk domain;
- explicit verification request;
- Canon write request.

Future categories such as `SOFT_VERIFY`, `DEEP_VERIFY`, and `CANON_ADMISSION` remain research-only until data justifies them.

## Ultra-practical v0 experiment

The first implementation is intentionally small and lives under:

```text
prototypes/dialogue_board_v0/
```

It should not use SQL, Pydantic, sqlite-vec, embeddings, LLM calls, background workers, or runtime wiring.

The v0 question is:

```text
Can long Velantrim dialogues maintain a compact working essence without losing meaning?
```

## Minimal v0 model

```text
BoardItem
├── text
├── kind: essence | question | decision | claim
├── receipt_hash?
├── valid
├── pinned
├── last_touched
├── changed
├── high_risk
├── verification_requested
├── canon_write_requested
└── conflict
```

## Minimal prune policy

The v0 board is bounded:

```text
board size <= 7
```

When over capacity, keep items by priority:

1. pinned items;
2. valid receipt-backed claims;
3. current essence;
4. open questions / decisions;
5. most recent remaining items.

Removing an item from the active board is not deletion, not erasure, and not a claim that the item is false.

## Required v0 metrics

Before any promotion beyond prototype-only status, measure:

```text
latency_ms
input_tokens
fast_path_rate
wrong_fast_path_count
essence_retention_failures
```

A reduction in token use is not enough. The active meaning of the dialogue must remain intact, and no unsafe fast path may bypass verification.

## Boundary with Mentaury

Essence Workdesk and Mentaury share a research concern: compact active working state without confusing salience with truth.

They remain architecturally separate:

```text
Essence Workdesk = Research Mode dialogue-attention layer.
Mentaury M0 / Working World Model = sandbox-local working projection.
Crystal Canon = verified truth authority.
```

No shared runtime, adapter, or Canon bridge is introduced by this RFC.

## Promotion path

```text
Research Mode note
→ neutral engineering primitive
→ RFC
→ tiny v0 prototype
→ real-dialogue measurement
→ tests
→ audit
→ GitHub main
→ Crystal documentation
→ grant-safe claim only if supported
```

Until then, Essence Workdesk remains research-only.
