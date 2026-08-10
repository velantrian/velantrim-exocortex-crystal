"""Minimal evidence-linked Reader Core domain skeleton (RC-1).

This module intentionally contains no storage, ingest, TruthGate, Canon, planner,
model-provider, embedding, or background-worker integration. It models source-bound
reader state only. Reader artifacts are observations/candidates, never truth admission.

The source identity conventions mirror ``core.evidence``: source URI, SHA-256 content
hash, and half-open character spans. Source body text is never retained by these
objects.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, replace
from enum import Enum
from typing import Dict, Optional

_SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")


class SourceFidelity(str, Enum):
    """How a Reader statement relates to its source."""

    DIRECT_SOURCE_OBSERVATION = "DIRECT_SOURCE_OBSERVATION"
    EXTRACTED_PROPOSITION = "EXTRACTED_PROPOSITION"
    READER_INTERPRETATION = "READER_INTERPRETATION"
    SUMMARY = "SUMMARY"
    INFERENCE = "INFERENCE"


class CoverageState(str, Enum):
    """Objective-specific reading coverage, not a comprehension score."""

    UNREAD = "UNREAD"
    SEEN = "SEEN"
    PROCESSED = "PROCESSED"
    REVISITED = "REVISITED"
    NEEDS_REVIEW = "NEEDS_REVIEW"


class ReaderSessionState(str, Enum):
    """Lifecycle of one bounded reading attempt."""

    OPEN = "OPEN"
    COMPLETED = "COMPLETED"
    INTERRUPTED = "INTERRUPTED"
    DEGRADED = "DEGRADED"
    STALE = "STALE"


def source_sha256(text: str) -> str:
    """Return the same UTF-8 SHA-256 convention used by ``core.evidence``."""

    return hashlib.sha256((text or "").encode("utf-8")).hexdigest()


def _required_text(value: str, field_name: str) -> str:
    value = (value or "").strip()
    if not value:
        raise ValueError(f"{field_name} must be non-empty")
    return value


@dataclass(frozen=True)
class SourceVersion:
    """One immutable Reader binding to one identified source version."""

    document_id: str
    source_uri: str
    source_sha256: str
    restricted: bool = False
    sensitivity: Optional[str] = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "document_id", _required_text(self.document_id, "document_id"))
        object.__setattr__(self, "source_uri", _required_text(self.source_uri, "source_uri"))
        digest = (self.source_sha256 or "").strip()
        if not _SHA256_RE.fullmatch(digest):
            raise ValueError("source_sha256 must be a 64-character hexadecimal SHA-256")
        object.__setattr__(self, "source_sha256", digest.lower())
        if not isinstance(self.restricted, bool):
            raise ValueError("restricted must be a bool")
        if self.sensitivity is not None:
            object.__setattr__(
                self, "sensitivity", _required_text(self.sensitivity, "sensitivity")
            )

    @classmethod
    def from_text(
        cls,
        document_id: str,
        source_uri: str,
        source_text: str,
        *,
        restricted: bool = False,
        sensitivity: Optional[str] = None,
    ) -> "SourceVersion":
        """Hash source text transiently; the returned object does not retain it."""

        return cls(
            document_id=document_id,
            source_uri=source_uri,
            source_sha256=source_sha256(source_text),
            restricted=restricted,
            sensitivity=sensitivity,
        )

    def same_version(self, other: "SourceVersion") -> bool:
        return isinstance(other, SourceVersion) and (
            self.document_id == other.document_id
            and self.source_uri == other.source_uri
            and self.source_sha256 == other.source_sha256
        )


@dataclass(frozen=True)
class SourceLocator:
    """Replayable location inside one exact source version.

    An exact half-open character span is preferred. When exact offsets cannot be
    represented, RC-1 permits an explicitly named structural locator. At least one
    addressing mode is mandatory; a missing locator cannot become evidence-linked.
    """

    source: SourceVersion
    span_start: Optional[int] = None
    span_end: Optional[int] = None
    structural_locator: Optional[str] = None
    section: Optional[str] = None
    chunk_id: Optional[str] = None

    def __post_init__(self) -> None:
        if not isinstance(self.source, SourceVersion):
            raise ValueError("source must be a SourceVersion")
        has_start = self.span_start is not None
        has_end = self.span_end is not None
        if has_start != has_end:
            raise ValueError("span_start and span_end must be given together")
        if has_start:
            if not isinstance(self.span_start, int) or not isinstance(self.span_end, int):
                raise ValueError("span offsets must be integers")
            if self.span_start < 0 or self.span_end < 0:
                raise ValueError("span offsets must be non-negative")
            if self.span_start > self.span_end:
                raise ValueError("span_start must be <= span_end")
        locator = self.structural_locator
        if locator is not None:
            object.__setattr__(
                self,
                "structural_locator",
                _required_text(locator, "structural_locator"),
            )
        if not has_start and self.structural_locator is None:
            raise ValueError("a source span or structural_locator is required")
        if self.section is not None:
            object.__setattr__(self, "section", _required_text(self.section, "section"))
        if self.chunk_id is not None:
            object.__setattr__(self, "chunk_id", _required_text(self.chunk_id, "chunk_id"))

    @property
    def has_exact_span(self) -> bool:
        return self.span_start is not None

    @property
    def replay_key(self) -> tuple[str, str, str, Optional[int], Optional[int], Optional[str]]:
        return (
            self.source.document_id,
            self.source.source_uri,
            self.source.source_sha256,
            self.span_start,
            self.span_end,
            self.structural_locator,
        )


@dataclass(frozen=True)
class SegmentCard:
    """A source-linked Reader observation/candidate, never a Canon fact."""

    card_id: str
    locator: SourceLocator
    fidelity: SourceFidelity
    statement: str
    supporting_locators: tuple[SourceLocator, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "card_id", _required_text(self.card_id, "card_id"))
        if not isinstance(self.locator, SourceLocator):
            raise ValueError("locator must be a SourceLocator")
        if not isinstance(self.fidelity, SourceFidelity):
            raise ValueError("fidelity must be a SourceFidelity")
        object.__setattr__(self, "statement", _required_text(self.statement, "statement"))
        supports = tuple(self.supporting_locators)
        object.__setattr__(self, "supporting_locators", supports)
        for supporting in supports:
            if not isinstance(supporting, SourceLocator):
                raise ValueError("supporting locators must be SourceLocator values")
            if not self.locator.source.same_version(supporting.source):
                raise ValueError("supporting locators must use the same source version in RC-1")

    @property
    def restricted(self) -> bool:
        return self.locator.source.restricted

    @property
    def sensitivity(self) -> Optional[str]:
        return self.locator.source.sensitivity


_ALLOWED_COVERAGE_TRANSITIONS = {
    CoverageState.UNREAD: {
        CoverageState.SEEN,
        CoverageState.PROCESSED,
        CoverageState.NEEDS_REVIEW,
    },
    CoverageState.SEEN: {
        CoverageState.PROCESSED,
        CoverageState.NEEDS_REVIEW,
    },
    CoverageState.PROCESSED: {
        CoverageState.REVISITED,
        CoverageState.NEEDS_REVIEW,
    },
    CoverageState.REVISITED: {
        CoverageState.REVISITED,
        CoverageState.NEEDS_REVIEW,
    },
    CoverageState.NEEDS_REVIEW: {
        CoverageState.PROCESSED,
        CoverageState.REVISITED,
    },
}


@dataclass(frozen=True)
class CoverageEntry:
    """Version-specific state for one declared reading region."""

    region_id: str
    state: CoverageState
    locator: Optional[SourceLocator] = None
    reason: Optional[str] = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "region_id", _required_text(self.region_id, "region_id"))
        if not isinstance(self.state, CoverageState):
            raise ValueError("state must be a CoverageState")
        if self.locator is not None and not isinstance(self.locator, SourceLocator):
            raise ValueError("locator must be a SourceLocator")
        if self.reason is not None:
            object.__setattr__(self, "reason", _required_text(self.reason, "reason"))
        if self.locator is None and self.state is not CoverageState.NEEDS_REVIEW:
            raise ValueError("coverage without a locator must be NEEDS_REVIEW")
        if self.state is CoverageState.NEEDS_REVIEW and self.reason is None:
            raise ValueError("NEEDS_REVIEW coverage requires an explicit reason")

    def transition(
        self,
        target: CoverageState,
        *,
        reason: Optional[str] = None,
    ) -> "CoverageEntry":
        if not isinstance(target, CoverageState):
            raise ValueError("target must be a CoverageState")
        if target is self.state:
            if target is CoverageState.NEEDS_REVIEW and reason is not None:
                return replace(self, reason=_required_text(reason, "reason"))
            return self
        if target not in _ALLOWED_COVERAGE_TRANSITIONS[self.state]:
            raise ValueError(f"illegal coverage transition: {self.state.value} -> {target.value}")
        if target is CoverageState.NEEDS_REVIEW:
            return replace(self, state=target, reason=_required_text(reason or "", "reason"))
        if self.state is CoverageState.NEEDS_REVIEW and reason is None:
            raise ValueError("recovering NEEDS_REVIEW requires an explicit review reason")
        return replace(
            self,
            state=target,
            reason=_required_text(reason, "reason") if reason is not None else None,
        )


@dataclass(frozen=True)
class ReaderBookmark:
    bookmark_id: str
    locator: SourceLocator
    reason: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "bookmark_id", _required_text(self.bookmark_id, "bookmark_id")
        )
        if not isinstance(self.locator, SourceLocator):
            raise ValueError("locator must be a SourceLocator")
        object.__setattr__(self, "reason", _required_text(self.reason, "reason"))

    @property
    def restricted(self) -> bool:
        return self.locator.source.restricted

    @property
    def sensitivity(self) -> Optional[str]:
        return self.locator.source.sensitivity


@dataclass(frozen=True)
class OpenLoop:
    loop_id: str
    locator: SourceLocator
    question: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "loop_id", _required_text(self.loop_id, "loop_id"))
        if not isinstance(self.locator, SourceLocator):
            raise ValueError("locator must be a SourceLocator")
        object.__setattr__(self, "question", _required_text(self.question, "question"))

    @property
    def restricted(self) -> bool:
        return self.locator.source.restricted

    @property
    def sensitivity(self) -> Optional[str]:
        return self.locator.source.sensitivity


@dataclass(frozen=True)
class CoverageTelemetry:
    """Counts only. Deliberately exposes no comprehension percentage."""

    counts: Dict[CoverageState, int]
    total_regions: int
    unresolved_regions: int
    missing_locator_regions: int

    @property
    def has_visible_gaps(self) -> bool:
        return self.unresolved_regions > 0


@dataclass(frozen=True)
class InvalidationReport:
    old_source_sha256: str
    new_source_sha256: str
    stale: bool
    scope: str
    invalidated_regions: int
    invalidated_artifacts: int


class ReaderSession:
    """Bounded, non-authoritative reading attempt over one source version.

    Identity and artifact collections are deliberately encapsulated. Callers receive
    immutable tuples or a copied coverage mapping so the same-version checks cannot be
    bypassed by mutating public containers.
    """

    __slots__ = (
        "_session_id",
        "_source",
        "_objective",
        "_state",
        "_state_reason",
        "_coverage",
        "_segment_cards",
        "_bookmarks",
        "_open_loops",
    )

    def __init__(
        self,
        session_id: str,
        source: SourceVersion,
        objective: str,
        state: ReaderSessionState = ReaderSessionState.OPEN,
        state_reason: Optional[str] = None,
    ) -> None:
        self._session_id = _required_text(session_id, "session_id")
        if not isinstance(source, SourceVersion):
            raise ValueError("source must be a SourceVersion")
        self._source = source
        self._objective = _required_text(objective, "objective")
        if not isinstance(state, ReaderSessionState):
            raise ValueError("state must be a ReaderSessionState")
        self._state = state
        self._state_reason = (
            _required_text(state_reason, "state_reason") if state_reason is not None else None
        )
        self._coverage: Dict[str, CoverageEntry] = {}
        self._segment_cards: list[SegmentCard] = []
        self._bookmarks: list[ReaderBookmark] = []
        self._open_loops: list[OpenLoop] = []

    @property
    def session_id(self) -> str:
        return self._session_id

    @property
    def source(self) -> SourceVersion:
        return self._source

    @property
    def objective(self) -> str:
        return self._objective

    @property
    def state(self) -> ReaderSessionState:
        return self._state

    @property
    def state_reason(self) -> Optional[str]:
        return self._state_reason

    @property
    def coverage(self) -> Dict[str, CoverageEntry]:
        return dict(self._coverage)

    @property
    def segment_cards(self) -> tuple[SegmentCard, ...]:
        return tuple(self._segment_cards)

    @property
    def bookmarks(self) -> tuple[ReaderBookmark, ...]:
        return tuple(self._bookmarks)

    @property
    def open_loops(self) -> tuple[OpenLoop, ...]:
        return tuple(self._open_loops)

    def _require_source(self, locator: SourceLocator) -> None:
        if not self._source.same_version(locator.source):
            raise ValueError("reader artifact belongs to a different source version")

    def add_segment_card(self, card: SegmentCard) -> None:
        self._require_open("add segment card to")
        if not isinstance(card, SegmentCard):
            raise ValueError("card must be a SegmentCard")
        self._require_source(card.locator)
        self._segment_cards.append(card)

    def set_coverage(self, entry: CoverageEntry) -> None:
        self._require_open("set coverage on")
        if not isinstance(entry, CoverageEntry):
            raise ValueError("entry must be a CoverageEntry")
        if entry.locator is not None:
            self._require_source(entry.locator)
        self._coverage[entry.region_id] = entry

    def transition_coverage(
        self,
        region_id: str,
        target: CoverageState,
        *,
        reason: Optional[str] = None,
    ) -> CoverageEntry:
        self._require_open("transition coverage on")
        region_id = _required_text(region_id, "region_id")
        if region_id not in self._coverage:
            raise KeyError(region_id)
        updated = self._coverage[region_id].transition(target, reason=reason)
        self._coverage[region_id] = updated
        return updated

    def add_bookmark(self, bookmark: ReaderBookmark) -> None:
        self._require_open("add bookmark to")
        if not isinstance(bookmark, ReaderBookmark):
            raise ValueError("bookmark must be a ReaderBookmark")
        self._require_source(bookmark.locator)
        self._bookmarks.append(bookmark)

    def add_open_loop(self, open_loop: OpenLoop) -> None:
        self._require_open("add open loop to")
        if not isinstance(open_loop, OpenLoop):
            raise ValueError("open_loop must be an OpenLoop")
        self._require_source(open_loop.locator)
        self._open_loops.append(open_loop)

    def coverage_telemetry(self) -> CoverageTelemetry:
        counts = {state: 0 for state in CoverageState}
        missing_locator = 0
        for entry in self._coverage.values():
            counts[entry.state] += 1
            if entry.locator is None:
                missing_locator += 1
        unresolved = counts[CoverageState.UNREAD] + counts[CoverageState.NEEDS_REVIEW]
        return CoverageTelemetry(
            counts=counts,
            total_regions=len(self._coverage),
            unresolved_regions=unresolved,
            missing_locator_regions=missing_locator,
        )

    def finish(self) -> None:
        self._require_open("finish")
        self._state = ReaderSessionState.COMPLETED
        self._state_reason = None

    def interrupt(self, reason: str) -> None:
        self._require_open("interrupt")
        validated_reason = _required_text(reason, "reason")
        self._state = ReaderSessionState.INTERRUPTED
        self._state_reason = validated_reason

    def degrade(self, reason: str) -> None:
        if self._state is ReaderSessionState.STALE:
            raise ValueError("cannot degrade a stale session")
        validated_reason = _required_text(reason, "reason")
        self._state = ReaderSessionState.DEGRADED
        self._state_reason = validated_reason

    def _require_open(self, operation: str) -> None:
        if self._state is not ReaderSessionState.OPEN:
            raise ValueError(f"cannot {operation} session in state {self._state.value}")

    def invalidate_for(self, new_source: SourceVersion) -> InvalidationReport:
        """Conservatively stale the whole session when exact source binding changes.

        RC-1 intentionally has no diff/remapping engine. Historical artifacts remain
        untouched and continue to point at the old source version; they simply cannot be
        treated as current coverage for ``new_source``.
        """

        if not isinstance(new_source, SourceVersion):
            raise ValueError("new_source must be a SourceVersion")
        if new_source.document_id != self._source.document_id:
            raise ValueError("cannot invalidate a session against a different document_id")
        if self._source.same_version(new_source):
            return InvalidationReport(
                old_source_sha256=self._source.source_sha256,
                new_source_sha256=new_source.source_sha256,
                stale=False,
                scope="none",
                invalidated_regions=0,
                invalidated_artifacts=0,
            )
        self._state = ReaderSessionState.STALE
        self._state_reason = "source version changed; RC-1 has no proven remapping"
        return InvalidationReport(
            old_source_sha256=self._source.source_sha256,
            new_source_sha256=new_source.source_sha256,
            stale=True,
            scope="all",
            invalidated_regions=len(self._coverage),
            invalidated_artifacts=(
                len(self._segment_cards) + len(self._bookmarks) + len(self._open_loops)
            ),
        )


__all__ = [
    "CoverageEntry",
    "CoverageState",
    "CoverageTelemetry",
    "InvalidationReport",
    "OpenLoop",
    "ReaderBookmark",
    "ReaderSession",
    "ReaderSessionState",
    "SegmentCard",
    "SourceFidelity",
    "SourceLocator",
    "SourceVersion",
    "source_sha256",
]
