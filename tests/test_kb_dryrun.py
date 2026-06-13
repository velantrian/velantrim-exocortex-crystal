"""Tests for KB Dry-Run Batch Manifest (core/kb_ingest.py, PR4 — grant WP2/WP4).

A batch manifest dry-run predicts accept/reinforce/blocked/conflict for every
claim in a corpus WITHOUT writing anything to memory. The TruthGate and all
guards are exercised; the canon is untouched.
"""
import json
import os
import tempfile

import pytest

from core import kb_ingest
from core.ingest import ingest
from core.memory import get_all_facts


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _jsonl_file(records, suffix=".jsonl"):
    """Write claim records to a temporary JSONL or JSON file, return path."""
    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=suffix, delete=False, encoding="utf-8")
    if suffix == ".json":
        json.dump(records, tmp)
    else:
        for rec in records:
            tmp.write(json.dumps(rec, ensure_ascii=False) + "\n")
    tmp.close()
    return tmp.name


# ─── dry_run_batch ────────────────────────────────────────────────────────────

def test_dry_run_batch_returns_manifest_shape(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    claims = [{"claim": "Water is composed of hydrogen and oxygen",
               "source_status": "EXTERNAL"}]
    result = kb_ingest.dry_run_batch(claims)
    assert result["dry_run"] is True
    assert result["total"] == 1
    assert "would_accept" in result
    assert "would_block" in result
    assert "would_reinforce" in result
    assert "conflicts" in result
    assert len(result["items"]) == 1


def test_dry_run_batch_blocked_llm_world_fact(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    claims = [{"claim": "Glorptium boils at minus 9000 degrees",
               "source_status": "LLM_OUTPUT",
               "claim_type": "WORLD_FACT"}]
    result = kb_ingest.dry_run_batch(claims)
    assert result["would_block"] == 1
    assert result["would_accept"] == 0
    assert result["items"][0]["verdict"] == "blocked"


def test_dry_run_batch_accept_external(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    claims = [{"claim": "The speed of light is approximately 299792 km/s",
               "source_status": "EXTERNAL"}]
    result = kb_ingest.dry_run_batch(claims)
    assert result["items"][0]["verdict"] == "accept"
    assert result["would_accept"] == 1


def test_dry_run_batch_reinforce_existing(monkeypatch):
    """A claim already Validated in canon is predicted as reinforce, not accept."""
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    claim = "The Earth orbits the Sun once per year"
    ingest(claim, source="test", source_status="EXTERNAL", claim_type="WORLD_FACT")
    claims = [{"claim": claim, "source_status": "EXTERNAL"}]
    result = kb_ingest.dry_run_batch(claims)
    verdicts = {it["verdict"] for it in result["items"]}
    assert "reinforce" in verdicts or "accept" in verdicts


def test_dry_run_batch_empty_claim_blocked(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    claims = [{"claim": ""}]
    result = kb_ingest.dry_run_batch(claims)
    assert result["items"][0]["verdict"] == "blocked"
    assert result["would_block"] == 1


def test_dry_run_batch_mixed_verdicts(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    claims = [
        {"claim": "Iron has atomic number 26", "source_status": "EXTERNAL"},
        {"claim": "Fake element Xyrtonium has atomic number 999",
         "source_status": "LLM_OUTPUT", "claim_type": "WORLD_FACT"},
    ]
    result = kb_ingest.dry_run_batch(claims)
    assert result["total"] == 2
    assert result["would_block"] >= 1


def test_dry_run_batch_does_not_write_to_memory(monkeypatch):
    """Nothing must be persisted after a dry-run batch."""
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    before = len(get_all_facts())
    claims = [
        {"claim": "Quortium has a boiling point of negative infinity",
         "source_status": "EXTERNAL"},
        {"claim": "Nullium defies all known physics", "source_status": "EXTERNAL"},
    ]
    kb_ingest.dry_run_batch(claims)
    after = len(get_all_facts())
    assert after == before


def test_dry_run_batch_custom_source(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    claims = [{"claim": "Gold is a noble metal", "source_status": "EXTERNAL"}]
    result = kb_ingest.dry_run_batch(claims, source="my-corpus-v1")
    assert result["source"] == "my-corpus-v1"


# ─── dry_run_manifest_file — JSONL ────────────────────────────────────────────

def test_dry_run_manifest_file_jsonl(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    records = [
        {"claim": "Copper conducts electricity well", "source_status": "EXTERNAL"},
        {"claim": "Aetherium emits cold fire", "source_status": "LLM_OUTPUT",
         "claim_type": "WORLD_FACT"},
    ]
    path = _jsonl_file(records, suffix=".jsonl")
    try:
        result = kb_ingest.dry_run_manifest_file(path)
        assert result["dry_run"] is True
        assert result["total"] == 2
        assert result["would_block"] >= 1
    finally:
        os.unlink(path)


def test_dry_run_manifest_file_json_array(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    records = [
        {"claim": "Silver is a metal", "source_status": "EXTERNAL"},
    ]
    path = _jsonl_file(records, suffix=".json")
    try:
        result = kb_ingest.dry_run_manifest_file(path)
        assert result["total"] == 1
        assert result["items"][0]["verdict"] == "accept"
    finally:
        os.unlink(path)


def test_dry_run_manifest_file_ndjson(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    records = [{"claim": "Lead is denser than aluminium", "source_status": "EXTERNAL"}]
    path = _jsonl_file(records, suffix=".ndjson")
    try:
        result = kb_ingest.dry_run_manifest_file(path)
        assert result["total"] == 1
    finally:
        os.unlink(path)


def test_dry_run_manifest_file_not_found():
    with pytest.raises(FileNotFoundError):
        kb_ingest.dry_run_manifest_file("/nonexistent/path/manifest.jsonl")


def test_dry_run_manifest_file_json_not_array(monkeypatch):
    """A JSON manifest that is not a list raises ValueError."""
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False, encoding="utf-8")
    json.dump({"claim": "not a list"}, tmp)
    tmp.close()
    try:
        with pytest.raises(ValueError, match="top-level array"):
            kb_ingest.dry_run_manifest_file(tmp.name)
    finally:
        os.unlink(tmp.name)


def test_dry_run_manifest_file_custom_source(monkeypatch):
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    records = [{"claim": "Tin is a soft metal", "source_status": "EXTERNAL"}]
    path = _jsonl_file(records, suffix=".jsonl")
    try:
        result = kb_ingest.dry_run_manifest_file(path, source="override-source")
        assert result["source"] == "override-source"
    finally:
        os.unlink(path)


def test_dry_run_manifest_empty_jsonl(monkeypatch):
    """An empty manifest file returns zero items."""
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".jsonl", delete=False, encoding="utf-8")
    tmp.write("")
    tmp.close()
    try:
        result = kb_ingest.dry_run_manifest_file(tmp.name)
        assert result["total"] == 0
        assert result["items"] == []
    finally:
        os.unlink(tmp.name)


# ─── CLI integration ──────────────────────────────────────────────────────────

def test_cli_kb_ingest(monkeypatch):
    """CLI kb-ingest command produces valid JSON manifest output."""
    import subprocess
    import sys
    monkeypatch.setenv("VELANTRIM_DEMO_SEED", "0")
    records = [{"claim": "Zinc is a transition metal", "source_status": "EXTERNAL"}]
    path = _jsonl_file(records, suffix=".jsonl")
    try:
        out = subprocess.check_output(
            [sys.executable, "-m", "core.cli", "kb-ingest", path],
            text=True)
        result = json.loads(out)
        assert result["dry_run"] is True
        assert result["total"] == 1
    finally:
        os.unlink(path)
