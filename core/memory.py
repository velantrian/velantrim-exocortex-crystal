# core/memory.py
# Velantrim ExoCortex — Memory Layer
#
# Memory levels:
#   L0: LRU in-memory cache (CAP=5, OrderedDict)
#   L1: SQLite (short-term, persistent across runs)
#
# Full L0–L6 architecture: docs/archive/Velantrim_V8_Crystal_Sprint1_toc.md
# ESM (Epistemic State Machine): 8 states of a fact's lifecycle.

import os
import sqlite3
import json
import threading
import time
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

# Once a fact has evidentiary support or has entered a terminal historical
# state, its text is its identity. Rewriting that text under the same fact_id
# would let evidence/validation for claim A silently describe claim B. Draft
# states (Observed/Hypothesized) may still be refined before promotion.
CLAIM_IDENTITY_LOCKED_STATES = {
    "Supported", "Validated", "ImmutableCore",
    "Contradicted", "Deprecated", "Collapsed",
}


class ImmutableStateError(Exception):
    """Raised when attempting to transition a Ring Zero / VALUES_CORE fact."""
    pass


class ClaimIdentityError(ValueError):
    """Raised when promoted/historical fact text is rewritten in place."""
    pass


# ─── L0: LRU cache (in-memory, lives only within the session) ─────────────────────────
# The L0 OrderedDict is shared module-level mutable state. The pipeline is run
# across worker threads (see core/aio.py asyncio.to_thread, and the FastAPI
# service layer), so every read/write/mutation of _L0 must hold _L0_LOCK — an
# unsynchronized OrderedDict under concurrent access raises "dictionary changed
# size during iteration"/KeyError and corrupts LRU order. Reentrant so a locked
# helper may safely call another. All access goes through _l0_put/_l0_get/_l0_pop.
L0_CAP = 5
_L0: OrderedDict = OrderedDict()
_L0_LOCK = threading.RLock()

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
# editing, deleting or reordering an entry is detectable (see core/audit).
# The chain_checkpoints row below also pins the latest seq/hash so deleting a
# contiguous suffix cannot make the shorter audit chain look valid.
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

# ─── CHAIN CHECKPOINTS: durable heads for suffix-truncation detection ────────
# A hash chain can detect an edit or a gap only while a later link survives.
# Deleting a contiguous suffix leaves the remaining prefix internally valid.
# This table pins the last committed seq/hash for the global audit chain and
# every per-fact provenance chain. Append operations advance the event row and
# its checkpoint in the same SQLite transaction; verification compares a full
# replay against the pinned head.
#
# This closes event-table tail deletion. It deliberately does not claim to
# detect rollback/replacement of the entire SQLite database or an attacker who
# can rewrite both event rows and checkpoints; that requires an externally held
# checkpoint/backup outside this database's trust boundary.
_CHAIN_CHECKPOINT_DDL = """
    CREATE TABLE IF NOT EXISTS chain_checkpoints (
        chain_name TEXT NOT NULL,
        scope_id   TEXT NOT NULL,
        seq        INTEGER NOT NULL CHECK(seq > 0),
        head_hash  TEXT NOT NULL,
        PRIMARY KEY (chain_name, scope_id)
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
    # Optimistic-CAS version token (#244 follow-up). Every writer of a facts row
    # (store_fact, update_fact, transition_esm, set_restricted) increments this
    # on each write. A monotonic integer cannot repeat a value for a given row
    # the way a wall-clock updated_at string in principle can (ABA risk) — see
    # update_fact()'s docstring for why this replaced an updated_at-based CAS.
    ("revision",      "INTEGER NOT NULL DEFAULT 0"),
]

# Columns added to evidence_spans after its first release (WP1 hardening, #61).
_EVIDENCE_MIGRATIONS = [
    ("section", "TEXT"),  # human-readable source location (heading/page/section)
]

# SQLite's PRAGMA user_version is the single schema-version marker for the L1
# database. Version 1 covers the revision CAS token added in #244; version 2
# adds durable audit/provenance chain checkpoints. Future schema changes must
# increment this value.
_SCHEMA_VERSION = 2

# Serializes first-open schema initialization within this process. The
# BEGIN IMMEDIATE inside _ensure_schema provides the corresponding
# cross-process serialization: a second process re-checks user_version only
# after the first process commits its migration.
_SCHEMA_INIT_LOCK = threading.Lock()


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

    # Establish a migration-time anchor for legacy non-empty chains. This can
    # only pin the tail present during migration; it cannot prove that an older
    # database was not truncated before version 2 first opened it.
    conn.execute(_CHAIN_CHECKPOINT_DDL)
    tables = {
        row["name"] for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        )
    }
    if "audit_log" in tables:
        conn.execute(
            "INSERT OR IGNORE INTO chain_checkpoints "
            "(chain_name, scope_id, seq, head_hash) "
            "SELECT 'audit', '', seq, entry_hash FROM audit_log "
            "ORDER BY seq DESC LIMIT 1"
        )
    if "provenance_chain" in tables:
        conn.execute(
            "INSERT OR IGNORE INTO chain_checkpoints "
            "(chain_name, scope_id, seq, head_hash) "
            "SELECT 'provenance', p.fact_id, p.seq, p.hash "
            "FROM provenance_chain AS p "
            "JOIN (SELECT fact_id, MAX(seq) AS seq FROM provenance_chain "
            "      GROUP BY fact_id) AS tail "
            "ON tail.fact_id = p.fact_id AND tail.seq = p.seq"
        )


def _schema_version(conn) -> int:
    """Return the SQLite schema version stored in PRAGMA user_version."""
    return int(conn.execute("PRAGMA user_version").fetchone()[0])


def _require_supported_schema(version: int) -> None:
    """Fail closed rather than opening a database created by newer code."""
    if version > _SCHEMA_VERSION:
        raise RuntimeError(
            f"database schema version {version} is newer than supported "
            f"version {_SCHEMA_VERSION}"
        )


def _ensure_schema(conn) -> None:
    """Create/migrate the L1 schema exactly once, safely under concurrency.

    The old connection-open path ran PRAGMA table_info followed by ALTER TABLE
    on every connection. Two threads opening a fresh or legacy database could
    both observe a missing column and then race to add it, making the loser
    fail with ``duplicate column name``. A process-local lock closes the thread
    race; BEGIN IMMEDIATE plus a version re-check closes the same race across
    multiple worker processes.
    """
    version = _schema_version(conn)
    _require_supported_schema(version)
    if version == _SCHEMA_VERSION:
        return

    with _SCHEMA_INIT_LOCK:
        # Another thread may have completed initialization while this caller
        # waited for the process-local lock.
        version = _schema_version(conn)
        _require_supported_schema(version)
        if version == _SCHEMA_VERSION:
            return

        # WAL is a persistent database-file property. Set it on the one
        # initialization path instead of making every read connection repeat
        # a journal-mode write.
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("BEGIN IMMEDIATE")
        try:
            # A different process may have migrated the file while this
            # process waited for SQLite's write lock. Re-check under the lock
            # before issuing any ALTER TABLE statement.
            version = _schema_version(conn)
            _require_supported_schema(version)
            if version < _SCHEMA_VERSION:
                for ddl in (
                    _DDL,
                    _OUTBOX_DDL,
                    _IMMUNE_DDL,
                    _NEUROCORE_DDL,
                    _EVIDENCE_DDL,
                    _IMPORT_SESSION_DDL,
                    _REVIEW_SESSION_DDL,
                    _TOMBSTONE_DDL,
                    _AUDIT_DDL,
                    _PROVENANCE_CHAIN_DDL,
                    _PROVENANCE_CHAIN_INDEX_DDL,
                    _CHAIN_CHECKPOINT_DDL,
                ):
                    conn.execute(ddl)
                _migrate(conn)
                conn.execute(f"PRAGMA user_version = {_SCHEMA_VERSION}")
            conn.commit()
        except Exception:
            conn.rollback()
            raise


def begin_immediate(conn) -> None:
    """Start a write-serializing transaction on `conn`.

    Used by callers that must serialize a check-then-act sequence (read the
    tail of an append-only log, then insert the next entry) across concurrent
    writers — see audit.append_event and provenance_chain.append. Acquires the
    write lock (RESERVED) up front so a competing writer blocks here instead
    of both readers computing the same "next" value. Pair with
    call_with_lock_retry() at the call site: a WAL-mode lock conflict can
    surface as an immediate "database is locked" OperationalError at BEGIN,
    at the INSERT, or at the implicit commit when the `with _db()` block
    exits — not only as a timed wait covered by connect(timeout=...).
    """
    conn.execute("BEGIN IMMEDIATE")


def call_with_lock_retry(fn, retries: int = 5, base_delay: float = 0.05):
    """Call `fn()`, retrying the WHOLE unit of work on a contended write lock.

    Retrying only the BEGIN statement is not enough: sqlite3's busy handler
    does not reliably cover every point a WAL-mode lock conflict can surface
    (BEGIN, INSERT, or the implicit commit on `with _db()` exit), so on
    "database is locked" we retry the entire fn() call — including opening a
    fresh connection — a few times with a short backoff before giving up.

    `fn` may run more than once, so it must be idempotent/side-effect-free
    until its own `_db()` block commits (e.g. audit.append_event and
    provenance_chain.append only read the DB tail and issue one INSERT inside
    `fn` — nothing observable happens unless that INSERT's transaction
    actually commits). Do not wrap a unit of work that has effects outside
    the SQLite transaction it opens (e.g. a network call, or a write to a
    second store) — a retried attempt would repeat that side effect.
    """
    for attempt in range(retries):
        try:
            return fn()
        except sqlite3.OperationalError as e:
            if "locked" not in str(e).lower() or attempt == retries - 1:
                raise
            time.sleep(base_delay * (attempt + 1))


@contextmanager
def _db():
    """Open one operation-scoped connection after ensuring the schema."""
    db_dir = os.path.dirname(SQLITE_PATH)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)
    # timeout=30: BEGIN IMMEDIATE callers (audit.append_event,
    # provenance_chain.append) serialize concurrent writers on this lock
    # instead of racing on a computed seq; give queued writers real headroom
    # instead of sqlite3's 5s default before raising "database is locked".
    conn = sqlite3.connect(SQLITE_PATH, timeout=30.0)
    conn.row_factory = sqlite3.Row
    _ensure_schema(conn)
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
    with _L0_LOCK:
        if fact_id in _L0:
            del _L0[fact_id]
        _L0[fact_id] = record
        if len(_L0) > L0_CAP:
            _L0.popitem(last=False)  # evict least-recently-used


def _l0_get(fact_id: str) -> Optional[Dict]:
    """Return from L0, refreshing recency. Returns None on miss."""
    with _L0_LOCK:
        if fact_id not in _L0:
            return None
        _L0.move_to_end(fact_id)
        return _L0[fact_id]


def _l0_pop(fact_id: str) -> None:
    """Evict a fact from L0 if present (no-op on miss). Lock-guarded."""
    with _L0_LOCK:
        _L0.pop(fact_id, None)


def _l0_put_if_fresher(fact_id: str, record: Dict) -> None:
    """Like _l0_put(), but refuses to overwrite an already-cached record with
    an OLDER one. Compares `updated_at` (an ISO-8601 UTC string set from
    datetime.now(timezone.utc).isoformat() everywhere it's produced, so
    lexical string comparison is a safe, correct chronological comparison)
    and skips the write only when the cached record is strictly newer. A tie
    (equal `updated_at`) accepts the incoming record.

    Used by get_fact()'s L1-rehydration-on-miss path ONLY. There, `record`'s
    `updated_at` is always the value actually read from a committed L1 row —
    a true historical snapshot — so comparing it against whatever else is
    cached is a valid freshness check: if L0 already holds something with a
    newer `updated_at`, a fresher write has already landed and this read's
    snapshot must not overwrite it.

    NOT used by store_fact() (Codex P1 correction on #248): store_fact()
    captures `now` and uses it as `updated_at` BEFORE performing the SQLite
    write, so two concurrent store_fact() calls' `updated_at` values reflect
    when each call STARTED, not the order their writes actually committed to
    L1 — those can differ (a call that captured an earlier `now` can still be
    the one whose write lands last in L1, e.g. if it was scheduled out right
    after capturing `now` and before reaching the write). Comparing such
    pre-write timestamps would reject a genuinely-latest L1 write just
    because its `now` happened to be captured first. store_fact() instead
    gets its ordering guarantee from _FACTS_WRITE_LOCK (serialized write +
    same-connection re-read + L0 populate as one atomic unit — see
    store_fact()) and populates L0 unconditionally within that lock, since
    whichever call holds the lock and just re-read its own committed write
    is, at that instant, guaranteed to hold the true latest L1 state.

    This is a cache-freshness guard, not a CAS/revision scheme: it never
    raises, never rejects the caller's write to L1 (which already happened
    by the time this runs), and never changes what get_fact() returns to its
    caller — only which record ends up cached in L0.
    """
    with _L0_LOCK:
        cached = _L0.get(fact_id)
        if cached is not None and cached.get("updated_at", "") > record.get("updated_at", ""):
            return  # a fresher record is already cached — do not clobber it
        _l0_put(fact_id, record)


# Shared facts-row write lock. store_fact(), update_fact(), transition_esm(),
# set_restricted(), and delete_fact_l1() serialize their ENTIRE SQLite mutation
# + same-connection re-read + L0 publish/evict sequence through this one lock,
# so DB-commit order and cache-publish order cannot diverge ACROSS APIs (for
# example, a transition racing a restriction update). See those functions and
# _l0_put_if_fresher()'s docstring for why a pre-write `updated_at` comparison
# alone is insufficient for this. Deliberately a single global lock, not
# per-fact_id: these writes are already serialized at the SQLite level
# (single-writer), so this adds no more contention than SQLite itself already
# imposes, and a per-key lock registry would be unwarranted complexity for the
# problem this actually is. SQLite's BEGIN IMMEDIATE remains the cross-process
# guard where a writer performs a read/check/write sequence.
_FACTS_WRITE_LOCK = threading.Lock()


# ─── API ───────────────────────────────────────────────────────────────────────

def _assert_claim_identity(
    fact_id: str,
    existing_claim: str,
    incoming_claim: str,
    epistemic_state: str,
) -> None:
    """Reject an in-place text rewrite once the fact identity is locked."""
    if (
        epistemic_state in CLAIM_IDENTITY_LOCKED_STATES
        and incoming_claim != existing_claim
    ):
        raise ClaimIdentityError(
            f"claim identity for '{fact_id}' is locked in state "
            f"'{epistemic_state}'; create a new fact and supersede the old one"
        )

def store_fact(fact: Dict) -> None:
    """
    Store a fact in L0 (LRU RAM) and L1 (SQLite).

    New facts: epistemic_state from the call is persisted and cached.
    Existing facts (conflict): epistemic_state is PRESERVED from the DB.
    Claim text may be refined only while the persisted state is Observed or
    Hypothesized. Supported/validated/terminal claims have stable identity;
    replace them by creating a new fact and calling reconcile.supersede().
    Other fields remain updateable. Use transition_esm() to advance state.

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
    # _FACTS_WRITE_LOCK (Codex P1 correction on #248): the write, the
    # same-connection re-read, and the L0 populate below are one atomic unit
    # relative to other store_fact()/update_fact() calls. `now`/`updated_at` is
    # captured BEFORE this lock is acquired, so it reflects when this call
    # STARTED, not the order in which writes actually commit to L1 — comparing
    # it against another call's timestamp would be comparing the wrong thing
    # (see _l0_put_if_fresher's docstring). The lock is the actual ordering
    # guarantee: whichever call acquires it and completes its write+reread
    # is, at that instant, unconditionally the true latest L1 state for this
    # fact_id, because no other store_fact()/update_fact() call can be
    # interleaved.
    with _FACTS_WRITE_LOCK:
        with _db() as conn:
            # Serialize the identity check + upsert against writers in other
            # processes too. Without the DB write lock, a concurrent
            # transition_esm() could promote the fact after this check but
            # before the upsert, letting a stale draft-state decision rewrite
            # an already-promoted claim.
            begin_immediate(conn)
            existing_row = conn.execute(
                "SELECT claim, epistemic_state FROM facts WHERE fact_id = ?",
                (fact_id,),
            ).fetchone()
            if existing_row is not None:
                _assert_claim_identity(
                    fact_id,
                    crypto.decrypt(existing_row["claim"]),
                    record["claim"],
                    existing_row["epistemic_state"],
                )
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
                    metadata        = excluded.metadata,
                    revision        = facts.revision + 1
            """, l1_record)
            # Re-read the persisted epistemic_state/created_at/restricted/revision
            # within the same connection so L0 is never poisoned with incoming/
            # default values on a conflict-update. The ON CONFLICT clause
            # intentionally omits epistemic_state and restricted (preserving the
            # existing row's state), and `record["created_at"]` above is always
            # "now" even though the DB row keeps the original insert timestamp.
            # For new inserts this returns the incoming/default values unchanged
            # (revision defaults to 0 on INSERT). Mirrors the "L0 after DB write"
            # discipline in transition_esm().
            row = conn.execute(
                "SELECT epistemic_state, created_at, restricted, revision "
                "FROM facts WHERE fact_id = ?",
                (fact_id,)
            ).fetchone()
            persisted_state = row["epistemic_state"] if row else epistemic_state
            persisted_created_at = row["created_at"] if row else now
            persisted_restricted = row["restricted"] if row else 0
            persisted_revision = row["revision"] if row else 0

        record["epistemic_state"] = persisted_state
        record["created_at"] = persisted_created_at
        record["restricted"] = persisted_restricted
        record["revision"] = persisted_revision
        # Unconditional _l0_put, not _l0_put_if_fresher: within this lock,
        # `record` (from the re-read above) IS the true, just-committed
        # latest L1 state for this fact_id — nothing else can have written
        # something newer without going through this same lock. Gating this
        # on a timestamp comparison would reintroduce the exact bug this
        # lock exists to fix (see _l0_put_if_fresher's docstring).
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
            # _l0_put_if_fresher, not _l0_put: this L1 snapshot may have been
            # read before a concurrent writer's newer store_fact()/update_fact()
            # already populated L0 — do not let a stale read clobber it. The
            # value returned to THIS caller is unaffected either way (`result`
            # is returned regardless of which record wins the cache).
            _l0_put_if_fresher(fact_id, result)
            return result
    return None


# ─── Columns that can be updated individually without changing the ESM state ─────────
_UPDATABLE = {"claim", "source", "confidence", "significance",
              "claim_type", "source_status", "metadata"}

# A Canon/L3 reconciliation occasionally has to repair an L1 row that was just
# created from an untrusted transient retrieval item before the physical L3 node
# was loaded. That is not a user-requested claim rewrite: it restores the same
# fact_id to the already-persisted canonical record. Keep this privilege
# process-local, thread-local and private so public update_fact()/store_fact()
# callers cannot opt out of claim-identity protection with a keyword flag.
_CANON_REPAIR_CONTEXT = threading.local()
_CANON_REPAIRABLE_FIELDS = {
    "claim", "source", "confidence", "claim_type", "source_status",
}


def update_fact(fact_id: str, **fields) -> bool:
    """
    Update individual fields of a fact WITHOUT touching epistemic_state.
    Changing the ESM state — only via transition_esm. Returns True if the
    fact is found and the update was applied.

    Optimistic CAS guard on `revision` (an integer column every writer of a
    facts row increments on each write — see _MIGRATIONS): the UPDATE only
    applies if the persisted revision still equals what we read. If a
    competing write landed on this fact_id between our read and our write,
    the UPDATE matches 0 rows and we abort instead of silently clobbering
    that write with a stale snapshot. Defense-in-depth for future
    concurrency/async — NOT a full atomicity guarantee.

    Originally this CAS-guarded on `updated_at` (a wall-clock string). Replaced
    with `revision` (#244 follow-up, after #248): a monotonically-incrementing
    integer cannot repeat a value for a given row, whereas two writes landing
    within the same timestamp-string resolution — or a backward clock
    adjustment — could in principle produce identical `updated_at` values,
    letting a stale reader's CAS incorrectly match (ABA). Low-probability with
    microsecond ISO timestamps, but the same "trusting wall-clock time to
    distinguish two different states" anti-pattern #248 fixed for L0-populate
    ordering — not something to also lean on for CAS identity once we know
    better. `revision` is immune to this by construction.

    The write, the post-commit re-read, and the L0 populate below run inside
    _FACTS_WRITE_LOCK (shared with store_fact()) as one atomic unit: on a CAS
    hit, L0 is populated from a fresh re-read of the row this call itself just
    committed — never from the pre-write `existing`/`fields` snapshot — so a
    concurrent store_fact()/update_fact() call's L0 populate can never be
    clobbered by this call's populate landing later with older data (the same
    class of bug #248 fixed for store_fact() alone; see _FACTS_WRITE_LOCK's
    docstring). Administrative fact writers use the same lock, so their cache
    publications cannot land out of SQLite commit order either.
    """
    fields = {k: v for k, v in fields.items() if k in _UPDATABLE}
    existing = get_fact(fact_id)
    if existing is None or not fields:
        return False

    if (
        "claim" in fields
        and not getattr(_CANON_REPAIR_CONTEXT, "enabled", False)
    ):
        _assert_claim_identity(
            fact_id,
            existing.get("claim", ""),
            fields["claim"],
            existing.get("epistemic_state", "Observed"),
        )

    expected_revision = existing["revision"]
    now = datetime.now(timezone.utc).isoformat()
    sets, params = [], {"fact_id": fact_id, "updated_at": now,
                         "expected_revision": expected_revision}
    for key, value in fields.items():
        sets.append(f"{key} = :{key}")
        if key == "metadata":
            params[key] = crypto.encrypt(json.dumps(value))  # encrypt at rest
        elif key == "claim":
            params[key] = crypto.encrypt(value)              # encrypt at rest
        else:
            params[key] = value

    with _FACTS_WRITE_LOCK:
        with _db() as conn:
            cur = conn.execute(
                f"UPDATE facts SET {', '.join(sets)}, revision = revision + 1, "  # nosec B608 — keys from _UPDATABLE allowlist
                f"updated_at = :updated_at "
                f"WHERE fact_id = :fact_id AND revision = :expected_revision",
                params,
            )
            if cur.rowcount != 1:
                # CAS miss: evict the stale L0 entry so the next get_fact()
                # re-reads the fresh DB state instead of serving stale cache to
                # a caller that ignores the return value. Never poison L0 with
                # our lost update.
                _l0_pop(fact_id)
                return False

            # Re-read the row we just committed, in the same connection/
            # transaction, so L0 is populated from the real persisted winner —
            # not from the pre-write `existing`/`fields` snapshot, which could
            # already be stale by the time this line runs relative to what we
            # ourselves just wrote (e.g. a concurrent value for a field this
            # call did not touch).
            row = conn.execute(
                "SELECT * FROM facts WHERE fact_id = ?", (fact_id,)
            ).fetchone()

        refreshed = dict(row)
        refreshed["claim"] = crypto.decrypt(refreshed["claim"])
        refreshed["metadata"] = json.loads(crypto.decrypt(refreshed["metadata"]))
        # Unconditional _l0_put, not _l0_put_if_fresher: within _FACTS_WRITE_LOCK,
        # `refreshed` IS the true, just-committed latest L1 state for this
        # fact_id — nothing else can have written something newer without
        # going through this same lock.
        _l0_put(fact_id, refreshed)
        return True


def _repair_fact_from_canon(fact_id: str, **fields) -> bool:
    """Repair L1 from an already-persisted physical L3 record.

    This is the sole internal exception to promoted claim-identity locking. It
    exists for ordinary recall reconciliation after build_facts_pack() created
    or refreshed L1 from a transient retrieval item before the authoritative L3
    node was loaded. Only trust-relevant fields already validated by
    pipeline._reconcile_recalled_fact() are accepted. The privilege is scoped to
    this synchronous call and cannot be requested through the public API.
    """
    canon_fields = {
        key: value
        for key, value in fields.items()
        if key in _CANON_REPAIRABLE_FIELDS
    }
    previous = getattr(_CANON_REPAIR_CONTEXT, "enabled", False)
    _CANON_REPAIR_CONTEXT.enabled = True
    try:
        return update_fact(fact_id, **canon_fields)
    finally:
        _CANON_REPAIR_CONTEXT.enabled = previous


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

    # The persisted-state read, policy check, mutation, fresh re-read and L0
    # publish form one ordered unit relative to every other facts-row API in
    # this process. BEGIN IMMEDIATE gives the read/check/write part the same
    # serialization across processes. Reading from SQLite here (not a possibly
    # stale L0 entry) means policy is evaluated against the state being changed.
    with _FACTS_WRITE_LOCK:
        with _db() as conn:
            begin_immediate(conn)
            row = conn.execute(
                "SELECT * FROM facts WHERE fact_id = ?", (fact_id,)
            ).fetchone()
            if row is None:
                return False

            current_state = row["epistemic_state"]
            allowed = ESM_TRANSITIONS.get(current_state)
            if allowed is not None and new_state not in allowed:
                # The caller may have reached us through a stale L0 snapshot
                # (for example, review read Observed before another process
                # collapsed the row). Do not leave that stale cache entry live
                # after reporting policy against the fresh persisted state.
                _l0_pop(fact_id)
                raise ValueError(
                    f"transition_esm: transition '{current_state}' → "
                    f"'{new_state}' is not allowed"
                )

            now = datetime.now(timezone.utc).isoformat()
            conn.execute(
                "UPDATE facts SET epistemic_state = ?, revision = revision + 1, "
                "updated_at = ? WHERE fact_id = ?",
                (new_state, now, fact_id),
            )
            refreshed_row = conn.execute(
                "SELECT * FROM facts WHERE fact_id = ?", (fact_id,)
            ).fetchone()

        refreshed = dict(refreshed_row)
        refreshed["claim"] = crypto.decrypt(refreshed["claim"])
        refreshed["metadata"] = json.loads(crypto.decrypt(refreshed["metadata"]))
        _l0_put(fact_id, refreshed)
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

    Bumps `revision` (see _MIGRATIONS) so update_fact()'s revision-based CAS
    (#244) can detect a set_restricted() write landing on this fact_id between
    update_fact()'s read and write. The SQLite read/write/fresh-read and L0
    publish share _FACTS_WRITE_LOCK with every other facts-row mutation.
    """
    val = int(bool(restricted))
    with _FACTS_WRITE_LOCK:
        with _db() as conn:
            begin_immediate(conn)
            existing_row = conn.execute(
                "SELECT fact_id FROM facts WHERE fact_id = ?", (fact_id,)
            ).fetchone()
            if existing_row is None:
                return False

            now = datetime.now(timezone.utc).isoformat()
            conn.execute(
                "UPDATE facts SET restricted = ?, revision = revision + 1, "
                "updated_at = ? WHERE fact_id = ?",
                (val, now, fact_id),
            )
            refreshed_row = conn.execute(
                "SELECT * FROM facts WHERE fact_id = ?", (fact_id,)
            ).fetchone()

        refreshed = dict(refreshed_row)
        refreshed["claim"] = crypto.decrypt(refreshed["claim"])
        refreshed["metadata"] = json.loads(crypto.decrypt(refreshed["metadata"]))
        _l0_put(fact_id, refreshed)
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
    with _FACTS_WRITE_LOCK:
        with _db() as conn:
            cur = conn.execute("DELETE FROM facts WHERE fact_id = ?", (fact_id,))
        _l0_pop(fact_id)
        return cur.rowcount > 0


def delete_import_session_entries_for(fact_id: str) -> int:
    """Delete all import_sessions rows for fact_id. Return deleted row count.

    Used by core.erasure.erase_fact() — import_sessions.source is plaintext
    (often a file path or corpus name) and can carry personal data (GDPR
    Art. 17 requires this gone too, not just the fact record itself). Lives
    here (not in core.imports, which owns the higher-level session API) so
    core.erasure can call it without an import cycle: core.imports already
    imports erase_fact() from core.erasure. Idempotent: erasing a fact_id
    with no import_sessions rows returns 0.
    """
    with _db() as conn:
        cur = conn.execute(
            "DELETE FROM import_sessions WHERE fact_id = ?", (fact_id,))
        return cur.rowcount


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
