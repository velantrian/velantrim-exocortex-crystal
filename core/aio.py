# core/aio.py
# Velantrim ExoCortex — async-friendly entry points.
#
# The core stores are synchronous by design (stdlib sqlite3, the L3 graph
# adapters and the embedder are all blocking). To embed Velantrim inside an
# async application (e.g. an asyncio service, a FastAPI handler, an MCP server)
# without blocking the event loop, these wrappers run the sync pipeline in the
# default thread-pool executor via asyncio.to_thread.
#
# This is an honest first step toward the "async/await throughout" roadmap item:
# the *interface* is async and event-loop friendly today; the underlying I/O is
# still synchronous and offloaded to a worker thread. This is safe across threads
# because the L0/L1 store opens a short-lived connection per operation
# (core.memory._db), and the on-disk L3 backend (SqliteL3Graph) opens its cached
# connection with check_same_thread=False and serializes access with a lock.

import asyncio
from typing import Any, Dict, Optional

from core import ingest as _ingest_mod
from core import pipeline as _pipeline_mod


async def arun(query: str, episode: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Async wrapper around pipeline.run (Query → Gate → Answer)."""
    return await asyncio.to_thread(_pipeline_mod.run, query, episode)


async def aingest(*args: Any, **kwargs: Any) -> Any:
    """Async wrapper around ingest.ingest (utterance → claim_type → gate → L3)."""
    return await asyncio.to_thread(lambda: _ingest_mod.ingest(*args, **kwargs))


async def adrain_l3_outbox(graph: Any = None) -> int:
    """Async wrapper around pipeline.drain_l3_outbox (self-heal re-merge)."""
    return await asyncio.to_thread(_pipeline_mod.drain_l3_outbox, graph)
