"""Local TXT/Markdown source preparation for the Crystal Reader product bridge.

This module is read-side only. It converts one bounded UTF-8 local file into the
existing RC-1 SourceVersion, RC-2 DocumentStructuralMap, ReaderSession, and
ReaderProductBridge contracts. It does not call knowledge ingest, TruthGate,
Guardian, memory, Canon, a model/provider, retrieval, or any network surface.

v0.1 deliberately supports only .txt and .md. PDF/EPUB/DOCX parsing requires a
separate reviewed extension rather than reusing knowledge-ingest adapters as
Reader authority.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from core.reader_core import ReaderSession, SourceLocator, SourceVersion
from core.reader_product_bridge import ReaderProductBridge, ReaderProductResult, RegionExecutor
from core.reader_structure import DocumentStructuralMap, StructuralKind, StructuralNode

SUPPORTED_READER_FILE_SUFFIXES = frozenset({".txt", ".md"})
DEFAULT_MAX_SOURCE_BYTES = 2_000_000
_BLOCK = re.compile(r"\S(?:.*?\S)?(?=\n[ \t]*\n|\Z)", re.DOTALL)


def _positive_limit(value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError("max_source_bytes must be a positive integer")
    return value


def _paragraph_spans(text: str) -> tuple[tuple[int, int], ...]:
    return tuple((match.start(), match.end()) for match in _BLOCK.finditer(text))


@dataclass(frozen=True)
class ReaderFileSource:
    """One local source prepared for the existing bounded Reader bridge.

    ``text`` is retained only in this foreground read-side object so a caller-supplied
    executor can replay exact structural spans. Nothing here persists or admits it.
    """

    path: str
    text: str
    source: SourceVersion
    structure: DocumentStructuralMap
    session: ReaderSession
    bridge: ReaderProductBridge

    def text_for(self, node: StructuralNode) -> str:
        """Return the exact source substring for one node from this prepared source."""

        if not isinstance(node, StructuralNode):
            raise ValueError("node must be a StructuralNode")
        if not self.source.same_version(node.source):
            raise ValueError("node belongs to a different source version")
        start = node.locator.span_start
        end = node.locator.span_end
        if start is None or end is None:
            raise ValueError("Reader file nodes require exact source spans")
        return self.text[start:end]

    def run(self, executor: RegionExecutor) -> ReaderProductResult:
        """Execute the existing ReaderProductBridge over this prepared file."""

        return self.bridge.run(executor)


def load_reader_file(
    path: str | Path,
    *,
    objective: str,
    document_id: Optional[str] = None,
    session_id: Optional[str] = None,
    restricted: bool = False,
    sensitivity: Optional[str] = None,
    max_source_bytes: int = DEFAULT_MAX_SOURCE_BYTES,
) -> ReaderFileSource:
    """Prepare one bounded local UTF-8 TXT/Markdown file for ReaderProductBridge.

    The byte ceiling bounds only local file loading. It does not claim a model/token/time
    budget for the caller-supplied Reader executor.
    """

    limit = _positive_limit(max_source_bytes)
    resolved = Path(path).expanduser().resolve()
    if not resolved.exists():
        raise FileNotFoundError(str(resolved))
    if not resolved.is_file():
        raise ValueError("Reader source path must be a regular file")
    suffix = resolved.suffix.lower()
    if suffix not in SUPPORTED_READER_FILE_SUFFIXES:
        raise ValueError("Reader file v0.1 supports only .txt and .md")
    if resolved.stat().st_size > limit:
        raise ValueError("Reader source exceeds max_source_bytes")

    with resolved.open("rb") as handle:
        raw = handle.read(limit + 1)
    if len(raw) > limit:
        raise ValueError("Reader source exceeds max_source_bytes")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Reader file v0.1 requires UTF-8 text") from exc
    if not text.strip():
        raise ValueError("Reader source must contain non-whitespace text")

    doc_id = document_id if document_id is not None else resolved.name
    source = SourceVersion.from_text(
        doc_id,
        resolved.as_uri(),
        text,
        restricted=restricted,
        sensitivity=sensitivity,
    )
    root_locator = SourceLocator(source, span_start=0, span_end=len(text))
    nodes: list[StructuralNode] = [
        StructuralNode("document", StructuralKind.DOCUMENT, root_locator, 0)
    ]
    for index, (start, end) in enumerate(_paragraph_spans(text), start=1):
        nodes.append(
            StructuralNode(
                f"paragraph-{index:04d}",
                StructuralKind.PARAGRAPH,
                SourceLocator(source, span_start=start, span_end=end),
                index,
                "document",
            )
        )

    structure = DocumentStructuralMap(source, nodes)
    sid = session_id if session_id is not None else f"reader-file-{source.source_sha256[:16]}"
    session = ReaderSession(sid, source, objective)
    bridge = ReaderProductBridge(session, structure)
    return ReaderFileSource(
        path=str(resolved),
        text=text,
        source=source,
        structure=structure,
        session=session,
        bridge=bridge,
    )


__all__ = [
    "DEFAULT_MAX_SOURCE_BYTES",
    "SUPPORTED_READER_FILE_SUFFIXES",
    "ReaderFileSource",
    "load_reader_file",
]
