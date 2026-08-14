# coding: utf-8
"""BusinessHub v2 - Structured logging configuration"""

from __future__ import annotations

import contextvars
import json
import logging
import logging.handlers
import os
import re
from datetime import datetime

# Context variable for request tracing
request_id: contextvars.ContextVar[str] = contextvars.ContextVar("request_id", default="")


class SensitiveDataFilter(logging.Filter):
    """Filter that masks sensitive data (credentials + PII) in log records.

    Masks credentials (password, token, api_key, Bearer) and PII specific to
    Uzbekistan e-invoicing: 9-digit TINs, 14-digit PINFLs, and +998 phone numbers.

    When env var ``LOG_UNMASK_DEBUG=true`` is set AND the LogRecord's level is
    DEBUG, masking is skipped so developers can see raw payloads while
    troubleshooting. This flag MUST stay false in production.

    Perf: every log line was running through 6 compiled regexes even when
    no sensitive content was possibly present (a clear majority of records
    — INFO startup banners, metric ticks, error traces). The fast-path
    ``_SENSITIVE_HINTS`` substring check rejects ~80% of records without
    paying the regex cost. The hint set is derived from the regex bodies
    below and the lowercase form is checked because every pattern is
    case-insensitive on its keyword.
    """

    # Credential patterns (always masked)
    _CRED_PATTERNS = [
        (
            re.compile(
                r"(authorization|proxy-authorization|cookie|set-cookie)\s*[:=]\s*[^\r\n]+",
                re.IGNORECASE,
            ),
            r"\1=***",
        ),
        (
            re.compile(
                r"(x-telegram-initdata|tginitdata|tgwebappdata|access_?token|refresh_?token)"
                r"(?:\s*[:=]\s*|%3[dD])\S+",
                re.IGNORECASE,
            ),
            r"\1=***",
        ),
        (re.compile(r"(password|пароль|token|sid|api_key|secret)\s*[:=]\s*\S+", re.IGNORECASE), r"\1=***"),
        (re.compile(r'("(?:password|token|secret|api_key)")\s*:\s*"[^"]*"', re.IGNORECASE), r'\1: "***"'),
        # Python dict/repr form: str({"password": "x"}) renders single quotes
        # (``'password': 'x'``), which the double-quote JSON pattern above
        # misses. Non-string args (dicts, dataclasses) are str()'d into the
        # final message, so this catches the secret once it lands there.
        (re.compile(r"('(?:password|token|secret|api_key)')\s*:\s*'[^']*'", re.IGNORECASE), r"\1: '***'"),
        (re.compile(r"Bearer\s+\S+"), "Bearer ***"),
    ]

    # PII patterns. Phone first so it doesn't get partially eaten by the
    # 9-digit TIN regex (the 9 digits following +998 would otherwise match).
    # The phone pattern now accepts an OPTIONAL leading "+" to catch log lines
    # where the "+" was stripped by upstream code (e.g. ``tg_url.encode()``).
    # The TIN pattern is CONTEXT-AWARE: 9-digit runs are only masked when
    # preceded (within 10 chars) by a ``tin``/``ИНН``/``taxId`` keyword so we
    # don't mask e.g. order numbers, prices, or timestamps that happen to be
    # exactly 9 digits.
    _PII_PATTERNS = [
        (re.compile(r"\+?998\d{9}"), "***PHONE***"),
        (re.compile(r"(?<!\d)\d{14}(?!\d)"), "***PINFL***"),
        (
            re.compile(
                r"(?i)(tin|ИНН|inn|taxId)[^0-9]{0,10}(?<!\d)(\d{9})(?!\d)",
            ),
            r"\1=***TIN***",
        ),
    ]

    _ALL_PATTERNS = _CRED_PATTERNS + _PII_PATTERNS

    # Substring hints. If NONE of these are in the lowercased message,
    # there is nothing for the regexes to mask and we can skip the regex
    # pass entirely. Hints cover every keyword the regexes look for plus
    # the only context-free trigger (the ``998`` country prefix). PINFL
    # (bare 14-digit run) has no keyword anchor, so we keep a "long-digit-
    # run" fast-path check (any digit-only character).
    # The PII PINFL pattern is the only one without a keyword; we look for
    # any run of >=14 digits via the digit hint below.
    # All hints are pre-lowercased — checked against ``text.lower()``.
    # Cyrillic ``ИНН`` lowercases to ``инн`` (verified). We include both
    # ASCII ``inn`` and Cyrillic ``инн`` so logs in either alphabet trip
    # the fast-path correctly.
    _SENSITIVE_HINTS = (
        "password",
        "пароль",
        "token",
        "secret",
        "api_key",
        "sid",
        "bearer",
        "x-telegram-initdata",
        "tginitdata",
        "tgwebappdata",
        "accesstoken",
        "access_token",
        "refreshtoken",
        "refresh_token",
        "authorization",
        "proxy-authorization",
        "cookie",
        "set-cookie",
        "998",
        "tin",
        "inn",
        "инн",
        "taxid",
    )

    def __init__(self, unmask_debug: bool = False) -> None:
        super().__init__()
        self._unmask_debug = unmask_debug

    @staticmethod
    def _needs_mask(text: str) -> bool:
        """Cheap substring/digit screen before running the regex set.

        Returns ``True`` if the text *might* contain something a regex
        would match; ``False`` is a guarantee no regex can match.
        """
        if not text:
            return False
        # Lowercase ONCE for keyword matching. ``str.lower`` is C-level
        # and cheaper than running 4 case-insensitive regexes.
        lowered = text.lower()
        for hint in SensitiveDataFilter._SENSITIVE_HINTS:
            if hint in lowered:
                return True
        # PINFL (14-digit run) has no keyword. Detect any sufficiently
        # long digit run cheaply by scanning for >=14 consecutive digits.
        # ``isdigit`` per-char in a tight loop is still faster than
        # compiling/running the regex on non-matching text.
        run = 0
        for ch in text:
            if ch.isdigit():
                run += 1
                if run >= 14:
                    return True
            else:
                run = 0
        return False

    @staticmethod
    def _mask(text: str) -> str:
        # Fast-path: most log records contain no sensitive markers; skip
        # the full regex sweep when we can prove there's nothing to mask.
        if not SensitiveDataFilter._needs_mask(text):
            return text
        for pattern, replacement in SensitiveDataFilter._ALL_PATTERNS:
            text = pattern.sub(replacement, text)
        return text

    def filter(self, record: logging.LogRecord) -> bool:
        # Dev escape hatch: skip masking for DEBUG lines when explicitly enabled.
        if self._unmask_debug and record.levelno == logging.DEBUG:
            return True

        # Render the FINAL message (interpolating every arg, including
        # non-string args such as dicts / dataclasses / objects) and mask the
        # whole rendered string. Masking the interpolated result — not msg and
        # args separately — closes the bypass where a dict/object arg carrying
        # a secret was str()'d into the output *after* per-arg masking, e.g.
        # ``log.info("ctx=%s", {"password": "x"})`` (audit CORE-6). Clearing
        # ``args`` lets downstream formatters re-render the already-masked text
        # verbatim without re-interpolating the raw values.
        try:
            message = record.getMessage()
        except Exception:
            # Malformed format string / args: fall back to the raw template so
            # a broken log call can never surface an unmasked payload.
            message = str(record.msg)
        record.msg = self._mask(message)
        record.args = None
        return True


class _MaskSecretsInExceptionMixin:
    """Mixin that masks secrets in formatted tracebacks and stack info.

    ``SensitiveDataFilter`` masks the log *message*, but exception text is
    produced by the formatter (``formatException`` / ``formatStack``) and would
    otherwise reach the sink unmasked — a secret raised inside an exception
    (bad password in a connection string, token in an aiohttp error) leaks
    through the traceback (audit CORE-6b). Applied to every formatter used by
    :func:`setup_logging`.
    """

    def formatException(self, ei) -> str:  # type: ignore[override]
        return SensitiveDataFilter._mask(super().formatException(ei))  # type: ignore[misc]

    def formatStack(self, stack_info: str) -> str:  # type: ignore[override]
        return SensitiveDataFilter._mask(super().formatStack(stack_info))  # type: ignore[misc]


class TextFormatter(_MaskSecretsInExceptionMixin, logging.Formatter):
    """Plain-text formatter that masks secrets in tracebacks (non-JSON sinks)."""


class JsonFormatter(_MaskSecretsInExceptionMixin, logging.Formatter):
    """Structured JSON log formatter for production environments."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Include request_id if set
        req_id = request_id.get("")
        if req_id:
            log_entry["request_id"] = req_id

        # Include exception info if present
        if record.exc_info and record.exc_info[0] is not None:
            log_entry["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_entry, ensure_ascii=False)


def _prune_old_log_files(logs_folder: str, keep: int = 20) -> None:
    """Best-effort removal of stale ``bot_*.log`` files.

    A fresh timestamped log file (``bot_<ts>.log``) is created on every process
    restart; without pruning they accumulate unbounded and eventually pressure
    the disk (audit CORE-11). Keep the ``keep`` most-recent (by mtime) and drop
    the rest, including their RotatingFileHandler backups (``.log.N``). Fully
    best-effort — this must never raise and never block startup.
    """
    try:
        candidates = [
            os.path.join(logs_folder, name)
            for name in os.listdir(logs_folder)
            if name.startswith("bot_") and ".log" in name
        ]
        candidates.sort(key=os.path.getmtime, reverse=True)
        for stale in candidates[keep:]:
            try:
                os.remove(stale)
            except OSError:
                pass
    except OSError:
        pass


def setup_logging(logs_folder: str = "logs", json_output: bool = False, level: str = "INFO") -> None:
    """Setup JSON-like structured logging with rotation and sensitive data filtering."""
    os.makedirs(logs_folder, exist_ok=True)
    # Trim old per-restart log files before opening a new one (best-effort).
    _prune_old_log_files(logs_folder)

    log_filename = os.path.join(logs_folder, f"bot_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")

    # File handler with rotation: 10MB per file, 5 backups
    file_handler = logging.handlers.RotatingFileHandler(
        log_filename,
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )

    # Console handler
    console_handler = logging.StreamHandler()

    # Formatter
    if json_output:
        formatter: logging.Formatter = JsonFormatter(datefmt="%Y-%m-%dT%H:%M:%S")
    else:
        formatter = TextFormatter(
            "%(asctime)s | %(levelname)-8s | %(name)-20s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Sensitive data filter (credentials + PII).
    # LOG_UNMASK_DEBUG=true lets DEBUG-level records bypass masking (dev only).
    # Force-disabled in production so a stray env value can never leak secrets/PII
    # into prod logs regardless of how the container is configured.
    unmask_debug = os.getenv("LOG_UNMASK_DEBUG", "false").lower() in ("1", "true", "yes")
    if unmask_debug and os.getenv("APP_ENV", "").lower() == "prod":
        logging.getLogger("logging_config").warning(
            "LOG_UNMASK_DEBUG is ignored in production — sensitive-data masking stays on."
        )
        unmask_debug = False
    sensitive_filter = SensitiveDataFilter(unmask_debug=unmask_debug)
    file_handler.addFilter(sensitive_filter)
    console_handler.addFilter(sensitive_filter)

    # Root logger
    root = logging.getLogger()
    root.setLevel(getattr(logging, level, logging.INFO))
    root.addHandler(file_handler)
    root.addHandler(console_handler)

    # Quiet noisy loggers
    logging.getLogger("aiogram").setLevel(logging.INFO)
    logging.getLogger("aiohttp").setLevel(logging.WARNING)
    logging.getLogger("websockets").setLevel(logging.WARNING)
    logging.getLogger("alembic").setLevel(logging.INFO)
