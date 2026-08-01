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

from core.memory import ESM_STATES, ESM_TRANSITIONS, IMMUTABLE_FACT_IDS

ESM_SPEC_SCHEMA_VERSION = 1
DEFAULT_ENTRY_STATES = frozenset({"Observed"})


def _terminal_states() -> frozenset[str]:
    """Derive terminal states from the active runtime table."""
    return frozenset(
        state
        for state in ESM_STATES
        if not ESM_TRANSITIONS.get(state, set())
    )


def _sorted_transition_table() -> dict[str, list[str]]:
    return {
        source: sorted(ESM_TRANSITIONS.get(source, set()))
        for source in sorted(ESM_STATES)
    }


def validate_esm_spec() -> dict[str, Any]:
    """Validate structural and reachability invariants of the runtime ESM table."""
    errors: list[str] = []
    states = set(ESM_STATES)
    entries = set(DEFAULT_ENTRY_STATES)

    if not states:
        errors.append("ESM_STATES must not be empty")
    if any(not isinstance(state, str) or not state.strip() for state in states):
        errors.append("every ESM state must be a non-blank string")
    if not entries <= states:
        errors.append("DEFAULT_ENTRY_STATES must be a subset of ESM_STATES")

    extra_sources = set(ESM_TRANSITIONS) - states
    if extra_sources:
        errors.append(
            "transition table contains unknown source states: "
            + ", ".join(sorted(extra_sources))
        )
    missing_sources = states - set(ESM_TRANSITIONS)
    if missing_sources:
        errors.append(
            "transition table is missing source states: "
            + ", ".join(sorted(missing_sources))
        )

    for source, targets in ESM_TRANSITIONS.items():
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

    reachable = set(entries)
    queue: deque[str] = deque(sorted(entries))
    while queue:
        source = queue.popleft()
        for target in ESM_TRANSITIONS.get(source, set()):
            if target in states and target not in reachable:
                reachable.add(target)
                queue.append(target)
    unreachable = states - reachable
    if unreachable:
        errors.append(
            "states unreachable from declared default entry states: "
            + ", ".join(sorted(unreachable))
        )

    if any(
        not isinstance(fact_id, str) or not fact_id.strip()
        for fact_id in IMMUTABLE_FACT_IDS
    ):
        errors.append("IMMUTABLE_FACT_IDS must contain only non-blank strings")

    terminals = _terminal_states()
    return {
        "valid": not errors,
        "errors": errors,
        "state_count": len(states),
        "terminal_count": len(terminals),
        "transition_count": sum(len(targets) for targets in ESM_TRANSITIONS.values()),
        "reachable_states": sorted(reachable),
    }


def esm_spec() -> dict[str, Any]:
    """Return a fresh JSON-serializable descriptor of the active runtime ESM."""
    table = _sorted_transition_table()
    terminals = _terminal_states()
    validation = validate_esm_spec()
    sealed = {
        "schema_version": ESM_SPEC_SCHEMA_VERSION,
        "states": sorted(ESM_STATES),
        "default_entry_states": sorted(DEFAULT_ENTRY_STATES),
        "terminal_states": sorted(terminals),
        "protected_fact_ids": sorted(IMMUTABLE_FACT_IDS),
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
    """Fail-closed query over the active runtime transition table.

    This answers matrix membership only. `memory.transition_esm()` remains the
    write authority and may additionally reject protected fact IDs.
    """
    if not isinstance(source, str) or not isinstance(target, str):
        return False
    return target in ESM_TRANSITIONS.get(source, set())


def shortest_transition_path(source: Any, target: Any) -> Optional[list[str]]:
    """Return the shortest matrix path, or None when no path exists."""
    if not isinstance(source, str) or not isinstance(target, str):
        return None
    if source not in ESM_STATES or target not in ESM_STATES:
        return None
    if source == target:
        return [source]

    queue: deque[tuple[str, list[str]]] = deque([(source, [source])])
    visited = {source}
    while queue:
        current, path = queue.popleft()
        for next_state in sorted(ESM_TRANSITIONS.get(current, set())):
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
        try:
            known = state in ESM_STATES
        except TypeError:
            known = False
        if not known:
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
    "DEFAULT_ENTRY_STATES",
    "ESM_SPEC_SCHEMA_VERSION",
    "esm_spec",
    "shortest_transition_path",
    "transition_allowed",
    "validate_esm_spec",
    "validate_state_records",
]
