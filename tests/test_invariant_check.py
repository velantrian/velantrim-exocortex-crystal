"""Tests for core/invariant_check.py and CLI invariant-check command."""

import json

import core.invariant_check as ic
import core.refusal_reasons as rr
from core.invariant_check import _aggregate_status, exit_code, run_checks


# ─── Helpers ─────────────────────────────────────────────────────────────────


def _fact(fact_id, truth_status, source_status, source="test-source"):
    return {
        "fact_id": fact_id,
        "claim": f"Test claim {fact_id}",
        "source": source,
        "truth_status": truth_status,
        "source_status": source_status,
        "claim_type": "WORLD_FACT",
    }


def _pass_report():
    return {
        "status": "PASS",
        "checked_at": "2026-06-13T00:00:00Z",
        "checks": [
            {"id": ic.ID_NO_LLM_VERIFIED, "status": "PASS", "violations": 0, "why": "ok"},
        ],
        "issues": [],
    }


def _fail_report():
    return {
        "status": "FAIL",
        "checked_at": "2026-06-13T00:00:00Z",
        "checks": [
            {"id": ic.ID_NO_LLM_VERIFIED, "status": "FAIL",
             "violations": 1, "why": "violation"},
        ],
        "issues": [
            {"check_id": ic.ID_NO_LLM_VERIFIED, "severity": "ERROR",
             "fact_id": "f:x", "why": "test", "suggestion": "test"},
        ],
    }


def _warn_report():
    return {
        "status": "WARN",
        "checked_at": "2026-06-13T00:00:00Z",
        "checks": [
            {"id": ic.ID_RECEIPT_INTEGRITY, "status": "SKIPPED_UNSUPPORTED",
             "violations": 0, "why": "no registry"},
        ],
        "issues": [],
    }


# ─── run_checks — clean pass ──────────────────────────────────────────────────


class TestCleanPass:
    def test_empty_facts_all_pass(self):
        report = run_checks([], _has_evidence=lambda fid: True)
        assert report["status"] == "PASS"
        by_id = {c["id"]: c for c in report["checks"]}
        assert by_id[ic.ID_NO_LLM_VERIFIED]["status"] == "PASS"
        assert by_id[ic.ID_VERIFIED_SOURCE]["status"] == "PASS"
        assert by_id[ic.ID_VERIFIED_EVIDENCE]["status"] == "PASS"
        assert report["issues"] == []

    def test_verified_external_with_source_and_evidence_passes(self):
        facts = [_fact("f:ok", "VERIFIED", "EXTERNAL", source="wiki")]
        report = run_checks(facts, _has_evidence=lambda fid: True)
        assert report["status"] == "PASS"

    def test_unverified_llm_fact_does_not_trigger(self):
        facts = [_fact("f:unv", "UNVERIFIED", "LLM_OUTPUT")]
        report = run_checks(facts, _has_evidence=lambda fid: True)
        by_id = {c["id"]: c for c in report["checks"]}
        assert by_id[ic.ID_NO_LLM_VERIFIED]["status"] == "PASS"


# ─── run_checks — violations ──────────────────────────────────────────────────


class TestViolations:
    def test_llm_output_verified_is_fail(self):
        """VERIFIED + LLM_OUTPUT → FAIL on no_llm_output_verified."""
        facts = [_fact("f:llm1", "VERIFIED", "LLM_OUTPUT")]
        report = run_checks(facts, _has_evidence=lambda fid: True)
        assert report["status"] == "FAIL"
        by_id = {c["id"]: c for c in report["checks"]}
        assert by_id[ic.ID_NO_LLM_VERIFIED]["status"] == "FAIL"
        assert by_id[ic.ID_NO_LLM_VERIFIED]["violations"] == 1
        assert any(i["fact_id"] == "f:llm1" for i in report["issues"])

    def test_multiple_llm_violations_all_counted(self):
        facts = [
            _fact("f:llm1", "VERIFIED", "LLM_OUTPUT"),
            _fact("f:llm2", "VERIFIED", "LLM_OUTPUT"),
            _fact("f:ok", "VERIFIED", "EXTERNAL"),
        ]
        report = run_checks(facts, _has_evidence=lambda fid: True)
        by_id = {c["id"]: c for c in report["checks"]}
        assert by_id[ic.ID_NO_LLM_VERIFIED]["violations"] == 2

    def test_missing_source_is_fail(self):
        """VERIFIED with empty source → FAIL on verified_requires_source."""
        facts = [_fact("f:nosrc", "VERIFIED", "EXTERNAL", source="")]
        report = run_checks(facts, _has_evidence=lambda fid: True)
        by_id = {c["id"]: c for c in report["checks"]}
        assert by_id[ic.ID_VERIFIED_SOURCE]["status"] == "FAIL"
        assert by_id[ic.ID_VERIFIED_SOURCE]["violations"] == 1

    def test_whitespace_only_source_is_missing(self):
        facts = [_fact("f:ws", "VERIFIED", "EXTERNAL", source="   ")]
        report = run_checks(facts, _has_evidence=lambda fid: True)
        by_id = {c["id"]: c for c in report["checks"]}
        assert by_id[ic.ID_VERIFIED_SOURCE]["status"] == "FAIL"

    def test_verified_without_evidence_is_fail(self):
        """VERIFIED fact with no evidence → FAIL on verified_requires_evidence."""
        facts = [_fact("f:noev", "VERIFIED", "EXTERNAL")]
        report = run_checks(facts, _has_evidence=lambda fid: False)
        by_id = {c["id"]: c for c in report["checks"]}
        assert by_id[ic.ID_VERIFIED_EVIDENCE]["status"] == "FAIL"
        assert by_id[ic.ID_VERIFIED_EVIDENCE]["violations"] == 1


# ─── run_checks — SKIPPED_UNSUPPORTED never fakes PASS ───────────────────────


class TestSkippedUnsupported:
    def test_receipt_integrity_always_skipped(self):
        report = run_checks([], _has_evidence=lambda fid: True)
        by_id = {c["id"]: c for c in report["checks"]}
        assert by_id[ic.ID_RECEIPT_INTEGRITY]["status"] == "SKIPPED_UNSUPPORTED"
        assert by_id[ic.ID_RECEIPT_INTEGRITY]["violations"] == 0

    def test_no_direct_l3_bypass_always_skipped(self):
        report = run_checks([], _has_evidence=lambda fid: True)
        by_id = {c["id"]: c for c in report["checks"]}
        assert by_id[ic.ID_NO_L3_BYPASS]["status"] == "SKIPPED_UNSUPPORTED"
        assert by_id[ic.ID_NO_L3_BYPASS]["violations"] == 0

    def test_skipped_checks_have_explanatory_why(self):
        report = run_checks([], _has_evidence=lambda fid: True)
        by_id = {c["id"]: c for c in report["checks"]}
        assert by_id[ic.ID_RECEIPT_INTEGRITY]["why"]
        assert by_id[ic.ID_NO_L3_BYPASS]["why"]


# ─── run_checks — output shape ────────────────────────────────────────────────


class TestOutputShape:
    def test_required_top_level_keys(self):
        report = run_checks([], _has_evidence=lambda fid: True)
        assert set(report) >= {"status", "checked_at", "checks", "issues"}

    def test_each_check_has_required_keys(self):
        report = run_checks([], _has_evidence=lambda fid: True)
        for c in report["checks"]:
            assert set(c) >= {"id", "status", "violations", "why"}

    def test_each_issue_has_required_keys(self):
        facts = [_fact("f:llm", "VERIFIED", "LLM_OUTPUT")]
        report = run_checks(facts, _has_evidence=lambda fid: True)
        for i in report["issues"]:
            assert set(i) >= {"check_id", "severity", "fact_id", "why", "suggestion"}

    def test_checked_at_ends_with_z(self):
        report = run_checks([], _has_evidence=lambda fid: True)
        assert report["checked_at"].endswith("Z")

    def test_no_mutation_of_input(self):
        import copy
        facts = [_fact("f:x", "VERIFIED", "EXTERNAL")]
        original = copy.deepcopy(facts)
        run_checks(facts, _has_evidence=lambda fid: True)
        assert facts == original

    def test_idempotent(self):
        """Same input always produces same status and violations."""
        facts = [_fact("f:x", "VERIFIED", "LLM_OUTPUT")]
        r1 = run_checks(facts, _has_evidence=lambda fid: True)
        r2 = run_checks(facts, _has_evidence=lambda fid: True)
        assert r1["status"] == r2["status"]
        assert [(c["id"], c["status"], c["violations"]) for c in r1["checks"]] == [
            (c["id"], c["status"], c["violations"]) for c in r2["checks"]
        ]


# ─── exit_code ────────────────────────────────────────────────────────────────


class TestAggregateStatus:
    def test_fail_when_any_fail(self):
        assert _aggregate_status({"FAIL", "PASS"}) == "FAIL"

    def test_warn_when_all_skipped(self):
        assert _aggregate_status({"SKIPPED_UNSUPPORTED"}) == "WARN"

    def test_pass_when_mix_of_pass_and_skipped(self):
        assert _aggregate_status({"PASS", "SKIPPED_UNSUPPORTED"}) == "PASS"

    def test_pass_when_only_pass(self):
        assert _aggregate_status({"PASS"}) == "PASS"


class TestExitCode:
    def test_pass_is_0(self):
        assert exit_code("PASS") == 0

    def test_warn_is_1(self):
        assert exit_code("WARN") == 1

    def test_fail_is_2(self):
        assert exit_code("FAIL") == 2

    def test_unknown_status_defaults_to_0(self):
        assert exit_code("SOMETHING_ELSE") == 0


class TestRealL3Integration:
    def test_run_checks_with_empty_l3(self, monkeypatch, tmp_path):
        """run_checks() (no args) loads from a real isolated L3 — PASS on empty store."""
        monkeypatch.setenv("VELANTRIM_DB", str(tmp_path / "l1.db"))
        monkeypatch.setenv("VELANTRIM_L3_PATH", str(tmp_path / "l3.db"))
        monkeypatch.setenv("VELANTRIM_L3_BACKEND", "sqlite")
        import core.l3_graph as _l3
        _l3.reset_l3_graph()
        try:
            report = run_checks()  # facts=None and _has_evidence=None → both loaded
            assert report["status"] == "PASS"
        finally:
            _l3.reset_l3_graph()


# ─── no restricted imports at module level ────────────────────────────────────


class TestModuleBoundaries:
    def test_does_not_expose_truth_gate_or_memory_at_module_level(self):
        forbidden = ("truth_gate", "memory", "l3_graph")
        for name in forbidden:
            assert name not in ic.__dict__, (
                f"core.invariant_check must not import {name} at module level"
            )


# ─── CLI integration ──────────────────────────────────────────────────────────


class TestCLI:
    def test_cli_exit_0_for_pass(self, monkeypatch, tmp_path, capsys):
        """Mocked PASS report → exit 0."""
        monkeypatch.setenv("VELANTRIM_DB", str(tmp_path / "l1.db"))
        monkeypatch.setattr(ic, "run_checks", lambda: _pass_report())
        from core.cli import main
        ret = main(["invariant-check"])
        assert ret == 0

    def test_cli_exit_1_for_warn(self, monkeypatch, tmp_path, capsys):
        """Mocked WARN report → exit 1."""
        monkeypatch.setenv("VELANTRIM_DB", str(tmp_path / "l1.db"))
        monkeypatch.setattr(ic, "run_checks", lambda: _warn_report())
        from core.cli import main
        ret = main(["invariant-check"])
        assert ret == 1

    def test_cli_exit_2_for_fail(self, monkeypatch, tmp_path, capsys):
        """Mocked FAIL report → exit 2."""
        monkeypatch.setenv("VELANTRIM_DB", str(tmp_path / "l1.db"))
        monkeypatch.setattr(ic, "run_checks", lambda: _fail_report())
        from core.cli import main
        ret = main(["invariant-check"])
        assert ret == 2

    def test_cli_output_is_valid_json(self, monkeypatch, tmp_path, capsys):
        """CLI always emits valid JSON."""
        monkeypatch.setenv("VELANTRIM_DB", str(tmp_path / "l1.db"))
        monkeypatch.setattr(ic, "run_checks", lambda: _pass_report())
        from core.cli import main
        main(["invariant-check"])
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert "status" in data
        assert "checks" in data


# ─── reason_code integration ──────────────────────────────────────────────────


class TestReasonCodeIntegration:
    def test_llm_fail_check_has_reason_code(self):
        facts = [_fact("f:llm", "VERIFIED", "LLM_OUTPUT")]
        report = run_checks(facts, _has_evidence=lambda fid: True)
        by_id = {c["id"]: c for c in report["checks"]}
        assert by_id[ic.ID_NO_LLM_VERIFIED]["reason_code"] == rr.LLM_OUTPUT_NOT_EVIDENCE

    def test_llm_fail_issue_has_reason_code(self):
        facts = [_fact("f:llm", "VERIFIED", "LLM_OUTPUT")]
        report = run_checks(facts, _has_evidence=lambda fid: True)
        issues = [i for i in report["issues"] if i["check_id"] == ic.ID_NO_LLM_VERIFIED]
        assert issues
        assert issues[0]["reason_code"] == rr.LLM_OUTPUT_NOT_EVIDENCE

    def test_missing_source_check_has_reason_code(self):
        facts = [_fact("f:ns", "VERIFIED", "EXTERNAL", source="")]
        report = run_checks(facts, _has_evidence=lambda fid: True)
        by_id = {c["id"]: c for c in report["checks"]}
        assert by_id[ic.ID_VERIFIED_SOURCE]["reason_code"] == rr.MISSING_SOURCE

    def test_missing_source_issue_has_reason_code(self):
        facts = [_fact("f:ns", "VERIFIED", "EXTERNAL", source="")]
        report = run_checks(facts, _has_evidence=lambda fid: True)
        issues = [i for i in report["issues"] if i["check_id"] == ic.ID_VERIFIED_SOURCE]
        assert issues
        assert issues[0]["reason_code"] == rr.MISSING_SOURCE

    def test_missing_evidence_check_has_reason_code(self):
        facts = [_fact("f:ne", "VERIFIED", "EXTERNAL")]
        report = run_checks(facts, _has_evidence=lambda fid: False)
        by_id = {c["id"]: c for c in report["checks"]}
        assert by_id[ic.ID_VERIFIED_EVIDENCE]["reason_code"] == rr.MISSING_EVIDENCE

    def test_missing_evidence_issue_has_reason_code(self):
        facts = [_fact("f:ne", "VERIFIED", "EXTERNAL")]
        report = run_checks(facts, _has_evidence=lambda fid: False)
        issues = [i for i in report["issues"] if i["check_id"] == ic.ID_VERIFIED_EVIDENCE]
        assert issues
        assert issues[0]["reason_code"] == rr.MISSING_EVIDENCE

    def test_receipt_integrity_skipped_has_reason_code(self):
        report = run_checks([], _has_evidence=lambda fid: True)
        by_id = {c["id"]: c for c in report["checks"]}
        assert by_id[ic.ID_RECEIPT_INTEGRITY]["reason_code"] == rr.UNSUPPORTED_SCHEMA_CHECK

    def test_no_l3_bypass_skipped_has_reason_code(self):
        report = run_checks([], _has_evidence=lambda fid: True)
        by_id = {c["id"]: c for c in report["checks"]}
        assert by_id[ic.ID_NO_L3_BYPASS]["reason_code"] == rr.UNSUPPORTED_SCHEMA_CHECK

    def test_pass_check_has_no_reason_code(self):
        facts = [_fact("f:ok", "VERIFIED", "EXTERNAL", source="wiki")]
        report = run_checks(facts, _has_evidence=lambda fid: True)
        by_id = {c["id"]: c for c in report["checks"]}
        # PASS checks must not carry a reason_code field
        assert "reason_code" not in by_id[ic.ID_NO_LLM_VERIFIED]
        assert "reason_code" not in by_id[ic.ID_VERIFIED_SOURCE]
        assert "reason_code" not in by_id[ic.ID_VERIFIED_EVIDENCE]

    def test_reason_codes_are_valid_rr_codes(self):
        facts = [
            _fact("f:llm", "VERIFIED", "LLM_OUTPUT"),
            _fact("f:ns", "VERIFIED", "EXTERNAL", source=""),
        ]
        report = run_checks(facts, _has_evidence=lambda fid: False)
        for check in report["checks"]:
            rc = check.get("reason_code")
            if rc:
                assert rr.is_valid_reason(rc), f"Invalid reason_code in check: {rc}"
        for issue in report["issues"]:
            rc = issue.get("reason_code")
            if rc:
                assert rr.is_valid_reason(rc), f"Invalid reason_code in issue: {rc}"
