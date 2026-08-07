"""Public HTTP curator identity/capability wiring for issue #316."""
import pytest

fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient  # noqa: E402

from core import api  # noqa: E402


def _configured_client(monkeypatch, *, role="CURATOR", scopes="fact:*"):
    monkeypatch.setenv("VELANTRIM_API_TOKEN", "secret")
    monkeypatch.setenv("VELANTRIM_CURATOR_ACTOR", "alice")
    monkeypatch.setenv("VELANTRIM_CURATOR_ROLES", role)
    monkeypatch.setenv("VELANTRIM_CURATOR_SCOPES", scopes)
    return TestClient(api.create_app()), {"Authorization": "Bearer secret"}


def _explicit_local_client(monkeypatch):
    monkeypatch.delenv("VELANTRIM_API_TOKEN", raising=False)
    monkeypatch.setenv("VELANTRIM_API_ALLOW_UNAUTH_LOCAL", "1")
    return TestClient(api.create_app())


def test_token_without_principal_configuration_fails_curator_writes(monkeypatch):
    monkeypatch.setenv("VELANTRIM_API_TOKEN", "secret")
    client = TestClient(api.create_app())
    response = client.post(
        "/review/approve",
        headers={"Authorization": "Bearer secret"},
        json={"fact_id": "fact-1"},
    )
    assert response.status_code == 403
    assert "VELANTRIM_CURATOR_ACTOR" in response.json()["detail"]


def test_whitespace_token_configuration_fails_closed(monkeypatch):
    monkeypatch.setenv("VELANTRIM_API_TOKEN", "   ")
    monkeypatch.setenv("VELANTRIM_API_ALLOW_UNAUTH_LOCAL", "1")
    called = []
    monkeypatch.setattr(
        "core.curator_runtime.review.reject",
        lambda *args, **kwargs: called.append((args, kwargs)) or {"found": True},
    )
    client = TestClient(api.create_app())
    response = client.post(
        "/review/reject",
        headers={"Authorization": "Bearer    "},
        json={"fact_id": "fact-1", "reason": "noise"},
    )
    assert response.status_code == 401
    assert "configuration is invalid" in response.json()["detail"]
    assert not called


def test_actor_spoof_is_403_before_approve_mutation(monkeypatch):
    client, auth = _configured_client(monkeypatch)
    called = []
    monkeypatch.setattr(
        "core.curator_runtime.review.approve",
        lambda *args, **kwargs: called.append((args, kwargs)) or {"found": True},
    )
    response = client.post(
        "/review/approve",
        headers=auth,
        json={"fact_id": "fact-1", "actor": "mallory"},
    )
    assert response.status_code == 403
    assert not called


def test_http_audit_actor_is_derived_from_principal(monkeypatch):
    client, auth = _configured_client(monkeypatch)
    seen = {}

    def approve(fact_id, **kwargs):
        seen.update({"fact_id": fact_id, **kwargs})
        return {"found": True, "approved": True}

    monkeypatch.setattr("core.curator_runtime.review.approve", approve)
    response = client.post(
        "/review/approve",
        headers=auth,
        json={"fact_id": "fact-1"},
    )
    assert response.status_code == 200
    assert seen["actor"] == "alice"


def test_force_approval_requires_admin_but_not_duplicate_actor(monkeypatch):
    client, auth = _configured_client(monkeypatch, role="CURATOR")
    monkeypatch.setattr(
        "core.curator_runtime.review.approve",
        lambda *args, **kwargs: {"found": True, "approved": True},
    )
    denied = client.post(
        "/review/approve",
        headers=auth,
        json={"fact_id": "fact-1", "force": True, "reason": "override"},
    )
    assert denied.status_code == 403

    client_admin, auth_admin = _configured_client(monkeypatch, role="ADMIN")
    allowed = client_admin.post(
        "/review/approve",
        headers=auth_admin,
        json={"fact_id": "fact-1", "force": True, "reason": "override"},
    )
    assert allowed.status_code == 200


def test_reject_actor_spoof_is_rejected_before_mutation(monkeypatch):
    client, auth = _configured_client(monkeypatch)
    called = []
    monkeypatch.setattr(
        "core.curator_runtime.review.reject",
        lambda *args, **kwargs: called.append((args, kwargs)) or {"found": True},
    )
    response = client.post(
        "/review/reject",
        headers=auth,
        json={"fact_id": "fact-1", "actor": "mallory", "reason": "noise"},
    )
    assert response.status_code == 403
    assert not called


def test_reject_without_actor_uses_principal_identity(monkeypatch):
    client, auth = _configured_client(monkeypatch)
    seen = {}

    def reject(fact_id, **kwargs):
        seen.update({"fact_id": fact_id, **kwargs})
        return {"found": True, "rejected": True}

    monkeypatch.setattr("core.curator_runtime.review.reject", reject)
    response = client.post(
        "/review/reject",
        headers=auth,
        json={"fact_id": "fact-1", "reason": "noise"},
    )
    assert response.status_code == 200
    assert seen["actor"] == "alice"


def test_candidate_scope_denial_is_zero_mutation(monkeypatch):
    client, auth = _configured_client(monkeypatch, scopes="fact:other")
    called = []
    monkeypatch.setattr(
        "core.curator_runtime.review.reject",
        lambda *args, **kwargs: called.append((args, kwargs)) or {"found": True},
    )
    response = client.post(
        "/review/reject",
        headers=auth,
        json={"fact_id": "fact-1", "reason": "noise"},
    )
    assert response.status_code == 403
    assert not called


def test_bundled_conflict_route_is_registered_and_principal_guarded(monkeypatch):
    client, auth = _configured_client(monkeypatch, role="REVIEWER")
    monkeypatch.setattr(
        "core.curator_runtime.review.review_item",
        lambda _fid: {
            "found": True,
            "diagnosis": {"contradiction_report": {"report_id": "report-1"}},
        },
    )
    called = []
    monkeypatch.setattr(
        "core.curator_runtime.review.resolve_conflict",
        lambda *args, **kwargs: called.append((args, kwargs)) or {
            "found": True,
            "approved": True,
        },
    )
    allowed = client.post(
        "/review/resolve-conflict",
        headers=auth,
        json={
            "fact_id": "fact-1",
            "disposition": "COEXIST",
            "reason": "contexts",
            "expected_report_id": "report-1",
        },
    )
    assert allowed.status_code == 200
    assert called[0][1]["actor"] == "alice"

    denied = client.post(
        "/review/resolve-conflict",
        headers=auth,
        json={
            "fact_id": "fact-1",
            "disposition": "SUPERSEDE",
            "reason": "replace",
            "target_fact_ids": ["old"],
        },
    )
    assert denied.status_code == 403


def test_bundled_conflict_route_returns_404_for_unknown_fact(monkeypatch):
    client, auth = _configured_client(monkeypatch, role="REVIEWER")
    monkeypatch.setattr(
        "core.curator_runtime.review.review_item",
        lambda _fid: {"found": False},
    )
    response = client.post(
        "/review/resolve-conflict",
        headers=auth,
        json={
            "fact_id": "missing",
            "disposition": "COEXIST",
            "reason": "contexts",
        },
    )
    assert response.status_code == 404
    assert "unknown fact missing" in response.json()["detail"]


def test_explicit_local_mode_ignores_configured_curator_identity(monkeypatch):
    monkeypatch.setenv("VELANTRIM_CURATOR_ACTOR", "mallory")
    monkeypatch.setenv("VELANTRIM_CURATOR_ROLES", "REVIEWER")
    monkeypatch.setenv("VELANTRIM_CURATOR_SCOPES", "fact:other")
    seen = {}

    def reject(fact_id, **kwargs):
        seen.update({"fact_id": fact_id, **kwargs})
        return {"found": True, "rejected": True}

    monkeypatch.setattr("core.curator_runtime.review.reject", reject)
    client = _explicit_local_client(monkeypatch)
    response = client.post(
        "/review/reject",
        json={"fact_id": "fact-1", "actor": "mallory", "reason": "noise"},
    )
    assert response.status_code == 200
    assert seen["fact_id"] == "fact-1"
    assert seen["actor"] == "api-curator"


def test_explicit_local_force_requires_exact_synthetic_actor(monkeypatch):
    monkeypatch.setenv("VELANTRIM_CURATOR_ACTOR", "mallory")
    monkeypatch.setenv("VELANTRIM_CURATOR_ROLES", "ADMIN")
    monkeypatch.setenv("VELANTRIM_CURATOR_SCOPES", "fact:*")
    seen = {}

    def approve(fact_id, **kwargs):
        seen.update({"fact_id": fact_id, **kwargs})
        return {"found": True, "approved": True}

    monkeypatch.setattr("core.curator_runtime.review.approve", approve)
    client = _explicit_local_client(monkeypatch)
    wrong = client.post(
        "/review/approve",
        json={
            "fact_id": "fact-1",
            "actor": "mallory",
            "force": True,
            "reason": "override",
        },
    )
    assert wrong.status_code == 422
    assert not seen

    allowed = client.post(
        "/review/approve",
        json={
            "fact_id": "fact-1",
            "actor": "api-curator",
            "force": True,
            "reason": "override",
        },
    )
    assert allowed.status_code == 200
    assert seen["actor"] == "api-curator"
