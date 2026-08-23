from __future__ import annotations

import ast
import inspect
from pathlib import Path
from types import SimpleNamespace

import pytest

import core.reader_file_source as reader_file_source
from core.reader_core import CoverageState, SourceLocator, SourceVersion
from core.reader_product_bridge import ReaderProductStatus, RegionReadResult
from core.reader_structure import StructuralKind, StructuralNode


def test_txt_preparation_builds_exact_paragraph_map_and_runs_bridge(tmp_path: Path):
    path = tmp_path / "book.txt"
    text = "Alpha one.\nStill alpha.\n\nBeta two."
    path.write_text(text, encoding="utf-8")

    prepared = reader_file_source.load_reader_file(path, objective="understand the book")

    assert prepared.path == str(path.resolve())
    assert prepared.text == text
    assert prepared.source.document_id == "book.txt"
    assert prepared.source.source_uri == path.resolve().as_uri()
    assert prepared.structure.source.same_version(prepared.source)
    assert prepared.session.source.same_version(prepared.source)
    assert prepared.session.objective == "understand the book"
    assert prepared.session.session_id.startswith("reader-file-")
    assert [node.kind for node in prepared.structure.nodes] == [
        StructuralKind.DOCUMENT,
        StructuralKind.PARAGRAPH,
        StructuralKind.PARAGRAPH,
    ]
    assert prepared.text_for(prepared.structure.root) == text
    paragraphs = prepared.structure.iter_kind(StructuralKind.PARAGRAPH)
    assert [prepared.text_for(node) for node in paragraphs] == [
        "Alpha one.\nStill alpha.",
        "Beta two.",
    ]

    seen: list[str] = []

    def executor(kind, node, before):
        assert before is CoverageState.UNREAD
        seen.append(prepared.text_for(node))
        return RegionReadResult(CoverageState.PROCESSED)

    result = prepared.run(executor)

    assert result.status is ReaderProductStatus.COMPLETE
    assert seen == ["Alpha one.\nStill alpha.", "Beta two."]


def test_markdown_supports_explicit_identity_and_source_metadata(tmp_path: Path):
    path = tmp_path / "notes.MD"
    path.write_text("# Heading\n\nBody text.", encoding="utf-8")

    prepared = reader_file_source.load_reader_file(
        path,
        objective="review notes",
        document_id="doc-custom",
        session_id="session-custom",
        restricted=True,
        sensitivity="private",
    )

    assert prepared.source.document_id == "doc-custom"
    assert prepared.session.session_id == "session-custom"
    assert prepared.source.restricted is True
    assert prepared.source.sensitivity == "private"
    assert [prepared.text_for(node) for node in prepared.structure.nodes[1:]] == [
        "# Heading",
        "Body text.",
    ]


@pytest.mark.parametrize("limit", [0, -1, True, 1.5])
def test_invalid_source_limit_is_rejected(tmp_path: Path, limit):
    path = tmp_path / "a.txt"
    path.write_text("content", encoding="utf-8")

    with pytest.raises(ValueError, match="positive integer"):
        reader_file_source.load_reader_file(
            path,
            objective="read",
            max_source_bytes=limit,
        )


def test_missing_directory_and_unsupported_sources_fail_closed(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        reader_file_source.load_reader_file(tmp_path / "missing.txt", objective="read")

    with pytest.raises(ValueError, match="regular file"):
        reader_file_source.load_reader_file(tmp_path, objective="read")

    unsupported = tmp_path / "book.pdf"
    unsupported.write_bytes(b"not a real pdf")
    with pytest.raises(ValueError, match="only .txt and .md"):
        reader_file_source.load_reader_file(unsupported, objective="read")


def test_size_limit_checks_before_and_after_read(tmp_path: Path, monkeypatch):
    path = tmp_path / "large.txt"
    path.write_text("abcdef", encoding="utf-8")

    with pytest.raises(ValueError, match="exceeds max_source_bytes"):
        reader_file_source.load_reader_file(path, objective="read", max_source_bytes=3)

    original_stat = Path.stat
    target = path.resolve()

    def fake_stat(self, *args, **kwargs):
        if self == target:
            return SimpleNamespace(st_size=1)
        return original_stat(self, *args, **kwargs)

    monkeypatch.setattr(Path, "stat", fake_stat)
    with pytest.raises(ValueError, match="exceeds max_source_bytes"):
        reader_file_source.load_reader_file(path, objective="read", max_source_bytes=3)


def test_invalid_utf8_and_whitespace_only_sources_are_rejected(tmp_path: Path):
    binary = tmp_path / "binary.txt"
    binary.write_bytes(b"\xff\xfe")
    with pytest.raises(ValueError, match="requires UTF-8"):
        reader_file_source.load_reader_file(binary, objective="read")

    blank = tmp_path / "blank.md"
    blank.write_text(" \n\t\n", encoding="utf-8")
    with pytest.raises(ValueError, match="non-whitespace"):
        reader_file_source.load_reader_file(blank, objective="read")


def test_text_for_rejects_wrong_type_version_and_non_exact_locator(tmp_path: Path):
    path = tmp_path / "one.txt"
    path.write_text("one paragraph", encoding="utf-8")
    prepared = reader_file_source.load_reader_file(path, objective="read")

    with pytest.raises(ValueError, match="StructuralNode"):
        prepared.text_for(object())  # type: ignore[arg-type]

    other = SourceVersion.from_text("other", "file:///other.txt", "other")
    other_node = StructuralNode(
        "other",
        StructuralKind.PARAGRAPH,
        SourceLocator(other, span_start=0, span_end=5),
        0,
    )
    with pytest.raises(ValueError, match="different source version"):
        prepared.text_for(other_node)

    structural_only = StructuralNode(
        "structural-only",
        StructuralKind.PARAGRAPH,
        SourceLocator(prepared.source, structural_locator="paragraph:1"),
        0,
    )
    with pytest.raises(ValueError, match="exact source spans"):
        prepared.text_for(structural_only)


def test_reader_file_source_has_no_ingest_authority_or_provider_imports():
    tree = ast.parse(inspect.getsource(reader_file_source))
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module)

    forbidden = {
        "core.adapters",
        "core.ingest",
        "core.truth_gate",
        "core.guardian",
        "core.memory",
        "core.pipeline",
        "core.embedding",
        "core.llm_router",
        "core.remote_egress",
    }
    assert imported.isdisjoint(forbidden)
