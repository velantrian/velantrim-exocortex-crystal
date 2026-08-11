from __future__ import annotations

import ast
import dataclasses
import inspect

import pytest

import core.reader_relations as reader_relations
from core.reader_core import CoverageState, ReaderSession, SourceLocator, SourceVersion
from core.reader_extraction import PropositionKind, ReaderPropositionExtractor
from core.reader_passes import MultiPassReader, ReaderPassKind
from core.reader_relations import (
    ReaderRelationCandidate,
    ReaderRelationKind,
    ReaderRelationRegistry,
    ReaderRelationSide,
)
from core.reader_structure import (
    DocumentStructuralMap,
    StructuralKind,
    StructuralNode,
)


def _source(text: str = "x" * 200) -> SourceVersion:
    return SourceVersion.from_text("doc-rel", "file:///doc-rel.txt", text)


def _loc(source: SourceVersion, start: int, end: int) -> SourceLocator:
    return SourceLocator(source, span_start=start, span_end=end)


def _extractor() -> tuple[SourceVersion, ReaderSession, ReaderPropositionExtractor]:
    source = _source()
    session = ReaderSession("session-rel", source, "compare source propositions")
    structure = DocumentStructuralMap(
        source,
        [
            StructuralNode("doc", StructuralKind.DOCUMENT, _loc(source, 0, 200), 0),
            StructuralNode("p-a", StructuralKind.PARAGRAPH, _loc(source, 10, 20), 1, "doc"),
            StructuralNode("p-b", StructuralKind.PARAGRAPH, _loc(source, 30, 40), 2, "doc"),
            StructuralNode("p-c", StructuralKind.PARAGRAPH, _loc(source, 50, 60), 3, "doc"),
        ],
    )
    reader = MultiPassReader(session, structure)
    reader.begin_pass(
        "cross-check",
        ReaderPassKind.BROAD_READ,
        ("p-a", "p-b", "p-c"),
    )
    for node_id in ("p-a", "p-b", "p-c"):
        reader.record_region("cross-check", node_id, CoverageState.PROCESSED)
    reader.complete_pass("cross-check")
    extractor = ReaderPropositionExtractor(reader)
    extractor.extract(
        "candidate-a",
        "cross-check",
        "X applies",
        PropositionKind.FACTUAL_ASSERTION,
        "author",
        "p-a",
    )
    extractor.extract(
        "candidate-b",
        "cross-check",
        "X does not apply",
        PropositionKind.FACTUAL_ASSERTION,
        "author",
        "p-b",
        negated=True,
        qualifiers=("except Y",),
    )
    extractor.extract(
        "candidate-c",
        "cross-check",
        "X applies only after 2020",
        PropositionKind.CONDITIONAL,
        "author",
        "p-c",
    )
    return source, session, extractor


def _side(source: SourceVersion, candidate_id: str = "candidate") -> ReaderRelationSide:
    return ReaderRelationSide(
        candidate_id,
        "pass",
        ("p-a",),
        _loc(source, 10, 20),
        (),
    )


def test_relation_kinds_are_minimal_and_explicit():
    assert {kind.value for kind in ReaderRelationKind} == {
        "POSSIBLE_CONTRADICTION",
        "EXCEPTION",
        "QUALIFICATION",
        "TENSION",
    }


def test_relation_side_validation_and_candidate_snapshot():
    source, _, extractor = _extractor()
    candidate = extractor.get_candidate("candidate-b")
    side = ReaderRelationSide.from_candidate(candidate)

    assert side.candidate_id == "candidate-b"
    assert side.pass_id == "cross-check"
    assert side.node_ids == ("p-b",)
    assert side.primary_locator.replay_key == candidate.primary_locator.replay_key
    assert side.supporting_locators == ()
    assert side.source.same_version(source)

    with pytest.raises(ValueError, match="ReaderPropositionCandidate"):
        ReaderRelationSide.from_candidate(object())  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="candidate_id"):
        ReaderRelationSide(" ", "pass", ("p-a",), _loc(source, 0, 1), ())
    with pytest.raises(ValueError, match="pass_id"):
        ReaderRelationSide("candidate", " ", ("p-a",), _loc(source, 0, 1), ())
    with pytest.raises(ValueError, match="non-empty strings"):
        ReaderRelationSide("candidate", "pass", (), _loc(source, 0, 1), ())
    with pytest.raises(ValueError, match="non-empty strings"):
        ReaderRelationSide("candidate", "pass", (" ",), _loc(source, 0, 1), ())
    with pytest.raises(ValueError, match="unique"):
        ReaderRelationSide(
            "candidate",
            "pass",
            ("p-a", "p-a"),
            _loc(source, 0, 1),
            (_loc(source, 1, 2),),
        )
    with pytest.raises(ValueError, match="primary_locator"):
        ReaderRelationSide("candidate", "pass", ("p-a",), object(), ())  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="SourceLocator"):
        ReaderRelationSide(
            "candidate",
            "pass",
            ("p-a", "p-b"),
            _loc(source, 0, 1),
            (object(),),  # type: ignore[arg-type]
        )
    with pytest.raises(ValueError, match=r"primary \+ supporting"):
        ReaderRelationSide("candidate", "pass", ("p-a", "p-b"), _loc(source, 0, 1), ())
    other = _source("changed")
    with pytest.raises(ValueError, match="one source version"):
        ReaderRelationSide(
            "candidate",
            "pass",
            ("p-a", "p-b"),
            _loc(source, 0, 1),
            (_loc(other, 1, 2),),
        )


def test_relation_candidate_validation_properties_and_no_authority_fields():
    source = _source()
    left = _side(source, "left")
    right = ReaderRelationSide("right", "pass", ("p-b",), _loc(source, 30, 40), ())
    relation = ReaderRelationCandidate(
        " rel ",
        " session ",
        ReaderRelationKind.EXCEPTION,
        left,
        right,
        " right is an explicit exception to left ",
    )

    assert relation.relation_id == "rel"
    assert relation.session_id == "session"
    assert relation.kind is ReaderRelationKind.EXCEPTION
    assert relation.rationale == "right is an explicit exception to left"
    assert relation.source.same_version(source)
    assert relation.restricted is False
    assert relation.sensitivity is None

    fields = {field.name for field in dataclasses.fields(ReaderRelationCandidate)}
    assert "truth_status" not in fields
    assert "confidence" not in fields
    assert "evidence_sufficiency" not in fields
    assert "resolved" not in fields
    assert "winner" not in fields

    with pytest.raises(ValueError, match="relation_id"):
        ReaderRelationCandidate(" ", "s", ReaderRelationKind.TENSION, left, right, "why")
    with pytest.raises(ValueError, match="session_id"):
        ReaderRelationCandidate("r", " ", ReaderRelationKind.TENSION, left, right, "why")
    with pytest.raises(ValueError, match="ReaderRelationKind"):
        ReaderRelationCandidate("r", "s", "TENSION", left, right, "why")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="left"):
        ReaderRelationCandidate("r", "s", ReaderRelationKind.TENSION, object(), right, "why")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="right"):
        ReaderRelationCandidate("r", "s", ReaderRelationKind.TENSION, left, object(), "why")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="distinct"):
        ReaderRelationCandidate("r", "s", ReaderRelationKind.TENSION, left, left, "why")
    other = _source("changed")
    other_right = _side(other, "right")
    with pytest.raises(ValueError, match="same source version"):
        ReaderRelationCandidate("r", "s", ReaderRelationKind.TENSION, left, other_right, "why")
    with pytest.raises(ValueError, match="rationale"):
        ReaderRelationCandidate("r", "s", ReaderRelationKind.TENSION, left, right, " ")


def test_registry_registers_all_kinds_with_deterministic_symmetric_order():
    _, session, extractor = _extractor()
    registry = ReaderRelationRegistry(extractor)

    contradiction = registry.register(
        "rel-contradiction",
        ReaderRelationKind.POSSIBLE_CONTRADICTION,
        "candidate-b",
        "candidate-a",
        "explicit positive versus explicit negation",
    )
    exception = registry.register(
        "rel-exception",
        ReaderRelationKind.EXCEPTION,
        "candidate-a",
        "candidate-b",
        "right side carries an explicit exception qualifier",
    )
    qualification = registry.register(
        "rel-qualification",
        ReaderRelationKind.QUALIFICATION,
        "candidate-a",
        "candidate-c",
        "right side narrows the temporal scope",
    )
    tension = registry.register(
        "rel-tension",
        ReaderRelationKind.TENSION,
        "candidate-c",
        "candidate-b",
        "different scoped presentations may be in tension",
    )

    assert registry.extractor is extractor
    assert registry.relations == (contradiction, exception, qualification, tension)
    assert registry.get_relation(" rel-contradiction ") is contradiction
    assert contradiction.session_id == session.session_id
    assert contradiction.left.candidate_id == "candidate-a"
    assert contradiction.right.candidate_id == "candidate-b"
    assert exception.left.candidate_id == "candidate-a"
    assert exception.right.candidate_id == "candidate-b"
    assert qualification.kind is ReaderRelationKind.QUALIFICATION
    assert tension.left.candidate_id == "candidate-b"
    assert tension.right.candidate_id == "candidate-c"

    telemetry = registry.telemetry()
    assert telemetry.total_candidates == 4
    assert all(telemetry.kind_counts[kind] == 1 for kind in ReaderRelationKind)


def test_registry_rejects_invalid_input_duplicates_and_unknown_candidates():
    _, _, extractor = _extractor()
    registry = ReaderRelationRegistry(extractor)

    with pytest.raises(ValueError, match="relation_id"):
        registry.register(" ", ReaderRelationKind.TENSION, "candidate-a", "candidate-b", "why")
    with pytest.raises(ValueError, match="ReaderRelationKind"):
        registry.register("r", "TENSION", "candidate-a", "candidate-b", "why")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="left_candidate_id"):
        registry.register("r", ReaderRelationKind.TENSION, " ", "candidate-b", "why")
    with pytest.raises(ValueError, match="right_candidate_id"):
        registry.register("r", ReaderRelationKind.TENSION, "candidate-a", " ", "why")
    with pytest.raises(ValueError, match="distinct"):
        registry.register("r", ReaderRelationKind.TENSION, "candidate-a", "candidate-a", "why")
    with pytest.raises(ValueError, match="rationale"):
        registry.register("r", ReaderRelationKind.TENSION, "candidate-a", "candidate-b", " ")
    with pytest.raises(KeyError, match="missing"):
        registry.register("r", ReaderRelationKind.TENSION, "candidate-a", "missing", "why")

    registry.register("dup-id", ReaderRelationKind.TENSION, "candidate-a", "candidate-b", "why")
    with pytest.raises(ValueError, match="relation_id"):
        registry.register(
            "dup-id",
            ReaderRelationKind.EXCEPTION,
            "candidate-a",
            "candidate-b",
            "another relation",
        )
    with pytest.raises(ValueError, match="relation candidate"):
        registry.register(
            "dup-semantic",
            ReaderRelationKind.TENSION,
            "candidate-b",
            "candidate-a",
            "same symmetric pair",
        )

    registry.register(
        "direction-a",
        ReaderRelationKind.EXCEPTION,
        "candidate-a",
        "candidate-c",
        "C is an exception to A",
    )
    reverse = registry.register(
        "direction-b",
        ReaderRelationKind.EXCEPTION,
        "candidate-c",
        "candidate-a",
        "A is separately asserted as an exception to C",
    )
    assert reverse.left.candidate_id == "candidate-c"

    with pytest.raises(ValueError, match="relation_id"):
        registry.get_relation(" ")
    with pytest.raises(KeyError, match="unknown"):
        registry.get_relation("unknown")


def test_registry_requires_registered_current_same_session_same_version_candidate():
    _, session, extractor = _extractor()
    registry = ReaderRelationRegistry(extractor)

    candidate = extractor.get_candidate("candidate-a")
    original_session_id = candidate.session_id
    object.__setattr__(candidate, "session_id", "other-session")
    with pytest.raises(ValueError, match="different Reader session"):
        registry.register("bad-session", ReaderRelationKind.TENSION, "candidate-a", "candidate-b", "why")
    object.__setattr__(candidate, "session_id", original_session_id)

    original_card = candidate.card
    other_source = _source("changed")
    object.__setattr__(
        candidate,
        "card",
        dataclasses.replace(
            original_card,
            locator=_loc(other_source, 10, 20),
        ),
    )
    with pytest.raises(ValueError, match="different source version"):
        registry.register("bad-source", ReaderRelationKind.TENSION, "candidate-a", "candidate-b", "why")
    object.__setattr__(candidate, "card", original_card)

    support_source = _source("support changed")
    object.__setattr__(
        original_card,
        "supporting_locators",
        (_loc(support_source, 1, 2),),
    )
    with pytest.raises(ValueError, match="support belongs"):
        registry.register("bad-support", ReaderRelationKind.TENSION, "candidate-a", "candidate-b", "why")
    object.__setattr__(original_card, "supporting_locators", ())

    session._segment_cards.remove(original_card)
    with pytest.raises(ValueError, match="not registered"):
        registry.register("missing-card", ReaderRelationKind.TENSION, "candidate-a", "candidate-b", "why")
    session._segment_cards.append(original_card)


def test_registry_fails_closed_when_session_finishes_or_becomes_stale():
    with pytest.raises(ValueError, match="ReaderPropositionExtractor"):
        ReaderRelationRegistry(object())  # type: ignore[arg-type]

    _, session, extractor = _extractor()
    session.finish()
    with pytest.raises(ValueError, match="OPEN"):
        ReaderRelationRegistry(extractor)

    source2, session2, extractor2 = _extractor()
    registry = ReaderRelationRegistry(extractor2)
    changed = SourceVersion.from_text(
        source2.document_id,
        source2.source_uri,
        "different source body",
    )
    report = session2.invalidate_for(changed)
    assert report.stale is True
    with pytest.raises(ValueError, match="no longer OPEN"):
        registry.register(
            "stale",
            ReaderRelationKind.POSSIBLE_CONTRADICTION,
            "candidate-a",
            "candidate-b",
            "old source cannot be current",
        )


def test_rc5_import_and_surface_have_no_authority_or_semantic_inference_dependencies():
    source = inspect.getsource(reader_relations)
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
    }
    assert "core.evidence" not in imported_modules
    assert "core.contradiction" not in imported_modules
    assert "core.contradiction_report" not in imported_modules
    assert "core.truth_gate" not in imported_modules
    assert "core.guardian" not in imported_modules
    assert "core.esm" not in imported_modules

    public_fields = {
        field.name
        for cls in (ReaderRelationSide, ReaderRelationCandidate)
        for field in dataclasses.fields(cls)
    }
    assert {
        "truth_status",
        "confidence",
        "evidence_sufficiency",
        "corroboration",
        "winner",
    }.isdisjoint(public_fields)
