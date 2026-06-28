# Response Policy v0

**Crystal-native deterministic read-path response decision module.**

`response_policy` v0 implements a pure decision layer that maps **existing Crystal axes** (from `core/memory.py`) to a response strategy.

It uses:
- `claim_type` (WORLD_FACT, USER_EXPERIENCE, EMOTION, OPINION, GOAL, PREFERENCE, INTERPRETATION)
- `source_status` (USER_REPORTED, OBSERVED, DERIVED, EXTERNAL, LLM_OUTPUT, UNKNOWN)
- `epistemic_state` (Validated, Supported, Hypothesized, Contradicted, Deprecated, Collapsed, ImmutableCore, ...)
- `risk_domain` + `mode_hint`

**Strictly read-path only.** Never calls TruthGate, never writes to L3/Canon, never mutates ESM.

## Core Decision Rules (v0)

| Condition                                      | Action          | Notes |
|------------------------------------------------|-----------------|-------|
| claim_type in {EMOTION, USER_EXPERIENCE, OPINION, PREFERENCE, GOAL} | ACKNOWLEDGE | Subjective – do not assert as world fact |
| WORLD_FACT + source_status=LLM_OUTPUT          | REFUSE          | Model output is not ground truth |
| epistemic_state in {Contradicted, Deprecated, Collapsed} | REFUSE     | Conflict or obsolescence |
| High-risk domain (HEALTH/LEGAL/FINANCIAL/SAFETY) + not Validated | CITE_OR_LIMIT | Requires citation or scope limit |
| Validated + source in {EXTERNAL, DERIVED, OBSERVED} | ASSERT     | Strong admissible fact (citation-aware) |
| epistemic_state = Supported                    | HEDGE           | Evidence exists, not fully validated |
| WORLD_FACT + USER_REPORTED + weak state        | SPECULATIVE     | User report without strong backing |
| Default                                        | ACKNOWLEDGE     | Safe neutral fallback |

## Read-path integration

As of the follow-up read-path integration PR, `generate_answer()` exposes response policy decisions as metadata in the answer payload:

```python
{
    "answer": "...",
    "facts": [...],
    "response_policy": [
        {
            "fact_id": "f2",
            "action": "ASSERT",
            "reason": "Validated fact from reliable source.",
            "requires_citation": True,
        }
    ],
}
```

This metadata is advisory for answer framing and UI/reporting. It does not admit facts, validate facts, write to Canon, mutate ESM, or bypass TruthGate.

## Invariants (unchanged)

- Read-path only — no TruthGate calls, no `transition_esm`, no `merge_fact`, no `get_l3_graph` inside `response_policy`.
- No L3 / Canon writes from `response_policy`.
- Mode/risk hints affect only read-path phrasing and **cannot** bypass TruthGate admission.
- No new runtime dependencies.
- No Research Mode / Essence Engine concepts in this PR.

## Usage

```python
from core.response_policy import decide_response_policy, ResponsePolicyInput

inp = ResponsePolicyInput(
    claim_type="WORLD_FACT",
    source_status="EXTERNAL",
    epistemic_state="Validated",
    risk_domain="GENERAL"
)

decision = decide_response_policy(inp)
print(decision.action)           # "ASSERT"
print(decision.requires_citation) # True
```

## Non-goals

- No changes to write-path admission or TruthGate.
- No change to Canon/L3 admission semantics.
- No Research Mode / Essence Engine / Mode Spine runtime.

---

**Status**: v0 — Crystal-native MVI contract implemented and exposed as read-path answer metadata.  
**Boundary**: response_policy remains speech/framing metadata, not a truth-admission mechanism.
