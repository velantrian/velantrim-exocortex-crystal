"""Pre-admission Reader relation candidates for Reader Core RC-5.

RC-5 records explicit, deterministic relations between already-registered RC-4
proposition candidates. It does not compare raw source text, infer semantic
identity, admit evidence, mutate truth/Canon/ESM, or resolve contradictions.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict

from core.reader_core import ReaderSessionState, SourceLocator, SourceVersion
from core.reader_extraction import ReaderPropositionCandidate, ReaderPropositionExtractor


class ReaderRelationKind(str, Enum):
    """Typed Reader-only relation suspicions.

    ``EXCEPTION`` and ``QUALIFICATION`` are directional: the right-hand candidate
    limits/refines the left-hand candidate. ``POSSIBLE_CONTRADICTION`` and
    ``TENSION`` are symmetric and are stored in deterministic candidate-id order.
    """

    POSSIBLE_CONTRADICTION = "POSSIBLE_CONTRADICTION"
    EXCEPTION = "EXCEPTION"
    QUALIFICATION = "QUALIFICATION"
    TENSION = "TENSION"


def _required_text(value: str, field_name: str) -> str:
    value = (value or "").strip()
    if not value:
        raise ValueError(f"{field_name} must be non-empty")
    return value


@dataclass(frozen=True)
class ReaderRelationSide:
    """Replayable provenance snapshot for one RC-4 proposition candidate."""

    candidate_id: str
    pass_id: str
    node_ids: tuple[str, ...]
    primary_locator: SourceLocator
    supporting_locators: tuple[SourceLocator, ...]

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "candidate_id", _required_text(self.candidate_id, "candidate_id")
        )
        object.__setattr__(self, "pass_id", _required_text(self.pass_id, "pass_id"))
        nodes = tuple(self.node_ids)
        if not nodes or any(not isinstance(node_id, str) or not node_id.strip() for node_id in nodes):
            raise ValueError("node_ids must contain non-empty strings")
        normalized_nodes = tuple(node_id.strip() for node_id in nodes)
        if len(set(normalized_nodes)) != len(normalized_nodes):
            raise ValueError("node_ids must contain unique values")
        object.__setattr__(self, "node_ids", normalized_nodes)
        if not isinstance(self.primary_locator, SourceLocator):
            raise ValueError("primary_locator must be a SourceLocator")
        supports = tuple(self.supporting_locators)
        if any(not isinstance(locator, SourceLocator) for locator in supports):
            raise ValueError("supporting_locators must contain SourceLocator values")
        if len(normalized_nodes) != 1 + len(supports):
            raise ValueError("node_ids must match primary + supporting source locators")
        if any(
            not self.primary_locator.source.same_version(locator.source)
            for locator in supports
        ):
            raise ValueError("all relation-side locators must use one source version")
        object.__setattr__(self, "supporting_locators", supports)

    @property
    def source(self) -> SourceVersion:
        return self.primary_locator.source

    @classmethod
    def from_candidate(cls, candidate: ReaderPropositionCandidate) -> "ReaderRelationSide":
        if not isinstance(candidate, ReaderPropositionCandidate):
            raise ValueError("candidate must be a ReaderPropositionCandidate")
        return cls(
            candidate_id=candidate.candidate_id,
            pass_id=candidate.pass_id,
            node_ids=candidate.node_ids,
            primary_locator=candidate.primary_locator,
            supporting_locators=candidate.card.supporting_locators,
        )


@dataclass(frozen=True)
class ReaderRelationCandidate:
    """One auditable Reader relation candidate; never a resolved contradiction."""

    relation_id: str
    session_id: str
    kind: ReaderRelationKind
    left: ReaderRelationSide
    right: ReaderRelationSide
    rationale: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "relation_id", _required_text(self.relation_id, "relation_id")
        )
        object.__setattr__(
            self, "session_id", _required_text(self.session_id, "session_id")
        )
        if not isinstance(self.kind, ReaderRelationKind):
            raise ValueError("kind must be a ReaderRelationKind")
        if not isinstance(self.left, ReaderRelationSide):
            raise ValueError("left must be a ReaderRelationSide")
        if not isinstance(self.right, ReaderRelationSide):
            raise ValueError("right must be a ReaderRelationSide")
        if self.left.candidate_id == self.right.candidate_id:
            raise ValueError("relation sides must reference distinct candidates")
        if not self.left.source.same_version(self.right.source):
            raise ValueError("relation sides must use the same source version")
        object.__setattr__(self, "rationale", _required_text(self.rationale, "rationale"))

    @property
    def source(self) -> SourceVersion:
        return self.left.source

    @property
    def restricted(self) -> bool:
        return self.source.restricted

    @property
    def sensitivity(self) -> str | None:
        return self.source.sensitivity


@dataclass(frozen=True)
class RelationTelemetry:
    """Counts only; deliberately no truth/confidence/evidence-sufficiency score."""

    total_candidates: int
    kind_counts: Dict[ReaderRelationKind, int]


class ReaderRelationRegistry:
    """RC-5 controller bound to one RC-4 extractor/session/source version."""

    __slots__ = ("_extractor", "_relations", "_relation_index", "_semantic_index")

    _SYMMETRIC_KINDS = {
        ReaderRelationKind.POSSIBLE_CONTRADICTION,
        ReaderRelationKind.TENSION,
    }

    def __init__(self, extractor: ReaderPropositionExtractor) -> None:
        if not isinstance(extractor, ReaderPropositionExtractor):
            raise ValueError("extractor must be a ReaderPropositionExtractor")
        if extractor.reader.session.state is not ReaderSessionState.OPEN:
            raise ValueError("RC-5 requires an OPEN ReaderSession")
        self._extractor = extractor
        self._relations: list[ReaderRelationCandidate] = []
        self._relation_index: Dict[str, int] = {}
        self._semantic_index: set[tuple[ReaderRelationKind, str, str]] = set()

    @property
    def extractor(self) -> ReaderPropositionExtractor:
        return self._extractor

    @property
    def relations(self) -> tuple[ReaderRelationCandidate, ...]:
        return tuple(self._relations)

    def get_relation(self, relation_id: str) -> ReaderRelationCandidate:
        relation_id = _required_text(relation_id, "relation_id")
        try:
            return self._relations[self._relation_index[relation_id]]
        except KeyError as exc:
            raise KeyError(relation_id) from exc

    def register(
        self,
        relation_id: str,
        kind: ReaderRelationKind,
        left_candidate_id: str,
        right_candidate_id: str,
        rationale: str,
    ) -> ReaderRelationCandidate:
        """Register an explicit candidate relation without inferring truth or identity."""

        self._require_session_open()
        relation_id = _required_text(relation_id, "relation_id")
        if relation_id in self._relation_index:
            raise ValueError(f"duplicate RC-5 relation_id: {relation_id}")
        if not isinstance(kind, ReaderRelationKind):
            raise ValueError("kind must be a ReaderRelationKind")

        left_id = _required_text(left_candidate_id, "left_candidate_id")
        right_id = _required_text(right_candidate_id, "right_candidate_id")
        if left_id == right_id:
            raise ValueError("relation sides must reference distinct candidates")
        rationale = _required_text(rationale, "rationale")

        left_candidate = self._registered_candidate(left_id)
        right_candidate = self._registered_candidate(right_id)

        if kind in self._SYMMETRIC_KINDS and right_id < left_id:
            left_candidate, right_candidate = right_candidate, left_candidate

        semantic_key = (kind, left_candidate.candidate_id, right_candidate.candidate_id)
        if semantic_key in self._semantic_index:
            raise ValueError("duplicate RC-5 relation candidate")

        left = ReaderRelationSide.from_candidate(left_candidate)
        right = ReaderRelationSide.from_candidate(right_candidate)
        relation = ReaderRelationCandidate(
            relation_id=relation_id,
            session_id=self._extractor.reader.session.session_id,
            kind=kind,
            left=left,
            right=right,
            rationale=rationale,
        )
        self._relation_index[relation_id] = len(self._relations)
        self._semantic_index.add(semantic_key)
        self._relations.append(relation)
        return relation

    def telemetry(self) -> RelationTelemetry:
        kind_counts = {kind: 0 for kind in ReaderRelationKind}
        for relation in self._relations:
            kind_counts[relation.kind] += 1
        return RelationTelemetry(
            total_candidates=len(self._relations),
            kind_counts=kind_counts,
        )

    def _require_session_open(self) -> None:
        state = self._extractor.reader.session.state
        if state is not ReaderSessionState.OPEN:
            raise ValueError(f"RC-5 session is no longer OPEN: {state.value}")

    def _registered_candidate(self, candidate_id: str) -> ReaderPropositionCandidate:
        candidate = self._extractor.get_candidate(candidate_id)
        session = self._extractor.reader.session
        if candidate.session_id != session.session_id:
            raise ValueError("RC-4 candidate belongs to a different Reader session")
        if not candidate.primary_locator.source.same_version(session.source):
            raise ValueError("RC-4 candidate belongs to a different source version")
        if any(
            not locator.source.same_version(session.source)
            for locator in candidate.card.supporting_locators
        ):
            raise ValueError("RC-4 candidate support belongs to a different source version")
        if not any(card is candidate.card for card in session.segment_cards):
            raise ValueError("RC-4 candidate card is not registered in the Reader session")
        return candidate


__all__ = [
    "ReaderRelationCandidate",
    "ReaderRelationKind",
    "ReaderRelationRegistry",
    "ReaderRelationSide",
    "RelationTelemetry",
]
