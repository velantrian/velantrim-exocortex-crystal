# Response Policy v0

**Deterministic read-path only response decision module.**

`response_policy` is a small, pure, testable component that decides **how to phrase** an answer based on already-computed epistemic status and confidence. It lives entirely on the read path.

It does **not** replace TruthGate.  
It does **not** perform any write-path admission.  
It does **not** write to L3 / Canon.  
It does **not** change ESM state.

## Core Idea

After TruthGate (or equivalent evaluation) has produced an epistemic status (`CONFIRMED`, `PROBABLE`, `SPECULATIVE`, `CONFLICTED`, `UNKNOWN` etc.) and a confidence score, `response_policy` maps that to a response strategy:

| Epistemic Status + Conditions       | Response Type    | Meaning |
|-------------------------------------|------------------|---------|
| `CONFIRMED` + confidence ≥ 0.80     | `ASSERT`         | State directly and confidently |
| `CONFIRMED`/`PROBABLE` + confidence ≥ 0.50 | `HEDGE`     | Use cautious language |
| `SPECULATIVE` or low-confidence     | `SPECULATIVE`    | Frame as hypothesis / possibility |
| `CONFLICTED` or explicit contradiction | `REFUSE`      | Decline firm answer |
| `UNKNOWN` / `INSUFFICIENT_EVIDENCE` | `CITE_OR_LIMIT`  | Cite what exists and limit scope |
| Fallback                            | `ACKNOWLEDGE`    | Neutral acknowledgment |

## Invariants (must hold)

- **Read-path only** — never calls `truth_gate`, `transition_esm`, `merge_fact`, `get_l3_graph`.
- **No L3 / Canon writes** — this module never attempts to promote anything to canonical memory.
- **Mode hints are read-path only** — `mode="strict"` can only make the decision more conservative. It **cannot** upgrade weak evidence into an `ASSERT` that would bypass TruthGate.
- **Deterministic & pure** — same inputs always produce same output. No randomness, no I/O, no mutation of external state.
- **Does not weaken TruthGate** — TruthGate remains the single gate for any L3 write. This module only affects how we *speak* about already-evaluated claims.

## Non-goals of v0 (explicit)

- No integration into `generate_answer` / main response loop in this PR.
- No Essence Engine, no Mode Spine, no Research Mode extensions.
- No new runtime dependencies.
- No biological metaphors or Velantrim persona names (Velaris, Karin, Aktaris etc.).
- No changes to write-path admission logic.

## Usage Example

```python
from core.response_policy import decide_response_policy

decision = decide_response_policy(
    epistemic_status="PROBABLE",
    confidence=0.67,
    has_contradiction=False,
    mode="normal"
)

print(decision)  # → "HEDGE"
```

## Why this separation matters

`TruthGate` answers: **"Is this claim admissible to L3 Canon?"**  
`response_policy` answers: **"Given what we know, how should we express the answer to the user?"**

Keeping them separate preserves the integrity of the write path while giving us clean, testable control over response tone and epistemic honesty on the read path.

---

**Status**: v0 — minimal deterministic implementation.  
**Next (future PRs)**: Integration point with response generation (behind feature flag), richer guidance, audit logging of policy decisions.
