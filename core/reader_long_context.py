"""Bounded long-context working sets for Reader Core RC-6.

RC-6 makes one-source Reader processing larger than a single working set explicit and
replayable. It partitions already-registered RC-4 proposition candidates by structural
order under caller-declared artifact/provenance budgets, can carry already-registered
RC-5 relations when both sides fit the same set, and can register caller-supplied
``SUMMARY`` artifacts that retain direct leaf provenance.

It deliberately performs no model/provider call, token estimation, parser/OCR work,
semantic identity inference, cross-document reasoning, evidence admission, truth/Canon/
ESM mutation, contradiction resolution, persistence, public API, or background work.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, Optional

from core.reader_core import (
    CoverageState,
    ReaderSessionState,
    SegmentCard,
    SourceFidelity,
    SourceLocator,
    SourceVersion,
)
from core.reader_extraction import ReaderPropositionCandidate, ReaderPropositionExtractor
from core.reader_passes import ReaderPassState
from core.reader_relations import ReaderRelationRegistry
from core.reader_structure import StructuralStatus

MAX_CANDIDATES_PER_WORKING_SET = 128
MAX_SOURCE_LOCATORS_PER_WORKING_SET = 512


def _required_text(value: str, field_name: str) -> str:
    value = (value or "").strip()
    if not value:
        raise ValueError(f"{field_name} must be non-empty")
    return value


def _text_tuple(values: Iterable[str], field_name: str, *, require_non_empty: bool) -> tuple[str, ...]:
    if isinstance(values, (str, bytes)):
        raise ValueError(f"{field_name} must be an iterable of strings")
    try:
        normalized = tuple(_required_text(value, field_name) for value in values)
    except TypeError as exc:
        raise ValueError(f"{field_name} must be an iterable of strings") from exc
    if require_non_empty and not normalized:
        raise ValueError(f"{field_name} must not be empty")
    if len(set(normalized)) != len(normalized):
        raise ValueError(f"{field_name} must contain unique values")
    return normalized


def _bounded_positive_int(value: int, field_name: str, maximum: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1 or value > maximum:
        raise ValueError(f"{field_name} must be an integer in [1, {maximum}]")
    return value


def _unique_locators(locators: Iterable[SourceLocator]) -> tuple[SourceLocator, ...]:
    result: list[SourceLocator] = []
    seen: set[tuple[object, ...]] = set()
    for locator in locators:
        if not isinstance(locator, SourceLocator):
            raise ValueError("locators must contain SourceLocator values")
        if locator.replay_key not in seen:
            seen.add(locator.replay_key)
            result.append(locator)
    return tuple(result)


@dataclass(frozen=True)
class ReaderWorkingSet:
    """One deterministic RC-6 rolling working set over direct RC-4 leaf candidates."""

    working_set_id: str
    session_id: str
    source: SourceVersion
    candidate_ids: tuple[str, ...]
    node_ids: tuple[str, ...]
    locators: tuple[SourceLocator, ...]
    relation_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "working_set_id", _required_text(self.working_set_id, "working_set_id")
        )
        object.__setattr__(self, "session_id", _required_text(self.session_id, "session_id"))
        if not isinstance(self.source, SourceVersion):
            raise ValueError("source must be a SourceVersion")
        object.__setattr__(
            self,
            "candidate_ids",
            _text_tuple(self.candidate_ids, "candidate_ids", require_non_empty=True),
        )
        object.__setattr__(
            self,
            "node_ids",
            _text_tuple(self.node_ids, "node_ids", require_non_empty=True),
        )
        locators = _unique_locators(self.locators)
        if not locators:
            raise ValueError("locators must not be empty")
        if any(not self.source.same_version(locator.source) for locator in locators):
            raise ValueError("working-set locators must use the working-set source version")
        object.__setattr__(self, "locators", locators)
        object.__setattr__(
            self,
            "relation_ids",
            _text_tuple(self.relation_ids, "relation_ids", require_non_empty=False),
        )

    @property
    def restricted(self) -> bool:
        return self.source.restricted

    @property
    def sensitivity(self) -> Optional[str]:
        return self.source.sensitivity


@dataclass(frozen=True)
class ReaderLongContextPlan:
    """Immutable snapshot of one bounded partitioning decision."""

    plan_id: str
    session_id: str
    source: SourceVersion
    max_candidates_per_set: int
    max_source_locators_per_set: int
    working_sets: tuple[ReaderWorkingSet, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "plan_id", _required_text(self.plan_id, "plan_id"))
        object.__setattr__(self, "session_id", _required_text(self.session_id, "session_id"))
        if not isinstance(self.source, SourceVersion):
            raise ValueError("source must be a SourceVersion")
        object.__setattr__(
            self,
            "max_candidates_per_set",
            _bounded_positive_int(
                self.max_candidates_per_set,
                "max_candidates_per_set",
                MAX_CANDIDATES_PER_WORKING_SET,
            ),
        )
        object.__setattr__(
            self,
            "max_source_locators_per_set",
            _bounded_positive_int(
                self.max_source_locators_per_set,
                "max_source_locators_per_set",
                MAX_SOURCE_LOCATORS_PER_WORKING_SET,
            ),
        )
        working_sets = tuple(self.working_sets)
        if not working_sets:
            raise ValueError("a long-context plan requires at least one working set")
        if any(not isinstance(item, ReaderWorkingSet) for item in working_sets):
            raise ValueError("working_sets must contain ReaderWorkingSet values")
        if len({item.working_set_id for item in working_sets}) != len(working_sets):
            raise ValueError("working_set_id values must be unique within a plan")
        if any(item.session_id != self.session_id for item in working_sets):
            raise ValueError("working sets must use the plan Reader session")
        if any(not self.source.same_version(item.source) for item in working_sets):
            raise ValueError("working sets must use the plan source version")
        object.__setattr__(self, "working_sets", working_sets)

    def get_working_set(self, working_set_id: str) -> ReaderWorkingSet:
        working_set_id = _required_text(working_set_id, "working_set_id")
        for working_set in self.working_sets:
            if working_set.working_set_id == working_set_id:
                return working_set
        raise KeyError(working_set_id)


@dataclass(frozen=True)
class ReaderSummaryCandidate:
    """Caller-supplied summary with direct RC-4 leaf provenance; never evidence or truth."""

    summary_id: str
    session_id: str
    plan_id: str
    working_set_id: str
    card: SegmentCard
    candidate_ids: tuple[str, ...]
    relation_ids: tuple[str, ...]
    rationale: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "summary_id", _required_text(self.summary_id, "summary_id"))
        object.__setattr__(self, "session_id", _required_text(self.session_id, "session_id"))
        object.__setattr__(self, "plan_id", _required_text(self.plan_id, "plan_id"))
        object.__setattr__(
            self, "working_set_id", _required_text(self.working_set_id, "working_set_id")
        )
        if not isinstance(self.card, SegmentCard):
            raise ValueError("card must be a SegmentCard")
        if self.card.fidelity is not SourceFidelity.SUMMARY:
            raise ValueError("RC-6 summary candidates require SUMMARY fidelity")
        object.__setattr__(
            self,
            "candidate_ids",
            _text_tuple(self.candidate_ids, "candidate_ids", require_non_empty=True),
        )
        object.__setattr__(
            self,
            "relation_ids",
            _text_tuple(self.relation_ids, "relation_ids", require_non_empty=False),
        )
        object.__setattr__(self, "rationale", _required_text(self.rationale, "rationale"))

    @property
    def summary(self) -> str:
        return self.card.statement

    @property
    def restricted(self) -> bool:
        return self.card.restricted

    @property
    def sensitivity(self) -> Optional[str]:
        return self.card.sensitivity


@dataclass(frozen=True)
class LongContextTelemetry:
    """Counts only; no comprehension, truth, confidence, or evidence-sufficiency score."""

    total_plans: int
    total_working_sets: int
    planned_candidate_references: int
    carried_relation_references: int
    total_summaries: int


class ReaderLongContextStrategy:
    """RC-6 controller over one RC-4 extractor and optional matching RC-5 registry."""

    __slots__ = ("_extractor", "_relations", "_plans", "_plan_index", "_summaries", "_summary_index")

    def __init__(
        self,
        extractor: ReaderPropositionExtractor,
        relations: Optional[ReaderRelationRegistry] = None,
    ) -> None:
        if not isinstance(extractor, ReaderPropositionExtractor):
            raise ValueError("extractor must be a ReaderPropositionExtractor")
        if extractor.reader.session.state is not ReaderSessionState.OPEN:
            raise ValueError("RC-6 requires an OPEN ReaderSession")
        if relations is not None:
            if not isinstance(relations, ReaderRelationRegistry):
                raise ValueError("relations must be a ReaderRelationRegistry")
            if relations.extractor is not extractor:
                raise ValueError("RC-5 registry must use the same RC-4 extractor")
        self._extractor = extractor
        self._relations = relations
        self._plans: list[ReaderLongContextPlan] = []
        self._plan_index: Dict[str, int] = {}
        self._summaries: list[ReaderSummaryCandidate] = []
        self._summary_index: Dict[str, int] = {}

    @property
    def extractor(self) -> ReaderPropositionExtractor:
        return self._extractor

    @property
    def relations(self) -> Optional[ReaderRelationRegistry]:
        return self._relations

    @property
    def plans(self) -> tuple[ReaderLongContextPlan, ...]:
        return tuple(self._plans)

    @property
    def summaries(self) -> tuple[ReaderSummaryCandidate, ...]:
        return tuple(self._summaries)

    def get_plan(self, plan_id: str) -> ReaderLongContextPlan:
        plan_id = _required_text(plan_id, "plan_id")
        try:
            return self._plans[self._plan_index[plan_id]]
        except KeyError as exc:
            raise KeyError(plan_id) from exc

    def get_summary(self, summary_id: str) -> ReaderSummaryCandidate:
        summary_id = _required_text(summary_id, "summary_id")
        try:
            return self._summaries[self._summary_index[summary_id]]
        except KeyError as exc:
            raise KeyError(summary_id) from exc

    def build_plan(
        self,
        plan_id: str,
        *,
        max_candidates_per_set: int,
        max_source_locators_per_set: int,
    ) -> ReaderLongContextPlan:
        """Partition current RC-4 candidates into bounded deterministic working sets."""

        self._require_session_open()
        plan_id = _required_text(plan_id, "plan_id")
        if plan_id in self._plan_index:
            raise ValueError(f"duplicate RC-6 plan_id: {plan_id}")
        candidate_budget = _bounded_positive_int(
            max_candidates_per_set,
            "max_candidates_per_set",
            MAX_CANDIDATES_PER_WORKING_SET,
        )
        locator_budget = _bounded_positive_int(
            max_source_locators_per_set,
            "max_source_locators_per_set",
            MAX_SOURCE_LOCATORS_PER_WORKING_SET,
        )

        candidates = tuple(self._extractor.candidates)
        if not candidates:
            raise ValueError("RC-6 planning requires at least one registered RC-4 candidate")
        for candidate in candidates:
            self._validate_candidate(candidate)

        ordered = tuple(
            sorted(
                candidates,
                key=lambda candidate: (
                    self._extractor.reader.structure.get(candidate.node_ids[0]).order,
                    candidate.candidate_id,
                ),
            )
        )
        working_sets: list[ReaderWorkingSet] = []
        current: list[ReaderPropositionCandidate] = []

        for candidate in ordered:
            candidate_locators = self._candidate_locators(candidate)
            if len(candidate_locators) > locator_budget:
                raise ValueError(
                    f"RC-4 candidate {candidate.candidate_id} exceeds the source-locator budget"
                )
            proposed = current + [candidate]
            proposed_locators = self._working_set_locators(proposed)
            if current and (
                len(proposed) > candidate_budget or len(proposed_locators) > locator_budget
            ):
                working_sets.append(self._make_working_set(plan_id, len(working_sets), current))
                current = [candidate]
            else:
                current = proposed

        if current:
            working_sets.append(self._make_working_set(plan_id, len(working_sets), current))

        plan = ReaderLongContextPlan(
            plan_id=plan_id,
            session_id=self._extractor.reader.session.session_id,
            source=self._extractor.reader.session.source,
            max_candidates_per_set=candidate_budget,
            max_source_locators_per_set=locator_budget,
            working_sets=tuple(working_sets),
        )
        self._plan_index[plan_id] = len(self._plans)
        self._plans.append(plan)
        return plan

    def register_summary(
        self,
        summary_id: str,
        plan_id: str,
        working_set_id: str,
        summary: str,
        rationale: str,
    ) -> ReaderSummaryCandidate:
        """Register caller-supplied SUMMARY text with direct RC-4 leaf provenance."""

        self._require_session_open()
        summary_id = _required_text(summary_id, "summary_id")
        if summary_id in self._summary_index:
            raise ValueError(f"duplicate RC-6 summary_id: {summary_id}")
        session = self._extractor.reader.session
        if any(card.card_id == summary_id for card in session.segment_cards):
            raise ValueError(f"Reader SegmentCard id already exists: {summary_id}")

        plan = self.get_plan(plan_id)
        working_set = plan.get_working_set(working_set_id)
        if plan.session_id != session.session_id or not plan.source.same_version(session.source):
            raise ValueError("RC-6 plan is stale for the current Reader session/source version")

        candidates = tuple(self._extractor.get_candidate(cid) for cid in working_set.candidate_ids)
        locators = self._working_set_locators(candidates)
        if tuple(locator.replay_key for locator in locators) != tuple(
            locator.replay_key for locator in working_set.locators
        ):
            raise ValueError("working-set leaf provenance no longer matches current RC-4 candidates")
        for candidate in candidates:
            self._validate_candidate(candidate)

        card = SegmentCard(
            card_id=summary_id,
            locator=locators[0],
            fidelity=SourceFidelity.SUMMARY,
            statement=_required_text(summary, "summary"),
            supporting_locators=locators[1:],
        )
        summary_candidate = ReaderSummaryCandidate(
            summary_id=summary_id,
            session_id=session.session_id,
            plan_id=plan.plan_id,
            working_set_id=working_set.working_set_id,
            card=card,
            candidate_ids=working_set.candidate_ids,
            relation_ids=working_set.relation_ids,
            rationale=rationale,
        )
        session.add_segment_card(card)
        self._summary_index[summary_id] = len(self._summaries)
        self._summaries.append(summary_candidate)
        return summary_candidate

    def telemetry(self) -> LongContextTelemetry:
        return LongContextTelemetry(
            total_plans=len(self._plans),
            total_working_sets=sum(len(plan.working_sets) for plan in self._plans),
            planned_candidate_references=sum(
                len(working_set.candidate_ids)
                for plan in self._plans
                for working_set in plan.working_sets
            ),
            carried_relation_references=sum(
                len(working_set.relation_ids)
                for plan in self._plans
                for working_set in plan.working_sets
            ),
            total_summaries=len(self._summaries),
        )

    def _require_session_open(self) -> None:
        state = self._extractor.reader.session.state
        if state is not ReaderSessionState.OPEN:
            raise ValueError(f"RC-6 session is no longer OPEN: {state.value}")

    def _validate_candidate(self, candidate: ReaderPropositionCandidate) -> None:
        if not isinstance(candidate, ReaderPropositionCandidate):
            raise ValueError("RC-6 inputs must be ReaderPropositionCandidate values")
        reader = self._extractor.reader
        session = reader.session
        if candidate.session_id != session.session_id:
            raise ValueError("RC-4 candidate belongs to a different Reader session")
        if candidate.card.fidelity is not SourceFidelity.EXTRACTED_PROPOSITION:
            raise ValueError("RC-6 requires direct RC-4 EXTRACTED_PROPOSITION leaf candidates")
        locators = self._candidate_locators(candidate)
        if any(not session.source.same_version(locator.source) for locator in locators):
            raise ValueError("RC-4 candidate belongs to a different source version")
        if not any(card is candidate.card for card in session.segment_cards):
            raise ValueError("RC-4 candidate card is not registered in the Reader session")

        record = reader.get_pass(candidate.pass_id)
        if record.state is not ReaderPassState.COMPLETED:
            raise ValueError("RC-6 requires candidates from a COMPLETED Reader pass")
        if record.session_id != session.session_id or not record.source.same_version(session.source):
            raise ValueError("RC-4 candidate pass is stale for the current Reader session/source")
        if len(candidate.node_ids) != len(locators):
            raise ValueError("RC-4 candidate node/provenance cardinality mismatch")

        coverage = session.coverage
        for node_id, locator in zip(candidate.node_ids, locators):
            node = reader.structure.get(node_id)
            if node.status is not StructuralStatus.RECOVERED:
                raise ValueError("RC-6 cannot plan unresolved structural regions")
            if node.locator.replay_key != locator.replay_key:
                raise ValueError("RC-4 candidate provenance no longer matches its structural node")
            entry = coverage.get(node_id)
            if (
                entry is None
                or entry.locator is None
                or entry.locator.replay_key != node.locator.replay_key
                or entry.state not in {CoverageState.PROCESSED, CoverageState.REVISITED}
            ):
                raise ValueError("current coverage/provenance is not valid for RC-6 planning")

    @staticmethod
    def _candidate_locators(candidate: ReaderPropositionCandidate) -> tuple[SourceLocator, ...]:
        return _unique_locators((candidate.primary_locator, *candidate.card.supporting_locators))

    def _working_set_locators(
        self, candidates: Iterable[ReaderPropositionCandidate]
    ) -> tuple[SourceLocator, ...]:
        return _unique_locators(
            locator
            for candidate in candidates
            for locator in (candidate.primary_locator, *candidate.card.supporting_locators)
        )

    def _make_working_set(
        self,
        plan_id: str,
        index: int,
        candidates: list[ReaderPropositionCandidate],
    ) -> ReaderWorkingSet:
        candidate_ids = tuple(candidate.candidate_id for candidate in candidates)
        node_ids: list[str] = []
        seen_nodes: set[str] = set()
        for candidate in candidates:
            for node_id in candidate.node_ids:
                if node_id not in seen_nodes:
                    seen_nodes.add(node_id)
                    node_ids.append(node_id)
        relation_ids: tuple[str, ...] = ()
        if self._relations is not None:
            selected = set(candidate_ids)
            relation_ids = tuple(
                sorted(
                    relation.relation_id
                    for relation in self._relations.relations
                    if relation.left.candidate_id in selected
                    and relation.right.candidate_id in selected
                )
            )
        return ReaderWorkingSet(
            working_set_id=f"{plan_id}:ws-{index + 1:04d}",
            session_id=self._extractor.reader.session.session_id,
            source=self._extractor.reader.session.source,
            candidate_ids=candidate_ids,
            node_ids=tuple(node_ids),
            locators=self._working_set_locators(candidates),
            relation_ids=relation_ids,
        )


__all__ = [
    "LongContextTelemetry",
    "MAX_CANDIDATES_PER_WORKING_SET",
    "MAX_SOURCE_LOCATORS_PER_WORKING_SET",
    "ReaderLongContextPlan",
    "ReaderLongContextStrategy",
    "ReaderSummaryCandidate",
    "ReaderWorkingSet",
]
