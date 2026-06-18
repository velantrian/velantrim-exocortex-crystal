# core/adapters/pdf_adapter.py
# Velantrim ExoCortex — PDF knowledge adapter (grant WP4)
#
# Extracts text from a PDF via pypdf, splits on blank lines, and returns each
# non-trivial paragraph as a candidate claim. One claim per paragraph keeps
# granularity close to what the plain-text adapter produces.
#
# Install: pip install "velantrim-exocortex-crystal[pdf]"
from __future__ import annotations

import re
from typing import Any, Dict, List, Optional

try:
    import pypdf as _pypdf
except ImportError as _exc:  # pragma: no cover - install hint when the extra is absent
    raise ImportError(
        "PDF adapter requires pypdf. "
        'Install with: pip install "velantrim-exocortex-crystal[pdf]"'
    ) from _exc

from core.adapters import register

_PARA = re.compile(r"\n{2,}")
_MIN_LEN = 15  # skip header/footer fragments shorter than this


def extract_pdf_claims(path: str) -> List[Dict[str, Any]]:
    """Extract text paragraphs from a PDF and return them as claim dicts.

    Each claim dict carries span_start/span_end (character offsets into the
    concatenated full text) and chunk_id (1-based page number) so that
    ingest_claims can attach precise WP1 source-span evidence without a second
    locate_claim scan.
    """
    reader = _pypdf.PdfReader(path)
    page_texts: List[str] = []
    for page in reader.pages:
        page_texts.append(page.extract_text() or "")
    full_text = "\n".join(page_texts)

    # Build a map: cumulative char offset at the start of each page.
    page_offsets: List[int] = []
    offset = 0
    for i, pt in enumerate(page_texts):
        page_offsets.append(offset)
        offset += len(pt) + (1 if i < len(page_texts) - 1 else 0)  # +1 for "\n"

    claims: List[Dict[str, Any]] = []
    cursor = 0  # advance past each matched paragraph so duplicates map to distinct spans
    for raw_para in _PARA.split(full_text):
        collapsed = " ".join(raw_para.split())
        if len(collapsed) < _MIN_LEN:
            continue
        # Locate the raw paragraph in full_text to get its character span.
        # Search from cursor (not 0) so a paragraph repeated verbatim resolves to
        # its actual occurrence instead of always the first one.
        para_start = full_text.find(raw_para, cursor)
        para_end = para_start + len(raw_para) if para_start != -1 else None
        if para_start != -1:
            cursor = para_end
        # Determine which page this paragraph starts on (1-based).
        chunk: Optional[str] = None
        if para_start != -1:
            page_num = 1
            for pg_idx, pg_off in enumerate(page_offsets):
                if pg_off <= para_start:
                    page_num = pg_idx + 1
                else:
                    break
            chunk = str(page_num)
        rec: Dict[str, Any] = {"claim": collapsed}
        if para_start != -1:
            rec["span_start"] = para_start
            rec["span_end"] = para_end
        if chunk is not None:
            rec["chunk_id"] = chunk
        claims.append(rec)
    return claims


register("pdf", extract_pdf_claims)
