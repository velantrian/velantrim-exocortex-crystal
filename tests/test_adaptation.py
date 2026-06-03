"""Tests for core/adaptation.py — epigenetic adaptation wiring (RFC0071)."""
from core import adaptation
from core.pipeline import truth_gate


def test_threshold_starts_at_base():
    assert adaptation.verification_threshold() == 0.05


def test_blocks_raise_threshold_successes_relax():
    base = adaptation.verification_threshold()
    for _ in range(3):
        adaptation.record_block()
    stressed = adaptation.verification_threshold()
    assert stressed > base                       # defensive after repeated blocks


def test_truth_gate_uses_adaptive_threshold():
    fact = {"facts": [{"fact_id": "a", "source": "s", "confidence": 0.1,
                       "claim_type": "WORLD_FACT"}]}
    # fresh: threshold 0.05 → 0.1 passes
    assert truth_gate(fact)[0] is True
    # after repeated stress the threshold climbs above 0.1 → same fact blocked
    for _ in range(5):
        adaptation.record_block()
    assert adaptation.verification_threshold() > 0.1
    assert truth_gate(fact)[0] is False


def test_explicit_min_confidence_overrides_adaptive():
    for _ in range(5):
        adaptation.record_block()
    fact = {"facts": [{"fact_id": "a", "source": "s", "confidence": 0.1,
                       "claim_type": "WORLD_FACT"}]}
    # explicit floor ignores the adaptive threshold
    assert truth_gate(fact, min_confidence=0.05)[0] is True


def test_state_summary_exposes_tags():
    adaptation.record_block()
    s = adaptation.state()
    assert "tags" in s and "verification" in s["tags"]
