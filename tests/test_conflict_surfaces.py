import json

import pytest

from core import conflict_surfaces


def test_payload_validates_and_delegates(monkeypatch):
    seen = {}

    def fake_resolve(fact_id, **kwargs):
        seen.update({"fact_id": fact_id, **kwargs})
        return {"approved": True, "fact_id": fact_id}

    monkeypatch.setattr(conflict_surfaces.review, "resolve_conflict", fake_resolve)
    result = conflict_surfaces.resolve_conflict_payload(
        " fact-1 ",
        disposition="COEXIST",
        actor=" alice ",
        reason=" distinct contexts ",
        target_fact_ids=["target-1"],
        expected_report_id="report-1",
    )
    assert result["approved"] is True
    assert seen == {
        "fact_id": "fact-1",
        "disposition": "COEXIST",
        "actor": "alice",
        "reason": "distinct contexts",
        "target_fact_ids": ("target-1",),
        "expected_report_id": "report-1",
    }


@pytest.mark.parametrize(
    "kwargs, message",
    [
        ({"fact_id": ""}, "fact_id"),
        ({"disposition": "WINNER"}, "disposition"),
        ({"actor": " "}, "actor"),
        ({"reason": ""}, "reason"),
        ({"target_fact_ids": [""]}, "target_fact_ids"),
        ({"expected_report_id": ""}, "expected_report_id"),
    ],
)
def test_payload_rejects_malformed_public_inputs(kwargs, message):
    base = {
        "fact_id": "fact-1",
        "disposition": "COEXIST",
        "actor": "alice",
        "reason": "reviewed",
    }
    base.update(kwargs)
    with pytest.raises(ValueError, match=message):
        conflict_surfaces.resolve_conflict_payload(**base)


def test_cli_success_and_fail_closed_exit_codes(monkeypatch, capsys):
    monkeypatch.setattr(
        conflict_surfaces,
        "resolve_conflict_payload",
        lambda *args, **kwargs: {"approved": True, "fact_id": "fact-1"},
    )
    assert conflict_surfaces.main([
        "fact-1", "--disposition", "COEXIST", "--actor", "alice",
        "--reason", "reviewed",
    ]) == 0
    assert json.loads(capsys.readouterr().out)["approved"] is True

    monkeypatch.setattr(
        conflict_surfaces,
        "resolve_conflict_payload",
        lambda *args, **kwargs: {"approved": False, "reason": "STALE"},
    )
    assert conflict_surfaces.main([
        "fact-1", "--disposition", "SUPERSEDE", "--actor", "alice",
        "--reason", "reviewed", "--target", "old-1",
    ]) == 1


def test_cli_validation_error_is_json(monkeypatch, capsys):
    def fail(*args, **kwargs):
        raise ValueError("bad payload")

    monkeypatch.setattr(conflict_surfaces, "resolve_conflict_payload", fail)
    assert conflict_surfaces.main([
        "fact-1", "--disposition", "COEXIST", "--actor", "alice",
        "--reason", "reviewed",
    ]) == 2
    assert json.loads(capsys.readouterr().out) == {"error": "bad payload"}


def test_route_registration_requires_guard():
    class App:
        pass

    with pytest.raises(ValueError, match="authentication"):
        conflict_surfaces.register_conflict_routes(App())


def test_http_route_success_and_validation(monkeypatch):
    fastapi = pytest.importorskip("fastapi")
    testclient = pytest.importorskip("fastapi.testclient")
    app = fastapi.FastAPI()
    conflict_surfaces.register_conflict_routes(app, allow_unguarded_local=True)

    monkeypatch.setattr(
        conflict_surfaces,
        "resolve_conflict_payload",
        lambda *args, **kwargs: {"approved": True, "fact_id": kwargs.get("fact_id", args[0])},
    )
    client = testclient.TestClient(app)
    response = client.post("/review/resolve-conflict", json={
        "fact_id": "fact-1",
        "disposition": "COEXIST",
        "actor": "alice",
        "reason": "reviewed",
    })
    assert response.status_code == 200
    assert response.json()["approved"] is True

    monkeypatch.setattr(
        conflict_surfaces,
        "resolve_conflict_payload",
        lambda *args, **kwargs: (_ for _ in ()).throw(ValueError("bad decision")),
    )
    response = client.post("/review/resolve-conflict", json={
        "fact_id": "fact-1",
        "disposition": "COEXIST",
        "actor": "alice",
        "reason": "reviewed",
    })
    assert response.status_code == 422
    assert response.json()["detail"] == "bad decision"
