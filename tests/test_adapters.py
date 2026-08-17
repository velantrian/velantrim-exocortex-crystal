"""Tests for external-ingestion format adapters (core/adapters.py, WP4)."""
import sys
import types

import pytest

from core import adapters, knowledge, imports


# ─── N-Triples (dependency-free RDF) ──────────────────────────────────────────

def test_ntriples_uris_literals_blank_and_comments():
    nt = (
        "# a comment line\n"
        "<http://ex.org/Earth> <http://ex.org/orbits> <http://ex.org/Sun> .\n"
        '<http://ex.org/Water> <http://ex.org/boilsAt> "100 C"@en .\n'
        "_:b1 <http://ex.org/type> <http://ex.org/Planet> .\n"
        "garbage line without a period\n"
    )
    out = adapters.extract_ntriples(nt)
    claims = [c["claim"] for c in out]
    assert claims == [
        "Earth orbits Sun",
        "Water boilsAt 100 C",
        "b1 type Planet",
    ]


def test_ntriples_empty():
    assert adapters.extract_ntriples("\n  \n# only comments\n") == []


def test_local_name_variants():
    assert adapters._local_name("<http://ex.org/path/Name>") == "Name"
    assert adapters._local_name("<http://ex.org#Frag>") == "Frag"
    assert adapters._local_name("_:blank1") == "blank1"
    assert adapters._local_name("bareTerm") == "bareTerm"      # fallback


def test_extract_claims_dispatches_nt():
    out = knowledge.extract_claims(
        "<http://x/A> <http://x/is> <http://x/B> .\n", "nt")
    assert out == [{"claim": "A is B"}]


def test_ingest_file_nt_through_truthgate(tmp_path):
    p = tmp_path / "facts.nt"
    p.write_text("<http://ex/Mars> <http://ex/isA> <http://ex/Planet> .\n",
                 encoding="utf-8")
    rep = knowledge.ingest_file(str(p))
    assert rep["accepted"] == 1
    from core.memory import get_fact
    assert get_fact(rep["fact_ids"][0])["claim"] == "Mars isA Planet"


def test_dry_run_nt(tmp_path):
    p = tmp_path / "facts.nt"
    p.write_text("<http://ex/Sun> <http://ex/isA> <http://ex/Star> .\n",
                 encoding="utf-8")
    rep = imports.dry_run_file(str(p))
    assert rep["dry_run"] is True and rep["total"] == 1


# ─── Optional-dependency loader ───────────────────────────────────────────────

def test_require_missing_raises_clear_error():
    with pytest.raises(ImportError, match=r"pip install '\.\[demo\]'"):
        adapters._require("velantrim_missing_module_xyz", "demo")


def test_require_returns_present_module():
    assert adapters._require("json", "x").__name__ == "json"


# ─── YAML adapter (optional; injected fake module) ────────────────────────────

def test_extract_yaml_with_injected_module(monkeypatch):
    fake = types.ModuleType("yaml")
    fake.safe_load = lambda content: ["The sky is blue", "Grass is green"]
    monkeypatch.setitem(sys.modules, "yaml", fake)
    out = adapters.extract_yaml("ignored: content")
    assert [c["claim"] for c in out] == ["The sky is blue", "Grass is green"]


def test_yaml_not_installed(monkeypatch):
    monkeypatch.setitem(sys.modules, "yaml", None)   # force ImportError
    with pytest.raises(ImportError, match=r"\[yaml\]"):
        adapters.extract_yaml("x: 1")


def test_ingest_file_yaml_via_fake(tmp_path, monkeypatch):
    fake = types.ModuleType("yaml")
    fake.safe_load = lambda content: {"claims": ["Copper conducts electricity"]}
    monkeypatch.setitem(sys.modules, "yaml", fake)
    p = tmp_path / "kb.yaml"
    p.write_text("claims:\n  - Copper conducts electricity\n", encoding="utf-8")
    rep = knowledge.ingest_file(str(p))
    assert rep["accepted"] == 1


# ─── PDF adapter (optional; injected fake module) ─────────────────────────────

class _FakePage:
    def __init__(self, text):
        self._text = text

    def extract_text(self):
        return self._text


class _FakeReader:
    def __init__(self, path):
        self.pages = [_FakePage("Gravity attracts mass"),
                      _FakePage("Energy is conserved")]


def _fake_pypdf():
    mod = types.ModuleType("pypdf")
    mod.PdfReader = _FakeReader
    return mod


def test_extract_pdf_text_with_injected_module(monkeypatch):
    monkeypatch.setitem(sys.modules, "pypdf", _fake_pypdf())
    text = adapters.extract_pdf_text("whatever.pdf")
    assert "Gravity attracts mass" in text and "Energy is conserved" in text


def test_ingest_file_pdf_via_fake(tmp_path, monkeypatch):
    monkeypatch.setitem(sys.modules, "pypdf", _fake_pypdf())
    p = tmp_path / "doc.pdf"
    p.write_bytes(b"%PDF-1.4 fake")     # content ignored (reader is faked)
    rep = knowledge.ingest_file(str(p), source="paper")
    assert rep["accepted"] == 2         # two lines → two facts
    assert rep["source"] == "paper"


def test_pdf_not_installed(monkeypatch, tmp_path):
    monkeypatch.setitem(sys.modules, "pypdf", None)
    p = tmp_path / "doc.pdf"
    p.write_bytes(b"%PDF fake")
    with pytest.raises(ImportError, match=r"\[pdf\]"):
        knowledge.ingest_file(str(p))
