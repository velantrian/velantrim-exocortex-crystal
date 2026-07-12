"""Tests for the dependency-free on-disk SQLite L3 backend."""
import pytest

from core.l3_graph import SqliteL3Graph, get_l3_graph, reset_l3_graph
from core.embedding import get_embedder


def _g(tmp_path, name="l3.db"):
    return SqliteL3Graph(db_path=str(tmp_path / name))


def _fact(fid, claim, **kw):
    return {"fact_id": fid, "claim": claim, "source": "s", "confidence": 0.9,
            "epistemic_state": "Validated", "claim_type": "WORLD_FACT",
            "significance": 0.5, **kw}


# ─── facts: merge / get / all ─────────────────────────────────────────────────

def test_merge_and_get(tmp_path):
    g = _g(tmp_path)
    g.merge_fact(_fact("a", "Water boils at 100 degrees"))
    node = g.get_fact("a")
    assert node["claim"] == "Water boils at 100 degrees"
    assert node["confidence"] == 0.9
    assert g.get_fact("missing") is None


def test_merge_is_idempotent_upsert(tmp_path):
    g = _g(tmp_path)
    g.merge_fact(_fact("a", "first"))
    g.merge_fact(_fact("a", "second", confidence=0.4))
    assert len(g.all_facts()) == 1
    assert g.get_fact("a")["claim"] == "second"
    assert g.get_fact("a")["confidence"] == 0.4


def test_merge_requires_fact_id(tmp_path):
    with pytest.raises(ValueError, match="fact_id"):
        _g(tmp_path).merge_fact({"claim": "no id"})


# ─── persistence across instances (the whole point) ───────────────────────────

def test_canon_survives_reopen(tmp_path):
    path = str(tmp_path / "persist.db")
    g1 = SqliteL3Graph(db_path=path)
    g1.merge_fact(_fact("a", "Earth orbits the Sun"))
    g1.add_edge("a", "RELATED_TO", "b", {"w": 1})
    g1._conn.close()

    g2 = SqliteL3Graph(db_path=path)  # fresh instance, same file
    assert g2.get_fact("a")["claim"] == "Earth orbits the Sun"
    assert g2.get_edges("a")[0]["target"] == "b"
    assert g2.get_edges("a")[0]["props"] == {"w": 1}


# ─── erase (GDPR Art. 17 cascade) ─────────────────────────────────────────────

def test_erase_removes_node_edges_vector_mentions(tmp_path):
    g = _g(tmp_path)
    g.merge_fact(_fact("a", "fact a"))
    g.merge_fact(_fact("b", "fact b"))
    g.add_edge("a", "LINK", "b")
    g.add_edge("b", "LINK", "a")
    g.merge_entity("who:bob", "person", "Bob")
    g.link_fact_to_entity("a", "who:bob")

    assert g.erase_fact("a") is True
    assert g.get_fact("a") is None
    assert g.get_edges("b") == []          # incoming/outgoing to a are gone
    assert g.incoming_edges("b") == []
    assert g.facts_for_entity("who:bob") == []
    assert g.vector_search(get_embedder().embed("fact a")) == [] or \
        all(n["fact_id"] != "a" for n in g.vector_search(get_embedder().embed("fact a")))
    assert g.erase_fact("a") is False      # idempotent


# ─── edges ────────────────────────────────────────────────────────────────────

def test_edges_and_neighbors(tmp_path):
    g = _g(tmp_path)
    g.merge_fact(_fact("a", "alpha"))
    g.merge_fact(_fact("b", "beta"))
    g.add_edge("a", "CONTRADICTS", "b", {"signal": "negation"})
    assert g.get_edges("a", "CONTRADICTS")[0]["target"] == "b"
    assert g.incoming_edges("b", "CONTRADICTS")[0]["source"] == "a"
    assert g.neighbors("a")[0]["fact_id"] == "b"
    # filter misses
    assert g.get_edges("a", "OTHER") == []


def test_edge_dedup(tmp_path):
    g = _g(tmp_path)
    g.add_edge("a", "LINK", "b", {"x": 1})
    g.add_edge("a", "LINK", "b", {"x": 1})   # identical → deduped
    g.add_edge("a", "LINK", "b", {"x": 2})   # different props → distinct
    assert len(g.get_edges("a")) == 2


# ─── vector search ────────────────────────────────────────────────────────────

def test_vector_search_ranks_by_similarity(tmp_path):
    g = _g(tmp_path)
    g.merge_fact(_fact("phys", "Water boils at 100 degrees celsius"))
    g.merge_fact(_fact("bio", "Cells divide during mitosis"))
    hits = g.vector_search(get_embedder().embed("at what temperature does water boil"))
    assert hits and hits[0]["fact_id"] == "phys"
    assert "_relevance" in hits[0] and "_score" in hits[0]


def test_vector_search_materializes_candidates_with_one_select(tmp_path):
    """Regression: vector search must not issue one get_fact SELECT per hit."""
    g = _g(tmp_path)
    for i in range(25):
        g.merge_fact(_fact(f"f{i}", f"shared benchmark topic item {i}"))

    statements = []
    g._conn.set_trace_callback(statements.append)
    hits = g.vector_search(get_embedder().embed("shared benchmark topic"), k=5)
    g._conn.set_trace_callback(None)

    selects = [sql for sql in statements if sql.lstrip().upper().startswith("SELECT")]
    assert len(selects) == 1
    assert "JOIN nodes" in selects[0]
    assert len(hits) == 5


# ─── entities ─────────────────────────────────────────────────────────────────

def test_entities_round_trip(tmp_path):
    g = _g(tmp_path)
    g.merge_fact(_fact("a", "Bob lives in Paris"))
    g.merge_entity("where:Paris", "place", "Paris")
    g.link_fact_to_entity("a", "where:Paris")
    g.link_fact_to_entity("a", "where:Paris")  # idempotent
    facts = g.facts_for_entity("where:Paris")
    assert len(facts) == 1 and facts[0]["fact_id"] == "a"


# ─── embedder fingerprint persists across restarts ────────────────────────────

def test_embedder_fingerprint_persists(tmp_path):
    path = str(tmp_path / "fp.db")
    g1 = SqliteL3Graph(db_path=path)
    assert g1.embedder_fingerprint() is None
    g1.set_embedder_fingerprint("hashing-2048")
    g1._conn.close()
    g2 = SqliteL3Graph(db_path=path)
    assert g2.embedder_fingerprint() == "hashing-2048"


# ─── clear ────────────────────────────────────────────────────────────────────

def test_clear_wipes_state(tmp_path):
    g = _g(tmp_path)
    g.merge_fact(_fact("a", "x"))
    g.add_edge("a", "L", "b")
    g.clear()
    assert g.all_facts() == []
    assert g.get_edges("a") == []


# ─── factory selection ────────────────────────────────────────────────────────

def test_factory_selects_sqlite(monkeypatch, tmp_path):
    monkeypatch.setenv("VELANTRIM_L3_BACKEND", "sqlite")
    monkeypatch.setenv("VELANTRIM_L3_PATH", str(tmp_path / "factory.db"))
    reset_l3_graph()
    assert isinstance(get_l3_graph(), SqliteL3Graph)
    reset_l3_graph()


def test_default_path_creates_dir(monkeypatch, tmp_path):
    target = tmp_path / "nested" / "dir" / "l3.db"
    monkeypatch.setenv("VELANTRIM_L3_PATH", str(target))
    g = SqliteL3Graph()
    g.merge_fact(_fact("a", "persisted"))
    assert target.exists()


# ─── thread-safety (#71): connection reused across worker threads ──────────────

def test_merge_and_read_from_another_thread(tmp_path):
    # The cached connection is opened check_same_thread=False; reuse from a
    # different thread must not raise sqlite3.ProgrammingError.
    import threading
    g = _g(tmp_path)
    g.merge_fact(_fact("a", "Water boils at 100 degrees"))

    result = {}
    errors = []

    def worker():
        try:
            result["node"] = g.get_fact("a")
            g.merge_fact(_fact("b", "Gold is a metal"))
            result["all"] = len(g.all_facts())
        except Exception as e:  # noqa: BLE001 — capture for assertion
            errors.append(e)

    t = threading.Thread(target=worker)
    t.start()
    t.join()

    assert not errors, f"cross-thread access raised: {errors}"
    assert result["node"]["claim"] == "Water boils at 100 degrees"
    assert result["all"] == 2


def test_concurrent_writes_are_serialized(tmp_path):
    # Many threads writing through the lock must all land without corruption.
    import threading
    g = _g(tmp_path)

    def writer(i):
        g.merge_fact(_fact(f"f{i}", f"claim number {i}"))

    threads = [threading.Thread(target=writer, args=(i,)) for i in range(20)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert len(g.all_facts()) == 20


# ─── reset closes the connection (#73 / M2) ───────────────────────────────────

def test_reset_l3_graph_closes_sqlite_connection(tmp_path, monkeypatch):
    monkeypatch.setenv("VELANTRIM_L3_BACKEND", "sqlite")
    monkeypatch.setenv("VELANTRIM_L3_PATH", str(tmp_path / "reset.db"))
    reset_l3_graph()
    g = get_l3_graph()            # caches a SqliteL3Graph singleton
    g.merge_fact(_fact("a", "Water boils"))
    reset_l3_graph()             # must close g's connection, no accumulation
    # The old connection is closed; using it now raises ProgrammingError.
    import sqlite3
    with pytest.raises(sqlite3.ProgrammingError):
        g._conn.execute("SELECT 1")
    # A fresh singleton still works.
    assert get_l3_graph().get_fact("a") is not None
    reset_l3_graph()
