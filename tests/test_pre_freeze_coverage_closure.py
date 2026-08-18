from __future__ import annotations

import pytest

from core import eval as core_eval, evidence


def test_strict_source_span_coverage_empty_input_is_zero():
    assert core_eval.strict_source_span_coverage([]) == 0.0


class _FixtureFile:
    def joinpath(self, _name):
        return self

    def read_text(self, **_kwargs):
        return '{"cases": []}'


def test_fixture_loader_rejects_missing_manifest_digest(monkeypatch):
    monkeypatch.setattr(core_eval.resources, "files", lambda _pkg: _FixtureFile())
    monkeypatch.setattr(core_eval, "_fixture_manifest", lambda: {"sha256": {}})

    with pytest.raises(RuntimeError, match="manifest has no digest"):
        core_eval._load_fixture_json("retrieval.json")


def test_fixture_loader_rejects_digest_drift(monkeypatch):
    monkeypatch.setattr(core_eval.resources, "files", lambda _pkg: _FixtureFile())
    monkeypatch.setattr(
        core_eval,
        "_fixture_manifest",
        lambda: {"sha256": {"retrieval.json": "0" * 64}},
    )

    with pytest.raises(RuntimeError, match="fixture digest mismatch"):
        core_eval._load_fixture_json("retrieval.json")


def test_grounding_evidence_missing_fact_is_not_valid(monkeypatch):
    monkeypatch.setattr(evidence.memory, "get_fact", lambda _fact_id: None)
    assert evidence.valid_evidence_for_grounding("missing") == []


def test_grounding_evidence_rejects_bad_uri_claim_binding_and_location(monkeypatch):
    claim = "alpha"
    claim_digest = evidence.sha256(claim)
    sealed_digest = "a" * 64
    monkeypatch.setattr(
        evidence.memory,
        "get_fact",
        lambda _fact_id: {"claim": claim, "restricted": False},
    )
    monkeypatch.setattr(
        evidence,
        "evidence_for",
        lambda _fact_id: [
            {
                "source_uri": "   ",
                "source_sha256": sealed_digest,
                "claim_sha256": claim_digest,
                "span_start": 0,
                "span_end": 1,
            },
            {
                "source_uri": "file://wrong-claim",
                "source_sha256": sealed_digest,
                "claim_sha256": "0" * 64,
                "span_start": 0,
                "span_end": 1,
            },
            {
                "source_uri": "file://no-location",
                "source_sha256": sealed_digest,
                "claim_sha256": claim_digest,
            },
        ],
    )

    assert evidence.valid_evidence_for_grounding("fact") == []


def test_lineage_metrics_empty_evidence_is_explicitly_zeroed():
    assert evidence.lineage_metrics([]) == {
        "evidence_count": 0,
        "known_lineage_coverage": 0.0,
        "same_lineage_duplicate_rate": 0.0,
        "unique_lineage_count": 0,
        "independence_assertion_coverage": 0.0,
        "unknown_lineage_rate": 0.0,
    }
