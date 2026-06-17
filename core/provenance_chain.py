# core/provenance_chain.py
# Velantrim ExoCortex — Per-Fact Provenance Chain (Sprint1 P1-5, invariant I89)
#
# An append-only, hash-chained lifecycle log SCOPED TO A SINGLE FACT. Where
# core/audit.py is a GLOBAL compliance ledger and core/provenance.py seals a
# single ANSWER (a receipt), this chain records the ordered lifecycle events of
# one fact: how it entered, was verified, promoted, restricted or erased.
#
# Each entry seals its own content and links to the previous entry FOR THE SAME
# fact_id:
#
#   hash = sha256(prev_hash | event_type | fact_id | from_state | to_state
#                 | payload_str | created_at | actor | reason)
#
# Because every entry commits to the previous entry's hash, editing, deleting or
# reordering ANY past entry of that fact changes its hash and breaks every link
# after it — verify() detects this. This realises invariant I89
# (ProvenanceAppendOnly): the per-fact provenance chain is append-only.
#
# The chain is content-light: payload_str holds a hash/short marker, never the
# claim text itself (the same discipline as the audit log).
#
# append() NEVER raises: it returns True on success and False on any failure, so
# that callers on a critical path (e.g. erase_fact, GDPR Art. 17) are never
# disturbed by a provenance-write problem. The erasure must complete even if the
# chain insert fails.

import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

from core import memory

# Per-fact chains start from this genesis link (same convention as core/audit.py).
_GENESIS = "0" * 64


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _compute_hash(
    prev_hash: str,
    event_type: str,
    fact_id: str,
    from_state: str,
    to_state: str,
    payload_str: str,
    created_at: str,
    actor: str = "system",
    reason: str = "",
) -> str:
    """
    Seal one provenance event. All fields participate in the hash, so tampering
    with ANY of them — including `actor` or `reason` — is detectable on replay.
    """
    blob = "|".join([
        prev_hash, event_type, fact_id, from_state, to_state,
        payload_str, created_at, actor, reason,
    ])
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


class ProvenanceChain:
    """
    Append-only, per-fact, hash-chained provenance log.

    Stateless wrapper over the `provenance_chain` SQLite table (one connection
    per operation, like core/audit.py) — no instance state to keep in sync.
    """

    def append(
        self,
        *,
        fact_id: str,
        event_type: str,
        from_state: str = "",
        to_state: str = "",
        payload_str: str = "",
        actor: str = "system",
        reason: str = "",
    ) -> bool:
        """
        Append one lifecycle event to this fact's chain.

        Reads the current tail (max seq for this fact_id), links the new entry to
        it, seals the entry and inserts it. Returns True on success, False on ANY
        failure — it never raises, so a critical-path caller (erase_fact) is not
        disturbed by a provenance-write problem.
        """
        created_at = _now()
        try:
            with memory._db() as conn:
                last = conn.execute(
                    "SELECT seq, hash FROM provenance_chain "
                    "WHERE fact_id = ? ORDER BY seq DESC LIMIT 1",
                    (fact_id,),
                ).fetchone()
                prev_hash = last["hash"] if last else _GENESIS
                seq = (last["seq"] + 1) if last else 1
                entry_hash = _compute_hash(
                    prev_hash, event_type, fact_id, from_state, to_state,
                    payload_str, created_at, actor, reason)
                conn.execute(
                    "INSERT INTO provenance_chain "
                    "(fact_id, seq, event_type, from_state, to_state, "
                    " payload_str, created_at, actor, reason, prev_hash, hash) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (fact_id, seq, event_type, from_state, to_state,
                     payload_str, created_at, actor, reason, prev_hash, entry_hash),
                )
            return True
        except Exception:
            return False

    def chain(self, fact_id: str) -> List[Dict[str, Any]]:
        """All provenance entries for a fact, in order (content-light)."""
        with memory._db() as conn:
            rows = conn.execute(
                "SELECT * FROM provenance_chain WHERE fact_id = ? ORDER BY seq",
                (fact_id,),
            ).fetchall()
        return [dict(r) for r in rows]

    def verify(self, fact_id: str) -> Dict[str, Any]:
        """
        Verify the integrity of one fact's provenance chain.

        An EMPTY chain is reported as `status="empty_chain", ok=False` — the
        absence of recorded provenance is NEVER equivalent to a verified
        non-empty chain (`status="ok"`). A non-empty chain is replayed: every
        entry hash is recomputed and the prev_hash links and seq order checked.

        Returns:
          fact_id    — the fact queried
          status     — "empty_chain" | "ok" | "tampered"
          ok         — True only for an intact non-empty chain
          length     — number of entries
          broken_at  — seq of the first bad entry, or None
          error      — reason for the break, or None
        """
        rows = self.chain(fact_id)
        if not rows:
            return {"fact_id": fact_id, "status": "empty_chain", "ok": False,
                    "length": 0, "broken_at": None, "error": "no_events"}

        prev = _GENESIS
        expected_seq = 1

        def fail(seq: int, error: str) -> Dict[str, Any]:
            return {"fact_id": fact_id, "status": "tampered", "ok": False,
                    "length": len(rows), "broken_at": seq, "error": error}

        for r in rows:
            if r["seq"] != expected_seq:
                return fail(r["seq"], "sequence gap or reordering")
            if r["prev_hash"] != prev:
                return fail(r["seq"], "prev_hash link mismatch")
            recomputed = _compute_hash(
                r["prev_hash"], r["event_type"], r["fact_id"], r["from_state"],
                r["to_state"], r["payload_str"], r["created_at"], r["actor"],
                r["reason"])
            if recomputed != r["hash"]:
                return fail(r["seq"], "hash mismatch (content altered)")
            prev = r["hash"]
            expected_seq += 1

        return {"fact_id": fact_id, "status": "ok", "ok": True,
                "length": len(rows), "broken_at": None, "error": None}
