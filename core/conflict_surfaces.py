"""Authenticated, fail-closed conflict-resolution surfaces.

CLI:
    VELANTRIM_CURATOR_ACTOR=alice \
    VELANTRIM_CURATOR_ROLES=CURATOR \
    VELANTRIM_CURATOR_SCOPES=fact:* \
    python -m core.conflict_surfaces FACT_ID --disposition COEXIST \
        --reason "independent contexts" --expected-report-id REPORT_ID

HTTP hosts register a dependency that returns ``CuratorPrincipal``. The bundled
FastAPI application provides a one-token/one-principal environment mapping.
Neither request bodies nor CLI arguments establish curator identity.
"""

from __future__ import annotations

import argparse
import asyncio
import json
from typing import Any, Iterable, Optional, Sequence

from core.contradiction_report import ConflictDisposition
from core.curator_auth import CuratorPrincipal
from core.curator_runtime import (
    PrincipalConfigurationError,
    principal_from_environment,
    resolve_conflict_as_principal,
    synthetic_local_admin_principal,
)

_DISPOSITIONS = tuple(
    item.value
    for item in ConflictDisposition
    if item is not ConflictDisposition.REVIEW_REQUIRED
)


def resolve_conflict_payload(
    principal: CuratorPrincipal,
    fact_id: str,
    *,
    disposition: str,
    actor: Optional[str] = None,
    reason: str,
    target_fact_ids: Iterable[str] = (),
    expected_report_id: Optional[str] = None,
) -> dict[str, Any]:
    """Validate public syntax and delegate through authenticated authorization."""
    if not isinstance(principal, CuratorPrincipal):
        raise ValueError("authenticated curator principal is required")
    if not isinstance(fact_id, str) or not fact_id.strip():
        raise ValueError("fact_id must be a non-empty string")
    if disposition not in _DISPOSITIONS:
        raise ValueError(f"disposition must be one of {', '.join(_DISPOSITIONS)}")
    if actor is not None and (not isinstance(actor, str) or not actor.strip()):
        raise ValueError("actor must be a non-empty string when supplied")
    if not isinstance(reason, str) or not reason.strip():
        raise ValueError("reason must be a non-empty string")
    targets = tuple(target_fact_ids)
    if any(not isinstance(item, str) or not item.strip() for item in targets):
        raise ValueError("target_fact_ids must contain non-empty strings")
    normalized_targets = tuple(item.strip() for item in targets)
    if expected_report_id is not None and (
        not isinstance(expected_report_id, str) or not expected_report_id.strip()
    ):
        raise ValueError("expected_report_id must be a non-empty string when supplied")
    return resolve_conflict_as_principal(
        principal,
        fact_id.strip(),
        disposition=disposition,
        requested_actor=actor.strip() if isinstance(actor, str) else None,
        reason=reason.strip(),
        target_fact_ids=normalized_targets,
        expected_report_id=(
            expected_report_id.strip()
            if isinstance(expected_report_id, str)
            else None
        ),
    )


def register_conflict_routes(
    app: Any,
    *,
    principal_dependency: Optional[Any] = None,
    dependencies: Sequence[Any] = (),
    allow_unguarded_local: bool = False,
) -> None:
    """Register ``POST /review/resolve-conflict`` with principal injection.

    Generic authentication dependencies alone are insufficient because they do
    not return the accountable identity. A host must supply
    ``principal_dependency``. The explicit local-development mode creates only
    the documented synthetic local admin and ignores configured curator actor
    variables because no authentication establishes those identities.
    """
    try:
        from fastapi import Depends, HTTPException
        from pydantic import BaseModel, Field
    except ImportError as exc:  # pragma: no cover - stdlib install path
        raise RuntimeError('install the optional API extra with: pip install ".[api]"') from exc

    if principal_dependency is None:
        if not allow_unguarded_local:
            raise ValueError("conflict route requires an authenticated principal dependency")

        def principal_dependency() -> CuratorPrincipal:
            return synthetic_local_admin_principal()

    class ResolveConflictRequest(BaseModel):
        fact_id: str = Field(..., min_length=1)
        disposition: str
        actor: Optional[str] = Field(None, min_length=1)
        reason: str = Field(..., min_length=1, max_length=500)
        target_fact_ids: list[str] = Field(default_factory=list)
        expected_report_id: Optional[str] = None

    async def resolve_conflict_endpoint(
        req,
        principal: CuratorPrincipal = Depends(principal_dependency),
    ) -> dict[str, Any]:
        try:
            result = await asyncio.to_thread(
                resolve_conflict_payload,
                principal,
                req.fact_id,
                disposition=req.disposition,
                actor=req.actor,
                reason=req.reason,
                target_fact_ids=req.target_fact_ids,
                expected_report_id=req.expected_report_id,
            )
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
        if result.get("authorized") is False:
            raise HTTPException(status_code=403, detail=result["reason"])
        if result.get("found") is False:
            raise HTTPException(status_code=404, detail=f"unknown fact {req.fact_id}")
        return result

    resolve_conflict_endpoint.__annotations__["req"] = ResolveConflictRequest
    app.post("/review/resolve-conflict", dependencies=list(dependencies))(
        resolve_conflict_endpoint
    )


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="velantrim-resolve-conflict",
        description="Apply an authenticated, scoped contradiction disposition.",
    )
    parser.add_argument("fact_id")
    parser.add_argument("--disposition", required=True, choices=_DISPOSITIONS)
    parser.add_argument(
        "--actor",
        default=None,
        help="compatibility assertion; must match configured principal",
    )
    parser.add_argument("--reason", required=True)
    parser.add_argument("--target", action="append", default=[], dest="target_fact_ids")
    parser.add_argument("--expected-report-id", default=None)
    args = parser.parse_args(argv)
    try:
        principal = principal_from_environment()
        result = resolve_conflict_payload(
            principal,
            args.fact_id,
            disposition=args.disposition,
            actor=args.actor,
            reason=args.reason,
            target_fact_ids=args.target_fact_ids,
            expected_report_id=args.expected_report_id,
        )
    except (ValueError, PrincipalConfigurationError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result.get("authorized") is False:
        return 3
    return 0 if result.get("approved") else 1


if __name__ == "__main__":  # pragma: no cover - exercised via main()
    raise SystemExit(main())
