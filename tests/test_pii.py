"""Tests for core/pii.py — PII detection & redaction (GDPR Art. 5 minimisation)."""
import json

import pytest

from core import pii, memory


# A Luhn-valid test card number (Visa test PAN).
_VALID_CARD = "4111 1111 1111 1111"


# ─── detection / redaction per type ───────────────────────────────────────────

def test_email_redacted():
    red, found = pii.redact("write to alice@example.com please")
    assert red == "write to [EMAIL] please"
    assert [f["type"] for f in found] == ["EMAIL"]


def test_phone_redacted():
    red, found = pii.redact("call me on +33 6 12 34 56 78 today")
    assert "[PHONE]" in red
    assert "12 34 56" not in red
    assert found[0]["type"] == "PHONE"


def test_valid_credit_card_redacted():
    red, found = pii.redact(f"card {_VALID_CARD} exp")
    assert red == "card [CREDIT_CARD] exp"
    assert found[0]["type"] == "CREDIT_CARD"


def test_invalid_card_not_treated_as_card():
    # Fails the Luhn check → not redacted as a card (16 digits, so also not phone).
    red, found = pii.redact("number 1234 5678 9012 3456 here")
    assert "CREDIT_CARD" not in [f["type"] for f in found]


def test_ipv4_redacted():
    red, found = pii.redact("server at 192.168.1.1 down")
    assert red == "server at [IPV4] down"
    assert found[0]["type"] == "IPV4"


def test_iban_redacted():
    red, found = pii.redact("IBAN DE89370400440532013000 ok")
    assert red == "IBAN [IBAN] ok"
    assert found[0]["type"] == "IBAN"


def test_plain_text_untouched():
    text = "The Eiffel Tower is in Paris."
    red, found = pii.redact(text)
    assert red == text
    assert found == []


# ─── overlap safety & content-free guarantees ─────────────────────────────────

def test_overlap_card_beats_phone():
    # A 16-digit card also matches the phone pattern; the more specific
    # (Luhn-validated) CREDIT_CARD must win, not PHONE.
    _red, found = pii.redact(f"pay {_VALID_CARD}")
    assert [f["type"] for f in found] == ["CREDIT_CARD"]


def test_multiple_pii_in_one_string():
    red, found = pii.redact("mail bob@x.io or call 0612345678")
    assert red == "mail [EMAIL] or call [PHONE]"
    assert {f["type"] for f in found} == {"EMAIL", "PHONE"}


def test_findings_are_content_free():
    _red, found = pii.redact("alice@example.com")
    blob = json.dumps(found)
    assert "alice@example.com" not in blob
    assert all(set(f) == {"type", "start", "end"} for f in found)


def test_summary_counts_by_type():
    _red, found = pii.redact("a@b.co and c@d.co and 192.168.0.1")
    assert pii.summary(found) == {"EMAIL": 2, "IPV4": 1}


# ─── enable flag ──────────────────────────────────────────────────────────────

def test_redaction_disabled_by_default(monkeypatch):
    monkeypatch.delenv("VELANTRIM_REDACT_PII", raising=False)
    assert pii.redaction_enabled() is False


def test_redaction_enable_flag(monkeypatch):
    monkeypatch.setenv("VELANTRIM_REDACT_PII", "1")
    assert pii.redaction_enabled() is True


# ─── ingest integration ───────────────────────────────────────────────────────

def test_ingest_redacts_when_enabled(monkeypatch):
    from core.ingest import ingest
    monkeypatch.setenv("VELANTRIM_REDACT_PII", "1")
    res = ingest("My email is dave@example.com")
    claim = res["fact"]["claim"]
    assert "dave@example.com" not in claim
    assert "[EMAIL]" in claim
    assert res["fact"]["metadata"]["pii_redacted"] == {"EMAIL": 1}


def test_ingest_keeps_text_when_disabled(monkeypatch):
    from core.ingest import ingest
    monkeypatch.delenv("VELANTRIM_REDACT_PII", raising=False)
    res = ingest("My email is dave@example.com")
    assert "dave@example.com" in res["fact"]["claim"]
    assert "metadata" not in res["fact"] or "pii_redacted" not in res["fact"].get("metadata", {})


def test_ropa_reports_pii_redaction(monkeypatch):
    from core.compliance import record_of_processing
    monkeypatch.setenv("VELANTRIM_REDACT_PII", "1")
    assert record_of_processing()["pii_redaction_at_ingest"] is True


def test_cli_redact(capsys):
    from core.cli import main
    assert main(["redact", "ping 10.0.0.1 or mail x@y.io"]) == 0
    out = json.loads(capsys.readouterr().out.strip())
    assert out["redacted"] == "ping [IPV4] or mail [EMAIL]"
    assert out["found"] == {"IPV4": 1, "EMAIL": 1}
