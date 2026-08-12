from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PREREG = ROOT / "eval" / "reader_rc10_retrieval_comparison_preregistration.json"
ARCH = ROOT / "docs" / "architecture" / "READER_RC10_RETRIEVAL_REUSE_PREREGISTRATION.md"


def _contract() -> dict:
    return json.loads(PREREG.read_text(encoding="utf-8"))


def test_rc10_freezes_exact_rc9_control_before_any_comparison() -> None:
    contract = _contract()
    assert contract["status"] == "PRE_REGISTERED_NO_COMPARISON_EXECUTED"
    control = contract["frozen_control"]
    assert control["method"] == "reader_rc9_bm25_lexical_v1"
    assert control["corpus_path"] == "eval/reader_rc8_retrieval_adversarial.jsonl"
    assert control["corpus_git_blob"] == "4be317549d7a8eae9d69f9fa208d07d8855779a4"
    assert control["result_git_blob"] == "7ffbc86d713b7be89d393fe56c2d160b9dee98dc"
    assert control["positive_hits"] == 15
    assert control["recall_at_k"] == 0.9375
    assert control["mrr"] == 0.895833
    assert control["hard_negative_hits"] == 4
    assert control["known_positive_miss_case_ids"] == ["rc8-004"]


def test_rc10_gate_requires_recall_recovery_and_hard_negative_improvement() -> None:
    gate = _contract()["future_comparison_gate"]
    assert gate["k"] == 5
    assert gate["required_positive_hits"] == 16
    assert gate["required_recall_at_k"] == 1.0
    assert gate["required_recover_case_ids"] == ["rc8-004"]
    assert gate["required_retain_rc9_positive_hit_count"] == 15
    assert gate["mrr_floor"] == 0.895833
    assert gate["max_hard_negative_hits"] == 2
    assert gate["max_paired_hard_negative_rate_at_k"] == 0.5
    assert gate["max_authority_violations"] == 0
    assert gate["passing_outcome"] == "ELIGIBLE_FOR_STRONGER_EVALUATION_AND_ARCHITECTURE_REVIEW_ONLY"


def test_rc10_comparison_identity_privacy_and_offline_constraints_are_fail_closed() -> None:
    contract = _contract()
    gate = contract["future_comparison_gate"]
    execution = contract["execution_constraints"]
    model = contract["future_model_comparator_requirements"]
    assert gate["exact_backend_identity_required"] is True
    assert gate["auto_backend_selection_allowed"] is False
    assert gate["query_time_network_calls_max"] == 0
    assert gate["external_source_text_transmission_allowed"] is False
    assert gate["deterministic_lexical_fallback_required_for_runtime_proposal"] is True
    assert execution["comparison_executed_in_rc10"] is False
    assert execution["semantic_runtime_authorized"] is False
    assert execution["hybrid_runtime_authorized"] is False
    assert execution["sqlite_fts_runtime_authorized"] is False
    assert execution["ann_vector_runtime_authorized"] is False
    assert execution["sentence_transformer_download_authorized"] is False
    assert execution["threshold_changes_after_results_allowed"] is False
    assert model["separate_execution_authorization_required"] is True
    assert model["immutable_model_revision_or_checksum_required"] is True
    assert model["assets_preloaded_locally_for_qualifying_run"] is True


def test_rc10_reuse_matrix_prevents_direct_admitted_memory_reader_wiring() -> None:
    reuse = _contract()["reuse_matrix"]
    assert reuse["core.rrf"] == "ELIGIBLE_FOR_FUTURE_READER_COMPARISON_REUSE"
    assert reuse["core.embedding.HashingEmbedder"] == "COMPARATOR_SIGNAL_ONLY"
    assert reuse["core.embedding.TrigramHashingEmbedder"] == "COMPARATOR_SIGNAL_ONLY"
    assert reuse["core.embedding.SentenceTransformerEmbedder"] == "FUTURE_OPTIONAL_COMPARATOR_ONLY"
    assert reuse["core.embedding.get_embedder:auto"] == "FORBIDDEN_FOR_PREREGISTERED_READER_COMPARISON"
    assert reuse["core.pipeline.retrieve"] == "DO_NOT_REUSE_AS_READER_PIPELINE"
    assert reuse["core.query_pipeline"] == "DO_NOT_REUSE_AS_READER_PIPELINE"
    assert reuse["core.legacy_retrieval"] == "DO_NOT_REUSE_AS_READER_BACKEND"
    assert reuse["sqlite_fts5"] == "NOT_IMPLEMENTED_FOR_READER_FUTURE_SCALING_OPTION"
    assert reuse["postgresql_pgvector"] == "NOT_AUTHORIZED_FOR_READER"


def test_rc10_preserves_authority_firewall_and_does_not_claim_runtime() -> None:
    contract = _contract()
    authority = contract["authority"]
    assert all(value is False for value in authority.values())
    text = ARCH.read_text(encoding="utf-8")
    for marker in (
        "retrieval match          != evidence",
        "similarity               != identity",
        "repetition               != corroboration",
        "cross-document candidate != Canon relation",
        "ranking                  != epistemic authority",
        "candidate discovery      != candidate adjudication",
        "comparison pass          != runtime authorization",
        "dedicated_reader_core=false",
        "No comparison executed",
    ):
        if marker == "No comparison executed":
            assert "NO COMPARISON EXECUTED" in text
        else:
            assert marker in text
