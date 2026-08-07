from __future__ import annotations

import json

from core import storage_ops as ops


def test_logical_cli_dispatch(monkeypatch, capsys):
    monkeypatch.setattr(
        ops,
        "export_sqlite_logical",
        lambda *args, **kwargs: {"status": "PASS", "kind": "export"},
    )
    assert ops.main(["export-logical", "bundle", "--profile", "profile.json"]) == 0
    assert json.loads(capsys.readouterr().out)["kind"] == "export"

    monkeypatch.setattr(
        ops,
        "verify_logical_export",
        lambda *args, **kwargs: {"status": "PASS", "kind": "verify-logical"},
    )
    assert ops.main(["verify-logical", "bundle"]) == 0
    assert json.loads(capsys.readouterr().out)["kind"] == "verify-logical"
