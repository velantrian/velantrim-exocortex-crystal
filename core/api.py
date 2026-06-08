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
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel, Field
    _HAS_FASTAPI = True
except ImportError:  # pragma: no cover - exercised on stdlib-only installs
    _HAS_FASTAPI = False

__version__ = "0.1.0"

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

    from core import aio, evidence, provenance

    app = FastAPI(
        title="Velantrim Crystal",
        version=__version__,
        description="Verifiable, local-first AI memory — HTTP service layer.",
    )

    # ─── request models ────────────────────────────────────────────────────────
    class IngestRequest(BaseModel):
        text: str = Field(..., min_length=1, description="The utterance to ingest.")
        source: str = "api"
        confidence: float = Field(0.6, ge=0.0, le=1.0)
        significance: float = Field(0.5, ge=0.0, le=1.0)
        claim_type: Optional[str] = None
        source_status: Optional[str] = None

    class AskRequest(BaseModel):
        query: str = Field(..., min_length=1)

    class VerifyRequest(BaseModel):
        receipt: Dict[str, Any]
        strict_provenance: bool = False

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
