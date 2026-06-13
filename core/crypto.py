# core/crypto.py
# Velantrim ExoCortex — Encryption at Rest (GDPR Art. 32)
#
# Application-level (field-level) encryption for personal-data columns in the L1
# SQLite store. The claim and metadata of a fact are encrypted before they touch
# disk and decrypted on read, so the database file at rest holds ciphertext for
# the personal-data-bearing fields. This is GDPR Art. 32 ("security of
# processing"): protection appropriate to the risk.
#
# OFF by default: with no key configured, encrypt()/decrypt() are the identity
# and the runtime stays standard-library only (no behaviour change). Set the key
# to enable:
#     export VELANTRIM_ENCRYPTION_KEY="<passphrase-or-fernet-key>"
#
# Two interchangeable backends behind one interface:
#   - Fernet (cryptography) — AES-128-CBC + HMAC. Used automatically when the
#     optional `cryptography` package is installed. Recommended.
#   - stdlib fallback — authenticated encryption built from standard primitives
#     only (HMAC-SHA256 keystream in CTR mode + encrypt-then-MAC). Keeps the
#     zero-dependency promise; install `cryptography` for AES-grade encryption.
#
# Both produce a self-describing token (scheme marker) so a store may contain a
# mix of plaintext (legacy / encryption-off) and ciphertext, and decrypt routes
# each value correctly. Tokens are tamper-evident: a wrong key or modified
# ciphertext fails authentication with a ValueError rather than returning garbage.

import os
import hmac
import struct
import base64
import hashlib
import secrets
from functools import lru_cache
from typing import Optional, Tuple

_ENV_KEY = "VELANTRIM_ENCRYPTION_KEY"

# Scheme markers (prefix of the stored token).
_MARK_FERNET = "enc:f1:"
_MARK_HMAC = "enc:h1:"

# Fixed application salt for passphrase → key derivation. A fixed salt means the
# same passphrase yields the same key across restarts (required to decrypt an
# existing store). Operators who want a per-deployment salt can supply a real
# 44-byte Fernet key directly instead of a passphrase.
_KDF_SALT = b"velantrim-exocortex-crystal::art32::v1"
_KDF_ITERS = 200_000


def _raw_key() -> Optional[bytes]:
    """The configured key material, or None if encryption is disabled."""
    value = os.environ.get(_ENV_KEY)
    return value.encode("utf-8") if value else None


def is_enabled() -> bool:
    """True if encryption at rest is configured (a key is present)."""
    return _raw_key() is not None


@lru_cache(maxsize=8)
def _derive(master: bytes) -> Tuple[bytes, bytes]:
    """Derive (enc_key, mac_key) from the master key via PBKDF2-HMAC-SHA256.

    Cached: PBKDF2 is deliberately slow, and the master key is constant for the
    process lifetime, so we derive once rather than on every encrypt/decrypt.
    """
    dk = hashlib.pbkdf2_hmac("sha256", master, _KDF_SALT, _KDF_ITERS, dklen=64)
    return dk[:32], dk[32:]


# ─── Fernet backend (preferred; optional dependency) ──────────────────────────

@lru_cache(maxsize=1)
def _fernet_class():  # pragma: no cover - depends on whether `cryptography` is usable
    """Import and cache the Fernet class once, or None if it is unusable.

    Cached so the import is attempted only once per process: a broken native
    backend prints a panic to stderr on import, and we don't want to repeat it
    on every call. Catches BaseException (a broken backend can raise pyo3
    PanicException, which is a BaseException) → graceful fallback to stdlib.
    """
    try:
        from cryptography.fernet import Fernet
        return Fernet
    except BaseException:
        return None


def _fernet():  # pragma: no cover - exercised only when `cryptography` is installed
    """Return a Fernet instance for the configured key, or None if unavailable."""
    master = _raw_key()
    if master is None:
        return None
    fernet_cls = _fernet_class()
    if fernet_cls is None:
        return None
    try:
        enc_key, _ = _derive(master)
        return fernet_cls(base64.urlsafe_b64encode(enc_key))
    except BaseException:
        return None


# ─── stdlib backend (zero-dependency authenticated encryption) ────────────────

def _keystream(enc_key: bytes, nonce: bytes, length: int) -> bytes:
    """CTR-mode keystream from HMAC-SHA256 (HMAC as a PRF over nonce‖counter)."""
    out = bytearray()
    counter = 0
    while len(out) < length:
        block = hmac.new(enc_key, nonce + struct.pack(">Q", counter),
                         hashlib.sha256).digest()
        out.extend(block)
        counter += 1
    return bytes(out[:length])


def _hmac_encrypt(plaintext: str) -> str:
    enc_key, mac_key = _derive(_raw_key())
    pt = plaintext.encode("utf-8")
    nonce = secrets.token_bytes(16)
    ct = bytes(a ^ b for a, b in zip(pt, _keystream(enc_key, nonce, len(pt))))
    tag = hmac.new(mac_key, nonce + ct, hashlib.sha256).digest()  # encrypt-then-MAC
    blob = nonce + tag + ct
    return _MARK_HMAC + base64.urlsafe_b64encode(blob).decode("ascii")


def _hmac_decrypt(token: str) -> str:
    enc_key, mac_key = _derive(_raw_key())
    blob = base64.urlsafe_b64decode(token[len(_MARK_HMAC):].encode("ascii"))
    nonce, tag, ct = blob[:16], blob[16:48], blob[48:]
    expected = hmac.new(mac_key, nonce + ct, hashlib.sha256).digest()
    if not hmac.compare_digest(tag, expected):
        raise ValueError("crypto: authentication failed (tampered data or wrong key)")
    pt = bytes(a ^ b for a, b in zip(ct, _keystream(enc_key, nonce, len(ct))))
    return pt.decode("utf-8")


# ─── Public API ───────────────────────────────────────────────────────────────

def backend_name() -> Optional[str]:
    """Name of the active backend, or None if encryption is disabled."""
    if not is_enabled():
        return None
    return "fernet" if _fernet() is not None else "hmac-sha256"


def encrypt(plaintext: str) -> str:
    """Encrypt a string for storage at rest. Identity when encryption is off."""
    if not isinstance(plaintext, str) or not is_enabled():
        return plaintext
    fernet = _fernet()
    if fernet is not None:  # pragma: no cover - Fernet path needs `cryptography`
        token = fernet.encrypt(plaintext.encode("utf-8")).decode("ascii")
        return _MARK_FERNET + token
    return _hmac_encrypt(plaintext)


def decrypt(value: str) -> str:
    """Decrypt a stored value. Plaintext (no marker) passes through unchanged."""
    if not isinstance(value, str):
        return value
    if value.startswith(_MARK_FERNET):  # pragma: no cover - needs `cryptography`
        fernet = _fernet()
        if fernet is None:
            raise ValueError(
                "crypto: value is Fernet-encrypted but `cryptography` is "
                "unavailable or the key is wrong")
        try:
            return fernet.decrypt(
                value[len(_MARK_FERNET):].encode("ascii")).decode("utf-8")
        except Exception as exc:  # noqa: BLE001 — Fernet raises InvalidToken; the
            # public contract is a uniform ValueError on auth failure, regardless
            # of backend, so callers don't depend on a backend-specific exception.
            raise ValueError(
                "crypto: authentication failed (tampered data or wrong key)"
            ) from exc
    if value.startswith(_MARK_HMAC):
        return _hmac_decrypt(value)
    return value  # legacy plaintext or encryption disabled
