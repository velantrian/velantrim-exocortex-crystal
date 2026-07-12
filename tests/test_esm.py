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


# ─── Serialized ESM transitions ──────────────────────────────────────────────
# transition_esm reads and validates the persisted state under the SQLite write
# transaction; a stale L0 record must never drive transition policy.

def test_transition_esm_happy_path_updates_db_and_l0():
    """Normal transition still returns True and updates both DB and L0."""
    from core.memory import store_fact, transition_esm, _db, _l0_get
    store_fact({"fact_id": "cas_ok", "claim": "x", "source": "s", "confidence": 0.5})

    assert transition_esm("cas_ok", "Validated") is True

    assert _l0_get("cas_ok")["epistemic_state"] == "Validated"
    with _db() as conn:
        row = conn.execute(
            "SELECT epistemic_state FROM facts WHERE fact_id = ?", ("cas_ok",)
        ).fetchone()
    assert row["epistemic_state"] == "Validated"


def test_transition_esm_uses_persisted_state_when_l0_is_stale():
    """Policy is evaluated against SQLite, not a stale cached state."""
    from core.memory import store_fact, transition_esm, get_fact, _db
    store_fact({"fact_id": "cas_miss", "claim": "x", "source": "s", "confidence": 0.5})

    # Competing/external writer mutates the persisted state directly; the L0 cache
    # stays stale at "Observed".
    with _db() as conn:
        conn.execute(
            "UPDATE facts SET epistemic_state = ? WHERE fact_id = ?",
            ("Supported", "cas_miss"),
        )

    # Supported → Validated is legal. The transition must use this persisted
    # state even though L0 still says Observed.
    assert transition_esm("cas_miss", "Validated") is True

    # DB and L0 converge on the same just-committed row.
    with _db() as conn:
        row = conn.execute(
            "SELECT epistemic_state FROM facts WHERE fact_id = ?", ("cas_miss",)
        ).fetchone()
    assert row["epistemic_state"] == "Validated"
    assert get_fact("cas_miss")["epistemic_state"] == "Validated"


# ─── store_fact() ESM preservation on upsert ──────────────────────────────────
# Regression tests for the fix that removes epistemic_state from the ON CONFLICT
# clause: store_fact must not overwrite an existing fact's state on upsert.

def test_store_fact_preserves_collapsed_on_conflict():
    """Collapsed must stay Collapsed when store_fact upserts with epistemic_state=Validated."""
    from core.memory import store_fact, _db

    store_fact({"fact_id": "sf_collapse", "claim": "x", "source": "s",
                "confidence": 0.5, "epistemic_state": "Collapsed"})

    store_fact({"fact_id": "sf_collapse", "claim": "x", "source": "s",
                "confidence": 0.8, "epistemic_state": "Validated"})

    with _db() as conn:
        row = conn.execute(
            "SELECT epistemic_state FROM facts WHERE fact_id = ?", ("sf_collapse",)
        ).fetchone()
    assert row["epistemic_state"] == "Collapsed"


def test_store_fact_preserves_validated_on_conflict():
    """Validated must stay Validated when store_fact upserts with epistemic_state=Observed."""
    from core.memory import store_fact, _db

    store_fact({"fact_id": "sf_valid", "claim": "a", "source": "s",
                "confidence": 1.0, "epistemic_state": "Validated"})

    store_fact({"fact_id": "sf_valid", "claim": "a", "source": "s",
                "confidence": 0.3, "epistemic_state": "Observed"})

    with _db() as conn:
        row = conn.execute(
            "SELECT epistemic_state FROM facts WHERE fact_id = ?", ("sf_valid",)
        ).fetchone()
    assert row["epistemic_state"] == "Validated"


def test_store_fact_new_fact_accepts_initial_state():
    """New facts must still receive the requested initial epistemic_state (insert path unaffected)."""
    from core.memory import store_fact, _db

    store_fact({"fact_id": "sf_new_hypo", "claim": "hypothesis", "source": "s",
                "confidence": 0.6, "epistemic_state": "Hypothesized"})

    with _db() as conn:
        row = conn.execute(
            "SELECT epistemic_state FROM facts WHERE fact_id = ?", ("sf_new_hypo",)
        ).fetchone()
    assert row["epistemic_state"] == "Hypothesized"


def test_store_fact_l0_not_poisoned_on_conflict():
    """After a conflict-update, L0 must hold the persisted state, not the incoming one.
    Non-state fields (confidence) must still be updated normally.
    """
    from core.memory import store_fact, _l0_get, _L0

    store_fact({"fact_id": "sf_l0_poison", "claim": "v1", "source": "s",
                "confidence": 0.5, "epistemic_state": "Collapsed"})

    # Evict from L0 so the re-read path inside the _db() block is exercised.
    _L0.pop("sf_l0_poison", None)

    store_fact({"fact_id": "sf_l0_poison", "claim": "v1", "source": "s",
                "confidence": 0.9, "epistemic_state": "Validated"})

    cached = _l0_get("sf_l0_poison")
    assert cached is not None
    assert cached["epistemic_state"] == "Collapsed"   # persisted state preserved
    assert cached["confidence"] == 0.9                # non-state field updated normally


# ─── Exhaustive transition-matrix coverage (mutation-killing pins) ─────────────
# Two complementary layers:
#   1. The matrix CONTENT is pinned against an explicit copy of the declared
#      policy, so any edit to ESM_TRANSITIONS fails loudly here (a deliberate
#      duplicate: the point is that policy changes cannot land silently).
#   2. transition_esm() BEHAVIOUR is checked for every one of the 8×8 pairs
#      against the canonical matrix, so the validator can never drift from it.

_ESM_STATES = ("Observed", "Hypothesized", "Supported", "Validated",
               "Contradicted", "Deprecated", "Collapsed", "ImmutableCore")

_PINNED_TRANSITIONS = {
    "Observed":      {"Hypothesized", "Supported", "Validated", "Collapsed"},
    "Hypothesized":  {"Supported", "Validated", "Collapsed"},
    "Supported":     {"Validated", "Collapsed"},
    "Validated":     {"Contradicted", "ImmutableCore", "Collapsed"},
    "Contradicted":  {"Deprecated", "Collapsed"},
    "Deprecated":    {"Collapsed"},
    "Collapsed":     set(),
    "ImmutableCore": set(),
}


def test_transition_matrix_content_is_pinned():
    from core.memory import ESM_TRANSITIONS
    assert ESM_TRANSITIONS == _PINNED_TRANSITIONS


@pytest.mark.parametrize("to_state", _ESM_STATES)
@pytest.mark.parametrize("from_state", _ESM_STATES)
def test_transition_esm_matches_matrix_exhaustively(from_state, to_state):
    """For every from/to pair (64 cases, self-transitions included):
    a pair in ESM_TRANSITIONS must succeed and persist the new state; any
    other pair must raise ValueError and leave the state untouched."""
    from core.memory import ESM_TRANSITIONS, store_fact, transition_esm, get_fact

    fact_id = f"esm_{from_state}_{to_state}"
    store_fact({"fact_id": fact_id, "claim": "x", "source": "s",
                "confidence": 0.5, "epistemic_state": from_state})

    if to_state in ESM_TRANSITIONS[from_state]:
        assert transition_esm(fact_id, to_state) is True
        assert get_fact(fact_id)["epistemic_state"] == to_state
    else:
        with pytest.raises(ValueError, match="is not allowed"):
            transition_esm(fact_id, to_state)
        assert get_fact(fact_id)["epistemic_state"] == from_state
