import json

import pytest

from core import conflict_surfaces
from core.curator_auth import CuratorPrincipal, CuratorRole


def _principal(actor="alice", role=CuratorRole.CURATOR, scopes=frozenset({"fact:*"})):
    return CuratorPrincipal(actor, frozenset({role}), scopes)


def test_payload_validates_and_delegates_through_principal(monkeypatch):
    seen = {}

    def fake_resolve(principal, fact_id, **kwargs):
        seen.update({"principal": principal, "fact_id": fact_id, **kwargs})
        return {"authorized": True, "approved": True, "fact_id": fact_id}

    monkeypatch.setattr(conflict_surfaces, "resolve_conflict_as_principal", fake_resolve)
    principal = _principal()
    result = conflict_surfaces.resolve_conflict_payload(
        principal,
        " fact-1 ",
        disposition="COEXIST",
        actor=" alice ",
        reason=" distinct contexts ",
        target_fact_ids=[" target-1 "],
        expected_report_id=" report-1 ",
    )
    assert result["approved"] is True
    assert seen == {
        "principal": principal,
        "fact_id": "fact-1",
        "disposition": "COEXIST",
        "requested_actor": "alice",
        "reason": "distinct contexts",
        "target_fact_ids": ("target-1",),
        "expected_report_id": "report-1",
    }


@pytest.mark.parametrize(
    "kwargs, message",
    [
        ({"fact_id": ""}, "fact_id"),
        ({"disposition": "WINNER"}, "disposition"),
        ({"disposition": "REVIEW_REQUIRED"}, "disposition"),
        ({"actor": " "}, "actor"),
        ({"reason": ""}, "reason"),
        ({"target_fact_ids": [""]}, "target_fact_ids"),
        ({"expected_report_id": ""}, "expected_report_id"),
    ],
)
def test_payload_rejects_malformed_public_inputs(kwargs, message):
    base = {
        "principal": _principal(),
        "fact_id": "fact-1",
        "disposition": "COEXIST",
        "actor": "alice",
        "reason": "reviewed",
    }
    base.update(kwargs)
    with pytest.raises(ValueError, match=message):
        conflict_surfaces.resolve_conflict_payload(**base)


def test_payload_requires_real_principal():
    with pytest.raises(ValueError, match="principal"):
        conflict_surfaces.resolve_conflict_payload(
            None,  # type: ignore[arg-type]
            "fact-1",
            disposition="COEXIST",
            reason="reviewed",
        )


def test_cli_uses_configured_principal(monkeypatch, capsys):
    principal = _principal()
    monkeypatch.setattr(
        conflict_surfaces,
        "principal_from_environment",
        lambda: principal,
    )
    monkeypatch.setattr(
        conflict_surfaces,
        "resolve_conflict_payload",
        lambda *args, **kwargs: {"authorized": True, "approved": True},
    )
    assert conflict_surfaces.main([
        "fact-1", "--disposition", "COEXIST", "--actor", "alice",
        "--reason", "reviewed",
    ]) == 0
    assert json.loads(capsys.readouterr().out)["approved"] is True


def test_cli_configuration_and_authorization_exit_codes(monkeypatch, capsys):
    monkeypatch.setattr(
        conflict_surfaces,
        "principal_from_environment",
        lambda: (_ for _ in ()).throw(ValueError("principal missing")),
    )
    assert conflict_surfaces.main([
        "fact-1", "--disposition", "COEXIST", "--reason", "reviewed",
    ]) == 2
    assert json.loads(capsys.readouterr().out) == {"error": "principal missing"}

    monkeypatch.setattr(conflict_surfaces, "principal_from_environment", lambda: _principal())
    monkeypatch.setattr(
        conflict_surfaces,
        "resolve_conflict_payload",
        lambda *args, **kwargs: {"authorized": False, "reason": "scope"},
    )
    assert conflict_surfaces.main([
        "fact-1", "--disposition", "COEXIST", "--reason", "reviewed",
    ]) == 3


def test_route_registration_requires_principal_dependency():
    class App:
        pass

    with pytest.raises(ValueError, match="principal"):
        conflict_surfaces.register_conflict_routes(App())


def test_http_route_derives_principal_and_rejects_spoof(monkeypatch):
    fastapi = pytest.importorskip("fastapi")
    testclient = pytest.importorskip("fastapi.testclient")
    app = fastapi.FastAPI()
    principal = _principal()

    def principal_dependency():
        return principal

    conflict_surfaces.register_conflict_routes(
        app, principal_dependency=principal_dependency
    )
    seen = {}

    def fake(principal_arg, fact_id, **kwargs):
        seen.update({"principal": principal_arg, "fact_id": fact_id, **kwargs})
        if kwargs.get("actor") == "mallory":
            return {"authorized": False, "reason": "actor does not match authenticated principal"}
        return {"authorized": True, "approved": True, "fact_id": fact_id}

    monkeypatch.setattr(conflict_surfaces, "resolve_conflict_payload", fake)
    client = testclient.TestClient(app)
    response = client.post("/review/resolve-conflict", json={
        "fact_id": "fact-1",
        "disposition": "COEXIST",
        "reason": "reviewed",
    })
    assert response.status_code == 200
    assert seen["principal"] is principal

    denied = client.post("/review/resolve-conflict", json={
        "fact_id": "fact-1",
        "disposition": "COEXIST",
        "actor": "mallory",
        "reason": "reviewed",
    })
    assert denied.status_code == 403


def test_explicit_local_route_ignores_configured_actor(monkeypatch):
    fastapi = pytest.importorskip("fastapi")
    testclient = pytest.importorskip("fastapi.testclient")
    monkeypatch.setenv("VELANTRIM_CURATOR_ACTOR", "mallory")
    monkeypatch.setenv("VELANTRIM_CURATOR_ROLES", "REVIEWER")
    monkeypatch.setenv("VELANTRIM_CURATOR_SCOPES", "fact:other")

    app = fastapi.FastAPI()
    conflict_surfaces.register_conflict_routes(app, allow_unguarded_local=True)
    seen = {}

    def fake(principal, fact_id, **kwargs):
        seen["principal"] = principal
        return {"authorized": True, "approved": True, "fact_id": fact_id}

    monkeypatch.setattr(conflict_surfaces, "resolve_conflict_payload", fake)
    client = testclient.TestClient(app)
    response = client.post("/review/resolve-conflict", json={
        "fact_id": "fact-1",
        "disposition": "COEXIST",
        "reason": "reviewed",
    })
    assert response.status_code == 200
    assert seen["principal"].actor_id == "api-curator"
    assert seen["principal"].roles == frozenset({CuratorRole.ADMIN})
    assert seen["principal"].scopes == frozenset({"fact:*"})
