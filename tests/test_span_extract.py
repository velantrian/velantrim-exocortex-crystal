"""Tests for core/span_extract.py — pure stdlib span extraction utilities (WP1)."""
import pytest

from core import span_extract


# ─── locate_claim ─────────────────────────────────────────────────────────────

def test_locate_claim_empty_claim_returns_none():
    assert span_extract.locate_claim("some content", "") == (None, None)


def test_locate_claim_empty_content_returns_none():
    assert span_extract.locate_claim("", "a claim") == (None, None)


def test_locate_claim_both_empty_returns_none():
    assert span_extract.locate_claim("", "") == (None, None)


def test_locate_claim_not_found_returns_none():
    assert span_extract.locate_claim("hello world", "missing text") == (None, None)


def test_locate_claim_found_returns_correct_offsets():
    content = "prefix THE CLAIM suffix"
    start, end = span_extract.locate_claim(content, "THE CLAIM")
    assert start == 7
    assert end == 16
    assert content[start:end] == "THE CLAIM"


def test_locate_claim_at_start():
    content = "claim at start more text"
    start, end = span_extract.locate_claim(content, "claim at start")
    assert start == 0
    assert end == 14


def test_locate_claim_at_end():
    content = "text before claim_at_end"
    start, end = span_extract.locate_claim(content, "claim_at_end")
    assert end == len(content)


def test_locate_claim_returns_first_occurrence():
    content = "abc abc abc"
    start, end = span_extract.locate_claim(content, "abc")
    assert start == 0
    assert end == 3


def test_locate_claim_span_length_matches_claim():
    claim = "some multi-word claim"
    content = "preamble " + claim + " epilogue"
    start, end = span_extract.locate_claim(content, claim)
    assert end - start == len(claim)


# ─── extract_section ──────────────────────────────────────────────────────────

def test_extract_section_empty_content_returns_none():
    assert span_extract.extract_section("", 10) is None


def test_extract_section_zero_pos_returns_none():
    assert span_extract.extract_section("# Title\ntext", 0) is None


def test_extract_section_negative_pos_returns_none():
    assert span_extract.extract_section("# Title\ntext", -5) is None


def test_extract_section_no_headings_returns_none():
    content = "plain text with no headings\nmore text"
    assert span_extract.extract_section(content, 15) is None


def test_extract_section_finds_heading_before_pos():
    content = "# Introduction\n\nThis is the first paragraph."
    pos = content.index("This")
    section = span_extract.extract_section(content, pos)
    assert section == "Introduction"


def test_extract_section_returns_last_heading_before_pos():
    content = "# Chapter One\n\nsome text\n\n## Section 1.1\n\nthe claim here\n"
    pos = content.index("the claim")
    section = span_extract.extract_section(content, pos)
    assert section == "Section 1.1"


def test_extract_section_ignores_headings_after_pos():
    content = "# Before\n\nclaim text\n\n# After\n"
    pos = content.index("claim text")
    section = span_extract.extract_section(content, pos)
    assert section == "Before"


def test_extract_section_strips_whitespace():
    content = "##   Padded Heading  \n\nfact here"
    pos = content.index("fact here")
    section = span_extract.extract_section(content, pos)
    assert section == "Padded Heading"


def test_extract_section_level_6_heading():
    content = "###### Deep Heading\n\ntext"
    pos = content.index("text")
    section = span_extract.extract_section(content, pos)
    assert section == "Deep Heading"


# ─── snippet_around ───────────────────────────────────────────────────────────

def test_snippet_around_returns_context_window():
    content = "a" * 200 + "TARGET" + "b" * 200
    start = 200
    end = 206
    snippet = span_extract.snippet_around(content, start, end, context=50)
    assert "TARGET" in snippet
    assert len(snippet) == 6 + 50 + 50  # TARGET + 50 before + 50 after


def test_snippet_around_clamps_to_content_start():
    content = "short prefix TARGET more text here"
    start = content.index("TARGET")
    end = start + 6
    snippet = span_extract.snippet_around(content, start, end, context=500)
    assert snippet.startswith("short prefix")
    assert snippet == content


def test_snippet_around_clamps_to_content_end():
    content = "some text before TARGET"
    start = content.index("TARGET")
    end = len(content)
    snippet = span_extract.snippet_around(content, start, end, context=500)
    assert snippet.endswith("TARGET")
    assert snippet == content


def test_snippet_around_default_context_is_120():
    content = "x" * 300 + "M" + "y" * 300
    start, end = 300, 301
    snippet = span_extract.snippet_around(content, start, end)
    assert len(snippet) == 1 + 120 + 120


def test_snippet_around_zero_context():
    content = "before MATCH after"
    start = content.index("MATCH")
    end = start + 5
    snippet = span_extract.snippet_around(content, start, end, context=0)
    assert snippet == "MATCH"
