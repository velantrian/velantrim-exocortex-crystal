# core/pii.py
# Velantrim ExoCortex — PII Detection & Redaction (GDPR Art. 5 data minimisation)
#
# Detects and redacts common personal data in free text before it is stored, so
# the memory keeps only what it needs ("data minimisation", Art. 5(1)(c)) and
# avoids retaining raw identifiers. Detection is heuristic and dependency-free
# (stdlib `re` only).
#
# Recognised: EMAIL, IBAN, CREDIT_CARD (Luhn-validated), IPV4, PHONE.
# Matching is overlap-safe: when two patterns claim overlapping spans, the
# higher-priority (more specific) type wins, so a card is never mislabelled as a
# phone number, an IP is never swallowed by the phone pattern, etc.
#
# OFF by default. Set VELANTRIM_REDACT_PII=1 to redact at ingest. The detect()/
# redact() helpers and the CLI `redact` command are always available regardless.
# Findings are content-free (type + span), never the matched value itself.

import os
import re
from datetime import datetime
from typing import Dict, Any, List, Tuple

# (type, priority, compiled_regex). Lower priority number = wins on overlap.
_PATTERNS = [
    ("EMAIL", 1, re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")),
    ("IBAN", 2, re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{11,30}\b")),
    ("CREDIT_CARD", 3, re.compile(r"\b\d(?:[ -]?\d){12,18}\b")),
    ("IPV4", 4, re.compile(
        r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b")),
    ("PHONE", 5, re.compile(r"(?<![\w.])\+?\d[\d\s().-]{5,}\d(?![\w])")),
]

_ENV_REDACT = "VELANTRIM_REDACT_PII"

# A bare ISO-8601 date (YYYY-MM-DD) clears the PHONE pattern's digit-count
# check (8 digits, within the 7-15 range) — exclude it explicitly rather than
# tighten the digit-count bound, which would risk rejecting real short phone
# numbers.
_ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _is_real_iso_date(raw: str) -> bool:
    """True only for a genuine calendar date shaped YYYY-MM-DD.

    Shape alone is not enough: a phone-like value such as "5555-12-34" (day
    34 does not exist) or "1234-56-78" (month 56 does not exist) matches the
    YYYY-MM-DD shape without being a real date, and must remain eligible for
    PHONE redaction.
    """
    raw = raw.strip()
    if not _ISO_DATE_RE.match(raw):
        return False
    try:
        datetime.strptime(raw, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def redaction_enabled() -> bool:
    """True if PII redaction at ingest is turned on (VELANTRIM_REDACT_PII)."""
    return os.environ.get(_ENV_REDACT, "").lower() in ("1", "true", "yes", "on")


def _luhn_ok(digits: str) -> bool:
    """Luhn checksum — filters digit runs that are not plausible card numbers."""
    total, alt = 0, False
    for ch in reversed(digits):
        d = ord(ch) - 48
        if alt:
            d *= 2
            if d > 9:
                d -= 9
        total += d
        alt = not alt
    return total % 10 == 0


def _valid(pii_type: str, raw: str) -> bool:
    """Post-match validation that prunes false positives."""
    if pii_type == "CREDIT_CARD":
        digits = re.sub(r"\D", "", raw)
        return 13 <= len(digits) <= 19 and _luhn_ok(digits)
    if pii_type == "PHONE":
        if _is_real_iso_date(raw):
            return False
        digits = re.sub(r"\D", "", raw)
        return 7 <= len(digits) <= 15
    return True


def detect(text: str) -> List[Dict[str, Any]]:
    """
    Return non-overlapping PII spans as content-free findings:
    [{"type", "start", "end"}], sorted by position. Never includes the value.
    """
    candidates = []
    for pii_type, priority, rgx in _PATTERNS:
        for m in rgx.finditer(text):
            if _valid(pii_type, m.group()):
                candidates.append((priority, pii_type, m.start(), m.end()))

    # Overlap resolution: place higher-priority matches first; skip any that
    # overlap an already-placed span. O(n^2) but n is tiny.
    candidates.sort(key=lambda c: (c[0], c[2]))
    kept: List[Tuple[int, int, str]] = []  # (start, end, type)
    for _prio, pii_type, start, end in candidates:
        if any(start < k_end and k_start < end for k_start, k_end, _ in kept):
            continue
        kept.append((start, end, pii_type))

    kept.sort(key=lambda k: k[0])
    return [{"type": t, "start": s, "end": e} for s, e, t in kept]


def redact(text: str) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Replace each detected PII span with a `[TYPE]` placeholder.
    Returns (redacted_text, findings) where findings is content-free.
    """
    findings = detect(text)
    if not findings:
        return text, []
    out, cursor = [], 0
    for f in findings:
        out.append(text[cursor:f["start"]])
        out.append(f"[{f['type']}]")
        cursor = f["end"]
    out.append(text[cursor:])
    return "".join(out), findings


def summary(findings: List[Dict[str, Any]]) -> Dict[str, int]:
    """Content-free count of redactions by type (for metadata / reporting)."""
    counts: Dict[str, int] = {}
    for f in findings:
        counts[f["type"]] = counts.get(f["type"], 0) + 1
    return counts
