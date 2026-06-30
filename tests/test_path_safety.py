"""Tests for core/path_safety.py — ingest path sandboxing."""
import os

import pytest
from pathlib import Path

from core.path_safety import resolve_safe_path, ingest_base_dir


def test_resolve_safe_path_accepts_file_under_base(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    f = tmp_path / "notes.txt"
    f.write_text("hello", encoding="utf-8")
    assert resolve_safe_path("notes.txt") == f.resolve()


def test_resolve_safe_path_rejects_parent_traversal(tmp_path, monkeypatch):
    (tmp_path / "work").mkdir(parents=True)
    monkeypatch.chdir(tmp_path / "work")
    secret = tmp_path / "secret.txt"
    secret.write_text("nope", encoding="utf-8")
    with pytest.raises(ValueError, match="escapes working directory"):
        resolve_safe_path("../secret.txt")


def test_resolve_safe_path_honours_velantrim_ingest_base(tmp_path, monkeypatch):
    base = tmp_path / "allowed"
    base.mkdir()
    f = base / "ok.json"
    f.write_text("[]", encoding="utf-8")
    monkeypatch.setenv("VELANTRIM_INGEST_BASE", str(base))
    assert ingest_base_dir() == base.resolve()
    assert resolve_safe_path("ok.json") == f.resolve()
    outside = tmp_path / "outside.txt"
    outside.write_text("x", encoding="utf-8")
    with pytest.raises(ValueError, match="escapes ingest base"):
        resolve_safe_path(str(outside))


def test_resolve_safe_path_missing_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with pytest.raises(FileNotFoundError):
        resolve_safe_path("missing.txt")


def test_resolve_safe_path_rejects_empty_path():
    with pytest.raises(ValueError, match="non-empty"):
        resolve_safe_path("")
    with pytest.raises(ValueError, match="non-empty"):
        resolve_safe_path("   ")


def test_ingest_base_dir_defaults_to_cwd(monkeypatch):
    monkeypatch.delenv("VELANTRIM_INGEST_BASE", raising=False)
    assert ingest_base_dir() == Path.cwd().resolve()
