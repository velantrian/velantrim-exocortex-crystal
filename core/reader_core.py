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
from dataclasses import dataclass, field, replace
from enum import Enum
from typing import Dict, List, Optional

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
        return (
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
        object.__setattr__(self, "statement", _required_text(self.statement, "statement"))
        for supporting in self.supporting_locators:
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
        object.__setattr__(self, "reason", _required_text(self.reason, "reason"))

    @property
    def restricted(self) -> bool:
        return self.locator.source.restricted


@dataclass(frozen=True)
class OpenLoop:
    loop_id: str
    locator: SourceLocator
    question: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "loop_id", _required_text(self.loop_id, "loop_id"))
        object.__setattr__(self, "question", _required_text(self.question, "question"))

    @property
    def restricted(self) -> bool:
        return self.locator.source.restricted


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


@dataclass
class ReaderSession:
    """Bounded, non-authoritative reading attempt over one source version."""

    session_id: str
    source: SourceVersion
    objective: str
    state: ReaderSessionState = ReaderSessionState.OPEN
    state_reason: Optional[str] = None
    coverage: Dict[str, CoverageEntry] = field(default_factory=dict)
    segment_cards: List[SegmentCard] = field(default_factory=list)
    bookmarks: List[ReaderBookmark] = field(default_factory=list)
    open_loops: List[OpenLoop] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.session_id = _required_text(self.session_id, "session_id")
        self.objective = _required_text(self.objective, "objective")
        if self.state_reason is not None:
            self.state_reason = _required_text(self.state_reason, "state_reason")

    def _require_source(self, locator: SourceLocator) -> None:
        if not self.source.same_version(locator.source):
            raise ValueError("reader artifact belongs to a different source version")

    def add_segment_card(self, card: SegmentCard) -> None:
        self._require_source(card.locator)
        self.segment_cards.append(card)

    def set_coverage(self, entry: CoverageEntry) -> None:
        if entry.locator is not None:
            self._require_source(entry.locator)
        self.coverage[entry.region_id] = entry

    def transition_coverage(
        self,
        region_id: str,
        target: CoverageState,
        *,
        reason: Optional[str] = None,
    ) -> CoverageEntry:
        if region_id not in self.coverage:
            raise KeyError(region_id)
        updated = self.coverage[region_id].transition(target, reason=reason)
        self.coverage[region_id] = updated
        return updated

    def add_bookmark(self, bookmark: ReaderBookmark) -> None:
        self._require_source(bookmark.locator)
        self.bookmarks.append(bookmark)

    def add_open_loop(self, open_loop: OpenLoop) -> None:
        self._require_source(open_loop.locator)
        self.open_loops.append(open_loop)

    def coverage_telemetry(self) -> CoverageTelemetry:
        counts = {state: 0 for state in CoverageState}
        missing_locator = 0
        for entry in self.coverage.values():
            counts[entry.state] += 1
            if entry.locator is None:
                missing_locator += 1
        unresolved = counts[CoverageState.UNREAD] + counts[CoverageState.NEEDS_REVIEW]
        return CoverageTelemetry(
            counts=counts,
            total_regions=len(self.coverage),
            unresolved_regions=unresolved,
            missing_locator_regions=missing_locator,
        )

    def finish(self) -> None:
        self._require_open("finish")
        self.state = ReaderSessionState.COMPLETED
        self.state_reason = None

    def interrupt(self, reason: str) -> None:
        self._require_open("interrupt")
        self.state = ReaderSessionState.INTERRUPTED
        self.state_reason = _required_text(reason, "reason")

    def degrade(self, reason: str) -> None:
        if self.state is ReaderSessionState.STALE:
            raise ValueError("cannot degrade a stale session")
        self.state = ReaderSessionState.DEGRADED
        self.state_reason = _required_text(reason, "reason")

    def _require_open(self, operation: str) -> None:
        if self.state is not ReaderSessionState.OPEN:
            raise ValueError(f"cannot {operation} session in state {self.state.value}")

    def invalidate_for(self, new_source: SourceVersion) -> InvalidationReport:
        """Conservatively stale the whole session when exact source binding changes.

        RC-1 intentionally has no diff/remapping engine. Historical artifacts remain
        untouched and continue to point at the old source version; they simply cannot be
        treated as current coverage for ``new_source``.
        """

        if new_source.document_id != self.source.document_id:
            raise ValueError("cannot invalidate a session against a different document_id")
        if self.source.same_version(new_source):
            return InvalidationReport(
                old_source_sha256=self.source.source_sha256,
                new_source_sha256=new_source.source_sha256,
                stale=False,
                scope="none",
                invalidated_regions=0,
                invalidated_artifacts=0,
            )
        self.state = ReaderSessionState.STALE
        self.state_reason = "source version changed; RC-1 has no proven remapping"
        return InvalidationReport(
            old_source_sha256=self.source.source_sha256,
            new_source_sha256=new_source.source_sha256,
            stale=True,
            scope="all",
            invalidated_regions=len(self.coverage),
            invalidated_artifacts=(
                len(self.segment_cards) + len(self.bookmarks) + len(self.open_loops)
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
