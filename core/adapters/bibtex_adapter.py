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

# Match an @type{key, ...} BibTeX entry (non-greedy, handles nested braces poorly
# but covers the common flat-field case reliably without a full parser).
_ENTRY_RE = re.compile(
    r"@\w+\s*\{\s*([^,\s]+)\s*,\s*(.*?)\n\}",
    re.DOTALL,
)
# Match a field: fieldname = {value} or fieldname = "value"
_FIELD_RE = re.compile(
    r"(\w+)\s*=\s*(?:\{([^}]*)\}|\"([^\"]*)\")",
    re.DOTALL,
)


def _parse_entries(text: str) -> List[Dict[str, str]]:
    """Return a list of dicts mapping lowercase field names → values, plus '_key'."""
    entries: List[Dict[str, str]] = []
    for m in _ENTRY_RE.finditer(text):
        key = m.group(1).strip()
        body = m.group(2)
        fields: Dict[str, str] = {"_key": key}
        for fm in _FIELD_RE.finditer(body):
            name = fm.group(1).lower()
            value = (fm.group(2) or fm.group(3) or "").strip()
            fields[name] = value
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
