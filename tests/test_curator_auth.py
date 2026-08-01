from core.contradiction_report import ConflictDisposition
from core.curator_auth import (
    CuratorCapability,
    CuratorLeaseRegistry,
    CuratorPrincipal,
    CuratorRole,
    authorize_conflict_decision,
)


def principal(role, *, scopes=frozenset({"fact:*"})):
    return CuratorPrincipal("alice", frozenset({role}), scopes)


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


def test_review_required_is_not_executable():
    result = authorize_conflict_decision(
        principal(CuratorRole.ADMIN),
        actor="alice",
        disposition="REVIEW_REQUIRED",
        candidate_fact_id="new",
    )
    assert not result.allowed


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
