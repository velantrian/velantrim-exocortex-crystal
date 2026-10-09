"""Regression coverage for claim-version-bound Guardian/TruthGate promotion."""
from __future__ import annotations

import os
import subprocess
import sys
import threading

import pytest

from core import evidence, memory, provenance
from core.ingest import ingest
from core.l3_graph import get_l3_graph


def _start_ingest_paused_after_truth_gate(monkeypatch, fact_id: str, claim: str):
    """Run a real ingest and pause only after the real TruthGate passes."""
    import core.ingest as ingest_module

    gate_passed = threading.Event()
    resume = threading.Event()
    outcome = {}
    real_truth_gate = ingest_module.truth_gate

    def truth_gate_with_barrier(facts_pack):
        result = real_truth_gate(facts_pack)
        if facts_pack["facts"][0]["claim"] == claim and result[0]:
            gate_passed.set()
            if not resume.wait(timeout=15):
                raise TimeoutError("F-001 deterministic barrier timed out")
        return result

    monkeypatch.setattr(ingest_module, "truth_gate", truth_gate_with_barrier)

    def writer():
        try:
            outcome["result"] = ingest_module.ingest(
                claim,
                fact_id=fact_id,
                source="writer-A",
                confidence=0.9,
                source_status="EXTERNAL",
            )
        except BaseException as exc:  # surfaced in the main test thread
            outcome["error"] = exc

    thread = threading.Thread(target=writer, name="f001-writer-A", daemon=True)
    thread.start()
    if not gate_passed.wait(timeout=15):
        resume.set()
        thread.join(timeout=15)
        pytest.fail("writer A did not reach the post-TruthGate barrier")
    return thread, resume, outcome


def _finish_writer(thread, resume, outcome):
    resume.set()
    thread.join(timeout=15)
    assert not thread.is_alive(), "writer A did not finish after barrier release"
    assert "error" not in outcome, repr(outcome.get("error"))
    return outcome["result"]


def test_f001_competing_claim_cannot_be_promoted_by_stale_gate_decision(monkeypatch):
    """RED on PR HEAD: A passes both gates, B replaces it and fails TruthGate."""
    fact_id = "synthetic-f001-claim-revision-race"
    claim_a = "Synthetic claim A passed by writer A"
    claim_b = "Synthetic claim B rejected by TruthGate"
    gate_decisions = []

    import core.ingest as ingest_module
    real_guardian = ingest_module.guardian
    real_truth_gate = ingest_module.truth_gate

    def record_guardian(facts_pack, trace):
        result = real_guardian(facts_pack, trace)
        gate_decisions.append(("Guardian", facts_pack["facts"][0]["claim"], result[0]))
        return result

    def record_truth_gate(facts_pack):
        result = real_truth_gate(facts_pack)
        gate_decisions.append(("TruthGate", facts_pack["facts"][0]["claim"], result[0]))
        if facts_pack["facts"][0]["claim"] == claim_a and result[0]:
            gate_passed.set()
            if not resume.wait(timeout=15):
                raise TimeoutError("F-001 deterministic barrier timed out")
        return result

    gate_passed = threading.Event()
    resume = threading.Event()
    monkeypatch.setattr(ingest_module, "guardian", record_guardian)
    monkeypatch.setattr(ingest_module, "truth_gate", record_truth_gate)
    outcome = {}

    def writer_a():
        try:
            outcome["A"] = ingest(
                claim_a, fact_id=fact_id, source="writer-A", confidence=0.9,
                source_status="EXTERNAL",
            )
        except BaseException as exc:
            outcome["error"] = exc

    thread = threading.Thread(target=writer_a, name="f001-writer-A", daemon=True)
    thread.start()
    if not gate_passed.wait(timeout=15):
        resume.set()
        thread.join(timeout=15)
        pytest.fail("writer A did not pass Guardian and TruthGate")

    try:
        # A remains outside any SQLite write transaction/lock while B ingests.
        result_b = ingest(
            claim_b, fact_id=fact_id, source="writer-B", confidence=0.9,
            source_status="LLM_OUTPUT",
        )
        persisted_before_resume = memory.get_fact(fact_id)
        assert result_b["accepted"] is False
        assert persisted_before_resume["claim"] == claim_b
        assert persisted_before_resume["epistemic_state"] == "Observed"
    finally:
        resume.set()
        thread.join(timeout=15)

    assert not thread.is_alive()
    assert "error" not in outcome, repr(outcome.get("error"))
    result_a = outcome["A"]
    after = memory.get_fact(fact_id)
    l3_fact = get_l3_graph().get_fact(fact_id)

    assert ("Guardian", claim_a, True) in gate_decisions
    assert ("TruthGate", claim_a, True) in gate_decisions
    assert ("Guardian", claim_b, True) in gate_decisions
    assert ("TruthGate", claim_b, False) in gate_decisions
    assert result_a["accepted"] is False
    assert "receipt" not in result_a
    with pytest.raises(ValueError, match="no answer"):
        provenance.build_receipt(result_a)
    assert after["claim"] == claim_b
    assert after["epistemic_state"] == "Observed"
    assert l3_fact is None
    assert evidence.evidence_for(fact_id) == []


def test_f001_revision_only_change_blocks_promotion_without_l3(monkeypatch):
    fact_id = "synthetic-f001-revision-only-race"
    claim = "Synthetic same claim with a new persisted revision"
    thread, resume, outcome = _start_ingest_paused_after_truth_gate(
        monkeypatch, fact_id, claim
    )
    try:
        before = memory.get_fact(fact_id)
        assert memory.update_fact(
            fact_id, metadata={"concurrent_revision_marker": "changed"}
        ) is True
        updated = memory.get_fact(fact_id)
        assert updated["claim"] == claim
        assert updated["revision"] == before["revision"] + 1
    finally:
        result = _finish_writer(thread, resume, outcome)

    assert result["accepted"] is False
    current = memory.get_fact(fact_id)
    assert current["claim"] == claim
    assert current["epistemic_state"] == "Observed"
    assert current["metadata"]["concurrent_revision_marker"] == "changed"
    assert get_l3_graph().get_fact(fact_id) is None
    assert evidence.evidence_for(fact_id) == []


def test_f001_terminal_transition_during_gates_is_not_resurrected(monkeypatch):
    fact_id = "synthetic-f001-terminal-race"
    claim = "Synthetic claim made terminal while gates run"
    thread, resume, outcome = _start_ingest_paused_after_truth_gate(
        monkeypatch, fact_id, claim
    )
    try:
        before = memory.get_fact(fact_id)
        assert memory.transition_esm(fact_id, "Collapsed") is True
    finally:
        result = _finish_writer(thread, resume, outcome)

    assert result["accepted"] is False
    current = memory.get_fact(fact_id)
    assert current["claim"] == before["claim"]
    assert current["source"] == before["source"]
    assert current["revision"] == before["revision"] + 1
    assert current["epistemic_state"] == "Collapsed"
    assert get_l3_graph().get_fact(fact_id) is None
    assert evidence.evidence_for(fact_id) == []


def test_f001_deleted_and_replaced_row_fails_closed(monkeypatch):
    fact_id = "synthetic-f001-delete-replace-race"
    claim_a = "Synthetic original claim A"
    claim_b = "Synthetic replacement claim B"
    thread, resume, outcome = _start_ingest_paused_after_truth_gate(
        monkeypatch, fact_id, claim_a
    )
    try:
        assert memory.delete_fact_l1(fact_id) is True
        memory.store_fact({
            "fact_id": fact_id,
            "claim": claim_b,
            "source": "replacement-writer",
            "confidence": 0.4,
            "epistemic_state": "Observed",
            "source_status": "LLM_OUTPUT",
            "metadata": {"replacement": True},
        })
    finally:
        result = _finish_writer(thread, resume, outcome)

    assert result["accepted"] is False
    current = memory.get_fact(fact_id)
    assert current["claim"] == claim_b
    assert current["epistemic_state"] == "Observed"
    assert current["metadata"] == {"replacement": True}
    assert get_l3_graph().get_fact(fact_id) is None
    assert evidence.evidence_for(fact_id) == []


def test_f001_cross_process_writer_revision_is_detected(monkeypatch):
    """A separate Python process changes SQLite after A's real gates pass."""
    fact_id = "synthetic-f001-cross-process-race"
    claim_a = "Synthetic cross-process claim A"
    claim_b = "Synthetic cross-process replacement B"
    thread, resume, outcome = _start_ingest_paused_after_truth_gate(
        monkeypatch, fact_id, claim_a
    )
    script = r"""
from core import memory
memory.store_fact({
    'fact_id': 'synthetic-f001-cross-process-race',
    'claim': 'Synthetic cross-process replacement B',
    'source': 'writer-B-process',
    'confidence': 0.8,
    'epistemic_state': 'Observed',
    'source_status': 'LLM_OUTPUT',
    'metadata': {'writer': 'separate-process'},
}, expected_state='Observed', reject_terminal=True)
print('writer-B-committed')
"""
    try:
        env = os.environ.copy()
        env.update({
            "VELANTRIM_DB": memory.SQLITE_PATH,
            "VELANTRIM_L3_BACKEND": "mock",
            "VELANTRIM_EMBEDDER": "hashing",
            "VELANTRIM_QUEUE_BACKEND": "sqlite",
            "VELANTRIM_DEMO_SEED": "0",
        })
        completed = subprocess.run(
            [sys.executable, "-c", script],
            cwd=os.getcwd(), env=env, check=True, capture_output=True,
            text=True, timeout=30,
        )
        assert "writer-B-committed" in completed.stdout
    finally:
        result = _finish_writer(thread, resume, outcome)

    assert result["accepted"] is False
    current = memory.get_fact(fact_id)
    assert current["claim"] == claim_b
    assert current["epistemic_state"] == "Observed"
    assert current["metadata"] == {"writer": "separate-process"}
    assert get_l3_graph().get_fact(fact_id) is None
    assert evidence.evidence_for(fact_id) == []


def test_f001_promotion_transaction_rollback_never_returns_acceptance():
    """A failed SQL promotion rolls back L1 and produces no L3/evidence result."""
    fact_id = "synthetic-f001-promotion-rollback"
    claim = "Synthetic claim whose guarded promotion is aborted by SQLite"
    with memory._db() as conn:
        conn.execute(f"""
            CREATE TRIGGER abort_f001_promotion
            BEFORE UPDATE OF epistemic_state ON facts
            WHEN OLD.fact_id = '{fact_id}'
            BEGIN
                SELECT RAISE(ABORT, 'synthetic promotion rollback');
            END
        """)

    with pytest.raises(Exception, match="synthetic promotion rollback"):
        ingest(
            claim, fact_id=fact_id, source="rollback-source", confidence=0.9,
            source_status="EXTERNAL",
        )

    current = memory.get_fact(fact_id)
    assert current["claim"] == claim
    assert current["epistemic_state"] == "Observed"
    assert current["revision"] == 0
    assert get_l3_graph().get_fact(fact_id) is None
    assert evidence.evidence_for(fact_id) == []


def test_f001_second_writer_order_keeps_the_last_checked_version_admissible():
    """If B commits first, A overwrites it before A's own gates and may pass."""
    fact_id = "synthetic-f001-reverse-order"
    claim_b = "Synthetic rejected draft from writer B"
    claim_a = "Synthetic replacement checked by writer A"

    result_b = ingest(
        claim_b, fact_id=fact_id, source="writer-B", confidence=0.9,
        source_status="LLM_OUTPUT",
    )
    assert result_b["accepted"] is False
    assert memory.get_fact(fact_id)["epistemic_state"] == "Observed"

    result_a = ingest(
        claim_a, fact_id=fact_id, source="writer-A", confidence=0.9,
        source_status="EXTERNAL",
    )

    assert result_a["accepted"] is True
    current = memory.get_fact(fact_id)
    l3_fact = get_l3_graph().get_fact(fact_id)
    assert current["claim"] == claim_a
    assert current["epistemic_state"] == "Validated"
    assert l3_fact["claim"] == claim_a
    assert l3_fact["epistemic_state"] == "Validated"
    assert evidence.evidence_for(fact_id) == []


def test_guarded_promotion_rejects_malformed_and_protected_snapshots():
    snapshot = {
        "fact_id": "synthetic-f001-helper-validation",
        "claim": "Synthetic helper validation claim",
        "revision": 0,
        "epistemic_state": "Observed",
        "created_at": "2026-01-01T00:00:00+00:00",
        "source": "test",
        "confidence": 0.9,
        "claim_type": "WORLD_FACT",
        "source_status": "EXTERNAL",
    }

    with pytest.raises(ValueError, match="incomplete persisted snapshot"):
        memory.transition_esm_if_unchanged({"fact_id": snapshot["fact_id"]}, "Validated")
    with pytest.raises(ValueError, match="fact_id is required"):
        memory.transition_esm_if_unchanged({**snapshot, "fact_id": ""}, "Validated")
    with pytest.raises(ValueError, match="invalid state"):
        memory.transition_esm_if_unchanged(snapshot, "not-an-esm-state")
    with pytest.raises(memory.ImmutableStateError, match="protected by Ring Zero"):
        memory.transition_esm_if_unchanged(
            {**snapshot, "fact_id": "VALUES_CORE"}, "Validated"
        )


def test_guarded_promotion_returns_none_when_row_is_missing():
    snapshot = {
        "fact_id": "synthetic-f001-helper-missing-row",
        "claim": "Synthetic missing row",
        "revision": 0,
        "epistemic_state": "Observed",
        "created_at": "2026-01-01T00:00:00+00:00",
        "source": "test",
        "confidence": 0.9,
        "claim_type": "WORLD_FACT",
        "source_status": "EXTERNAL",
    }
    assert memory.transition_esm_if_unchanged(snapshot, "Validated") is None


def test_guarded_promotion_refuses_disallowed_esm_transition():
    fact_id = "synthetic-f001-helper-disallowed-transition"
    snapshot = memory.store_fact({
        "fact_id": fact_id,
        "claim": "Synthetic terminal state",
        "source": "test",
        "confidence": 0.9,
        "epistemic_state": "Collapsed",
        "source_status": "EXTERNAL",
    }, return_persisted=True)
    assert snapshot is not None

    with pytest.raises(ValueError, match="transition 'Collapsed'.*not allowed"):
        memory.transition_esm_if_unchanged(snapshot, "Validated")

    current = memory.get_fact(fact_id)
    assert current["epistemic_state"] == "Collapsed"
    assert current["revision"] == snapshot["revision"]


def test_guarded_promotion_returns_none_when_sqlite_update_is_ignored():
    fact_id = "synthetic-f001-helper-ignored-update"
    snapshot = memory.store_fact({
        "fact_id": fact_id,
        "claim": "Synthetic ignored update",
        "source": "test",
        "confidence": 0.9,
        "epistemic_state": "Observed",
        "source_status": "EXTERNAL",
    }, return_persisted=True)
    assert snapshot is not None
    with memory._db() as conn:
        conn.execute(f"""
            CREATE TRIGGER ignore_f001_promotion
            BEFORE UPDATE OF epistemic_state ON facts
            WHEN OLD.fact_id = '{fact_id}'
            BEGIN
                SELECT RAISE(IGNORE);
            END
        """)

    assert memory.transition_esm_if_unchanged(snapshot, "Validated") is None
    current = memory.get_fact(fact_id)
    assert current["epistemic_state"] == "Observed"
    assert current["revision"] == snapshot["revision"]
