# core/normalized_ingest_index.py
# Derived compatibility index for pre-normalization auto-ingest ids.

from __future__ import annotations

import re
import sqlite3
from typing import Iterable, Optional

from core import crypto, memory
from core.ingest_identity import normalize_claim, normalized_ingest_id

_PROTOCOL_VERSION = 1
_INDEX_TABLE = "normalized_ingest_index"
_STATE_TABLE = "normalized_ingest_index_state"
_LOOKUP_INDEX = "idx_normalized_ingest_id"
_AUTO_ID_GLOB = "ing:" + "[0-9a-f]" * 12
_ELIGIBLE = (
    "epistemic_state = 'Validated' AND restricted = 0 "
    "AND fact_id GLOB '" + _AUTO_ID_GLOB + "'"
)


def _eligible(alias: str) -> str:
    return (
        f"{alias}.epistemic_state = 'Validated' AND {alias}.restricted = 0 "
        f"AND {alias}.fact_id GLOB '{_AUTO_ID_GLOB}'"
    )

_INDEX_DDL = """
CREATE TABLE normalized_ingest_index (
    fact_id TEXT PRIMARY KEY,
    normalized_id TEXT NOT NULL,
    fact_revision INTEGER NOT NULL
)
"""
_STATE_DDL = """
CREATE TABLE normalized_ingest_index_state (
    state_id INTEGER PRIMARY KEY CHECK (state_id = 1),
    protocol_version INTEGER NOT NULL,
    generation INTEGER NOT NULL,
    covered_generation INTEGER NOT NULL,
    complete INTEGER NOT NULL CHECK (complete IN (0, 1))
)
"""
_LOOKUP_DDL = (
    "CREATE INDEX idx_normalized_ingest_id "
    "ON normalized_ingest_index(normalized_id)"
)


def _invalidate_sql() -> str:
    return (
        "UPDATE normalized_ingest_index_state "
        "SET generation = generation + 1, complete = 0 WHERE state_id = 1"
    )


_FACT_TRIGGERS = {
    "normalized_ingest_facts_ai": f"""
        CREATE TRIGGER normalized_ingest_facts_ai AFTER INSERT ON facts
        WHEN {_eligible('NEW')}
        BEGIN {_invalidate_sql()}; END
    """,
    "normalized_ingest_facts_au": f"""
        CREATE TRIGGER normalized_ingest_facts_au AFTER UPDATE ON facts
        WHEN {_eligible('OLD')} OR {_eligible('NEW')}
        BEGIN {_invalidate_sql()}; END
    """,
    "normalized_ingest_facts_ad": f"""
        CREATE TRIGGER normalized_ingest_facts_ad AFTER DELETE ON facts
        WHEN {_eligible('OLD')}
        BEGIN {_invalidate_sql()}; END
    """,
}
_MAPPING_TRIGGERS = {
    "normalized_ingest_mapping_ai": f"""
        CREATE TRIGGER normalized_ingest_mapping_ai AFTER INSERT ON {_INDEX_TABLE}
        BEGIN {_invalidate_sql()}; END
    """,
    "normalized_ingest_mapping_au": f"""
        CREATE TRIGGER normalized_ingest_mapping_au AFTER UPDATE ON {_INDEX_TABLE}
        BEGIN {_invalidate_sql()}; END
    """,
    "normalized_ingest_mapping_ad": f"""
        CREATE TRIGGER normalized_ingest_mapping_ad AFTER DELETE ON {_INDEX_TABLE}
        BEGIN {_invalidate_sql()}; END
    """,
}


def _sql_key(sql: str) -> str:
    return re.sub(r"\s+", " ", sql.strip().rstrip(";")).casefold()


def _object_type(conn, name: str) -> Optional[str]:
    row = conn.execute(
        "SELECT type FROM sqlite_master WHERE name = ?", (name,)
    ).fetchone()
    return row["type"] if row else None


def _create_state_storage(conn) -> None:
    """Install versioned generation state and facts-write invalidation triggers."""
    state_type = _object_type(conn, _STATE_TABLE)
    if state_type == "view":
        conn.execute(f"DROP VIEW {_STATE_TABLE}")
    elif state_type == "index":
        conn.execute(f"DROP INDEX {_STATE_TABLE}")
    elif state_type == "trigger":
        conn.execute(f"DROP TRIGGER {_STATE_TABLE}")
    if _object_type(conn, _STATE_TABLE) == "table":
        columns = [row["name"] for row in conn.execute(
            f"PRAGMA table_info({_STATE_TABLE})"
        )]
        if columns != [
            "state_id", "protocol_version", "generation",
            "covered_generation", "complete",
        ]:
            conn.execute(f"DROP TABLE {_STATE_TABLE}")
    conn.execute(_STATE_DDL.replace("CREATE TABLE ", "CREATE TABLE IF NOT EXISTS ", 1))
    conn.execute(
        f"INSERT OR IGNORE INTO {_STATE_TABLE} "
        "(state_id, protocol_version, generation, covered_generation, complete) "
        "VALUES (1, ?, 0, -1, 0)",
        (_PROTOCOL_VERSION,),
    )
    _install_triggers(conn, _FACT_TRIGGERS)


def _install_triggers(conn, definitions: dict[str, str]) -> None:
    for name, ddl in definitions.items():
        row = conn.execute(
            "SELECT sql FROM sqlite_master WHERE type = 'trigger' AND name = ?",
            (name,),
        ).fetchone()
        if row is not None and _sql_key(row["sql"]) != _sql_key(ddl):
            conn.execute(f"DROP TRIGGER {name}")
            row = None
        if row is None:
            conn.execute(ddl)


def install_state_migration(conn) -> None:
    """Create state + fact invalidation triggers inside the schema migration."""
    _create_state_storage(conn)


def _index_columns(conn) -> list[str]:
    if _object_type(conn, _INDEX_TABLE) != "table":
        return []
    return [row["name"] for row in conn.execute(
        f"PRAGMA table_info({_INDEX_TABLE})"
    )]


def _ensure_index_storage(conn) -> None:
    _create_state_storage(conn)
    object_type = _object_type(conn, _INDEX_TABLE)
    if object_type == "view":
        conn.execute(f"DROP VIEW {_INDEX_TABLE}")
        object_type = None
    elif object_type == "index":
        conn.execute(f"DROP INDEX {_INDEX_TABLE}")
        object_type = None
    elif object_type == "trigger":
        conn.execute(f"DROP TRIGGER {_INDEX_TABLE}")
        object_type = None
    if object_type == "table" and _index_columns(conn) != [
        "fact_id", "normalized_id", "fact_revision",
    ]:
        # This is disposable derived routing data; fact identity and all
        # authoritative tables are untouched. Rebuild below repopulates it.
        conn.execute(f"UPDATE {_STATE_TABLE} SET complete = 0 WHERE state_id = 1")
        conn.execute(f"DROP TABLE {_INDEX_TABLE}")
        object_type = None
    if object_type is None:
        conn.execute(_INDEX_DDL)
    indexes = {
        row["name"]: row for row in conn.execute(
            f"PRAGMA index_list({_INDEX_TABLE})"
        )
    }
    if _LOOKUP_INDEX in indexes:
        columns = [row["name"] for row in conn.execute(
            f"PRAGMA index_info({_LOOKUP_INDEX})"
        )]
        if columns != ["normalized_id"]:
            conn.execute(f"DROP INDEX {_LOOKUP_INDEX}")
    conn.execute(_LOOKUP_DDL.replace("CREATE INDEX ", "CREATE INDEX IF NOT EXISTS ", 1))
    _install_triggers(conn, _MAPPING_TRIGGERS)


def _structure_is_valid(conn) -> bool:
    try:
        if _object_type(conn, _STATE_TABLE) != "table":
            return False
        if _object_type(conn, _INDEX_TABLE) != "table":
            return False
        state_columns = [row["name"] for row in conn.execute(
            f"PRAGMA table_info({_STATE_TABLE})"
        )]
        if state_columns != [
            "state_id", "protocol_version", "generation",
            "covered_generation", "complete",
        ]:
            return False
        index_info = conn.execute(
            f"PRAGMA table_info({_INDEX_TABLE})"
        ).fetchall()
        if [row["name"] for row in index_info] != [
            "fact_id", "normalized_id", "fact_revision",
        ]:
            return False
        if not index_info[0]["pk"] or not index_info[1]["notnull"] or not index_info[2]["notnull"]:
            return False
        index_row = conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type = 'index' AND name = ?",
            (_LOOKUP_INDEX,),
        ).fetchone()
        if index_row is None or [row["name"] for row in conn.execute(
            f"PRAGMA index_info({_LOOKUP_INDEX})"
        )] != ["normalized_id"]:
            return False
        expected = {**_FACT_TRIGGERS, **_MAPPING_TRIGGERS}
        found = {
            row["name"]: row["sql"] for row in conn.execute(
                "SELECT name, sql FROM sqlite_master WHERE type = 'trigger' "
                "AND name LIKE 'normalized_ingest_%'"
            )
        }
        return all(
            name in found and _sql_key(found[name]) == _sql_key(ddl)
            for name, ddl in expected.items()
        ) and set(found) == set(expected)
    except (sqlite3.Error, TypeError, KeyError):
        return False


def is_complete(conn) -> bool:
    """True only when schema, invalidation triggers and generation agree."""
    if not _structure_is_valid(conn):
        return False
    try:
        row = conn.execute(
            f"SELECT protocol_version, generation, covered_generation, complete "
            f"FROM {_STATE_TABLE} WHERE state_id = 1"
        ).fetchone()
        return bool(
            row is not None
            and row["protocol_version"] == _PROTOCOL_VERSION
            and row["complete"] == 1
            and row["generation"] == row["covered_generation"]
        )
    except sqlite3.Error:
        return False


def _mark_incomplete(conn) -> None:
    try:
        if _object_type(conn, _STATE_TABLE) == "table":
            conn.execute(
                f"UPDATE {_STATE_TABLE} SET complete = 0 WHERE state_id = 1"
            )
    except sqlite3.Error:
        # The trigger-invalidated generation remains the primary fail-closed
        # signal. A damaged/missing state table also makes _structure_is_valid
        # false, so reads fall back to the exact scan.
        pass


def _upsert_fact_mapping(conn, fact_id: str) -> None:
    row = conn.execute(
        "SELECT fact_id, claim, revision FROM facts WHERE fact_id = ? "
        "AND " + _ELIGIBLE,
        (fact_id,),
    ).fetchone()
    if row is None:
        conn.execute(f"DELETE FROM {_INDEX_TABLE} WHERE fact_id = ?", (fact_id,))
        return
    plain_claim = crypto.decrypt(row["claim"])
    conn.execute(
        f"INSERT INTO {_INDEX_TABLE} (fact_id, normalized_id, fact_revision) "
        "VALUES (?, ?, ?) ON CONFLICT(fact_id) DO UPDATE SET "
        "normalized_id = excluded.normalized_id, "
        "fact_revision = excluded.fact_revision",
        (fact_id, normalized_ingest_id(plain_claim), row["revision"]),
    )


def capture_complete(conn) -> bool:
    """Capture a proven pre-mutation complete state under the caller's write lock."""
    return is_complete(conn)


def refresh_facts_after_write(
    conn, fact_ids: Iterable[str], *, was_complete: bool
) -> None:
    """Maintain touched mappings inside the facts transaction when coverage was sound.

    Direct SQL writers intentionally do not get this repair step: their triggers
    leave the generation dirty and force exact-scan fallback until a full rebuild.
    """
    if not was_complete:
        return
    try:
        if not _structure_is_valid(conn):
            _mark_incomplete(conn)
            return
        state = conn.execute(
            f"SELECT generation, covered_generation, complete "
            f"FROM {_STATE_TABLE} WHERE state_id = 1"
        ).fetchone()
        if (
            state is not None
            and state["complete"] == 1
            and state["generation"] == state["covered_generation"]
        ):
            # The facts trigger did not fire, so the committed row change was
            # outside the eligible set. Do not touch either the routing table
            # or its metadata (notably for pre-gate Observed writes).
            return
        for fact_id in dict.fromkeys(fact_ids):
            _upsert_fact_mapping(conn, fact_id)
        conn.execute(
            f"UPDATE {_STATE_TABLE} SET complete = 1, "
            "covered_generation = generation WHERE state_id = 1 "
            "AND protocol_version = ?",
            (_PROTOCOL_VERSION,),
        )
        if not is_complete(conn):
            _mark_incomplete(conn)
    except Exception:  # derived cache failures must never block the primary L1 write
        _mark_incomplete(conn)


def _ensure_index_storage_and_dirty(conn) -> None:
    _ensure_index_storage(conn)
    conn.execute(
        f"UPDATE {_STATE_TABLE} SET complete = 0 WHERE state_id = 1"
    )


def _rebuild_conn(conn) -> int:
    _ensure_index_storage_and_dirty(conn)
    conn.execute(f"DELETE FROM {_INDEX_TABLE}")
    rows = conn.execute(
        "SELECT fact_id, claim, revision FROM facts WHERE " + _ELIGIBLE +
        " ORDER BY created_at, fact_id"
    ).fetchall()
    for row in rows:
        conn.execute(
            f"INSERT INTO {_INDEX_TABLE} "
            "(fact_id, normalized_id, fact_revision) VALUES (?, ?, ?)",
            (
                row["fact_id"],
                normalized_ingest_id(crypto.decrypt(row["claim"])),
                row["revision"],
            ),
        )
    indexed_count = conn.execute(
        f"SELECT COUNT(*) FROM {_INDEX_TABLE}"
    ).fetchone()[0]
    if indexed_count != len(rows):
        raise RuntimeError("normalized ingest index rebuild row-count mismatch")
    conn.execute(
        f"UPDATE {_STATE_TABLE} SET protocol_version = ?, complete = 1, "
        "covered_generation = generation WHERE state_id = 1",
        (_PROTOCOL_VERSION,),
    )
    if not is_complete(conn):
        raise RuntimeError("normalized ingest index rebuild failed completeness check")
    return indexed_count


def rebuild_normalized_ingest_index() -> int:
    """Atomically rebuild all eligible mappings and publish complete last."""
    def _rebuild() -> int:
        with memory._db() as conn:
            memory.begin_immediate(conn)
            return _rebuild_conn(conn)

    return memory.call_with_lock_retry(_rebuild)


def rebuild_if_incomplete() -> Optional[int]:
    """Rebuild only after a successful ingest when a dirty/unknown state remains."""
    def _rebuild_if_needed() -> Optional[int]:
        with memory._db() as conn:
            memory.begin_immediate(conn)
            if is_complete(conn):
                return None
            return _rebuild_conn(conn)

    return memory.call_with_lock_retry(_rebuild_if_needed)


def _read_only_match(conn, query_text: str) -> Optional[str]:
    query_norm = normalize_claim(query_text)
    rows = conn.execute(
        "SELECT fact_id, claim FROM facts WHERE " + _ELIGIBLE +
        " ORDER BY created_at, fact_id"
    )
    for row in rows:
        if normalize_claim(crypto.decrypt(row["claim"])) == query_norm:
            return row["fact_id"]
    return None


def resolve_validated_normalized_fact(
    query_text: str,
    *,
    persist_index: bool = False,
) -> Optional[str]:
    """Return the deterministic exact-normalized legacy target without writes.

    A complete indexed state may prove a fast negative lookup. When completeness,
    schema compatibility or row revision is uncertain, the resolver performs the
    historical exact scan. The short MD5-derived ID is only a prefilter: every
    returned candidate is decrypted and exact-normalized before reuse.
    ``persist_index`` is retained as a source-compatible keyword but is ignored;
    rebuilding is explicit and is only called after successful ingest.
    """
    del persist_index
    query_norm = normalize_claim(query_text)
    normalized_id = normalized_ingest_id(query_text)
    with memory._db() as conn:
        # Hold one MVCC snapshot across the completeness check and candidate
        # query. A concurrent writer either precedes this snapshot or is visible
        # only to the next resolver call; mixed generations are never observed.
        conn.execute("BEGIN")
        if not is_complete(conn):
            return _read_only_match(conn, query_text)
        rows = conn.execute(
            f"SELECT f.fact_id, f.claim, f.revision, n.fact_revision "
            f"FROM {_INDEX_TABLE} AS n JOIN facts AS f ON f.fact_id = n.fact_id "
            "WHERE n.normalized_id = ? AND " + _eligible("f") +
            " ORDER BY f.created_at, f.fact_id",
            (normalized_id,),
        ).fetchall()
        # A stale current-key row is evidence that the marker can no longer be
        # trusted. Fall back to the exact scan rather than accepting absence.
        if any(row["fact_revision"] != row["revision"] for row in rows):
            return _read_only_match(conn, query_text)
        for row in rows:
            if normalize_claim(crypto.decrypt(row["claim"])) == query_norm:
                return row["fact_id"]
        return None


def remove_fact(fact_id: str) -> bool:
    """Remove a single derived mapping; direct maintenance invalidates coverage."""
    with memory._db() as conn:
        if _object_type(conn, _INDEX_TABLE) != "table":
            return False
        cur = conn.execute(f"DELETE FROM {_INDEX_TABLE} WHERE fact_id = ?", (fact_id,))
        return cur.rowcount == 1
