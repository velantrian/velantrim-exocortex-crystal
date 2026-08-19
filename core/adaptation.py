# core/adaptation.py
# Velantrim ExoCortex — adaptive verification telemetry (formerly RFC0071)
#
# Gate outcomes feed a process-local verification signal: blocks add high-stress
# telemetry; successful answers record low-stress telemetry. In the current
# implementation low stress increases exploration/creativity but does not lower
# the verification tag. The resulting verification_threshold() value is
# advisory telemetry/research output only. It does not own the default TruthGate
# admission policy; the default authority decision is fixed and versioned in
# core/truth_gate.py. Existing callers may request this signal explicitly for
# bounded experiments/tests, but process history must not silently mutate
# admission authority.

from typing import Dict, Any, Optional

from adaptive_threshold_module import AdaptiveThresholdModule

# Base value for the advisory verification signal (verification == 0.5).
_BASE_CONFIDENCE = 0.05
# The maximum amount the advisory signal rises by at verification == 1.0.
_MAX_BOOST = 0.3
_STRESS_HIGH = 0.85   # gate block
_STRESS_LOW = 0.2     # successful answer

_MODULE: Optional[AdaptiveThresholdModule] = None


def get_adaptation() -> AdaptiveThresholdModule:
    global _MODULE
    if _MODULE is None:
        _MODULE = AdaptiveThresholdModule()
    return _MODULE


def reset_adaptation() -> None:
    """Reset process-local telemetry state (for tests / a new window)."""
    global _MODULE
    _MODULE = None


def record_block() -> None:
    """Record stress after a block at Guardian/TruthGate/L3."""
    get_adaptation().record_stress(_STRESS_HIGH, context="gate_block")


def record_success() -> None:
    """Record a healthy outcome after a successful answer."""
    get_adaptation().record_stress(_STRESS_LOW, context="answered")


def verification_threshold() -> float:
    """
    Return an advisory adaptive confidence signal for WORLD_FACT review.

    verification 0.5 -> base 0.05; 1.0 -> 0.05 + _MAX_BOOST. This value is
    intentionally not consulted by the default TruthGate admission path. The
    fixed/versioned default policy lives in ``core.truth_gate``; using this
    adaptive signal as an admission threshold requires an explicit caller and
    must not occur implicitly through process history.
    """
    v = get_adaptation().epigenetic_tags["verification"]
    return round(_BASE_CONFIDENCE + max(0.0, v - 0.5) * (_MAX_BOOST / 0.5), 4)


def state() -> Dict[str, Any]:
    """Summary of the process-local epigenetic telemetry state."""
    return get_adaptation().get_state_summary()
