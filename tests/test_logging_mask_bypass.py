# coding: utf-8
"""Audit CORE-6 / CORE-11 — the SensitiveDataFilter mask must not be bypassed.

Regression coverage for three concrete leak vectors that the previous
implementation missed:

  * (a) A non-string log arg (dict / object) carrying a secret was ``str()``'d
    into the final message *after* per-arg masking, so the credential slipped
    through verbatim: ``log.info("ctx=%s", {"password": "..."})``.
  * (b) A secret raised inside an exception reached the sink through the
    formatted traceback, which the message-level filter never touched.

These tests drive the *real* filter + formatter pipeline (no mocks of the code
under test) and assert the secret is genuinely present in the raw payload but
absent from the emitted line — a true negative test, not a tautology.

CORE-11: stale ``bot_*.log`` files are pruned on startup — verified against a
temp directory so no real log files are touched.
"""

from __future__ import annotations

import json
import logging
import os
import sys

import pytest

from services.logging_config import (
    JsonFormatter,
    SensitiveDataFilter,
    TextFormatter,
    _prune_old_log_files,
    setup_logging,
)


def _make_record(msg: str, args, exc_info=None) -> logging.LogRecord:
    return logging.LogRecord(
        name="test",
        level=logging.ERROR,
        pathname=__file__,
        lineno=1,
        msg=msg,
        args=args,
        exc_info=exc_info,
    )


# ---------------------------------------------------------------------------
# CORE-6 (a): non-string dict arg carrying a secret
# ---------------------------------------------------------------------------


def test_dict_arg_password_is_masked_in_text_output():
    payload = {"password": "hunter2", "user": "alice"}  # pragma: allowlist secret
    # Sanity: the secret really is in the interpolated payload.
    assert "hunter2" in ("ctx=%s" % payload)

    record = _make_record("ctx=%s", (payload,))
    assert SensitiveDataFilter().filter(record) is True

    out = TextFormatter("%(message)s").format(record)
    assert "hunter2" not in out
    assert "***" in out


@pytest.mark.parametrize(
    "message",
    [
        "X-TeLeGrAm-InItDaTa: canary.jwt.secret",
        "GET /stream?tgInitData=canary.jwt.secret&run=1",
        "GET /stream?accessToken=canary.jwt.secret",
        "GET /stream?tgInitData%3Dcanary.jwt.secret",
        "refresh_token=canary.jwt.secret",
        "Authorization: Basic canary.jwt.secret",
        "Cookie: session=canary.jwt.secret",
        "Set-Cookie: refresh=canary.jwt.secret; HttpOnly",
    ],
)
def test_telegram_and_web_credentials_are_masked(message: str):
    record = _make_record(message, ())
    SensitiveDataFilter().filter(record)
    out = TextFormatter("%(message)s").format(record)
    assert "canary.jwt.secret" not in out
    assert "***" in out


def test_dict_arg_token_is_masked():
    payload = {"token": "abc123secret", "ok": True}
    record = _make_record("state=%s", (payload,))
    SensitiveDataFilter().filter(record)
    out = TextFormatter("%(message)s").format(record)
    assert "abc123secret" not in out


def test_dict_arg_secret_masked_in_json_output():
    payload = {"api_key": "sk-live-DEADBEEF", "n": 3}  # pragma: allowlist secret
    record = _make_record("cfg=%s", (payload,))
    SensitiveDataFilter().filter(record)
    out = JsonFormatter().format(record)
    data = json.loads(out)
    assert "sk-live-DEADBEEF" not in out
    assert "sk-live-DEADBEEF" not in data["message"]


def test_object_arg_with_secret_repr_is_masked():
    """An arbitrary object whose repr embeds a secret must be masked once it is
    ``str()``'d into the message."""

    class Conn:
        def __repr__(self) -> str:
            return "Conn(password='topsecret')"  # pragma: allowlist secret

    record = _make_record("connecting %s", (Conn(),))
    SensitiveDataFilter().filter(record)
    out = TextFormatter("%(message)s").format(record)
    assert "topsecret" not in out


# ---------------------------------------------------------------------------
# CORE-6 (b): secret inside an exception traceback
# ---------------------------------------------------------------------------


def test_exception_traceback_secret_is_masked_text():
    try:
        raise ValueError("db connect failed password=SuperSecret123")
    except ValueError:
        exc_info = sys.exc_info()

    record = _make_record("operation failed", None, exc_info=exc_info)
    SensitiveDataFilter().filter(record)
    out = TextFormatter("%(message)s").format(record)

    # The traceback line carrying the secret is present but redacted.
    assert "SuperSecret123" not in out
    assert "password=***" in out


def test_exception_traceback_bearer_masked_json():
    try:
        raise RuntimeError("auth rejected: Bearer eyJhbGciOiJ_LEAK_TOKEN")
    except RuntimeError:
        exc_info = sys.exc_info()

    record = _make_record("boom", None, exc_info=exc_info)
    SensitiveDataFilter().filter(record)
    out = JsonFormatter().format(record)
    data = json.loads(out)

    assert "eyJhbGciOiJ_LEAK_TOKEN" not in out
    assert "Bearer ***" in data["exception"]


# ---------------------------------------------------------------------------
# Existing message masking still works after the getMessage() rewrite
# ---------------------------------------------------------------------------


def test_string_arg_tin_still_masked():
    record = _make_record("TIN=%s", ("123456789",))
    SensitiveDataFilter().filter(record)
    out = TextFormatter("%(message)s").format(record)
    assert "***TIN***" in out
    assert "123456789" not in out


def test_debug_unmask_hatch_still_bypasses():
    record = logging.LogRecord("t", logging.DEBUG, __file__, 1, "password=raw", None, None)
    assert SensitiveDataFilter(unmask_debug=True).filter(record) is True
    out = TextFormatter("%(message)s").format(record)
    assert "password=raw" in out  # untouched at DEBUG when hatch enabled


def test_setup_logging_forces_debug_unmask_off_in_prod(monkeypatch, tmp_path):
    root = logging.getLogger()
    old_handlers = list(root.handlers)
    old_level = root.level
    for handler in old_handlers:
        root.removeHandler(handler)

    monkeypatch.setenv("APP_ENV", "prod")
    monkeypatch.setenv("LOG_UNMASK_DEBUG", "true")

    try:
        setup_logging(logs_folder=str(tmp_path), level="DEBUG")
        logging.getLogger("sec6").debug("password=raw")
        for handler in root.handlers:
            handler.flush()

        log_file = next(tmp_path.glob("bot_*.log"))
        out = log_file.read_text(encoding="utf-8")
        assert "password=raw" not in out
        assert "password=***" in out
    finally:
        for handler in list(root.handlers):
            root.removeHandler(handler)
            handler.close()
        for handler in old_handlers:
            root.addHandler(handler)
        root.setLevel(old_level)


# ---------------------------------------------------------------------------
# CORE-11: stale log-file pruning
# ---------------------------------------------------------------------------


def test_prune_old_log_files_keeps_newest(tmp_path):
    folder = str(tmp_path)
    # 25 timestamped files with increasing mtime.
    for i in range(25):
        p = os.path.join(folder, f"bot_2026-07-11_00-00-{i:02d}.log")
        with open(p, "w", encoding="utf-8") as fh:
            fh.write("x")
        os.utime(p, (1_000_000 + i, 1_000_000 + i))
    # An unrelated file must survive.
    other = os.path.join(folder, "keepme.txt")
    with open(other, "w", encoding="utf-8") as fh:
        fh.write("y")

    _prune_old_log_files(folder, keep=20)

    remaining = sorted(n for n in os.listdir(folder) if n.startswith("bot_"))
    assert len(remaining) == 20
    # Newest 20 (indices 05..24) survive; oldest 5 pruned.
    assert "bot_2026-07-11_00-00-24.log" in remaining
    assert "bot_2026-07-11_00-00-00.log" not in remaining
    assert os.path.exists(other)


def test_prune_old_log_files_missing_dir_is_noop():
    # Best-effort: a non-existent folder must not raise.
    _prune_old_log_files("/nonexistent/path/for/test", keep=5)
