"""Tests for core/refusal_reasons.py — Refusal Reasons Taxonomy v0.1."""

import pytest

import core.refusal_reasons as rr

# ─── Expected reason codes ─────────────────────────────────────────────────────

ALL_CODES = [
    "NO_VERIFIED_CLAIM",
    "LLM_OUTPUT_NOT_EVIDENCE",
    "MISSING_SOURCE",
    "MISSING_PROVENANCE",
    "MISSING_EVIDENCE",
    "MISSING_TRACE",
    "RECEIPT_TAMPERED",
    "CONTRADICTION_UNRESOLVED",
    "UNSUPPORTED_SCHEMA_CHECK",
    "TRUTHGATE_REJECTED",
    "GUARDIAN_BLOCKED",
    "REQUIRES_HUMAN_REVIEW",
    "OUT_OF_SCOPE",
]


# ─── Taxonomy completeness ─────────────────────────────────────────────────────


class TestTaxonomyCompleteness:
    def test_exactly_13_reasons(self):
        assert len(rr.list_reasons()) == 13

    def test_all_expected_codes_present(self):
        codes = {r["code"] for r in rr.list_reasons()}
        for code in ALL_CODES:
            assert code in codes, f"Missing code: {code}"

    def test_no_unexpected_codes(self):
        codes = {r["code"] for r in rr.list_reasons()}
        assert codes == set(ALL_CODES)


# ─── Required fields ──────────────────────────────────────────────────────────


class TestRequiredFields:
    def test_each_reason_has_code(self):
        for r in rr.list_reasons():
            assert r["code"] and isinstance(r["code"], str)

    def test_each_reason_has_title(self):
        for r in rr.list_reasons():
            assert r["title"] and isinstance(r["title"], str)

    def test_each_reason_has_severity(self):
        for r in rr.list_reasons():
            assert r["severity"] in rr.SEVERITIES, (
                f"{r['code']} has unknown severity {r['severity']!r}"
            )

    def test_each_reason_has_description(self):
        for r in rr.list_reasons():
            assert r["description"] and isinstance(r["description"], str)

    def test_each_reason_has_suggestion(self):
        for r in rr.list_reasons():
            assert r["suggestion"] and isinstance(r["suggestion"], str)


# ─── Severity coverage ────────────────────────────────────────────────────────


class TestSeverityCoverage:
    def test_severities_constant_contains_four_levels(self):
        assert rr.SEVERITIES == frozenset({"INFO", "WARN", "ERROR", "CRITICAL"})

    def test_at_least_one_info(self):
        assert any(r["severity"] == "INFO" for r in rr.list_reasons())

    def test_at_least_one_warn(self):
        assert any(r["severity"] == "WARN" for r in rr.list_reasons())

    def test_at_least_one_error(self):
        assert any(r["severity"] == "ERROR" for r in rr.list_reasons())

    def test_at_least_one_critical(self):
        assert any(r["severity"] == "CRITICAL" for r in rr.list_reasons())

    def test_known_severities_for_key_codes(self):
        assert rr.get_reason("LLM_OUTPUT_NOT_EVIDENCE")["severity"] == "ERROR"
        assert rr.get_reason("RECEIPT_TAMPERED")["severity"] == "CRITICAL"
        assert rr.get_reason("MISSING_EVIDENCE")["severity"] == "WARN"
        assert rr.get_reason("NO_VERIFIED_CLAIM")["severity"] == "INFO"
        assert rr.get_reason("GUARDIAN_BLOCKED")["severity"] == "CRITICAL"
        assert rr.get_reason("CONTRADICTION_UNRESOLVED")["severity"] == "ERROR"


# ─── get_reason ───────────────────────────────────────────────────────────────


class TestGetReason:
    def test_returns_dict_for_known_code(self):
        r = rr.get_reason("MISSING_SOURCE")
        assert isinstance(r, dict)

    def test_returned_dict_has_all_fields(self):
        r = rr.get_reason("MISSING_SOURCE")
        assert set(r) >= {"code", "title", "severity", "description", "suggestion"}

    def test_raises_key_error_for_unknown(self):
        with pytest.raises(KeyError):
            rr.get_reason("NONEXISTENT_CODE")

    def test_returns_copy_not_original(self):
        r1 = rr.get_reason("MISSING_SOURCE")
        r1["title"] = "mutated"
        r2 = rr.get_reason("MISSING_SOURCE")
        assert r2["title"] != "mutated"

    @pytest.mark.parametrize("code", ALL_CODES)
    def test_get_reason_for_every_code(self, code):
        r = rr.get_reason(code)
        assert r["code"] == code


# ─── is_valid_reason ──────────────────────────────────────────────────────────


class TestIsValidReason:
    def test_returns_true_for_known_code(self):
        assert rr.is_valid_reason("LLM_OUTPUT_NOT_EVIDENCE") is True

    def test_returns_false_for_unknown_code(self):
        assert rr.is_valid_reason("MADE_UP_CODE") is False

    def test_returns_false_for_empty_string(self):
        assert rr.is_valid_reason("") is False

    @pytest.mark.parametrize("code", ALL_CODES)
    def test_all_codes_are_valid(self, code):
        assert rr.is_valid_reason(code) is True


# ─── list_reasons ─────────────────────────────────────────────────────────────


class TestListReasons:
    def test_returns_list(self):
        assert isinstance(rr.list_reasons(), list)

    def test_returns_copies_not_originals(self):
        lst = rr.list_reasons()
        lst[0]["title"] = "mutated"
        lst2 = rr.list_reasons()
        assert lst2[0]["title"] != "mutated"

    def test_order_is_stable(self):
        codes1 = [r["code"] for r in rr.list_reasons()]
        codes2 = [r["code"] for r in rr.list_reasons()]
        assert codes1 == codes2

    def test_first_code_is_no_verified_claim(self):
        assert rr.list_reasons()[0]["code"] == "NO_VERIFIED_CLAIM"


# ─── format_reason ────────────────────────────────────────────────────────────


class TestFormatReason:
    def test_returns_string(self):
        assert isinstance(rr.format_reason("MISSING_SOURCE"), str)

    def test_contains_severity_bracket(self):
        s = rr.format_reason("MISSING_SOURCE")
        assert "[ERROR]" in s

    def test_contains_code(self):
        s = rr.format_reason("MISSING_SOURCE")
        assert "MISSING_SOURCE" in s

    def test_contains_description(self):
        r = rr.get_reason("MISSING_SOURCE")
        s = rr.format_reason("MISSING_SOURCE")
        assert r["description"] in s

    def test_format_structure(self):
        s = rr.format_reason("RECEIPT_TAMPERED")
        assert s.startswith("[CRITICAL] RECEIPT_TAMPERED:")

    def test_raises_key_error_for_unknown(self):
        with pytest.raises(KeyError):
            rr.format_reason("NO_SUCH_CODE")

    @pytest.mark.parametrize("code", ALL_CODES)
    def test_format_reason_for_every_code(self, code):
        s = rr.format_reason(code)
        r = rr.get_reason(code)
        expected_prefix = f"[{r['severity']}] {code}:"
        assert s.startswith(expected_prefix)


# ─── Module-level constants ───────────────────────────────────────────────────


class TestModuleConstants:
    def test_constants_match_index_codes(self):
        for code in ALL_CODES:
            assert hasattr(rr, code), f"Module constant {code} not found"
            assert getattr(rr, code) == code

    def test_no_unexpected_string_constants(self):
        module_str_consts = {
            k for k, v in rr.__dict__.items()
            if isinstance(v, str) and k.isupper() and not k.startswith("_")
        }
        assert module_str_consts == set(ALL_CODES)
