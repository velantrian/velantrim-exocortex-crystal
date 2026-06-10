"""Tests for external knowledge ingestion (core/knowledge.py, RFC0063)."""
import json

import pytest

from core import knowledge
from core.memory import get_fact


# ─── Claim extraction (dependency-free parsers) ───────────────────────────────

def test_extract_text():
    out = knowledge.extract_claims("first line\n\n  second line  \n", "txt")
    assert [c["claim"] for c in out] == ["first line", "second line"]


def test_extract_markdown_strips_structure():
    md = "# Title\n- claim one\n* claim two\n1. claim three\n```\nignored code\n```\nplain claim\n"
    assert [c["claim"] for c in knowledge.extract_claims(md, "md")] == [
        "claim one", "claim two", "claim three", "plain claim"]


def test_extract_json_shapes():
    assert knowledge.extract_claims('"single"', "json") == [{"claim": "single"}]
    assert knowledge.extract_claims('["a", "b"]', "json") == [
        {"claim": "a"}, {"claim": "b"}]
    rich = '[{"claim": "x", "confidence": 0.9, "claim_type": "WORLD_FACT"}]'
    assert knowledge.extract_claims(rich, "json") == [
        {"claim": "x", "confidence": 0.9, "claim_type": "WORLD_FACT"}]
    assert knowledge.extract_claims('{"claims": ["p", "q"]}', "json") == [
        {"claim": "p"}, {"claim": "q"}]


def test_extract_jsonl():
    out = knowledge.extract_claims('"a"\n{"claim": "b"}\n', "jsonl")
    assert [c["claim"] for c in out] == ["a", "b"]


def test_extract_csv_requires_claim_column():
    out = knowledge.extract_claims("claim,confidence\nThe sky is blue,0.9\n", "csv")
    assert out == [{"claim": "The sky is blue", "confidence": 0.9}]
    with pytest.raises(ValueError):
        knowledge.extract_claims("text,value\nx,1\n", "csv")


def test_unsupported_format_raises():
    with pytest.raises(ValueError):
        knowledge.extract_claims("...", "yaml")


def test_extract_csv_tolerates_bad_numbers_and_skips_empty_rows():
    csv_text = "claim,confidence,claim_type\n,0.5,WORLD_FACT\nValid claim,bad,OPINION\n"
    assert knowledge.extract_claims(csv_text, "csv") == [
        {"claim": "Valid claim", "claim_type": "OPINION"}]  # empty row skipped, bad conf dropped


def test_extract_json_ignores_unusable_shapes():
    assert knowledge.extract_claims("{}", "json") == []        # dict w/o claim(s)
    assert knowledge.extract_claims("123", "json") == []       # not str/dict/list


def test_ingest_claims_skips_blank_claims():
    rep = knowledge.ingest_claims([{"claim": "   "}, {"claim": "Iron is a metal"}])
    assert rep["total"] == 1 and rep["accepted"] == 1


def test_ingest_file_honours_explicit_fmt_without_extension(tmp_path):
    p = tmp_path / "dump"                                       # no extension
    p.write_text("Salt dissolves in water\n", encoding="utf-8")
    rep = knowledge.ingest_file(str(p), fmt="txt")
    assert rep["accepted"] == 1


# ─── Ingestion through the TruthGate ──────────────────────────────────────────

def test_ingest_claims_tags_external_provenance():
    rep = knowledge.ingest_claims(
        [{"claim": "The Sun is a star"}], source="astro.txt")
    assert rep["accepted"] == 1 and rep["blocked"] == 0
    fid = rep["fact_ids"][0]
    fact = get_fact(fid)
    assert fact["source_status"] == "EXTERNAL"      # imported, not user-reported
    assert fact["source"] == "astro.txt"            # provenance kept


def test_ingest_claims_blocks_low_confidence():
    rep = knowledge.ingest_claims(
        [{"claim": "Dubious imported claim", "confidence": 0.0}], source="x")
    assert rep["accepted"] == 0 and rep["blocked"] == 1
    assert rep["blocked_reasons"][0]["claim"] == "Dubious imported claim"


def test_ingest_text_end_to_end():
    rep = knowledge.ingest_text(
        "Water boils at 100C\nThe Earth orbits the Sun\n", fmt="txt", source="facts")
    assert rep["total"] == 2 and rep["accepted"] == 2


def test_duplicate_claims_reinforce():
    knowledge.ingest_claims([{"claim": "Gold is a metal"}], source="s")
    rep = knowledge.ingest_claims([{"claim": "Gold is a metal"}], source="s")
    assert rep["reinforced"] == 1


# ─── File ingestion ───────────────────────────────────────────────────────────

def test_ingest_file_dispatches_by_extension(tmp_path):
    p = tmp_path / "kb.json"
    p.write_text(json.dumps(["Mercury is a planet", "Helium is a gas"]),
                 encoding="utf-8")
    rep = knowledge.ingest_file(str(p))
    assert rep["accepted"] == 2
    assert rep["source"] == "kb.json"               # default source = basename


def test_ingest_file_rejects_unsupported_extension(tmp_path):
    p = tmp_path / "data.bin"
    p.write_text("x", encoding="utf-8")
    with pytest.raises(ValueError):
        knowledge.ingest_file(str(p))


# ─── ingest() source_status passthrough (the enabling change) ─────────────────

def test_ingest_accepts_explicit_source_status():
    from core.ingest import ingest
    res = ingest("Neptune is a planet", source_status="EXTERNAL")
    assert res["accepted"] is True
    assert get_fact(res["fact"]["fact_id"])["source_status"] == "EXTERNAL"


# ─── CLI ──────────────────────────────────────────────────────────────────────

def test_cli_learn(tmp_path, capsys):
    from core.cli import main
    p = tmp_path / "notes.md"
    p.write_text("# Heading\n- The Moon orbits the Earth\n- Stars emit light\n",
                 encoding="utf-8")
    assert main(["learn", str(p), "--source", "lesson1"]) == 0
    rep = json.loads(capsys.readouterr().out.strip())
    assert rep["accepted"] == 2 and rep["source"] == "lesson1"
