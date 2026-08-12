from __future__ import annotations

import ast
import dataclasses
import inspect

import pytest

import core.reader_long_context as reader_long_context
from core.reader_core import (
    CoverageState,
    ReaderSession,
    SegmentCard,
    SourceFidelity,
    SourceLocator,
    SourceVersion,
)
from core.reader_extraction import PropositionKind, ReaderPropositionExtractor
from core.reader_long_context import (
    MAX_CANDIDATES_PER_WORKING_SET,
    MAX_SOURCE_LOCATORS_PER_WORKING_SET,
    ReaderLongContextPlan,
    ReaderLongContextStrategy,
    ReaderSummaryCandidate,
    ReaderWorkingSet,
)
from core.reader_passes import MultiPassReader, ReaderPassKind, ReaderPassState
from core.reader_relations import ReaderRelationKind, ReaderRelationRegistry
from core.reader_structure import (
    DocumentStructuralMap,
    StructuralKind,
    StructuralNode,
    StructuralStatus,
)


def _source(text: str = "x" * 500, *, restricted: bool = False) -> SourceVersion:
    return SourceVersion.from_text(
        "doc-long",
        "file:///doc-long.txt",
        text,
        restricted=restricted,
        sensitivity="private" if restricted else None,
    )


def _loc(source: SourceVersion, start: int, end: int) -> SourceLocator:
    return SourceLocator(source, span_start=start, span_end=end)


def _extractor(
    *,
    restricted: bool = False,
) -> tuple[SourceVersion, ReaderSession, ReaderPropositionExtractor]:
    source = _source(restricted=restricted)
    session = ReaderSession("session-long", source, "bounded long-context reading")
    nodes = [
        StructuralNode("doc", StructuralKind.DOCUMENT, _loc(source, 0, 500), 0),
        StructuralNode("p-a", StructuralKind.PARAGRAPH, _loc(source, 10, 20), 1, "doc"),
        StructuralNode("p-b", StructuralKind.PARAGRAPH, _loc(source, 30, 40), 2, "doc"),
        StructuralNode("p-c", StructuralKind.PARAGRAPH, _loc(source, 50, 60), 3, "doc"),
        StructuralNode("p-d", StructuralKind.PARAGRAPH, _loc(source, 70, 80), 4, "doc"),
        StructuralNode("p-e", StructuralKind.PARAGRAPH, _loc(source, 90, 100), 5, "doc"),
    ]
    structure = DocumentStructuralMap(source, nodes)
    reader = MultiPassReader(session, structure)
    reader.begin_pass("broad", ReaderPassKind.BROAD_READ, ("p-a", "p-b", "p-c", "p-d", "p-e"))
    for node_id in ("p-a", "p-b", "p-c", "p-d", "p-e"):
        reader.record_region("broad", node_id, CoverageState.PROCESSED)
    reader.complete_pass("broad")

    extractor = ReaderPropositionExtractor(reader)
    extractor.extract(
        "candidate-z",
        "broad",
        "A later-normalized statement from the first paragraph",
        PropositionKind.FACTUAL_ASSERTION,
        "author",
        "p-a",
    )
    extractor.extract(
        "candidate-a",
        "broad",
        "An earlier-normalized statement from the first paragraph",
        PropositionKind.AUTHOR_OPINION,
        "author",
        "p-a",
    )
    extractor.extract(
        "candidate-b",
        "broad",
        "A statement supported by two source regions",
        PropositionKind.HYPOTHESIS,
        "author",
        "p-b",
        supporting_node_ids=("p-c",),
    )
    extractor.extract(
        "candidate-d",
        "broad",
        "A fourth statement",
        PropositionKind.CONDITIONAL,
        "author",
        "p-d",
    )
    extractor.extract(
        "candidate-e",
        "broad",
        "A fifth statement",
        PropositionKind.DEFINITION,
        "author",
        "p-e",
    )
    return source, session, extractor


def _registry(extractor: ReaderPropositionExtractor) -> ReaderRelationRegistry:
    registry = ReaderRelationRegistry(extractor)
    registry.register(
        "relation-in-first-set",
        ReaderRelationKind.TENSION,
        "candidate-z",
        "candidate-a",
        "two presentations from one region deserve joint inspection",
    )
    registry.register(
        "relation-in-second-set",
        ReaderRelationKind.QUALIFICATION,
        "candidate-b",
        "candidate-d",
        "the fourth statement qualifies the two-region statement",
    )
    registry.register(
        "relation-cross-set",
        ReaderRelationKind.POSSIBLE_CONTRADICTION,
        "candidate-a",
        "candidate-b",
        "kept outside a working set when the sides are partitioned",
    )
    return registry


def _working_set(source: SourceVersion, *, session_id: str = "session-long") -> ReaderWorkingSet:
    return ReaderWorkingSet(
        "plan:ws-0001",
        session_id,
        source,
        ("candidate-a",),
        ("p-a",),
        (_loc(source, 10, 20),),
        (),
    )


def test_working_set_contract_validation_privacy_and_deduplicated_provenance():
    source = _source(restricted=True)
    locator = _loc(source, 10, 20)
    item = ReaderWorkingSet(
        " set ",
        " session ",
        source,
        (" candidate ",),
        (" node ",),
        (locator, locator),
        (" relation ",),
    )
    assert item.working_set_id == "set"
    assert item.session_id == "session"
    assert item.candidate_ids == ("candidate",)
    assert item.node_ids == ("node",)
    assert item.locators == (locator,)
    assert item.relation_ids == ("relation",)
    assert item.restricted is True
    assert item.sensitivity == "private"

    with pytest.raises(ValueError, match="working_set_id"):
        ReaderWorkingSet(" ", "s", source, ("c",), ("n",), (locator,))
    with pytest.raises(ValueError, match="session_id"):
        ReaderWorkingSet("w", " ", source, ("c",), ("n",), (locator,))
    with pytest.raises(ValueError, match="SourceVersion"):
        ReaderWorkingSet("w", "s", object(), ("c",), ("n",), (locator,))  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="iterable of strings"):
        ReaderWorkingSet("w", "s", source, "c", ("n",), (locator,))  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="must not be empty"):
        ReaderWorkingSet("w", "s", source, (), ("n",), (locator,))
    with pytest.raises(ValueError, match="unique"):
        ReaderWorkingSet("w", "s", source, ("c", "c"), ("n",), (locator,))
    with pytest.raises(ValueError, match="iterable of strings"):
        ReaderWorkingSet("w", "s", source, None, ("n",), (locator,))  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="must not be empty"):
        ReaderWorkingSet("w", "s", source, ("c",), (), (locator,))
    with pytest.raises(ValueError, match="SourceLocator"):
        ReaderWorkingSet("w", "s", source, ("c",), ("n",), (object(),))  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="locators must not be empty"):
        ReaderWorkingSet("w", "s", source, ("c",), ("n",), ())
    other = _source("changed")
    with pytest.raises(ValueError, match="source version"):
        ReaderWorkingSet("w", "s", source, ("c",), ("n",), (_loc(other, 1, 2),))
    with pytest.raises(ValueError, match="unique"):
        ReaderWorkingSet("w", "s", source, ("c",), ("n",), (locator,), ("r", "r"))


def test_plan_and_summary_domain_validation_and_no_authority_fields():
    source = _source()
    working_set = _working_set(source)
    plan = ReaderLongContextPlan(" plan ", " session-long ", source, 2, 3, (working_set,))
    assert plan.plan_id == "plan"
    assert plan.get_working_set(" plan:ws-0001 ") is working_set
    with pytest.raises(KeyError, match="missing"):
        plan.get_working_set("missing")
    with pytest.raises(ValueError, match="working_set_id"):
        plan.get_working_set(" ")

    with pytest.raises(ValueError, match="plan_id"):
        ReaderLongContextPlan(" ", "s", source, 1, 1, (working_set,))
    with pytest.raises(ValueError, match="session_id"):
        ReaderLongContextPlan("p", " ", source, 1, 1, (working_set,))
    with pytest.raises(ValueError, match="SourceVersion"):
        ReaderLongContextPlan("p", "s", object(), 1, 1, (working_set,))  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="max_candidates_per_set"):
        ReaderLongContextPlan("p", "session-long", source, 0, 1, (working_set,))
    with pytest.raises(ValueError, match="max_source_locators_per_set"):
        ReaderLongContextPlan("p", "session-long", source, 1, True, (working_set,))  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="at least one working set"):
        ReaderLongContextPlan("p", "session-long", source, 1, 1, ())
    with pytest.raises(ValueError, match="ReaderWorkingSet"):
        ReaderLongContextPlan("p", "session-long", source, 1, 1, (object(),))  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="working_set_id values"):
        ReaderLongContextPlan("p", "session-long", source, 1, 1, (working_set, working_set))
    wrong_session = _working_set(source, session_id="other")
    with pytest.raises(ValueError, match="plan Reader session"):
        ReaderLongContextPlan("p", "session-long", source, 1, 1, (wrong_session,))
    other = _source("other")
    wrong_source = _working_set(other)
    with pytest.raises(ValueError, match="plan source version"):
        ReaderLongContextPlan("p", "session-long", source, 1, 1, (wrong_source,))

    card = SegmentCard("summary", _loc(source, 10, 20), SourceFidelity.SUMMARY, "summary text")
    summary = ReaderSummaryCandidate(
        " summary ",
        " session-long ",
        " plan ",
        " set ",
        card,
        (" candidate-a ",),
        (" relation ",),
        " explicit bounded synthesis ",
    )
    assert summary.summary_id == "summary"
    assert summary.summary == "summary text"
    assert summary.candidate_ids == ("candidate-a",)
    assert summary.relation_ids == ("relation",)
    assert summary.restricted is False
    assert summary.sensitivity is None

    with pytest.raises(ValueError, match="summary_id"):
        ReaderSummaryCandidate(" ", "s", "p", "w", card, ("c",), (), "why")
    with pytest.raises(ValueError, match="card must"):
        ReaderSummaryCandidate("s", "s", "p", "w", object(), ("c",), (), "why")  # type: ignore[arg-type]
    proposition_card = SegmentCard(
        "prop", _loc(source, 10, 20), SourceFidelity.EXTRACTED_PROPOSITION, "prop"
    )
    with pytest.raises(ValueError, match="SUMMARY fidelity"):
        ReaderSummaryCandidate("s", "s", "p", "w", proposition_card, ("c",), (), "why")
    with pytest.raises(ValueError, match="candidate_ids must not be empty"):
        ReaderSummaryCandidate("s", "s", "p", "w", card, (), (), "why")
    with pytest.raises(ValueError, match="unique"):
        ReaderSummaryCandidate("s", "s", "p", "w", card, ("c",), ("r", "r"), "why")
    with pytest.raises(ValueError, match="rationale"):
        ReaderSummaryCandidate("s", "s", "p", "w", card, ("c",), (), " ")

    public_fields = {
        field.name
        for cls in (ReaderWorkingSet, ReaderLongContextPlan, ReaderSummaryCandidate)
        for field in dataclasses.fields(cls)
    }
    for forbidden in (
        "truth_status",
        "confidence",
        "evidence_sufficiency",
        "resolved",
        "winner",
        "canon",
    ):
        assert forbidden not in public_fields


def test_strategy_builds_deterministic_bounded_sets_and_only_carries_internal_relations():
    source, session, extractor = _extractor(restricted=True)
    registry = _registry(extractor)
    strategy = ReaderLongContextStrategy(extractor, registry)

    plan = strategy.build_plan(
        "plan-main",
        max_candidates_per_set=2,
        max_source_locators_per_set=3,
    )

    assert strategy.extractor is extractor
    assert strategy.relations is registry
    assert strategy.plans == (plan,)
    assert plan.session_id == session.session_id
    assert plan.source.same_version(source)
    assert plan.max_candidates_per_set == 2
    assert plan.max_source_locators_per_set == 3
    assert [item.working_set_id for item in plan.working_sets] == [
        "plan-main:ws-0001",
        "plan-main:ws-0002",
        "plan-main:ws-0003",
    ]
    assert [item.candidate_ids for item in plan.working_sets] == [
        ("candidate-a", "candidate-z"),
        ("candidate-b", "candidate-d"),
        ("candidate-e",),
    ]
    assert plan.working_sets[0].node_ids == ("p-a",)
    assert plan.working_sets[1].node_ids == ("p-b", "p-c", "p-d")
    assert len(plan.working_sets[0].locators) == 1
    assert len(plan.working_sets[1].locators) == 3
    assert plan.working_sets[0].relation_ids == ("relation-in-first-set",)
    assert plan.working_sets[1].relation_ids == ("relation-in-second-set",)
    assert plan.working_sets[2].relation_ids == ()
    assert "relation-cross-set" not in {
        relation_id
        for item in plan.working_sets
        for relation_id in item.relation_ids
    }
    assert all(item.restricted for item in plan.working_sets)
    assert all(item.sensitivity == "private" for item in plan.working_sets)

    telemetry = strategy.telemetry()
    assert telemetry.total_plans == 1
    assert telemetry.total_working_sets == 3
    assert telemetry.planned_candidate_references == 5
    assert telemetry.carried_relation_references == 2
    assert telemetry.total_summaries == 0

    without_relations = ReaderLongContextStrategy(extractor)
    assert without_relations.relations is None
    simple = without_relations.build_plan(
        "simple",
        max_candidates_per_set=5,
        max_source_locators_per_set=8,
    )
    assert len(simple.working_sets) == 1
    assert simple.working_sets[0].relation_ids == ()


def test_strategy_constructor_lookup_budget_empty_input_and_duplicate_plan_fail_closed():
    with pytest.raises(ValueError, match="ReaderPropositionExtractor"):
        ReaderLongContextStrategy(object())  # type: ignore[arg-type]

    _, session, extractor = _extractor()
    registry = _registry(extractor)
    with pytest.raises(ValueError, match="ReaderRelationRegistry"):
        ReaderLongContextStrategy(extractor, object())  # type: ignore[arg-type]
    _, _, other_extractor = _extractor()
    other_registry = ReaderRelationRegistry(other_extractor)
    with pytest.raises(ValueError, match="same RC-4 extractor"):
        ReaderLongContextStrategy(extractor, other_registry)

    strategy = ReaderLongContextStrategy(extractor, registry)
    with pytest.raises(ValueError, match="plan_id"):
        strategy.build_plan(" ", max_candidates_per_set=1, max_source_locators_per_set=1)
    with pytest.raises(ValueError, match="max_candidates_per_set"):
        strategy.build_plan(
            "bad-candidates",
            max_candidates_per_set=MAX_CANDIDATES_PER_WORKING_SET + 1,
            max_source_locators_per_set=1,
        )
    with pytest.raises(ValueError, match="max_source_locators_per_set"):
        strategy.build_plan(
            "bad-locators",
            max_candidates_per_set=1,
            max_source_locators_per_set=MAX_SOURCE_LOCATORS_PER_WORKING_SET + 1,
        )
    strategy.build_plan("dup", max_candidates_per_set=5, max_source_locators_per_set=8)
    with pytest.raises(ValueError, match="duplicate RC-6 plan_id"):
        strategy.build_plan("dup", max_candidates_per_set=5, max_source_locators_per_set=8)
    assert strategy.get_plan(" dup ").plan_id == "dup"
    with pytest.raises(ValueError, match="plan_id"):
        strategy.get_plan(" ")
    with pytest.raises(KeyError, match="unknown"):
        strategy.get_plan("unknown")
    with pytest.raises(ValueError, match="summary_id"):
        strategy.get_summary(" ")
    with pytest.raises(KeyError, match="unknown"):
        strategy.get_summary("unknown")

    empty_source = _source("empty")
    empty_session = ReaderSession("empty", empty_source, "empty")
    empty_structure = DocumentStructuralMap(
        empty_source,
        [StructuralNode("doc", StructuralKind.DOCUMENT, _loc(empty_source, 0, 5), 0)],
    )
    empty_extractor = ReaderPropositionExtractor(MultiPassReader(empty_session, empty_structure))
    empty_strategy = ReaderLongContextStrategy(empty_extractor)
    with pytest.raises(ValueError, match="at least one registered RC-4 candidate"):
        empty_strategy.build_plan(
            "empty",
            max_candidates_per_set=1,
            max_source_locators_per_set=1,
        )

    session.finish()
    with pytest.raises(ValueError, match="OPEN"):
        ReaderLongContextStrategy(extractor)


def test_candidate_that_cannot_fit_locator_budget_fails_atomically():
    _, _, extractor = _extractor()
    strategy = ReaderLongContextStrategy(extractor)
    with pytest.raises(ValueError, match="candidate-b.*source-locator budget"):
        strategy.build_plan(
            "too-small",
            max_candidates_per_set=5,
            max_source_locators_per_set=1,
        )


def test_candidate_revalidation_rejects_tampered_session_fidelity_source_card_pass_and_nodes():
    _, session, extractor = _extractor()
    strategy = ReaderLongContextStrategy(extractor)
    candidate = extractor.get_candidate("candidate-e")

    original_session = candidate.session_id
    object.__setattr__(candidate, "session_id", "other")
    with pytest.raises(ValueError, match="different Reader session"):
        strategy.build_plan("bad-session", max_candidates_per_set=5, max_source_locators_per_set=8)
    object.__setattr__(candidate, "session_id", original_session)

    original_fidelity = candidate.card.fidelity
    object.__setattr__(candidate.card, "fidelity", SourceFidelity.SUMMARY)
    with pytest.raises(ValueError, match="direct RC-4"):
        strategy.build_plan("bad-fidelity", max_candidates_per_set=5, max_source_locators_per_set=8)
    object.__setattr__(candidate.card, "fidelity", original_fidelity)

    original_locator = candidate.card.locator
    other_source = _source("changed")
    object.__setattr__(candidate.card, "locator", _loc(other_source, 90, 100))
    with pytest.raises(ValueError, match="different source version"):
        strategy.build_plan("bad-source", max_candidates_per_set=5, max_source_locators_per_set=8)
    object.__setattr__(candidate.card, "locator", original_locator)

    session._segment_cards.remove(candidate.card)
    with pytest.raises(ValueError, match="not registered"):
        strategy.build_plan("missing-card", max_candidates_per_set=5, max_source_locators_per_set=8)
    session._segment_cards.append(candidate.card)

    record = extractor.reader.get_pass(candidate.pass_id)
    object.__setattr__(record, "state", ReaderPassState.ATTEMPTED)
    with pytest.raises(ValueError, match="COMPLETED"):
        strategy.build_plan("bad-pass-state", max_candidates_per_set=5, max_source_locators_per_set=8)
    object.__setattr__(record, "state", ReaderPassState.COMPLETED)

    original_pass_session = record.session_id
    object.__setattr__(record, "session_id", "other")
    with pytest.raises(ValueError, match="pass is stale"):
        strategy.build_plan("bad-pass-session", max_candidates_per_set=5, max_source_locators_per_set=8)
    object.__setattr__(record, "session_id", original_pass_session)

    original_nodes = candidate.node_ids
    object.__setattr__(candidate, "node_ids", ("p-e", "p-d"))
    with pytest.raises(ValueError, match="cardinality"):
        strategy.build_plan("bad-cardinality", max_candidates_per_set=5, max_source_locators_per_set=8)
    object.__setattr__(candidate, "node_ids", original_nodes)

    node = extractor.reader.structure.get("p-e")
    object.__setattr__(node, "status", StructuralStatus.AMBIGUOUS)
    with pytest.raises(ValueError, match="unresolved structural"):
        strategy.build_plan("bad-structure", max_candidates_per_set=5, max_source_locators_per_set=8)
    object.__setattr__(node, "status", StructuralStatus.RECOVERED)

    object.__setattr__(candidate.card, "locator", _loc(session.source, 91, 100))
    with pytest.raises(ValueError, match="no longer matches"):
        strategy.build_plan("bad-node-locator", max_candidates_per_set=5, max_source_locators_per_set=8)
    object.__setattr__(candidate.card, "locator", original_locator)

    original_coverage = session._coverage["p-e"]
    session._coverage["p-e"] = dataclasses.replace(original_coverage, state=CoverageState.SEEN)
    with pytest.raises(ValueError, match="coverage/provenance"):
        strategy.build_plan("bad-coverage", max_candidates_per_set=5, max_source_locators_per_set=8)
    session._coverage["p-e"] = original_coverage

    original_candidates = extractor._candidates
    extractor._candidates = [object()]  # type: ignore[list-item]
    with pytest.raises(ValueError, match="ReaderPropositionCandidate"):
        strategy.build_plan("bad-type", max_candidates_per_set=5, max_source_locators_per_set=8)
    extractor._candidates = original_candidates


def test_summary_preserves_direct_leaf_provenance_and_is_registered_as_summary_only():
    _, session, extractor = _extractor(restricted=True)
    registry = _registry(extractor)
    strategy = ReaderLongContextStrategy(extractor, registry)
    plan = strategy.build_plan(
        "plan",
        max_candidates_per_set=2,
        max_source_locators_per_set=3,
    )
    working_set = plan.working_sets[1]

    summary = strategy.register_summary(
        "summary-2",
        "plan",
        working_set.working_set_id,
        "The bounded set contains a hypothesis and a qualifying conditional.",
        "caller-supplied synthesis of this exact working set",
    )

    assert strategy.summaries == (summary,)
    assert strategy.get_summary(" summary-2 ") is summary
    assert summary.session_id == session.session_id
    assert summary.plan_id == "plan"
    assert summary.working_set_id == working_set.working_set_id
    assert summary.card.fidelity is SourceFidelity.SUMMARY
    assert summary.candidate_ids == ("candidate-b", "candidate-d")
    assert summary.relation_ids == ("relation-in-second-set",)
    assert summary.card.locator.replay_key == working_set.locators[0].replay_key
    assert tuple(locator.replay_key for locator in summary.card.supporting_locators) == tuple(
        locator.replay_key for locator in working_set.locators[1:]
    )
    assert any(card is summary.card for card in session.segment_cards)
    assert summary.restricted is True
    assert summary.sensitivity == "private"
    assert strategy.telemetry().total_summaries == 1


def test_summary_validation_duplicate_ids_unknown_sets_stale_plan_and_leaf_drift_fail_closed():
    source, session, extractor = _extractor()
    strategy = ReaderLongContextStrategy(extractor)
    plan = strategy.build_plan("plan", max_candidates_per_set=2, max_source_locators_per_set=3)
    working_set = plan.working_sets[0]

    with pytest.raises(KeyError, match="missing"):
        strategy.register_summary("s", "missing", working_set.working_set_id, "text", "why")
    with pytest.raises(KeyError, match="missing"):
        strategy.register_summary("s", "plan", "missing", "text", "why")
    with pytest.raises(ValueError, match="summary_id"):
        strategy.register_summary(" ", "plan", working_set.working_set_id, "text", "why")
    with pytest.raises(ValueError, match="summary"):
        strategy.register_summary("s", "plan", working_set.working_set_id, " ", "why")
    with pytest.raises(ValueError, match="rationale"):
        strategy.register_summary("s", "plan", working_set.working_set_id, "text", " ")
    with pytest.raises(ValueError, match="SegmentCard id"):
        strategy.register_summary(
            "candidate-a", "plan", working_set.working_set_id, "text", "why"
        )

    strategy.register_summary("s", "plan", working_set.working_set_id, "text", "why")
    with pytest.raises(ValueError, match="duplicate RC-6 summary_id"):
        strategy.register_summary("s", "plan", working_set.working_set_id, "text 2", "why")

    plan2 = strategy.build_plan("stale-plan", max_candidates_per_set=2, max_source_locators_per_set=3)
    object.__setattr__(plan2, "session_id", "other")
    with pytest.raises(ValueError, match="plan is stale"):
        strategy.register_summary(
            "stale-summary",
            "stale-plan",
            plan2.working_sets[0].working_set_id,
            "text",
            "why",
        )
    object.__setattr__(plan2, "session_id", session.session_id)

    plan3 = strategy.build_plan("drift-plan", max_candidates_per_set=2, max_source_locators_per_set=3)
    candidate = extractor.get_candidate(plan3.working_sets[0].candidate_ids[0])
    original_locator = candidate.card.locator
    object.__setattr__(candidate.card, "locator", _loc(source, 11, 20))
    original_node = extractor.reader.structure.get(candidate.node_ids[0])
    object.__setattr__(original_node, "locator", candidate.card.locator)
    original_coverage = session._coverage[candidate.node_ids[0]]
    session._coverage[candidate.node_ids[0]] = dataclasses.replace(
        original_coverage,
        locator=candidate.card.locator,
    )
    with pytest.raises(ValueError, match="leaf provenance no longer matches"):
        strategy.register_summary(
            "drift-summary",
            "drift-plan",
            plan3.working_sets[0].working_set_id,
            "text",
            "why",
        )
    object.__setattr__(candidate.card, "locator", original_locator)
    object.__setattr__(original_node, "locator", original_locator)
    session._coverage[candidate.node_ids[0]] = original_coverage


def test_strategy_operations_fail_after_session_completion_or_source_invalidation():
    source, session, extractor = _extractor()
    strategy = ReaderLongContextStrategy(extractor)
    plan = strategy.build_plan("plan", max_candidates_per_set=2, max_source_locators_per_set=3)
    session.finish()
    with pytest.raises(ValueError, match="no longer OPEN"):
        strategy.build_plan("later", max_candidates_per_set=2, max_source_locators_per_set=3)
    with pytest.raises(ValueError, match="no longer OPEN"):
        strategy.register_summary(
            "summary",
            "plan",
            plan.working_sets[0].working_set_id,
            "text",
            "why",
        )

    source2, session2, extractor2 = _extractor()
    stale_strategy = ReaderLongContextStrategy(extractor2)
    changed = SourceVersion.from_text(source2.document_id, source2.source_uri, "changed source")
    assert session2.invalidate_for(changed).stale is True
    with pytest.raises(ValueError, match="no longer OPEN"):
        stale_strategy.build_plan(
            "stale",
            max_candidates_per_set=2,
            max_source_locators_per_set=3,
        )


def test_rc6_import_surface_has_no_authority_model_storage_or_cross_document_dependencies():
    source = inspect.getsource(reader_long_context)
    tree = ast.parse(source)
    imported_modules = {
        node.module
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
    }
    assert imported_modules == {
        "__future__",
        "dataclasses",
        "typing",
        "core.reader_core",
        "core.reader_extraction",
        "core.reader_passes",
        "core.reader_relations",
        "core.reader_structure",
    }
    for forbidden in (
        "core.evidence",
        "core.truth_gate",
        "core.pipeline",
        "core.immune",
        "core.canonical_view",
        "core.contradiction",
        "core.contradiction_report",
        "core.esm",
        "psycopg",
        "openai",
        "anthropic",
    ):
        assert forbidden not in imported_modules

    lowered = source.lower()
    assert "attach_evidence(" not in lowered
    assert "truth_status" not in lowered
    assert "evidence_sufficiency" not in lowered
    assert "winner" not in lowered
    assert "embedding" not in lowered
    assert "vector database" not in lowered
    assert "cross-document" in lowered
    assert "no model/provider call" in lowered
