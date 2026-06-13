"""Tests for TRACE Visualization (core/trace_visualize.py, scripts/trace_visualize.py)."""

import json
import sys
from pathlib import Path

import pytest

from core.trace_visualize import _extract_receipt_and_verify, to_dot, to_markdown


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

MINIMAL_RECEIPT = {
    "query": "Where is the Eiffel Tower?",
    "answer": "The Eiffel Tower is in Paris.",
}

FULL_RECEIPT = {
    "version": "2",
    "created_at": "2026-06-13T00:00:00Z",
    "query": "Where is the Eiffel Tower?",
    "answer": "The Eiffel Tower is in Paris.",
    "citations": [
        {
            "fact_id": "f:abc123",
            "claim_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "source": "demo",
            "epistemic_state": "Validated",
            "truth_status": "VERIFIED",
            "evidence": [
                {
                    "evidence_id": "ev:xyz",
                    "source_uri": "file.md",
                    "span_start": 10,
                    "span_end": 42,
                }
            ],
        }
    ],
    "digest": "abc123def456abc123def456abc123def456abc123def456abc123def456abc1",
    "signature": "hmachash",
}

VERIFY_RESULT = {
    "digest_valid": True,
    "signature_valid": True,
    "verified": True,
    "citations": [{"fact_id": "f:abc123", "status": "ok"}],
}

COMBINED = {"receipt": FULL_RECEIPT, "verify": VERIFY_RESULT}


# ---------------------------------------------------------------------------
# _extract_receipt_and_verify
# ---------------------------------------------------------------------------


class TestExtractReceiptAndVerify:
    def test_combined_with_verify(self):
        receipt, verify = _extract_receipt_and_verify(COMBINED)
        assert receipt is FULL_RECEIPT
        assert verify is VERIFY_RESULT

    def test_combined_without_verify(self):
        data = {"receipt": FULL_RECEIPT}
        receipt, verify = _extract_receipt_and_verify(data)
        assert receipt is FULL_RECEIPT
        assert verify == {}

    def test_plain_receipt(self):
        receipt, verify = _extract_receipt_and_verify(FULL_RECEIPT)
        assert receipt is FULL_RECEIPT
        assert verify == {}


# ---------------------------------------------------------------------------
# to_markdown
# ---------------------------------------------------------------------------


class TestToMarkdown:
    def test_minimal_receipt_has_sections(self):
        result = to_markdown(MINIMAL_RECEIPT)
        assert "## Query" in result
        assert "## Answer" in result
        assert "## Boundary Notes" in result

    def test_verified_citation_evidence_present(self):
        result = to_markdown(FULL_RECEIPT)
        assert "truth_status=VERIFIED" in result
        assert "evidence=present" in result

    def test_citation_missing_evidence_field(self):
        receipt = {
            "query": "q",
            "answer": "a",
            "citations": [
                {
                    "fact_id": "f:no_evidence",
                    "truth_status": "VERIFIED",
                    "source": "demo",
                    # no "evidence" key
                }
            ],
        }
        result = to_markdown(receipt)
        assert "evidence=absent" in result

    def test_missing_optional_fields_no_crash(self):
        result = to_markdown({})
        assert "(none)" in result
        assert "absent" in result
        assert "## Query" in result
        assert "## Answer" in result

    def test_fact_id_truncated_at_20(self):
        long_id = "f:" + "x" * 25  # 27 chars total
        receipt = {
            "citations": [
                {"fact_id": long_id, "truth_status": "VERIFIED", "source": "s"}
            ]
        }
        result = to_markdown(receipt)
        assert "…" in result
        # The displayed id should not be more than 20 chars + ellipsis
        assert long_id not in result

    def test_fact_id_none_shows_unknown(self):
        receipt = {
            "citations": [
                {"fact_id": None, "truth_status": "VERIFIED", "source": "s"}
            ]
        }
        result = to_markdown(receipt)
        assert "(unknown)" in result

    def test_with_verify_dict_shows_values(self):
        result = to_markdown(COMBINED)
        assert "digest_valid: True" in result
        assert "verified: True" in result

    def test_without_verify_shows_dash(self):
        result = to_markdown(FULL_RECEIPT)
        assert "digest_valid: —" in result
        assert "signature_valid: —" in result
        assert "verified: —" in result

    def test_claim_sha256_not_readable_text(self):
        """SHA-256 hashes are hex strings, not readable sentences."""
        result = to_markdown(FULL_RECEIPT)
        # The claim_sha256 value is a hex hash; it should not appear as plain text
        sha = FULL_RECEIPT["citations"][0]["claim_sha256"]
        # Hashes are long hex strings — they wouldn't appear as natural text anyway,
        # but explicitly confirm the formatter doesn't embed raw claim text
        assert sha not in result

    def test_citations_count_displayed(self):
        result = to_markdown(FULL_RECEIPT)
        assert "Citations (1 total)" in result

    def test_empty_citations(self):
        receipt = {"query": "q", "answer": "a", "citations": []}
        result = to_markdown(receipt)
        assert "Citations (0 total)" in result

    def test_digest_truncated(self):
        result = to_markdown(FULL_RECEIPT)
        # Only first 16 chars of digest should appear
        digest = FULL_RECEIPT["digest"]
        assert digest[:16] in result
        assert digest not in result


# ---------------------------------------------------------------------------
# to_dot
# ---------------------------------------------------------------------------


class TestToDot:
    def test_starts_with_digraph(self):
        result = to_dot(FULL_RECEIPT)
        assert result.startswith("digraph trace {")

    def test_contains_core_nodes(self):
        result = to_dot(FULL_RECEIPT)
        assert "query" in result
        assert "answer" in result
        assert "receipt" in result

    def test_verified_citation_no_dashed(self):
        result = to_dot(FULL_RECEIPT)
        assert "claim_0" in result
        assert 'shape=box' in result
        # VERIFIED should not have style=dashed
        # Find the claim_0 node line
        for line in result.splitlines():
            if "claim_0" in line and "label" in line:
                assert "style=dashed" not in line

    def test_unverified_citation_dashed(self):
        receipt = {
            "citations": [
                {"fact_id": "f:unv", "truth_status": "UNVERIFIED", "source": "s"}
            ]
        }
        result = to_dot(receipt)
        assert "style=dashed" in result

    def test_blocked_citation_dashed(self):
        receipt = {
            "citations": [
                {"fact_id": "f:blk", "truth_status": "BLOCKED", "source": "s"}
            ]
        }
        result = to_dot(receipt)
        assert "style=dashed" in result

    def test_verify_dict_in_receipt_label(self):
        result = to_dot(COMBINED)
        assert "verified:" in result

    def test_double_quotes_escaped(self):
        receipt = {
            "citations": [
                {
                    "fact_id": 'f:has"quote',
                    "truth_status": "VERIFIED",
                    "source": "s",
                }
            ]
        }
        result = to_dot(receipt)
        assert '\\"' in result

    def test_empty_citations_no_claim_nodes(self):
        receipt = {"citations": []}
        result = to_dot(receipt)
        assert "claim_" not in result

    def test_no_verify_receipt_label_plain(self):
        receipt = {"citations": []}
        result = to_dot(receipt)
        # receipt label should just be "Receipt" without verified:
        assert 'label="Receipt"' in result

    def test_combined_dict_works(self):
        result = to_dot(COMBINED)
        assert "digraph trace {" in result

    def test_fact_id_none_shows_unknown_in_dot(self):
        receipt = {
            "citations": [
                {"fact_id": None, "truth_status": "VERIFIED", "source": "s"}
            ]
        }
        result = to_dot(receipt)
        assert "(unknown)" in result

    def test_fact_id_truncated_at_20_in_dot(self):
        long_id = "f:" + "x" * 25  # 27 chars total
        receipt = {
            "citations": [
                {"fact_id": long_id, "truth_status": "VERIFIED", "source": "s"}
            ]
        }
        result = to_dot(receipt)
        assert "…" in result
        assert long_id not in result


# ---------------------------------------------------------------------------
# No-mutation tests
# ---------------------------------------------------------------------------


class TestNoMutation:
    def test_to_markdown_does_not_modify_input(self):
        import copy
        original = copy.deepcopy(FULL_RECEIPT)
        to_markdown(FULL_RECEIPT)
        assert FULL_RECEIPT == original

    def test_to_dot_does_not_modify_input(self):
        import copy
        original = copy.deepcopy(FULL_RECEIPT)
        to_dot(FULL_RECEIPT)
        assert FULL_RECEIPT == original

    def test_no_memory_truth_gate_l3_imports(self):
        """trace_visualize must not import or call memory/truth_gate/l3_graph."""
        import core.trace_visualize as tv_module
        import importlib

        # Reload to ensure we inspect what was actually imported at module level
        importlib.reload(tv_module)
        # Check module's globals — should not contain references to restricted modules
        mod_globals = set(tv_module.__dict__.keys())
        for forbidden in ("memory", "truth_gate", "l3_graph"):
            assert forbidden not in mod_globals, (
                f"core.trace_visualize must not import {forbidden}"
            )


# ---------------------------------------------------------------------------
# CLI smoke tests (scripts/trace_visualize.py)
# ---------------------------------------------------------------------------


class TestCLI:
    def _write_receipt(self, tmp_path: Path) -> Path:
        p = tmp_path / "receipt.json"
        p.write_text(json.dumps(FULL_RECEIPT), encoding="utf-8")
        return p

    def test_markdown_to_stdout(self, tmp_path: Path, capsys):
        p = self._write_receipt(tmp_path)
        from scripts.trace_visualize import main
        ret = main([str(p), "--format", "markdown"])
        assert ret == 0
        captured = capsys.readouterr()
        assert "## Query" in captured.out

    def test_dot_to_stdout(self, tmp_path: Path, capsys):
        p = self._write_receipt(tmp_path)
        from scripts.trace_visualize import main
        ret = main([str(p), "--format", "dot"])
        assert ret == 0
        captured = capsys.readouterr()
        assert "digraph" in captured.out

    def test_markdown_to_file(self, tmp_path: Path):
        p = self._write_receipt(tmp_path)
        out = tmp_path / "out.md"
        from scripts.trace_visualize import main
        ret = main([str(p), "--format", "markdown", "--out", str(out)])
        assert ret == 0
        content = out.read_text(encoding="utf-8")
        assert "## Query" in content

    def test_dot_to_file(self, tmp_path: Path):
        p = self._write_receipt(tmp_path)
        out = tmp_path / "out.dot"
        from scripts.trace_visualize import main
        ret = main([str(p), "--format", "dot", "--out", str(out)])
        assert ret == 0
        content = out.read_text(encoding="utf-8")
        assert "digraph" in content

    def test_default_format_is_markdown(self, tmp_path: Path, capsys):
        p = self._write_receipt(tmp_path)
        from scripts.trace_visualize import main
        ret = main([str(p)])
        assert ret == 0
        captured = capsys.readouterr()
        assert "## Query" in captured.out

    def test_combined_dict_cli(self, tmp_path: Path, capsys):
        p = tmp_path / "combined.json"
        p.write_text(json.dumps(COMBINED), encoding="utf-8")
        from scripts.trace_visualize import main
        ret = main([str(p), "--format", "markdown"])
        assert ret == 0
        captured = capsys.readouterr()
        assert "digest_valid: True" in captured.out
