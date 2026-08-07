"""Coverage for fail-closed curator surface refusal branches."""

import json

import pytest

from core import cli, conflict_surfaces
from core.curator_auth import CuratorPrincipal, CuratorRole
from core.curator_runtime import PrincipalConfigurationError


def test_cli_approve_fails_closed_without_principal_configuration(monkeypatch, capsys):
    monkeypatch.setattr(
        cli,
        "principal_from_environment",
        lambda: (_ for _ in ()).throw(
            PrincipalConfigurationError("VELANTRIM_CURATOR_ACTOR is required")
        ),
    )

    assert cli.main(["review-approve", "fact-1"]) == 2
    assert json.loads(capsys.readouterr().out) == {
        "authorized": False,
        "reason": "VELANTRIM_CURATOR_ACTOR is required",
    }


def test_conflict_http_maps_composer_validation_to_422(monkeypatch):
    fastapi = pytest.importorskip("fastapi")
    testclient = pytest.importorskip("fastapi.testclient")
    app = fastapi.FastAPI()
    principal = CuratorPrincipal(
        "alice",
        frozenset({CuratorRole.CURATOR}),
        frozenset({"fact:*"}),
    )

    conflict_surfaces.register_conflict_routes(
        app,
        principal_dependency=lambda: principal,
    )
    monkeypatch.setattr(
        conflict_surfaces,
        "resolve_conflict_payload",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(
            ValueError("synthetic validation refusal")
        ),
    )

    response = testclient.TestClient(app).post(
        "/review/resolve-conflict",
        json={
            "fact_id": "fact-1",
            "disposition": "COEXIST",
            "reason": "reviewed",
        },
    )

    assert response.status_code == 422
    assert response.json()["detail"] == "synthetic validation refusal"
