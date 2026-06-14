"""Tests for Force Override Audit Pinning (core/review.py, PR5 — grant WP2).

Force approval is a trust-boundary operation: a curator explicitly overrides
a blocking gate diagnosis. It must be:
  - rejected without an explicit actor
  - rejected without a non-empty reason
  - audited under its own event type (review_force_approve)
  - metric-counted (review.override)
  - visibly warned at runtime (RuntimeWarning)
  - never silent

Normal approve must NOT emit the force-override warning.
No claim text must appear in the warning or audit metadata.
"""
import warnings

import pytest

from core import review, audit as _audit, metrics as _metrics
from core.ingest import ingest


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _blocked_fact(claim: str) -> str:
    """Ingest a WORLD_FACT the gate blocks → stays Observed (pending)."""
    res = ingest(claim, claim_type="WORLD_FACT", source_status="LLM_OUTPUT")
    assert res["accepted"] is False
    return res["fact"]["fact_id"]


# ─── Rejection guards ─────────────────────────────────────────────────────────

def test_force_approve_without_actor_is_rejected(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    fid = _blocked_fact("Xyrtonite defies all thermodynamic laws")
    res = review.approve(fid, force=True, reason="testing override", actor="")
    assert res["approved"] is False
    assert "actor" in res["reason"].lower() or "force" in res["reason"].lower()


def test_force_approve_without_reason_is_rejected(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    fid = _blocked_fact("Quortium emits negative energy at standard conditions")
    res = review.approve(fid, force=True, reason="", actor="admin")
    assert res["approved"] is False
    assert "reason" in res["reason"].lower() or "force" in res["reason"].lower()


def test_force_approve_without_actor_and_reason_is_rejected(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    fid = _blocked_fact("Nullium exists outside spacetime")
    res = review.approve(fid, force=True, reason=None, actor=None)
    assert res["approved"] is False


def test_force_approve_reason_too_long_is_rejected(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    fid = _blocked_fact("Velantrium violates conservation of energy")
    long_reason = "x" * 501
    res = review.approve(fid, force=True, reason=long_reason, actor="admin")
    assert res["approved"] is False
    assert "500" in res["reason"] or "exceeds" in res["reason"]


# ─── RuntimeWarning emitted ───────────────────────────────────────────────────

def test_force_approve_emits_runtime_warning(monkeypatch):
    """Valid force approval must emit a RuntimeWarning."""
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    fid = _blocked_fact("Aetherium conducts cold fire")
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        res = review.approve(fid, force=True, reason="exception for demo",
                             actor="admin-curator")
    assert res["approved"] is True
    runtime_warnings = [w for w in caught if issubclass(w.category, RuntimeWarning)]
    assert len(runtime_warnings) == 1


def test_force_approve_warning_contains_fact_id_and_actor(monkeypatch):
    """Warning message must reference fact_id and actor (content-free metadata)."""
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    fid = _blocked_fact("Phlogiston is real and measurable")
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        review.approve(fid, force=True, reason="grant demo override",
                       actor="grant-admin")
    runtime_warnings = [w for w in caught if issubclass(w.category, RuntimeWarning)]
    assert len(runtime_warnings) == 1
    msg = str(runtime_warnings[0].message)
    assert fid in msg
    assert "grant-admin" in msg


def test_force_approve_warning_does_not_contain_claim_text(monkeypatch):
    """Warning must be content-free — claim text must NOT appear in the message."""
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    claim = "Secretum-X boils at absolute zero under pressure"
    fid = _blocked_fact(claim)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        review.approve(fid, force=True, reason="content-free test",
                       actor="security-admin")
    runtime_warnings = [w for w in caught if issubclass(w.category, RuntimeWarning)]
    assert len(runtime_warnings) == 1
    msg = str(runtime_warnings[0].message)
    assert claim not in msg


# ─── Normal approve — no warning ─────────────────────────────────────────────

def test_normal_approve_does_not_emit_force_warning(monkeypatch):
    """A normal (non-force) approve of a ready fact must NOT emit RuntimeWarning."""
    from core.memory import store_fact
    import uuid
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    fid = str(uuid.uuid4())
    store_fact({
        "fact_id": fid, "claim": "Platinum is a precious metal",
        "source": "test", "confidence": 0.9,
        "epistemic_state": "Observed", "claim_type": "WORLD_FACT",
        "source_status": "EXTERNAL", "significance": 0.5,
    })
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        res = review.approve(fid, actor="curator")
    assert res["approved"] is True
    runtime_warnings = [w for w in caught if issubclass(w.category, RuntimeWarning)]
    assert len(runtime_warnings) == 0


# ─── Audit chain ─────────────────────────────────────────────────────────────

def test_force_approve_writes_force_approve_audit_event(monkeypatch):
    """Force approve must be recorded as review_force_approve in the audit chain."""
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    fid = _blocked_fact("Omega-prime particle has negative mass")
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        review.approve(fid, force=True, reason="audit pinning test",
                       actor="test-curator")
    log = _audit.audit_log()
    force_events = [e for e in log
                    if e["event"] == "review_force_approve"
                    and e["fact_id"] == fid]
    assert len(force_events) == 1
    detail = force_events[0]["detail"]
    assert detail["actor"] == "test-curator"
    assert detail["reason"] == "audit pinning test"


def test_force_approve_audit_event_is_content_free(monkeypatch):
    """The audit chain entry must not contain the claim text."""
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    claim = "Vortexium-99 reverses entropy locally"
    fid = _blocked_fact(claim)
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        review.approve(fid, force=True, reason="content-free audit check",
                       actor="auditor")
    log = _audit.audit_log()
    for entry in log:
        if entry["event"] == "review_force_approve" and entry["fact_id"] == fid:
            assert claim not in str(entry["detail"])


# ─── Metric ──────────────────────────────────────────────────────────────────

def test_force_approve_increments_override_metric(monkeypatch):
    """review.override metric must increment on a successful force approval."""
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    fid = _blocked_fact("Zeta-particle oscillates faster than light")
    before = _metrics.value("review.override")
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        review.approve(fid, force=True, reason="metric increment test",
                       actor="metric-curator")
    after = _metrics.value("review.override")
    assert after == before + 1


# ─── PYTHONWARNINGS=error safety (Codex P2 fix) ──────────────────────────────

def test_force_approve_esm_and_audit_survive_warnings_as_errors(monkeypatch):
    """ESM transition and audit append must complete BEFORE the warning is emitted.

    When RuntimeWarning is treated as an error (PYTHONWARNINGS=error), the warning
    raises inside the caller's frame.  The fix emits the warning as the LAST action
    in approve(), after transition_esm() and audit.append_event() have already
    committed.  So even if the warning is re-raised by the caller, the fact is
    already Validated and the audit record already exists.

    Regression: the warning was previously emitted BEFORE the ESM transition and
    audit append, so raising would leave the fact in Observed with no audit record.
    """
    from core.memory import get_fact
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    fid = _blocked_fact("Thermium ignites at absolute zero under no pressure")

    # Simulate PYTHONWARNINGS=error: catch the RuntimeWarning as an exception.
    # The fact MUST be Validated and the audit record MUST exist even though
    # the warning raised — because the warning is emitted last.
    with warnings.catch_warnings():
        warnings.simplefilter("error", RuntimeWarning)
        try:
            review.approve(fid, force=True, reason="pythonwarnings-error test",
                           actor="safety-admin")
        except RuntimeWarning:
            # The warning raised — but transition_esm + audit should have run first.
            pass
        else:
            # The warning did NOT raise (e.g. if it was suppressed elsewhere).
            pass

    # Regardless of whether the warning raised, the ESM transition and audit
    # must have completed because they now happen BEFORE warnings.warn().
    assert get_fact(fid)["epistemic_state"] == "Validated", (
        "Fact must be Validated even when RuntimeWarning is treated as an error; "
        "the warning should be emitted AFTER transition_esm()."
    )
    log = _audit.audit_log()
    force_events = [e for e in log
                    if e["event"] == "review_force_approve"
                    and e["fact_id"] == fid]
    assert len(force_events) == 1, (
        "Audit record must exist even when RuntimeWarning is treated as an error; "
        "audit.append_event() should run BEFORE warnings.warn()."
    )
