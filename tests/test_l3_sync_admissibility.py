"""Tests for L3 secondary sync admissibility (Ring Zero hardening)."""
from core.memory import store_fact, transition_esm, get_fact, l3_secondary_sync_admissible
from core.l3_graph import get_l3_graph
from core import reconcile, compliance


def test_l3_secondary_sync_rejects_none_and_collapsed():
    assert l3_secondary_sync_admissible(None) is False
    store_fact({"fact_id": "col1", "claim": "c", "source": "s",
                "epistemic_state": "Collapsed", "confidence": 0.5})
    assert l3_secondary_sync_admissible(get_fact("col1")) is False


def test_l3_secondary_sync_blocks_pre_canonical_states():
    for state in ("Observed", "Hypothesized", "Supported"):
        fid = f"pre_{state.lower()}"
        store_fact({"fact_id": fid, "claim": "c", "source": "s",
                    "epistemic_state": state, "confidence": 0.8})
        assert l3_secondary_sync_admissible(get_fact(fid)) is False


def test_l3_secondary_sync_allows_validated():
    store_fact({"fact_id": "val1", "claim": "c", "source": "s",
                "confidence": 0.8})
    transition_esm("val1", "Validated")
    assert l3_secondary_sync_admissible(get_fact("val1")) is True


def test_reinforce_on_supported_does_not_merge_into_l3():
    store_fact({"fact_id": "sup_r", "claim": "supported claim", "source": "s",
                "confidence": 0.5, "epistemic_state": "Supported"})
    assert reconcile.reinforce("sup_r") is not None
    assert get_l3_graph().get_fact("sup_r") is None


def test_sync_l3_skips_contradicted_not_yet_in_l3():
    store_fact({"fact_id": "ghost_c", "claim": "c", "source": "s",
                "confidence": 0.9, "epistemic_state": "Contradicted"})
    reconcile._sync_l3("ghost_c")
    assert get_l3_graph().get_fact("ghost_c") is None


def test_sync_l3_updates_contradicted_already_in_l3():
    store_fact({"fact_id": "live_c", "claim": "c", "source": "s",
                "confidence": 0.9})
    transition_esm("live_c", "Validated")
    get_l3_graph().merge_fact(get_fact("live_c"))
    transition_esm("live_c", "Contradicted")
    reconcile._sync_l3("live_c")
    assert get_l3_graph().get_fact("live_c")["epistemic_state"] == "Contradicted"


def test_restrict_supported_fact_does_not_merge_into_l3():
    store_fact({"fact_id": "sup_f", "claim": "c", "source": "s",
                "epistemic_state": "Supported", "confidence": 0.8})
    compliance.restrict_processing("sup_f")
    assert get_l3_graph().get_fact("sup_f") is None
