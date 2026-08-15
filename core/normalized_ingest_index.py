# core/normalized_ingest_index.py
# Derived compatibility index for pre-normalization auto-ingest ids.

from typing import Optional

from core import crypto, memory
from core.ingest_identity import normalize_claim, normalized_ingest_id

_INDEX_DDL = """
    CREATE TABLE IF NOT EXISTS normalized_ingest_index (
        fact_id        TEXT PRIMARY KEY,
        normalized_id  TEXT NOT NULL,
        fact_revision  INTEGER NOT NULL
    )
"""
_INDEX_LOOKUP_DDL = (
    "CREATE INDEX IF NOT EXISTS idx_normalized_ingest_id "
    "ON normalized_ingest_index(normalized_id)"
)
_AUTO_ID_GLOB = "ing:" + "[0-9a-f]" * 12


def _ensure_index(conn) -> None:
    conn.execute(_INDEX_DDL)
    conn.execute(_INDEX_LOOKUP_DDL)


def _read_only_match(conn, query_text: str) -> Optional[str]:
    query_norm = normalize_claim(query_text)
    rows = conn.execute(
        "SELECT fact_id, claim FROM facts "
        "WHERE epistemic_state = 'Validated' AND restricted = 0 "
        "AND fact_id GLOB ? ORDER BY created_at, fact_id",
        (_AUTO_ID_GLOB,),
    )
    for row in rows:
        if normalize_claim(crypto.decrypt(row["claim"])) == query_norm:
            return row["fact_id"]
    return None


def _sync_index(conn) -> None:
    rows = conn.execute(
        "SELECT f.fact_id, f.claim, f.revision "
        "FROM facts AS f "
        "LEFT JOIN normalized_ingest_index AS n ON n.fact_id = f.fact_id "
        "WHERE f.epistemic_state = 'Validated' AND f.restricted = 0 "
        "AND f.fact_id GLOB ? "
        "AND (n.fact_id IS NULL OR n.fact_revision != f.revision) "
        "ORDER BY f.created_at, f.fact_id",
        (_AUTO_ID_GLOB,),
    ).fetchall()
    for row in rows:
        claim = crypto.decrypt(row["claim"])
        nid = normalized_ingest_id(claim)
        conn.execute(
            "INSERT INTO normalized_ingest_index "
            "(fact_id, normalized_id, fact_revision) VALUES (?, ?, ?) "
            "ON CONFLICT(fact_id) DO UPDATE SET "
            "normalized_id = excluded.normalized_id, "
            "fact_revision = excluded.fact_revision",
            (row["fact_id"], nid, row["revision"]),
        )


def resolve_validated_normalized_fact(
    query_text: str,
    *,
    persist_index: bool = True,
) -> Optional[str]:
    """Return a deterministic unrestricted Validated exact-normalized target.

    The short normalized id is only a lookup key. The current stored claim is
    decrypted and normalized again before a target is returned. Restricted rows
    are excluded from both backfill and lookup.
    """
    if not persist_index:
        with memory._db() as conn:
            return _read_only_match(conn, query_text)

    query_norm = normalize_claim(query_text)
    normalized_id = normalized_ingest_id(query_text)

    def _resolve() -> Optional[str]:
        with memory._db() as conn:
            _ensure_index(conn)
            _sync_index(conn)
            rows = conn.execute(
                "SELECT f.fact_id, f.claim FROM normalized_ingest_index AS n "
                "JOIN facts AS f ON f.fact_id = n.fact_id "
                "WHERE n.normalized_id = ? AND f.epistemic_state = 'Validated' "
                "AND f.restricted = 0 ORDER BY f.created_at, f.fact_id",
                (normalized_id,),
            ).fetchall()
            for row in rows:
                if normalize_claim(crypto.decrypt(row["claim"])) == query_norm:
                    return row["fact_id"]
            return None

    return memory.call_with_lock_retry(_resolve)


def remove_fact(fact_id: str) -> bool:
    with memory._db() as conn:
        table = conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type = 'table' "
            "AND name = 'normalized_ingest_index'"
        ).fetchone()
        if table is None:
            return False
        cur = conn.execute(
            "DELETE FROM normalized_ingest_index WHERE fact_id = ?", (fact_id,)
        )
        return cur.rowcount == 1
