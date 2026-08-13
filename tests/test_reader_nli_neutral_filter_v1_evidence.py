from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PREREG = ROOT / "eval/reader_nli_neutral_filter_v1_preregistration.json"
RESULT = ROOT / "eval/reader_nli_neutral_filter_v1_result.json"
LOCK = ROOT / "eval/reader_nli_neutral_filter_v1_requirements.txt"
DOC = ROOT / "docs/architecture/READER_NLI_NEUTRAL_FILTER_V1.md"

DEPENDENCY_SHA = "9a2902d1b7d5b7ca5b5105be46d1a1151fddf683e0ed67b078a09c948b3f4bd9"
FULL_QUALIFYING_RESULT_SHA = "4f1e1391c3c4983d4a090429aae2f67d430d9d7891ca6f0da1e90457033dc315"
REPEATABILITY_FINGERPRINT = "cae703bd3cb38aa80334c013b5f17860f9e36c013092a2ea6f81b2426c71b132"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_reader_nli_neutral_filter_v1_frozen_fail_evidence() -> None:
    prereg = _load(PREREG)
    result = _load(RESULT)
    doc = DOC.read_text(encoding="utf-8")

    assert prereg["status"] == "PRE_REGISTERED_BEFORE_RESULT"
    assert prereg["tracking_issue"] == 388
    assert prereg["audited_start_main"] == "1ca31f92dfc0818a07b6a33560799c962b6e7d9f"
    assert prereg["semantic_source"]["k"] == 5
    assert prereg["semantic_source"]["ranking_frozen"] is True
    assert prereg["nli"]["score_threshold"] is None
    assert prereg["gates"]["threshold_changes_after_result"] is False
    assert prereg["runtime_changes_authorized"] is False
    assert _sha256(LOCK) == DEPENDENCY_SHA

    assert result["status"] == "QUALIFYING_RESULT_FAIL"
    assert result["classification"] == "NLI_NEUTRAL_FILTER_GATE_FAILED"
    assert result["overall_gate_pass"] is False
    assert result["runtime_authorization"] is False

    identity = result["identity"]
    assert identity["k"] == 5
    assert identity["index"] == "NO_INDEX_EXACT_POOL_SCORING"
    assert identity["semantic_revision"] == "e8f8c211226b894fcb81acc59f3b34ba3efd5f42"
    assert identity["semantic_safetensors_sha256"] == "eaa086f0ffee582aeb45b36e34cdd1fe2d6de2bef61f8a559a1bbc9bd955917b"
    assert identity["nli_revision"] == "0a71e92a985b6e1ad1828cf67ce9c459639c1dca"
    assert identity["nli_safetensors_sha256"] == "91b323ccf247ec1e3b5925d566230bae7c52de8147e6062b42e250089a3fc80b"
    assert identity["nli_id2label"] == {"0": "entailment", "1": "neutral", "2": "contradiction"}
    assert identity["rule"] == "filter iff both directional argmax labels are neutral"

    evidence = result["frozen_evidence"]
    assert evidence["qualifying_run_id"] == 31736269934
    assert evidence["qualifying_job_id"] == 94568540864
    assert evidence["qualifying_head_sha"] == "9520d3d8b93020e8570702e7dcf13459b3bf6d18"
    assert evidence["pytest_artifact_id"] == 9195428397
    assert evidence["full_qualifying_result_file_sha256"] == FULL_QUALIFYING_RESULT_SHA

    execution = result["execution"]
    assert execution["dependency_freeze_sha256"] == DEPENDENCY_SHA
    assert execution["hf_hub_offline"] is True
    assert execution["transformers_offline"] is True
    assert execution["network_isolation_required_by_workflow"] is True
    assert execution["external_reader_source_text_transmission"] is False
    assert execution["repeatable"] is True
    assert execution["repeatability_fingerprint_first"] == REPEATABILITY_FINGERPRINT
    assert execution["repeatability_fingerprint_second"] == REPEATABILITY_FINGERPRINT

    historical = result["historical_rc10"]
    assert historical["metrics"] == {
        "hard_negative_hits": 1,
        "hard_negative_rate_at_5": 0.25,
        "hard_negative_total": 4,
        "mrr": 0.9375,
        "positive_hits": 15,
        "positive_total": 16,
        "recall_at_5": 0.9375,
    }
    assert historical["lost_positive_case_ids"] == ["rc8-020"]

    v2 = result["evaluation_surface_v2"]
    assert v2["metrics"]["useful_hits"] == 46
    assert v2["metrics"]["useful_total"] == 48
    assert v2["metrics"]["useful_recall_at_5"] == 0.958333
    assert v2["metrics"]["all_useful_query_rate_at_5"] == 0.916667
    assert v2["metrics"]["mrr"] == 1.0
    assert v2["metrics"]["hard_negative_hits"] == 18
    assert v2["metrics"]["hard_negative_total"] == 48
    assert v2["metrics"]["hard_negative_rate_at_5"] == 0.375
    assert v2["lost_useful_candidate_ids"] == [
        "v2-c-0a8ace12cae2f46b",
        "v2-c-7dd0f1454ab1266a",
    ]
    for stratum in (
        "boilerplate_same_topic",
        "cross_lingual_paraphrase",
        "homonym_entity_collision",
        "negation_polarity",
    ):
        assert v2["per_stratum"][stratum]["hard_negative_rate_at_5"] == 0.75

    gates = result["gates"]
    assert gates["historical"]["pass"] is False
    assert gates["historical"]["checks"]["positive_hits"] is False
    assert gates["historical"]["checks"]["recall"] is False
    assert gates["v2"]["pass"] is False
    assert gates["v2"]["checks"]["per_stratum_hard_negative"] is False
    assert gates["v2"]["checks"]["retain_rc9_useful"] is False
    assert len(gates["v2"]["recovered_rc9_misses"]) == 5
    assert gates["no_recall_loss"]["pass"] is False

    authority = result["authority"]
    assert authority["authority_violations"] == 0
    assert authority["nli_label_is_identity"] is False
    assert authority["nli_label_is_adjudication"] is False
    assert authority["filtering_is_epistemic_authority"] is False
    assert authority["pass_is_runtime_authorization"] is False

    assert "COMPLETED — FROZEN GATE FAIL" in doc
    assert "NLI_NEUTRAL_FILTER_GATE_FAILED" in doc
    assert FULL_QUALIFYING_RESULT_SHA in doc
    assert "`runtime_authorization = false`" in doc
    assert "STOP" in doc
