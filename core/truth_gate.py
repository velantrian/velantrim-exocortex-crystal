# core/truth_gate.py
# Velantrim ExoCortex — TruthGate (the verification boundary)
#
# Extracted from core/pipeline.py so the gate is visible as a first-class
# module. The only automatic entry into the L3 graph. Bypassing it = an
# architectural bug. core/pipeline.py re-exports `truth_gate` for backward
# compatibility — both import paths resolve to this single function.
# TODO Sprint 2: full ESM transition matrix, Laplace confidence.

from typing import Any, Dict, Optional

from core.memory import SUBJECTIVE_CLAIM_TYPES


# Freeze-grade default admission policy. This value is deliberately fixed and
# versioned: process-local adaptation may remain useful as telemetry/research,
# but prior request history must not silently change admission authority.
DEFAULT_MIN_CONFIDENCE = 0.05
TRUTH_GATE_POLICY_VERSION = "truth-gate-v1-fixed-0.05"


def truth_gate(
    facts_pack: Dict[str, Any],
    min_confidence: Optional[float] = None,
) -> tuple[bool, Optional[str]]:
    """
    Decide whether facts may be admitted to L3.

    ``min_confidence=None`` uses the fixed, versioned freeze policy
    ``DEFAULT_MIN_CONFIDENCE``. Callers may still provide an explicit threshold
    for bounded tests/specialized internal flows, but process-local adaptive
    history is not part of the default authority decision.

    Type-aware: the gate does not discard subjective experience, but it does not
    let it masquerade as a fact about the external world.
      - WORLD_FACT      → requires source + confidence ≥ threshold.
      - subjective      → passes without an evidentiary bar (a feeling is real
        (EMOTION, OPINION…) as a feeling), but will not become WORLD_FACT.
      - LLM_OUTPUT      → can never be admitted as WORLD_FACT by itself.

    The LLM_OUTPUT → WORLD_FACT block is a fixed Ring Zero invariant. No
    environment variable, runtime mode or caller option can disable it. Tests,
    migrations and demos that need a different provenance must provide an
    honest independent source_status or use an appropriate non-world-fact type;
    they may not weaken the production gate.

    Transitioning facts into the Validated ESM state is done by the caller when
    passed=True. truth_gate() only makes the admission decision and performs no
    canon/database writes.
    """
    if min_confidence is None:
        min_confidence = DEFAULT_MIN_CONFIDENCE
    facts = facts_pack.get("facts", [])

    if not facts:
        return False, "No facts to verify"

    for fact in facts:
        if not fact.get("source"):
            return False, f"Fact without source: {fact.get('fact_id')}"

        claim_type = fact.get("claim_type", "WORLD_FACT")

        # Ring Zero: model output is never independent evidence about the world.
        # This invariant is intentionally non-configurable. A caller may classify
        # the output as an interpretation/hypothesis or attach an independent
        # source, but it cannot turn model provenance into a verified WORLD_FACT
        # by changing process environment or runtime mode.
        if (
            claim_type == "WORLD_FACT"
            and fact.get("source_status") == "LLM_OUTPUT"
        ):
            return False, (
                "LLM_OUTPUT cannot be WORLD_FACT without an independent source: "
                f"{fact.get('fact_id')}"
            )

        # Subjective claims are valid as experience — without an evidentiary bar.
        if claim_type in SUBJECTIVE_CLAIM_TYPES:
            continue

        # WORLD_FACT and INTERPRETATION require a minimum confidence.
        confidence = fact.get("confidence", 0)
        if confidence < min_confidence:
            return False, (
                f"Confidence {confidence} < threshold {min_confidence}: "
                f"{fact.get('fact_id')}"
            )

    return True, None
