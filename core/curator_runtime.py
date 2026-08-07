"""Runtime composition for authenticated curator write operations.

This module is the only bundled public-write bridge from an authenticated
principal to ``core.review``. It derives the audit actor from the principal,
checks capabilities and candidate/target scopes before mutation, and composes
the process-local report lease for contradiction decisions.
"""
from __future__ import annotations

import os
from typing import Any, Iterable, Mapping, Optional

from core import review
from core.curator_auth import (
    CuratorAction,
    CuratorLeaseRegistry,
    CuratorPrincipal,
    CuratorRole,
    authorize_conflict_decision,
    authorize_review_action,
)


class PrincipalConfigurationError(ValueError):
    """Bundled single-principal configuration is missing or malformed."""


_GLOBAL_LEASES = CuratorLeaseRegistry()


def synthetic_local_admin_principal() -> CuratorPrincipal:
    """Return the only identity allowed in explicit unauthenticated local mode."""
    return CuratorPrincipal(
        "api-curator",
        frozenset({CuratorRole.ADMIN}),
        frozenset({"fact:*"}),
    )


def _csv_values(raw: Optional[str], *, field: str) -> tuple[str, ...]:
    if not isinstance(raw, str) or not raw.strip():
        raise PrincipalConfigurationError(f"{field} is required")
    values = tuple(item.strip() for item in raw.split(",") if item.strip())
    if not values:
        raise PrincipalConfigurationError(f"{field} is required")
    return values


def principal_from_environment(
    environ: Optional[Mapping[str, str]] = None,
    *,
    allow_explicit_local_admin: bool = False,
) -> CuratorPrincipal:
    """Build the bundled one-token/one-principal mapping.

    Production-like use requires ``VELANTRIM_CURATOR_ACTOR``,
    ``VELANTRIM_CURATOR_ROLES`` and ``VELANTRIM_CURATOR_SCOPES``. A caller may
    opt into the synthetic local admin only when no principal configuration is
    present. Public unauthenticated-local surfaces call
    :func:`synthetic_local_admin_principal` directly so environment values can
    never replace that documented identity.
    """
    env = os.environ if environ is None else environ
    actor = env.get("VELANTRIM_CURATOR_ACTOR")
    roles_raw = env.get("VELANTRIM_CURATOR_ROLES")
    scopes_raw = env.get("VELANTRIM_CURATOR_SCOPES")

    no_principal_configuration = (
        actor is None and roles_raw is None and scopes_raw is None
    )
    if allow_explicit_local_admin and no_principal_configuration:
        return synthetic_local_admin_principal()

    if not isinstance(actor, str) or not actor.strip():
        raise PrincipalConfigurationError("VELANTRIM_CURATOR_ACTOR is required")
    role_names = _csv_values(roles_raw, field="VELANTRIM_CURATOR_ROLES")
    scopes = _csv_values(scopes_raw, field="VELANTRIM_CURATOR_SCOPES")
    try:
        roles = frozenset(CuratorRole(name) for name in role_names)
    except ValueError as exc:
        raise PrincipalConfigurationError(
            "VELANTRIM_CURATOR_ROLES contains an unknown role"
        ) from exc
    return CuratorPrincipal(actor, roles, frozenset(scopes))


def _authorization_denied(result) -> dict[str, Any]:
    return {
        "authorized": False,
        "reason": result.reason,
        "required_capability": (
            result.capability.value if result.capability is not None else None
        ),
    }


def _normalize_fact_id(fact_id: Any) -> Any:
    return fact_id.strip() if isinstance(fact_id, str) else fact_id


def approve_as_principal(
    principal: CuratorPrincipal,
    fact_id: str,
    *,
    requested_actor: Optional[str] = None,
    note: Optional[str] = None,
    force: bool = False,
    reason: Optional[str] = None,
) -> dict[str, Any]:
    """Authorize then call the canonical approve path with principal identity."""
    normalized_fact_id = _normalize_fact_id(fact_id)
    action = CuratorAction.FORCE_APPROVE if force else CuratorAction.APPROVE
    auth = authorize_review_action(
        principal,
        action=action,
        candidate_fact_id=normalized_fact_id,
        actor=requested_actor,
    )
    if not auth.allowed:
        return _authorization_denied(auth)
    result = review.approve(
        normalized_fact_id,
        actor=principal.actor_id,
        note=note,
        force=force,
        reason=reason,
    )
    return {"authorized": True, **result}


def reject_as_principal(
    principal: CuratorPrincipal,
    fact_id: str,
    *,
    requested_actor: Optional[str] = None,
    reason: str = "curator_rejected",
) -> dict[str, Any]:
    """Authorize then reject with principal-derived audit identity."""
    normalized_fact_id = _normalize_fact_id(fact_id)
    auth = authorize_review_action(
        principal,
        action=CuratorAction.REJECT,
        candidate_fact_id=normalized_fact_id,
        actor=requested_actor,
    )
    if not auth.allowed:
        return _authorization_denied(auth)
    result = review.reject(
        normalized_fact_id,
        actor=principal.actor_id,
        reason=reason,
    )
    return {"authorized": True, **result}


def resolve_conflict_as_principal(
    principal: CuratorPrincipal,
    fact_id: str,
    *,
    disposition: str,
    requested_actor: Optional[str] = None,
    reason: str,
    target_fact_ids: Iterable[str] = (),
    expected_report_id: Optional[str] = None,
    lease_registry: CuratorLeaseRegistry = _GLOBAL_LEASES,
    lease_ttl_seconds: float = 30.0,
) -> dict[str, Any]:
    """Authorize scopes/capability, pin the current report and hold a lease."""
    normalized_fact_id = _normalize_fact_id(fact_id)
    targets = tuple(_normalize_fact_id(item) for item in target_fact_ids)
    auth = authorize_conflict_decision(
        principal,
        actor=requested_actor,
        disposition=disposition,
        candidate_fact_id=normalized_fact_id,
        target_fact_ids=targets,
    )
    if not auth.allowed:
        return _authorization_denied(auth)

    item = review.review_item(normalized_fact_id)
    if not item.get("found"):
        return {"authorized": True, "found": False, "fact_id": normalized_fact_id}
    diagnosis = item.get("diagnosis") or {}
    report = diagnosis.get("contradiction_report") or {}
    current_report_id = report.get("report_id")
    if not isinstance(current_report_id, str) or not current_report_id:
        return {
            "authorized": True,
            "found": True,
            "approved": False,
            "reason": "NO_CURRENT_CONTRADICTION",
        }
    if expected_report_id is not None and expected_report_id != current_report_id:
        return {
            "authorized": True,
            "found": True,
            "approved": False,
            "reason": "CONTRADICTION_REPORT_CHANGED",
            "report": report,
        }

    lease = lease_registry.acquire(
        candidate_fact_id=normalized_fact_id,
        report_id=current_report_id,
        owner=principal.actor_id,
        ttl_seconds=lease_ttl_seconds,
    )
    if lease is None:
        return {
            "authorized": True,
            "found": True,
            "approved": False,
            "reason": "CURATOR_DECISION_LEASE_BUSY",
            "report_id": current_report_id,
        }
    try:
        result = review.resolve_conflict(
            normalized_fact_id,
            disposition=disposition,
            actor=principal.actor_id,
            reason=reason,
            target_fact_ids=targets,
            expected_report_id=current_report_id,
        )
        return {"authorized": True, **result}
    finally:
        lease_registry.release(lease)


__all__ = [
    "PrincipalConfigurationError",
    "approve_as_principal",
    "principal_from_environment",
    "reject_as_principal",
    "resolve_conflict_as_principal",
    "synthetic_local_admin_principal",
]
