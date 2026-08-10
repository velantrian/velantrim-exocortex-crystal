"""Source-linked proposition extraction for Reader Core RC-4.

RC-4 turns explicitly processed RC-3 reading regions into non-authoritative
``EXTRACTED_PROPOSITION`` candidates. It does not perform NLP/model extraction,
write fact evidence, admit truth, resolve contradictions, or create a second
knowledge authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Iterable, Optional

from core.reader_core import (
    CoverageState,
    ReaderSessionState,
    SegmentCard,
    SourceFidelity,
    SourceLocator,
)
from core.reader_passes import MultiPassReader, ReaderPassRecord, ReaderPassState
from core.reader_structure import StructuralStatus


class PropositionKind(str, Enum):
    """How the source presents the extracted proposition.

    These categories describe source presentation only. ``FACTUAL_ASSERTION``
    means that the source presents a statement as factual; it does not mean
    Crystal has verified the statement as a world fact.
    """

    FACTUAL_ASSERTION = "FACTUAL_ASSERTION"
    AUTHOR_OPINION = "AUTHOR_OPINION"
    HYPOTHESIS = "HYPOTHESIS"
    CONDITIONAL = "CONDITIONAL"
    EXAMPLE = "EXAMPLE"
    QUOTED_SPEECH = "QUOTED_SPEECH"
    REPORTED_POSITION = "REPORTED_POSITION"
    DEFINITION = "DEFINITION"
    UNCERTAIN_ASSERTION = "UNCERTAIN_ASSERTION"


def _required_text(value: str, field_name: str) -> str:
    value = (value or "").strip()
    if not value:
        raise ValueError(f"{field_name} must be non-empty")
    return value


def _text_tuple(values: Iterable[str], field_name: str) -> tuple[str, ...]:
    if isinstance(values, (str, bytes)):
        raise ValueError(f"{field_name} must be an iterable of strings")
    try:
        normalized = tuple(_required_text(value, field_name) for value in values)
    except TypeError as exc:
        raise ValueError(f"{field_name} must be an iterable of strings") from exc
    if len(set(normalized)) != len(normalized):
        raise ValueError(f"{field_name} must contain unique values")
    return normalized


@dataclass(frozen=True)
class ReaderPropositionCandidate:
    """One source-linked proposition candidate produced by RC-4.

    The embedded SegmentCard is always ``EXTRACTED_PROPOSITION`` fidelity.
    Source ownership, source-presentation category, negation and scope qualifiers
    remain explicit so extraction cannot silently turn reported/conditional text
    into an unqualified author-endorsed fact.
    """

    candidate_id: str
    session_id: str
    pass_id: str
    card: SegmentCard
    kind: PropositionKind
    source_owner: str
    node_ids: tuple[str, ...]
    negated: bool = False
    qualifiers: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "candidate_id", _required_text(self.candidate_id, "candidate_id")
        )
        object.__setattr__(self, "session_id", _required_text(self.session_id, "session_id"))
        object.__setattr__(self, "pass_id", _required_text(self.pass_id, "pass_id"))
        if not isinstance(self.card, SegmentCard):
            raise ValueError("card must be a SegmentCard")
        if self.card.fidelity is not SourceFidelity.EXTRACTED_PROPOSITION:
            raise ValueError("RC-4 candidates require EXTRACTED_PROPOSITION fidelity")
        if not isinstance(self.kind, PropositionKind):
            raise ValueError("kind must be a PropositionKind")
        object.__setattr__(
            self, "source_owner", _required_text(self.source_owner, "source_owner")
        )
        nodes = _text_tuple(self.node_ids, "node_ids")
        if not nodes:
            raise ValueError("node_ids must contain at least one source region")
        if len(nodes) != 1 + len(self.card.supporting_locators):
            raise ValueError("node_ids must match primary + supporting source locators")
        object.__setattr__(self, "node_ids", nodes)
        if not isinstance(self.negated, bool):
            raise ValueError("negated must be a bool")
        object.__setattr__(self, "qualifiers", _text_tuple(self.qualifiers, "qualifiers"))

    @property
    def proposition(self) -> str:
        return self.card.statement

    @property
    def primary_locator(self) -> SourceLocator:
        return self.card.locator

    @property
    def restricted(self) -> bool:
        return self.card.restricted

    @property
    def sensitivity(self) -> Optional[str]:
        return self.card.sensitivity


@dataclass(frozen=True)
class ExtractionTelemetry:
    """Counts only; deliberately no truth/confidence/evidence-sufficiency score."""

    total_candidates: int
    negated_candidates: int
    qualified_candidates: int
    multi_span_candidates: int
    kind_counts: Dict[PropositionKind, int]


class ReaderPropositionExtractor:
    """RC-4 extraction controller bound to one RC-3 reader."""

    __slots__ = ("_reader", "_candidates", "_candidate_index")

    def __init__(self, reader: MultiPassReader) -> None:
        if not isinstance(reader, MultiPassReader):
            raise ValueError("reader must be a MultiPassReader")
        if reader.session.state is not ReaderSessionState.OPEN:
            raise ValueError("RC-4 requires an OPEN ReaderSession")
        self._reader = reader
        self._candidates: list[ReaderPropositionCandidate] = []
        self._candidate_index: Dict[str, int] = {}

    @property
    def reader(self) -> MultiPassReader:
        return self._reader

    @property
    def candidates(self) -> tuple[ReaderPropositionCandidate, ...]:
        return tuple(self._candidates)

    def get_candidate(self, candidate_id: str) -> ReaderPropositionCandidate:
        candidate_id = _required_text(candidate_id, "candidate_id")
        try:
            return self._candidates[self._candidate_index[candidate_id]]
        except KeyError as exc:
            raise KeyError(candidate_id) from exc

    def extract(
        self,
        candidate_id: str,
        pass_id: str,
        proposition: str,
        kind: PropositionKind,
        source_owner: str,
        primary_node_id: str,
        *,
        supporting_node_ids: Iterable[str] = (),
        negated: bool = False,
        qualifiers: Iterable[str] = (),
    ) -> ReaderPropositionCandidate:
        self._require_session_open()
        candidate_id = _required_text(candidate_id, "candidate_id")
        if candidate_id in self._candidate_index:
            raise ValueError(f"duplicate RC-4 candidate_id: {candidate_id}")
        if any(card.card_id == candidate_id for card in self._reader.session.segment_cards):
            raise ValueError(f"Reader SegmentCard id already exists: {candidate_id}")
        if not isinstance(kind, PropositionKind):
            raise ValueError("kind must be a PropositionKind")
        if not isinstance(negated, bool):
            raise ValueError("negated must be a bool")

        record = self._reader.get_pass(pass_id)
        self._validate_pass_binding(record)

        primary = _required_text(primary_node_id, "primary_node_id")
        supports = _text_tuple(supporting_node_ids, "supporting_node_ids")
        node_ids = (primary,) + supports
        if len(set(node_ids)) != len(node_ids):
            raise ValueError("primary/supporting node ids must be unique")

        outcome_by_node = {outcome.node_id: outcome for outcome in record.outcomes}
        locators: list[SourceLocator] = []
        for node_id in node_ids:
            if node_id not in record.target_node_ids:
                raise ValueError("extraction node must be a declared target of the completed pass")
            outcome = outcome_by_node[node_id]
            if outcome.after not in {CoverageState.PROCESSED, CoverageState.REVISITED}:
                raise ValueError("RC-4 extraction requires PROCESSED or REVISITED pass outcome")
            node = self._reader.structure.get(node_id)
            if node.status is not StructuralStatus.RECOVERED:
                raise ValueError("RC-4 cannot extract from unresolved structural regions")
            coverage = self._reader.session.coverage.get(node_id)
            if (
                coverage is None
                or coverage.locator is None
                or coverage.locator.replay_key != node.locator.replay_key
            ):
                raise ValueError("current coverage/provenance does not match the structural node")
            if coverage.state not in {CoverageState.PROCESSED, CoverageState.REVISITED}:
                raise ValueError("current coverage is not substantive enough for RC-4 extraction")
            locators.append(node.locator)

        card = SegmentCard(
            card_id=candidate_id,
            locator=locators[0],
            fidelity=SourceFidelity.EXTRACTED_PROPOSITION,
            statement=_required_text(proposition, "proposition"),
            supporting_locators=tuple(locators[1:]),
        )
        candidate = ReaderPropositionCandidate(
            candidate_id=candidate_id,
            session_id=self._reader.session.session_id,
            pass_id=record.pass_id,
            card=card,
            kind=kind,
            source_owner=source_owner,
            node_ids=node_ids,
            negated=negated,
            qualifiers=_text_tuple(qualifiers, "qualifiers"),
        )
        self._reader.session.add_segment_card(card)
        self._candidate_index[candidate_id] = len(self._candidates)
        self._candidates.append(candidate)
        return candidate

    def telemetry(self) -> ExtractionTelemetry:
        kind_counts = {kind: 0 for kind in PropositionKind}
        negated = 0
        qualified = 0
        multi_span = 0
        for candidate in self._candidates:
            kind_counts[candidate.kind] += 1
            negated += int(candidate.negated)
            qualified += int(bool(candidate.qualifiers))
            multi_span += int(len(candidate.node_ids) > 1)
        return ExtractionTelemetry(
            total_candidates=len(self._candidates),
            negated_candidates=negated,
            qualified_candidates=qualified,
            multi_span_candidates=multi_span,
            kind_counts=kind_counts,
        )

    def _require_session_open(self) -> None:
        if self._reader.session.state is not ReaderSessionState.OPEN:
            raise ValueError(
                f"RC-4 session is no longer OPEN: {self._reader.session.state.value}"
            )

    def _validate_pass_binding(self, record: ReaderPassRecord) -> None:
        if record.state is not ReaderPassState.COMPLETED:
            raise ValueError("RC-4 extraction requires a COMPLETED Reader pass")
        if record.session_id != self._reader.session.session_id:
            raise ValueError("Reader pass belongs to a different session")
        if not record.source.same_version(self._reader.session.source):
            raise ValueError("Reader pass belongs to a different source version")
