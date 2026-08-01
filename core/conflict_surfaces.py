"""Public, fail-closed conflict-resolution surfaces.

CLI:
    python -m core.conflict_surfaces FACT_ID --disposition COEXIST \
        --actor alice --reason "independent contexts" \
        --expected-report-id REPORT_ID

HTTP:
    register_conflict_routes(app, dependencies=[Depends(auth_guard)])

The HTTP helper refuses an unguarded registration unless the caller opts in
explicitly for local development. Both surfaces delegate to
``core.review.resolve_conflict``; they do not create an alternative write path.
"""

from __future__ import annotations

import argparse
import asyncio
import json
from typing import Any, Iterable, Optional, Sequence

from core import review
from core.contradiction_report import ConflictDisposition

_DISPOSITIONS = tuple(item.value for item in ConflictDisposition)


def resolve_conflict_payload(
    fact_id: str,
    *,
    disposition: str,
    actor: str,
    reason: str,
    target_fact_ids: Iterable[str] = (),
    expected_report_id: Optional[str] = None,
) -> dict[str, Any]:
    """Validate the public payload and delegate to the canonical core contract."""
    if not isinstance(fact_id, str) or not fact_id.strip():
        raise ValueError("fact_id must be a non-empty string")
    if disposition not in _DISPOSITIONS:
        raise ValueError(f"disposition must be one of {', '.join(_DISPOSITIONS)}")
    if not isinstance(actor, str) or not actor.strip():
        raise ValueError("actor must be a non-empty string")
    if not isinstance(reason, str) or not reason.strip():
        raise ValueError("reason must be a non-empty string")
    targets = tuple(target_fact_ids)
    if any(not isinstance(item, str) or not item.strip() for item in targets):
        raise ValueError("target_fact_ids must contain non-empty strings")
    if expected_report_id is not None and (
        not isinstance(expected_report_id, str) or not expected_report_id.strip()
    ):
        raise ValueError("expected_report_id must be a non-empty string when supplied")
    return review.resolve_conflict(
        fact_id.strip(),
        disposition=disposition,
        actor=actor.strip(),
        reason=reason.strip(),
        target_fact_ids=targets,
        expected_report_id=expected_report_id,
    )


def register_conflict_routes(
    app: Any,
    *,
    dependencies: Sequence[Any] = (),
    allow_unguarded_local: bool = False,
) -> None:
    """Register ``POST /review/resolve-conflict`` on a FastAPI application.

    Authentication dependencies must be supplied by the host application.
    Empty dependencies fail closed unless ``allow_unguarded_local=True`` is an
    explicit local-development choice.
    """
    if not dependencies and not allow_unguarded_local:
        raise ValueError("conflict route requires authentication dependencies")
    try:
        from fastapi import HTTPException
        from pydantic import BaseModel, Field
    except ImportError as exc:  # pragma: no cover - stdlib install path
        raise RuntimeError('install the optional API extra with: pip install ".[api]"') from exc

    class ResolveConflictRequest(BaseModel):
        fact_id: str = Field(..., min_length=1)
        disposition: str
        actor: str = Field(..., min_length=1)
        reason: str = Field(..., min_length=1, max_length=500)
        target_fact_ids: list[str] = Field(default_factory=list)
        expected_report_id: Optional[str] = None

    async def resolve_conflict_endpoint(req) -> dict[str, Any]:
        try:
            return await asyncio.to_thread(
                resolve_conflict_payload,
                req.fact_id,
                disposition=req.disposition,
                actor=req.actor,
                reason=req.reason,
                target_fact_ids=req.target_fact_ids,
                expected_report_id=req.expected_report_id,
            )
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    resolve_conflict_endpoint.__annotations__["req"] = ResolveConflictRequest
    app.post("/review/resolve-conflict", dependencies=list(dependencies))(
        resolve_conflict_endpoint
    )


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="velantrim-resolve-conflict",
        description="Apply an explicit, audited contradiction disposition.",
    )
    parser.add_argument("fact_id")
    parser.add_argument("--disposition", required=True, choices=_DISPOSITIONS)
    parser.add_argument("--actor", required=True)
    parser.add_argument("--reason", required=True)
    parser.add_argument("--target", action="append", default=[], dest="target_fact_ids")
    parser.add_argument("--expected-report-id", default=None)
    args = parser.parse_args(argv)
    try:
        result = resolve_conflict_payload(
            args.fact_id,
            disposition=args.disposition,
            actor=args.actor,
            reason=args.reason,
            target_fact_ids=args.target_fact_ids,
            expected_report_id=args.expected_report_id,
        )
    except ValueError as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("approved") else 1


if __name__ == "__main__":  # pragma: no cover - exercised via main()
    raise SystemExit(main())
