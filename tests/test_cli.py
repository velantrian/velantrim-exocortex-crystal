"""Tests for core/cli.py — the command-line interface."""
import io
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
    # Seed via core.ingest directly with source_status="EXTERNAL": the plain
    # CLI `ingest` subcommand has no --source-status flag, and a fact ingested
    # through it defaults to USER_REPORTED -> truth_status USER_CLAIMED, which
    # CanonicalView strict grounding (core/canonical_view.py) now correctly
    # excludes from answer grounding. This test is about the `ask` subcommand
    # printing the answer text, not about write-path classification — seed
    # with genuinely verifiable content so the read path under test has
    # something to ground on.
    from core import evidence
    from core.ingest import ingest
    admitted = ingest("Octopuses have three hearts", source_status="EXTERNAL")
    evidence.attach_evidence(
        admitted["fact"]["fact_id"], "file://octopus.txt",
        source_text="Octopus source", section="fixture",
    )
    capsys.readouterr()
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


# ─── Reviewer tooling: trace (read-only pretty-printer) ───────────────────────

def test_cli_trace_from_receipt_file_human(tmp_path, capsys):
    receipt = {"citations": [
        {"fact_id": "f1", "source": "src", "epistemic_state": "Validated",
         "truth_status": "VERIFIED"}]}
    p = tmp_path / "receipt.json"
    p.write_text(json.dumps(receipt), encoding="utf-8")
    rc = main(["trace", str(p)])
    assert rc == 0
    out = capsys.readouterr().out
    assert "TRACE:" in out
    assert "f1" in out


def test_cli_trace_json_flag_from_trace_list(tmp_path, capsys):
    trace = [{"fact_id": "f1", "source": "s", "epistemic_state": "Observed",
              "confidence": 0.5}]
    p = tmp_path / "trace.json"
    p.write_text(json.dumps(trace), encoding="utf-8")
    rc = main(["trace", str(p), "--json"])
    assert rc == 0
    assert json.loads(capsys.readouterr().out) == trace


def test_cli_trace_dict_with_trace_key(tmp_path, capsys):
    payload = {"trace": [{"fact_id": "f9", "source": "s",
                          "epistemic_state": "Validated", "confidence": 0.9}]}
    p = tmp_path / "payload.json"
    p.write_text(json.dumps(payload), encoding="utf-8")
    rc = main(["trace", str(p), "--json"])
    assert rc == 0
    assert json.loads(capsys.readouterr().out)[0]["fact_id"] == "f9"


def test_cli_trace_from_stdin(monkeypatch, capsys):
    trace = [{"fact_id": "fx", "source": "s", "epistemic_state": "Observed",
              "confidence": 0.3}]
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps(trace)))
    rc = main(["trace"])                      # default file == "-"
    assert rc == 0
    assert "fx" in capsys.readouterr().out


def test_cli_trace_unrecognized_payload(tmp_path, capsys):
    p = tmp_path / "bad.json"
    p.write_text("123", encoding="utf-8")     # int — not a trace/receipt
    rc = main(["trace", str(p)])
    assert rc == 1
    assert "error" in json.loads(capsys.readouterr().out)


# ─── Evidence (GDPR Art. 18 redaction) ────────────────────────────────────────

def test_cli_evidence_returns_empty_for_restricted_fact(capsys):
    from core import evidence
    from core.compliance import restrict_processing

    main(["ingest", "A restricted claim with a source"])
    fid = json.loads(capsys.readouterr().out)["fact_id"]
    evidence.attach_evidence(fid, "private/notes.txt")
    restrict_processing(fid, reason="dispute")

    rc = main(["evidence", fid])
    assert rc == 0
    assert json.loads(capsys.readouterr().out) == []


def test_cli_evidence_returns_rows_for_unrestricted_fact(capsys):
    from core import evidence

    main(["ingest", "An ordinary claim with a source"])
    fid = json.loads(capsys.readouterr().out)["fact_id"]
    evidence.attach_evidence(fid, "public/notes.txt")

    rc = main(["evidence", fid])
    assert rc == 0
    rows = json.loads(capsys.readouterr().out)
    assert rows and rows[0]["source_uri"] == "public/notes.txt"


def test_cli_evidence_verify_does_not_expose_source_uri_for_restricted_fact(capsys):
    from core import evidence
    from core.compliance import restrict_processing

    main(["ingest", "A restricted claim to be verified"])
    fid = json.loads(capsys.readouterr().out)["fact_id"]
    evidence.attach_evidence(fid, "private/source.txt")
    restrict_processing(fid, reason="dispute")

    rc = main(["evidence", fid, "--verify"])
    assert rc == 0
    out = capsys.readouterr().out
    assert json.loads(out) == []
    assert "private/source.txt" not in out


def test_cli_evidence_verify_reports_status_for_unrestricted_fact(capsys):
    from core import evidence

    main(["ingest", "An ordinary claim to be verified"])
    fid = json.loads(capsys.readouterr().out)["fact_id"]
    evidence.attach_evidence(fid, "public/source.txt")

    rc = main(["evidence", fid, "--verify"])
    assert rc == 0
    report = json.loads(capsys.readouterr().out)
    assert report and report[0]["status"] == "ok"


# ─── Reviewer tooling: health (read-only diagnostic score) ────────────────────

def test_cli_health_score(capsys):
    main(["ingest", "Water boils at 100 degrees"])
    capsys.readouterr()                       # discard ingest output
    rc = main(["health"])
    assert rc == 0
    out = json.loads(capsys.readouterr().out)
    assert "health_score" in out
    assert "components" in out
    assert out["meaning"].startswith("diagnostic")
    assert 0.0 <= out["health_score"] <= 1.0
