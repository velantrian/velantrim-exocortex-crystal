# core/memory.py
# Velantrim ExoCortex — Memory Layer
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
from typing import Any, Dict, Optional

from core import crypto  # field-level encryption at rest (GDPR Art. 32; off by default)

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


# ─── L3 secondary sync admissibility ─────────────────────────────────────────
# Pre-canonical facts must enter L3 only through TruthGate admission.
# Secondary sync paths (reinforce, restriction, outbox heal) may update L3
# metadata only for post-admission facts.

L3_PRE_CANONICAL_STATES = frozenset({"Observed", "Hypothesized", "Supported"})


def l3_secondary_sync_admissible(
    fact: Optional[Dict[str, Any]],
    *,
    graph: Any = None,
) -> bool:
    """Return True when a fact may be merged into L3 via a secondary sync path."""
    if fact is None:
        return False
    state = fact.get("epistemic_state", "Observed")
    if state in L3_PRE_CANONICAL_STATES:
        return False
    if state == "Validated":
        return True
    if state in {"Contradicted", "Deprecated", "ImmutableCore"}:
        from core.l3_graph import get_l3_graph
        g = graph if graph is not None else get_l3_graph()
        return g.get_fact(fact["fact_id"]) is not None
    return False


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
# VELANTRIM_DB redirects the L1 store (read at import time, like the other
# VELANTRIM_* backend variables). scripts/eval_gate.py and docs/DEMO.md rely on
# it to isolate the L1 database from real data.
SQLITE_PATH = os.environ.get("VELANTRIM_DB", "./data/velantrim_memory.db")

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

# ─── IMMUNE MEMORY: persistent CRISPR threat patterns (RFC0072) ───────────────
# Recorded "spacers" — claim signatures (hallucination/harmful/refuted patterns)
# that the Immune Guard recognises and blocks on sight (see core/immune.py).
# Content-addressable by normalized pattern; hit counters make the response
# observable. Empty by default → the guard is a no-op until something is recorded.
_IMMUNE_DDL = """
    CREATE TABLE IF NOT EXISTS immune_memory (
        pattern_id   TEXT PRIMARY KEY,
        pattern      TEXT NOT NULL,
        threat_type  TEXT NOT NULL,
        severity     REAL NOT NULL,
        recorded_at  TEXT NOT NULL,
        actor        TEXT NOT NULL,
        hits         INTEGER NOT NULL DEFAULT 0,
        last_hit_at  TEXT
    )
"""

# ─── NEUROCORE DELTA LOG: passive plasticity tracker (RFC0068, Phase 0) ───────
# NeuroCore is a plastic adaptation layer that, in later phases, updates an SSM
# model's weights during a dialogue. Phase 0 is PASSIVE: it only logs the norm of
# the would-be weight delta (ΔW) when surprise crosses the threshold — it never
# touches the model and NEVER writes to the L3 graph (invariant I68, Graph =
# Truth is absolute). This table is the Phase 0 observation log.
_NEUROCORE_DDL = """
    CREATE TABLE IF NOT EXISTS neurocore_delta_log (
        id             INTEGER PRIMARY KEY,
        timestamp      TEXT NOT NULL,
        surprise_score REAL NOT NULL,
        delta_norm     REAL NOT NULL,
        domain         TEXT NOT NULL,
        session_id     TEXT
    )
"""

# ─── EVIDENCE SPANS: source-span provenance for a fact (RFC0063 / WP1) ────────
# Links a canonical fact to where its claim came from — a source URI/file, an
# optional chunk and character span, the source content hash and the claim hash
# at attach time. Additive and content-light: the source TEXT is not stored, only
# hashes, so receipts can replay against exact source spans without re-exposing
# personal data. A fact may have many evidence spans (independent corroboration).
_EVIDENCE_DDL = """
    CREATE TABLE IF NOT EXISTS evidence_spans (
        evidence_id   TEXT PRIMARY KEY,
        fact_id       TEXT NOT NULL,
        source_uri    TEXT NOT NULL,
        source_kind   TEXT NOT NULL,
        chunk_id      TEXT,
        section       TEXT,
        span_start    INTEGER,
        span_end      INTEGER,
        source_sha256 TEXT,
        claim_sha256  TEXT NOT NULL,
        created_at    TEXT NOT NULL
    )
"""

# ─── IMPORT SESSIONS: batch provenance for knowledge imports (WP2) ────────────
# Each external import (a `learn` of a file/corpus) gets a session id; every fact
# it accepts is recorded here. This lets a whole batch be reviewed, restricted or
# erased together — important for institutions importing curated corpora.
_IMPORT_SESSION_DDL = """
    CREATE TABLE IF NOT EXISTS import_sessions (
        session_id  TEXT NOT NULL,
        fact_id     TEXT NOT NULL,
        source      TEXT NOT NULL,
        created_at  TEXT NOT NULL,
        PRIMARY KEY (session_id, fact_id)
    )
"""

# ─── REVIEW SESSIONS: resumable curator review batches ───────────────────────
# Stores session progress as fact-ID lists only — no claim text is copied into
# this table. The review queue (Observed facts in L1) is the source of truth;
# sessions track which IDs were included in a batch and which have been resolved.
_REVIEW_SESSION_DDL = """
    CREATE TABLE IF NOT EXISTS review_sessions (
        session_id     TEXT PRIMARY KEY,
        status         TEXT NOT NULL DEFAULT 'pending',
        batch_size     INTEGER,
        claim_ids      TEXT NOT NULL DEFAULT '[]',
        reviewed_ids   TEXT NOT NULL DEFAULT '[]',
        deferred_ids   TEXT NOT NULL DEFAULT '[]',
        approved_count INTEGER NOT NULL DEFAULT 0,
        rejected_count INTEGER NOT NULL DEFAULT 0,
        created_at     TEXT NOT NULL,
        updated_at     TEXT NOT NULL
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

# ─── AUDIT LOG: tamper-evident hash chain of compliance events (Art. 5(2)/24/30) ─
# Append-only ledger. Each row links to the previous via prev_hash and seals its
# own content in entry_hash = sha256(seq|ts|event|fact_id|detail|prev_hash), so
# editing, deleting or reordering any past entry is detectable (see core/audit).
# signature is an optional per-entry HMAC when VELANTRIM_AUDIT_KEY is configured.
_AUDIT_DDL = """
    CREATE TABLE IF NOT EXISTS audit_log (
        seq        INTEGER PRIMARY KEY,
        ts         TEXT NOT NULL,
        event      TEXT NOT NULL,
        fact_id    TEXT,
        detail     TEXT NOT NULL,
        prev_hash  TEXT NOT NULL,
        entry_hash TEXT NOT NULL,
        signature  TEXT
    )
"""

# ─── PROVENANCE CHAIN: per-fact, append-only lifecycle log (Sprint1 P1-5 / I89) ─
# A hash-chained log SCOPED TO ONE fact_id (distinct from the GLOBAL audit_log).
# Each row links to the previous row FOR THE SAME fact via prev_hash and seals
# its own content in hash = sha256(prev_hash|event_type|fact_id|from_state|
# to_state|payload_str|created_at|actor|reason), so editing, deleting or
# reordering any past entry of that fact is detectable (see core/provenance_chain).
# Content-light: payload_str holds a hash/marker, never the claim text.
# UNIQUE(fact_id, seq) prevents two appends writing the same position.
_PROVENANCE_CHAIN_DDL = """
    CREATE TABLE IF NOT EXISTS provenance_chain (
        id           INTEGER PRIMARY KEY AUTOINCREMENT,
        fact_id      TEXT NOT NULL,
        seq          INTEGER NOT NULL,
        event_type   TEXT NOT NULL,
        from_state   TEXT NOT NULL DEFAULT '',
        to_state     TEXT NOT NULL DEFAULT '',
        payload_str  TEXT NOT NULL DEFAULT '',
        created_at   TEXT NOT NULL,
        actor        TEXT NOT NULL DEFAULT 'system',
        reason       TEXT NOT NULL DEFAULT '',
        prev_hash    TEXT NOT NULL,
        hash         TEXT NOT NULL,
        UNIQUE(fact_id, seq)
    )
"""
_PROVENANCE_CHAIN_INDEX_DDL = (
    "CREATE INDEX IF NOT EXISTS idx_pc_fact_id "
    "ON provenance_chain(fact_id, seq)"
)

# ─── Migration: columns added after the first schema release ────────────────
# CREATE TABLE IF NOT EXISTS does not touch an already existing DB, so old
# velantrim_memory.db files must be brought up to date via ALTER TABLE ADD COLUMN (idempotent).
_MIGRATIONS = [
    ("claim_type",    "TEXT DEFAULT 'WORLD_FACT'"),
    ("source_status", "TEXT DEFAULT 'UNKNOWN'"),
    ("significance",  "REAL DEFAULT 0.5"),
    ("restricted",    "INTEGER DEFAULT 0"),  # GDPR Art. 18 (processing restriction)
]

# Columns added to evidence_spans after its first release (WP1 hardening, #61).
_EVIDENCE_MIGRATIONS = [
    ("section", "TEXT"),  # human-readable source location (heading/page/section)
]


def _migrate(conn) -> None:
    """Add missing columns to existing tables (idempotent)."""
    facts_cols = {row["name"] for row in conn.execute("PRAGMA table_info(facts)")}
    for column, ddl in _MIGRATIONS:
        if column not in facts_cols:
            conn.execute(f"ALTER TABLE facts ADD COLUMN {column} {ddl}")
    ev_cols = {row["name"] for row in conn.execute("PRAGMA table_info(evidence_spans)")}
    for column, ddl in _EVIDENCE_MIGRATIONS:
        if column not in ev_cols:
            conn.execute(f"ALTER TABLE evidence_spans ADD COLUMN {column} {ddl}")


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
    conn.execute(_IMMUNE_DDL)
    conn.execute(_NEUROCORE_DDL)
    conn.execute(_EVIDENCE_DDL)
    conn.execute(_IMPORT_SESSION_DDL)
    conn.execute(_REVIEW_SESSION_DDL)
    conn.execute(_TOMBSTONE_DDL)
    conn.execute(_AUDIT_DDL)
    conn.execute(_PROVENANCE_CHAIN_DDL)
    conn.execute(_PROVENANCE_CHAIN_INDEX_DDL)
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

    New facts: epistemic_state from the call is persisted and cached.
    Existing facts (conflict): epistemic_state is PRESERVED from the DB;
    other fields (claim, source, confidence, etc.) are still updated.
    Use transition_esm() to advance epistemic state explicitly.

    A direct write to the L3 graph is only via the TruthGate (not here).
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

    # Encrypt personal-data fields (claim, metadata) before they touch disk.
    # L0 keeps the plaintext record; only the L1/SQLite copy is encrypted at rest.
    l1_record = {
        **record,
        "claim":    crypto.encrypt(record["claim"]),
        "metadata": crypto.encrypt(json.dumps(metadata_dict)),
    }
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
                claim_type      = excluded.claim_type,
                source_status   = excluded.source_status,
                significance    = excluded.significance,
                updated_at      = excluded.updated_at,
                metadata        = excluded.metadata
        """, l1_record)
        # Re-read the persisted epistemic_state within the same connection so L0
        # is never poisoned with the incoming value when this is a conflict-update
        # (the ON CONFLICT clause intentionally omits epistemic_state, preserving
        # the existing row's state). For new inserts this returns the incoming
        # state unchanged. Mirrors the "L0 after DB write" discipline in
        # transition_esm().
        row = conn.execute(
            "SELECT epistemic_state FROM facts WHERE fact_id = ?", (fact_id,)
        ).fetchone()
        persisted_state = row["epistemic_state"] if row else epistemic_state

    record["epistemic_state"] = persisted_state
    _l0_put(fact_id, record)


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
            result["claim"] = crypto.decrypt(result["claim"])
            result["metadata"] = json.loads(crypto.decrypt(result["metadata"]))
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
        if key == "metadata":
            params[key] = crypto.encrypt(json.dumps(value))  # encrypt at rest
        elif key == "claim":
            params[key] = crypto.encrypt(value)              # encrypt at rest
        else:
            params[key] = value

    with _db() as conn:
        conn.execute(
            f"UPDATE facts SET {', '.join(sets)}, updated_at = :updated_at "  # nosec B608 — keys from _UPDATABLE allowlist
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

    # CAS guard: only transition if the persisted state still equals the state we
    # read (current_state). If a competing/external write changed it since the
    # L0/DB read, the UPDATE matches 0 rows and we abort instead of clobbering.
    # Defense-in-depth for future concurrency/async — NOT a full atomicity guarantee.
    with _db() as conn:
        cur = conn.execute(
            "UPDATE facts SET epistemic_state = ?, updated_at = ? "
            "WHERE fact_id = ? AND epistemic_state = ?",
            (new_state, now, fact_id, current_state)
        )
        if cur.rowcount != 1:
            # CAS miss: a competing/external write changed the persisted state
            # since our read. Evict the now-stale L0 entry so the next get_fact()
            # re-reads the fresh DB state instead of serving stale cache to a
            # caller that ignores the return value. Defense-in-depth, not atomicity.
            _L0.pop(fact_id, None)
            return False

    # Update L0 only after the DB write succeeds, so the cache is never poisoned
    # with a state that did not persist.
    fact["epistemic_state"] = new_state
    fact["updated_at"] = now
    _l0_put(fact_id, fact)
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
            r["claim"] = crypto.decrypt(r["claim"])
            r["metadata"] = json.loads(crypto.decrypt(r["metadata"]))
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


# ─── Review session storage ───────────────────────────────────────────────────

def _rs_to_dict(row) -> Dict:
    d = dict(row)
    d["claim_ids"] = json.loads(d["claim_ids"])
    d["reviewed_ids"] = json.loads(d["reviewed_ids"])
    d["deferred_ids"] = json.loads(d["deferred_ids"])
    return d


def save_review_session(session: Dict[str, Any]) -> None:
    """Upsert a review session record (ID + progress metadata, no claim text)."""
    now = datetime.now(timezone.utc).isoformat()
    with _db() as conn:
        conn.execute(
            """INSERT INTO review_sessions
               (session_id, status, batch_size, claim_ids, reviewed_ids,
                deferred_ids, approved_count, rejected_count, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(session_id) DO UPDATE SET
                 status         = excluded.status,
                 reviewed_ids   = excluded.reviewed_ids,
                 deferred_ids   = excluded.deferred_ids,
                 approved_count = excluded.approved_count,
                 rejected_count = excluded.rejected_count,
                 updated_at     = excluded.updated_at
            """,
            (
                session["session_id"],
                session.get("status", "pending"),
                session.get("batch_size"),
                json.dumps(session.get("claim_ids", [])),
                json.dumps(session.get("reviewed_ids", [])),
                json.dumps(session.get("deferred_ids", [])),
                session.get("approved_count", 0),
                session.get("rejected_count", 0),
                session.get("created_at", now),
                now,
            ),
        )


def get_review_session(session_id: str) -> Optional[Dict]:
    """Fetch one review session by ID, or None if not found."""
    with _db() as conn:
        row = conn.execute(
            "SELECT * FROM review_sessions WHERE session_id = ?", (session_id,)
        ).fetchone()
        return _rs_to_dict(row) if row else None


def list_review_sessions(status: Optional[str] = None) -> list:
    """List review sessions, newest first. Optionally filter by status."""
    with _db() as conn:
        if status is not None:
            rows = conn.execute(
                "SELECT * FROM review_sessions WHERE status = ? "
                "ORDER BY created_at DESC", (status,)
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM review_sessions ORDER BY created_at DESC"
            ).fetchall()
        return [_rs_to_dict(r) for r in rows]
