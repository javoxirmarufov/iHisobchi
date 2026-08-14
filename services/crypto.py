# coding: utf-8
"""BusinessHub v3 - Fernet encryption for secrets (passwords, tokens, SIDs)

Supports key rotation: new encryptions use the current key with a "v1:" prefix.
Decryption tries the current key first, then falls back to the old key for
data encrypted before rotation. Legacy ciphertexts (no prefix) are also supported.
"""

from __future__ import annotations

import logging
from typing import Optional

from cryptography.fernet import Fernet, InvalidToken

from config import ENCRYPTION_KEY

log = logging.getLogger("crypto")

_fernet_current = Fernet(ENCRYPTION_KEY.encode())

# Optional old key for rotation — allows decrypting data encrypted with the previous key
_fernet_old = None
try:
    from config import ENCRYPTION_KEY_OLD

    if ENCRYPTION_KEY_OLD:
        _fernet_old = Fernet(ENCRYPTION_KEY_OLD.encode())
except (ImportError, AttributeError):
    pass

_PREFIX = "v1:"
_BINARY_PREFIX = b"bin1:"


def _bump_old_key_metric() -> None:
    """Increment the Prometheus counter for ENCRYPTION_KEY_OLD decrypts.

    Swallows all failures — metrics are best-effort and must not break
    real decryption. During unit tests ``services.metrics`` is importable
    but the Counter may not be incrementable (test registry); logging at
    DEBUG level keeps noise out of the test output.
    """
    try:
        from services.metrics import didox_encryption_old_key_reads_total

        didox_encryption_old_key_reads_total.inc()
    except Exception:
        log.debug("didox_encryption_old_key_reads_total inc failed", exc_info=True)


def encrypt(plain: Optional[str]) -> Optional[str]:
    """Encrypt a string with Fernet. Returns None if input is None/empty."""
    if not plain:
        return plain
    return _PREFIX + _fernet_current.encrypt(plain.encode()).decode()


def decrypt(encrypted: Optional[str]) -> Optional[str]:
    """Decrypt a string. Returns None if input is None/empty.

    Handles three formats:
    - "v1:<ciphertext>" — current versioned format
    - "<ciphertext>" — legacy format (no prefix), tries current key then old key
    """
    if not encrypted:
        return encrypted

    if encrypted.startswith(_PREFIX):
        try:
            return _fernet_current.decrypt(encrypted[len(_PREFIX) :].encode()).decode()
        except InvalidToken:
            if _fernet_old:
                log.warning("Decryption used OLD encryption key — data should be re-encrypted")
                _bump_old_key_metric()
                return _fernet_old.decrypt(encrypted[len(_PREFIX) :].encode()).decode()
            raise

    # Legacy (no prefix) — try current key first, then old key
    try:
        return _fernet_current.decrypt(encrypted.encode()).decode()
    except InvalidToken:
        if _fernet_old:
            log.warning("Decryption used OLD encryption key — data should be re-encrypted")
            _bump_old_key_metric()
            return _fernet_old.decrypt(encrypted.encode()).decode()
        raise


def encrypt_bytes(plain: bytes) -> bytes:
    """Encrypt an opaque binary payload using the current Fernet key.

    Binary report artifacts deliberately use a distinct, byte-native prefix.
    This avoids accidental UTF-8 decoding of XLSX/XLS/CSV payloads and keeps
    the existing string/PII wire formats unchanged.
    """
    if not isinstance(plain, bytes):
        raise TypeError("plain must be bytes")
    return _BINARY_PREFIX + _fernet_current.encrypt(plain)


def decrypt_bytes(encrypted: bytes) -> bytes:
    """Decrypt a binary payload, falling back to the configured old key.

    Only the explicitly versioned binary format is accepted.  Unlike the
    legacy string helper, arbitrary plaintext bytes are never passed through:
    report storage must fail closed when a blob is not encrypted.
    """
    if not isinstance(encrypted, bytes):
        raise TypeError("encrypted must be bytes")
    if not encrypted.startswith(_BINARY_PREFIX):
        raise InvalidToken

    token = encrypted[len(_BINARY_PREFIX) :]
    try:
        return _fernet_current.decrypt(token)
    except InvalidToken:
        if _fernet_old:
            log.warning("Binary payload decrypted with OLD key — re-encrypt on next write")
            _bump_old_key_metric()
            return _fernet_old.decrypt(token)
        raise


# ---------------------------------------------------------------------------
# PII helpers (distinct prefix so we can identify/audit PII values separately
# and tolerate plaintext during the online migration window)
# ---------------------------------------------------------------------------

_PII_PREFIX = "pii1:"


def encrypt_pii(value: Optional[str]) -> Optional[str]:
    """Encrypt a PII string. Returns None for None, empty string for empty."""
    if value is None:
        return None
    if value == "":
        return ""
    return _PII_PREFIX + _fernet_current.encrypt(value.encode()).decode()


def decrypt_pii(value: Optional[str]) -> Optional[str]:
    """Decrypt a PII string. Pass-through for plaintext (backfill window)."""
    if value is None:
        return None
    if value == "":
        return ""
    if value.startswith(_PII_PREFIX):
        try:
            return _fernet_current.decrypt(value[len(_PII_PREFIX) :].encode()).decode()
        except InvalidToken:
            if _fernet_old:
                log.warning("PII decrypted with OLD key — re-encrypt on next write")
                _bump_old_key_metric()
                return _fernet_old.decrypt(value[len(_PII_PREFIX) :].encode()).decode()
            raise
    # Not a PII-encrypted blob — treat as plaintext (legacy or not-yet-migrated)
    return value
