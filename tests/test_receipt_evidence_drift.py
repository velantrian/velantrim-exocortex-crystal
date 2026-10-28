"""A source ID is not sufficient to replay sealed evidence after drift."""
import copy
import json

import pytest

from core import evidence, memory, provenance
from core.ingest import ingest


def _receipt():
    fact = ingest("A source-linked test claim", source_status="EXTERNAL")["fact"]
    evidence.attach_evidence(
        fact["fact_id"], "source.txt", source_kind="file", source_text="source text",
        chunk_id="chunk:1", section="section:1", span_start=0, span_end=5,
    )
    return provenance.build_receipt({"answer": fact["claim"], "query": "test", "facts": [fact]})


@pytest.mark.parametrize("signed", [False, True])
@pytest.mark.parametrize("strict", [False, True])
@pytest.mark.parametrize("field,value", [
    ("source_uri", "different.txt"), ("source_kind", "url"),
    ("chunk_id", "chunk:2"), ("section", "section:2"),
    ("span_start", 1), ("span_end", 6),
    ("source_sha256", "0" * 64), ("claim_sha256", "1" * 64),
])
def test_source_metadata_drift_is_rejected(monkeypatch, signed, strict, field, value):
    if signed:
        monkeypatch.setenv("VELANTRIM_PROVENANCE_KEY", "synthetic-test-key")
    else:
        monkeypatch.delenv("VELANTRIM_PROVENANCE_KEY", raising=False)
    receipt = _receipt()
    assert provenance.verify_receipt(receipt, strict_provenance=strict)["verified"] is True
    sealed = copy.deepcopy(receipt)
    span_id = receipt["citations"][0]["evidence"][0]["evidence_id"]
    # field is from the closed parametrization above, never caller input.
    with memory._db() as conn:
        conn.execute(f"UPDATE evidence_spans SET {field} = ? WHERE evidence_id = ?", (value, span_id))
    before = evidence.evidence_for(receipt["citations"][0]["fact_id"])
    report = provenance.verify_receipt(receipt, strict_provenance=strict)
    assert report["digest_valid"] is True
    assert report["signature_valid"] is (True if signed else None)
    assert report["verified"] is False
    assert report["citations"][0]["status"] == "evidence_modified"
    assert report["citations"][0]["evidence"][0]["status"] == "evidence_modified"
    assert receipt == sealed
    assert evidence.evidence_for(receipt["citations"][0]["fact_id"]) == before


def test_omitted_optional_legacy_span_fields_remain_compatible():
    receipt = _receipt()
    span = receipt["citations"][0]["evidence"][0]
    for name in ("chunk_id", "section"):
        del span[name]
    receipt["digest"] = provenance._digest(receipt)
    assert provenance.verify_receipt(receipt)["verified"] is True


def test_missing_evidence_has_priority_over_changed_evidence():
    receipt = _receipt()
    citation = receipt["citations"][0]
    missing = dict(citation["evidence"][0], evidence_id="ev:missing")
    citation["evidence"].append(missing)
    receipt["digest"] = provenance._digest(receipt)
    with memory._db() as conn:
        conn.execute("UPDATE evidence_spans SET source_sha256 = ?", ("0" * 64,))
    report = provenance.verify_receipt(receipt)
    assert report["verified"] is False
    assert report["citations"][0]["status"] == "evidence_missing"
    assert report["summary"] == {"evidence_missing": 1}
    assert {span["status"] for span in report["citations"][0]["evidence"]} == {
        "evidence_missing", "evidence_modified",
    }


def test_claim_drift_keeps_fact_level_verdict_with_existing_evidence():
    receipt = _receipt()
    fid = receipt["citations"][0]["fact_id"]
    with memory._db() as conn:
        conn.execute(
            "UPDATE facts SET claim = ?, revision = revision + 1 WHERE fact_id = ?",
            (memory.crypto.encrypt("changed claim"), fid),
        )
    memory._L0.clear()
    report = provenance.verify_receipt(receipt)
    assert report["verified"] is False
    assert report["citations"][0]["status"] == "modified"
    assert report["citations"][0]["evidence"][0]["status"] == "modified"


def test_cli_negative_evidence_verdict_keeps_json_contract(tmp_path, capsys):
    """Exit zero means a verdict was emitted, not that the receipt is valid."""
    from core.cli import main

    receipt = _receipt()
    evidence_id = receipt["citations"][0]["evidence"][0]["evidence_id"]
    with memory._db() as conn:
        conn.execute(
            "UPDATE evidence_spans SET source_uri = ? WHERE evidence_id = ?",
            ("tampered.txt", evidence_id),
        )

    path = tmp_path / "receipt.json"
    path.write_text(json.dumps(receipt), encoding="utf-8")
    assert main(["verify-receipt", str(path), "--strict-provenance"]) == 0

    report = json.loads(capsys.readouterr().out)
    assert report["digest_valid"] is True
    assert report["verified"] is False
    assert report["citations"][0]["status"] == "evidence_modified"
    assert report["summary"] == {"evidence_modified": 1}


def test_mcp_transports_negative_evidence_verdict_without_tool_error():
    """MCP transport success is not receipt verification success."""
    from core.mcp_server import handle_message

    receipt = _receipt()
    evidence_id = receipt["citations"][0]["evidence"][0]["evidence_id"]
    with memory._db() as conn:
        conn.execute(
            "UPDATE evidence_spans SET source_sha256 = ? WHERE evidence_id = ?",
            ("0" * 64, evidence_id),
        )

    response = handle_message({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {"name": "verify_receipt", "arguments": {"receipt": receipt}},
    })
    assert response["result"]["isError"] is False
    report = json.loads(response["result"]["content"][0]["text"])
    assert report["verified"] is False
    assert report["citations"][0]["status"] == "evidence_modified"
