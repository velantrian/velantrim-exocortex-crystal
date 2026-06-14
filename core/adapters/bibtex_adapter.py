# core/adapters/bibtex_adapter.py
# Velantrim ExoCortex — BibTeX knowledge adapter (grant WP4)
#
# Parses .bib files using a minimal stdlib-only regex-based parser (no bibtexparser
# dependency). Extracts @type{key, ...} entries and builds human-readable claim
# strings from the title, author, year, and abstract fields.
#
# Claim format: '"{title}" ({author}, {year})' — or just the title if other
# fields are absent.  An abstract field (if present) is emitted as a separate
# claim so that fine-grained content is preserved alongside the citation.
#
# No optional dependency — pure stdlib.
from __future__ import annotations

import re
from typing import Any, Dict, List, Optional

from core.adapters import register

# Match an @type{key, ...} BibTeX entry.  The closing `}` may have optional
# leading whitespace (some generators indent it; single-line entries end with
# `}\n` which also matches after the fix).
_ENTRY_RE = re.compile(
    r"@\w+\s*\{\s*([^,\s]+)\s*,\s*(.*?)\n[ \t]*\}",
    re.DOTALL,
)
# Match a field: fieldname = {value}, fieldname = "value", or bare integer/token
# The brace form is handled by _extract_brace_value to support nested braces.
_FIELD_RE = re.compile(
    r'(\w+)\s*=\s*(?:\{|"([^"]*)"|([\w\d./-]+))',
    re.DOTALL,
)


def _extract_brace_value(text: str, start: int) -> tuple[str, int]:
    """Return the content of a top-level {...} starting at *start* (the '{')
    and the index one past the closing '}'.  Handles arbitrarily nested braces.
    """
    depth = 0
    buf: list[str] = []
    i = start
    while i < len(text):
        ch = text[i]
        if ch == "{":
            if depth > 0:
                buf.append(ch)
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return "".join(buf), i + 1
            buf.append(ch)
        else:
            buf.append(ch)
        i += 1
    # Unclosed brace — return what we have
    return "".join(buf), i


def _parse_fields(body: str) -> Dict[str, str]:
    """Parse all BibTeX fields from an entry body string.

    Handles three value syntaxes:
      - Brace-delimited:  field = {value with {nested} braces}
      - Quote-delimited:  field = "value"
      - Bare token:       year = 1905
    """
    fields: Dict[str, str] = {}
    i = 0
    while i < len(body):
        m = _FIELD_RE.search(body, i)
        if m is None:
            break
        name = m.group(1).lower()
        if body[m.start(0):].lstrip()[len(name):].lstrip().startswith("="):
            # Determine which syntax matched
            after_eq = m.end(0)
            if m.group(2) is not None:
                # Quoted string — group(2) captured content
                value = m.group(2).strip()
                i = after_eq
            elif m.group(3) is not None:
                # Bare token (e.g. year = 1905)
                value = m.group(3).strip()
                i = after_eq
            else:
                # Brace-delimited — find the opening '{' then walk nested braces
                brace_pos = body.find("{", m.start(0) + len(name))
                if brace_pos == -1:  # pragma: no cover — regex guarantees '{' present
                    i = after_eq
                    continue
                value, end_pos = _extract_brace_value(body, brace_pos)
                value = value.strip()
                i = end_pos
            fields[name] = value
        else:  # pragma: no cover — _FIELD_RE always includes '=' so condition is always True
            i = m.end(0)
    return fields


def _parse_entries(text: str) -> List[Dict[str, str]]:
    """Return a list of dicts mapping lowercase field names → values, plus '_key'."""
    entries: List[Dict[str, str]] = []
    for m in _ENTRY_RE.finditer(text):
        key = m.group(1).strip()
        body = m.group(2)
        fields: Dict[str, str] = {"_key": key}
        fields.update(_parse_fields(body))
        entries.append(fields)
    return entries


def _build_citation_claim(fields: Dict[str, str]) -> Optional[str]:
    """Build a human-readable citation string from title/author/year fields."""
    title = fields.get("title", "").strip()
    if not title:
        return None
    author = fields.get("author", "").strip()
    year = fields.get("year", "").strip()
    if author and year:
        return f'"{title}" ({author}, {year})'
    if author:
        return f'"{title}" ({author})'
    if year:
        return f'"{title}" ({year})'
    return f'"{title}"'


def extract_bibtex_claims(path: str) -> List[Dict[str, Any]]:
    """Parse a .bib file and return a list of claim dicts.

    Each claim dict has:
      - "claim": human-readable string derived from citation fields
      - "chunk_id": the BibTeX entry key (e.g. "einstein1905")

    Two claims may be emitted per entry: one from the citation metadata
    (title/author/year) and one from the abstract when present.
    """
    with open(path, encoding="utf-8") as fh:
        text = fh.read()

    claims: List[Dict[str, Any]] = []
    for fields in _parse_entries(text):
        chunk_id = fields["_key"]
        citation = _build_citation_claim(fields)
        if citation:
            claims.append({"claim": citation, "chunk_id": chunk_id})
        abstract = fields.get("abstract", "").strip()
        if abstract:
            claims.append({"claim": abstract, "chunk_id": chunk_id})
    return claims


register("bib", extract_bibtex_claims)
