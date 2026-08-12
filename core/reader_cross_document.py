"""Bounded cross-document Reader link candidates for Reader Core RC-7.

RC-7 records explicit caller-supplied semantic link *candidates* between already
registered RC-4 proposition candidates from different documents. It preserves
exact two-sided provenance and revalidates the current Reader state before every
registration.

This module performs no automatic semantic matching, identity inference,
similarity search, evidence admission, truth/Canon/ESM mutation, contradiction
resolution, model/provider call, parser/OCR work, persistence, public API, or
background processing.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Iterable, Optional

from core.reader_core import (
    CoverageState,
    ReaderSessionState,
    SourceFidelity,
    SourceLocator,
    SourceVersion,
)
from core.reader_extraction import ReaderPropositionCandidate, ReaderPropositionExtractor
from core.reader_passes import ReaderPassState
from core.reader_structure import StructuralStatus

MAX_REGISTERED_SOURCES = 32
MAX_LINK_CANDIDATES = 4096


class CrossDocumentLinkKind(str, Enum):
    """RC-0 cross-document candidate-link vocabulary."""

    SUPPORTS = "SUPPORTS"
    CONTRADICTS = "CONTRADICTS"
    ELABORATES = "ELABORATES"
    REFERENCES = "REFERENCES"
    DEFINES = "DEFINES"
    EXAMPLE_OF = "EXAMPLE_OF"
    PREREQUISITE_FOR = "PREREQUISITE_FOR"
    SAME_TOPIC = "SAME_TOPIC"
    POSSIBLE_SAME_CLAIM = "POSSIBLE_SAME_CLAIM"


class CrossDocumentInspectionBasis(str, Enum):
    """Descriptive caller-supplied inspection metadata; never identity proof."""

    EXPLICIT_SOURCE_REFERENCE = "EXPLICIT_SOURCE_REFERENCE"
    CALLER_COMPARISON = "CALLER_COMPARISON"
    LEXICAL_SIMILARITY_SIGNAL = "LEXICAL_SIMILARITY_SIGNAL"
    SHARED_TOPIC_SIGNAL = "SHARED_TOPIC_SIGNAL"
    OTHER = "OTHER"


def _required_text(value: str, field_name: str) -> str:
    value = (value or "").strip()
    if not value:
        raise ValueError(f"{field_name} must be non-empty")
    return value


def _bounded_positive_int(value: int, field_name: str, maximum: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1 or value > maximum:
        raise ValueError(f"{field_name} must be an integer in [1, {maximum}]")
    return value


def _node_ids(values: Iterable[str]) -> tuple[str, ...]:
    if isinstance(values, (str, bytes)):
        raise ValueError("node_ids must be an iterable of strings")
    try:
        result = tuple(_required_text(value, "node_id") for value in values)
    except TypeError as exc:
        raise ValueError("node_ids must be an iterable of strings") from exc
    if not result:
        raise ValueError("node_ids must not be empty")
    if len(set(result)) != len(result):
        raise ValueError("node_ids must contain unique values")
    return result


@dataclass(frozen=True)
class CrossDocumentLinkSide:
    """Immutable exact-provenance snapshot of one RC-4 proposition candidate."""

    session_id: str
    candidate_id: str
    pass_id: str
    node_ids: tuple[str, ...]
    source: SourceVersion
    primary_locator: SourceLocator
    supporting_locators: tuple[SourceLocator, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "session_id", _required_text(self.session_id, "session_id"))
        object.__setattr__(self, "candidate_id", _required_text(self.candidate_id, "candidate_id"))
        object.__setattr__(self, "pass_id", _required_text(self.pass_id, "pass_id"))
        object.__setattr__(self, "node_ids", _node_ids(self.node_ids))
        if not isinstance(self.source, SourceVersion):
            raise ValueError("source must be a SourceVersion")
        if not isinstance(self.primary_locator, SourceLocator):
            raise ValueError("primary_locator must be a SourceLocator")
        supports = tuple(self.supporting_locators)
        if any(not isinstance(locator, SourceLocator) for locator in supports):
            raise ValueError("supporting_locators must contain SourceLocator values")
        if len(self.node_ids) != 1 + len(supports):
            raise ValueError("node_ids must match primary + supporting source locators")
        all_locators = (self.primary_locator,) + supports
        if any(
            not self.source.same_version(locator.source)
            or locator.source.restricted != self.source.restricted
            or locator.source.sensitivity != self.source.sensitivity
            for locator in all_locators
        ):
            raise ValueError("all side locators must use the exact source and privacy binding")
        object.__setattr__(self, "supporting_locators", supports)

    @classmethod
    def from_candidate(
        cls, candidate: ReaderPropositionCandidate
    ) -> "CrossDocumentLinkSide":
        if not isinstance(candidate, ReaderPropositionCandidate):
            raise ValueError("candidate must be a ReaderPropositionCandidate")
        return cls(
            session_id=candidate.session_id,
            candidate_id=candidate.candidate_id,
            pass_id=candidate.pass_id,
            node_ids=candidate.node_ids,
            source=candidate.primary_locator.source,
            primary_locator=candidate.primary_locator,
            supporting_locators=candidate.card.supporting_locators,
        )

    @property
    def document_id(self) -> str:
        return self.source.document_id

    @property
    def restricted(self) -> bool:
        return self.source.restricted

    @property
    def sensitivity(self) -> Optional[str]:
        return self.source.sensitivity

    @property
    def sort_key(self) -> tuple[str, str, str, str, str]:
        return (
            self.source.document_id,
            self.source.source_uri,
            self.source.source_sha256,
            self.session_id,
            self.candidate_id,
        )


@dataclass(frozen=True)
class CrossDocumentLinkCandidate:
    """One cross-document semantic-link candidate; never a Canon relation."""

    link_id: str
    kind: CrossDocumentLinkKind
    left: CrossDocumentLinkSide
    right: CrossDocumentLinkSide
    rationale: str
    inspection_basis: Optional[CrossDocumentInspectionBasis] = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "link_id", _required_text(self.link_id, "link_id"))
        if not isinstance(self.kind, CrossDocumentLinkKind):
            raise ValueError("kind must be a CrossDocumentLinkKind")
        if not isinstance(self.left, CrossDocumentLinkSide):
            raise ValueError("left must be a CrossDocumentLinkSide")
        if not isinstance(self.right, CrossDocumentLinkSide):
            raise ValueError("right must be a CrossDocumentLinkSide")
        if self.left.document_id == self.right.document_id:
            raise ValueError("RC-7 link sides must use different document identities")
        object.__setattr__(self, "rationale", _required_text(self.rationale, "rationale"))
        if self.inspection_basis is not None and not isinstance(
            self.inspection_basis, CrossDocumentInspectionBasis
        ):
            raise ValueError("inspection_basis must be a CrossDocumentInspectionBasis")

    @property
    def restricted(self) -> bool:
        return self.left.restricted or self.right.restricted

    @property
    def sensitivities(self) -> tuple[str, ...]:
        values: list[str] = []
        for value in (self.left.sensitivity, self.right.sensitivity):
            if value is not None and value not in values:
                values.append(value)
        return tuple(values)


@dataclass(frozen=True)
class CrossDocumentTelemetry:
    """Counts only; no truth, identity, confidence, or corroboration score."""

    total_links: int
    restricted_links: int
    kind_counts: Dict[CrossDocumentLinkKind, int]
    inspection_basis_counts: Dict[CrossDocumentInspectionBasis, int]


class ReaderCrossDocumentRegistry:
    """RC-7 registry over explicit RC-4 extractors from different documents."""

    __slots__ = (
        "_extractors",
        "_max_links",
        "_links",
        "_link_index",
        "_semantic_index",
    )

    _SYMMETRIC_KINDS = {
        CrossDocumentLinkKind.CONTRADICTS,
        CrossDocumentLinkKind.SAME_TOPIC,
        CrossDocumentLinkKind.POSSIBLE_SAME_CLAIM,
    }

    def __init__(
        self,
        extractors: Iterable[ReaderPropositionExtractor],
        *,
        max_links: int = 1024,
    ) -> None:
        if isinstance(extractors, (str, bytes)):
            raise ValueError("extractors must be an iterable of ReaderPropositionExtractor values")
        try:
            items = tuple(extractors)
        except TypeError as exc:
            raise ValueError(
                "extractors must be an iterable of ReaderPropositionExtractor values"
            ) from exc
        if len(items) < 2:
            raise ValueError("RC-7 requires at least two Reader extractors")
        if len(items) > MAX_REGISTERED_SOURCES:
            raise ValueError(f"RC-7 supports at most {MAX_REGISTERED_SOURCES} registered sources")
        if any(not isinstance(item, ReaderPropositionExtractor) for item in items):
            raise ValueError("extractors must contain ReaderPropositionExtractor values")
        if any(item.reader.session.state is not ReaderSessionState.OPEN for item in items):
            raise ValueError("RC-7 requires OPEN Reader sessions")

        by_session: Dict[str, ReaderPropositionExtractor] = {}
        for item in items:
            session_id = item.reader.session.session_id
            if session_id in by_session:
                raise ValueError("RC-7 Reader session IDs must be unique")
            by_session[session_id] = item
        if len({item.reader.session.source.document_id for item in items}) < 2:
            raise ValueError("RC-7 requires at least two distinct document identities")

        self._extractors = by_session
        self._max_links = _bounded_positive_int(max_links, "max_links", MAX_LINK_CANDIDATES)
        self._links: list[CrossDocumentLinkCandidate] = []
        self._link_index: Dict[str, int] = {}
        self._semantic_index: set[
            tuple[CrossDocumentLinkKind, tuple[str, ...], tuple[str, ...]]
        ] = set()

    @property
    def session_ids(self) -> tuple[str, ...]:
        return tuple(self._extractors)

    @property
    def links(self) -> tuple[CrossDocumentLinkCandidate, ...]:
        return tuple(self._links)

    @property
    def max_links(self) -> int:
        return self._max_links

    def get_link(self, link_id: str) -> CrossDocumentLinkCandidate:
        link_id = _required_text(link_id, "link_id")
        try:
            return self._links[self._link_index[link_id]]
        except KeyError as exc:
            raise KeyError(link_id) from exc

    def register(
        self,
        link_id: str,
        kind: CrossDocumentLinkKind,
        left_session_id: str,
        left_candidate_id: str,
        right_session_id: str,
        right_candidate_id: str,
        rationale: str,
        *,
        inspection_basis: Optional[CrossDocumentInspectionBasis] = None,
    ) -> CrossDocumentLinkCandidate:
        """Register one explicit cross-document candidate link."""

        link_id = _required_text(link_id, "link_id")
        if link_id in self._link_index:
            raise ValueError(f"duplicate RC-7 link_id: {link_id}")
        if len(self._links) >= self._max_links:
            raise ValueError("RC-7 link budget exhausted")
        if not isinstance(kind, CrossDocumentLinkKind):
            raise ValueError("kind must be a CrossDocumentLinkKind")
        if inspection_basis is not None and not isinstance(
            inspection_basis, CrossDocumentInspectionBasis
        ):
            raise ValueError("inspection_basis must be a CrossDocumentInspectionBasis")

        left_sid = _required_text(left_session_id, "left_session_id")
        right_sid = _required_text(right_session_id, "right_session_id")
        if left_sid == right_sid:
            raise ValueError("RC-7 link sides must use different Reader sessions")
        left_extractor = self._extractor(left_sid)
        right_extractor = self._extractor(right_sid)

        left = self._current_side(left_extractor, left_candidate_id)
        right = self._current_side(right_extractor, right_candidate_id)
        if left.document_id == right.document_id:
            raise ValueError("RC-7 link sides must use different document identities")

        if kind in self._SYMMETRIC_KINDS and right.sort_key < left.sort_key:
            left, right = right, left

        semantic_key = (kind, left.sort_key, right.sort_key)
        if semantic_key in self._semantic_index:
            raise ValueError("duplicate RC-7 cross-document link candidate")

        link = CrossDocumentLinkCandidate(
            link_id=link_id,
            kind=kind,
            left=left,
            right=right,
            rationale=rationale,
            inspection_basis=inspection_basis,
        )
        self._link_index[link_id] = len(self._links)
        self._semantic_index.add(semantic_key)
        self._links.append(link)
        return link

    def telemetry(self) -> CrossDocumentTelemetry:
        kind_counts = {kind: 0 for kind in CrossDocumentLinkKind}
        basis_counts = {basis: 0 for basis in CrossDocumentInspectionBasis}
        restricted = 0
        for link in self._links:
            kind_counts[link.kind] += 1
            restricted += int(link.restricted)
            if link.inspection_basis is not None:
                basis_counts[link.inspection_basis] += 1
        return CrossDocumentTelemetry(
            total_links=len(self._links),
            restricted_links=restricted,
            kind_counts=kind_counts,
            inspection_basis_counts=basis_counts,
        )

    def _extractor(self, session_id: str) -> ReaderPropositionExtractor:
        try:
            extractor = self._extractors[session_id]
        except KeyError as exc:
            raise KeyError(session_id) from exc
        if extractor.reader.session.state is not ReaderSessionState.OPEN:
            raise ValueError(f"RC-7 session is no longer OPEN: {session_id}")
        return extractor

    @staticmethod
    def _current_side(
        extractor: ReaderPropositionExtractor,
        candidate_id: str,
    ) -> CrossDocumentLinkSide:
        candidate = extractor.get_candidate(_required_text(candidate_id, "candidate_id"))
        session = extractor.reader.session

        if candidate.session_id != session.session_id:
            raise ValueError("RC-4 candidate belongs to a different Reader session")
        if candidate.card.fidelity is not SourceFidelity.EXTRACTED_PROPOSITION:
            raise ValueError("RC-7 requires EXTRACTED_PROPOSITION RC-4 candidates")
        source = session.source
        primary = candidate.primary_locator
        locators = (primary,) + candidate.card.supporting_locators
        if any(
            not source.same_version(locator.source)
            or locator.source.restricted != source.restricted
            or locator.source.sensitivity != source.sensitivity
            for locator in locators
        ):
            raise ValueError("RC-4 candidate provenance no longer matches its exact source binding")
        if not any(card is candidate.card for card in session.segment_cards):
            raise ValueError("RC-4 candidate card is not registered in the Reader session")

        record = extractor.reader.get_pass(candidate.pass_id)
        if record.state is not ReaderPassState.COMPLETED:
            raise ValueError("RC-7 requires candidates from a COMPLETED Reader pass")
        if record.session_id != session.session_id or not source.same_version(record.source):
            raise ValueError("RC-4 candidate pass no longer matches its Reader session/source")

        if len(candidate.node_ids) != len(locators):
            raise ValueError("RC-4 candidate node/provenance cardinality mismatch")
        outcomes = {outcome.node_id: outcome for outcome in record.outcomes}
        coverage = session.coverage
        for node_id, locator in zip(candidate.node_ids, locators):
            if node_id not in record.target_node_ids:
                raise ValueError("RC-4 candidate node is not a declared pass target")
            outcome = outcomes.get(node_id)
            if outcome is None or outcome.after not in {
                CoverageState.PROCESSED,
                CoverageState.REVISITED,
            }:
                raise ValueError("RC-4 candidate pass outcome is not substantive")
            node = extractor.reader.structure.get(node_id)
            if node.status is not StructuralStatus.RECOVERED:
                raise ValueError("RC-4 candidate structural node is unresolved")
            if (
                not source.same_version(node.locator.source)
                or node.locator.replay_key != locator.replay_key
            ):
                raise ValueError("RC-4 candidate locator no longer matches structural provenance")
            current = coverage.get(node_id)
            if (
                current is None
                or current.locator is None
                or not source.same_version(current.locator.source)
                or current.locator.replay_key != locator.replay_key
            ):
                raise ValueError("RC-4 candidate current coverage/provenance mismatch")
            if current.state not in {CoverageState.PROCESSED, CoverageState.REVISITED}:
                raise ValueError("RC-4 candidate current coverage is not substantive")

        return CrossDocumentLinkSide.from_candidate(candidate)


__all__ = [
    "CrossDocumentInspectionBasis",
    "CrossDocumentLinkCandidate",
    "CrossDocumentLinkKind",
    "CrossDocumentLinkSide",
    "CrossDocumentTelemetry",
    "MAX_LINK_CANDIDATES",
    "MAX_REGISTERED_SOURCES",
    "ReaderCrossDocumentRegistry",
]
