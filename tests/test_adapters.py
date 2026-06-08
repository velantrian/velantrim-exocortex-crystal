"""Tests for WP4 optional knowledge adapters (core/adapters/).

YAML and PDF and RDF tests are skipped when their optional deps are absent so
the core CI (no extras) stays green. Each test installs and exercises the real
adapter pipeline: extract → ingest_file → TruthGate → canon.
"""
from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any, Dict, List

import pytest

from core.adapters import known_extensions, load as _load_adapter, get as _get_adapter


# ─── Registry / auto-load API ─────────────────────────────────────────────────

def test_known_extensions_includes_expected():
    exts = known_extensions()
    for e in (".yaml", ".yml", ".pdf", ".ttl", ".n3", ".nt", ".rdf", ".owl"):
        assert e in exts


def test_load_unknown_extension_raises_value_error():
    with pytest.raises(ValueError, match="No adapter registered"):
        _load_adapter("docx")


def test_get_unregistered_returns_none():
    assert _get_adapter("docx") is None


# ─── YAML adapter ─────────────────────────────────────────────────────────────

yaml = pytest.importorskip("yaml", reason="pyyaml not installed — skip YAML adapter tests")


def test_yaml_adapter_registers_on_import():
    import core.adapters.yaml_adapter  # noqa: F401
    assert _get_adapter("yaml") is not None
    assert _get_adapter("yml") is not None


def _write_yaml(tmp: Path, content: str) -> str:
    p = tmp / "facts.yaml"
    p.write_text(content, encoding="utf-8")
    return str(p)


def test_yaml_list_of_strings(tmp_path, monkeypatch):
    _reset_env(monkeypatch)
    path = _write_yaml(tmp_path, "- Water boils at 100 degrees\n- Gold is a metal\n")
    from core.adapters.yaml_adapter import extract_yaml_claims
    claims = extract_yaml_claims(path)
    assert len(claims) == 2
    assert claims[0]["claim"] == "Water boils at 100 degrees"


def test_yaml_list_of_dicts(tmp_path, monkeypatch):
    _reset_env(monkeypatch)
    path = _write_yaml(
        tmp_path,
        "- claim: The sky is blue\n  confidence: 0.95\n"
        "- claim: Pi is approximately 3.14\n  claim_type: WORLD_FACT\n",
    )
    from core.adapters.yaml_adapter import extract_yaml_claims
    claims = extract_yaml_claims(path)
    assert claims[0]["confidence"] == 0.95
    assert claims[1]["claim_type"] == "WORLD_FACT"


def test_yaml_dict_with_claims_key(tmp_path, monkeypatch):
    _reset_env(monkeypatch)
    path = _write_yaml(tmp_path,
                       "description: physics facts\nclaims:\n  - Light travels fast\n")
    from core.adapters.yaml_adapter import extract_yaml_claims
    claims = extract_yaml_claims(path)
    assert len(claims) == 1
    assert "Light" in claims[0]["claim"]


def test_yaml_empty_file(tmp_path):
    path = tmp_path / "empty.yaml"
    path.write_text("", encoding="utf-8")
    from core.adapters.yaml_adapter import extract_yaml_claims
    assert extract_yaml_claims(str(path)) == []


def test_yaml_ingest_file_roundtrip(tmp_path, monkeypatch):
    _reset_env(monkeypatch)
    path = _write_yaml(tmp_path, "- Vienna is the capital of Austria\n")
    from core import knowledge
    rep = knowledge.ingest_file(str(path))
    assert rep["accepted"] >= 1
    assert rep["source"] == "facts.yaml"


def test_yaml_dry_run_file(tmp_path, monkeypatch):
    _reset_env(monkeypatch)
    path = _write_yaml(tmp_path, "- Jupiter is the largest planet\n")
    from core import imports
    rep = imports.dry_run_file(str(path))
    assert rep["dry_run"] is True
    assert rep["total"] >= 1


# ─── PDF adapter ──────────────────────────────────────────────────────────────

pypdf = pytest.importorskip("pypdf", reason="pypdf not installed — skip PDF adapter tests")


def _make_blank_pdf(tmp: Path) -> str:
    """Create a valid blank-page PDF using pypdf's PdfWriter."""
    import io
    from pypdf import PdfWriter
    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)
    buf = io.BytesIO()
    writer.write(buf)
    path = tmp / "test.pdf"
    path.write_bytes(buf.getvalue())
    return str(path)


def test_pdf_adapter_registers_on_import():
    import core.adapters.pdf_adapter  # noqa: F401
    assert _get_adapter("pdf") is not None


def test_pdf_extract_returns_claims(tmp_path):
    import core.adapters.pdf_adapter  # noqa: F401
    from core.adapters.pdf_adapter import extract_pdf_claims
    # A blank-page PDF has no text; adapter must return an empty list, not crash.
    path = _make_blank_pdf(tmp_path)
    claims = extract_pdf_claims(path)
    assert isinstance(claims, list)


def test_pdf_ingest_file_accepts_extension(tmp_path, monkeypatch):
    _reset_env(monkeypatch)
    import core.adapters.pdf_adapter  # noqa: F401
    path = _make_blank_pdf(tmp_path)
    from core import knowledge
    # Should not raise on .pdf extension; blank page → 0 accepted is fine.
    rep = knowledge.ingest_file(path)
    assert "accepted" in rep


# ─── RDF adapter ──────────────────────────────────────────────────────────────

rdflib = pytest.importorskip("rdflib", reason="rdflib not installed — skip RDF adapter tests")


def test_rdf_adapter_registers_on_import():
    import core.adapters.rdf_adapter  # noqa: F401
    for ext in ("ttl", "n3", "nt", "rdf", "owl"):
        assert _get_adapter(ext) is not None


_TURTLE = """\
@prefix ex: <http://example.org/> .
@prefix schema: <http://schema.org/> .

ex:Einstein a schema:Person ;
    schema:name "Albert Einstein" ;
    schema:birthPlace ex:Ulm .

ex:Ulm a schema:City ;
    schema:country ex:Germany .
"""


def test_rdf_extract_turtle(tmp_path):
    import core.adapters.rdf_adapter  # noqa: F401
    from core.adapters.rdf_adapter import extract_rdf_claims
    ttl = tmp_path / "facts.ttl"
    ttl.write_text(_TURTLE, encoding="utf-8")
    claims = extract_rdf_claims(str(ttl))
    assert len(claims) >= 3
    texts = [c["claim"] for c in claims]
    assert any("einstein" in t for t in texts)


def test_rdf_skips_blank_node_subjects(tmp_path):
    import core.adapters.rdf_adapter  # noqa: F401
    from core.adapters.rdf_adapter import extract_rdf_claims
    nt = tmp_path / "blank.nt"
    nt.write_text(
        "_:b0 <http://schema.org/name> \"Unnamed\" .\n"
        "<http://example.org/Known> <http://schema.org/name> \"Known\" .\n",
        encoding="utf-8",
    )
    claims = extract_rdf_claims(str(nt))
    texts = [c["claim"] for c in claims]
    assert all("unnamed" not in t.lower() for t in texts)
    assert any("known" in t.lower() for t in texts)


def test_rdf_ingest_file_turtle(tmp_path, monkeypatch):
    _reset_env(monkeypatch)
    import core.adapters.rdf_adapter  # noqa: F401
    ttl = tmp_path / "kb.ttl"
    ttl.write_text(_TURTLE, encoding="utf-8")
    from core import knowledge
    rep = knowledge.ingest_file(str(ttl))
    assert "accepted" in rep
    assert rep["source"] == "kb.ttl"


def test_rdf_dry_run_file(tmp_path, monkeypatch):
    _reset_env(monkeypatch)
    import core.adapters.rdf_adapter  # noqa: F401
    ttl = tmp_path / "kb.ttl"
    ttl.write_text(_TURTLE, encoding="utf-8")
    from core import imports
    rep = imports.dry_run_file(str(ttl))
    assert rep["dry_run"] is True
    assert rep["total"] >= 3


# ─── CLI integration ──────────────────────────────────────────────────────────

def test_cli_learn_yaml(tmp_path, monkeypatch):
    yaml = pytest.importorskip("yaml")
    _reset_env(monkeypatch)
    path = tmp_path / "facts.yaml"
    path.write_text("- Saturn has rings\n", encoding="utf-8")
    import core.adapters.yaml_adapter  # noqa: F401
    from core.cli import main
    rc = main(["learn", str(path)])
    assert rc == 0


def test_cli_learn_unsupported_raises(tmp_path, monkeypatch):
    _reset_env(monkeypatch)
    path = tmp_path / "doc.docx"
    path.write_bytes(b"not a real docx")
    from core.cli import main
    with pytest.raises((ValueError, SystemExit)):
        main(["learn", str(path)])


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _reset_env(monkeypatch) -> None:
    """Point the stores at a throwaway temp dir (mirrors eval_gate isolation)."""
    tmp = tempfile.mkdtemp(prefix="velantrim-test-adapters-")
    monkeypatch.setenv("VELANTRIM_L3_PATH", str(Path(tmp) / "l3.db"))
    monkeypatch.setenv("VELANTRIM_DB", str(Path(tmp) / "l1.db"))
    monkeypatch.delenv("VELANTRIM_NEUROCORE", raising=False)
    # Reset the in-process singleton so each test gets a clean L1.
    import core.memory as _mem
    if hasattr(_mem, "_CONN"):
        try:
            _mem._CONN.close()
        except Exception:
            pass
        _mem._CONN = None  # type: ignore[assignment]
