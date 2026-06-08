# core/l3_graph.py
# Velantrim ExoCortex — L3 Canonical Graph (adapter)
# v8.2.0-sprint2
#
# Principle: Graph = Truth. L3 is the single source of canonical truth.
# The only entry into L3 is via the TruthGate (see pipeline.run). A direct MERGE
# into the graph bypassing the TruthGate is an architectural bug.
#
# Memory layers (physically distinct fabrics):
#   SQLite (core/memory.py) — L0/L1 + L2-pending: fast working memory of "now",
#                             ESM stages Observed/Hypothesized before the gate.
#   L3 graph (this module)  — canon after the gate: nodes + edges (links, episodes, schemas).
#
# Pluggable backend. Default — MockL3Graph (in-memory, dependency-free).
# Prod target — LadybugDB: successor to Kuzu (Kuzu was frozen in Oct. 2025 after
# the Apple acquisition). LadybugDB is embedded, Cypher-compatible, with a vector index
# and full-text search. Standard Cypher → the backend stays portable.

import functools
import json
import logging
import os
import sqlite3
import threading
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any

from core._registry import BackendRegistry

logger = logging.getLogger(__name__)

# Contribution of salience to vector_search ranking: final score =
# similarity × (1 + W × significance). Relevance dominates, significance
# lifts important memories when cosines are close. significance ≠ truth.
_SIGNIFICANCE_WEIGHT = 0.5


def _salience_score(similarity: float, significance: Any) -> float:
    """Similarity boosted by the node's significance (default significance=0.5)."""
    try:
        sig = float(significance)
    except (TypeError, ValueError):
        sig = 0.5
    return similarity * (1.0 + _SIGNIFICANCE_WEIGHT * sig)


# ─── BACKEND INTERFACE ────────────────────────────────────────────────────────

class L3GraphBackend(ABC):
    """
    Minimal contract of the L3 canonical graph.
    All implementations (mock / LadybugDB) must honor it,
    so the backend can be swapped without touching the pipeline.
    """

    # ─── Embedder fingerprint (guard against mixing vectors) ───────────────────
    # Concrete methods (not abstract): they store the id of the embedder the
    # store's vectors were built with, so embedding.assert_compatible_embedder
    # catches an embedder swap. Default — an in-process attribute; that is enough
    # for the mock and for detecting a swap within a session. Cross-restart persistence
    # of the fingerprint on LadybugDB/Neo4j (a metadata row) is an optional step, see FUTURE.md §2.2.
    def embedder_fingerprint(self) -> Optional[str]:
        """id of the embedder the store's vectors were built with (None before the first write)."""
        return getattr(self, "_embedder_fp", None)

    def set_embedder_fingerprint(self, fingerprint: str) -> None:
        """Record the embedder id for this store."""
        self._embedder_fp = fingerprint

    @abstractmethod
    def merge_fact(self, fact: Dict[str, Any]) -> None:
        """Upsert a canonical node by fact_id. Idempotent."""

    @abstractmethod
    def get_fact(self, fact_id: str) -> Optional[Dict[str, Any]]:
        """Return the canonical node by fact_id or None."""

    @abstractmethod
    def erase_fact(self, fact_id: str) -> bool:
        """
        Physically delete a fact node from the canon together with ALL its edges
        (outgoing and incoming), its vector and mentions links.
        GDPR Art. 17 (right to be forgotten). Idempotent: True if the node
        existed and was deleted, otherwise False.
        """

    @abstractmethod
    def all_facts(self) -> List[Dict[str, Any]]:
        """All canonical nodes of the graph."""

    @abstractmethod
    def add_edge(
        self, src_id: str, rel_type: str, dst_id: str,
        props: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Add a directed edge src -[rel_type]-> dst."""

    @abstractmethod
    def neighbors(
        self, fact_id: str, rel_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Neighboring nodes via outgoing edges (optionally filtered by type)."""

    @abstractmethod
    def get_edges(
        self, fact_id: str, rel_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        A fact's outgoing edges together with their props (unlike neighbors,
        which returns only nodes). Element: {rel_type, target, props}.
        Needed to read the episodic who/where/when context from edges.
        """

    @abstractmethod
    def incoming_edges(
        self, fact_id: str, rel_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        A fact's incoming edges (mirror of get_edges). Element: {rel_type, source,
        props}. Needed for reverse queries: what replaced the fact / what
        refutes it / what references it.
        """

    @abstractmethod
    def vector_search(
        self, query_vector: List[float], k: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Semantic search over node embeddings.
        Returns up to k facts, sorted by descending similarity;
        each augmented with a '_score' field (cosine similarity).
        """

    # ─── Episodic entity nodes (Person/Place/Time as first-class nodes) ──
    @abstractmethod
    def merge_entity(self, entity_id: str, kind: str, label: str) -> None:
        """Upsert an entity node (kind: person/place/time). Idempotent."""

    @abstractmethod
    def link_fact_to_entity(
        self, fact_id: str, entity_id: str, rel: str = "MENTIONS",
    ) -> None:
        """Link a fact to an entity node (the fact mentions the entity)."""

    @abstractmethod
    def facts_for_entity(self, entity_id: str) -> List[Dict[str, Any]]:
        """Facts linked to an entity node (reverse MENTIONS traversal)."""


# ─── MOCK BACKEND (in-memory, default) ─────────────────────────────────────────

class MockL3Graph(L3GraphBackend):
    """
    In-memory implementation of L3 without external dependencies.
    Sufficient for tests and the MVP pipeline; replicates the semantics of the future
    LadybugDB (MERGE node, directed edges), but without persistence.
    """

    def __init__(self) -> None:
        self._nodes: Dict[str, Dict[str, Any]] = {}
        # edge: (src_id, rel_type, dst_id, props)
        self._edges: List[tuple] = []
        # node embeddings for vector_search (separate from node data)
        self._vectors: Dict[str, List[float]] = {}
        # entity nodes and fact→entity links (separate from the Fact space)
        self._entities: Dict[str, Dict[str, Any]] = {}
        self._mentions: List[tuple] = []  # (fact_id, entity_id, rel)
        self._embedder_fp: Optional[str] = None  # store's embedder fingerprint

    def merge_entity(self, entity_id: str, kind: str, label: str) -> None:
        self._entities[entity_id] = {
            "entity_id": entity_id, "kind": kind, "label": label}

    def link_fact_to_entity(self, fact_id, entity_id, rel="MENTIONS") -> None:
        edge = (fact_id, entity_id, rel)
        if edge not in self._mentions:
            self._mentions.append(edge)

    def facts_for_entity(self, entity_id: str) -> List[Dict[str, Any]]:
        ids = [fid for fid, eid, _ in self._mentions if eid == entity_id]
        return [dict(self._nodes[fid]) for fid in ids if fid in self._nodes]

    def merge_fact(self, fact: Dict[str, Any]) -> None:
        fact_id = fact.get("fact_id")
        if not fact_id:
            raise ValueError("merge_fact: fact_id is required")
        # MERGE: update the existing node, do not create duplicates.
        node = self._nodes.get(fact_id, {})
        node.update(fact)
        self._nodes[fact_id] = node
        # Embedding of the claim for semantic search.
        claim = node.get("claim")
        if claim:
            from core.embedding import get_embedder
            self._vectors[fact_id] = get_embedder().embed(claim)

    def get_fact(self, fact_id: str) -> Optional[Dict[str, Any]]:
        node = self._nodes.get(fact_id)
        return dict(node) if node is not None else None

    def all_facts(self) -> List[Dict[str, Any]]:
        return [dict(n) for n in self._nodes.values()]

    def erase_fact(self, fact_id: str) -> bool:
        existed = fact_id in self._nodes
        self._nodes.pop(fact_id, None)
        self._vectors.pop(fact_id, None)
        # Remove all edges where the fact is the source OR the target (no dangling refs).
        self._edges = [e for e in self._edges
                       if e[0] != fact_id and e[2] != fact_id]
        self._mentions = [m for m in self._mentions if m[0] != fact_id]
        return existed

    def add_edge(
        self, src_id: str, rel_type: str, dst_id: str,
        props: Optional[Dict[str, Any]] = None,
    ) -> None:
        edge = (src_id, rel_type, dst_id, props or {})
        if edge not in self._edges:
            self._edges.append(edge)

    def neighbors(
        self, fact_id: str, rel_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        out = []
        for src, rel, dst, _ in self._edges:
            if src != fact_id:
                continue
            if rel_type is not None and rel != rel_type:
                continue
            node = self._nodes.get(dst)
            if node is not None:
                out.append(dict(node))
        return out

    def vector_search(
        self, query_vector: List[float], k: int = 5,
    ) -> List[Dict[str, Any]]:
        from core.embedding import cosine
        scored = []
        for fact_id, vec in self._vectors.items():
            sim = cosine(query_vector, vec)
            if sim <= 0.0:
                continue
            node = dict(self._nodes[fact_id])
            node["_relevance"] = round(sim, 6)
            node["_score"] = round(_salience_score(sim, node.get("significance", 0.5)), 6)
            scored.append(node)
        scored.sort(key=lambda n: n["_score"], reverse=True)
        return scored[:k]

    def get_edges(
        self, fact_id: str, rel_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        out = []
        for src, rel, dst, props in self._edges:
            if src != fact_id:
                continue
            if rel_type is not None and rel != rel_type:
                continue
            out.append({"rel_type": rel, "target": dst, "props": dict(props)})
        return out

    def incoming_edges(
        self, fact_id: str, rel_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        out = []
        for src, rel, dst, props in self._edges:
            if dst != fact_id:
                continue
            if rel_type is not None and rel != rel_type:
                continue
            out.append({"rel_type": rel, "source": src, "props": dict(props)})
        return out

    def clear(self) -> None:
        """Reset state (for tests)."""
        self._nodes.clear()
        self._edges.clear()
        self._vectors.clear()
        self._entities.clear()
        self._mentions.clear()
        self._embedder_fp = None


# ─── SQLITE BACKEND (on-disk, dependency-free) ─────────────────────────────────

def _synchronized(method):
    """Serialize a SqliteL3Graph method on the instance's reentrant lock.

    The connection is opened with check_same_thread=False so it can be reused
    across worker threads (e.g. asyncio.to_thread via core/aio.py); the RLock
    serializes access so a single sqlite3.Connection is never used concurrently.
    Reentrant because several methods call others (merge_fact → get_fact, etc.).
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        with self._lock:
            return method(self, *args, **kwargs)
    return wrapper


class SqliteL3Graph(L3GraphBackend):
    """
    On-disk L3 canon backed by SQLite (Python standard library — no external
    dependency). Same MERGE/edge/vector semantics as MockL3Graph, but the canon
    SURVIVES restarts: this is the local-first, dependency-free persistence
    target. Selected with VELANTRIM_L3_BACKEND=sqlite (and is the 'auto' fallback
    when LadybugDB is not installed). The DB file path is VELANTRIM_L3_PATH
    (default ./data/velantrim_l3.db); ':memory:' gives an ephemeral instance.

    Node payloads are stored as JSON; vectors as a JSON array of floats. Vector
    search is a linear cosine scan (fine for the MVP working-set; the LadybugDB
    backend adds a real vector index for scale). The embedder fingerprint is
    persisted in a meta row, so an embedder swap is detected across restarts too.
    """

    def __init__(self, db_path: Optional[str] = None) -> None:
        if db_path is None:
            db_path = os.environ.get("VELANTRIM_L3_PATH", "./data/velantrim_l3.db")
        if db_path not in (":memory:", "") and os.path.dirname(db_path):
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
        # check_same_thread=False + an RLock (see _synchronized): the cached
        # singleton connection is safe to reuse from asyncio worker threads.
        self._lock = threading.RLock()
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._ensure_schema()

    def close(self) -> None:
        """Close the underlying SQLite connection."""
        with self._lock:
            self._conn.close()

    def _ensure_schema(self) -> None:
        with self._conn:
            self._conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS nodes (
                    fact_id TEXT PRIMARY KEY,
                    data    TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS vectors (
                    fact_id TEXT PRIMARY KEY,
                    vec     TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS edges (
                    src      TEXT NOT NULL,
                    rel_type TEXT NOT NULL,
                    dst      TEXT NOT NULL,
                    props    TEXT NOT NULL DEFAULT '{}',
                    UNIQUE(src, rel_type, dst, props)
                );
                CREATE INDEX IF NOT EXISTS idx_edges_src ON edges(src);
                CREATE INDEX IF NOT EXISTS idx_edges_dst ON edges(dst);
                CREATE TABLE IF NOT EXISTS entities (
                    entity_id TEXT PRIMARY KEY,
                    kind      TEXT,
                    label     TEXT
                );
                CREATE TABLE IF NOT EXISTS mentions (
                    fact_id   TEXT NOT NULL,
                    entity_id TEXT NOT NULL,
                    rel       TEXT NOT NULL,
                    UNIQUE(fact_id, entity_id, rel)
                );
                CREATE TABLE IF NOT EXISTS meta (
                    key   TEXT PRIMARY KEY,
                    value TEXT
                );
                """
            )

    # ─── embedder fingerprint (persisted across restarts) ──────────────────────
    @_synchronized
    def embedder_fingerprint(self) -> Optional[str]:
        row = self._conn.execute(
            "SELECT value FROM meta WHERE key = 'embedder_fp'").fetchone()
        return row["value"] if row else None

    @_synchronized
    def set_embedder_fingerprint(self, fingerprint: str) -> None:
        with self._conn:
            self._conn.execute(
                "INSERT INTO meta(key, value) VALUES('embedder_fp', ?) "
                "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
                (fingerprint,))

    # ─── facts ─────────────────────────────────────────────────────────────────
    @_synchronized
    def merge_fact(self, fact: Dict[str, Any]) -> None:
        fact_id = fact.get("fact_id")
        if not fact_id:
            raise ValueError("merge_fact: fact_id is required")
        node = self.get_fact(fact_id) or {}
        node.update(fact)
        with self._conn:
            self._conn.execute(
                "INSERT INTO nodes(fact_id, data) VALUES(?, ?) "
                "ON CONFLICT(fact_id) DO UPDATE SET data = excluded.data",
                (fact_id, json.dumps(node)))
            claim = node.get("claim")
            if claim:
                from core.embedding import get_embedder
                vec = get_embedder().embed(claim)
                self._conn.execute(
                    "INSERT INTO vectors(fact_id, vec) VALUES(?, ?) "
                    "ON CONFLICT(fact_id) DO UPDATE SET vec = excluded.vec",
                    (fact_id, json.dumps(vec)))

    @_synchronized
    def get_fact(self, fact_id: str) -> Optional[Dict[str, Any]]:
        row = self._conn.execute(
            "SELECT data FROM nodes WHERE fact_id = ?", (fact_id,)).fetchone()
        return json.loads(row["data"]) if row else None

    @_synchronized
    def all_facts(self) -> List[Dict[str, Any]]:
        return [json.loads(r["data"])
                for r in self._conn.execute("SELECT data FROM nodes")]

    @_synchronized
    def erase_fact(self, fact_id: str) -> bool:
        with self._conn:
            cur = self._conn.execute(
                "DELETE FROM nodes WHERE fact_id = ?", (fact_id,))
            existed = cur.rowcount > 0
            self._conn.execute("DELETE FROM vectors WHERE fact_id = ?", (fact_id,))
            self._conn.execute(
                "DELETE FROM edges WHERE src = ? OR dst = ?", (fact_id, fact_id))
            self._conn.execute("DELETE FROM mentions WHERE fact_id = ?", (fact_id,))
        return existed

    # ─── edges ─────────────────────────────────────────────────────────────────
    @_synchronized
    def add_edge(
        self, src_id: str, rel_type: str, dst_id: str,
        props: Optional[Dict[str, Any]] = None,
    ) -> None:
        with self._conn:
            self._conn.execute(
                "INSERT OR IGNORE INTO edges(src, rel_type, dst, props) "
                "VALUES(?, ?, ?, ?)",
                (src_id, rel_type, dst_id, json.dumps(props or {}, sort_keys=True)))

    @_synchronized
    def neighbors(
        self, fact_id: str, rel_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        out = []
        for edge in self.get_edges(fact_id, rel_type):
            node = self.get_fact(edge["target"])
            if node is not None:
                out.append(node)
        return out

    @_synchronized
    def get_edges(
        self, fact_id: str, rel_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        q = "SELECT rel_type, dst, props FROM edges WHERE src = ?"
        params: List[Any] = [fact_id]
        if rel_type is not None:
            q += " AND rel_type = ?"
            params.append(rel_type)
        return [{"rel_type": r["rel_type"], "target": r["dst"],
                 "props": json.loads(r["props"])}
                for r in self._conn.execute(q, params)]

    @_synchronized
    def incoming_edges(
        self, fact_id: str, rel_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        q = "SELECT rel_type, src, props FROM edges WHERE dst = ?"
        params: List[Any] = [fact_id]
        if rel_type is not None:
            q += " AND rel_type = ?"
            params.append(rel_type)
        return [{"rel_type": r["rel_type"], "source": r["src"],
                 "props": json.loads(r["props"])}
                for r in self._conn.execute(q, params)]

    # ─── vectors ───────────────────────────────────────────────────────────────
    @_synchronized
    def vector_search(
        self, query_vector: List[float], k: int = 5,
    ) -> List[Dict[str, Any]]:
        from core.embedding import cosine
        scored = []
        for r in self._conn.execute("SELECT fact_id, vec FROM vectors"):
            sim = cosine(query_vector, json.loads(r["vec"]))
            if sim <= 0.0:
                continue
            node = self.get_fact(r["fact_id"])
            if node is None:
                continue
            node["_relevance"] = round(sim, 6)
            node["_score"] = round(_salience_score(sim, node.get("significance", 0.5)), 6)
            scored.append(node)
        scored.sort(key=lambda n: n["_score"], reverse=True)
        return scored[:k]

    # ─── entities ──────────────────────────────────────────────────────────────
    @_synchronized
    def merge_entity(self, entity_id: str, kind: str, label: str) -> None:
        with self._conn:
            self._conn.execute(
                "INSERT INTO entities(entity_id, kind, label) VALUES(?, ?, ?) "
                "ON CONFLICT(entity_id) DO UPDATE SET kind = excluded.kind, "
                "label = excluded.label",
                (entity_id, kind, label))

    @_synchronized
    def link_fact_to_entity(self, fact_id, entity_id, rel="MENTIONS") -> None:
        with self._conn:
            self._conn.execute(
                "INSERT OR IGNORE INTO mentions(fact_id, entity_id, rel) "
                "VALUES(?, ?, ?)", (fact_id, entity_id, rel))

    @_synchronized
    def facts_for_entity(self, entity_id: str) -> List[Dict[str, Any]]:
        rows = self._conn.execute(
            "SELECT fact_id FROM mentions WHERE entity_id = ?", (entity_id,))
        out = []
        for r in rows:
            node = self.get_fact(r["fact_id"])
            if node is not None:
                out.append(node)
        return out

    @_synchronized
    def clear(self) -> None:
        """Reset all state (for tests)."""
        with self._conn:
            for tbl in ("nodes", "vectors", "edges", "entities", "mentions", "meta"):
                self._conn.execute(f"DELETE FROM {tbl}")  # nosec B608 — tbl from hardcoded tuple


# ─── LADYBUGDB BACKEND (slot for the spike) ───────────────────────────────────────

class LadybugL3Graph(L3GraphBackend):  # pragma: no cover
    """
    Backend on LadybugDB — an embedded, Cypher-compatible successor to Kuzu
    (Kuzu frozen Oct.2025). Fact nodes + generalized EDGE edges with a type property.

    API verified by a spike (v0.17.0): Database/Connection, MERGE-upsert by
    PRIMARY KEY, REL tables, vector index (INSTALL vector / CREATE_VECTOR_INDEX).

    `ladybug` — optional dependency (native package + numpy). Lazy import;
    if missing — a clear ImportError. The default backend stays 'mock', and
    these methods are excluded from the coverage gate (pragma), since CI does not install ladybug;
    behavior is verified locally by tests under pytest.importorskip('ladybug').
    """

    # Columns of the Fact node that we persist (the rest — in metadata JSON).
    _COLS = [
        "fact_id", "claim", "source", "confidence", "epistemic_state",
        "claim_type", "source_status", "significance", "truth_status", "metadata",
    ]

    def __init__(self, db_path: Optional[str] = None) -> None:
        import os
        # The persistent DB path is configured via VELANTRIM_L3_PATH; the DB
        # survives restarts (unlike the in-memory mock default).
        if db_path is None:
            db_path = os.environ.get("VELANTRIM_L3_PATH", "./data/velantrim_l3.lbug")
        try:
            import ladybug as lb
        except ImportError as e:
            raise ImportError(
                "LadybugDB backend requires the 'ladybug' package (optional "
                "dependency): pip install ladybug. Default — backend='mock'."
            ) from e
        self._lb = lb
        self._db = lb.Database(db_path)
        self._conn = lb.Connection(self._db)
        self._ensure_schema()

    def _ensure_schema(self) -> None:
        from core.embedding import EMBED_DIM
        try:
            self._conn.execute("INSTALL vector; LOAD vector;")
        except Exception:
            pass  # extension already installed/loaded
        for ddl in (
            f"CREATE NODE TABLE Fact(fact_id STRING PRIMARY KEY, claim STRING, "
            f"source STRING, confidence DOUBLE, epistemic_state STRING, "
            f"claim_type STRING, source_status STRING, significance DOUBLE, "
            f"truth_status STRING, metadata STRING, embedding FLOAT[{EMBED_DIM}])",
            "CREATE REL TABLE EDGE(FROM Fact TO Fact, rel_type STRING, props STRING)",
            "CREATE NODE TABLE Entity(entity_id STRING PRIMARY KEY, kind STRING, label STRING)",
            "CREATE REL TABLE MENTIONS(FROM Fact TO Entity, rel STRING)",
        ):
            try:
                self._conn.execute(ddl)
            except Exception:
                pass  # table already exists — the schema is idempotent

    @staticmethod
    def _serialize(fact: Dict[str, Any]) -> Dict[str, Any]:
        # metadata is base64-encoded: LadybugDB auto-parses a STRING like {..}/[..]
        # as a map/list and loses JSON quotes, so we hide JSON behind base64.
        import json, base64
        out = {}
        for col in LadybugL3Graph._COLS:
            if col == "metadata":
                raw = json.dumps(fact.get("metadata", {})).encode("utf-8")
                out["metadata"] = base64.b64encode(raw).decode("ascii")
            elif col in fact:
                out[col] = fact[col]
        return out

    @staticmethod
    def _row_to_fact(row: list, cols: list) -> Dict[str, Any]:
        import json, base64
        d = dict(zip(cols, row))
        if "metadata" in d and isinstance(d["metadata"], str):
            try:
                d["metadata"] = json.loads(base64.b64decode(d["metadata"]))
            except (ValueError, TypeError):
                d["metadata"] = {}
        return {k: v for k, v in d.items() if v is not None}

    def merge_fact(self, fact: Dict[str, Any]) -> None:
        fact_id = fact.get("fact_id")
        if not fact_id:
            raise ValueError("merge_fact: fact_id is required")
        params = self._serialize(fact)
        sets = [f"f.{c} = ${c}" for c in params if c != "fact_id"]
        # Embedding of the claim into a FLOAT[] column for the native vector index.
        claim = fact.get("claim")
        if claim:
            from core.embedding import get_embedder
            params["embedding"] = get_embedder().embed(claim)
            sets.append("f.embedding = $embedding")
        cypher = "MERGE (f:Fact {fact_id: $fact_id})"
        if sets:
            cypher += " SET " + ", ".join(sets)
        self._conn.execute(cypher, params)

    def get_fact(self, fact_id: str) -> Optional[Dict[str, Any]]:
        cols = self._COLS
        ret = ", ".join(f"f.{c}" for c in cols)
        res = self._conn.execute(
            f"MATCH (f:Fact {{fact_id: $id}}) RETURN {ret}", {"id": fact_id})
        if not res.has_next():
            return None
        return self._row_to_fact(res.get_next(), cols)

    def erase_fact(self, fact_id: str) -> bool:
        existed = self.get_fact(fact_id) is not None
        # DETACH DELETE removes the node together with all incident edges
        # (EDGE + MENTIONS) — no dangling references remain.
        self._conn.execute(
            "MATCH (f:Fact {fact_id: $id}) DETACH DELETE f", {"id": fact_id})
        return existed

    def all_facts(self) -> List[Dict[str, Any]]:
        cols = self._COLS
        ret = ", ".join(f"f.{c}" for c in cols)
        res = self._conn.execute(f"MATCH (f:Fact) RETURN {ret}")
        out = []
        while res.has_next():
            out.append(self._row_to_fact(res.get_next(), cols))
        return out

    def add_edge(
        self, src_id: str, rel_type: str, dst_id: str,
        props: Optional[Dict[str, Any]] = None,
    ) -> None:
        import json, base64
        # props in base64 for the same reason as metadata (see _serialize).
        payload = base64.b64encode(json.dumps(props or {}).encode("utf-8")).decode("ascii")
        self._conn.execute(
            "MATCH (a:Fact {fact_id: $s}), (b:Fact {fact_id: $d}) "
            "MERGE (a)-[e:EDGE {rel_type: $rt}]->(b) SET e.props = $p",
            {"s": src_id, "d": dst_id, "rt": rel_type, "p": payload})

    def neighbors(
        self, fact_id: str, rel_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        cols = self._COLS
        ret = ", ".join(f"b.{c}" for c in cols)
        cypher = "MATCH (a:Fact {fact_id: $id})-[e:EDGE]->(b:Fact)"
        params: Dict[str, Any] = {"id": fact_id}
        if rel_type is not None:
            cypher += " WHERE e.rel_type = $rt"
            params["rt"] = rel_type
        res = self._conn.execute(f"{cypher} RETURN {ret}", params)
        out = []
        while res.has_next():
            out.append(self._row_to_fact(res.get_next(), cols))
        return out

    def get_edges(
        self, fact_id: str, rel_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        import json, base64
        cypher = "MATCH (a:Fact {fact_id: $id})-[e:EDGE]->(b:Fact)"
        params: Dict[str, Any] = {"id": fact_id}
        if rel_type is not None:
            cypher += " WHERE e.rel_type = $rt"
            params["rt"] = rel_type
        res = self._conn.execute(
            f"{cypher} RETURN e.rel_type, b.fact_id, e.props", params)
        out = []
        while res.has_next():
            rel, target, raw = res.get_next()
            try:
                props = json.loads(base64.b64decode(raw)) if raw else {}
            except (ValueError, TypeError):
                props = {}
            out.append({"rel_type": rel, "target": target, "props": props})
        return out

    def incoming_edges(
        self, fact_id: str, rel_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        import json, base64
        cypher = "MATCH (a:Fact)-[e:EDGE]->(b:Fact {fact_id: $id})"
        params: Dict[str, Any] = {"id": fact_id}
        if rel_type is not None:
            cypher += " WHERE e.rel_type = $rt"
            params["rt"] = rel_type
        res = self._conn.execute(
            f"{cypher} RETURN e.rel_type, a.fact_id, e.props", params)
        out = []
        while res.has_next():
            rel, source, raw = res.get_next()
            try:
                props = json.loads(base64.b64decode(raw)) if raw else {}
            except (ValueError, TypeError):
                props = {}
            out.append({"rel_type": rel, "source": source, "props": props})
        return out

    def merge_entity(self, entity_id: str, kind: str, label: str) -> None:
        self._conn.execute(
            "MERGE (e:Entity {entity_id: $id}) SET e.kind = $kind, e.label = $label",
            {"id": entity_id, "kind": kind, "label": label})

    def link_fact_to_entity(self, fact_id, entity_id, rel="MENTIONS") -> None:
        self._conn.execute(
            "MATCH (f:Fact {fact_id: $f}), (e:Entity {entity_id: $e}) "
            "MERGE (f)-[m:MENTIONS {rel: $rel}]->(e)",
            {"f": fact_id, "e": entity_id, "rel": rel})

    def facts_for_entity(self, entity_id: str) -> List[Dict[str, Any]]:
        cols = self._COLS
        ret = ", ".join(f"f.{c}" for c in cols)
        res = self._conn.execute(
            f"MATCH (f:Fact)-[:MENTIONS]->(e:Entity {{entity_id: $id}}) RETURN {ret}",
            {"id": entity_id})
        out = []
        while res.has_next():
            out.append(self._row_to_fact(res.get_next(), cols))
        return out

    def vector_search(
        self, query_vector: List[float], k: int = 5,
    ) -> List[Dict[str, Any]]:
        # We create the index once: the spike confirmed that rows added
        # AFTER creation are visible to search — an expensive DROP+CREATE on every query
        # is not needed. A repeated CREATE → "already exists" → swallow it.
        try:
            self._conn.execute("CALL CREATE_VECTOR_INDEX('Fact', 'fact_vec', 'embedding')")
        except Exception:
            pass  # index already exists, or there are no rows with an embedding yet
        # Fetch with a margin (k*3), then re-rank by significance so that
        # a salient memory does not drop out of top-k when cosines are close.
        # distance — cosine distance (0 = exact).
        try:
            res = self._conn.execute(
                "CALL QUERY_VECTOR_INDEX('Fact', 'fact_vec', $q, $k) "
                "RETURN node.fact_id, distance",
                {"q": query_vector, "k": max(k * 3, k)})
        except Exception:
            return []  # no index (empty graph) — nothing to search
        out = []
        while res.has_next():
            fact_id, distance = res.get_next()
            node = self.get_fact(fact_id)
            if node is not None:
                sim = 1.0 - distance  # similarity ≈ 1 - cosine distance
                node["_relevance"] = round(sim, 6)
                node["_score"] = round(_salience_score(sim, node.get("significance", 0.5)), 6)
                out.append(node)
        out.sort(key=lambda n: n["_score"], reverse=True)
        return out[:k]


# ─── NEO4J BACKEND (optional alternative) ────────────────────────────────

class Neo4jL3Graph(L3GraphBackend):  # pragma: no cover
    """
    Backend on Neo4j (optional alternative to LadybugDB). Standard Cypher
    via the neo4j driver; config — NEO4J_URI / NEO4J_USER / NEO4J_PASSWORD /
    NEO4J_DATABASE. metadata and edge props are stored as a JSON string (Neo4j does
    not allow nested maps in properties); embedding — a float array.

    `neo4j` — optional dependency (lazy import). vector_search computes
    cosine on the Python side (version-independent, without Neo4j's vector index).

    Network backend: requires a running Neo4j server. There is no server in this
    environment, so the class is excluded from the coverage gate; the Cypher mirrors the
    LadybugL3Graph verified in the spike (MERGE/MATCH semantics are identical).
    """

    def __init__(self) -> None:
        import os
        try:
            from neo4j import GraphDatabase
        except ImportError as e:
            raise ImportError(
                "Neo4j backend requires the 'neo4j' package (optional dependency): "
                "pip install neo4j. Default — backend='auto' (LadybugDB/mock)."
            ) from e
        uri = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
        user = os.environ.get("NEO4J_USER", "neo4j")
        password = os.environ.get("NEO4J_PASSWORD", "neo4j")
        self._db = os.environ.get("NEO4J_DATABASE", "neo4j")
        self._driver = GraphDatabase.driver(uri, auth=(user, password))
        self._driver.execute_query(
            "CREATE CONSTRAINT fact_id IF NOT EXISTS "
            "FOR (f:Fact) REQUIRE f.fact_id IS UNIQUE",
            database_=self._db)

    def _run(self, cypher: str, **params):
        records, _, _ = self._driver.execute_query(
            cypher, database_=self._db, **params)
        return records

    @staticmethod
    def _props(fact: Dict[str, Any]) -> Dict[str, Any]:
        import json
        out = {}
        for k, v in fact.items():
            if k.startswith("_"):
                continue
            out[k] = json.dumps(v) if k == "metadata" else v
        return out

    @staticmethod
    def _node(props: Dict[str, Any]) -> Dict[str, Any]:
        import json
        d = dict(props)
        if isinstance(d.get("metadata"), str):
            try:
                d["metadata"] = json.loads(d["metadata"])
            except (ValueError, TypeError):
                d["metadata"] = {}
        d.pop("embedding", None)
        return d

    def merge_fact(self, fact: Dict[str, Any]) -> None:
        if not fact.get("fact_id"):
            raise ValueError("merge_fact: fact_id is required")
        props = self._props(fact)
        if fact.get("claim"):
            from core.embedding import get_embedder
            props["embedding"] = get_embedder().embed(fact["claim"])
        self._run("MERGE (f:Fact {fact_id: $id}) SET f += $props",
                  id=fact["fact_id"], props=props)

    def get_fact(self, fact_id: str) -> Optional[Dict[str, Any]]:
        rows = self._run(
            "MATCH (f:Fact {fact_id: $id}) RETURN properties(f) AS p", id=fact_id)
        return self._node(rows[0]["p"]) if rows else None

    def erase_fact(self, fact_id: str) -> bool:
        existed = self.get_fact(fact_id) is not None
        # DETACH DELETE removes the node with all incident edges (EDGE/MENTIONS).
        self._run("MATCH (f:Fact {fact_id: $id}) DETACH DELETE f", id=fact_id)
        return existed

    def all_facts(self) -> List[Dict[str, Any]]:
        rows = self._run("MATCH (f:Fact) RETURN properties(f) AS p")
        return [self._node(r["p"]) for r in rows]

    def add_edge(self, src_id, rel_type, dst_id, props=None) -> None:
        import json
        self._run(
            "MATCH (a:Fact {fact_id: $s}), (b:Fact {fact_id: $d}) "
            "MERGE (a)-[e:EDGE {rel_type: $rt}]->(b) SET e.props = $p",
            s=src_id, d=dst_id, rt=rel_type, p=json.dumps(props or {}))

    def neighbors(self, fact_id, rel_type=None) -> List[Dict[str, Any]]:
        cypher = "MATCH (a:Fact {fact_id: $id})-[e:EDGE]->(b:Fact)"
        params = {"id": fact_id}
        if rel_type is not None:
            cypher += " WHERE e.rel_type = $rt"
            params["rt"] = rel_type
        rows = self._run(cypher + " RETURN properties(b) AS p", **params)
        return [self._node(r["p"]) for r in rows]

    def get_edges(self, fact_id, rel_type=None) -> List[Dict[str, Any]]:
        import json
        cypher = "MATCH (a:Fact {fact_id: $id})-[e:EDGE]->(b:Fact)"
        params = {"id": fact_id}
        if rel_type is not None:
            cypher += " WHERE e.rel_type = $rt"
            params["rt"] = rel_type
        rows = self._run(
            cypher + " RETURN e.rel_type AS rt, b.fact_id AS t, e.props AS p", **params)
        out = []
        for r in rows:
            try:
                props = json.loads(r["p"]) if r["p"] else {}
            except (ValueError, TypeError):
                props = {}
            out.append({"rel_type": r["rt"], "target": r["t"], "props": props})
        return out

    def incoming_edges(self, fact_id, rel_type=None) -> List[Dict[str, Any]]:
        import json
        cypher = "MATCH (a:Fact)-[e:EDGE]->(b:Fact {fact_id: $id})"
        params = {"id": fact_id}
        if rel_type is not None:
            cypher += " WHERE e.rel_type = $rt"
            params["rt"] = rel_type
        rows = self._run(
            cypher + " RETURN e.rel_type AS rt, a.fact_id AS s, e.props AS p", **params)
        out = []
        for r in rows:
            try:
                props = json.loads(r["p"]) if r["p"] else {}
            except (ValueError, TypeError):
                props = {}
            out.append({"rel_type": r["rt"], "source": r["s"], "props": props})
        return out

    def merge_entity(self, entity_id, kind, label) -> None:
        self._run("MERGE (e:Entity {entity_id: $id}) SET e.kind = $k, e.label = $l",
                  id=entity_id, k=kind, l=label)

    def link_fact_to_entity(self, fact_id, entity_id, rel="MENTIONS") -> None:
        self._run(
            "MATCH (f:Fact {fact_id: $f}), (e:Entity {entity_id: $e}) "
            "MERGE (f)-[m:MENTIONS {rel: $rel}]->(e)",
            f=fact_id, e=entity_id, rel=rel)

    def facts_for_entity(self, entity_id) -> List[Dict[str, Any]]:
        rows = self._run(
            "MATCH (f:Fact)-[:MENTIONS]->(e:Entity {entity_id: $id}) "
            "RETURN properties(f) AS p", id=entity_id)
        return [self._node(r["p"]) for r in rows]

    def vector_search(self, query_vector, k=5) -> List[Dict[str, Any]]:
        from core.embedding import cosine
        rows = self._run(
            "MATCH (f:Fact) WHERE f.embedding IS NOT NULL "
            "RETURN f.fact_id AS id, f.embedding AS v")
        scored = []
        for r in rows:
            sim = cosine(query_vector, r["v"])
            if sim <= 0.0:
                continue
            node = self.get_fact(r["id"])
            if node is None:
                continue
            node["_relevance"] = round(sim, 6)
            node["_score"] = round(_salience_score(sim, node.get("significance", 0.5)), 6)
            scored.append(node)
        scored.sort(key=lambda n: n["_score"], reverse=True)
        return scored[:k]


# ─── FACTORY / SINGLETON ──────────────────────────────────────────────────────

_BACKENDS = {
    "mock": MockL3Graph,        # in-memory, dependency-free (dev / CI)
    "sqlite": SqliteL3Graph,    # on-disk, dependency-free (local-first persistence)
    "ladybug": LadybugL3Graph,  # recommended prod default (successor to Kuzu)
    "neo4j": Neo4jL3Graph,      # optional alternative (server required)
}


def _make(name: str) -> L3GraphBackend:
    if name == "auto":
        # Prod default: LadybugDB if available (vector index, scale); otherwise the
        # dependency-free on-disk SQLite backend (local-first persistence). The
        # in-memory mock is the last-resort fallback if even SQLite cannot open.
        try:
            return LadybugL3Graph()
        except Exception as e:  # noqa: BLE001 — any init failure → fallback
            logger.warning(
                "auto L3: LadybugDB unavailable (%s), falling back to on-disk SQLite",
                type(e).__name__,
            )
        try:
            return SqliteL3Graph()
        except Exception as e:  # noqa: BLE001 — disk/permission issue → in-memory
            logger.warning(
                "auto L3: SQLite unavailable (%s), falling back to in-memory mock",
                type(e).__name__,
            )
            return MockL3Graph()
    if name not in _BACKENDS:
        raise ValueError(
            f"get_l3_graph: unknown backend '{name}'. "
            f"Available: {sorted(_BACKENDS) + ['auto']}"
        )
    return _BACKENDS[name]()


_REGISTRY = BackendRegistry("VELANTRIM_L3_BACKEND", "auto", _make)


def get_l3_graph(backend: Optional[str] = None) -> L3GraphBackend:
    """
    Return the L3 graph singleton. Backend — via argument or VELANTRIM_L3_BACKEND.

    Modes:
      'auto' (default) — LadybugDB if installed (the recommended prod engine,
                        successor to Kuzu); otherwise the dependency-free on-disk
                        SQLite backend (persists to ./data/velantrim_l3.db); the
                        in-memory mock only as a last resort if SQLite cannot open.
      'sqlite'        — always on-disk SQLite (dependency-free, local-first).
      'ladybug'       — always LadybugDB (ImportError if the package is missing).
      'neo4j'         — optional alternative (a running server is required).
      'mock'          — always in-memory (dev / CI).
    """
    return _REGISTRY.get(backend)


def reset_l3_graph() -> None:
    """Reset the singleton (for tests)."""
    _REGISTRY.reset()
