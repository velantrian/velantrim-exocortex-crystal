"""Tests for the machine-readable runtime ESM specification."""

import json

import core.esm_spec as esm


def test_active_spec_is_valid_deterministic_json_and_fresh():
    first = esm.esm_spec()
    second = esm.esm_spec()

    assert first == second
    assert first is not second
    assert first["schema_version"] == 1
    assert first["validation"] == {
        "valid": True,
        "errors": [],
        "state_count": 8,
        "terminal_count": 3,
        "transition_count": 19,
        "reachable_states": sorted(first["states"]),
    }
    assert len(first["sha256"]) == 64
    assert json.loads(json.dumps(first)) == first

    first["transitions"]["Observed"].append("mutated")
    assert "mutated" not in second["transitions"]["Observed"]


def test_transition_queries_fail_closed_and_find_shortest_paths():
    assert esm.transition_allowed("Observed", "Validated") is True
    assert esm.transition_allowed("Validated", "Hypothesized") is False
    assert esm.transition_allowed("Unknown", "Validated") is False
    assert esm.transition_allowed([], "Validated") is False
    assert esm.transition_allowed("Observed", {}) is False

    assert esm.shortest_transition_path("Observed", "Observed") == ["Observed"]
    assert esm.shortest_transition_path("Observed", "Deprecated") == [
        "Observed",
        "Contradicted",
        "Deprecated",
    ]
    assert esm.shortest_transition_path("Validated", "Hypothesized") is None
    assert esm.shortest_transition_path("ImmutableCore", "Observed") is None
    assert esm.shortest_transition_path("Unknown", "Observed") is None
    assert esm.shortest_transition_path([], "Observed") is None


def test_state_record_validation_is_read_only_and_preserves_only_safe_state_shape():
    records = [
        {"fact_id": "ok", "epistemic_state": "Validated"},
        {"fact_id": "unknown", "epistemic_state": "Invented"},
        {"fact_id": "missing"},
        {"fact_id": "unhashable", "epistemic_state": ["Validated"]},
        "not-a-record",
    ]
    original = [dict(item) if isinstance(item, dict) else item for item in records]

    report = esm.validate_state_records(records)

    assert report["valid"] is False
    assert report["checked"] == 5
    assert report["invalid"] == [
        {
            "index": 1,
            "fact_id": "unknown",
            "state": "Invented",
            "reason": "unknown_or_missing_state",
        },
        {
            "index": 2,
            "fact_id": "missing",
            "state": None,
            "reason": "unknown_or_missing_state",
        },
        {
            "index": 3,
            "fact_id": "unhashable",
            "state": None,
            "reason": "unknown_or_missing_state",
        },
        {
            "index": 4,
            "fact_id": None,
            "state": None,
            "reason": "not_a_mapping",
        },
    ]
    assert records == original
    assert esm.validate_state_records([]) == {
        "valid": True,
        "checked": 0,
        "invalid": [],
    }


def test_validator_reports_empty_and_malformed_state_universes(monkeypatch):
    monkeypatch.setattr(esm, "ESM_STATES", frozenset())
    monkeypatch.setattr(esm, "TERMINAL_STATES", frozenset())
    monkeypatch.setattr(esm, "ENTRY_STATES", frozenset())
    monkeypatch.setattr(esm, "ISOLATED_ENTRY_STATES", frozenset())
    monkeypatch.setattr(esm, "_ALLOWED_TRANSITIONS", {})

    empty = esm.validate_esm_spec()
    assert empty["valid"] is False
    assert "ESM_STATES must not be empty" in empty["errors"]

    monkeypatch.setattr(esm, "ESM_STATES", frozenset({"Observed", " "}))
    monkeypatch.setattr(esm, "ENTRY_STATES", frozenset({"Observed"}))
    monkeypatch.setattr(esm, "_ALLOWED_TRANSITIONS", {"Observed": frozenset({" "})})
    malformed = esm.validate_esm_spec()
    assert "every ESM state must be a non-blank string" in malformed["errors"]


def test_validator_reports_all_structural_transition_failures(monkeypatch):
    states = frozenset(
        {"Observed", "Validated", "Deprecated", "ImmutableCore", "Orphan"}
    )
    monkeypatch.setattr(esm, "ESM_STATES", states)
    monkeypatch.setattr(esm, "TERMINAL_STATES", frozenset({"Deprecated", "ImmutableCore"}))
    monkeypatch.setattr(esm, "ENTRY_STATES", frozenset({"Observed", "ImmutableCore"}))
    monkeypatch.setattr(esm, "ISOLATED_ENTRY_STATES", frozenset({"ImmutableCore"}))
    monkeypatch.setattr(
        esm,
        "_ALLOWED_TRANSITIONS",
        {
            "Observed": frozenset(
                {"Observed", "Validated", "ImmutableCore", "Unknown"}
            ),
            "Validated": ["Deprecated"],
            "Deprecated": frozenset({"Validated"}),
            "Extra": frozenset({"Validated"}),
        },
    )

    report = esm.validate_esm_spec()
    text = "\n".join(report["errors"])

    assert report["valid"] is False
    assert "unknown source states: Extra" in text
    assert "targets for 'Validated' must be a set/frozenset" in text
    assert "unknown targets: Unknown" in text
    assert "self-transition is not allowed for 'Observed'" in text
    assert "terminal state 'Deprecated' must have no outgoing transitions" in text
    assert "states unreachable from declared entry states: Orphan" in text
    assert "ImmutableCore must be created explicitly" in text


def test_validator_reports_invalid_terminal_and_entry_subsets(monkeypatch):
    monkeypatch.setattr(esm, "ESM_STATES", frozenset({"Observed"}))
    monkeypatch.setattr(esm, "TERMINAL_STATES", frozenset({"MissingTerminal"}))
    monkeypatch.setattr(esm, "ENTRY_STATES", frozenset({"MissingEntry"}))
    monkeypatch.setattr(esm, "ISOLATED_ENTRY_STATES", frozenset())
    monkeypatch.setattr(esm, "_ALLOWED_TRANSITIONS", {})

    report = esm.validate_esm_spec()
    assert "TERMINAL_STATES must be a subset of ESM_STATES" in report["errors"]
    assert "ENTRY_STATES must be a subset of ESM_STATES" in report["errors"]
