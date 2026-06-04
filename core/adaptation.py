# core/adaptation.py
# Velantrim ExoCortex — Epigenetic Adaptation wiring (RFC0071)
# v8.9.0-sprint2
#
# Brings the epigenetic_adaptation_module prototype to life in the core: gate blocks
# are "stress"; as it accumulates, it raises the verification tag, which tightens
# the TruthGate threshold. Hallucination defense adapts without retraining; under
# a healthy flow (successes) the threshold gradually relaxes.

from typing import Dict, Any, Optional

from epigenetic_adaptation_module import EpigeneticAdaptationModule

# Base confidence threshold for WORLD_FACT at the gate (verification == 0.5).
_BASE_CONFIDENCE = 0.05
# The maximum amount the threshold rises by at verification == 1.0.
_MAX_BOOST = 0.3
_STRESS_HIGH = 0.85   # gate block
_STRESS_LOW = 0.2     # successful answer

_MODULE: Optional[EpigeneticAdaptationModule] = None


def get_adaptation() -> EpigeneticAdaptationModule:
    global _MODULE
    if _MODULE is None:
        _MODULE = EpigeneticAdaptationModule()
    return _MODULE


def reset_adaptation() -> None:
    """Reset state (for tests / a new window)."""
    global _MODULE
    _MODULE = None


def record_block() -> None:
    """Record stress — a block at Guardian/TruthGate/L3."""
    get_adaptation().record_stress(_STRESS_HIGH, context="gate_block")


def record_success() -> None:
    """Record a healthy outcome — a successful answer."""
    get_adaptation().record_stress(_STRESS_LOW, context="answered")


def verification_threshold() -> float:
    """
    Adaptive confidence threshold for WORLD_FACT: rises with the verification tag.
    verification 0.5 → base 0.05; 1.0 → 0.05 + _MAX_BOOST.
    """
    v = get_adaptation().epigenetic_tags["verification"]
    return round(_BASE_CONFIDENCE + max(0.0, v - 0.5) * (_MAX_BOOST / 0.5), 4)


def state() -> Dict[str, Any]:
    """Summary of the epigenetic state (tags, mean stress)."""
    return get_adaptation().get_state_summary()
