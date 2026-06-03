"""Tests for core/reconcile.py — truth maintenance (reinforce / supersede / contradict)."""
import pytest

from core.memory import store_fact, transition_esm, get_fact
from core.l3_graph import get_l3_graph
from core.reconcile import (
    reinforce,
    supersede,
    contradict,
    REL_SUPERSEDED_BY,
    REL_CONTRADICTS,
)


def _validated(fact_id, confidence=0.5, claim="c"):
    store_fact({"fact_id": fact_id, "claim": claim, "source": "s",
                "confidence": confidence})
    transition_esm(fact_id, "Validated")
    get_l3_graph().merge_fact(get_fact(fact_id))


# ─── reinforce ────────────────────────────────────────────────────────────────

def test_reinforce_raises_confidence_with_diminishing_returns():
    _validated("r1", confidence=0.5)
    c1 = reinforce("r1")
    c2 = reinforce("r1")
    assert 0.5 < c1 < c2
    assert (c1 - 0.5) > (c2 - c1)            # each repeat adds less
    assert get_fact("r1")["metadata"]["observations"] == 3


def test_reinforce_disagreement_lowers_confidence():
    _validated("r2", confidence=0.8)
    assert reinforce("r2", agreement=False) < 0.8


def test_reinforce_missing_fact_returns_none():
    assert reinforce("ghost") is None


def test_reinforce_syncs_confidence_into_l3():
    _validated("r3", confidence=0.5)
    new_conf = reinforce("r3")
    assert get_l3_graph().get_fact("r3")["confidence"] == new_conf


# ─── supersede ──────────────────────────────────────────────────────────────

def test_supersede_deprecates_old_and_links_new():
    _validated("old", claim="earth is flat")
    new_id = supersede("old", {"fact_id": "new", "claim": "earth is round",
                               "source": "s", "confidence": 0.9})
    assert new_id == "new"
    assert get_fact("old")["epistemic_state"] == "Deprecated"
    assert get_fact("new")["epistemic_state"] == "Validated"
    neighbors = get_l3_graph().neighbors("old", rel_type=REL_SUPERSEDED_BY)
    assert "new" in {n["fact_id"] for n in neighbors}


def test_supersede_requires_new_fact_id():
    with pytest.raises(ValueError, match="fact_id"):
        supersede("old", {"claim": "no id"})


# ─── contradict ─────────────────────────────────────────────────────────────

def test_contradict_marks_validated_fact_and_adds_edge():
    _validated("c1")
    changed = contradict("c1", "source_fact")
    assert changed is True
    assert get_fact("c1")["epistemic_state"] == "Contradicted"
    g = get_l3_graph()
    assert any(e[0] == "c1" and e[1] == REL_CONTRADICTS and e[2] == "source_fact"
               for e in g._edges)


def test_contradict_non_validated_adds_edge_without_state_change():
    store_fact({"fact_id": "obs", "claim": "c", "source": "s"})  # stays Observed
    get_l3_graph().merge_fact(get_fact("obs"))
    changed = contradict("obs", "src")
    assert changed is False
    assert get_fact("obs")["epistemic_state"] == "Observed"
    assert any(e[0] == "obs" and e[1] == REL_CONTRADICTS for e in get_l3_graph()._edges)
