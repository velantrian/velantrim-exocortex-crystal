"""Tests for core/observe.py — L3 memory observability report."""
from core.memory import store_fact, transition_esm, get_fact
from core.l3_graph import get_l3_graph
from core.observe import memory_report, format_report


def _canon(fact_id, claim_type="WORLD_FACT", truth_status="VERIFIED",
           confidence=0.9, state="Validated"):
    store_fact({"fact_id": fact_id, "claim": fact_id, "source": "s",
                "confidence": confidence, "claim_type": claim_type})
    if state != "Observed":
        transition_esm(fact_id, "Validated")
    f = get_fact(fact_id)
    f["truth_status"] = truth_status
    f["epistemic_state"] = state
    get_l3_graph().merge_fact(f)


def test_empty_report():
    r = memory_report()
    assert r["total_facts"] == 0
    assert r["avg_confidence"] == 0.0
    assert r["edges"]["total"] == 0


def test_report_counts_states_types_and_edges():
    _canon("w1", claim_type="WORLD_FACT", truth_status="VERIFIED")
    _canon("e1", claim_type="EMOTION", truth_status="SUBJECTIVE")
    _canon("c1", state="Contradicted")
    _canon("d1", state="Deprecated")
    g = get_l3_graph()
    g.add_edge("w1", "CO_OCCURRED", "e1", {})
    g.add_edge("w1", "SUPERSEDED_BY", "d1", {})

    r = memory_report()
    assert r["total_facts"] == 4
    assert r["by_claim_type"]["WORLD_FACT"] == 3   # w1, c1, d1
    assert r["by_claim_type"]["EMOTION"] == 1
    assert r["by_epistemic_state"]["Contradicted"] == 1
    assert r["contradicted"] == ["c1"]
    assert r["deprecated"] == ["d1"]
    assert r["edges"]["total"] == 2
    assert r["edges"]["by_type"]["CO_OCCURRED"] == 1
    assert r["by_truth_status"]["SUBJECTIVE"] == 1


def test_report_flags_weak_confidence():
    _canon("strong", confidence=0.9)
    _canon("faded", confidence=0.05)   # decayed / weak
    r = memory_report(weak_confidence=0.2)
    assert r["weak_confidence"] == ["faded"]


def test_format_report_is_readable():
    _canon("w1")
    text = format_report(memory_report())
    assert "MEMORY REPORT" in text
    assert "facts: 1" in text
