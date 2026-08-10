"""Source-version-bound structural document map for Reader Core RC-2.

RC-2 represents structure that a caller has already recovered. It is deliberately not a
parser, chunker, OCR/layout engine, model integration, storage layer, or truth-admission
path. Structural position is reader metadata only and carries no epistemic authority.

The map reuses RC-1 source identity and replayable locator primitives. Source body text is
not stored by this module.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Iterable, Optional

from core.reader_core import SourceLocator, SourceVersion


class StructuralKind(str, Enum):
    """Structural categories required by the RC-0 architecture contract."""

    DOCUMENT = "DOCUMENT"
    SECTION = "SECTION"
    SUBSECTION = "SUBSECTION"
    PARAGRAPH = "PARAGRAPH"
    DIALOGUE_TURN = "DIALOGUE_TURN"
    LIST = "LIST"
    LIST_ITEM = "LIST_ITEM"
    TABLE = "TABLE"
    TABLE_REGION = "TABLE_REGION"
    CODE_BLOCK = "CODE_BLOCK"
    QUOTATION = "QUOTATION"
    FOOTNOTE = "FOOTNOTE"
    ENDNOTE = "ENDNOTE"
    REFERENCE = "REFERENCE"
    FIGURE = "FIGURE"
    CAPTION = "CAPTION"


class StructuralStatus(str, Enum):
    """Whether a structural boundary is usable, ambiguous, or unsupported."""

    RECOVERED = "RECOVERED"
    AMBIGUOUS = "AMBIGUOUS"
    UNSUPPORTED = "UNSUPPORTED"


def _required_text(value: str, field_name: str) -> str:
    value = (value or "").strip()
    if not value:
        raise ValueError(f"{field_name} must be non-empty")
    return value


@dataclass(frozen=True)
class StructuralNode:
    """One source-linked structural region within an exact document version."""

    node_id: str
    kind: StructuralKind
    locator: SourceLocator
    order: int
    parent_id: Optional[str] = None
    status: StructuralStatus = StructuralStatus.RECOVERED
    reason: Optional[str] = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "node_id", _required_text(self.node_id, "node_id"))
        if not isinstance(self.kind, StructuralKind):
            raise ValueError("kind must be a StructuralKind")
        if not isinstance(self.locator, SourceLocator):
            raise ValueError("locator must be a SourceLocator")
        if isinstance(self.order, bool) or not isinstance(self.order, int) or self.order < 0:
            raise ValueError("order must be a non-negative integer")
        if self.parent_id is not None:
            parent_id = _required_text(self.parent_id, "parent_id")
            if parent_id == self.node_id:
                raise ValueError("a structural node cannot parent itself")
            object.__setattr__(self, "parent_id", parent_id)
        if not isinstance(self.status, StructuralStatus):
            raise ValueError("status must be a StructuralStatus")
        if self.status is StructuralStatus.RECOVERED:
            if self.reason is not None:
                raise ValueError("RECOVERED structure must not carry an ambiguity reason")
        else:
            object.__setattr__(self, "reason", _required_text(self.reason or "", "reason"))

    @property
    def source(self) -> SourceVersion:
        return self.locator.source

    @property
    def restricted(self) -> bool:
        return self.locator.source.restricted

    @property
    def sensitivity(self) -> Optional[str]:
        return self.locator.source.sensitivity

    @property
    def has_exact_span(self) -> bool:
        return self.locator.has_exact_span


@dataclass(frozen=True)
class StructuralMapTelemetry:
    """Structural counts only; never a comprehension or truth score."""

    total_nodes: int
    exact_span_nodes: int
    unresolved_nodes: int
    kind_counts: Dict[StructuralKind, int]
    status_counts: Dict[StructuralStatus, int]

    @property
    def has_unresolved_structure(self) -> bool:
        return self.unresolved_nodes > 0


class DocumentStructuralMap:
    """Validated, immutable-view structural map for one source version."""

    __slots__ = ("_source", "_nodes", "_by_id", "_children")

    def __init__(self, source: SourceVersion, nodes: Iterable[StructuralNode]) -> None:
        if not isinstance(source, SourceVersion):
            raise ValueError("source must be a SourceVersion")
        try:
            declared = tuple(nodes)
        except TypeError as exc:
            raise ValueError("nodes must be an iterable of StructuralNode values") from exc
        if not declared:
            raise ValueError("a structural map requires at least one DOCUMENT node")
        for node in declared:
            if not isinstance(node, StructuralNode):
                raise ValueError("nodes must contain StructuralNode values")
            if not source.same_version(node.source):
                raise ValueError("all structural nodes must use the map source version")

        by_id: Dict[str, StructuralNode] = {}
        orders: set[int] = set()
        for node in declared:
            if node.node_id in by_id:
                raise ValueError(f"duplicate structural node_id: {node.node_id}")
            if node.order in orders:
                raise ValueError(f"duplicate structural order: {node.order}")
            by_id[node.node_id] = node
            orders.add(node.order)

        roots = [node for node in declared if node.kind is StructuralKind.DOCUMENT]
        if len(roots) != 1:
            raise ValueError("a structural map requires exactly one DOCUMENT node")
        root = roots[0]
        if root.parent_id is not None:
            raise ValueError("the DOCUMENT node must not have a parent")
        for node in declared:
            if node is root:
                continue
            if node.parent_id is None:
                raise ValueError("every non-DOCUMENT node must have a parent")
            if node.parent_id not in by_id:
                raise ValueError(f"missing structural parent: {node.parent_id}")

        self._validate_cycles(by_id)
        self._validate_parent_order_and_spans(by_id, root)

        ordered = tuple(sorted(declared, key=lambda node: node.order))
        children: Dict[str, list[StructuralNode]] = {node.node_id: [] for node in ordered}
        for node in ordered:
            if node.parent_id is not None:
                children[node.parent_id].append(node)

        self._source = source
        self._nodes = ordered
        self._by_id = by_id
        self._children = {key: tuple(value) for key, value in children.items()}

    @staticmethod
    def _validate_cycles(by_id: Dict[str, StructuralNode]) -> None:
        for node in by_id.values():
            seen: set[str] = set()
            current = node
            while current.parent_id is not None:
                if current.node_id in seen:
                    raise ValueError("structural parent cycle detected")
                seen.add(current.node_id)
                current = by_id[current.parent_id]

    @staticmethod
    def _validate_parent_order_and_spans(
        by_id: Dict[str, StructuralNode], root: StructuralNode
    ) -> None:
        for node in by_id.values():
            if node is root:
                continue
            parent = by_id[node.parent_id]  # type: ignore[index]
            if parent.order >= node.order:
                raise ValueError("structural parent order must precede child order")
            if parent.has_exact_span and node.has_exact_span:
                parent_start = parent.locator.span_start
                parent_end = parent.locator.span_end
                child_start = node.locator.span_start
                child_end = node.locator.span_end
                if not (
                    parent_start is not None
                    and parent_end is not None
                    and child_start is not None
                    and child_end is not None
                    and parent_start <= child_start
                    and child_end <= parent_end
                ):
                    raise ValueError("child exact span must be contained by parent exact span")

    @property
    def source(self) -> SourceVersion:
        return self._source

    @property
    def nodes(self) -> tuple[StructuralNode, ...]:
        return self._nodes

    @property
    def root(self) -> StructuralNode:
        for node in self._nodes:
            if node.kind is StructuralKind.DOCUMENT:
                return node
        raise RuntimeError("validated structural map lost its DOCUMENT root")

    @property
    def unresolved_nodes(self) -> tuple[StructuralNode, ...]:
        return tuple(node for node in self._nodes if node.status is not StructuralStatus.RECOVERED)

    def get(self, node_id: str) -> StructuralNode:
        node_id = _required_text(node_id, "node_id")
        try:
            return self._by_id[node_id]
        except KeyError as exc:
            raise KeyError(node_id) from exc

    def children_of(self, node_id: str) -> tuple[StructuralNode, ...]:
        node = self.get(node_id)
        return self._children[node.node_id]

    def ancestors_of(self, node_id: str) -> tuple[StructuralNode, ...]:
        node = self.get(node_id)
        ancestors: list[StructuralNode] = []
        while node.parent_id is not None:
            node = self._by_id[node.parent_id]
            ancestors.append(node)
        ancestors.reverse()
        return tuple(ancestors)

    def descendants_of(self, node_id: str) -> tuple[StructuralNode, ...]:
        target = self.get(node_id)
        descendants: list[StructuralNode] = []
        for candidate in self._nodes:
            if candidate.node_id == target.node_id:
                continue
            current = candidate
            while current.parent_id is not None:
                if current.parent_id == target.node_id:
                    descendants.append(candidate)
                    break
                current = self._by_id[current.parent_id]
        return tuple(descendants)

    def iter_kind(self, kind: StructuralKind) -> tuple[StructuralNode, ...]:
        if not isinstance(kind, StructuralKind):
            raise ValueError("kind must be a StructuralKind")
        return tuple(node for node in self._nodes if node.kind is kind)

    def telemetry(self) -> StructuralMapTelemetry:
        kind_counts = {kind: 0 for kind in StructuralKind}
        status_counts = {status: 0 for status in StructuralStatus}
        exact_span_nodes = 0
        unresolved_nodes = 0
        for node in self._nodes:
            kind_counts[node.kind] += 1
            status_counts[node.status] += 1
            if node.has_exact_span:
                exact_span_nodes += 1
            if node.status is not StructuralStatus.RECOVERED:
                unresolved_nodes += 1
        return StructuralMapTelemetry(
            total_nodes=len(self._nodes),
            exact_span_nodes=exact_span_nodes,
            unresolved_nodes=unresolved_nodes,
            kind_counts=kind_counts,
            status_counts=status_counts,
        )
