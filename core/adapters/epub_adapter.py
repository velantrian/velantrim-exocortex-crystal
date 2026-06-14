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

import html
import re
from html.parser import HTMLParser
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

_MIN_LEN = 30

# Block-level tags whose boundaries become paragraph separators.
_BLOCK_TAGS = frozenset(
    ["p", "div", "br", "h1", "h2", "h3", "h4", "h5", "h6", "li", "tr"]
)
_TAG_RE = re.compile(r"<[^>]+>")


class _BodyExtractor(HTMLParser):
    """Extract the text content of the <body> element only."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self._in_body = False
        self._skip_tags = {"head", "style", "script"}
        self._skip_depth = 0
        self.parts: List[str] = []

    def handle_starttag(self, tag: str, attrs: Any) -> None:
        tag = tag.lower()
        if tag == "body":
            self._in_body = True
            return
        if not self._in_body:
            return
        if tag in self._skip_tags:
            self._skip_depth += 1
            return
        if tag in _BLOCK_TAGS:
            self.parts.append("\n\n")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "body":
            self._in_body = False
            return
        if not self._in_body:
            return
        if tag in self._skip_tags:
            self._skip_depth = max(0, self._skip_depth - 1)
            return
        if tag in _BLOCK_TAGS:
            self.parts.append("\n\n")

    def handle_data(self, data: str) -> None:
        if self._in_body and self._skip_depth == 0:
            self.parts.append(data)

    def handle_entityref(self, name: str) -> None:  # HTML4 named entities
        if self._in_body and self._skip_depth == 0:
            self.parts.append(html.unescape(f"&{name};"))

    def handle_charref(self, name: str) -> None:  # &#NN; / &#xNN;
        if self._in_body and self._skip_depth == 0:
            self.parts.append(html.unescape(f"&#{name};"))

    def get_text(self) -> str:
        return "".join(self.parts)


def _html_to_text(html_bytes: bytes) -> str:
    """Extract body text from XHTML bytes, decode HTML entities, return plain text.

    Parses only the <body> element so that <head>/<style>/<script> content is
    excluded.  Falls back to whole-document tag-stripping when no <body> element
    is present (e.g. fragment inputs or malformed XHTML).
    """
    try:
        raw = html_bytes.decode("utf-8")
    except UnicodeDecodeError:
        raw = html_bytes.decode("latin-1", errors="replace")

    parser = _BodyExtractor()
    try:
        parser.feed(raw)
        text = parser.get_text()
    except Exception:
        text = ""

    # If no <body> was found (fragment or malformed input), strip tags from whole doc.
    if not text.strip():
        text = _TAG_RE.sub(" ", raw)

    return html.unescape(text)


def extract_epub_claims(path: str) -> List[Dict[str, Any]]:
    """Extract text paragraphs from an EPUB and return them as claim dicts.

    Only spine/chapter items are processed (navigation, cover, and TOC items
    are excluded).  Each claim dict carries a chunk_id equal to the epub item
    id (e.g. "chapter01") so that ingest_claims can attach WP1 source-span
    evidence at chapter granularity without a second locate_claim scan.
    """
    book = _epub.read_epub(path)
    claims: List[Dict[str, Any]] = []
    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        # Skip navigation / cover / TOC items — process only real chapters.
        if not item.is_chapter():
            continue
        chunk_id = item.get_id()
        text = _html_to_text(item.get_content())
        for raw_para in text.split("\n\n"):
            collapsed = " ".join(raw_para.split())
            if len(collapsed) >= _MIN_LEN:
                claims.append({"claim": collapsed, "chunk_id": chunk_id})
    return claims


register("epub", extract_epub_claims)
