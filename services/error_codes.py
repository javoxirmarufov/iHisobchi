# coding: utf-8
"""Centralized error codes for user-facing error messages.

Each code follows the pattern ERR-{category}{number}:
    A = Auth, D = Document, X = External API, B = Business

Usage::

    from services.error_codes import ERR_AUTH_WRONG_PASSWORD, format_error
    await message.answer(format_error("Неверный пароль Didox", ERR_AUTH_WRONG_PASSWORD))
"""

from __future__ import annotations

# Auth errors
ERR_AUTH_WRONG_PASSWORD = "ERR-A01"
ERR_AUTH_RATE_LIMITED = "ERR-A02"
ERR_AUTH_API_DOWN = "ERR-A03"
ERR_AUTH_TOKEN_EXPIRED = "ERR-A04"
ERR_AUTH_COOLDOWN = "ERR-A05"
ERR_AUTH_NOT_REGISTERED = "ERR-A06"
DIDOX_USER_NOT_REGISTERED = "ERR-A07"
DIDOX_PARTNER_ROUTING = "ERR-A08"
DIDOX_NO_PERMISSION = "ERR-A09"

# In-bot Didox signup errors (ERR-A20..A26)
SIGNUP_ALREADY_REGISTERED = "ERR-A20"
SIGNUP_INVALID_EMAIL = "ERR-A21"
SIGNUP_INVALID_MOBILE = "ERR-A22"
SIGNUP_OFFER_NOT_ACCEPTED = "ERR-A23"
SIGNUP_SIGNATURE_FAILED = "ERR-A24"
SIGNUP_AGENT_OFFLINE = "ERR-A25"
SIGNUP_NO_EIMZO_CERT = "ERR-A26"

# Localised user-facing messages for the in-bot signup failure modes.
SIGNUP_ALREADY_REGISTERED_MESSAGES = {
    "ru": "Этот ИНН уже зарегистрирован в Didox. Введите пароль для входа.",
    "uz": "Bu STIR Didox tizimida ro‘yxatdan o‘tgan. Kirish uchun parolni kiriting.",
}

SIGNUP_INVALID_EMAIL_MESSAGES = {
    "ru": "Некорректный email. Пример: example@mail.uz",
    "uz": "Noto‘g‘ri email. Misol: example@mail.uz",
}

SIGNUP_INVALID_MOBILE_MESSAGES = {
    "ru": "Некорректный номер. Формат: 998XXXXXXXXX",
    "uz": "Noto‘g‘ri raqam. Format: 998XXXXXXXXX",
}

SIGNUP_OFFER_NOT_ACCEPTED_MESSAGES = {
    "ru": "Чтобы продолжить, примите оферту Didox.",
    "uz": "Davom etish uchun Didox ofertasini qabul qiling.",
}

SIGNUP_SIGNATURE_FAILED_MESSAGES = {
    "ru": "Не удалось получить подпись E-IMZO. Попробуйте снова или обратитесь в поддержку.",
    "uz": "E-IMZO imzosini olishning iloji bo‘lmadi. Qayta urinib ko‘ring yoki yordam xizmatiga murojaat qiling.",
}

SIGNUP_AGENT_OFFLINE_MESSAGES = {
    "ru": "Admin Agent не подключён. Запустите его на своём ПК.",
    "uz": "Admin Agent ulanmagan. Uni o‘z kompyuteringizda ishga tushiring.",
}

SIGNUP_NO_EIMZO_CERT_MESSAGES = {
    "ru": "У вас нет E-IMZO TIN-сертификата.",
    "uz": "Sizda E-IMZO STIR sertifikati yo‘q.",
}

# Localised user-facing messages for the new Didox auth failure modes.
# Keep the payload minimal — callers typically wrap with ``format_error``.
DIDOX_USER_NOT_REGISTERED_MESSAGES = {
    "ru": "Аккаунт Didox не найден. Зарегистрируйтесь на didox.uz или через бота.",
    "uz": "Didox akkauntingiz topilmadi. didox.uz saytida yoki bot orqali ro‘yxatdan o‘ting.",
}

DIDOX_PARTNER_ROUTING_MESSAGES = {
    "ru": "Временная ошибка маршрутизации Didox. Попробуйте позже.",
    "uz": "Didox marshrutizatsiyasida vaqtinchalik xatolik. Birozdan so‘ng qayta urinib ko‘ring.",
}

DIDOX_NO_PERMISSION_MESSAGES = {
    "ru": "У вас нет прав для входа в эту компанию Didox.",
    "uz": "Bu Didox kompaniyasiga kirish uchun ruxsatingiz yo‘q.",
}

# Document errors
ERR_DOC_CREATE_FAILED = "ERR-D01"
ERR_DOC_SIGN_FAILED = "ERR-D02"
ERR_DOC_SIGN_TIMEOUT = "ERR-D03"
ERR_DOC_NOT_FOUND = "ERR-D04"
ERR_DOC_PDF_FAILED = "ERR-D05"

# API errors
ERR_API_DIDOX = "ERR-X01"
ERR_API_EIMZO = "ERR-X02"
ERR_API_BANK = "ERR-X03"
ERR_API_TASNIF = "ERR-X04"
ERR_API_CIRCUIT_OPEN = "ERR-X05"

# Business errors
ERR_BIZ_NOT_FOUND = "ERR-B01"
ERR_BIZ_NO_TOKEN = "ERR-B02"


def format_error(message: str, code: str) -> str:
    """Format user-facing error message with error code.

    The code is rendered as monospace so users can quote it in support requests.
    """
    return f"{message}\n\n<code>[{code}]</code>"
