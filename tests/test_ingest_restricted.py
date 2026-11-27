"""Ordinary ingest must not process a restricted fact (GDPR Art. 18).

Before this guard, a repeat ingest of a restricted Validated fact recorded an
occurrence (duplicate path) and returned the full stored record, and a repeat
of a restricted non-Validated fact updated source/confidence/metadata through
store_fact(). Both were processing of restricted data, and HTTP /ingest
returned the stored claim and metadata to the caller.
"""
from copy import deepcopy

import pytest

from core import memory
from core.ingest import IngestError, _fact_id, ingest
from core.l3_graph import get_l3_graph


def _seed(fact_id, claim, state):
    memory.store_fact({
        "fact_id": fact_id,
        "claim": claim,
        "source": "baseline-source",
        "source_status": "EXTERNAL",
        "confidence": 0.91,
        "epistemic_state": state,
        "metadata": {"occurrences": 4, "sources_seen": ["baseline-source"]},
    })
    get_l3_graph().merge_fact({**memory.get_fact(fact_id), "truth_status": "VERIFIED"})


def _snapshot(fact_id):
    with memory._db() as conn:
        row = dict(conn.execute(
            "SELECT * FROM facts WHERE fact_id = ?", (fact_id,)).fetchone())
    return {"l1": row, "l3": deepcopy(get_l3_graph().get_fact(fact_id))}


@pytest.mark.parametrize("state", ["Validated", "Observed"])
def test_auto_id_repeat_of_restricted_fact_is_refused_without_writes(state):
    claim = f"Synthetic restricted repeat {state}"
    fact_id = _fact_id(claim)
    _seed(fact_id, claim, state)
    assert memory.set_restricted(fact_id, True) is True
    before = _snapshot(fact_id)

    with pytest.raises(IngestError) as exc_info:
        ingest(claim, source="second-source", confidence=0.2)

    assert exc_info.value.code == "RESTRICTED"
    assert _snapshot(fact_id) == before


def test_explicit_id_update_of_restricted_fact_is_refused_without_writes():
    claim = "Synthetic restricted explicit id"
    _seed("restricted-explicit", claim, "Observed")
    assert memory.set_restricted("restricted-explicit", True) is True
    before = _snapshot("restricted-explicit")

    with pytest.raises(IngestError) as exc_info:
        ingest(claim, fact_id="restricted-explicit", source="other",
               metadata={"new": "value"})

    assert exc_info.value.code == "RESTRICTED"
    assert _snapshot("restricted-explicit") == before


def test_http_ingest_of_restricted_fact_returns_422_without_the_record(monkeypatch):
    from fastapi.testclient import TestClient
    from core import api

    monkeypatch.setenv("VELANTRIM_API_ALLOW_UNAUTH_LOCAL", "1")
    monkeypatch.delenv("VELANTRIM_API_TOKEN", raising=False)
    claim = "Synthetic restricted HTTP repeat"
    fact_id = _fact_id(claim)
    _seed(fact_id, claim, "Validated")
    assert memory.set_restricted(fact_id, True) is True
    before = _snapshot(fact_id)

    response = TestClient(api.create_app()).post(
        "/ingest", json={"text": claim, "source": "http-repeat"})

    assert response.status_code == 422
    assert response.json()["detail"].startswith("RESTRICTED:")
    assert "baseline-source" not in response.text
    assert "occurrences" not in response.text
    assert _snapshot(fact_id) == before


def test_lifting_the_restriction_restores_ordinary_duplicate_handling():
    claim = "Synthetic restriction lifted"
    fact_id = _fact_id(claim)
    _seed(fact_id, claim, "Validated")
    assert memory.set_restricted(fact_id, True) is True
    with pytest.raises(IngestError):
        ingest(claim, source="while-restricted")
    assert memory.set_restricted(fact_id, False) is True

    result = ingest(claim, source="after-lift")

    assert result["accepted"] is True and result["duplicate"] is True
    assert result["occurrences"] == 5
