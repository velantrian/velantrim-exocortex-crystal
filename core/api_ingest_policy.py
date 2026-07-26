# core/api_ingest_policy.py
# Epistemic policy for the optional HTTP /ingest surface.
#
# Default API ingest treats utterances as USER_REPORTED. Privileged
# source_status values (EXTERNAL/DERIVED/OBSERVED) require explicit import
# mode, declared evidence references in metadata, and
# VELANTRIM_API_PRIVILEGED_INGEST=1.
#
# IMPORTANT: this module validates the *shape* of evidence references only.
# Admission code must not interpret a syntactically valid reference as proof
# that the underlying source exists or supports the claim. Resolution and
# EvidenceSpan attachment remain a separate trust-boundary operation.

import os
from typing import Any, Dict, List, Optional
from urllib.parse import urlsplit

PRIVILEGED_SOURCE_STATUSES = frozenset({"EXTERNAL", "DERIVED", "OBSERVED"})
_MAX_EVIDENCE_REFS = 32
_MAX_EVIDENCE_REF_LENGTH = 2048
_ALLOWED_URI_SCHEMES = frozenset({"file", "http", "https", "urn"})


def privileged_ingest_enabled() -> bool:
    return os.environ.get("VELANTRIM_API_PRIVILEGED_INGEST", "") == "1"


def _normalize_evidence_refs(evidence_refs: Optional[List[str]]) -> List[str]:
    """Return bounded, unique evidence references or raise ValueError.

    The API previously accepted arbitrary objects via ``str(value)`` and kept
    duplicate, control-character-bearing, or unbounded references. Besides
    producing noisy provenance metadata, that allowed log/terminal injection
    and oversized metadata records at the privileged admission boundary.

    This function deliberately performs syntax validation only. It does not
    claim that a URI is reachable, immutable, or evidentially sufficient.
    """
    refs: List[str] = []
    seen = set()
    for raw in evidence_refs or []:
        if not isinstance(raw, str):
            raise ValueError("evidence_refs entries must be strings")
        ref = raw.strip()
        if not ref:
            continue
        if len(ref) > _MAX_EVIDENCE_REF_LENGTH:
            raise ValueError(
                f"evidence reference exceeds {_MAX_EVIDENCE_REF_LENGTH} characters"
            )
        if any(ord(ch) < 32 or ord(ch) == 127 for ch in ref):
            raise ValueError("evidence reference contains control characters")

        parsed = urlsplit(ref)
        if parsed.scheme and parsed.scheme.lower() not in _ALLOWED_URI_SCHEMES:
            raise ValueError(f"unsupported evidence URI scheme: {parsed.scheme!r}")
        if parsed.scheme in {"http", "https"} and not parsed.netloc:
            raise ValueError("HTTP evidence reference requires a host")
        if parsed.scheme == "file" and not parsed.path:
            raise ValueError("file evidence reference requires a path")

        if ref not in seen:
            refs.append(ref)
            seen.add(ref)
        if len(refs) > _MAX_EVIDENCE_REFS:
            raise ValueError(f"at most {_MAX_EVIDENCE_REFS} evidence references are allowed")
    return refs


def resolve_api_ingest(
    *,
    source_status: Optional[str],
    import_mode: bool = False,
    evidence_refs: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Validate and normalize API ingest parameters.

    Returns kwargs fragment for ingest(): source_status and optional metadata.
    Raises ValueError when privileged source_status is requested without the
    full import-mode contract.

    Privileged ingest stores validated declarations in metadata only. A caller
    must still resolve those declarations and attach real EvidenceSpan records
    before treating the fact as externally verified.
    """
    refs = _normalize_evidence_refs(evidence_refs)
    if source_status in PRIVILEGED_SOURCE_STATUSES:
        if not (privileged_ingest_enabled() and import_mode and refs):
            raise ValueError(
                f"privileged source_status {source_status!r} requires "
                "import_mode=true, non-empty evidence_refs, and "
                "VELANTRIM_API_PRIVILEGED_INGEST=1"
            )
        return {
            "source_status": source_status,
            "metadata": {
                "import_mode": True,
                "evidence_refs": refs,
                "evidence_resolution": "DECLARED_NOT_RESOLVED",
                "admission_path": "api_privileged_import",
            },
        }
    if source_status is not None and source_status not in {
            "USER_REPORTED", "LLM_OUTPUT"}:
        raise ValueError(
            f"unsupported source_status for public API ingest: {source_status!r}"
        )
    return {"source_status": source_status or "USER_REPORTED"}
