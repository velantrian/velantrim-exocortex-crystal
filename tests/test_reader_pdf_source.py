from __future__ import annotations

import ast
import hashlib
import inspect
from pathlib import Path
from types import SimpleNamespace

import pytest

import core.reader_pdf_source as reader_pdf_source
from core.reader_core import CoverageState, SourceLocator, SourceVersion
from core.reader_product_bridge import ReaderProductStatus, RegionReadResult
from core.reader_structure import StructuralKind, StructuralNode


class _Page:
    def __init__(self, text="", error=None):
        self.text = text
        self.error = error

    def extract_text(self):
        if self.error is not None:
            raise self.error
        return self.text


def _pdf(tmp_path: Path, payload: bytes = b"%PDF-1.7\nfixture") -> Path:
    path = tmp_path / "book.pdf"
    path.write_bytes(payload)
    return path


def _reader(monkeypatch, pages, *, encrypted=False):
    fake = SimpleNamespace(pages=list(pages), is_encrypted=encrypted)
    monkeypatch.setattr(reader_pdf_source, "_load_pdf_reader", lambda path: fake)
    return fake


def test_pdf_preparation_binds_binary_hash_pages_and_existing_bridge(tmp_path, monkeypatch):
    path = _pdf(tmp_path)
    _reader(monkeypatch, [_Page("Alpha page"), _Page("Beta page")])

    prepared = reader_pdf_source.load_reader_pdf(path, objective="read book")

    assert prepared.path == str(path.resolve())
    assert prepared.source.document_id == "book.pdf"
    assert prepared.source.source_uri == path.resolve().as_uri()
    assert prepared.source.source_sha256 == hashlib.sha256(path.read_bytes()).hexdigest()
    assert prepared.session.source.same_version(prepared.source)
    assert prepared.session.objective == "read book"
    assert prepared.session.session_id.startswith("reader-pdf-")
    assert [node.kind for node in prepared.structure.nodes] == [
        StructuralKind.DOCUMENT,
        StructuralKind.SECTION,
        StructuralKind.SECTION,
    ]
    assert [node.locator.structural_locator for node in prepared.structure.nodes] == [
        "pdf:document",
        "pdf:page:1",
        "pdf:page:2",
    ]
    assert prepared.text_for(prepared.structure.root) == "Alpha page\n\nBeta page"
    assert [prepared.text_for(node) for node in prepared.structure.nodes[1:]] == [
        "Alpha page",
        "Beta page",
    ]

    seen = []

    def executor(kind, node, before):
        assert before is CoverageState.UNREAD
        seen.append(prepared.text_for(node))
        return RegionReadResult(CoverageState.PROCESSED)

    result = prepared.run(executor)
    assert result.status is ReaderProductStatus.COMPLETE
    assert seen == ["Alpha page", "Beta page"]


def test_pdf_supports_explicit_identity_and_source_metadata(tmp_path, monkeypatch):
    path = _pdf(tmp_path)
    _reader(monkeypatch, [_Page("text")])
    prepared = reader_pdf_source.load_reader_pdf(
        path,
        objective="review",
        document_id="pdf-custom",
        session_id="session-custom",
        restricted=True,
        sensitivity="private",
    )
    assert prepared.source.document_id == "pdf-custom"
    assert prepared.session.session_id == "session-custom"
    assert prepared.source.restricted is True
    assert prepared.source.sensitivity == "private"


@pytest.mark.parametrize("field,value", [("max_pdf_bytes", 0), ("max_pages", -1), ("max_extracted_chars", True), ("max_pages", 1.5)])
def test_invalid_limits_fail_closed(tmp_path, monkeypatch, field, value):
    path = _pdf(tmp_path)
    _reader(monkeypatch, [_Page("text")])
    kwargs = {field: value}
    with pytest.raises(ValueError, match="positive integer"):
        reader_pdf_source.load_reader_pdf(path, objective="read", **kwargs)


def test_missing_directory_extension_and_signature_fail_closed(tmp_path):
    with pytest.raises(FileNotFoundError):
        reader_pdf_source.load_reader_pdf(tmp_path / "missing.pdf", objective="read")
    with pytest.raises(ValueError, match="regular file"):
        reader_pdf_source.load_reader_pdf(tmp_path, objective="read")
    txt = tmp_path / "not-pdf.txt"
    txt.write_bytes(b"%PDF-1.7")
    with pytest.raises(ValueError, match="only .pdf"):
        reader_pdf_source.load_reader_pdf(txt, objective="read")
    bad = _pdf(tmp_path, b"not pdf")
    with pytest.raises(ValueError, match="not a PDF"):
        reader_pdf_source.load_reader_pdf(bad, objective="read")


def test_pdf_byte_ceiling_is_checked_before_and_during_read(tmp_path, monkeypatch):
    path = _pdf(tmp_path, b"%PDF-123456")
    with pytest.raises(ValueError, match="max_pdf_bytes"):
        reader_pdf_source.load_reader_pdf(path, objective="read", max_pdf_bytes=5)

    path.write_bytes(b"%PDF-")
    original_open = Path.open
    target = path.resolve()

    class _Growing:
        def __enter__(self):
            return self
        def __exit__(self, *args):
            return False
        def read(self, size=-1):
            return b"%PDF-123456"

    def fake_open(self, *args, **kwargs):
        if self == target:
            return _Growing()
        return original_open(self, *args, **kwargs)

    monkeypatch.setattr(Path, "open", fake_open)
    with pytest.raises(ValueError, match="max_pdf_bytes"):
        reader_pdf_source.load_reader_pdf(path, objective="read", max_pdf_bytes=6)


def test_parser_encryption_page_and_character_failures_are_closed(tmp_path, monkeypatch):
    path = _pdf(tmp_path)
    monkeypatch.setattr(reader_pdf_source, "_load_pdf_reader", lambda path: (_ for _ in ()).throw(Exception("bad")))
    with pytest.raises(ValueError, match="could not open"):
        reader_pdf_source.load_reader_pdf(path, objective="read")

    _reader(monkeypatch, [_Page("secret")], encrypted=True)
    with pytest.raises(ValueError, match="Encrypted PDFs"):
        reader_pdf_source.load_reader_pdf(path, objective="read")

    _reader(monkeypatch, [])
    with pytest.raises(ValueError, match="at least one page"):
        reader_pdf_source.load_reader_pdf(path, objective="read")

    _reader(monkeypatch, [_Page("a"), _Page("b")])
    with pytest.raises(ValueError, match="max_pages"):
        reader_pdf_source.load_reader_pdf(path, objective="read", max_pages=1)

    _reader(monkeypatch, [_Page(error=RuntimeError("extract"))])
    with pytest.raises(ValueError, match="extraction failed"):
        reader_pdf_source.load_reader_pdf(path, objective="read")

    _reader(monkeypatch, [_Page("abcdef")])
    with pytest.raises(ValueError, match="max_extracted_chars"):
        reader_pdf_source.load_reader_pdf(path, objective="read", max_extracted_chars=3)

    _reader(monkeypatch, [_Page(None), _Page(" \n")])
    with pytest.raises(ValueError, match="no extractable text"):
        reader_pdf_source.load_reader_pdf(path, objective="read")


def test_text_for_rejects_wrong_nodes_and_locators(tmp_path, monkeypatch):
    path = _pdf(tmp_path)
    _reader(monkeypatch, [_Page("one")])
    prepared = reader_pdf_source.load_reader_pdf(path, objective="read")

    with pytest.raises(ValueError, match="StructuralNode"):
        prepared.text_for(object())

    other = SourceVersion("other", "file:///other.pdf", "0" * 64)
    other_node = StructuralNode("other", StructuralKind.SECTION, SourceLocator(other, structural_locator="pdf:page:1"), 0)
    with pytest.raises(ValueError, match="different source"):
        prepared.text_for(other_node)

    bad_kind = StructuralNode("paragraph", StructuralKind.PARAGRAPH, SourceLocator(prepared.source, structural_locator="pdf:page:1"), 0)
    with pytest.raises(ValueError, match="page SECTION"):
        prepared.text_for(bad_kind)

    bad_locator = StructuralNode("bad", StructuralKind.SECTION, SourceLocator(prepared.source, structural_locator="page:1"), 0)
    with pytest.raises(ValueError, match="pdf:page"):
        prepared.text_for(bad_locator)

    non_integer = StructuralNode("bad-int", StructuralKind.SECTION, SourceLocator(prepared.source, structural_locator="pdf:page:x"), 0)
    with pytest.raises(ValueError, match="integer"):
        prepared.text_for(non_integer)

    outside = StructuralNode("outside", StructuralKind.SECTION, SourceLocator(prepared.source, structural_locator="pdf:page:2"), 0)
    with pytest.raises(ValueError, match="outside"):
        prepared.text_for(outside)


def test_reader_pdf_source_has_no_ingest_authority_or_provider_imports():
    tree = ast.parse(inspect.getsource(reader_pdf_source))
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module)
    forbidden = {
        "core.adapters", "core.ingest", "core.truth_gate", "core.guardian",
        "core.memory", "core.pipeline", "core.embedding", "core.llm_router", "core.remote_egress",
    }
    assert imported.isdisjoint(forbidden)
