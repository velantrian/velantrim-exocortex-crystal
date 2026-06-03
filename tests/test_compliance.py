"""Tests for core/compliance.py — GDPR Art. 18 (restriction) & Art. 30 (RoPA)."""
import json

import pytest

from core.compliance import (
    restrict_processing, unrestrict_processing, is_restricted,
    restricted_facts, record_of_processing,
)
from core.memory import store_fact, get_fact
from core.l3_graph import get_l3_graph
from core.pipeline import retrieve


def _seed(fact_id, claim, state="Validated"):
    store_fact({"fact_id": fact_id, "claim": claim, "source": "test",
                "epistemic_state": state})
    get_l3_graph().merge_fact(get_fact(fact_id))
    return fact_id


# ─── Art. 18: restriction of processing ───────────────────────────────────────

def test_restrict_sets_flag_and_is_reversible():
    _seed("f1", "some claim")
    assert is_restricted("f1") is False

    rec = restrict_processing("f1", reason="dispute")
    assert rec["found"] is True
    assert rec["restricted"] is True
    assert is_restricted("f1") is True

    rec2 = unrestrict_processing("f1")
    assert rec2["restricted"] is False
    assert is_restricted("f1") is False


def test_restrict_unknown_fact_reports_not_found():
    rec = restrict_processing("ghost")
    assert rec["found"] is False
    assert is_restricted("ghost") is False


def test_restricted_fact_excluded_from_recall():
    # Unique claim so it only matches the L3 fact, not the seed corpus.
    _seed("f1", "Zorblax craves mauve telemetry")
    hits_before = [h["id"] for h in retrieve("Zorblax craves mauve telemetry")]
    assert "f1" in hits_before

    restrict_processing("f1")
    hits_after = [h["id"] for h in retrieve("Zorblax craves mauve telemetry")]
    assert "f1" not in hits_after

    # Lifting the restriction brings it back into recall.
    unrestrict_processing("f1")
    hits_restored = [h["id"] for h in retrieve("Zorblax craves mauve telemetry")]
    assert "f1" in hits_restored


def test_restricted_facts_lists_only_restricted():
    _seed("f1", "alpha")
    _seed("f2", "beta")
    restrict_processing("f2")
    assert restricted_facts() == ["f2"]


# ─── Art. 30: record of processing ────────────────────────────────────────────

def test_ropa_aggregates_and_is_content_free():
    _seed("f1", "highly sensitive personal claim")
    store_fact({"fact_id": "f2", "claim": "a feeling", "source": "user",
                "claim_type": "EMOTION", "epistemic_state": "Validated"})
    get_l3_graph().merge_fact(get_fact("f2"))
    restrict_processing("f1")

    ropa = record_of_processing(controller="Acme BV")

    assert ropa["controller"] == "Acme BV"
    assert ropa["regulation"].startswith("GDPR")
    assert ropa["fact_count"] == 2
    assert ropa["categories_of_data"]["WORLD_FACT"] == 1
    assert ropa["categories_of_data"]["EMOTION"] == 1
    assert ropa["restricted_count"] == 1
    assert ropa["restricted_fact_ids"] == ["f1"]
    # Content-free: no actual claim text leaks into the record.
    assert "highly sensitive personal claim" not in json.dumps(ropa)


def test_ropa_reports_local_no_transfer_by_default(monkeypatch):
    monkeypatch.setenv("VELANTRIM_GENERATOR", "extractive")
    monkeypatch.setenv("VELANTRIM_L3_BACKEND", "mock")
    ropa = record_of_processing()
    assert ropa["international_transfer"] is False
    assert ropa["backends"]["generator"] == "extractive"


def test_ropa_flags_transfer_when_claude_generator(monkeypatch):
    monkeypatch.setenv("VELANTRIM_GENERATOR", "claude")
    ropa = record_of_processing()
    assert ropa["international_transfer"] is True


# ─── CLI ──────────────────────────────────────────────────────────────────────

def test_cli_restrict_unrestrict_and_ropa(capsys):
    from core.cli import main

    _seed("f1", "cli claim")
    assert main(["restrict", "f1"]) == 0
    assert json.loads(capsys.readouterr().out.strip())["restricted"] is True
    assert is_restricted("f1") is True

    assert main(["unrestrict", "f1"]) == 0
    assert json.loads(capsys.readouterr().out.strip())["restricted"] is False

    assert main(["ropa"]) == 0
    ropa = json.loads(capsys.readouterr().out.strip())
    assert ropa["fact_count"] >= 1
    assert "data_subject_rights" in ropa
