# core/audit.py
# Velantrim ExoCortex — Tamper-Evident Audit Log (GDPR Art. 5(2) / 24 / 30)
#
# An append-only, hash-chained ledger of compliance events (erase / restrict /
# unrestrict). Each entry seals its own content and links to the previous one:
#
#   entry_hash = sha256(seq | ts | event | fact_id | detail | prev_hash)
#
# Because every entry commits to the previous entry's hash, editing, deleting or
# reordering an entry breaks its hash or a surviving link. A durable checkpoint
# in the same transaction pins the latest seq/hash so deleting the event-table
# tail is also detected by verify_audit_log(). This makes the erasure (Art. 17) and
# restriction (Art. 18) registers accountable: you can demonstrate the log has
# not been altered ("integrity and confidentiality", Art. 5(2)(f); accountability,
# Art. 5(2) / 24).
#
# Signing (optional): when VELANTRIM_AUDIT_KEY is set, each entry also carries an
# HMAC-SHA256 signature. The hash chain alone is tamper-EVIDENT (an attacker who
# rewrites the whole chain leaves a consistent-but-different head); the HMAC
# prevents forging signed entry content without the key. Off by default.
# Same-database checkpoints do not detect rollback/replacement of the entire DB;
# that requires an externally held checkpoint or backup.
#
# The log is content-free: detail holds reasons/actors/hashes, never the claim.

import os
import json
import hmac
import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

from core import memory

_GENESIS = "0" * 64
_ENV_AUDIT_KEY = "VELANTRIM_AUDIT_KEY"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _audit_key() -> Optional[bytes]:
    value = os.environ.get(_ENV_AUDIT_KEY)
    return value.encode("utf-8") if value else None


def _entry_hash(seq: int, ts: str, event: str, fact_id: Optional[str],
                detail_json: str, prev_hash: str) -> str:
    blob = f"{seq}|{ts}|{event}|{fact_id}|{detail_json}|{prev_hash}"
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def _sign(entry_hash: str, key: Optional[bytes] = None) -> Optional[str]:
    key = key if key is not None else _audit_key()
    if key is None:
        return None
    return hmac.new(key, entry_hash.encode("utf-8"), hashlib.sha256).hexdigest()


def append_event(
    event: str, fact_id: Optional[str], detail: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Append a compliance event to the tamper-evident audit chain. Returns a
    receipt with the assigned seq and entry_hash. detail must be content-free
    (reasons/actors/hashes — never personal data).
    """
    detail_json = json.dumps(detail or {}, sort_keys=True, ensure_ascii=False)
    ts = _now()

    def _write():
        with memory._db() as conn:
            # BEGIN IMMEDIATE acquires the write lock before the tail read, so
            # a concurrent append_event() call (e.g. two /review/approve
            # requests in FastAPI's thread pool) cannot read the same
            # `last seq` and race to insert the same seq — the second caller
            # blocks here until the first transaction commits, then sees the
            # updated tail. call_with_lock_retry covers contention that
            # surfaces later in this block (INSERT / implicit commit).
            memory.begin_immediate(conn)
            last = conn.execute(
                "SELECT seq, entry_hash FROM audit_log ORDER BY seq DESC LIMIT 1"
            ).fetchone()
            checkpoint = conn.execute(
                "SELECT seq, head_hash FROM chain_checkpoints "
                "WHERE chain_name = 'audit' AND scope_id = ''"
            ).fetchone()
            if checkpoint is None and last is not None:
                raise RuntimeError("audit chain checkpoint missing")
            if checkpoint is not None and (
                last is None
                or checkpoint["seq"] != last["seq"]
                or checkpoint["head_hash"] != last["entry_hash"]
            ):
                raise RuntimeError("audit chain checkpoint mismatch")
            prev_hash = last["entry_hash"] if last else _GENESIS
            seq = (last["seq"] + 1) if last else 1
            entry_hash = _entry_hash(seq, ts, event, fact_id, detail_json, prev_hash)
            signature = _sign(entry_hash)
            conn.execute(
                "INSERT INTO audit_log "
                "(seq, ts, event, fact_id, detail, prev_hash, entry_hash, signature) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (seq, ts, event, fact_id, detail_json, prev_hash, entry_hash, signature),
            )
            if checkpoint is None:
                conn.execute(
                    "INSERT INTO chain_checkpoints "
                    "(chain_name, scope_id, seq, head_hash) "
                    "VALUES ('audit', '', ?, ?)",
                    (seq, entry_hash),
                )
            else:
                conn.execute(
                    "UPDATE chain_checkpoints SET seq = ?, head_hash = ? "
                    "WHERE chain_name = 'audit' AND scope_id = ''",
                    (seq, entry_hash),
                )
            return seq, entry_hash, signature

    seq, entry_hash, signature = memory.call_with_lock_retry(_write)
    return {"seq": seq, "ts": ts, "event": event, "fact_id": fact_id,
            "entry_hash": entry_hash, "signed": signature is not None}


def audit_log() -> List[Dict[str, Any]]:
    """All audit entries in order (content-free)."""
    with memory._db() as conn:
        rows = conn.execute("SELECT * FROM audit_log ORDER BY seq").fetchall()
    out = []
    for r in rows:
        d = dict(r)
        d["detail"] = json.loads(d["detail"])
        out.append(d)
    return out


def verify_audit_log() -> Dict[str, Any]:
    """
    Verify the integrity of the audit chain.

    Recomputes every entry hash, checks the prev_hash links and seq sequence,
    then compares the replayed tail with the transactionally pinned checkpoint.
    If a signing key is configured and entries are signed, also verifies the
    HMACs. Returns:
      ok          — chain (and signatures, if checked) intact
      length      — number of entries
      broken_at   — seq of the first bad entry, or None
      error       — reason for the break, or None
      checkpointed— a pinned head exists (required for a non-empty chain)
      signed      — every entry carries a signature
      verified    — signatures were present and checked against the key
    """
    key = _audit_key()
    with memory._db() as conn:
        conn.execute("BEGIN")
        rows = conn.execute("SELECT * FROM audit_log ORDER BY seq").fetchall()
        checkpoint = conn.execute(
            "SELECT seq, head_hash FROM chain_checkpoints "
            "WHERE chain_name = 'audit' AND scope_id = ''"
        ).fetchone()

    prev = _GENESIS
    expected_seq = 1
    signed_all = len(rows) > 0
    checked_sigs = False

    def fail(seq, error):
        return {"ok": False, "length": len(rows), "broken_at": seq,
                "error": error, "checkpointed": checkpoint is not None,
                "signed": signed_all, "verified": checked_sigs}

    for r in rows:
        if r["seq"] != expected_seq:
            return fail(r["seq"], "sequence gap or reordering")
        if r["prev_hash"] != prev:
            return fail(r["seq"], "prev_hash link mismatch")
        recomputed = _entry_hash(
            r["seq"], r["ts"], r["event"], r["fact_id"], r["detail"], r["prev_hash"])
        if recomputed != r["entry_hash"]:
            return fail(r["seq"], "entry_hash mismatch (content altered)")
        if r["signature"] is None:
            signed_all = False
        elif key is not None:
            checked_sigs = True
            if not hmac.compare_digest(r["signature"], _sign(r["entry_hash"], key)):
                return fail(r["seq"], "signature mismatch")
        prev = r["entry_hash"]
        expected_seq += 1

    if checkpoint is None and rows:
        return fail(expected_seq, "chain checkpoint missing")
    if checkpoint is not None and (
        checkpoint["seq"] != len(rows) or checkpoint["head_hash"] != prev
    ):
        return fail(checkpoint["seq"], "checkpoint mismatch (tail truncated or replaced)")

    return {"ok": True, "length": len(rows), "broken_at": None, "error": None,
            "checkpointed": checkpoint is not None,
            "signed": signed_all, "verified": checked_sigs}
