"""The attested answer/receipt covers only admitted current grounds.

Historical (time-excluded) claims are reported in the separately labelled
``uncertainty`` and ``applicability["historical_facts"]`` fields. They are not
concatenated into ``answer`` and therefore never sealed into a receipt whose
citations do not include them. Real isolated SQLite L1/L3, real retrieval.
"""
import json

import pytest

from core import provenance
from core.query_pipeline import query
from tests.test_applicability_live_path import NOW, admit, reopen
from tests.test_applicability_live_path import durable as durable  # pytest fixture registration

CURRENT = "Laboratory component ready now"
OLD = "Laboratory component broken earlier"
QUESTION = "Laboratory component"
OLD_AT = "2026-10-08T10:00:00+02:00"
PARAMS = {"asked_object": "L", "as_of": NOW, "temporal_scope": "current"}


def _store(*, current, old):
    if current:
        admit("cur", CURRENT, {"primary_object": "L", "observed_at": NOW})
    if old:
        admit("old", OLD, {"primary_object": "L", "observed_at": OLD_AT})
    reopen()


def _http_client(monkeypatch):
    from core.api import create_app
    from fastapi.testclient import TestClient
    monkeypatch.setenv("VELANTRIM_API_ALLOW_UNAUTH_LOCAL", "1")
    monkeypatch.delenv("VELANTRIM_API_TOKEN", raising=False)
    return TestClient(create_app())


def _cli(capsys, *argv):
    from core.cli import main
    code = main([*argv, QUESTION, "--asked-object", "L", "--as-of", NOW,
                 "--temporal-scope", "current"])
    return code, capsys.readouterr().out


def test_current_next_to_old_receipt_attests_only_current_answer(durable, monkeypatch, capsys):
    _store(current=True, old=True)
    result = query(QUESTION, **PARAMS)
    assert result["answer"] == CURRENT
    assert OLD not in result["answer"] and "Uncertainty" not in result["answer"]
    assert [f["fact_id"] for f in result["facts"]] == ["cur"]
    assert {t.get("id") or t.get("fact_id") for t in result["trace"]} == {"cur"}
    # Old material is preserved, but only in the separately labelled fields.
    historical = result["applicability"]["historical_facts"]
    assert [(h["fact_id"], h["claim"]) for h in historical] == [("old", OLD)]
    assert OLD in result["uncertainty"] and "Historical evidence only" in result["uncertainty"]

    receipt = provenance.build_receipt(result)
    assert receipt["answer"] == CURRENT
    assert [c["fact_id"] for c in receipt["citations"]] == ["cur"]
    assert OLD not in json.dumps(receipt, ensure_ascii=False)
    assert provenance.verify_receipt(receipt)["verified"] is True

    client = _http_client(monkeypatch)
    ask = client.post("/ask", json={"query": QUESTION, **PARAMS}).json()
    assert ask["answer"] == CURRENT
    assert ask["applicability"]["historical_facts"][0]["claim"] == OLD
    http_receipt = client.get("/receipt", params={"q": QUESTION, **PARAMS})
    assert http_receipt.status_code == 200
    assert http_receipt.json()["answer"] == CURRENT
    assert OLD not in http_receipt.text
    assert [c["fact_id"] for c in http_receipt.json()["citations"]] == ["cur"]

    code, out = _cli(capsys, "ask")
    lines = out.splitlines()
    assert code == 0 and lines[0] == CURRENT
    assert lines[1].startswith("[uncertainty, not attested] ") and OLD in lines[1]
    code, out = _cli(capsys, "receipt")
    assert code == 0
    cli_receipt = json.loads(out)
    assert cli_receipt["answer"] == CURRENT and OLD not in out
    assert provenance.verify_receipt(cli_receipt)["verified"] is True


def test_only_old_information_yields_no_current_status_receipt(durable, monkeypatch, capsys):
    _store(current=False, old=True)
    result = query(QUESTION, **PARAMS)
    assert result["answer"] is None
    assert result["facts"] == []
    assert "current status is not established" in result["error"]
    assert [h["claim"] for h in result["applicability"]["historical_facts"]] == [OLD]
    assert OLD in result["uncertainty"]
    with pytest.raises(ValueError, match="no answer"):
        provenance.build_receipt(result)

    client = _http_client(monkeypatch)
    ask = client.post("/ask", json={"query": QUESTION, **PARAMS}).json()
    assert ask["answer"] is None
    assert ask["applicability"]["historical_facts"][0]["claim"] == OLD
    http_receipt = client.get("/receipt", params={"q": QUESTION, **PARAMS})
    assert http_receipt.status_code == 422
    assert "digest" not in http_receipt.text

    code, out = _cli(capsys, "receipt")
    assert code == 1
    assert "digest" not in json.loads(out)
    code, out = _cli(capsys, "ask")
    assert out.startswith("[blocked] ") and "[uncertainty, not attested]" not in out


def test_only_current_information_receipt_has_no_historical_or_uncertainty(durable, monkeypatch, capsys):
    _store(current=True, old=False)
    result = query(QUESTION, **PARAMS)
    assert result["answer"] == CURRENT
    assert "uncertainty" not in result and "applicability" not in result
    receipt = provenance.build_receipt(result)
    assert receipt["answer"] == CURRENT
    assert [c["fact_id"] for c in receipt["citations"]] == ["cur"]
    assert provenance.verify_receipt(receipt)["verified"] is True

    client = _http_client(monkeypatch)
    ask = client.post("/ask", json={"query": QUESTION, **PARAMS}).json()
    assert ask["answer"] == CURRENT and "uncertainty" not in ask
    assert client.get("/receipt", params={"q": QUESTION, **PARAMS}).json()["answer"] == CURRENT

    code, out = _cli(capsys, "ask")
    assert code == 0 and out.splitlines() == [CURRENT]
