"""Bounded CR-09 recovery regressions using real, disposable SQLite L1/L3.

Only explicit recorded edges are exercised. Injected exceptions model an
interrupted invocation, not OS-level power loss or a concurrent read fence.
"""
import pytest

from core import erasure, memory
from core.l3_graph import SqliteL3Graph


@pytest.fixture
def durable_graph(tmp_path, monkeypatch):
    graphs = []

    def reopen():
        graph = SqliteL3Graph(str(tmp_path / "cascade-l3.db"))
        graphs.append(graph)
        monkeypatch.setattr(erasure, "get_l3_graph", lambda: graph)
        memory._L0.clear()
        return graph

    yield reopen
    for graph in graphs:
        graph.close()


def _seed(graph, fact_id):
    memory.store_fact({
        "fact_id": fact_id,
        "claim": "Synthetic cascade sample " + fact_id,
        "source": "synthetic",
        "epistemic_state": "Validated",
    })
    graph.merge_fact(memory.get_fact(fact_id))


def _assert_gone(graph, *ids):
    for fact_id in ids:
        assert memory.get_fact(fact_id) is None
        assert graph.get_fact(fact_id) is None
        assert erasure.is_erased(fact_id)


def test_resume_cascade_after_parent_tombstone(durable_graph, monkeypatch):
    graph = durable_graph()
    for fid in ("root", "child", "grandchild", "independent"):
        _seed(graph, fid)
    erasure.record_derivation("child", "root")
    erasure.record_derivation("grandchild", "child")
    erasure.record_derivation("child", "independent")
    erase = graph.erase_fact

    def interrupt_child(fact_id):
        if fact_id == "child":
            raise RuntimeError("synthetic interrupted child erase")
        return erase(fact_id)

    with monkeypatch.context() as patch:
        patch.setattr(graph, "erase_fact", interrupt_child)
        with pytest.raises(RuntimeError, match="synthetic interrupted child erase"):
            erasure.erase_fact("root", cascade=True)
    assert erasure.is_erased("root")
    original_root = memory.get_tombstone("root")
    assert graph.incoming_edges("root", erasure.REL_DERIVED_FROM) == []
    assert graph.get_fact("child") is not None

    # Drop process-local cache and reopen the same on-disk graph.
    graph = durable_graph()
    result = erasure.erase_fact("root", cascade=True)
    _assert_gone(graph, "root", "child", "grandchild")
    assert memory.get_tombstone("root") == original_root
    assert {row["fact_id"] for row in result["cascaded"]} == {"child"}
    assert memory.get_fact("independent") is not None
    assert graph.get_fact("independent") is not None
    assert erasure.erase_fact("root", cascade=True)["cascaded"] == []


def test_resume_cascade_after_parent_graph_delete_before_tombstone(
    durable_graph, monkeypatch
):
    graph = durable_graph()
    _seed(graph, "root")
    _seed(graph, "child")
    erasure.record_derivation("child", "root")
    write = erasure.write_tombstone

    def interrupt_tombstone(fact_id, **kwargs):
        if fact_id == "root":
            raise RuntimeError("synthetic interruption before tombstone")
        return write(fact_id, **kwargs)

    with monkeypatch.context() as patch:
        patch.setattr(erasure, "write_tombstone", interrupt_tombstone)
        with pytest.raises(RuntimeError, match="synthetic interruption before tombstone"):
            erasure.erase_fact("root", cascade=True)

    assert memory.get_fact("root") is None
    assert graph.get_fact("root") is None
    assert not erasure.is_erased("root")
    assert graph.get_fact("child") is not None

    graph = durable_graph()
    result = erasure.erase_fact("root", cascade=True)
    _assert_gone(graph, "root", "child")
    assert {row["fact_id"] for row in result["cascaded"]} == {"child"}
    # The original claim was already deleted before its tombstone was written.
    # Do not manufacture a digest or pretend that earlier proof was recovered.
    assert memory.get_tombstone("root")["content_hash"] is None


def test_cascade_plan_contains_only_pending_ids_and_is_released(
    durable_graph, monkeypatch
):
    graph = durable_graph()
    _seed(graph, "root")
    _seed(graph, "child")
    erasure.record_derivation("child", "root")
    erase = graph.erase_fact

    def interrupt_root(fact_id):
        if fact_id == "root":
            raise RuntimeError("synthetic interrupted root erase")
        return erase(fact_id)

    with monkeypatch.context() as patch:
        patch.setattr(graph, "erase_fact", interrupt_root)
        with pytest.raises(RuntimeError, match="synthetic interrupted root erase"):
            erasure.erase_fact("root", cascade=True)
    with memory._db() as conn:
        rows = [tuple(row) for row in conn.execute(
            "SELECT * FROM erasure_cascade_targets"
        )]
    assert rows == [("root", "child")]
    erasure.erase_fact("root", cascade=True)
    _assert_gone(graph, "root", "child")
    with memory._db() as conn:
        assert conn.execute(
            "SELECT COUNT(*) FROM erasure_cascade_targets"
        ).fetchone()[0] == 0
