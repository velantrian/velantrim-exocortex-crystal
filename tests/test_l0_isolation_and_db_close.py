"""L0 must own its records, and _db() must close its connection on schema failure.

L0 isolation: get_fact() and store_fact(return_persisted=True) used to hand
callers the very dict held in the process-local L0 cache (or a shallow copy
sharing nested metadata), and store_fact() cached the caller's own metadata
dict. The freshness check in get_fact() compares the raw L1 row, not the
cached dict, so a caller mutating a returned object changed later reads in
this process without any write. The SQLite row itself was never changed.

_db(): _ensure_schema(conn) ran before the try/finally that closes the
connection, so a schema or migration failure leaked the connection.
"""
import sqlite3

import pytest

from core import memory
from core.memory import get_fact, set_restricted, store_fact


def _store(fid="iso1", **extra):
    fact = {"fact_id": fid, "claim": "original claim", "source": "s",
            "metadata": {"tags": ["a"], "nested": {"k": "v"}}}
    fact.update(extra)
    return store_fact(fact)


def _row(fid):
    with memory._db() as conn:
        return dict(conn.execute(
            "SELECT claim, restricted FROM facts WHERE fact_id = ?", (fid,)
        ).fetchone())


class TestGetFactReturnsCopies:
    def test_top_level_mutation_does_not_change_next_read(self):
        _store()
        first = get_fact("iso1")
        first["claim"] = "tampered"
        first["epistemic_state"] = "Validated"
        second = get_fact("iso1")
        assert second["claim"] == "original claim"
        assert second["epistemic_state"] == "Observed"

    def test_nested_mutation_does_not_change_next_read(self):
        _store()
        first = get_fact("iso1")
        first["metadata"]["tags"].append("b")
        first["metadata"]["nested"]["k"] = "changed"
        second = get_fact("iso1")
        assert second["metadata"] == {"tags": ["a"], "nested": {"k": "v"}}

    def test_restricted_flag_cannot_be_lifted_through_a_returned_object(self):
        _store()
        assert set_restricted("iso1", True) is True
        got = get_fact("iso1")
        assert got["restricted"]
        got["restricted"] = 0
        assert get_fact("iso1")["restricted"]
        assert _row("iso1")["restricted"] == 1

    def test_mutation_after_l1_rebuild_does_not_change_next_read(self):
        # Covers the branch that rebuilds the record from L1 (cache miss).
        _store()
        memory._L0.clear()
        first = get_fact("iso1")
        first["metadata"]["nested"]["k"] = "changed"
        first["claim"] = "tampered"
        second = get_fact("iso1")
        assert second["claim"] == "original claim"
        assert second["metadata"]["nested"]["k"] == "v"

    def test_each_read_is_a_distinct_object(self):
        _store()
        a, b = get_fact("iso1"), get_fact("iso1")
        assert a == b
        assert a is not b
        assert a["metadata"] is not b["metadata"]


class TestStoreFactDoesNotShareWithCaller:
    def test_caller_metadata_mutation_after_store_does_not_change_read(self):
        meta = {"tags": ["a"], "nested": {"k": "v"}}
        store_fact({"fact_id": "iso2", "claim": "c", "source": "s",
                    "metadata": meta})
        meta["tags"].append("b")
        meta["nested"]["k"] = "changed"
        assert get_fact("iso2")["metadata"] == {"tags": ["a"], "nested": {"k": "v"}}

    def test_return_persisted_snapshot_is_independent(self):
        snap = store_fact(
            {"fact_id": "iso3", "claim": "c", "source": "s",
             "metadata": {"nested": {"k": "v"}}},
            return_persisted=True,
        )
        snap["metadata"]["nested"]["k"] = "changed"
        snap["claim"] = "tampered"
        got = get_fact("iso3")
        assert got["metadata"]["nested"]["k"] == "v"
        assert got["claim"] == "c"


class _TrackingConnection(sqlite3.Connection):
    closed_count = 0

    def close(self):
        type(self).closed_count += 1
        super().close()


class TestDbClosesOnSchemaFailure:
    def test_connection_is_closed_when_ensure_schema_raises(self, monkeypatch):
        opened = []
        real_connect = sqlite3.connect

        def tracking_connect(*args, **kwargs):
            conn = real_connect(*args, factory=_TrackingConnection, **kwargs)
            opened.append(conn)
            return conn

        def broken_schema(conn):
            raise sqlite3.OperationalError("schema boom")

        _TrackingConnection.closed_count = 0
        monkeypatch.setattr(memory.sqlite3, "connect", tracking_connect)
        monkeypatch.setattr(memory, "_ensure_schema", broken_schema)

        with pytest.raises(sqlite3.OperationalError, match="schema boom"):
            with memory._db():
                pytest.fail("body must not run when schema setup fails")

        assert len(opened) == 1
        assert _TrackingConnection.closed_count == 1
        with pytest.raises(sqlite3.ProgrammingError):
            opened[0].execute("SELECT 1")

    def test_normal_use_still_commits_and_closes(self, monkeypatch):
        opened = []
        real_connect = sqlite3.connect

        def tracking_connect(*args, **kwargs):
            conn = real_connect(*args, factory=_TrackingConnection, **kwargs)
            opened.append(conn)
            return conn

        _TrackingConnection.closed_count = 0
        monkeypatch.setattr(memory.sqlite3, "connect", tracking_connect)
        _store("iso4")
        memory._L0.clear()
        assert get_fact("iso4")["claim"] == "original claim"
        assert opened and _TrackingConnection.closed_count == len(opened)
