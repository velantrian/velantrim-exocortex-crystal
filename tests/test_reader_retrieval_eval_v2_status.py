from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode()
    return hashlib.sha1(header + data).hexdigest()


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_historical_reader_retrieval_evidence_is_byte_identical():
    assert _git_blob_sha1(ROOT / "eval/reader_rc8_retrieval_adversarial.jsonl") == "4be317549d7a8eae9d69f9fa208d07d8855779a4"
    assert _git_blob_sha1(ROOT / "eval/reader_rc9_lexical_baseline.json") == "7ffbc86d713b7be89d393fe56c2d160b9dee98dc"
    assert _git_blob_sha1(ROOT / "eval/reader_rc10_retrieval_comparison_preregistration.json") == "70758595c220820d456a2ea4db68589289995294"


def test_eval_v2_manifest_surface_and_control_are_frozen():
    manifest = json.loads((ROOT / "eval/reader_retrieval_eval_v2_manifest.json").read_text(encoding="utf-8"))
    assert manifest["status"] == "FROZEN_RC9_CONTROL_REPRODUCED_NO_MODEL_COMPARATOR"
    assert manifest["tracking_issue"] == 384
    assert manifest["surface_identity"]["digest"] == "753cc550bc5fc47697aa6d7b1cda294bf11abaa08d515816e5e1db59eb526cdd"
    assert manifest["design"]["query_count"] == 24
    assert manifest["design"]["primary_strata_count"] == 12
    assert manifest["design"]["queries_per_primary_stratum"] == 2
    assert manifest["design"]["candidates_per_query_pool"] == 6
    assert manifest["design"]["useful_judgment_count"] == 48
    assert manifest["design"]["hard_negative_judgment_count"] == 48
    assert manifest["design"]["neutral_decoy_judgment_count"] == 48
    assert manifest["design"]["judgment_coverage"] == 1.0
    assert "qrel-label-independent" in manifest["design"]["candidate_ordering"]
    assert manifest["review_corrections_before_freeze"]["refund_scope_conflict_judged_possible_contradiction"] is True
    assert manifest["review_corrections_before_freeze"]["cache_scope_conflict_judged_possible_contradiction"] is True
    files = manifest["surface_files"]
    for key in ("queries", "candidates", "qrels"):
        assert _sha256(ROOT / files[key]["path"]) == files[key]["sha256"]
    control = json.loads((ROOT / manifest["rc9_v2_control"]["result_path"]).read_text(encoding="utf-8"))
    assert control["method"] == "reader_rc9_bm25_lexical_v1"
    assert control["judgment_coverage"] == 1.0
    assert control["metrics"]["useful_hits"] == 42
    assert control["metrics"]["useful_recall_at_k"] == 0.875
    assert control["metrics"]["precision_at_k"] == 0.35
    assert control["metrics"]["judged_precision_over_returned"] == 0.355932
    assert control["metrics"]["mrr"] == 0.857639
    assert control["metrics"]["hard_negative_hits"] == 38
    assert control["metrics"]["hard_negative_hit_rate_at_k"] == 0.791667


def test_future_comparator_gate_is_preresult_complete_and_non_authorizing():
    gate = json.loads((ROOT / "eval/reader_retrieval_eval_v2_future_comparator_gate.json").read_text(encoding="utf-8"))
    assert gate["status"] == "PRE_REGISTERED_NO_MODEL_COMPARATOR_EXECUTED"
    assert gate["historical_rc10_screen"]["required_unchanged_and_passed_separately"] is True
    frozen = gate["frozen_rc9_v2_control"]
    future = gate["future_comparator_gate"]
    assert frozen["useful_hits"] == 42
    assert len(frozen["retained_useful_candidate_ids"]) == 42
    assert frozen["missed_useful_candidate_ids"] == [
        "v2-c-0a8ace12cae2f46b", "v2-c-276b3efe332a9a8e", "v2-c-2dbbcb4d5fd9024b",
        "v2-c-33a2bceca3914a17", "v2-c-bd24e316a3f799aa", "v2-c-ea4d49c11eccb857",
    ]
    assert future["required_useful_hits_min"] == 46
    assert future["required_recover_at_least_n_rc9_v2_misses"] == 4
    assert future["mrr_floor"] == 0.857639
    assert future["max_hard_negative_hits"] == 24
    assert future["max_authority_violations"] == 0
    assert future["query_time_network_calls_max"] == 0
    assert future["external_reader_source_text_transmission_allowed"] is False
    assert future["auto_backend_selection_allowed"] is False
    assert future["exact_index_identity_required_when_indexed"] is True
    assert future["index_identity_or_explicit_no_index_required"] is True
    assert future["privacy_review_required"] is True
    assert future["passing_outcome"] == "ELIGIBLE_FOR_ARCHITECTURE_REVIEW_ONLY"
    assert gate["authority"]["comparison_pass_is_runtime_authorization"] is False
    assert gate["execution_constraints"]["model_comparator_executed_in_eval_v2"] is False
    assert gate["execution_constraints"]["semantic_runtime_authorized"] is False
    assert gate["execution_constraints"]["threshold_changes_after_future_results_allowed"] is False


def test_refund_scope_conflict_is_useful_possible_contradiction():
    qrels = [json.loads(line) for line in (ROOT / "eval/reader_retrieval_eval_v2_qrels.jsonl").read_text(encoding="utf-8").splitlines() if line]
    candidates = {row["candidate_id"]: row for row in (json.loads(line) for line in (ROOT / "eval/reader_retrieval_eval_v2_candidates.jsonl").read_text(encoding="utf-8").splitlines() if line)}
    q04 = [row for row in qrels if row["query_id"] == "v2-q04"]
    conflict = next(row for row in q04 if candidates[row["candidate_id"]]["proposition"] == "Customers may request a refund at any time after delivery.")
    portal = next(row for row in q04 if candidates[row["candidate_id"]]["proposition"] == "The return label can be downloaded from the customer portal.")
    assert conflict == {"candidate_id": conflict["candidate_id"], "judgment": "USEFUL_CANDIDATE", "query_id": "v2-q04", "review_class": "POSSIBLE_CONTRADICTION"}
    assert portal["judgment"] == "HARD_NEGATIVE"
    assert portal["review_class"] == "SAME_TOPIC"


def test_cache_scope_conflict_is_useful_possible_contradiction():
    qrels = [json.loads(line) for line in (ROOT / "eval/reader_retrieval_eval_v2_qrels.jsonl").read_text(encoding="utf-8").splitlines() if line]
    candidates = {row["candidate_id"]: row for row in (json.loads(line) for line in (ROOT / "eval/reader_retrieval_eval_v2_candidates.jsonl").read_text(encoding="utf-8").splitlines() if line)}
    q23 = [row for row in qrels if row["query_id"] == "v2-q23"]
    conflict = next(row for row in q23 if candidates[row["candidate_id"]]["proposition"] == "The cache is cleared whenever the user logs out.")
    conditional = next(row for row in q23 if candidates[row["candidate_id"]]["proposition"] == "If secure mode is enabled, logging out clears the cache.")
    assert conflict == {"candidate_id": conflict["candidate_id"], "judgment": "USEFUL_CANDIDATE", "query_id": "v2-q23", "review_class": "POSSIBLE_CONTRADICTION"}
    assert conditional["judgment"] == "USEFUL_CANDIDATE"
    assert conditional["review_class"] == "SAME_PROPOSITION_CANDIDATE"


def test_current_surfaces_describe_corrected_eval_v2_without_runtime_overclaim():
    required = {
        "ROADMAP.md": ("Reader Retrieval Evaluation Surface v2", "0.875000", "0.350000", "0.355932", "0.857639", "0.791667", "comparison pass != runtime authorization"),
        "docs/STATUS.md": ("Reader Retrieval Evaluation Surface v2", "LEXICAL_CONTROL_EXPOSES_MULTI_STRATUM_GAPS", "42 / 48", "candidate discovery != candidate adjudication", "active=false"),
        "docs/IMPLEMENTATION_STATUS.md": ("Reader Retrieval Evaluation Surface v2", "Reader RC-9 lexical candidate discovery", "dedicated_reader_core=false", "comparison pass != runtime authorization"),
        "docs/ai/CURRENT_STATE.md": ("51c205fe048fd69d39fcd47b43e042a50de432bc", "reader_core_rc7_cross_document_links", "eight other localized root README files", "LEXICAL_BASELINE_EXPOSES_MEASURED_GAP", "LEXICAL_CONTROL_EXPOSES_MULTI_STRATUM_GAPS"),
        "docs/architecture/READER_RETRIEVAL_EVAL_V2.md": ("144/144", "42 / 48", "38 / 48", "753cc550bc5fc47697aa6d7b1cda294bf11abaa08d515816e5e1db59eb526cdd", "NO MODEL COMPARATOR EXECUTED"),
        "docs/ai/COMPONENT_MAP.md": ("Reader Retrieval Evaluation Surface v2", "scripts/bench_reader_eval_v2_lexical.py", "comparison pass != runtime authorization"),
        "docs/ai/WORK_LOG.md": ("Reader Retrieval Evaluation Surface v2 (#384 / PR #385)", "label-independent", "model-backed comparator"),
    }
    for relative, markers in required.items():
        text = (ROOT / relative).read_text(encoding="utf-8")
        for marker in markers:
            assert marker in text
    combined = "\n".join((ROOT / relative).read_text(encoding="utf-8") for relative in required)
    assert "semantic/hybrid/vector Reader runtime" in combined
    assert "model-backed comparator execution" in combined or "model-backed comparator" in combined
