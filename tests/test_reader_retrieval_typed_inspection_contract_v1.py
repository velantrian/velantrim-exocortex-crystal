from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "eval/reader_retrieval_typed_inspection_contract_v1.json"
DOC = ROOT / "docs/architecture/READER_RETRIEVAL_TYPED_INSPECTION_CONTRACT_V1.md"


def _contract() -> dict:
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def test_rrtic_v1_bounded_contract() -> None:
    contract = _contract()
    assert contract["status"] == "FROZEN_ARCHITECTURE_CONTRACT"
    assert contract["tracking_issue"] == 391
    assert len(contract["relation_families"]) == 6
    assert len(contract["qualifier_dimensions"]) == 10
    assert contract["qualifier_states"] == [
        "MATCH",
        "MISMATCH",
        "UNKNOWN",
        "NOT_APPLICABLE",
    ]
    assert contract["stop_gate"]["max_relation_families"] == 6
    assert contract["stop_gate"]["max_qualifier_dimensions"] == 10
    assert contract["stop_gate"]["implicit_accept_reject_forbidden"] is True


def test_rrtic_v1_authority_and_runtime_are_disabled() -> None:
    contract = _contract()
    assert all(value is False for value in contract["required_authority_flags"].values())
    assert all(value is False for value in contract["decision_policy"].values())
    assert all(value is False for value in contract["runtime"].values())


def test_rrtic_v1_examples_use_only_frozen_vocabulary() -> None:
    contract = _contract()
    families = set(contract["relation_families"])
    dimensions = set(contract["qualifier_dimensions"])
    states = set(contract["qualifier_states"])
    assert len(contract["representability_examples"]) == 5
    for example in contract["representability_examples"]:
        assert example["relation_family"] in families
        assert set(example["qualifiers"]) == dimensions
        assert set(example["qualifiers"].values()) <= states


def test_rrtic_v1_keeps_rc5_and_evaluation_separate() -> None:
    contract = _contract()
    rc5 = contract["rc5_compatibility"]
    assert rc5["existing_module"] == "core/reader_relations.py"
    assert rc5["replaces_rc5"] is False
    assert rc5["auto_registers_rc5"] is False
    assert rc5["relation_kind_mapping_authorized"] is False

    policy = contract["evaluation_policy"]
    assert policy["prior_frozen_surfaces_are_explanatory_only"] is True
    assert policy["performance_qualification_authorized"] is False
    assert policy["future_discriminator_requires_new_experiment_identity"] is True
    assert policy["future_discriminator_requires_preregistration"] is True
    assert policy["future_discriminator_requires_fresh_validation_design"] is True


def test_rrtic_v1_document_states_stop_and_authority_boundaries() -> None:
    doc = DOC.read_text(encoding="utf-8")
    assert "FROZEN ARCHITECTURE CONTRACT" in doc
    assert "Runtime authorization:** false" in doc
    assert "RRTIC diagnostic" in doc
    assert "RC-5 registered relation" in doc
    assert "retrieval match          != evidence" in doc
    assert "more than six relation families" in doc
    assert "more than ten qualifier dimensions" in doc
    assert "new experiment identity" in doc
    assert "fresh validation design" in doc
