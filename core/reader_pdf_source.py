"""Bounded local PDF preparation for the Crystal Reader product bridge.

This module is read-side only. It binds Reader source identity to the exact PDF bytes,
extracts page text through the optional low-level ``pypdf`` dependency, and represents
page locations with replayable structural locators. It never imports the WP4 knowledge-
ingest adapters and adds no evidence admission, TruthGate, Guardian, memory, Canon,
provider, retrieval, network, persistence, or background-worker authority.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from core.reader_core import ReaderSession, SourceLocator, SourceVersion
from core.reader_product_bridge import ReaderProductBridge, ReaderProductResult, RegionExecutor
from core.reader_structure import DocumentStructuralMap, StructuralKind, StructuralNode

DEFAULT_MAX_PDF_BYTES = 20_000_000
DEFAULT_MAX_PDF_PAGES = 512
DEFAULT_MAX_EXTRACTED_CHARS = 2_000_000


def _positive_limit(value: int, field_name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{field_name} must be a positive integer")
    return value


def _load_pdf_reader(path: Path):
    try:
        from pypdf import PdfReader
    except ImportError as exc:  # pragma: no cover - exercised through import blocking
        raise RuntimeError("PDF Reader support requires the optional 'pdf' dependency") from exc
    return PdfReader(str(path))


@dataclass(frozen=True)
class ReaderPdfSource:
    """One exact local PDF prepared for the existing bounded Reader bridge."""

    path: str
    source: SourceVersion
    page_texts: tuple[str, ...]
    structure: DocumentStructuralMap
    session: ReaderSession
    bridge: ReaderProductBridge

    def text_for(self, node: StructuralNode) -> str:
        """Replay extracted text for a page node from this exact PDF version."""

        if not isinstance(node, StructuralNode):
            raise ValueError("node must be a StructuralNode")
        if not self.source.same_version(node.source):
            raise ValueError("node belongs to a different source version")
        locator = node.locator.structural_locator
        if node.kind is StructuralKind.DOCUMENT and locator == "pdf:document":
            return "\n\n".join(self.page_texts)
        if node.kind is not StructuralKind.SECTION or locator is None:
            raise ValueError("PDF Reader text replay requires a page SECTION locator")
        prefix = "pdf:page:"
        if not locator.startswith(prefix):
            raise ValueError("PDF Reader text replay requires a pdf:page:N locator")
        try:
            page_number = int(locator[len(prefix) :])
        except ValueError as exc:
            raise ValueError("PDF page locator must end with an integer page number") from exc
        if page_number < 1 or page_number > len(self.page_texts):
            raise ValueError("PDF page locator is outside the prepared page range")
        return self.page_texts[page_number - 1]

    def run(self, executor: RegionExecutor) -> ReaderProductResult:
        """Execute the existing ReaderProductBridge over the prepared PDF pages."""

        return self.bridge.run(executor)


def load_reader_pdf(
    path: str | Path,
    *,
    objective: str,
    document_id: Optional[str] = None,
    session_id: Optional[str] = None,
    restricted: bool = False,
    sensitivity: Optional[str] = None,
    max_pdf_bytes: int = DEFAULT_MAX_PDF_BYTES,
    max_pages: int = DEFAULT_MAX_PDF_PAGES,
    max_extracted_chars: int = DEFAULT_MAX_EXTRACTED_CHARS,
) -> ReaderPdfSource:
    """Prepare one bounded local PDF for ReaderProductBridge.

    Boundedness covers local PDF bytes, page count, and total extracted characters only.
    It does not claim a token/time/provider-cost or caller-executor budget.
    """

    byte_limit = _positive_limit(max_pdf_bytes, "max_pdf_bytes")
    page_limit = _positive_limit(max_pages, "max_pages")
    char_limit = _positive_limit(max_extracted_chars, "max_extracted_chars")

    resolved = Path(path).expanduser().resolve()
    if not resolved.exists():
        raise FileNotFoundError(str(resolved))
    if not resolved.is_file():
        raise ValueError("Reader PDF source path must be a regular file")
    if resolved.suffix.lower() != ".pdf":
        raise ValueError("Reader PDF v0.1 supports only .pdf")
    if resolved.stat().st_size > byte_limit:
        raise ValueError("Reader PDF source exceeds max_pdf_bytes")

    with resolved.open("rb") as handle:
        raw = handle.read(byte_limit + 1)
    if len(raw) > byte_limit:
        raise ValueError("Reader PDF source exceeds max_pdf_bytes")
    if not raw.startswith(b"%PDF-"):
        raise ValueError("Reader PDF source is not a PDF file")

    source = SourceVersion(
        document_id=document_id if document_id is not None else resolved.name,
        source_uri=resolved.as_uri(),
        source_sha256=hashlib.sha256(raw).hexdigest(),
        restricted=restricted,
        sensitivity=sensitivity,
    )

    try:
        reader = _load_pdf_reader(resolved)
    except Exception as exc:
        if isinstance(exc, RuntimeError):
            raise
        raise ValueError("Reader PDF parser could not open the source") from exc

    if getattr(reader, "is_encrypted", False):
        raise ValueError("Encrypted PDFs are not supported by Reader PDF v0.1")
    pages = tuple(reader.pages)
    if not pages:
        raise ValueError("Reader PDF source must contain at least one page")
    if len(pages) > page_limit:
        raise ValueError("Reader PDF source exceeds max_pages")

    extracted: list[str] = []
    total_chars = 0
    for page in pages:
        try:
            text = page.extract_text()
        except Exception as exc:
            raise ValueError("Reader PDF page text extraction failed") from exc
        text = text or ""
        total_chars += len(text)
        if total_chars > char_limit:
            raise ValueError("Reader PDF extraction exceeds max_extracted_chars")
        extracted.append(text)

    if not any(text.strip() for text in extracted):
        raise ValueError("Reader PDF source contains no extractable text")

    nodes: list[StructuralNode] = [
        StructuralNode(
            "document",
            StructuralKind.DOCUMENT,
            SourceLocator(source, structural_locator="pdf:document"),
            0,
        )
    ]
    for index, text in enumerate(extracted, start=1):
        nodes.append(
            StructuralNode(
                f"page-{index:04d}",
                StructuralKind.SECTION,
                SourceLocator(
                    source,
                    structural_locator=f"pdf:page:{index}",
                    section=f"page:{index}",
                ),
                index,
                "document",
            )
        )

    structure = DocumentStructuralMap(source, nodes)
    sid = session_id if session_id is not None else f"reader-pdf-{source.source_sha256[:16]}"
    session = ReaderSession(sid, source, objective)
    bridge = ReaderProductBridge(session, structure)
    return ReaderPdfSource(
        path=str(resolved),
        source=source,
        page_texts=tuple(extracted),
        structure=structure,
        session=session,
        bridge=bridge,
    )


__all__ = [
    "DEFAULT_MAX_EXTRACTED_CHARS",
    "DEFAULT_MAX_PDF_BYTES",
    "DEFAULT_MAX_PDF_PAGES",
    "ReaderPdfSource",
    "load_reader_pdf",
]
