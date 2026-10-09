"""Focused synthetic regressions for CRYSTAL-REMEDIATION-PR-A-01."""
from copy import deepcopy
import json
import os
import subprocess
import sys
import threading

import pytest

from core import canonical_view, evidence, memory
from core.ingest import _fact_id, _legacy_fact_id, ingest
from core.l3_graph import get_l3_graph


TERMINAL_STATES = ("Collapsed", "Deprecated", "Contradicted")


def _seed_fact(fact_id, claim, state):
    memory.store_fact({
        "fact_id": fact_id,
        "claim": claim,
        "source": "baseline-source",
        "source_status": "EXTERNAL",
        "confidence": 0.91,
        "epistemic_state": state,
        "metadata": {
            "existing_marker": "preserve-me",
            "occurrences": 4,
            "fingerprint_sha256": "existing-fingerprint",
            "sources_seen": ["baseline-source"],
        },
    })
    get_l3_graph().merge_fact({
        **memory.get_fact(fact_id),
        "truth_status": "VERIFIED",
    })
    evidence.attach_evidence(
        fact_id, "synthetic://baseline/source", source_text="synthetic evidence"
    )


def _snapshot(fact_id):
    with memory._db() as conn:
        row = conn.execute(
            "SELECT * FROM facts WHERE fact_id = ?", (fact_id,)
        ).fetchone()
        index_exists = conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type = 'table' "
            "AND name = 'normalized_ingest_index'"
        ).fetchone() is not None
        index_rows = []
        if index_exists:
            index_rows = [dict(index_row) for index_row in conn.execute(
                "SELECT fact_id, normalized_id, fact_revision "
                "FROM normalized_ingest_index ORDER BY fact_id"
            ).fetchall()]
    graph = get_l3_graph()
    l3_fact = deepcopy(graph.get_fact(fact_id))
    return {
        "l1": dict(row),
        "normalized_ingest_index": {
            "exists": index_exists,
            "rows": index_rows,
        },
        "l3": l3_fact,
        "strict_canonical": bool(
            l3_fact is not None and canonical_view.is_strict_canonical(l3_fact)
        ),
        "l3_edges": deepcopy(graph.get_edges(fact_id)),
        "evidence": deepcopy(evidence.evidence_for(fact_id)),
    }


def _assert_error_code(exc_info, expected):
    assert getattr(exc_info.value, "code", None) == expected
    assert isinstance(exc_info.value, ValueError)
    assert str(exc_info.value)


def _assert_only_state_transition(before, after, expected_state):
    before_row = before["l1"]
    after_row = after["l1"]
    for field in before_row:
        if field not in {"epistemic_state", "revision", "updated_at"}:
            assert after_row[field] == before_row[field]
    assert after_row["epistemic_state"] == expected_state
    assert after_row["revision"] == before_row["revision"] + 1
    assert after["l3"] == before["l3"]
    assert after["strict_canonical"] == before["strict_canonical"]
    assert after["l3_edges"] == before["l3_edges"]
    assert after["evidence"] == before["evidence"]


@pytest.mark.parametrize("state", TERMINAL_STATES)
@pytest.mark.parametrize("auto_id", (False, True), ids=("explicit-id", "auto-id"))
def test_terminal_repeat_rejects_before_any_persisted_mutation(state, auto_id):
    """T01–T04, T12–T14: both ID routes refuse without touching stored state."""
    claim = f"Synthetic terminal claim for {state}"
    fact_id = (
        _legacy_fact_id(claim) if auto_id else f"synthetic-terminal-{state}"
    )
    if auto_id:
        assert fact_id != _fact_id(claim)
    _seed_fact(fact_id, claim, state)
    before = _snapshot(fact_id)

    with pytest.raises(ValueError) as exc_info:
        ingest(
            claim,
            fact_id=None if auto_id else fact_id,
            source="untrusted-repeat-source",
            confidence=0.1,
            source_status="LLM_OUTPUT",
            metadata={"incoming_marker": "must-not-persist"},
        )

    assert _snapshot(fact_id) == before
    _assert_error_code(exc_info, "TERMINAL_STATE")


def test_terminal_auto_repeat_does_not_backfill_existing_normalized_index():
    claim = "Synthetic terminal legacy identity with unrelated validated row"
    terminal_id = _legacy_fact_id(claim)
    _seed_fact(terminal_id, claim, "Deprecated")

    other_claim = "Synthetic unrelated validated index candidate"
    other_id = _fact_id(other_claim)
    _seed_fact(other_id, other_claim, "Validated")
    with memory._db() as conn:
        conn.execute(
            "CREATE TABLE normalized_ingest_index ("
            "fact_id TEXT PRIMARY KEY, normalized_id TEXT NOT NULL, "
            "fact_revision INTEGER NOT NULL)"
        )

    before = _snapshot(terminal_id)
    assert before["normalized_ingest_index"] == {"exists": True, "rows": []}

    with pytest.raises(ValueError) as exc_info:
        ingest(claim, source="terminal-repeat-source")

    assert _snapshot(terminal_id) == before
    _assert_error_code(exc_info, "TERMINAL_STATE")


def test_immutable_core_repeat_is_terminal_and_unchanged():
    """T05: ImmutableCore facts are protected from ordinary repeated ingest."""
    fact_id = "synthetic-immutable-core"
    claim = "Synthetic immutable-core identity"
    _seed_fact(fact_id, claim, "ImmutableCore")
    before = _snapshot(fact_id)

    with pytest.raises(ValueError) as exc_info:
        ingest(claim, fact_id=fact_id, source="untrusted-repeat-source")

    assert _snapshot(fact_id) == before
    _assert_error_code(exc_info, "TERMINAL_STATE")


def test_validated_exact_explicit_repeat_preserves_duplicate_only_semantics():
    """T06, T19–T20: exact duplicates add frequency, never confidence/evidence."""
    fact_id = "synthetic-validated-exact"
    claim = "Synthetic validated identity remains exact"
    _seed_fact(fact_id, claim, "Validated")
    before = _snapshot(fact_id)
    assert before["strict_canonical"] is True

    result = ingest(claim, fact_id=fact_id, source="repeat-source")

    assert result["accepted"] is True
    assert result["duplicate"] is True
    assert result["occurrences"] == 5
    current = memory.get_fact(fact_id)
    assert current["claim"] == claim
    assert current["confidence"] == before["l3"]["confidence"]
    assert current["epistemic_state"] == "Validated"
    assert current["metadata"]["occurrences"] == 5
    assert "observations" not in current["metadata"]
    assert current["metadata"]["sources_seen"] == [
        "baseline-source", "repeat-source"
    ]
    after = _snapshot(fact_id)
    assert after["l3"]["truth_status"] == before["l3"]["truth_status"]
    assert after["strict_canonical"] is True
    assert after["evidence"] == before["evidence"]


def test_auto_id_duplicate_keeps_existing_normalized_identity_contract():
    """Auto-ID still permits Crystal's pre-existing exact-normalized duplicate."""
    claim = "Synthetic claim with exact normalized identity"
    fact_id = _fact_id(claim)
    _seed_fact(fact_id, claim, "Validated")

    result = ingest("  synthetic   CLAIM WITH exact normalized identity  ")

    assert result["accepted"] is True
    assert result["duplicate"] is True
    assert result["fact"]["fact_id"] == fact_id
    assert result["occurrences"] == 5
    assert memory.get_fact(fact_id)["claim"] == claim


@pytest.mark.parametrize(
    "state", ("Supported", "Validated", "Contradicted", "Deprecated", "Collapsed", "ImmutableCore")
)
def test_different_claim_on_locked_explicit_id_is_identity_conflict(state):
    """T07–T09: a locked ID cannot absorb a different claim or occurrence."""
    fact_id = f"synthetic-identity-conflict-{state}"
    original_claim = f"Synthetic original identity for {state}"
    _seed_fact(fact_id, original_claim, state)
    before = _snapshot(fact_id)

    with pytest.raises(ValueError) as exc_info:
        ingest(
            "Synthetic unrelated incoming claim",
            fact_id=fact_id,
            source="foreign-source",
            confidence=1.0,
            metadata={"incoming_marker": "must-not-persist"},
        )

    _assert_error_code(exc_info, "CLAIM_IDENTITY_CONFLICT")
    assert _snapshot(fact_id) == before
    assert before["l1"]["revision"] == _snapshot(fact_id)["l1"]["revision"]
    assert memory.get_fact(fact_id)["metadata"]["occurrences"] == 4
    assert memory.get_fact(fact_id)["metadata"]["fingerprint_sha256"] == "existing-fingerprint"
    assert memory.get_fact(fact_id)["metadata"]["sources_seen"] == ["baseline-source"]


def test_new_fact_ingest_still_succeeds_normally():
    """T10: a fresh identity continues through the normal gate and L3 path."""
    result = ingest(
        "Synthetic new fact with an external source",
        source="synthetic-source",
        source_status="EXTERNAL",
        confidence=0.91,
    )
    assert result["accepted"] is True
    assert result["fact"]["epistemic_state"] == "Validated"
    assert get_l3_graph().get_fact(result["fact"]["fact_id"]) is not None


def test_new_observed_fact_keeps_existing_gate_blocking_behavior():
    """T11: a new LLM_OUTPUT world claim is still stored as Observed then blocked."""
    result = ingest(
        "Synthetic untrusted world claim that must remain pending",
        source="synthetic-llm",
        source_status="LLM_OUTPUT",
        claim_type="WORLD_FACT",
        confidence=0.91,
    )
    assert result["accepted"] is False
    assert memory.get_fact(result["fact"]["fact_id"])["epistemic_state"] == "Observed"
    assert get_l3_graph().get_fact(result["fact"]["fact_id"]) is None


def test_observed_fact_refinement_remains_permitted():
    """An existing draft-state identity may retain its established refinement path."""
    fact_id = "synthetic-observed-refinement"
    memory.store_fact({"fact_id": fact_id, "claim": "Synthetic draft A"})

    result = ingest(
        "I feel calm about this synthetic draft",
        fact_id=fact_id,
        claim_type="EMOTION",
    )

    assert result["accepted"] is True
    assert result["fact"]["claim"] == "I feel calm about this synthetic draft"
    assert memory.get_fact(fact_id)["epistemic_state"] == "Validated"


def test_http_auto_id_terminal_repeat_keeps_422_and_returns_stable_code(monkeypatch):
    """T15: HTTP still uses 422; the code is machine-readable in detail."""
    from fastapi.testclient import TestClient
    from core import api

    monkeypatch.setenv("VELANTRIM_API_ALLOW_UNAUTH_LOCAL", "1")
    monkeypatch.delenv("VELANTRIM_API_TOKEN", raising=False)
    claim = "Synthetic HTTP terminal repeat"
    fact_id = _fact_id(claim)
    _seed_fact(fact_id, claim, "Collapsed")
    before = _snapshot(fact_id)
    client = TestClient(api.create_app())

    response = client.post("/ingest", json={"text": claim, "source": "http-repeat"})

    assert response.status_code == 422
    assert _snapshot(fact_id) == before
    assert response.json()["detail"].startswith("TERMINAL_STATE:")


def test_http_auto_id_identity_conflict_keeps_422_and_returns_stable_code(monkeypatch):
    from fastapi.testclient import TestClient
    from core import api

    monkeypatch.setenv("VELANTRIM_API_ALLOW_UNAUTH_LOCAL", "1")
    monkeypatch.delenv("VELANTRIM_API_TOKEN", raising=False)
    claim = "Synthetic HTTP auto-ID collision target"
    fact_id = _fact_id(claim)
    _seed_fact(fact_id, "Synthetic different persisted identity", "Validated")
    before = _snapshot(fact_id)
    client = TestClient(api.create_app())

    response = client.post("/ingest", json={"text": claim, "source": "http-collision"})

    assert response.status_code == 422
    assert response.json()["detail"].startswith("CLAIM_IDENTITY_CONFLICT:")
    assert _snapshot(fact_id) == before


def test_knowledge_ingest_does_not_accept_or_attach_evidence_after_terminal_refusal():
    """T16: import callers propagate rejection before accepted/evidence bookkeeping."""
    from core import knowledge

    claim = "Synthetic knowledge import terminal repeat"
    fact_id = _fact_id(claim)
    _seed_fact(fact_id, claim, "Deprecated")
    before = _snapshot(fact_id)

    with pytest.raises(ValueError) as exc_info:
        knowledge.ingest_claims(
            [{"claim": claim}],
            source="synthetic-import",
            source_content=claim,
        )

    assert _snapshot(fact_id) == before
    _assert_error_code(exc_info, "TERMINAL_STATE")


def test_concurrent_writer_terminal_transition_prevents_stale_ingest_write(monkeypatch):
    """T17: final transaction check rejects state changed after ingest's first read."""
    import core.ingest as ingest_module

    fact_id = "synthetic-terminal-write-race"
    claim = "Synthetic claim changed by a concurrent writer"
    memory.store_fact({
        "fact_id": fact_id,
        "claim": claim,
        "source": "original-source",
        "source_status": "EXTERNAL",
        "confidence": 0.9,
        "metadata": {"preserve": "original"},
    })
    before = _snapshot(fact_id)
    reached_write = threading.Event()
    writer_finished = threading.Event()
    errors = []
    real_store_fact = ingest_module.store_fact

    def concurrent_writer():
        if not reached_write.wait(timeout=5):
            errors.append("ingest did not reach store boundary")
            return
        try:
            memory.transition_esm(fact_id, "Collapsed")
        except Exception as exc:  # pragma: no cover - reported through assertion
            errors.append(exc)
        finally:
            writer_finished.set()

    writer = threading.Thread(target=concurrent_writer)
    writer.start()

    def store_after_writer(fact, **kwargs):
        reached_write.set()
        assert writer_finished.wait(timeout=5)
        return real_store_fact(fact, **kwargs)

    monkeypatch.setattr(ingest_module, "store_fact", store_after_writer)
    with pytest.raises(ValueError) as exc_info:
        ingest(
            claim,
            fact_id=fact_id,
            source="stale-ingest-source",
            confidence=0.1,
            metadata={"incoming": "must-not-persist"},
        )
    writer.join(timeout=5)

    assert not writer.is_alive()
    assert errors == []
    _assert_only_state_transition(before, _snapshot(fact_id), "Collapsed")
    _assert_error_code(exc_info, "TERMINAL_STATE")


def test_validated_duplicate_race_to_terminal_state_does_not_record_occurrence(monkeypatch):
    """The final duplicate occurrence write is state-checked, not a TOCTOU preflight."""
    import core.reconcile as reconcile_module

    fact_id = "synthetic-duplicate-race"
    claim = "Synthetic validated identity racing a terminal transition"
    _seed_fact(fact_id, claim, "Validated")
    before = _snapshot(fact_id)
    real_update_fact = reconcile_module.update_fact
    transitioned = {"done": False}

    def transition_before_update(*args, **kwargs):
        if not transitioned["done"]:
            transitioned["done"] = True
            memory.transition_esm(fact_id, "Collapsed")
        return real_update_fact(*args, **kwargs)

    monkeypatch.setattr(reconcile_module, "update_fact", transition_before_update)
    with pytest.raises(ValueError) as exc_info:
        ingest(claim, fact_id=fact_id, source="racing-repeat")

    _assert_only_state_transition(before, _snapshot(fact_id), "Collapsed")
    _assert_error_code(exc_info, "TERMINAL_STATE")


def test_terminal_guard_is_effective_after_process_restart():
    """T18: a fresh interpreter reads persisted state and still rejects the repeat."""
    fact_id = "synthetic-terminal-after-restart"
    claim = "Synthetic terminal claim survives a process restart"
    _seed_fact(fact_id, claim, "Deprecated")
    before = _snapshot(fact_id)
    script = """
import json
import sys
from core.ingest import ingest
try:
    ingest(sys.argv[1], fact_id=sys.argv[2], source='restart-repeat')
except ValueError as exc:
    print(json.dumps({'code': getattr(exc, 'code', None)}))
else:
    print(json.dumps({'accepted': True}))
"""
    env = os.environ.copy()
    env["VELANTRIM_DB"] = memory.SQLITE_PATH
    env["VELANTRIM_DEMO_SEED"] = "0"
    completed = subprocess.run(
        [sys.executable, "-c", script, claim, fact_id],
        cwd=os.getcwd(),
        env=env,
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    )

    assert _snapshot(fact_id) == before
    assert json.loads(completed.stdout.strip()) == {"code": "TERMINAL_STATE"}



def test_concurrent_writer_nonterminal_esm_change_prevents_stale_upsert(monkeypatch):
    """A valid Observed→Supported race is refused before provenance is overwritten."""
    import core.ingest as ingest_module

    fact_id = "synthetic-supported-write-race"
    claim = "Synthetic claim racing to Supported"
    memory.store_fact({
        "fact_id": fact_id,
        "claim": claim,
        "source": "original-source",
        "source_status": "EXTERNAL",
        "confidence": 0.9,
        "metadata": {"preserve": "original"},
    })
    before = _snapshot(fact_id)
    reached_write = threading.Event()
    writer_finished = threading.Event()
    errors = []
    real_store_fact = ingest_module.store_fact

    def concurrent_writer():
        if not reached_write.wait(timeout=5):
            errors.append("ingest did not reach store boundary")
            return
        try:
            memory.transition_esm(fact_id, "Supported")
        except Exception as exc:  # pragma: no cover - reported through assertion
            errors.append(exc)
        finally:
            writer_finished.set()

    writer = threading.Thread(target=concurrent_writer)
    writer.start()

    def store_after_writer(fact, **kwargs):
        reached_write.set()
        assert writer_finished.wait(timeout=5)
        return real_store_fact(fact, **kwargs)

    monkeypatch.setattr(ingest_module, "store_fact", store_after_writer)
    with pytest.raises(ValueError) as exc_info:
        ingest(
            claim,
            fact_id=fact_id,
            source="stale-ingest-source",
            confidence=0.1,
            metadata={"incoming": "must-not-persist"},
        )
    writer.join(timeout=5)

    assert not writer.is_alive()
    assert errors == []
    _assert_only_state_transition(before, _snapshot(fact_id), "Supported")
    assert getattr(exc_info.value, "code", None) == "CONCURRENT_STATE_CHANGE"


def test_concurrent_delete_does_not_resurrect_fact_from_stale_ingest(monkeypatch):
    import core.ingest as ingest_module

    fact_id = "synthetic-delete-before-ingest-write"
    claim = "Synthetic claim deleted at the write boundary"
    memory.store_fact({"fact_id": fact_id, "claim": claim, "source": "original"})
    real_store_fact = ingest_module.store_fact

    def delete_before_store(fact, **kwargs):
        assert memory.delete_fact_l1(fact_id) is True
        return real_store_fact(fact, **kwargs)

    monkeypatch.setattr(ingest_module, "store_fact", delete_before_store)
    with pytest.raises(ValueError) as exc_info:
        ingest(claim, fact_id=fact_id, source="must-not-resurrect")

    assert getattr(exc_info.value, "code", None) == "CONCURRENT_STATE_CHANGE"
    assert memory.get_fact(fact_id) is None
    assert get_l3_graph().get_fact(fact_id) is None
    assert evidence.evidence_for(fact_id) == []
    with memory._db() as conn:
        assert conn.execute(
            "SELECT 1 FROM facts WHERE fact_id = ?", (fact_id,)
        ).fetchone() is None


def test_occurrence_revision_cas_miss_retries_without_losing_duplicate(monkeypatch):
    """A competing revision between occurrence read and write retries against fresh L1."""
    import sqlite3

    fact_id = "synthetic-occurrence-revision-race"
    claim = "Synthetic exact duplicate with a revision race"
    _seed_fact(fact_id, claim, "Validated")
    before = _snapshot(fact_id)
    real_begin_immediate = memory.begin_immediate
    raced = {"done": False}

    def bump_revision_before_lock(conn):
        if not raced["done"]:
            raced["done"] = True
            with sqlite3.connect(memory.SQLITE_PATH, timeout=10) as competitor:
                competitor.execute(
                    "UPDATE facts SET revision = revision + 1 WHERE fact_id = ?",
                    (fact_id,),
                )
        return real_begin_immediate(conn)

    monkeypatch.setattr(memory, "begin_immediate", bump_revision_before_lock)
    result = ingest(claim, fact_id=fact_id, source="cas-retry-source")

    assert raced["done"] is True
    assert result["accepted"] is True and result["duplicate"] is True
    assert result["occurrences"] == 5
    current = memory.get_fact(fact_id)
    assert current["metadata"]["occurrences"] == 5
    assert current["confidence"] == 0.91
    assert current["epistemic_state"] == "Validated"
    assert current["metadata"]["sources_seen"] == [
        "baseline-source", "cas-retry-source"
    ]
    assert evidence.evidence_for(fact_id) == before["evidence"]


def test_occurrence_write_rejects_a_stale_expected_claim():
    from core import reconcile

    fact_id = "synthetic-occurrence-identity-guard"
    claim = "Synthetic persisted identity for conditional occurrence"
    _seed_fact(fact_id, claim, "Validated")
    before = _snapshot(fact_id)

    with pytest.raises(memory.ClaimIdentityError) as exc_info:
        reconcile.record_occurrence(
            fact_id, source="foreign-source", expected_claim="different claim"
        )

    assert exc_info.value.code == "CLAIM_IDENTITY_CONFLICT"
    assert _snapshot(fact_id) == before


def test_occurrence_write_rejects_a_nonvalidated_persisted_state():
    from core import reconcile

    fact_id = "synthetic-occurrence-nonvalidated-state"
    claim = "Synthetic Supported identity is not duplicate-admissible"
    _seed_fact(fact_id, claim, "Supported")
    before = _snapshot(fact_id)

    with pytest.raises(memory.IngestStateChangedError):
        reconcile.record_occurrence(
            fact_id, source="repeat-source", expected_claim=claim
        )

    assert _snapshot(fact_id) == before


def test_duplicate_path_maps_unexpected_state_change_code(monkeypatch):
    import core.ingest as ingest_module

    fact_id = "synthetic-duplicate-state-error-map"
    claim = "Synthetic validated identity for state-error mapping"
    _seed_fact(fact_id, claim, "Validated")
    before = _snapshot(fact_id)

    def reject_occurrence(*args, **kwargs):
        raise memory.IngestStateChangedError("synthetic competing state change")

    monkeypatch.setattr(ingest_module, "record_occurrence", reject_occurrence)
    with pytest.raises(ValueError) as exc_info:
        ingest(claim, fact_id=fact_id, source="repeat-source")

    assert getattr(exc_info.value, "code", None) == "CONCURRENT_STATE_CHANGE"
    assert _snapshot(fact_id) == before


def test_occurrence_cas_exhaustion_returns_actual_count_without_mutation(monkeypatch):
    from core import reconcile

    fact_id = "synthetic-occurrence-cas-exhaustion"
    claim = "Synthetic exact duplicate under sustained CAS contention"
    _seed_fact(fact_id, claim, "Validated")
    before = _snapshot(fact_id)
    monkeypatch.setattr(reconcile, "update_fact", lambda *args, **kwargs: False)

    result = ingest(claim, fact_id=fact_id, source="dropped-sighting")

    assert result["accepted"] is True and result["duplicate"] is True
    assert result["occurrences"] == 4
    assert _snapshot(fact_id) == before


def test_occurrence_cas_exhaustion_refuses_if_writer_moved_to_terminal(monkeypatch):
    from core import reconcile

    fact_id = "synthetic-occurrence-cas-terminal-exhaustion"
    claim = "Synthetic duplicate races to a terminal state under contention"
    _seed_fact(fact_id, claim, "Validated")
    before = _snapshot(fact_id)
    real_update_fact = reconcile.update_fact
    transitioned = {"done": False}

    def terminal_then_miss(*args, **kwargs):
        if not transitioned["done"]:
            transitioned["done"] = True
            memory.transition_esm(fact_id, "Collapsed")
        return False

    monkeypatch.setattr(reconcile, "update_fact", terminal_then_miss)
    with pytest.raises(memory.TerminalStateError):
        reconcile.record_occurrence(
            fact_id, source="racing-repeat", expected_claim=claim
        )

    assert transitioned["done"] is True
    _assert_only_state_transition(before, _snapshot(fact_id), "Collapsed")
    monkeypatch.setattr(reconcile, "update_fact", real_update_fact)


def test_occurrence_cas_exhaustion_refuses_identity_mismatch(monkeypatch):
    from core import reconcile

    fact_id = "synthetic-occurrence-cas-identity-exhaustion"
    claim = "Synthetic persisted claim under repeated CAS misses"
    _seed_fact(fact_id, claim, "Validated")
    before = _snapshot(fact_id)
    monkeypatch.setattr(reconcile, "update_fact", lambda *args, **kwargs: False)

    with pytest.raises(memory.ClaimIdentityError) as exc_info:
        reconcile.record_occurrence(
            fact_id, source="foreign-source", expected_claim="stale claim"
        )

    assert exc_info.value.code == "CLAIM_IDENTITY_CONFLICT"
    assert _snapshot(fact_id) == before


def test_occurrence_cas_exhaustion_refuses_nonterminal_state(monkeypatch):
    from core import reconcile

    fact_id = "synthetic-occurrence-cas-nonterminal-exhaustion"
    claim = "Synthetic supported fact under repeated CAS misses"
    _seed_fact(fact_id, claim, "Supported")
    before = _snapshot(fact_id)
    monkeypatch.setattr(reconcile, "update_fact", lambda *args, **kwargs: False)

    with pytest.raises(memory.IngestStateChangedError):
        reconcile.record_occurrence(
            fact_id, source="repeat-source", expected_claim=claim
        )

    assert _snapshot(fact_id) == before



def test_auto_index_refresh_failure_after_primary_write_is_nonfatal(monkeypatch):
    import core.ingest as ingest_module

    real_resolver = ingest_module.resolve_validated_normalized_fact

    def fail_only_persistent_refresh(query_text, *, persist_index=True):
        if persist_index:
            raise OSError("synthetic derived-index storage failure")
        return real_resolver(query_text, persist_index=persist_index)

    monkeypatch.setattr(
        ingest_module,
        "resolve_validated_normalized_fact",
        fail_only_persistent_refresh,
    )
    claim = "Synthetic new identity with unavailable derived-index cache"

    result = ingest(claim, source="synthetic-source")

    assert result["accepted"] is True
    assert result["fact"]["epistemic_state"] == "Validated"
    assert memory.get_fact(result["fact"]["fact_id"])["epistemic_state"] == "Validated"
