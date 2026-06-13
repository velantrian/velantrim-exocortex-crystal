# core/invariant_check.py
# Velantrim ExoCortex — Read-Only Machine-Executable Invariant Checker
#
# Verifies selected epistemic invariants over the current canonical (L3) state.
# Does not write to memory, does not call TruthGate, does not modify receipts.
#
# Output: machine-readable JSON report with status (PASS/FAIL/WARN) and issues.
# Exit codes (via exit_code()): 0=PASS, 1=WARN, 2=FAIL.

import datetime
from typing import Any, Callable, Dict, List, Optional

from core import refusal_reasons as _rr

# ─── Vocabulary constants (match the repo's actual enums) ────────────────────
_SOURCE_LLM = "LLM_OUTPUT"
_TS_VERIFIED = "VERIFIED"

# ─── Check IDs ───────────────────────────────────────────────────────────────
ID_NO_LLM_VERIFIED = "no_llm_output_verified"
ID_VERIFIED_SOURCE = "verified_requires_source"
ID_VERIFIED_EVIDENCE = "verified_requires_evidence"
ID_RECEIPT_INTEGRITY = "receipt_integrity"
ID_NO_L3_BYPASS = "no_direct_l3_bypass"


def _check(
    check_id: str, status: str, violations: int, why: str, reason_code: str = ""
) -> Dict[str, Any]:
    d: Dict[str, Any] = {
        "id": check_id, "status": status, "violations": violations, "why": why,
    }
    if reason_code:
        d["reason_code"] = reason_code
    return d


def _issue(
    check_id: str, severity: str, fact_id: str, why: str, suggestion: str,
    reason_code: str = "",
) -> Dict[str, Any]:
    d: Dict[str, Any] = {
        "check_id": check_id,
        "severity": severity,
        "fact_id": fact_id,
        "why": why,
        "suggestion": suggestion,
    }
    if reason_code:
        d["reason_code"] = reason_code
    return d


def run_checks(
    facts: Optional[List[Dict[str, Any]]] = None,
    *,
    _has_evidence: Optional[Callable[[str], bool]] = None,
) -> Dict[str, Any]:
    """Run all invariant checks against the canonical (L3) state.

    Parameters
    ----------
    facts:
        Fact dicts to check. If None, fetched live from L3 via get_l3_graph().
        Pass an explicit list for isolated testing.
    _has_evidence:
        Injectable evidence-lookup for testing. Defaults to core.evidence.has_evidence.

    Returns
    -------
    dict
        Machine-readable report: {status, checked_at, checks, issues}.
    """
    if facts is None:
        from core.l3_graph import get_l3_graph
        facts = get_l3_graph().all_facts()

    if _has_evidence is None:
        from core.evidence import has_evidence
        _has_evidence = has_evidence

    checked_at = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    checks: List[Dict[str, Any]] = []
    issues: List[Dict[str, Any]] = []

    # ── Check 1: no_llm_output_verified ──────────────────────────────────────
    # No VERIFIED claim may have source_status == LLM_OUTPUT.
    llm_v = [
        f.get("fact_id", "(unknown)")
        for f in facts
        if f.get("truth_status") == _TS_VERIFIED
        and f.get("source_status") == _SOURCE_LLM
    ]
    if llm_v:
        checks.append(_check(
            ID_NO_LLM_VERIFIED, "FAIL", len(llm_v),
            "A VERIFIED claim must not have source_status=LLM_OUTPUT.",
            reason_code=_rr.LLM_OUTPUT_NOT_EVIDENCE,
        ))
        for fid in llm_v:
            issues.append(_issue(
                ID_NO_LLM_VERIFIED, "ERROR", fid,
                "truth_status=VERIFIED but source_status=LLM_OUTPUT",
                "Demote to UNVERIFIED or attach external evidence and review.",
                reason_code=_rr.LLM_OUTPUT_NOT_EVIDENCE,
            ))
    else:
        checks.append(_check(
            ID_NO_LLM_VERIFIED, "PASS", 0,
            "No VERIFIED claim is sourced only from LLM_OUTPUT.",
        ))

    # ── Check 2: verified_requires_source ────────────────────────────────────
    # Every VERIFIED claim must have a non-empty source field.
    src_v = [
        f.get("fact_id", "(unknown)")
        for f in facts
        if f.get("truth_status") == _TS_VERIFIED
        and not (f.get("source") or "").strip()
    ]
    if src_v:
        checks.append(_check(
            ID_VERIFIED_SOURCE, "FAIL", len(src_v),
            "Every VERIFIED claim must have a non-empty source field.",
            reason_code=_rr.MISSING_SOURCE,
        ))
        for fid in src_v:
            issues.append(_issue(
                ID_VERIFIED_SOURCE, "ERROR", fid,
                "truth_status=VERIFIED but source is absent or empty",
                "Attach a source label or demote to UNVERIFIED.",
                reason_code=_rr.MISSING_SOURCE,
            ))
    else:
        checks.append(_check(
            ID_VERIFIED_SOURCE, "PASS", 0,
            "All VERIFIED claims carry a non-empty source field.",
        ))

    # ── Check 3: verified_requires_evidence (evidence-span sub-check only) ───
    # Receipt-linkage is SKIPPED_UNSUPPORTED — no global receipt registry in L3.
    ev_v = [
        f["fact_id"]
        for f in facts
        if f.get("truth_status") == _TS_VERIFIED
        and f.get("fact_id")
        and not _has_evidence(f["fact_id"])
    ]
    if ev_v:
        checks.append(_check(
            ID_VERIFIED_EVIDENCE, "FAIL", len(ev_v),
            "VERIFIED claims should carry at least one source-span evidence record. "
            "(Receipt-linkage sub-check is SKIPPED_UNSUPPORTED — no global receipt registry.)",
            reason_code=_rr.MISSING_EVIDENCE,
        ))
        for fid in ev_v:
            issues.append(_issue(
                ID_VERIFIED_EVIDENCE, "WARN", fid,
                "truth_status=VERIFIED but no source-span evidence record found",
                "Attach evidence via 'velantrim learn' with an external sourced file.",
                reason_code=_rr.MISSING_EVIDENCE,
            ))
    else:
        checks.append(_check(
            ID_VERIFIED_EVIDENCE, "PASS", 0,
            "All VERIFIED claims carry at least one source-span evidence record. "
            "(Receipt-linkage sub-check is SKIPPED_UNSUPPORTED — no global receipt registry.)",
        ))

    # ── Check 4: receipt_integrity — SKIPPED_UNSUPPORTED ─────────────────────
    checks.append(_check(
        ID_RECEIPT_INTEGRITY, "SKIPPED_UNSUPPORTED", 0,
        "No global receipt registry in L3. "
        "Use 'velantrim verify-receipt <file>' to replay individual receipts.",
        reason_code=_rr.UNSUPPORTED_SCHEMA_CHECK,
    ))

    # ── Check 5: no_direct_l3_bypass — SKIPPED_UNSUPPORTED ───────────────────
    checks.append(_check(
        ID_NO_L3_BYPASS, "SKIPPED_UNSUPPORTED", 0,
        "Audit log captures compliance events (erase/restrict) but not L3 write events. "
        "Structural enforcement is provided by TruthGate and Guardian at write time.",
        reason_code=_rr.UNSUPPORTED_SCHEMA_CHECK,
    ))

    overall = _aggregate_status({c["status"] for c in checks})
    return {
        "status": overall,
        "checked_at": checked_at,
        "checks": checks,
        "issues": issues,
    }


def _aggregate_status(statuses: set) -> str:
    """Derive overall status from the set of individual check statuses."""
    if "FAIL" in statuses:
        return "FAIL"
    if statuses == {"SKIPPED_UNSUPPORTED"}:
        return "WARN"
    return "PASS"


def exit_code(status: str) -> int:
    """Map report status to CLI exit code (0=PASS, 1=WARN, 2=FAIL)."""
    if status == "FAIL":
        return 2
    if status == "WARN":
        return 1
    return 0
