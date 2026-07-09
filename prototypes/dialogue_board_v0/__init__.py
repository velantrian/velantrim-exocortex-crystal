"""Tiny research-only dialogue board prototype.

This package is intentionally kept under prototypes/ and has no Crystal runtime
wiring.
"""

from .board_v0 import BoardItem, essence_retention_failure, prune_board, route

__all__ = [
    "BoardItem",
    "essence_retention_failure",
    "prune_board",
    "route",
]
