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


def test_truth_gate_default_ignores_adaptive_threshold():
    fact = {"facts": [{"fact_id": "a", "source": "s", "confidence": 0.1,
                       "claim_type": "WORLD_FACT"}]}
    # fresh: fixed default threshold 0.05 → 0.1 passes
    assert truth_gate(fact)[0] is True
    # adaptation telemetry still reacts to stress, but does not own admission.
    for _ in range(5):
        adaptation.record_block()
    assert adaptation.verification_threshold() > 0.1
    assert truth_gate(fact)[0] is True


def test_explicit_min_confidence_remains_caller_controlled():
    for _ in range(5):
        adaptation.record_block()
    fact = {"facts": [{"fact_id": "a", "source": "s", "confidence": 0.1,
                       "claim_type": "WORLD_FACT"}]}
    # an explicit bounded floor remains available to existing callers
    assert truth_gate(fact, min_confidence=0.05)[0] is True


def test_state_summary_exposes_tags():
    adaptation.record_block()
    s = adaptation.state()
    assert "tags" in s and "verification" in s["tags"]
