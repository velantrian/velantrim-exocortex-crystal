"""Tests for core/erasure.py — GDPR Art. 17 physical right to erasure."""
import pytest

from core.erasure import erase_fact, erasure_log, is_erased
from core.memory import (
    store_fact, get_fact, enqueue_l3_write, pending_l3_writes, get_tombstone,
    ImmutableStateError,
)
from core.l3_graph import get_l3_graph


def _seed(fact_id="f1", claim="Water boils at 100C", state="Validated"):
    """Store a fact in L1 and merge it into the L3 canonical graph."""
    store_fact({"fact_id": fact_id, "claim": claim, "source": "physics",
                "epistemic_state": state})
    get_l3_graph().merge_fact(get_fact(fact_id))
    return fact_id


def test_erase_removes_from_l1_and_l3():
    _seed("f1")
    assert get_fact("f1") is not None
    assert get_l3_graph().get_fact("f1") is not None

    receipt = erase_fact("f1")

    assert receipt["erased_now"] is True
    assert receipt["l1_removed"] is True
    assert receipt["l3_removed"] is True
    assert get_fact("f1") is None
    assert get_l3_graph().get_fact("f1") is None


def test_erase_writes_content_free_tombstone():
    _seed("f1", claim="secret personal detail")
    erase_fact("f1", reason="gdpr_request", actor="dpo")

    tomb = get_tombstone("f1")
    assert tomb is not None
    assert tomb["fact_id"] == "f1"
    assert tomb["reason"] == "gdpr_request"
    assert tomb["actor"] == "dpo"
    assert tomb["content_hash"].startswith("sha256:")
    # The personal data itself must NOT be retained anywhere in the tombstone.
    assert "secret personal detail" not in str(tomb)
    assert is_erased("f1") is True


def test_erase_is_idempotent_and_tombstone_immutable():
    _seed("f1", claim="original")
    first = erase_fact("f1", reason="first")
    original_hash = first["content_hash"]
    original_at = first["erased_at"]

    # Re-erasing an already-gone fact: nothing left to remove, no duplicate event.
    second = erase_fact("f1", reason="second")
    assert second["erased_now"] is False
    # First erasure event is preserved (reason/hash/time unchanged).
    assert second["content_hash"] == original_hash
    assert second["erased_at"] == original_at
    assert get_tombstone("f1")["reason"] == "first"
    assert len([t for t in erasure_log() if t["fact_id"] == "f1"]) == 1


def test_ring_zero_cannot_be_erased():
    with pytest.raises(ImmutableStateError, match="Ring Zero"):
        erase_fact("VALUES_CORE")
    with pytest.raises(ImmutableStateError):
        erase_fact("RING_ZERO")
    assert is_erased("VALUES_CORE") is False


def test_erase_removes_incident_edges_both_directions():
    _seed("a", claim="claim a")
    _seed("b", claim="claim b")
    graph = get_l3_graph()
    graph.add_edge("a", "SUPERSEDED_BY", "b")   # a -> b (outgoing from a)
    graph.add_edge("b", "RELATED", "a")          # b -> a (incoming to a)

    erase_fact("a")

    # No dangling edges referencing the erased node, in either direction.
    assert graph.get_edges("a") == []
    assert graph.incoming_edges("a") == []
    assert graph.get_edges("b") == []            # b -> a edge removed
    assert graph.get_fact("b") is not None       # neighbour itself survives


def test_erase_clears_pending_outbox_entry():
    _seed("f1")
    enqueue_l3_write("f1")
    assert "f1" in pending_l3_writes()

    erase_fact("f1")
    assert "f1" not in pending_l3_writes()


def test_erase_unknown_fact_still_tombstones():
    # Erasing a fact that was never stored is a valid no-op that is still logged.
    receipt = erase_fact("ghost")
    assert receipt["erased_now"] is False
    assert receipt["content_hash"] is None
    assert is_erased("ghost") is True


def test_erasure_log_lists_tombstones_content_free():
    _seed("f1", claim="alpha")
    _seed("f2", claim="beta")
    erase_fact("f1")
    erase_fact("f2")

    log = erasure_log()
    ids = {t["fact_id"] for t in log}
    assert {"f1", "f2"} <= ids
    blob = str(log)
    assert "alpha" not in blob and "beta" not in blob


def test_cli_erase_and_erasures(capsys):
    import json
    from core.cli import main

    _seed("f1", claim="cli secret")
    assert main(["erase", "f1", "--reason", "cli_test"]) == 0
    out = json.loads(capsys.readouterr().out.strip())
    assert out["fact_id"] == "f1"
    assert out["erased_now"] is True
    assert get_fact("f1") is None

    assert main(["erasures"]) == 0
    log = json.loads(capsys.readouterr().out.strip())
    assert any(t["fact_id"] == "f1" and t["reason"] == "cli_test" for t in log)
    assert "cli secret" not in str(log)
