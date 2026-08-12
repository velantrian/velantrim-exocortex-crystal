from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_rc9_public_truth_documents_bounded_lexical_baseline():
    for path in (
        "docs/STATUS.md",
        "docs/IMPLEMENTATION_STATUS.md",
        "docs/ai/CURRENT_STATE.md",
        "docs/architecture/READER_RC9_LEXICAL_BASELINE.md",
    ):
        text = _text(path)
        for marker in (
            "LEXICAL_BASELINE_EXPOSES_MEASURED_GAP",
            "0.937500",
            "1.000000",
            "candidate discovery",
            "candidate adjudication",
        ):
            assert marker in text, (path, marker)

    assert "reader_rc9_bm25_lexical_v1" in _text(
        "docs/architecture/READER_RC9_LEXICAL_BASELINE.md"
    )
    for path in (
        "docs/STATUS.md",
        "docs/IMPLEMENTATION_STATUS.md",
        "docs/ai/CURRENT_STATE.md",
    ):
        text = _text(path)
        assert "core/reader_lexical_discovery.py" in text, path
        assert "dedicated_reader_core" in text and "false" in text, path


def test_rc9_preserves_rc8_history_and_does_not_authorize_next_mechanism():
    rc8 = _text("docs/architecture/READER_RC8_RETRIEVAL_DECISION.md")
    assert "deterministic lexical Reader candidate discovery + benchmark runner" in rc8
    rc9 = _text("docs/architecture/READER_RC9_LEXICAL_BASELINE.md")
    for marker in (
        "does **not** mean embeddings",
        "no PostgreSQL/pgvector activation",
        "No RC-7 link is auto-registered",
        "RC-10",
        "stop",
    ):
        assert marker.lower() in rc9.lower(), marker


def test_rc9_does_not_change_dedicated_reader_machine_truth():
    manifest = json.loads(_text("docs/status/implementation-manifest.json"))
    boundaries = manifest["implemented_boundaries"]
    assert boundaries["reader_core_rc7_cross_document_links"] is True
    assert boundaries["dedicated_reader_core"] is False
    assert "reader_core_rc9_lexical_candidate_discovery" not in boundaries
