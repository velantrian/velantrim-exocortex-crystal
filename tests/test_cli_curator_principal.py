"""CLI curator writes must use configured principal capability and scope checks."""

import json

from core import cli
from core.curator_auth import CuratorPrincipal, CuratorRole
from core.curator_runtime import PrincipalConfigurationError


def _principal(
    role: CuratorRole = CuratorRole.CURATOR,
    scopes: frozenset[str] = frozenset({"fact:*"}),
) -> CuratorPrincipal:
    return CuratorPrincipal("alice", frozenset({role}), scopes)


def _last_json(capsys) -> dict:
    lines = [line for line in capsys.readouterr().out.splitlines() if line.strip()]
    return json.loads(lines[-1])


def test_cli_curator_write_fails_closed_without_principal_configuration(
    monkeypatch, capsys
):
    called = []
    monkeypatch.setattr(
        cli,
        "principal_from_environment",
        lambda: (_ for _ in ()).throw(
            PrincipalConfigurationError("VELANTRIM_CURATOR_ACTOR is required")
        ),
    )
    monkeypatch.setattr(
        "core.curator_runtime.review.reject",
        lambda *args, **kwargs: called.append((args, kwargs)),
    )

    code = cli.main(["review-reject", "fact-1", "--reason", "noise"])

    assert code == 2
    assert called == []
    assert _last_json(capsys) == {
        "authorized": False,
        "reason": "VELANTRIM_CURATOR_ACTOR is required",
    }


def test_cli_actor_spoof_is_denied_before_mutation(monkeypatch, capsys):
    called = []
    monkeypatch.setattr(cli, "principal_from_environment", lambda: _principal())
    monkeypatch.setattr(
        "core.curator_runtime.review.reject",
        lambda *args, **kwargs: called.append((args, kwargs)),
    )

    code = cli.main(
        [
            "review-reject",
            "fact-1",
            "--actor",
            "mallory",
            "--reason",
            "noise",
        ]
    )

    assert code == 3
    assert called == []
    result = _last_json(capsys)
    assert result["authorized"] is False
    assert result["reason"] == "actor does not match authenticated principal"


def test_cli_approve_and_reject_derive_audit_actor_from_principal(
    monkeypatch, capsys
):
    seen = []
    monkeypatch.setattr(cli, "principal_from_environment", lambda: _principal())
    monkeypatch.setattr(
        "core.curator_runtime.review.approve",
        lambda fact_id, **kwargs: seen.append(("approve", fact_id, kwargs))
        or {"found": True, "approved": True},
    )
    monkeypatch.setattr(
        "core.curator_runtime.review.reject",
        lambda fact_id, **kwargs: seen.append(("reject", fact_id, kwargs))
        or {"found": True, "rejected": True},
    )

    approve_code = cli.main(["review-approve", " fact-1 "])
    approve_result = _last_json(capsys)
    reject_code = cli.main(["review-reject", "\tfact-1\n", "--reason", "noise"])
    reject_result = _last_json(capsys)

    assert approve_code == 0
    assert reject_code == 0
    assert approve_result["authorized"] is True
    assert reject_result["authorized"] is True
    assert seen[0][0:2] == ("approve", "fact-1")
    assert seen[1][0:2] == ("reject", "fact-1")
    assert seen[0][2]["actor"] == "alice"
    assert seen[1][2]["actor"] == "alice"


def test_cli_scope_denial_is_zero_mutation(monkeypatch, capsys):
    called = []
    monkeypatch.setattr(
        cli,
        "principal_from_environment",
        lambda: _principal(scopes=frozenset({"fact:other"})),
    )
    monkeypatch.setattr(
        "core.curator_runtime.review.approve",
        lambda *args, **kwargs: called.append((args, kwargs)),
    )

    code = cli.main(["review-approve", "fact-1"])

    assert code == 3
    assert called == []
    result = _last_json(capsys)
    assert result["authorized"] is False
    assert result["reason"] == "candidate fact is outside principal scope"


def test_cli_force_approval_requires_admin_capability(monkeypatch, capsys):
    called = []
    monkeypatch.setattr(
        "core.curator_runtime.review.approve",
        lambda fact_id, **kwargs: called.append((fact_id, kwargs))
        or {"found": True, "approved": True},
    )

    monkeypatch.setattr(
        cli,
        "principal_from_environment",
        lambda: _principal(CuratorRole.CURATOR),
    )
    denied_code = cli.main(
        ["review-approve", "fact-1", "--force", "--reason", "override"]
    )
    denied = _last_json(capsys)
    assert denied_code == 3
    assert denied["authorized"] is False
    assert called == []

    monkeypatch.setattr(
        cli,
        "principal_from_environment",
        lambda: _principal(CuratorRole.ADMIN),
    )
    allowed_code = cli.main(
        ["review-approve", "fact-1", "--force", "--reason", "override"]
    )
    allowed = _last_json(capsys)
    assert allowed_code == 0
    assert allowed["authorized"] is True
    assert called[0][0] == "fact-1"
    assert called[0][1]["actor"] == "alice"
    assert called[0][1]["force"] is True
