from __future__ import annotations

import ast
import dataclasses
import inspect

import pytest

import core.reader_passes as reader_passes
from core.reader_core import (
    CoverageEntry,
    CoverageState,
    ReaderSession,
    SourceLocator,
    SourceVersion,
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
        "doc-pass",
        "file:///doc-pass.txt",
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
    session = ReaderSession("session-1", source, "understand source")
    structure = _structure(source)
    return source, session, structure, MultiPassReader(session, structure)


def test_pass_enums_and_outcome_validation():
    assert {kind.value for kind in ReaderPassKind} == {
        "ORIENTATION",
        "BROAD_READ",
        "FOCUSED_READ",
        "CROSS_CHECK",
        "TARGETED_REREAD",
    }
    assert {state.value for state in ReaderPassState} == {
        "ATTEMPTED",
        "COMPLETED",
        "INTERRUPTED",
        "DEGRADED",
    }

    outcome = RegionPassOutcome(
        " p-a ",
        CoverageState.UNREAD,
        CoverageState.SEEN,
        " orientation ",
    )
    assert outcome.node_id == "p-a"
    assert outcome.reason == "orientation"

    with pytest.raises(ValueError, match="node_id"):
        RegionPassOutcome(" ", CoverageState.UNREAD, CoverageState.SEEN)
    with pytest.raises(ValueError, match="before"):
        RegionPassOutcome("p", "UNREAD", CoverageState.SEEN)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="after"):
        RegionPassOutcome("p", CoverageState.UNREAD, "SEEN")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="reason"):
        RegionPassOutcome("p", CoverageState.UNREAD, CoverageState.SEEN, " ")


def test_pass_record_is_source_linked_private_and_fail_closed():
    source = _source(restricted=True, sensitivity="private")
    outcome = RegionPassOutcome("p-a", CoverageState.UNREAD, CoverageState.SEEN)
    record = ReaderPassRecord(
        " pass ",
        " session ",
        source,
        ReaderPassKind.ORIENTATION,
        ["p-a"],  # type: ignore[arg-type]
        ReaderPassState.COMPLETED,
        rationale=" orient ",
        outcomes=[outcome],  # type: ignore[arg-type]
    )
    assert record.pass_id == "pass"
    assert record.session_id == "session"
    assert record.target_node_ids == ("p-a",)
    assert record.rationale == "orient"
    assert record.restricted is True
    assert record.sensitivity == "private"

    with pytest.raises(ValueError, match="pass_id"):
        ReaderPassRecord(" ", "s", source, ReaderPassKind.ORIENTATION, ("p",), ReaderPassState.ATTEMPTED)
    with pytest.raises(ValueError, match="session_id"):
        ReaderPassRecord("p", " ", source, ReaderPassKind.ORIENTATION, ("p",), ReaderPassState.ATTEMPTED)
    with pytest.raises(ValueError, match="source"):
        ReaderPassRecord("p", "s", object(), ReaderPassKind.ORIENTATION, ("p",), ReaderPassState.ATTEMPTED)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="kind"):
        ReaderPassRecord("p", "s", source, "ORIENTATION", ("p",), ReaderPassState.ATTEMPTED)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="target_node_id"):
        ReaderPassRecord("p", "s", source, ReaderPassKind.ORIENTATION, (" ",), ReaderPassState.ATTEMPTED)
    with pytest.raises(ValueError, match="at least one"):
        ReaderPassRecord("p", "s", source, ReaderPassKind.ORIENTATION, (), ReaderPassState.ATTEMPTED)
    with pytest.raises(ValueError, match="unique"):
        ReaderPassRecord("p", "s", source, ReaderPassKind.ORIENTATION, ("a", "a"), ReaderPassState.ATTEMPTED)
    with pytest.raises(ValueError, match="state"):
        ReaderPassRecord("p", "s", source, ReaderPassKind.ORIENTATION, ("p",), "ATTEMPTED")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="rationale"):
        ReaderPassRecord(
            "p", "s", source, ReaderPassKind.ORIENTATION, ("p",), ReaderPassState.ATTEMPTED, rationale=" "
        )
    with pytest.raises(ValueError, match="RegionPassOutcome"):
        ReaderPassRecord(
            "p",
            "s",
            source,
            ReaderPassKind.ORIENTATION,
            ("p",),
            ReaderPassState.ATTEMPTED,
            outcomes=(object(),),  # type: ignore[arg-type]
        )
    with pytest.raises(ValueError, match="declared target"):
        ReaderPassRecord(
            "p",
            "s",
            source,
            ReaderPassKind.ORIENTATION,
            ("p",),
            ReaderPassState.ATTEMPTED,
            outcomes=(RegionPassOutcome("x", CoverageState.UNREAD, CoverageState.SEEN),),
        )
    duplicate = RegionPassOutcome("p", CoverageState.UNREAD, CoverageState.SEEN)
    with pytest.raises(ValueError, match="multiple outcomes"):
        ReaderPassRecord(
            "p",
            "s",
            source,
            ReaderPassKind.ORIENTATION,
            ("p",),
            ReaderPassState.ATTEMPTED,
            outcomes=(duplicate, duplicate),
        )
    with pytest.raises(ValueError, match="reason"):
        ReaderPassRecord(
            "p",
            "s",
            source,
            ReaderPassKind.ORIENTATION,
            ("p",),
            ReaderPassState.INTERRUPTED,
            reason=" ",
        )
    with pytest.raises(ValueError, match="requires an explicit reason"):
        ReaderPassRecord(
            "p", "s", source, ReaderPassKind.ORIENTATION, ("p",), ReaderPassState.INTERRUPTED
        )
    with pytest.raises(ValueError, match="terminal reason"):
        ReaderPassRecord(
            "p",
            "s",
            source,
            ReaderPassKind.ORIENTATION,
            ("p",),
            ReaderPassState.ATTEMPTED,
            reason="should not exist",
        )
    with pytest.raises(ValueError, match="outcome for every"):
        ReaderPassRecord(
            "p", "s", source, ReaderPassKind.ORIENTATION, ("p",), ReaderPassState.COMPLETED
        )


def test_controller_constructor_and_views_are_version_bound():
    source, session, structure, reader = _reader()

    assert reader.session is session
    assert reader.structure is structure
    assert reader.records == ()
    assert reader.active_pass_id is None
    assert not hasattr(reader, "__dict__")

    with pytest.raises(ValueError, match="ReaderSession"):
        MultiPassReader(object(), structure)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="DocumentStructuralMap"):
        MultiPassReader(session, object())  # type: ignore[arg-type]

    closed = ReaderSession("closed", source, "objective")
    closed.finish()
    with pytest.raises(ValueError, match="OPEN"):
        MultiPassReader(closed, structure)

    changed = _source("changed")
    with pytest.raises(ValueError, match="same source version"):
        MultiPassReader(ReaderSession("other", changed, "objective"), structure)


def test_begin_pass_validates_targets_without_partial_mutation():
    _, session, structure, reader = _reader()
    assert session.coverage == {}

    with pytest.raises(ValueError, match="pass_id"):
        reader.begin_pass(" ", ReaderPassKind.ORIENTATION, ["p-a"])
    with pytest.raises(ValueError, match="ReaderPassKind"):
        reader.begin_pass("p", "ORIENTATION", ["p-a"])  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="iterable"):
        reader.begin_pass("p", ReaderPassKind.ORIENTATION, "p-a")
    with pytest.raises(ValueError, match="iterable"):
        reader.begin_pass("p", ReaderPassKind.ORIENTATION, 1)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="at least one"):
        reader.begin_pass("p", ReaderPassKind.ORIENTATION, [])
    with pytest.raises(ValueError, match="target_node_id"):
        reader.begin_pass("p", ReaderPassKind.ORIENTATION, [" "])
    with pytest.raises(ValueError, match="unique"):
        reader.begin_pass("p", ReaderPassKind.ORIENTATION, ["p-a", "p-a"])
    with pytest.raises(ValueError, match="at least two"):
        reader.begin_pass("p", ReaderPassKind.CROSS_CHECK, ["p-a"])
    with pytest.raises(ValueError, match="explicit rationale"):
        reader.begin_pass("p", ReaderPassKind.TARGETED_REREAD, ["p-a"])
    with pytest.raises(ValueError, match="rationale"):
        reader.begin_pass("p", ReaderPassKind.TARGETED_REREAD, ["p-a"], rationale=" ")
    with pytest.raises(KeyError):
        reader.begin_pass("p", ReaderPassKind.ORIENTATION, ["missing"])
    assert session.coverage == {}

    wrong_locator = SourceLocator(session.source, span_start=11, span_end=19)
    session.set_coverage(CoverageEntry("p-a", CoverageState.UNREAD, wrong_locator))
    with pytest.raises(ValueError, match="does not match"):
        reader.begin_pass("p", ReaderPassKind.ORIENTATION, ["p-a", "p-b"])
    assert "p-b" not in session.coverage

    session.set_coverage(CoverageEntry("missing-locator", CoverageState.NEEDS_REVIEW, reason="legacy gap"))
    with pytest.raises(KeyError):
        structure.get("missing-locator")


def test_orientation_records_explicit_gaps_and_requires_all_targets_before_completion():
    _, session, _, reader = _reader()
    record = reader.begin_pass(
        "orientation",
        ReaderPassKind.ORIENTATION,
        ["p-a", "amb"],
        rationale="map source",
    )
    assert record.state is ReaderPassState.ATTEMPTED
    assert record.source is session.source
    assert session.coverage["p-a"].state is CoverageState.UNREAD

    with pytest.raises(ValueError, match="unrecorded"):
        reader.complete_pass("orientation")
    with pytest.raises(ValueError, match="declared target"):
        reader.record_region("orientation", "p-b", CoverageState.SEEN)
    with pytest.raises(ValueError, match="CoverageState"):
        reader.record_region("orientation", "p-a", "SEEN")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="ORIENTATION"):
        reader.record_region("orientation", "p-a", CoverageState.PROCESSED)

    first = reader.record_region("orientation", "p-a", CoverageState.SEEN)
    assert first.before is CoverageState.UNREAD
    assert first.after is CoverageState.SEEN
    with pytest.raises(ValueError, match="already has an outcome"):
        reader.record_region("orientation", "p-a", CoverageState.SEEN)

    with pytest.raises(ValueError, match="unresolved structural"):
        reader.record_region("orientation", "amb", CoverageState.SEEN)
    with pytest.raises(ValueError, match="reason"):
        reader.record_region("orientation", "amb", CoverageState.NEEDS_REVIEW)
    gap = reader.record_region(
        "orientation",
        "amb",
        CoverageState.NEEDS_REVIEW,
        reason="ambiguous table boundary",
    )
    assert gap.after is CoverageState.NEEDS_REVIEW
    assert gap.reason == "ambiguous table boundary"

    completed = reader.complete_pass("orientation")
    assert completed.state is ReaderPassState.COMPLETED
    assert reader.active_pass_id is None
    assert reader.get_pass(" orientation ") is completed
    with pytest.raises(KeyError):
        reader.get_pass("missing")
    with pytest.raises(ValueError, match="pass_id"):
        reader.get_pass(" ")


def test_broad_and_focused_passes_preserve_coverage_ordering():
    _, session, _, reader = _reader()

    reader.begin_pass("broad", ReaderPassKind.BROAD_READ, ["p-a"])
    with pytest.raises(ValueError, match="BROAD_READ"):
        reader.record_region("broad", "p-a", CoverageState.SEEN)
    reader.record_region("broad", "p-a", CoverageState.PROCESSED, reason="substantive read")
    reader.complete_pass("broad")
    assert session.coverage["p-a"].state is CoverageState.PROCESSED

    reader.begin_pass("focus-existing", ReaderPassKind.FOCUSED_READ, ["p-a"])
    with pytest.raises(ValueError, match="FOCUSED_READ"):
        reader.record_region("focus-existing", "p-a", CoverageState.PROCESSED)
    reader.record_region("focus-existing", "p-a", CoverageState.REVISITED)
    reader.complete_pass("focus-existing")

    reader.begin_pass("focus-new", ReaderPassKind.FOCUSED_READ, ["p-b"])
    with pytest.raises(ValueError, match="FOCUSED_READ"):
        reader.record_region("focus-new", "p-b", CoverageState.REVISITED)
    reader.record_region("focus-new", "p-b", CoverageState.PROCESSED)
    reader.complete_pass("focus-new")
    assert session.coverage["p-a"].state is CoverageState.REVISITED
    assert session.coverage["p-b"].state is CoverageState.PROCESSED


def test_cross_check_and_targeted_reread_require_prior_processing_and_recovery_reason():
    _, session, _, reader = _reader()

    reader.begin_pass("broad", ReaderPassKind.BROAD_READ, ["p-a", "p-b"])
    reader.record_region("broad", "p-a", CoverageState.PROCESSED)
    reader.record_region("broad", "p-b", CoverageState.PROCESSED)
    reader.complete_pass("broad")

    reader.begin_pass("cross", ReaderPassKind.CROSS_CHECK, ["p-a", "p-b"])
    with pytest.raises(ValueError, match="only produce"):
        reader.record_region("cross", "p-a", CoverageState.PROCESSED)
    reader.record_region("cross", "p-a", CoverageState.REVISITED)
    reader.record_region("cross", "p-b", CoverageState.NEEDS_REVIEW, reason="possible conflict")
    reader.complete_pass("cross")

    targeted = reader.begin_pass(
        "reread",
        ReaderPassKind.TARGETED_REREAD,
        ["p-b"],
        rationale="open loop: possible conflict",
    )
    assert targeted.rationale == "open loop: possible conflict"
    with pytest.raises(ValueError, match="review reason"):
        reader.record_region("reread", "p-b", CoverageState.REVISITED)
    recovered = reader.record_region(
        "reread",
        "p-b",
        CoverageState.REVISITED,
        reason="targeted reread resolved local ambiguity",
    )
    assert recovered.before is CoverageState.NEEDS_REVIEW
    reader.complete_pass("reread")

    fresh_source, fresh_session, _, fresh_reader = _reader()
    assert fresh_source is fresh_session.source
    fresh_reader.begin_pass("orient", ReaderPassKind.ORIENTATION, ["p-a"])
    fresh_reader.record_region("orient", "p-a", CoverageState.SEEN)
    fresh_reader.complete_pass("orient")
    fresh_reader.begin_pass(
        "too-early",
        ReaderPassKind.TARGETED_REREAD,
        ["p-a"],
        rationale="query",
    )
    with pytest.raises(ValueError, match="prior processing"):
        fresh_reader.record_region("too-early", "p-a", CoverageState.REVISITED)
    fresh_reader.interrupt_pass("too-early", "cannot reread an only-seen region")


def test_interrupt_and_degrade_preserve_partial_progress_and_allow_next_pass():
    _, session, _, reader = _reader()
    reader.begin_pass("partial", ReaderPassKind.BROAD_READ, ["p-a", "p-b"])
    reader.record_region("partial", "p-a", CoverageState.PROCESSED)

    with pytest.raises(ValueError, match="reason"):
        reader.interrupt_pass("partial", " ")
    assert reader.active_pass_id == "partial"
    interrupted = reader.interrupt_pass("partial", "provider-independent processor stopped")
    assert interrupted.state is ReaderPassState.INTERRUPTED
    assert interrupted.reason == "provider-independent processor stopped"
    assert len(interrupted.outcomes) == 1
    assert session.coverage["p-a"].state is CoverageState.PROCESSED
    assert session.coverage["p-b"].state is CoverageState.UNREAD

    reader.begin_pass("degraded", ReaderPassKind.BROAD_READ, ["p-b"])
    degraded = reader.degrade_pass("degraded", "source region unavailable")
    assert degraded.state is ReaderPassState.DEGRADED
    assert reader.active_pass_id is None

    reader.begin_pass("next", ReaderPassKind.BROAD_READ, ["p-b"])
    with pytest.raises(ValueError, match="not the active"):
        reader.record_region("wrong", "p-b", CoverageState.PROCESSED)
    with pytest.raises(ValueError, match="already active"):
        reader.begin_pass("another", ReaderPassKind.BROAD_READ, ["p-a"])
    reader.record_region("next", "p-b", CoverageState.PROCESSED)
    reader.complete_pass("next")

    with pytest.raises(ValueError, match="duplicate"):
        reader.begin_pass("next", ReaderPassKind.BROAD_READ, ["p-a"])


def test_session_closure_fails_closed_and_terminal_private_guard_is_defensive():
    _, session, _, reader = _reader()
    reader.begin_pass("active", ReaderPassKind.BROAD_READ, ["p-a"])
    session.finish()
    with pytest.raises(ValueError, match="no longer OPEN"):
        reader.record_region("active", "p-a", CoverageState.PROCESSED)
    with pytest.raises(ValueError, match="no longer OPEN"):
        reader.complete_pass("active")
    with pytest.raises(ValueError, match="no longer OPEN"):
        reader.interrupt_pass("active", "stop")
    with pytest.raises(ValueError, match="no longer OPEN"):
        reader.begin_pass("new", ReaderPassKind.BROAD_READ, ["p-a"])

    _, _, _, defensive = _reader()
    defensive.begin_pass("p", ReaderPassKind.BROAD_READ, ["p-a"])
    defensive.record_region("p", "p-a", CoverageState.PROCESSED)
    defensive.complete_pass("p")
    defensive._active_pass_id = "p"
    with pytest.raises(ValueError, match="not ATTEMPTED"):
        defensive._require_active("p")


def test_telemetry_counts_passes_without_comprehension_scores():
    _, _, _, reader = _reader()

    reader.begin_pass("done", ReaderPassKind.BROAD_READ, ["p-a"])
    reader.record_region("done", "p-a", CoverageState.PROCESSED)
    reader.complete_pass("done")

    reader.begin_pass("interrupted", ReaderPassKind.BROAD_READ, ["p-b"])
    reader.interrupt_pass("interrupted", "stopped")

    reader.begin_pass("degraded", ReaderPassKind.ORIENTATION, ["amb"])
    reader.degrade_pass("degraded", "unsupported structure")

    reader.begin_pass("active", ReaderPassKind.ORIENTATION, ["section-a"])
    telemetry = reader.telemetry()

    assert telemetry.total_passes == 4
    assert telemetry.completed_passes == 1
    assert telemetry.unresolved_passes == 3
    assert telemetry.active_pass_id == "active"
    assert telemetry.kind_counts[ReaderPassKind.BROAD_READ] == 2
    assert telemetry.kind_counts[ReaderPassKind.ORIENTATION] == 2
    assert telemetry.state_counts[ReaderPassState.COMPLETED] == 1
    assert telemetry.state_counts[ReaderPassState.INTERRUPTED] == 1
    assert telemetry.state_counts[ReaderPassState.DEGRADED] == 1
    assert telemetry.state_counts[ReaderPassState.ATTEMPTED] == 1
    assert not hasattr(telemetry, "comprehension_percent")
    assert not hasattr(telemetry, "truth_score")


def test_rc3_exposes_no_authority_fields_and_imports_only_reader_layers():
    record_fields = {field.name for field in dataclasses.fields(ReaderPassRecord)}
    outcome_fields = {field.name for field in dataclasses.fields(RegionPassOutcome)}
    forbidden = {
        "truth_status",
        "confidence",
        "canon",
        "esm",
        "belief",
        "authority",
        "planner",
        "importance",
    }
    assert record_fields.isdisjoint(forbidden)
    assert outcome_fields.isdisjoint(forbidden)

    source = inspect.getsource(reader_passes)
    tree = ast.parse(source)
    core_imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            core_imports.update(alias.name for alias in node.names if alias.name.startswith("core."))
        elif isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("core."):
            core_imports.add(node.module)
    assert core_imports == {"core.reader_core", "core.reader_structure"}

    src = _source()
    recovered = _structure(src).get("p-a")
    with pytest.raises(ValueError, match="unsupported Reader pass kind"):
        MultiPassReader._validate_effect(  # type: ignore[arg-type]
            "UNKNOWN",
            recovered,
            CoverageState.PROCESSED,
            CoverageState.REVISITED,
        )
