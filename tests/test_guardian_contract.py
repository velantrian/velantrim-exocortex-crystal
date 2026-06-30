"""Tests for the Guardian detect → flag/block contract (pipeline baseline)."""
from core.pipeline import (
    GUARDIAN_CONTRACT,
    GUARDIAN_VERDICT_BLOCK,
    GUARDIAN_VERDICT_PASS,
    guardian,
    guardian_diagnose,
)


def _pack(*facts):
    return {"facts": list(facts), "query": "q", "total": len(facts)}


def _trace(*fact_ids):
    return [{"fact_id": fid, "source": "s", "origin": "test",
             "epistemic_state": "Observed"} for fid in fact_ids]


def test_guardian_contract_documents_baseline():
    assert "TruthGate" in GUARDIAN_CONTRACT
    assert "Does not promote" in GUARDIAN_CONTRACT


def test_guardian_diagnose_passes_valid_pack():
    fact = {"fact_id": "f1", "claim": "c", "source": "s", "confidence": 0.8}
    diag = guardian_diagnose(_pack(fact), _trace("f1"))
    assert diag["verdict"] == GUARDIAN_VERDICT_PASS
    assert diag["reason"] is None
    assert all(diag["checks"].values())


def test_guardian_diagnose_blocks_empty_pack():
    diag = guardian_diagnose(_pack(), _trace())
    assert diag["verdict"] == GUARDIAN_VERDICT_BLOCK
    assert "empty" in diag["reason"].lower()


def test_guardian_diagnose_blocks_trace_mismatch():
    fact = {"fact_id": "f1", "claim": "c", "source": "s", "confidence": 0.8}
    diag = guardian_diagnose(_pack(fact), [])
    assert diag["verdict"] == GUARDIAN_VERDICT_BLOCK
    assert "Trace is empty" in diag["reason"]


def test_guardian_tuple_matches_diagnose():
    fact = {"fact_id": "f1", "claim": "c", "source": "s", "confidence": 0.0}
    ok, reason = guardian(_pack(fact), _trace("f1"))
    assert ok is False
    assert "Zero confidence" in reason
    assert guardian_diagnose(_pack(fact), _trace("f1"))["verdict"] == GUARDIAN_VERDICT_BLOCK
