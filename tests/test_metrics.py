"""Tests for core/metrics.py and pipeline/ingest instrumentation."""
from core import metrics
from core.pipeline import run
from core.ingest import ingest


def test_counter_incr_value_snapshot_reset():
    metrics.incr("x")
    metrics.incr("x", 2)
    assert metrics.value("x") == 3
    assert metrics.value("missing") == 0
    assert metrics.snapshot()["x"] == 3
    metrics.reset()
    assert metrics.snapshot() == {}


def test_query_counters_answered_and_blocked():
    run("quantum entanglement")          # answers
    run("zxqvbnmqwerty")                 # blocked (no retrieval)
    assert metrics.value("query.total") == 2
    assert metrics.value("query.answered") == 1
    assert metrics.value("query.blocked") == 1


def test_ingest_counters_accepted_duplicate_blocked():
    ingest("Water boils at 100 degrees")          # accepted
    ingest("Water boils at 100 degrees")          # exact repeat → duplicate
    ingest("Shaky claim", confidence=0.0)         # WORLD_FACT below gate → blocked
    assert metrics.value("ingest.total") == 3
    assert metrics.value("ingest.accepted") == 1
    assert metrics.value("ingest.duplicate") == 1
    assert metrics.value("ingest.blocked") == 1
