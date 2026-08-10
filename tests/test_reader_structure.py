from __future__ import annotations

import ast
import dataclasses
import inspect

import pytest

import core.reader_structure as reader_structure
from core.reader_core import SourceLocator, SourceVersion
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
        "doc-structure",
        "file:///doc-structure.txt",
        text,
        restricted=restricted,
        sensitivity=sensitivity,
    )


def _exact(source: SourceVersion, start: int, end: int) -> SourceLocator:
    return SourceLocator(source, span_start=start, span_end=end)


def _root(source: SourceVersion | None = None, *, end: int = 200) -> StructuralNode:
    source = source or _source()
    return StructuralNode("doc", StructuralKind.DOCUMENT, _exact(source, 0, end), 0)


def test_structural_kind_contract_covers_rc0_categories():
    assert {kind.value for kind in StructuralKind} == {
        "DOCUMENT",
        "SECTION",
        "SUBSECTION",
        "PARAGRAPH",
        "DIALOGUE_TURN",
        "LIST",
        "LIST_ITEM",
        "TABLE",
        "TABLE_REGION",
        "CODE_BLOCK",
        "QUOTATION",
        "FOOTNOTE",
        "ENDNOTE",
        "REFERENCE",
        "FIGURE",
        "CAPTION",
    }
    assert {status.value for status in StructuralStatus} == {
        "RECOVERED",
        "AMBIGUOUS",
        "UNSUPPORTED",
    }


def test_structural_node_normalizes_identity_and_inherits_source_privacy():
    source = _source(restricted=True, sensitivity="private")
    node = StructuralNode(
        " paragraph-1 ",
        StructuralKind.PARAGRAPH,
        _exact(source, 10, 20),
        1,
        parent_id=" doc ",
    )

    assert node.node_id == "paragraph-1"
    assert node.parent_id == "doc"
    assert node.source is source
    assert node.restricted is True
    assert node.sensitivity == "private"
    assert node.has_exact_span is True
    assert node.status is StructuralStatus.RECOVERED
    assert node.reason is None


def test_structural_node_requires_explicit_reason_for_ambiguous_or_unsupported():
    source = _source()
    ambiguous = StructuralNode(
        "a",
        StructuralKind.TABLE_REGION,
        SourceLocator(source, structural_locator="table:1:region:?"),
        1,
        parent_id="doc",
        status=StructuralStatus.AMBIGUOUS,
        reason=" merged cells cannot be distinguished ",
    )
    unsupported = StructuralNode(
        "u",
        StructuralKind.FIGURE,
        SourceLocator(source, structural_locator="figure:1"),
        2,
        parent_id="doc",
        status=StructuralStatus.UNSUPPORTED,
        reason=" image understanding is outside RC-2 ",
    )

    assert ambiguous.reason == "merged cells cannot be distinguished"
    assert unsupported.reason == "image understanding is outside RC-2"
    assert ambiguous.has_exact_span is False

    with pytest.raises(ValueError, match="reason"):
        StructuralNode(
            "bad",
            StructuralKind.TABLE,
            SourceLocator(source, structural_locator="table:bad"),
            3,
            parent_id="doc",
            status=StructuralStatus.AMBIGUOUS,
        )
    with pytest.raises(ValueError, match="reason"):
        StructuralNode(
            "bad",
            StructuralKind.TABLE,
            SourceLocator(source, structural_locator="table:bad"),
            3,
            parent_id="doc",
            status=StructuralStatus.UNSUPPORTED,
            reason=" ",
        )
    with pytest.raises(ValueError, match="RECOVERED"):
        StructuralNode(
            "bad",
            StructuralKind.PARAGRAPH,
            _exact(source, 1, 2),
            3,
            parent_id="doc",
            reason="should not exist",
        )


def test_structural_node_runtime_validation_is_fail_closed():
    source = _source()
    locator = _exact(source, 1, 2)

    with pytest.raises(ValueError, match="node_id"):
        StructuralNode(" ", StructuralKind.PARAGRAPH, locator, 1, parent_id="doc")
    with pytest.raises(ValueError, match="StructuralKind"):
        StructuralNode("n", "PARAGRAPH", locator, 1, parent_id="doc")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="SourceLocator"):
        StructuralNode("n", StructuralKind.PARAGRAPH, object(), 1, parent_id="doc")  # type: ignore[arg-type]
    for bad_order in (-1, True, "1"):
        with pytest.raises(ValueError, match="non-negative integer"):
            StructuralNode(
                "n",
                StructuralKind.PARAGRAPH,
                locator,
                bad_order,  # type: ignore[arg-type]
                parent_id="doc",
            )
    with pytest.raises(ValueError, match="parent_id"):
        StructuralNode("n", StructuralKind.PARAGRAPH, locator, 1, parent_id=" ")
    with pytest.raises(ValueError, match="parent itself"):
        StructuralNode("n", StructuralKind.PARAGRAPH, locator, 1, parent_id="n")
    with pytest.raises(ValueError, match="StructuralStatus"):
        StructuralNode(
            "n",
            StructuralKind.PARAGRAPH,
            locator,
            1,
            parent_id="doc",
            status="RECOVERED",  # type: ignore[arg-type]
        )


def test_map_requires_typed_source_iterable_nodes_and_single_document_root():
    source = _source()
    root = _root(source)

    with pytest.raises(ValueError, match="SourceVersion"):
        DocumentStructuralMap(object(), [root])  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="iterable"):
        DocumentStructuralMap(source, 1)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="at least one DOCUMENT"):
        DocumentStructuralMap(source, [])
    with pytest.raises(ValueError, match="StructuralNode"):
        DocumentStructuralMap(source, [object()])  # type: ignore[list-item]
    with pytest.raises(ValueError, match="exactly one DOCUMENT"):
        DocumentStructuralMap(
            source,
            [StructuralNode("p", StructuralKind.PARAGRAPH, _exact(source, 1, 2), 0)],
        )
    with pytest.raises(ValueError, match="exactly one DOCUMENT"):
        DocumentStructuralMap(
            source,
            [
                root,
                StructuralNode("doc2", StructuralKind.DOCUMENT, _exact(source, 0, 200), 1),
            ],
        )


def test_map_rejects_cross_version_duplicate_ids_and_duplicate_order():
    source = _source()
    other = _source("changed")
    root = _root(source)

    with pytest.raises(ValueError, match="map source version"):
        DocumentStructuralMap(
            source,
            [
                root,
                StructuralNode(
                    "p",
                    StructuralKind.PARAGRAPH,
                    _exact(other, 1, 2),
                    1,
                    parent_id="doc",
                ),
            ],
        )
    with pytest.raises(ValueError, match="duplicate structural node_id"):
        DocumentStructuralMap(
            source,
            [
                root,
                StructuralNode("doc", StructuralKind.PARAGRAPH, _exact(source, 1, 2), 1, "doc"),
            ],
        )
    with pytest.raises(ValueError, match="duplicate structural order"):
        DocumentStructuralMap(
            source,
            [
                root,
                StructuralNode("p", StructuralKind.PARAGRAPH, _exact(source, 1, 2), 0, "doc"),
            ],
        )


def test_map_rejects_invalid_parent_topology_cycle_and_parent_order():
    source = _source()
    root = _root(source)

    root_with_parent = StructuralNode(
        "doc",
        StructuralKind.DOCUMENT,
        _exact(source, 0, 200),
        0,
        parent_id="x",
    )
    with pytest.raises(ValueError, match="DOCUMENT node must not have a parent"):
        DocumentStructuralMap(
            source,
            [
                root_with_parent,
                StructuralNode("x", StructuralKind.PARAGRAPH, _exact(source, 1, 2), 1, "doc"),
            ],
        )

    with pytest.raises(ValueError, match="non-DOCUMENT node must have a parent"):
        DocumentStructuralMap(
            source,
            [root, StructuralNode("orphan", StructuralKind.PARAGRAPH, _exact(source, 1, 2), 1)],
        )
    with pytest.raises(ValueError, match="missing structural parent"):
        DocumentStructuralMap(
            source,
            [
                root,
                StructuralNode("orphan", StructuralKind.PARAGRAPH, _exact(source, 1, 2), 1, "missing"),
            ],
        )

    cycle_a = StructuralNode("a", StructuralKind.SECTION, _exact(source, 10, 100), 1, "b")
    cycle_b = StructuralNode("b", StructuralKind.SUBSECTION, _exact(source, 20, 90), 2, "a")
    with pytest.raises(ValueError, match="cycle"):
        DocumentStructuralMap(source, [root, cycle_a, cycle_b])

    parent = StructuralNode("parent", StructuralKind.SECTION, _exact(source, 10, 100), 3, "doc")
    child = StructuralNode("child", StructuralKind.PARAGRAPH, _exact(source, 20, 30), 2, "parent")
    with pytest.raises(ValueError, match="parent order"):
        DocumentStructuralMap(source, [root, child, parent])


def test_map_rejects_impossible_exact_span_containment_but_allows_structural_only_child():
    source = _source()
    root = _root(source, end=100)
    section = StructuralNode("section", StructuralKind.SECTION, _exact(source, 10, 50), 1, "doc")
    outside = StructuralNode("outside", StructuralKind.PARAGRAPH, _exact(source, 45, 60), 2, "section")

    with pytest.raises(ValueError, match="contained"):
        DocumentStructuralMap(source, [root, section, outside])

    structural_only = StructuralNode(
        "structural-only",
        StructuralKind.REFERENCE,
        SourceLocator(source, structural_locator="section:1:reference:unspanned"),
        2,
        "section",
        status=StructuralStatus.AMBIGUOUS,
        reason="offsets unavailable in source representation",
    )
    mapping = DocumentStructuralMap(source, [root, section, structural_only])
    assert mapping.get("structural-only") is structural_only


def test_map_orders_nodes_and_exposes_hierarchy_without_mutation():
    source = _source()
    root = _root(source)
    section = StructuralNode("section", StructuralKind.SECTION, _exact(source, 10, 150), 1, "doc")
    paragraph = StructuralNode("paragraph", StructuralKind.PARAGRAPH, _exact(source, 20, 40), 2, "section")
    quotation = StructuralNode("quote", StructuralKind.QUOTATION, _exact(source, 25, 35), 3, "paragraph")
    sibling = StructuralNode("sibling", StructuralKind.PARAGRAPH, _exact(source, 50, 70), 4, "section")

    mapping = DocumentStructuralMap(source, [sibling, quotation, root, paragraph, section])

    assert mapping.source is source
    assert tuple(node.node_id for node in mapping.nodes) == (
        "doc",
        "section",
        "paragraph",
        "quote",
        "sibling",
    )
    assert mapping.root is root
    assert mapping.get(" paragraph ") is paragraph
    assert mapping.children_of("section") == (paragraph, sibling)
    assert mapping.children_of("quote") == ()
    assert mapping.ancestors_of("quote") == (root, section, paragraph)
    assert mapping.ancestors_of("doc") == ()
    assert mapping.descendants_of("section") == (paragraph, quotation, sibling)
    assert mapping.descendants_of("quote") == ()
    assert mapping.iter_kind(StructuralKind.PARAGRAPH) == (paragraph, sibling)

    snapshot = mapping.nodes
    snapshot += (paragraph,)
    assert len(mapping.nodes) == 5

    with pytest.raises(ValueError, match="node_id"):
        mapping.get(" ")
    with pytest.raises(KeyError):
        mapping.get("missing")
    with pytest.raises(ValueError, match="StructuralKind"):
        mapping.iter_kind("PARAGRAPH")  # type: ignore[arg-type]


def test_map_can_represent_every_rc0_kind_and_reports_unresolved_structure_without_scores():
    source = _source()
    root = _root(source)
    nodes = [root]
    offset = 1
    for order, kind in enumerate((kind for kind in StructuralKind if kind is not StructuralKind.DOCUMENT), 1):
        status = StructuralStatus.RECOVERED
        reason = None
        if kind is StructuralKind.FIGURE:
            status = StructuralStatus.UNSUPPORTED
            reason = "figure pixels are not interpreted by RC-2"
        elif kind is StructuralKind.TABLE_REGION:
            status = StructuralStatus.AMBIGUOUS
            reason = "table region boundary is ambiguous"
        locator = _exact(source, offset, offset + 1)
        nodes.append(
            StructuralNode(
                f"node-{kind.value.lower()}",
                kind,
                locator,
                order,
                "doc",
                status=status,
                reason=reason,
            )
        )
        offset += 2

    mapping = DocumentStructuralMap(source, reversed(nodes))
    telemetry = mapping.telemetry()

    assert {node.kind for node in mapping.nodes} == set(StructuralKind)
    assert telemetry.total_nodes == len(StructuralKind)
    assert telemetry.exact_span_nodes == len(StructuralKind)
    assert telemetry.unresolved_nodes == 2
    assert telemetry.has_unresolved_structure is True
    assert telemetry.status_counts[StructuralStatus.AMBIGUOUS] == 1
    assert telemetry.status_counts[StructuralStatus.UNSUPPORTED] == 1
    assert all(telemetry.kind_counts[kind] == 1 for kind in StructuralKind)
    assert {node.status for node in mapping.unresolved_nodes} == {
        StructuralStatus.AMBIGUOUS,
        StructuralStatus.UNSUPPORTED,
    }
    assert not hasattr(telemetry, "comprehension_percent")
    assert not hasattr(telemetry, "truth_score")

    clean = DocumentStructuralMap(source, [_root(source)])
    clean_telemetry = clean.telemetry()
    assert clean_telemetry.unresolved_nodes == 0
    assert clean_telemetry.has_unresolved_structure is False


def test_structural_map_retains_no_source_body_and_exposes_no_epistemic_authority_fields():
    text = "SECRET SOURCE BODY " * 5
    source = _source(text)
    mapping = DocumentStructuralMap(source, [_root(source, end=len(text))])

    assert "source_text" not in {field.name for field in dataclasses.fields(StructuralNode)}
    assert "source_body" not in {field.name for field in dataclasses.fields(StructuralNode)}
    assert text not in repr(mapping.nodes)

    field_names = {field.name for field in dataclasses.fields(StructuralNode)}
    assert field_names.isdisjoint(
        {"truth_status", "confidence", "canon", "esm", "importance", "belief", "authority"}
    )


def test_reader_structure_imports_only_rc1_source_primitives_from_core():
    source = inspect.getsource(reader_structure)
    tree = ast.parse(source)
    core_imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            core_imports.update(alias.name for alias in node.names if alias.name.startswith("core."))
        elif isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("core."):
            core_imports.add(node.module)

    assert core_imports == {"core.reader_core"}
    imported_names = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module == "core.reader_core"
        for alias in node.names
    }
    assert imported_names == {"SourceLocator", "SourceVersion"}


def test_root_runtime_guard_fails_visibly_if_internal_invariant_is_corrupted():
    source = _source()
    mapping = DocumentStructuralMap(source, [_root(source)])
    mapping._nodes = ()  # type: ignore[attr-defined]

    with pytest.raises(RuntimeError, match="lost its DOCUMENT root"):
        _ = mapping.root
