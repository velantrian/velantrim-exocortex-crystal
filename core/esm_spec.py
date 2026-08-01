# core/esm_spec.py
# Velantrim ExoCortex — machine-readable Epistemic State Machine contract.
#
# The runtime transition table remains defined in core.memory and is used by all
# write paths through memory.transition_esm(). This module exposes that same
# table as a deterministic, validated read model instead of creating a second
# independently editable state machine.

from __future__ import annotations

from collections import deque
import hashlib
import json
from typing import Any, Iterable, Mapping, Optional

from core.memory import ESM_STATES, TERMINAL_STATES, _ALLOWED_TRANSITIONS

ESM_SPEC_SCHEMA_VERSION = 1
ENTRY_STATES = frozenset({"Observed", "ImmutableCore"})
ISOLATED_ENTRY_STATES = frozenset({"ImmutableCore"})


def _sorted_transition_table() -> dict[str, list[str]]:
    return {
        source: sorted(_ALLOWED_TRANSITIONS.get(source, frozenset()))
        for source in sorted(ESM_STATES)
    }


def validate_esm_spec() -> dict[str, Any]:
    """Validate structural and reachability invariants of the runtime ESM table."""
    errors: list[str] = []
    states = set(ESM_STATES)
    terminals = set(TERMINAL_STATES)
    entries = set(ENTRY_STATES)

    if not states:
        errors.append("ESM_STATES must not be empty")
    if any(not isinstance(state, str) or not state.strip() for state in states):
        errors.append("every ESM state must be a non-blank string")
    if not terminals <= states:
        errors.append("TERMINAL_STATES must be a subset of ESM_STATES")
    if not entries <= states:
        errors.append("ENTRY_STATES must be a subset of ESM_STATES")

    extra_sources = set(_ALLOWED_TRANSITIONS) - states
    if extra_sources:
        errors.append(
            "transition table contains unknown source states: "
            + ", ".join(sorted(extra_sources))
        )

    for source, targets in _ALLOWED_TRANSITIONS.items():
        if not isinstance(targets, (set, frozenset)):
            errors.append(f"transition targets for {source!r} must be a set/frozenset")
            continue
        unknown_targets = set(targets) - states
        if unknown_targets:
            errors.append(
                f"{source!r} contains unknown targets: "
                + ", ".join(sorted(unknown_targets))
            )
        if source in targets:
            errors.append(f"self-transition is not allowed for {source!r}")

    for terminal in terminals:
        if _ALLOWED_TRANSITIONS.get(terminal, frozenset()):
            errors.append(f"terminal state {terminal!r} must have no outgoing transitions")

    reachable = set(ISOLATED_ENTRY_STATES)
    queue: deque[str] = deque(sorted(entries - ISOLATED_ENTRY_STATES))
    reachable.update(queue)
    while queue:
        source = queue.popleft()
        for target in _ALLOWED_TRANSITIONS.get(source, frozenset()):
            if target not in reachable:
                reachable.add(target)
                queue.append(target)
    unreachable = states - reachable
    if unreachable:
        errors.append(
            "states unreachable from declared entry states: "
            + ", ".join(sorted(unreachable))
        )

    if any(
        target == "ImmutableCore"
        for targets in _ALLOWED_TRANSITIONS.values()
        for target in targets
    ):
        errors.append("ImmutableCore must be created explicitly, never reached by transition")

    return {
        "valid": not errors,
        "errors": errors,
        "state_count": len(states),
        "terminal_count": len(terminals),
        "transition_count": sum(len(targets) for targets in _ALLOWED_TRANSITIONS.values()),
        "reachable_states": sorted(reachable),
    }


def esm_spec() -> dict[str, Any]:
    """Return a fresh JSON-serializable descriptor of the active runtime ESM."""
    table = _sorted_transition_table()
    validation = validate_esm_spec()
    sealed = {
        "schema_version": ESM_SPEC_SCHEMA_VERSION,
        "states": sorted(ESM_STATES),
        "entry_states": sorted(ENTRY_STATES),
        "isolated_entry_states": sorted(ISOLATED_ENTRY_STATES),
        "terminal_states": sorted(TERMINAL_STATES),
        "transitions": table,
    }
    canonical = json.dumps(
        sealed, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    )
    return {
        **sealed,
        "sha256": hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
        "validation": validation,
    }


def transition_allowed(source: Any, target: Any) -> bool:
    """Fail-closed query over the active runtime transition table."""
    if not isinstance(source, str) or not isinstance(target, str):
        return False
    return target in _ALLOWED_TRANSITIONS.get(source, frozenset())


def shortest_transition_path(source: Any, target: Any) -> Optional[list[str]]:
    """Return the shortest allowed state path, or None when no path exists."""
    if source not in ESM_STATES or target not in ESM_STATES:
        return None
    if source == target:
        return [source]

    queue: deque[tuple[str, list[str]]] = deque([(source, [source])])
    visited = {source}
    while queue:
        current, path = queue.popleft()
        for next_state in sorted(_ALLOWED_TRANSITIONS.get(current, frozenset())):
            if next_state == target:
                return [*path, next_state]
            if next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, [*path, next_state]))
    return None


def validate_state_records(records: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    """Validate fact-like records without mutating storage or guessing defaults."""
    invalid: list[dict[str, Any]] = []
    checked = 0
    for index, record in enumerate(records):
        checked += 1
        if not isinstance(record, Mapping):
            invalid.append(
                {"index": index, "fact_id": None, "state": None, "reason": "not_a_mapping"}
            )
            continue
        state = record.get("epistemic_state")
        if state not in ESM_STATES:
            invalid.append(
                {
                    "index": index,
                    "fact_id": record.get("fact_id"),
                    "state": state if isinstance(state, str) else None,
                    "reason": "unknown_or_missing_state",
                }
            )
    return {"valid": not invalid, "checked": checked, "invalid": invalid}


__all__ = [
    "ENTRY_STATES",
    "ESM_SPEC_SCHEMA_VERSION",
    "ISOLATED_ENTRY_STATES",
    "esm_spec",
    "shortest_transition_path",
    "transition_allowed",
    "validate_esm_spec",
    "validate_state_records",
]
