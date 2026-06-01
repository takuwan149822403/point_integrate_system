"""認証フォーム向けの入力検証ユーティリティ。"""

from __future__ import annotations

import re

from .errors import ValidationError

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_PASSWORD_RE = re.compile(r"^(?=.*[A-Za-z])(?=.*\d).{8,}$")


def normalize_email(value: str | None) -> str:
    """メールアドレスを比較用に正規化する。"""

    return (value or "").strip().lower()


def validate_email(value: str | None) -> str:
    """メールアドレス形式を検証し、正規化済み文字列を返す。"""

    email = normalize_email(value)
    if not email:
        raise ValidationError("メールアドレスを入力してください。")
    if len(email) > 255 or not _EMAIL_RE.match(email):
        raise ValidationError("メールアドレスの形式が正しくありません。")
    return email


def validate_name(value: str | None) -> str:
    """表示名を検証する。"""

    name = (value or "").strip()
    if not name:
        raise ValidationError("名前を入力してください。")
    if len(name) > 120:
        raise ValidationError("名前は120文字以内で入力してください。")
    return name


def validate_password(value: str | None) -> str:
    """パスワードの最低要件を検証する。"""

    password = value or ""
    if not password:
        raise ValidationError("パスワードを入力してください。")
    if len(password) > 128:
        raise ValidationError("パスワードは128文字以内で入力してください。")
    if not _PASSWORD_RE.match(password):
        raise ValidationError("パスワードは8文字以上で、英字と数字を含めてください。")
    return password


def validate_password_confirmation(password: str | None, confirmation: str | None) -> None:
    """確認用パスワードとの一致を検証する。"""

    if (password or "") != (confirmation or ""):
        raise ValidationError("確認用パスワードが一致しません。")
