"""Tests for the optional FastAPI service layer (core/api.py).

Skipped automatically on a stdlib-only install (no fastapi). CI installs the
dev requirements (fastapi + httpx), so these run there.
"""
import pytest

fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient  # noqa: E402

from core import api  # noqa: E402


@pytest.fixture
def client(monkeypatch):
    # A TestClient is definitionally a local-development instance. The service
    # now fails closed when no token is configured, so opt into the explicit
    # local-dev bypass here; tests that exercise real token auth set
    # VELANTRIM_API_TOKEN themselves (which takes precedence over the bypass).
    monkeypatch.setenv("VELANTRIM_API_ALLOW_UNAUTH_LOCAL", "1")
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
                                     "source": "test", "claim_type": "WORLD_FACT"})
    assert r.status_code == 200
    assert r.json()["accepted"] is True

    r2 = client.post("/ask", json={"query": "what is the capital of Portugal"})
    assert r2.status_code == 200
    assert r2.json()["answer"] is not None


def test_ingest_blocks_llm_output_world_fact(client):
    """Write-path gate (Track 3B pin): POST /ingest with an LLM_OUTPUT
    WORLD_FACT is a valid request (200) but the gate blocks promotion —
    accepted is False with the gate reason. An LLM output cannot become a
    WORLD_FACT through the HTTP write path."""
    r = client.post("/ingest", json={
        "text": "Krellium absorbs all wavelengths of light at room temperature",
        "source": "test", "claim_type": "WORLD_FACT",
        "source_status": "LLM_OUTPUT", "confidence": 0.9,
    })
    assert r.status_code == 200
    body = r.json()
    assert body["accepted"] is False
    assert "LLM_OUTPUT cannot be WORLD_FACT" in body["reason"]


def test_ingest_rejects_empty_text(client):
    # pydantic min_length=1 → 422 before the pipeline is touched.
    assert client.post("/ingest", json={"text": ""}).status_code == 422


def test_ingest_rejects_privileged_source_status_without_import_mode(client):
    r = client.post("/ingest", json={
        "text": "A privileged world fact from the API",
        "source_status": "EXTERNAL",
        "claim_type": "WORLD_FACT",
    })
    assert r.status_code == 422
    assert "privileged source_status" in r.json()["detail"]


def test_ingest_defaults_api_source_status_to_user_reported(client):
    r = client.post("/ingest", json={
        "text": "Lisbon is the capital of Portugal",
        "source": "test", "claim_type": "WORLD_FACT",
    })
    assert r.status_code == 200
    assert r.json()["fact"]["source_status"] == "USER_REPORTED"


def test_ingest_privileged_import_with_env(client, monkeypatch):
    monkeypatch.setenv("VELANTRIM_API_PRIVILEGED_INGEST", "1")
    r = client.post("/ingest", json={
        "text": "The speed of light in vacuum is constant",
        "source_status": "EXTERNAL",
        "import_mode": True,
        "evidence_refs": ["physics/constants.txt"],
        "claim_type": "WORLD_FACT",
        "confidence": 0.95,
    })
    assert r.status_code == 200
    meta = r.json()["fact"]["metadata"]
    assert meta["admission_path"] == "api_privileged_import"
    assert meta["evidence_refs"] == ["physics/constants.txt"]


def test_ingest_invalid_source_status_is_422(client):
    r = client.post("/ingest", json={"text": "A fact", "source_status": "NONSENSE"})
    assert r.status_code == 422


def test_ingest_invalid_claim_type_from_ingest_is_422(client):
    r = client.post("/ingest", json={"text": "A fact", "claim_type": "NONSENSE"})
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
                                 "source": "test", "claim_type": "WORLD_FACT",
                                 "confidence": 0.9})
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
                                       "source": "test", "claim_type": "WORLD_FACT",
                                       "confidence": 0.9})
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


def test_evidence_endpoint_redacts_restricted_fact(client):
    res = client.post("/ingest", json={"text": "A restricted claim with a source",
                                       "source": "test", "claim_type": "WORLD_FACT",
                                       "confidence": 0.9})
    fact_id = res.json()["fact"]["fact_id"]
    from core import evidence
    from core.compliance import restrict_processing
    evidence.attach_evidence(fact_id, "private/notes.txt")
    restrict_processing(fact_id, reason="dispute")

    r = client.get(f"/evidence/{fact_id}")
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


def test_review_force_without_explicit_actor_is_422(client, monkeypatch):
    """force=true demands an explicit actor — no default identity may sign a
    blocking-diagnosis override; a reason longer than 500 chars is also 422."""
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    fid = _pending_blocked("A claim force-approved by nobody")
    r = client.post("/review/approve",
                    json={"fact_id": fid, "force": True, "reason": "vetted"})
    assert r.status_code == 422
    assert "actor" in r.json()["detail"]
    r2 = client.post("/review/approve",
                     json={"fact_id": fid, "actor": "  ", "force": True,
                           "reason": "vetted"})
    assert r2.status_code == 422
    r3 = client.post("/review/approve",
                     json={"fact_id": fid, "actor": "x", "force": True,
                           "reason": "x" * 501})
    assert r3.status_code == 422  # pydantic max_length on reason
    # The fact never moved.
    from core.memory import get_fact
    assert get_fact(fid)["epistemic_state"] == "Observed"


def test_review_decisions_include_claim_false_is_content_free(client, monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    claim = "A privacy-sensitive http claim"
    fid = _pending_blocked(claim)
    ok = client.post("/review/approve",
                     json={"fact_id": fid, "actor": "api-curator",
                           "force": True, "reason": "vetted by hand"})
    assert ok.status_code == 200
    full = client.get("/review/decisions").json()
    assert full[0]["claim"] == claim            # default keeps the UI working
    lean = client.get("/review/decisions",
                      params={"include_claim": "false"}).json()
    assert "claim" not in lean[0] and "claim_type" not in lean[0]
    assert claim not in str(lean)


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


def test_api_token_guard_on_memory_and_review_endpoints(client, monkeypatch):
    """With VELANTRIM_API_TOKEN set, memory and review endpoints require Bearer."""
    monkeypatch.setenv("VELANTRIM_API_TOKEN", "s3cret")
    auth = {"Authorization": "Bearer s3cret"}
    for path in ("/review/queue", "/review/report", "/review/decisions"):
        assert client.get(path).status_code == 401
        assert client.get(
            path, headers={"Authorization": "Bearer wrong"}).status_code == 401
        assert client.get(path, headers=auth).status_code == 200
    assert client.get("/review/item/ing:x").status_code == 401
    assert client.post("/review/approve",
                       json={"fact_id": "ing:x"}).status_code == 401
    assert client.post("/review/reject",
                       json={"fact_id": "ing:x"}).status_code == 401
    # Memory endpoints are guarded too when the token is set.
    assert client.post("/ingest", json={"text": "hello"}).status_code == 401
    assert client.post("/ask", json={"query": "hello"}).status_code == 401
    assert client.get("/receipt", params={"q": "hello"}).status_code == 401
    assert client.post("/verify-receipt",
                       json={"receipt": {"digest": "x"}}).status_code == 401
    assert client.get("/evidence/ing:x").status_code == 401
    assert client.post("/ingest", json={"text": "hello"}, headers=auth).status_code == 200
    # Health and the static review shell stay public.
    assert client.get("/health").status_code == 200
    assert client.get("/review/ui").status_code == 200


def test_api_fails_closed_without_token_or_bypass(monkeypatch):
    """No token AND no local-dev bypass → guarded endpoints refuse with 401.
    The unconfigured service is not implicitly open."""
    monkeypatch.delenv("VELANTRIM_API_TOKEN", raising=False)
    monkeypatch.delenv("VELANTRIM_API_ALLOW_UNAUTH_LOCAL", raising=False)
    c = TestClient(api.create_app())
    assert c.post("/ingest", json={"text": "hello"}).status_code == 401
    assert c.post("/ask", json={"query": "hello"}).status_code == 401
    assert c.get("/review/queue").status_code == 401
    # Public surfaces stay reachable even when unconfigured.
    assert c.get("/health").status_code == 200
    assert c.get("/review/ui").status_code == 200


def test_api_correct_token_accepted(monkeypatch):
    monkeypatch.setenv("VELANTRIM_API_TOKEN", "s3cret")
    monkeypatch.delenv("VELANTRIM_API_ALLOW_UNAUTH_LOCAL", raising=False)
    c = TestClient(api.create_app())
    r = c.post("/ingest", json={"text": "hello"},
               headers={"Authorization": "Bearer s3cret"})
    assert r.status_code == 200


def test_api_wrong_token_rejected(monkeypatch):
    monkeypatch.setenv("VELANTRIM_API_TOKEN", "s3cret")
    c = TestClient(api.create_app())
    # Wrong token, and no token at all, are both rejected.
    assert c.post("/ingest", json={"text": "hello"},
                  headers={"Authorization": "Bearer wrong"}).status_code == 401
    assert c.post("/ingest", json={"text": "hello"}).status_code == 401


def test_api_unauth_local_bypass_accepted(monkeypatch):
    """With no token but VELANTRIM_API_ALLOW_UNAUTH_LOCAL=1, guarded endpoints
    are reachable without a bearer (explicit local-dev opt-in)."""
    monkeypatch.delenv("VELANTRIM_API_TOKEN", raising=False)
    monkeypatch.setenv("VELANTRIM_API_ALLOW_UNAUTH_LOCAL", "1")
    c = TestClient(api.create_app())
    assert c.post("/ingest", json={"text": "hello"}).status_code == 200


def test_ingest_rejects_oversized_text(client):
    assert client.post("/ingest", json={"text": "x" * 10_001}).status_code == 422


def test_ask_rejects_oversized_query(client):
    assert client.post("/ask", json={"query": "x" * 10_001}).status_code == 422


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


def test_review_ui_decision_card_distinguishes_restricted_from_erased():
    """No JS execution harness ships with this repo, so this is a targeted
    text-level check (mirroring test_review_ui_ships_as_package_data above):
    decisionCard() must check `restricted` before falling back to the erased
    "(fact erased)" placeholder, so a restricted decision never renders as
    if the fact had been erased (Codex P2 follow-up on #246)."""
    from importlib import resources
    html = resources.files("core").joinpath(
        "_webui/review.html").read_text(encoding="utf-8")
    assert "function decisionCard" in html
    body = html[html.index("function decisionCard"):html.index("function fill")]
    assert "(fact restricted)" in body
    assert "(fact erased)" in body
    assert "d.restricted" in body
    # The restricted check must be evaluated before the erased/null fallback.
    assert body.index("d.restricted") < body.index('"(fact erased)"')
