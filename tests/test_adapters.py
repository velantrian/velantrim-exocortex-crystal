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


# ─── BibTeX adapter ───────────────────────────────────────────────────────────
# No optional dep — bibtex adapter is stdlib-only; no importorskip needed.

def test_bibtex_adapter_registers_on_import():
    import core.adapters.bibtex_adapter  # noqa: F401
    assert _get_adapter("bib") is not None


_BIB_TWO_ENTRIES = """\
@article{einstein1905,
  title = {On the Electrodynamics of Moving Bodies},
  author = {Albert Einstein},
  year = {1905},
  abstract = {This paper introduces the special theory of relativity.}
}
@book{darwin1859,
  title = {On the Origin of Species},
  author = {Charles Darwin},
  year = {1859}
}
"""

_BIB_ALL_CITATION_FORMS = """\
@article{authoronly,
  title = {A Paper With Author Only},
  author = {Some Author}
}
@article{yearonly,
  title = {A Paper With Year Only},
  year = {2000}
}
@article{titleonly,
  title = {Just A Title}
}
@article{notitle,
  author = {Nobody},
  year = {2020}
}
@article{quotedfields,
  title = "Quoted Title",
  author = "Quoted Author",
  year = "2021"
}
"""


def test_bibtex_two_entries_with_abstract(tmp_path):
    """Two entries; the first has an abstract → 3 total claims."""
    import core.adapters.bibtex_adapter  # noqa: F401
    from core.adapters.bibtex_adapter import extract_bibtex_claims
    bib = tmp_path / "refs.bib"
    bib.write_text(_BIB_TWO_ENTRIES, encoding="utf-8")
    claims = extract_bibtex_claims(str(bib))
    # einstein1905: citation claim + abstract claim; darwin1859: citation only
    assert len(claims) == 3
    chunk_ids = [c["chunk_id"] for c in claims]
    assert chunk_ids.count("einstein1905") == 2
    assert chunk_ids.count("darwin1859") == 1
    # citation format: "title" (author, year)
    einstein_citation = next(c["claim"] for c in claims if c["chunk_id"] == "einstein1905"
                             and "abstract" not in c["claim"].lower()[:20])
    assert "Einstein" in einstein_citation
    assert "1905" in einstein_citation
    # abstract stored separately
    abstract_claim = next(c["claim"] for c in claims if c["chunk_id"] == "einstein1905"
                          and "relativity" in c["claim"].lower())
    assert "relativity" in abstract_claim.lower()


def test_bibtex_empty_file(tmp_path):
    """Empty .bib → empty list."""
    import core.adapters.bibtex_adapter  # noqa: F401
    from core.adapters.bibtex_adapter import extract_bibtex_claims
    bib = tmp_path / "empty.bib"
    bib.write_text("", encoding="utf-8")
    assert extract_bibtex_claims(str(bib)) == []


def test_bibtex_all_citation_forms(tmp_path):
    """Exercise all branches of _build_citation_claim."""
    import core.adapters.bibtex_adapter  # noqa: F401
    from core.adapters.bibtex_adapter import extract_bibtex_claims
    bib = tmp_path / "forms.bib"
    bib.write_text(_BIB_ALL_CITATION_FORMS, encoding="utf-8")
    claims = extract_bibtex_claims(str(bib))
    claims_by_key: dict = {}
    for c in claims:
        claims_by_key.setdefault(c["chunk_id"], []).append(c["claim"])

    # author only (no year)
    assert any("Some Author" in cl and "2" not in cl for cl in claims_by_key["authoronly"])
    # year only (no author)
    assert any("2000" in cl and "Author" not in cl for cl in claims_by_key["yearonly"])
    # title only (no author, no year)
    assert any(cl == '"Just A Title"' for cl in claims_by_key["titleonly"])
    # no title → no claim for that key
    assert "notitle" not in claims_by_key
    # quoted-field syntax ("...") parsed the same as brace syntax ({...})
    assert any("Quoted Title" in cl for cl in claims_by_key["quotedfields"])
    assert any("Quoted Author" in cl for cl in claims_by_key["quotedfields"])
    assert any("2021" in cl for cl in claims_by_key["quotedfields"])


def test_bibtex_ingest_file(tmp_path, monkeypatch):
    """End-to-end: ingest_file accepts .bib extension."""
    _reset_env(monkeypatch)
    import core.adapters.bibtex_adapter  # noqa: F401
    bib = tmp_path / "refs.bib"
    bib.write_text(_BIB_TWO_ENTRIES, encoding="utf-8")
    from core import knowledge
    rep = knowledge.ingest_file(str(bib))
    assert "accepted" in rep
    assert rep["source"] == "refs.bib"


def test_bibtex_nested_braces(tmp_path):
    """title = {An {Important} Result} preserves full text including nested brace content."""
    from core.adapters.bibtex_adapter import extract_bibtex_claims, _extract_brace_value
    bib = tmp_path / "nested.bib"
    bib.write_text(
        "@article{nested1,\n"
        "  title = {An {Important} Result},\n"
        "  year = {2020}\n"
        "}\n",
        encoding="utf-8",
    )
    claims = extract_bibtex_claims(str(bib))
    assert len(claims) == 1
    # The brace-counter preserves inner text; inner {} appear as literal chars in output
    assert "Important" in claims[0]["claim"]
    assert "2020" in claims[0]["claim"]

    # _extract_brace_value: depth>0 inner '{' appended to buf (line 46)
    val, end = _extract_brace_value("{outer {inner} text}", 0)
    assert "inner" in val
    assert "outer" in val

    # _extract_brace_value: depth>1 inner '}' appended to buf (line 52)
    val2, _ = _extract_brace_value("{A {B {deeply nested} end} final}", 0)
    assert "deeply nested" in val2

    # _extract_brace_value: unclosed brace returns partial content (line 57)
    val3, end3 = _extract_brace_value("{unclosed content", 0)
    assert "unclosed content" in val3


def test_bibtex_bare_integer_year(tmp_path):
    """year = 1905 (unquoted integer) is parsed correctly."""
    from core.adapters.bibtex_adapter import extract_bibtex_claims
    bib = tmp_path / "bare.bib"
    bib.write_text(
        "@article{bare1,\n"
        "  title = {A Famous Paper},\n"
        "  year = 1905\n"
        "}\n",
        encoding="utf-8",
    )
    claims = extract_bibtex_claims(str(bib))
    assert len(claims) == 1
    assert "1905" in claims[0]["claim"]


def test_bibtex_parse_fields_no_match_break(tmp_path):
    """Cover _parse_fields break (line 73): body with non-field trailing content."""
    from core.adapters.bibtex_adapter import extract_bibtex_claims
    # A BibTeX entry with a comment line after the last field. The comment
    # text ends up in 'body' but matches nothing in _FIELD_RE → line 73 (break).
    bib = tmp_path / "comment.bib"
    bib.write_text(
        "@article{commented,\n"
        "  title = {A Paper With Comment},\n"
        "  % trailing comment that forces the break path\n"
        "}\n",
        encoding="utf-8",
    )
    claims = extract_bibtex_claims(str(bib))
    # Should still extract the title claim despite the comment
    assert len(claims) == 1
    assert "A Paper With Comment" in claims[0]["claim"]


# ─── EPUB adapter ─────────────────────────────────────────────────────────────

ebooklib = pytest.importorskip("ebooklib", reason="ebooklib not installed — skip EPUB adapter tests")


def _make_minimal_epub(tmp: Path) -> str:
    """Build a minimal valid EPUB in-memory using ebooklib's EpubBook API."""
    from ebooklib import epub
    book = epub.EpubBook()
    book.set_identifier("test-epub-001")
    book.set_title("Test Book")
    book.set_language("en")

    # Chapter with paragraphs long enough to become claims.
    c1 = epub.EpubHtml(title="Chapter 1", file_name="chapter01.xhtml", lang="en")
    c1.content = (
        b"<html><body>"
        b"<p>The quick brown fox jumps over the lazy dog near the river bank.</p>"
        b"\n\n"
        b"<p>Short</p>"
        b"\n\n"
        b"<p>This is another sufficiently long paragraph for testing claim extraction.</p>"
        b"</body></html>"
    )
    book.add_item(c1)

    # Chapter whose content intentionally triggers the latin-1 fallback.
    c2 = epub.EpubHtml(title="Chapter 2", file_name="chapter02.xhtml", lang="en")
    # latin-1 bytes that are not valid UTF-8
    latin1_text = "Caf\xe9 culture is a cornerstone of Parisian daily life indeed.".encode("latin-1")
    c2.content = b"<html><body><p>" + latin1_text + b"</p></body></html>"
    book.add_item(c2)

    # Required navigation items for a valid EPUB
    book.toc = (epub.Link("chapter01.xhtml", "Chapter 1", "chapter01"),
                epub.Link("chapter02.xhtml", "Chapter 2", "chapter02"))
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ["nav", c1, c2]

    path = tmp / "test.epub"
    epub.write_epub(str(path), book)
    return str(path)


def test_epub_adapter_registers_on_import():
    import core.adapters.epub_adapter  # noqa: F401
    assert _get_adapter("epub") is not None


def test_epub_extract_returns_claims_with_chunk_id(tmp_path):
    """Minimal valid EPUB → claims have correct chunk_ids; short paragraphs skipped."""
    import core.adapters.epub_adapter  # noqa: F401
    from core.adapters.epub_adapter import extract_epub_claims
    path = _make_minimal_epub(tmp_path)
    claims = extract_epub_claims(path)
    assert isinstance(claims, list)
    assert len(claims) >= 2  # at least the two long paragraphs
    chunk_ids = {c["chunk_id"] for c in claims}
    # Both chapters should produce at least one claim
    assert len(chunk_ids) >= 1
    # Every claim must have a chunk_id and a non-empty claim string
    for c in claims:
        assert "chunk_id" in c
        assert "claim" in c
        assert len(c["claim"]) >= 30


def test_epub_html_to_text_latin1_fallback(tmp_path):
    """_html_to_text falls back to latin-1 when bytes are not valid UTF-8."""
    import core.adapters.epub_adapter  # noqa: F401
    from core.adapters.epub_adapter import _html_to_text
    # bytes that are invalid UTF-8 but valid latin-1
    latin1_bytes = b"Caf\xe9 au lait is a very pleasant morning drink indeed."
    result = _html_to_text(latin1_bytes)
    assert "Caf" in result  # decoded without crash


def test_epub_ingest_file(tmp_path, monkeypatch):
    """End-to-end: ingest_file accepts .epub extension."""
    _reset_env(monkeypatch)
    import core.adapters.epub_adapter  # noqa: F401
    path = _make_minimal_epub(tmp_path)
    from core import knowledge
    rep = knowledge.ingest_file(path)
    assert "accepted" in rep


def test_epub_html_to_text_html_entities(tmp_path):
    """_html_to_text decodes HTML entities (&amp;, &nbsp;, &#x2019;) correctly."""
    from core.adapters.epub_adapter import _html_to_text
    # Named entity (&amp;) and numeric charref (&#x2019; = right single quote)
    html_bytes = (
        b"<html><body><p>Fish &amp; chips &#x2019;tis great!</p></body></html>"
    )
    result = _html_to_text(html_bytes)
    assert "&" in result  # &amp; decoded
    assert "’" in result  # &#x2019; decoded


def test_epub_html_to_text_skips_head_and_script(tmp_path):
    """Content inside <head>, <style>, and <script> is excluded from output."""
    from core.adapters.epub_adapter import _html_to_text
    html_bytes = (
        b"<html>"
        b"<head><style>body { color: red; }</style><title>My Title</title></head>"
        b"<body>"
        b"<script>var x = 1;</script>"
        b"<p>Only this paragraph should appear in output text.</p>"
        b"</body></html>"
    )
    result = _html_to_text(html_bytes)
    assert "color" not in result
    assert "var x" not in result
    assert "My Title" not in result
    assert "Only this paragraph" in result


def test_epub_html_to_text_parser_exception_fallback(tmp_path):
    """When the HTML parser raises, _html_to_text falls back to regex tag-stripping."""
    import unittest.mock as _mock
    from core.adapters.epub_adapter import _html_to_text, _BodyExtractor

    # Patch _BodyExtractor.feed to raise so we hit the except branch
    original_feed = _BodyExtractor.feed

    def bad_feed(self, data):
        raise RuntimeError("simulated parser failure")

    with _mock.patch.object(_BodyExtractor, "feed", bad_feed):
        result = _html_to_text(b"<p>Hello world fallback text</p>")
    # Fallback strips tags via regex — should still contain the text
    assert "Hello world" in result


def test_epub_html_to_text_no_body_fallback(tmp_path):
    """When XHTML has no <body>, tag-stripping fallback is used."""
    from core.adapters.epub_adapter import _html_to_text
    # Fragment with no <body> tag at all
    html_bytes = b"<p>Fragment content without a body wrapper, long enough to check.</p>"
    result = _html_to_text(html_bytes)
    assert "Fragment content" in result


# ─── Wikidata adapter ─────────────────────────────────────────────────────────

requests_lib = pytest.importorskip("requests", reason="requests not installed — skip Wikidata adapter tests")

_WIKIDATA_MOCK_RESPONSE = {
    "entities": {
        "Q42": {
            "id": "Q42",
            "labels": {"en": {"value": "Douglas Adams"}},
            "descriptions": {"en": {"value": "English author and humorist"}},
        },
        "Q937": {
            "id": "Q937",
            "labels": {"en": {"value": "Albert Einstein"}},
            "descriptions": {"en": {"value": "German-born theoretical physicist"}},
        },
    }
}


def _mock_requests_get(monkeypatch, response_json: dict, status_code: int = 200):
    """Patch requests.get inside wikidata_adapter to return a fake response."""
    import unittest.mock as _mock

    mock_resp = _mock.MagicMock()
    mock_resp.status_code = status_code
    mock_resp.json.return_value = response_json

    monkeypatch.setattr(
        "core.adapters.wikidata_adapter._requests.get",
        _mock.MagicMock(return_value=mock_resp),
    )
    return mock_resp


def test_wikidata_adapter_registers_on_import():
    import core.adapters.wikidata_adapter  # noqa: F401
    assert _get_adapter("qids") is not None
    assert _get_adapter("wikidata") is not None


def test_wikidata_extract_from_json_array(tmp_path, monkeypatch):
    _reset_env(monkeypatch)
    qids_file = tmp_path / "entities.qids"
    qids_file.write_text('["Q42", "Q937"]', encoding="utf-8")
    _mock_requests_get(monkeypatch, _WIKIDATA_MOCK_RESPONSE)
    from core.adapters.wikidata_adapter import extract_wikidata_claims
    claims = extract_wikidata_claims(str(qids_file))
    assert len(claims) == 2
    chunk_ids = {c["chunk_id"] for c in claims}
    assert chunk_ids == {"Q42", "Q937"}
    claim_by_qid = {c["chunk_id"]: c["claim"] for c in claims}
    assert claim_by_qid["Q42"] == "Douglas Adams: English author and humorist"
    assert claim_by_qid["Q937"] == "Albert Einstein: German-born theoretical physicist"


def test_wikidata_extract_from_text_lines(tmp_path, monkeypatch):
    _reset_env(monkeypatch)
    qids_file = tmp_path / "entities.qids"
    qids_file.write_text("Q42\nQ937\n", encoding="utf-8")
    _mock_requests_get(monkeypatch, _WIKIDATA_MOCK_RESPONSE)
    from core.adapters.wikidata_adapter import extract_wikidata_claims
    claims = extract_wikidata_claims(str(qids_file))
    assert len(claims) == 2
    chunk_ids = {c["chunk_id"] for c in claims}
    assert chunk_ids == {"Q42", "Q937"}


def test_wikidata_extract_skips_missing_label(tmp_path, monkeypatch):
    _reset_env(monkeypatch)
    qids_file = tmp_path / "entities.qids"
    qids_file.write_text("Q42\nQ999\n", encoding="utf-8")
    # Q999 has no English label
    mock_response = {
        "entities": {
            "Q42": {
                "id": "Q42",
                "labels": {"en": {"value": "Douglas Adams"}},
                "descriptions": {"en": {"value": "English author and humorist"}},
            },
            "Q999": {
                "id": "Q999",
                "labels": {},
                "descriptions": {},
            },
        }
    }
    _mock_requests_get(monkeypatch, mock_response)
    from core.adapters.wikidata_adapter import extract_wikidata_claims
    claims = extract_wikidata_claims(str(qids_file))
    assert len(claims) == 1
    assert claims[0]["chunk_id"] == "Q42"


def test_wikidata_extract_label_only_no_description(tmp_path, monkeypatch):
    _reset_env(monkeypatch)
    qids_file = tmp_path / "entities.qids"
    qids_file.write_text("Q42\n", encoding="utf-8")
    mock_response = {
        "entities": {
            "Q42": {
                "id": "Q42",
                "labels": {"en": {"value": "Douglas Adams"}},
                "descriptions": {},
            },
        }
    }
    _mock_requests_get(monkeypatch, mock_response)
    from core.adapters.wikidata_adapter import extract_wikidata_claims
    claims = extract_wikidata_claims(str(qids_file))
    assert len(claims) == 1
    assert claims[0]["claim"] == "Douglas Adams"
    assert claims[0]["chunk_id"] == "Q42"


def test_wikidata_extract_deduplicates_qids(tmp_path, monkeypatch):
    _reset_env(monkeypatch)
    qids_file = tmp_path / "entities.qids"
    qids_file.write_text("Q42\nQ42\n", encoding="utf-8")
    import unittest.mock as _mock
    mock_get = _mock.MagicMock()
    mock_resp = _mock.MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "entities": {
            "Q42": {
                "id": "Q42",
                "labels": {"en": {"value": "Douglas Adams"}},
                "descriptions": {"en": {"value": "English author and humorist"}},
            }
        }
    }
    mock_get.return_value = mock_resp
    monkeypatch.setattr("core.adapters.wikidata_adapter._requests.get", mock_get)
    from core.adapters.wikidata_adapter import extract_wikidata_claims
    claims = extract_wikidata_claims(str(qids_file))
    assert len(claims) == 1
    assert mock_get.call_count == 1
    # The single API call should contain Q42 only once
    call_params = mock_get.call_args[1]["params"]
    assert call_params["ids"] == "Q42"


def test_wikidata_http_error_raises(tmp_path, monkeypatch):
    _reset_env(monkeypatch)
    qids_file = tmp_path / "entities.qids"
    qids_file.write_text("Q42\n", encoding="utf-8")
    import unittest.mock as _mock
    import requests as _reqs
    monkeypatch.setattr(
        "core.adapters.wikidata_adapter._requests.get",
        _mock.MagicMock(side_effect=_reqs.exceptions.RequestException("network error")),
    )
    from core.adapters.wikidata_adapter import extract_wikidata_claims
    with pytest.raises(RuntimeError, match="Wikidata API request failed"):
        extract_wikidata_claims(str(qids_file))


def test_wikidata_non_200_response_raises(tmp_path, monkeypatch):
    _reset_env(monkeypatch)
    qids_file = tmp_path / "entities.qids"
    qids_file.write_text("Q42\n", encoding="utf-8")
    _mock_requests_get(monkeypatch, {}, status_code=503)
    from core.adapters.wikidata_adapter import extract_wikidata_claims
    with pytest.raises(RuntimeError, match="Wikidata API returned HTTP 503"):
        extract_wikidata_claims(str(qids_file))


def test_wikidata_ingest_file_qids_extension(tmp_path, monkeypatch):
    _reset_env(monkeypatch)
    qids_file = tmp_path / "entities.qids"
    qids_file.write_text('["Q42", "Q937"]', encoding="utf-8")
    _mock_requests_get(monkeypatch, _WIKIDATA_MOCK_RESPONSE)
    import core.adapters.wikidata_adapter  # noqa: F401
    from core import knowledge
    rep = knowledge.ingest_file(str(qids_file))
    assert "accepted" in rep
    assert rep["accepted"] >= 1


def test_wikidata_empty_file_returns_empty(tmp_path, monkeypatch):
    _reset_env(monkeypatch)
    qids_file = tmp_path / "entities.qids"
    qids_file.write_text("", encoding="utf-8")
    import unittest.mock as _mock
    mock_get = _mock.MagicMock()
    monkeypatch.setattr("core.adapters.wikidata_adapter._requests.get", mock_get)
    from core.adapters.wikidata_adapter import extract_wikidata_claims
    claims = extract_wikidata_claims(str(qids_file))
    assert claims == []
    mock_get.assert_not_called()


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
