from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_post_rc10_reassessment_selects_evaluation_before_comparator_execution():
    decision = json.loads(_text("eval/reader_post_rc10_reassessment.json"))

    assert decision["status"] == "ARCHITECTURE_DECISION_NO_COMPARATOR_EXECUTED"
    assert decision["tracking_issue"] == 382
    assert decision["audited_start_main"] == "59cf060629c25ddf0747ca46ea1fadf87fa86857"
    assert decision["rc10_preregistration_preserved"] is True
    assert decision["measured_findings"]["retrieval_quality_gap_measured"] is True
    assert decision["measured_findings"]["reader_scale_or_latency_blocker_measured"] is False

    assert (
        decision["option_disposition"]["stronger_prefrozen_evaluation_surface"]
        == "SELECTED_NEXT_BOUNDED_MILESTONE"
    )
    next_milestone = decision["selected_next_milestone"]
    assert next_milestone["name"] == "reader_retrieval_evaluation_surface_v2"
    assert next_milestone["kind"] == "EVALUATION_RESEARCH_ONLY"
    assert next_milestone["started_by_this_decision"] is False
    assert next_milestone["semantic_comparator_executed"] is False
    assert next_milestone["model_dependency_added"] is False
    assert next_milestone["runtime_change_authorized"] is False
    assert next_milestone["model_backed_comparator_allowed_in_same_milestone"] is False

    admission = decision["future_comparator_admission"]
    assert admission["requires_separate_authorization"] is True
    assert admission["must_pass_unchanged_rc10_screen"] is True
    assert admission["must_be_evaluated_on_stronger_surface_after_freeze"] is True
    assert admission["auto_backend_allowed"] is False
    assert admission["query_time_network_calls_max"] == 0
    assert admission["external_reader_source_text_transmission_allowed"] is False
    assert admission["runtime_authorized_by_comparison_pass"] is False


def test_rc10_frozen_screen_is_not_rewritten_by_post_rc10_decision():
    prereg = json.loads(_text("eval/reader_rc10_retrieval_comparison_preregistration.json"))
    gate = prereg["future_comparison_gate"]

    assert prereg["status"] == "PRE_REGISTERED_NO_COMPARISON_EXECUTED"
    assert gate["required_positive_hits"] == 16
    assert gate["required_recall_at_k"] == 1.0
    assert gate["required_recover_case_ids"] == ["rc8-004"]
    assert gate["required_retain_rc9_positive_hit_count"] == 15
    assert gate["mrr_floor"] == 0.895833
    assert gate["max_hard_negative_hits"] == 2
    assert gate["max_paired_hard_negative_rate_at_k"] == 0.5
    assert gate["max_authority_violations"] == 0
    assert gate["auto_backend_selection_allowed"] is False
    assert gate["query_time_network_calls_max"] == 0
    assert gate["external_source_text_transmission_allowed"] is False
    assert (
        gate["passing_outcome"]
        == "ELIGIBLE_FOR_STRONGER_EVALUATION_AND_ARCHITECTURE_REVIEW_ONLY"
    )


def test_current_truth_surfaces_advance_beyond_completed_377_and_379():
    current_paths = (
        "ROADMAP.md",
        "docs/STATUS.md",
        "docs/IMPLEMENTATION_STATUS.md",
        "docs/ai/CURRENT_STATE.md",
    )
    for path in current_paths:
        text = _text(path)
        assert "#382" in text, path
        assert "Evaluation Surface v2" in text, path
        assert "comparison pass != runtime authorization" in text, path
        assert "Current bounded milestone: issue #379" not in text, path
        assert "current bounded documentation milestone: **post-RC-9 grant presentation truth reconciliation, issue #379**" not in text, path
        assert "#377 remains separate RC-10 preregistration/completion bookkeeping" not in text, path


def test_architecture_decision_preserves_authority_and_nonimplementation():
    text = _text("docs/architecture/READER_POST_RC10_REASSESSMENT.md")
    for marker in (
        "measured retrieval-quality gap != measured scaling gap",
        "SQLite FTS",
        "HashingEmbedder",
        "TrigramHashingEmbedder",
        "core/rrf.py",
        "Reader Retrieval Evaluation Surface v2",
        "retrieval match          != evidence",
        "similarity               != identity",
        "comparison pass          != runtime authorization",
        "NLnet remains `submitted / under review / not awarded`",
        "dedicated_reader_core                    false",
        "Do not automatically start Evaluation Surface v2",
    ):
        assert marker in text, marker
