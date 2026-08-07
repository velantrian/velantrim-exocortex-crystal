"""Explicit operator reindex for legacy L3 stores.

Public query paths must never initialise an embedder fingerprint or rebuild
vectors. This module is an operator-only maintenance command that recomputes
vectors from already-stored claims and stamps the active embedder only after a
successful complete pass. Fact payloads, ESM, truth status, edges and audit are
not modified.
"""
from __future__ import annotations

import argparse
import json
from typing import Any, Callable, Optional, Sequence

from core.embedding import get_embedder
from core.l3_graph import MockL3Graph, SqliteL3Graph, get_l3_graph
from core.legacy_retrieval import legacy_retrieval_status


class ReindexUnsupported(RuntimeError):
    pass


def _validate_batch_size(value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1 or value > 10_000:
        raise ValueError("batch_size must be an integer between 1 and 10000")
    return value


def _sqlite_reindex(graph: SqliteL3Graph, *, batch_size: int, progress: Optional[Callable]) -> dict[str, Any]:
    embedder = get_embedder()
    processed = 0
    skipped = 0
    with graph._lock:
        total = int(graph._conn.execute("SELECT COUNT(*) FROM nodes").fetchone()[0])
        # A partial rebuild is never advertised as compatible: remove the old
        # marker first. If a later batch fails, public queries stay on the
        # bounded legacy path instead of consuming mixed/partial vectors.
        with graph._conn:
            graph._conn.execute("DELETE FROM meta WHERE key = 'embedder_fp'")
            graph._conn.execute("DELETE FROM vectors")

        cursor = graph._conn.execute("SELECT fact_id, data FROM nodes ORDER BY fact_id")
        while True:
            rows = cursor.fetchmany(batch_size)
            if not rows:
                break
            prepared = []
            for row in rows:
                node = json.loads(row["data"])
                claim = node.get("claim")
                # Reindex must reproduce the ordinary L3 vector-build contract:
                # empty strings are skipped, while truthy strings — including
                # whitespace-only legacy claims — receive vectors.
                if not isinstance(claim, str) or not claim:
                    skipped += 1
                    continue
                prepared.append((row["fact_id"], json.dumps(embedder.embed(claim))))
            with graph._conn:
                graph._conn.executemany(
                    "INSERT INTO vectors(fact_id, vec) VALUES(?, ?) "
                    "ON CONFLICT(fact_id) DO UPDATE SET vec = excluded.vec",
                    prepared,
                )
            processed += len(prepared)
            if progress is not None:
                progress({"processed": processed, "skipped": skipped, "total": total})

        with graph._conn:
            graph._conn.execute(
                "INSERT INTO meta(key, value) VALUES('embedder_fp', ?) "
                "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
                (embedder.id,),
            )
    return {
        "ok": True,
        "backend": type(graph).__name__,
        "embedder": embedder.id,
        "total": total,
        "processed": processed,
        "skipped": skipped,
        "fingerprint": graph.embedder_fingerprint(),
        "truth_state_changed": False,
    }


def _mock_reindex(graph: MockL3Graph, *, batch_size: int, progress: Optional[Callable]) -> dict[str, Any]:
    embedder = get_embedder()
    ids = sorted(graph._nodes)
    total = len(ids)
    processed = 0
    skipped = 0
    rebuilt: dict[str, list[float]] = {}
    for offset in range(0, total, batch_size):
        for fact_id in ids[offset:offset + batch_size]:
            claim = graph._nodes[fact_id].get("claim")
            if not isinstance(claim, str) or not claim:
                skipped += 1
                continue
            rebuilt[fact_id] = embedder.embed(claim)
            processed += 1
        if progress is not None:
            progress({"processed": processed, "skipped": skipped, "total": total})
    graph._vectors = rebuilt
    graph.set_embedder_fingerprint(embedder.id)
    return {
        "ok": True,
        "backend": type(graph).__name__,
        "embedder": embedder.id,
        "total": total,
        "processed": processed,
        "skipped": skipped,
        "fingerprint": graph.embedder_fingerprint(),
        "truth_state_changed": False,
    }


def reindex_embeddings(
    graph=None,
    *,
    batch_size: int = 100,
    progress: Optional[Callable[[dict[str, int]], None]] = None,
) -> dict[str, Any]:
    """Rebuild vectors and fingerprint explicitly without changing fact truth."""
    graph = graph or get_l3_graph()
    batch_size = _validate_batch_size(batch_size)
    if isinstance(graph, SqliteL3Graph):
        return _sqlite_reindex(graph, batch_size=batch_size, progress=progress)
    if isinstance(graph, MockL3Graph):
        return _mock_reindex(graph, batch_size=batch_size, progress=progress)
    raise ReindexUnsupported(
        f"{type(graph).__name__} does not expose a reviewed embedding reindex adapter"
    )


def reindex_status(graph=None) -> dict[str, Any]:
    graph = graph or get_l3_graph()
    status = legacy_retrieval_status(graph).to_dict()
    status["active_fingerprint"] = graph.embedder_fingerprint()
    status["reindex_supported"] = isinstance(graph, (MockL3Graph, SqliteL3Graph))
    return status


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m core.reindex_embeddings")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status", help="show fingerprint and bounded-legacy capability")
    rebuild = sub.add_parser("rebuild", help="explicitly rebuild vectors and fingerprint")
    rebuild.add_argument("--batch-size", type=int, default=100)
    args = parser.parse_args(argv)
    try:
        result = (
            reindex_status()
            if args.command == "status"
            else reindex_embeddings(batch_size=args.batch_size)
        )
    except (ValueError, ReindexUnsupported) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps(result, sort_keys=True, ensure_ascii=False))
    return 0


__all__ = [
    "ReindexUnsupported",
    "reindex_embeddings",
    "reindex_status",
    "main",
]


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
