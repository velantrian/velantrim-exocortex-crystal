from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "eval/reader_retrieval_comparator_v1_result.json"
PREREG = ROOT / "eval/reader_retrieval_comparator_v1_preregistration.json"
V2_GATE = ROOT / "eval/reader_retrieval_eval_v2_future_comparator_gate.json"


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_comparator_v1_frozen_identity_and_result() -> None:
    prereg = _load(PREREG)
    result = _load(RESULT)
    identity = result["comparator_identity"]

    assert prereg["status"] == "PRE_REGISTERED_BEFORE_RESULT"
    assert prereg["tracking_issue"] == result["tracking_issue"] == 386
    assert prereg["comparator"]["model_name"] == identity["model_name"]
    assert prereg["comparator"]["model_revision"] == identity["model_revision"]
    assert prereg["comparator"]["model_safetensors_sha256"] == identity["model_safetensors_sha256"]
    assert prereg["comparator"]["auto_backend_selection"] is identity["auto_backend_selection"] is False
    assert result["status"] == "COMPLETED_GATE_FAIL"
    assert result["classification"] == "SEMANTIC_RECALL_RECOVERED_DISCRIMINATION_GATE_FAILED"
    assert result["overall_gate_pass"] is False


def test_comparator_v1_recovers_recall_but_fails_hard_negative_gate() -> None:
    result = _load(RESULT)
    contract = _load(V2_GATE)["future_comparator_gate"]
    v2 = result["evaluation_surface_v2"]
    metrics = v2["comparator_metrics"]

    assert metrics["useful_hits"] == metrics["useful_total"] == 48
    assert metrics["useful_recall_at_5"] == 1.0
    assert metrics["mrr"] == 1.0
    assert set(v2["recovered_rc9_miss_candidate_ids"]) == set(contract["rc9_v2_miss_candidate_ids"])
    assert metrics["hard_negative_hits"] == 41 > contract["max_hard_negative_hits"] == 24
    assert metrics["hard_negative_rate_at_5"] == 0.854167 > contract["max_hard_negative_hit_rate_at_k"] == 0.5
    assert metrics["hard_negative_hits"] > v2["control_metrics"]["hard_negative_hits"] == 38
    assert v2["pass"] is False


def test_comparator_v1_preserves_authority_firewall() -> None:
    result = _load(RESULT)
    assert result["authority"]["authority_violations"] == 0
    assert result["authority"]["similarity_is_identity"] is False
    assert result["authority"]["retrieval_match_is_evidence"] is False
    assert result["authority"]["ranking_is_epistemic_authority"] is False
    assert result["authority"]["comparison_pass_is_runtime_authorization"] is False
    assert all(value is False for value in result["runtime_authorization"].values())
