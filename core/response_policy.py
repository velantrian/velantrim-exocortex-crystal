'''response_policy v0

Deterministic read-path only module for deciding response framing
based on epistemic status. Pure function with no side effects on
write path, L3, Canon, ESM or TruthGate.

This module receives already-evaluated epistemic status and returns
a speech/response strategy. It does not perform any admission checks
or mutations.
'''

from typing import Literal, Dict

ResponseType = Literal[
    "ASSERT",
    "HEDGE",
    "SPECULATIVE",
    "REFUSE",
    "ACKNOWLEDGE",
    "CITE_OR_LIMIT"
]

def decide_response_policy(
    epistemic_status: str,
    confidence: float,
    has_contradiction: bool = False,
    mode: str = "normal"
) -> ResponseType:
    """Pure deterministic decision for read-path response strategy.

    Rules (v0):
    - REFUSE if contradiction or CONFLICTED status.
    - ASSERT only for CONFIRMED + high confidence.
    - Mode hint can only downgrade (strict mode), never upgrade weak evidence.
    - All other cases map to HEDGE / SPECULATIVE / CITE_OR_LIMIT / ACKNOWLEDGE.
    - Never calls TruthGate, never writes, never affects ESM state.
    """
    if not isinstance(epistemic_status, str):
        epistemic_status = str(epistemic_status or "")

    status = epistemic_status.strip().upper()
    conf = float(confidence) if confidence is not None else 0.0
    contradict = bool(has_contradiction)
    mode = (mode or "normal").lower().strip()

    if contradict or status == "CONFLICTED":
        return "REFUSE"

    # Strict mode can only make decision more conservative (downgrade),
    # never promote weak support to ASSERT. Applies only to statuses
    # that could otherwise reach HEDGE or ASSERT.
    if mode == "strict" and status in ("PROBABLE", "CONFIRMED"):
        if not (status == "CONFIRMED" and conf >= 0.80):
            status = "SPECULATIVE"

    if status == "CONFIRMED" and conf >= 0.80:
        return "ASSERT"

    if status in ("CONFIRMED", "PROBABLE") and conf >= 0.50:
        return "HEDGE"

    if status == "SPECULATIVE" or (status == "PROBABLE" and conf < 0.50):
        return "SPECULATIVE"

    if status in ("UNKNOWN", "INSUFFICIENT_EVIDENCE", "LOW_EVIDENCE", "INSUFFICIENT"):
        return "CITE_OR_LIMIT"

    # Default safe fallback
    return "ACKNOWLEDGE"


def get_response_guidance(response_type: ResponseType) -> str:
    """Return human-readable guidance for the chosen response type."""
    mapping: Dict[str, str] = {
        "ASSERT": "State the claim directly and confidently. Include primary sources when available.",
        "HEDGE": "Use cautious language ('likely', 'evidence suggests', 'tends to'). Avoid absolute claims.",
        "SPECULATIVE": "Frame as possibility or hypothesis. Use 'could', 'might', 'one possible view'.",
        "REFUSE": "Do not assert. Clearly state the presence of conflict or insufficient grounding for a firm answer.",
        "ACKNOWLEDGE": "Acknowledge the query neutrally without making a substantive claim.",
        "CITE_OR_LIMIT": "Cite the strongest available evidence and explicitly limit the scope of any claim."
    }
    return mapping.get(response_type, "Respond with appropriate caution based on available epistemic status.")
