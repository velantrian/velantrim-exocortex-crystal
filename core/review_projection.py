"""Idempotent L3 projector for durable curator decisions."""
from __future__ import annotations

import argparse
import json
from typing import Any, Optional, Sequence

from core import memory
from core.l3_graph import get_l3_graph
from core.review_decision_store import (
    get_review_decision,
    list_projection_work,
    mark_projection_result,
    projection_health,
)


class ProjectionBlocked(RuntimeError):
    """Projection is unsafe until an operator resolves current participant state."""


def _participant_fact(participant: dict[str, Any]) -> dict[str, Any]:
    fact_id = participant.get("fact_id")
    if not isinstance(fact_id, str) or not fact_id:
        raise ProjectionBlocked("malformed projection participant")
    if memory.get_tombstone(fact_id) is not None:
        raise ProjectionBlocked(f"participant {fact_id!r} was erased")
    fact = memory.get_fact(fact_id)
    if fact is None:
        raise ProjectionBlocked(f"participant {fact_id!r} no longer exists")
    if fact.get("restricted"):
        raise ProjectionBlocked(f"participant {fact_id!r} is restricted")
    required_state = participant.get("required_state")
    if required_state is not None and fact.get("epistemic_state") != required_state:
        raise ProjectionBlocked(
            f"participant {fact_id!r} state changed from required {required_state!r}"
        )
    return fact


def project_review_decision(decision_id: str) -> dict[str, Any]:
    """Apply one stored projection command; safe to call repeatedly."""
    decision = get_review_decision(decision_id)
    if decision is None:
        return {
            "ok": False,
            "decision_id": decision_id,
            "projection_status": "missing",
            "reason": "decision not found",
        }
    if decision["projection_status"] == "completed":
        return {
            "ok": True,
            "decision_id": decision_id,
            "projection_status": "completed",
            "attempts": decision["attempts"],
            "idempotent": True,
        }

    projection = decision["payload"].get("projection") or {}
    if not projection:
        completed = mark_projection_result(decision_id, status="completed")
        return {
            "ok": True,
            "decision_id": decision_id,
            "projection_status": "completed",
            "attempts": completed["attempts"],
        }

    try:
        participants = list(projection.get("participants") or [])
        facts: dict[str, dict[str, Any]] = {}
        for participant in participants:
            fact = _participant_fact(dict(participant))
            facts[fact["fact_id"]] = fact

        graph = get_l3_graph()
        # Import lazily to avoid making the projection module part of pipeline's
        # import cycle. Projection is an admitted-decision consumer, not a gate.
        from core.pipeline import _l3_payload

        for participant in participants:
            participant = dict(participant)
            if not participant.get("merge"):
                continue
            fact_id = participant["fact_id"]
            fact = facts[fact_id]
            payload = _l3_payload(fact)
            explicit_truth = participant.get("truth_status")
            if explicit_truth is not None:
                payload["truth_status"] = explicit_truth
            elif participant.get("preserve_truth_status"):
                existing = graph.get_fact(fact_id) or {}
                if "truth_status" in existing:
                    payload["truth_status"] = existing["truth_status"]
            graph.merge_fact(payload)

        for edge in projection.get("edges") or []:
            edge = dict(edge)
            graph.add_edge(
                edge["src"], edge["rel_type"], edge["dst"], dict(edge.get("props") or {})
            )

        completed = mark_projection_result(decision_id, status="completed")
        return {
            "ok": True,
            "decision_id": decision_id,
            "projection_status": "completed",
            "attempts": completed["attempts"],
            "idempotent": False,
        }
    except ProjectionBlocked as exc:
        blocked = mark_projection_result(
            decision_id, status="blocked", error=str(exc)
        )
        return {
            "ok": False,
            "decision_id": decision_id,
            "projection_status": "blocked",
            "attempts": blocked["attempts"],
            "reason": str(exc),
        }
    except Exception as exc:  # backend failure stays durable and retryable
        failed = mark_projection_result(
            decision_id,
            status="failed",
            error=f"{type(exc).__name__}: {exc}",
        )
        return {
            "ok": False,
            "decision_id": decision_id,
            "projection_status": "failed",
            "attempts": failed["attempts"],
            "reason": failed["last_error"],
        }


def drain_review_projections(limit: int = 100) -> dict[str, Any]:
    """Retry pending/failed/blocked commands in deterministic enqueue order."""
    results = [
        project_review_decision(item["decision_id"])
        for item in list_projection_work(limit=limit)
    ]
    return {
        "processed": len(results),
        "completed": sum(r.get("projection_status") == "completed" for r in results),
        "failed": sum(r.get("projection_status") == "failed" for r in results),
        "blocked": sum(r.get("projection_status") == "blocked" for r in results),
        "results": results,
    }


def review_projection_health() -> dict[str, Any]:
    return projection_health()


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Operator CLI for content-light projection status and recovery."""
    parser = argparse.ArgumentParser(prog="python -m core.review_projection")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status", help="show content-light curator projection health")
    drain = sub.add_parser("drain", help="retry pending/failed/blocked projections")
    drain.add_argument("--limit", type=int, default=100)
    args = parser.parse_args(argv)
    result = (
        review_projection_health()
        if args.command == "status"
        else drain_review_projections(limit=args.limit)
    )
    print(json.dumps(result, sort_keys=True, ensure_ascii=False))
    return 0


__all__ = [
    "ProjectionBlocked",
    "drain_review_projections",
    "project_review_decision",
    "review_projection_health",
    "main",
]


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
