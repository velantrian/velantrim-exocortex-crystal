"""Tests for the curator review queue (core/review.py, grant WP2).

The queue is the set of Observed facts: stored in L1 but never promoted to the
canon. A fact blocked by the gates stays Observed; a fact that passes is
Validated. Curator approve/reject decisions are accountable (audit chain).
"""
import pytest

from core import review, audit
from core.compliance import restrict_processing
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


def test_pending_redacts_restricted_facts(monkeypatch):
    """GDPR Art. 18: a restricted fact sitting in the review queue must not
    surface its claim/source/confidence — only a redacted stub, even though
    it is technically still Observed/pending."""
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    restricted_fid = _blocked_world_fact("A restricted pending claim")
    open_fid = _blocked_world_fact("An ordinary pending claim")
    restrict_processing(restricted_fid, reason="dispute")

    items = {i["fact_id"]: i for i in review.pending()}
    restricted_item = items[restricted_fid]
    assert restricted_item == {
        "fact_id": restricted_fid, "restricted": True, "reason": "RESTRICTED_BY_POLICY"}
    assert "A restricted pending claim" not in str(restricted_item)

    open_item = items[open_fid]
    assert open_item["claim"] == "An ordinary pending claim"


def test_pending_claim_type_filter_omits_restricted_fact_even_when_type_matches(monkeypatch):
    """GDPR Art. 18: an explicit claim_type filter must not reveal a restricted
    fact's real claim_type via its mere presence — a restricted WORLD_FACT
    must be entirely absent from pending(claim_type="WORLD_FACT"), even though
    it DOES appear (redacted) in the unfiltered pending()."""
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    restricted_fid = _blocked_world_fact("A restricted world fact, typed query")
    open_fid = _blocked_world_fact("An ordinary world fact, typed query")
    restrict_processing(restricted_fid, reason="dispute")

    unfiltered_ids = {i["fact_id"] for i in review.pending()}
    assert restricted_fid in unfiltered_ids       # present, redacted, unfiltered

    typed_ids = {i["fact_id"] for i in review.pending(claim_type="WORLD_FACT")}
    assert restricted_fid not in typed_ids        # absent from the typed query
    assert open_fid in typed_ids                  # unrestricted typed filtering intact


def test_pending_claim_type_filter_omits_restricted_fact_of_different_type(monkeypatch):
    """A restricted fact must not appear in a typed query even for a
    claim_type OTHER than its real one — its absence there must not become a
    positive signal either (it's simply never included in any typed query)."""
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    restricted_fid = _blocked_world_fact("A restricted world fact, wrong-type query")
    restrict_processing(restricted_fid, reason="dispute")

    assert review.pending(claim_type="EMOTION") == []
    assert restricted_fid not in {i["fact_id"] for i in review.pending(claim_type="WORLD_FACT")}


def test_pending_diagnose_claim_type_filter_omits_restricted_facts(monkeypatch):
    """The claim_type-omission behavior applies identically to the
    diagnose=True variant used by the Kanban UI."""
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    restricted_fid = _blocked_world_fact("A restricted world fact, diagnosed typed query")
    open_fid = _ready_pending("Argon is a noble gas", "ing:ready08")
    restrict_processing(restricted_fid, reason="dispute")

    typed_ids = {i["fact_id"] for i in review.pending(claim_type="WORLD_FACT", diagnose=True)}
    assert restricted_fid not in typed_ids
    assert open_fid in typed_ids


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


def test_review_item_redacts_restricted_fact(monkeypatch):
    """GDPR Art. 18: review_item() must not expose claim/source, and must not
    run the live diagnosis (immune/Guardian/TruthGate/find_conflicts) against
    a restricted fact's claim just to produce a verdict."""
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    fid = _blocked_world_fact("A restricted claim under review")
    restrict_processing(fid, reason="dispute")

    def _boom(*args, **kwargs):
        raise AssertionError("_diagnose must not run for a restricted fact")
    monkeypatch.setattr(review, "_diagnose", _boom)

    item = review.review_item(fid)
    assert item["found"] is True
    assert item["restricted"] is True
    assert item["reason"] == "RESTRICTED_BY_POLICY"
    assert item["diagnosis"] == {"verdict": "restricted", "reason": "RESTRICTED_BY_POLICY"}
    assert "claim" not in item and "source" not in item and "confidence" not in item
    assert "A restricted claim under review" not in str(item)


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


def test_approve_aborts_on_cas_miss_without_l3_merge(monkeypatch):
    """Defense-in-depth: if a competing reviewer changes the persisted state after
    the queue read, approve() hits a CAS miss in transition_esm, aborts, and never
    merges into the canon. This is not a full thread/process atomicity guarantee.
    """
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    from core.memory import _db
    fid = _ready_pending("A concurrently collapsed world claim", "cas:rev1")
    get_fact(fid)  # prime L0 with the "Observed" record the curator sees

    # A competing reviewer collapses the row directly in the DB; L0 stays stale.
    with _db() as conn:
        conn.execute("UPDATE facts SET epistemic_state = ? WHERE fact_id = ?",
                     ("Collapsed", fid))

    res = review.approve(fid, actor="alice")
    assert res["approved"] is False
    assert "CAS conflict" in res["reason"]
    # The concurrently-collapsed fact was never resurrected into the canon.
    assert get_l3_graph().get_fact(fid) is None
    # The persisted state stays Collapsed (the attempted Validated did not win).
    assert get_fact(fid)["epistemic_state"] == "Collapsed"


def test_approve_refuses_restricted_fact(monkeypatch):
    """GDPR Art. 18: a restricted fact must not be actionable from approve() —
    not diagnosed, not transitioned, not merged into L3, no success audit."""
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    fid = _ready_pending("A restricted claim awaiting approval", "ing:restricted-appr1")
    restrict_processing(fid, reason="dispute")

    def _boom(*args, **kwargs):
        raise AssertionError("_diagnose must not run for a restricted fact")
    monkeypatch.setattr(review, "_diagnose", _boom)

    events_before = len(audit.audit_log())
    res = review.approve(fid, actor="alice")

    assert res == {"found": True, "fact_id": fid, "approved": False,
                    "restricted": True, "reason": "RESTRICTED_BY_POLICY"}
    assert get_fact(fid)["epistemic_state"] == "Observed"   # never transitioned
    assert get_l3_graph().get_fact(fid) is None              # never merged
    assert len(audit.audit_log()) == events_before           # no success event


def test_approve_force_true_also_refuses_restricted_fact(monkeypatch):
    """Force approval must not override GDPR Art. 18 restriction — the correct
    path is to lift the restriction first (compliance.unrestrict_processing),
    not to force-approve through it."""
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    fid = _blocked_world_fact("A restricted claim a curator tries to force")
    restrict_processing(fid, reason="dispute")

    def _boom(*args, **kwargs):
        raise AssertionError("_diagnose must not run for a restricted fact")
    monkeypatch.setattr(review, "_diagnose", _boom)

    events_before = len(audit.audit_log())
    res = review.approve(fid, actor="bob", force=True, reason="vetted anyway")

    assert res["approved"] is False
    assert res["restricted"] is True
    assert res["reason"] == "RESTRICTED_BY_POLICY"
    assert get_fact(fid)["epistemic_state"] == "Observed"
    assert get_l3_graph().get_fact(fid) is None
    assert len(audit.audit_log()) == events_before


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


def test_force_without_reason_or_actor_is_refused(monkeypatch):
    """Negative test: force approval is a trust-boundary override — without a
    non-empty reason AND an explicit actor (no default identity for an
    override) nothing moves and nothing is audited."""
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    fid = _blocked_world_fact("A blocked claim without a justification")
    for kwargs in ({"force": True},                      # no reason at all
                   {"force": True, "reason": "  "},      # blank reason
                   {"force": True, "reason": "ok"},      # no explicit actor
                   {"force": True, "reason": "ok", "actor": ""},   # empty actor
                   {"force": True, "reason": "ok", "actor": " "}):  # blank actor
        res = review.approve(fid, **kwargs)
        assert res["approved"] is False
        assert "reason" in res["reason"] or "actor" in res["reason"]
    assert get_fact(fid)["epistemic_state"] == "Observed"
    assert all(e["event"] != "review_force_approve" for e in audit.audit_log())


def test_force_reason_over_500_chars_is_refused(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    fid = _blocked_world_fact("A blocked claim with an essay for a reason")
    res = review.approve(fid, actor="bob", force=True, reason="x" * 501)
    assert res["approved"] is False
    assert "500" in res["reason"]
    assert get_fact(fid)["epistemic_state"] == "Observed"
    # Boundary: exactly 500 characters is still a valid reason.
    res = review.approve(fid, actor="bob", force=True, reason="x" * 500)
    assert res["approved"] is True


def test_non_force_approve_keeps_default_actor(monkeypatch):
    """Backward compatibility: a normal approve without an actor is still
    audited under the historical default identity 'curator'."""
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    fid = _ready_pending("Krypton is a noble gas", "ing:ready-default-actor")
    res = review.approve(fid)
    assert res["approved"] is True
    entry = [e for e in audit.audit_log() if e["event"] == "review_approve"][-1]
    assert entry["detail"]["actor"] == "curator"


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


def test_force_approve_retries_on_cas_miss_for_override_metadata(monkeypatch):
    """Regression for a Codex P1 finding (#244): the override-metadata
    update_fact() call ignored its boolean return, so a CAS miss could
    silently drop the override/gate_passed/gate_reason markers even though
    the force-approval itself (transition_esm + audit) went through. It must
    retry against fresh state instead."""
    claim = "A force-approved claim under a CAS race"
    fid = _blocked_world_fact(claim)

    real_update_fact = review.update_fact
    calls = {"n": 0}

    def flaky_update_fact(*args, **kwargs):
        calls["n"] += 1
        if calls["n"] == 1:
            return False  # simulate one lost CAS race
        return real_update_fact(*args, **kwargs)

    monkeypatch.setattr(review, "update_fact", flaky_update_fact)

    result = review.approve(fid, actor="bob", force=True, reason="manual vetting")
    assert result["approved"] is True
    meta = get_fact(fid)["metadata"]
    assert meta["override"] is True
    assert meta["admission_path"] == "review_force_approve"
    assert calls["n"] == 2  # first attempt lost the race, second succeeded


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


def test_reject_aborts_on_cas_miss(monkeypatch):
    """If transition_esm reports a CAS miss, reject() aborts: rejected False and no
    reject-success audit event. Defense-in-depth, not full atomicity."""
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    fid = _blocked_world_fact("A concurrently changed pending claim")
    before = len([e for e in audit.audit_log() if e["event"] == "review_reject"])
    monkeypatch.setattr(review, "transition_esm", lambda *a, **k: False)
    res = review.reject(fid, actor="dave")
    assert res["rejected"] is False
    assert "CAS conflict" in res["reason"]
    after = len([e for e in audit.audit_log() if e["event"] == "review_reject"])
    assert after == before  # no reject-success audit event was recorded


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


def test_cli_force_without_explicit_actor_is_refused(monkeypatch, capsys):
    """--force without an explicit --actor must not promote: the CLI no longer
    supplies a default identity that could sign an override."""
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    from core.cli import main
    fid = _blocked_world_fact("A CLI override missing its actor")
    assert main(["review-approve", fid, "--force", "--reason", "vetted"]) == 0
    out = capsys.readouterr().out
    assert '"approved": false' in out and "actor" in out
    assert get_fact(fid)["epistemic_state"] == "Observed"


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


def test_decisions_redact_claim_for_restricted_facts(monkeypatch):
    """GDPR Art. 18: a fact that was approved and later restricted must have
    claim=None in its decision-history entry (like the erased case), plus a
    distinct restricted marker — while an unrestricted entry in the same
    history is untouched. `restricted_reason` (not `reason`) carries the
    marker, since `reason` already holds the curator's own decision reason."""
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    restricted_fid = _blocked_world_fact("A claim approved then restricted")
    open_fid = _blocked_world_fact("A claim approved and left alone")
    review.approve(restricted_fid, actor="dave", force=True, reason="vetted")
    review.approve(open_fid, actor="dave", force=True, reason="vetted")
    restrict_processing(restricted_fid, reason="dispute")

    history = {d["fact_id"]: d for d in review.decisions()}
    restricted_entry = history[restricted_fid]
    assert restricted_entry["claim"] is None
    assert restricted_entry["claim_type"] is None
    assert restricted_entry["restricted"] is True
    assert restricted_entry["restricted_reason"] == "RESTRICTED_BY_POLICY"
    assert restricted_entry["reason"] == "vetted"          # curator's own reason, untouched
    assert "A claim approved then restricted" not in str(restricted_entry)

    open_entry = history[open_fid]
    assert open_entry["claim"] == "A claim approved and left alone"
    assert "restricted" not in open_entry


def test_decisions_without_claim_stay_content_free(monkeypatch):
    """include_claim=False must not rehydrate memory content from L1: the
    entries carry decision metadata only — no claim text, no claim_type."""
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    claim = "A privacy-sensitive claim text"
    fid = _blocked_world_fact(claim)
    review.approve(fid, actor="carol", force=True, reason="vetted offline")
    entry = [d for d in review.decisions(include_claim=False)
             if d["fact_id"] == fid][0]
    assert "claim" not in entry and "claim_type" not in entry
    assert claim not in str(entry)
    assert entry["actor"] == "carol"


def test_pending_diagnose_attaches_verdicts(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    _ready_pending("Xenon is a noble gas", "ing:ready05")
    _blocked_world_fact("A blocked claim for the kanban")
    items = review.pending(diagnose=True)
    verdicts = {i["fact_id"]: i["diagnosis"]["verdict"] for i in items}
    assert "ready" in verdicts.values()
    assert "blocked" in verdicts.values()
    assert all("diagnosis" not in i for i in review.pending())   # opt-in only


def test_pending_diagnose_does_not_run_live_gates_on_restricted_facts(monkeypatch):
    """GDPR Art. 18: pending(diagnose=True) must not pass a restricted fact's
    claim through immune/Guardian/TruthGate/find_conflicts just to produce a
    diagnosis — it must short-circuit to a restricted verdict instead. An
    unrestricted item in the same batch must still get a real diagnosis."""
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    restricted_fid = _blocked_world_fact("A restricted claim for the kanban")
    open_fid = _ready_pending("Neon is a noble gas", "ing:ready07")
    restrict_processing(restricted_fid, reason="dispute")

    original_diagnose = review._diagnose
    diagnosed_ids = []

    def _tracking_diagnose(fact):
        diagnosed_ids.append(fact["fact_id"])
        return original_diagnose(fact)
    monkeypatch.setattr(review, "_diagnose", _tracking_diagnose)

    items = {i["fact_id"]: i for i in review.pending(diagnose=True)}

    assert restricted_fid not in diagnosed_ids   # never passed through the live gates
    assert open_fid in diagnosed_ids             # the real gate did run for this one

    restricted_item = items[restricted_fid]
    assert restricted_item["restricted"] is True
    assert restricted_item["diagnosis"] == {"verdict": "restricted", "reason": "RESTRICTED_BY_POLICY"}
    assert "claim" not in restricted_item

    assert items[open_fid]["diagnosis"]["verdict"] == "ready"


def test_cli_review_decisions(monkeypatch, capsys):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    from core.cli import main
    fid = _ready_pending("Radon is a noble gas", "ing:ready06")
    review.approve(fid, actor="cli-test")
    assert main(["review-decisions", "--limit", "5"]) == 0
    out = capsys.readouterr().out
    assert "cli-test" in out and fid in out
