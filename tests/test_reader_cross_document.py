from __future__ import annotations

import ast
import dataclasses
import inspect

import pytest

import core.reader_cross_document as cross_document
from core.reader_core import (
    CoverageState,
    ReaderSession,
    SourceFidelity,
    SourceLocator,
    SourceVersion,
)
from core.reader_cross_document import (
    MAX_LINK_CANDIDATES,
    MAX_REGISTERED_SOURCES,
    CrossDocumentInspectionBasis,
    CrossDocumentLinkCandidate,
    CrossDocumentLinkKind,
    CrossDocumentLinkSide,
    ReaderCrossDocumentRegistry,
)
from core.reader_extraction import PropositionKind, ReaderPropositionExtractor
from core.reader_passes import MultiPassReader, ReaderPassKind, ReaderPassState
from core.reader_structure import (
    DocumentStructuralMap,
    StructuralKind,
    StructuralNode,
    StructuralStatus,
)


def _source(
    document_id: str,
    session_id: str,
    *,
    restricted: bool = False,
    sensitivity: str | None = None,
) -> SourceVersion:
    return SourceVersion.from_text(
        document_id,
        f"file:///{document_id}-{session_id}.txt",
        (document_id + session_id) * 80,
        restricted=restricted,
        sensitivity=sensitivity,
    )


def _loc(source: SourceVersion, start: int, end: int) -> SourceLocator:
    return SourceLocator(source, span_start=start, span_end=end)


def _extractor(
    document_id: str,
    session_id: str,
    candidate_id: str,
    *,
    restricted: bool = False,
    sensitivity: str | None = None,
) -> tuple[SourceVersion, ReaderSession, MultiPassReader, ReaderPropositionExtractor]:
    source = _source(
        document_id,
        session_id,
        restricted=restricted,
        sensitivity=sensitivity,
    )
    session = ReaderSession(session_id, source, "compare across documents")
    structure = DocumentStructuralMap(
        source,
        (
            StructuralNode(
                "doc",
                StructuralKind.DOCUMENT,
                _loc(source, 0, 100),
                0,
            ),
            StructuralNode(
                "p-a",
                StructuralKind.PARAGRAPH,
                _loc(source, 10, 20),
                1,
                "doc",
            ),
            StructuralNode(
                "p-b",
                StructuralKind.PARAGRAPH,
                _loc(source, 30, 40),
                2,
                "doc",
            ),
        ),
    )
    reader = MultiPassReader(session, structure)
    reader.begin_pass(
        "broad",
        ReaderPassKind.BROAD_READ,
        ("p-a", "p-b"),
    )
    reader.record_region("broad", "p-a", CoverageState.PROCESSED)
    reader.record_region("broad", "p-b", CoverageState.PROCESSED)
    reader.complete_pass("broad")
    extractor = ReaderPropositionExtractor(reader)
    extractor.extract(
        candidate_id,
        "broad",
        f"{document_id} proposition",
        PropositionKind.FACTUAL_ASSERTION,
        "author",
        "p-a",
        supporting_node_ids=("p-b",),
    )
    return source, session, reader, extractor


def _pair():
    left = _extractor("doc-a", "session-a", "candidate-a")
    right = _extractor(
        "doc-b",
        "session-b",
        "candidate-b",
        restricted=True,
        sensitivity="restricted-research",
    )
    return left, right


def test_rc7_vocabularies_and_limits_are_explicit():
    assert {kind.value for kind in CrossDocumentLinkKind} == {
        "SUPPORTS",
        "CONTRADICTS",
        "ELABORATES",
        "REFERENCES",
        "DEFINES",
        "EXAMPLE_OF",
        "PREREQUISITE_FOR",
        "SAME_TOPIC",
        "POSSIBLE_SAME_CLAIM",
    }
    assert {basis.value for basis in CrossDocumentInspectionBasis} == {
        "EXPLICIT_SOURCE_REFERENCE",
        "CALLER_COMPARISON",
        "LEXICAL_SIMILARITY_SIGNAL",
        "SHARED_TOPIC_SIGNAL",
        "OTHER",
    }
    assert MAX_REGISTERED_SOURCES == 32
    assert MAX_LINK_CANDIDATES == 4096


def test_side_snapshot_properties_and_validation():
    left, _ = _pair()
    source, _, _, extractor = left
    candidate = extractor.get_candidate("candidate-a")
    side = CrossDocumentLinkSide.from_candidate(candidate)

    assert side.session_id == "session-a"
    assert side.candidate_id == "candidate-a"
    assert side.pass_id == "broad"
    assert side.node_ids == ("p-a", "p-b")
    assert side.document_id == "doc-a"
    assert side.restricted is False
    assert side.sensitivity is None
    assert side.sort_key[:3] == (
        source.document_id,
        source.source_uri,
        source.source_sha256,
    )

    with pytest.raises(ValueError, match="ReaderPropositionCandidate"):
        CrossDocumentLinkSide.from_candidate(object())  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="session_id"):
        dataclasses.replace(side, session_id=" ")
    with pytest.raises(ValueError, match="candidate_id"):
        dataclasses.replace(side, candidate_id=" ")
    with pytest.raises(ValueError, match="pass_id"):
        dataclasses.replace(side, pass_id=" ")
    with pytest.raises(ValueError, match="iterable"):
        dataclasses.replace(side, node_ids="p-a")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="iterable"):
        dataclasses.replace(side, node_ids=object())  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="must not be empty"):
        dataclasses.replace(side, node_ids=())
    with pytest.raises(ValueError, match="unique"):
        dataclasses.replace(side, node_ids=("p-a", "p-a"))
    with pytest.raises(ValueError, match="source"):
        dataclasses.replace(side, source=object())  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="primary_locator"):
        dataclasses.replace(side, primary_locator=object())  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="SourceLocator"):
        dataclasses.replace(
            side,
            supporting_locators=(object(),),  # type: ignore[arg-type]
        )
    with pytest.raises(ValueError, match=r"primary \+ supporting"):
        dataclasses.replace(side, supporting_locators=())
    changed = _source("doc-a", "changed")
    with pytest.raises(ValueError, match="exact source and privacy"):
        dataclasses.replace(
            side,
            source=changed,
            primary_locator=_loc(changed, 10, 20),
            supporting_locators=(_loc(source, 30, 40),),
        )


def test_link_candidate_properties_no_authority_fields_and_validation():
    left, right = _pair()
    left_side = CrossDocumentLinkSide.from_candidate(
        left[3].get_candidate("candidate-a")
    )
    right_side = CrossDocumentLinkSide.from_candidate(
        right[3].get_candidate("candidate-b")
    )
    link = CrossDocumentLinkCandidate(
        " link ",
        CrossDocumentLinkKind.SUPPORTS,
        left_side,
        right_side,
        " explicit caller comparison ",
        CrossDocumentInspectionBasis.CALLER_COMPARISON,
    )

    assert link.link_id == "link"
    assert link.restricted is True
    assert link.sensitivities == ("restricted-research",)
    assert link.rationale == "explicit caller comparison"

    fields = {field.name for field in dataclasses.fields(CrossDocumentLinkCandidate)}
    for forbidden in (
        "truth_status",
        "confidence",
        "evidence_sufficiency",
        "resolved",
        "winner",
        "identity",
        "similarity_score",
    ):
        assert forbidden not in fields

    with pytest.raises(ValueError, match="link_id"):
        dataclasses.replace(link, link_id=" ")
    with pytest.raises(ValueError, match="CrossDocumentLinkKind"):
        dataclasses.replace(link, kind="SUPPORTS")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="left"):
        dataclasses.replace(link, left=object())  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="right"):
        dataclasses.replace(link, right=object())  # type: ignore[arg-type]
    same_doc_right = dataclasses.replace(
        right_side,
        source=left_side.source,
        primary_locator=left_side.primary_locator,
        supporting_locators=left_side.supporting_locators,
    )
    with pytest.raises(ValueError, match="different document"):
        CrossDocumentLinkCandidate(
            "same-doc",
            CrossDocumentLinkKind.SAME_TOPIC,
            left_side,
            same_doc_right,
            "not allowed",
        )
    with pytest.raises(ValueError, match="rationale"):
        dataclasses.replace(link, rationale=" ")
    with pytest.raises(ValueError, match="inspection_basis"):
        dataclasses.replace(link, inspection_basis="OTHER")  # type: ignore[arg-type]

    sensitive_source = SourceVersion(
        left_side.source.document_id,
        left_side.source.source_uri,
        left_side.source.source_sha256,
        sensitivity="restricted-research",
    )
    both_sensitive_left = dataclasses.replace(
        left_side,
        source=sensitive_source,
        primary_locator=_loc(sensitive_source, 10, 20),
        supporting_locators=(_loc(sensitive_source, 30, 40),),
    )
    duplicate_sensitivity = dataclasses.replace(link, left=both_sensitive_left)
    assert duplicate_sensitivity.sensitivities == ("restricted-research",)


def test_registry_constructor_boundaries_and_public_accessors():
    left, right = _pair()
    registry = ReaderCrossDocumentRegistry((left[3], right[3]), max_links=2)
    assert registry.session_ids == ("session-a", "session-b")
    assert registry.links == ()
    assert registry.max_links == 2

    with pytest.raises(ValueError, match="iterable"):
        ReaderCrossDocumentRegistry("bad")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="iterable"):
        ReaderCrossDocumentRegistry(object())  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="at least two"):
        ReaderCrossDocumentRegistry((left[3],))
    with pytest.raises(ValueError, match="at most"):
        ReaderCrossDocumentRegistry((left[3],) * (MAX_REGISTERED_SOURCES + 1))
    with pytest.raises(ValueError, match="ReaderPropositionExtractor"):
        ReaderCrossDocumentRegistry((left[3], object()))  # type: ignore[arg-type]

    closed = _extractor("doc-c", "session-c", "candidate-c")
    closed[1].finish()
    with pytest.raises(ValueError, match="OPEN"):
        ReaderCrossDocumentRegistry((left[3], closed[3]))

    duplicate_session = _extractor("doc-d", "session-a", "candidate-d")
    with pytest.raises(ValueError, match="session IDs"):
        ReaderCrossDocumentRegistry((left[3], duplicate_session[3]))

    same_doc = _extractor("doc-a", "session-x", "candidate-x")
    with pytest.raises(ValueError, match="distinct document"):
        ReaderCrossDocumentRegistry((left[3], same_doc[3]))

    for invalid in (True, 0, MAX_LINK_CANDIDATES + 1):
        with pytest.raises(ValueError, match="max_links"):
            ReaderCrossDocumentRegistry(
                (left[3], right[3]),
                max_links=invalid,  # type: ignore[arg-type]
            )


@pytest.mark.parametrize(
    ("kind", "symmetric"),
    [
        (CrossDocumentLinkKind.SUPPORTS, False),
        (CrossDocumentLinkKind.CONTRADICTS, True),
        (CrossDocumentLinkKind.ELABORATES, False),
        (CrossDocumentLinkKind.REFERENCES, False),
        (CrossDocumentLinkKind.DEFINES, False),
        (CrossDocumentLinkKind.EXAMPLE_OF, False),
        (CrossDocumentLinkKind.PREREQUISITE_FOR, False),
        (CrossDocumentLinkKind.SAME_TOPIC, True),
        (CrossDocumentLinkKind.POSSIBLE_SAME_CLAIM, True),
    ],
)
def test_registry_registers_all_kinds_and_symmetric_order(kind, symmetric):
    left, right = _pair()
    registry = ReaderCrossDocumentRegistry((right[3], left[3]))
    link = registry.register(
        f"link-{kind.value}",
        kind,
        "session-b",
        "candidate-b",
        "session-a",
        "candidate-a",
        "explicit cross-source inspection",
        inspection_basis=CrossDocumentInspectionBasis.CALLER_COMPARISON,
    )
    if symmetric:
        assert link.left.document_id == "doc-a"
        assert link.right.document_id == "doc-b"
    else:
        assert link.left.document_id == "doc-b"
        assert link.right.document_id == "doc-a"
    assert registry.get_link(f" link-{kind.value} ") is link


def test_registry_rejects_invalid_registration_duplicates_budget_and_same_doc():
    left, right = _pair()
    third_same_doc = _extractor("doc-a", "session-c", "candidate-c")
    registry = ReaderCrossDocumentRegistry(
        (left[3], right[3], third_same_doc[3]),
        max_links=2,
    )

    with pytest.raises(ValueError, match="link_id"):
        registry.register(
            " ",
            CrossDocumentLinkKind.SUPPORTS,
            "session-a",
            "candidate-a",
            "session-b",
            "candidate-b",
            "why",
        )
    with pytest.raises(ValueError, match="CrossDocumentLinkKind"):
        registry.register(
            "bad-kind",
            "SUPPORTS",  # type: ignore[arg-type]
            "session-a",
            "candidate-a",
            "session-b",
            "candidate-b",
            "why",
        )
    with pytest.raises(ValueError, match="inspection_basis"):
        registry.register(
            "bad-basis",
            CrossDocumentLinkKind.SUPPORTS,
            "session-a",
            "candidate-a",
            "session-b",
            "candidate-b",
            "why",
            inspection_basis="OTHER",  # type: ignore[arg-type]
        )
    with pytest.raises(ValueError, match="left_session_id"):
        registry.register(
            "bad-left-session",
            CrossDocumentLinkKind.SUPPORTS,
            " ",
            "candidate-a",
            "session-b",
            "candidate-b",
            "why",
        )
    with pytest.raises(ValueError, match="right_session_id"):
        registry.register(
            "bad-right-session",
            CrossDocumentLinkKind.SUPPORTS,
            "session-a",
            "candidate-a",
            " ",
            "candidate-b",
            "why",
        )
    with pytest.raises(ValueError, match="different Reader sessions"):
        registry.register(
            "same-session",
            CrossDocumentLinkKind.SUPPORTS,
            "session-a",
            "candidate-a",
            "session-a",
            "candidate-a",
            "why",
        )
    with pytest.raises(KeyError, match="missing-session"):
        registry.register(
            "missing-session",
            CrossDocumentLinkKind.SUPPORTS,
            "missing-session",
            "candidate-a",
            "session-b",
            "candidate-b",
            "why",
        )
    with pytest.raises(ValueError, match="candidate_id"):
        registry.register(
            "blank-candidate",
            CrossDocumentLinkKind.SUPPORTS,
            "session-a",
            " ",
            "session-b",
            "candidate-b",
            "why",
        )
    with pytest.raises(KeyError, match="missing"):
        registry.register(
            "missing-candidate",
            CrossDocumentLinkKind.SUPPORTS,
            "session-a",
            "missing",
            "session-b",
            "candidate-b",
            "why",
        )
    with pytest.raises(ValueError, match="different document"):
        registry.register(
            "same-doc",
            CrossDocumentLinkKind.SUPPORTS,
            "session-a",
            "candidate-a",
            "session-c",
            "candidate-c",
            "why",
        )

    first = registry.register(
        "first",
        CrossDocumentLinkKind.CONTRADICTS,
        "session-b",
        "candidate-b",
        "session-a",
        "candidate-a",
        "possible tension",
    )
    assert first.left.document_id == "doc-a"
    with pytest.raises(ValueError, match="link_id"):
        registry.register(
            "first",
            CrossDocumentLinkKind.SUPPORTS,
            "session-a",
            "candidate-a",
            "session-b",
            "candidate-b",
            "other",
        )
    with pytest.raises(ValueError, match="link candidate"):
        registry.register(
            "dup-semantic",
            CrossDocumentLinkKind.CONTRADICTS,
            "session-a",
            "candidate-a",
            "session-b",
            "candidate-b",
            "same semantic link",
        )

    registry.register(
        "second",
        CrossDocumentLinkKind.SUPPORTS,
        "session-a",
        "candidate-a",
        "session-b",
        "candidate-b",
        "directional link",
    )
    with pytest.raises(ValueError, match="budget exhausted"):
        registry.register(
            "third",
            CrossDocumentLinkKind.ELABORATES,
            "session-a",
            "candidate-a",
            "session-b",
            "candidate-b",
            "budget overflow",
        )

    with pytest.raises(ValueError, match="link_id"):
        registry.get_link(" ")
    with pytest.raises(KeyError, match="unknown"):
        registry.get_link("unknown")


def test_directional_reverse_is_distinct_and_telemetry_is_counts_only():
    left, right = _pair()
    registry = ReaderCrossDocumentRegistry((left[3], right[3]))
    registry.register(
        "forward",
        CrossDocumentLinkKind.SUPPORTS,
        "session-a",
        "candidate-a",
        "session-b",
        "candidate-b",
        "A explicitly supports B",
        inspection_basis=CrossDocumentInspectionBasis.EXPLICIT_SOURCE_REFERENCE,
    )
    reverse = registry.register(
        "reverse",
        CrossDocumentLinkKind.SUPPORTS,
        "session-b",
        "candidate-b",
        "session-a",
        "candidate-a",
        "B separately supports A",
        inspection_basis=CrossDocumentInspectionBasis.SHARED_TOPIC_SIGNAL,
    )
    registry.register(
        "topic",
        CrossDocumentLinkKind.SAME_TOPIC,
        "session-a",
        "candidate-a",
        "session-b",
        "candidate-b",
        "same subject",
    )
    assert reverse.left.document_id == "doc-b"

    telemetry = registry.telemetry()
    assert telemetry.total_links == 3
    assert telemetry.restricted_links == 3
    assert telemetry.kind_counts[CrossDocumentLinkKind.SUPPORTS] == 2
    assert telemetry.kind_counts[CrossDocumentLinkKind.SAME_TOPIC] == 1
    assert (
        telemetry.inspection_basis_counts[
            CrossDocumentInspectionBasis.EXPLICIT_SOURCE_REFERENCE
        ]
        == 1
    )
    assert (
        telemetry.inspection_basis_counts[
            CrossDocumentInspectionBasis.SHARED_TOPIC_SIGNAL
        ]
        == 1
    )


def test_registry_fails_closed_when_session_is_no_longer_open():
    left, right = _pair()
    registry = ReaderCrossDocumentRegistry((left[3], right[3]))
    right[1].finish()
    with pytest.raises(ValueError, match="no longer OPEN"):
        registry.register(
            "closed",
            CrossDocumentLinkKind.SUPPORTS,
            "session-a",
            "candidate-a",
            "session-b",
            "candidate-b",
            "closed session",
        )


def test_current_candidate_session_fidelity_source_and_card_guards():
    left, right = _pair()
    registry = ReaderCrossDocumentRegistry((left[3], right[3]))
    candidate = left[3].get_candidate("candidate-a")

    original_session_id = candidate.session_id
    object.__setattr__(candidate, "session_id", "wrong-session")
    with pytest.raises(ValueError, match="different Reader session"):
        registry.register(
            "bad-session",
            CrossDocumentLinkKind.SUPPORTS,
            "session-a",
            "candidate-a",
            "session-b",
            "candidate-b",
            "why",
        )
    object.__setattr__(candidate, "session_id", original_session_id)

    original_card = candidate.card
    summary_card = dataclasses.replace(
        original_card,
        fidelity=SourceFidelity.SUMMARY,
    )
    object.__setattr__(candidate, "card", summary_card)
    with pytest.raises(ValueError, match="EXTRACTED_PROPOSITION"):
        registry.register(
            "bad-fidelity",
            CrossDocumentLinkKind.SUPPORTS,
            "session-a",
            "candidate-a",
            "session-b",
            "candidate-b",
            "why",
        )
    object.__setattr__(candidate, "card", original_card)

    other_source = _source("doc-a", "other")
    other_card = dataclasses.replace(
        original_card,
        locator=_loc(other_source, 10, 20),
        supporting_locators=(_loc(other_source, 30, 40),),
    )
    object.__setattr__(candidate, "card", other_card)
    with pytest.raises(ValueError, match="exact source binding"):
        registry.register(
            "bad-source",
            CrossDocumentLinkKind.SUPPORTS,
            "session-a",
            "candidate-a",
            "session-b",
            "candidate-b",
            "why",
        )
    object.__setattr__(candidate, "card", original_card)

    left[1]._segment_cards.remove(original_card)
    with pytest.raises(ValueError, match="not registered"):
        registry.register(
            "missing-card",
            CrossDocumentLinkKind.SUPPORTS,
            "session-a",
            "candidate-a",
            "session-b",
            "candidate-b",
            "why",
        )
    left[1]._segment_cards.append(original_card)


def test_current_candidate_pass_and_cardinality_guards():
    left, right = _pair()
    registry = ReaderCrossDocumentRegistry((left[3], right[3]))
    candidate = left[3].get_candidate("candidate-a")
    record = left[2].get_pass("broad")

    original_state = record.state
    object.__setattr__(record, "state", ReaderPassState.ATTEMPTED)
    with pytest.raises(ValueError, match="COMPLETED"):
        registry.register(
            "pass-state",
            CrossDocumentLinkKind.SUPPORTS,
            "session-a",
            "candidate-a",
            "session-b",
            "candidate-b",
            "why",
        )
    object.__setattr__(record, "state", original_state)

    original_record_session = record.session_id
    object.__setattr__(record, "session_id", "wrong-session")
    with pytest.raises(ValueError, match="pass no longer matches"):
        registry.register(
            "pass-session",
            CrossDocumentLinkKind.SUPPORTS,
            "session-a",
            "candidate-a",
            "session-b",
            "candidate-b",
            "why",
        )
    object.__setattr__(record, "session_id", original_record_session)

    original_source = record.source
    object.__setattr__(record, "source", _source("doc-a", "different-pass-source"))
    with pytest.raises(ValueError, match="pass no longer matches"):
        registry.register(
            "pass-source",
            CrossDocumentLinkKind.SUPPORTS,
            "session-a",
            "candidate-a",
            "session-b",
            "candidate-b",
            "why",
        )
    object.__setattr__(record, "source", original_source)

    original_nodes = candidate.node_ids
    object.__setattr__(candidate, "node_ids", ("p-a",))
    with pytest.raises(ValueError, match="cardinality"):
        registry.register(
            "cardinality",
            CrossDocumentLinkKind.SUPPORTS,
            "session-a",
            "candidate-a",
            "session-b",
            "candidate-b",
            "why",
        )
    object.__setattr__(candidate, "node_ids", original_nodes)


def test_current_candidate_pass_target_outcome_and_structure_guards():
    left, right = _pair()
    registry = ReaderCrossDocumentRegistry((left[3], right[3]))
    candidate = left[3].get_candidate("candidate-a")
    record = left[2].get_pass("broad")

    original_targets = record.target_node_ids
    object.__setattr__(record, "target_node_ids", ("p-b",))
    with pytest.raises(ValueError, match="declared pass target"):
        registry.register(
            "not-target",
            CrossDocumentLinkKind.SUPPORTS,
            "session-a",
            "candidate-a",
            "session-b",
            "candidate-b",
            "why",
        )
    object.__setattr__(record, "target_node_ids", original_targets)

    original_outcomes = record.outcomes
    object.__setattr__(record, "outcomes", record.outcomes[1:])
    with pytest.raises(ValueError, match="outcome is not substantive"):
        registry.register(
            "missing-outcome",
            CrossDocumentLinkKind.SUPPORTS,
            "session-a",
            "candidate-a",
            "session-b",
            "candidate-b",
            "why",
        )
    object.__setattr__(record, "outcomes", original_outcomes)

    first_outcome = record.outcomes[0]
    original_after = first_outcome.after
    object.__setattr__(first_outcome, "after", CoverageState.SEEN)
    with pytest.raises(ValueError, match="outcome is not substantive"):
        registry.register(
            "weak-outcome",
            CrossDocumentLinkKind.SUPPORTS,
            "session-a",
            "candidate-a",
            "session-b",
            "candidate-b",
            "why",
        )
    object.__setattr__(first_outcome, "after", original_after)

    node = left[2].structure.get(candidate.node_ids[0])
    original_status = node.status
    object.__setattr__(node, "status", StructuralStatus.AMBIGUOUS)
    with pytest.raises(ValueError, match="unresolved"):
        registry.register(
            "unresolved-node",
            CrossDocumentLinkKind.SUPPORTS,
            "session-a",
            "candidate-a",
            "session-b",
            "candidate-b",
            "why",
        )
    object.__setattr__(node, "status", original_status)

    original_locator = node.locator
    object.__setattr__(node, "locator", _loc(left[0], 11, 19))
    with pytest.raises(ValueError, match="structural provenance"):
        registry.register(
            "node-provenance",
            CrossDocumentLinkKind.SUPPORTS,
            "session-a",
            "candidate-a",
            "session-b",
            "candidate-b",
            "why",
        )
    object.__setattr__(node, "locator", original_locator)


def test_current_candidate_coverage_guards_and_success_snapshot():
    left, right = _pair()
    registry = ReaderCrossDocumentRegistry((left[3], right[3]))
    candidate = left[3].get_candidate("candidate-a")
    coverage = left[1]._coverage
    original_entry = coverage["p-a"]

    del coverage["p-a"]
    with pytest.raises(ValueError, match="coverage/provenance mismatch"):
        registry.register(
            "coverage-missing",
            CrossDocumentLinkKind.SUPPORTS,
            "session-a",
            "candidate-a",
            "session-b",
            "candidate-b",
            "why",
        )
    coverage["p-a"] = original_entry

    object.__setattr__(original_entry, "locator", None)
    with pytest.raises(ValueError, match="coverage/provenance mismatch"):
        registry.register(
            "coverage-no-locator",
            CrossDocumentLinkKind.SUPPORTS,
            "session-a",
            "candidate-a",
            "session-b",
            "candidate-b",
            "why",
        )
    object.__setattr__(original_entry, "locator", candidate.primary_locator)

    other_source = _source("doc-a", "coverage-other")
    object.__setattr__(original_entry, "locator", _loc(other_source, 10, 20))
    with pytest.raises(ValueError, match="coverage/provenance mismatch"):
        registry.register(
            "coverage-source",
            CrossDocumentLinkKind.SUPPORTS,
            "session-a",
            "candidate-a",
            "session-b",
            "candidate-b",
            "why",
        )
    object.__setattr__(original_entry, "locator", candidate.primary_locator)

    object.__setattr__(original_entry, "locator", _loc(left[0], 11, 19))
    with pytest.raises(ValueError, match="coverage/provenance mismatch"):
        registry.register(
            "coverage-replay",
            CrossDocumentLinkKind.SUPPORTS,
            "session-a",
            "candidate-a",
            "session-b",
            "candidate-b",
            "why",
        )
    object.__setattr__(original_entry, "locator", candidate.primary_locator)

    original_state = original_entry.state
    object.__setattr__(original_entry, "state", CoverageState.SEEN)
    with pytest.raises(ValueError, match="coverage is not substantive"):
        registry.register(
            "coverage-state",
            CrossDocumentLinkKind.SUPPORTS,
            "session-a",
            "candidate-a",
            "session-b",
            "candidate-b",
            "why",
        )
    object.__setattr__(original_entry, "state", original_state)

    link = registry.register(
        "valid",
        CrossDocumentLinkKind.POSSIBLE_SAME_CLAIM,
        "session-a",
        "candidate-a",
        "session-b",
        "candidate-b",
        "caller suspects overlap; identity remains unproven",
        inspection_basis=CrossDocumentInspectionBasis.LEXICAL_SIMILARITY_SIGNAL,
    )
    assert link.left.candidate_id == "candidate-a"
    assert link.right.candidate_id == "candidate-b"
    assert link.left.primary_locator.replay_key == candidate.primary_locator.replay_key


def test_rc7_import_surface_has_no_authority_or_automatic_semantic_dependencies():
    source = inspect.getsource(cross_document)
    tree = ast.parse(source)
    imported_modules = {
        node.module
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
    }
    assert imported_modules == {
        "__future__",
        "dataclasses",
        "enum",
        "typing",
        "core.reader_core",
        "core.reader_extraction",
        "core.reader_passes",
        "core.reader_structure",
    }

    for forbidden in (
        "core.evidence",
        "core.truth_gate",
        "core.guardian",
        "core.esm",
        "core.contradiction",
        "sentence_transformers",
        "pgvector",
        "anthropic",
        "openai",
    ):
        assert forbidden not in imported_modules

    public_fields = {
        field.name
        for cls in (CrossDocumentLinkSide, CrossDocumentLinkCandidate)
        for field in dataclasses.fields(cls)
    }
    assert not {
        "truth_status",
        "confidence",
        "evidence_sufficiency",
        "resolved",
        "winner",
        "identity",
        "similarity_score",
    } & public_fields

    assert "attach_evidence(" not in source
    assert "similarity != identity" not in source
