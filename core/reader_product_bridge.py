"""Bounded orchestration bridge over Crystal Reader RC-1..RC-3.

This module composes existing Reader primitives into one foreground run without
adding parser, model/provider, storage, ingest, TruthGate, Canon, planner, or
background-worker authority.

The bridge is deliberately execution-neutral: a caller supplies a region executor
that reports the result of actually processing a structural region. The bridge
never marks a region PROCESSED merely because it was scheduled.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Callable, Optional

from core.reader_core import CoverageState, ReaderSession, ReaderSessionState
from core.reader_passes import MultiPassReader, ReaderPassKind, ReaderPassRecord
from core.reader_structure import DocumentStructuralMap, StructuralKind, StructuralNode


class ReaderProductStatus(str, Enum):
    """User-facing projection of one bounded foreground Reader run."""

    COMPLETE = "COMPLETE"
    DEGRADED = "DEGRADED"


@dataclass(frozen=True)
class RegionReadResult:
    """Outcome returned by a caller-supplied semantic/reading executor."""

    state: CoverageState
    reason: Optional[str] = None

    def __post_init__(self) -> None:
        if not isinstance(self.state, CoverageState):
            raise ValueError("state must be a CoverageState")
        if self.reason is not None:
            reason = self.reason.strip()
            if not reason:
                raise ValueError("reason must be non-empty when provided")
            object.__setattr__(self, "reason", reason)


RegionExecutor = Callable[
    [ReaderPassKind, StructuralNode, CoverageState],
    RegionReadResult,
]


@dataclass(frozen=True)
class ReaderProductResult:
    """Read-side result; never evidence admission or Canon authority."""

    status: ReaderProductStatus
    session: ReaderSession
    passes: tuple[ReaderPassRecord, ...]
    reread_node_ids: tuple[str, ...]
    unresolved_node_ids: tuple[str, ...]

    @property
    def complete(self) -> bool:
        return self.status is ReaderProductStatus.COMPLETE


class ReaderProductBridge:
    """One bounded Reader orchestration path over an existing structural map.

    v0.1 executes exactly:

    1. one BROAD_READ pass over every non-DOCUMENT structural node;
    2. at most one TARGETED_REREAD pass over bridge-target regions left NEEDS_REVIEW;
    3. fail-closed completion: any remaining session-visible UNREAD/NEEDS_REVIEW
       region degrades the session and the result.

    No semantic work is invented here. ``executor`` owns the actual region
    processing and must return an explicit coverage outcome for every scheduled
    region. Existing RC-3 transition rules remain the enforcement boundary.
    """

    __slots__ = ("_session", "_structure", "_reader")

    def __init__(self, session: ReaderSession, structure: DocumentStructuralMap) -> None:
        if not isinstance(session, ReaderSession):
            raise ValueError("session must be a ReaderSession")
        if not isinstance(structure, DocumentStructuralMap):
            raise ValueError("structure must be a DocumentStructuralMap")
        if session.state is not ReaderSessionState.OPEN:
            raise ValueError("Reader product bridge requires an OPEN ReaderSession")
        if not session.source.same_version(structure.source):
            raise ValueError("ReaderSession and structural map must use the same source version")
        self._session = session
        self._structure = structure
        self._reader = MultiPassReader(session, structure)

    @property
    def reader(self) -> MultiPassReader:
        return self._reader

    def run(self, executor: RegionExecutor) -> ReaderProductResult:
        if not callable(executor):
            raise ValueError("executor must be callable")
        if self._session.state is not ReaderSessionState.OPEN:
            raise ValueError("Reader product run requires an OPEN ReaderSession")

        targets = tuple(
            node for node in self._structure.nodes if node.kind is not StructuralKind.DOCUMENT
        )
        target_ids = tuple(node.node_id for node in targets)
        if not targets:
            self._session.degrade("reader_product_no_readable_regions")
            return self._result((), ())

        broad = self._reader.begin_pass(
            "product-broad-read",
            ReaderPassKind.BROAD_READ,
            target_ids,
            rationale="bounded product broad read",
        )
        try:
            for node in targets:
                before = self._session.coverage[node.node_id].state
                outcome = self._execute(executor, ReaderPassKind.BROAD_READ, node, before)
                self._reader.record_region(
                    broad.pass_id,
                    node.node_id,
                    outcome.state,
                    reason=outcome.reason,
                )
            self._reader.complete_pass(broad.pass_id)
        except Exception as exc:
            if self._reader.active_pass_id == broad.pass_id:
                self._reader.degrade_pass(broad.pass_id, f"executor failure: {type(exc).__name__}")
            self._session.degrade("reader_product_broad_read_failed")
            raise

        coverage = self._session.coverage
        reread_nodes = tuple(
            self._structure.get(region_id)
            for region_id in target_ids
            if coverage[region_id].state is CoverageState.NEEDS_REVIEW
        )

        if reread_nodes:
            reread = self._reader.begin_pass(
                "product-targeted-reread",
                ReaderPassKind.TARGETED_REREAD,
                [node.node_id for node in reread_nodes],
                rationale="single bounded reread for unresolved regions",
            )
            try:
                for node in reread_nodes:
                    before = self._session.coverage[node.node_id].state
                    outcome = self._execute(
                        executor,
                        ReaderPassKind.TARGETED_REREAD,
                        node,
                        before,
                    )
                    self._reader.record_region(
                        reread.pass_id,
                        node.node_id,
                        outcome.state,
                        reason=outcome.reason,
                    )
                self._reader.complete_pass(reread.pass_id)
            except Exception as exc:
                if self._reader.active_pass_id == reread.pass_id:
                    self._reader.degrade_pass(
                        reread.pass_id,
                        f"executor failure: {type(exc).__name__}",
                    )
                self._session.degrade("reader_product_targeted_reread_failed")
                raise

        unresolved = tuple(
            region_id
            for region_id, entry in self._session.coverage.items()
            if entry.state in {CoverageState.UNREAD, CoverageState.NEEDS_REVIEW}
        )
        reread_ids = tuple(node.node_id for node in reread_nodes)
        if unresolved:
            self._session.degrade("reader_product_incomplete_after_bounded_reread")
        else:
            self._session.finish()
        return self._result(reread_ids, unresolved)

    @staticmethod
    def _execute(
        executor: RegionExecutor,
        kind: ReaderPassKind,
        node: StructuralNode,
        before: CoverageState,
    ) -> RegionReadResult:
        outcome = executor(kind, node, before)
        if not isinstance(outcome, RegionReadResult):
            raise ValueError("executor must return RegionReadResult")
        return outcome

    def _result(
        self,
        reread_node_ids: tuple[str, ...],
        unresolved_node_ids: tuple[str, ...],
    ) -> ReaderProductResult:
        status = (
            ReaderProductStatus.COMPLETE
            if self._session.state is ReaderSessionState.COMPLETED
            else ReaderProductStatus.DEGRADED
        )
        return ReaderProductResult(
            status=status,
            session=self._session,
            passes=self._reader.records,
            reread_node_ids=reread_node_ids,
            unresolved_node_ids=unresolved_node_ids,
        )


__all__ = [
    "ReaderProductBridge",
    "ReaderProductResult",
    "ReaderProductStatus",
    "RegionExecutor",
    "RegionReadResult",
]
