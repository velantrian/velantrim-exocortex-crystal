"""Scoped curator authorization and local decision leases.

A host authenticates an identity, maps it to :class:`CuratorPrincipal` and
then composes the fail-closed authorization helpers in this module before
calling Crystal's canonical review contract.

The bundled lease registry coordinates one Python process only. Distributed
hosts must supply an external lease/fencing adapter and must not describe this
registry as a distributed lock.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import hashlib
import threading
import time
from typing import Iterable, Optional

from core.contradiction_report import ConflictDisposition


class CuratorRole(str, Enum):
    REVIEWER = "REVIEWER"
    CURATOR = "CURATOR"
    ADMIN = "ADMIN"


class CuratorCapability(str, Enum):
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    FORCE_APPROVE = "FORCE_APPROVE"
    RESOLVE_COEXIST = "RESOLVE_COEXIST"
    RESOLVE_CONTEXTUALIZE = "RESOLVE_CONTEXTUALIZE"
    RESOLVE_SUPERSEDE = "RESOLVE_SUPERSEDE"


class CuratorAction(str, Enum):
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    FORCE_APPROVE = "FORCE_APPROVE"


_ROLE_CAPABILITIES = {
    CuratorRole.REVIEWER: frozenset(
        {
            CuratorCapability.APPROVE,
            CuratorCapability.REJECT,
            CuratorCapability.RESOLVE_COEXIST,
        }
    ),
    CuratorRole.CURATOR: frozenset(
        {
            CuratorCapability.APPROVE,
            CuratorCapability.REJECT,
            CuratorCapability.RESOLVE_COEXIST,
            CuratorCapability.RESOLVE_CONTEXTUALIZE,
            CuratorCapability.RESOLVE_SUPERSEDE,
        }
    ),
    CuratorRole.ADMIN: frozenset(CuratorCapability),
}

_ACTION_CAPABILITY = {
    CuratorAction.APPROVE: CuratorCapability.APPROVE,
    CuratorAction.REJECT: CuratorCapability.REJECT,
    CuratorAction.FORCE_APPROVE: CuratorCapability.FORCE_APPROVE,
}

_DISPOSITION_CAPABILITY = {
    ConflictDisposition.COEXIST: CuratorCapability.RESOLVE_COEXIST,
    ConflictDisposition.CONTEXTUALIZE: CuratorCapability.RESOLVE_CONTEXTUALIZE,
    ConflictDisposition.SUPERSEDE: CuratorCapability.RESOLVE_SUPERSEDE,
}


@dataclass(frozen=True)
class CuratorPrincipal:
    actor_id: str
    roles: frozenset[CuratorRole]
    scopes: frozenset[str] = frozenset({"fact:*"})

    def __post_init__(self) -> None:
        if not isinstance(self.actor_id, str) or not self.actor_id.strip():
            raise ValueError("actor_id must be a non-empty string")
        if not self.roles:
            raise ValueError("at least one curator role is required")
        if any(not isinstance(role, CuratorRole) for role in self.roles):
            raise TypeError("roles must contain CuratorRole values")
        if not self.scopes:
            raise ValueError("at least one curator scope is required")
        if any(not isinstance(scope, str) or not scope.strip() for scope in self.scopes):
            raise ValueError("scopes must contain non-empty strings")
        object.__setattr__(self, "actor_id", self.actor_id.strip())
        object.__setattr__(
            self,
            "scopes",
            frozenset(scope.strip() for scope in self.scopes),
        )

    @property
    def capabilities(self) -> frozenset[CuratorCapability]:
        merged: set[CuratorCapability] = set()
        for role in self.roles:
            merged.update(_ROLE_CAPABILITIES[role])
        return frozenset(merged)


@dataclass(frozen=True)
class AuthorizationResult:
    allowed: bool
    reason: str
    capability: Optional[CuratorCapability] = None


def _scope_allows(scopes: Iterable[str], fact_id: str) -> bool:
    return "fact:*" in scopes or f"fact:{fact_id}" in scopes


def _actor_matches(principal: CuratorPrincipal, actor: Optional[str]) -> bool:
    """A missing compatibility actor is acceptable; a supplied actor must match."""
    return actor is None or (
        isinstance(actor, str) and actor.strip() == principal.actor_id
    )


def authorize_review_action(
    principal: CuratorPrincipal,
    *,
    action: CuratorAction | str,
    candidate_fact_id: str,
    actor: Optional[str] = None,
) -> AuthorizationResult:
    """Authorize approve/reject/force without inspecting claim content."""
    if not isinstance(principal, CuratorPrincipal):
        return AuthorizationResult(False, "authenticated curator principal is required")
    if not _actor_matches(principal, actor):
        return AuthorizationResult(False, "actor does not match authenticated principal")
    try:
        selected = CuratorAction(action)
    except (TypeError, ValueError):
        return AuthorizationResult(False, "unknown curator action")
    capability = _ACTION_CAPABILITY[selected]
    if capability not in principal.capabilities:
        return AuthorizationResult(False, "principal lacks required capability", capability)
    if not isinstance(candidate_fact_id, str) or not candidate_fact_id.strip():
        return AuthorizationResult(False, "candidate fact id is invalid", capability)
    normalized_candidate_id = candidate_fact_id.strip()
    if not _scope_allows(principal.scopes, normalized_candidate_id):
        return AuthorizationResult(False, "candidate fact is outside principal scope", capability)
    return AuthorizationResult(True, "authorized", capability)


def authorize_conflict_decision(
    principal: CuratorPrincipal,
    *,
    actor: Optional[str],
    disposition: ConflictDisposition | str,
    candidate_fact_id: str,
    target_fact_ids: Iterable[str] = (),
) -> AuthorizationResult:
    """Authorize one explicit contradiction decision without claim content."""
    if not isinstance(principal, CuratorPrincipal):
        return AuthorizationResult(False, "authenticated curator principal is required")
    if not _actor_matches(principal, actor):
        return AuthorizationResult(False, "actor does not match authenticated principal")
    try:
        selected = ConflictDisposition(disposition)
    except (TypeError, ValueError):
        return AuthorizationResult(False, "unknown conflict disposition")
    if selected is ConflictDisposition.REVIEW_REQUIRED:
        return AuthorizationResult(False, "REVIEW_REQUIRED is not an executable decision")
    capability = _DISPOSITION_CAPABILITY[selected]
    if capability not in principal.capabilities:
        return AuthorizationResult(False, "principal lacks required capability", capability)
    if not isinstance(candidate_fact_id, str) or not candidate_fact_id.strip():
        return AuthorizationResult(False, "candidate fact id is invalid", capability)
    normalized_candidate_id = candidate_fact_id.strip()
    if not _scope_allows(principal.scopes, normalized_candidate_id):
        return AuthorizationResult(False, "candidate fact is outside principal scope", capability)
    for target_id in target_fact_ids:
        if not isinstance(target_id, str) or not target_id.strip():
            return AuthorizationResult(False, "target fact id is invalid", capability)
        normalized_target_id = target_id.strip()
        if not _scope_allows(principal.scopes, normalized_target_id):
            return AuthorizationResult(False, "target fact is outside principal scope", capability)
    return AuthorizationResult(True, "authorized", capability)


@dataclass(frozen=True)
class DecisionLease:
    key: str
    owner: str
    token: str
    expires_at: float


class CuratorLeaseRegistry:
    """Thread-safe, fail-closed in-process lease registry."""

    def __init__(self, *, clock=time.monotonic) -> None:
        self._clock = clock
        self._lock = threading.RLock()
        self._leases: dict[str, DecisionLease] = {}

    @staticmethod
    def lease_key(candidate_fact_id: str, report_id: str) -> str:
        if not isinstance(candidate_fact_id, str) or not candidate_fact_id:
            raise ValueError("candidate_fact_id and report_id are required")
        if not isinstance(report_id, str) or not report_id:
            raise ValueError("candidate_fact_id and report_id are required")
        return f"{len(candidate_fact_id)}:{candidate_fact_id}|{len(report_id)}:{report_id}"

    def acquire(
        self,
        *,
        candidate_fact_id: str,
        report_id: str,
        owner: str,
        ttl_seconds: float = 30.0,
    ) -> Optional[DecisionLease]:
        if not owner or ttl_seconds <= 0:
            raise ValueError("owner must be non-empty and ttl_seconds must be positive")
        key = self.lease_key(candidate_fact_id, report_id)
        now = self._clock()
        with self._lock:
            current = self._leases.get(key)
            if current is not None and current.expires_at > now:
                return None
            raw = f"{key}|{owner}|{now:.9f}|{ttl_seconds:.9f}".encode("utf-8")
            token = hashlib.sha256(raw).hexdigest()
            lease = DecisionLease(key, owner, token, now + ttl_seconds)
            self._leases[key] = lease
            return lease

    def release(self, lease: DecisionLease) -> bool:
        with self._lock:
            current = self._leases.get(lease.key)
            if current is None or current.token != lease.token or current.owner != lease.owner:
                return False
            del self._leases[lease.key]
            return True

    def is_active(self, *, candidate_fact_id: str, report_id: str) -> bool:
        key = self.lease_key(candidate_fact_id, report_id)
        now = self._clock()
        with self._lock:
            current = self._leases.get(key)
            if current is None:
                return False
            if current.expires_at <= now:
                del self._leases[key]
                return False
            return True


__all__ = [
    "AuthorizationResult",
    "CuratorAction",
    "CuratorCapability",
    "CuratorLeaseRegistry",
    "CuratorPrincipal",
    "CuratorRole",
    "DecisionLease",
    "authorize_conflict_decision",
    "authorize_review_action",
]
