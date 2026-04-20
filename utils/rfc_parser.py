"""Shared RFC extraction utilities for the Velantrim toolchain."""

import re
from typing import List, Optional


def extract_rfc(text: str) -> Optional[str]:
    """Extract first RFC reference from text. Returns e.g. 'RFC0067 v2.0' or None."""
    m = re.search(r'RFC\s*0*(\d{2,4})\s*(?:v\s*(\d+\.\d+))?', text, re.IGNORECASE)
    if m:
        rfc = f"RFC{m.group(1).zfill(4)}"
        if m.group(2):
            rfc += f" v{m.group(2)}"
        return rfc
    return None


def extract_rfc_mentions(text: str) -> List[str]:
    """Extract all unique RFC mentions from text, preserving order."""
    matches = re.findall(r'RFC\d{4}(?:\s+v\d+\.\d+)?', text)
    return list(dict.fromkeys(matches))
