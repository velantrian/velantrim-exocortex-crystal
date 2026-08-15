# core/ingest_identity.py
# Shared exact-normalized identity helpers for ingestion and legacy-index repair.

import hashlib
import re
import unicodedata


def normalize_claim(text: str) -> str:
    """Return Crystal's exact claim-identity form.

    Normalization is deliberately narrow and deterministic: NFC, trim,
    collapse internal whitespace and Unicode case-fold. It is not semantic or
    near-duplicate matching and it grants no evidence/Canon authority.
    """
    text = unicodedata.normalize("NFC", text).strip()
    text = re.sub(r"\s+", " ", text)
    return text.casefold()


def normalized_ingest_id(text: str) -> str:
    """Return the canonical auto-ingest fact id for exact normalized content."""
    norm = normalize_claim(text)
    digest = hashlib.md5(norm.encode("utf-8"), usedforsecurity=False).hexdigest()
    return "ing:" + digest[:12]
