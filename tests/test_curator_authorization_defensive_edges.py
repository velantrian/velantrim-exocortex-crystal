"""Defensive coverage for principal validation and authorization denial paths."""
from __future__ import annotations

import pytest

from core.contradiction_report import ConflictDisposition
from core.curator_auth import (
    AuthorizationResult,
    CuratorAction,
    CuratorCapability,
    CuratorPrincipal,
    CuratorRole,
    authorize_conflict_decision,
    authorize_review_action,
)
from core.curator_runtime import (
    PrincipalConfigurationError,
    _authorization_denied,
    _csv_values,
    _normalize_fact_id,
)


def _principal(
    role: CuratorRole = CuratorRole.REVIEWER,
    *,
    scopes: frozenset[str] = frozenset({"fact:allowed"}),
) -> CuratorPrincipal:
    return CuratorPrincipal("alice", frozenset({role}), scopes)


def test_principal_requires_nonempty_scope_collection_and_merges_roles():
    with pytest.raises(ValueError, match="at least one curator scope"):
        CuratorPrincipal("alice", frozenset({CuratorRole.ADMIN}), frozenset())

    principal = CuratorPrincipal(
        " alice ",
        frozenset({CuratorRole.REVIEWER, CuratorRole.CURATOR}),
        frozenset({" fact:allowed "}),
    )
    assert principal.actor_id == "alice"
    assert principal.scopes == frozenset({"fact:allowed"})
    assert CuratorCapability.RESOLVE_SUPERSEDE in principal.capabilities


def test_review_authorization_denies_every_invalid_boundary():
    assert not authorize_review_action(  # type: ignore[arg-type]
        None,
        action=CuratorAction.APPROVE,
        candidate_fact_id="allowed",
    ).allowed

    principal = _principal()
    assert not authorize_review_action(
        principal,
        action=CuratorAction.APPROVE,
        candidate_fact_id="allowed",
        actor="mallory",
    ).allowed
    assert not authorize_review_action(
        principal,
        action="UNKNOWN",
        candidate_fact_id="allowed",
    ).allowed

    missing_capability = authorize_review_action(
        principal,
        action=CuratorAction.FORCE_APPROVE,
        candidate_fact_id="allowed",
    )
    assert not missing_capability.allowed
    assert missing_capability.capability is CuratorCapability.FORCE_APPROVE

    assert not authorize_review_action(
        principal,
        action=CuratorAction.APPROVE,
        candidate_fact_id=" ",
    ).allowed
    assert not authorize_review_action(
        principal,
        action=CuratorAction.APPROVE,
        candidate_fact_id="outside",
    ).allowed
    assert authorize_review_action(
        principal,
        action=CuratorAction.APPROVE,
        candidate_fact_id=" allowed ",
    ).allowed


def test_conflict_authorization_denies_invalid_principal_ids_and_targets():
    assert not authorize_conflict_decision(  # type: ignore[arg-type]
        None,
        actor=None,
        disposition=ConflictDisposition.COEXIST,
        candidate_fact_id="allowed",
    ).allowed

    principal = _principal(CuratorRole.CURATOR)
    assert not authorize_conflict_decision(
        principal,
        actor="alice",
        disposition=ConflictDisposition.COEXIST,
        candidate_fact_id=" ",
    ).allowed
    assert not authorize_conflict_decision(
        principal,
        actor="alice",
        disposition=ConflictDisposition.SUPERSEDE,
        candidate_fact_id="allowed",
        target_fact_ids=(" ",),
    ).allowed
    assert not authorize_conflict_decision(
        principal,
        actor="alice",
        disposition=ConflictDisposition.SUPERSEDE,
        candidate_fact_id="allowed",
        target_fact_ids=("outside",),
    ).allowed


def test_runtime_helpers_fail_closed_and_preserve_capability_metadata():
    with pytest.raises(PrincipalConfigurationError, match="roles"):
        _csv_values(", ,", field="roles")

    no_capability = _authorization_denied(AuthorizationResult(False, "denied"))
    assert no_capability == {
        "authorized": False,
        "reason": "denied",
        "required_capability": None,
    }
    with_capability = _authorization_denied(
        AuthorizationResult(False, "denied", CuratorCapability.REJECT)
    )
    assert with_capability["required_capability"] == "REJECT"
    assert _normalize_fact_id(" allowed ") == "allowed"
    marker = object()
    assert _normalize_fact_id(marker) is marker
