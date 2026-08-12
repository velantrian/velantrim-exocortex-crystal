from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_rc7_machine_truth_and_authority_firewall_are_documented():
    manifest = json.loads(_text("docs/status/implementation-manifest.json"))
    assert manifest["implemented_boundaries"]["reader_core_rc7_cross_document_links"] is True
    assert manifest["implemented_boundaries"]["reader_core_rc6_long_context_strategy"] is True
    assert manifest["implemented_boundaries"]["dedicated_reader_core"] is False

    rc7 = manifest["reader_core_rc7"]
    assert rc7["tracking_issue"] == 371
    assert rc7["pull_request"] == 372
    assert rc7["runtime_module"] == "core/reader_cross_document.py"
    assert rc7["test_module"] == "tests/test_reader_cross_document.py"
    assert rc7["input_boundary"] == "current_registered_rc4_proposition_candidates_only"
    assert rc7["minimum_registered_sources"] == 2
    assert rc7["max_registered_sources"] == 32
    assert rc7["max_link_candidates"] == 4096
    assert rc7["different_document_identity_required"] is True
    assert rc7["relation_kinds"] == [
        "SUPPORTS",
        "CONTRADICTS",
        "ELABORATES",
        "REFERENCES",
        "DEFINES",
        "EXAMPLE_OF",
        "PREREQUISITE_FOR",
        "SAME_TOPIC",
        "POSSIBLE_SAME_CLAIM",
    ]
    assert rc7["symmetric_kinds"] == [
        "CONTRADICTS",
        "SAME_TOPIC",
        "POSSIBLE_SAME_CLAIM",
    ]
    for key in (
        "directional_order_preserved",
        "exact_two_sided_provenance",
        "explicit_rationale_required",
        "descriptive_inspection_basis_only",
        "count_only_telemetry",
    ):
        assert rc7[key] is True
    for key in (
        "same_topic_implies_same_proposition",
        "possible_same_claim_implies_identity",
        "similarity_signal_proves_identity",
        "automatic_semantic_matching",
        "automatic_entity_resolution",
        "automatic_corroboration",
        "evidence_admission",
        "fact_evidence_write",
        "confidence_promotion",
        "contradiction_resolution_authority",
        "automatic_winner_selection",
        "durable_storage_schema",
        "public_api_or_cli",
        "llm_or_provider_integration",
        "parser_or_semantic_chunker",
        "ocr_or_pdf_layout_reconstruction",
        "embeddings_or_vector_database",
        "planner_or_belief_update_authority",
        "truth_or_canon_authority",
        "dedicated_full_reader_core",
    ):
        assert rc7[key] is False

    machine_markers = (
        "reader_core_rc7_cross_document_links",
        "dedicated_reader_core",
    )
    for path in (
        "README.md",
        "ROADMAP.md",
        "docs/STATUS.md",
        "docs/IMPLEMENTATION_STATUS.md",
        "docs/ai/CURRENT_STATE.md",
    ):
        text = _text(path)
        for marker in machine_markers:
            assert marker in text, (path, marker)

    authority_markers = (
        "cross-document link",
        "same-topic",
        "possible-same-claim",
        "similarity signal",
        "repetition across sources",
    )
    for path in (
        "README.md",
        "ROADMAP.md",
        "docs/STATUS.md",
        "docs/IMPLEMENTATION_STATUS.md",
        "docs/ai/CURRENT_STATE.md",
        "docs/architecture/READER_RC7_CROSS_DOCUMENT.md",
    ):
        text = _text(path)
        for marker in authority_markers:
            assert marker in text, (path, marker)


def test_rc6_merge_truth_is_reconciled_before_rc7_merge():
    for path in (
        "README.md",
        "ROADMAP.md",
        "docs/STATUS.md",
        "docs/IMPLEMENTATION_STATUS.md",
        "docs/ai/CURRENT_STATE.md",
    ):
        text = _text(path)
        assert "1f5129d3276af28608b16e369fd38d21fe38c0d5" in text, path
        assert "31566408978" in text, path
        assert "reader_core_rc6_long_context_strategy" in text, path

    state = _text("docs/ai/CURRENT_STATE.md")
    assert "RC-1 through RC-6 are merged bounded Reader layers" in state
    roadmap = _text("ROADMAP.md")
    assert "Delivered Reader baseline through RC-6" in roadmap
    assert "RC-7 — Bounded Cross-Document Candidate Links" in roadmap


def test_rc7_does_not_start_semantic_vector_retrieval():
    combined = "\n".join(
        _text(path)
        for path in (
            "README.md",
            "ROADMAP.md",
            "docs/STATUS.md",
            "docs/IMPLEMENTATION_STATUS.md",
            "docs/ai/CURRENT_STATE.md",
            "docs/architecture/READER_RC7_CROSS_DOCUMENT.md",
        )
    )
    for marker in (
        "no automatic semantic matching",
        "embeddings/ANN/vector",
        "not started and not implied",
        "submitted / under review / not awarded",
        "active=false",
    ):
        assert marker in combined
