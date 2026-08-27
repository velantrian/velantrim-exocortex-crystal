"""Regression coverage for Issue #463: current standing after evidence loss."""

from core import evidence, query_pipeline
from core.ingest import ingest


def test_final_qualifying_evidence_loss_blocks_current_factual_answer(monkeypatch):
    """Historical admission remains intact, but current public authority must fail closed."""
    monkeypatch.delenv("VELANTRIM_RELEASE_PROFILE", raising=False)
    claim = "C463 final qualifying support loss"
    admitted = ingest(
        claim,
        fact_id="c463-final-support-loss",
        source="file://c463-source.txt",
        confidence=0.9,
        source_status="EXTERNAL",
    )["fact"]
    assert admitted["epistemic_state"] == "Validated"
    assert admitted["truth_status"] == "VERIFIED"

    evidence.attach_evidence(
        admitted["fact_id"],
        "file://c463-source.txt",
        source_text="C463 source text",
        span_start=0,
        span_end=6,
    )
    assert query_pipeline.query(claim)["answer"] is not None

    assert evidence.delete_evidence_for(admitted["fact_id"]) == 1
    assert not evidence.has_valid_evidence_for_grounding(admitted["fact_id"])

    result = query_pipeline.query(claim)
    assert result["answer"] is None
    assert result["reason_code"] == "insufficient_grounding_missing_verified_evidence"
