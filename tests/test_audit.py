"""Tests for core/audit.py — tamper-evident audit log (GDPR Art. 5(2)/24/30)."""
import sqlite3

import pytest

from core import audit, memory
from core.erasure import erase_fact
from core.compliance import restrict_processing, unrestrict_processing, record_of_processing


def _seed(fact_id, claim="a claim"):
    memory.store_fact({"fact_id": fact_id, "claim": claim, "source": "s",
                       "epistemic_state": "Validated"})


# ─── chain basics ─────────────────────────────────────────────────────────────

def test_empty_log_verifies():
    v = audit.verify_audit_log()
    assert v["ok"] is True
    assert v["length"] == 0


def test_append_and_verify_chain():
    audit.append_event("erase", "f1", {"reason": "r"})
    audit.append_event("restrict", "f2", {"reason": "r"})
    audit.append_event("unrestrict", "f2", {})

    v = audit.verify_audit_log()
    assert v["ok"] is True
    assert v["length"] == 3

    entries = audit.audit_log()
    assert [e["seq"] for e in entries] == [1, 2, 3]
    assert [e["event"] for e in entries] == ["erase", "restrict", "unrestrict"]
    # First entry links to genesis; each subsequent links to the previous.
    assert entries[0]["prev_hash"] == "0" * 64
    assert entries[1]["prev_hash"] == entries[0]["entry_hash"]
    assert entries[2]["prev_hash"] == entries[1]["entry_hash"]


def test_detail_is_content_free():
    audit.append_event("erase", "f1", {"reason": "gdpr", "actor": "dpo"})
    assert "claim" not in str(audit.audit_log())


# ─── tamper detection ─────────────────────────────────────────────────────────

def _raw_exec(sql, params=()):
    with sqlite3.connect(memory.SQLITE_PATH) as conn:
        conn.execute(sql, params)
        conn.commit()


def test_editing_an_entry_breaks_the_chain():
    audit.append_event("erase", "f1", {"reason": "one"})
    audit.append_event("erase", "f2", {"reason": "two"})

    # Tamper: alter the stored detail of entry #1 without updating its hash.
    _raw_exec("UPDATE audit_log SET detail = ? WHERE seq = 1",
              ('{"reason": "TAMPERED"}',))

    v = audit.verify_audit_log()
    assert v["ok"] is False
    assert v["broken_at"] == 1
    assert "entry_hash" in v["error"]


def test_deleting_an_entry_is_detected():
    audit.append_event("erase", "f1", {})
    audit.append_event("erase", "f2", {})
    _raw_exec("DELETE FROM audit_log WHERE seq = 1")

    v = audit.verify_audit_log()
    assert v["ok"] is False
    assert v["broken_at"] == 2  # first surviving row is seq 2, expected 1


def test_broken_prev_hash_link_is_detected():
    audit.append_event("erase", "f1", {})
    audit.append_event("erase", "f2", {})
    # Repoint entry #2's prev_hash so it no longer links to entry #1.
    _raw_exec("UPDATE audit_log SET prev_hash = ? WHERE seq = 2", ("ab" * 32,))
    v = audit.verify_audit_log()
    assert v["ok"] is False
    assert v["broken_at"] == 2
    assert "prev_hash" in v["error"]


def test_relinking_entry_hash_is_detected():
    audit.append_event("erase", "f1", {})
    audit.append_event("erase", "f2", {})
    # Forge entry #1's entry_hash to a plausible-looking value.
    _raw_exec("UPDATE audit_log SET entry_hash = ? WHERE seq = 1", ("deadbeef" * 8,))
    v = audit.verify_audit_log()
    assert v["ok"] is False
    assert v["broken_at"] == 1


# ─── signing ──────────────────────────────────────────────────────────────────

def test_signed_entries_verify_with_key(monkeypatch):
    monkeypatch.setenv("VELANTRIM_AUDIT_KEY", "audit-secret")
    audit.append_event("erase", "f1", {"reason": "r"})
    audit.append_event("restrict", "f2", {})

    v = audit.verify_audit_log()
    assert v["ok"] is True
    assert v["signed"] is True
    assert v["verified"] is True
    assert all(e["signature"] for e in audit.audit_log())


def test_forged_signature_is_detected(monkeypatch):
    monkeypatch.setenv("VELANTRIM_AUDIT_KEY", "audit-secret")
    audit.append_event("erase", "f1", {})
    _raw_exec("UPDATE audit_log SET signature = ? WHERE seq = 1", ("00" * 32,))
    v = audit.verify_audit_log()
    assert v["ok"] is False
    assert "signature" in v["error"]


def test_unsigned_when_no_key():
    audit.append_event("erase", "f1", {})
    v = audit.verify_audit_log()
    assert v["ok"] is True
    assert v["signed"] is False
    assert v["verified"] is False


# ─── integration ──────────────────────────────────────────────────────────────

def test_erase_appends_audit_event():
    _seed("f1")
    erase_fact("f1", reason="user_request")
    events = [e for e in audit.audit_log() if e["event"] == "erase"]
    assert len(events) == 1
    assert events[0]["fact_id"] == "f1"
    assert events[0]["detail"]["reason"] == "user_request"
    assert audit.verify_audit_log()["ok"] is True


def test_restrict_and_unrestrict_append_events():
    _seed("f1")
    restrict_processing("f1")
    unrestrict_processing("f1")
    events = [e["event"] for e in audit.audit_log()]
    assert "restrict" in events and "unrestrict" in events
    assert audit.verify_audit_log()["ok"] is True


def test_restrict_unknown_fact_does_not_log():
    restrict_processing("ghost")  # found=False → no state change → no event
    assert audit.audit_log() == []


def test_ropa_reports_audit_integrity():
    _seed("f1")
    erase_fact("f1")
    ropa = record_of_processing()
    assert ropa["audit_log"]["tamper_evident"] is True
    assert ropa["audit_log"]["integrity_verified"] is True
    assert ropa["audit_log"]["entries"] >= 1


def test_cli_audit_and_verify(capsys):
    import json
    from core.cli import main

    _seed("f1")
    erase_fact("f1")
    assert main(["audit"]) == 0
    log = json.loads(capsys.readouterr().out.strip())
    assert any(e["event"] == "erase" for e in log)

    assert main(["audit-verify"]) == 0
    v = json.loads(capsys.readouterr().out.strip())
    assert v["ok"] is True
