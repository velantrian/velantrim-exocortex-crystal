import pytest

from prototypes.dialogue_board_v0 import (
    BoardItem,
    essence_retention_failure,
    prune_board,
    route,
)
from prototypes.dialogue_board_v0.board_v0 import DEEP, FAST


def test_board_item_validates_text_and_kind() -> None:
    with pytest.raises(ValueError, match="text"):
        BoardItem(text="   ", kind="essence")

    with pytest.raises(ValueError, match="kind"):
        BoardItem(text="hello", kind="unknown")


def test_valid_receipt_claim_routes_fast() -> None:
    item = BoardItem(text="PR #204 is prototype-only", kind="claim", receipt_hash="abc", valid=True)

    assert item.has_valid_receipt is True
    assert route(item) == FAST


def test_claim_without_valid_receipt_routes_deep() -> None:
    item = BoardItem(text="new unsupported claim", kind="claim")

    assert item.has_valid_receipt is False
    assert route(item) == DEEP


def test_local_working_items_route_fast() -> None:
    assert route(BoardItem(text="current essence", kind="essence")) == FAST
    assert route(BoardItem(text="open question", kind="question")) == FAST
    assert route(BoardItem(text="local decision", kind="decision")) == FAST


def test_risk_and_verification_flags_route_deep() -> None:
    assert route(BoardItem(text="medical claim", kind="claim", high_risk=True)) == DEEP
    assert route(BoardItem(text="verify this", kind="question", verification_requested=True)) == DEEP
    assert route(BoardItem(text="write canon", kind="decision", canon_write_requested=True)) == DEEP


def test_changed_or_conflicting_item_routes_deep() -> None:
    assert route(BoardItem(text="changed claim", kind="claim", changed=True, receipt_hash="abc", valid=True)) == DEEP
    assert route(BoardItem(text="conflict", kind="decision", conflict=True)) == DEEP


def test_prune_returns_copy_when_under_limit() -> None:
    items = [BoardItem(text="essence", kind="essence")]

    pruned = prune_board(items, max_items=7)

    assert pruned == items
    assert pruned is not items


def test_prune_keeps_priority_items() -> None:
    items = [
        BoardItem(text="old claim", kind="claim", last_touched=1.0),
        BoardItem(text="open question", kind="question", last_touched=2.0),
        BoardItem(text="current essence", kind="essence", last_touched=3.0),
        BoardItem(text="valid claim", kind="claim", receipt_hash="abc", valid=True, last_touched=4.0),
        BoardItem(text="pinned decision", kind="decision", pinned=True, last_touched=5.0),
    ]

    pruned = prune_board(items, max_items=3)

    assert [item.text for item in pruned] == ["pinned decision", "valid claim", "current essence"]


def test_prune_rejects_invalid_limit() -> None:
    with pytest.raises(ValueError, match="max_items"):
        prune_board([], max_items=0)


def test_essence_retention_failure_detects_missing_essence() -> None:
    assert essence_retention_failure([BoardItem(text="question", kind="question")]) is True
    assert essence_retention_failure([BoardItem(text="current essence", kind="essence")]) is False
