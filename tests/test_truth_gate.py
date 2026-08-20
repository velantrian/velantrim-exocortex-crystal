"""Pin tests for core/truth_gate.py — the extracted admission boundary.

These tests pin import compatibility and exact gate behaviour so any future
change that weakens Ring Zero or reintroduces history-dependent default
admission fails loudly.
"""
import pytest

from core import pipeline
from core.pipeline import truth_gate as truth_gate_via_pipeline
from core.truth_gate import (
    DEFAULT_MIN_CONFIDENCE,
    TRUTH_GATE_POLICY_VERSION,
    truth_gate,
)


# ─── Import compatibility ─────────────────────────────────────────────────────

def test_both_import_paths_resolve_to_the_same_object():
    assert truth_gate is truth_gate_via_pipeline
    assert pipeline.truth_gate is truth_gate


def test_pipeline_monkeypatch_compatibility(monkeypatch):
    """run() must keep resolving truth_gate through pipeline's globals, so the
    historical `monkeypatch.setattr(pipeline, "truth_gate", …)` idiom from
    test_pipeline.py keeps intercepting the gate after the extraction."""
    monkeypatch.setattr(pipeline, "truth_gate", lambda fp, **k: (False, "pinned"))
    res = pipeline.run("quantum entanglement")
    assert res["answer"] is None
    assert "pinned" in res["error"]


# ─── Gate behaviour pins ──────────────────────────────────────────────────────

def _fact(**kw):
    base = {"fact_id": "f1", "source": "probe", "confidence": 0.9,
            "claim_type": "WORLD_FACT", "source_status": "OBSERVED"}
    base.update(kw)
    return base


def test_empty_facts_pack_is_blocked():
    ok, reason = truth_gate({"facts": []})
    assert ok is False and reason == "No facts to verify"


def test_missing_source_fact_is_blocked():
    ok, reason = truth_gate({"facts": [_fact(source=None)]})
    assert ok is False and "without source" in reason


def test_llm_output_world_fact_is_blocked():
    ok, reason = truth_gate(
        {"facts": [_fact(source_status="LLM_OUTPUT")]}, min_confidence=0.0)
    assert ok is False and "LLM_OUTPUT cannot be WORLD_FACT" in reason


def test_low_confidence_world_fact_is_blocked():
    ok, reason = truth_gate({"facts": [_fact(confidence=0.2)]},
                            min_confidence=0.5)
    assert ok is False and "Confidence 0.2 < threshold 0.5" in reason


def test_missing_confidence_is_controlled_rejection_not_keyerror():
    """A WORLD_FACT with no `confidence` key must be rejected with a clear
    reason, not raise KeyError while building the rejection message."""
    fact = _fact()
    del fact["confidence"]
    ok, reason = truth_gate({"facts": [fact]}, min_confidence=0.5)
    assert ok is False
    assert "confidence" in reason.lower()


def test_subjective_claim_passes_without_evidentiary_bar():
    ok, reason = truth_gate(
        {"facts": [_fact(claim_type="EMOTION", confidence=0.01)]},
        min_confidence=0.99)
    assert ok is True and reason is None


def test_sourced_confident_world_fact_passes():
    ok, reason = truth_gate({"facts": [_fact()]}, min_confidence=0.5)
    assert ok is True and reason is None


def test_default_policy_is_fixed_and_versioned():
    assert DEFAULT_MIN_CONFIDENCE == 0.05
    assert TRUTH_GATE_POLICY_VERSION == "truth-gate-v1-fixed-0.05"


def test_default_threshold_is_not_process_history_dependent():
    """The same admission input must produce the same answer regardless of
    volatile adaptive history; adaptation is telemetry/research, not authority."""
    from core import adaptation

    fact = _fact(confidence=DEFAULT_MIN_CONFIDENCE)
    adaptation.reset_adaptation()
    before = truth_gate({"facts": [fact]})
    for _ in range(20):
        adaptation.record_block()
    stressed = truth_gate({"facts": [fact]})
    for _ in range(20):
        adaptation.record_success()
    relaxed = truth_gate({"facts": [fact]})
    adaptation.reset_adaptation()
    restarted = truth_gate({"facts": [fact]})

    assert before == (True, None)
    assert stressed == before
    assert relaxed == before
    assert restarted == before


# ─── Threshold boundary (mutation-killing pins) ───────────────────────────────
# The gate comparison is strict `<`: confidence EQUAL to the threshold is
# sufficient evidence and must be admitted. These pins make an accidental
# `<` → `<=` (or inverse) regression fail loudly.

def test_confidence_exactly_at_threshold_passes():
    ok, reason = truth_gate({"facts": [_fact(confidence=0.5)]},
                            min_confidence=0.5)
    assert ok is True and reason is None


def test_confidence_just_below_threshold_is_blocked():
    ok, reason = truth_gate({"facts": [_fact(confidence=0.4999)]},
                            min_confidence=0.5)
    assert ok is False and "Confidence 0.4999 < threshold 0.5" in reason


def test_default_threshold_boundary_admits_equality():
    ok, reason = truth_gate(
        {"facts": [_fact(confidence=DEFAULT_MIN_CONFIDENCE)]})
    assert ok is True and reason is None


# ─── Ring Zero: policy cannot be disabled by process environment ──────────────

@pytest.mark.parametrize("value", ["off", "OFF", "false", "0", "legacy", "on"])
def test_truth_policy_environment_cannot_admit_llm_world_fact(monkeypatch, value):
    """Historical ENABLE_TRUTH_POLICY values are inert. No process environment
    value may turn model output into independent evidence about the world."""
    monkeypatch.setenv("ENABLE_TRUTH_POLICY", value)
    ok, reason = truth_gate(
        {"facts": [_fact(source_status="LLM_OUTPUT")]}, min_confidence=0.0)
    assert ok is False
    assert "LLM_OUTPUT cannot be WORLD_FACT" in reason


def test_truth_policy_unset_is_strict(monkeypatch):
    monkeypatch.delenv("ENABLE_TRUTH_POLICY", raising=False)
    ok, reason = truth_gate(
        {"facts": [_fact(source_status="LLM_OUTPUT")]}, min_confidence=0.0)
    assert ok is False and "LLM_OUTPUT cannot be WORLD_FACT" in reason


def test_environment_does_not_change_legitimate_external_fact(monkeypatch):
    """Removing the bypass does not make unrelated policy environment values
    influence a legitimately sourced WORLD_FACT."""
    monkeypatch.setenv("ENABLE_TRUTH_POLICY", "off")
    ok, reason = truth_gate(
        {"facts": [_fact(source_status="EXTERNAL")]}, min_confidence=0.5)
    assert ok is True and reason is None
