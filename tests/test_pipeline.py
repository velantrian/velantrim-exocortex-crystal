"""Smoke tests for the MVP pipeline."""
import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


@pytest.fixture(autouse=True)
def isolated_db(monkeypatch, tmp_path):
    from core import memory
    memory._L0.clear()
    memory._conn = None
    monkeypatch.setattr(memory, "SQLITE_PATH", str(tmp_path / "test.db"))
    yield
    if memory._conn is not None:
        memory._conn.close()
        memory._conn = None


def test_pipeline_happy_path():
    from core.pipeline import run
    result = run("quantum entanglement")
    assert result.get("answer") is not None
    assert "error" not in result or result.get("error") is None
    assert len(result["facts"]) > 0
    for f in result["facts"]:
        assert f["epistemic_state"] == "Validated"
        assert f["truth_status"] == "VERIFIED"


def test_pipeline_empty_retrieval_blocks():
    from core.pipeline import run
    result = run("zxqvbnmqwerty")   # matches nothing in DATABASE
    assert result.get("answer") is None
    assert "Retrieval" in result.get("error", "")


def test_trace_is_built_for_each_fact():
    from core.pipeline import run
    result = run("DNA")
    assert len(result["trace"]) == len(result["facts"])
    for el in result["trace"]:
        assert "fact_id" in el
        assert "epistemic_state" in el
        assert el["epistemic_state"] == "Validated"
