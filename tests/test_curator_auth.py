import pytest

from core.contradiction_report import ConflictDisposition
from core.curator_auth import (
    CuratorCapability,
    CuratorLeaseRegistry,
    CuratorPrincipal,
    CuratorRole,
    DecisionLease,
    authorize_conflict_decision,
)


def principal(role, *, scopes=frozenset({"fact:*"})):
    return CuratorPrincipal("alice", frozenset({role}), scopes)


def test_principal_validation_fails_closed():
    with pytest.raises(ValueError, match="actor_id"):
        CuratorPrincipal("", frozenset({CuratorRole.ADMIN}))
    with pytest.raises(ValueError, match="at least one"):
        CuratorPrincipal("alice", frozenset())
    with pytest.raises(TypeError, match="CuratorRole"):
        CuratorPrincipal("alice", frozenset({"ADMIN"}))  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="scopes"):
        CuratorPrincipal("alice", frozenset({CuratorRole.ADMIN}), frozenset({""}))


def test_reviewer_can_only_coexist():
    reviewer = principal(CuratorRole.REVIEWER)
    allowed = authorize_conflict_decision(
        reviewer,
        actor="alice",
        disposition=ConflictDisposition.COEXIST,
        candidate_fact_id="new",
    )
    denied = authorize_conflict_decision(
        reviewer,
        actor="alice",
        disposition=ConflictDisposition.SUPERSEDE,
        candidate_fact_id="new",
        target_fact_ids=("old",),
    )
    assert allowed.allowed
    assert allowed.capability is CuratorCapability.RESOLVE_COEXIST
    assert not denied.allowed
    assert denied.capability is CuratorCapability.RESOLVE_SUPERSEDE


def test_curator_can_resolve_all_executable_dispositions():
    curator = principal(CuratorRole.CURATOR)
    for disposition in (
        ConflictDisposition.COEXIST,
        ConflictDisposition.CONTEXTUALIZE,
        ConflictDisposition.SUPERSEDE,
    ):
        result = authorize_conflict_decision(
            curator,
            actor="alice",
            disposition=disposition,
            candidate_fact_id="new",
            target_fact_ids=("old",) if disposition is ConflictDisposition.SUPERSEDE else (),
        )
        assert result.allowed


def test_actor_and_fact_scopes_fail_closed():
    scoped = principal(
        CuratorRole.CURATOR,
        scopes=frozenset({"fact:new", "fact:old-1"}),
    )
    assert not authorize_conflict_decision(
        scoped,
        actor="mallory",
        disposition="COEXIST",
        candidate_fact_id="new",
    ).allowed
    assert not authorize_conflict_decision(
        scoped,
        actor="alice",
        disposition="COEXIST",
        candidate_fact_id="outside",
    ).allowed
    assert not authorize_conflict_decision(
        scoped,
        actor="alice",
        disposition="SUPERSEDE",
        candidate_fact_id="new",
        target_fact_ids=("old-2",),
    ).allowed
    assert authorize_conflict_decision(
        scoped,
        actor="alice",
        disposition="SUPERSEDE",
        candidate_fact_id="new",
        target_fact_ids=("old-1",),
    ).allowed


def test_unknown_and_review_required_dispositions_are_not_executable():
    admin = principal(CuratorRole.ADMIN)
    assert not authorize_conflict_decision(
        admin,
        actor="alice",
        disposition="UNKNOWN",
        candidate_fact_id="new",
    ).allowed
    assert not authorize_conflict_decision(
        admin,
        actor="alice",
        disposition="REVIEW_REQUIRED",
        candidate_fact_id="new",
    ).allowed


def test_lease_key_and_acquire_validation():
    with pytest.raises(ValueError, match="candidate_fact_id"):
        CuratorLeaseRegistry.lease_key("", "report")
    with pytest.raises(ValueError, match="candidate_fact_id"):
        CuratorLeaseRegistry.lease_key("fact", "")
    registry = CuratorLeaseRegistry()
    with pytest.raises(ValueError, match="owner"):
        registry.acquire(candidate_fact_id="fact", report_id="report", owner="")
    with pytest.raises(ValueError, match="ttl_seconds"):
        registry.acquire(
            candidate_fact_id="fact", report_id="report", owner="alice", ttl_seconds=0
        )


def test_lease_registry_blocks_parallel_owner_and_releases_exact_token():
    now = [10.0]
    registry = CuratorLeaseRegistry(clock=lambda: now[0])
    first = registry.acquire(
        candidate_fact_id="new",
        report_id="report",
        owner="alice",
        ttl_seconds=5.0,
    )
    assert first is not None
    assert registry.is_active(candidate_fact_id="new", report_id="report")
    assert (
        registry.acquire(
            candidate_fact_id="new",
            report_id="report",
            owner="bob",
            ttl_seconds=5.0,
        )
        is None
    )
    wrong_owner = DecisionLease(first.key, "mallory", first.token, first.expires_at)
    wrong_token = DecisionLease(first.key, first.owner, "wrong", first.expires_at)
    assert not registry.release(wrong_owner)
    assert not registry.release(wrong_token)
    assert registry.release(first)
    assert not registry.release(first)


def test_expired_lease_can_be_reacquired():
    now = [10.0]
    registry = CuratorLeaseRegistry(clock=lambda: now[0])
    first = registry.acquire(
        candidate_fact_id="new",
        report_id="report",
        owner="alice",
        ttl_seconds=1.0,
    )
    assert first is not None
    now[0] = 11.1
    assert not registry.is_active(candidate_fact_id="new", report_id="report")
    second = registry.acquire(
        candidate_fact_id="new",
        report_id="report",
        owner="bob",
        ttl_seconds=1.0,
    )
    assert second is not None
    assert second.owner == "bob"
