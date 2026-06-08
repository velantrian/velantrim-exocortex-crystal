"""Tests for the optional FastAPI service layer (core/api.py).

Skipped automatically on a stdlib-only install (no fastapi). CI installs the
dev requirements (fastapi + httpx), so these run there.
"""
import pytest

fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient  # noqa: E402

from core import api  # noqa: E402


@pytest.fixture
def client():
    return TestClient(api.create_app())


# ─── health ───────────────────────────────────────────────────────────────────

def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert body["service"] == "velantrim-crystal"


# ─── ingest → ask ──────────────────────────────────────────────────────────────

def test_ingest_then_ask(client):
    r = client.post("/ingest", json={"text": "Lisbon is the capital of Portugal",
                                     "source": "test", "claim_type": "WORLD_FACT",
                                     "source_status": "EXTERNAL"})
    assert r.status_code == 200
    assert r.json()["accepted"] is True

    r2 = client.post("/ask", json={"query": "what is the capital of Portugal"})
    assert r2.status_code == 200
    assert r2.json()["answer"] is not None


def test_ingest_rejects_empty_text(client):
    # pydantic min_length=1 → 422 before the pipeline is touched.
    assert client.post("/ingest", json={"text": ""}).status_code == 422


def test_ingest_invalid_source_status_is_422(client):
    r = client.post("/ingest", json={"text": "A fact", "source_status": "NONSENSE"})
    assert r.status_code == 422


def test_ask_blocked_returns_200_with_error(client):
    # A query with no grounding is a valid verifiable outcome, not a 500.
    r = client.post("/ask", json={"query": "zzz nonexistent topic qqq"})
    assert r.status_code == 200
    body = r.json()
    assert body["answer"] is None
    assert "error" in body


# ─── receipt → verify ───────────────────────────────────────────────────────────

def test_receipt_and_verify(client):
    client.post("/ingest", json={"text": "Gold is a chemical element",
                                 "source": "test", "source_status": "EXTERNAL"})
    r = client.get("/receipt", params={"q": "tell me about gold"})
    assert r.status_code == 200
    receipt = r.json()
    assert receipt["digest"]

    v = client.post("/verify-receipt", json={"receipt": receipt})
    assert v.status_code == 200
    assert v.json()["digest_valid"] is True


def test_receipt_blocked_returns_422(client):
    # No grounding → no answer to attest to → build_receipt raises → 422.
    r = client.get("/receipt", params={"q": "zzz nothing matches qqq"})
    assert r.status_code == 422


# ─── evidence ───────────────────────────────────────────────────────────────────

def test_evidence_endpoint(client):
    res = client.post("/ingest", json={"text": "Helium is a noble gas",
                                       "source": "test", "source_status": "EXTERNAL"})
    fact_id = res.json()["fact"]["fact_id"]
    from core import evidence
    evidence.attach_evidence(fact_id, "chem.txt", source_text="Helium is a noble gas")

    r = client.get(f"/evidence/{fact_id}")
    assert r.status_code == 200
    rows = r.json()
    assert rows and rows[0]["source_uri"] == "chem.txt"


def test_evidence_unknown_fact_is_empty(client):
    r = client.get("/evidence/does-not-exist")
    assert r.status_code == 200
    assert r.json() == []


# ─── guarded import ──────────────────────────────────────────────────────────────

def test_create_app_without_fastapi_raises(monkeypatch):
    monkeypatch.setattr(api, "_HAS_FASTAPI", False)
    with pytest.raises(RuntimeError, match="optional extra"):
        api.create_app()
