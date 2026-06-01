"""認証とユーザー入口に関するサービス。"""

from __future__ import annotations

from copy import deepcopy
from threading import RLock
from typing import Any

from werkzeug.security import check_password_hash, generate_password_hash

from .errors import ConflictError, LoginError, PermissionError, RegistrationError
from .validators import normalize_email, validate_email, validate_name, validate_password


class AuthService:
    """ユーザー登録・ログインを扱うサービス。

    T03ではFlask test clientでのセッション制御を確実に確認できるよう、
    プロセス内の安全な開発用ストアを使用する。後続の永続化統合では、
    この公開メソッドの入出力を保ったままRepositoryへ委譲できる。
    """

    _lock = RLock()
    _users_by_email: dict[str, dict[str, Any]] = {}
    _users_by_id: dict[int, dict[str, Any]] = {}
    _next_id = 1
    _dev_seeded = False

    def __init__(self) -> None:
        self.seed_dev_user()

    @classmethod
    def reset_for_tests(cls) -> None:
        """テスト用にユーザーストアを初期化する。"""

        with cls._lock:
            cls._users_by_email = {}
            cls._users_by_id = {}
            cls._next_id = 1
            cls._dev_seeded = False
        cls().seed_dev_user()

    @classmethod
    def seed_dev_user(cls) -> None:
        """開発・テスト専用ユーザーを登録する。"""

        with cls._lock:
            if cls._dev_seeded:
                return
            email = normalize_email("dev.user@example.com")
            user = {
                "id": cls._next_id,
                "name": "開発ユーザー",
                "email": email,
                "password_hash": generate_password_hash("Password123!"),
                "is_active": True,
            }
            cls._users_by_email[email] = user
            cls._users_by_id[user["id"]] = user
            cls._next_id += 1
            cls._dev_seeded = True

    def register_user(self, name: str, email: str, password: str, confirm_password: str | None = None) -> dict[str, Any]:
        """ユーザーを登録して公開可能なユーザー辞書を返す。"""

        clean_name = validate_name(name)
        clean_email = validate_email(email)
        clean_password = validate_password(password)
        if confirm_password is not None and clean_password != confirm_password:
            raise RegistrationError("確認用パスワードが一致しません。")

        with self._lock:
            if clean_email in self._users_by_email:
                raise ConflictError("このメールアドレスは既に登録されています。")
            user = {
                "id": self._next_id,
                "name": clean_name,
                "email": clean_email,
                "password_hash": generate_password_hash(clean_password),
                "is_active": True,
            }
            self._users_by_email[clean_email] = user
            self._users_by_id[user["id"]] = user
            self.__class__._next_id += 1
            return self._public_user(user)

    def authenticate(self, email: str, password: str) -> dict[str, Any]:
        """メールアドレスとパスワードでログイン認証する。"""

        clean_email = validate_email(email)
        if not password:
            raise LoginError("メールアドレスまたはパスワードが正しくありません。")
        with self._lock:
            user = self._users_by_email.get(clean_email)
            if user is None or not check_password_hash(user["password_hash"], password):
                raise LoginError("メールアドレスまたはパスワードが正しくありません。")
            if not user.get("is_active", True):
                raise PermissionError("このユーザーは利用できません。")
            return self._public_user(user)

    def get_user(self, user_id: int | str | None) -> dict[str, Any] | None:
        """セッション中のユーザーIDからユーザーを取得する。"""

        if user_id is None:
            return None
        try:
            numeric_user_id = int(user_id)
        except (TypeError, ValueError):
            return None
        with self._lock:
            user = self._users_by_id.get(numeric_user_id)
            if user is None:
                return None
            return self._public_user(user)

    @staticmethod
    def _public_user(user: dict[str, Any]) -> dict[str, Any]:
        """パスワードハッシュを含まないユーザー情報へ変換する。"""

        public_user = deepcopy(user)
        public_user.pop("password_hash", None)
        return public_user


class DomainService:
    """後続タスク向けの業務サービス基底クラス。"""

    def health(self) -> dict[str, str]:
        """簡易ヘルス情報を返す。"""

        return {"status": "ok"}
