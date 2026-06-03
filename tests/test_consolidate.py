"""Tests for core/consolidate.py — the SleepCycle confidence-decay pass."""
from datetime import datetime, timedelta, timezone

from core.memory import store_fact, transition_esm, get_fact, update_fact
from core.l3_graph import get_l3_graph
from core.consolidate import consolidate


def _canon(fact_id, confidence, significance, age_days):
    """A Validated L3 fact whose decay clock sits `age_days` in the past."""
    store_fact({"fact_id": fact_id, "claim": "c", "source": "s",
                "confidence": confidence, "significance": significance})
    transition_esm(fact_id, "Validated")
    old = (datetime.now(timezone.utc) - timedelta(days=age_days)).isoformat()
    update_fact(fact_id, metadata={"last_consolidated": old})
    get_l3_graph().merge_fact(get_fact(fact_id))


def test_confidence_decays_with_age():
    _canon("d1", confidence=0.8, significance=0.0, age_days=30)  # one half-life
    consolidate()
    assert get_fact("d1")["confidence"] < 0.8


def test_significant_facts_decay_slower():
    _canon("low", confidence=0.8, significance=0.0, age_days=30)
    _canon("high", confidence=0.8, significance=1.0, age_days=30)
    consolidate()
    assert get_fact("high")["confidence"] > get_fact("low")["confidence"]


def test_decay_respects_floor():
    _canon("ancient", confidence=0.9, significance=0.0, age_days=4000)
    consolidate()
    assert get_fact("ancient")["confidence"] == 0.02   # floored, not zero/negative


def test_consolidate_is_idempotent_at_same_instant():
    _canon("d2", confidence=0.8, significance=0.0, age_days=30)
    now = datetime.now(timezone.utc)
    consolidate(now=now)
    c1 = get_fact("d2")["confidence"]
    second = consolidate(now=now)            # same instant → no further decay
    assert second["decayed"] == 0
    assert get_fact("d2")["confidence"] == c1


def test_consolidate_skips_non_validated():
    store_fact({"fact_id": "obs", "claim": "c", "source": "s", "confidence": 0.8})
    get_l3_graph().merge_fact(get_fact("obs"))   # stays Observed
    result = consolidate()
    assert result["decayed"] == 0
    assert get_fact("obs")["confidence"] == 0.8


def test_consolidate_starts_clock_for_baseline_less_node():
    """A canonical node with no created_at/last_consolidated (e.g. a backend
    that doesn't persist created_at as a column) must not be skipped forever:
    the first cycle starts its decay clock via metadata, the next one decays it.
    Backend-agnostic — metadata is persisted by every backend."""
    store_fact({"fact_id": "nobase", "claim": "c", "source": "s",
                "confidence": 0.8, "significance": 0.0})
    transition_esm("nobase", "Validated")
    g = get_l3_graph()
    # Merge a bare node: simulate a backend that dropped created_at + metadata.
    g.merge_fact({"fact_id": "nobase", "claim": "c", "source": "s",
                  "confidence": 0.8, "significance": 0.0,
                  "epistemic_state": "Validated"})
    assert "created_at" not in g.get_fact("nobase")

    now = datetime.now(timezone.utc)
    first = consolidate(now=now)
    assert first["decayed"] == 0                                  # clock just started …
    assert g.get_fact("nobase")["metadata"]["last_consolidated"]  # … baseline now set

    second = consolidate(now=now + timedelta(days=30))
    assert second["decayed"] >= 1                                 # now it decays
    assert g.get_fact("nobase")["confidence"] < 0.8
