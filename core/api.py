# core/api.py
# Velantrim ExoCortex — optional FastAPI service layer (grant milestone M2).
#
# This is an OPTIONAL extra. The default Velantrim runtime is pure standard
# library; FastAPI/uvicorn are only needed to expose the memory core over HTTP.
# Install with:  pip install ".[api]"
#
# The import of fastapi is guarded so that merely importing core.api on a
# stdlib-only install does not crash — create_app() raises a clear, actionable
# error instead. The endpoints are thin async wrappers over core/aio.py
# (asyncio.to_thread), so the synchronous pipeline never blocks the event loop;
# the on-disk L3 backend is thread-safe (see SqliteL3Graph, check_same_thread).
#
# The service exposes the same operations as the CLI, and nothing more: it does
# NOT add a write path that bypasses the TruthGate. Every /ingest and /ask call
# goes through the same Guardian + TruthGate pipeline as the CLI.

from typing import Any, Dict, List, Optional

try:
    from fastapi import Depends, FastAPI, Header, HTTPException
    from fastapi.responses import HTMLResponse
    from pydantic import BaseModel, Field
    _HAS_FASTAPI = True
except ImportError:  # pragma: no cover - exercised on stdlib-only installs
    _HAS_FASTAPI = False

__version__ = "0.2.0"

_INSTALL_HINT = (
    "The FastAPI service layer is an optional extra. Install it with:\n"
    '    pip install ".[api]"\n'
    "(this pulls in fastapi + uvicorn; the default Velantrim runtime stays "
    "standard-library only)."
)


def create_app():
    """Build and return the Velantrim FastAPI application.

    Raises RuntimeError with an install hint if FastAPI is not available.
    """
    if not _HAS_FASTAPI:
        raise RuntimeError(_INSTALL_HINT)

    import asyncio
    import hmac
    import os
    from importlib import resources

    from core import aio, evidence, provenance, review

    app = FastAPI(
        title="Velantrim Crystal",
        version=__version__,
        description="Verifiable, local-first AI memory — HTTP service layer.",
    )

    # ─── review token guard ────────────────────────────────────────────────────
    # With VELANTRIM_API_TOKEN set, EVERY /review/* JSON endpoint — GET and POST
    # alike — requires `Authorization: Bearer <token>`: the read endpoints expose
    # claims, sources, confidence and curator decisions, so they are no less
    # sensitive than the write ones. Constant-time comparison (hmac.compare_digest)
    # avoids token-guessing via timing. Without the env var the service keeps its
    # historical localhost-trust posture (see SECURITY.md).
    def _require_review_token(
            authorization: Optional[str] = Header(None)) -> None:
        expected = os.environ.get("VELANTRIM_API_TOKEN", "")
        if not expected:
            return
        supplied = ""
        if authorization and authorization.lower().startswith("bearer "):
            supplied = authorization[7:]
        if not hmac.compare_digest(supplied, expected):
            raise HTTPException(status_code=401,
                                detail="missing or invalid bearer token")

    _guarded = [Depends(_require_review_token)]

    # ─── request models ────────────────────────────────────────────────────────
    class IngestRequest(BaseModel):
        text: str = Field(..., min_length=1, description="The utterance to ingest.")
        source: str = "api"
        confidence: float = Field(0.6, ge=0.0, le=1.0)
        # None → auto-derived from utterance salience; explicit value wins.
        significance: Optional[float] = Field(None, ge=0.0, le=1.0)
        claim_type: Optional[str] = None
        source_status: Optional[str] = None

    class AskRequest(BaseModel):
        query: str = Field(..., min_length=1)

    class VerifyRequest(BaseModel):
        receipt: Dict[str, Any]
        strict_provenance: bool = False

    class ApproveRequest(BaseModel):
        fact_id: str = Field(..., min_length=1)
        # No default identity: force=True demands an explicit actor (422
        # otherwise); a non-force approve falls back to "curator" in
        # review.approve() for backward compatibility.
        actor: Optional[str] = Field(None, min_length=1)
        note: Optional[str] = None
        force: bool = False
        # Required (non-empty, <=500 chars) when force=True — see review.approve().
        reason: Optional[str] = Field(None, max_length=500)

    class RejectRequest(BaseModel):
        fact_id: str = Field(..., min_length=1)
        actor: str = Field("curator", min_length=1)
        reason: str = "curator_rejected"

    # ─── endpoints ───────────────────────────────────────────────────────────────
    @app.get("/health")
    async def health() -> Dict[str, Any]:
        """Liveness/readiness probe — no canon access, always cheap."""
        return {"status": "ok", "service": "velantrim-crystal", "version": __version__}

    @app.post("/ingest")
    async def ingest_endpoint(req: IngestRequest) -> Dict[str, Any]:
        """Ingest an utterance through the full Guardian + TruthGate path."""
        kwargs: Dict[str, Any] = {
            "source": req.source,
            "confidence": req.confidence,
            "significance": req.significance,
        }
        if req.claim_type is not None:
            kwargs["claim_type"] = req.claim_type
        if req.source_status is not None:
            kwargs["source_status"] = req.source_status
        try:
            return await aio.aingest(req.text, **kwargs)
        except ValueError as e:  # invalid claim_type / source_status etc.
            raise HTTPException(status_code=422, detail=str(e))

    @app.post("/ask")
    async def ask_endpoint(req: AskRequest) -> Dict[str, Any]:
        """Run the verifiable pipeline. Returns the answer or a blocked result.

        A blocked result (insufficient grounding, gate failure) is returned with
        HTTP 200 and answer=null plus an `error` field — it is a valid, expected
        outcome of a verifiable system, not a server error.
        """
        return await aio.arun(req.query)

    @app.get("/receipt")
    async def receipt_endpoint(q: str) -> Dict[str, Any]:
        """Run a query and return a replayable provenance receipt."""
        result = await aio.arun(q)
        try:
            return await asyncio.to_thread(provenance.build_receipt, result)
        except ValueError as e:  # blocked result has no answer to attest to
            raise HTTPException(status_code=422, detail=str(e))

    @app.post("/verify-receipt")
    async def verify_receipt_endpoint(req: VerifyRequest) -> Dict[str, Any]:
        """Verify a receipt and replay its citations against the current canon."""
        return await asyncio.to_thread(
            provenance.verify_receipt, req.receipt,
            strict_provenance=req.strict_provenance,
        )

    @app.get("/evidence/{fact_id}")
    async def evidence_endpoint(fact_id: str) -> List[Dict[str, Any]]:
        """List the source-span evidence records attached to a fact."""
        return await asyncio.to_thread(evidence.evidence_for, fact_id)

    # ─── curator review (WP2) ──────────────────────────────────────────────────
    # Thin wrappers over core/review.py: the same gates, ESM transitions and
    # audit events as the CLI — no new write path into L3.

    @app.get("/review/queue", dependencies=_guarded)
    async def review_queue(limit: Optional[int] = None,
                           claim_type: Optional[str] = None,
                           diagnose: bool = False) -> List[Dict[str, Any]]:
        """Pending (Observed) facts; diagnose=true adds a gate verdict per item."""
        return await asyncio.to_thread(
            review.pending, limit=limit, claim_type=claim_type, diagnose=diagnose)

    @app.get("/review/report", dependencies=_guarded)
    async def review_report_endpoint() -> Dict[str, Any]:
        """Queue health: pending count and a claim_type breakdown."""
        return await asyncio.to_thread(review.review_report)

    @app.get("/review/decisions", dependencies=_guarded)
    async def review_decisions(limit: int = 50,
                               include_claim: bool = True) -> List[Dict[str, Any]]:
        """Curator decision history reconstructed from the audit chain.
        include_claim=false keeps entries content-free (no L1 rehydration)."""
        return await asyncio.to_thread(review.decisions, limit=limit,
                                       include_claim=include_claim)

    @app.get("/review/item/{fact_id}", dependencies=_guarded)
    async def review_item_endpoint(fact_id: str) -> Dict[str, Any]:
        """One queued fact with a fresh gate diagnosis (404 if unknown)."""
        item = await asyncio.to_thread(review.review_item, fact_id)
        if not item.get("found"):
            raise HTTPException(status_code=404, detail=f"unknown fact {fact_id}")
        return item

    @app.post("/review/approve", dependencies=_guarded)
    async def review_approve(req: ApproveRequest) -> Dict[str, Any]:
        """Promote a pending fact. force=true overrides a blocking diagnosis and
        requires a non-empty reason AND an explicit actor (422 otherwise) —
        audited as review_force_approve."""
        if req.force and not (req.reason and req.reason.strip()):
            raise HTTPException(
                status_code=422,
                detail="force approval overrides a blocking diagnosis and "
                       "requires a non-empty 'reason'")
        if req.force and not (req.actor and req.actor.strip()):
            raise HTTPException(
                status_code=422,
                detail="force approval requires an explicit non-empty 'actor' "
                       "(no default identity for an override)")
        res = await asyncio.to_thread(
            review.approve, req.fact_id, actor=req.actor, note=req.note,
            force=req.force, reason=req.reason)
        if not res.get("found"):
            raise HTTPException(status_code=404,
                                detail=f"unknown fact {req.fact_id}")
        return res

    @app.post("/review/reject", dependencies=_guarded)
    async def review_reject(req: RejectRequest) -> Dict[str, Any]:
        """Reject a pending fact (Observed → Collapsed), audited."""
        res = await asyncio.to_thread(
            review.reject, req.fact_id, actor=req.actor, reason=req.reason)
        if not res.get("found"):
            raise HTTPException(status_code=404,
                                detail=f"unknown fact {req.fact_id}")
        return res

    @app.get("/review/ui", response_class=HTMLResponse)
    async def review_ui() -> str:
        """The static Kanban review shell (core/_webui/review.html).

        Deliberately UNguarded: the HTML embeds no claims, fact ids or any
        local memory content (tested) — all data is fetched client-side from
        the token-guarded /review/* JSON endpoints above.
        """
        return resources.files("core").joinpath(
            "_webui/review.html").read_text(encoding="utf-8")

    return app


def main() -> None:  # pragma: no cover - thin uvicorn launcher
    """Console-script entry point (`velantrim-api`). Runs the service via uvicorn."""
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
