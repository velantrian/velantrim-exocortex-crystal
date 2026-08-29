# core/compliance.py
# Velantrim ExoCortex — GDPR-oriented compliance operations
#
# Two accountability operations not related to deletion (Art. 17 → erasure.py):
#
#   Art. 18 — restriction of processing. restrict_processing() "freezes" a fact:
#     it is stored, but excluded from active processing (recall/answers; see
#     pipeline.retrieve, the node['restricted'] filter). Reversible via
#     unrestrict_processing(). Not a deletion and not an ESM state change.
#
#   Art. 30 — record of processing. record_of_processing() builds an aggregate,
#     content-free processing report: counters by category, restrictions,
#     deletions, backends, data location. Personal data (claim) is NOT
#     included — only metadata and identifiers.

import os
from collections import Counter
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

from core.memory import (
    set_restricted, get_fact, get_all_facts, get_tombstones,
    l3_secondary_sync_admissible,
)
from core.l3_graph import get_l3_graph
from core import crypto, audit, pii


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sync_restriction(fact_id: str) -> bool:
    """Best-effort L3 sync; authoritative L1 restriction must survive outages."""
    fact = get_fact(fact_id)
    if fact is None or not l3_secondary_sync_admissible(fact):
        return False
    try:
        get_l3_graph().merge_fact(fact)
    except Exception:
        # L1 is the authoritative processing-restriction boundary. A secondary
        # graph outage must not roll back or hide that deny-dominant state; the
        # graph can be reconciled by a later retry without resurrecting access.
        return False
    return True


def restrict_processing(
    fact_id: str, *, reason: str = "data_subject_request", actor: str = "operator"
) -> Dict[str, Any]:
    """
    Restrict processing of a fact (GDPR Art. 18): the fact stays in memory, but
    is excluded from recall/answers. Returns a receipt; found=False if the
    fact does not exist.
    """
    found = set_restricted(fact_id, True)
    if found:
        _sync_restriction(fact_id)
        audit.append_event("restrict", fact_id, {"reason": reason, "actor": actor})
    return {"fact_id": fact_id, "restricted": True, "found": found,
            "reason": reason, "actor": actor, "at": _now()}


def unrestrict_processing(
    fact_id: str, *, actor: str = "operator"
) -> Dict[str, Any]:
    """Lift the processing restriction (Art. 18): the fact takes part in recall again."""
    found = set_restricted(fact_id, False)
    if found:
        _sync_restriction(fact_id)
        audit.append_event("unrestrict", fact_id, {"actor": actor})
    return {"fact_id": fact_id, "restricted": False, "found": found,
            "actor": actor, "at": _now()}


def is_restricted(fact_id: str) -> bool:
    """True if processing of the fact is restricted (Art. 18)."""
    fact = get_fact(fact_id)
    return bool(fact and fact.get("restricted"))


def restricted_facts() -> List[str]:
    """fact_ids of all facts with a processing restriction."""
    return [f["fact_id"] for f in get_all_facts() if f.get("restricted")]


def record_of_processing(controller: Optional[str] = None) -> Dict[str, Any]:
    """
    Build a record of processing (GDPR Art. 30): an aggregate content-free
    processing report. Contains no personal data (claim) — only
    counters, identifiers and configuration.
    """
    facts = get_all_facts()
    by_claim_type = Counter(f.get("claim_type", "UNKNOWN") for f in facts)
    by_state = Counter(f.get("epistemic_state", "Observed") for f in facts)
    by_source_status = Counter(f.get("source_status", "UNKNOWN") for f in facts)
    restricted = [f["fact_id"] for f in facts if f.get("restricted")]
    erasures = get_tombstones()
    audit_status = audit.verify_audit_log()

    l3 = os.environ.get("VELANTRIM_L3_BACKEND", "auto")
    embedder = os.environ.get("VELANTRIM_EMBEDDER", "auto")
    generator = os.environ.get("VELANTRIM_GENERATOR", "extractive")
    transfers = (generator == "anthropic") or l3 == "neo4j"

    return {
        "generated_at": _now(),
        "regulation": "GDPR (EU) 2016/679, Art. 30",
        "controller": controller or os.environ.get(
            "VELANTRIM_CONTROLLER", "(operator-defined)"),
        "processing_purpose": (
            "Verifiable AI memory: storage and provenance-tracked retrieval "
            "of facts for trustworthy AI systems"),
        "data_location": (
            "local: L1 (SQLite) + L3 (embedded graph). No third-party transfer "
            "in the default configuration."),
        "backends": {"l3_graph": l3, "embedder": embedder, "generator": generator},
        "international_transfer": transfers,
        "encryption_at_rest": crypto.is_enabled(),
        "encryption_backend": crypto.backend_name(),
        "pii_redaction_at_ingest": pii.redaction_enabled(),
        "fact_count": len(facts),
        "categories_of_data": dict(by_claim_type),
        "by_epistemic_state": dict(by_state),
        "by_source_status": dict(by_source_status),
        "restricted_count": len(restricted),
        "restricted_fact_ids": restricted,
        "erasure_count": len(erasures),
        "erasure_log": erasures,
        "audit_log": {
            "entries": audit_status["length"],
            "tamper_evident": True,
            "integrity_verified": audit_status["ok"],
            "signed": audit_status["signed"],
        },
        "data_subject_rights": {
            "access": "get_all_facts() / CLI report",
            "rectification": "update_fact / reconcile.supersede (Art. 16)",
            "erasure": "erasure.erase_fact (Art. 17)",
            "restriction": "compliance.restrict_processing (Art. 18)",
            "portability": "SQLite + JSON export (Art. 20)",
            "data_minimisation": "pii.redact at ingest (Art. 5(1)(c))",
        },
        "security_measures": [
            "single-entry TruthGate (policy-constrained Canon admission, I1)",
            "Ring Zero immutability (I6)",
            "validated ESM transitions",
            "content-free erasure tombstones",
            "tamper-evident hash-chained audit log",
            "no telemetry; no outbound calls by default",
        ] + ([f"encryption at rest ({crypto.backend_name()}) on claim/metadata"]
             if crypto.is_enabled() else []),
    }
