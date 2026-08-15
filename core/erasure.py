# core/erasure.py
# Velantrim ExoCortex — Right to Erasure (GDPR Art. 17)
#
# Physical deletion of a fact across all memory fabrics + accountability.
#
# Principle: deletion must be COMPLETE and PROVABLE at the same time.
#   Complete — the node disappears from L0 (cache), L1 (SQLite), L3 (canon: node + edges +
#             mentions), the L3 outbox (re-merge queue), evidence_spans,
#             import_sessions, and the derived normalized-ingest compatibility
#             index. No personal data or dangling references remain anywhere.
#   Provable — a content-free tombstone is written to erasure_log: fact_id, time,
#             reason, actor and the sha256 hash of the erased claim (not the claim itself). This is a
#             record of processing (Art. 30): one can prove WHAT and WHEN was
#             deleted without recreating what was erased (Art. 17).
#
# Ring Zero / VALUES_CORE are NOT deleted (invariant I6): these are system values,
# not personal data; deleting them would break the system.

import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

from core.memory import (
    get_fact,
    delete_fact_l1,
    delete_import_session_entries_for,
    write_tombstone,
    get_tombstone,
    get_tombstones,
    IMMUTABLE_FACT_IDS,
    ImmutableStateError,
)
from core.l3_graph import get_l3_graph
from core.queue import get_outbox_queue
from core.normalized_ingest_index import remove_fact as remove_normalized_ingest_mapping
from core import audit
from core import evidence
from core.provenance_chain import ProvenanceChain

# Provenance edge: derived -DERIVED_FROM-> source. Marks that a fact is derived
# from another. Used by cascade deletion: erasing the source can also erase
# everything derived from it (GDPR Art. 17 — derived personal data).
REL_DERIVED_FROM = "DERIVED_FROM"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _hash_claim(claim: str) -> str:
    """Hash of the erased claim — proof without storing the content."""
    return "sha256:" + hashlib.sha256(claim.encode("utf-8")).hexdigest()


def record_derivation(derived_id: str, source_id: str) -> None:
    """
    Record that fact derived_id is derived from source_id (a DERIVED_FROM edge).
    Then a cascade deletion of source_id can also erase derived_id.
    """
    get_l3_graph().add_edge(
        derived_id, REL_DERIVED_FROM, source_id, {"at": _now()})


def erase_fact(
    fact_id: str,
    *,
    reason: str = "data_subject_request",
    actor: str = "operator",
    cascade: bool = False,
    _visited: Optional[set] = None,
) -> Dict[str, Any]:
    """
    Physically and irreversibly delete a fact (GDPR Art. 17, right to be forgotten).

    Removes the fact from L0, L1, the L3 canonical graph (node + all edges + mentions),
    the L3 outbox, evidence_spans, import_sessions, and the derived exact-normalized
    ingest compatibility index, then writes a content-free tombstone to erasure_log.

    cascade=True: besides the fact itself, also erases everything derived from it —
    facts with a DERIVED_FROM edge to it (recursively, with cycle protection). This way
    derived personal data does not survive the deletion of the source.

    Ring Zero / VALUES_CORE are non-deletable (I6) → ImmutableStateError.

    Idempotent: a repeated deletion of an already erased fact returns
    erased_now=False, the tombstone is not duplicated (the first deletion is recorded).

    Returns a receipt with the details of the operation.
    """
    if fact_id in IMMUTABLE_FACT_IDS:
        raise ImmutableStateError(
            f"erase_fact: '{fact_id}' is protected by Ring Zero (I6) and cannot be deleted"
        )

    visited = _visited if _visited is not None else set()
    visited.add(fact_id)

    graph = get_l3_graph()
    fact = get_fact(fact_id)
    l3_node = graph.get_fact(fact_id)
    # Delete evidence/import-session pointers and any derived normalized-id
    # mapping BEFORE the no-op check below. The compatibility index is a
    # rebuildable lookup cache and is intentionally not folded into `erased_now`
    # or used as proof that canonical/personal data existed.
    evidence_removed = evidence.delete_evidence_for(fact_id)
    import_sessions_removed = delete_import_session_entries_for(fact_id)
    remove_normalized_ingest_mapping(fact_id)

    # A fact_id that was never stored anywhere — L1 (fact), L3 (l3_node),
    # evidence_spans, OR import_sessions — AND was never previously erased is
    # a true no-op: skip the tombstone/audit/provenance writes entirely.
    # Doing otherwise would fabricate an Art. 30 erasure record for personal
    # data that was never present. Checking L3 too (not just L1 via get_fact)
    # matters for an L3-only orphan — e.g. a node left behind by a partial
    # write failure — which must still be deleted, not silently skipped. A
    # fact_id that WAS previously erased (fact and l3_node are both None
    # because it is already gone, but a tombstone exists) still falls
    # through to the idempotent path below, unchanged.
    if (fact is None and l3_node is None and not evidence_removed
            and not import_sessions_removed and get_tombstone(fact_id) is None):
        return {
            "fact_id": fact_id,
            "erased_now": False,
            "l1_removed": False,
            "l3_removed": False,
            "evidence_removed": 0,
            "import_sessions_removed": 0,
            "reason": reason,
            "actor": actor,
            "content_hash": None,
            "erased_at": None,
        }

    if fact and fact.get("claim"):
        content_hash = _hash_claim(fact["claim"])
    elif l3_node and l3_node.get("claim"):
        content_hash = _hash_claim(l3_node["claim"])
    else:
        content_hash = None

    # Who to cascade-erase — collected BEFORE deletion (deletion removes the edges).
    derived_ids: List[str] = []
    if cascade:
        derived_ids = [e["source"]
                       for e in graph.incoming_edges(fact_id, REL_DERIVED_FROM)]

    # Deletion across all fabrics. Each step is idempotent and independent.
    # (evidence_spans, import_sessions and the derived compatibility mapping
    # were already deleted above, before the no-op check.)
    l1_removed = delete_fact_l1(fact_id)
    l3_removed = graph.erase_fact(fact_id)
    get_outbox_queue().clear(fact_id)  # remove any possible entry from the re-merge queue

    erased_now = l1_removed or l3_removed or bool(evidence_removed) or bool(import_sessions_removed)

    # The tombstone is immutable: on a repeated deletion the original hash is preserved.
    write_tombstone(fact_id, reason=reason, actor=actor, content_hash=content_hash)
    tombstone = get_tombstone(fact_id)

    # Record the event in the tamper-evident audit chain (Art. 5(2)/24/30). Content-free.
    audit.append_event("erase", fact_id, {
        "reason": reason, "actor": actor,
        "content_hash": content_hash, "erased_now": erased_now})

    # Also record an "erase" event on this fact's per-fact provenance chain
    # (Sprint1 P1-5 / I89). Additive and non-blocking: append() never raises, so
    # a provenance-write problem cannot prevent the erasure from completing.
    ProvenanceChain().append(
        fact_id=fact_id, event_type="erase",
        from_state=(fact.get("epistemic_state", "") if fact else ""),
        to_state="erased", payload_str=(content_hash or ""),
        actor=actor, reason=reason)

    receipt: Dict[str, Any] = {
        "fact_id": fact_id,
        "erased_now": erased_now,
        "l1_removed": l1_removed,
        "l3_removed": l3_removed,
        "evidence_removed": evidence_removed,
        "import_sessions_removed": import_sessions_removed,
        "reason": reason,
        "actor": actor,
        "content_hash": (tombstone or {}).get("content_hash"),
        "erased_at": (tombstone or {}).get("erased_at", _now()),
    }

    if cascade:
        cascaded = []
        for d in derived_ids:
            if d in visited or d in IMMUTABLE_FACT_IDS:
                continue
            cascaded.append(erase_fact(
                d, reason=f"cascade_from:{fact_id}", actor=actor,
                cascade=True, _visited=visited))
        receipt["cascaded"] = cascaded
    return receipt


def is_erased(fact_id: str) -> bool:
    """True if a tombstone exists for the fact (it was erased)."""
    return get_tombstone(fact_id) is not None


def erasure_log() -> List[Dict[str, Any]]:
    """
    Log of all deletions (Art. 30, record of processing). Content-free:
    contains fact_id / time / reason / actor / hash, but no personal data.
    """
    return get_tombstones()
