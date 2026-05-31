from __future__ import annotations

from typing import Any, Generic, Iterable, TypeVar

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

ModelT = TypeVar('ModelT')


class RepositoryError(Exception):
    '''Repository層で発生した永続化エラーを表します。'''


class BaseRepository(Generic[ModelT]):
    '''SQLAlchemyモデル向けの基本Repositoryです。'''

    model_class: type[ModelT]

    def __init__(self, model_class: type[ModelT] | None = None) -> None:
        if model_class is not None:
            self.model_class = model_class
        if not hasattr(self, 'model_class'):
            raise RepositoryError('Repositoryの対象モデルが設定されていません。')

    def add(self, entity: ModelT, *, commit: bool = True) -> ModelT:
        '''エンティティを追加します。'''
        try:
            db.session.add(entity)
            if commit:
                db.session.commit()
            else:
                db.session.flush()
            return entity
        except SQLAlchemyError as exc:
            db.session.rollback()
            raise RepositoryError('データの保存に失敗しました。') from exc

    def create(self, *, commit: bool = True, **fields: Any) -> ModelT:
        '''モデルを生成して保存します。'''
        entity = self.model_class(**fields)
        return self.add(entity, commit=commit)

    def get_by_id(self, entity_id: int) -> ModelT | None:
        '''主キーで1件取得します。'''
        if not isinstance(entity_id, int) or entity_id <= 0:
            return None
        return db.session.get(self.model_class, entity_id)

    def list_all(self) -> list[ModelT]:
        '''全件を主キー昇順で取得します。'''
        return list(self.model_class.query.order_by(self.model_class.id.asc()).all())

    def find_by(self, **filters: Any) -> list[ModelT]:
        '''指定条件に一致するレコードを取得します。'''
        return list(self.model_class.query.filter_by(**filters).all())

    def first_by(self, **filters: Any) -> ModelT | None:
        '''指定条件に一致する最初のレコードを取得します。'''
        return self.model_class.query.filter_by(**filters).first()

    def update(self, entity: ModelT, *, commit: bool = True, **fields: Any) -> ModelT:
        '''既存エンティティの属性を更新します。'''
        for key, value in fields.items():
            if not hasattr(entity, key):
                raise RepositoryError(f'存在しない属性は更新できません: {key}')
            setattr(entity, key, value)
        try:
            if commit:
                db.session.commit()
            else:
                db.session.flush()
            return entity
        except SQLAlchemyError as exc:
            db.session.rollback()
            raise RepositoryError('データの更新に失敗しました。') from exc

    def delete(self, entity: ModelT, *, commit: bool = True) -> None:
        '''エンティティを削除します。'''
        try:
            db.session.delete(entity)
            if commit:
                db.session.commit()
            else:
                db.session.flush()
        except SQLAlchemyError as exc:
            db.session.rollback()
            raise RepositoryError('データの削除に失敗しました。') from exc

    def add_many(self, entities: Iterable[ModelT], *, commit: bool = True) -> list[ModelT]:
        '''複数エンティティを追加します。'''
        entity_list = list(entities)
        try:
            db.session.add_all(entity_list)
            if commit:
                db.session.commit()
            else:
                db.session.flush()
            return entity_list
        except SQLAlchemyError as exc:
            db.session.rollback()
            raise RepositoryError('複数データの保存に失敗しました。') from exc


class UserRepository(BaseRepository[User]):
    model_class = User

    def find_by_email(self, email: str) -> User | None:
        return self.first_by(email=email)


class PointAccountRepository(BaseRepository[PointAccount]):
    model_class = PointAccount

    def find_by_user_id(self, user_id: int) -> PointAccount | None:
        return self.first_by(user_id=user_id)


class PointTransactionRepository(BaseRepository[PointTransaction]):
    model_class = PointTransaction

    def list_by_user_id(self, user_id: int) -> list[PointTransaction]:
        return list(
            self.model_class.query.filter_by(user_id=user_id)
            .order_by(self.model_class.created_at.desc(), self.model_class.id.desc())
            .all()
        )


class CouponRepository(BaseRepository[Coupon]):
    model_class = Coupon

    def list_by_user_id(self, user_id: int) -> list[Coupon]:
        return self.find_by(user_id=user_id)


class RankRepository(BaseRepository[Rank]):
    model_class = Rank

    def list_by_user_id(self, user_id: int) -> list[Rank]:
        return self.find_by(user_id=user_id)


class OrderRepository(BaseRepository[Order]):
    model_class = Order

    def list_by_user_id(self, user_id: int) -> list[Order]:
        return self.find_by(user_id=user_id)


class PaymentRepository(BaseRepository[Payment]):
    model_class = Payment

    def list_by_user_id(self, user_id: int) -> list[Payment]:
        return self.find_by(user_id=user_id)


class NotificationRepository(BaseRepository[Notification]):
    model_class = Notification

    def list_by_user_id(self, user_id: int) -> list[Notification]:
        return list(
            self.model_class.query.filter_by(user_id=user_id)
            .order_by(self.model_class.created_at.desc(), self.model_class.id.desc())
            .all()
        )


class UserGroupRepository(BaseRepository[UserGroup]):
    model_class = UserGroup

    def list_by_owner_user_id(self, owner_user_id: int) -> list[UserGroup]:
        return self.find_by(owner_user_id=owner_user_id)


__all__ = [
    'RepositoryError',
    'UserRepository',
    'PointAccountRepository',
    'PointTransactionRepository',
    'CouponRepository',
    'RankRepository',
    'OrderRepository',
    'PaymentRepository',
    'NotificationRepository',
    'UserGroupRepository',
]
