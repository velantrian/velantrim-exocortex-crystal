"""Tests for core/cli.py — the command-line interface."""
import json
import pytest

from core.cli import main


def test_cli_ingest_outputs_classification(capsys):
    rc = main(["ingest", "I feel anxious about the deadline"])
    assert rc == 0
    out = json.loads(capsys.readouterr().out)
    assert out["accepted"] is True
    assert out["claim_type"] == "EMOTION"
    assert out["truth_status"] == "SUBJECTIVE"


def test_cli_ask_returns_answer(capsys):
    main(["ingest", "Octopuses have three hearts"])
    main(["ask", "octopus hearts"])
    out = capsys.readouterr().out
    assert "hearts" in out.lower()


def test_cli_history_outputs_json(capsys):
    main(["ingest", "Pluto is a dwarf planet"])
    capsys.readouterr()                      # discard the ingest output
    main(["history", "nonexistent"])
    out = json.loads(capsys.readouterr().out)
    assert out == {"superseded_by": [], "supersedes": [],
                   "contradicts": [], "contradicted_by": []}


def test_cli_report_renders(capsys):
    main(["ingest", "Water boils at 100 degrees"])
    main(["report"])
    assert "MEMORY REPORT" in capsys.readouterr().out


def test_cli_requires_subcommand():
    with pytest.raises(SystemExit):
        main([])
