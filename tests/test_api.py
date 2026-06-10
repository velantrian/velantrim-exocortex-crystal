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


# ─── curator review endpoints (WP2) ────────────────────────────────────────────

def _pending_blocked(text="A blocked api review claim"):
    """An LLM_OUTPUT WORLD_FACT is deterministically gate-blocked → Observed."""
    from core.ingest import ingest
    res = ingest(text, claim_type="WORLD_FACT", source_status="LLM_OUTPUT")
    assert res["accepted"] is False
    return res["fact"]["fact_id"]


def test_review_queue_report_item_decisions_flow(client, monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    fid = _pending_blocked("The api queue shows this claim")

    queue = client.get("/review/queue", params={"diagnose": "true"}).json()
    assert any(i["fact_id"] == fid and i["diagnosis"]["verdict"] == "blocked"
               for i in queue)
    assert client.get("/review/report").json()["pending"] >= 1

    item = client.get(f"/review/item/{fid}")
    assert item.status_code == 200
    assert item.json()["diagnosis"]["verdict"] == "blocked"
    assert client.get("/review/item/ing:nope").status_code == 404

    ok = client.post("/review/approve",
                     json={"fact_id": fid, "actor": "api-curator",
                           "force": True, "reason": "vetted by hand"})
    assert ok.status_code == 200
    assert ok.json()["approved"] is True and ok.json()["override"] is True

    history = client.get("/review/decisions").json()
    assert history[0]["decision"] == "force_approved"
    assert history[0]["actor"] == "api-curator"


def test_review_force_without_reason_is_422(client, monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    fid = _pending_blocked("A claim force-approved without a reason")
    r = client.post("/review/approve",
                    json={"fact_id": fid, "actor": "x", "force": True})
    assert r.status_code == 422
    assert "reason" in r.json()["detail"]
    r2 = client.post("/review/approve",
                     json={"fact_id": fid, "force": True, "reason": "   "})
    assert r2.status_code == 422


def test_review_reject_endpoint_and_404(client, monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    fid = _pending_blocked("A claim rejected over http")
    r = client.post("/review/reject",
                    json={"fact_id": fid, "actor": "api", "reason": "noise"})
    assert r.status_code == 200 and r.json()["rejected"] is True
    assert client.post("/review/reject",
                       json={"fact_id": "ing:nope"}).status_code == 404
    assert client.post("/review/approve",
                       json={"fact_id": "ing:nope"}).status_code == 404


def test_review_token_guard_on_get_and_post(client, monkeypatch):
    """Negative test: with VELANTRIM_API_TOKEN set, every /review/* JSON
    endpoint — GET and POST — answers 401 without (or with a wrong) Bearer
    token, and 200 with the right one."""
    monkeypatch.setenv("VELANTRIM_API_TOKEN", "s3cret")
    for path in ("/review/queue", "/review/report", "/review/decisions"):
        assert client.get(path).status_code == 401
        assert client.get(
            path, headers={"Authorization": "Bearer wrong"}).status_code == 401
        assert client.get(
            path, headers={"Authorization": "Bearer s3cret"}).status_code == 200
    assert client.get("/review/item/ing:x").status_code == 401
    assert client.post("/review/approve",
                       json={"fact_id": "ing:x"}).status_code == 401
    assert client.post("/review/reject",
                       json={"fact_id": "ing:x"}).status_code == 401
    # Non-review endpoints keep the historical localhost-trust posture.
    assert client.get("/health").status_code == 200


def test_review_ui_is_a_dataless_static_shell(client, monkeypatch):
    """The public /review/ui shell must embed NO claims, fact ids or local
    memory content — data flows only through the guarded JSON endpoints."""
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    marker = "an extremely unique zanzibar gateway claim"
    fid = _pending_blocked(marker)
    r = client.get("/review/ui")
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("text/html")
    html = r.text
    assert "Crystal Review Queue" in html
    assert marker not in html and "zanzibar" not in html
    assert fid not in html
    # And it stays public even when the JSON endpoints are token-guarded.
    monkeypatch.setenv("VELANTRIM_API_TOKEN", "s3cret")
    assert client.get("/review/ui").status_code == 200


def test_review_ui_ships_as_package_data():
    from importlib import resources
    html = resources.files("core").joinpath(
        "_webui/review.html").read_text(encoding="utf-8")
    assert "Crystal Review Queue" in html
