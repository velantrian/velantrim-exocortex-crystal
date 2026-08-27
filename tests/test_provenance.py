"""Tests for core/provenance.py — verifiable, replayable answer receipts."""
import copy
import json

import pytest

from core import provenance, memory, evidence
from core.pipeline import run
from core.ingest import ingest
from core.erasure import erase_fact
from core.compliance import restrict_processing


def _tamper_claim_at_rest(fact_id, claim):
    """Simulate out-of-band DB tampering; public APIs reject this rewrite."""
    with memory._db() as conn:
        conn.execute(
            "UPDATE facts SET claim = ?, revision = revision + 1 WHERE fact_id = ?",
            (memory.crypto.encrypt(claim), fact_id),
        )
    memory._L0.clear()


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
    _tamper_claim_at_rest(fid, "A completely different claim now")
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

def _seed_cli_receipt_fact():
    """Explicitly admit one source fact; read-only receipt must never seed it."""
    claim = "DNA carries genetic information"
    result = ingest(
        claim,
        source="reference",
        source_status="EXTERNAL",
        confidence=0.95,
    )
    assert result["accepted"] is True
    evidence.attach_evidence(
        result["fact"]["fact_id"], "file://dna.txt",
        source_text="DNA source", section="fixture",
    )
    return claim


def test_cli_receipt_then_verify(capsys):
    from core.cli import main
    claim = _seed_cli_receipt_fact()
    assert main(["receipt", claim]) == 0
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
    monkeypatch.setattr(cli, "query", lambda q: {"answer": None, "error": "no results"})
    assert cli.main(["receipt", "nothing matches"]) == 1
    assert json.loads(capsys.readouterr().out.strip())["error"] == "no results"


def test_cli_verify_receipt_from_file(tmp_path, capsys):
    from core.cli import main
    claim = _seed_cli_receipt_fact()
    assert main(["receipt", claim]) == 0
    receipt_json = capsys.readouterr().out.strip()
    path = tmp_path / "receipt.json"
    path.write_text(receipt_json, encoding="utf-8")
    assert main(["verify-receipt", str(path)]) == 0
    assert json.loads(capsys.readouterr().out.strip())["verified"] is True


# ─── strict provenance: VERIFIED claims must carry evidence (#61) ──────────────

def _verified_fact_result():
    """A pipeline-shaped result citing one VERIFIED fact (no evidence attached)."""
    res = ingest("Lisbon is the capital of Portugal", source_status="EXTERNAL")
    fact = res["fact"]
    assert fact["truth_status"] == "VERIFIED"
    return fact["fact_id"], {
        "answer": "Lisbon is the capital of Portugal.",
        "query": "What is the capital of Portugal?",
        "facts": [fact],
    }


def test_strict_provenance_flags_verified_without_evidence():
    _fid, result = _verified_fact_result()
    receipt = provenance.build_receipt(result)
    # Lenient (default): the citation replays cleanly.
    lenient = provenance.verify_receipt(receipt)
    assert lenient["citations"][0]["status"] == "ok"
    assert lenient["verified"] is True
    # Strict: a VERIFIED claim with no evidence is unsupported provenance.
    strict = provenance.verify_receipt(receipt, strict_provenance=True)
    assert strict["citations"][0]["status"] == "unsupported_provenance"
    assert strict["verified"] is False


def test_strict_provenance_passes_once_evidence_attached():
    fid, result = _verified_fact_result()
    evidence.attach_evidence(
        fid, "geo.md", source_text="Lisbon is the capital of Portugal.")
    receipt = provenance.build_receipt(result)
    strict = provenance.verify_receipt(receipt, strict_provenance=True)
    assert strict["citations"][0]["status"] == "ok"
    assert strict["verified"] is True


def test_cli_verify_receipt_strict_provenance_flag(tmp_path, capsys):
    """`velantrim verify-receipt --strict-provenance` flags a VERIFIED citation
    with no source-span evidence (parity with the API's strict_provenance)."""
    from core.cli import main
    _fid, result = _verified_fact_result()
    path = tmp_path / "receipt.json"
    path.write_text(json.dumps(provenance.build_receipt(result)), encoding="utf-8")

    assert main(["verify-receipt", str(path)]) == 0
    lenient = json.loads(capsys.readouterr().out.strip())
    assert lenient["verified"] is True

    assert main(["verify-receipt", str(path), "--strict-provenance"]) == 0
    strict = json.loads(capsys.readouterr().out.strip())
    assert strict["citations"][0]["status"] == "unsupported_provenance"
    assert strict["verified"] is False
