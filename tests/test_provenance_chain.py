"""Tests for core/provenance_chain.py — per-fact, append-only provenance chain
(Sprint1 P1-5, invariant I89 ProvenanceAppendOnly).

Covers the seven behaviours required by the audit spec:
  1. append() succeeds for a normal event
  2. verify() succeeds on a non-empty chain
  3. tampering payload_str fails verification
  4. tampering actor fails verification
  5. tampering reason fails verification
  6. the GDPR/erasure path records a provenance event
  7. an empty chain reports empty_chain / no_events, never a verified non-empty chain
"""
import pytest

from core import memory
from core.provenance_chain import ProvenanceChain, _compute_hash, _GENESIS
from core.erasure import erase_fact


def _seed(fact_id, claim="a claim", state="Validated"):
    memory.store_fact({"fact_id": fact_id, "claim": claim, "source": "s",
                       "epistemic_state": state})


def _tamper(fact_id, column, value, seq=1):
    """Directly corrupt one stored column without re-sealing the hash."""
    with memory._db() as conn:
        conn.execute(
            f"UPDATE provenance_chain SET {column} = ? "
            f"WHERE fact_id = ? AND seq = ?",
            (value, fact_id, seq))


# ─── 1. append() succeeds for a normal event ──────────────────────────────────

def test_append_succeeds_for_normal_event():
    pc = ProvenanceChain()
    ok = pc.append(fact_id="f1", event_type="ingest",
                   from_state="", to_state="Observed",
                   payload_str="sha256:abc", actor="user", reason="seen")
    assert ok is True
    chain = pc.chain("f1")
    assert len(chain) == 1
    entry = chain[0]
    assert entry["seq"] == 1
    assert entry["event_type"] == "ingest"
    assert entry["prev_hash"] == _GENESIS  # first link starts at genesis


def test_append_links_successive_events():
    pc = ProvenanceChain()
    assert pc.append(fact_id="f1", event_type="ingest", to_state="Observed")
    assert pc.append(fact_id="f1", event_type="promote",
                     from_state="Observed", to_state="Validated")
    chain = pc.chain("f1")
    assert [e["seq"] for e in chain] == [1, 2]
    # The second entry links to the first; chains are per-fact.
    assert chain[1]["prev_hash"] == chain[0]["hash"]


# ─── 2. verify() succeeds on a non-empty chain ────────────────────────────────

def test_verify_non_empty_chain_ok():
    pc = ProvenanceChain()
    pc.append(fact_id="f1", event_type="ingest", to_state="Observed")
    pc.append(fact_id="f1", event_type="promote",
              from_state="Observed", to_state="Validated", actor="curator")
    v = pc.verify("f1")
    assert v["status"] == "ok"
    assert v["ok"] is True
    assert v["length"] == 2
    assert v["broken_at"] is None


# ─── 3-5. tampering any sealed field fails verification ───────────────────────

def test_tamper_payload_fails_verification():
    pc = ProvenanceChain()
    pc.append(fact_id="f1", event_type="ingest", payload_str="sha256:orig")
    _tamper("f1", "payload_str", "sha256:forged")
    v = pc.verify("f1")
    assert v["ok"] is False
    assert v["status"] == "tampered"
    assert v["broken_at"] == 1


def test_tamper_actor_fails_verification():
    pc = ProvenanceChain()
    pc.append(fact_id="f1", event_type="ingest", actor="user")
    _tamper("f1", "actor", "attacker")
    v = pc.verify("f1")
    assert v["ok"] is False
    assert v["status"] == "tampered"


def test_tamper_reason_fails_verification():
    pc = ProvenanceChain()
    pc.append(fact_id="f1", event_type="ingest", reason="data_subject_request")
    _tamper("f1", "reason", "rewritten reason")
    v = pc.verify("f1")
    assert v["ok"] is False
    assert v["status"] == "tampered"


def test_sequence_gap_fails_verification():
    """Deleting/renumbering an entry so seq jumps is detected as reordering."""
    pc = ProvenanceChain()
    pc.append(fact_id="f1", event_type="ingest")
    pc.append(fact_id="f1", event_type="promote")
    # Delete the genesis entry (seq 1): the surviving row now starts at seq 2,
    # so verify() expects seq 1 but finds seq 2 — a gap / reordering.
    with memory._db() as conn:
        conn.execute("DELETE FROM provenance_chain WHERE fact_id = ? AND seq = 1",
                     ("f1",))
    v = pc.verify("f1")
    assert v["ok"] is False
    assert v["status"] == "tampered"
    assert v["error"] == "sequence gap or reordering"
    assert v["broken_at"] == 2


def test_broken_prev_hash_link_fails_verification():
    """Corrupting prev_hash on a non-genesis entry breaks the chain link."""
    pc = ProvenanceChain()
    pc.append(fact_id="f1", event_type="ingest")
    pc.append(fact_id="f1", event_type="promote")
    _tamper("f1", "prev_hash", "f" * 64, seq=2)
    v = pc.verify("f1")
    assert v["ok"] is False
    assert v["error"] == "prev_hash link mismatch"
    assert v["broken_at"] == 2


def test_tamper_in_middle_reports_first_broken_seq():
    pc = ProvenanceChain()
    pc.append(fact_id="f1", event_type="ingest")
    pc.append(fact_id="f1", event_type="promote")
    pc.append(fact_id="f1", event_type="restrict")
    _tamper("f1", "event_type", "FORGED", seq=2)
    v = pc.verify("f1")
    assert v["ok"] is False
    # seq 2's hash no longer matches; seq 3's prev_hash link still points at the
    # original seq 2 hash, so the break surfaces at seq 2.
    assert v["broken_at"] == 2


# ─── 6. the GDPR/erasure path records a provenance event ──────────────────────

def test_erase_fact_records_provenance_event():
    _seed("f1", claim="personal data", state="Validated")
    erase_fact("f1", reason="data_subject_request", actor="dpo")

    chain = ProvenanceChain().chain("f1")
    erase_events = [e for e in chain if e["event_type"] == "erase"]
    assert len(erase_events) == 1
    ev = erase_events[0]
    assert ev["actor"] == "dpo"
    assert ev["reason"] == "data_subject_request"
    assert ev["to_state"] == "erased"
    # Content-light: the claim text is never copied into the chain.
    assert "personal data" not in str(chain)


def test_erase_fact_provenance_chain_verifies():
    _seed("f1", state="Validated")
    erase_fact("f1", reason="r", actor="dpo")
    v = ProvenanceChain().verify("f1")
    assert v["status"] == "ok"
    assert v["ok"] is True


# ─── 7. empty chain is reported, never treated as a verified non-empty chain ──

def test_empty_chain_is_not_verified():
    v = ProvenanceChain().verify("never_seen")
    assert v["status"] == "empty_chain"
    assert v["error"] == "no_events"
    assert v["ok"] is False
    assert v["length"] == 0
    # An empty chain must be DISTINGUISHABLE from a verified non-empty chain.
    assert v["status"] != "ok"


# ─── append() never raises (critical-path contract) ──────────────────────────

def test_append_returns_false_on_failure(monkeypatch):
    """append() must swallow errors and return False — a provenance-write
    problem must never disturb a critical-path caller such as erase_fact()."""
    def _boom():
        raise RuntimeError("db down")
    monkeypatch.setattr(memory, "_db", _boom)
    ok = ProvenanceChain().append(fact_id="f1", event_type="ingest")
    assert ok is False


# ─── _compute_hash is deterministic and field-sensitive ──────────────────────

def test_compute_hash_is_deterministic_and_sensitive():
    base = dict(prev_hash=_GENESIS, event_type="ingest", fact_id="f1",
                from_state="", to_state="Observed", payload_str="p",
                created_at="2026-01-01T00:00:00+00:00", actor="user",
                reason="seen")
    h1 = _compute_hash(**base)
    h2 = _compute_hash(**base)
    assert h1 == h2  # deterministic
    # Changing any single sealed field changes the hash.
    assert _compute_hash(**{**base, "actor": "other"}) != h1
    assert _compute_hash(**{**base, "reason": "other"}) != h1
    assert _compute_hash(**{**base, "payload_str": "other"}) != h1
