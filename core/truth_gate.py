# core/truth_gate.py
# Velantrim ExoCortex — TruthGate (the verification boundary)
#
# Extracted verbatim from core/pipeline.py so the gate is visible as a
# first-class module. The only entry into the L3 graph. Bypassing it = an
# architectural bug. core/pipeline.py re-exports `truth_gate` for backward
# compatibility — both import paths resolve to this single function.
# TODO Sprint 2: full ESM transition matrix, Laplace confidence.

from typing import Any, Dict, Optional
import os

from core.memory import SUBJECTIVE_CLAIM_TYPES
from core import adaptation


def _truth_policy_enabled() -> bool:
    """Track 3A — strict TruthPolicy production default.

    Strict policy is ON by default and stays ON unless ENABLE_TRUTH_POLICY is
    explicitly set to "off" (the legacy bypass). Any other value — including
    unset or "on" — means strict ON, so the secure behaviour is the default and
    the bypass must be opted into deliberately.

      ENABLE_TRUTH_POLICY unset  -> strict ON
      ENABLE_TRUTH_POLICY=on     -> strict ON
      ENABLE_TRUTH_POLICY=off    -> legacy bypass

    Read at call time (not import time) so tests can monkeypatch.setenv().
    """
    return os.environ.get("ENABLE_TRUTH_POLICY", "on").strip().lower() != "off"


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
    # Strict TruthPolicy is the production default; ENABLE_TRUTH_POLICY=off opts
    # into the legacy bypass for the LLM_OUTPUT→WORLD_FACT rule below.
    truth_policy_enabled = _truth_policy_enabled()
    facts = facts_pack.get("facts", [])

    if not facts:
        return False, "No facts to verify"

    for fact in facts:
        if not fact.get("source"):
            return False, f"Fact without source: {fact.get('fact_id')}"

        claim_type = fact.get("claim_type", "WORLD_FACT")

        # An LLM output by itself is not a fact about the external world. This is
        # the strict TruthPolicy rule; the legacy bypass (ENABLE_TRUTH_POLICY=off)
        # skips it and lets the fact be judged on source + confidence alone.
        if (
            truth_policy_enabled
            and claim_type == "WORLD_FACT"
            and fact.get("source_status") == "LLM_OUTPUT"
        ):
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
