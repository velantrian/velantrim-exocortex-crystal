"""Tests for core/provenance.py — verifiable, replayable answer receipts."""
import copy
import json

import pytest

from core import provenance, memory
from core.pipeline import run
from core.ingest import ingest
from core.erasure import erase_fact
from core.compliance import restrict_processing


def _answer_with_facts():
    """Drive the pipeline to a real answer and return its result."""
    res = run("What is quantum entanglement?")
    assert res.get("answer") is not None
    assert res["facts"], "expected at least one cited fact"
    return res


# ─── receipt construction & sealing ───────────────────────────────────────────

def test_build_receipt_shape():
    receipt = provenance.build_receipt(_answer_with_facts())
    assert receipt["version"] == provenance.RECEIPT_VERSION
    assert receipt["answer"]
    assert receipt["query"] == "What is quantum entanglement?"
    assert len(receipt["digest"]) == 64
    for cit in receipt["citations"]:
        assert set(cit) == {"fact_id", "claim_sha256", "source",
                            "epistemic_state", "truth_status"}
        assert len(cit["claim_sha256"]) == 64


def test_build_receipt_rejects_blocked():
    with pytest.raises(ValueError):
        provenance.build_receipt({"answer": None, "facts": []})


def test_receipt_is_content_light():
    # Citations commit to claims by hash, not by storing the text (the answer
    # field naturally contains the synthesised text; the citations must not).
    res = _answer_with_facts()
    receipt = provenance.build_receipt(res)
    citations_blob = json.dumps(receipt["citations"])
    for f in res["facts"]:
        assert f["claim"] not in citations_blob


# ─── digest verification (tamper-evidence) ────────────────────────────────────

def test_verify_fresh_receipt_ok():
    report = provenance.verify_receipt(provenance.build_receipt(_answer_with_facts()))
    assert report["digest_valid"] is True
    assert report["verified"] is True
    assert all(c["status"] == "ok" for c in report["citations"])


def test_tampered_answer_breaks_digest():
    receipt = provenance.build_receipt(_answer_with_facts())
    receipt["answer"] += " (and the moon is made of cheese)"
    report = provenance.verify_receipt(receipt)
    assert report["digest_valid"] is False
    assert report["verified"] is False


def test_tampered_citation_breaks_digest():
    receipt = provenance.build_receipt(_answer_with_facts())
    receipt["citations"][0]["claim_sha256"] = "0" * 64
    assert provenance.verify_receipt(receipt)["digest_valid"] is False


# ─── replay against the canon: drift detection ────────────────────────────────

def test_replay_detects_erasure():
    res = _answer_with_facts()
    receipt = provenance.build_receipt(res)
    erase_fact(receipt["citations"][0]["fact_id"], reason="test")
    report = provenance.verify_receipt(receipt)
    assert report["digest_valid"] is True       # receipt itself untouched
    assert report["verified"] is False          # but a source is gone
    assert any(c["status"] == "erased" for c in report["citations"])


def test_replay_detects_restriction():
    res = _answer_with_facts()
    receipt = provenance.build_receipt(res)
    restrict_processing(receipt["citations"][0]["fact_id"])
    report = provenance.verify_receipt(receipt)
    assert any(c["status"] == "restricted" for c in report["citations"])
    assert report["verified"] is False


def test_replay_detects_modification():
    res = _answer_with_facts()
    receipt = provenance.build_receipt(res)
    fid = receipt["citations"][0]["fact_id"]
    memory.update_fact(fid, claim="A completely different claim now")
    report = provenance.verify_receipt(receipt)
    assert any(c["status"] == "modified" for c in report["citations"])
    assert report["verified"] is False


def test_replay_detects_invalidation():
    res = _answer_with_facts()
    receipt = provenance.build_receipt(res)
    fid = receipt["citations"][0]["fact_id"]
    memory.transition_esm(fid, "Collapsed")
    report = provenance.verify_receipt(receipt)
    assert any(c["status"] == "invalidated" for c in report["citations"])


def test_replay_detects_missing():
    receipt = {
        "version": 1, "created_at": "2026-01-01T00:00:00+00:00",
        "query": "q", "answer": "a",
        "citations": [{"fact_id": "nonexistent", "claim_sha256": provenance.claim_digest("x"),
                       "source": "s", "epistemic_state": "Validated", "truth_status": "VERIFIED"}],
    }
    receipt["digest"] = provenance._digest(receipt)
    report = provenance.verify_receipt(receipt)
    assert report["citations"][0]["status"] == "missing"


# ─── optional HMAC signing ────────────────────────────────────────────────────

def test_signed_receipt_round_trip(monkeypatch):
    monkeypatch.setenv("VELANTRIM_PROVENANCE_KEY", "s3cret")
    receipt = provenance.build_receipt(_answer_with_facts())
    assert "signature" in receipt
    report = provenance.verify_receipt(receipt)
    assert report["signature_valid"] is True
    assert report["verified"] is True


def test_forged_signature_rejected(monkeypatch):
    monkeypatch.setenv("VELANTRIM_PROVENANCE_KEY", "s3cret")
    receipt = provenance.build_receipt(_answer_with_facts())
    receipt["signature"] = "deadbeef" * 8
    report = provenance.verify_receipt(receipt)
    assert report["signature_valid"] is False
    assert report["verified"] is False


def test_unsigned_when_no_key(monkeypatch):
    monkeypatch.delenv("VELANTRIM_PROVENANCE_KEY", raising=False)
    receipt = provenance.build_receipt(_answer_with_facts())
    assert "signature" not in receipt
    assert provenance.verify_receipt(receipt)["signature_valid"] is None


# ─── CLI ──────────────────────────────────────────────────────────────────────

def test_cli_receipt_then_verify(capsys):
    from core.cli import main
    assert main(["receipt", "How does DNA work?"]) == 0
    receipt_json = capsys.readouterr().out.strip()
    receipt = json.loads(receipt_json)
    assert receipt["digest"]

    # Feed the receipt back through verify-receipt via stdin.
    import io
    import sys
    monkey_stdin = io.StringIO(receipt_json)
    old = sys.stdin
    sys.stdin = monkey_stdin
    try:
        assert main(["verify-receipt", "-"]) == 0
    finally:
        sys.stdin = old
    out = json.loads(capsys.readouterr().out.strip())
    assert out["digest_valid"] is True
    assert out["verified"] is True


def test_cli_receipt_blocked_returns_1(monkeypatch, capsys):
    from core import cli
    monkeypatch.setattr(cli, "run", lambda q: {"answer": None, "error": "no results"})
    assert cli.main(["receipt", "nothing matches"]) == 1
    assert json.loads(capsys.readouterr().out.strip())["error"] == "no results"


def test_cli_verify_receipt_from_file(tmp_path, capsys):
    from core.cli import main
    main(["receipt", "How does DNA work?"])
    receipt_json = capsys.readouterr().out.strip()
    path = tmp_path / "receipt.json"
    path.write_text(receipt_json, encoding="utf-8")
    assert main(["verify-receipt", str(path)]) == 0
    assert json.loads(capsys.readouterr().out.strip())["verified"] is True
