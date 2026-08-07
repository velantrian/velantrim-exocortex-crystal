"""Crash-consistent curator decision journal.

SQLite is the authoritative decision boundary: candidate/target L1 state,
decision metadata, tamper-evident audit proof and durable L3 projection intent
commit together. The physically separate graph is projected idempotently after
that transaction.

The journal is content-light. It stores ids, bounded policy/error metadata and
curator reason/note fields already permitted by the audit contract; it never
stores claim or source text in operator health records.
"""
from __future__ import annotations

import hashlib
import json
import threading
from datetime import datetime, timezone
from typing import Any, Callable, Iterable, Mapping, Optional

from core import audit, crypto, memory

_DECISION_DDL = """
CREATE TABLE IF NOT EXISTS review_decisions (
    decision_id       TEXT PRIMARY KEY,
    fact_id           TEXT NOT NULL,
    event             TEXT NOT NULL,
    payload           TEXT NOT NULL,
    projection_status TEXT NOT NULL,
    attempts          INTEGER NOT NULL DEFAULT 0,
    last_error        TEXT,
    created_at        TEXT NOT NULL,
    updated_at        TEXT NOT NULL,
    completed_at      TEXT
)
"""
_DECISION_INDEX_DDL = (
    "CREATE INDEX IF NOT EXISTS idx_review_decisions_status "
    "ON review_decisions(projection_status, created_at, decision_id)"
)
_DECISION_LOCK = threading.RLock()
_PROJECTION_STATUSES = frozenset({"pending", "completed", "failed", "blocked"})
_ERROR_MAX = 500


class DecisionConflict(RuntimeError):
    """A staged decision no longer matches current persisted state."""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _ensure_schema(conn) -> None:
    conn.execute(_DECISION_DDL)
    conn.execute(_DECISION_INDEX_DDL)


def _decode_row(row) -> dict[str, Any]:
    item = dict(row)
    item["payload"] = json.loads(item["payload"])
    return item


def make_decision_id(
    *,
    event: str,
    fact_id: str,
    expected_revision: int,
    actor: str,
    reason: Optional[str] = None,
    report_id: Optional[str] = None,
    target_ids: Iterable[str] = (),
    material: Optional[Mapping[str, Any]] = None,
) -> str:
    body = {
        "event": event,
        "fact_id": fact_id,
        "expected_revision": int(expected_revision),
        "actor": actor,
        "reason": reason,
        "report_id": report_id,
        "target_ids": sorted(dict.fromkeys(target_ids)),
        "material": dict(material or {}),
    }
    canonical = json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return "review:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _append_audit_event_conn(
    conn,
    *,
    event: str,
    fact_id: Optional[str],
    detail: Mapping[str, Any],
    ts: str,
) -> dict[str, Any]:
    detail_json = json.dumps(dict(detail), sort_keys=True, ensure_ascii=False)
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
    prev_hash = last["entry_hash"] if last else audit._GENESIS
    seq = (last["seq"] + 1) if last else 1
    entry_hash = audit._entry_hash(seq, ts, event, fact_id, detail_json, prev_hash)
    signature = audit._sign(entry_hash)
    conn.execute(
        "INSERT INTO audit_log "
        "(seq, ts, event, fact_id, detail, prev_hash, entry_hash, signature) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (seq, ts, event, fact_id, detail_json, prev_hash, entry_hash, signature),
    )
    if checkpoint is None:
        conn.execute(
            "INSERT INTO chain_checkpoints "
            "(chain_name, scope_id, seq, head_hash) VALUES ('audit', '', ?, ?)",
            (seq, entry_hash),
        )
    else:
        conn.execute(
            "UPDATE chain_checkpoints SET seq = ?, head_hash = ? "
            "WHERE chain_name = 'audit' AND scope_id = ''",
            (seq, entry_hash),
        )
    return {"seq": seq, "entry_hash": entry_hash}


def _validate_path(current_state: str, path: Iterable[str]) -> str:
    state = current_state
    for new_state in path:
        if new_state not in memory.ESM_STATES:
            raise DecisionConflict(f"invalid ESM target state {new_state!r}")
        allowed = memory.ESM_TRANSITIONS.get(state)
        if allowed is not None and new_state not in allowed:
            raise DecisionConflict(
                f"transition {state!r} -> {new_state!r} is no longer allowed"
            )
        state = new_state
    return state


def _read_metadata(row) -> dict[str, Any]:
    value = json.loads(crypto.decrypt(row["metadata"]))
    return dict(value) if isinstance(value, dict) else {}


def _guard_mutable_fact_id(fact_id: Any, *, role: str) -> str:
    if not isinstance(fact_id, str) or not fact_id:
        raise DecisionConflict(f"{role} fact id is invalid")
    if fact_id in memory.IMMUTABLE_FACT_IDS:
        raise DecisionConflict(f"{role} fact {fact_id!r} is immutable")
    return fact_id


def stage_review_decision(
    *,
    decision_id: str,
    fact_id: str,
    expected_revision: int,
    expected_state: str,
    candidate_path: Iterable[str],
    event: str,
    audit_detail: Mapping[str, Any],
    projection_builder: Optional[Callable[[tuple[str, ...]], Mapping[str, Any]]] = None,
    metadata_patch: Optional[Mapping[str, Any]] = None,
    target_transitions: Iterable[Mapping[str, Any]] = (),
    allow_partial_targets: bool = False,
) -> dict[str, Any]:
    try:
        fact_id = _guard_mutable_fact_id(fact_id, role="candidate")
    except DecisionConflict as exc:
        return {"ok": False, "created": False, "reason": str(exc)}
    if not isinstance(decision_id, str) or not decision_id:
        raise ValueError("decision_id must be a non-empty string")
    if not isinstance(event, str) or not event:
        raise ValueError("event must be a non-empty string")
    candidate_path = tuple(candidate_path)
    target_specs = [dict(item) for item in target_transitions]
    changed_ids: list[str] = [fact_id]
    for spec in target_specs:
        target_id = spec.get("fact_id")
        if isinstance(target_id, str) and target_id:
            changed_ids.append(target_id)

    def _write() -> dict[str, Any]:
        with memory._db() as conn:
            memory.begin_immediate(conn)
            _ensure_schema(conn)
            existing = conn.execute(
                "SELECT * FROM review_decisions WHERE decision_id = ?", (decision_id,)
            ).fetchone()
            if existing is not None:
                result = _decode_row(existing)
                if result["fact_id"] != fact_id or result["event"] != event:
                    raise DecisionConflict("decision idempotency key collision")
                result.update({"ok": True, "created": False})
                return result

            candidate = conn.execute(
                "SELECT * FROM facts WHERE fact_id = ?", (fact_id,)
            ).fetchone()
            if candidate is None:
                raise DecisionConflict("candidate no longer exists")
            if candidate["restricted"]:
                raise DecisionConflict("RESTRICTED_BY_POLICY")
            if candidate["epistemic_state"] != expected_state:
                raise DecisionConflict("ESM CAS conflict: candidate state changed concurrently")
            if int(candidate["revision"]) != int(expected_revision):
                raise DecisionConflict("ESM CAS conflict: candidate revision changed concurrently")
            final_candidate_state = _validate_path(candidate["epistemic_state"], candidate_path)

            partial_target_ids: list[str] = []
            applicable_targets: list[tuple[Mapping[str, Any], Any]] = []
            for spec in target_specs:
                target_id = _guard_mutable_fact_id(spec.get("fact_id"), role="target")
                target = conn.execute(
                    "SELECT * FROM facts WHERE fact_id = ?", (target_id,)
                ).fetchone()
                if target is None:
                    raise DecisionConflict(f"conflict target {target_id!r} no longer exists")
                if target["restricted"]:
                    raise DecisionConflict(f"conflict target {target_id!r} is restricted")
                matches = (
                    target["epistemic_state"] == spec.get("expected_state")
                    and int(target["revision"]) == int(spec.get("expected_revision"))
                )
                if not matches:
                    if allow_partial_targets:
                        partial_target_ids.append(target_id)
                        continue
                    raise DecisionConflict(f"conflict target {target_id!r} changed concurrently")
                _validate_path(target["epistemic_state"], tuple(spec.get("path") or ()))
                applicable_targets.append((spec, target))

            now = _now()
            metadata = _read_metadata(candidate)
            metadata.update(dict(metadata_patch or {}))
            cur = conn.execute(
                "UPDATE facts SET epistemic_state = ?, metadata = ?, "
                "revision = revision + 1, updated_at = ? "
                "WHERE fact_id = ? AND epistemic_state = ? AND revision = ? "
                "AND restricted = 0",
                (
                    final_candidate_state,
                    crypto.encrypt(json.dumps(metadata)),
                    now,
                    fact_id,
                    expected_state,
                    expected_revision,
                ),
            )
            if cur.rowcount != 1:
                raise DecisionConflict("ESM CAS conflict: candidate state changed concurrently")
            changed_ids.append(fact_id)

            for spec, target in applicable_targets:
                target_id = str(spec["fact_id"])
                current_state = target["epistemic_state"]
                revision = int(target["revision"])
                for new_state in tuple(spec.get("path") or ()):
                    cur = conn.execute(
                        "UPDATE facts SET epistemic_state = ?, revision = revision + 1, "
                        "updated_at = ? WHERE fact_id = ? AND epistemic_state = ? "
                        "AND revision = ? AND restricted = 0",
                        (new_state, now, target_id, current_state, revision),
                    )
                    if cur.rowcount != 1:
                        raise DecisionConflict(f"conflict target {target_id!r} changed concurrently")
                    current_state = new_state
                    revision += 1
                changed_ids.append(target_id)

            partial_tuple = tuple(sorted(dict.fromkeys(partial_target_ids)))
            projection = dict(projection_builder(partial_tuple)) if projection_builder else {}
            projection_status = "pending" if projection else "completed"
            detail = dict(audit_detail)
            detail.update(
                {
                    "decision_id": decision_id,
                    "projection_status": projection_status,
                    "partial_target_ids": list(partial_tuple),
                }
            )
            audit_receipt = _append_audit_event_conn(
                conn, event=event, fact_id=fact_id, detail=detail, ts=now
            )
            payload = {
                "version": 1,
                "audit": audit_receipt,
                "projection": projection,
                "partial_target_ids": list(partial_tuple),
            }
            completed_at = now if projection_status == "completed" else None
            conn.execute(
                "INSERT INTO review_decisions "
                "(decision_id, fact_id, event, payload, projection_status, attempts, "
                "last_error, created_at, updated_at, completed_at) "
                "VALUES (?, ?, ?, ?, ?, 0, NULL, ?, ?, ?)",
                (
                    decision_id,
                    fact_id,
                    event,
                    json.dumps(payload, sort_keys=True, ensure_ascii=False),
                    projection_status,
                    now,
                    now,
                    completed_at,
                ),
            )
            return {
                "ok": True,
                "created": True,
                "decision_id": decision_id,
                "fact_id": fact_id,
                "event": event,
                "payload": payload,
                "projection_status": projection_status,
                "attempts": 0,
                "last_error": None,
                "created_at": now,
                "updated_at": now,
                "completed_at": completed_at,
            }

    try:
        with audit._AUDIT_LOCK, _DECISION_LOCK, memory._FACTS_WRITE_LOCK:
            return memory.call_with_lock_retry(_write)
    except DecisionConflict as exc:
        return {"ok": False, "created": False, "reason": str(exc)}
    finally:
        for changed_id in dict.fromkeys(changed_ids):
            memory._l0_pop(changed_id)


def get_review_decision(decision_id: str) -> Optional[dict[str, Any]]:
    with memory._db() as conn:
        _ensure_schema(conn)
        row = conn.execute(
            "SELECT * FROM review_decisions WHERE decision_id = ?", (decision_id,)
        ).fetchone()
        return _decode_row(row) if row else None


def list_projection_work(limit: int = 100) -> list[dict[str, Any]]:
    if isinstance(limit, bool):
        raise ValueError("limit must be an integer")
    safe_limit = max(0, min(int(limit), 1000))
    with memory._db() as conn:
        _ensure_schema(conn)
        rows = conn.execute(
            "SELECT * FROM review_decisions "
            "WHERE projection_status IN ('pending', 'failed', 'blocked') "
            "ORDER BY created_at, decision_id LIMIT ?",
            (safe_limit,),
        ).fetchall()
        return [_decode_row(row) for row in rows]


def mark_projection_result(
    decision_id: str,
    *,
    status: str,
    error: Optional[str] = None,
) -> dict[str, Any]:
    if status not in _PROJECTION_STATUSES - {"pending"}:
        raise ValueError(f"unsupported projection status {status!r}")
    clean_error = str(error)[:_ERROR_MAX] if error else None

    def _write() -> dict[str, Any]:
        with memory._db() as conn:
            memory.begin_immediate(conn)
            _ensure_schema(conn)
            row = conn.execute(
                "SELECT * FROM review_decisions WHERE decision_id = ?", (decision_id,)
            ).fetchone()
            if row is None:
                raise KeyError(decision_id)
            current = _decode_row(row)
            if current["projection_status"] == "completed":
                return current
            now = _now()
            attempts = int(current["attempts"]) + 1
            completed_at = now if status == "completed" else None
            conn.execute(
                "UPDATE review_decisions SET projection_status = ?, attempts = ?, "
                "last_error = ?, updated_at = ?, completed_at = ? WHERE decision_id = ?",
                (status, attempts, clean_error, now, completed_at, decision_id),
            )
            _append_audit_event_conn(
                conn,
                event="review_projection_" + status,
                fact_id=current["fact_id"],
                detail={
                    "decision_id": decision_id,
                    "status": status,
                    "attempt": attempts,
                    "error": clean_error,
                },
                ts=now,
            )
            current.update(
                {
                    "projection_status": status,
                    "attempts": attempts,
                    "last_error": clean_error,
                    "updated_at": now,
                    "completed_at": completed_at,
                }
            )
            return current

    with audit._AUDIT_LOCK, _DECISION_LOCK:
        return memory.call_with_lock_retry(_write)


def projection_health() -> dict[str, Any]:
    with memory._db() as conn:
        _ensure_schema(conn)
        rows = conn.execute(
            "SELECT projection_status, COUNT(*) AS count "
            "FROM review_decisions GROUP BY projection_status"
        ).fetchall()
        counts = {status: 0 for status in sorted(_PROJECTION_STATUSES)}
        for row in rows:
            counts[row["projection_status"]] = row["count"]
        attention = [
            dict(row)
            for row in conn.execute(
                "SELECT decision_id, fact_id, event, projection_status, attempts, "
                "last_error, updated_at FROM review_decisions "
                "WHERE projection_status IN ('failed', 'blocked') "
                "ORDER BY updated_at DESC, decision_id LIMIT 20"
            )
        ]
    return {"counts": counts, "attention": attention}


__all__ = [
    "DecisionConflict",
    "get_review_decision",
    "list_projection_work",
    "make_decision_id",
    "mark_projection_result",
    "projection_health",
    "stage_review_decision",
]
