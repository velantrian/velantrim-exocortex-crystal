import pytest

from core import audit
from core.curator_auth import CuratorLeaseRegistry, CuratorPrincipal, CuratorRole
from core.curator_runtime import (
    PrincipalConfigurationError,
    approve_as_principal,
    principal_from_environment,
    reject_as_principal,
    resolve_conflict_as_principal,
    synthetic_local_admin_principal,
)
from core.memory import get_fact, store_fact


def _principal(role=CuratorRole.CURATOR, scopes=frozenset({"fact:*"})):
    return CuratorPrincipal("alice", frozenset({role}), scopes)


def _pending(fid="runtime:pending"):
    store_fact({
        "fact_id": fid,
        "claim": "A pending claim",
        "source": "runtime-test",
        "confidence": 0.9,
        "epistemic_state": "Observed",
        "claim_type": "WORLD_FACT",
        "source_status": "EXTERNAL",
    })
    return fid


def test_environment_principal_is_explicit_and_fail_closed():
    with pytest.raises(PrincipalConfigurationError, match="ACTOR"):
        principal_from_environment({})
    with pytest.raises(PrincipalConfigurationError, match="ROLES"):
        principal_from_environment({"VELANTRIM_CURATOR_ACTOR": "alice"})
    with pytest.raises(PrincipalConfigurationError, match="unknown role"):
        principal_from_environment({
            "VELANTRIM_CURATOR_ACTOR": "alice",
            "VELANTRIM_CURATOR_ROLES": "GOD",
            "VELANTRIM_CURATOR_SCOPES": "fact:*",
        })
    principal = principal_from_environment({
        "VELANTRIM_CURATOR_ACTOR": " alice ",
        "VELANTRIM_CURATOR_ROLES": "REVIEWER,CURATOR",
        "VELANTRIM_CURATOR_SCOPES": "fact:new,fact:old",
    })
    assert principal.actor_id == "alice"
    assert principal.scopes == frozenset({"fact:new", "fact:old"})


def test_synthetic_local_admin_is_fixed_and_broad_only_by_explicit_contract():
    local = synthetic_local_admin_principal()
    assert local.actor_id == "api-curator"
    assert local.roles == frozenset({CuratorRole.ADMIN})
    assert local.scopes == frozenset({"fact:*"})


def test_local_admin_requires_explicit_caller_opt_in_and_empty_config():
    with pytest.raises(PrincipalConfigurationError):
        principal_from_environment({}, allow_explicit_local_admin=False)
    local = principal_from_environment({}, allow_explicit_local_admin=True)
    assert local == synthetic_local_admin_principal()

    partial_configurations = (
        {"VELANTRIM_CURATOR_ROLES": "ADMIN"},
        {"VELANTRIM_CURATOR_SCOPES": "fact:*"},
        {
            "VELANTRIM_CURATOR_ACTOR": "",
            "VELANTRIM_CURATOR_ROLES": "ADMIN",
            "VELANTRIM_CURATOR_SCOPES": "fact:*",
        },
    )
    for partial in partial_configurations:
        with pytest.raises(PrincipalConfigurationError, match="ACTOR"):
            principal_from_environment(
                partial,
                allow_explicit_local_admin=True,
            )


def test_actor_spoof_and_scope_denial_are_zero_mutation():
    fid = _pending("runtime:spoof")
    before = list(audit.audit_log())
    spoof = approve_as_principal(
        _principal(), fid, requested_actor="mallory"
    )
    assert spoof["authorized"] is False
    assert get_fact(fid)["epistemic_state"] == "Observed"
    assert audit.audit_log() == before

    scoped = _principal(scopes=frozenset({"fact:other"}))
    denied = reject_as_principal(scoped, fid, reason="noise")
    assert denied["authorized"] is False
    assert get_fact(fid)["epistemic_state"] == "Observed"
    assert audit.audit_log() == before


def test_force_approval_requires_admin_capability(monkeypatch):
    fid = _pending("runtime:force")
    monkeypatch.setattr(
        "core.curator_runtime.review.approve",
        lambda *args, **kwargs: {"found": True, "approved": True, "actor": kwargs["actor"]},
    )
    denied = approve_as_principal(
        _principal(CuratorRole.CURATOR),
        fid,
        force=True,
        reason="override",
    )
    assert denied["authorized"] is False
    allowed = approve_as_principal(
        _principal(CuratorRole.ADMIN),
        fid,
        force=True,
        reason="override",
    )
    assert allowed["authorized"] is True
    assert allowed["actor"] == "alice"


def test_approve_and_reject_normalize_fact_id_and_use_principal_actor(monkeypatch):
    seen = []
    monkeypatch.setattr(
        "core.curator_runtime.review.approve",
        lambda fact_id, **kwargs: seen.append(("approve", fact_id, kwargs)) or {"found": True},
    )
    monkeypatch.setattr(
        "core.curator_runtime.review.reject",
        lambda fact_id, **kwargs: seen.append(("reject", fact_id, kwargs)) or {"found": True},
    )
    principal = _principal()
    assert approve_as_principal(principal, " fact-1 ")["authorized"] is True
    assert reject_as_principal(principal, "\tfact-1\n")["authorized"] is True
    assert seen[0][1] == seen[1][1] == "fact-1"
    assert seen[0][2]["actor"] == seen[1][2]["actor"] == "alice"


def test_conflict_capability_target_scope_and_lease_fail_closed(monkeypatch):
    report = {"report_id": "report-1"}
    monkeypatch.setattr(
        "core.curator_runtime.review.review_item",
        lambda _fid: {"found": True, "diagnosis": {"contradiction_report": report}},
    )
    calls = []
    monkeypatch.setattr(
        "core.curator_runtime.review.resolve_conflict",
        lambda *args, **kwargs: calls.append((args, kwargs)) or {"found": True, "approved": True},
    )

    reviewer = _principal(CuratorRole.REVIEWER)
    denied = resolve_conflict_as_principal(
        reviewer,
        "new",
        disposition="SUPERSEDE",
        reason="new source",
        target_fact_ids=("old",),
    )
    assert denied["authorized"] is False
    assert not calls

    scoped = _principal(scopes=frozenset({"fact:new"}))
    denied_scope = resolve_conflict_as_principal(
        scoped,
        "new",
        disposition="SUPERSEDE",
        reason="new source",
        target_fact_ids=("old",),
    )
    assert denied_scope["authorized"] is False
    assert not calls

    registry = CuratorLeaseRegistry()
    held = registry.acquire(
        candidate_fact_id="new", report_id="report-1", owner="other"
    )
    assert held is not None
    busy = resolve_conflict_as_principal(
        _principal(),
        "new",
        disposition="COEXIST",
        reason="contexts",
        lease_registry=registry,
    )
    assert busy["reason"] == "CURATOR_DECISION_LEASE_BUSY"
    assert not calls


def test_conflict_report_is_pinned_ids_normalized_and_lease_released(monkeypatch):
    report = {"report_id": "report-1"}
    monkeypatch.setattr(
        "core.curator_runtime.review.review_item",
        lambda _fid: {"found": True, "diagnosis": {"contradiction_report": report}},
    )
    seen = {}

    def resolve(fact_id, **kwargs):
        seen.update({"fact_id": fact_id, **kwargs})
        return {"found": True, "approved": True}

    monkeypatch.setattr("core.curator_runtime.review.resolve_conflict", resolve)
    registry = CuratorLeaseRegistry()
    result = resolve_conflict_as_principal(
        _principal(),
        " new ",
        disposition="SUPERSEDE",
        requested_actor="alice",
        reason="new source",
        target_fact_ids=(" old ",),
        expected_report_id="report-1",
        lease_registry=registry,
    )
    assert result["authorized"] is True and result["approved"] is True
    assert seen["fact_id"] == "new"
    assert seen["target_fact_ids"] == ("old",)
    assert seen["actor"] == "alice"
    assert seen["expected_report_id"] == "report-1"
    assert not registry.is_active(candidate_fact_id="new", report_id="report-1")


def test_conflict_stale_or_absent_report_never_mutates(monkeypatch):
    monkeypatch.setattr(
        "core.curator_runtime.review.review_item",
        lambda _fid: {"found": True, "diagnosis": {"contradiction_report": {"report_id": "new"}}},
    )
    monkeypatch.setattr(
        "core.curator_runtime.review.resolve_conflict",
        lambda *args, **kwargs: pytest.fail("must not mutate"),
    )
    stale = resolve_conflict_as_principal(
        _principal(), "fact", disposition="COEXIST", reason="why",
        expected_report_id="old",
    )
    assert stale["reason"] == "CONTRADICTION_REPORT_CHANGED"

    monkeypatch.setattr(
        "core.curator_runtime.review.review_item",
        lambda _fid: {"found": True, "diagnosis": {}},
    )
    absent = resolve_conflict_as_principal(
        _principal(), "fact", disposition="COEXIST", reason="why"
    )
    assert absent["reason"] == "NO_CURRENT_CONTRADICTION"
