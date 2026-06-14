"""Tests for scripts/eval_track.py — per-release eval tracking (grant WP3)."""
import importlib
import json
import sys
import os

import pytest

# Ensure scripts/ is importable (conftest adds project root, but not scripts/)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import eval_track
import core as _core_pkg


# ─── Helpers ─────────────────────────────────────────────────────────────────

def _synthetic_record(version="0.2.0", lang="en", hit_at_1=0.8, hit_at_3=0.9,
                      mrr=0.85, contradiction_precision=0.8,
                      contradiction_recall=0.7):
    return {
        "version": version,
        "timestamp": "2026-06-13T00:00:00+00:00",
        "lang": lang,
        "hit_at_1": hit_at_1,
        "hit_at_3": hit_at_3,
        "hit_at_5": 1.0,
        "mrr": mrr,
        "trace_completeness": 1.0,
        "metadata_completeness": 0.9,
        "source_span_coverage": 0.5,
        "receipt_replay_survival": 1.0,
        "contradiction_precision": contradiction_precision,
        "contradiction_recall": contradiction_recall,
    }


# ─── Tests ────────────────────────────────────────────────────────────────────

def test_track_appends_record(tmp_path):
    """track() creates the file and appends a well-formed record."""
    out = str(tmp_path / "h.jsonl")
    record = eval_track.track(output_path=out)
    assert os.path.exists(out)
    expected_keys = {
        "version", "timestamp", "lang",
        "hit_at_1", "hit_at_3", "hit_at_5", "mrr",
        "trace_completeness", "metadata_completeness",
        "source_span_coverage", "receipt_replay_survival",
        "contradiction_precision", "contradiction_recall",
    }
    assert expected_keys <= set(record.keys())


def test_track_multiple_appends(tmp_path):
    """Calling track() twice appends two lines to the JSONL file."""
    out = str(tmp_path / "h.jsonl")
    eval_track.track(output_path=out)
    eval_track.track(output_path=out)
    with open(out, encoding="utf-8") as fh:
        lines = [l for l in fh if l.strip()]
    assert len(lines) == 2


def test_load_history_empty_if_missing(tmp_path):
    """load_history returns [] for a nonexistent file."""
    result = eval_track.load_history(str(tmp_path / "no_such_file.jsonl"))
    assert result == []


def test_load_history_returns_records(tmp_path):
    """load_history returns a list of dicts from a JSONL file."""
    path = tmp_path / "h.jsonl"
    rec1 = _synthetic_record(version="0.1.0")
    rec2 = _synthetic_record(version="0.2.0")
    path.write_text(
        json.dumps(rec1) + "\n" + json.dumps(rec2) + "\n",
        encoding="utf-8"
    )
    records = eval_track.load_history(str(path))
    assert len(records) == 2
    assert records[0]["version"] == "0.1.0"
    assert records[1]["version"] == "0.2.0"


def test_format_trend_md_empty():
    """format_trend_md([]) returns the 'no history' message."""
    result = eval_track.format_trend_md([])
    assert result == "No eval history found."


def test_format_trend_md_with_records():
    """format_trend_md with records returns a Markdown table with expected columns."""
    records = [
        _synthetic_record(version="0.1.0", hit_at_1=0.75),
        _synthetic_record(version="0.2.0", hit_at_1=0.875),
    ]
    md = eval_track.format_trend_md(records)
    assert "version" in md
    assert "hit@1" in md
    assert "0.1.0" in md
    assert "0.2.0" in md
    assert "0.75" in md
    assert "0.875" in md


def test_main_default_runs_track(tmp_path):
    """main() with --output runs track(), returns 0, creates the file."""
    out = str(tmp_path / "h.jsonl")
    ret = eval_track.main(["--output", out])
    assert ret == 0
    assert os.path.exists(out)


def test_main_report_flag(tmp_path, capsys):
    """main() with --report prints the Markdown trend table."""
    path = tmp_path / "h.jsonl"
    rec = _synthetic_record()
    path.write_text(json.dumps(rec) + "\n", encoding="utf-8")
    ret = eval_track.main(["--output", str(path), "--report"])
    assert ret == 0
    captured = capsys.readouterr()
    assert "version" in captured.out
    assert "hit@1" in captured.out
    assert "0.2.0" in captured.out


def test_main_report_empty(tmp_path, capsys):
    """main() with --report on missing file prints 'No eval history found.'"""
    out = str(tmp_path / "empty.jsonl")
    ret = eval_track.main(["--output", out, "--report"])
    assert ret == 0
    captured = capsys.readouterr()
    assert "No eval history found." in captured.out


def test_track_lang_field(tmp_path, monkeypatch):
    """track() records the requested lang in the output record."""
    # run_baseline only supports "en" and "ru"; patch it so we can verify
    # that the lang field flows through correctly for any value.
    out = str(tmp_path / "h.jsonl")

    def _fake_run_baseline(fixture=None, *, k=5, detail=False, lang="en"):
        return {
            "cases": 4,
            "retrieval": {"hit@1": 0.8, "hit@3": 0.9, "hit@5": 1.0, "mrr": 0.85},
            "trace_completeness": 1.0,
            "metadata_completeness": 0.9,
            "source_span_coverage": 0.5,
            "unsupported_provenance": 0,
            "receipt_replay_survival": 1.0,
            "contradiction": {
                "pairs": 4, "tp": 2, "fp": 0, "fn": 0, "tn": 2,
                "precision": 1.0, "recall": 1.0, "false_positive_rate": 0.0,
            },
        }

    monkeypatch.setattr(eval_track._eval, "run_baseline", _fake_run_baseline)
    record = eval_track.track(output_path=out, lang="de")
    assert record["lang"] == "de"


def test_track_record_has_version(tmp_path):
    """The version field in the record matches core.__version__."""
    out = str(tmp_path / "h.jsonl")
    record = eval_track.track(output_path=out)
    assert record["version"] == _core_pkg.__version__


def test_track_does_not_pollute_live_canon(tmp_path, monkeypatch):
    """eval_track.track() must not write eval fixtures into the configured DB.

    Regression: run_baseline() was called without switching to a temp DB, so
    it ingested the eval corpus into whatever VELANTRIM_DB was active.  The fix
    wraps run_baseline() in a TemporaryDirectory context that redirects both
    VELANTRIM_DB and VELANTRIM_L3_PATH.
    (Codex P2 fix: scripts/eval_track.py)
    """
    from core.memory import get_all_facts
    import core.memory as _mem
    import core.l3_graph as _l3

    # Snapshot the fact count BEFORE the eval run.
    before_count = len(get_all_facts())

    out = str(tmp_path / "h.jsonl")
    eval_track.track(output_path=out)

    # Reset singletons so we read from the same DB that was active before.
    _mem._L0.clear()
    _l3.reset_l3_graph()

    after_count = len(get_all_facts())
    assert after_count == before_count, (
        f"track() wrote {after_count - before_count} fact(s) into the live canon; "
        "it must use a temp DB instead."
    )
