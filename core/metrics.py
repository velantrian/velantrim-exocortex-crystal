# core/metrics.py
# Velantrim ExoCortex — lightweight in-process metrics
# v8.8.0-sprint2
#
# Counters for memory operations (queries, ingest, gates) — observability without external
# dependencies. The structure is simple (name → count), easily exported to
# Prometheus later. Thread safety is not required for the MVP (sync pipeline).

from typing import Dict

_COUNTERS: Dict[str, int] = {}


def incr(name: str, n: int = 1) -> None:
    """Increment counter `name` by n."""
    _COUNTERS[name] = _COUNTERS.get(name, 0) + n


def value(name: str) -> int:
    """Current value of the counter (0 if it has not been set)."""
    return _COUNTERS.get(name, 0)


def snapshot() -> Dict[str, int]:
    """A copy of all counters."""
    return dict(_COUNTERS)


def reset() -> None:
    """Zero out all counters (for tests / a new observation window)."""
    _COUNTERS.clear()
