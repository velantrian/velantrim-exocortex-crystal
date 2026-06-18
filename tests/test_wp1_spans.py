"""Integration tests for WP1 — Source Span Offsets.

Verifies that span_start/span_end/section/chunk_id are correctly propagated
through the ingestion pipeline (knowledge.ingest_text / ingest_claims) and
stored as evidence records, and that the PDF adapter emits per-paragraph
span fields.
"""
from __future__ import annotations

import io
import os
import tempfile
from pathlib import Path
from typing import Any, Dict, List
from unittest.mock import MagicMock, patch

import pytest

from core import evidence, knowledge, span_extract


# ─── ingest_text: plain text ──────────────────────────────────────────────────

def test_ingest_text_records_span_offsets(monkeypatch):
    """ingest_text must detect char offsets for accepted facts."""
    content = "Water is a liquid at room temperature."
    rep = knowledge.ingest_text(content, fmt="txt", source="phys.txt")
    assert rep["accepted"] >= 1
    fid = rep["fact_ids"][0]
    spans = evidence.evidence_for(fid)
    assert spans, "evidence span must be attached for accepted fact"
    span = spans[0]
    assert span["span_start"] == 0
    assert span["span_end"] == len(content)
    assert content[span["span_start"]:span["span_end"]] == content.strip()


def test_ingest_text_multi_line_records_individual_spans():
    """Each claim in a multi-line text gets its own span."""
    content = "Gold is a metal\nSilver is a metal\n"
    rep = knowledge.ingest_text(content, fmt="txt", source="metals.txt")
    assert rep["accepted"] >= 2
    for fid in rep["fact_ids"]:
        spans = evidence.evidence_for(fid)
        assert spans, f"span missing for fact {fid}"
        span = spans[0]
        assert span["span_start"] is not None
        assert span["span_end"] is not None


# ─── ingest_text: markdown with sections ─────────────────────────────────────

def test_ingest_text_markdown_records_section():
    """Evidence section must reflect the nearest Markdown heading."""
    md = "# Physics Facts\n\nLight travels at 299792 km/s.\n"
    rep = knowledge.ingest_text(md, fmt="md", source="physics.md")
    assert rep["accepted"] >= 1
    fid = rep["fact_ids"][0]
    spans = evidence.evidence_for(fid)
    assert spans
    assert spans[0]["section"] == "Physics Facts"


def test_ingest_text_markdown_no_heading_section_is_none():
    """Claims before any heading get section=None."""
    md = "Helium is a noble gas.\n"
    rep = knowledge.ingest_text(md, fmt="md", source="chem.md")
    assert rep["accepted"] >= 1
    fid = rep["fact_ids"][0]
    spans = evidence.evidence_for(fid)
    assert spans
    assert spans[0]["section"] is None


def test_ingest_text_markdown_multiple_sections():
    """Each claim gets the section of its nearest preceding heading."""
    md = "# Chapter A\n\nFact about chapter A.\n\n# Chapter B\n\nFact about chapter B.\n"
    rep = knowledge.ingest_text(md, fmt="md", source="doc.md")
    # May get 1 or 2 accepted depending on gate; check whichever is accepted
    for fid in rep["fact_ids"]:
        spans = evidence.evidence_for(fid)
        assert spans
        section = spans[0]["section"]
        assert section in ("Chapter A", "Chapter B")


# ─── ingest_claims: adapter-supplied spans take precedence ───────────────────

def test_ingest_claims_adapter_supplied_spans_used_as_is():
    """When the adapter pre-populates span_start/span_end, ingest_claims must
    store them verbatim — it must not override with locate_claim output."""
    claims = [{"claim": "Oxygen supports combustion",
               "span_start": 42, "span_end": 68, "chunk_id": "3"}]
    rep = knowledge.ingest_claims(
        claims, source="chem.pdf", source_content="some content that does not matter",
    )
    assert rep["accepted"] >= 1
    fid = rep["fact_ids"][0]
    spans = evidence.evidence_for(fid)
    assert spans
    assert spans[0]["span_start"] == 42
    assert spans[0]["span_end"] == 68
    assert spans[0]["chunk_id"] == "3"


def test_ingest_claims_adapter_supplied_section_used_as_is():
    """Adapter-supplied section is stored without overwrite."""
    claims = [{"claim": "Nitrogen is inert", "section": "Adapter Section"}]
    rep = knowledge.ingest_claims(
        claims, source="x.pdf",
        source_content="# Different Section\n\nNitrogen is inert\n",
    )
    assert rep["accepted"] >= 1
    fid = rep["fact_ids"][0]
    spans = evidence.evidence_for(fid)
    assert spans
    assert spans[0]["section"] == "Adapter Section"


# ─── ingest_claims: no source_content → span detection skipped ───────────────

def test_ingest_claims_no_source_content_span_is_none():
    """Without source_content, span offsets are None but evidence is still attached."""
    claims = [{"claim": "Copper conducts electricity"}]
    rep = knowledge.ingest_claims(claims, source="metals.json")
    assert rep["accepted"] >= 1
    fid = rep["fact_ids"][0]
    spans = evidence.evidence_for(fid)
    assert spans
    assert spans[0]["span_start"] is None
    assert spans[0]["span_end"] is None


# ─── ingest_claims: claim not found in source_content ────────────────────────

def test_ingest_claims_claim_not_in_source_content_span_is_none():
    """If locate_claim returns (None, None), span fields remain None in evidence."""
    content = "This document does not contain the claim."
    claims = [{"claim": "Iron is magnetic"}]  # not in content
    rep = knowledge.ingest_claims(
        claims, source="doc.txt", source_content=content,
    )
    assert rep["accepted"] >= 1
    fid = rep["fact_ids"][0]
    spans = evidence.evidence_for(fid)
    assert spans
    assert spans[0]["span_start"] is None
    assert spans[0]["span_end"] is None


# ─── ingest_text: duplicate path does not double-attach evidence ──────────────

def test_ingest_text_duplicate_no_duplicate_evidence():
    """Duplicate (already-known) facts must not get a second evidence span."""
    content = "Titanium is lightweight and strong."
    rep1 = knowledge.ingest_text(content, fmt="txt", source="mat.txt")
    assert rep1["accepted"] >= 1
    fid = rep1["fact_ids"][0]

    rep2 = knowledge.ingest_text(content, fmt="txt", source="mat.txt")
    assert rep2["duplicates"] >= 1
    # After a duplicate, exactly ONE span must exist (the original).
    spans = evidence.evidence_for(fid)
    assert len(spans) == 1


# ─── ingest_file: stdlib path passes source_content ─────────────────────────

def test_ingest_file_txt_records_spans(tmp_path):
    """ingest_file for .txt files must propagate source_content so spans are detected."""
    claim_text = "Platinum is a precious metal."
    p = tmp_path / "facts.txt"
    p.write_text(claim_text + "\n", encoding="utf-8")
    rep = knowledge.ingest_file(str(p))
    assert rep["accepted"] >= 1
    fid = rep["fact_ids"][0]
    spans = evidence.evidence_for(fid)
    assert spans
    assert spans[0]["span_start"] is not None


# ─── PDF adapter: span fields ─────────────────────────────────────────────────

pypdf = pytest.importorskip("pypdf", reason="pypdf not installed — skip PDF span tests")


def _make_text_pdf(tmp: Path, page_texts: List[str]) -> str:
    """Create a minimal PDF with actual text content using a low-level approach.

    We mock pypdf.PdfReader so the adapter sees real page text without
    requiring a fully compliant PDF file (which would need reportlab/fpdf2).
    """
    path = tmp / "test.pdf"
    # Write a placeholder file; the test patches the reader.
    path.write_bytes(b"%PDF-1.4\n")
    return str(path)


def _mock_reader(page_texts: List[str]):
    """Return a mock PdfReader whose .pages yield the given text strings."""
    reader = MagicMock()
    pages = []
    for text in page_texts:
        page = MagicMock()
        page.extract_text.return_value = text
        pages.append(page)
    reader.pages = pages
    return reader


def test_pdf_adapter_single_page_span_fields(tmp_path):
    """extract_pdf_claims on a single-page PDF adds span_start/span_end/chunk_id."""
    import core.adapters.pdf_adapter as pdf_mod
    page_text = "  \n\nChlorine is a toxic gas\n\nSodium is a soft metal\n\n  "
    with patch.object(pdf_mod._pypdf, "PdfReader", return_value=_mock_reader([page_text])):
        claims = pdf_mod.extract_pdf_claims(_make_text_pdf(tmp_path, [page_text]))
    assert claims, "should extract at least one claim"
    for c in claims:
        assert "span_start" in c
        assert "span_end" in c
        assert "chunk_id" in c
        assert c["chunk_id"] == "1"
        assert isinstance(c["span_start"], int)
        assert isinstance(c["span_end"], int)
        assert c["span_start"] <= c["span_end"]


def test_pdf_adapter_multipage_chunk_id(tmp_path):
    """Second-page paragraphs must have chunk_id == '2'.

    Each page ends with a newline so that when pages are joined with "\n",
    the junction produces "\n\n" — the double-newline that _PARA splits on.
    """
    import core.adapters.pdf_adapter as pdf_mod
    # Page text ends with "\n" so "page1\n" + "\n" + "page2" gives "\n\n".
    page1 = "First page paragraph with enough text here\n"
    page2 = "Second page paragraph with enough text here"
    with patch.object(pdf_mod._pypdf, "PdfReader",
                      return_value=_mock_reader([page1, page2])):
        claims = pdf_mod.extract_pdf_claims(
            _make_text_pdf(tmp_path, [page1, page2]))
    assert len(claims) >= 2, "must extract one paragraph per page"
    chunk_ids = {c.get("chunk_id") for c in claims}
    assert "1" in chunk_ids
    assert "2" in chunk_ids


def test_pdf_adapter_span_content_matches_raw_paragraph(tmp_path):
    """span_start/span_end in each claim must address the raw paragraph in full_text."""
    import core.adapters.pdf_adapter as pdf_mod
    page_text = "Short paragraph A is here.\n\nShort paragraph B is here."
    with patch.object(pdf_mod._pypdf, "PdfReader",
                      return_value=_mock_reader([page_text])):
        claims = pdf_mod.extract_pdf_claims(
            _make_text_pdf(tmp_path, [page_text]))
    # Reconstruct full_text exactly as the adapter does.
    full_text = page_text  # single page → full_text == page_text
    for c in claims:
        raw_slice = full_text[c["span_start"]:c["span_end"]]
        assert " ".join(raw_slice.split()) == c["claim"], (
            f"collapsed slice must equal stored claim: {c!r}")


def test_pdf_adapter_blank_page_no_crash(tmp_path):
    """A page with no text must not crash — returns empty claims list."""
    import core.adapters.pdf_adapter as pdf_mod
    with patch.object(pdf_mod._pypdf, "PdfReader",
                      return_value=_mock_reader([""])):
        claims = pdf_mod.extract_pdf_claims(
            _make_text_pdf(tmp_path, [""]))
    assert claims == []


def test_pdf_adapter_short_fragments_excluded(tmp_path):
    """Paragraphs shorter than _MIN_LEN (15 chars) must be excluded."""
    import core.adapters.pdf_adapter as pdf_mod
    page_text = "Hi.\n\nThis is a paragraph that is definitely long enough to pass."
    with patch.object(pdf_mod._pypdf, "PdfReader",
                      return_value=_mock_reader([page_text])):
        claims = pdf_mod.extract_pdf_claims(
            _make_text_pdf(tmp_path, [page_text]))
    claim_texts = [c["claim"] for c in claims]
    assert "Hi." not in claim_texts
    assert any("definitely long enough" in ct for ct in claim_texts)


def test_pdf_adapter_duplicate_paragraphs_distinct_spans(tmp_path):
    """A verbatim-repeated paragraph must map to its own occurrence, not the first.

    Regression: extract_pdf_claims used full_text.find(raw_para) (offset 0), so a
    paragraph appearing twice gave both claims the *first* occurrence's span. The
    cursor-based search must resolve the second claim to the second occurrence.
    """
    import core.adapters.pdf_adapter as pdf_mod
    para = "The Earth orbits the Sun in an elliptical path."
    page_text = para + "\n\n" + para  # same paragraph twice, blank line between
    with patch.object(pdf_mod._pypdf, "PdfReader",
                      return_value=_mock_reader([page_text])):
        claims = pdf_mod.extract_pdf_claims(
            _make_text_pdf(tmp_path, [page_text]))
    assert len(claims) == 2, "both duplicate paragraphs must yield a claim"
    assert claims[0]["claim"] == para
    assert claims[1]["claim"] == para
    # First occurrence at offset 0; second after "<para>\n\n".
    assert claims[0]["span_start"] == 0
    assert claims[1]["span_start"] == len(para) + 2
    assert claims[0]["span_start"] != claims[1]["span_start"]
    # Each span must slice the actual paragraph text out of full_text.
    full_text = page_text  # single page → full_text == page_text
    for c in claims:
        assert full_text[c["span_start"]:c["span_end"]] == para
