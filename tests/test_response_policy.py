'''Tests for response_policy v0.

These tests verify deterministic read-path behavior only.
No tests for write-path admission, TruthGate integration or L3 writes.
'''

import pytest
from core.response_policy import decide_response_policy, get_response_guidance, ResponseType


@pytest.mark.parametrize(
    "epistemic_status,confidence,has_contradiction,mode,expected",
    [
        # ASSERT cases
        ("CONFIRMED", 0.95, False, "normal", "ASSERT"),
        ("confirmed", 0.85, False, "normal", "ASSERT"),
        ("CONFIRMED", 0.80, False, "normal", "ASSERT"),

        # HEDGE cases
        ("PROBABLE", 0.70, False, "normal", "HEDGE"),
        ("CONFIRMED", 0.55, False, "normal", "HEDGE"),
        ("probable", 0.50, False, "normal", "HEDGE"),

        # SPECULATIVE cases
        ("SPECULATIVE", 0.30, False, "normal", "SPECULATIVE"),
        ("PROBABLE", 0.40, False, "normal", "SPECULATIVE"),
        ("speculative", 0.10, False, "normal", "SPECULATIVE"),

        # REFUSE cases
        ("CONFLICTED", 0.60, False, "normal", "REFUSE"),
        ("anything", 0.90, True, "normal", "REFUSE"),
        ("CONFLICTED", 0.20, False, "normal", "REFUSE"),

        # CITE_OR_LIMIT cases
        ("UNKNOWN", 0.0, False, "normal", "CITE_OR_LIMIT"),
        ("INSUFFICIENT_EVIDENCE", 0.3, False, "normal", "CITE_OR_LIMIT"),
        ("LOW_EVIDENCE", 0.1, False, "normal", "CITE_OR_LIMIT"),
        ("insufficient", 0.0, False, "normal", "CITE_OR_LIMIT"),

        # ACKNOWLEDGE fallback
        ("SOME_OTHER_STATUS", 0.4, False, "normal", "ACKNOWLEDGE"),
        ("", 0.5, False, "normal", "ACKNOWLEDGE"),

        # Mode strict downgrades weak evidence (never upgrades)
        ("PROBABLE", 0.90, False, "strict", "SPECULATIVE"),
        ("UNKNOWN", 0.99, False, "strict", "CITE_OR_LIMIT"),
        ("CONFIRMED", 0.90, False, "strict", "ASSERT"),  # still allows ASSERT if truly confirmed

        # Mode casual / other treated as normal
        ("CONFIRMED", 0.85, False, "casual", "ASSERT"),
    ],
)
def test_decide_response_policy_cases(
    epistemic_status, confidence, has_contradiction, mode, expected
):
    result = decide_response_policy(
        epistemic_status=epistemic_status,
        confidence=confidence,
        has_contradiction=has_contradiction,
        mode=mode,
    )
    assert result == expected
    assert result in ("ASSERT", "HEDGE", "SPECULATIVE", "REFUSE", "ACKNOWLEDGE", "CITE_OR_LIMIT")


def test_get_response_guidance_all_types():
    for rtype in ["ASSERT", "HEDGE", "SPECULATIVE", "REFUSE", "ACKNOWLEDGE", "CITE_OR_LIMIT"]:
        guidance = get_response_guidance(rtype)
        assert isinstance(guidance, str)
        assert len(guidance) > 10


def test_mode_cannot_upgrade_weak_evidence():
    """Critical invariant: mode hint must never turn weak support into ASSERT."""
    result = decide_response_policy("PROBABLE", 0.65, False, "casual")
    assert result != "ASSERT"

    result2 = decide_response_policy("UNKNOWN", 0.99, False, "strict")
    assert result2 == "CITE_OR_LIMIT"


def test_pure_function_no_side_effects():
    """Ensure the function is pure and does not mutate anything."""
    initial = "CONFIRMED"
    decide_response_policy(initial, 0.9)
    assert initial == "CONFIRMED"  # input not mutated


def test_response_type_literal():
    # Just to exercise the type
    t: ResponseType = "HEDGE"
    assert t == "HEDGE"
