from __future__ import annotations

import ast
import inspect

import pytest

import core.reader_product_bridge as reader_product_bridge
from core.reader_core import (
    CoverageEntry,
    CoverageState,
    ReaderSession,
    ReaderSessionState,
    SourceLocator,
    SourceVersion,
)
from core.reader_passes import ReaderPassKind, ReaderPassState
from core.reader_product_bridge import (
    ReaderProductBridge,
    ReaderProductStatus,
    RegionReadResult,
)
from core.reader_structure import (
    DocumentStructuralMap,
    StructuralKind,
    StructuralNode,
    StructuralStatus,
)


def _source(text: str = "a" * 300) -> SourceVersion:
    return SourceVersion.from_text("doc-product", "file:///doc-product.txt", text)


def _loc(source: SourceVersion, start: int, end: int) -> SourceLocator:
    return SourceLocator(source, span_start=start, span_end=end)


def _structure(source: SourceVersion | None = None) -> DocumentStructuralMap:
    source = source or _source()
    return DocumentStructuralMap(
        source,
        [
            StructuralNode("doc", StructuralKind.DOCUMENT, _loc(source, 0, 300), 0),
            StructuralNode("section-a", StructuralKind.SECTION, _loc(source, 0, 140), 1, "doc"),
            StructuralNode("section-b", StructuralKind.SECTION, _loc(source, 150, 290), 2, "doc"),
        ],
    )


def _bridge(source: SourceVersion | None = None) -> ReaderProductBridge:
    source = source or _source()
    return ReaderProductBridge(
        ReaderSession("product-session", source, "understand document"),
        _structure(source),
    )


def test_complete_product_run_uses_one_broad_pass_and_no_reread():
    bridge = _bridge()
    calls: list[tuple[ReaderPassKind, str, CoverageState]] = []

    def executor(kind, node, before):
        calls.append((kind, node.node_id, before))
        return RegionReadResult(CoverageState.PROCESSED)

    result = bridge.run(executor)

    assert result.status is ReaderProductStatus.COMPLETE
    assert result.complete is True
    assert result.session.state is ReaderSessionState.COMPLETED
    assert result.reread_node_ids == ()
    assert result.unresolved_node_ids == ()
    assert len(result.passes) == 1
    assert result.passes[0].kind is ReaderPassKind.BROAD_READ
    assert result.passes[0].state is ReaderPassState.COMPLETED
    assert calls == [
        (ReaderPassKind.BROAD_READ, "section-a", CoverageState.UNREAD),
        (ReaderPassKind.BROAD_READ, "section-b", CoverageState.UNREAD),
    ]


def test_one_targeted_reread_can_close_visible_gap():
    bridge = _bridge()
    calls: list[tuple[ReaderPassKind, str]] = []

    def executor(kind, node, before):
        calls.append((kind, node.node_id))
        if kind is ReaderPassKind.BROAD_READ and node.node_id == "section-b":
            return RegionReadResult(CoverageState.NEEDS_REVIEW, "ambiguous first pass")
        if kind is ReaderPassKind.TARGETED_REREAD:
            assert before is CoverageState.NEEDS_REVIEW
            return RegionReadResult(CoverageState.REVISITED, "ambiguity resolved on reread")
        return RegionReadResult(CoverageState.PROCESSED)

    result = bridge.run(executor)

    assert result.status is ReaderProductStatus.COMPLETE
    assert result.reread_node_ids == ("section-b",)
    assert result.unresolved_node_ids == ()
    assert [record.kind for record in result.passes] == [
        ReaderPassKind.BROAD_READ,
        ReaderPassKind.TARGETED_REREAD,
    ]
    assert calls.count((ReaderPassKind.TARGETED_REREAD, "section-b")) == 1


def test_remaining_gap_degrades_after_exactly_one_reread_round():
    bridge = _bridge()
    reread_calls = 0

    def executor(kind, node, before):
        nonlocal reread_calls
        if node.node_id == "section-b":
            if kind is ReaderPassKind.TARGETED_REREAD:
                reread_calls += 1
            return RegionReadResult(CoverageState.NEEDS_REVIEW, "still unresolved")
        return RegionReadResult(CoverageState.PROCESSED)

    result = bridge.run(executor)

    assert result.status is ReaderProductStatus.DEGRADED
    assert result.complete is False
    assert result.session.state is ReaderSessionState.DEGRADED
    assert result.session.state_reason == "reader_product_incomplete_after_bounded_reread"
    assert result.reread_node_ids == ("section-b",)
    assert result.unresolved_node_ids == ("section-b",)
    assert reread_calls == 1
    assert len(result.passes) == 2


def test_preexisting_out_of_map_gap_degrades_without_hidden_reread_or_crash():
    source = _source()
    session = ReaderSession("product-session", source, "understand document")
    session.set_coverage(
        CoverageEntry(
            region_id="legacy-region",
            state=CoverageState.NEEDS_REVIEW,
            locator=_loc(source, 291, 299),
            reason="pre-existing unresolved region",
        )
    )
    bridge = ReaderProductBridge(session, _structure(source))
    calls: list[tuple[ReaderPassKind, str]] = []

    def executor(kind, node, before):
        calls.append((kind, node.node_id))
        return RegionReadResult(CoverageState.PROCESSED)

    result = bridge.run(executor)

    assert result.status is ReaderProductStatus.DEGRADED
    assert result.session.state is ReaderSessionState.DEGRADED
    assert result.session.state_reason == "reader_product_incomplete_after_bounded_reread"
    assert result.reread_node_ids == ()
    assert result.unresolved_node_ids == ("legacy-region",)
    assert [record.kind for record in result.passes] == [ReaderPassKind.BROAD_READ]
    assert calls == [
        (ReaderPassKind.BROAD_READ, "section-a"),
        (ReaderPassKind.BROAD_READ, "section-b"),
    ]


def test_unresolved_structure_cannot_be_silently_marked_processed():
    source = _source()
    structure = DocumentStructuralMap(
        source,
        [
            StructuralNode("doc", StructuralKind.DOCUMENT, _loc(source, 0, 300), 0),
            StructuralNode(
                "table",
                StructuralKind.TABLE_REGION,
                _loc(source, 20, 50),
                1,
                "doc",
                status=StructuralStatus.AMBIGUOUS,
                reason="layout unresolved",
            ),
        ],
    )
    bridge = ReaderProductBridge(ReaderSession("s", source, "read"), structure)

    with pytest.raises(ValueError, match="unresolved structural regions"):
        bridge.run(lambda kind, node, before: RegionReadResult(CoverageState.PROCESSED))

    assert bridge.reader.session.state is ReaderSessionState.DEGRADED
    assert bridge.reader.session.state_reason == "reader_product_broad_read_failed"


def test_executor_failure_degrades_and_propagates_without_hidden_retry():
    bridge = _bridge()
    calls = 0

    def executor(kind, node, before):
        nonlocal calls
        calls += 1
        raise RuntimeError("reader unavailable")

    with pytest.raises(RuntimeError, match="reader unavailable"):
        bridge.run(executor)

    assert calls == 1
    assert bridge.reader.session.state is ReaderSessionState.DEGRADED
    assert bridge.reader.records[0].state is ReaderPassState.DEGRADED


def test_bridge_rejects_wrong_versions_closed_sessions_and_non_callable_executor():
    source = _source()
    changed = _source("changed")
    with pytest.raises(ValueError, match="same source version"):
        ReaderProductBridge(ReaderSession("s", changed, "read"), _structure(source))

    closed = ReaderSession("closed", source, "read")
    closed.finish()
    with pytest.raises(ValueError, match="OPEN"):
        ReaderProductBridge(closed, _structure(source))

    bridge = _bridge()
    with pytest.raises(ValueError, match="callable"):
        bridge.run(object())  # type: ignore[arg-type]


def test_bridge_constructor_rejects_invalid_runtime_types():
    source = _source()
    with pytest.raises(ValueError, match="ReaderSession"):
        ReaderProductBridge(object(), _structure(source))  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="DocumentStructuralMap"):
        ReaderProductBridge(
            ReaderSession("typed", source, "read"),
            object(),  # type: ignore[arg-type]
        )


def test_run_rejects_session_that_closed_after_bridge_creation():
    bridge = _bridge()
    bridge.reader.session.degrade("closed externally")

    with pytest.raises(ValueError, match="OPEN"):
        bridge.run(lambda kind, node, before: RegionReadResult(CoverageState.PROCESSED))


def test_document_only_structure_degrades_without_executor_call():
    source = _source()
    structure = DocumentStructuralMap(
        source,
        [StructuralNode("doc", StructuralKind.DOCUMENT, _loc(source, 0, 300), 0)],
    )
    bridge = ReaderProductBridge(ReaderSession("doc-only", source, "read"), structure)
    calls = 0

    def executor(kind, node, before):
        nonlocal calls
        calls += 1
        return RegionReadResult(CoverageState.PROCESSED)

    result = bridge.run(executor)

    assert result.status is ReaderProductStatus.DEGRADED
    assert result.session.state is ReaderSessionState.DEGRADED
    assert result.session.state_reason == "reader_product_no_readable_regions"
    assert result.passes == ()
    assert calls == 0


def test_targeted_reread_failure_degrades_and_propagates_without_hidden_retry():
    bridge = _bridge()
    calls: list[tuple[ReaderPassKind, str]] = []

    def executor(kind, node, before):
        calls.append((kind, node.node_id))
        if kind is ReaderPassKind.TARGETED_REREAD:
            raise RuntimeError("reread unavailable")
        if node.node_id == "section-b":
            return RegionReadResult(CoverageState.NEEDS_REVIEW, "needs reread")
        return RegionReadResult(CoverageState.PROCESSED)

    with pytest.raises(RuntimeError, match="reread unavailable"):
        bridge.run(executor)

    assert bridge.reader.session.state is ReaderSessionState.DEGRADED
    assert bridge.reader.session.state_reason == "reader_product_targeted_reread_failed"
    assert len(bridge.reader.records) == 2
    assert bridge.reader.records[1].kind is ReaderPassKind.TARGETED_REREAD
    assert bridge.reader.records[1].state is ReaderPassState.DEGRADED
    assert sum(kind is ReaderPassKind.TARGETED_REREAD for kind, _ in calls) == 1


def test_executor_must_return_region_read_result():
    bridge = _bridge()

    with pytest.raises(ValueError, match="RegionReadResult"):
        bridge.run(lambda kind, node, before: object())  # type: ignore[return-value]

    assert bridge.reader.session.state is ReaderSessionState.DEGRADED
    assert bridge.reader.session.state_reason == "reader_product_broad_read_failed"
    assert bridge.reader.records[0].state is ReaderPassState.DEGRADED


def test_region_result_validation():
    with pytest.raises(ValueError, match="CoverageState"):
        RegionReadResult("PROCESSED")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="reason"):
        RegionReadResult(CoverageState.NEEDS_REVIEW, " ")


def test_product_bridge_has_no_authority_or_provider_imports():
    tree = ast.parse(inspect.getsource(reader_product_bridge))
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module)

    forbidden = {
        "core.truth_gate",
        "core.guardian",
        "core.memory",
        "core.pipeline",
        "core.ingest",
        "core.embedding",
        "core.llm_router",
        "core.remote_egress",
    }
    assert imported.isdisjoint(forbidden)
