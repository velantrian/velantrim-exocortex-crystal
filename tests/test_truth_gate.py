"""Pin tests for core/truth_gate.py — the extracted verification boundary.

The extraction (core/pipeline.py → core/truth_gate.py) is move-only: these
tests pin the import compatibility and the exact gate behaviour so any future
"improvement" that changes semantics fails loudly.
"""
import pytest

from core import pipeline
from core.pipeline import truth_gate as truth_gate_via_pipeline
from core.truth_gate import truth_gate


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


# ─── Gate behaviour pins (verbatim semantics from the pipeline era) ───────────

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


def test_subjective_claim_passes_without_evidentiary_bar():
    ok, reason = truth_gate(
        {"facts": [_fact(claim_type="EMOTION", confidence=0.01)]},
        min_confidence=0.99)
    assert ok is True and reason is None


def test_sourced_confident_world_fact_passes():
    ok, reason = truth_gate({"facts": [_fact()]}, min_confidence=0.5)
    assert ok is True and reason is None


def test_default_threshold_comes_from_adaptation(monkeypatch):
    from core import adaptation
    monkeypatch.setattr(adaptation, "verification_threshold", lambda: 0.95)
    ok, reason = truth_gate({"facts": [_fact(confidence=0.9)]})
    assert ok is False and "0.95" in reason


# ─── Track 3A: ENABLE_TRUTH_POLICY production default ─────────────────────────

def test_truth_policy_on_blocks_llm_output_world_fact(monkeypatch):
    """ENABLE_TRUTH_POLICY=on enforces the strict rule: an LLM_OUTPUT cannot be
    admitted as a WORLD_FACT."""
    monkeypatch.setenv("ENABLE_TRUTH_POLICY", "on")
    ok, reason = truth_gate(
        {"facts": [_fact(source_status="LLM_OUTPUT")]}, min_confidence=0.0)
    assert ok is False and "LLM_OUTPUT cannot be WORLD_FACT" in reason


def test_truth_policy_off_is_legacy_bypass(monkeypatch):
    """ENABLE_TRUTH_POLICY=off is the legacy bypass: the SAME LLM_OUTPUT +
    WORLD_FACT case is no longer blocked by the policy and is judged on
    source + confidence alone (here: present + sufficient → passes)."""
    monkeypatch.setenv("ENABLE_TRUTH_POLICY", "off")
    ok, reason = truth_gate(
        {"facts": [_fact(source_status="LLM_OUTPUT")]}, min_confidence=0.0)
    assert ok is True and reason is None


def test_truth_policy_unset_defaults_to_strict(monkeypatch):
    """An unset ENABLE_TRUTH_POLICY defaults to strict ON (secure by default)."""
    monkeypatch.delenv("ENABLE_TRUTH_POLICY", raising=False)
    ok, reason = truth_gate(
        {"facts": [_fact(source_status="LLM_OUTPUT")]}, min_confidence=0.0)
    assert ok is False and "LLM_OUTPUT cannot be WORLD_FACT" in reason
