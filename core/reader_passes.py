"""Deterministic multi-pass reading mechanics for Reader Core RC-3.

RC-3 records what reading pass was attempted over which source-linked structural
regions and how that pass affected RC-1 coverage. It deliberately contains no
model/provider call, parser, retrieval stack, storage authority, ingest path,
TruthGate/Canon integration, contradiction resolution, planner, or background
worker.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
from typing import Dict, Iterable, Optional

from core.reader_core import (
    CoverageEntry,
    CoverageState,
    ReaderSession,
    ReaderSessionState,
    SourceVersion,
)
from core.reader_structure import (
    DocumentStructuralMap,
    StructuralNode,
    StructuralStatus,
)


class ReaderPassKind(str, Enum):
    """Pass categories allowed by the RC-0 multi-pass contract."""

    ORIENTATION = "ORIENTATION"
    BROAD_READ = "BROAD_READ"
    FOCUSED_READ = "FOCUSED_READ"
    CROSS_CHECK = "CROSS_CHECK"
    TARGETED_REREAD = "TARGETED_REREAD"


class ReaderPassState(str, Enum):
    """Lifecycle of one declared pass attempt."""

    ATTEMPTED = "ATTEMPTED"
    COMPLETED = "COMPLETED"
    INTERRUPTED = "INTERRUPTED"
    DEGRADED = "DEGRADED"


def _required_text(value: str, field_name: str) -> str:
    value = (value or "").strip()
    if not value:
        raise ValueError(f"{field_name} must be non-empty")
    return value


@dataclass(frozen=True)
class RegionPassOutcome:
    """One explicit coverage effect produced by one pass over one structural node."""

    node_id: str
    before: CoverageState
    after: CoverageState
    reason: Optional[str] = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "node_id", _required_text(self.node_id, "node_id"))
        if not isinstance(self.before, CoverageState):
            raise ValueError("before must be a CoverageState")
        if not isinstance(self.after, CoverageState):
            raise ValueError("after must be a CoverageState")
        if self.reason is not None:
            object.__setattr__(self, "reason", _required_text(self.reason, "reason"))


@dataclass(frozen=True)
class ReaderPassRecord:
    """Immutable audit record for one pass attempt."""

    pass_id: str
    session_id: str
    source: SourceVersion
    kind: ReaderPassKind
    target_node_ids: tuple[str, ...]
    state: ReaderPassState
    rationale: Optional[str] = None
    outcomes: tuple[RegionPassOutcome, ...] = ()
    reason: Optional[str] = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "pass_id", _required_text(self.pass_id, "pass_id"))
        object.__setattr__(self, "session_id", _required_text(self.session_id, "session_id"))
        if not isinstance(self.source, SourceVersion):
            raise ValueError("source must be a SourceVersion")
        if not isinstance(self.kind, ReaderPassKind):
            raise ValueError("kind must be a ReaderPassKind")
        targets = tuple(
            _required_text(node_id, "target_node_id") for node_id in self.target_node_ids
        )
        if not targets:
            raise ValueError("a Reader pass requires at least one target node")
        if len(set(targets)) != len(targets):
            raise ValueError("target_node_ids must be unique")
        object.__setattr__(self, "target_node_ids", targets)
        if not isinstance(self.state, ReaderPassState):
            raise ValueError("state must be a ReaderPassState")
        if self.rationale is not None:
            object.__setattr__(self, "rationale", _required_text(self.rationale, "rationale"))
        outcomes = tuple(self.outcomes)
        for outcome in outcomes:
            if not isinstance(outcome, RegionPassOutcome):
                raise ValueError("outcomes must contain RegionPassOutcome values")
            if outcome.node_id not in targets:
                raise ValueError("pass outcome must belong to a declared target node")
        if len({outcome.node_id for outcome in outcomes}) != len(outcomes):
            raise ValueError("a pass cannot record multiple outcomes for one target node")
        object.__setattr__(self, "outcomes", outcomes)
        if self.reason is not None:
            object.__setattr__(self, "reason", _required_text(self.reason, "reason"))
        if (
            self.state in {ReaderPassState.INTERRUPTED, ReaderPassState.DEGRADED}
            and self.reason is None
        ):
            raise ValueError(f"{self.state.value} pass requires an explicit reason")
        if self.state is ReaderPassState.ATTEMPTED and self.reason is not None:
            raise ValueError("ATTEMPTED pass must not carry a terminal reason")
        if self.state is ReaderPassState.COMPLETED and len(outcomes) != len(targets):
            raise ValueError("COMPLETED pass requires an outcome for every target node")

    @property
    def restricted(self) -> bool:
        return self.source.restricted

    @property
    def sensitivity(self) -> Optional[str]:
        return self.source.sensitivity


@dataclass(frozen=True)
class MultiPassTelemetry:
    """Pass counts only; deliberately no comprehension or truth percentage."""

    total_passes: int
    completed_passes: int
    unresolved_passes: int
    active_pass_id: Optional[str]
    kind_counts: Dict[ReaderPassKind, int]
    state_counts: Dict[ReaderPassState, int]


class MultiPassReader:
    """Sequential RC-3 pass controller over one RC-1 session and RC-2 map."""

    __slots__ = ("_session", "_structure", "_records", "_record_index", "_active_pass_id")

    def __init__(self, session: ReaderSession, structure: DocumentStructuralMap) -> None:
        if not isinstance(session, ReaderSession):
            raise ValueError("session must be a ReaderSession")
        if not isinstance(structure, DocumentStructuralMap):
            raise ValueError("structure must be a DocumentStructuralMap")
        if session.state is not ReaderSessionState.OPEN:
            raise ValueError("RC-3 requires an OPEN ReaderSession")
        if not session.source.same_version(structure.source):
            raise ValueError("ReaderSession and structural map must use the same source version")
        self._session = session
        self._structure = structure
        self._records: list[ReaderPassRecord] = []
        self._record_index: Dict[str, int] = {}
        self._active_pass_id: Optional[str] = None

    @property
    def session(self) -> ReaderSession:
        return self._session

    @property
    def structure(self) -> DocumentStructuralMap:
        return self._structure

    @property
    def records(self) -> tuple[ReaderPassRecord, ...]:
        return tuple(self._records)

    @property
    def active_pass_id(self) -> Optional[str]:
        return self._active_pass_id

    def get_pass(self, pass_id: str) -> ReaderPassRecord:
        pass_id = _required_text(pass_id, "pass_id")
        try:
            return self._records[self._record_index[pass_id]]
        except KeyError as exc:
            raise KeyError(pass_id) from exc

    def begin_pass(
        self,
        pass_id: str,
        kind: ReaderPassKind,
        target_node_ids: Iterable[str],
        *,
        rationale: Optional[str] = None,
    ) -> ReaderPassRecord:
        self._require_session_open()
        pass_id = _required_text(pass_id, "pass_id")
        if not isinstance(kind, ReaderPassKind):
            raise ValueError("kind must be a ReaderPassKind")
        if pass_id in self._record_index:
            raise ValueError(f"duplicate Reader pass_id: {pass_id}")
        if self._active_pass_id is not None:
            raise ValueError(f"Reader pass already active: {self._active_pass_id}")
        if isinstance(target_node_ids, (str, bytes)):
            raise ValueError("target_node_ids must be an iterable of node ids")
        try:
            targets = tuple(
                _required_text(node_id, "target_node_id") for node_id in target_node_ids
            )
        except TypeError as exc:
            raise ValueError("target_node_ids must be an iterable of node ids") from exc
        if not targets:
            raise ValueError("a Reader pass requires at least one target node")
        if len(set(targets)) != len(targets):
            raise ValueError("target_node_ids must be unique")
        if kind is ReaderPassKind.CROSS_CHECK and len(targets) < 2:
            raise ValueError("CROSS_CHECK requires at least two target nodes")
        validated_rationale = (
            _required_text(rationale, "rationale") if rationale is not None else None
        )
        if kind is ReaderPassKind.TARGETED_REREAD and validated_rationale is None:
            raise ValueError("TARGETED_REREAD requires an explicit rationale")

        nodes = tuple(self._structure.get(node_id) for node_id in targets)
        coverage = self._session.coverage
        for node in nodes:
            existing = coverage.get(node.node_id)
            if existing is not None and (
                existing.locator is None
                or existing.locator.replay_key != node.locator.replay_key
            ):
                raise ValueError("coverage region does not match structural node locator")
        for node in nodes:
            if node.node_id not in coverage:
                self._session.set_coverage(
                    CoverageEntry(
                        region_id=node.node_id,
                        state=CoverageState.UNREAD,
                        locator=node.locator,
                    )
                )

        record = ReaderPassRecord(
            pass_id=pass_id,
            session_id=self._session.session_id,
            source=self._session.source,
            kind=kind,
            target_node_ids=targets,
            state=ReaderPassState.ATTEMPTED,
            rationale=validated_rationale,
        )
        self._record_index[pass_id] = len(self._records)
        self._records.append(record)
        self._active_pass_id = pass_id
        return record

    def record_region(
        self,
        pass_id: str,
        node_id: str,
        target: CoverageState,
        *,
        reason: Optional[str] = None,
    ) -> RegionPassOutcome:
        self._require_session_open()
        record = self._require_active(pass_id)
        node_id = _required_text(node_id, "node_id")
        if node_id not in record.target_node_ids:
            raise ValueError("region is not a declared target of the active pass")
        if any(outcome.node_id == node_id for outcome in record.outcomes):
            raise ValueError("region already has an outcome in this pass")
        if not isinstance(target, CoverageState):
            raise ValueError("target must be a CoverageState")

        node = self._structure.get(node_id)
        before = self._session.coverage[node_id].state
        self._validate_effect(record.kind, node, before, target)
        updated = self._session.transition_coverage(node_id, target, reason=reason)
        outcome = RegionPassOutcome(
            node_id=node_id,
            before=before,
            after=updated.state,
            reason=updated.reason,
        )
        self._replace_record(record, replace(record, outcomes=record.outcomes + (outcome,)))
        return outcome

    def complete_pass(self, pass_id: str) -> ReaderPassRecord:
        self._require_session_open()
        record = self._require_active(pass_id)
        if {outcome.node_id for outcome in record.outcomes} != set(record.target_node_ids):
            raise ValueError("cannot complete pass with unrecorded target regions")
        completed = replace(record, state=ReaderPassState.COMPLETED)
        self._replace_record(record, completed)
        self._active_pass_id = None
        return completed

    def interrupt_pass(self, pass_id: str, reason: str) -> ReaderPassRecord:
        return self._terminate_pass(pass_id, ReaderPassState.INTERRUPTED, reason)

    def degrade_pass(self, pass_id: str, reason: str) -> ReaderPassRecord:
        return self._terminate_pass(pass_id, ReaderPassState.DEGRADED, reason)

    def telemetry(self) -> MultiPassTelemetry:
        kind_counts = {kind: 0 for kind in ReaderPassKind}
        state_counts = {state: 0 for state in ReaderPassState}
        for record in self._records:
            kind_counts[record.kind] += 1
            state_counts[record.state] += 1
        unresolved = (
            state_counts[ReaderPassState.ATTEMPTED]
            + state_counts[ReaderPassState.INTERRUPTED]
            + state_counts[ReaderPassState.DEGRADED]
        )
        return MultiPassTelemetry(
            total_passes=len(self._records),
            completed_passes=state_counts[ReaderPassState.COMPLETED],
            unresolved_passes=unresolved,
            active_pass_id=self._active_pass_id,
            kind_counts=kind_counts,
            state_counts=state_counts,
        )

    def _require_session_open(self) -> None:
        if self._session.state is not ReaderSessionState.OPEN:
            raise ValueError(f"RC-3 session is no longer OPEN: {self._session.state.value}")

    def _require_active(self, pass_id: str) -> ReaderPassRecord:
        pass_id = _required_text(pass_id, "pass_id")
        if self._active_pass_id != pass_id:
            raise ValueError("pass is not the active Reader pass")
        record = self.get_pass(pass_id)
        if record.state is not ReaderPassState.ATTEMPTED:
            raise ValueError("active Reader pass is not ATTEMPTED")
        return record

    def _replace_record(self, old: ReaderPassRecord, new: ReaderPassRecord) -> None:
        self._records[self._record_index[old.pass_id]] = new

    def _terminate_pass(
        self,
        pass_id: str,
        state: ReaderPassState,
        reason: str,
    ) -> ReaderPassRecord:
        self._require_session_open()
        record = self._require_active(pass_id)
        terminal = replace(
            record,
            state=state,
            reason=_required_text(reason, "reason"),
        )
        self._replace_record(record, terminal)
        self._active_pass_id = None
        return terminal

    @staticmethod
    def _validate_effect(
        kind: ReaderPassKind,
        node: StructuralNode,
        before: CoverageState,
        target: CoverageState,
    ) -> None:
        if node.status is not StructuralStatus.RECOVERED:
            if target is not CoverageState.NEEDS_REVIEW:
                raise ValueError("unresolved structural regions must remain NEEDS_REVIEW")
            return

        if kind is ReaderPassKind.ORIENTATION:
            if target not in {CoverageState.SEEN, CoverageState.NEEDS_REVIEW}:
                raise ValueError("ORIENTATION may only produce SEEN or NEEDS_REVIEW")
            return

        if kind is ReaderPassKind.BROAD_READ:
            if target not in {CoverageState.PROCESSED, CoverageState.NEEDS_REVIEW}:
                raise ValueError("BROAD_READ may only produce PROCESSED or NEEDS_REVIEW")
            return

        if kind is ReaderPassKind.FOCUSED_READ:
            if before in {CoverageState.UNREAD, CoverageState.SEEN}:
                allowed = {CoverageState.PROCESSED, CoverageState.NEEDS_REVIEW}
            else:
                allowed = {CoverageState.REVISITED, CoverageState.NEEDS_REVIEW}
            if target not in allowed:
                raise ValueError("FOCUSED_READ outcome is incompatible with prior coverage")
            return

        if kind in {ReaderPassKind.CROSS_CHECK, ReaderPassKind.TARGETED_REREAD}:
            if before in {CoverageState.UNREAD, CoverageState.SEEN}:
                raise ValueError(f"{kind.value} requires substantive prior processing")
            if target not in {CoverageState.REVISITED, CoverageState.NEEDS_REVIEW}:
                raise ValueError(f"{kind.value} may only produce REVISITED or NEEDS_REVIEW")
            return

        raise ValueError("unsupported Reader pass kind")
