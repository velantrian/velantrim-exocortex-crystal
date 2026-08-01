"""Scoped curator authorization and local decision leases.

This module is deliberately independent from identity-provider plumbing. A host
maps an authenticated identity to ``CuratorPrincipal`` and then asks this module
for a fail-closed authorization decision before calling Crystal's canonical
review contract.

The lease registry prevents two curator workers in one process from applying a
decision for the same candidate/report concurrently. Distributed deployments
must provide an external lease implementation with the same acquire/release
contract.
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
    RESOLVE_COEXIST = "RESOLVE_COEXIST"
    RESOLVE_CONTEXTUALIZE = "RESOLVE_CONTEXTUALIZE"
    RESOLVE_SUPERSEDE = "RESOLVE_SUPERSEDE"


_ROLE_CAPABILITIES = {
    CuratorRole.REVIEWER: frozenset({CuratorCapability.RESOLVE_COEXIST}),
    CuratorRole.CURATOR: frozenset(
        {
            CuratorCapability.RESOLVE_COEXIST,
            CuratorCapability.RESOLVE_CONTEXTUALIZE,
            CuratorCapability.RESOLVE_SUPERSEDE,
        }
    ),
    CuratorRole.ADMIN: frozenset(CuratorCapability),
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
        if any(not isinstance(scope, str) or not scope.strip() for scope in self.scopes):
            raise ValueError("scopes must contain non-empty strings")
        object.__setattr__(self, "actor_id", self.actor_id.strip())

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


def authorize_conflict_decision(
    principal: CuratorPrincipal,
    *,
    actor: str,
    disposition: ConflictDisposition | str,
    candidate_fact_id: str,
    target_fact_ids: Iterable[str] = (),
) -> AuthorizationResult:
    """Authorize one explicit decision without inspecting claim content."""
    if not isinstance(actor, str) or actor.strip() != principal.actor_id:
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
    if not _scope_allows(principal.scopes, candidate_fact_id):
        return AuthorizationResult(False, "candidate fact is outside principal scope", capability)
    for target_id in target_fact_ids:
        if not _scope_allows(principal.scopes, target_id):
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
        if not candidate_fact_id or not report_id:
            raise ValueError("candidate_fact_id and report_id are required")
        return f"{candidate_fact_id}:{report_id}"

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
    "CuratorCapability",
    "CuratorLeaseRegistry",
    "CuratorPrincipal",
    "CuratorRole",
    "DecisionLease",
    "authorize_conflict_decision",
]
