"""Tiny Essence Workdesk / L0.5 prototype.

This module is research-only. It is not Crystal runtime, not Canon, and not a
TruthGate replacement. The goal is to test whether a small active board can keep
long dialogues focused without unsafe fast-path decisions.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field

ALLOWED_KINDS = frozenset({"essence", "question", "decision", "claim"})
FAST = "FAST"
DEEP = "DEEP"


@dataclass(frozen=True)
class BoardItem:
    """One active item on the v0 dialogue board."""

    text: str
    kind: str
    receipt_hash: str | None = None
    valid: bool = False
    pinned: bool = False
    last_touched: float = field(default_factory=time.time)
    changed: bool = False
    high_risk: bool = False
    verification_requested: bool = False
    canon_write_requested: bool = False
    conflict: bool = False

    def __post_init__(self) -> None:
        if not self.text.strip():
            raise ValueError("BoardItem.text must not be empty")
        if self.kind not in ALLOWED_KINDS:
            allowed = ", ".join(sorted(ALLOWED_KINDS))
            raise ValueError(f"BoardItem.kind must be one of: {allowed}")

    @property
    def has_valid_receipt(self) -> bool:
        """Return whether the item has a receipt that may be reused locally."""

        return bool(self.receipt_hash and self.valid)


def route(item: BoardItem) -> str:
    """Route one board item through the minimal v0 FAST / DEEP policy."""

    if item.high_risk or item.verification_requested or item.canon_write_requested:
        return DEEP
    if item.conflict or item.changed:
        return DEEP
    if item.kind == "claim":
        return FAST if item.has_valid_receipt else DEEP
    return FAST


def prune_board(items: list[BoardItem], max_items: int = 7) -> list[BoardItem]:
    """Keep a bounded active board without deleting source material."""

    if max_items < 1:
        raise ValueError("max_items must be at least 1")
    if len(items) <= max_items:
        return list(items)

    def priority(item: BoardItem) -> tuple[int, float]:
        if item.pinned:
            return (4, item.last_touched)
        if item.kind == "claim" and item.has_valid_receipt:
            return (3, item.last_touched)
        if item.kind == "essence":
            return (2, item.last_touched)
        if item.kind in {"question", "decision"}:
            return (1, item.last_touched)
        return (0, item.last_touched)

    return sorted(items, key=priority, reverse=True)[:max_items]


def essence_retention_failure(items: list[BoardItem]) -> bool:
    """Detect whether the active board lost its current essence anchor."""

    return not any(item.kind == "essence" and item.text.strip() for item in items)
