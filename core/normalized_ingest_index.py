# core/normalized_ingest_index.py
# Persistent, derived compatibility index for pre-normalization auto-ingest ids.
#
# The table is a rebuildable lookup cache, not a new authority source. Every
# returned target is joined back to the current facts row, must still be
# Validated, and is rechecked against exact normalized text before routing. It
# never merges/re-keys historical facts and never performs semantic or
# near-duplicate matching.

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
# Auto-generated historical/current ids are exactly ``ing:`` + 12 lowercase
# hex characters. Keep the compatibility scan inside that namespace so an
# unrelated explicit id such as ``ing:custom`` is not silently enrolled merely
# because it shares the prefix.
_AUTO_ID_GLOB = "ing:" + "[0-9a-f]" * 12


def _ensure_index(conn) -> None:
    """Create the optional derived index without changing the facts schema."""
    conn.execute(_INDEX_DDL)
    conn.execute(_INDEX_LOOKUP_DDL)


def _read_only_match(conn, query_text: str) -> Optional[str]:
    """Resolve exact normalized equality without writes (dry-run path)."""
    query_norm = normalize_claim(query_text)
    rows = conn.execute(
        "SELECT fact_id, claim FROM facts "
        "WHERE epistemic_state = 'Validated' AND fact_id GLOB ? "
        "ORDER BY created_at, fact_id",
        (_AUTO_ID_GLOB,),
    )
    for row in rows:
        if normalize_claim(crypto.decrypt(row["claim"])) == query_norm:
            return row["fact_id"]
    return None


def _sync_index(conn) -> None:
    """Index new/stale Validated auto-id rows in deterministic order.

    ``revision`` is used only as a cheap change detector. Claim identity is
    locked after validation, but revision also lets a low-level delete/recreate
    or administrative rewrite fail toward recomputation instead of trusting a
    stale derived mapping.
    """
    rows = conn.execute(
        "SELECT f.fact_id, f.claim, f.revision "
        "FROM facts AS f "
        "LEFT JOIN normalized_ingest_index AS n ON n.fact_id = f.fact_id "
        "WHERE f.epistemic_state = 'Validated' AND f.fact_id GLOB ? "
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
    """Return a deterministic existing Validated exact-normalized target.

    Live lookup uses the existing short normalized fact-id only as an indexed
    prefilter, then decrypts the current fact and rechecks exact normalized text
    equality before returning it. The 12-hex id is therefore never treated as
    equality proof, and a stale/corrupt derived row fails closed.

    When persistence is disabled (dry-run), the same exact equality and ordering
    are computed read-only. Existing collisions are intentionally preserved; the
    oldest ``created_at`` row wins, with ``fact_id`` as a deterministic tie-breaker.
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
                "ORDER BY f.created_at, f.fact_id",
                (normalized_id,),
            ).fetchall()
            for row in rows:
                if normalize_claim(crypto.decrypt(row["claim"])) == query_norm:
                    return row["fact_id"]
            return None

    return memory.call_with_lock_retry(_resolve)


def remove_fact(fact_id: str) -> bool:
    """Remove one derived mapping during full erasure.

    The compatibility table is optional/lazy. Erasing a fact that never used the
    index must not create the table merely to delete from it. Returns whether a
    mapping actually existed; callers must not treat that derived-cache detail as
    proof that personal/canonical data existed.
    """
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
