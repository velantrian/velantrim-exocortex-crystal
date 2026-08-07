"""Read-only Crystal deployment-doctor tests."""

import json

import pytest

from core import backend_profiles as profiles
from core import doctor


def _write_profile(backend, configuration):
    profile = profiles._build_profile(backend, configuration)
    return profiles._persist_profile_if_absent(
        profile,
        profiles.storage_profile_path(),
    )


def test_doctor_passes_for_locked_existing_sqlite(monkeypatch, tmp_path):
    data_path = tmp_path / "l3.db"
    data_path.write_bytes(b"sqlite")
    _write_profile("sqlite", {"path": str(data_path.resolve())})
    monkeypatch.setenv("VELANTRIM_L3_BACKEND", "auto")

    report = doctor.doctor_report()

    assert report["status"] == "PASS"
    assert report["exit_code"] == 0
    assert report["locked_backend"] == "sqlite"
    assert {check["status"] for check in report["checks"]} == {"PASS"}


def test_doctor_warns_before_initialization_and_for_explicit_mock(monkeypatch):
    monkeypatch.setenv("VELANTRIM_L3_BACKEND", "auto")
    report = doctor.doctor_report()
    assert report["status"] == "WARN"
    assert "first successful durable startup" in report["checks"][0]["message"]

    monkeypatch.setenv("VELANTRIM_L3_BACKEND", "mock")
    report = doctor.doctor_report()
    assert report["status"] == "WARN"
    assert "ephemeral" in report["checks"][0]["message"]


def test_doctor_fails_for_invalid_profile_path(monkeypatch):
    monkeypatch.setenv("VELANTRIM_STORAGE_PROFILE_PATH", " ")
    report = doctor.doctor_report()
    assert report["status"] == "FAIL"
    assert report["profile_path"] is None
    assert report["exit_code"] == 2


def test_doctor_fails_for_malformed_profile():
    path = profiles.storage_profile_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("{", encoding="utf-8")

    report = doctor.doctor_report()

    assert report["status"] == "FAIL"
    assert report["locked_backend"] is None
    assert report["checks"][0]["id"] == "profile_integrity"


def test_doctor_reports_backend_mismatch(monkeypatch, tmp_path):
    data_path = tmp_path / "l3.db"
    data_path.write_bytes(b"sqlite")
    _write_profile("sqlite", {"path": str(data_path.resolve())})
    monkeypatch.setenv("VELANTRIM_L3_BACKEND", "ladybug")

    report = doctor.doctor_report()

    assert report["status"] == "FAIL"
    backend_check = next(
        check for check in report["checks"] if check["id"] == "backend_lock"
    )
    assert backend_check["status"] == "FAIL"


def test_doctor_fails_when_optional_dependency_is_unavailable(
    monkeypatch, tmp_path
):
    data_path = tmp_path / "l3.lbug"
    _write_profile("ladybug", {"path": str(data_path.resolve())})
    monkeypatch.setenv("VELANTRIM_L3_BACKEND", "auto")
    monkeypatch.setattr(doctor.importlib.util, "find_spec", lambda package: None)

    report = doctor.doctor_report()

    assert report["status"] == "FAIL"
    dependency = next(
        check for check in report["checks"] if check["id"] == "backend_dependency"
    )
    assert dependency["status"] == "FAIL"
    instance = next(
        check for check in report["checks"] if check["id"] == "storage_instance"
    )
    assert instance["status"] == "WARN"


def test_doctor_passes_for_locked_neo4j_locator(monkeypatch):
    _write_profile(
        "neo4j",
        {"uri": "bolt://db:7687", "database": "crystal"},
    )
    monkeypatch.setenv("VELANTRIM_L3_BACKEND", "auto")
    monkeypatch.setattr(
        doctor.importlib.util,
        "find_spec",
        lambda package: object(),
    )

    report = doctor.doctor_report()

    assert report["status"] == "PASS"
    instance = next(
        check for check in report["checks"] if check["id"] == "storage_instance"
    )
    assert instance["uri"] == "bolt://db:7687"
    assert instance["database"] == "crystal"


def test_doctor_fails_for_missing_storage_directory(monkeypatch, tmp_path):
    missing_path = tmp_path / "missing" / "l3.db"
    _write_profile("sqlite", {"path": str(missing_path.resolve())})
    monkeypatch.setenv("VELANTRIM_L3_BACKEND", "auto")

    report = doctor.doctor_report()

    assert report["status"] == "FAIL"
    directory = next(
        check for check in report["checks"] if check["id"] == "storage_directory"
    )
    assert directory["status"] == "FAIL"


def test_dependency_helper_covers_builtin_optional_and_unknown(monkeypatch):
    assert doctor._dependency_available("sqlite")
    assert doctor._dependency_available("mock")

    monkeypatch.setattr(
        doctor.importlib.util,
        "find_spec",
        lambda package: object() if package == "neo4j" else None,
    )
    assert doctor._dependency_available("neo4j")
    assert not doctor._dependency_available("ladybug")
    assert not doctor._dependency_available("unknown")


def test_overall_status_precedence():
    assert doctor._overall_status([{"status": "PASS"}]) == "PASS"
    assert doctor._overall_status([{"status": "WARN"}]) == "WARN"
    assert doctor._overall_status(
        [{"status": "WARN"}, {"status": "FAIL"}]
    ) == "FAIL"


def test_doctor_main_prints_json_and_rejects_arguments(
    monkeypatch, capsys, tmp_path
):
    data_path = tmp_path / "l3.db"
    data_path.write_bytes(b"sqlite")
    _write_profile("sqlite", {"path": str(data_path.resolve())})
    monkeypatch.setenv("VELANTRIM_L3_BACKEND", "auto")

    assert doctor.main([]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["status"] == "PASS"

    monkeypatch.setattr(doctor.sys, "argv", ["velantrim-doctor"])
    assert doctor.main() == 0
    capsys.readouterr()

    with pytest.raises(SystemExit, match="accepts no arguments"):
        doctor.main(["unexpected"])


def test_doctor_reports_locked_locator_conflict(monkeypatch, tmp_path):
    data_path = tmp_path / "l3.db"
    data_path.write_bytes(b"sqlite")
    _write_profile("sqlite", {"path": str(data_path.resolve())})
    monkeypatch.setenv("VELANTRIM_L3_BACKEND", "auto")
    monkeypatch.setenv("VELANTRIM_L3_PATH", str(tmp_path / "other.db"))

    report = doctor.doctor_report()

    assert report["status"] == "FAIL"
    backend_check = next(
        check for check in report["checks"] if check["id"] == "backend_lock"
    )
    assert "L3_PATH conflicts" in backend_check["message"]
