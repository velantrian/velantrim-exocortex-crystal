"""Tests for core/trace.py (provenance layer)."""
import pytest

from core.trace import build_trace, promote_trace, format_trace


def test_build_trace_maps_fields_and_defaults():
    trace = build_trace([{"id": "f1", "source": "physics", "_score": 0.42}])
    assert len(trace) == 1
    el = trace[0]
    assert el["fact_id"] == "f1"
    assert el["source"] == "physics"
    assert el["origin"] == "retrieval"            # default
    assert el["epistemic_state"] == "Observed"    # default
    assert el["confidence"] == pytest.approx(0.42)
    assert "retrieved_at" in el


def test_build_trace_accepts_fact_id_alias_and_skips_idless():
    trace = build_trace([
        {"fact_id": "alias", "source": "s"},
        {"source": "no-id-here"},                 # skipped: no id/fact_id
    ])
    assert [el["fact_id"] for el in trace] == ["alias"]


def test_promote_trace_mutates_in_place():
    trace = build_trace([{"id": "f1", "source": "s"}])
    promote_trace(trace, "Validated")
    assert trace[0]["epistemic_state"] == "Validated"
    assert "promoted_at" in trace[0]


def test_promote_trace_rejects_invalid_state():
    trace = build_trace([{"id": "f1", "source": "s"}])
    with pytest.raises(ValueError, match="invalid ESM"):
        promote_trace(trace, "Bogus")


def test_format_trace_empty_and_populated():
    assert format_trace([]) == "TRACE: empty"
    out = format_trace(build_trace([{"id": "f1", "source": "physics", "_score": 0.5}]))
    assert out.startswith("TRACE:")
    assert "f1" in out
    assert "source=physics" in out
