# core/span_extract.py
# Velantrim ExoCortex — Source-span extraction utilities (grant WP1)
#
# When a claim is extracted from a source document, we want to record WHERE in
# that document it came from — the character offset, the surrounding snippet,
# and the nearest section heading. This enables side-by-side source display and
# stronger claim-to-source auditability.
#
# All functions are pure (no I/O, no imports beyond stdlib) so they can be used
# by any ingestion path: text, markdown, JSONL, adapters.

import re
from typing import Optional, Tuple

# Matches Markdown headings (ATX style: # / ## / ### …)
_HEADING = re.compile(r"^#{1,6}\s+(.+)$", re.MULTILINE)


def locate_claim(content: str, claim: str) -> Tuple[Optional[int], Optional[int]]:
    """Find the first occurrence of `claim` in `content`.

    Returns (span_start, span_end) as half-open character offsets [start, end),
    or (None, None) if the claim is not found verbatim in the content.
    """
    if not claim or not content:
        return None, None
    pos = content.find(claim)
    if pos == -1:
        return None, None
    return pos, pos + len(claim)


def extract_section(content: str, char_pos: int) -> Optional[str]:
    """Return the text of the nearest Markdown heading before `char_pos`.

    Scans the content up to `char_pos` for ATX-style headings (# … through
    ###### …) and returns the text of the last one found, stripped of hashes
    and leading/trailing whitespace. Returns None if no heading precedes the
    position.
    """
    if not content or char_pos <= 0:
        return None
    before = content[:char_pos]
    headings = _HEADING.findall(before)
    if not headings:
        return None
    return headings[-1].strip()


def snippet_around(content: str, start: int, end: int,
                   context: int = 120) -> str:
    """Return the text around [start, end) with up to `context` chars of
    surrounding context on each side.

    The returned slice is from the original content — no normalisation applied —
    so it can be shown alongside the stored claim for provenance verification.
    """
    snip_start = max(0, start - context)
    snip_end = min(len(content), end + context)
    return content[snip_start:snip_end]
