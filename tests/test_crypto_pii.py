# coding: utf-8
"""Tests for PII encryption helpers in services.crypto."""

from services.crypto import decrypt, decrypt_pii, encrypt, encrypt_pii


class TestPiiRoundtrip:
    def test_non_empty_string_roundtrip(self):
        enc = encrypt_pii("+998 90 123-45-67")
        assert enc != "+998 90 123-45-67"
        assert enc.startswith("pii1:")
        assert decrypt_pii(enc) == "+998 90 123-45-67"

    def test_none_passthrough(self):
        assert encrypt_pii(None) is None
        assert decrypt_pii(None) is None

    def test_empty_string_passthrough(self):
        assert encrypt_pii("") == ""
        assert decrypt_pii("") == ""

    def test_plaintext_decrypt_is_passthrough(self):
        """Rows written before migration are plaintext — must not raise."""
        assert decrypt_pii("Toshkent, Yunusobod 7") == "Toshkent, Yunusobod 7"
        assert decrypt_pii("Ivanov Ivan") == "Ivanov Ivan"

    def test_unicode(self):
        value = "Иванов Иван Иванович, Ташкент"
        assert decrypt_pii(encrypt_pii(value)) == value

    def test_long_value(self):
        value = "Very long address, " * 20
        enc = encrypt_pii(value)
        assert len(enc) > len(value)
        assert decrypt_pii(enc) == value

    def test_pii_prefix_distinct_from_v1(self):
        """PII ciphertext shouldn't be mistaken for secret ciphertext."""
        enc = encrypt_pii("hello")
        assert enc.startswith("pii1:")
        assert not enc.startswith("v1:")

    def test_encrypt_secret_still_works(self):
        """The existing encrypt/decrypt pair must be unaffected by new helpers."""
        secret = "password-with-bangs!"
        assert decrypt(encrypt(secret)) == secret
