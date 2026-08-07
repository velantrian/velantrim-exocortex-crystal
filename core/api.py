# core/api.py
# Velantrim ExoCortex — optional FastAPI service layer (grant milestone M2).
#
# This is an OPTIONAL extra. The default Velantrim runtime is pure standard
# library; FastAPI/uvicorn are only needed to expose the memory core over HTTP.
# Install with:  pip install ".[api]"
#
# Read endpoints are bearer-token guarded. Curator writes add a second
# fail-closed layer: the authenticated token maps to one configured
# CuratorPrincipal, and request text never establishes audit identity.

from typing import Any, Dict, List, Optional

try:
    from fastapi import Depends, FastAPI, Header, HTTPException, Query
    from fastapi.responses import HTMLResponse
    from pydantic import BaseModel, Field
    _HAS_FASTAPI = True
except ImportError:  # pragma: no cover - exercised on stdlib-only installs
    _HAS_FASTAPI = False

__version__ = "0.3.0"

_INSTALL_HINT = (
    "The FastAPI service layer is an optional extra. Install it with:\n"
    '    pip install ".[api]"\n'
    "(this pulls in fastapi + uvicorn; the default Velantrim runtime stays "
    "standard-library only)."
)


def create_app():
    """Build and return the Velantrim FastAPI application."""
    if not _HAS_FASTAPI:
        raise RuntimeError(_INSTALL_HINT)

    import asyncio
    import hmac
    import os
    from importlib import resources

    from core import aio, evidence, provenance, review
    from core.api_ingest_policy import resolve_api_ingest
    from core.conflict_surfaces import register_conflict_routes
    from core.curator_auth import CuratorPrincipal
    from core.curator_runtime import (
        PrincipalConfigurationError,
        approve_as_principal,
        principal_from_environment,
        reject_as_principal,
        synthetic_local_admin_principal,
    )

    app = FastAPI(
        title="Velantrim Crystal",
        version=__version__,
        description="Verifiable, local-first AI memory — HTTP service layer.",
    )

    def _configured_api_token() -> str:
        raw = os.environ.get("VELANTRIM_API_TOKEN")
        if raw is None or raw == "":
            return ""
        if raw != raw.strip():
            raise HTTPException(
                status_code=401,
                detail="API authentication configuration is invalid: "
                       "VELANTRIM_API_TOKEN must not be blank or padded with whitespace.",
            )
        return raw

    def _explicit_unauth_local() -> bool:
        raw_token = os.environ.get("VELANTRIM_API_TOKEN")
        return (
            (raw_token is None or raw_token == "")
            and os.environ.get("VELANTRIM_API_ALLOW_UNAUTH_LOCAL") == "1"
        )

    def _require_api_token(
            authorization: Optional[str] = Header(None)) -> None:
        expected = _configured_api_token()
        if not expected:
            if _explicit_unauth_local():
                return
            raise HTTPException(
                status_code=401,
                detail="API authentication is not configured. Set "
                       "VELANTRIM_API_TOKEN to require a bearer token, or set "
                       "VELANTRIM_API_ALLOW_UNAUTH_LOCAL=1 to explicitly allow "
                       "an unauthenticated local-development instance.")
        supplied = ""
        if authorization and authorization.lower().startswith("bearer "):
            supplied = authorization[7:]
        if not hmac.compare_digest(supplied, expected):
            raise HTTPException(status_code=401,
                                detail="missing or invalid bearer token")

    def _require_curator_principal(
            authorization: Optional[str] = Header(None)) -> CuratorPrincipal:
        _require_api_token(authorization)
        if _explicit_unauth_local():
            return synthetic_local_admin_principal()
        try:
            return principal_from_environment()
        except PrincipalConfigurationError as exc:
            raise HTTPException(status_code=403, detail=str(exc)) from exc

    _guarded = [Depends(_require_api_token)]
    _MAX_UTTERANCE = 10_000

    class IngestRequest(BaseModel):
        text: str = Field(..., min_length=1, max_length=_MAX_UTTERANCE,
                          description="The utterance to ingest.")
        source: str = "api"
        confidence: float = Field(0.6, ge=0.0, le=1.0)
        significance: Optional[float] = Field(None, ge=0.0, le=1.0)
        claim_type: Optional[str] = None
        source_status: Optional[str] = None
        import_mode: bool = False
        evidence_refs: Optional[List[str]] = None

    class AskRequest(BaseModel):
        query: str = Field(..., min_length=1, max_length=_MAX_UTTERANCE)

    class VerifyRequest(BaseModel):
        receipt: Dict[str, Any]
        strict_provenance: bool = False

    class ApproveRequest(BaseModel):
        fact_id: str = Field(..., min_length=1)
        actor: Optional[str] = Field(None, min_length=1)
        note: Optional[str] = None
        force: bool = False
        reason: Optional[str] = Field(None, max_length=500)

    class RejectRequest(BaseModel):
        fact_id: str = Field(..., min_length=1)
        actor: Optional[str] = Field(None, min_length=1)
        reason: str = "curator_rejected"

    @app.get("/health")
    async def health() -> Dict[str, Any]:
        return {"status": "ok", "service": "velantrim-crystal", "version": __version__}

    @app.post("/ingest", dependencies=_guarded)
    async def ingest_endpoint(req: IngestRequest) -> Dict[str, Any]:
        try:
            policy = resolve_api_ingest(
                source_status=req.source_status,
                import_mode=req.import_mode,
                evidence_refs=req.evidence_refs,
            )
        except ValueError as e:
            raise HTTPException(status_code=422, detail=str(e))
        kwargs: Dict[str, Any] = {
            "source": req.source,
            "confidence": req.confidence,
            "significance": req.significance,
            "source_status": policy["source_status"],
        }
        if req.claim_type is not None:
            kwargs["claim_type"] = req.claim_type
        if policy.get("metadata"):
            kwargs["metadata"] = policy["metadata"]
        try:
            return await aio.aingest(req.text, **kwargs)
        except ValueError as e:
            raise HTTPException(status_code=422, detail=str(e))

    @app.post("/ask", dependencies=_guarded)
    async def ask_endpoint(req: AskRequest) -> Dict[str, Any]:
        return await aio.arun(req.query)

    @app.get("/receipt", dependencies=_guarded)
    async def receipt_endpoint(
            q: str = Query(..., min_length=1, max_length=_MAX_UTTERANCE)) -> Dict[str, Any]:
        result = await aio.arun(q)
        try:
            return await asyncio.to_thread(provenance.build_receipt, result)
        except ValueError as e:
            raise HTTPException(status_code=422, detail=str(e))

    @app.post("/verify-receipt", dependencies=_guarded)
    async def verify_receipt_endpoint(req: VerifyRequest) -> Dict[str, Any]:
        return await asyncio.to_thread(
            provenance.verify_receipt, req.receipt,
            strict_provenance=req.strict_provenance,
        )

    @app.get("/evidence/{fact_id}", dependencies=_guarded)
    async def evidence_endpoint(fact_id: str) -> List[Dict[str, Any]]:
        return await asyncio.to_thread(evidence.public_evidence_for, fact_id)

    @app.get("/review/queue", dependencies=_guarded)
    async def review_queue(limit: Optional[int] = None,
                           claim_type: Optional[str] = None,
                           diagnose: bool = False) -> List[Dict[str, Any]]:
        return await asyncio.to_thread(
            review.pending, limit=limit, claim_type=claim_type, diagnose=diagnose)

    @app.get("/review/report", dependencies=_guarded)
    async def review_report_endpoint() -> Dict[str, Any]:
        return await asyncio.to_thread(review.review_report)

    @app.get("/review/decisions", dependencies=_guarded)
    async def review_decisions(limit: int = 50,
                               include_claim: bool = True) -> List[Dict[str, Any]]:
        return await asyncio.to_thread(review.decisions, limit=limit,
                                       include_claim=include_claim)

    @app.get("/review/item/{fact_id}", dependencies=_guarded)
    async def review_item_endpoint(fact_id: str) -> Dict[str, Any]:
        item = await asyncio.to_thread(review.review_item, fact_id)
        if not item.get("found"):
            raise HTTPException(status_code=404, detail=f"unknown fact {fact_id}")
        return item

    @app.post("/review/approve")
    async def review_approve(
        req: ApproveRequest,
        principal: CuratorPrincipal = Depends(_require_curator_principal),
    ) -> Dict[str, Any]:
        if req.force and not (req.reason and req.reason.strip()):
            raise HTTPException(
                status_code=422,
                detail="force approval overrides a blocking diagnosis and "
                       "requires a non-empty 'reason'")
        # In explicit unauthenticated local mode there is no external identity
        # provider. Preserve the historical requirement that an override must
        # consciously assert the exact synthetic local principal. Under bearer
        # auth, identity already comes from the principal and actor is optional.
        if (
            req.force
            and _explicit_unauth_local()
            and not (req.actor and req.actor.strip() == "api-curator")
        ):
            raise HTTPException(
                status_code=422,
                detail="local force approval requires an explicit actor assertion "
                       "matching api-curator")
        res = await asyncio.to_thread(
            approve_as_principal,
            principal,
            req.fact_id,
            requested_actor=req.actor,
            note=req.note,
            force=req.force,
            reason=req.reason,
        )
        if res.get("authorized") is False:
            raise HTTPException(status_code=403, detail=res["reason"])
        if not res.get("found"):
            raise HTTPException(status_code=404,
                                detail=f"unknown fact {req.fact_id}")
        return res

    @app.post("/review/reject")
    async def review_reject(
        req: RejectRequest,
        principal: CuratorPrincipal = Depends(_require_curator_principal),
    ) -> Dict[str, Any]:
        # A body actor is an exact-match assertion only in authenticated mode.
        # In explicit unauthenticated local mode it cannot establish identity,
        # so it is ignored and the synthetic principal is recorded.
        requested_actor = None if _explicit_unauth_local() else req.actor
        res = await asyncio.to_thread(
            reject_as_principal,
            principal,
            req.fact_id,
            requested_actor=requested_actor,
            reason=req.reason,
        )
        if res.get("authorized") is False:
            raise HTTPException(status_code=403, detail=res["reason"])
        if not res.get("found"):
            raise HTTPException(status_code=404,
                                detail=f"unknown fact {req.fact_id}")
        return res

    register_conflict_routes(app, principal_dependency=_require_curator_principal)

    @app.get("/review/ui", response_class=HTMLResponse)
    async def review_ui() -> str:
        return resources.files("core").joinpath(
            "_webui/review.html").read_text(encoding="utf-8")

    return app


def main() -> None:  # pragma: no cover - thin uvicorn launcher
    if not _HAS_FASTAPI:
        raise SystemExit(_INSTALL_HINT)
    try:
        import uvicorn
    except ImportError:
        raise SystemExit(_INSTALL_HINT)
    import os

    host = os.environ.get("VELANTRIM_API_HOST", "127.0.0.1")
    port = int(os.environ.get("VELANTRIM_API_PORT", "8000"))
    uvicorn.run(create_app(), host=host, port=port)


if __name__ == "__main__":  # pragma: no cover
    main()
