from __future__ import annotations

import ast
import dataclasses
import inspect

import pytest

import core.reader_extraction as reader_extraction
from core.reader_core import (
    CoverageEntry,
    CoverageState,
    ReaderSession,
    SegmentCard,
    SourceFidelity,
    SourceLocator,
    SourceVersion,
)
from core.reader_extraction import (
    PropositionKind,
    ReaderPropositionCandidate,
    ReaderPropositionExtractor,
)
from core.reader_passes import (
    MultiPassReader,
    ReaderPassKind,
    ReaderPassRecord,
    ReaderPassState,
    RegionPassOutcome,
)
from core.reader_structure import (
    DocumentStructuralMap,
    StructuralKind,
    StructuralNode,
    StructuralStatus,
)


def _source(
    text: str = "x" * 200,
    *,
    restricted: bool = False,
    sensitivity: str | None = None,
) -> SourceVersion:
    return SourceVersion.from_text(
        "doc-extract",
        "file:///doc-extract.txt",
        text,
        restricted=restricted,
        sensitivity=sensitivity,
    )


def _loc(source: SourceVersion, start: int, end: int) -> SourceLocator:
    return SourceLocator(source, span_start=start, span_end=end)


def _structure(source: SourceVersion | None = None) -> DocumentStructuralMap:
    source = source or _source()
    return DocumentStructuralMap(
        source,
        [
            StructuralNode("doc", StructuralKind.DOCUMENT, _loc(source, 0, 200), 0),
            StructuralNode("section-a", StructuralKind.SECTION, _loc(source, 0, 90), 1, "doc"),
            StructuralNode("p-a", StructuralKind.PARAGRAPH, _loc(source, 10, 20), 2, "section-a"),
            StructuralNode("section-b", StructuralKind.SECTION, _loc(source, 100, 190), 3, "doc"),
            StructuralNode("p-b", StructuralKind.PARAGRAPH, _loc(source, 110, 120), 4, "section-b"),
            StructuralNode(
                "amb",
                StructuralKind.TABLE_REGION,
                _loc(source, 130, 140),
                5,
                "section-b",
                status=StructuralStatus.AMBIGUOUS,
                reason="merged cells unresolved",
            ),
        ],
    )


def _reader(
    source: SourceVersion | None = None,
) -> tuple[SourceVersion, ReaderSession, DocumentStructuralMap, MultiPassReader]:
    source = source or _source()
    session = ReaderSession("session-extract", source, "extract source propositions")
    structure = _structure(source)
    return source, session, structure, MultiPassReader(session, structure)


def _complete_broad(
    reader: MultiPassReader,
    *,
    pass_id: str = "pass-broad",
    targets: tuple[str, ...] = ("p-a",),
) -> ReaderPassRecord:
    reader.begin_pass(pass_id, ReaderPassKind.BROAD_READ, targets)
    for target in targets:
        reader.record_region(pass_id, target, CoverageState.PROCESSED)
    return reader.complete_pass(pass_id)


def _card(
    source: SourceVersion,
    *,
    fidelity: SourceFidelity = SourceFidelity.EXTRACTED_PROPOSITION,
    supports: tuple[SourceLocator, ...] = (),
) -> SegmentCard:
    return SegmentCard(
        "card",
        _loc(source, 10, 20),
        fidelity,
        "the source presents a proposition",
        supports,
    )


def test_proposition_kinds_are_explicit_source_presentation_categories():
    assert {kind.value for kind in PropositionKind} == {
        "FACTUAL_ASSERTION",
        "AUTHOR_OPINION",
        "HYPOTHESIS",
        "CONDITIONAL",
        "EXAMPLE",
        "QUOTED_SPEECH",
        "REPORTED_POSITION",
        "DEFINITION",
        "UNCERTAIN_ASSERTION",
    }


def test_candidate_validation_properties_and_privacy_inheritance():
    source = _source(restricted=True, sensitivity="medical")
    support = _loc(source, 110, 120)
    candidate = ReaderPropositionCandidate(
        " candidate ",
        " session ",
        " pass ",
        _card(source, supports=(support,)),
        PropositionKind.CONDITIONAL,
        " author ",
        ("p-a", "p-b"),
        negated=True,
        qualifiers=(" only adults ", " after 2020 "),
    )
    assert candidate.candidate_id == "candidate"
    assert candidate.session_id == "session"
    assert candidate.pass_id == "pass"
    assert candidate.source_owner == "author"
    assert candidate.node_ids == ("p-a", "p-b")
    assert candidate.negated is True
    assert candidate.qualifiers == ("only adults", "after 2020")
    assert candidate.proposition == "the source presents a proposition"
    assert candidate.primary_locator.replay_key == _loc(source, 10, 20).replay_key
    assert candidate.restricted is True
    assert candidate.sensitivity == "medical"

    with pytest.raises(ValueError, match="candidate_id"):
        ReaderPropositionCandidate(" ", "s", "p", _card(source), PropositionKind.EXAMPLE, "a", ("p-a",))
    with pytest.raises(ValueError, match="session_id"):
        ReaderPropositionCandidate("c", " ", "p", _card(source), PropositionKind.EXAMPLE, "a", ("p-a",))
    with pytest.raises(ValueError, match="pass_id"):
        ReaderPropositionCandidate("c", "s", " ", _card(source), PropositionKind.EXAMPLE, "a", ("p-a",))
    with pytest.raises(ValueError, match="SegmentCard"):
        ReaderPropositionCandidate("c", "s", "p", object(), PropositionKind.EXAMPLE, "a", ("p-a",))  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="EXTRACTED_PROPOSITION"):
        ReaderPropositionCandidate(
            "c", "s", "p", _card(source, fidelity=SourceFidelity.SUMMARY), PropositionKind.EXAMPLE, "a", ("p-a",)
        )
    with pytest.raises(ValueError, match="PropositionKind"):
        ReaderPropositionCandidate("c", "s", "p", _card(source), "EXAMPLE", "a", ("p-a",))  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="source_owner"):
        ReaderPropositionCandidate("c", "s", "p", _card(source), PropositionKind.EXAMPLE, " ", ("p-a",))
    with pytest.raises(ValueError, match="iterable"):
        ReaderPropositionCandidate("c", "s", "p", _card(source), PropositionKind.EXAMPLE, "a", "p-a")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="at least one"):
        ReaderPropositionCandidate("c", "s", "p", _card(source), PropositionKind.EXAMPLE, "a", ())
    with pytest.raises(ValueError, match="unique"):
        ReaderPropositionCandidate("c", "s", "p", _card(source), PropositionKind.EXAMPLE, "a", ("p-a", "p-a"))
    with pytest.raises(ValueError, match="primary \\+ supporting"):
        ReaderPropositionCandidate(
            "c", "s", "p", _card(source, supports=(support,)), PropositionKind.EXAMPLE, "a", ("p-a",)
        )
    with pytest.raises(ValueError, match="negated"):
        ReaderPropositionCandidate("c", "s", "p", _card(source), PropositionKind.EXAMPLE, "a", ("p-a",), negated=1)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="iterable"):
        ReaderPropositionCandidate(
            "c", "s", "p", _card(source), PropositionKind.EXAMPLE, "a", ("p-a",), qualifiers="scope"  # type: ignore[arg-type]
        )
    with pytest.raises(ValueError, match="qualifiers"):
        ReaderPropositionCandidate(
            "c", "s", "p", _card(source), PropositionKind.EXAMPLE, "a", ("p-a",), qualifiers=(" ",)
        )
    with pytest.raises(ValueError, match="unique"):
        ReaderPropositionCandidate(
            "c", "s", "p", _card(source), PropositionKind.EXAMPLE, "a", ("p-a",), qualifiers=("x", "x")
        )
    with pytest.raises(ValueError, match="iterable"):
        ReaderPropositionCandidate(
            "c", "s", "p", _card(source), PropositionKind.EXAMPLE, "a", ("p-a",), qualifiers=None  # type: ignore[arg-type]
        )


def test_extractor_requires_reader_and_open_session():
    with pytest.raises(ValueError, match="MultiPassReader"):
        ReaderPropositionExtractor(object())  # type: ignore[arg-type]

    _, session, structure, _ = _reader()
    session.finish()
    closed_reader = object.__new__(MultiPassReader)
    closed_reader._session = session
    closed_reader._structure = structure
    closed_reader._records = []
    closed_reader._record_index = {}
    closed_reader._active_pass_id = None
    with pytest.raises(ValueError, match="OPEN"):
        ReaderPropositionExtractor(closed_reader)


def test_extracts_source_linked_candidate_only_after_substantive_completed_pass():
    source = _source(restricted=True, sensitivity="confidential")
    _, session, _, reader = _reader(source)
    record = _complete_broad(reader, targets=("p-a", "p-b"))
    extractor = ReaderPropositionExtractor(reader)

    candidate = extractor.extract(
        " cand-1 ",
        record.pass_id,
        " in some jurisdictions X does not apply ",
        PropositionKind.REPORTED_POSITION,
        " cited regulator ",
        " p-a ",
        supporting_node_ids=(" p-b ",),
        negated=True,
        qualifiers=("in some jurisdictions", "subject to exception Y"),
    )

    assert extractor.reader is reader
    assert extractor.candidates == (candidate,)
    assert extractor.get_candidate(" cand-1 ") is candidate
    assert candidate.card in session.segment_cards
    assert candidate.card.fidelity is SourceFidelity.EXTRACTED_PROPOSITION
    assert candidate.card.locator.replay_key == reader.structure.get("p-a").locator.replay_key
    assert tuple(loc.replay_key for loc in candidate.card.supporting_locators) == (
        reader.structure.get("p-b").locator.replay_key,
    )
    assert candidate.node_ids == ("p-a", "p-b")
    assert candidate.proposition == "in some jurisdictions X does not apply"
    assert candidate.source_owner == "cited regulator"
    assert candidate.negated is True
    assert candidate.qualifiers == ("in some jurisdictions", "subject to exception Y")
    assert candidate.restricted is True
    assert candidate.sensitivity == "confidential"

    telemetry = extractor.telemetry()
    assert telemetry.total_candidates == 1
    assert telemetry.negated_candidates == 1
    assert telemetry.qualified_candidates == 1
    assert telemetry.multi_span_candidates == 1
    assert telemetry.kind_counts[PropositionKind.REPORTED_POSITION] == 1
    assert sum(telemetry.kind_counts.values()) == 1

    with pytest.raises(ValueError, match="candidate_id"):
        extractor.get_candidate(" ")
    with pytest.raises(KeyError, match="missing"):
        extractor.get_candidate("missing")


def test_each_source_presentation_kind_survives_extraction_without_truth_fields():
    _, _, _, reader = _reader()
    record = _complete_broad(reader)
    extractor = ReaderPropositionExtractor(reader)

    for index, kind in enumerate(PropositionKind):
        candidate = extractor.extract(
            f"kind-{index}",
            record.pass_id,
            f"statement {kind.value}",
            kind,
            "document author",
            "p-a",
        )
        assert candidate.kind is kind
        assert candidate.card.fidelity is SourceFidelity.EXTRACTED_PROPOSITION

    fields = {field.name for field in dataclasses.fields(ReaderPropositionCandidate)}
    assert "truth_status" not in fields
    assert "confidence" not in fields
    assert "evidence_sufficiency" not in fields
    assert "significance" not in fields

    telemetry = extractor.telemetry()
    assert telemetry.total_candidates == len(PropositionKind)
    assert telemetry.negated_candidates == 0
    assert telemetry.qualified_candidates == 0
    assert telemetry.multi_span_candidates == 0
    assert all(telemetry.kind_counts[kind] == 1 for kind in PropositionKind)


def test_extraction_rejects_duplicate_ids_card_collision_bad_kind_and_bad_negated():
    source, session, _, reader = _reader()
    record = _complete_broad(reader)
    extractor = ReaderPropositionExtractor(reader)
    extractor.extract("dup", record.pass_id, "x", PropositionKind.FACTUAL_ASSERTION, "author", "p-a")

    with pytest.raises(ValueError, match="duplicate"):
        extractor.extract("dup", record.pass_id, "x", PropositionKind.FACTUAL_ASSERTION, "author", "p-a")

    existing = SegmentCard(
        "collision",
        _loc(source, 10, 20),
        SourceFidelity.DIRECT_SOURCE_OBSERVATION,
        "source text exists",
    )
    session.add_segment_card(existing)
    with pytest.raises(ValueError, match="SegmentCard id"):
        extractor.extract(
            "collision", record.pass_id, "x", PropositionKind.FACTUAL_ASSERTION, "author", "p-a"
        )

    with pytest.raises(ValueError, match="PropositionKind"):
        extractor.extract("bad-kind", record.pass_id, "x", "FACTUAL_ASSERTION", "author", "p-a")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="negated"):
        extractor.extract(
            "bad-negated", record.pass_id, "x", PropositionKind.FACTUAL_ASSERTION, "author", "p-a", negated=1  # type: ignore[arg-type]
        )


def test_extraction_rejects_incomplete_pass_orientation_seen_and_wrong_target():
    _, _, _, reader = _reader()
    extractor = ReaderPropositionExtractor(reader)
    reader.begin_pass("active", ReaderPassKind.BROAD_READ, ("p-a",))
    with pytest.raises(ValueError, match="COMPLETED"):
        extractor.extract(
            "c-active", "active", "x", PropositionKind.FACTUAL_ASSERTION, "author", "p-a"
        )
    reader.interrupt_pass("active", "operator stop")

    reader.begin_pass("orient", ReaderPassKind.ORIENTATION, ("p-a",))
    reader.record_region("orient", "p-a", CoverageState.SEEN)
    reader.complete_pass("orient")
    with pytest.raises(ValueError, match="PROCESSED or REVISITED"):
        extractor.extract(
            "c-seen", "orient", "x", PropositionKind.FACTUAL_ASSERTION, "author", "p-a"
        )

    _, _, _, reader2 = _reader()
    record = _complete_broad(reader2)
    extractor2 = ReaderPropositionExtractor(reader2)
    with pytest.raises(ValueError, match="declared target"):
        extractor2.extract(
            "c-target", record.pass_id, "x", PropositionKind.FACTUAL_ASSERTION, "author", "p-b"
        )


def test_extraction_rejects_bad_support_iterables_duplicates_and_empty_proposition():
    _, _, _, reader = _reader()
    record = _complete_broad(reader, targets=("p-a", "p-b"))
    extractor = ReaderPropositionExtractor(reader)

    with pytest.raises(ValueError, match="iterable"):
        extractor.extract(
            "c-str",
            record.pass_id,
            "x",
            PropositionKind.FACTUAL_ASSERTION,
            "author",
            "p-a",
            supporting_node_ids="p-b",  # type: ignore[arg-type]
        )
    with pytest.raises(ValueError, match="iterable"):
        extractor.extract(
            "c-none",
            record.pass_id,
            "x",
            PropositionKind.FACTUAL_ASSERTION,
            "author",
            "p-a",
            supporting_node_ids=None,  # type: ignore[arg-type]
        )
    with pytest.raises(ValueError, match="unique"):
        extractor.extract(
            "c-dup-support",
            record.pass_id,
            "x",
            PropositionKind.FACTUAL_ASSERTION,
            "author",
            "p-a",
            supporting_node_ids=("p-b", "p-b"),
        )
    with pytest.raises(ValueError, match="primary/supporting"):
        extractor.extract(
            "c-primary-dup",
            record.pass_id,
            "x",
            PropositionKind.FACTUAL_ASSERTION,
            "author",
            "p-a",
            supporting_node_ids=("p-a",),
        )
    with pytest.raises(ValueError, match="proposition"):
        extractor.extract(
            "c-empty",
            record.pass_id,
            " ",
            PropositionKind.FACTUAL_ASSERTION,
            "author",
            "p-a",
        )


def test_extraction_rejects_current_needs_review_and_provenance_mismatch():
    _, session, _, reader = _reader()
    record = _complete_broad(reader)
    extractor = ReaderPropositionExtractor(reader)

    session.transition_coverage("p-a", CoverageState.NEEDS_REVIEW, reason="new ambiguity")
    with pytest.raises(ValueError, match="current coverage is not substantive"):
        extractor.extract(
            "c-review", record.pass_id, "x", PropositionKind.FACTUAL_ASSERTION, "author", "p-a"
        )

    _, session2, structure2, reader2 = _reader(_source("y" * 200))
    record2 = _complete_broad(reader2)
    extractor2 = ReaderPropositionExtractor(reader2)
    session2.set_coverage(
        CoverageEntry(
            "p-a",
            CoverageState.PROCESSED,
            locator=structure2.get("p-b").locator,
        )
    )
    with pytest.raises(ValueError, match="coverage/provenance"):
        extractor2.extract(
            "c-provenance", record2.pass_id, "x", PropositionKind.FACTUAL_ASSERTION, "author", "p-a"
        )


def test_extraction_rejects_unresolved_structure_even_if_corrupt_upstream_state_claims_processed():
    _, session, _, reader = _reader()
    session.set_coverage(
        CoverageEntry(
            "amb",
            CoverageState.PROCESSED,
            locator=reader.structure.get("amb").locator,
        )
    )
    corrupt = ReaderPassRecord(
        "corrupt",
        session.session_id,
        session.source,
        ReaderPassKind.BROAD_READ,
        ("amb",),
        ReaderPassState.COMPLETED,
        outcomes=(
            RegionPassOutcome("amb", CoverageState.UNREAD, CoverageState.PROCESSED),
        ),
    )
    reader._records.append(corrupt)
    reader._record_index["corrupt"] = len(reader._records) - 1
    extractor = ReaderPropositionExtractor(reader)

    with pytest.raises(ValueError, match="unresolved structural"):
        extractor.extract(
            "c-amb", "corrupt", "x", PropositionKind.FACTUAL_ASSERTION, "author", "amb"
        )


def test_extraction_rejects_corrupt_pass_session_and_source_bindings():
    source, session, _, reader = _reader()
    record = _complete_broad(reader)
    index = reader._record_index[record.pass_id]
    extractor = ReaderPropositionExtractor(reader)

    wrong_session = ReaderPassRecord(
        record.pass_id,
        "other-session",
        source,
        record.kind,
        record.target_node_ids,
        record.state,
        outcomes=record.outcomes,
    )
    reader._records[index] = wrong_session
    with pytest.raises(ValueError, match="different session"):
        extractor.extract(
            "c-session", record.pass_id, "x", PropositionKind.FACTUAL_ASSERTION, "author", "p-a"
        )

    other_source = _source("different")
    wrong_source = ReaderPassRecord(
        record.pass_id,
        session.session_id,
        other_source,
        record.kind,
        record.target_node_ids,
        record.state,
        outcomes=record.outcomes,
    )
    reader._records[index] = wrong_source
    with pytest.raises(ValueError, match="different source version"):
        extractor.extract(
            "c-source", record.pass_id, "x", PropositionKind.FACTUAL_ASSERTION, "author", "p-a"
        )


def test_extraction_stops_when_session_closes_after_extractor_creation():
    _, session, _, reader = _reader()
    _complete_broad(reader)
    extractor = ReaderPropositionExtractor(reader)
    session.finish()
    with pytest.raises(ValueError, match="no longer OPEN"):
        extractor.extract(
            "closed", "pass-broad", "x", PropositionKind.FACTUAL_ASSERTION, "author", "p-a"
        )


def test_rc4_import_and_authority_firewall():
    source = inspect.getsource(reader_extraction)
    tree = ast.parse(source)
    imported_core_modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("core."):
            imported_core_modules.add(node.module)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith("core."):
                    imported_core_modules.add(alias.name)

    assert imported_core_modules == {
        "core.reader_core",
        "core.reader_passes",
        "core.reader_structure",
    }
    assert "core.evidence" not in imported_core_modules
    assert "core.pipeline" not in imported_core_modules
    assert "core.memory" not in imported_core_modules

    methods = set(vars(ReaderPropositionExtractor))
    assert "attach_evidence" not in methods
    assert "write_canon" not in methods
    assert "set_truth_status" not in methods
