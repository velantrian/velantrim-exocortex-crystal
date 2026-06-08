# core/adapters/pdf_adapter.py
# Velantrim ExoCortex — PDF knowledge adapter (grant WP4)
# v8.27.0-sprint6
#
# Extracts text from a PDF via pypdf, splits on blank lines, and returns each
# non-trivial paragraph as a candidate claim. One claim per paragraph keeps
# granularity close to what the plain-text adapter produces.
#
# Install: pip install "velantrim-exocortex-crystal[pdf]"
from __future__ import annotations

import re
from typing import Any, Dict, List

try:
    import pypdf as _pypdf
except ImportError as _exc:
    raise ImportError(
        "PDF adapter requires pypdf. "
        'Install with: pip install "velantrim-exocortex-crystal[pdf]"'
    ) from _exc

from core.adapters import register

_PARA = re.compile(r"\n{2,}")
_MIN_LEN = 15  # skip header/footer fragments shorter than this


def extract_pdf_claims(path: str) -> List[Dict[str, Any]]:
    """Extract text paragraphs from a PDF and return them as claim dicts."""
    reader = _pypdf.PdfReader(path)
    pages: List[str] = []
    for page in reader.pages:
        text = page.extract_text() or ""
        pages.append(text)
    full_text = "\n".join(pages)
    claims: List[Dict[str, Any]] = []
    for para in _PARA.split(full_text):
        para = " ".join(para.split())  # collapse internal whitespace
        if len(para) >= _MIN_LEN:
            claims.append({"claim": para})
    return claims


register("pdf", extract_pdf_claims)
