# core/memory.py
# Velantrim ExoCortex — Memory Layer
# v8.7.0-sprint2
#
# Memory levels:
#   L0: LRU in-memory cache (CAP=5, OrderedDict)
#   L1: SQLite (short-term, persistent across runs)
#
# Full L0–L6 architecture: docs/Velantrim_V8_Crystal_Sprint1_toc.md
# ESM (Epistemic State Machine): 8 states of a fact's lifecycle.

import os
import sqlite3
import json
from collections import OrderedDict
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Dict, Optional

# ─── ESM: valid fact states ──────────────────────────────────────────
# Observed → Hypothesized → Supported → Validated → ImmutableCore
#                                    ↘ Contradicted → Deprecated → Collapsed
ESM_STATES = {
    "Observed",       # raw input, before classification
    "Hypothesized",   # accepted, not yet confirmed
    "Supported",      # there is evidence
    "Validated",      # verified by the TruthGate
    "Contradicted",   # conflict with another fact
    "Deprecated",     # obsolete
    "Collapsed",      # logically removed
    "ImmutableCore",  # immutable (Ring Zero)
}

# ─── ESM: matrix of valid transitions ────────────────────────────────────────
# MVP fast-path: Observed → Validated is allowed directly for the demo pipeline.
# I6: VALUES_CORE / RING_ZERO are protected in transition_esm, not via the matrix.
ESM_TRANSITIONS: Dict[str, set] = {
    "Observed":      {"Hypothesized", "Supported", "Validated", "Collapsed"},
    "Hypothesized":  {"Supported", "Validated", "Collapsed"},
    "Supported":     {"Validated", "Collapsed"},
    "Validated":     {"Contradicted", "ImmutableCore", "Collapsed"},
    "Contradicted":  {"Deprecated", "Collapsed"},
    "Deprecated":    {"Collapsed"},
    "Collapsed":     set(),
    "ImmutableCore": set(),
}

# ─── CLAIM TYPE: claim modality (axis orthogonal to ESM) ─────────────
# ESM answers "how verified", claim_type — "what kind of claim it is".
# WORLD_FACT is separated from FACT on purpose: "a fact about the external world", not "verified".
# A feeling is real as a feeling — EMOTION may become Validated, but NOT WORLD_FACT.
CLAIM_TYPES = {
    "WORLD_FACT",       # claim about the external world (requires evidence)
    "USER_EXPERIENCE",  # an event as the user experienced it
    "EMOTION",          # internal state / feeling
    "INTERPRETATION",   # inference / explanation (hypothesis)
    "OPINION",          # the user's opinion
    "GOAL",             # goal
    "PREFERENCE",       # preference
}
DEFAULT_CLAIM_TYPE = "WORLD_FACT"

# ─── SOURCE STATUS: origin of the claim (source monitoring) ─────────────
# Guard against source confusion: mixing up "saw / imagined / heard / inferred".
SOURCE_STATUSES = {
    "USER_REPORTED",  # reported by the user
    "OBSERVED",       # observed by the system
    "DERIVED",        # derived from other facts
    "EXTERNAL",       # external source / retrieval
    "LLM_OUTPUT",     # the model's answer — by itself NOT a fact about the world
    "UNKNOWN",
}
DEFAULT_SOURCE_STATUS = "UNKNOWN"

# claim_type for which the TruthGate does NOT require an evidentiary bar:
# they are valid as subjective experience, but not as a fact about the world.
SUBJECTIVE_CLAIM_TYPES = {
    "USER_EXPERIENCE", "EMOTION", "OPINION", "PREFERENCE", "GOAL",
}

# ─── RING ZERO / VALUES CORE: immutable facts (I6) ─────────────────────────
IMMUTABLE_FACT_IDS = {"VALUES_CORE", "RING_ZERO"}


class ImmutableStateError(Exception):
    """Raised when attempting to transition a Ring Zero / VALUES_CORE fact."""
    pass


# ─── L0: LRU cache (in-memory, lives only within the session) ─────────────────────────
L0_CAP = 5
_L0: OrderedDict = OrderedDict()

# ─── L1: SQLite path ──────────────────────────────────────────────────────────
SQLITE_PATH = "./data/velantrim_memory.db"

_DDL = """
    CREATE TABLE IF NOT EXISTS facts (
        fact_id        TEXT PRIMARY KEY,
        claim          TEXT NOT NULL,
        source         TEXT NOT NULL,
        confidence     REAL DEFAULT 0.5,
        epistemic_state TEXT DEFAULT 'Observed',
        claim_type     TEXT DEFAULT 'WORLD_FACT',
        source_status  TEXT DEFAULT 'UNKNOWN',
        significance   REAL DEFAULT 0.5,
        created_at     TEXT NOT NULL,
        updated_at     TEXT NOT NULL,
        metadata       TEXT DEFAULT '{}',
        restricted     INTEGER DEFAULT 0
    )
"""

# ─── L3 OUTBOX: persistent queue for re-merging into the canon ────────────────────────
# L3 (canon) and SQLite (pending) do not share a transaction. If a merge into L3 fails
# (backend unavailable), the fact stays Validated in SQLite without a node in the graph. The outbox
# makes this self-healing: the failed fact is enqueued and idempotently
# re-merged on the next access (drain), instead of waiting for a retry of the same request.
_OUTBOX_DDL = """
    CREATE TABLE IF NOT EXISTS l3_outbox (
        fact_id     TEXT PRIMARY KEY,
        enqueued_at TEXT NOT NULL
    )
"""

# ─── ERASURE LOG: tombstones of physical deletion (GDPR Art. 17 / Art. 30) ────
# Contains PROOF of the deletion without the personal data itself: the claim
# is not stored, only its sha256 hash. This way deletion stays accountable
# (record of processing, Art. 30) without recreating what was erased (right to erasure,
# Art. 17). A tombstone record is immutable: the first deletion is recorded forever.
_TOMBSTONE_DDL = """
    CREATE TABLE IF NOT EXISTS erasure_log (
        fact_id      TEXT PRIMARY KEY,
        erased_at    TEXT NOT NULL,
        reason       TEXT NOT NULL,
        actor        TEXT NOT NULL,
        content_hash TEXT
    )
"""

# ─── Migration: columns added after the first schema release ────────────────
# CREATE TABLE IF NOT EXISTS does not touch an already existing DB, so old
# velantrim_memory.db files must be brought up to date via ALTER TABLE ADD COLUMN (idempotent).
_MIGRATIONS = [
    ("claim_type",    "TEXT DEFAULT 'WORLD_FACT'"),
    ("source_status", "TEXT DEFAULT 'UNKNOWN'"),
    ("significance",  "REAL DEFAULT 0.5"),
    ("restricted",    "INTEGER DEFAULT 0"),  # GDPR Art. 18 (processing restriction)
]


def _migrate(conn) -> None:
    """Add missing columns to the existing facts table (idempotent)."""
    existing = {row["name"] for row in conn.execute("PRAGMA table_info(facts)")}
    for column, ddl in _MIGRATIONS:
        if column not in existing:
            conn.execute(f"ALTER TABLE facts ADD COLUMN {column} {ddl}")


@contextmanager
def _db():
    """Connection per operation — no global state, no database-is-locked."""
    db_dir = os.path.dirname(SQLITE_PATH)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)
    conn = sqlite3.connect(SQLITE_PATH)
    conn.row_factory = sqlite3.Row
    # WAL: the writer does not block readers (better concurrency for evidence/audit).
    # It is a property of the DB file — set once and persisted; repeating it is harmless.
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute(_DDL)
    conn.execute(_OUTBOX_DDL)
    conn.execute(_TOMBSTONE_DDL)
    _migrate(conn)
    conn.commit()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


# ─── L0 helpers ───────────────────────────────────────────────────────────────

def _l0_put(fact_id: str, record: Dict) -> None:
    """Insert into L0 LRU cache, evict oldest entry when over capacity."""
    if fact_id in _L0:
        del _L0[fact_id]
    _L0[fact_id] = record
    if len(_L0) > L0_CAP:
        _L0.popitem(last=False)  # evict least-recently-used


def _l0_get(fact_id: str) -> Optional[Dict]:
    """Return from L0, refreshing recency. Returns None on miss."""
    if fact_id not in _L0:
        return None
    _L0.move_to_end(fact_id)
    return _L0[fact_id]


# ─── API ───────────────────────────────────────────────────────────────────────

def store_fact(fact: Dict) -> None:
    """
    Store a fact in L0 (LRU RAM) and L1 (SQLite).
    Initial ESM state: Observed.
    A direct write to the L3 graph — only via the TruthGate (not here).
    """
    fact_id = fact.get("fact_id")
    if not fact_id:
        raise ValueError("store_fact: fact_id is required")

    now = datetime.now(timezone.utc).isoformat()
    epistemic_state = fact.get("epistemic_state", "Observed")

    if epistemic_state not in ESM_STATES:
        raise ValueError(f"store_fact: invalid ESM state '{epistemic_state}'")

    claim_type = fact.get("claim_type", DEFAULT_CLAIM_TYPE)
    if claim_type not in CLAIM_TYPES:
        raise ValueError(f"store_fact: invalid claim_type '{claim_type}'")

    source_status = fact.get("source_status", DEFAULT_SOURCE_STATUS)
    if source_status not in SOURCE_STATUSES:
        raise ValueError(f"store_fact: invalid source_status '{source_status}'")

    metadata_dict = fact.get("metadata", {})

    record = {
        "fact_id":         fact_id,
        "claim":           fact.get("claim", ""),
        "source":          fact.get("source", "unknown"),
        "confidence":      round(float(fact.get("confidence", 0.5)), 4),
        "epistemic_state": epistemic_state,
        "claim_type":      claim_type,
        "source_status":   source_status,
        "significance":    round(float(fact.get("significance", 0.5)), 4),
        "created_at":      now,
        "updated_at":      now,
        "metadata":        metadata_dict,
    }

    _l0_put(fact_id, record)

    l1_record = {**record, "metadata": json.dumps(metadata_dict)}
    with _db() as conn:
        conn.execute("""
            INSERT INTO facts
                (fact_id, claim, source, confidence, epistemic_state,
                 claim_type, source_status, significance,
                 created_at, updated_at, metadata)
            VALUES
                (:fact_id, :claim, :source, :confidence, :epistemic_state,
                 :claim_type, :source_status, :significance,
                 :created_at, :updated_at, :metadata)
            ON CONFLICT(fact_id) DO UPDATE SET
                claim           = excluded.claim,
                source          = excluded.source,
                confidence      = excluded.confidence,
                epistemic_state = excluded.epistemic_state,
                claim_type      = excluded.claim_type,
                source_status   = excluded.source_status,
                significance    = excluded.significance,
                updated_at      = excluded.updated_at,
                metadata        = excluded.metadata
        """, l1_record)


def get_fact(fact_id: str) -> Optional[Dict]:
    """Get a fact: first L0 (LRU), then L1."""
    cached = _l0_get(fact_id)
    if cached is not None:
        return cached
    with _db() as conn:
        row = conn.execute(
            "SELECT * FROM facts WHERE fact_id = ?", (fact_id,)
        ).fetchone()
        if row:
            result = dict(row)
            result["metadata"] = json.loads(result["metadata"])
            _l0_put(fact_id, result)
            return result
    return None


# ─── Columns that can be updated individually without changing the ESM state ─────────
_UPDATABLE = {"claim", "source", "confidence", "significance",
              "claim_type", "source_status", "metadata"}


def update_fact(fact_id: str, **fields) -> bool:
    """
    Update individual fields of a fact WITHOUT touching epistemic_state.
    Changing the ESM state — only via transition_esm. Returns True if the
    fact is found and updated.
    """
    fields = {k: v for k, v in fields.items() if k in _UPDATABLE}
    existing = get_fact(fact_id)
    if existing is None or not fields:
        return False

    now = datetime.now(timezone.utc).isoformat()
    sets, params = [], {"fact_id": fact_id, "updated_at": now}
    for key, value in fields.items():
        sets.append(f"{key} = :{key}")
        params[key] = json.dumps(value) if key == "metadata" else value

    with _db() as conn:
        conn.execute(
            f"UPDATE facts SET {', '.join(sets)}, updated_at = :updated_at "
            f"WHERE fact_id = :fact_id",
            params,
        )

    merged = {**existing, **fields, "updated_at": now}
    _l0_put(fact_id, merged)
    return True


def transition_esm(fact_id: str, new_state: str) -> bool:
    """
    Transition a fact to a new ESM state.
    A direct SET of epistemic_state bypassing this function is an architectural bug.
    """
    if new_state not in ESM_STATES:
        raise ValueError(f"transition_esm: invalid state '{new_state}'")

    if fact_id in IMMUTABLE_FACT_IDS:
        raise ImmutableStateError(
            f"transition_esm: fact '{fact_id}' is protected by Ring Zero (I6), "
            f"the transition to '{new_state}' is forbidden"
        )

    fact = get_fact(fact_id)
    if not fact:
        return False

    current_state = fact.get("epistemic_state", "Observed")
    allowed = ESM_TRANSITIONS.get(current_state)
    if allowed is not None and new_state not in allowed:
        raise ValueError(
            f"transition_esm: transition '{current_state}' → '{new_state}' is not allowed"
        )

    now = datetime.now(timezone.utc).isoformat()
    fact["epistemic_state"] = new_state
    fact["updated_at"] = now

    _l0_put(fact_id, fact)
    with _db() as conn:
        conn.execute(
            "UPDATE facts SET epistemic_state = ?, updated_at = ? WHERE fact_id = ?",
            (new_state, now, fact_id)
        )
    return True


def get_all_facts(epistemic_state: Optional[str] = None) -> list:
    """Get all facts from L1. Optionally — filtered by ESM state."""
    with _db() as conn:
        if epistemic_state:
            rows = conn.execute(
                "SELECT * FROM facts WHERE epistemic_state = ?",
                (epistemic_state,)
            ).fetchall()
        else:
            rows = conn.execute("SELECT * FROM facts").fetchall()
        result = []
        for row in rows:
            r = dict(row)
            r["metadata"] = json.loads(r["metadata"])
            result.append(r)
        return result


# ─── L3 OUTBOX API ────────────────────────────────────────────────────────────

def enqueue_l3_write(fact_id: str) -> None:
    """Enqueue a fact for re-merge into L3 (idempotent: upsert by fact_id)."""
    now = datetime.now(timezone.utc).isoformat()
    with _db() as conn:
        conn.execute(
            "INSERT INTO l3_outbox (fact_id, enqueued_at) VALUES (?, ?) "
            "ON CONFLICT(fact_id) DO UPDATE SET enqueued_at = excluded.enqueued_at",
            (fact_id, now),
        )


def pending_l3_writes() -> list:
    """fact_ids awaiting re-merge into L3 (in enqueue order)."""
    with _db() as conn:
        return [row["fact_id"] for row in conn.execute(
            "SELECT fact_id FROM l3_outbox ORDER BY enqueued_at, fact_id")]


def clear_l3_write(fact_id: str) -> None:
    """Remove a fact from the queue (after a successful merge or if it is no longer needed)."""
    with _db() as conn:
        conn.execute("DELETE FROM l3_outbox WHERE fact_id = ?", (fact_id,))


# ─── PROCESSING RESTRICTION (GDPR Art. 18) ─────────────────────────────────────
# restricted=1 means "the fact is stored but excluded from active processing"
# (recall/answers). This is NOT deletion and NOT an ESM state change: the fact stays
# valid but is temporarily "frozen". Reversible. Orchestration of the sync to L3 —
# in core/compliance.py (memory.py does not import l3_graph, to avoid a cycle).

def set_restricted(fact_id: str, restricted: bool) -> bool:
    """
    Set/clear the processing restriction on a fact (L0 + L1). Returns True if the
    fact is found. Does not touch the ESM state. Sync to L3 — on the caller's side.
    """
    existing = get_fact(fact_id)
    if existing is None:
        return False
    val = int(bool(restricted))
    now = datetime.now(timezone.utc).isoformat()
    with _db() as conn:
        conn.execute(
            "UPDATE facts SET restricted = ?, updated_at = ? WHERE fact_id = ?",
            (val, now, fact_id),
        )
    _l0_put(fact_id, {**existing, "restricted": val, "updated_at": now})
    return True


# ─── PHYSICAL DELETION (GDPR Art. 17) ───────────────────────────────────────
# Low-level primitives. Full deletion across all fabrics (L0/L1/L3/outbox) +
# tombstone is orchestrated in core/erasure.py — do not call delete_fact_l1 directly
# for GDPR deletion, otherwise a node will remain in L3 and there will be no tombstone.

def delete_fact_l1(fact_id: str) -> bool:
    """
    Physically delete a fact from L0 (LRU) and L1 (SQLite). Does not touch L3 or the tombstone.
    Returns True if the row in SQLite was actually deleted.
    """
    _L0.pop(fact_id, None)
    with _db() as conn:
        cur = conn.execute("DELETE FROM facts WHERE fact_id = ?", (fact_id,))
        return cur.rowcount > 0


def write_tombstone(
    fact_id: str, *, reason: str, actor: str, content_hash: Optional[str] = None
) -> None:
    """
    Write a deletion tombstone (idempotent, immutable: the first deletion
    is recorded forever). A repeated call does not overwrite the original record —
    there is a single deletion event. Personal data is NOT stored (only the hash).
    """
    now = datetime.now(timezone.utc).isoformat()
    with _db() as conn:
        conn.execute(
            "INSERT INTO erasure_log (fact_id, erased_at, reason, actor, content_hash) "
            "VALUES (?, ?, ?, ?, ?) ON CONFLICT(fact_id) DO NOTHING",
            (fact_id, now, reason, actor, content_hash),
        )


def get_tombstone(fact_id: str) -> Optional[Dict]:
    """Return the deletion tombstone by fact_id or None."""
    with _db() as conn:
        row = conn.execute(
            "SELECT * FROM erasure_log WHERE fact_id = ?", (fact_id,)
        ).fetchone()
        return dict(row) if row else None


def get_tombstones() -> list:
    """All deletion tombstones (the log, Art. 30). Without personal data."""
    with _db() as conn:
        return [dict(r) for r in conn.execute(
            "SELECT * FROM erasure_log ORDER BY erased_at, fact_id")]
