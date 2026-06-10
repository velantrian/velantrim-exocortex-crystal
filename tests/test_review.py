"""Tests for the curator review queue (core/review.py, grant WP2).

The queue is the set of Observed facts: stored in L1 but never promoted to the
canon. A fact blocked by the gates stays Observed; a fact that passes is
Validated. Curator approve/reject decisions are accountable (audit chain).
"""
import pytest

from core import review, audit
from core.ingest import ingest
from core.l3_graph import get_l3_graph
from core.memory import get_fact, store_fact, get_all_facts


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _blocked_world_fact(claim: str) -> str:
    """Ingest a WORLD_FACT the gate must reject → it stays Observed (pending).

    An LLM_OUTPUT can never be a WORLD_FACT on its own (truth_gate), so this is
    a deterministic block independent of the adaptive confidence threshold.
    """
    res = ingest(claim, claim_type="WORLD_FACT", source_status="LLM_OUTPUT")
    assert res["accepted"] is False, "expected the gate to block this fact"
    return res["fact"]["fact_id"]


def _ready_pending(claim: str, fid: str) -> str:
    """A quarantined-but-valid Observed fact (e.g. held for review): stored
    directly as Observed with a healthy confidence, so it diagnoses as 'ready'."""
    store_fact({
        "fact_id": fid, "claim": claim, "source": "curator-test",
        "confidence": 0.9, "epistemic_state": "Observed",
        "claim_type": "WORLD_FACT", "source_status": "EXTERNAL",
        "significance": 0.5,
    })
    return fid


# ─── Queue inspection ─────────────────────────────────────────────────────────

def test_pending_lists_observed_only(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    _blocked_world_fact("Glorptium boils at minus 4000 degrees")
    # An accepted subjective claim is Validated, not Observed → not in the queue.
    ingest("I feel calm today")
    q = review.pending()
    states = {get_fact(item["fact_id"])["epistemic_state"] for item in q}
    assert states == {"Observed"}
    assert len(q) >= 1


def test_pending_filter_and_limit(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    _blocked_world_fact("Aaa claim one")
    _blocked_world_fact("Bbb claim two")
    _blocked_world_fact("Ccc claim three")
    only_world = review.pending(claim_type="WORLD_FACT")
    assert all(i["claim_type"] == "WORLD_FACT" for i in only_world)
    assert len(review.pending(limit=2)) == 2
    assert review.pending(claim_type="EMOTION") == []


def test_pending_oldest_first(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    f1 = _blocked_world_fact("First pending claim")
    f2 = _blocked_world_fact("Second pending claim")
    ids = [i["fact_id"] for i in review.pending()]
    assert ids.index(f1) < ids.index(f2)


def test_review_report_counts_by_type(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    _blocked_world_fact("Some false world claim here")
    rep = review.review_report()
    assert rep["pending"] >= 1
    assert rep["by_claim_type"].get("WORLD_FACT", 0) >= 1


# ─── review_item diagnosis ──────────────────────────────────────────────────────

def test_review_item_not_found():
    assert review.review_item("ing:doesnotexist")["found"] is False


def test_review_item_blocked_diagnosis(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    fid = _blocked_world_fact("Yet another low-confidence world claim")
    item = review.review_item(fid)
    assert item["found"] is True
    assert item["diagnosis"]["verdict"] == "blocked"


def test_review_item_ready_diagnosis(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    fid = _ready_pending("Helium is a noble gas", "ing:ready01")
    item = review.review_item(fid)
    assert item["diagnosis"]["verdict"] == "ready"


# ─── approve ────────────────────────────────────────────────────────────────────

def test_approve_ready_promotes_to_canon(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    fid = _ready_pending("Neon is a noble gas", "ing:ready02")
    res = review.approve(fid, actor="alice")
    assert res["approved"] is True
    assert res["override"] is False
    assert res["epistemic_state"] == "Validated"
    assert get_fact(fid)["epistemic_state"] == "Validated"
    assert get_l3_graph().get_fact(fid) is not None  # reached the canon


def test_approve_blocked_without_force_refuses(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    fid = _blocked_world_fact("A blocked claim awaiting review")
    res = review.approve(fid)
    assert res["approved"] is False
    assert res["diagnosis"]["verdict"] == "blocked"
    # Still Observed, still not in the canon.
    assert get_fact(fid)["epistemic_state"] == "Observed"
    assert get_l3_graph().get_fact(fid) is None


def test_approve_blocked_with_force_and_reason_overrides(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    fid = _blocked_world_fact("A blocked claim a curator insists on")
    res = review.approve(fid, actor="bob", note="vetted manually", force=True,
                         reason="verified against the printed source")
    assert res["approved"] is True
    assert res["override"] is True
    assert get_fact(fid)["epistemic_state"] == "Validated"
    assert get_l3_graph().get_fact(fid) is not None


def test_force_without_reason_is_refused(monkeypatch):
    """Negative test: force approval is a trust-boundary override — without a
    non-empty reason (or actor) nothing moves and nothing is audited."""
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    fid = _blocked_world_fact("A blocked claim without a justification")
    for kwargs in ({"force": True},                      # no reason at all
                   {"force": True, "reason": "  "},      # blank reason
                   {"force": True, "reason": "ok", "actor": ""}):  # no actor
        res = review.approve(fid, **kwargs)
        assert res["approved"] is False
        assert "reason" in res["reason"]
    assert get_fact(fid)["epistemic_state"] == "Observed"
    assert all(e["event"] != "review_force_approve" for e in audit.audit_log())


def test_force_approve_audited_distinctly_and_content_free(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    claim = "A very distinctive blocked claim text"
    fid = _blocked_world_fact(claim)
    review.approve(fid, actor="bob", force=True, reason="manual vetting")
    events = [e for e in audit.audit_log()
              if e["event"] == "review_force_approve"]
    assert len(events) == 1
    detail = events[0]["detail"]
    assert detail["actor"] == "bob"
    assert detail["reason"] == "manual vetting"
    # Content-free: decision metadata only — the claim text is not duplicated.
    assert claim not in str(detail)
    assert audit.verify_audit_log()["ok"] is True


def test_approve_not_found():
    assert review.approve("ing:nope")["found"] is False


def test_approve_non_pending_is_noop(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    res = ingest("Water boils at 100 degrees Celsius at sea level")
    fid = res["fact"]["fact_id"]
    assert get_fact(fid)["epistemic_state"] == "Validated"
    out = review.approve(fid)
    assert out["approved"] is False
    assert "not pending" in out["reason"]


# ─── reject ──────────────────────────────────────────────────────────────────

def test_reject_collapses_pending(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    fid = _blocked_world_fact("A claim the curator throws out")
    res = review.reject(fid, actor="carol", reason="off-topic")
    assert res["rejected"] is True
    assert res["epistemic_state"] == "Collapsed"
    assert get_fact(fid)["epistemic_state"] == "Collapsed"
    # No longer in the pending queue.
    assert fid not in [i["fact_id"] for i in review.pending()]


def test_reject_not_found():
    assert review.reject("ing:nope")["found"] is False


def test_reject_non_pending_is_noop(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    fid = ingest("Tokyo is the capital of Japan")["fact"]["fact_id"]
    out = review.reject(fid)
    assert out["rejected"] is False
    assert "not pending" in out["reason"]


# ─── Accountability: audit chain stays intact ──────────────────────────────────

def test_decisions_are_audited(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    approved = _ready_pending("Argon is a noble gas", "ing:ready03")
    rejected = _blocked_world_fact("A rejected pending claim")
    review.approve(approved, actor="dave")
    review.reject(rejected, actor="dave")
    events = {e["event"] for e in audit.audit_log()}
    assert {"review_approve", "review_reject"} <= events
    assert audit.verify_audit_log()["ok"] is True


# ─── CLI ────────────────────────────────────────────────────────────────────────

def test_cli_review_flow(monkeypatch, capsys):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    from core.cli import main
    fid = _blocked_world_fact("A CLI-reviewed pending claim")

    assert main(["review-queue"]) == 0
    assert fid in capsys.readouterr().out

    assert main(["review-report"]) == 0
    assert "pending" in capsys.readouterr().out

    assert main(["review-item", fid]) == 0
    assert "diagnosis" in capsys.readouterr().out

    assert main(["review-approve", fid, "--force", "--actor", "cli"]) == 0
    assert '"approved": false' in capsys.readouterr().out   # force needs --reason

    assert main(["review-approve", fid, "--force", "--actor", "cli",
                 "--reason", "vetted"]) == 0
    assert '"approved": true' in capsys.readouterr().out
    assert get_fact(fid)["epistemic_state"] == "Validated"


def test_cli_review_reject(monkeypatch, capsys):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    from core.cli import main
    fid = _blocked_world_fact("A CLI-rejected pending claim")
    assert main(["review-reject", fid, "--reason", "spam"]) == 0
    assert '"rejected": true' in capsys.readouterr().out
    assert get_fact(fid)["epistemic_state"] == "Collapsed"


# ─── Decisions history + diagnose listing ──────────────────────────────────────

def test_decisions_history_from_audit_chain(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    ok_id = _ready_pending("Krypton is a noble gas", "ing:ready04")
    bad_id = _blocked_world_fact("A claim destined for rejection")
    forced = _blocked_world_fact("A claim promoted by override")
    review.approve(ok_id, actor="alice")
    review.reject(bad_id, actor="bob", reason="off-topic")
    review.approve(forced, actor="carol", force=True, reason="vetted offline")
    history = review.decisions()
    kinds = [d["decision"] for d in history[:3]]
    assert kinds == ["force_approved", "rejected", "approved"]  # newest first
    forced_entry = history[0]
    assert forced_entry["actor"] == "carol"
    assert forced_entry["reason"] == "vetted offline"
    assert forced_entry["claim"] == "A claim promoted by override"
    assert review.decisions(limit=1) == [forced_entry]


def test_decisions_survive_fact_erasure(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    from core.erasure import erase_fact
    fid = _blocked_world_fact("A rejected then erased claim")
    review.reject(fid, actor="dave")
    erase_fact(fid, reason="gdpr_request")
    entry = [d for d in review.decisions() if d["fact_id"] == fid][0]
    assert entry["decision"] == "rejected"
    assert entry["claim"] is None            # content gone, decision record stays


def test_pending_diagnose_attaches_verdicts(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    _ready_pending("Xenon is a noble gas", "ing:ready05")
    _blocked_world_fact("A blocked claim for the kanban")
    items = review.pending(diagnose=True)
    verdicts = {i["fact_id"]: i["diagnosis"]["verdict"] for i in items}
    assert "ready" in verdicts.values()
    assert "blocked" in verdicts.values()
    assert all("diagnosis" not in i for i in review.pending())   # opt-in only


def test_cli_review_decisions(monkeypatch, capsys):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    from core.cli import main
    fid = _ready_pending("Radon is a noble gas", "ing:ready06")
    review.approve(fid, actor="cli-test")
    assert main(["review-decisions", "--limit", "5"]) == 0
    out = capsys.readouterr().out
    assert "cli-test" in out and fid in out
