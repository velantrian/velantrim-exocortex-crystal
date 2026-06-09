"""Tests for core/crypto.py — GDPR Art. 32 encryption at rest.

In this environment `cryptography` is unavailable, so the stdlib HMAC-SHA256
backend is exercised. The same round-trip / tamper tests pass on either backend.
"""
import json
import sqlite3

import pytest

from core import crypto, memory


_KEY = "correct horse battery staple"


@pytest.fixture
def enc(monkeypatch):
    """Enable encryption at rest for the duration of a test."""
    monkeypatch.setenv("VELANTRIM_ENCRYPTION_KEY", _KEY)
    return crypto


@pytest.fixture
def enc_stdlib(monkeypatch):
    """Enable encryption AND force the dependency-free HMAC-SHA256 backend, even
    where `cryptography` happens to be installed. This keeps the stdlib backend
    exercised on every machine (not only on CI, which omits `cryptography`)."""
    monkeypatch.setenv("VELANTRIM_ENCRYPTION_KEY", _KEY)
    monkeypatch.setattr(crypto, "_fernet", lambda: None)
    return crypto


# ─── crypto module ────────────────────────────────────────────────────────────

def test_disabled_by_default_is_identity(monkeypatch):
    monkeypatch.delenv("VELANTRIM_ENCRYPTION_KEY", raising=False)
    assert crypto.is_enabled() is False
    assert crypto.backend_name() is None
    assert crypto.encrypt("hello") == "hello"
    assert crypto.decrypt("hello") == "hello"


def test_round_trip(enc):
    assert crypto.is_enabled() is True
    token = crypto.encrypt("personal data")
    assert token != "personal data"
    assert token.startswith(("enc:f1:", "enc:h1:"))
    assert crypto.decrypt(token) == "personal data"


def test_round_trip_unicode_and_empty(enc):
    for text in ["", "тревога 🌿", "a" * 5000]:
        assert crypto.decrypt(crypto.encrypt(text)) == text


def test_ciphertext_is_nondeterministic(enc):
    # Random nonce/IV → encrypting the same plaintext twice differs.
    assert crypto.encrypt("same") != crypto.encrypt("same")


def test_tamper_is_detected(enc):
    token = crypto.encrypt("trustworthy")
    # Flip the first char of the base64 body (right after the "enc:xx:" prefix).
    # This position carries full-information nonce bits, so the flip always
    # changes the decoded bytes — unlike the padding-adjacent tail, where base64
    # redundancy can absorb a single-char change and mask the tamper.
    prefix_len = token.index(":", 4) + 1  # end of the "enc:f1:" / "enc:h1:" marker
    body = list(token)
    body[prefix_len] = "A" if body[prefix_len] != "A" else "B"
    tampered = "".join(body)
    with pytest.raises(ValueError, match="authentication failed"):
        crypto.decrypt(tampered)


def test_wrong_key_fails(monkeypatch):
    monkeypatch.setenv("VELANTRIM_ENCRYPTION_KEY", _KEY)
    token = crypto.encrypt("secret")
    monkeypatch.setenv("VELANTRIM_ENCRYPTION_KEY", "a different key")
    with pytest.raises(ValueError):
        crypto.decrypt(token)


# ─── stdlib HMAC backend (forced — covers the zero-dependency path everywhere) ──

def test_stdlib_round_trip(enc_stdlib):
    token = crypto.encrypt("hmac payload")
    assert token.startswith("enc:h1:")
    assert crypto.decrypt(token) == "hmac payload"


def test_stdlib_backend_name(enc_stdlib):
    assert crypto.backend_name() == "hmac-sha256"


def test_stdlib_tamper_is_detected(enc_stdlib):
    token = crypto.encrypt("trustworthy")
    prefix_len = token.index(":", 4) + 1
    body = list(token)
    body[prefix_len] = "A" if body[prefix_len] != "A" else "B"
    with pytest.raises(ValueError, match="authentication failed"):
        crypto.decrypt("".join(body))


def test_stdlib_wrong_key_fails(monkeypatch):
    monkeypatch.setenv("VELANTRIM_ENCRYPTION_KEY", _KEY)
    monkeypatch.setattr(crypto, "_fernet", lambda: None)
    token = crypto.encrypt("secret")
    monkeypatch.setenv("VELANTRIM_ENCRYPTION_KEY", "a different key")
    with pytest.raises(ValueError, match="authentication failed"):
        crypto.decrypt(token)


# ─── Fernet backend (only when `cryptography` is installed; CI omits it) ────────

def test_fernet_round_trip_when_available(monkeypatch):
    pytest.importorskip("cryptography")
    monkeypatch.setenv("VELANTRIM_ENCRYPTION_KEY", _KEY)
    if crypto._fernet() is None:
        pytest.skip("cryptography present but Fernet backend unusable here")
    token = crypto.encrypt("fernet payload")
    assert token.startswith("enc:f1:")
    assert crypto.decrypt(token) == "fernet payload"


def test_fernet_wrong_key_raises_uniform_valueerror(monkeypatch):
    # Regression: the Fernet path used to leak cryptography's InvalidToken; the
    # contract is a uniform ValueError("authentication failed") like the stdlib path.
    pytest.importorskip("cryptography")
    monkeypatch.setenv("VELANTRIM_ENCRYPTION_KEY", _KEY)
    if crypto._fernet() is None:
        pytest.skip("cryptography present but Fernet backend unusable here")
    token = crypto.encrypt("secret")
    monkeypatch.setenv("VELANTRIM_ENCRYPTION_KEY", "a different key")
    with pytest.raises(ValueError, match="authentication failed"):
        crypto.decrypt(token)


def test_plaintext_passthrough(enc):
    # A value without a scheme marker (legacy / pre-encryption) is returned as-is.
    assert crypto.decrypt("no marker here") == "no marker here"


def test_backend_name(enc):
    assert crypto.backend_name() in ("fernet", "hmac-sha256")


def test_non_string_passes_through(enc):
    # Non-string values (e.g. None) are returned unchanged by both ends.
    assert crypto.encrypt(None) is None
    assert crypto.decrypt(None) is None
    assert crypto.decrypt(123) == 123


# ─── integration with the L1 store ────────────────────────────────────────────

def test_store_encrypts_at_rest_and_reads_back(enc):
    memory.store_fact({"fact_id": "f1", "claim": "highly sensitive",
                       "source": "user", "metadata": {"pii": "value"}})

    # The raw SQLite row must NOT contain the plaintext (encrypted at rest).
    with sqlite3.connect(memory.SQLITE_PATH) as conn:
        row = conn.execute(
            "SELECT claim, metadata FROM facts WHERE fact_id='f1'").fetchone()
    raw_claim, raw_meta = row
    assert raw_claim != "highly sensitive"
    assert raw_claim.startswith(("enc:f1:", "enc:h1:"))
    assert "highly sensitive" not in raw_claim
    assert "value" not in raw_meta

    # Reading back through the API transparently decrypts (force the L1 path).
    memory._L0.clear()
    fact = memory.get_fact("f1")
    assert fact["claim"] == "highly sensitive"
    assert fact["metadata"] == {"pii": "value"}


def test_update_fact_keeps_ciphertext_at_rest(enc):
    memory.store_fact({"fact_id": "f1", "claim": "old", "source": "s"})
    memory.update_fact("f1", claim="new claim", metadata={"k": "v"})

    with sqlite3.connect(memory.SQLITE_PATH) as conn:
        raw = conn.execute(
            "SELECT claim FROM facts WHERE fact_id='f1'").fetchone()[0]
    assert "new claim" not in raw
    assert raw.startswith(("enc:f1:", "enc:h1:"))

    memory._L0.clear()
    assert memory.get_fact("f1")["claim"] == "new claim"


def test_get_all_facts_decrypts(enc):
    memory.store_fact({"fact_id": "f1", "claim": "alpha", "source": "s"})
    memory.store_fact({"fact_id": "f2", "claim": "beta", "source": "s"})
    memory._L0.clear()
    claims = {f["claim"] for f in memory.get_all_facts()}
    assert {"alpha", "beta"} <= claims


def test_plaintext_db_still_readable_after_enabling(monkeypatch):
    # A fact written WITHOUT encryption stays readable after encryption is on
    # (decrypt passes unmarked plaintext through) — no forced migration needed.
    monkeypatch.delenv("VELANTRIM_ENCRYPTION_KEY", raising=False)
    memory.store_fact({"fact_id": "f1", "claim": "legacy plain", "source": "s"})
    monkeypatch.setenv("VELANTRIM_ENCRYPTION_KEY", _KEY)
    memory._L0.clear()
    assert memory.get_fact("f1")["claim"] == "legacy plain"


def test_ropa_reports_encryption(enc):
    from core.compliance import record_of_processing
    ropa = record_of_processing()
    assert ropa["encryption_at_rest"] is True
    assert ropa["encryption_backend"] in ("fernet", "hmac-sha256")
    assert any("encryption at rest" in m for m in ropa["security_measures"])
