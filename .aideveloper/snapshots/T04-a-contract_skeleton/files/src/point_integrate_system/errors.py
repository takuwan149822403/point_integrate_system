"""アプリケーション共通の例外定義。"""

from __future__ import annotations


class AppError(Exception):
    """画面へ返却可能なアプリケーション例外。"""

    status_code = 400

    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.message = message
        if status_code is not None:
            self.status_code = status_code


class AuthError(AppError):
    """認証・セッション関連の例外。"""

    status_code = 403


class RegistrationError(AuthError):
    """ユーザー登録の入力不備。"""

    status_code = 422


class LoginError(AuthError):
    """ログイン失敗。"""

    status_code = 401


class PermissionError(AuthError):
    """権限不足。"""

    status_code = 403


class ConflictError(AppError):
    """重複など競合状態。"""

    status_code = 409


class DomainServiceError(AppError):
    """業務サービス層の例外。"""

    status_code = 400


class PersistenceError(AppError):
    """永続化層の例外。"""

    status_code = 500


class ValidationError(AppError):
    """フォーム入力検証の例外。"""

    status_code = 422
