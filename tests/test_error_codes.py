# coding: utf-8
"""Tests for services/error_codes.py — the user-facing error-code registry.

These strings are the face of every failure the bot shows; a missing
``uz`` translation or a duplicated code silently degrades support
("quote the code in brackets") for half the user base. The tests are
introspective on purpose: any NEW constant added to the module is
ratcheted into the same guarantees automatically.
"""

from __future__ import annotations

import re

from services import error_codes as ec

_CODE_RE = re.compile(r"^ERR-[ADXB]\d{2}$")


def _all_code_constants():
    out = {}
    for name in dir(ec):
        if name.startswith("_") or name.endswith("_MESSAGES"):
            continue
        val = getattr(ec, name)
        if isinstance(val, str) and val.startswith("ERR-"):
            out[name] = val
    return out


def _all_message_tables():
    return {name: getattr(ec, name) for name in dir(ec) if name.endswith("_MESSAGES")}


def test_registry_is_not_empty():
    assert len(_all_code_constants()) >= 20
    assert len(_all_message_tables()) >= 10


def test_every_code_matches_documented_pattern():
    # ERR-{category}{number}, category ∈ A/D/X/B (module docstring)
    for name, code in _all_code_constants().items():
        assert _CODE_RE.match(code), f"{name} = {code!r} breaks the ERR-<cat><NN> pattern"


def test_no_duplicate_codes():
    codes = list(_all_code_constants().values())
    dupes = {c for c in codes if codes.count(c) > 1}
    assert not dupes, f"duplicated error codes: {dupes}"


def test_every_message_table_has_both_languages_non_empty():
    for name, table in _all_message_tables().items():
        assert isinstance(table, dict), name
        assert set(table.keys()) >= {"ru", "uz"}, f"{name} is missing a language"
        for lang in ("ru", "uz"):
            assert isinstance(table[lang], str) and table[lang].strip(), f"{name}[{lang}] is empty"


def test_message_tables_pair_with_an_existing_code_constant():
    # SIGNUP_INVALID_EMAIL_MESSAGES must accompany SIGNUP_INVALID_EMAIL etc.
    codes = _all_code_constants()
    for name in _all_message_tables():
        base = name[: -len("_MESSAGES")]
        assert base in codes, f"{name} has no matching code constant {base}"


def test_format_error_renders_quotable_code():
    out = ec.format_error("Неверный пароль Didox", ec.ERR_AUTH_WRONG_PASSWORD)
    assert "Неверный пароль Didox" in out
    assert "<code>[ERR-A01]</code>" in out  # monospace, quotable in support chats
