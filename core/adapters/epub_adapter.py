# core/adapters/epub_adapter.py
# Velantrim ExoCortex — EPUB knowledge adapter (grant WP4)
#
# Extracts text from each chapter/document item in an EPUB, splits on double
# newlines, and returns each non-trivial paragraph as a candidate claim.
# One claim per paragraph with the epub item id as chunk_id keeps provenance
# at chapter granularity (TruthGate still applies — nothing is blindly trusted
# because it arrived as EPUB).
#
# Install: pip install "velantrim-exocortex-crystal[epub]"
from __future__ import annotations

import re
from typing import Any, Dict, List

try:
    import ebooklib
    from ebooklib import epub as _epub
except ImportError as _exc:  # pragma: no cover - install hint when the extra is absent
    raise ImportError(
        "EPUB adapter requires ebooklib. "
        'Install with: pip install "velantrim-exocortex-crystal[epub]"'
    ) from _exc

from core.adapters import register

_TAG_RE = re.compile(r"<[^>]+>")
_MIN_LEN = 30


def _html_to_text(html_bytes: bytes) -> str:
    """Strip HTML tags and return plain text."""
    try:
        text = html_bytes.decode("utf-8")
    except UnicodeDecodeError:
        text = html_bytes.decode("latin-1", errors="replace")
    return _TAG_RE.sub(" ", text)


def extract_epub_claims(path: str) -> List[Dict[str, Any]]:
    """Extract text paragraphs from an EPUB and return them as claim dicts.

    Each claim dict carries a chunk_id equal to the epub item id (e.g.
    "chapter01") so that ingest_claims can attach WP1 source-span evidence at
    chapter granularity without a second locate_claim scan.
    """
    book = _epub.read_epub(path)
    claims: List[Dict[str, Any]] = []
    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        chunk_id = item.get_id()
        text = _html_to_text(item.get_content())
        for raw_para in text.split("\n\n"):
            collapsed = " ".join(raw_para.split())
            if len(collapsed) >= _MIN_LEN:
                claims.append({"claim": collapsed, "chunk_id": chunk_id})
    return claims


register("epub", extract_epub_claims)
