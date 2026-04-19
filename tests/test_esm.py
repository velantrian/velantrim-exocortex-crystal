"""
Tests for core/memory.py ESM (Epistemic State Machine).

Covers only the MVP-level behavior actually implemented in code.
Full RFC0001 invariants (I1–I95) are a Sprint 3+ task.
"""
import os
import sys
import tempfile
import pytest

# Ensure core/ is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


@pytest.fixture(autouse=True)
def isolated_db(monkeypatch, tmp_path):
    """Each test gets its own SQLite file and fresh L0 cache."""
    from core import memory
    # Reset module-level state
    memory._L0.clear()
    memory._conn = None
    monkeypatch.setattr(memory, "SQLITE_PATH", str(tmp_path / "test.db"))
    yield
    if memory._conn is not None:
        memory._conn.close()
        memory._conn = None


def test_esm_has_eight_states():
    """Spec: 8 epistemic states."""
    from core.memory import ESM_STATES
    assert len(ESM_STATES) == 8
    assert {"Observed", "Hypothesized", "Supported", "Validated",
            "Contradicted", "Deprecated", "Collapsed", "ImmutableCore"} == ESM_STATES


def test_validated_can_reach_contradicted():
    """Bug 2.1 regression: Validated → Contradicted must be allowed."""
    from core.memory import ESM_TRANSITIONS
    assert "Contradicted" in ESM_TRANSITIONS["Validated"]


def test_terminal_states_have_no_exits():
    """Collapsed and ImmutableCore are terminal."""
    from core.memory import ESM_TRANSITIONS
    assert ESM_TRANSITIONS["Collapsed"] == set()
    assert ESM_TRANSITIONS["ImmutableCore"] == set()


def test_store_and_get_fact_roundtrip():
    from core.memory import store_fact, get_fact
    store_fact({"fact_id": "t1", "claim": "hello", "source": "test", "confidence": 0.9})
    f = get_fact("t1")
    assert f is not None
    assert f["claim"] == "hello"
    assert f["epistemic_state"] == "Observed"


def test_transition_esm_valid():
    from core.memory import store_fact, transition_esm, get_fact
    store_fact({"fact_id": "t2", "claim": "x", "source": "s", "confidence": 0.5})
    assert transition_esm("t2", "Validated") is True
    assert get_fact("t2")["epistemic_state"] == "Validated"


def test_transition_esm_invalid_transition_raises():
    from core.memory import store_fact, transition_esm
    store_fact({"fact_id": "t3", "claim": "x", "source": "s", "confidence": 0.5,
                "epistemic_state": "Collapsed"})
    with pytest.raises(ValueError, match="недопустим"):
        transition_esm("t3", "Validated")


def test_ring_zero_is_immutable():
    """I6 (RingZeroImmutable): VALUES_CORE and RING_ZERO cannot be transitioned."""
    from core.memory import store_fact, transition_esm, ImmutableStateError, IMMUTABLE_FACT_IDS
    assert "VALUES_CORE" in IMMUTABLE_FACT_IDS
    assert "RING_ZERO" in IMMUTABLE_FACT_IDS

    store_fact({"fact_id": "VALUES_CORE", "claim": "honesty", "source": "ring_zero",
                "confidence": 1.0, "epistemic_state": "Validated"})
    with pytest.raises(ImmutableStateError):
        transition_esm("VALUES_CORE", "Contradicted")


def test_store_fact_rejects_invalid_state():
    from core.memory import store_fact
    with pytest.raises(ValueError, match="недопустимое ESM"):
        store_fact({"fact_id": "bad", "claim": "x", "source": "s",
                    "epistemic_state": "NotAState"})
