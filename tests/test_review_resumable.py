"""Tests for resumable review sessions (core/review.py, PR3 — grant WP2).

A resumable session snapshots the pending queue at creation time so a curator
can pause and return to the same unresolved batch.

Key invariant under test:
  resume_session() returns ONLY claims that (a) were pending when the session
  was created AND (b) are still in Observed state AND (c) have not yet been
  reviewed in this session.
"""
import pytest

from core import review
from core.ingest import ingest
from core.memory import get_all_facts, store_fact


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _blocked_fact(claim: str) -> str:
    """Ingest a WORLD_FACT the gate blocks → stays Observed (pending)."""
    res = ingest(claim, claim_type="WORLD_FACT", source_status="LLM_OUTPUT")
    assert res["accepted"] is False
    return res["fact"]["fact_id"]


def _ready_pending(claim: str, fid: str) -> str:
    """Store a directly-Observed fact (ready for curator approval)."""
    store_fact({
        "fact_id": fid, "claim": claim, "source": "session-test",
        "confidence": 0.9, "epistemic_state": "Observed",
        "claim_type": "WORLD_FACT", "source_status": "EXTERNAL",
        "significance": 0.5,
    })
    return fid


# ─── Session lifecycle ────────────────────────────────────────────────────────

def test_create_session_captures_pending_ids(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    fid = _blocked_fact("Quortium has a half-life of zero")
    session = review.create_session()
    assert session["session_id"]
    assert session["status"] == "pending"
    assert fid in session["claim_ids"]


def test_get_session_round_trip(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    _blocked_fact("Zorbium melts at 9000 K")
    session = review.create_session()
    fetched = review.get_session(session["session_id"])
    assert fetched is not None
    assert fetched["session_id"] == session["session_id"]
    assert fetched["claim_ids"] == session["claim_ids"]


def test_get_session_unknown_returns_none():
    assert review.get_session("no-such-id-00000000") is None


def test_create_session_batch_size(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    _blocked_fact("Planck-1 goes negative")
    _blocked_fact("Planck-2 goes negative")
    _blocked_fact("Planck-3 goes negative")
    session = review.create_session(batch_size=2)
    assert len(session["claim_ids"]) <= 2
    assert session["batch_size"] == 2


# ─── Core resumability guarantee ──────────────────────────────────────────────

def test_review_resume_shows_same_pending_claims(monkeypatch):
    """The central PR3 invariant: resume returns the same unresolved batch."""
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    fid_a = _blocked_fact("Xyrion boils below zero Kelvin")
    fid_b = _blocked_fact("Xyrion freezes above 5000 K")

    session = review.create_session()
    assert fid_a in session["claim_ids"]
    assert fid_b in session["claim_ids"]

    # First resume — both claims visible
    result = review.resume_session(session["session_id"])
    assert result["found"] is True
    assert result["status"] == "in_progress"
    ids_first = {item["fact_id"] for item in result["pending_items"]}
    assert fid_a in ids_first
    assert fid_b in ids_first

    # Simulate curator approving fid_a (approve transitions it to Validated)
    review.approve(fid_a, actor="curator")
    review.record_session_decision(session["session_id"], fid_a, "approved")

    # Second resume — fid_a gone (no longer Observed), fid_b still there
    result2 = review.resume_session(session["session_id"])
    ids_second = {item["fact_id"] for item in result2["pending_items"]}
    assert fid_a not in ids_second
    assert fid_b in ids_second


def test_resume_session_unknown_returns_not_found():
    result = review.resume_session("no-such-session-xxxx")
    assert result["found"] is False


def test_resume_completed_session_returns_empty(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    _blocked_fact("Velantrium emits dark matter continuously")
    session = review.create_session()
    review.complete_session(session["session_id"])
    result = review.resume_session(session["session_id"])
    assert result["found"] is True
    assert result["status"] == "completed"
    assert result["pending_items"] == []


# ─── record_session_decision ──────────────────────────────────────────────────

def test_record_session_decision_approved(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    fid = _blocked_fact("Omega-7 is unstable at room temperature")
    session = review.create_session()
    sid = session["session_id"]
    review.approve(fid, actor="curator")
    res = review.record_session_decision(sid, fid, "approved")
    assert res["ok"] is True
    updated = review.get_session(sid)
    assert fid in updated["reviewed_ids"]
    assert updated["approved_count"] == 1
    assert updated["rejected_count"] == 0


def test_record_session_decision_rejected(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    fid = _blocked_fact("Negantropy violates thermodynamics locally")
    session = review.create_session()
    sid = session["session_id"]
    review.reject(fid)
    res = review.record_session_decision(sid, fid, "rejected")
    assert res["ok"] is True
    updated = review.get_session(sid)
    assert fid in updated["reviewed_ids"]
    assert updated["rejected_count"] == 1
    assert updated["approved_count"] == 0


def test_record_session_decision_invalid_decision(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    _blocked_fact("Phlogiston is real")
    session = review.create_session()
    res = review.record_session_decision(session["session_id"], "any-id", "skipped")
    assert res["ok"] is False


def test_record_session_decision_unknown_session():
    res = review.record_session_decision("no-such-session", "fid-xyz", "approved")
    assert res["ok"] is False


# ─── complete_session ─────────────────────────────────────────────────────────

def test_complete_session(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    _blocked_fact("Aetherium defies gravity locally")
    session = review.create_session()
    res = review.complete_session(session["session_id"])
    assert res["ok"] is True
    assert res["status"] == "completed"
    updated = review.get_session(session["session_id"])
    assert updated["status"] == "completed"


def test_complete_session_unknown():
    res = review.complete_session("no-such-session-yyyy")
    assert res["ok"] is False


# ─── list_sessions ────────────────────────────────────────────────────────────

def test_list_sessions_filter_by_status(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    _blocked_fact("Zeta particle oscillates at 1 Hz")
    s1 = review.create_session()
    s2 = review.create_session()
    review.complete_session(s1["session_id"])

    completed = review.list_sessions(status="completed")
    pending = review.list_sessions(status="pending")
    sids_completed = [s["session_id"] for s in completed]
    sids_pending = [s["session_id"] for s in pending]
    assert s1["session_id"] in sids_completed
    assert s2["session_id"] in sids_pending
    assert s2["session_id"] not in sids_completed


def test_list_sessions_no_filter(monkeypatch):
    """list_sessions() with no status arg returns all sessions (covers else branch)."""
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    _blocked_fact("Nullium has infinite density")
    s1 = review.create_session()
    review.complete_session(s1["session_id"])
    s2 = review.create_session()

    all_sessions = review.list_sessions()
    sids = [s["session_id"] for s in all_sessions]
    assert s1["session_id"] in sids
    assert s2["session_id"] in sids


def test_resume_skips_fact_no_longer_observed(monkeypatch):
    """resume_session skips facts that left Observed state outside the session."""
    import uuid
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    fid = str(uuid.uuid4())
    # A ready fact (EXTERNAL, passes truth_gate) stored directly as Observed.
    _ready_pending("Tritium has a half-life of 12 years", fid)

    session = review.create_session()
    assert fid in session["claim_ids"]

    # Approve outside session tracking — fact moves to Validated, not in reviewed_ids.
    review.approve(fid, actor="curator")

    # resume must skip the now-Validated fact (line 287-288 in review.py).
    result = review.resume_session(session["session_id"])
    ids = {item["fact_id"] for item in result["pending_items"]}
    assert fid not in ids
