# core/api_ingest_policy.py
# Epistemic policy for the optional HTTP /ingest surface.
#
# Default API ingest treats utterances as USER_REPORTED. Privileged
# source_status values (EXTERNAL/DERIVED/OBSERVED) require explicit import
# mode, declared evidence references in metadata, and
# VELANTRIM_API_PRIVILEGED_INGEST=1. Refs are not validated against the
# evidence span store and evidence.attach_evidence() is not called.

import os
from typing import Any, Dict, List, Optional

PRIVILEGED_SOURCE_STATUSES = frozenset({"EXTERNAL", "DERIVED", "OBSERVED"})


def privileged_ingest_enabled() -> bool:
    return os.environ.get("VELANTRIM_API_PRIVILEGED_INGEST", "") == "1"


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

    Privileged ingest stores declared evidence_refs in metadata only; it does
    not validate URIs or attach evidence records.
    """
    refs = [r.strip() for r in (evidence_refs or []) if r and str(r).strip()]
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
                "admission_path": "api_privileged_import",
            },
        }
    if source_status is not None and source_status not in {
            "USER_REPORTED", "LLM_OUTPUT"}:
        raise ValueError(
            f"unsupported source_status for public API ingest: {source_status!r}"
        )
    return {"source_status": source_status or "USER_REPORTED"}
