# core/truth_gate.py
# Velantrim ExoCortex — TruthGate (the verification boundary)
#
# Extracted verbatim from core/pipeline.py so the gate is visible as a
# first-class module. The only entry into the L3 graph. Bypassing it = an
# architectural bug. core/pipeline.py re-exports `truth_gate` for backward
# compatibility — both import paths resolve to this single function.
# TODO Sprint 2: full ESM transition matrix, Laplace confidence.

from typing import Any, Dict, Optional

from core.memory import SUBJECTIVE_CLAIM_TYPES
from core import adaptation


def truth_gate(
    facts_pack: Dict[str, Any],
    min_confidence: Optional[float] = None,
) -> tuple[bool, Optional[str]]:
    """
    Verifies facts before writing to L3.
    min_confidence=None → adaptive threshold (epigenetic verification, RFC0071):
    after blocks the threshold rises (more defensive), under a healthy flow — it relaxes.
    Returns (passed: bool, reason: str | None).

    Type-aware: the gate does NOT throw out the subjective, but does not let it
    masquerade as a fact about the world.
      - WORLD_FACT      → requires source + confidence ≥ threshold.
      - subjective      → pass without an evidentiary bar (a feeling is real
        (EMOTION, OPINION…)  as a feeling), but will not become WORLD_FACT.
      - LLM_OUTPUT      → cannot be WORLD_FACT by itself.

    Transitioning facts into the Validated ESM state is done by the caller
    (run()) when passed=True. truth_gate() only makes the verification decision.
    """
    if min_confidence is None:
        min_confidence = adaptation.verification_threshold()
    facts = facts_pack.get("facts", [])

    if not facts:
        return False, "No facts to verify"

    for fact in facts:
        if not fact.get("source"):
            return False, f"Fact without source: {fact.get('fact_id')}"

        claim_type = fact.get("claim_type", "WORLD_FACT")

        # An LLM output by itself is not a fact about the external world.
        if claim_type == "WORLD_FACT" and fact.get("source_status") == "LLM_OUTPUT":
            return False, (
                f"LLM_OUTPUT cannot be WORLD_FACT without an independent source: "
                f"{fact.get('fact_id')}"
            )

        # Subjective claims are valid as experience — without an evidentiary bar.
        if claim_type in SUBJECTIVE_CLAIM_TYPES:
            continue

        # WORLD_FACT and INTERPRETATION — require a minimum confidence.
        if fact.get("confidence", 0) < min_confidence:
            return False, (
                f"Confidence {fact['confidence']} < threshold {min_confidence}: "
                f"{fact.get('fact_id')}"
            )

    return True, None
