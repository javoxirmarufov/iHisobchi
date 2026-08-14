# coding: utf-8
"""Verify ENCRYPTION_KEY rotation for the ``v1:``-prefixed secret format.

Regression guard for audit P2/SEC-1: before the fix, ``crypto.decrypt`` decrypted
``v1:`` ciphertexts with ``_fernet_current`` only, with no fallback to
``_fernet_old``. Rotating ENCRYPTION_KEY therefore made every ``v1:`` secret
(didox_password, didox_token, bank_sid, ...) undecryptable until re-encryption.
"""

from __future__ import annotations

import pytest
from cryptography.fernet import Fernet, InvalidToken

from services import crypto as crypto_module


def _make_v1_ciphertext(fernet: Fernet, plaintext: str) -> str:
    """Encrypt ``plaintext`` with ``fernet`` and prepend the ``v1:`` prefix,
    emulating a secret that was written before the key was rotated."""
    return crypto_module._PREFIX + fernet.encrypt(plaintext.encode()).decode()


def test_v1_decrypt_falls_back_to_old_key(monkeypatch) -> None:
    # Two distinct keys: the value was written with the OLD key, then the
    # operator rotated ENCRYPTION_KEY so current != the key that encrypted it.
    old_fernet = Fernet(Fernet.generate_key())
    new_fernet = Fernet(Fernet.generate_key())

    plaintext = "s3cr3t-didox-password!"
    ciphertext = _make_v1_ciphertext(old_fernet, plaintext)

    monkeypatch.setattr(crypto_module, "_fernet_current", new_fernet)
    monkeypatch.setattr(crypto_module, "_fernet_old", old_fernet)

    # Sanity: current key genuinely cannot decrypt it — proving the fallback
    # (not the current key) is what returns the value.
    with pytest.raises(InvalidToken):
        new_fernet.decrypt(ciphertext[len(crypto_module._PREFIX) :].encode())

    assert crypto_module.decrypt(ciphertext) == plaintext


def test_v1_decrypt_without_old_key_still_raises(monkeypatch) -> None:
    # No ENCRYPTION_KEY_OLD configured: a v1: ciphertext the current key cannot
    # decrypt must surface InvalidToken rather than silently return garbage.
    wrong_fernet = Fernet(Fernet.generate_key())
    new_fernet = Fernet(Fernet.generate_key())

    ciphertext = _make_v1_ciphertext(wrong_fernet, "value")

    monkeypatch.setattr(crypto_module, "_fernet_current", new_fernet)
    monkeypatch.setattr(crypto_module, "_fernet_old", None)

    with pytest.raises(InvalidToken):
        crypto_module.decrypt(ciphertext)
