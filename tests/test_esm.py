"""
Tests for core/memory.py ESM (Epistemic State Machine).

Covers only the MVP-level behavior actually implemented in code.
Full RFC0001 invariants (I1–I95) are a Sprint 3+ task.
"""
import pytest

# DB isolation is provided by the autouse `isolated_db` fixture in conftest.py.


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
    with pytest.raises(ValueError, match="is not allowed"):
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
    with pytest.raises(ValueError, match="invalid ESM"):
        store_fact({"fact_id": "bad", "claim": "x", "source": "s",
                    "epistemic_state": "NotAState"})


# ─── B1: L0 LRU cache ─────────────────────────────────────────────────────────

def test_lru_cap_respected():
    """B1: L0 must never exceed L0_CAP entries."""
    from core.memory import store_fact, _L0, L0_CAP
    for i in range(L0_CAP + 3):
        store_fact({"fact_id": f"lru_{i}", "claim": f"c{i}", "source": "t",
                    "confidence": 0.5})
    assert len(_L0) <= L0_CAP


def test_lru_evicts_oldest():
    """B1: first-inserted entry is evicted when capacity is exceeded."""
    from core.memory import store_fact, _L0, L0_CAP
    for i in range(L0_CAP):
        store_fact({"fact_id": f"ev_{i}", "claim": f"c{i}", "source": "t",
                    "confidence": 0.5})
    assert "ev_0" in _L0  # still present before overflow

    store_fact({"fact_id": "ev_overflow", "claim": "x", "source": "t",
                "confidence": 0.5})
    assert "ev_0" not in _L0  # evicted (oldest)
    assert "ev_overflow" in _L0


def test_lru_read_refreshes_recency():
    """B1: reading a fact makes it most-recently-used; a newer insert evicts another."""
    from core.memory import store_fact, get_fact, _L0, L0_CAP
    for i in range(L0_CAP):
        store_fact({"fact_id": f"rec_{i}", "claim": f"c{i}", "source": "t",
                    "confidence": 0.5})

    # Read rec_0 — moves it to MRU position
    get_fact("rec_0")

    # Add one more — should evict rec_1 (now oldest), not rec_0
    store_fact({"fact_id": "rec_new", "claim": "x", "source": "t",
                "confidence": 0.5})

    assert "rec_0" in _L0   # refreshed, not evicted
    assert "rec_1" not in _L0  # was oldest after rec_0 was refreshed
