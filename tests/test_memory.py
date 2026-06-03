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


def test_update_fact_changes_columns_without_touching_esm():
    store_fact({"fact_id": "u1", "claim": "c", "source": "s", "confidence": 0.5})
    transition_esm("u1", "Validated")
    from core.memory import update_fact
    assert update_fact("u1", confidence=0.9, metadata={"observations": 3}) is True
    f = get_fact("u1")
    assert f["confidence"] == 0.9
    assert f["metadata"] == {"observations": 3}
    assert f["epistemic_state"] == "Validated"   # ESM untouched


def test_update_fact_missing_or_no_fields_returns_false():
    from core.memory import update_fact
    assert update_fact("nope", confidence=0.9) is False          # missing fact
    store_fact({"fact_id": "u2", "claim": "c", "source": "s"})
    assert update_fact("u2", epistemic_state="Validated") is False  # not updatable


def test_db_uses_wal_journal_mode():
    """Evidence/audit store runs in WAL so writers don't block readers."""
    from core import memory
    with memory._db() as conn:
        mode = conn.execute("PRAGMA journal_mode").fetchone()[0]
    assert mode.lower() == "wal"


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


# ─── claim_type / source_status / significance (ось модальности) ──────────────

def test_new_fields_default_when_omitted():
    """store_fact must apply sane defaults for the orthogonal modality axis."""
    _L0.clear()
    store_fact({"fact_id": "d1", "claim": "c", "source": "s", "confidence": 0.5})
    _L0.clear()  # force the L1 read path
    f = get_fact("d1")
    assert f["claim_type"] == "WORLD_FACT"
    assert f["source_status"] == "UNKNOWN"
    assert f["significance"] == pytest.approx(0.5)


def test_new_fields_round_trip_through_l1():
    _L0.clear()
    store_fact({"fact_id": "e1", "claim": "felt anxious", "source": "user",
                "confidence": 0.9, "claim_type": "EMOTION",
                "source_status": "USER_REPORTED", "significance": 0.7})
    _L0.clear()
    f = get_fact("e1")
    assert f["claim_type"] == "EMOTION"
    assert f["source_status"] == "USER_REPORTED"
    assert f["significance"] == pytest.approx(0.7)


def test_store_fact_rejects_unknown_claim_type():
    with pytest.raises(ValueError, match="claim_type"):
        store_fact({"fact_id": "bad", "claim": "c", "source": "s",
                    "claim_type": "TELEPATHY"})


def test_store_fact_rejects_unknown_source_status():
    with pytest.raises(ValueError, match="source_status"):
        store_fact({"fact_id": "bad2", "claim": "c", "source": "s",
                    "source_status": "OUIJA_BOARD"})


def test_migration_adds_columns_to_legacy_table(monkeypatch, tmp_path):
    """A pre-existing DB built on the old schema must gain the new columns."""
    import sqlite3
    from core import memory

    legacy = str(tmp_path / "legacy.db")
    conn = sqlite3.connect(legacy)
    conn.execute("""
        CREATE TABLE facts (
            fact_id TEXT PRIMARY KEY, claim TEXT NOT NULL, source TEXT NOT NULL,
            confidence REAL DEFAULT 0.5, epistemic_state TEXT DEFAULT 'Observed',
            created_at TEXT NOT NULL, updated_at TEXT NOT NULL,
            metadata TEXT DEFAULT '{}'
        )
    """)
    conn.commit()
    conn.close()

    memory._L0.clear()
    monkeypatch.setattr(memory, "SQLITE_PATH", legacy)
    # store_fact opens _db(), which must ALTER the legacy table before INSERT.
    store_fact({"fact_id": "leg1", "claim": "c", "source": "s",
                "claim_type": "OPINION", "significance": 0.3})
    memory._L0.clear()
    f = get_fact("leg1")
    assert f["claim_type"] == "OPINION"
    assert f["significance"] == pytest.approx(0.3)
