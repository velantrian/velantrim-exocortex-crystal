# core/refusal_reasons.py
# Velantrim ExoCortex — Refusal Reasons Taxonomy v0.1
#
# Stable, machine-readable reason codes for why Crystal refuses to treat a
# claim as VERIFIED.  Pure stdlib; no runtime imports.
#
# API:
#   get_reason(code)     → dict  (raises KeyError if unknown)
#   is_valid_reason(code) → bool
#   list_reasons()       → list[dict]  (defensive copies)
#   format_reason(code)  → str  "[SEVERITY] CODE: description"

from typing import Dict, List

SEVERITIES: frozenset = frozenset({"INFO", "WARN", "ERROR", "CRITICAL"})

_REASONS: List[Dict] = [
    {
        "code": "NO_VERIFIED_CLAIM",
        "title": "No VERIFIED claim present",
        "severity": "INFO",
        "description": (
            "The requested fact does not exist in the canonical store "
            "with truth_status=VERIFIED."
        ),
        "suggestion": (
            "Ingest the fact via TruthGate with external evidence before "
            "requesting VERIFIED status."
        ),
    },
    {
        "code": "LLM_OUTPUT_NOT_EVIDENCE",
        "title": "LLM output is not admissible evidence",
        "severity": "ERROR",
        "description": (
            "The only evidence for this claim is LLM-generated text "
            "(source_status=LLM_OUTPUT).  LLM output is not admissible as "
            "verification evidence."
        ),
        "suggestion": (
            "Attach an external source (document, URL, user-confirmed record) "
            "or demote the claim to UNVERIFIED."
        ),
    },
    {
        "code": "MISSING_SOURCE",
        "title": "No source field",
        "severity": "ERROR",
        "description": (
            "The claim carries truth_status=VERIFIED but has no non-empty "
            "source field.  Provenance is required for VERIFIED status."
        ),
        "suggestion": (
            "Supply a source label that identifies the originating document "
            "or data origin, or demote to UNVERIFIED."
        ),
    },
    {
        "code": "MISSING_PROVENANCE",
        "title": "Provenance chain incomplete",
        "severity": "WARN",
        "description": (
            "The claim has a source field but the provenance chain cannot be "
            "traced end-to-end.  One or more intermediate links are absent."
        ),
        "suggestion": (
            "Re-ingest the fact through TruthGate with a complete provenance "
            "chain, or downgrade to UNVERIFIED."
        ),
    },
    {
        "code": "MISSING_EVIDENCE",
        "title": "No source-span evidence record",
        "severity": "WARN",
        "description": (
            "The claim is marked VERIFIED but no source-span evidence record "
            "is attached.  Evidence spans are required to ground verification."
        ),
        "suggestion": (
            "Run 'velantrim learn' with an externally sourced file to attach "
            "evidence spans, or demote to UNVERIFIED."
        ),
    },
    {
        "code": "MISSING_TRACE",
        "title": "No epistemic trace",
        "severity": "WARN",
        "description": (
            "No epistemic trace (ESM state history) is available for this "
            "claim.  The path to VERIFIED cannot be audited."
        ),
        "suggestion": (
            "Re-ingest the fact through the standard TruthGate write path "
            "to produce a traceable ESM transition."
        ),
    },
    {
        "code": "RECEIPT_TAMPERED",
        "title": "Receipt integrity check failed",
        "severity": "CRITICAL",
        "description": (
            "The sealed receipt for this claim failed integrity verification. "
            "The digest or signature does not match the stored answer."
        ),
        "suggestion": (
            "Run 'velantrim verify-receipt <file>' for details. "
            "Do not promote this claim. Investigate the source of tampering."
        ),
    },
    {
        "code": "CONTRADICTION_UNRESOLVED",
        "title": "Unresolved contradiction",
        "severity": "ERROR",
        "description": (
            "This claim directly contradicts one or more other claims in the "
            "canonical store, and no resolution has been recorded."
        ),
        "suggestion": (
            "Resolve the contradiction via the review queue before promoting "
            "to VERIFIED status."
        ),
    },
    {
        "code": "UNSUPPORTED_SCHEMA_CHECK",
        "title": "Check not supported by current schema",
        "severity": "INFO",
        "description": (
            "The requested invariant check cannot be evaluated because the "
            "current schema or audit log does not expose the required fields."
        ),
        "suggestion": (
            "This is a SKIPPED_UNSUPPORTED result, not a PASS. "
            "No action required, but the invariant is not verified."
        ),
    },
    {
        "code": "TRUTHGATE_REJECTED",
        "title": "TruthGate rejected the claim",
        "severity": "ERROR",
        "description": (
            "TruthGate evaluated the claim and returned a rejection. "
            "The claim did not satisfy one or more verification criteria."
        ),
        "suggestion": (
            "Review the TruthGate rejection details in the audit log. "
            "Correct the evidence or source before re-submitting."
        ),
    },
    {
        "code": "GUARDIAN_BLOCKED",
        "title": "Guardian blocked the write",
        "severity": "CRITICAL",
        "description": (
            "Crystal's Guardian policy engine blocked the write operation. "
            "The claim violates a configured policy constraint (e.g. "
            "personal data handling rules)."
        ),
        "suggestion": (
            "Review the Guardian policy that triggered the block. "
            "Adjust the claim data or the policy as appropriate."
        ),
    },
    {
        "code": "REQUIRES_HUMAN_REVIEW",
        "title": "Human review required",
        "severity": "WARN",
        "description": (
            "This claim has been placed in the review queue and requires "
            "explicit human confirmation before it can be promoted to VERIFIED."
        ),
        "suggestion": (
            "Complete the human review step in the review queue "
            "('velantrim review-queue')."
        ),
    },
    {
        "code": "OUT_OF_SCOPE",
        "title": "Claim type out of scope",
        "severity": "INFO",
        "description": (
            "The claim type or domain is outside the scope of what Crystal "
            "can verify in this configuration.  No applicable check exists."
        ),
        "suggestion": (
            "Use an appropriate external verification tool for this claim type, "
            "or record the claim as UNVERIFIED."
        ),
    },
]

# Build index once at import time.
_INDEX: Dict[str, Dict] = {r["code"]: r for r in _REASONS}

# ─── Code constants for import-friendly access ───────────────────────────────
NO_VERIFIED_CLAIM = "NO_VERIFIED_CLAIM"
LLM_OUTPUT_NOT_EVIDENCE = "LLM_OUTPUT_NOT_EVIDENCE"
MISSING_SOURCE = "MISSING_SOURCE"
MISSING_PROVENANCE = "MISSING_PROVENANCE"
MISSING_EVIDENCE = "MISSING_EVIDENCE"
MISSING_TRACE = "MISSING_TRACE"
RECEIPT_TAMPERED = "RECEIPT_TAMPERED"
CONTRADICTION_UNRESOLVED = "CONTRADICTION_UNRESOLVED"
UNSUPPORTED_SCHEMA_CHECK = "UNSUPPORTED_SCHEMA_CHECK"
TRUTHGATE_REJECTED = "TRUTHGATE_REJECTED"
GUARDIAN_BLOCKED = "GUARDIAN_BLOCKED"
REQUIRES_HUMAN_REVIEW = "REQUIRES_HUMAN_REVIEW"
OUT_OF_SCOPE = "OUT_OF_SCOPE"


def get_reason(code: str) -> Dict:
    """Return a copy of the reason dict for *code*.

    Raises KeyError for unknown codes.
    """
    return dict(_INDEX[code])


def is_valid_reason(code: str) -> bool:
    """Return True if *code* is a known refusal reason code."""
    return code in _INDEX


def list_reasons() -> List[Dict]:
    """Return a list of all reason dicts (defensive copies)."""
    return [dict(r) for r in _REASONS]


def format_reason(code: str) -> str:
    """Return a single-line human-readable summary for *code*.

    Format: "[SEVERITY] CODE: description"

    Raises KeyError for unknown codes.
    """
    r = _INDEX[code]
    return f"[{r['severity']}] {r['code']}: {r['description']}"
