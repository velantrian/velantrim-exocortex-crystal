# Velantrim Crystal — Dogfooding Epistemic Cases Log

**Status:** Dogfooding / evaluation data
**Runtime status:** No runtime claim — this file changes no behaviour
**Scope:** Documentation only
**Tracking issue:** [#158](https://github.com/velantrian/velantrim-exocortex-crystal/issues/158)

> **This log is evaluation input, not a source of truth.**
> It records observed cases where Crystal should expose evidence state clearly
> (KNOWN / PARTIAL / UNKNOWN). It does **not** assign or change truth status.
> Nothing in this file may feed L3, and it must never bypass or weaken the
> **FactsPack → TruthGate → Guardian → TRACE → Receipt** boundary. Cases here are
> requirements/observations for the proposed Epistemic Router / Evidence State
> Layer; they are not audited results and confer no confidence on any claim.

## Purpose

This is a practical validation track for the proposed Epistemic Router / Evidence
State Layer. We collect real cases where Crystal's answer *should* carry an explicit
evidence state — confidently **KNOWN**, qualified **PARTIAL**, or honestly
**UNKNOWN** — and note where current behaviour diverges. The log turns the abstract
goal ("understand the truth, do not hallucinate") into concrete, reviewable cases
that future runtime work can be measured against.

It complements, but does not replace, the authoritative evaluation docs:
- [`../EVAL.md`](../EVAL.md) — the evaluation plan and current metric baseline (authoritative).
- [`../EPISTEMIC_INFRASTRUCTURE_UPGRADE.md`](../EPISTEMIC_INFRASTRUCTURE_UPGRADE.md) — the future epistemic-state RFC.
- [`../core/CLAIM_TYPE_AND_ORIGIN.md`](../core/CLAIM_TYPE_AND_ORIGIN.md) — claim type / origin / `UNKNOWN` source status.
- [`../benchmarks/CASE_FORMAT.md`](../benchmarks/CASE_FORMAT.md) — the reproducible benchmark case schema.

## Reusable case template

Copy this block per case and fill it in:

```text
case_id:
query:
expected_state: KNOWN | PARTIAL | UNKNOWN
actual_behavior:
facts_retrieved:
truthgate_result:
guardian_result:
trace_available: yes/no
receipt_available: yes/no
problem_type: overconfident_answer | unclear_rejection | missing_partial_state | silent_failure | contradiction_not_explained | other
notes:
```

## Initial case categories

- System should answer with confidence but gives weak output.
- System should say insufficient evidence but answers confidently.
- System has partial evidence but does not mark its limits.
- TruthGate rejects a claim but does not explain why.
- A contradiction exists but the review path is unclear.
- A TRACE exists but the reviewer cannot see the exact evidence span.

## Cases

> The entries below are **placeholders / illustrative examples**, not audited real
> results. They show how to fill the template and seed the initial categories.
> Replace them with real observed cases as dogfooding proceeds.

### EX-001 — confident answer expected, output too weak

```text
case_id: EX-001
query: "What is the boiling point of water at sea level?"
expected_state: KNOWN
actual_behavior: Answer hedges ("around 100 °C, possibly") despite a single, well-supported fact.
facts_retrieved: 1 supporting fact (verified)
truthgate_result: pass
guardian_result: pass
trace_available: yes
receipt_available: yes
problem_type: missing_partial_state
notes: PLACEHOLDER — example only. KNOWN state should read as confident, not hedged, when evidence is sufficient.
```

### EX-002 — should say UNKNOWN, but answers confidently

```text
case_id: EX-002
query: "What did internal memo X conclude about project Y?"
expected_state: UNKNOWN
actual_behavior: System produces a fluent, specific answer with no supporting fact in the store.
facts_retrieved: 0 supporting facts
truthgate_result: (not reached / not surfaced to user)
guardian_result: pass
trace_available: no
receipt_available: no
problem_type: overconfident_answer
notes: PLACEHOLDER — example only. With no evidence the response must surface UNKNOWN, not fabricate detail.
```

### EX-003 — partial evidence, limits not marked

```text
case_id: EX-003
query: "Summarize the side effects of medication Z."
expected_state: PARTIAL
actual_behavior: System lists some side effects as if complete; coverage gap is not flagged.
facts_retrieved: 2 supporting facts (partial coverage of the topic)
truthgate_result: pass
guardian_result: pass
trace_available: yes
receipt_available: yes
problem_type: missing_partial_state
notes: PLACEHOLDER — example only. PARTIAL answers should state what is and is not covered by retrieved evidence.
```

### EX-004 — TruthGate rejects without explanation

```text
case_id: EX-004
query: "Is claim Q true?"
expected_state: UNKNOWN
actual_behavior: Claim is rejected, but the user sees no reason and no path to review.
facts_retrieved: 1 candidate (conflicting / unverified)
truthgate_result: reject
guardian_result: pass
trace_available: yes
receipt_available: yes
problem_type: unclear_rejection
notes: PLACEHOLDER — example only. A rejection should expose why (e.g. unverified / contradicted) and how to review.
```

## How to contribute a case

1. Reproduce the query against current Crystal.
2. Fill one template block; choose the closest `problem_type`.
3. Record `expected_state` (what an honest evidence-aware system should return) and
   `actual_behavior` (what happened), without editing any verified fact.
4. Keep entries factual and reviewer-safe; this log makes no runtime claims.
