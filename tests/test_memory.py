"""Tests for core/memory.py paths not covered by test_esm.py.

Focus: L0→L1 fallback, get_all_facts, and the input-validation / not-found
branches of store_fact / transition_esm.
"""
import pytest

from core.memory import (
    store_fact,
    get_fact,
    transition_esm,
    get_all_facts,
    _L0,
    L0_CAP,
)


def test_store_fact_requires_fact_id():
    with pytest.raises(ValueError, match="fact_id"):
        store_fact({"claim": "no id", "source": "s"})


def test_get_fact_falls_back_to_l1_after_l0_eviction():
    """A fact pushed out of the L0 LRU must still be retrievable from L1."""
    store_fact({"fact_id": "deep", "claim": "persisted", "source": "disk",
                "confidence": 0.7})

    # Overflow L0 so "deep" is evicted from the in-memory cache.
    for i in range(L0_CAP + 2):
        store_fact({"fact_id": f"flood_{i}", "claim": "x", "source": "t",
                    "confidence": 0.5})
    assert "deep" not in _L0

    # get_fact must hit SQLite, rehydrate metadata, and re-promote into L0.
    f = get_fact("deep")
    assert f is not None
    assert f["claim"] == "persisted"
    assert f["metadata"] == {}          # JSON round-trips back to a dict
    assert "deep" in _L0                # promoted back into the cache


def test_get_fact_unknown_returns_none():
    assert get_fact("does-not-exist") is None


def test_store_fact_upsert_updates_existing_row():
    store_fact({"fact_id": "up1", "claim": "v1", "source": "s", "confidence": 0.5})
    store_fact({"fact_id": "up1", "claim": "v2", "source": "s", "confidence": 0.9})
    f = get_fact("up1")
    assert f["claim"] == "v2"
    assert f["confidence"] == pytest.approx(0.9)


def test_metadata_round_trips_through_l1():
    _L0.clear()  # force the L1 read path on get
    store_fact({"fact_id": "meta1", "claim": "c", "source": "s", "confidence": 0.5,
                "metadata": {"tags": ["a", "b"], "n": 3}})
    _L0.clear()
    f = get_fact("meta1")
    assert f["metadata"] == {"tags": ["a", "b"], "n": 3}


def test_transition_esm_rejects_unknown_state():
    store_fact({"fact_id": "tr1", "claim": "c", "source": "s", "confidence": 0.5})
    with pytest.raises(ValueError, match="недопустимое состояние"):
        transition_esm("tr1", "Imaginary")


def test_transition_esm_missing_fact_returns_false():
    assert transition_esm("ghost", "Validated") is False


def test_db_rolls_back_on_exception():
    """_db() must roll back (and re-raise) when the with-block raises."""
    from core import memory
    with pytest.raises(ValueError, match="boom"):
        with memory._db() as conn:
            conn.execute(
                "INSERT INTO facts (fact_id, claim, source, created_at, updated_at) "
                "VALUES ('rb', 'c', 's', 't', 't')"
            )
            raise ValueError("boom")
    # The insert must not have been committed.
    assert get_fact("rb") is None


def test_get_all_facts_unfiltered_and_filtered():
    store_fact({"fact_id": "a1", "claim": "c", "source": "s", "confidence": 0.5})
    store_fact({"fact_id": "a2", "claim": "c", "source": "s", "confidence": 0.5})
    transition_esm("a2", "Validated")

    all_facts = get_all_facts()
    ids = {f["fact_id"] for f in all_facts}
    assert {"a1", "a2"} <= ids
    # metadata is deserialized for every row
    assert all(isinstance(f["metadata"], dict) for f in all_facts)

    validated = get_all_facts(epistemic_state="Validated")
    assert {f["fact_id"] for f in validated} == {"a2"}
