"""Flask request.form から認証入力を取り出す軽量フォーム。"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from .validators import (
    validate_email,
    validate_name,
    validate_password,
    validate_password_confirmation,
)


@dataclass(frozen=True)
class LoginForm:
    """ログインフォーム。"""

    email: str
    password: str

    @classmethod
    def from_mapping(cls, values: Mapping[str, str]) -> "LoginForm":
        """フォーム値を検証してログインフォームを生成する。"""

        email = validate_email(values.get("email"))
        password = values.get("password") or ""
        if not password:
            from .errors import ValidationError

            raise ValidationError("パスワードを入力してください。")
        return cls(email=email, password=password)


@dataclass(frozen=True)
class RegistrationForm:
    """ユーザー登録フォーム。"""

    name: str
    email: str
    password: str
    confirm_password: str

    @classmethod
    def from_mapping(cls, values: Mapping[str, str]) -> "RegistrationForm":
        """フォーム値を検証して登録フォームを生成する。"""

        name = validate_name(values.get("name"))
        email = validate_email(values.get("email"))
        password = validate_password(values.get("password"))
        confirm_password = values.get("confirm_password") or ""
        validate_password_confirmation(password, confirm_password)
        return cls(
            name=name,
            email=email,
            password=password,
            confirm_password=confirm_password,
        )
