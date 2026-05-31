"""Repository層。

SQLAlchemyのdbセッションを直接扱う箇所をこのモジュールへ集約する。
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Generic, TypeVar

from sqlalchemy.exc import SQLAlchemyError

from .models import (
    Coupon,
    Notification,
    Order,
    Payment,
    PointAccount,
    PointTransaction,
    Rank,
    User,
    UserGroup,
    db,
)

ModelT = TypeVar("ModelT")


class RepositoryError(RuntimeError):
    """Repository処理で永続化に失敗した場合の例外。"""


class BaseRepository(Generic[ModelT]):
    """基本CRUD操作を提供するRepository基底クラス。"""

    model_class: type[ModelT]

    def __init__(self, model_class: type[ModelT] | None = None) -> None:
        if model_class is not None:
            self.model_class = model_class
        if not hasattr(self, "model_class"):
            raise RepositoryError("Repositoryの対象モデルが設定されていません。")

    def add(self, entity: ModelT, *, commit: bool = True) -> ModelT:
        """エンティティをセッションへ追加し、必要に応じてコミットする。"""
        db.session.add(entity)
        if commit:
            self.commit()
        return entity

    def create(self, *, commit: bool = True, **kwargs: object) -> ModelT:
        """キーワード引数からモデルを生成して保存する。"""
        entity = self.model_class(**kwargs)
        return self.add(entity, commit=commit)

    def get_by_id(self, entity_id: int) -> ModelT | None:
        """主キーで1件取得する。"""
        if not isinstance(entity_id, int) or entity_id <= 0:
            return None
        return db.session.get(self.model_class, entity_id)

    def list_all(self) -> list[ModelT]:
        """全件を主キー昇順で取得する。"""
        return list(self.model_class.query.order_by(self.model_class.id.asc()).all())

    def save(self, entity: ModelT) -> ModelT:
        """既存エンティティの変更をコミットする。"""
        db.session.add(entity)
        self.commit()
        return entity

    def delete(self, entity: ModelT, *, commit: bool = True) -> None:
        """エンティティを削除する。"""
        db.session.delete(entity)
        if commit:
            self.commit()

    def commit(self) -> None:
        """セッションをコミットし、失敗時はロールバックする。"""
        try:
            db.session.commit()
        except SQLAlchemyError as exc:
            db.session.rollback()
            raise RepositoryError("DB保存に失敗しました。") from exc

    def add_all(self, entities: Iterable[ModelT], *, commit: bool = True) -> list[ModelT]:
        """複数エンティティを追加する。"""
        entity_list = list(entities)
        db.session.add_all(entity_list)
        if commit:
            self.commit()
        return entity_list


class UserRepository(BaseRepository[User]):
    """User用Repository。"""

    model_class = User

    def find_by_email(self, email: str) -> User | None:
        """メールアドレスでユーザーを取得する。"""
        normalized_email = email.strip().lower()
        if not normalized_email:
            return None
        return User.query.filter_by(email=normalized_email).first()


class PointAccountRepository(BaseRepository[PointAccount]):
    """PointAccount用Repository。"""

    model_class = PointAccount

    def get_by_user_id(self, user_id: int) -> PointAccount | None:
        """ユーザーIDでポイント口座を取得する。"""
        if not isinstance(user_id, int) or user_id <= 0:
            return None
        return PointAccount.query.filter_by(user_id=user_id).first()


class PointTransactionRepository(BaseRepository[PointTransaction]):
    """PointTransaction用Repository。"""

    model_class = PointTransaction

    def list_by_user_id(self, user_id: int) -> list[PointTransaction]:
        """ユーザーIDでポイント履歴を作成日時昇順に取得する。"""
        if not isinstance(user_id, int) or user_id <= 0:
            return []
        return list(
            PointTransaction.query.filter_by(user_id=user_id)
            .order_by(PointTransaction.created_at.asc(), PointTransaction.id.asc())
            .all()
        )


class CouponRepository(BaseRepository[Coupon]):
    """Coupon用Repository。"""

    model_class = Coupon

    def list_by_user_id(self, user_id: int) -> list[Coupon]:
        """ユーザーIDでクーポンを取得する。"""
        if not isinstance(user_id, int) or user_id <= 0:
            return []
        return list(Coupon.query.filter_by(user_id=user_id).order_by(Coupon.id.asc()).all())


class RankRepository(BaseRepository[Rank]):
    """Rank用Repository。"""

    model_class = Rank

    def list_by_user_id(self, user_id: int) -> list[Rank]:
        """ユーザーIDでランクを取得する。"""
        if not isinstance(user_id, int) or user_id <= 0:
            return []
        return list(Rank.query.filter_by(user_id=user_id).order_by(Rank.id.asc()).all())


class OrderRepository(BaseRepository[Order]):
    """Order用Repository。"""

    model_class = Order

    def list_by_user_id(self, user_id: int) -> list[Order]:
        """ユーザーIDで注文・申請を取得する。"""
        if not isinstance(user_id, int) or user_id <= 0:
            return []
        return list(Order.query.filter_by(user_id=user_id).order_by(Order.id.asc()).all())


class PaymentRepository(BaseRepository[Payment]):
    """Payment用Repository。"""

    model_class = Payment

    def list_by_user_id(self, user_id: int) -> list[Payment]:
        """ユーザーIDで支払い・決済を取得する。"""
        if not isinstance(user_id, int) or user_id <= 0:
            return []
        return list(Payment.query.filter_by(user_id=user_id).order_by(Payment.id.asc()).all())


class NotificationRepository(BaseRepository[Notification]):
    """Notification用Repository。"""

    model_class = Notification

    def list_by_user_id(self, user_id: int) -> list[Notification]:
        """ユーザーIDで通知を作成日時昇順に取得する。"""
        if not isinstance(user_id, int) or user_id <= 0:
            return []
        return list(
            Notification.query.filter_by(user_id=user_id)
            .order_by(Notification.created_at.asc(), Notification.id.asc())
            .all()
        )


class UserGroupRepository(BaseRepository[UserGroup]):
    """UserGroup用Repository。"""

    model_class = UserGroup

    def list_by_owner_user_id(self, owner_user_id: int) -> list[UserGroup]:
        """所有者ユーザーIDでグループを取得する。"""
        if not isinstance(owner_user_id, int) or owner_user_id <= 0:
            return []
        return list(
            UserGroup.query.filter_by(owner_user_id=owner_user_id)
            .order_by(UserGroup.id.asc())
            .all()
        )
