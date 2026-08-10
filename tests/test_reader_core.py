from __future__ import annotations

import ast
import dataclasses
import inspect

import pytest

import core.reader_core as reader_core
from core.evidence import sha256 as evidence_sha256
from core.reader_core import (
    CoverageEntry,
    CoverageState,
    OpenLoop,
    ReaderBookmark,
    ReaderSession,
    ReaderSessionState,
    SegmentCard,
    SourceFidelity,
    SourceLocator,
    SourceVersion,
    source_sha256,
)


def _source(
    text: str = "alpha beta gamma",
    *,
    document_id: str = "doc-1",
    source_uri: str = "file:///doc-1.txt",
    restricted: bool = False,
    sensitivity: str | None = None,
) -> SourceVersion:
    return SourceVersion.from_text(
        document_id,
        source_uri,
        text,
        restricted=restricted,
        sensitivity=sensitivity,
    )


def _locator(source: SourceVersion | None = None) -> SourceLocator:
    return SourceLocator(source=source or _source(), span_start=0, span_end=5)


def test_source_hash_matches_existing_evidence_convention_and_text_is_not_retained():
    text = "Привет, evidence"
    source = SourceVersion.from_text(" doc ", " file:///x ", text)

    assert source_sha256(text) == evidence_sha256(text)
    assert source_sha256("") == evidence_sha256("")
    assert source.document_id == "doc"
    assert source.source_uri == "file:///x"
    assert source.source_sha256 == evidence_sha256(text)
    assert "source_text" not in {field.name for field in dataclasses.fields(SourceVersion)}
    assert text not in repr(source)


def test_source_version_validation_normalization_identity_and_runtime_types():
    digest = "A" * 64
    source = SourceVersion("doc", "file:///x", digest, sensitivity=" restricted ")
    assert source.source_sha256 == digest.lower()
    assert source.sensitivity == "restricted"
    assert source.same_version(SourceVersion("doc", "file:///x", digest.lower()))
    assert not source.same_version(SourceVersion("doc", "file:///other", digest.lower()))
    assert source.same_version(object()) is False  # type: ignore[arg-type]

    with pytest.raises(ValueError, match="document_id"):
        SourceVersion(" ", "file:///x", digest)
    with pytest.raises(ValueError, match="source_uri"):
        SourceVersion("doc", " ", digest)
    with pytest.raises(ValueError, match="source_sha256"):
        SourceVersion("doc", "file:///x", "bad")
    with pytest.raises(ValueError, match="restricted must be a bool"):
        SourceVersion("doc", "file:///x", digest, restricted=1)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="sensitivity"):
        SourceVersion("doc", "file:///x", digest, sensitivity=" ")


def test_source_locator_supports_exact_and_structural_replayable_addresses():
    source = _source()
    exact = SourceLocator(
        source,
        span_start=1,
        span_end=4,
        structural_locator=" paragraph:1 ",
        section=" intro ",
        chunk_id=" c1 ",
    )
    assert exact.has_exact_span is True
    assert exact.structural_locator == "paragraph:1"
    assert exact.section == "intro"
    assert exact.chunk_id == "c1"
    assert exact.replay_key == (
        source.document_id,
        source.source_uri,
        source.source_sha256,
        1,
        4,
        "paragraph:1",
    )

    structural = SourceLocator(source, structural_locator="section:2")
    assert structural.has_exact_span is False
    assert structural.replay_key[-1] == "section:2"


def test_source_locator_rejects_missing_or_invalid_addresses_and_source_type():
    source = _source()
    with pytest.raises(ValueError, match="SourceVersion"):
        SourceLocator(object(), span_start=0, span_end=1)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="given together"):
        SourceLocator(source, span_start=0)
    with pytest.raises(ValueError, match="integers"):
        SourceLocator(source, span_start="0", span_end=1)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="non-negative"):
        SourceLocator(source, span_start=-1, span_end=1)
    with pytest.raises(ValueError, match="span_start"):
        SourceLocator(source, span_start=2, span_end=1)
    with pytest.raises(ValueError, match="structural_locator"):
        SourceLocator(source, structural_locator=" ")
    with pytest.raises(ValueError, match="required"):
        SourceLocator(source)
    with pytest.raises(ValueError, match="section"):
        SourceLocator(source, span_start=0, span_end=1, section=" ")
    with pytest.raises(ValueError, match="chunk_id"):
        SourceLocator(source, span_start=0, span_end=1, chunk_id=" ")


def test_segment_card_preserves_fidelity_provenance_and_source_restrictions():
    source = _source(restricted=True, sensitivity="PII")
    locator = _locator(source)
    support = SourceLocator(source, span_start=6, span_end=10)

    for fidelity in SourceFidelity:
        card = SegmentCard(
            card_id=f"card-{fidelity.value}",
            locator=locator,
            fidelity=fidelity,
            statement=" derived statement ",
            supporting_locators=[support],  # type: ignore[arg-type]
        )
        assert card.statement == "derived statement"
        assert card.restricted is True
        assert card.sensitivity == "PII"
        assert card.locator.source.source_sha256 == source.source_sha256
        assert card.supporting_locators == (support,)


def test_segment_card_rejects_invalid_runtime_types_and_mixed_versions():
    locator = _locator()
    with pytest.raises(ValueError, match="card_id"):
        SegmentCard(" ", locator, SourceFidelity.SUMMARY, "summary")
    with pytest.raises(ValueError, match="locator must be a SourceLocator"):
        SegmentCard("card", object(), SourceFidelity.SUMMARY, "summary")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="fidelity must be a SourceFidelity"):
        SegmentCard("card", locator, "SUMMARY", "summary")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="statement"):
        SegmentCard("card", locator, SourceFidelity.SUMMARY, " ")
    with pytest.raises(ValueError, match="supporting locators must be SourceLocator"):
        SegmentCard(
            "card",
            locator,
            SourceFidelity.INFERENCE,
            "inference",
            supporting_locators=(object(),),  # type: ignore[arg-type]
        )

    other_version = _source("changed")
    with pytest.raises(ValueError, match="same source version"):
        SegmentCard(
            "card",
            locator,
            SourceFidelity.INFERENCE,
            "inference",
            supporting_locators=(_locator(other_version),),
        )


def test_coverage_entry_requires_fail_visible_missing_locator_and_typed_state():
    locator = _locator()
    with pytest.raises(ValueError, match="region_id"):
        CoverageEntry(" ", CoverageState.NEEDS_REVIEW, reason="missing")
    with pytest.raises(ValueError, match="state must be a CoverageState"):
        CoverageEntry("r1", "UNREAD", locator=locator)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="locator must be a SourceLocator"):
        CoverageEntry("r1", CoverageState.UNREAD, locator=object())  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="must be NEEDS_REVIEW"):
        CoverageEntry("r1", CoverageState.UNREAD)
    with pytest.raises(ValueError, match="explicit reason"):
        CoverageEntry("r1", CoverageState.NEEDS_REVIEW)
    with pytest.raises(ValueError, match="reason"):
        CoverageEntry("r1", CoverageState.NEEDS_REVIEW, reason=" ")

    entry = CoverageEntry(" r1 ", CoverageState.NEEDS_REVIEW, reason=" missing span ")
    assert entry.region_id == "r1"
    assert entry.reason == "missing span"
    assert entry.locator is None


def test_coverage_transitions_are_explicit_and_review_recovery_is_auditable():
    locator = _locator()
    unread = CoverageEntry("r1", CoverageState.UNREAD, locator=locator)
    assert unread.transition(CoverageState.UNREAD) is unread

    with pytest.raises(ValueError, match="target must be a CoverageState"):
        unread.transition("SEEN")  # type: ignore[arg-type]

    seen = unread.transition(CoverageState.SEEN)
    assert seen.state is CoverageState.SEEN
    processed = seen.transition(CoverageState.PROCESSED, reason="objective read")
    assert processed.state is CoverageState.PROCESSED
    assert processed.reason == "objective read"
    revisited = processed.transition(CoverageState.REVISITED)
    assert revisited.state is CoverageState.REVISITED
    assert revisited.transition(CoverageState.REVISITED) is revisited

    review = revisited.transition(CoverageState.NEEDS_REVIEW, reason="ambiguous")
    assert review.state is CoverageState.NEEDS_REVIEW
    assert review.reason == "ambiguous"
    assert review.transition(CoverageState.NEEDS_REVIEW) is review
    refreshed_review = review.transition(CoverageState.NEEDS_REVIEW, reason="still ambiguous")
    assert refreshed_review.reason == "still ambiguous"

    with pytest.raises(ValueError, match="review reason"):
        review.transition(CoverageState.PROCESSED)
    recovered = review.transition(CoverageState.REVISITED, reason="manual reread")
    assert recovered.state is CoverageState.REVISITED
    assert recovered.reason == "manual reread"

    with pytest.raises(ValueError, match="non-empty"):
        processed.transition(CoverageState.NEEDS_REVIEW)
    with pytest.raises(ValueError, match="illegal coverage transition"):
        processed.transition(CoverageState.SEEN)

    direct = unread.transition(CoverageState.PROCESSED)
    assert direct.state is CoverageState.PROCESSED
    assert direct.reason is None


def test_bookmarks_and_open_loops_are_source_linked_and_inherit_privacy_metadata():
    source = _source(restricted=True, sensitivity="private")
    locator = _locator(source)
    bookmark = ReaderBookmark(" bookmark ", locator, " revisit qualifier ")
    open_loop = OpenLoop(" loop ", locator, " what does this reference mean? ")

    assert bookmark.bookmark_id == "bookmark"
    assert bookmark.reason == "revisit qualifier"
    assert bookmark.restricted is True
    assert bookmark.sensitivity == "private"
    assert open_loop.loop_id == "loop"
    assert open_loop.question == "what does this reference mean?"
    assert open_loop.restricted is True
    assert open_loop.sensitivity == "private"

    with pytest.raises(ValueError, match="bookmark_id"):
        ReaderBookmark(" ", locator, "reason")
    with pytest.raises(ValueError, match="locator must be a SourceLocator"):
        ReaderBookmark("bookmark", object(), "reason")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="reason"):
        ReaderBookmark("bookmark", locator, " ")
    with pytest.raises(ValueError, match="loop_id"):
        OpenLoop(" ", locator, "question")
    with pytest.raises(ValueError, match="locator must be a SourceLocator"):
        OpenLoop("loop", object(), "question")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="question"):
        OpenLoop("loop", locator, " ")


def test_reader_session_identity_is_read_only_and_collections_are_encapsulated():
    source = _source(restricted=True, sensitivity="private")
    locator = _locator(source)
    session = ReaderSession(" session ", source, " read objective ", state_reason=" initial ")
    assert session.session_id == "session"
    assert session.source is source
    assert session.objective == "read objective"
    assert session.state is ReaderSessionState.OPEN
    assert session.state_reason == "initial"
    assert not hasattr(session, "__dict__")

    card = SegmentCard("card", locator, SourceFidelity.DIRECT_SOURCE_OBSERVATION, "source says X")
    bookmark = ReaderBookmark("bookmark", locator, "important")
    open_loop = OpenLoop("loop", locator, "resolve reference")
    coverage = CoverageEntry("r1", CoverageState.UNREAD, locator=locator)
    session.add_segment_card(card)
    session.add_bookmark(bookmark)
    session.add_open_loop(open_loop)
    session.set_coverage(coverage)

    assert session.segment_cards == (card,)
    assert session.bookmarks == (bookmark,)
    assert session.open_loops == (open_loop,)
    assert session.coverage == {"r1": coverage}

    coverage_snapshot = session.coverage
    coverage_snapshot.clear()
    assert session.coverage == {"r1": coverage}
    cards_snapshot = session.segment_cards
    cards_snapshot += (card,)
    assert session.segment_cards == (card,)

    with pytest.raises(AttributeError):
        session.source = _source("changed")  # type: ignore[misc]


def test_reader_session_rejects_wrong_types_versions_and_unknown_regions():
    source = _source()
    locator = _locator(source)
    session = ReaderSession("session", source, "objective")

    with pytest.raises(ValueError, match="card must be a SegmentCard"):
        session.add_segment_card(object())  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="entry must be a CoverageEntry"):
        session.set_coverage(object())  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="bookmark must be a ReaderBookmark"):
        session.add_bookmark(object())  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="open_loop must be an OpenLoop"):
        session.add_open_loop(object())  # type: ignore[arg-type]

    other = _source("changed")
    with pytest.raises(ValueError, match="different source version"):
        session.add_segment_card(
            SegmentCard("other", _locator(other), SourceFidelity.SUMMARY, "summary")
        )
    with pytest.raises(ValueError, match="different source version"):
        session.set_coverage(CoverageEntry("other", CoverageState.PROCESSED, _locator(other)))
    with pytest.raises(ValueError, match="different source version"):
        session.add_bookmark(ReaderBookmark("other", _locator(other), "reason"))
    with pytest.raises(ValueError, match="different source version"):
        session.add_open_loop(OpenLoop("other", _locator(other), "question"))

    session.set_coverage(CoverageEntry("r1", CoverageState.UNREAD, locator=locator))
    with pytest.raises(ValueError, match="region_id"):
        session.transition_coverage(" ", CoverageState.SEEN)
    with pytest.raises(KeyError):
        session.transition_coverage("unknown", CoverageState.SEEN)
    assert session.transition_coverage("r1", CoverageState.SEEN).state is CoverageState.SEEN


def test_reader_session_constructor_validation_and_closed_sessions_fail_closed():
    source = _source()
    locator = _locator(source)
    card = SegmentCard("card", locator, SourceFidelity.SUMMARY, "summary")

    with pytest.raises(ValueError, match="session_id"):
        ReaderSession(" ", source, "objective")
    with pytest.raises(ValueError, match="source must be a SourceVersion"):
        ReaderSession("session", object(), "objective")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="objective"):
        ReaderSession("session", source, " ")
    with pytest.raises(ValueError, match="state must be a ReaderSessionState"):
        ReaderSession("session", source, "objective", state="OPEN")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="state_reason"):
        ReaderSession("session", source, "objective", state_reason=" ")

    session = ReaderSession("session", source, "objective", state_reason="temporary")
    session.finish()
    assert session.state is ReaderSessionState.COMPLETED
    assert session.state_reason is None
    with pytest.raises(ValueError, match="cannot finish"):
        session.finish()
    with pytest.raises(ValueError, match="cannot add segment card"):
        session.add_segment_card(card)


def test_interrupted_and_degraded_sessions_fail_visibly_without_partial_mutation():
    source = _source()

    interrupted = ReaderSession("i", source, "objective")
    with pytest.raises(ValueError, match="reason"):
        interrupted.interrupt(" ")
    assert interrupted.state is ReaderSessionState.OPEN
    interrupted.interrupt(" provider failed ")
    assert interrupted.state is ReaderSessionState.INTERRUPTED
    assert interrupted.state_reason == "provider failed"
    with pytest.raises(ValueError, match="cannot interrupt"):
        interrupted.interrupt("again")

    degraded = ReaderSession("d", source, "objective")
    with pytest.raises(ValueError, match="reason"):
        degraded.degrade(" ")
    assert degraded.state is ReaderSessionState.OPEN
    degraded.degrade(" truncated source ")
    assert degraded.state is ReaderSessionState.DEGRADED
    assert degraded.state_reason == "truncated source"


def test_coverage_telemetry_exposes_gaps_without_a_comprehension_percentage():
    source = _source()
    locator = _locator(source)
    session = ReaderSession("session", source, "objective")
    session.set_coverage(CoverageEntry("u", CoverageState.UNREAD, locator=locator))
    session.set_coverage(CoverageEntry("p", CoverageState.PROCESSED, locator=locator))
    session.set_coverage(CoverageEntry("r", CoverageState.REVISITED, locator=locator))
    session.set_coverage(
        CoverageEntry("n", CoverageState.NEEDS_REVIEW, reason="unsupported structure")
    )

    telemetry = session.coverage_telemetry()
    assert telemetry.total_regions == 4
    assert telemetry.counts[CoverageState.UNREAD] == 1
    assert telemetry.counts[CoverageState.PROCESSED] == 1
    assert telemetry.counts[CoverageState.REVISITED] == 1
    assert telemetry.counts[CoverageState.NEEDS_REVIEW] == 1
    assert telemetry.counts[CoverageState.SEEN] == 0
    assert telemetry.unresolved_regions == 2
    assert telemetry.missing_locator_regions == 1
    assert telemetry.has_visible_gaps is True
    assert not hasattr(telemetry, "comprehension")
    assert not hasattr(telemetry, "comprehension_percentage")

    telemetry.counts[CoverageState.UNREAD] = 99
    assert session.coverage_telemetry().counts[CoverageState.UNREAD] == 1

    clean = ReaderSession("clean", source, "objective")
    clean.set_coverage(CoverageEntry("p", CoverageState.PROCESSED, locator=locator))
    assert clean.coverage_telemetry().has_visible_gaps is False


def test_source_change_stales_whole_rc1_session_without_rewriting_history():
    source = _source("version one")
    locator = _locator(source)
    session = ReaderSession("session", source, "objective")
    card = SegmentCard("card", locator, SourceFidelity.SUMMARY, "derived summary")
    session.add_segment_card(card)
    session.add_bookmark(ReaderBookmark("bookmark", locator, "revisit"))
    session.add_open_loop(OpenLoop("loop", locator, "question"))
    session.set_coverage(CoverageEntry("r1", CoverageState.PROCESSED, locator=locator))

    with pytest.raises(ValueError, match="new_source must be a SourceVersion"):
        session.invalidate_for(object())  # type: ignore[arg-type]

    same = session.invalidate_for(source)
    assert same.stale is False
    assert same.scope == "none"
    assert same.invalidated_regions == 0
    assert same.invalidated_artifacts == 0
    assert session.state is ReaderSessionState.OPEN

    with pytest.raises(ValueError, match="different document_id"):
        session.invalidate_for(_source("other", document_id="doc-2"))

    changed = _source("version two")
    report = session.invalidate_for(changed)
    assert report.stale is True
    assert report.scope == "all"
    assert report.old_source_sha256 == source.source_sha256
    assert report.new_source_sha256 == changed.source_sha256
    assert report.invalidated_regions == 1
    assert report.invalidated_artifacts == 3
    assert session.state is ReaderSessionState.STALE
    assert "no proven remapping" in (session.state_reason or "")
    assert session.segment_cards[0] is card
    assert card.locator.source.same_version(source)

    with pytest.raises(ValueError, match="cannot degrade a stale session"):
        session.degrade("failure")
    with pytest.raises(ValueError, match="cannot set coverage"):
        session.set_coverage(CoverageEntry("r2", CoverageState.PROCESSED, locator=locator))


def test_reader_core_has_structural_authority_firewall_and_no_truth_fields():
    tree = ast.parse(inspect.getsource(reader_core))
    imported_modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_modules.add(node.module)

    assert not any(module == "core" or module.startswith("core.") for module in imported_modules)

    authority_fields = {
        "truth_status",
        "esm_state",
        "canon",
        "claim_id",
        "contradiction_resolution",
        "planner_authority",
    }
    for cls in (
        SourceVersion,
        SourceLocator,
        SegmentCard,
        CoverageEntry,
        ReaderBookmark,
        OpenLoop,
    ):
        assert authority_fields.isdisjoint({field.name for field in dataclasses.fields(cls)})

    normalized_slots = {name.lstrip("_") for name in ReaderSession.__slots__}
    assert authority_fields.isdisjoint(normalized_slots)
    assert not hasattr(ReaderSession, "ingest")
    assert not hasattr(ReaderSession, "promote")
    assert not hasattr(ReaderSession, "resolve_contradiction")
    assert not hasattr(ReaderSession, "plan")
