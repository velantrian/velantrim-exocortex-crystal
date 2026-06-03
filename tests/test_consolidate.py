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
